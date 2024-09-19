from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PersonRegistrationForm, PersonLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse_lazy

from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)
from .forms import CustomPasswordResetForm, SetPasswordForm


def registration(request):
    if request.method == 'POST':
        form = PersonRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration was successful!')
            return redirect('login')
        else:
            messages.error(request, 'There are some errors while registration. Check your forms.')
    else:
        form = PersonRegistrationForm()
    
    return render(request, 'user/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = PersonLoginForm(request.POST)
        if form.is_valid():
            if form.login_user(request):
                messages.success(request, 'Zalogowano pomyślnie.')
                return redirect('mainPage')
            else:
                messages.error(request, 'Błąd logowania.')
    else:
        form = PersonLoginForm()

    return render(request, 'user/login.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'user/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'user/password_reset_email.html'  
    subject_template_name = 'user/password_reset_subject.txt'  


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'user/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordForm
    template_name = 'user/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'user/password_reset_complete.html'


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def mainPage(request):
    return render(request, 'user/mainPage.html')