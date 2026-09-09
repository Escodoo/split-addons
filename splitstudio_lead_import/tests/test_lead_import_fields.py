# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestLeadImportFields(common.TransactionCase):
    """Verify that description, priority, website, city and country_id
    columns of the spreadsheet are mapped to the corresponding crm.lead
    fields and that the priority text/number mapping is correct."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.team = cls.env["crm.team"].search([("use_leads", "=", True)], limit=1)
        cls.br = cls.env["res.country"].search([("code", "=", "BR")], limit=1)

    def _build_csv(self, header, rows):
        import csv
        import io

        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=header)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
        return buf.getvalue().encode("utf-8")

    def _run_wizard(self, csv_bytes, name="Test Session"):
        Wizard = self.env["splitstudio.lead.import.wizard"]
        wiz = Wizard.create(
            {
                "name": name,
                "team_id": self.team.id,
                "file_data": base64.b64encode(csv_bytes),
                "file_name": "test.csv",
                "state": "draft",
            }
        )
        wiz.action_parse_and_check()
        return wiz

    def test_01_alias_opportunity_and_email_from(self):
        """Header `opportunity` and `email_from` are recognized."""
        csv_bytes = self._build_csv(
            ["opportunity", "email_from", "partner_name"],
            [
                {
                    "opportunity": "Alias Test Lead",
                    "email_from": "alias@example.com",
                    "partner_name": "Alias Co",
                }
            ],
        )
        wiz = self._run_wizard(csv_bytes)
        self.assertEqual(len(wiz.line_ids), 1)
        line = wiz.line_ids[0]
        self.assertEqual(line.name, "Alias Test Lead")
        self.assertEqual(line.email, "alias@example.com")

    def test_02_alias_tag_ids_singular(self):
        """Header `tag_ids` (singular, as in the user's spreadsheet) is
        recognized alongside `tags_ids` (plural)."""
        csv_bytes = self._build_csv(
            ["name", "email", "tag_ids"],
            [
                {
                    "name": "Tag Singular",
                    "email": "singular@x.com",
                    "tag_ids": "alpha, beta",
                },
            ],
        )
        wiz = self._run_wizard(csv_bytes)
        line = wiz.line_ids[0]
        self.assertEqual(set(line.tag_ids.mapped("name")), {"alpha", "beta"})

    def test_03_priority_mapping_text(self):
        """English text labels map to the right selection value."""
        for text, expected in [
            ("Low", "0"),
            ("Medium", "1"),
            ("High", "2"),
            ("Very High", "3"),
        ]:
            wiz = self._run_wizard(
                self._build_csv(
                    ["name", "email", "priority"],
                    [{"name": f"P {text}", "email": f"{text}@x.com", "priority": text}],
                ),
                name=f"Priority {text}",
            )
            self.assertEqual(
                wiz.line_ids[0].priority,
                expected,
                f"Priority text {text!r} should map to {expected!r}",
            )

    def test_04_priority_mapping_number_and_pt(self):
        """Numbers and Portuguese labels are mapped as well."""
        cases = [
            ("0", "0"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("baixa", "0"),
            ("média", "1"),
            ("alta", "2"),
            ("muito alta", "3"),
        ]
        for raw, expected in cases:
            wiz = self._run_wizard(
                self._build_csv(
                    ["name", "email", "priority"],
                    [{"name": f"P {raw}", "email": f"p{raw}@x.com", "priority": raw}],
                ),
                name=f"Priority {raw}",
            )
            self.assertEqual(
                wiz.line_ids[0].priority,
                expected,
                f"Priority raw {raw!r} should map to {expected!r}",
            )

    def test_05_description_field_and_chatter_note(self):
        """Description is set on the lead and also posted as an
        internal note on the chatter."""
        description_text = "Cliente VIP pediu reunião sexta às 14h."
        wiz = self._run_wizard(
            self._build_csv(
                ["name", "email", "description"],
                [
                    {
                        "name": "Desc Test",
                        "email": "desc@x.com",
                        "description": description_text,
                    }
                ],
            ),
            name="Description Test",
        )
        line = wiz.line_ids[0]
        line.write({"import_line": True})
        self.assertEqual(line.description, description_text)
        wiz.action_import_leads()
        lead = self.env["crm.lead"].search([("name", "=", "Desc Test")])
        # crm.lead.description is rendered as HTML, so it is wrapped in <p>.
        self.assertIn(description_text, lead.description)
        notes = lead.message_ids.filtered(
            lambda m: m.subtype_id and "note" in (m.subtype_id.name or "").lower()
        )
        self.assertTrue(
            notes,
            "An internal note (Anotações internas) should be posted",
        )

    def test_06_country_iso_code_and_name(self):
        """Country is resolved by ISO code first, then by name."""
        wiz = self._run_wizard(
            self._build_csv(
                ["name", "email", "country_id"],
                [
                    {"name": "ByCode", "email": "bycode@x.com", "country_id": "BR"},
                    {
                        "name": "ByName",
                        "email": "byname@x.com",
                        "country_id": "United States",
                    },
                ],
            ),
            name="Country Test",
        )
        by_code = wiz.line_ids.filtered(lambda line: line.name == "ByCode")
        by_name = wiz.line_ids.filtered(lambda line: line.name == "ByName")
        self.assertEqual(by_code.country_id, self.br)
        us = self.env["res.country"].search([("code", "=", "US")], limit=1)
        self.assertEqual(by_name.country_id, us)

    def test_07_website_city_country_create(self):
        """Website and city are stored on the wizard line and on the
        lead after import."""
        wiz = self._run_wizard(
            self._build_csv(
                ["name", "email", "website", "city", "country_id"],
                [
                    {
                        "name": "Site City Lead",
                        "email": "sc@x.com",
                        "website": "https://example.com",
                        "city": "Sao Paulo",
                        "country_id": "BR",
                    }
                ],
            ),
            name="Site City Test",
        )
        line = wiz.line_ids[0]
        self.assertEqual(line.website, "https://example.com")
        self.assertEqual(line.city, "Sao Paulo")
        self.assertEqual(line.country_id, self.br)
        line.write({"import_line": True})
        wiz.action_import_leads()
        lead = self.env["crm.lead"].search([("name", "=", "Site City Lead")])
        self.assertEqual(lead.website, "https://example.com")
        self.assertEqual(lead.city, "Sao Paulo")
        self.assertEqual(lead.country_id, self.br)
        # Cleanup
        lead.unlink()

    def test_08_campaign_auto_create(self):
        """A campaign that does not exist is created on the fly, and a
        pre-existing campaign with the same name is re-used."""
        unique_name = "Auto Campaign Unit Test"
        # Pre-create the campaign so the ``if existing:`` branch is
        # exercised when this test runs after a previous one (or in
        # isolation, when the campaign still exists from a prior run).
        self.env["utm.campaign"].create({"name": unique_name})
        existing = self.env["utm.campaign"].search([("name", "=", unique_name)])
        if existing:
            existing.unlink()
        # First run: campaign does not exist yet, must be auto-created.
        wiz_first = self._run_wizard(
            self._build_csv(
                ["name", "email", "campaign_id"],
                [
                    {
                        "name": "Auto Campaign Lead 1",
                        "email": "auto_camp_1@x.com",
                        "campaign_id": unique_name,
                    }
                ],
            ),
            name="Auto Campaign Test 1",
        )
        first_campaign = wiz_first.line_ids[0].campaign_id
        self.assertEqual(first_campaign.name, unique_name)
        # Second run: same campaign name now exists; the helper must
        # reuse it instead of creating a duplicate.
        wiz_second = self._run_wizard(
            self._build_csv(
                ["name", "email", "campaign_id"],
                [
                    {
                        "name": "Auto Campaign Lead 2",
                        "email": "auto_camp_2@x.com",
                        "campaign_id": unique_name,
                    }
                ],
            ),
            name="Auto Campaign Test 2",
        )
        self.assertEqual(wiz_second.line_ids[0].campaign_id, first_campaign)
        # Cleanup
        first_campaign.unlink()

    def test_09_duplicate_detection_email(self):
        """An email that already exists in crm.lead flags the row."""
        self.env["crm.lead"].create(
            {"name": "Dup Probe", "email_from": "dup_probe@x.com", "type": "lead"}
        )
        wiz = self._run_wizard(
            self._build_csv(
                ["name", "email"],
                [
                    {
                        "name": "Dup Probe 2",
                        "email": "dup_probe@x.com",
                    }
                ],
            ),
            name="Dup Test",
        )
        line = wiz.line_ids[0]
        self.assertTrue(line.is_duplicate)
        self.assertIn("Email exists in Lead", line.duplicate_reason)
