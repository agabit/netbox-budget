from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from netbox.views import generic
from . import models, tables, forms
from .filtersets import BudgetPlanFilterSet, TenderFilterSet


# BudgetPlan views
class BudgetPlanListView(generic.ObjectListView):
    queryset = models.BudgetPlan.objects.prefetch_related('supplier', 'contract')
    table = tables.BudgetPlanTable
    filterset = BudgetPlanFilterSet
    filterset_form = forms.BudgetPlanFilterForm

    def get_queryset(self, request):
        from datetime import datetime
        queryset = super().get_queryset(request)
        # If no filters applied, default to current year
        if not request.GET:
            current_year = datetime.now().year
            queryset = queryset.filter(year=current_year)
        return queryset

class BudgetPlanView(generic.ObjectView):
    queryset = models.BudgetPlan.objects.prefetch_related(
        'supplier', 'contract', 'tenders'
    )

    def get_extra_context(self, request, instance):
        donations_made = instance.donations_made.all()
        donations_received = instance.donations_received.all()
        return {
            'donations_made': donations_made,
            'donations_received': donations_received,
        }


class BudgetPlanEditView(generic.ObjectEditView):
    queryset = models.BudgetPlan.objects.all()
    form = forms.BudgetPlanForm


class BudgetPlanDeleteView(generic.ObjectDeleteView):
    queryset = models.BudgetPlan.objects.all()


class DonateBudgetView(generic.ObjectView):
    queryset = models.BudgetPlan.objects.all()

    def get(self, request, pk):
        source_plan = get_object_or_404(models.BudgetPlan, pk=pk)
        form = forms.DonateBudgetForm()
        # Exclude current plan from target choices
        form.fields['target_plan'].queryset = models.BudgetPlan.objects.exclude(pk=pk)
        return render(request, 'netbox_budget/donate_budget.html', {
            'form': form,
            'source_plan': source_plan,
        })

    def post(self, request, pk):
        source_plan = get_object_or_404(models.BudgetPlan, pk=pk)
        form = forms.DonateBudgetForm(request.POST)
        form.fields['target_plan'].queryset = models.BudgetPlan.objects.exclude(pk=pk)

        if form.is_valid():
            amount = form.cleaned_data['amount']
            target_plan = form.cleaned_data['target_plan']
            notes = form.cleaned_data['notes']

            # Validate amount
            if amount > source_plan.agreed_budget:
                messages.error(request, f'Amount exceeds available budget ({source_plan.agreed_budget} KZT)')
                return render(request, 'netbox_budget/donate_budget.html', {
                    'form': form,
                    'source_plan': source_plan,
                })

            # Create merge record
            models.BudgetMerge.objects.create(
                source_plan=source_plan,
                target_plan=target_plan,
                amount=amount,
                notes=notes
            )

            # Update source budget
            source_plan.agreed_budget -= amount
            if source_plan.agreed_budget == 0:
                source_plan.status = 'donated'
            source_plan.save()

            # Update target budget
            target_plan.agreed_budget += amount
            target_plan.save()

            messages.success(
                request,
                f'Successfully donated {amount} KZT from "{source_plan.project_name}" to "{target_plan.project_name}"'
            )
            return redirect(source_plan.get_absolute_url())

        return render(request, 'netbox_budget/donate_budget.html', {
            'form': form,
            'source_plan': source_plan,
        })


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
