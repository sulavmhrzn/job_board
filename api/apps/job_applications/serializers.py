from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.job_applications.models import JobApplication


class JobApplicationSerializer(serializers.ModelSerializer):
    job = serializers.SerializerMethodField()
    applicant = serializers.SerializerMethodField()

    @extend_schema_field(
        {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "title": {"type": "string"},
                "description": {"type": "string"},
                "employer": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "company_name": {"type": "string"},
                        "company_email": {"type": "string"},
                    },
                },
            },
        }
    )
    def get_job(self, obj):
        return {
            "id": obj.job.id,
            "title": obj.job.position,
            "description": obj.job.description,
            "employer": {
                "id": obj.job.employer.id,
                "company_name": obj.job.employer.company_name,
                "company_email": obj.job.employer.company_email,
            },
        }

    @extend_schema_field(
        {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
                "email": {"type": "string"},
            },
        }
    )
    def get_applicant(self, obj):
        return {
            "id": obj.applicant.id,
            "first_name": obj.applicant.user.first_name,
            "last_name": obj.applicant.user.last_name,
            "email": obj.applicant.user.email,
        }

    class Meta:
        model = JobApplication
        fields = [
            "id",
            "job",
            "status",
            "applicant",
            "cover_letter",
            "resume",
            "expected_salary",
        ]
        read_only_fields = [
            "id",
            "job",
            "status",
            "applicant",
            "applied_at",
            "updated_at",
        ]

    def validate_resume(self, resume):
        if resume.content_type not in ["application/pdf", "application/msword"]:
            raise serializers.ValidationError("Only PDF and Word files are accepted.")
        if resume.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("File size too large. Max 5MB allowed.")
        return resume

    def create(self, validated_data):
        if JobApplication.objects.filter(
            job=validated_data["job"], applicant=validated_data["applicant"]
        ).exists():
            raise serializers.ValidationError("You have already applied for this job.")
        return super().create(validated_data)


class UpdateJobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ["status"]
