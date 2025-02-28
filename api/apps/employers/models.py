from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.accounts.models import User


class EmployerProfile(models.Model):
    class COMPANY_SIZE(models.TextChoices):
        SMALL = "1-10", "1-10"
        MEDIUM = "11-50", "11-50"
        LARGE = "51-200", "51-200"
        VERY_LARGE = "201-500", "201-500"
        HUGE = "500", "500+"

    class INDUSTRY(models.TextChoices):
        TECHNOLOGY = "TECHNOLOGY", "Technology"
        FINANCE = "FINANCE", "Finance"
        HEALTHCARE = "HEALTHCARE", "Healthcare"
        EDUCATION = "EDUCATION", "Education"

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="employer_profile"
    )
    company_name = models.CharField(max_length=255, blank=True)
    company_address = models.CharField(max_length=255, blank=True)
    company_description = models.TextField(blank=True)
    company_email = models.EmailField()
    company_phone = PhoneNumberField(blank=True)
    company_website = models.URLField(blank=True)
    company_logo = models.ImageField(
        upload_to="employer_logos", blank=True, default="default_employer_logo.png"
    )
    company_size = models.CharField(
        max_length=20, choices=COMPANY_SIZE.choices, default=COMPANY_SIZE.SMALL
    )
    industry = models.CharField(max_length=20, choices=INDUSTRY.choices, blank=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = "Employer Profile"
        verbose_name_plural = "Employer Profiles"


class SocialAccount(models.Model):
    profile = models.ForeignKey(
        EmployerProfile, on_delete=models.CASCADE, related_name="social_accounts"
    )
    platform = models.CharField(max_length=20)
    url = models.URLField()

    def __str__(self):
        return f"{self.profile.company_name} - {self.platform}"

    class Meta:
        verbose_name = "Social Account"
        verbose_name_plural = "Social Accounts"
