from django.urls import path

from .views import EducationAPIView, JobSeekerProfileAPIView

urlpatterns = [
    path(
        "job-seeker-profile/basic/",
        JobSeekerProfileAPIView.as_view(),
        name="job-seeker-profile",
    ),
    path(
        "job-seeker-profile/education/",
        EducationAPIView.as_view(http_method_names={"post", "get"}),
        name="education-list-create",
    ),
    path(
        "job-seeker-profile/education/<int:pk>/",
        EducationAPIView.as_view(http_method_names={"put", "delete"}),
        name="education-update-delete",
    ),
]
