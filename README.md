# NetBox Budget Plugin

A NetBox plugin for IT budget planning and tender/procurement tracking.

## Features

- **Budget Plans** — yearly IT purchase items with CAPEX/OPEX classification
- **Tenders** — procurement tender tracking linked to budget plans
- **Color-coded statuses** — Planned (gray), Active (cyan), Completed (green), Cancelled (red)
- **Auto-calculated fields** — Total Sum and Shortfall calculated automatically
- **KZT formatting** — readable number format (e.g. 26 854 560 KZT)
- **Site integration** — linked to NetBox Sites (Aqtau Office CC13 / Buzachi Field CC21)
- **Supplier integration** — linked to netbox_digital_assets Suppliers
- **Contract integration** — linked to netbox_digital_assets Contracts
- **Device integration** — Budget & Procurement panel visible on Device detail pages
- **Global search** — all objects searchable via NetBox global search
- **REST API** — full API support for all models
- **Year filtering** — filter budget items by year

## Compatibility

| Plugin Version | NetBox Version |
|---------------|----------------|
| 0.1           | 4.5.x          |

## Requirements

- [netbox-digital-assets](https://github.com/agabit/netbox-digital-assets) plugin

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/agabit/netbox-budget.git
cd netbox-budget
pip install -e .
```

### 2. Add to NetBox configuration

In `netbox/netbox/configuration.py`:

```python
PLUGINS = [
    'netbox_digital_assets',
    'netbox_budget',
]

PLUGINS_CONFIG = {
    'netbox_digital_assets': {},
    'netbox_budget': {},
}
```

### 3. Run migrations

```bash
python manage.py migrate netbox_budget
```

### 4. Restart NetBox

```bash
sudo systemctl restart netbox
```

## Models

### BudgetPlan
- Year, project name, PROXY number, nomenclature code
- Budget type: CAPEX / OPEX
- Site: Aqtau Office (CC13) / Buzachi Field (CC21) / 50/50%
- Unit: Quantity / Service / Set
- Price per unit, planned quantity, total sum (auto), agreed budget, shortfall (auto)
- Commercial proposal URL, tender name
- Links to Supplier, Contract, Device

### Tender
- Budget Plan (FK), tender name, status
- Start/end dates, responsible person, expected delivery date
- Links to Supplier, Winner Supplier, Contract

## Author

Aidarbek Gabit ([@agabit](https://github.com/agabit))

## Credits

This plugin was developed with the assistance of [Claude AI](https://claude.ai) by Anthropic.
The plugin architecture, models, views, forms, templates and all code were generated through
an interactive conversation with Claude AI, following the official NetBox plugin development
documentation and tutorial.

## License

Apache 2.0
