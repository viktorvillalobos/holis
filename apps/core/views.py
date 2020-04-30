from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def webapp(request):
    return render(request, "core/webapp.html")
