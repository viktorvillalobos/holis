import logging

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, TemplateView
from django.views.generic.edit import UpdateView

from apps.web import forms
from apps.web.models import Lead

# Create your views here.

logger = logging.getLogger(__name__)


class RedirectToAppMixin:
    def dispatch(self, request, *args, **kwargs):
        host = request.META.get("HTTP_HOST", "")
        is_subdomain = len(host.split(".")) > 2

        if is_subdomain and self.request.user.is_authenticated:
            return redirect(reverse("webapp"))

        if not is_subdomain and self.request.user.is_authenticated:
            return self.redirect_from_subdomain(host)

        if is_subdomain and self.request.user.is_anonymous:
            return redirect(reverse("web:login"))

        return super().dispatch(request, *args, **kwargs)

    def redirect_from_subdomain(self, host):
        scheme_url = self.request.is_secure() and "https" or "http"
        url = f"{scheme_url}://{self.request.user.company.code}.{host}/app/"
        return HttpResponseRedirect(url)


class SoonTemplateView(RedirectToAppMixin, TemplateView):
    template_name = "pages/soon.html"


class PWAView(TemplateView):
    template_name = "pages/soon.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            host = request.META.get("HTTP_HOST", "")
            scheme_url = request.is_secure() and "https" or "http"
            url = f"{scheme_url}://{self.request.user.company.code}.{host}/app/"
            return HttpResponseRedirect(url)

        return redirect(reverse("web:check-company"))


class CheckCompanyView(TemplateView):
    template_name = "auth/check_company.html"


class LoginView(FormView):
    form_class = forms.LoginForm
    template_name = "auth/login.html"
    success_url = "/app/"

    def dispatch(self, request, *args, **kwargs):
        if not self.request.company:
            return redirect(reverse("web:check-company"))

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
