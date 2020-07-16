import logging
from django import forms
from apps.web.models import Lead


logger = logging.getLogger(__name__)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()


class SignUpStep1(forms.ModelForm):
    class Meta:
        fields = ["email"]
        model = Lead

    def send_email(self):
        logger.info("SENDING EMAIL")
