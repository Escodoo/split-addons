# Copyright 2026 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, tagged


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

    def test_team_pipeline_includes_activity_view(self):
        action = self.env.ref("crm.crm_case_form_view_salesteams_opportunity")
        self.assertIn("activity", action.view_mode.split(","))
