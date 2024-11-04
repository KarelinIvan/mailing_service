import logging
import smtplib

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from mailing_service.models import Mailing, Attempt

logger = logging.getLogger(__name__)


def send_due_mailings():
    timezone.get_current_timezone()
    current_datetime = timezone.now()

    mailings = Mailing.objects.filter(
        start_datetime__lte=current_datetime,
        status__in=['created', 'started']
    )

    for mailing in mailings:
        try:
            send_mail(
                subject=mailing.message.topic,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email for client in mailing.clients.all()],
                fail_silently=False,
            )

            Attempt.objects.create(
                mailing=mailing,
                attempt_datetime=current_datetime,
                status='successful',
                server_response='Письмо отправлено успешно'
            )

            logger.info(f"Рассылка {mailing.id} отправлена успешно.")

            if mailing.periodicity == 'once':
                mailing.status = 'completed'
            else:
                mailing.status = 'started'
                mailing.start_datetime = calculate_next_send_time(mailing, current_datetime)
            mailing.save()

        except smtplib.SMTPException as e:
            Attempt.objects.create(
                mailing=mailing,
                attempt_datetime=current_datetime,
                status='failed',
                server_response=str(e)
            )

            logger.error(f"Ошибка при отправке рассылки {mailing.id}: {e}")

            mailing.status = 'started'
            mailing.save()

        except Exception as e:
            Attempt.objects.create(
                mailing=mailing,
                attempt_datetime=current_datetime,
                status='failed',
                server_response=str(e)
            )

            logger.error(f"Неизвестная ошибка при отправке рассылки {mailing.id}: {e}")

            mailing.status = 'started'
            mailing.save()


def calculate_next_send_time(mailing, last_send_time):
    if mailing.periodicity == 'daily':
        return last_send_time + timezone.timedelta(days=1)
    elif mailing.periodicity == 'weekly':
        return last_send_time + timezone.timedelta(weeks=1)
    elif mailing.periodicity == 'monthly':
        return last_send_time + timezone.timedelta(days=30)
    else:
        return last_send_time
