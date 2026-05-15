from netbox.api.viewsets import NetBoxModelViewSet
from ..models import BudgetPlan, Tender, ItemCode
from .serializers import BudgetPlanSerializer, TenderSerializer, ItemCodeSerializer
from .filtersets import BudgetPlanFilterSet, ItemCodeFilterSet

class ItemCodeViewSet(NetBoxModelViewSet):
    queryset = ItemCode.objects.all()
    serializer_class = ItemCodeSerializer
    filterset_class = ItemCodeFilterSet

class BudgetPlanViewSet(NetBoxModelViewSet):
    queryset = BudgetPlan.objects.prefetch_related("supplier", "contract", "item_code")
    serializer_class = BudgetPlanSerializer
    filterset_class = BudgetPlanFilterSet

class TenderViewSet(NetBoxModelViewSet):
    queryset = Tender.objects.prefetch_related(
        "budget_plans", "supplier", "winner_supplier", "contract"
    )
    serializer_class = TenderSerializer
