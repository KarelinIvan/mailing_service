from django.contrib import admin

from mailing_service.models import Client, Message, Mailing, Attempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment')
    search_fields = ('email', 'full_name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('topic',)
    search_fields = ('topic',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_datetime', 'periodicity', 'status', 'message')
    list_filter = ('periodicity', 'status')
    filter_horizontal = ('clients',)


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing', 'attempt_datetime', 'status')
    list_filter = ('status',)
    search_fields = ('mailing__id',)

