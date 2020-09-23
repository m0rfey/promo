from django.core.mail import EmailMultiAlternatives
from .models import Bonus, User
from invite.models import Invite, Used
from configs.celery import app


@app.task(bind=True)
def send_email(self, subject, body, from_email, recipient_list, html, fail_silently=False):
    msg = EmailMultiAlternatives(subject, body, from_email, recipient_list)
    if html:
        msg.attach_alternative(html, "text/html")
    msg.send(fail_silently)


@app.task
def calculate_bonuses(user_id):
    invites = Invite.objects.filter(used__user_id=user_id)
    for invite in invites:
        invite.owner.bonus.counter += 1
        invite.owner.bonus.save(update_fields=['counter'])
        calculate_bonuses.delay(invite.owner.id)
