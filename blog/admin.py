from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug')
