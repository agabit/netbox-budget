from netbox.api.viewsets import NetBoxModelViewSet
from ..models import BudgetPlan, Tender
from .serializers import BudgetPlanSerializer, TenderSerializer
from .filtersets import BudgetPlanFilterSet

class BudgetPlanViewSet(NetBoxModelViewSet):
    queryset = BudgetPlan.objects.prefetch_related("supplier", "contract")
    serializer_class = BudgetPlanSerializer
    filterset_class = BudgetPlanFilterSet

class TenderViewSet(NetBoxModelViewSet):
    queryset = Tender.objects.prefetch_related(
        "budget_plans", "supplier", "winner_supplier", "contract"
    )
    serializer_class = TenderSerializer
