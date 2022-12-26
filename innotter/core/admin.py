from django.contrib import admin

from .models import Page, Post, Subscriber

class PageAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'name', ]

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'page', ]

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['subscriber', 'follower', 'follow_requests', ]


admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Page, PageAdmin)
