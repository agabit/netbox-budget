from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField
from .models import BudgetPlan, Tender, BudgetMerge, ItemCode
from netbox_digital_assets.models import Supplier, Contract

class ItemCodeForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = ItemCode
        fields = [
            "name", "status", "short_name_kaz", "specification_kaz",
            "short_name_rus", "specification_rus", "pdf_file",
            "cancelled_date", "comments",
        ]
        widgets = {
            "cancelled_date": forms.DateInput(attrs={"type": "date"}),
        }

class ItemCodeFilterForm(NetBoxModelFilterSetForm):
    model = ItemCode
    status = forms.ChoiceField(
        choices=[("", "All")] + ItemCode.STATUS_CHOICES,
        required=False
    )
    name = forms.CharField(
        required=False,
        label="Name"
    )
    short_name_kaz = forms.CharField(
        required=False,
        label="Short Name KAZ"
    )
    short_name_rus = forms.CharField(
        required=False,
        label="Short Name RUS"
    )

class BudgetPlanForm(NetBoxModelForm):
    item_code = DynamicModelMultipleChoiceField(
        queryset=ItemCode.objects.all(),
        required=False,
        label="Item Code"
    )
    supplier = DynamicModelChoiceField(
        queryset=Supplier.objects.all(),
        required=False
    )
    contract = DynamicModelChoiceField(
        queryset=Contract.objects.all(),
        required=False
    )
    comments = CommentField()

    class Meta:
        model = BudgetPlan
        fields = [
            "year", "status", "project_name", "proxy_number", "item_code",
            "device", "budget_type", "site_budget", "unit",
            "planned_quantity", "price_per_unit", "agreed_budget",
            "commercial_proposal_url", "tender_name",
            "supplier", "contract", "comments", "tags",
        ]

class BudgetPlanFilterForm(NetBoxModelFilterSetForm):
    model = BudgetPlan
    year = forms.ChoiceField(
        choices=[("", "All Years")] + BudgetPlan.YEAR_CHOICES,
        required=False
    )
    status = forms.ChoiceField(
        choices=[("", "All")] + BudgetPlan.STATUS_CHOICES,
        required=False
    )
    budget_type = forms.ChoiceField(
        choices=[("", "All")] + BudgetPlan.BUDGET_TYPE_CHOICES,
        required=False
    )
    site_budget = forms.ChoiceField(
        choices=[("", "All Sites")] + BudgetPlan.SITE_CHOICES,
        required=False
    )
    proxy_number = forms.CharField(
        required=False,
        label="Proxy Number"
    )
    tender_name = forms.CharField(
        required=False,
        label="Tender Name"
    )
    item_code = DynamicModelMultipleChoiceField(
        queryset=ItemCode.objects.all(),
        required=False,
        label="Item Code"
    )

class TenderForm(NetBoxModelForm):
    budget_plan_year = forms.ChoiceField(
        choices=[("", "--- Select Year First ---")] + BudgetPlan.YEAR_CHOICES,
        required=False,
        label="Budget Plan Year",
        help_text="Select a year to filter the Budget Plans list below"
    )
    budget_plan_type = forms.ChoiceField(
        choices=[("", "--- Select Type ---")] + BudgetPlan.BUDGET_TYPE_CHOICES,
        required=False,
        label="Budget Type",
        help_text="Select a type to filter the Budget Plans list below"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Auto-fill year and type from existing budget plans when editing
        if self.instance and self.instance.pk:
            plans = self.instance.budget_plans.all()
            if plans.exists():
                first_plan = plans.first()
                self.initial['budget_plan_year'] = first_plan.year
                self.initial['budget_plan_type'] = first_plan.budget_type

    budget_plans = DynamicModelMultipleChoiceField(
        queryset=BudgetPlan.objects.all(),
        label="Budget Plans",
        query_params={
            "year": "$budget_plan_year",
            "budget_type": "$budget_plan_type",
        },
        required=False
    )
    supplier = DynamicModelChoiceField(
        queryset=Supplier.objects.all(),
        required=False
    )
    winner_supplier = DynamicModelChoiceField(
        queryset=Supplier.objects.all(),
        required=False
    )
    contract = DynamicModelChoiceField(
        queryset=Contract.objects.all(),
        required=False
    )
    comments = CommentField()

    class Meta:
        model = Tender
        fields = [
            "budget_plan_year", "budget_plan_type", "budget_plans", "tender_name", "status",
            "start_date", "end_date", "responsible_person",
            "supplier", "winner_supplier", "contract",
            "expected_delivery_date", "contract_sum", "comments", "tags",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "expected_delivery_date": forms.DateInput(attrs={"type": "date"}),
        }

class TenderFilterForm(NetBoxModelFilterSetForm):
    model = Tender
    status = forms.ChoiceField(
        choices=[("", "All")] + Tender.STATUS_CHOICES,
        required=False
    )
    budget_plan_year = forms.ChoiceField(
        choices=[("", "All Years")] + BudgetPlan.YEAR_CHOICES,
        required=False,
        label="Budget Plan Year"
    )
    budget_plan_type = forms.ChoiceField(
        choices=[("", "All Types")] + BudgetPlan.BUDGET_TYPE_CHOICES,
        required=False,
        label="Budget Type"
    )
    budget_plans = DynamicModelMultipleChoiceField(
        queryset=BudgetPlan.objects.all(),
        required=False,
        label="Budget Plan"
    )
    tender_name = forms.CharField(
        required=False,
        label="Tender Name"
    )
    winner_supplier = DynamicModelChoiceField(
        queryset=Supplier.objects.all(),
        required=False,
        label="Winner Supplier"
    )
    contract = DynamicModelChoiceField(
        queryset=Contract.objects.all(),
        required=False,
        label="Contract"
    )

class DonateBudgetForm(forms.Form):
    target_plan = DynamicModelChoiceField(
        queryset=BudgetPlan.objects.all(),
        label="Donate TO project"
    )
    amount = forms.DecimalField(
        max_digits=20,
        decimal_places=2,
        label="Amount to donate (KZT)",
        min_value=1
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        label="Notes (optional)"
    )
