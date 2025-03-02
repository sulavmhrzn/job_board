from django.urls import path

from apps.job_applications.views import (
    JobApplicationAPIView,
    JobProviderApplicationsAPIView,
)

urlpatterns = [
    path(
        "my-applications/",
        JobApplicationAPIView.as_view(http_method_names=["get"]),
        name="my-applications",
    ),
    path(
        "received-applications/",
        JobProviderApplicationsAPIView.as_view(http_method_names=["get"]),
        name="received-applications",
    ),
    path(
        "<int:pk>/",
        JobProviderApplicationsAPIView.as_view(http_method_names=["patch", "delete"]),
        name="update-application",
    ),
]
