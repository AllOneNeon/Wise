from django.db import models
import uuid
from user.models import User

class Page(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='pages')
    name = models.CharField(max_length=80)
    description = models.TextField()
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, related_name='tags')
    image = models.FileField(max_length=30, null=True, blank=True)
    is_private = models.BooleanField(default=False)
    count_followers = models.IntegerField(default=0)
    count_follow_requests = models.IntegerField(default=0)
    unblock_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

class Post(models.Model):
    page = models.ForeignKey('Page', on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=180)
    reply_to = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_likes = models.IntegerField(default=0)

class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='like_post', on_delete=models.CASCADE)

class Subscriber(models.Model):
    subscriber = models.ForeignKey(User, related_name='subscribers', on_delete=models.CASCADE)
    follower = models.ForeignKey('Page', related_name='followers', on_delete=models.CASCADE, blank=True, null=True,)
    follow_requests = models.ForeignKey('Page', related_name='follow_requests', on_delete=models.CASCADE, blank=True, null=True)

