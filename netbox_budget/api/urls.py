from netbox.api.routers import NetBoxRouter
from . import views

router = NetBoxRouter()
router.register("item-codes", views.ItemCodeViewSet)
router.register("budget-merges", views.BudgetMergeViewSet)
router.register("budget-plans", views.BudgetPlanViewSet)
router.register("tenders", views.TenderViewSet)
urlpatterns = router.urls
