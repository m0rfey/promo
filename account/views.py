from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import CreateView

from invite.forms import CreateInviteCode
from invite.services import get_user_invite
from . import services
from .tasks import send_email

from account.forms import RegistrationsForm

User = get_user_model()


class Registrations(CreateView):
    template_name = 'account/registrations.html'
    queryset = User.objects.all()
    form_class = RegistrationsForm
    success_url = '/'

    def form_valid(self, form):
        self.object = super().form_valid(form)
        link = f'http://127.0.0.1:8000/account/{form.instance.email}/'
        html = render_to_string('account/confirm_email.html', {'link': link})
        send_email.delay(
            subject='Confirm email',
            body='',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[form.instance.email],
            fail_silently=False,
            html=html
        )
        return self.object


def confirm_email(request, email):
    user = services.confirm_account(email)
    if user is not None:
        return HttpResponseRedirect(reverse('account:profile', kwargs={'user_id': user.id}))
    return HttpResponseRedirect('/')


class Profile(CreateView):
    template_name = 'account/profile.html'
    queryset = User.objects.all()
    form_class = CreateInviteCode

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        self.object = services.get_user_by_id(self.kwargs.get('user_id'))
        kwargs['form'] = self.form_class(initial={"owner": self.object})
        context = super().get_context_data(**kwargs)
        context['invite'] = self.object.invite.all()
        context['used_invite'] = self.object.invite.all()
        context['users'] = get_user_invite(self.object.id)
        context['bonus'] = self.object.bonus.counter
        return context



