from django.core.mail import send_mail
from config import settings
from users.models import User


def send_registrations_email(user: User):
    send_mail(
        'Благодарю за регистрацию!',
        f'{user.username}! Спасибо за то, что решили воспользоваться данным приложением!',
        settings.EMAIL_HOST_USER,
        [user.email]
    )