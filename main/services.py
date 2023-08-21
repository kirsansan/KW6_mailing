import smtplib
from random import randint

from django import template
from django.core.mail import send_mail
from django.conf import settings

from config.config import EMAIL_SENDING_SIMULATION_MODE
from main.models import Client, MailingMessage, MailingList, MailingListLogs

register = template.Library()


def checking_and_send_emails():
    # all_email = []
    # for client in Client.objects.all():
    #     all_email.append(str(client.email))

    for mailing in MailingList.objects.filter(status=MailingList.ACTIVE):
        print(mailing)
        # print("mailing", mailing, mailing.__dir__(), mailing.client_id.all())
        # if mailing.status == MailingList.ACTIVE:
        for client in mailing.client_id.all():
            print(client)
            #     print(client.email)
            if mailing.periodicity == mailing.ONCE:
                if mailing.mailinglistlogs_set.filter(client=client.pk).exists():
                    print("status:", mailing.mailinglistlogs_set.filter(client=client.pk).last().status)
            elif mailing.periodicity == mailing.DAILY:
                if mailing.mailinglistlogs_set.filter(client=client.pk).exists():
                    print("status:", mailing.mailinglistlogs_set.filter(client=client.pk).last().status)
            elif mailing.periodicity == mailing.WEEKLY:
                if mailing.mailinglistlogs_set.filter(client=client.pk).exists():
                    print("status:", mailing.mailinglistlogs_set.filter(client=client.pk).last().status)
            else:  # it is mailing.MONTHLY
                if mailing.mailinglistlogs_set.filter(client=client.pk).exists():
                    print("status:", mailing.mailinglistlogs_set.filter(client=client.pk).last().status)

            # filtered_message = mailing.message
            # message = MailingMessage.objects.filter(subject=filtered_message)
            # for m in message:
            #     send_mail(
            #         subject=m.subject,
            #         message=m.body,
            #         from_email=settings.EMAIL_HOST_USER,
            #         recipient_list=[*all_email],
            #     )
            #     status_list = []
            #     server_response = {
            #         'sending': MailingList.objects.get(pk=mailing.id),
            #         'status': MailingListLogs.SENT,
            #         'response': [*all_email]}
            #     status_list.append(MailingListLogs(**server_response))
            #     MailingListLogs.objects.bulk_create(status_list)
            #     if mailing.periodicity == MailingList.ONCE:
            #         mailing.status = MailingList.COMPLETED
            #         mailing.save()
            #     else:
            #         mailing.status = MailingList.ACTIVE
            #         mailing.save()


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
        if chaos > 80:
            new_log_string.status = new_log_string.ERROR
            new_log_string.response = 'email sending simulation error'
        else:
            new_log_string.status = new_log_string.SENT
            new_log_string.response = 'simulation sending is Ok'

    # new_log_string = MailingListLogs()
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


def check_time(time, periodicity):
    """"""

    return True
