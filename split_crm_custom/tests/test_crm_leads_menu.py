# Copyright 2026 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, tagged
from odoo.tools.safe_eval import safe_eval


@tagged("post_install", "-at_install")
class TestCrmLeadsMenu(TransactionCase):
    def test_leads_menu_comes_before_sales(self):
        leads_menu = self.env.ref("crm.crm_menu_leads")
        sales_menu = self.env.ref("crm.crm_menu_sales")
        crm_root = self.env.ref("crm.crm_menu_root")
        self.assertEqual(leads_menu.parent_id, crm_root)
        self.assertEqual(sales_menu.parent_id, crm_root)
        self.assertLess(leads_menu.sequence, sales_menu.sequence)

    def test_leads_action_opens_kanban_first(self):
        action = self.env.ref("crm.crm_lead_all_leads")
        self.assertTrue(action.view_mode.startswith("kanban"))
        kanban_view = self.env.ref("crm.crm_lead_all_leads_view_kanban")
        list_view = self.env.ref("crm.crm_lead_all_leads_view_tree")
        self.assertLess(kanban_view.sequence, list_view.sequence)

    def test_leads_kanban_groups_by_stage(self):
        view = self.env.ref("crm.view_crm_lead_kanban")
        arch = view.get_combined_arch()
        self.assertIn('default_group_by="stage_id"', arch)

    def test_lead_form_shows_stage_statusbar(self):
        view = self.env.ref("crm.crm_lead_view_form")
        arch = view.get_combined_arch()
        self.assertIn('name="stage_id"', arch)
        self.assertIn('widget="statusbar_duration"', arch)
        self.assertNotIn("invisible=\"not active or type == 'lead'\"", arch)

    def test_team_pipeline_includes_activity_view(self):
        action = self.env.ref("crm.crm_case_form_view_salesteams_opportunity")
        self.assertIn("activity", action.view_mode.split(","))

    def test_leads_action_uses_intake_team(self):
        action = self.env.ref("crm.crm_lead_all_leads")
        team = self.env.ref("split_crm_custom.crm_team_intake")
        context = safe_eval(action.context, {"uid": self.env.uid})
        self.assertEqual(context.get("default_team_id"), team.id)
        self.assertEqual(context.get("search_default_team_id"), [team.id])
        self.assertTrue(team.use_leads)
        self.assertFalse(team.use_opportunities)

    def test_empty_intake_stages_are_expanded(self):
        team = self.env.ref("split_crm_custom.crm_team_intake")
        intake_stages = self.env["crm.stage"].search([("team_id", "=", team.id)])
        self.assertGreaterEqual(len(intake_stages), 4)
        expanded = (
            self.env["crm.lead"]
            .with_context(default_team_id=team.id)
            ._read_group_stage_ids(self.env["crm.stage"], [])
        )
        self.assertTrue(intake_stages <= expanded)
