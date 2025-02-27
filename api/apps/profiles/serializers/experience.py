from datetime import datetime

from rest_framework import serializers

from apps.profiles.models import Experience


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            "id",
            "organization",
            "job_title",
            "job_location",
            "job_category",
            "job_level",
            "start_date",
            "end_date",
            "currently_working",
            "description",
        ]

    def validate_start_date(self, value):
        if value > datetime.now().date():
            raise serializers.ValidationError("Start date cannot be in the future")
        return value

    def validate_end_date(self, value):
        if value and value > datetime.now().date():
            raise serializers.ValidationError("End date cannot be in the future")
        return value

    def validate(self, attrs):
        currently_working = attrs.get(
            "currently_working",
            self.instance.currently_working if self.instance else None,
        )
        end_date = attrs.get(
            "end_date", self.instance.end_date if self.instance else None
        )
        if not currently_working and not end_date:
            raise serializers.ValidationError(
                "End date is required if you are not currently working"
            )
        if currently_working and end_date:
            raise serializers.ValidationError(
                "End date should not be provided if you are currently working"
            )
        return attrs
