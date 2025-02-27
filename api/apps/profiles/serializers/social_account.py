from rest_framework import serializers

from apps.profiles.models import SocialAccount


class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ["id", "account_name", "url"]
