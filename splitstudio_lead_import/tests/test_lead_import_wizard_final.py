# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import builtins
import io
from unittest import mock

from odoo.exceptions import UserError
from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestLeadImportWizardFinal(common.TransactionCase):
    """Final round of coverage for the lead import wizard.

    Targets the remaining unhit branches reported by Codecov:

    * ``_resolve_partner`` email branch: child found, but the
      ``actual = child.child_ids.filtered(...)`` call returns a
      recordset that is falsy, so the fallback ``actual or child``
      resolves to ``child`` (the company, not a child contact).
    * ``_resolve_partner`` name branch: same as above for the name
      path.
    * ``_read_rows_from_xlsx`` with openpyxl not importable
      (``ImportError`` is converted to ``UserError``).
    * ``action_parse_and_check`` generic exception in the CSV path
      (anything that is not ``UserError`` and not ``StopIteration``
      should be wrapped as ``UserError``).
    * ``action_parse_and_check`` duplicate-by-opportunity-name branch
      (L430-438).
    * ``action_return_from_opportunities`` recreate path (L560-582):
      when the original wizard is gone we re-create one and, if a
      ``partner_id`` is provided via context, we add a single
      "Continue reviewing opportunities" line.  ``team_id`` is
      required on the wizard so the test seeds it through
      ``default_team_id`` in the context, which the ORM applies to
      the recreated wizard.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.team = cls.env["crm.team"].create(
            {
                "name": "Final Coverage Team",
                "use_leads": True,
                "use_opportunities": True,
            }
        )

    def _wiz(self):
        return self.env["splitstudio.lead.import.wizard"].create(
            {"name": "Final", "team_id": self.team.id}
        )

    def _csv_bytes(self, header, rows):
        import csv

        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=header)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
        return buf.getvalue().encode("utf-8")

    # ------------------------------------------------------------------
    # _resolve_partner: filtered() returns empty recordset (email path)
    # ------------------------------------------------------------------
    def test_01_resolve_partner_email_child_actual_via_mock(self):
        """Force the L111-115 branch where ``child.child_ids.filtered(...)``
        is called and the result drives ``person = actual or child``.
        We patch ``env['res.partner'].search`` so the direct email
        search returns nothing and the child_ids.email search returns
        a company with no children (so actual is empty)."""
        company = self.env["res.partner"].create(
            {"name": "Email Mock Co", "is_company": True}
        )
        wiz = self._wiz()
        partner_model = self.env.registry["res.partner"]

        def fake_search(self_, domain, *args, **kwargs):
            for leaf in domain:
                if isinstance(leaf, tuple) and leaf[0] in (
                    "email",
                    "email_normalized",
                ):
                    return self_.browse()
            for leaf in domain:
                if isinstance(leaf, tuple) and leaf[0] == "child_ids.email":
                    return company
            return self.env["res.partner"].browse()

        with mock.patch.object(partner_model, "search", fake_search):
            person, company_ret = wiz._resolve_partner("any@x.com", "", "")

        self.assertEqual(person, company)
        self.assertEqual(company_ret, company)

    # ------------------------------------------------------------------
    # _resolve_partner: filtered() returns empty recordset (name path)
    # ------------------------------------------------------------------
    def test_02_resolve_partner_name_child_actual_via_mock(self):
        """Same strategy as test_01 but for the name branch (L124-130).

        We also intercept the ``child_ids.email`` and direct email
        searches (returning empty) so the ``name`` and ``child_ids.name``
        searches fall through to the final ``return self_.browse()``
        fallback of the mock, which exercises that line too."""
        company = self.env["res.partner"].create(
            {"name": "Name Mock Co", "is_company": True}
        )
        wiz = self._wiz()
        partner_model = self.env.registry["res.partner"]

        def fake_search(self_, domain, *args, **kwargs):
            for leaf in domain:
                if isinstance(leaf, tuple) and leaf[0] in (
                    "email",
                    "email_normalized",
                    "child_ids.email",
                ):
                    return self_.browse()
            for leaf in domain:
                if isinstance(leaf, tuple) and leaf[0] == "child_ids.name":
                    return company
            # The direct name search reaches this fallback.
            return self_.browse()

        with mock.patch.object(partner_model, "search", fake_search):
            person, company_ret = wiz._resolve_partner("any@x.com", "Some Contact", "")

        self.assertEqual(person, company)
        self.assertEqual(company_ret, company)

    # ------------------------------------------------------------------
    # _read_rows_from_xlsx: openpyxl ImportError
    # ------------------------------------------------------------------
    def test_03_read_rows_from_xlsx_raises_usererror_when_openpyxl_missing(self):
        """When ``import openpyxl`` fails inside ``_read_rows_from_xlsx``
        the wizard must raise a ``UserError``."""
        wiz = self._wiz()
        real_import = builtins.__import__

        def fake_import(name, *args, **kwargs):
            if name == "openpyxl":
                raise ImportError("No module named 'openpyxl'")
            return real_import(name, *args, **kwargs)

        with mock.patch("builtins.__import__", side_effect=fake_import):
            with self.assertRaises(UserError):
                wiz._read_rows_from_xlsx(b"not really xlsx")

    # ------------------------------------------------------------------
    # action_parse_and_check: generic exception in CSV path
    # ------------------------------------------------------------------
    def test_04_action_parse_and_check_wraps_generic_exception(self):
        """When csv.DictReader raises something that is neither
        UserError nor StopIteration, action_parse_and_check must wrap
        it in a UserError mentioning the file name."""
        wiz = self._wiz()
        wiz.write(
            {
                "file_data": base64.b64encode(b"name,email\nA,a@x.com\n"),
                "file_name": "broken.csv",
            }
        )
        with mock.patch(
            "odoo.addons.splitstudio_lead_import.wizards.lead_import_wizard.csv.DictReader",
            side_effect=ValueError("simulated csv failure"),
        ):
            with self.assertRaises(UserError) as cm:
                wiz.action_parse_and_check()
        self.assertIn("broken.csv", str(cm.exception))

    # ------------------------------------------------------------------
    # action_parse_and_check: duplicate detection by opportunity name
    # ------------------------------------------------------------------
    def test_05_duplicate_detection_by_opportunity_name(self):
        """An opportunity name that already exists in crm.lead flags
        the imported row as duplicate."""
        self.env["crm.lead"].create(
            {"name": "Existing Opportunity", "type": "opportunity"}
        )
        wiz = self._wiz()
        wiz.write(
            {
                "file_data": base64.b64encode(
                    self._csv_bytes(
                        ["name", "email"],
                        [
                            {
                                "name": "Existing Opportunity",
                                "email": "new_unique@x.com",
                            }
                        ],
                    )
                ),
                "file_name": "opp.csv",
            }
        )
        wiz.action_parse_and_check()
        line = wiz.line_ids[0]
        self.assertTrue(line.is_duplicate)
        self.assertIn("Name exists in Lead", line.duplicate_reason)

    # ------------------------------------------------------------------
    # action_return_from_opportunities: full recreate path
    # ------------------------------------------------------------------
    def test_06_action_return_from_opportunities_recreate_with_partner(self):
        """When the original wizard is gone, action_return_from_opportunities
        recreates a wizard in 'preview' state and, if a partner is
        provided via context, adds a 'Continue reviewing opportunities'
        line referencing that partner."""
        Wizard = self.env["splitstudio.lead.import.wizard"]
        partner = self.env["res.partner"].create(
            {"name": "Return Partner Co", "is_company": True}
        )
        # Use default_team_id so the recreated wizard satisfies the
        # required team_id field.
        result = (
            Wizard.with_context(
                default_team_id=self.team.id,
                splitstudio_lead_import_partner_id=partner.id,
            )
            .create({"name": "Outer", "team_id": self.team.id})
            .action_return_from_opportunities()
        )
        self.assertEqual(result["res_model"], "splitstudio.lead.import.wizard")
        new_wiz = Wizard.browse(result["res_id"])
        # The recreated wizard must be in 'preview' state and contain
        # the seeded line.
        self.assertEqual(new_wiz.state, "preview")
        self.assertEqual(len(new_wiz.line_ids), 1)
        self.assertEqual(new_wiz.line_ids[0].partner_id, partner)
        self.assertEqual(new_wiz.line_ids[0].partner_company_id, partner)

    def test_07_action_return_from_opportunities_recreate_no_partner(self):
        """The recreate path with no partner_id in context must still
        succeed, creating a wizard with no lines."""
        Wizard = self.env["splitstudio.lead.import.wizard"]
        result = (
            Wizard.with_context(default_team_id=self.team.id)
            .create({"name": "Outer", "team_id": self.team.id})
            .action_return_from_opportunities()
        )
        new_wiz = Wizard.browse(result["res_id"])
        self.assertEqual(new_wiz.state, "preview")
        self.assertFalse(new_wiz.line_ids)

    def test_08_action_return_from_opportunities_recreate_with_active_id(self):
        """When the original wizard is gone and the context carries
        ``active_id`` (but no ``splitstudio_lead_import_partner_id``),
        the recreate path resolves ``partner_id`` from the related
        crm.lead.partner_id (L555-559)."""
        Wizard = self.env["splitstudio.lead.import.wizard"]
        partner = self.env["res.partner"].create(
            {"name": "Active Id Partner", "is_company": True}
        )
        lead = self.env["crm.lead"].create(
            {
                "name": "Active Id Lead",
                "type": "lead",
                "team_id": self.team.id,
                "partner_id": partner.id,
            }
        )
        result = (
            Wizard.with_context(
                default_team_id=self.team.id,
                active_id=lead.id,
            )
            .create({"name": "Outer", "team_id": self.team.id})
            .action_return_from_opportunities()
        )
        new_wiz = Wizard.browse(result["res_id"])
        self.assertEqual(new_wiz.state, "preview")
        self.assertEqual(len(new_wiz.line_ids), 1)
        self.assertEqual(new_wiz.line_ids[0].partner_id, partner)

    # ------------------------------------------------------------------
    # _resolve_partner: all-empty inputs (exercises elif False branch)
    # ------------------------------------------------------------------
    def test_09_resolve_partner_all_empty(self):
        """Calling ``_resolve_partner`` with empty email, name and
        partner_name returns an empty recordset pair.  This exercises
        the ``elif partner_name_clean:`` False branch (L137->146) and
        the early ``return`` at L146."""
        wiz = self._wiz()
        person, company = wiz._resolve_partner("", "", "")
        self.assertFalse(person)
        self.assertFalse(company)

    # ------------------------------------------------------------------
    # action_parse_and_check: oportunidade empty (skip branch L430->440)
    # ------------------------------------------------------------------
    def test_10_action_parse_skips_oportunidade_branch_when_empty(self):
        """When the spreadsheet row has an empty ``name``/``oportunidade``
        column, the ``if oportunidade_clean:`` branch in
        ``action_parse_and_check`` is skipped.  This exercises the
        L430->L440 edge."""
        wiz = self._wiz()
        wiz.write(
            {
                "file_data": base64.b64encode(
                    self._csv_bytes(
                        ["name", "email", "partner_name"],
                        [
                            {
                                "name": "",
                                "email": "no_name@x.com",
                                "partner_name": "Some Co",
                            }
                        ],
                    )
                ),
                "file_name": "noname.csv",
            }
        )
        wiz.action_parse_and_check()
        self.assertEqual(len(wiz.line_ids), 1)

    # ------------------------------------------------------------------
    # _resolve_partner: mock fallback reached (L92)
    # ------------------------------------------------------------------
    def test_11_resolve_partner_reaches_mock_fallback(self):
        """Patch ``Partner.search`` so every domain falls through to the
        final ``return self.env[...]`` line of the mock.  This exercises
        the test-side fallback branch and confirms the wizard handles
        the all-empty-via-mock case without crashing."""
        self.env["res.partner"].create({"name": "Fallback Probe"})
        wiz = self._wiz()
        partner_model = self.env.registry["res.partner"]

        def fake_search(self_, domain, *args, **kwargs):
            return self.env["res.partner"].browse()

        with mock.patch.object(partner_model, "search", fake_search):
            # email is set so the email/child_ids.email branches
            # execute; both fall through to the mock fallback.
            person, company_ret = wiz._resolve_partner(
                "fallback@x.com", "Some Contact", "Some Co"
            )

        self.assertFalse(person)
        self.assertFalse(company_ret)
