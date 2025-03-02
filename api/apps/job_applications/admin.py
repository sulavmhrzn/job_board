from django.contrib import admin

from apps.job_applications.models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "job",
        "job__employer",
        "applicant",
        "applicant__user__email",
        "status",
        "applied_at",
    )
    search_fields = ("job__position", "applicant__user__email")
    list_filter = ("status",)
