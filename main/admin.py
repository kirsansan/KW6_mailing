from django.contrib import admin

from main.models import MailingList, MailingMessage, Client, MailingListLogs


# для продуктов выведите в список id, название, цену и категорию.
@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'message', 'start',)
    list_filter = ('start',)
    search_fields = ('message', 'start',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'creator', 'is_active',)


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_time',)


@admin.register(MailingListLogs)
class MailingListLogsAdmin(admin.ModelAdmin):
    list_display = ('mailing_list_id', 'send_time', 'status',)
