from django.contrib import admin
from django.urls import path
from .views import Registrations, confirm_email, Profile

app_name = 'account'
urlpatterns = [
    path('registrations/', Registrations.as_view(), name='registrations'),
    path('profile/<int:user_id>/', Profile.as_view(), name='profile'),
    path('<str:email>/', confirm_email, name='confirm_email'),
]
