import logging

from apps.core import models as core_models
from django.urls import reverse
from django.shortcuts import redirect
from apps.web.forms import LoginForm
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, TemplateView
from django.http import HttpResponseRedirect

# Create your views here.

logger = logging.getLogger(__name__)


class RedirectToAppMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            # return redirect(reverse("webapp"))
            host = request.META.get('HTTP_HOST', '')
            scheme_url = request.is_secure() and "https" or "http"
            url = f"{scheme_url}://{self.request.user.company.code}.{host}/app/"
            return HttpResponseRedirect(url)

        return super().dispatch(request, *args, **kwargs)


class SoonTemplateView(RedirectToAppMixin, TemplateView):
    template_name = "pages/soon.html"


class CheckCompanyView(TemplateView):
    template_name = "auth/check_company.html"


class LoginView(FormView):
    form_class = LoginForm
    template_name = "auth/login.html"
    success_url = "/app/"

    def dispatch(self, request, *args, **kwargs):
        if not self.request.company:
            return redirect(reverse("web:check-company"))

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        user = authenticate(self.request, email=email, password=password,)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)

        form.add_error("password", _("Invalid user or password"))
        return super().form_invalid(form)


class RegistrationView(TemplateView):
    template_name = "auth/signup.html"
