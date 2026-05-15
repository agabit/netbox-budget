import django_filters
from ..models import BudgetPlan, Tender, ItemCode

class ItemCodeFilterSet(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method="search",
        label="Search"
    )

    def search(self, queryset, name, value):
        return queryset.filter(
            __import__("django.db.models", fromlist=["Q"]).Q(name__icontains=value) |
            __import__("django.db.models", fromlist=["Q"]).Q(short_name_rus__icontains=value) |
            __import__("django.db.models", fromlist=["Q"]).Q(short_name_kaz__icontains=value)
        )

    class Meta:
        model = ItemCode
        fields = ["q", "status"]

class BudgetPlanFilterSet(django_filters.FilterSet):
    year = django_filters.NumberFilter(
        field_name="year",
        label="Year"
    )
    budget_type = django_filters.CharFilter(
        field_name="budget_type",
        label="Budget Type"
    )

    class Meta:
        model = BudgetPlan
        fields = ["year", "budget_type"]
