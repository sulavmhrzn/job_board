from django.contrib import admin

from apps.employers.models import EmployerProfile, SocialAccount


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ("company_name", "user", "company_email", "company_phone")
    search_fields = ("company_name", "company_email")
    list_filter = ("company_size", "industry")


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ("profile", "platform", "url")
    search_fields = ("profile__company_name", "platform")
    list_filter = ("platform",)
