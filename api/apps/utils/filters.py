from django_filters import rest_framework as filters

from apps.jobs.models import Job


class JobFilter(filters.FilterSet):
    position = filters.CharFilter(field_name="position", lookup_expr="icontains")
    company = filters.CharFilter(
        field_name="employer__company_name", lookup_expr="icontains"
    )

    class Meta:
        model = Job
        fields = ["position", "company"]
