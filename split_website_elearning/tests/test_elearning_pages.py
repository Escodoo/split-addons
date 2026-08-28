# Copyright 2026 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
from pathlib import Path

from odoo.modules.module import get_module_path
from odoo.tests import HttpCase, tagged

CHANNEL_XMLIDS = (
    "slide_channel_backgrounds",
    "slide_channel_cutout_acting",
    "slide_channel_cutout_harmony",
    "slide_channel_rigs_harmony",
    "slide_channel_visual_development",
    "slide_channel_creative_writing",
    "slide_channel_production",
)

ACADEMY_MENU_URLS = ("/", "/slides", "/about", "/educators", "/contactus")


@tagged("post_install", "-at_install")
class TestSplitWebsiteElearningPages(HttpCase):
    def _academy(self):
        return self.env.ref("split_website_elearning.website_academia")

    def _channel(self, xmlid):
        return self.env.ref(f"split_website_elearning.{xmlid}")

    def _open_academy(self, path):
        return self.url_open(path, headers={"Host": "academia.localhost"})

    def test_catalog_lists_academy_courses(self):
        names = (
            self.env["slide.channel"]
            .with_context(lang="en_US")
            .search(
                [
                    (
                        "id",
                        "in",
                        [self._channel(xmlid).id for xmlid in CHANNEL_XMLIDS],
                    )
                ]
            )
            .mapped("name")
        )
        self.assertEqual(len(names), 7)
        self.assertIn("The Art of Creating Backgrounds", names)
        self.assertIn("Cut-out Acting – Bringing Characters to Life", names)
        self.assertIn("Cut-out Animation in Toon Boom Harmony", names)
        self.assertIn("Creating Rigs in Toon Boom Harmony", names)
        self.assertIn("Visual Development – Building Worlds", names)
        self.assertIn("Creative Writing for Animation Projects", names)
        self.assertIn("Production and Planning for 2D Animation Projects", names)

    def test_courses_are_public_and_published(self):
        channels = self.env["slide.channel"].browse(
            [self._channel(xmlid).id for xmlid in CHANNEL_XMLIDS]
        )
        self.assertTrue(all(channel.is_published for channel in channels))
        self.assertTrue(all(channel.visibility == "public" for channel in channels))
        self.assertTrue(all(channel.enroll == "public" for channel in channels))
        self.assertTrue(all(channel.image_1920 for channel in channels))
        featured = self._channel("slide_channel_backgrounds")
        self.assertTrue(featured.website_url)
        self.assertIn("/slides/", featured.website_url)

    def test_courses_belong_to_academia_website(self):
        academy = self._academy()
        self.assertEqual(academy.name, "Split Academia")
        self.assertFalse(academy.homepage_url)
        channels = self.env["slide.channel"].browse(
            [self._channel(xmlid).id for xmlid in CHANNEL_XMLIDS]
        )
        self.assertTrue(all(channel.website_id == academy for channel in channels))
        intake = self.env.ref("split_crm_custom.crm_team_intake")
        self.assertEqual(academy.crm_default_team_id, intake)

    def test_featured_course_shows_about_and_instructor(self):
        channel = self._channel("slide_channel_backgrounds").with_context(lang="en_US")
        lesson_names = channel.slide_ids.mapped("name")
        self.assertIn("About the course", lesson_names)
        self.assertIn("Instructor", lesson_names)
        self.assertIn("Beatriz Gondim", lesson_names)
        self.assertIn("Build a production background", lesson_names)
        about = self.env.ref("split_website_elearning.slide_lesson_backgrounds_about")
        self.assertTrue(about.is_preview)
        practice = self.env.ref(
            "split_website_elearning.slide_lesson_backgrounds_practice"
        )
        self.assertFalse(practice.is_preview)

    def test_each_course_has_about_and_practice(self):
        samples = (
            (
                "slide_channel_cutout_acting",
                "slide_lesson_cutout_acting_practice",
                "Animate a thought change",
                "Luiz do Futuro",
            ),
            (
                "slide_channel_cutout_harmony",
                "slide_lesson_cutout_harmony_practice",
                "Build a walk cycle",
                "Luiz do Futuro",
            ),
            (
                "slide_channel_rigs_harmony",
                "slide_lesson_rigs_harmony_practice",
                "Rig a simple puppet",
                "Luiz do Futuro",
            ),
            (
                "slide_channel_visual_development",
                "slide_lesson_visual_development_practice",
                "Build a color script",
                "Ana Maria Sena",
            ),
            (
                "slide_channel_creative_writing",
                "slide_lesson_creative_writing_practice",
                "Write a one-page pitch",
                "Bruno Antonio",
            ),
            (
                "slide_channel_production",
                "slide_lesson_production_practice",
                "Write a production plan",
                "Belisa Proença",
            ),
        )
        for channel_xmlid, practice_xmlid, practice_name, instructor in samples:
            channel = self._channel(channel_xmlid).with_context(lang="en_US")
            names = channel.slide_ids.mapped("name")
            self.assertIn("About the course", names, channel_xmlid)
            self.assertIn(practice_name, names, channel_xmlid)
            self.assertIn(instructor, names, channel_xmlid)
            practice = self.env.ref(f"split_website_elearning.{practice_xmlid}")
            self.assertFalse(practice.is_preview, practice_xmlid)

    def test_academy_crm_tag_exists(self):
        tag = self.env.ref("split_website_elearning.crm_tag_academy")
        self.assertEqual(tag.with_context(lang="en_US").name, "Academy")
        intake = self.env.ref("split_crm_custom.crm_team_intake")
        self.assertTrue(intake.exists())

    def test_academia_menus_and_studio_hides_courses(self):
        academy = self._academy()
        studio = self.env.ref("website.default_website")
        academy_urls = set(
            self.env["website.menu"]
            .search(
                [
                    ("website_id", "=", academy.id),
                    ("parent_id", "!=", False),
                ]
            )
            .mapped("url")
        )
        self.assertEqual(academy_urls, set(ACADEMY_MENU_URLS))
        self.assertFalse(
            self.env["website.menu"].search(
                [("website_id", "=", studio.id), ("url", "=", "/slides")]
            )
        )
        contact = self.env["website.menu"].search(
            [("website_id", "=", academy.id), ("url", "=", "/contactus")],
            limit=1,
        )
        self.assertEqual(contact.with_context(lang="en_US").name, "Contact")
        self.assertEqual(contact.with_context(lang="pt_BR").name, "Contato")

    def test_academia_pages_are_reachable(self):
        for path in ACADEMY_MENU_URLS:
            with self.subTest(path=path):
                response = self._open_academy(path)
                self.assertEqual(response.status_code, 200, path)

    def test_academia_home_shows_official_sections(self):
        body = self._open_academy("/").text
        self.assertIn("split-academia", body)
        self.assertNotIn("acd-kicker", body)
        self.assertIn("What", body)
        self.assertIn("Academia?", body)
        self.assertIn("Learn more", body)
        self.assertIn("Join our community", body)
        self.assertIn("discord.com/invite/Xw7PyfEvjw", body)
        self.assertIn("Those who teach, inspire.", body)
        self.assertIn("Murilo Carvalho", body)
        self.assertIn("Shall we", body)
        self.assertIn("hero_academia_day.jpg", body)
        self.assertIn("acd-card-yellow", body)
        self.assertIn("acd-form", body)
        self.assertIn("brain.gif", body)
        self.assertIn("placeholder=\"Name\"", body)
        self.assertNotIn("Subscribe to the newsletter and stay tuned for news.", body)

    def test_academia_contact_matches_official_form(self):
        body = self._open_academy("/contactus").text
        self.assertIn("acd-contact", body)
        self.assertIn("acd-form", body)
        self.assertIn("brain.gif", body)
        self.assertIn("placeholder=\"E-mail\"", body)
        self.assertIn("placeholder=\"Message\"", body)
        self.assertNotIn("acd-kicker", body)

    def test_academy_course_cover_uses_navy(self):
        channel = self._channel("slide_channel_cutout_harmony")
        self.assertIn("003f59", channel.cover_properties)
        self.assertNotIn("875A7B", channel.cover_properties)
        page = self._open_academy(channel.website_url)
        self.assertEqual(page.status_code, 200)
        self.assertNotIn("875A7B", page.text)
        self.assertNotIn("78516F", page.text)

    def test_academia_slides_uses_branded_hero(self):
        home = self._open_academy("/slides").text
        self.assertIn("acd-slides-hero", home)
        self.assertIn("What do you want to", home)
        self.assertNotIn("Reach new heights", home)
        self.assertNotIn("banner_default.svg", home)
        catalog = self._open_academy("/slides/all").text
        self.assertIn("acd-slides-hero", catalog)
        self.assertNotIn("banner_default_all.svg", catalog)

    def test_academia_about_and_educators_content(self):
        about = self._open_academy("/about").text
        self.assertIn("What", about)
        self.assertIn("Academia?", about)
        self.assertIn("More than a school", about)
        self.assertIn("official", about)
        self.assertIn("Toon Boom", about)
        self.assertIn("Commitment", about)
        self.assertIn("learning options", about)
        self.assertIn("Workshops", about)
        self.assertIn("Masterclass", about)
        self.assertIn("splitstudio.tv", about)
        self.assertIn("institutosplit", about)
        self.assertIn("atc_toonboom.webp", about)
        self.assertNotIn("acd-kicker", about)
        educators = self._open_academy("/educators").text
        self.assertNotIn("acd-kicker", educators)
        self.assertIn("acd-edu-card", educators)
        self.assertIn("Those who", educators)
        self.assertIn("inspire", educators)
        self.assertIn("Selected work", educators)
        self.assertIn("Beatriz Gondim", educators)
        self.assertIn("Belisa Proença", educators)
        self.assertIn("Bruno Antonio", educators)
        self.assertIn("Ana Maria Sena", educators)
        self.assertIn("Luiz do Futuro", educators)
        self.assertIn("luizdofuturo", educators)
        self.assertIn("Rick and Morty", educators)

    def test_academy_rank_badges_are_branded(self):
        ranks_dir = Path(get_module_path("split_website_elearning")) / (
            "static/src/img/ranks"
        )
        for name in ("newbie", "student", "bachelor", "master", "doctor"):
            rank = self.env.ref(f"gamification.rank_{name}")
            self.assertTrue(rank.image_1920, name)
            raw = base64.b64decode(rank.image_1920)
            self.assertNotIn(b"CB9600", raw, name)
            self.assertTrue((ranks_dir / f"{name}.svg").is_file(), name)
            if raw.lstrip().startswith(b"<svg") or raw.lstrip().startswith(b"<?xml"):
                self.assertIn(f"acd-rank-{name}".encode(), raw)
            else:
                self.assertGreater(len(raw), 80, name)

    def test_academia_public_shows_sign_in(self):
        body = self._open_academy("/").text
        self.assertIn("split-academia", body)
        self.assertIn("Sign in", body)
        self.assertIn("/web/login", body)
        self.assertNotIn("o_backend_user_dropdown_link", body)
        self.assertNotIn("Administrator", body)
        portuguese = self._academy().language_ids.filtered(
            lambda lang: lang.code == "pt_BR"
        )[:1]
        self.assertTrue(portuguese, "Academia must serve Portuguese")
        pt_body = self._open_academy(f"/{portuguese.url_code}").text
        self.assertIn("Entrar", pt_body)
        self.assertIn("/web/login", pt_body)

    def test_academia_hides_admin_chrome(self):
        self.authenticate("admin", "admin")
        body = self._open_academy("/").text
        self.assertIn("split-academia", body)
        self.assertNotIn("o_frontend_to_backend_nav", body)
        self.assertNotIn("o_frontend_to_backend_edit_btn", body)
        self.assertIn("js_usermenu", body)
        self.assertIn("o_backend_user_dropdown_link", body)
        self.assertIn("Administrator", body)
        slides = self._open_academy("/slides").text
        self.assertNotIn("rank_doctor_badge.svg", slides)
        self.assertNotIn("rank_newbie_badge.svg", slides)
        self.assertTrue(
            "Your progress" in slides or "Seu progresso" in slides
        )
        self.assertIn("Administrator", slides)

    def test_academia_view_terms_are_translated(self):
        about = self.env.ref("split_website_elearning.about")
        about_pt = about.with_context(lang="pt_BR").arch_db
        self.assertIn("Queremos multiplicar e somar!", about_pt)
        self.assertIn("Mais do que uma escola", about_pt)
        self.assertIn("ensino oficial do", about_pt)
        self.assertIn("opções de aprendizado", about_pt)
        educators = self.env.ref("split_website_elearning.educators")
        educators_pt = educators.with_context(lang="pt_BR").arch_db
        self.assertIn("Trabalhos selecionados", educators_pt)
        self.assertIn("artista visual brasiliense", educators_pt)
        self.assertIn("Diretora de arte e cenarista", educators_pt)
        academy = self._academy()
        home = self.env["ir.ui.view"].search(
            [
                ("key", "=", "website.homepage"),
                ("website_id", "=", academy.id),
            ],
            limit=1,
        )
        self.assertTrue(home)
        home_pt = home.with_context(lang="pt_BR").arch_db
        self.assertIn("Acesse nossa comunidade", home_pt)
        self.assertIn("Dúvidas frequentes", home_pt)
        self.assertIn("conversar?", home_pt)
        channel = self._channel("slide_channel_backgrounds").with_context(
            lang="pt_BR"
        )
        self.assertEqual(channel.name, "A Arte de Criar Cenários")
        self.assertIn("porta de entrada", channel.description)
