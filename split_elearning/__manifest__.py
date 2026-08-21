# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Split eLearning",
    "summary": "Academy course catalog on eLearning with an Intake CRM tag",
    "version": "18.0.1.0.0",
    "category": "Website/eLearning",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/split-addons",
    "license": "AGPL-3",
    "development_status": "Beta",
    "maintainers": ["marcelsavegnago"],
    "depends": [
        "website_slides",
        "split_crm_custom",
    ],
    "data": [
        "data/slide_channel_tag.xml",
        "data/slide_channel.xml",
        "data/slide_slide.xml",
        "data/crm_tag.xml",
        "data/website_menu.xml",
    ],
    "installable": True,
}
