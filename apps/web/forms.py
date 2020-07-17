import logging
from django import forms
from django.core.mail import send_mail
from apps.web.models import Lead


logger = logging.getLogger(__name__)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()


class SignUpStep1(forms.ModelForm):
    class Meta:
        fields = ["email"]
        model = Lead

    def send_email(self, request):
        logger.info("SENDING EMAIL")
        root = request.build_absolute_uri('/')[:-1].strip("/")
        logger.info(self.instance.secret)
        content = f"""
            Activate: {root}/signup/step3/{self.instance.secret}/
        """

        try:
            send_mail(
                "Welcome to Holis.",
                content,
                self.instance.email,
                [self.instance.email],
                fail_silently=False,
            )
            logger.info(
                f"Sending early access email lead: {self.instance.email}"
            )
        except Exception as ex:
            logger.info(f"failed to send email early {self.instance.email}")
            logger.info(str(ex))
