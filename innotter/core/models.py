from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Page(models.Model):
    name = models.CharField(max_length=80, unique=True)
    uuid = models.UUIDField(max_length=30, unique=True)  # example:3422b448-2460-4fd2-9183-8000de6f8343
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='tags', blank=True)
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField('user.User', related_name='followers', null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField('user.User', related_name='follow_requests', null=True, blank=True)
    liked_posts = models.ManyToManyField('core.Post', related_name='liked_posts', null=True, blank=True)
    unblock_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

class Post(models.Model):
    page = models.ForeignKey('core.Page', on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=180)
    reply_to = models.ForeignKey('core.Post', on_delete=models.SET_NULL, null=True, related_name='replies', blank=True)
    pages_that_liked = models.ManyToManyField('core.Page', related_name='pages_that_liked', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content