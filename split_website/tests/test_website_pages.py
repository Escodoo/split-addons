# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestSplitWebsitePages(HttpCase):
    PAGE_URLS = ["/", "/reel", "/our-work", "/split-originals", "/about", "/contactus"]

    def test_pages_are_reachable(self):
        for url in self.PAGE_URLS:
            with self.subTest(url=url):
                response = self.url_open(url)
                self.assertEqual(response.status_code, 200)

    def test_pages_are_published(self):
        pages = self.env["website.page"].search(
            [("url", "in", ["/reel", "/our-work", "/split-originals", "/about"])]
        )
        self.assertEqual(len(pages), 4)
        self.assertTrue(all(pages.mapped("is_published")))

    def test_home_shows_split_content(self):
        body = self.url_open("/").text
        self.assertIn("Animation & Games", body)
        self.assertIn("What Split does", body)
        self.assertIn("/web/image/split_website.work_tito_and_the_birds", body)

    def test_contact_form_targets_crm_lead(self):
        body = self.url_open("/contactus").text
        self.assertIn('data-model_name="crm.lead"', body)
        # The team and medium placeholders must have been resolved at install.
        self.assertNotIn("*crm_team_intake*", body)
        self.assertNotIn("*utm_medium_website*", body)

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
                "team_id": str(team.id),
            },
        )
        self.assertEqual(response.status_code, 200)
        lead = self.env["crm.lead"].search(
            [("email_from", "=", "belisa@example.com")], limit=1
        )
        self.assertTrue(lead, "The contact form must create a lead")
        self.assertEqual(lead.team_id, team)

    def test_newsletter_list_is_resolved(self):
        body = self.url_open("/").text
        self.assertNotIn("*mailing_list_id*", body)
