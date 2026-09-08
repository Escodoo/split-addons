# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo.tests import common


class TestLeadImportWizard(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create an existing partner/lead for duplicate testing
        cls.existing_partner = cls.env["res.partner"].create(
            {
                "name": "Acme Corp Partner",
                "email": "contact@acme.com",
            }
        )
        cls.existing_lead = cls.env["crm.lead"].create(
            {
                "name": "Existing Lead John",
                "email_from": "john@example.com",
                "partner_name": "Globex",
            }
        )

    def test_01_lead_import_wizard_duplicates(self):
        # CSV content with one duplicate email and one clean row
        csv_data = (
            "name,email,partner_name,phone\n"
            "John Duplicate,john@example.com,Globex,123456\n"
            "New Lead,new@example.com,NewCo,987654\n"
        )
        file_base64 = base64.b64encode(csv_data.encode("utf-8"))

        team = self.env["crm.team"].search([("use_leads", "=", True)], limit=1)
        wizard = self.env["splitstudio.lead.import.wizard"].create(
            {
                "file_data": file_base64,
                "file_name": "leads.csv",
                "team_id": team.id,
            }
        )

        wizard.action_parse_and_check()

        self.assertEqual(wizard.state, "preview")
        self.assertTrue(wizard.duplicate_count > 0)

        # Confirm import
        wizard.action_import_leads()
        self.assertEqual(wizard.state, "done")
