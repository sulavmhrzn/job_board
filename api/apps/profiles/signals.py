from apps.accounts.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import JobSeekerProfile


@receiver(post_save, sender=User)
def create_job_seeker_profile(sender, instance, created, **kwargs):
    if created and instance.is_job_seeker():
        JobSeekerProfile.objects.create(user=instance)
