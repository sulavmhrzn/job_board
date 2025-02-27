from django.urls import path

from .views import EducationAPIView, ExperienceAPIView, JobSeekerProfileAPIView

urlpatterns = [
    path(
        "job-seeker-profile/basic/",
        JobSeekerProfileAPIView.as_view(),
        name="job-seeker-profile",
    ),
    path(
        "job-seeker-profile/educations/",
        EducationAPIView.as_view(http_method_names={"post", "get"}),
        name="education-list-create",
    ),
    path(
        "job-seeker-profile/educations/<int:pk>/",
        EducationAPIView.as_view(http_method_names={"put", "delete"}),
        name="education-update-delete",
    ),
    path(
        "job-seeker-profile/experiences/",
        ExperienceAPIView.as_view(http_method_names={"post", "get"}),
        name="experience-list-create",
    ),
    path(
        "job-seeker-profile/experiences/<int:pk>/",
        ExperienceAPIView.as_view(http_method_names={"put", "delete"}),
        name="experience-update-delete",
    ),
]
