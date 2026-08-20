# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Split CRM Custom",
    "summary": "Intake team, lead stages and Leads kanban before Sales",
    "version": "18.0.1.0.0",
    "category": "Sales/CRM",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/split-addons",
    "license": "AGPL-3",
    "development_status": "Beta",
    "maintainers": ["marcelsavegnago"],
    "depends": ["crm"],
    "data": [
        "data/crm_team.xml",
        "data/crm_stage.xml",
        "views/crm_lead_views.xml",
        "views/crm_menu_views.xml",
    ],
    "installable": True,
}
