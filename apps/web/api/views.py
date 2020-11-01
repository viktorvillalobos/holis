from django.conf import settings
from django.core.mail import send_mail
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

import logging
import requests

from . import serializers

logger = logging.getLogger(__name__)


class GetEarlyAccessAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.GetEarlyAccessSerializer

    def post(self, request):
        self.serializer = self.serializer_class(data=request.data)
        self.serializer.is_valid(raise_exception=True)

        email, email_sent = self.send_email()
        self.to_email_relay(email)
        return Response({"email": email, "sent": email_sent}, status=status.HTTP_200_OK)

    def to_email_relay(self, email):
        if settings.DEBUG or not settings.EMAIL_RELAY_TOKEN:
            return

        URL = "https://holis.ipzmarketing.com/api/v1/subscribers"

        headers = {"X-AUTH-TOKEN": settings.EMAIL_RELAY_TOKEN}
        payload = {"status": "active", "email": email}
        resp = requests.post(URL, json=payload, headers=headers)
        logger.info(resp.content)

    def send_email(self):
        email = self.serializer.validated_data["email"]
        origin = self.serializer.validated_data["origin"]

        content = f"""
            email: {email}
            origin: {origin}
        """

        try:
            send_mail(
                "Get Early Access",
                content,
                "early@mail.holis.chat",
                ["sales@holis.chat"],
                fail_silently=False,
            )
            logger.info(f"Sending early access email lead: {email} from {origin}")
            return email, True
        except Exception:
            logger.info(f"failed to send email early {email} from {origin}")
            return email, False
