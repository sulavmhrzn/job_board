from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/create/", TokenObtainPairView.as_view(), name="token_create"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/profiles/job-seeker-profile/", include("apps.profiles.urls")),
    path("api/profiles/employer-profile/", include("apps.employers.urls")),
    path("api/jobs/", include("apps.jobs.urls")),
    path("api/job-applications/", include("apps.job_applications.urls")),
    path("api/dashboard/", include("apps.dashboard.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
