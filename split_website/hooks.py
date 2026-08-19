# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import logging
from pathlib import Path

from odoo.modules.module import get_module_path

_logger = logging.getLogger(__name__)

COMPANY_VALUES = {
    "email": "contato@splitstudio.tv",
    "phone": "+55 11 91366 8953",
    "city": "São Paulo",
    "website": "https://splitstudio.tv",
}

MENU_NAMES = {
    "/": "Home",
    "/contactus": "Contact",
}

# The header and footer variants ship hard-coded sample contact details, so the
# only way to brand them is to patch the shipped arch.
BRANDED_VIEWS = (
    "website.header_text_element",
    "website.footer_custom",
    "website.footer_copyright_company_name",
)

BRANDING_REPLACEMENTS = (
    ("info@yourcompany.example.com", "contato@splitstudio.tv"),
    ("Company name</span>", "Split Studio</span>"),
    ("+1 555-555-5556", "+55 11 91366 8953"),
    ('<a href="#">About us</a>', '<a href="/about">About</a>'),
    ('<a href="#">Products</a>', '<a href="/our-work">Our Work</a>'),
    ('<a href="#">Services</a>', '<a href="/split-originals">Split Originals</a>'),
    ('<a href="#">Legal</a>', '<a href="/reel">Reel</a>'),
    ('<a href="/extra">Extra Page</a>', '<a href="/privacy">Privacy</a>'),
    ('<a href="/extra">Extra page</a>', '<a href="/privacy">Privacy</a>'),
    ('aria-label="Extra page"', 'aria-label="Home"'),
    ('aria-label="Extra Page"', 'aria-label="Home"'),
    (
        "We are a team of passionate people whose goal is to improve everyone's "
        "life through disruptive products. We build great products to solve your "
        "business problems.",
        "Split is an animation and games studio. Since 2009 we create, develop and "
        "produce animated stories for channels, studios, agencies and brands "
        "around the world.",
    ),
    (
        "Our products are designed for small to medium size companies willing to "
        "optimize their performance.",
        "If there's 2D animation, Split can do it.",
    ),
)


# ERP chrome that the studio site never shows.
HIDDEN_HEADER_VIEWS = (
    "website.header_search_box",
    "website.header_text_element",
    "website.header_call_to_action",
    "portal.user_sign_in",
)


def post_init_hook(env):
    """Serve the public site in English and align the studio contact details."""
    _serve_website_languages(env)
    _rename_default_menus(env)
    _brand_header_and_footer(env)
    _brand_social(env)
    _hide_erp_chrome(env)
    _hide_extra_page(env)
    _overlay_public_headers(env)
    _refresh_client_logos(env)
    # base.main_company is a noupdate record, so its data cannot be set from XML.
    env.company.write(COMPANY_VALUES)


def _serve_website_languages(env):
    """English is the source language; Portuguese is loaded from i18n."""
    english = env["res.lang"]._activate_lang("en_US")
    portuguese = env["res.lang"]._activate_lang("pt_BR")
    if not english:
        _logger.warning("Split Website: en_US is unavailable, keeping the site locale")
        return
    langs = english
    if portuguese:
        langs |= portuguese
    website = env.ref("website.default_website")
    website.write(
        {"language_ids": [(6, 0, langs.ids)], "default_lang_id": english.id}
    )


def _rename_default_menus(env):
    """Keep inherited menus in the English source language."""
    menus = env["website.menu"].search(
        [
            ("website_id", "=", env.ref("website.default_website").id),
            ("url", "in", list(MENU_NAMES)),
        ]
    )
    for menu in menus.with_context(lang="en_US"):
        menu.name = MENU_NAMES[menu.url]


def _brand_header_and_footer(env):
    """Replace the sample contact details of the shipped header and footer."""
    website_id = env.ref("website.default_website").id
    website = env["website"].with_context(website_id=website_id)
    for key in BRANDED_VIEWS:
        view = website.viewref(key)
        arch = view.arch
        branded_arch = arch
        for sample, branded in BRANDING_REPLACEMENTS:
            branded_arch = branded_arch.replace(sample, branded)
        if branded_arch != arch:
            view.write({"arch": branded_arch})
    # Writing on a shipped view yields a website-specific copy, so read them again.
    archs = "".join(website.viewref(key).arch for key in BRANDED_VIEWS)
    for sample, branded in BRANDING_REPLACEMENTS:
        if branded not in archs:
            _logger.warning("Split Website: could not brand the sample text %r", sample)


def _brand_social(env):
    """website.xml is noupdate; keep the official LinkedIn on existing databases."""
    website = env.ref("website.default_website")
    website.write(
        {"social_linkedin": "https://br.linkedin.com/company/splitstudio"}
    )


def _hide_extra_page(env):
    """Drop the sample Extra page the Website module ships with."""
    website_id = env.ref("website.default_website").id
    menus = env["website.menu"].search(
        [
            ("website_id", "=", website_id),
            ("name", "ilike", "extra"),
        ]
    )
    if menus:
        menus.write({"is_visible": False})
    pages = env["website.page"].search(
        [
            ("website_id", "=", website_id),
            "|",
            ("name", "ilike", "extra"),
            ("url", "in", ("/extra", "/page/extra")),
        ]
    )
    if pages:
        pages.write({"is_published": False})


def _hide_erp_chrome(env):
    """Drop search, phone, Sign in and the Contact Us button from the header."""
    website_id = env.ref("website.default_website").id
    website = env["website"].with_context(website_id=website_id)
    for key in HIDDEN_HEADER_VIEWS:
        view = website.viewref(key)
        if view.active:
            view.write({"active": False})


def _overlay_public_headers(env):
    """Let the first artwork sit under a transparent header, like the studio site."""
    pages = env["website.page"].search(
        [("website_id", "=", env.ref("website.default_website").id)]
    )
    pages.write({"header_overlay": True})


def _refresh_client_logos(env):
    """Reload knocked-out PNGs even when the attachment records are noupdate."""
    binary_dir = (
        Path(get_module_path("split_website")) / "static/src/binary/ir_attachment"
    )
    for path in binary_dir.glob("client_*"):
        attachment = env.ref(f"split_website.{path.stem}", raise_if_not_found=False)
        if not attachment:
            continue
        attachment.write(
            {
                "name": path.name,
                "mimetype": "image/png",
                "datas": base64.b64encode(path.read_bytes()),
            }
        )
