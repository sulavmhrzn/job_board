from rest_framework import serializers

from apps.employers.models import SocialAccount


class EmployerSocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ("id", "platform", "url")
