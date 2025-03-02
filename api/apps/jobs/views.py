from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.jobs.models import Job
from apps.jobs.serializers import JobListSerializer, JobSerializer
from apps.utils.filters import JobFilter
from apps.utils.paginations import JobsResultSetPagination
from apps.utils.permissions import IsJobProvider


@extend_schema(tags=["Jobs"])
class JobListCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsJobProvider]
    queryset = Job.objects.filter(status=Job.STATUS.ACTIVE)
    serializer_class = JobSerializer
    pagination_class = JobsResultSetPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = JobFilter

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return JobListSerializer
        return super().get_serializer_class()

    @extend_schema(responses={200: JobSerializer(many=True)})
    def get(self, request):
        page = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(employer=request.user.employer_profile)
        return Response(
            {"message": "Job created successfully", "data": serializer.data}
        )


@extend_schema(tags=["Jobs"])
class JobRetrieveUpdateDeleteAPIView(generics.GenericAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsJobProvider]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return super().get_permissions()

    def get(self, request, pk):
        # If user is authenticated and is job provider,
        # then they can view their own job regardless of status
        # Otherwise, only active jobs can be viewed
        if request.user.is_authenticated and request.user.is_job_provider():
            job = get_object_or_404(Job, pk=pk, employer=request.user.employer_profile)
        else:
            job = get_object_or_404(Job, pk=pk, status=Job.STATUS.ACTIVE)
        serializer = self.serializer_class(job)
        return Response(
            {"message": "Job fetched successfully", "data": serializer.data}
        )

    def put(self, request, pk):
        job = get_object_or_404(Job, pk=pk, employer=request.user.employer_profile)
        serializer = self.serializer_class(job, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Job updated successfully", "data": serializer.data}
        )

    def delete(self, request, pk):
        job = get_object_or_404(Job, pk=pk, employer=request.user.employer_profile)
        job.delete()
        return Response(
            {"message": "Job deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
