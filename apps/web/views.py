import logging

from apps.core import models as core_models
from django.urls import reverse
from django.shortcuts import redirect
from apps.web.forms import LoginForm
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, TemplateView

# Create your views here.

logger = logging.getLogger(__name__)


class SoonTemplateView(TemplateView):
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
