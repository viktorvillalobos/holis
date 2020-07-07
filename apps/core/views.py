from django.contrib.auth.decorators import login_required
from django.shortcuts import render


#@login_required
def webapp(request):
    return render(request, "core/webapp.html")
