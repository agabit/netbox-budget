from netbox.api.serializers import NetBoxModelSerializer
from ..models import BudgetPlan, Tender, ItemCode

class ItemCodeSerializer(NetBoxModelSerializer):
    class Meta:
        model = ItemCode
        fields = [
            "id", "url", "display", "name", "status",
            "short_name_kaz", "short_name_rus",
            "specification_kaz", "specification_rus",
            "cancelled_date", "comments",
        ]

class BudgetPlanSerializer(NetBoxModelSerializer):
    class Meta:
        model = BudgetPlan
        fields = [
            "id", "url", "display", "year", "project_name",
            "proxy_number", "item_code", "budget_type",
            "site_budget", "unit", "planned_quantity", "price_per_unit",
            "total_sum", "agreed_budget", "shortfall",
            "commercial_proposal_url", "tender_name",
            "supplier", "contract",
        ]

class TenderSerializer(NetBoxModelSerializer):
    class Meta:
        model = Tender
        fields = [
            "id", "url", "display", "budget_plans", "tender_name",
            "status", "start_date", "end_date", "responsible_person",
            "supplier", "winner_supplier", "contract",
            "expected_delivery_date",
        ]
