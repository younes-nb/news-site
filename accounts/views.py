from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse

from News_Site import settings
from news import views


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if request.GET.get("next"):
                return HttpResponseRedirect(request.GET.get("next"))
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        else:
            context = {
                "error_massage": "کاربری با این مشخصات یافت نشد"
            }
            return render(request, "accounts/login.html", context)
    else:
        return render(request, "accounts/login.html", {})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse(views.home_view))
