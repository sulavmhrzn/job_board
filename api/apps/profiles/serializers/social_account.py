from apps.profiles.models import SocialAccount
from rest_framework import serializers


class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ["id", "account_name", "url"]
