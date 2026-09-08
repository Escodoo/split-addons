# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestCrmLeadReassignWizard(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.lead_team = cls.env["crm.team"].create(
            {
                "name": "Reassign Origin",
                "use_leads": True,
                "use_opportunities": True,
            }
        )
        cls.target_team = cls.env["crm.team"].create(
            {
                "name": "Reassign Target",
                "use_leads": True,
                "use_opportunities": True,
            }
        )
        cls.opp_only_team = cls.env["crm.team"].create(
            {
                "name": "Reassign Opp Only",
                "use_leads": False,
                "use_opportunities": True,
            }
        )
        cls.lead = cls.env["crm.lead"].create(
            {
                "name": "Reassign Test Lead",
                "type": "lead",
                "team_id": cls.lead_team.id,
            }
        )
        cls.opportunity = cls.env["crm.lead"].create(
            {
                "name": "Reassign Test Opportunity",
                "type": "opportunity",
                "team_id": cls.lead_team.id,
            }
        )

    def _make_wizard(self, lead):
        return (
            self.env["crm.lead.reassign.wizard"]
            .with_context(default_lead_id=lead.id)
            .create({"lead_id": lead.id, "new_team_id": self.target_team.id})
        )

    def test_01_onchange_lead_id_lead(self):
        wizard = self._make_wizard(self.lead)
        result = wizard._onchange_lead_id()
        self.assertEqual(
            result, {"domain": {"new_team_id": [("use_leads", "=", True)]}}
        )

    def test_02_onchange_lead_id_opportunity(self):
        wizard = self._make_wizard(self.opportunity)
        result = wizard._onchange_lead_id()
        self.assertEqual(
            result,
            {"domain": {"new_team_id": [("use_opportunities", "=", True)]}},
        )

    def test_03_onchange_lead_id_empty_returns_none(self):
        wizard = self.env["crm.lead.reassign.wizard"].new(
            {"lead_id": False, "new_team_id": self.target_team.id}
        )
        self.assertIsNone(wizard._onchange_lead_id())

    def test_04_action_reassign_moves_lead(self):
        wizard = self._make_wizard(self.lead)
        action = wizard.action_reassign()
        self.assertEqual(action, {"type": "ir.actions.act_window_close"})
        self.assertEqual(self.lead.team_id, self.target_team)

    def test_05_action_reassign_noop_when_same_team(self):
        wizard = self.env["crm.lead.reassign.wizard"].create(
            {
                "lead_id": self.lead.id,
                "new_team_id": self.lead_team.id,
            }
        )
        action = wizard.action_reassign()
        self.assertEqual(action, {"type": "ir.actions.act_window_close"})
        self.assertEqual(self.lead.team_id, self.lead_team)

    def test_06_action_open_reassign_wizard_lead(self):
        action = (
            self.env["crm.lead.reassign.wizard"]
            .with_context(active_id=self.lead.id)
            .action_open_reassign_wizard()
        )
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "crm.lead.reassign.wizard")
        self.assertEqual(action["context"]["default_lead_id"], self.lead.id)
        self.assertEqual(action["context"]["default_new_team_id"], self.lead_team.id)
        self.assertEqual(
            action["context"]["default_domain_new_team_id"],
            [("use_leads", "=", True)],
        )

    def test_07_action_open_reassign_wizard_opportunity(self):
        action = (
            self.env["crm.lead.reassign.wizard"]
            .with_context(active_id=self.opportunity.id)
            .action_open_reassign_wizard()
        )
        self.assertEqual(
            action["context"]["default_domain_new_team_id"],
            [("use_opportunities", "=", True)],
        )
