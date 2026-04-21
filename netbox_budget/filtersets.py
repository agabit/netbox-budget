import django_filters
from netbox.filtersets import NetBoxModelFilterSet
from .models import BudgetPlan, Tender


class BudgetPlanFilterSet(NetBoxModelFilterSet):
    year = django_filters.ChoiceFilter(
        choices=BudgetPlan.YEAR_CHOICES,
        label='Year'
    )
    status = django_filters.ChoiceFilter(
        choices=BudgetPlan.STATUS_CHOICES,
        label='Status'
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
        fields = ['year', 'status', 'budget_type', 'site_budget']


class TenderFilterSet(NetBoxModelFilterSet):
    status = django_filters.ChoiceFilter(
        choices=Tender.STATUS_CHOICES,
        label='Status'
    )

    class Meta:
        model = Tender
        fields = ['status']
