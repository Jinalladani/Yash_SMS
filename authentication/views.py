from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import views as auth_views

from authentication.forms import SignUpForm
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.
class SignUp(View):

    def get(self, request):
        context = {}
        registration_form = SignUpForm()
        context['registration_form'] = registration_form
        return render(request, "authentication/registration.html", context)

    def post(self, request):
        context = {}
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
        else:
            context['registration_form'] = form
            return render(request, 'authentication/registration.html', context)