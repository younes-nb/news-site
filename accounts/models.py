from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="كاربر", related_name='profile')

    def __str__(self):
        return self.user.username
