from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.employers.models import EmployerProfile


class Job(models.Model):
    class LEVEL(models.TextChoices):
        ENTRY = "ENTRY", "Entry"
        MID = "MID", "Mid"
        SENIOR = "SENIOR", "Senior"
        TOP = "TOP", "Top"

    class JOB_TYPE(models.TextChoices):
        FULL_TIME = "FULL_TIME", "Full Time"
        PART_TIME = "PART_TIME", "Part Time"
        CONTRACT = "CONTRACT", "Contract"
        INTERNSHIP = "INTERNSHIP", "Internship"
        REMOTE = "REMOTE", "Remote"
        TRAINEESHIP = "TRAINEESHIP", "Traineeship"

    class SALARY_TYPE(models.TextChoices):
        MONTHLY = "MONTHLY", "Monthly"
        YEARLY = "YEARLY", "Yearly"
        HOURLY = "HOURLY", "Hourly"
        DAILY = "DAILY", "Daily"
        WEEKLY = "WEEKLY", "Weekly"

    class CURRENCY(models.TextChoices):
        DOLLAR = "DOLLAR", "Dollar"
        INR = "INR", "Indian Rupee"
        NRS = "NRS", "Nepalese Rupee"

    class OFFER_TYPE(models.TextChoices):
        RANGE = "RANGE", "Range"
        FIXED = "FIXED", "Fixed"

    employer = models.ForeignKey(
        EmployerProfile, on_delete=models.CASCADE, related_name="jobs"
    )
    position = models.CharField(max_length=255)
    no_of_employee = models.PositiveIntegerField()
    category = models.CharField(max_length=255)
    level = models.CharField(max_length=20, choices=LEVEL.choices)
    job_type = models.CharField(max_length=255, choices=JOB_TYPE.choices)
    location = models.CharField(max_length=255, blank=True)
    offer_type = models.CharField(max_length=255, choices=OFFER_TYPE.choices)
    salary_type = models.CharField(max_length=255, choices=SALARY_TYPE.choices)
    currency = models.CharField(
        max_length=255, choices=CURRENCY.choices, default=CURRENCY.NRS
    )
    minimum_salary = models.PositiveIntegerField()
    maximum_salary = models.PositiveIntegerField(blank=True)
    description = models.TextField()
    deadline = models.DateField(blank=True, null=True)
    hide_salary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.position

    def clean(self):
        if self.offer_type == self.OFFER_TYPE.FIXED:
            self.maximum_salary = self.minimum_salary

        if (
            self.minimum_salary
            and self.maximum_salary
            and self.minimum_salary > self.maximum_salary
        ):
            raise ValidationError(
                {"maximum_salary": "Maximum salary cannot be less than minimum salary."}
            )

        if self.offer_type == self.OFFER_TYPE.RANGE and not self.maximum_salary:
            raise ValidationError(
                {"maximum_salary": "Maximum salary is required for range offer type."}
            )

        if self.deadline and self.deadline < timezone.now().date():
            raise ValidationError({"deadline": "Deadline cannot be in the past."})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
