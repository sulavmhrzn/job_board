from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            "Welcome to Job Board",
            f"Welcome {instance.first_name} {instance.last_name} to Job Board",
            "no-reply@jobboard.com",
            [instance.email],
        )
