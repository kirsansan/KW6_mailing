import smtplib
from random import randint

from django import template
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta

from django.utils import timezone

from config.config import EMAIL_SENDING_SIMULATION_MODE
from main.models import Client, MailingMessage, MailingList, MailingListLogs

register = template.Library()


def checking_and_send_emails():
    """ for all mailing check timings and active status
        also check for needing to send mailing
            if it's need - try to send and write result is log database"""
    print("Start checking at", datetime.now(timezone.get_current_timezone()))
    for mailing in MailingList.objects.filter(status=MailingList.ACTIVE):
        print(">>>See on mailing:", mailing)
        # your time has not yet come
        if mailing.start > datetime.now(timezone.get_current_timezone()):
            continue
        # your time is over (finished)
        if mailing.finish < datetime.now(timezone.get_current_timezone()):
            print("your time is over")
            mailing.status = mailing.COMPLETED
            mailing.save()
            continue
        # on this step start and finish timing has already ok - we will try to check logs
        for client in mailing.client_id.all():
            print(">", client)
            #     print(client.email)
            if mailing.periodicity == mailing.ONCE:
                if mailing.mailinglistlogs_set.filter(client=client.pk).exists():
                    if mailing.mailinglistlogs_set.filter(client=client.pk).last().status == 'was sent':
                        continue
                send_one_email(mailing, client)
            else:  # it is mailing.MONTHLY WEEKLY DAILY
                if mailing.mailinglistlogs_set.filter(client=client.pk).exists():
                    last_update = mailing.mailinglistlogs_set.filter(client=client.pk).last()
                    if last_update.status == 'was sent':
                        print('this  mailing was sent, need checking timing for resending')
                        if not checking_time(mailing, last_update):
                            continue
                send_one_email(mailing, client)



def send_one_email(mailing: MailingList, client: Client) -> bool:
    """ send mail and write result to log table (MailingListLogs)
        in EMAIL_SENDING_SIMULATION_MODE=True this func gives error with a 20 percent chance """
    new_log_string = MailingListLogs()
    new_log_string.client = client
    new_log_string.mailing_list_id = mailing

    if not EMAIL_SENDING_SIMULATION_MODE:
        try:
            send_status = send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email],
                fail_silently=False
            )
            if send_status == 1:
                new_log_string.status = new_log_string.SENT
                new_log_string.response = "Ok"
            else:
                new_log_string.status = new_log_string.ERROR
                new_log_string.response = "Unknown error"
        except smtplib.SMTPException as e:
            print("e", e, e.strerror)
            new_log_string.status = new_log_string.ERROR
            new_log_string.response = e
        finally:
            pass
    else:
        chaos = randint(0, 100)
        if chaos > 80:     # simulate errors
            new_log_string.status = new_log_string.ERROR
            new_log_string.response = 'email sending simulation error'
        else:
            new_log_string.status = new_log_string.SENT
            new_log_string.response = 'simulation sending is Ok'

    # new_log_string = MailingListLogs()
    new_log_string.send_time = datetime.now(timezone.get_current_timezone())
    new_log_string.save()
    if new_log_string.status == new_log_string.SENT:
        return True
    return False


def mail_testing():
    """for test using command line like as
    python manage.py email_test
    """
    mailing = MailingList.objects.latest()
    print("TESTING FOR:", mailing, "WITH ", mailing.client_id.latest())
    print("test mailing result =", send_one_email(mailing, mailing.client_id.latest()))


def checking_time(mailing: MailingList, last: MailingListLogs) -> bool:
    """calculate timing """
    hours_before_the_next = 24
    if mailing.status is mailing.WEEKLY:
        hours_before_the_next *= 7
    if mailing.status is mailing.MONTHLY:
        hours_before_the_next *= 7*30
    print("checking time with", datetime.now(timezone.get_current_timezone()) - timedelta(hours=hours_before_the_next) )
    if last.send_time < datetime.now(timezone.get_current_timezone()) - timedelta(hours=hours_before_the_next):
        return True
    else:
        return False
