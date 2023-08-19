from django.contrib import admin

from main.models import Mailing


# для продуктов выведите в список id, название, цену и категорию.
@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', )
    list_filter = ('title',)
    search_fields = ('title', 'text',)

