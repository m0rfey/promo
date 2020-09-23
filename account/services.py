from django.contrib.auth import get_user_model

User = get_user_model()


def get_user_by_email(email):
    return User.objects.filter(email=email).first()


def get_user_by_id(user_id):
    return User.objects.get(id=user_id)


def confirm_account(email):
    user = get_user_by_email(email)
    if user is not None:
        user.is_active = True
        user.save(update_fields=['is_active'])
    return user
