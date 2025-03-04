from django.db.models import Count
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.job_applications.models import JobApplication, StatusHistory
from apps.job_applications.serializers import StatusHistorySerialzier
from apps.utils.permissions import IsJobSeeker


@extend_schema(tags=["Dashboard"])
class JobSeekerDashboardAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsJobSeeker]

    def get(self, request):
        profile = self.request.user.job_seeker_profile
        applications_submitted = JobApplication.objects.filter(
            applicant=profile
        ).prefetch_related("status_histories")
        applications_based_on_status = applications_submitted.values("status").annotate(
            count=Count("status")
        )
        status_history = StatusHistory.objects.filter(
            application__applicant=profile
        ).select_related("application")
        status_history_serializer = StatusHistorySerialzier(status_history, many=True)

        return Response(
            {
                "total_applications_submitted": applications_submitted.count(),
                "applications_based_on_status": applications_based_on_status,
                "status_histories": status_history_serializer.data,
                "bookmarked_jobs": 0,
            },
            status=status.HTTP_200_OK,
        )
