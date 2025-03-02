from django.urls import path

from apps.job_applications.views import JobApplicationAPIView
from apps.jobs.views import JobListCreateAPIView, JobRetrieveUpdateDeleteAPIView

urlpatterns = [
    path(
        "",
        JobListCreateAPIView.as_view(http_method_names=["get", "post"]),
        name="job-list-create",
    ),
    path(
        "<int:pk>/",
        JobRetrieveUpdateDeleteAPIView.as_view(
            http_method_names=["get", "put", "delete"]
        ),
        name="job-retrieve-update-delete",
    ),
    path(
        "<int:pk>/apply/",
        JobApplicationAPIView.as_view(http_method_names=["post"]),
        name="job-apply",
    ),
]
