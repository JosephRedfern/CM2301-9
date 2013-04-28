from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model


@receiver(post_save, sender=get_user_model())
def start_traceroute(sender, instance, created, **kwargs):
    if created:
        print "SET PERMISSIONS"