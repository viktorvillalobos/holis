import django
import logging
from django.conf import settings
from django.core.exceptions import DisallowedHost
from django.db import connection
from django.http import Http404
from apps.core.middleware.utils import remove_www
from apps.core.models import Company


logger = logging.getLogger(__name__)


class HolisTenantMiddleware(django.utils.deprecation.MiddlewareMixin):
    TENANT_NOT_FOUND_EXCEPTION = Http404

    def get_tenant(self, model, hostname, request):
        return Company.objects.get(code=hostname)

    def hostname_from_request(self, request):
        """ Extracts hostname from request. Used for custom requests filtering.
            By default removes the request"s port and common prefixes.
        """
        return remove_www(request.get_host().split(":")[0]).lower()

    def has_subdomain(self, request):
        hostname = self.hostname_from_request(request)
        return len(hostname.split('.')) >= 2

    def process_request(self, request):
        hostname = self.hostname_from_request(request)
        is_subdomain = len(hostname.split('.')) > 2

        code = hostname.split(".")[0]
        TenantModel = Company

        if not is_subdomain:
            request.company = None
            return

        logger.info("TENANT")
        logger.info(code)

        logger.info("user")
        logger.info(request.user)

        logger.info("company")
        logger.info(request.user.company)

        if request.user.company.code != code:
            raise Http404

        try:
            # get_tenant must be implemented by extending this class.
            tenant = self.get_tenant(TenantModel, code, request)
            assert isinstance(tenant, TenantModel)
        except TenantModel.DoesNotExist:
            raise self.TENANT_NOT_FOUND_EXCEPTION(
                "No tenant for {!r}".format(request.get_host())
            )
        except AssertionError:
            raise self.TENANT_NOT_FOUND_EXCEPTION(
                "Invalid tenant {!r}".format(request.tenant)
            )

        request.company = tenant
        logger.info(f"TENANT: {request.company}")
