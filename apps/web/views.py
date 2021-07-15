from typing import Any, Dict

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, ListView, TemplateView
from django.views.generic.edit import UpdateView

import logging
from djpaddle.models import Plan

from config.settings.base import DJPADDLE_VENDOR_ID

from apps.billings import services as billing_services

from . import forms
from .models import BlogEntry, Lead, Page
from .providers import blog_entry as blog_entry_providers
from .providers import page as page_providers

# Create your views here.

logger = logging.getLogger(__name__)


class RedirectToLangPage:
    url_name = None

    def dispatch(self, request, *args, **kwargs):
        if not self.url_name:
            raise Exception("url_name attribute is required")

        kwargs_with_lang_code = kwargs | {"lang_code": request.LANGUAGE_CODE}

        if (
            not self.kwargs.get("lang_code")
            or self.kwargs.get("lang_code") != request.LANGUAGE_CODE
        ):
            return redirect(reverse(self.url_name, kwargs=kwargs_with_lang_code))

        return super().dispatch(request, *args, **kwargs_with_lang_code)


class RedirectToAppMixin:
    def dispatch(self, request, *args, **kwargs):
        host = request.META.get("HTTP_HOST", "")
        if settings.ENVIRONMENT == settings.LOCAL and "localhost" in host:
            is_subdomain = len(host.split(".")) > 1
        else:
            is_subdomain = len(host.split(".")) > 2

        if is_subdomain and self.request.user.is_authenticated:
            return redirect(reverse("webapp"))

        if is_subdomain and self.request.user.is_anonymous:
            return redirect(reverse("web:login"))

        return super().dispatch(request, *args, **kwargs)


class SoonTemplateView(RedirectToAppMixin, TemplateView):
    template_name = "pages/soon.html"


class CheckCompanyView(TemplateView):
    template_name = "auth/check_company.html"


class LoginView(FormView):
    form_class = forms.LoginForm
    template_name = "auth/login.html"
    success_url = "/app/"

    def dispatch(self, request, *args, **kwargs):
        if not self.request.company_code:
            return redirect(reverse("web:check-company"))

        if self.request.user.is_authenticated:
            return redirect(reverse("webapp"))

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        user = authenticate(self.request, email=email, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)

        form.add_error("password", _("Invalid user or password"))
        return super().form_invalid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return {"email": "viktor@hol.is", "password": "", **context}


class RegistrationView(TemplateView):
    template_name = "auth/signup.html"


class GetObjectByUUIDMixin:
    def get_object(self):
        return Lead.objects.get(secret=self.kwargs["pk"])


class SignUpStep1(FormView):
    template_name = "auth/signup/step1.html"
    form_class = forms.SignUpStep1Form
    success_url = reverse_lazy("web:signup-step-2")

    def form_valid(self, form):
        lead = Lead.objects.filter(email=form.cleaned_data.get("email")).first()

        if not lead:
            form.save()
        else:
            form = self.form_class(instance=lead)

        form.send_email(self.request)
        return super().form_valid(form)


class SignUpStep2(TemplateView):
    template_name = "auth/signup/step2.html"


class SignUpStep3(GetObjectByUUIDMixin, UpdateView):
    template_name = "auth/signup/step3.html"
    model = Lead
    form_class = forms.SignUpStep3Form

    def get_success_url(self, **kwargs):
        return reverse_lazy("web:signup-step-4", kwargs={"pk": self.kwargs["pk"]})


class SignUpStep4(GetObjectByUUIDMixin, UpdateView):
    template_name = "auth/signup/step4.html"
    model = Lead
    form_class = forms.SignUpStep4Form
    success_url = reverse_lazy("web:signup-step-5")

    def get_success_url(self, **kwargs):
        return reverse_lazy("web:signup-step-5", kwargs={"pk": self.kwargs["pk"]})


class SignUpStep5(GetObjectByUUIDMixin, UpdateView):
    template_name = "auth/signup/step5.html"
    model = Lead
    form_class = forms.SignUpStep5Form
    success_url = "/app"


def logout_view(request):
    logout(request)
    return redirect("webapp")


class HomeView(RedirectToAppMixin, RedirectToLangPage, TemplateView):
    template_name = "pages/home_v2.html"
    url_name = "web:home_with_lang"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_current_full_plan_subscriptions = (
            billing_services.get_total_current_full_plan_subscriptions() + 6
        )
        pending_full_subcscriptions = 100 - total_current_full_plan_subscriptions

        return context | {
            "PLANS": billing_services.get_paddle_plans_sorted_by_price(),
            "DJPADDLE_VENDOR_ID": settings.DJPADDLE_VENDOR_ID,
            "TOTAL_FULL_SUBSCRIPTIONS": total_current_full_plan_subscriptions,
            "PENDING_FULL_SUBSCRIPTIONS": pending_full_subcscriptions,
        }


class PageSingleView(RedirectToLangPage, TemplateView):
    template_name = "pages/page_single.html"
    url_name = "web:page-simple"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            page = page_providers.get_page_by_slug(slug=self.kwargs["slug"])
        except Page.DoesNotExist:
            raise Http404()

        return context | {"PAGE": page}


class BlogSingleView(TemplateView):
    template_name = "blog/blog_single.html"
    url_name = "web:blog-single"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            blog_entry = blog_entry_providers.get_blog_entry_by_slug(
                slug=self.kwargs["slug"]
            )
        except BlogEntry.DoesNotExist:
            raise Http404()

        return context | {
            "PAGE": blog_entry,
            "RELATED_POSTS": blog_entry.tags.similar_objects(),
        }


class BlogListView(RedirectToLangPage, ListView):
    template_name = "blog/blog_list.html"
    model = BlogEntry
    paginate_by = 6
    url_name = "web:blog-list"

    def get_queryset(self):
        return self.model.objects.filter(
            is_draft=False, lang=self.request.LANGUAGE_CODE
        ).order_by("-created")
