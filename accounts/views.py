from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse

from News_Site import settings
from accounts.forms import UserLoginForm, UserRegisterForm
from accounts.models import UserProfile
from news import views


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request=request, user=user)
                if request.GET.get("next"):
                    return HttpResponseRedirect(request.GET.get("next"))
                return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
            else:
                context = {
                    "error_massage": "کاربری با این مشخصات یافت نشد"
                }
            return render(request, "accounts/login.html", context)
    else:
        form = UserLoginForm()
    return render(request=request, template_name='accounts/login.html', context={'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'], cd['email'], cd['password'])
            UserProfile.objects.create(user=user)
            login(request=request, user=user)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = UserRegisterForm()
    return render(request=request, template_name='accounts/sign-in.html', context={'form': form})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse(views.home_view))
