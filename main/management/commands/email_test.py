from django.core.management import BaseCommand
from main.models import MailingList, Client, MailingListLogs
from main.services import mail_testing


class Command(BaseCommand):

    def handle(self, *args, **options):
        mail_testing()
