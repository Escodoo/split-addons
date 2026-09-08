# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import csv
import io
import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class LeadImportWizard(models.Model):
    _name = "splitstudio.lead.import.wizard"
    _description = "Lead Import Wizard with Duplicate Check"
    _order = "create_date desc"

    name = fields.Char(
        string="Description",
        required=True,
        default=lambda self: _("Lead Import"),
    )
    user_id = fields.Many2one(
        "res.users",
        string="Owner",
        default=lambda self: self.env.user,
        readonly=True,
    )
    team_id = fields.Many2one(
        "crm.team",
        string="Pipeline (Sales Team)",
        required=True,
        domain="[('use_leads', '=', True)]",
    )

    @api.constrains("team_id")
    def _check_team_is_lead_pipeline(self):
        for wiz in self:
            if wiz.team_id and not wiz.team_id.use_leads:
                raise UserError(
                    _(
                        "The pipeline %(team)s does not accept leads. "
                        "Choose a pipeline with 'Leads' enabled.",
                        team=wiz.team_id.display_name,
                    )
                )
    file_data = fields.Binary(string="CSV File", required=True)
    file_name = fields.Char(string="File Name")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("preview", "Review Duplicates"),
            ("done", "Done"),
        ],
        string="Status",
        default="draft",
        required=True,
    )
    line_ids = fields.One2many(
        "splitstudio.lead.import.line",
        "wizard_id",
        string="Import Lines",
    )
    duplicate_count = fields.Integer(
        string="Duplicate Count",
        compute="_compute_duplicate_count",
    )

    def _compute_duplicate_count(self):
        for wizard in self:
            wizard.duplicate_count = sum(
                1 for line in wizard.line_ids if line.is_duplicate
            )

    def action_discard(self):
        """Permanently delete this import session and its lines."""
        self.ensure_one()
        self.unlink()
        return {"type": "ir.actions.act_window_close"}

    def _resolve_partner(self, email_clean, contact_name_clean, partner_name_clean):
        """Find an existing res.partner for the row.

        Returns a tuple (person, company):
        - person: matching contact (child or standalone person), or False
        - company: matching company the contact belongs to, or False
        """
        Partner = self.env["res.partner"]
        person = Partner
        company = Partner

        is_person_row = bool(contact_name_clean or email_clean)
        if is_person_row:
            if email_clean:
                # Try direct email match on the partner itself first
                person = Partner.search(
                    [
                        "|",
                        ("email", "=ilike", email_clean),
                        ("email_normalized", "=ilike", email_clean),
                    ],
                    limit=1,
                )
                if not person:
                    child = Partner.search(
                        [("child_ids.email", "=ilike", email_clean)],
                        limit=1,
                    )
                    if child:
                        actual = child.child_ids.filtered(
                            lambda c: c.email and c.email.lower() == email_clean
                        )[:1]
                        person = actual or child
            if not person and contact_name_clean:
                person = Partner.search(
                    [("name", "=ilike", contact_name_clean)], limit=1
                )
                if not person:
                    child = Partner.search(
                        [("child_ids.name", "=ilike", contact_name_clean)], limit=1
                    )
                    if child:
                        actual = child.child_ids.filtered(
                            lambda c: c.name and c.name.lower() == contact_name_clean.lower()
                        )[:1]
                        person = actual or child
            if person:
                company = person.parent_id if person.parent_id else (
                    person if person.is_company else Partner
                )
        elif partner_name_clean:
            company = Partner.search(
                [
                    "|",
                    ("name", "=ilike", partner_name_clean),
                    ("parent_id.name", "=ilike", partner_name_clean),
                ],
                limit=1,
            )
        return person, company

    def _resolve_campaign(self, campaign_clean):
        """Find or create a utm.campaign by name (case-insensitive).

        Returns (campaign, found_bool). If the campaign does not exist,
        it is created automatically (same behaviour as ``_resolve_tags``).
        """
        if not campaign_clean:
            return self.env["utm.campaign"], False
        campaign = self.env["utm.campaign"].search(
            [("name", "=ilike", campaign_clean)], limit=1
        )
        if not campaign:
            campaign = self.env["utm.campaign"].search(
                [("name", "ilike", campaign_clean)], limit=1
            )
        if not campaign:
            campaign = self.env["utm.campaign"].create({"name": campaign_clean})
        return campaign, bool(campaign)

    def _resolve_country(self, country_clean):
        """Find a res.country by ISO code (preferred) or name (case-insensitive).

        Accepts short codes such as ``US``, ``BR``, ``AR`` or full names like
        ``United States``. Returns an empty recordset when nothing matches.
        """
        if not country_clean:
            return self.env["res.country"]
        Country = self.env["res.country"]
        value = country_clean.strip()
        if not value:
            return Country
        country = Country.search([("code", "=ilike", value)], limit=1)
        if not country:
            country = Country.search([("name", "=ilike", value)], limit=1)
        if not country:
            country = Country.search([("name", "ilike", value)], limit=1)
        return country

    def _resolve_tags(self, tags_raw):
        """Resolve/create crm.tag records from a comma/semicolon-separated string.

        Returns the crm.tag recordset (empty if no tags in input).
        """
        if not tags_raw:
            return self.env["crm.tag"]
        names = [n.strip() for n in tags_raw.replace(";", ",").split(",") if n.strip()]
        if not names:
            return self.env["crm.tag"]
        Tag = self.env["crm.tag"]
        # Look up case-insensitive by name
        existing = Tag.search([("name", "in", names)])
        existing_names = {t.name.lower(): t for t in existing}
        to_create = []
        for name in names:
            if name.lower() not in existing_names:
                to_create.append({"name": name})
        if to_create:
            new_tags = Tag.create(to_create)
            for t in new_tags:
                existing_names[t.name.lower()] = t
        return Tag.browse([t.id for t in existing_names.values()])

    def _is_xlsx(self, file_content):
        return file_content[:2] == b"PK"

    def _read_rows_from_xlsx(self, file_content):
        try:
            import openpyxl  # noqa: PLC0415
        except ImportError as err:
            raise UserError(
                _(
                    "XLSX support requires the 'openpyxl' Python library. "
                    "Please contact your administrator."
                )
            ) from err
        workbook = openpyxl.load_workbook(io.BytesIO(file_content), data_only=True, read_only=True)
        worksheet = workbook.active
        rows = worksheet.iter_rows(values_only=True)
        try:
            header = [str(cell).strip() if cell is not None else "" for cell in next(rows)]
        except StopIteration:
            return [], []
        records = []
        for row in rows:
            if row is None or all(cell is None or cell == "" for cell in row):
                continue
            records.append({header[i]: ("" if value is None else value) for i, value in enumerate(row) if i < len(header)})
        return header, records

    def _decode_csv_bytes(self, file_content):
        if not file_content:
            return ""
        if file_content.startswith(b"\xef\xbb\xbf"):
            return file_content[3:].decode("utf-8")
        if file_content.startswith(b"\xff\xfe") or file_content.startswith(b"\xfe\xff"):
            return file_content.decode("utf-16")
        if b"\x00" in file_content:
            try:
                return file_content.decode("utf-16")
            except UnicodeDecodeError:
                pass
        try:
            return file_content.decode("utf-8")
        except UnicodeDecodeError:
            return file_content.decode("latin1")

    def action_parse_and_check(self):
        self.ensure_one()
        if not self.file_data:
            raise UserError(_("Please upload a file before checking."))

        try:
            file_content = base64.b64decode(self.file_data)
            file_name = self.file_name or ""

            if self._is_xlsx(file_content):
                _xlsx_header, parsed_rows = self._read_rows_from_xlsx(file_content)
                rows_iter = parsed_rows
            else:
                decoded_file = self._decode_csv_bytes(file_content)
                if "\x00" in decoded_file:
                    raise UserError(
                        _(
                            "Could not parse CSV file '%(name)s': it contains NUL bytes. "
                            "Please re-save it as UTF-8 (e.g. in Excel: 'Save As > CSV UTF-8').",
                            name=file_name,
                        )
                    )
                rows_iter = csv.DictReader(io.StringIO(decoded_file))
        except UserError:
            raise
        except Exception as e:
            raise UserError(
                _("Could not parse file '%(name)s': %(error)s", name=self.file_name or "", error=e)
            )

        # Clear existing lines
        self.line_ids.unlink()

        lines_to_create = []
        for row in rows_iter:
            # Expected columns:
            #   oportunidade/name → name of the lead/opportunity to be created
            #   contact_name     → person name (used to match res.partner)
            #   partner_name     → company name
            #   email, phone     → contact data
            oportunidade = (
                row.get("oportunidade")
                or row.get("Oportunidade")
                or row.get("opportunity")
                or row.get("Opportunity")
                or row.get("opportunity_id")
                or row.get("name")
                or row.get("Name")
                or row.get("Nome")
                or ""
            )
            contact_name = (
                row.get("contact_name")
                or row.get("Contact Name")
                or row.get("Contato")
                or row.get("Nome do Contato")
                or ""
            )
            email = (
                row.get("email")
                or row.get("email_from")
                or row.get("Email")
                or row.get("E-mail")
                or row.get("Email From")
                or ""
            )
            partner_name = (
                row.get("partner_name")
                or row.get("Company")
                or row.get("Empresa")
                or row.get("Nome da Empresa")
                or ""
            )
            phone = row.get("phone") or row.get("Phone") or row.get("Telefone") or ""
            website = (
                row.get("website")
                or row.get("Website")
                or row.get("Site")
                or row.get("URL")
                or ""
            )
            city = (
                row.get("city")
                or row.get("City")
                or row.get("Cidade")
                or row.get("Localidade")
                or ""
            )
            country_value = (
                row.get("country_id")
                or row.get("country")
                or row.get("Country")
                or row.get("País")
                or row.get("Pais")
                or ""
            )
            campaign = (
                row.get("campaign")
                or row.get("campaign_id")
                or row.get("Campaign")
                or row.get("Campanha")
                or row.get("UTM Campaign")
                or ""
            )
            tags_raw = (
                row.get("tags")
                or row.get("tag_ids")
                or row.get("tags_ids")
                or row.get("Tags")
                or row.get("Etiquetas")
                or row.get("Labels")
                or ""
            )
            description_raw = (
                row.get("description")
                or row.get("Description")
                or row.get("Descricao")
                or row.get("Descrição")
                or row.get("Anotações internas")
                or row.get("Anotacoes internas")
                or row.get("Internal Notes")
                or ""
            )
            priority_raw = (
                row.get("priority")
                or row.get("Priority")
                or row.get("Prioridade")
                or ""
            )

            if not oportunidade and not contact_name and not email and not partner_name:
                continue

            # Check duplicates in crm.lead and res.partner
            duplicate_reasons = []
            is_dup = False

            oportunidade_clean = oportunidade.strip()
            contact_name_clean = contact_name.strip()
            email_clean = email.strip().lower()
            partner_name_clean = partner_name.strip()

            domain_oportunidade = (
                [("name", "=ilike", oportunidade_clean)] if oportunidade_clean else []
            )
            domain_company = (
                [("partner_name", "=ilike", partner_name_clean)]
                if partner_name_clean
                else []
            )

            # Check in crm.lead
            if email_clean:
                existing_leads_email = self.env["crm.lead"].search(
                    [("email_from", "=ilike", email_clean)], limit=1
                )
                if existing_leads_email:
                    is_dup = True
                    duplicate_reasons.append(
                        _("Email exists in Lead: %s") % existing_leads_email.name
                    )

            if oportunidade_clean:
                existing_leads_name = self.env["crm.lead"].search(
                    domain_oportunidade, limit=1
                )
                if existing_leads_name:
                    is_dup = True
                    duplicate_reasons.append(
                        _("Name exists in Lead: %s") % existing_leads_name.name
                    )

            if partner_name_clean:
                existing_leads_comp = self.env["crm.lead"].search(domain_company, limit=1)
                if existing_leads_comp:
                    is_dup = True
                    duplicate_reasons.append(
                        _("Company exists in Lead: %s") % existing_leads_comp.name
                    )

            # Also check res.partner (clients)
            resolved_person, resolved_company = self._resolve_partner(
                email_clean, contact_name_clean, partner_name_clean
            )
            if resolved_person:
                is_dup = True
                duplicate_reasons.append(
                    _("Contact exists in Partner: %s") % resolved_person.display_name
                )
            if resolved_company and (not resolved_person or resolved_person != resolved_company):
                is_dup = True
                duplicate_reasons.append(
                    _("Company exists in Partner: %s") % resolved_company.display_name
                )

            reason_str = " | ".join(duplicate_reasons) if duplicate_reasons else ""

            campaign_clean = campaign.strip()
            campaign_record, _campaign_created = self._resolve_campaign(campaign_clean)
            resolved_tags = self._resolve_tags(tags_raw)
            tag_names = ",".join(resolved_tags.mapped("name")) if resolved_tags else ""
            country_record = self._resolve_country(country_value.strip())

            reason_str = " | ".join(duplicate_reasons) if duplicate_reasons else ""

            priority_value = False
            if priority_raw:
                p_raw = str(priority_raw).strip().lower()
                priority_mapping = {
                    "low": "0",
                    "very low": "0",
                    "medium": "1",
                    "med": "1",
                    "normal": "1",
                    "high": "2",
                    "hi": "2",
                    "very high": "3",
                    "urgent": "3",
                    "baixa": "0",
                    "muito baixa": "0",
                    "média": "1",
                    "media": "1",
                    "alta": "2",
                    "muito alta": "3",
                    "urgente": "3",
                    "0": "0",
                    "1": "1",
                    "2": "2",
                    "3": "3",
                }
                priority_value = priority_mapping.get(p_raw, False)

            lines_to_create.append(
                {
                    "wizard_id": self.id,
                    "name": oportunidade,
                    "contact_name": contact_name,
                    "email": email,
                    "partner_name": partner_name,
                    "phone": phone,
                    "website": website,
                    "city": city,
                    "country_id": country_record.id if country_record else False,
                    "is_duplicate": is_dup,
                    "duplicate_reason": reason_str,
                    "import_line": True,
                    "partner_id": resolved_person.id if resolved_person else False,
                    "partner_company_id": resolved_company.id if resolved_company else False,
                    "campaign_id": campaign_record.id if campaign_record else False,
                    "tag_ids": [(6, 0, resolved_tags.ids)] if resolved_tags else False,
                    "tag_names": tag_names,
                    "description": description_raw,
                    "priority": priority_value,
                }
            )

        if lines_to_create:
            self.env["splitstudio.lead.import.line"].create(lines_to_create)

        self.state = "preview"
        return {
            "type": "ir.actions.act_window",
            "res_model": "splitstudio.lead.import.wizard",
            "view_mode": "form",
            "res_id": self.id,
            "target": "new",
        }

    def action_return_from_opportunities(self):
        """Re-open this import wizard in preview state.

        Called from a server action attached to the crm.lead form. Since
        transient wizards can expire between page loads, we re-create one
        when the original is gone, scoped to the partner of the opportunity
        the user came from.
        """
        wizard_id = self.env.context.get("splitstudio_lead_import_wizard_id")
        wizard = wizard_id and self.browse(wizard_id)
        if wizard and wizard.exists():
            res_id = wizard_id
        else:
            partner_id = self.env.context.get("splitstudio_lead_import_partner_id")
            if not partner_id:
                active_id = self.env.context.get("active_id")
                if active_id:
                    partner_id = (
                        self.env["crm.lead"].browse(active_id).partner_id.id
                    )
            new_wiz = self.create({"state": "preview"})
            if partner_id:
                partner = self.env["res.partner"].browse(partner_id)
                existing_opps = self.env["crm.lead"].search(
                    [
                        ("partner_id", "=", partner.id),
                        ("type", "=", "opportunity"),
                        ("probability", "<", 100),
                    ]
                )
                company = (
                    partner.parent_id
                    if partner.parent_id
                    else (partner if partner.is_company else False)
                )
                self.env["splitstudio.lead.import.line"].create(
                    {
                        "wizard_id": new_wiz.id,
                        "name": _("Continue reviewing opportunities"),
                        "contact_name": partner.name if not partner.is_company else "",
                        "partner_name": (company.name if company else ""),
                        "email": partner.email or "",
                        "phone": partner.phone or "",
                        "is_duplicate": False,
                        "duplicate_reason": "",
                        "import_line": False,
                        "partner_id": partner.id,
                        "partner_company_id": company.id if company else False,
                    }
                )
            res_id = new_wiz.id
        return {
            "type": "ir.actions.act_window",
            "name": _("Import Leads"),
            "res_model": "splitstudio.lead.import.wizard",
            "view_mode": "form",
            "res_id": res_id,
            "target": "new",
            "context": {"default_state": "preview"},
        }

    def action_import_leads(self):
        self.ensure_one()
        Lead = self.env["crm.lead"]
        imported_count = 0

        for line in self.line_ids:
            if not line.import_line:
                continue
            # Prefer the matched person (contact) over the company. The
            # `crm.lead.partner_id` field accepts a person; the company is
            # already linked to the person via `parent_id`, so we don't
            # need to set it explicitly on the lead.
            person = line.partner_id
            company = line.partner_company_id
            lead_vals = {
                "name": line.name or _("Imported Lead"),
                "email_from": line.email,
                "partner_name": line.partner_name,
                "phone": line.phone,
                "type": "lead",
                "team_id": self.team_id.id,
            }
            if person:
                lead_vals["partner_id"] = person.id
            elif company:
                # No person match; fall back to the company.
                lead_vals["partner_id"] = company.id
            # Never create new partners here.
            if line.campaign_id:
                lead_vals["campaign_id"] = line.campaign_id.id
            if line.tag_ids:
                lead_vals["tag_ids"] = [(6, 0, line.tag_ids.ids)]
            if line.website:
                lead_vals["website"] = line.website
            if line.city:
                lead_vals["city"] = line.city
            if line.country_id:
                lead_vals["country_id"] = line.country_id.id
            if line.description:
                lead_vals["description"] = line.description
            if line.priority:
                lead_vals["priority"] = line.priority
            lead = Lead.create(lead_vals)
            if line.description:
                lead.message_post(
                    body=line.description,
                    message_type="comment",
                    subtype_xmlid="mail.mt_note",
                )
            imported_count += 1

        self.state = "done"
        return {
            "type": "ir.actions.act_window",
            "res_model": "splitstudio.lead.import.wizard",
            "view_mode": "form",
            "res_id": self.id,
            "target": "new",
        }


class LeadImportLine(models.Model):
    _name = "splitstudio.lead.import.line"
    _description = "Lead Import Wizard Line"

    wizard_id = fields.Many2one(
        "splitstudio.lead.import.wizard",
        string="Wizard",
        required=True,
        ondelete="cascade",
    )
    name = fields.Char(string="Opportunity / Lead Name")
    contact_name = fields.Char(string="Contact Name")
    email = fields.Char(string="Email")
    partner_name = fields.Char(string="Company Name")
    phone = fields.Char(string="Phone")
    is_duplicate = fields.Boolean(string="Duplicate?")
    duplicate_reason = fields.Char(string="Duplicate Reason")
    import_line = fields.Boolean(string="Import?", default=True)
    partner_id = fields.Many2one(
        "res.partner",
        string="Existing Contact",
        readonly=True,
    )
    partner_company_id = fields.Many2one(
        "res.partner",
        string="Existing Company",
        readonly=True,
    )
    opportunity_count = fields.Integer(
        string="Open Opportunities",
        compute="_compute_pipeline_count",
    )
    opportunity_summary = fields.Html(
        string="Open Opportunities Summary",
        compute="_compute_pipeline_count",
        sanitize=False,
    )
    opportunity_ids = fields.Many2many(
        "crm.lead",
        "splitstudio_lead_import_line_opp_rel",
        "line_id",
        "lead_id",
        string="Open Opportunities",
        compute="_compute_pipeline_count",
    )
    lead_count = fields.Integer(
        string="Open Leads",
        compute="_compute_pipeline_count",
    )
    lead_summary = fields.Html(
        string="Open Leads Summary",
        compute="_compute_pipeline_count",
        sanitize=False,
    )
    lead_record_ids = fields.Many2many(
        "crm.lead",
        "splitstudio_lead_import_line_lead_rel",
        "line_id",
        "lead_id",
        string="Open Leads",
        compute="_compute_pipeline_count",
    )
    campaign_id = fields.Many2one(
        "utm.campaign",
        string="Campaign",
        readonly=True,
    )
    tag_ids = fields.Many2many(
        "crm.tag",
        string="Tags",
        readonly=True,
    )
    tag_names = fields.Char(
        string="Tag Names",
        readonly=True,
    )
    description = fields.Text(
        string="Description",
        readonly=True,
    )
    priority = fields.Selection(
        [
            ("0", "Low"),
            ("1", "Medium"),
            ("2", "High"),
            ("3", "Very High"),
        ],
        string="Priority",
        readonly=True,
    )
    website = fields.Char(
        string="Website",
        readonly=True,
    )
    city = fields.Char(
        string="City",
        readonly=True,
    )
    country_id = fields.Many2one(
        "res.country",
        string="Country",
        readonly=True,
    )

    def _compute_pipeline_count(self):
        Lead = self.env["crm.lead"]
        for line in self:
            partner = line.partner_id or line.partner_company_id
            opps = Lead.browse([])
            leads = Lead.browse([])
            if partner:
                base_domain = self._build_opportunity_domain(partner)
                opps = Lead.search(
                    list(base_domain) + [("type", "=", "opportunity")],
                    order="expected_revenue desc, date_deadline asc",
                )
                leads = Lead.search(
                    list(base_domain) + [("type", "=", "lead")],
                    order="create_date desc",
                )
            line.opportunity_count = len(opps)
            line.opportunity_ids = opps
            line.opportunity_summary = self._format_pipeline_summary(opps, kind="opportunity")
            line.lead_count = len(leads)
            line.lead_record_ids = leads
            line.lead_summary = self._format_pipeline_summary(leads, kind="lead")

    def _build_opportunity_domain(self, partner):
        """Build a search domain for open opportunities matching the partner.

        Includes:
        - Opportunities directly linked via partner_id.
        - Orphan opportunities (partner_id IS NULL) whose partner_name
          matches the contact or the company name (text match, case-insensitive).
        """
        Lead = self.env["crm.lead"]
        company = (
            partner.parent_id
            if partner.parent_id
            else (partner if partner.is_company else Lead.browse([]))
        )
        name_matches = [("partner_name", "=ilike", partner.name)]
        if company and company.name and company.name != partner.name:
            name_matches = ["|", *name_matches, ("partner_name", "=ilike", company.name)]
        domain = [
            "&",
            "|",
            ("partner_id", "=", partner.id),
            "&",
            ("partner_id", "=", False),
            *name_matches,
            ("probability", "<", 100),
            "|",
            ("active", "=", True),
            ("active", "=", False),
        ]
        return domain

    def _format_pipeline_summary(self, records, kind="opportunity"):
        if not records:
            return ""
        items = []
        for rec in records:
            stage = rec.stage_id.name if rec.stage_id else ""
            if kind == "opportunity":
                revenue = (
                    "{:,.2f}".format(rec.expected_revenue).replace(",", "X").replace(".", ",").replace("X", ".")
                    if rec.expected_revenue
                    else "0,00"
                )
                items.append(
                    f"<li><strong>{rec.name}</strong> &mdash; {stage} &mdash; R$ {revenue}</li>"
                )
            else:
                items.append(
                    f"<li><strong>{rec.name}</strong> &mdash; {stage}</li>"
                )
        return (
            "<ul style='margin:0; padding-left:1em;'>"
            + "".join(items)
            + "</ul>"
        )

    def action_view_opportunities(self):
        """Open the open opportunities of the matched partner as a read-only
        pop-up on top of the wizard (3rd layer).

        The user closes the pop-up with the X / Esc to fall back to the
        wizard (2nd layer) without losing the current import state.
        """
        self.ensure_one()
        if not self.opportunity_ids:
            raise UserError(_("No open opportunities for this contact."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Open Opportunities"),
            "res_model": "crm.lead",
            "view_mode": "list,form",
            "domain": [("id", "in", self.opportunity_ids.ids)],
            "target": "new",
            "context": {
                "create": False,
                "edit": False,
                "delete": False,
                "search_default_type": "opportunity",
                "splitstudio_lead_import_wizard_id": self.wizard_id.id,
                "splitstudio_lead_import_line_id": self.id,
                "splitstudio_lead_import_partner_id": (
                    self.partner_id.id if self.partner_id else False
                ),
            },
            "flags": {
                "withBreadcrumbs": False,
            },
        }

    def action_view_leads(self):
        """Open the open leads of the matched partner as a read-only pop-up
        on top of the wizard (3rd layer)."""
        self.ensure_one()
        if not self.lead_record_ids:
            raise UserError(_("No open leads for this contact."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Open Leads"),
            "res_model": "crm.lead",
            "view_mode": "list,form",
            "domain": [("id", "in", self.lead_record_ids.ids)],
            "target": "new",
            "context": {
                "create": False,
                "edit": False,
                "delete": False,
                "search_default_type": "lead",
                "splitstudio_lead_import_wizard_id": self.wizard_id.id,
                "splitstudio_lead_import_line_id": self.id,
                "splitstudio_lead_import_partner_id": (
                    self.partner_id.id if self.partner_id else False
                ),
            },
            "flags": {
                "withBreadcrumbs": False,
            },
        }
