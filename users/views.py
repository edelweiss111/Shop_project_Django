import random
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail

from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.shortcuts import redirect
from config.settings import EMAIL_HOST_USER
from users.forms import RegisterForm, UserForm
from users.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required


class LoginUserView(LoginView):
    """Контроллер страницы входа"""
    template_name = 'users/login.html'


class LogoutUserView(LogoutView):
    """Контроллер выхода из аккаунта"""
    pass


class RegisterUserView(SuccessMessageMixin, CreateView):
    """Контроллер страницы регистрации"""
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def get_success_message(self, cleaned_data):
        """Сообщение на страницу входа"""
        return 'Вам на почту отправлено письмо, для прохождения верификации перейдите по ссылку в письме'

    def form_valid(self, form):
        """Верификация по ссылке через почту"""
        new_user = form.save(commit=False)
        code = ''.join(random.sample('0123456789', 5))
        new_user.verify_code = code
        new_user.is_active = False
        new_user.save()

        send_mail(
            subject='Верификация',
            message=f'Перейдите по ссылке для верификации: http://127.0.0.1:8000/users/verification/{code}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[new_user.email],
            fail_silently=False,
        )
        self.object = new_user
        return redirect(self.get_success_url())


def verification(request, code):
    """Контроллер подтверждения верификации"""
    user = User.objects.filter(verify_code=code).first()
    if user:
        user.is_active = True
        user.verify_code = None  # опционально, чтобы код нельзя было использовать повторно
        user.save()
        messages.success(request, 'Почта подтверждена! Теперь вы можете войти.')
    else:
        messages.error(request, 'Неверная или устаревшая ссылка верификации.')
    return redirect(reverse('users:login'))


class UserUpdateView(UpdateView):
    """Контроллер страницы редактирования профиля"""
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """Отключение необходимости получения pk"""
        return self.request.user


@login_required
def generate_password(request):
    """Контроллер смены пароля и отправка нового сгенерированного пароля на почту"""
    if not request.user.email:
        messages.error(request, 'У вашего аккаунта не указан email.')
        return redirect(reverse('users:profile'))

    new_password = User.objects.make_random_password()
    sent_count = send_mail(
        subject='Смена пароля',
        message=f'Ваш новый пароль для авторизации: {new_password}',
        from_email=EMAIL_HOST_USER,
        recipient_list=[request.user.email],
        fail_silently=False,
    )

    if sent_count:
        request.user.set_password(new_password)
        request.user.save()
        messages.success(request, 'Вам на почту отправлено письмо с новым паролем для вашего аккаунта')
    else:
        messages.error(request, 'Не удалось отправить письмо. Попробуйте позже.')

    return redirect(reverse('users:login'))
