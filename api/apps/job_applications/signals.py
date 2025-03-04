from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.job_applications.models import JobApplication


@receiver(pre_save, sender=JobApplication)
def store_old_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_status = JobApplication.objects.get(pk=instance.pk).status
        except JobApplication.DoesNotExist:
            instance._old_status = None


@receiver(post_save, sender=JobApplication)
def send_job_application_update_email(sender, instance, **kwargs):
    if kwargs.get("created"):
        return

    if instance.status != instance._old_status:
        send_mail(
            subject="Job Application Update",
            message=f"Your job application for position '{instance.job.position}' has been updated from {instance._old_status} to {instance.status}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.applicant.user.email],
            fail_silently=False,
        )
