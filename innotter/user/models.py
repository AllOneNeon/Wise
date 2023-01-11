import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
import jwt

from innotter.settings import SECRET_KEY


class User(AbstractUser):
    class Roles(models.TextChoices):
       USER = 'user'
       MODERATOR = 'moderator'
       ADMIN = 'admin'

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices)
    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)
   
   #  @property
   #  def token(self):
   #     return self._generate_jwt_token()

   #  def get_full_name(self):
   #     return self.username

   #  def get_short_name(self):
   #     return self.username

   #  def _generate_jwt_token(self):
   #     dt = datetime.now() + datetime.timedelta(days=30)

   #     token = jwt.encode(
   #          {
   #          'id': self.pk,
   #          'exp': dt.utcfromtimestamp(dt.timestamp())
   #          },
   #          SECRET_KEY, algorithm='HS256'
   #      )
   #     return token