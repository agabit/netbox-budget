import django_filters
from ..models import BudgetPlan, Tender

class BudgetPlanFilterSet(django_filters.FilterSet):
    year = django_filters.NumberFilter(
        field_name="year",
        label="Year"
    )

    class Meta:
        model = BudgetPlan
        fields = ["year"]
