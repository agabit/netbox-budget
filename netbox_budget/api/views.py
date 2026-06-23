from netbox.api.viewsets import NetBoxModelViewSet
from ..models import BudgetPlan, Tender, ItemCode, BudgetMerge
from .serializers import BudgetPlanSerializer, TenderSerializer, ItemCodeSerializer, BudgetMergeSerializer
from .filtersets import BudgetPlanFilterSet, ItemCodeFilterSet

class ItemCodeViewSet(NetBoxModelViewSet):
    queryset = ItemCode.objects.all()
    serializer_class = ItemCodeSerializer
    filterset_class = ItemCodeFilterSet

class BudgetPlanViewSet(NetBoxModelViewSet):
    queryset = BudgetPlan.objects.prefetch_related("supplier", "contract", "item_code")
    serializer_class = BudgetPlanSerializer
    filterset_class = BudgetPlanFilterSet

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        q = self.request.query_params.get("q", None)
        if q:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(project_name__icontains=q) |
                Q(proxy_number__icontains=q) |
                Q(tender_name__icontains=q)
            )
        return queryset

class TenderViewSet(NetBoxModelViewSet):
    queryset = Tender.objects.prefetch_related(
        "budget_plans", "supplier", "winner_supplier", "contract"
    )
    serializer_class = TenderSerializer

class BudgetMergeViewSet(NetBoxModelViewSet):
    queryset = BudgetMerge.objects.all()
    serializer_class = BudgetMergeSerializer
