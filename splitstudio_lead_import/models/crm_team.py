import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class CrmTeam(models.Model):
    _inherit = "crm.team"

    show_in_pipeline_menu = fields.Boolean(
        string="Show in Pipeline Menu",
        help="If checked, a menu item will be "
        "created under CRM > Pipelines for this team.",
        default=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        teams = super().create(vals_list)
        for team in teams:
            if team.show_in_pipeline_menu:
                team._create_pipeline_menu()
        return teams

    def write(self, vals):
        result = super().write(vals)
        if "show_in_pipeline_menu" in vals:
            for team in self:
                if team.show_in_pipeline_menu:
                    team._create_pipeline_menu()
                else:
                    team._remove_pipeline_menus()
            return {
                "type": "ir.actions.client",
                "tag": "reload",
            }
        return result

    def unlink(self):
        for team in self:
            team._remove_pipeline_menus()
        return super().unlink()

    def _create_pipeline_menu(self):
        self.ensure_one()
        Action = self.env["ir.actions.act_window"]
        Menu = self.env["ir.ui.menu"]

        PipelineRoot = self.env.ref("crm.crm_menu_leads", raise_if_not_found=False)
        if not PipelineRoot:
            return

        if self.use_leads:
            domain = [("type", "=", "lead"), ("team_id", "=", self.id)]
            default_type = "lead"
        else:
            domain = [("type", "=", "opportunity"), ("team_id", "=", self.id)]
            default_type = "opportunity"

        action = Action.search(
            [("name", "=", self.name), ("res_model", "=", "crm.lead")],
            limit=1,
        )

        action_ctx = {
            "default_type": default_type,
            "default_team_id": self.id,
            "search_default_team_id": self.id,
        }

        if not action:
            action = Action.create(
                {
                    "name": self.name,
                    "res_model": "crm.lead",
                    "view_mode": "kanban,list,form",
                    "domain": str(domain),
                    "context": str(action_ctx),
                }
            )
        else:
            action.write(
                {
                    "domain": str(domain),
                    "context": str(action_ctx),
                }
            )

        existing_menu = Menu.search(
            [("parent_id", "=", PipelineRoot.id), ("name", "=", self.name)],
            limit=1,
        )

        if not existing_menu:
            Menu.create(
                {
                    "name": self.name,
                    "parent_id": PipelineRoot.id,
                    "action": f"ir.actions.act_window,{action.id}",
                    "sequence": 10,
                }
            )

    def _remove_pipeline_menus(self):
        self.ensure_one()
        Menu = self.env["ir.ui.menu"]
        PipelineRoot = self.env.ref("crm.crm_menu_leads", raise_if_not_found=False)
        if not PipelineRoot:
            return

        existing_menu = Menu.search(
            [("parent_id", "=", PipelineRoot.id), ("name", "=", self.name)],
            limit=1,
        )
        if existing_menu:
            action = existing_menu.action
            existing_menu.unlink()
            if action and not Menu.search([("action", "=", action.id)]):
                action.unlink()
