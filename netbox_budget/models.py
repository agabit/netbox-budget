from django.db import models
from django.utils import timezone
from netbox.models import NetBoxModel

class ItemCode(NetBoxModel):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('not_active', 'Not Active'),
    ]

    name = models.CharField(max_length=500, verbose_name='Name')
    short_name_kaz = models.CharField(max_length=1000, blank=True, verbose_name='Short Name KAZ')
    specification_kaz = models.TextField(blank=True, verbose_name='Specification KAZ')
    short_name_rus = models.CharField(max_length=1000, blank=True, verbose_name='Short Name RUS')
    specification_rus = models.TextField(blank=True, verbose_name='Specification RUS')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    pdf_file = models.FileField(
        upload_to='item_codes/',
        null=True,
        blank=True,
        verbose_name='Commercial Proposal (PDF)'
    )
    cancelled_date = models.DateField(null=True, blank=True, verbose_name='Cancelled Date')
    comments = models.TextField(blank=True, verbose_name='Comments')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Delete old PDF if replaced
        if self.pk:
            try:
                old = ItemCode.objects.get(pk=self.pk)
                if old.pdf_file and old.pdf_file != self.pdf_file:
                    import os
                    if os.path.isfile(old.pdf_file.path):
                        os.remove(old.pdf_file.path)
            except ItemCode.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete PDF file when record is deleted
        import os
        if self.pdf_file and os.path.isfile(self.pdf_file.path):
            os.remove(self.pdf_file.path)
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('plugins:netbox_budget:itemcode', args=[self.pk])

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
    item_code = models.ForeignKey(
        'ItemCode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='budget_plans',
        verbose_name='Item Code'
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

    comments = models.TextField(blank=True, verbose_name='Comments')
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
    budget_plans = models.ManyToManyField(
        BudgetPlan,
        related_name='tenders',
        blank=True
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
    contract_sum = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Contract Sum (KZT)'
    )

    comments = models.TextField(blank=True, verbose_name='Comments')
    class Meta:
        ordering = ['tender_name']

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

    @property
    def economy(self):
        if not self.contract_sum:
            return None
        total_agreed = sum(p.agreed_budget for p in self.budget_plans.all())
        return total_agreed - self.contract_sum

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
