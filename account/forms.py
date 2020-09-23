from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied, ValidationError

from invite import services as inv_services
from .models import FreeRegistration
from . import services
from .tasks import calculate_bonuses

User = get_user_model()


class RegistrationsForm(forms.ModelForm):
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=128, widget=forms.PasswordInput())
    invite_code = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise ValidationError('password not match')
        cleaned_data['password'] = make_password(password)
        return cleaned_data

    def save(self, commit=True):
        cd = self.cleaned_data
        free_reg = FreeRegistration.objects.latest('id')
        if free_reg.counter > 0 and len(cd['invite_code']) == 0:
            obj = super().save(commit=commit)
            free_reg.counter -= 1
            free_reg.save(update_fields=['counter'])
            return obj
        else:
            if len(cd['invite_code']) > 0:
                obj = super().save(commit=commit)
                inv_services.use_invite(self.cleaned_data['invite_code'],
                                        services.get_user_by_email(self.cleaned_data['email']))
                calculate_bonuses.delay(obj.id)
                return obj
            raise PermissionDenied('Invite code is mandatory')
