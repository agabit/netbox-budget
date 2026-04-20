from netbox.api.viewsets import NetBoxModelViewSet
from ..models import BudgetPlan, Tender
from .serializers import BudgetPlanSerializer, TenderSerializer


class BudgetPlanViewSet(NetBoxModelViewSet):
    queryset = BudgetPlan.objects.prefetch_related('supplier', 'contract')
    serializer_class = BudgetPlanSerializer


class TenderViewSet(NetBoxModelViewSet):
    queryset = Tender.objects.prefetch_related(
        'budget_plan', 'supplier', 'winner_supplier', 'contract'
    )
    serializer_class = TenderSerializer
