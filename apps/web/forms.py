from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.postgres.forms import SimpleArrayField
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

import logging

from apps.core.context import models as core_models
from apps.core.context.uc.company import CreateCompany
from apps.users.context.uc import CreateUser
from apps.web.models import Lead

logger = logging.getLogger(__name__)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()


class SignUpStep1Form(forms.ModelForm):
    class Meta:
        fields = ["email"]
        model = Lead

    def send_email(self, request):
        root = request.build_absolute_uri("/")[:-1].strip("/")
        content = f"""
            Activate: {root}/signup/step3/{self.instance.secret}/
        """

        try:
            send_mail(
                "Welcome to Holis.",
                content,
                "welcome@hol.is",
                [self.instance.email],
                fail_silently=False,
            )
            logger.info(f"Sending early access email lead: {self.instance.email}")
        except Exception as ex:
            logger.info(f"failed to send email early {self.instance.email}")
            logger.info(str(ex))


class SignUpStep3Form(forms.ModelForm):
    class Meta:
        fields = ["company_name", "company_code"]
        model = Lead

    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data["company_code"]:
            cleaned_data["company_code"] = (
                cleaned_data["company_name"].strip().lower().replace(" ", "-")
            )

        if core_models.Company.objects.filter(
            code=cleaned_data["company_code"]
        ).exists():
            self.add_error(
                "company_code", _("This company code is already used, please use other")
            )
        return cleaned_data


class SignUpStep4Form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ["name", "position", "avatar", "password"]
        model = Lead

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error(
                "password", _("password and confirm_password does not match")
            )

        cleaned_data["password"] = make_password(password)
        return cleaned_data


class SignUpStep5Form(forms.ModelForm):
    invitations = SimpleArrayField(forms.CharField(max_length=100), required=False)

    class Meta:
        fields = ["invitations"]
        model = Lead

    def save(self):
        lead = super().save()
        create_company = CreateCompany(lead.company_name, lead.company_code, lead.email)
        company = create_company.execute()

        create_user = CreateUser(
            company,
            lead.email,
            lead.password,
            name=lead.name,
            avatar=lead.avatar,
            position=lead.position,
        )
        create_user.execute()

        return lead
