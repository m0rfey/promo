from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class User(AbstractUser):
    username = models.CharField('username', max_length=150, blank=True, null=True)
    email = models.EmailField('email address', unique=True)
    bonus = models.ForeignKey('Bonus', on_delete=models.CASCADE, related_name='user')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


@receiver(pre_save, sender=User, dispatch_uid="bonus_create")
def bonus_create(sender, instance, **kwargs):
    instance.bonus = Bonus.objects.create(counter=0)


class FreeRegistration(models.Model):
    counter = models.IntegerField(default=5)


class Bonus(models.Model):
    counter = models.IntegerField(default=0)
