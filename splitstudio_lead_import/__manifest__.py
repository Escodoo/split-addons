# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "SplitStudio Lead Import",
    "summary": "Import leads from XLSX/CSV with duplicate check.",
    "version": "18.0.1.0.0",
    "category": "CRM",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/split-addons",
    "license": "AGPL-3",
    "development_status": "Beta",
    "maintainers": ["escodoo"],
    "depends": ["crm"],
    "external_dependencies": {
        "python": ["openpyxl"],
    },
    "data": [
        "security/ir.model.access.csv",
        "wizards/lead_reassign_wizard_views.xml",
        "wizards/lead_import_wizard_views.xml",
        "views/wizard_list.xml",
        "views/crm_lead_readonly.xml",
        "views/crm_lead_conversion.xml",
        "views/menu_pipelines.xml",
    ],
    "installable": True,
    "application": False,
}
