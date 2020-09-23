from django.forms import model_to_dict

from .models import Invite, Used


def use_invite(code, user):
    invite = Invite.objects.get(code=code)
    u = Used.objects.create(user_id=user.id)
    invite.used.add(u)
    return invite


def get_user_invite(user_id):
    return Invite.objects.filter(used__user_id=user_id)
