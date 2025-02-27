from django.urls import path

from .views import (
    UserCreateView,
    UserRetrieveUpdateView,
)

urlpatterns = [
    path("", UserCreateView.as_view(), name="users-create"),
    path("me/", UserRetrieveUpdateView.as_view(), name="users-get"),
]
