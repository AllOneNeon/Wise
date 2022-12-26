from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import jwt
from innotter.settings import SECRET_KEY


class User(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices, default=Roles.USER)
    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)
    followed_pages = models.ManyToManyField('core.Page', related_name='followed_pages', null=True, blank=True)
    requested_pages = models.ManyToManyField('core.Page', related_name='requested_pages', null=True, blank=True)



# class UserManager(BaseUserManager):
#     """Creates and saves a User with the given email, date of
#     birth and password."""
#     def create_user(self, username, email, password=None):
#         if username is None:
#             raise TypeError('Users must have a username.')

#         if email is None:
#             raise TypeError('Users must have an email address.')
#         user = self.model(username=username, email=self.normalize_email(email))
#         user.set_password(password)
#         user.save()
#         return user
#     def create_superuser(self, username, email, password):
#         """Creates and saves a superuser with the given email, date of
#         birth and password."""
#         if password is None:
#             raise TypeError('Superusers must have a password.')
#         user = self.create_user(username, email, password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save()
#         return user

    # username = models.CharField(db_index=True, max_length=255, unique=True)
    # email = models.EmailField(db_index=True, unique=True)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']
    # objects = UserManager()

    # def __str__(self):
    #     return self.email

    # @property
    # def token(self):
    #     return self._generate_jwt_token()

    # def get_full_name(self):
    #     return self.username

    # def get_short_name(self):
    #     return self.username

    # def _generate_jwt_token(self):
    #     dt = datetime.now() + datetime.timedelta(days=30)

    #     token = jwt.encode(
    #             {
    #                     'id': self.pk,
    #                     'exp': dt.utcfromtimestamp(dt.timestamp())
    #             },
    #             SECRET_KEY, algorithm='HS256'
    #     )
    #     return token
