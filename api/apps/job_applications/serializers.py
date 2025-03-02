from rest_framework import serializers

from apps.job_applications.models import JobApplication


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = [
            "id",
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
