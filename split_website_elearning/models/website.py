# Copyright 2026 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import ast
import base64
import json
import re
from pathlib import Path

from odoo import api, models
from odoo.modules.module import get_module_path

_WHITESPACE_RE = re.compile(r"\s+")

ACADEMY_CHANNEL_XMLIDS = (
    "slide_channel_backgrounds",
    "slide_channel_cutout_acting",
    "slide_channel_cutout_harmony",
    "slide_channel_rigs_harmony",
    "slide_channel_visual_development",
    "slide_channel_creative_writing",
    "slide_channel_production",
)

# Stock website_slides covers default to Odoo purple (#875A7B).
ACADEMY_COURSE_COVER_PROPERTIES = {
    "background_color_class": "",
    "background_color_style": "background-color: #003f59; background-image: none;",
    "opacity": "0",
    "resize_class": "cover_auto",
}

# Stock gamification badges are gold circles with "1st" / numbers.
ACADEMY_RANK_IMAGES = (
    ("gamification.rank_newbie", "newbie.svg"),
    ("gamification.rank_student", "student.svg"),
    ("gamification.rank_bachelor", "bachelor.svg"),
    ("gamification.rank_master", "master.svg"),
    ("gamification.rank_doctor", "doctor.svg"),
)

ACADEMY_MENUS = (
    ("/", "Home", "Home", 10),
    ("/slides", "Courses", "Cursos", 20),
    ("/about", "About", "Sobre", 30),
    ("/educators", "Educators", "Educadores", 40),
    ("/contactus", "Contact", "Contato", 50),
)


class Website(models.Model):
    _inherit = "website"

    @api.model
    def _split_website_elearning_setup(self):
        """Keep the Academia site on its own menus and course catalog."""
        academy = self.env.ref(
            "split_website_elearning.website_academia", raise_if_not_found=False
        )
        if not academy:
            return
        self._split_configure_academy_website(academy)
        self._split_brand_academy_website(academy)
        self._split_brand_academy_ranks()
        self._split_bind_academy_channels(academy)
        self._split_serve_academy_languages(academy)
        self._split_hide_studio_courses_menu()
        self._split_setup_academy_menus(academy)
        self._split_sync_academy_view_translations(academy)

    @api.model
    def _split_configure_academy_website(self, academy):
        values = {
            "homepage_url": False,
            "domain": academy.domain or "http://academia.localhost",
        }
        intake = self.env.ref(
            "split_crm_custom.crm_team_intake", raise_if_not_found=False
        )
        if intake:
            values["crm_default_team_id"] = intake.id
        academy.write(values)

    @api.model
    def _split_brand_academy_website(self, academy):
        module_path = Path(get_module_path("split_website_elearning"))
        logo = module_path / "static/src/img/brand/logo.png"
        favicon = module_path / "static/src/img/brand/favicon.png"
        values = {
            "social_instagram": "https://www.instagram.com/splitacademia/",
            "social_linkedin": (
                "https://www.linkedin.com/company/instituto-de-inova%C3%A7%C3%A3o-split"
            ),
            "social_youtube": (
                "https://www.youtube.com/@InstitutodeInova%C3%A7%C3%A3oSplit"
            ),
            "social_facebook": False,
            "social_twitter": False,
        }
        if logo.is_file():
            values["logo"] = base64.b64encode(logo.read_bytes())
        if favicon.is_file():
            values["favicon"] = base64.b64encode(favicon.read_bytes())
        academy.write(values)

    @api.model
    def _split_brand_academy_ranks(self):
        ranks_dir = Path(get_module_path("split_website_elearning")) / (
            "static/src/img/ranks"
        )
        stock_badge = re.compile(r"/gamification/static/img/rank_[a-z]+_badge\.svg")
        for xmlid, filename in ACADEMY_RANK_IMAGES:
            rank = self.env.ref(xmlid, raise_if_not_found=False)
            path = ranks_dir / filename
            if not rank:
                continue
            values = {}
            if path.is_file():
                values["image_1920"] = base64.b64encode(path.read_bytes())
            if values:
                rank.write(values)
            new_src = f"/split_website_elearning/static/src/img/ranks/{filename}"
            for lang in ("en_US", "pt_BR"):
                mot = rank.with_context(lang=lang).description_motivational or ""
                updated = stock_badge.sub(new_src, mot)
                if updated != mot:
                    rank.with_context(lang=lang).write(
                        {"description_motivational": updated}
                    )

    @api.model
    def _split_bind_academy_channels(self, academy):
        channels = self.env["slide.channel"]
        for xmlid in ACADEMY_CHANNEL_XMLIDS:
            channel = self.env.ref(
                f"split_website_elearning.{xmlid}", raise_if_not_found=False
            )
            if channel:
                channels |= channel
        if channels:
            channels.write({"website_id": academy.id})
            for channel in channels:
                props = {}
                if channel.cover_properties:
                    try:
                        props = json.loads(channel.cover_properties)
                    except (TypeError, ValueError):
                        props = {}
                props.update(ACADEMY_COURSE_COVER_PROPERTIES)
                channel.cover_properties = json.dumps(props)

    @api.model
    def _split_serve_academy_languages(self, academy):
        english = self.env["res.lang"]._activate_lang("en_US")
        portuguese = self.env["res.lang"]._activate_lang("pt_BR")
        if not english:
            return
        langs = english
        if portuguese:
            langs |= portuguese
        academy.write(
            {"language_ids": [(6, 0, langs.ids)], "default_lang_id": english.id}
        )

    @api.model
    def _split_hide_studio_courses_menu(self):
        studio = self.env.ref("website.default_website", raise_if_not_found=False)
        if not studio:
            return
        self.env["website.menu"].search(
            [("website_id", "=", studio.id), ("url", "=", "/slides")]
        ).unlink()

    @api.model
    def _split_setup_academy_menus(self, academy):
        top = self.env["website.menu"].search(
            [("website_id", "=", academy.id), ("parent_id", "=", False)],
            limit=1,
        )
        if not top:
            return
        keep_urls = {url for url, _en, _pt, _sequence in ACADEMY_MENUS}
        extra = top.child_id.filtered(lambda menu: menu.url not in keep_urls)
        extra.unlink()
        top.invalidate_recordset(["child_id"])
        for url, name_en, name_pt, sequence in ACADEMY_MENUS:
            matches = top.child_id.filtered(lambda menu: menu.url == url)
            keep = matches[:1]
            (matches - keep).unlink()
            values = {
                "name": name_en,
                "url": url,
                "website_id": academy.id,
                "parent_id": top.id,
                "sequence": sequence,
            }
            if keep:
                menu = keep
                menu.with_context(lang="en_US").write(values)
            else:
                menu = self.env["website.menu"].with_context(lang="en_US").create(
                    values
                )
            menu.with_context(lang="pt_BR").write({"name": name_pt})

    @api.model
    def _split_collapse_term(self, term):
        collapsed = _WHITESPACE_RE.sub(" ", term or "").strip()
        return (
            collapsed.replace("&amp;", "&")
            .replace("&lt;", "<")
            .replace("&gt;", ">")
        )

    @api.model
    def _split_read_po_pairs(self):
        """Read collapsed msgid -> msgstr pairs from the module pt_BR catalog."""
        path = Path(get_module_path("split_website_elearning")) / "i18n" / "pt_BR.po"
        if not path.is_file():
            return {}
        pairs = {}
        state = None
        msgid_parts = []
        msgstr_parts = []

        def _flush():
            if not msgid_parts:
                return
            source = "".join(msgid_parts)
            value = "".join(msgstr_parts)
            if source and value:
                pairs[self._split_collapse_term(source)] = value

        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line.startswith("msgid "):
                _flush()
                state = "msgid"
                msgid_parts = [ast.literal_eval(line[6:])]
                msgstr_parts = []
            elif line.startswith("msgstr "):
                state = "msgstr"
                msgstr_parts = [ast.literal_eval(line[7:])]
            elif line.startswith('"') and state == "msgid":
                msgid_parts.append(ast.literal_eval(line))
            elif line.startswith('"') and state == "msgstr":
                msgstr_parts.append(ast.literal_eval(line))
        _flush()
        return pairs

    @api.model
    def _split_apply_po_terms_to_view(self, view, pairs, lang="pt_BR"):
        if not view or not pairs:
            return
        terms, _ctx = view.get_field_translations("arch_db", langs=[lang])
        mapping = {}
        seen = set()
        for item in terms:
            source = item.get("source") or ""
            if not source or source in seen:
                continue
            seen.add(source)
            value = pairs.get(self._split_collapse_term(source))
            if value:
                mapping[source] = value
        if mapping:
            view.update_field_translations("arch_db", {lang: mapping})

    @api.model
    def _split_academy_translation_views(self, academy):
        xmlids = (
            "homepage",
            "about",
            "educators",
            "contactus",
            "layout",
            "courses_home",
            "courses_all",
            "contact_form",
            "newsletter_form",
        )
        views = self.env["ir.ui.view"]
        for xmlid in xmlids:
            view = self.env.ref(
                f"split_website_elearning.{xmlid}", raise_if_not_found=False
            )
            if view:
                views |= view
        if academy:
            views |= self.env["ir.ui.view"].search(
                [
                    ("website_id", "=", academy.id),
                    ("key", "in", ("website.homepage", "website.contactus")),
                ]
            )
        return views

    @api.model
    def _split_lookup_po(self, source, pairs):
        collapsed = self._split_collapse_term(source)
        if collapsed in pairs:
            return pairs[collapsed]
        inner = re.sub(r"^<p>(.*)</p>$", r"\1", collapsed, flags=re.I | re.S)
        inner = self._split_collapse_term(inner)
        if inner in pairs:
            value = pairs[inner]
            stripped = (source or "").strip()
            if stripped.startswith("<p") and not value.startswith("<"):
                return f"<p>{value}</p>"
            return value
        return None

    @api.model
    def _split_apply_po_to_field(self, record, field_name, pairs, lang="pt_BR"):
        if not record or field_name not in record._fields:
            return
        field = record._fields[field_name]
        if field.translate is True:
            source = record.with_context(lang="en_US")[field_name]
            if not source:
                return
            value = self._split_lookup_po(str(source), pairs)
            if value:
                record.update_field_translations(field_name, {lang: value})
            return
        terms, _ctx = record.get_field_translations(field_name, langs=[lang])
        mapping = {}
        seen = set()
        for item in terms:
            source = item.get("source") or ""
            if not source or source in seen:
                continue
            seen.add(source)
            value = self._split_lookup_po(source, pairs)
            if value:
                mapping[source] = value
        if mapping:
            record.update_field_translations(field_name, {lang: mapping})

    @api.model
    def _split_sync_academy_record_translations(self, pairs):
        for xmlid in ACADEMY_CHANNEL_XMLIDS:
            channel = self.env.ref(
                f"split_website_elearning.{xmlid}", raise_if_not_found=False
            )
            if not channel:
                continue
            self._split_apply_po_to_field(channel, "name", pairs)
            self._split_apply_po_to_field(channel, "description", pairs)
            for slide in channel.slide_ids:
                self._split_apply_po_to_field(slide, "name", pairs)
                self._split_apply_po_to_field(slide, "description", pairs)
                self._split_apply_po_to_field(slide, "html_content", pairs)
        for xmlid in ("page_about", "page_educators"):
            page = self.env.ref(
                f"split_website_elearning.{xmlid}", raise_if_not_found=False
            )
            if page:
                self._split_apply_po_to_field(
                    page, "website_meta_description", pairs
                )

    @api.model
    def _split_sync_academy_view_translations(self, academy=None):
        """Apply pt_BR terms even when COW copies or HTML wrappers differ."""
        academy = academy or self.env.ref(
            "split_website_elearning.website_academia", raise_if_not_found=False
        )
        if not academy:
            return
        pairs = self._split_read_po_pairs()
        if not pairs:
            return
        for view in self._split_academy_translation_views(academy):
            self._split_apply_po_terms_to_view(view, pairs)
        self._split_sync_academy_record_translations(pairs)
