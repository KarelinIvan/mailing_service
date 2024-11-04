from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing_service.models import Mailing


class MailingListView(ListView):
    model = Mailing
    context_object_name = 'mailings'


class MailingDetailView(DetailView):
    model = Mailing
    context_object_name = 'mailing'


class MailingCreateView(CreateView):
    model = Mailing
    fields = ['start_datetime', 'periodicity', 'message', 'clients']
    success_url = reverse_lazy('mailing_list')


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['start_datetime', 'periodicity', 'message', 'clients']
    success_url = reverse_lazy('mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    fields = ['start_datetime', 'periodicity', 'message', 'clients']
    success_url = reverse_lazy('mailing_list')
