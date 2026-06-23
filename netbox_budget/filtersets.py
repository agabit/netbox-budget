import django_filters
from netbox.filtersets import NetBoxModelFilterSet
from .models import BudgetPlan, Tender, ItemCode
from netbox_digital_assets.models import Supplier, Contract

class ItemCodeFilterSet(NetBoxModelFilterSet):
    status = django_filters.ChoiceFilter(
        choices=ItemCode.STATUS_CHOICES,
        label="Status"
    )
    name = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Name"
    )
    short_name_kaz = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Short Name KAZ"
    )
    short_name_rus = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Short Name RUS"
    )

    class Meta:
        model = ItemCode
        fields = ["status", "name", "short_name_kaz", "short_name_rus"]

class BudgetPlanFilterSet(NetBoxModelFilterSet):
    year = django_filters.ChoiceFilter(
        choices=BudgetPlan.YEAR_CHOICES,
        label="Year"
    )
    status = django_filters.ChoiceFilter(
        choices=BudgetPlan.STATUS_CHOICES,
        label="Status"
    )
    budget_type = django_filters.ChoiceFilter(
        choices=BudgetPlan.BUDGET_TYPE_CHOICES,
        label="Budget Type"
    )
    site_budget = django_filters.ChoiceFilter(
        choices=BudgetPlan.SITE_CHOICES,
        label="Site"
    )
    proxy_number = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Proxy Number"
    )
    tender_name = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Tender Name"
    )
    item_code = django_filters.ModelMultipleChoiceFilter(
        queryset=ItemCode.objects.all(),
        label="Item Code"
    )

    class Meta:
        model = BudgetPlan
        fields = ["year", "status", "budget_type", "site_budget", "proxy_number", "tender_name", "item_code"]

class TenderFilterSet(NetBoxModelFilterSet):
    status = django_filters.ChoiceFilter(
        choices=Tender.STATUS_CHOICES,
        label="Status"
    )
    budget_plan_year = django_filters.ChoiceFilter(
        choices=BudgetPlan.YEAR_CHOICES,
        label="Budget Plan Year",
        field_name="budget_plans__year"
    )
    budget_plans = django_filters.ModelMultipleChoiceFilter(
        queryset=BudgetPlan.objects.all(),
        label="Budget Plan"
    )
    budget_plan_type = django_filters.ChoiceFilter(
        choices=BudgetPlan.BUDGET_TYPE_CHOICES,
        label="Budget Type",
        field_name="budget_plans__budget_type"
    )
    tender_name = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Tender Name"
    )
    winner_supplier = django_filters.ModelChoiceFilter(
        queryset=Supplier.objects.all(),
        label="Winner Supplier"
    )
    contract = django_filters.ModelChoiceFilter(
        queryset=Contract.objects.all(),
        label="Contract"
    )

    class Meta:
        model = Tender
        fields = ["status", "budget_plan_year", "budget_plans", "tender_name", "winner_supplier", "contract"]

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset).distinct()
