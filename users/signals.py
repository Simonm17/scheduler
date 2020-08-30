from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile

""" Create a signal so that a Profile object is made whenever a user signs up.
    Update the Profile model object whenever a User updates their account.
    IMPORTANT: add the ready() function to apps.py to register the signals.
    https://docs.djangoproject.com/en/3.1/ref/applications/#django.apps.AppConfig.ready
"""


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print(f'---- PROFILE CREATED ---')


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    print(f'---- PROFILE UPDATED ---')