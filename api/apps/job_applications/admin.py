from django.contrib import admin

from apps.job_applications.models import JobApplication, StatusHistory


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


@admin.register(StatusHistory)
class StatusHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "application",
        "previous_status",
        "new_status",
        "updated_at",
    )
    search_fields = (
        "application__job__position",
        "application__applicant__user__email",
    )
    list_filter = ("previous_status", "new_status")
