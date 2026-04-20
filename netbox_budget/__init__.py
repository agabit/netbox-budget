from netbox.plugins import PluginConfig


class BudgetConfig(PluginConfig):
    name = 'netbox_budget'
    verbose_name = 'Budget'
    description = 'Budget planning and tender tracking for NetBox'
    version = '0.1'
    author = 'Gabit Aidarbek'
    author_email = 'gabit.aidarbek@gmail.com'
    base_url = 'budget'
    search_extensions = 'search'

config = BudgetConfig
