from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.jobs.models import Job
from apps.jobs.serializers import JobSerializer
from apps.utils.permissions import IsJobProvider


@extend_schema(tags=["Jobs"])
class JobListCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsJobProvider]
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return super().get_permissions()

    @extend_schema(responses={200: JobSerializer(many=True)})
    def get(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(
            {"message": "Jobs fetched successfully", "data": serializer.data}
        )

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
        job = get_object_or_404(Job, pk=pk)
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
