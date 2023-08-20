from django import template
from django.core.mail import send_mail
from django.conf import settings
from main.models import Client, MailingMessage, MailingList, MailingListLogs

register = template.Library()


def send_email():
    # all_email = []
    # for client in Client.objects.all():
    #     all_email.append(str(client.email))

    for mailing in MailingList.objects.filter(status=MailingList.ACTIVE):
        #print("mailing", mailing, mailing.__dir__(), mailing.client_id.all())
        # if mailing.status == MailingList.ACTIVE:
        for client in mailing.client_id.all():
            print(client)
        #     print(client.email)





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

def check_time():
    """"""
    return True