from django.core.management import BaseCommand
from main.services import send_email, checking_and_send_emails


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Handler was called by hands")
        checking_and_send_emails()
