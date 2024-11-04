from django.core.management import BaseCommand

from mailing_service.tasks import send_due_mailings


class Command(BaseCommand):
    help = "Запуск рассылок вручную"

    def handle(self, *args, **options):
        self.stdout.write("Запуск отправки рассылок...")
        send_due_mailings()
        self.stdout.write(self.style.SUCCESS("Отправка рассылок завершена."))
