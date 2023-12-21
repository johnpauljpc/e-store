from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from .forms import SignupForm, LoginForm

# Create your views here.
class SignupView(View):
    def get(self, request, *args, **kwargs):
        form = SignupForm()
        context = {
            "form":form
        }
        return render(request, "users\signup.html", context)
    
    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        context = {
            "form":form
        }
        if form.is_valid():
            u = form.save(commit=False)
            u.save()
            
            try:
                login(request, u)
                messages.success(request, f"account successfully created for <b>{u.first_name}</b>")
                return redirect(f"{settings.LOGIN_REDIRECT_URL}")
            except:
                messages.success(request, f"account successfully created for <b>{u.first_name}</b> please login")
                return redirect(f"{settings.LOGIN_URL}")


        return render(request, "users\signup.html", context)
signup_view = SignupView.as_view()


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {
            "form":form
        }
        if request.GET.get('next'):
            messages.info(request, f'To continue, please <b>login</b>!')
        else:
            messages.info(request, 'Hi there, welcome back! Please login')
        return render(request, "users\login.html", context)
    
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        context = {
            "form":form
        }
        if form.is_valid():
            user_email = form.cleaned_data["email"]
            password = form.cleaned_data.get("password",)
            user = authenticate(email=user_email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, <b>{ user.first_name }.</b> Thanks for logging in.")
                if 'next' in request.POST:
                    return redirect(request.POST['next'])
                else:
                    return redirect(f"{settings.LOGIN_REDIRECT_URL}")
            else:
                messages.error(request, "your credentials are not valid!")
        return render(request, "users\login.html", context)
    
login_view = LoginView.as_view()

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out!")
    return redirect(f"{settings.LOGOUT_REDIRECT_URL}")