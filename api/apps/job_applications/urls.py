from django.urls import path

from apps.job_applications.views import JobApplicationAPIView

urlpatterns = [
    path(
        "my-applications/",
        JobApplicationAPIView.as_view(http_method_names=["get"]),
        name="my-applications",
    ),
]
