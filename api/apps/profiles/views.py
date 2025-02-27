from apps.profiles.models import Education, JobSeekerProfile
from apps.utils.permissions import IsJobSeeker
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers.education import EducationSerializer
from .serializers.job_seeker import (
    JobSeekerProfileSerializer,
)


@extend_schema(tags=["Job Seeker Profile"])
class JobSeekerProfileAPIView(generics.GenericAPIView):
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [IsAuthenticated, IsJobSeeker]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        try:
            return JobSeekerProfile.objects.get(user=self.request.user)
        except JobSeekerProfile.DoesNotExist:
            raise NotFound("Job Seeker Profile does not exist")

    def get(self, request):
        return Response(
            {
                "message": "Job Seeker Profile",
                "data": JobSeekerProfileSerializer(self.get_object()).data,
            }
        )

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(
            {
                "message": "Job Seeker Profile created successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def put(self, request):
        serializer = self.serializer_class(
            request.user.job_seeker_profile,
            data=request.data,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "Job Seeker Profile updated successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Job Seeker Profile"])
class EducationAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsJobSeeker]
    serializer_class = EducationSerializer

    def get_queryset(self):
        return Education.objects.filter(profile=self.request.user.job_seeker_profile)

    def get(self, request):
        return Response(
            {
                "message": "Education fetched successfully",
                "data": EducationSerializer(self.get_queryset(), many=True).data,
            }
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(profile=request.user.job_seeker_profile)
        return Response(
            {
                "message": "Education created successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def put(self, request, pk):
        education = get_object_or_404(
            Education, pk=pk, profile=request.user.job_seeker_profile
        )
        serializer = self.serializer_class(education, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "Education updated successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        education = get_object_or_404(
            Education, pk=pk, profile=request.user.job_seeker_profile
        )
        education.delete()
        return Response(
            {"message": "Education deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
