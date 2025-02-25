from django.urls import path

from .views import UserCreateView, UserGetView

urlpatterns = [
    path("", UserCreateView.as_view(), name="users-create"),
    path("me/", UserGetView.as_view(), name="users-get"),
]
