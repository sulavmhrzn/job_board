from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.employers.serializers.employer import EmployerProfileSerializer
from apps.employers.serializers.social_account import EmployerSocialAccountSerializer
from apps.utils.permissions import IsJobProvider

EMPLOYER_PROFILE = "Employer Profile"


@extend_schema(tags=[EMPLOYER_PROFILE])
class EmployerProfileAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsJobProvider]
    serializer_class = EmployerProfileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        return Response(
            {
                "message": "Employer profile fetched successfully",
                "data": self.serializer_class(request.user.employer_profile).data,
            }
        )

    def put(self, request):
        serializer = self.serializer_class(
            request.user.employer_profile, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(
            {
                "message": "Employer profile updated successfully",
                "data": serializer.data,
            }
        )


@extend_schema(tags=[EMPLOYER_PROFILE])
class SocialAccountAPIView(generics.GenericAPIView):
    serializer_class = EmployerSocialAccountSerializer
    permission_classes = [IsAuthenticated, IsJobProvider]

    def get_queryset(self):
        return self.request.user.employer_profile.social_accounts.all()

    def get_object(self, pk):
        return get_object_or_404(
            self.get_queryset(),
            pk=pk,
            profile=self.request.user.employer_profile,
        )

    @extend_schema(responses={200: EmployerSocialAccountSerializer(many=True)})
    def get(self, request):
        return Response(
            {
                "message": "Social accounts fetched successfully",
                "data": self.serializer_class(self.get_queryset(), many=True).data,
            }
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(profile=request.user.employer_profile)
        return Response(
            {
                "message": "Social account created successfully",
                "data": serializer.data,
            },
            status=201,
        )

    def delete(self, request, pk):
        social_account = self.get_object(pk)
        social_account.delete()
        return Response({"message": "Social account deleted successfully"}, status=204)

    def put(self, request, pk):
        serializer = self.serializer_class(
            self.get_object(pk), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "Social account updated successfully",
                "data": serializer.data,
            }
        )
