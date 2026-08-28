# Copyright 2026 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models

from .website import ACADEMY_COURSE_COVER_PROPERTIES


class SlideChannel(models.Model):
    _inherit = "slide.channel"

    def _default_cover_properties(self):
        """Keep new Academia courses on navy instead of the stock Odoo purple."""
        res = super()._default_cover_properties()
        academy = self.env.ref(
            "split_website_elearning.website_academia", raise_if_not_found=False
        )
        website_id = self.env.context.get("website_id")
        if academy and website_id == academy.id:
            res.update(ACADEMY_COURSE_COVER_PROPERTIES)
        return res
