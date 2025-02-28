from django.urls import path

from apps.profiles.views import (
    EducationAPIView,
    ExperienceAPIView,
    JobSeekerProfileAPIView,
    SocialAccountAPIView,
)

urlpatterns = [
    path(
        "basic/",
        JobSeekerProfileAPIView.as_view(),
        name="job-seeker-profile",
    ),
    path(
        "educations/",
        EducationAPIView.as_view(http_method_names={"post", "get"}),
        name="education-list-create",
    ),
    path(
        "educations/<int:pk>/",
        EducationAPIView.as_view(http_method_names={"put", "delete"}),
        name="education-update-delete",
    ),
    path(
        "experiences/",
        ExperienceAPIView.as_view(http_method_names={"post", "get"}),
        name="experience-list-create",
    ),
    path(
        "experiences/<int:pk>/",
        ExperienceAPIView.as_view(http_method_names={"put", "delete"}),
        name="experience-update-delete",
    ),
    path(
        "social-accounts/",
        SocialAccountAPIView.as_view(http_method_names={"post", "get"}),
        name="social-accounts",
    ),
    path(
        "social-accounts/<int:pk>/",
        SocialAccountAPIView.as_view(http_method_names={"put", "delete"}),
        name="social-account-update-delete",
    ),
]
