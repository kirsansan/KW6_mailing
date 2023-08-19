from django.db import models
from django.utils.datetime_safe import datetime

from KW6_mailing import settings

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='first_name', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='last_name', **NULLABLE)
    email = models.EmailField(max_length=150, verbose_name='email')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='creator')
    is_active = models.BooleanField(default=True, verbose_name='is_active')

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ('last_name',)


class MailingMessage(models.Model):
    subject = models.CharField(max_length=200, verbose_name='subject')
    body = models.TextField(verbose_name='body')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='creation time')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='creator')

    def __str__(self):
        return f'{self.subject} at {self.created_time}'

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'


class MailingList(models.Model):
    ONCE = 'onetime'
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

    PERIODICITY = [
        (ONCE, 'onetime'),
        (DAILY, 'daily'),
        (WEEKLY, 'weekly'),
        (MONTHLY, 'monthly'),
    ]

    CREATED = 'was created'
    COMPLETED = 'was ended'
    ACTIVE = 'is active'

    SELECT_STATUS = [
        (CREATED, 'was created'),
        (COMPLETED, 'was ended'),
        (ACTIVE, 'active'),
    ]

    client_id = models.ManyToManyField(Client, verbose_name='client id')
    message = models.ForeignKey(MailingMessage, on_delete=models.CASCADE, verbose_name='message')
    time = models.TimeField(default=datetime.now, verbose_name='time')
    start = models.DateTimeField(default=datetime.now, verbose_name='start time')
    finish = models.DateTimeField(default=datetime.now, verbose_name='finish time')
    periodicity = models.CharField(max_length=150, choices=PERIODICITY, verbose_name='periodicity')
    status = models.CharField(max_length=100, default='was created', choices=SELECT_STATUS, verbose_name='status')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='creator')

    def __str__(self):
        return f"{self.message.subject} have to start from {self.start} every {self.periodicity}"

    class Meta:
        verbose_name = 'mailing list'
        verbose_name_plural = 'mailing lists'


class MailingListLogs(models.Model):
    SENT = 'was sent'
    ERROR = 'sending error'

    STATUS = (
        (SENT, 'sent'),
        (ERROR, 'sending error'),
    )

    mailing_list_id = models.ForeignKey(MailingList, on_delete=models.CASCADE, verbose_name='mailing list id')
    send_time = models.DateTimeField(auto_now_add=True, verbose_name='send time')
    status = models.CharField(choices=STATUS, verbose_name='status')
    response = models.TextField(**NULLABLE, verbose_name='response from server')

    def __str__(self):
        return f'{self.mailing_list_id.message.subject} was processed: {self.send_time}'

    class Meta:
        verbose_name = 'mailing effort'
        verbose_name_plural = 'mailing efforts'
