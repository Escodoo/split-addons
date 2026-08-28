# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models

from ..hooks import (
    _refresh_client_logos,
    _rename_default_menus,
    sync_copied_view_translations,
)


class Website(models.Model):
    _inherit = "website"

    @api.model
    def _register_hook(self):
        super()._register_hook()
        _refresh_client_logos(self.env)
        _rename_default_menus(self.env)
        sync_copied_view_translations(self.env)
