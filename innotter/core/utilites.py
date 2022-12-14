from .models import Like, Subscriber
from user.models import User
from .models import Post, Page
from django.db.models import F

#likes
def add_like(obj, user):
    if not Like.objects.filter(user=user, post=obj):
        Like.objects.create(user=user, post=obj)
        Post.objects.filter(pk=obj.id).update(total_likes=F('total_likes')+1)

def remove_like(obj, user):
    if Like.objects.filter(user=user, post=obj):
        Like.objects.filter(user=user, post=obj).delete()
        Post.objects.filter(pk=obj.id).update(total_likes=F('total_likes')-1)

def is_fan(obj, user):
    if not user.is_authenticated:
        return False
    likes = Like.objects.filter(user=user, post=obj)
    return likes.exists()

def get_fans(obj):
    return User.objects.filter(likes__post=obj)


#subscribes
def add_subscription(obj, user):
    if user.is_staff:
        subscription, is_created = Subscriber.objects.get_or_create(
            subscriber=user, follower=obj)
        return subscription
    elif user.is_authenticated and Page.objects.filter(id=obj.id, is_private=False):
        subscription, is_created = Subscriber.objects.get_or_create(
            subscriber=user, follower=obj)
        return subscription
    elif user.is_authenticated and Page.objects.filter(id=obj.id, is_private=True):
        subscription, is_created = Subscriber.objects.get_or_create(
            subscriber=user, follow_requests=obj)
        return subscription

def confirm_subscription_everybody(obj, user):
    if user.is_authenticated and Page.objects.filter(owner=user).exists():
        follow_requests = User.objects.filter(subscribers__follow_requests=obj)
        for one_user in follow_requests:
            subscription = Subscriber.objects.filter(subscriber=one_user).update(follower=obj, follow_requests=None)
            return subscription

def remove_subscription(obj, user):
    if user.is_authenticated and Page.objects.filter(id=obj.id, owner=user).exists():
        Subscriber.objects.filter(follower=obj).delete()
    elif user.is_authenticated:
        if Subscriber.objects.filter(subscriber=user, follower=obj).exists():
            Subscriber.objects.filter(subscriber=user, follower=obj).delete()

def get_follow_requests(obj):
    return User.objects.filter(subscribers__follow_requests=obj)

def get_subscribers(obj):
    return User.objects.filter(subscribers__follower=obj)

def is_subscriber(obj, user):
    if not user.is_authenticated:
        return False
    subscriber = Subscriber.objects.filter(subscriber=user, follower=obj)
    return subscriber.exists()

def is_follow_requests(obj, user):
    if not user.is_authenticated:
        return False
    subscriber = Subscriber.objects.filter(
        subscriber=user, follow_requests=obj)
    return subscriber.exists()