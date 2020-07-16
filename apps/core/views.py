import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

logger = logging.getLogger(__name__)


@login_required
def webapp(request):
    host = request.META["HTTP_HOST"].split(".")[0]

    if host == "holis":
        return redirect(reverse("web:login"))

    return render(request, "core/webapp.html")
