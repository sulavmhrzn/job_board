from datetime import datetime

from apps.profiles.models import JobSeekerProfile
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .education import EducationSerializer


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    education = serializers.SerializerMethodField()

    @extend_schema_field(EducationSerializer(many=True))
    def get_education(self, obj):
        return EducationSerializer(obj.education.all(), many=True).data

    class Meta:
        model = JobSeekerProfile
        fields = [
            "phone_number",
            "gender",
            "date_of_birth",
            "current_address",
            "permanent_address",
            "marital_status",
            "date_of_birth",
            "resume",
            "profile_picture",
            "education",
        ]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def validate_resume(self, value):
        self._validate_file_type(value, ["application/pdf", "image/jpeg", "image/jpg"])
        self._validate_file_size(value, 1024 * 1024 * 2)
        return value

    def validate_profile_picture(self, value):
        self._validate_file_size(value, 1024 * 1024 * 2)
        return value

    def validate_date_of_birth(self, value):
        if value:
            if value > datetime.now().date():
                raise serializers.ValidationError(
                    "Date of birth cannot be in the future"
                )
        return value

    def validate(self, attrs):
        if (
            getattr(self.context["request"].user, "job_seeker_profile", None)
            and self.context["request"].method == "POST"
        ):
            raise serializers.ValidationError(
                "Job Seeker Profile already exists. Please update it instead of creating a new one."
            )

        return attrs

    def _validate_file_size(self, value, max_size):
        if value:
            if value.size > max_size:
                raise serializers.ValidationError("File size must be less than 5MB")
        return value

    def _validate_file_type(self, value, allowed_types):
        if value:
            if value.content_type not in allowed_types:
                raise serializers.ValidationError("File type must be a PDF or image")
        return value
