from django.db import models

from apps.jobs.models import Job
from apps.profiles.models import JobSeekerProfile


class JobApplication(models.Model):
    class STATUS(models.TextChoices):
        PENDING = "PENDING", "Pending"
        REVIEWED = "REVIEWED", "Reviewed"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(
        JobSeekerProfile, on_delete=models.CASCADE, related_name="applications"
    )
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to="resumes/")
    status = models.CharField(
        max_length=20, choices=STATUS.choices, default=STATUS.PENDING
    )
    expected_salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.applicant.user.email} - {self.job.position}"
