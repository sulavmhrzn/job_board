from rest_framework.permissions import BasePermission


class IsJobSeeker(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_job_seeker()


class IsJobProvider(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_job_provider()
