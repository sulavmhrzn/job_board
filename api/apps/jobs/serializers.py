from django.utils import timezone
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.jobs.models import Job


class JobSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()

    @extend_schema_field(
        {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "company_name": {"type": "string"},
                "company_logo": {"type": "string"},
                "email": {"type": "string"},
            },
        }
    )
    def get_company(self, obj):
        return {
            "id": obj.employer.id,
            "company_name": obj.employer.company_name,
            "comapny_logo": obj.employer.company_logo.url,
            "email": obj.employer.company_email,
        }

    class Meta:
        model = Job
        fields = (
            "id",
            "company",
            "position",
            "no_of_employee",
            "category",
            "level",
            "job_type",
            "location",
            "offer_type",
            "salary_type",
            "currency",
            "minimum_salary",
            "maximum_salary",
            "description",
            "hide_salary",
            "deadline",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "employer": {"read_only": True},
        }

    def validate_deadline(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Deadline cannot be in the past.")
        return value

    def validate(self, attrs):
        offer_type = attrs.get(
            "offer_type", self.instance.offer_type if self.instance else None
        )
        maximum_salary = attrs.get(
            "maximum_salary", self.instance.maximum_salary if self.instance else None
        )
        minimum_salary = attrs.get(
            "minimum_salary", self.instance.minimum_salary if self.instance else None
        )

        if offer_type == Job.OFFER_TYPE.FIXED:
            maximum_salary = minimum_salary
        if offer_type == Job.OFFER_TYPE.RANGE and not attrs.get("maximum_salary"):
            raise serializers.ValidationError(
                {"maximum_salary": "Maximum salary is required for range offer type."}
            )
        if minimum_salary and maximum_salary and minimum_salary > maximum_salary:
            raise serializers.ValidationError(
                {"maximum_salary": "Maximum salary cannot be less than minimum salary."}
            )
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data["hide_salary"]:
            data.pop("minimum_salary")
            data.pop("maximum_salary")
        return data
