from netbox.api.serializers import NetBoxModelSerializer
from ..models import BudgetPlan, Tender


class BudgetPlanSerializer(NetBoxModelSerializer):
    class Meta:
        model = BudgetPlan
        fields = [
            'id', 'url', 'display', 'year', 'project_name',
            'proxy_number', 'nomenclature_code', 'budget_type',
            'site_budget', 'unit', 'planned_quantity', 'price_per_unit',
            'total_sum', 'agreed_budget', 'shortfall',
            'commercial_proposal_url', 'tender_name',
            'supplier', 'contract',
        ]


class TenderSerializer(NetBoxModelSerializer):
    class Meta:
        model = Tender
        fields = [
            'id', 'url', 'display', 'budget_plan', 'tender_name',
            'status', 'start_date', 'end_date', 'responsible_person',
            'supplier', 'winner_supplier', 'contract',
            'expected_delivery_date',
        ]
