from datetime import datetime

from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from apps.profiles.models import JobSeekerProfile
from apps.profiles.serializers import education, experience, social_account


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    education = education.EducationSerializer(many=True, read_only=True)
    experience = experience.ExperienceSerializer(many=True, read_only=True)
    social_accounts = social_account.SocialAccountSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = JobSeekerProfile
        fields = [
            "id",
            "user",
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
            "experience",
            "social_accounts",
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
