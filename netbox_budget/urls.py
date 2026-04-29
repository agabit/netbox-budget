from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from . import views, models

urlpatterns = [
    # Item Codes
    path("item-codes/", views.ItemCodeListView.as_view(), name="itemcode_list"),
    path("item-codes/add/", views.ItemCodeEditView.as_view(), name="itemcode_add"),
    path("item-codes/<int:pk>/", views.ItemCodeView.as_view(), name="itemcode"),
    path("item-codes/<int:pk>/edit/", views.ItemCodeEditView.as_view(), name="itemcode_edit"),
    path("item-codes/<int:pk>/delete/", views.ItemCodeDeleteView.as_view(), name="itemcode_delete"),
    path("item-codes/<int:pk>/changelog/", ObjectChangeLogView.as_view(), name="itemcode_changelog", kwargs={"model": models.ItemCode}),

    # Budget Plans
    path("budget-plans/", views.BudgetPlanListView.as_view(), name="budgetplan_list"),
    path("budget-plans/add/", views.BudgetPlanEditView.as_view(), name="budgetplan_add"),
    path("budget-plans/<int:pk>/", views.BudgetPlanView.as_view(), name="budgetplan"),
    path("budget-plans/<int:pk>/edit/", views.BudgetPlanEditView.as_view(), name="budgetplan_edit"),
    path("budget-plans/<int:pk>/delete/", views.BudgetPlanDeleteView.as_view(), name="budgetplan_delete"),
    path("budget-plans/<int:pk>/changelog/", ObjectChangeLogView.as_view(), name="budgetplan_changelog", kwargs={"model": models.BudgetPlan}),
    path("budget-plans/<int:pk>/donate/", views.DonateBudgetView.as_view(), name="budgetplan_donate"),

    # Tenders
    path("tenders/", views.TenderListView.as_view(), name="tender_list"),
    path("tenders/add/", views.TenderEditView.as_view(), name="tender_add"),
    path("tenders/<int:pk>/", views.TenderView.as_view(), name="tender"),
    path("tenders/<int:pk>/edit/", views.TenderEditView.as_view(), name="tender_edit"),
    path("tenders/<int:pk>/delete/", views.TenderDeleteView.as_view(), name="tender_delete"),
    path("tenders/<int:pk>/changelog/", ObjectChangeLogView.as_view(), name="tender_changelog", kwargs={"model": models.Tender}),
]
