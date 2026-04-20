from netbox.plugins.navigation import PluginMenu, PluginMenuButton, PluginMenuItem

menu = PluginMenu(
    label='Budget',
    groups=(
        ('Planning', (
            PluginMenuItem(
                link='plugins:netbox_budget:budgetplan_list',
                link_text='Budget Plans',
                buttons=(
                    PluginMenuButton(
                        link='plugins:netbox_budget:budgetplan_add',
                        title='Add',
                        icon_class='mdi mdi-plus-thick',
                    ),
                ),
            ),
            PluginMenuItem(
                link='plugins:netbox_budget:tender_list',
                link_text='Tenders',
                buttons=(
                    PluginMenuButton(
                        link='plugins:netbox_budget:tender_add',
                        title='Add',
                        icon_class='mdi mdi-plus-thick',
                    ),
                ),
            ),
        )),
    ),
    icon_class='mdi mdi-cash-multiple',
)
