from django.utils import timezone
from .models import Page
from user.models import User

#page
def is_page_unblocked(unblock_date):
    return timezone.now() >= unblock_date

def add_follow_requests_to_request_data(request_data, follow_requests):
    # taking all the User's ids
    follow_requests = list(follow_requests.values_list('pk', flat=True))
    # adding them to request data
    request_data.update({'follow_requests': follow_requests})
    return request_data

def user_is_in_page_follow_requests_or_followers(user, page):
    return page.follow_requests.filter(id=user.pk).exists() or page.followers.filter(id=user.pk).exists()

def add_user_to_page_follow_requests(user, page):
    page.follow_requests.add(user)

def add_user_to_page_followers(user, page):
    page.followers.add(user)

#post
def add_like_to_post(page_id, post):
    page = Page.objects.get(pk=page_id)
    page.liked_posts.add(post)
    post.pages_that_liked.add(page)
    page.save()
    post.save()


def user_is_able_to_see_the_post(user, post):
    page = Page.objects.get(pk=post.page.id)
    return (not page.is_private) or (page.owner == user) or (user.role == User.Roles.ADMIN) or\
           (user.role == User.Roles.MODERATOR) or (user.id in page.followers)


def user_is_page_owner(user, page_id):
    page = Page.objects.get(id=page_id)
    return page.owner == user


def foreign_page(user, page_id):
    page = Page.objects.get(pk=page_id)
    return page.owner != user
