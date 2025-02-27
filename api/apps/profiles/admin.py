from apps.profiles.models import Education, Experience, JobSeekerProfile
from django.contrib import admin


@admin.register(JobSeekerProfile)
class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "gender", "date_of_birth")
    search_fields = ("user__email", "user__first_name", "user__last_name")
    ordering = ("user__email",)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = (
        "profile",
        "degree",
        "course",
        "university",
        "start_date",
        "end_date",
        "is_current",
    )
    search_fields = (
        "profile__user__email",
        "profile__user__first_name",
        "profile__user__last_name",
    )
    ordering = ("profile__user__email",)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "profile",
        "job_title",
        "organization",
        "start_date",
        "end_date",
        "currently_working",
    )
    search_fields = (
        "profile__user__email",
        "profile__user__first_name",
        "profile__user__last_name",
    )
    ordering = ("profile__user__email",)
