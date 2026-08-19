# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestSplitWebsitePages(HttpCase):
    PAGE_URLS = [
        "/",
        "/reel",
        "/our-work",
        "/split-originals",
        "/about",
        "/contactus",
        "/privacy",
        "/work/rick-and-morty",
        "/work/fit-ufc-true-myth",
        "/work/are-you-okay",
        "/work/is-anybody-out-there",
        "/work/bit-wars",
        "/work/mr-men-little-miss",
        "/work/bubu-and-the-little-owls",
        "/work/the-boy-and-the-world",
        "/originals/weeboom",
        "/originals/among-the-stars",
        "/originals/whats-up-bud",
        "/originals/the-charcoal-swordsman",
        "/originals/sun-boy-and-friends",
        "/originals/que-corpo-e-esse",
        "/originals/wizavior",
        "/originals/egregore",
        "/originals/children-of-the-world",
        "/originals/blue-butterflies",
        "/originals/howdy-harrdy",
        "/originals/miss-and-grubs",
        "/originals/to-reach-the-moon",
    ]

    def test_pages_are_reachable(self):
        for url in self.PAGE_URLS:
            with self.subTest(url=url):
                response = self.url_open(url)
                self.assertEqual(response.status_code, 200)

    def test_pages_are_published(self):
        pages = self.env["website.page"].search(
            [
                (
                    "url",
                    "in",
                    [
                        "/reel",
                        "/our-work",
                        "/split-originals",
                        "/about",
                        "/work/rick-and-morty",
                        "/originals/weeboom",
                    ],
                )
            ]
        )
        self.assertEqual(len(pages), 6)
        self.assertTrue(all(pages.mapped("is_published")))

    def test_about_shows_the_official_manifesto(self):
        body = self.url_open("/about").text
        self.assertIn("We love telling stories", body)
        self.assertIn("about_hero", body)
        self.assertIn("about_character_01", body)
        self.assertIn("Future Channel", body)
        self.assertIn("Character Design", body)
        self.assertIn("Motion Animation", body)
        self.assertNotIn("banner_split_academy", body)
        self.assertNotIn("OS ORIGINAIS SPLIT", body)

    def test_home_shows_split_content(self):
        body = self.url_open("/").text
        self.assertIn("Animation & Games", body)
        self.assertIn("What Split does", body)
        self.assertIn("/web/image/split_website.work_tito_and_the_birds", body)
        self.assertIn("home_hero.webm", body)
        self.assertIn("home_hero_mobile.webm", body)
        self.assertIn("/work/bit-wars", body)
        self.assertIn("catarse.com.br/entreasestrelas-original", body)
        self.assertNotIn("splitacademia.com.br", body)

    def test_contact_form_targets_crm_lead(self):
        body = self.url_open("/contactus").text
        self.assertIn('data-model_name="crm.lead"', body)
        # The team and medium placeholders must have been resolved at install.
        self.assertNotIn("*crm_team_intake*", body)
        self.assertNotIn("*utm_medium_website*", body)
        self.assertNotIn("banner_hello_kitty", body)
        self.assertIn("charcoal_cover", body)
        self.assertIn("/privacy", body)
        self.assertIn('name="Privacy"', body)

    def test_contact_form_creates_intake_lead(self):
        team = self.env["crm.team"].search([("name", "=", "Intake")], limit=1)
        self.assertTrue(team, "The Intake team is required by the contact form")
        response = self.url_open(
            "/website/form/crm.lead",
            data={
                "contact_name": "Belisa Proença",
                "email_from": "belisa@example.com",
                "partner_name": "Split Studio",
                "name": "Work with Split",
                "description": "We would like to co-produce a series.",
                "Privacy": "on",
                "team_id": str(team.id),
            },
        )
        self.assertEqual(response.status_code, 200)
        lead = self.env["crm.lead"].search(
            [("email_from", "=", "belisa@example.com")], limit=1
        )
        self.assertTrue(lead, "The contact form must create a lead")
        self.assertEqual(lead.team_id, team)

    def test_public_chrome_is_hidden(self):
        body = self.url_open("/").text
        self.assertNotIn("Sign in", body)
        self.assertNotIn("Powered by", body)
        self.assertNotIn("Extra page", body)
        self.assertNotIn("Extra Page", body)
        self.assertNotIn('id="split_work_all"', body)
        self.assertIn("vimeo.com/splitstudio", body)
        self.assertIn("Sign up for our newsletter", body)

    def test_our_work_has_category_filter(self):
        body = self.url_open("/our-work").text
        self.assertIn('id="split_work_all"', body)
        self.assertIn('data-category="shows"', body)
        self.assertIn("/work/rick-and-morty", body)

    def test_newsletter_list_is_resolved(self):
        body = self.url_open("/").text
        self.assertNotIn("*mailing_list_id*", body)

    def test_originals_page_links_every_card(self):
        body = self.url_open("/split-originals").text
        for url in (
            "/originals/weeboom",
            "/originals/among-the-stars",
            "/originals/whats-up-bud",
            "/originals/the-charcoal-swordsman",
            "/originals/sun-boy-and-friends",
            "/originals/que-corpo-e-esse",
            "/originals/wizavior",
            "/originals/egregore",
            "/originals/children-of-the-world",
            "/originals/blue-butterflies",
            "/originals/howdy-harrdy",
            "/originals/miss-and-grubs",
            "/originals/to-reach-the-moon",
        ):
            with self.subTest(url=url):
                self.assertIn(f'href="{url}"', body)

    def test_charcoal_swordsman_is_a_full_ip_page(self):
        body = self.url_open("/originals/the-charcoal-swordsman").text
        self.assertIn("10 x 22", body)
        self.assertIn("Adventure | Fantasy | Drama", body)
        self.assertIn("Affonso Solano", body)
        self.assertIn("Adapak", body)
        self.assertIn("Sirara", body)
        self.assertIn("youtube.com/embed/Y4jV4n_K7mc", body)
        self.assertIn("/web/image/split_website.charcoal_character_adapak", body)

    def test_weeboom_is_a_full_ip_page(self):
        body = self.url_open("/originals/weeboom").text
        self.assertIn("26 x 7", body)
        self.assertIn("Comedy | Adventure | Travel", body)
        self.assertIn("Characters", body)
        self.assertIn("The Adventure", body)
        self.assertIn("Mamma Mia", body)
        self.assertIn("weeboom_hero.mp4", body)
        self.assertIn("/web/image/split_website.weeboom_character_wee", body)

    def test_work_page_lists_credits(self):
        body = self.url_open("/work/hello-kitty-supercute").text
        self.assertIn("Sanrio Brazil", body)
        self.assertIn("75 x 3", body)
        self.assertIn("Storyboard", body)

    def test_fit_ufc_embeds_the_official_video(self):
        body = self.url_open("/work/fit-ufc-true-myth").text
        self.assertIn("player.vimeo.com/video/655025664", body)
        self.assertIn("ratio ratio-16x9", body)

    def test_are_you_okay_lists_credits_and_video(self):
        body = self.url_open("/work/are-you-okay").text
        self.assertIn("Wonder Media", body)
        self.assertIn("2021", body)
        self.assertIn("youtube.com/embed/tJsGGsPNakw", body)

    def test_our_work_links_every_card(self):
        body = self.url_open("/our-work").text
        for url in (
            "/work/are-you-okay",
            "/work/is-anybody-out-there",
            "/work/bit-wars",
            "/work/mr-men-little-miss",
            "/work/bubu-and-the-little-owls",
            "/work/the-boy-and-the-world",
        ):
            with self.subTest(url=url):
                self.assertIn(f'href="{url}"', body)
        # The card captions must match the official credits.
        self.assertIn("Up Content · Preschool series", body)
        self.assertNotIn("Mr Plot", body)

    def test_among_the_stars_links_to_catarse(self):
        body = self.url_open("/originals/among-the-stars").text
        self.assertIn("catarse.com.br/entreasestrelas-original", body)

    def test_privacy_page_explains_how_data_is_used(self):
        body = self.url_open("/privacy").text
        self.assertIn("How Split uses the information you send us", body)
        self.assertIn("contato@splitstudio.tv", body)

    def test_portuguese_locale_is_available(self):
        website = self.env.ref("website.default_website")
        portuguese = self.env["res.lang"].search([("code", "=", "pt_BR")], limit=1)
        self.assertTrue(portuguese, "pt_BR must be activated for the public site")
        self.assertIn(portuguese, website.language_ids)
        home = self.url_open("/").text
        self.assertTrue(
            "js_language_selector" in home
            or "o_header_language_selector" in home
            or portuguese.url_code in home,
            "The language selector must appear when more than one language is active",
        )
        response = self.url_open(f"/{portuguese.url_code}/our-work")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Nossos trabalhos", response.text)
        self.assertIn("Inscreva-se na newsletter", response.text)
        weeboom = self.url_open(f"/{portuguese.url_code}/originals/weeboom")
        self.assertEqual(weeboom.status_code, 200)
        self.assertIn("Personagens", weeboom.text)
        self.assertIn("Aventureira", weeboom.text)
        self.assertIn("4 a 7 anos", weeboom.text)
        home_pt = self.url_open(f"/{portuguese.url_code}/")
        self.assertEqual(home_pt.status_code, 200)
        self.assertIn("Entre as Estrelas", home_pt.text)
        self.assertIn("Apoie no Catarse", home_pt.text)
        about = self.url_open(f"/{portuguese.url_code}/about")
        self.assertEqual(about.status_code, 200)
        self.assertIn("Somos a Split", about.text)
        self.assertIn("Já percebeu que a personagem", about.text)
        charcoal = self.url_open(
            f"/{portuguese.url_code}/originals/the-charcoal-swordsman"
        )
        self.assertEqual(charcoal.status_code, 200)
        self.assertIn("O Espadachim de Carvão", charcoal.text)
        self.assertIn("Fiel companheira", charcoal.text)
        children = self.url_open(
            f"/{portuguese.url_code}/originals/children-of-the-world"
        )
        self.assertEqual(children.status_code, 200)
        self.assertIn("Crianças do Mundo", children.text)
        contact = self.url_open(f"/{portuguese.url_code}/contactus")
        self.assertEqual(contact.status_code, 200)
        self.assertIn("Fale conosco", contact.text)
