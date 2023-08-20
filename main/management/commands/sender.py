from django.core.management import BaseCommand

from main.models import MailingList, Client, MailingListLogs
from main.services import send_email


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Handler was called by hands")
        send_email()
