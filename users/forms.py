from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
import logging
from users.models import User

logger = logging.getLogger(__name__)


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class EmailAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        logger.info(f"Попытка входа в систему с помощью электронной почты: {email}")

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                logger.warning("Не удалось выполнить проверку подлинности для электронной почты: %s", email)
                raise forms.ValidationError("Неверный адрес электронной почты или пароль.")
        return self.cleaned_data
