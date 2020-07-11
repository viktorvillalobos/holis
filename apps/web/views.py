import logging

from apps.core import models as core_models
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
    success_url = '/app/'

    def get_company(self, pk):
        return core_models.Company.objects.filter(pk=pk).first()

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        company = form.cleaned_data['company']

        company = self.get_company(company)

        if not company:
            form.add_error('company', _('Company does not exists'))
            return super().form_invalid(form)

        user = authenticate(
            self.request, company_id=company.id, email=email, password=password
        )

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)

        form.add_error('password', _('Invalid user or password'))
        return super().form_invalid(form)


class RegistrationView(TemplateView):
    template_name = "auth/signup.html"
