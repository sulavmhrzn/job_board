from django.urls import path

from .views import EmployerProfileAPIView, SocialAccountAPIView

urlpatterns = [
    path("basic/", EmployerProfileAPIView.as_view(), name="employer-profile-basic"),
    path(
        "social-accounts/",
        SocialAccountAPIView.as_view(http_method_names={"get", "post"}),
        name="social-accounts",
    ),
    path(
        "social-accounts/<int:pk>/",
        SocialAccountAPIView.as_view(http_method_names={"put", "delete"}),
        name="social-account",
    ),
]
