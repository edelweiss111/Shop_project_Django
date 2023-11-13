import random

from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail

from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.shortcuts import render, redirect
from config.settings import EMAIL_HOST_USER
from users.forms import UserForm
from users.models import User


class LoginUserView(LoginView):
    template_name = 'users/login.html'


class LogoutUserView(LogoutView):
    pass


class RegisterUserView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:verify')
    template_name = 'users/register.html'

    def form_valid(self, form):
        new_user = form.save()
        code = ''.join(random.sample('0123456789', 5))
        new_user.verify_code = code
        new_user.is_active = False
        send_mail(
            'Верификация',
            f'Перейдите по ссылке для верификации: http://127.0.0.1:8000/users/verification/{code}',
            EMAIL_HOST_USER,
            [new_user.email]
        )
        return super().form_valid(form)


class Verify(TemplateView):
    template_name = 'users/verify.html'


def verification(request, code):
    user = User.objects.get(verify_code=code)
    user.is_active = True
    user.save()
    return redirect('/users')
