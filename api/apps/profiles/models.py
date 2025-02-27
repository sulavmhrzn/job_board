from apps.accounts.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class JobSeekerProfile(models.Model):
    class GENDER(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        OTHERS = "OTHERS", "Others"

    class MARITAL_STATUS(models.TextChoices):
        UNMARRIED = (
            "UNMARRIED",
            "Unmarried",
        )
        MARRIED = "MARRIED", "MARRIED"

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="job_seeker_profile"
    )
    phone_number = PhoneNumberField(blank=True)
    gender = models.TextField(max_length=20, choices=GENDER.choices)
    date_of_birth = models.DateField(blank=True, null=True)
    current_address = models.CharField(blank=True)
    permanent_address = models.CharField(blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS.choices)
    resume = models.FileField(upload_to="resumes/", blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()}"


class Education(models.Model):
    profile = models.ForeignKey(
        JobSeekerProfile, on_delete=models.CASCADE, related_name="education"
    )
    degree = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    grade = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.profile.user.get_full_name()} - {self.degree}"


class Experience(models.Model):
    class JOB_LEVEL(models.TextChoices):
        ENTRY = "ENTRY", "Entry"
        MID = "MID", "Mid"
        SENIOR = "SENIOR", "Senior"
        TOP = "TOP", "Top"

    profile = models.ForeignKey(
        JobSeekerProfile, on_delete=models.CASCADE, related_name="experience"
    )
    organization = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    job_location = models.CharField(max_length=255)
    job_category = models.CharField(max_length=255)
    job_level = models.CharField(max_length=255, choices=JOB_LEVEL.choices)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    currently_working = models.BooleanField(default=False)
    description = models.TextField()

    def __str__(self):
        return f"{self.job_title} at {self.organization}"

    class Meta:
        verbose_name_plural = "Experiences"
        verbose_name = "Experience"


class SocialAccount(models.Model):
    profile = models.ForeignKey(
        JobSeekerProfile, on_delete=models.CASCADE, related_name="social_accounts"
    )
    account_name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)

    def __str__(self):
        return f"{self.profile.user.get_full_name()} - {self.account_name}"
