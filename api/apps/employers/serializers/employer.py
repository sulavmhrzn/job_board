from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from apps.employers.models import EmployerProfile
from apps.employers.serializers import social_account


class EmployerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    social_accounts = social_account.EmployerSocialAccountSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = EmployerProfile
        fields = (
            "user",
            "company_name",
            "company_email",
            "company_phone",
            "company_website",
            "company_logo",
            "company_address",
            "company_size",
            "company_description",
            "industry",
            "social_accounts",
        )
