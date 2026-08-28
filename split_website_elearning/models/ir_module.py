# Copyright 2026 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    def _update_translations(self, filter_lang=None, overwrite=False):
        res = super()._update_translations(
            filter_lang=filter_lang, overwrite=overwrite
        )
        if self.filtered(lambda module: module.name == "split_website_elearning"):
            self.env["website"]._split_sync_academy_view_translations()
        return res
