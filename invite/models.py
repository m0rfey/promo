import random
import string

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Used(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='used_invite')


class Invite(models.Model):
    code = models.CharField(max_length=15, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invite')
    created_date = models.DateTimeField(auto_now_add=True)
    used = models.ManyToManyField(Used, related_name='invite')

    def __str__(self):
        return f'code={self.code}, owner={self.owner_id}, created={self.created_date}'

    @staticmethod
    def get_code():
        sequence = list(string.ascii_letters + string.digits)
        code = ""
        while len(code) < 15:
            code = code + str(random.choice(sequence))
        return code

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.code is None:
            self.code = self.get_code()
        super().save(force_insert, force_update, using, update_fields)

