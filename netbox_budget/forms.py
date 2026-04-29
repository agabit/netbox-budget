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

class BudgetPlanForm(NetBoxModelForm):
    item_code = DynamicModelChoiceField(
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
            "supplier", "contract", "tags",
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

class TenderForm(NetBoxModelForm):
    budget_plan_year = forms.ChoiceField(
        choices=[("", "--- Select Year First ---")] + BudgetPlan.YEAR_CHOICES,
        required=False,
        label="Budget Plan Year",
        help_text="Select a year to filter the Budget Plans list below"
    )
    budget_plans = DynamicModelMultipleChoiceField(
        queryset=BudgetPlan.objects.all(),
        label="Budget Plans",
        query_params={
            "year": "$budget_plan_year",
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
            "budget_plan_year", "budget_plans", "tender_name", "status",
            "start_date", "end_date", "responsible_person",
            "supplier", "winner_supplier", "contract",
            "expected_delivery_date", "contract_sum", "tags",
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
    budget_plans = DynamicModelMultipleChoiceField(
        queryset=BudgetPlan.objects.all(),
        required=False,
        label="Budget Plan"
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
