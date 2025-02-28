from django.urls import path

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
]
