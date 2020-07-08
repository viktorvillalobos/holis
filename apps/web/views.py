from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

# Create your views here.


class SoonTemplateView(TemplateView):
    template_name = "pages/soon.html"

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.GET.get("no_redirect") and request.user.is_authenticated:
    #         return redirect(reverse('webapp'))

    #     return super().dispatch(request, *args, **kwargs)


class CheckCompanyView(TemplateView):
    template_name = "auth/check_company.html"


class LoginView(TemplateView):
    template_name = "auth/login.html"


class RegistrationView(TemplateView):
    template_name = "auth/signup.html"
