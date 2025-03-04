from django.urls import path

from apps.dashboard.views import JobSeekerDashboardAPIView

urlpatterns = [
    path(
        "job-seeker", JobSeekerDashboardAPIView.as_view(), name="job_seeker_dashboard"
    ),
]
