from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore

from mailing_service.tasks import send_due_mailings


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')

    scheduler.add_job(
        send_due_mailings,
        trigger=IntervalTrigger(minutes=1),
        id='send_due_mailings',
        max_instances=1,
        replace_existing=True
    )
    scheduler.start()
