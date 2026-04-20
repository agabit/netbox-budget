import django_tables2 as tables
from netbox.tables import NetBoxTable
from .models import BudgetPlan, Tender


class BudgetPlanTable(NetBoxTable):
    year = tables.Column()
    project_name = tables.Column(linkify=True)
    proxy_number = tables.Column()
    budget_type = tables.Column()
    site_budget = tables.Column()
    unit = tables.Column()
    planned_quantity = tables.Column()
    price_per_unit = tables.Column()
    total_sum = tables.Column(
        verbose_name='Total Sum (KZT)',
        orderable=False
    )
    agreed_budget = tables.Column()
    shortfall = tables.Column(
        verbose_name='Shortfall (KZT)',
        orderable=False
    )
    supplier = tables.Column(linkify=True)
    contract = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = BudgetPlan
        fields = (
            'pk', 'id', 'year', 'project_name', 'proxy_number',
            'budget_type', 'site_budget', 'unit', 'planned_quantity',
            'price_per_unit', 'total_sum', 'agreed_budget', 'shortfall',
            'tender_name', 'supplier', 'contract',
        )
        default_columns = (
            'year', 'project_name', 'proxy_number', 'budget_type',
            'site_budget', 'total_sum', 'agreed_budget', 'shortfall',
        )


class TenderTable(NetBoxTable):
    tender_name = tables.Column(linkify=True)
    budget_plan = tables.Column(linkify=True)
    status = tables.Column()
    supplier = tables.Column(linkify=True)
    winner_supplier = tables.Column(linkify=True)
    contract = tables.Column(linkify=True)

    def render_status(self, value, record):
        from django.utils.safestring import mark_safe
        colors = {
            'planned': 'secondary',
            'active': 'info',
            'completed': 'success',
            'cancelled': 'danger',
        }
        color = colors.get(record.status, 'secondary')
        return mark_safe(
            f'<span class="badge bg-{color} text-white">{record.get_status_display()}</span>'
        )

    def get_row_class(self, record):
        colors = {
            'planned': 'table-secondary',
            'active': 'table-info',
            'completed': 'table-success',
            'cancelled': 'table-danger',
        }
        return colors.get(record.status, '')

    class Meta(NetBoxTable.Meta):
        model = Tender
        fields = (
            'pk', 'id', 'tender_name', 'budget_plan', 'status',
            'start_date', 'end_date', 'responsible_person',
            'supplier', 'winner_supplier', 'contract',
            'expected_delivery_date',
        )
        default_columns = (
            'tender_name', 'budget_plan', 'status',
            'start_date', 'end_date', 'winner_supplier', 'contract',
        )
        row_attrs = {
            'class': lambda record: {
                'planned': 'table-secondary',
                'active': 'table-info',
                'completed': 'table-success',
                'cancelled': 'table-danger',
            }.get(record.status, '')
        }
