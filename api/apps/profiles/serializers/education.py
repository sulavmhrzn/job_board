from datetime import datetime

from apps.profiles.models import Education
from rest_framework import serializers


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            "id",
            "degree",
            "course",
            "university",
            "start_date",
            "end_date",
            "is_current",
            "description",
            "grade",
        ]
        extra_kwargs = {
            "profile": {"read_only": True},
        }

    def validate_start_date(self, value):
        if value > datetime.now().date():
            raise serializers.ValidationError("Start date cannot be in the future")
        return value

    def validate(self, attrs):
        end_date = attrs.get(
            "end_date", self.instance.end_date if self.instance else None
        )
        start_date = attrs.get(
            "start_date", self.instance.start_date if self.instance else None
        )
        is_current = attrs.get(
            "is_current", self.instance.is_current if self.instance else None
        )

        if is_current and end_date:
            raise serializers.ValidationError(
                "End date cannot be set if is_current is true"
            )
        if not is_current and not end_date:
            raise serializers.ValidationError(
                "End date is required if is_current is false"
            )
        if end_date:
            if end_date < start_date:
                raise serializers.ValidationError(
                    "End date cannot be before start date"
                )
        return attrs
