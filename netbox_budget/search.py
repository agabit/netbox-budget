from netbox.search import SearchIndex, register_search
from .models import BudgetPlan, Tender


@register_search
class BudgetPlanIndex(SearchIndex):
    model = BudgetPlan
    fields = (
        ('project_name', 100),
        ('proxy_number', 100),
        ('nomenclature_code', 200),
        ('tender_name', 200),
    )


@register_search
class TenderIndex(SearchIndex):
    model = Tender
    fields = (
        ('tender_name', 100),
        ('responsible_person', 200),
    )
