from django.contrib import admin

from apps.jobs.models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "position",
        "category",
        "level",
        "job_type",
        "location",
        "salary_type",
        "employer__company_name",
        "status",
    )
    search_fields = ("position", "category", "location")
    list_filter = ("level", "job_type", "salary_type")
