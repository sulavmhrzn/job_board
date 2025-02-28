from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import User
from apps.employers.models import EmployerProfile


@receiver(post_save, sender=User)
def create_employer_profile(sender, instance, created, **kwargs):
    if created:
        EmployerProfile.objects.create(user=instance, company_email=instance.email)
