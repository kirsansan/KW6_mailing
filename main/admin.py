from django.contrib import admin

from main.models import MailingList, MailingMessage, Client


# для продуктов выведите в список id, название, цену и категорию.
@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'message', 'start', )
    list_filter = ('start',)
    search_fields = ('message', 'start',)

