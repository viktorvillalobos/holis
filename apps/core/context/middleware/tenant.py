import django
from django.conf import settings
from django.http import Http404

import logging

from ..middleware.utils import remove_www
from ..models import Company

logger = logging.getLogger(__name__)


class HolisTenantMiddleware(django.utils.deprecation.MiddlewareMixin):
    TENANT_NOT_FOUND_EXCEPTION = Http404
    TENANT_MODEL = Company

    def hostname_from_request(self, request):
        """
        Extracts hostname from request.
        Used for custom requests filtering.
        By default removes the request"s port and common prefixes.
        """
        return remove_www(request.get_host().split(":")[0]).lower()

    def get_hostname_and_subdomain(self, request):
        hostname = self.hostname_from_request(request)
        if settings.ENVIRONMENT is settings.LOCAL and "localhost" in hostname:
            return hostname, len(hostname.split(".")) > 1

        return hostname, len(hostname.split(".")) > 2

    def process_request(self, request):
        request.hostname, request.is_subdomain = self.get_hostname_and_subdomain(
            request
        )

        if request.is_subdomain:
            domain_code = request.hostname.split(".")[0]
        else:
            domain_code = None

        request.company_code = domain_code

        # The user is not logged
        if not request.user.is_authenticated:
            request.company = None
            request.company_id = None
            return

        # The user is logged but not in a subdomain app
        if not request.is_subdomain:
            request.company = request.user.company
            request.company_id = request.user.company_id
            return

        # The user is in a valid application subdomain
        user_is_in_correct_subdomain = (
            request.is_subdomain
            and request.user.is_authenticated
            and request.user.company.code == domain_code
        )

        if not user_is_in_correct_subdomain:
            raise Http404

        tenant = request.user.company
        request.company = tenant
        request.company_id = tenant.id

        logger.info(f"TENANT: {request.company_code}")
