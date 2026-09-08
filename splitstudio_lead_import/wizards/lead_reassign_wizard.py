# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class CrmLeadReassignWizard(models.TransientModel):
    _name = "crm.lead.reassign.wizard"
    _description = "Move a lead/opportunity to another sales team"

    lead_id = fields.Many2one(
        "crm.lead",
        string="Lead / Opportunity",
        required=True,
        readonly=True,
    )
    new_team_id = fields.Many2one(
        "crm.team",
        string="New Pipeline",
        required=True,
        domain="[('id', '!=', False)]",
    )
    note = fields.Char(string="Reason (optional)")

    @api.onchange("lead_id")
    def _onchange_lead_id(self):
        """Constrain `new_team_id` to teams that receive the same kind of
        record (lead or opportunity) as the selected one.
        """
        if not self.lead_id:
            return
        if self.lead_id.type == "lead":
            domain = [("use_leads", "=", True)]
        else:
            domain = [("use_opportunities", "=", True)]
        return {"domain": {"new_team_id": domain}}

    def action_reassign(self):
        """Move the lead/opportunity to the selected sales team.

        The Odoo core recomputes `stage_id` automatically via
        ``@api.depends('team_id', 'type')`` so the new pipeline's
        equivalent stage is set.
        """
        self.ensure_one()
        if self.new_team_id == self.lead_id.team_id:
            return {"type": "ir.actions.act_window_close"}
        self.lead_id.write({"team_id": self.new_team_id.id})
        return {"type": "ir.actions.act_window_close"}

    def action_open_reassign_wizard(self):
        """Server-action entry point from a lead/opportunity header.

        Computes the proper domain for ``new_team_id`` based on the
        current lead's type (leads vs opportunities).
        """
        lead = self.env["crm.lead"].browse(self.env.context.get("active_id"))
        if lead.type == "lead":
            domain = [("use_leads", "=", True)]
        else:
            domain = [("use_opportunities", "=", True)]
        return {
            "type": "ir.actions.act_window",
            "name": _("Move to another pipeline"),
            "res_model": "crm.lead.reassign.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_lead_id": lead.id,
                "default_new_team_id": lead.team_id.id,
                "default_domain_new_team_id": domain,
            },
        }
