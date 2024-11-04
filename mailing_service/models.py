from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    comment = models.TextField(**NULLABLE)

    class Meta:
        verbose_name = "Клиент сервиса"
        verbose_name_plural = "Клиенты сервиса"

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Message(models.Model):
    topic = models.CharField(max_length=200, verbose_name="Тема")
    body = models.TextField()

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.topic


class Mailing(models.Model):
    """
    PERIODICITY_CHOICES, STATUS_CHOICES - наборы значении для полей periodicity и status соответственно
    """

    PERIODICITY_CHOICES = [
        ('once', 'Однократная'),
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ]

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_datetime = models.DateTimeField(default=timezone.now, verbose_name='Дата и время первой рассылки')
    periodicity = models.CharField(max_length=10, choices=PERIODICITY_CHOICES, default='once',
                                   verbose_name='Периодичность')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name='Статус рассылки')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    clients = models.ManyToManyField(Client, related_name='mailings', verbose_name='Клиент сервиса')

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return f"Рассылка: {self.start_datetime}, {self.periodicity}, {self.status}, {self.message}, {self.clients}"


class Attempt(models.Model):
    STATUS_CHOICES = [
        ('successful', 'Успешно'),
        ('failed', 'Не успешно'),
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts', verbose_name='Попытка')
    attempt_datetime = models.DateTimeField(default=timezone.now,
                                            verbose_name='Дата и время попытки отправки рассылки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    server_response = models.TextField(**NULLABLE)

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"

    def __str__(self):
        return f"Попытка: {self.mailing}, {self.attempt_datetime}, {self.status}, {self.server_response}"
