from netbox.views import generic
from . import models, tables, forms
from .filtersets import BudgetPlanFilterSet, TenderFilterSet


# BudgetPlan views
class BudgetPlanListView(generic.ObjectListView):
    queryset = models.BudgetPlan.objects.prefetch_related('supplier', 'contract')
    table = tables.BudgetPlanTable
    filterset = BudgetPlanFilterSet
    filterset_form = forms.BudgetPlanFilterForm


class BudgetPlanView(generic.ObjectView):
    queryset = models.BudgetPlan.objects.prefetch_related(
        'supplier', 'contract', 'tenders'
    )


class BudgetPlanEditView(generic.ObjectEditView):
    queryset = models.BudgetPlan.objects.all()
    form = forms.BudgetPlanForm


class BudgetPlanDeleteView(generic.ObjectDeleteView):
    queryset = models.BudgetPlan.objects.all()


# Tender views
class TenderListView(generic.ObjectListView):
    queryset = models.Tender.objects.prefetch_related(
        'budget_plan', 'supplier', 'winner_supplier', 'contract'
    )
    table = tables.TenderTable
    filterset = TenderFilterSet
    filterset_form = forms.TenderFilterForm


class TenderView(generic.ObjectView):
    queryset = models.Tender.objects.prefetch_related(
        'budget_plan', 'supplier', 'winner_supplier', 'contract'
    )


class TenderEditView(generic.ObjectEditView):
    queryset = models.Tender.objects.all()
    form = forms.TenderForm


class TenderDeleteView(generic.ObjectDeleteView):
    queryset = models.Tender.objects.all()
