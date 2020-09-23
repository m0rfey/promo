from django import forms
from django.contrib.auth import get_user_model

from invite.models import Invite

User = get_user_model()


class CreateInviteCode(forms.ModelForm):
    owner = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Invite
        fields = ('code', 'owner')
