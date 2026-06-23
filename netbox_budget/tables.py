import django_tables2 as tables
from netbox.tables import NetBoxTable
from .models import BudgetPlan, Tender, ItemCode


class ItemCodeTable(NetBoxTable):
    name = tables.LinkColumn(verbose_name="Name", attrs={"a": {"target": "_blank"}})
    status = tables.Column()
    short_name_rus = tables.Column(verbose_name="Short Name RUS")
    short_name_kaz = tables.Column(verbose_name="Short Name KAZ")

    def render_status(self, value, record):
        from django.utils.safestring import mark_safe
        colors = {
            "active": "success",
            "not_active": "secondary",
        }
        color = colors.get(record.status, "secondary")
        return mark_safe(
            f'<span class="badge bg-{color} text-white">{record.get_status_display()}</span>'
        )

    class Meta(NetBoxTable.Meta):
        model = ItemCode
        fields = (
            "pk", "id", "name", "short_name_rus", "short_name_kaz", "status", "cancelled_date",
        )
        default_columns = (
            "name", "short_name_rus", "short_name_kaz", "status",
        )


class BudgetPlanTable(NetBoxTable):
    year = tables.Column()
    status = tables.Column()
    project_name = tables.LinkColumn(
        verbose_name="Project Name",
        attrs={"a": {"target": "_blank"}}
    )
    proxy_number = tables.Column()
    budget_type = tables.Column()
    site_budget = tables.Column()
    unit = tables.Column()
    planned_quantity = tables.Column()
    price_per_unit = tables.Column()
    total_sum = tables.Column(
        verbose_name="Total Sum (KZT)",
        orderable=False
    )
    agreed_budget = tables.Column(
        verbose_name="Agreed Budget (KZT)",
    )
    shortfall = tables.Column(
        verbose_name="Shortfall (KZT)",
        orderable=False
    )
    supplier = tables.Column(linkify=True)
    contract = tables.Column(linkify=True)
    item_code = tables.ManyToManyColumn(
        verbose_name="Item Code",
        linkify_item=True
    )

    def render_status(self, value, record):
        from django.utils.safestring import mark_safe
        colors = {
            "draft": "secondary",
            "approved": "success",
            "cancelled": "danger",
            "donated": "purple",
        }
        color = colors.get(record.status, "secondary")
        return mark_safe(
            f'<span class="badge bg-{color} text-white">{record.get_status_display()}</span>'
        )

    def render_total_sum(self, value):
        return f"{abs(float(value)):,.0f} KZT".replace(",", " ")

    def render_agreed_budget(self, value):
        return f"{abs(float(value)):,.0f} KZT".replace(",", " ")

    def render_shortfall(self, value):
        value = float(value)
        formatted = f"{abs(value):,.0f}".replace(",", " ")
        if value > 0:
            return f"-{formatted} KZT"
        elif value < 0:
            return f"+{formatted} KZT"
        else:
            return "0 KZT"

    def render_price_per_unit(self, value):
        return f"{abs(float(value)):,.0f} KZT".replace(",", " ")

    def render_planned_quantity(self, value):
        value = float(value)
        if value == int(value):
            return str(int(value))
        return str(value)

    class Meta(NetBoxTable.Meta):
        model = BudgetPlan
        fields = (
            "pk", "id", "year", "status", "project_name", "proxy_number",
            "budget_type", "site_budget", "unit", "planned_quantity",
            "price_per_unit", "total_sum", "agreed_budget", "shortfall",
            "tender_name", "supplier", "contract", "item_code",
        )
        default_columns = (
            "id", "year", "status", "project_name", "proxy_number", "budget_type",
            "site_budget", "total_sum", "agreed_budget", "shortfall",
        )


class TenderTable(NetBoxTable):
    tender_name = tables.LinkColumn(attrs={"a": {"target": "_blank"}})
    budget_plans = tables.ManyToManyColumn(
        verbose_name="Budget Plans",
        linkify_item=True
    )
    budget_type = tables.Column(
        verbose_name="Budget Type",
        empty_values=()
    )
    status = tables.Column()
    supplier = tables.Column(linkify=True)
    winner_supplier = tables.Column(linkify=True)
    contract = tables.Column(linkify=True)

    def render_budget_type(self, record):
        types = record.budget_plans.values_list("budget_type", flat=True).distinct()
        return ", ".join([t.upper() for t in types]) if types else "—"

    def render_status(self, value, record):
        from django.utils.safestring import mark_safe
        colors = {
            "planned": "secondary",
            "active": "info",
            "completed": "success",
            "cancelled": "danger",
        }
        color = colors.get(record.status, "secondary")
        return mark_safe(
            f'<span class="badge bg-{color} text-white">{record.get_status_display()}</span>'
        )

    class Meta(NetBoxTable.Meta):
        model = Tender
        fields = (
            "pk", "id", "tender_name", "budget_plans", "budget_type", "status",
            "start_date", "end_date", "responsible_person",
            "supplier", "winner_supplier", "contract",
            "expected_delivery_date",
        )
        default_columns = (
            "tender_name", "budget_plans", "status",
            "start_date", "end_date", "winner_supplier", "contract",
        )
        row_attrs = {
            "class": lambda record: {
                "planned": "table-secondary",
                "active": "table-info",
                "completed": "table-success",
                "cancelled": "table-danger",
            }.get(record.status, "")
        }
