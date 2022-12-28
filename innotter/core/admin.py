from django.contrib import admin

from .models import *

class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_private')
    search_fields = ('owner', 'name', 'description')
    list_editable = ('is_private',)
    list_filter = ('is_private', 'tags')

class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'page', 'reply_to', 'created_at')
    search_fields = ('page', 'content')
    list_filter = ('page', 'created_at', 'updated_at')


admin.site.register(Tag)
admin.site.register(Page, PageAdmin)
admin.site.register(Post, PostAdmin)
