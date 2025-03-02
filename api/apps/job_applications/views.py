from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.job_applications.models import JobApplication
from apps.job_applications.serializers import JobApplicationSerializer
from apps.jobs.models import Job
from apps.utils.permissions import IsJobSeeker


@extend_schema(tags=["Job Applications"])
class JobApplicationAPIView(generics.GenericAPIView):
    serializer_class = JobApplicationSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsJobSeeker]

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk, status=Job.STATUS.ACTIVE)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        job_application = serializer.save(
            job=job, applicant=request.user.job_seeker_profile
        )
        return Response(
            {
                "message": "Job applied successfully",
                "data": self.serializer_class(job_application).data,
            },
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(responses={200: JobApplicationSerializer(many=True)})
    def get(self, request):
        job_applications = JobApplication.objects.filter(
            applicant=request.user.job_seeker_profile
        )
        serializer = self.serializer_class(job_applications, many=True)
        return Response(
            {
                "message": "Job applications fetched successfully",
                "data": serializer.data,
            }
        )
