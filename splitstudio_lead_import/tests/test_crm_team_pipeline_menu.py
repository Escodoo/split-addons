# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestCrmTeamPipelineMenu(TransactionCase):
    def setUp(self):
        super().setUp()
        self.Team = self.env["crm.team"]
        self.Menu = self.env["ir.ui.menu"]
        self.Action = self.env["ir.actions.act_window"]
        self.pipeline_root = self.env.ref("crm.crm_menu_leads")

    def test_create_team_with_menu_flag(self):
        team = self.Team.create(
            {
                "name": "Test Pipeline Team",
                "use_leads": True,
                "show_in_pipeline_menu": True,
            }
        )
        menu = self.Menu.search(
            [
                ("parent_id", "=", self.pipeline_root.id),
                ("name", "=", team.name),
            ],
            limit=1,
        )
        self.assertTrue(menu, "Submenu should be created for team with flag")
        self.assertEqual(menu.action.res_model, "crm.lead")
        self.assertIn("team_id", menu.action.domain)

    def test_create_team_without_menu_flag(self):
        team = self.Team.create(
            {
                "name": "No Menu Team",
                "use_leads": True,
                "show_in_pipeline_menu": False,
            }
        )
        menu = self.Menu.search(
            [
                ("parent_id", "=", self.pipeline_root.id),
                ("name", "=", team.name),
            ],
            limit=1,
        )
        self.assertFalse(menu, "No submenu should be created without flag")

    def test_write_enable_menu_flag(self):
        team = self.Team.create(
            {
                "name": "Toggle Team",
                "use_leads": True,
                "show_in_pipeline_menu": False,
            }
        )
        result = team.write({"show_in_pipeline_menu": True})
        self.assertEqual(result.get("type"), "ir.actions.client")
        self.assertEqual(result.get("tag"), "reload")
        menu = self.Menu.search(
            [
                ("parent_id", "=", self.pipeline_root.id),
                ("name", "=", team.name),
            ],
            limit=1,
        )
        self.assertTrue(menu, "Submenu should appear after enabling flag")

    def test_write_disable_menu_flag(self):
        team = self.Team.create(
            {
                "name": "Remove Team",
                "use_leads": True,
                "show_in_pipeline_menu": True,
            }
        )
        menu = self.Menu.search(
            [
                ("parent_id", "=", self.pipeline_root.id),
                ("name", "=", team.name),
            ],
            limit=1,
        )
        self.assertTrue(menu)
        result = team.write({"show_in_pipeline_menu": False})
        self.assertEqual(result.get("type"), "ir.actions.client")
        menu = self.Menu.search(
            [
                ("parent_id", "=", self.pipeline_root.id),
                ("name", "=", team.name),
            ],
            limit=1,
        )
        self.assertFalse(menu, "Submenu should be removed after disabling flag")

    def test_write_other_field_no_reload(self):
        team = self.Team.create(
            {
                "name": "Other Field Team",
                "use_leads": True,
                "show_in_pipeline_menu": True,
            }
        )
        result = team.write({"name": "Renamed Team"})
        self.assertNotEqual(
            result.get("tag") if isinstance(result, dict) else None,
            "reload",
            "write for other fields should not return reload",
        )

    def test_unlink_team_removes_menu(self):
        team = self.Team.create(
            {
                "name": "Delete Team",
                "use_leads": True,
                "show_in_pipeline_menu": True,
            }
        )
        menu = self.Menu.search(
            [
                ("parent_id", "=", self.pipeline_root.id),
                ("name", "=", team.name),
            ],
            limit=1,
        )
        self.assertTrue(menu)
        team.unlink()
        menu = self.Menu.search(
            [
                ("parent_id", "=", self.pipeline_root.id),
                ("name", "=", "Delete Team"),
            ],
            limit=1,
        )
        self.assertFalse(menu, "Submenu should be removed when team is deleted")

    def test_create_opportunity_team_menu(self):
        team = self.Team.create(
            {
                "name": "Opp Team",
                "use_leads": False,
                "show_in_pipeline_menu": True,
            }
        )
        menu = self.Menu.search(
            [
                ("parent_id", "=", self.pipeline_root.id),
                ("name", "=", team.name),
            ],
            limit=1,
        )
        self.assertTrue(menu)
        self.assertIn("opportunity", menu.action.domain)
        self.assertIn("opportunity", menu.action.context)

    def test_action_reuse_on_write(self):
        team = self.Team.create(
            {
                "name": "Reuse Team",
                "use_leads": True,
                "show_in_pipeline_menu": True,
            }
        )
        action = self.Action.search(
            [
                ("name", "=", team.name),
                ("res_model", "=", "crm.lead"),
            ],
            limit=1,
        )
        self.assertTrue(action)
        team.write({"show_in_pipeline_menu": False})
        team.write({"show_in_pipeline_menu": True})
        menu2 = self.Menu.search(
            [
                ("parent_id", "=", self.pipeline_root.id),
                ("name", "=", team.name),
            ],
            limit=1,
        )
        self.assertTrue(menu2, "Submenu should be recreated")

    def test_action_reuse_updates_domain_and_context(self):
        team = self.Team.create(
            {
                "name": "Update Team",
                "use_leads": True,
                "show_in_pipeline_menu": True,
            }
        )
        action = self.Action.search(
            [
                ("name", "=", team.name),
                ("res_model", "=", "crm.lead"),
            ],
            limit=1,
        )
        self.assertIn("lead", action.domain)
        team.write({"use_leads": False})
        team.write({"show_in_pipeline_menu": True})
        action.invalidate_recordset(["domain", "context"])
        self.assertIn("opportunity", action.domain)

    def test_unlink_removes_action_when_no_menus_left(self):
        team = self.Team.create(
            {
                "name": "Solo Team",
                "use_leads": True,
                "show_in_pipeline_menu": True,
            }
        )
        action = self.Action.search(
            [
                ("name", "=", team.name),
                ("res_model", "=", "crm.lead"),
            ],
            limit=1,
        )
        action_id = action.id
        team.unlink()
        self.assertFalse(
            self.env["ir.actions.act_window"].browse(action_id).exists(),
            "Action should be deleted when no menus reference it",
        )

    def test_no_menu_when_pipeline_root_missing(self):
        self.pipeline_root.unlink()
        team = self.Team.create(
            {
                "name": "No Root Team",
                "use_leads": True,
                "show_in_pipeline_menu": True,
            }
        )
        menu = self.Menu.search(
            [
                ("name", "=", team.name),
            ],
            limit=1,
        )
        self.assertFalse(menu)

    def test_remove_no_menu_is_noop(self):
        team = self.Team.create(
            {
                "name": "Noop Team",
                "use_leads": True,
                "show_in_pipeline_menu": False,
            }
        )
        team._remove_pipeline_menus()
        menu = self.Menu.search(
            [
                ("name", "=", "Noop Team"),
            ],
            limit=1,
        )
        self.assertFalse(menu)

    def test_remove_menu_when_pipeline_root_missing(self):
        team = self.Team.create(
            {
                "name": "No Root Remove",
                "use_leads": True,
                "show_in_pipeline_menu": True,
            }
        )
        self.pipeline_root.unlink()
        team._remove_pipeline_menus()

    def test_remove_menu_keeps_action_if_other_menu_references(self):
        team_a = self.Team.create(
            {
                "name": "Shared Action A",
                "use_leads": True,
                "show_in_pipeline_menu": True,
            }
        )
        team_b = self.Team.create(
            {
                "name": "Shared Action B",
                "use_leads": True,
                "show_in_pipeline_menu": True,
            }
        )
        action_a = self.Action.search(
            [("name", "=", team_a.name), ("res_model", "=", "crm.lead")],
            limit=1,
        )
        action_b = self.Action.search(
            [("name", "=", team_b.name), ("res_model", "=", "crm.lead")],
            limit=1,
        )
        self.assertNotEqual(action_a, action_b)
        menu_a = self.Menu.search(
            [
                ("parent_id", "=", self.pipeline_root.id),
                ("name", "=", team_a.name),
            ],
            limit=1,
        )
        menu_a.action = f"ir.actions.act_window,{action_b.id}"
        action_a_id = action_a.id
        team_a.unlink()
        self.assertTrue(
            self.env["ir.actions.act_window"].browse(action_a_id).exists(),
            "Action should be kept when another menu still references it",
        )

    def test_remove_menu_with_null_action(self):
        team = self.Team.create(
            {
                "name": "Null Action Team",
                "use_leads": True,
                "show_in_pipeline_menu": True,
            }
        )
        menu = self.Menu.search(
            [
                ("parent_id", "=", self.pipeline_root.id),
                ("name", "=", team.name),
            ],
            limit=1,
        )
        self.env.cr.execute(
            "UPDATE ir_ui_menu SET action = NULL WHERE id = %s",
            (menu.id,),
        )
        menu.invalidate_recordset(["action"])
        team._remove_pipeline_menus()
        self.assertFalse(menu.exists())
