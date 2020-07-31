import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

logger = logging.getLogger(__name__)


@login_required
def webapp(request):
    host = request.META["HTTP_HOST"]
    is_subdomain = len(host.split('.')) > 2

    if not is_subdomain and request.user.is_anonymous:
        return redirect(reverse("web:login"))

    if not is_subdomain and request.user.is_authenticated:
        scheme_url = request.is_secure() and "https" or "http"
        url = f"{scheme_url}://{request.user.company.code}.{host}/app/"
        return HttpResponseRedirect(url)

    return render(request, "core/webapp.html")
