# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Split Website",
    "summary": "Public website for Split Studio: work, originals, reel and contact",
    "version": "18.0.1.0.0",
    "category": "Website",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/split-addons",
    "license": "AGPL-3",
    "development_status": "Beta",
    "maintainers": ["marcelsavegnago"],
    "depends": [
        "website",
        "website_crm",
        "website_mass_mailing",
    ],
    "data": [
        "data/ir_attachment_pre.xml",
        "data/website.xml",
        "data/website_view_home.xml",
        "data/website_view_reel.xml",
        "data/website_view_our_work.xml",
        "data/website_view_originals.xml",
        "data/website_view_about.xml",
        "data/website_view_contactus.xml",
        "data/website_view_projects.xml",
        "data/website_templates.xml",
        "data/website_page.xml",
        "data/website_menu.xml",
        "data/website_theme_apply.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "split_website/static/src/scss/split_website.scss",
        ],
    },
    "installable": True,
    "post_init_hook": "post_init_hook",
}
