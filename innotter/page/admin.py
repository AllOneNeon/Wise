from django.contrib import admin

from .models import *

class PageAdmin(admin.ModelAdmin):
    display_lists = ('name', 'owner', 'is_private')
    search_fields = ('owner', 'name', 'description')
    list_editor = ('is_private',)
    list_filters = ('is_private', 'tags')

admin.site.register(Tag)
admin.site.register(Page, PageAdmin)
