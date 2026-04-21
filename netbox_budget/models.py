from django.db import models
from netbox.models import NetBoxModel


class BudgetPlan(NetBoxModel):

    YEAR_CHOICES = [(y, str(y)) for y in range(2024, 2051)]

    BUDGET_TYPE_CHOICES = [
        ('capex', 'CAPEX'),
        ('opex', 'OPEX'),
    ]

    SITE_CHOICES = [
        ('cc13', 'Aqtau Office (CC13)'),
        ('cc21', 'Buzachi Field (CC21)'),
        ('5050', '50/50% Aqtau+Buzachi'),
    ]

    UNIT_CHOICES = [
        ('qty', 'Quantity'),
        ('work', 'Service'),
        ('set', 'Set'),
    ]
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
        ('donated', 'Donated'),
    ]
    NOMENCLATURE_CHOICES = [
        ('need', 'Need item code'),
    ]

    # Identity
    year = models.IntegerField(choices=YEAR_CHOICES)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    project_name = models.CharField(max_length=300)
    proxy_number = models.CharField(max_length=100, blank=True)
    nomenclature_code = models.CharField(
        max_length=200,
        blank=True,
        help_text='Nomenclature item code or "Need item code"'
    )
    device = models.ForeignKey(
        'dcim.Device',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='budget_plans',
        help_text='Link to existing NetBox device'
    )

    # Classification
    budget_type = models.CharField(
        max_length=10,
        choices=BUDGET_TYPE_CHOICES,
        default='capex'
    )
    site_budget = models.CharField(
        max_length=10,
        choices=SITE_CHOICES,
        default='cc13'
    )

    # Financial
    unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        default='qty'
    )
    planned_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1
    )
    price_per_unit = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0
    )
    agreed_budget = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0
    )

    # Documents
    commercial_proposal_url = models.CharField(
        max_length=500,
        blank=True,
        help_text='Network path or URL to commercial proposal file'
    )
    tender_name = models.CharField(max_length=300, blank=True)

    # Links
    supplier = models.ForeignKey(
        'netbox_digital_assets.Supplier',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='budget_plans'
    )
    contract = models.ForeignKey(
        'netbox_digital_assets.Contract',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='budget_plans'
    )

    class Meta:
        ordering = ['-year', 'project_name']

    def __str__(self):
        return f'[{self.year}] {self.project_name}'

    @property
    def total_sum(self):
        return self.planned_quantity * self.price_per_unit

    @property
    def shortfall(self):
        return self.total_sum - self.agreed_budget

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('plugins:netbox_budget:budgetplan', args=[self.pk])


class Tender(NetBoxModel):

    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    STATUS_COLORS = {
        'planned': 'secondary',
        'active': 'info',
        'completed': 'success',
        'cancelled': 'danger',
    }

    # Link to BudgetPlan
    budget_plan = models.ForeignKey(
        BudgetPlan,
        on_delete=models.PROTECT,
        related_name='tenders'
    )

    # Tender specific
    tender_name = models.CharField(max_length=300)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned'
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    responsible_person = models.CharField(max_length=200, blank=True)

    # Supplier & Contract (filled when Completed)
    supplier = models.ForeignKey(
        'netbox_digital_assets.Supplier',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tenders'
    )
    winner_supplier = models.ForeignKey(
        'netbox_digital_assets.Supplier',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='won_tenders'
    )
    contract = models.ForeignKey(
        'netbox_digital_assets.Contract',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tenders'
    )
    expected_delivery_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-budget_plan__year', 'tender_name']

    def __str__(self):
        return f'{self.tender_name} ({self.get_status_display()})'

    @property
    def status_color(self):
        colors = {
            'planned': 'secondary',
            'active': 'info',
            'completed': 'success',
            'cancelled': 'danger',
        }
        return colors.get(self.status, 'secondary')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('plugins:netbox_budget:tender', args=[self.pk])

class BudgetMerge(NetBoxModel):
    source_plan = models.ForeignKey(
        BudgetPlan,
        on_delete=models.PROTECT,
        related_name='donations_made',
        verbose_name='Donor Project'
    )
    target_plan = models.ForeignKey(
        BudgetPlan,
        on_delete=models.PROTECT,
        related_name='donations_received',
        verbose_name='Receiver Project'
    )
    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name='Amount (KZT)'
    )
    date = models.DateField(
        auto_now_add=True
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.source_plan} → {self.target_plan}: {self.amount} KZT"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('plugins:netbox_budget:budgetmerge', args=[self.pk])
