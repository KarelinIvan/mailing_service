from django.contrib.auth import login, logout
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, FormView
from rest_framework.authtoken.models import Token

from users.forms import UserRegisterForm, EmailAuthenticationForm, User
from users.services import send_registrations_email


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('mailing_service:mailing_list')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'Пользователь с таким email уже существует')
            return self.form_invalid(form)

        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        send_registrations_email(user)
        Token.objects.get_or_create(user=user)

        return response


class LoginView(FormView):
    form_class = EmailAuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('mailing_service:mailing_list')

    def form_valid(self, form):
        user = form.user_cache
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('users:login')


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))
