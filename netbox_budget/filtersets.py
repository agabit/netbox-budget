import django_filters
from .models import BudgetPlan, Tender


class BudgetPlanFilterSet(django_filters.FilterSet):
    year = django_filters.ChoiceFilter(
        choices=BudgetPlan.YEAR_CHOICES,
        label='Year'
    )
    budget_type = django_filters.ChoiceFilter(
        choices=BudgetPlan.BUDGET_TYPE_CHOICES,
        label='Budget Type'
    )
    site_budget = django_filters.ChoiceFilter(
        choices=BudgetPlan.SITE_CHOICES,
        label='Site'
    )

    class Meta:
        model = BudgetPlan
        fields = ['year', 'budget_type', 'site_budget']


class TenderFilterSet(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        choices=Tender.STATUS_CHOICES,
        label='Status'
    )

    class Meta:
        model = Tender
        fields = ['status']
