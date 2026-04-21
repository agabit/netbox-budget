from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from .models import BudgetPlan, Tender
from netbox_digital_assets.models import Supplier, Contract
from .models import BudgetPlan, Tender, BudgetMerge

class BudgetPlanForm(NetBoxModelForm):
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
            'year', 'status', 'project_name', 'proxy_number', 'nomenclature_code',
            'device', 'budget_type', 'site_budget', 'unit',
            'planned_quantity', 'price_per_unit', 'agreed_budget',
            'commercial_proposal_url', 'tender_name',
            'supplier', 'contract', 'tags',
        ]


class BudgetPlanFilterForm(NetBoxModelFilterSetForm):
    model = BudgetPlan
    year = forms.ChoiceField(
        choices=[('', 'All Years')] + BudgetPlan.YEAR_CHOICES,
        required=False
    )
    status = forms.ChoiceField(
        choices=[('', 'All')] + BudgetPlan.STATUS_CHOICES,
        required=False
    )
    budget_type = forms.ChoiceField(
        choices=[('', 'All')] + BudgetPlan.BUDGET_TYPE_CHOICES,
        required=False
    )
    site_budget = forms.ChoiceField(
        choices=[('', 'All Sites')] + BudgetPlan.SITE_CHOICES,
        required=False
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TenderForm(NetBoxModelForm):
    budget_plan = DynamicModelChoiceField(
        queryset=BudgetPlan.objects.all()
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
            'budget_plan', 'tender_name', 'status',
            'start_date', 'end_date', 'responsible_person',
            'supplier', 'winner_supplier', 'contract',
            'expected_delivery_date', 'tags',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }


class TenderFilterForm(NetBoxModelFilterSetForm):
    model = Tender
    status = forms.ChoiceField(
        choices=[('', 'All')] + Tender.STATUS_CHOICES,
        required=False
    )
    budget_plan = DynamicModelChoiceField(
        queryset=BudgetPlan.objects.all(),
        required=False
    )
class DonateBudgetForm(forms.Form):
    target_plan = DynamicModelChoiceField(
        queryset=BudgetPlan.objects.all(),
        label='Donate TO project'
    )
    amount = forms.DecimalField(
        max_digits=20,
        decimal_places=2,
        label='Amount to donate (KZT)',
        min_value=1
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Notes (optional)'
    )
