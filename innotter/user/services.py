import datetime

import jwt
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

import innotter.settings
from core.models import Page
from .models import RefreshToken



def unblock_all_users_pages(user):
    unblock_date = timezone.now()
    Page.objects.filter(owner=user).update(unblock_date=unblock_date)


def block_all_users_pages(user):
    unblock_date = timezone.make_aware(timezone.datetime.max, timezone.get_default_timezone())
    Page.objects.filter(owner=user).update(unblock_date=unblock_date)


def generate_access_token(user):
    token = jwt.encode({
        'username': user.username,
        'iat': datetime.datetime.utcnow(),
        'nbf': datetime.datetime.utcnow() + datetime.timedelta(minutes=-5),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }, innotter.settings.SECRET_KEY)
    return token


def generate_refresh_token():
    refresh_token = jwt.encode({
        'iat': datetime.datetime.utcnow(),
        'nbf': datetime.datetime.utcnow() + datetime.timedelta(minutes=-5),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }, innotter.settings.SECRET_KEY)
    return refresh_token


def get_refresh_token_obj(refresh_token):
    try:
        old_token = RefreshToken.objects.get(refresh_token=refresh_token)
    except ObjectDoesNotExist:
        return None
    return old_token


def set_refresh_token(refresh_token, user):
    refresh_token = RefreshToken(user=user, refresh_token=refresh_token,
                                 exp_time=innotter.settings.CUSTOM_JWT['REFRESH_TOKEN_LIFETIME_MODEL'])
    refresh_token.save()


def check_and_update_refresh_token(refresh_token):
    old_token = get_refresh_token_obj(refresh_token)
    if old_token:
        # checks if refresh_token is still works
        if timezone.now() - datetime.timedelta(days=old_token.exp_time) > old_token.created_at:
            return None
        new_access_token = generate_access_token(old_token.user)
        new_refresh_token = generate_refresh_token()
        set_refresh_token(new_refresh_token, old_token.user)
        old_token.delete()
        return {innotter.settings.CUSTOM_JWT['AUTH_COOKIE']: new_access_token,
                innotter.settings.CUSTOM_JWT['AUTH_COOKIE_REFRESH']: new_refresh_token}