# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import io
import zipfile

from odoo.exceptions import UserError
from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestLeadImportWizardFileParsing(common.TransactionCase):
    """Cover the file-format / encoding paths in the lead import wizard:

    - _is_xlsx (PK signature detection)
    - _read_rows_from_xlsx (XLSX import path with the openpyxl backend)
    - _decode_csv_bytes (BOM, UTF-16, latin1 fallback)
    - action_parse_and_check routing to the XLSX path
    - _resolve_partner child_ids branch where the actual contact is found
    - action_import_leads when only a company partner matches
    - _compute_pipeline_count when no partner matches
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.team = cls.env["crm.team"].create(
            {
                "name": "File Parsing Team",
                "use_leads": True,
                "use_opportunities": True,
            }
        )

    def _build_xlsx(self, header, rows):
        from openpyxl import Workbook

        wb = Workbook()
        ws = wb.active
        ws.append(header)
        for row in rows:
            ws.append(row)
        buf = io.BytesIO()
        wb.save(buf)
        return buf.getvalue()

    def _csv(self, header, rows):
        import csv

        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=header)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
        return base64.b64encode(buf.getvalue().encode("utf-8"))

    def _empty_wizard(self, file_name="x.csv"):
        """Create a wizard with a minimal valid CSV (no data rows)."""
        b64 = self._csv(["name", "email"], [])
        return self.env["splitstudio.lead.import.wizard"].create(
            {
                "name": "File Parsing",
                "team_id": self.team.id,
                "file_data": b64,
                "file_name": file_name,
                "state": "draft",
            }
        )

    def _xlsx_wizard(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("a", "b")
        return self.env["splitstudio.lead.import.wizard"].create(
            {
                "name": "File Parsing",
                "team_id": self.team.id,
                "file_data": base64.b64encode(buf.getvalue()),
                "file_name": "x.xlsx",
                "state": "draft",
            }
        )

    # ------------------------------------------------------------------
    # _is_xlsx
    # ------------------------------------------------------------------
    def test_01_is_xlsx_true_for_zip(self):
        """A file starting with 'PK' (zip signature) is XLSX."""
        wiz = self._xlsx_wizard()
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("a", "b")
        self.assertTrue(wiz._is_xlsx(buf.getvalue()))

    def test_02_is_xlsx_false_for_plain_bytes(self):
        """Plain CSV content does not start with 'PK'."""
        wiz = self._empty_wizard()
        self.assertFalse(wiz._is_xlsx(base64.b64decode(wiz.file_data)))

    # ------------------------------------------------------------------
    # _read_rows_from_xlsx
    # ------------------------------------------------------------------
    def test_03_read_rows_from_xlsx_roundtrip(self):
        xlsx_bytes = self._build_xlsx(
            ["name", "email"],
            [["Alpha", "alpha@x.com"], ["Beta", "beta@x.com"]],
        )
        wiz = self._xlsx_wizard()
        header, records = wiz._read_rows_from_xlsx(xlsx_bytes)
        self.assertEqual(header, ["name", "email"])
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["name"], "Alpha")
        self.assertEqual(records[1]["email"], "beta@x.com")

    def test_04_read_rows_from_xlsx_empty_sheet(self):
        """An xlsx with only the header returns one empty record list."""
        xlsx_bytes = self._build_xlsx(["name", "email"], [])
        wiz = self._xlsx_wizard()
        header, records = wiz._read_rows_from_xlsx(xlsx_bytes)
        self.assertEqual(header, ["name", "email"])
        self.assertEqual(records, [])

    def test_05_read_rows_from_xlsx_skips_blank_rows(self):
        """Completely blank rows are skipped."""
        xlsx_bytes = self._build_xlsx(
            ["name", "email"],
            [["Keep", "k@x.com"], [None, None], ["", ""], ["Also Keep", "a@x.com"]],
        )
        wiz = self._xlsx_wizard()
        _header, records = wiz._read_rows_from_xlsx(xlsx_bytes)
        self.assertEqual(len(records), 2)
        self.assertEqual([r["name"] for r in records], ["Keep", "Also Keep"])

    # ------------------------------------------------------------------
    # action_parse_and_check XLSX path
    # ------------------------------------------------------------------
    def test_06_action_parse_xlsx(self):
        xlsx_bytes = self._build_xlsx(
            ["name", "email"],
            [["Xlsx Lead", "xl@x.com"]],
        )
        wiz = self.env["splitstudio.lead.import.wizard"].create(
            {
                "name": "File Parsing",
                "team_id": self.team.id,
                "file_data": base64.b64encode(xlsx_bytes),
                "file_name": "leads.xlsx",
                "state": "draft",
            }
        )
        wiz.action_parse_and_check()
        self.assertEqual(wiz.state, "preview")
        self.assertEqual(len(wiz.line_ids), 1)
        self.assertEqual(wiz.line_ids.name, "Xlsx Lead")

    # ------------------------------------------------------------------
    # _decode_csv_bytes
    # ------------------------------------------------------------------
    def test_07_decode_csv_bytes_utf8(self):
        wiz = self._empty_wizard()
        self.assertEqual(wiz._decode_csv_bytes(b"hello"), "hello")

    def test_08_decode_csv_bytes_utf8_bom(self):
        wiz = self._empty_wizard()
        content = b"\xef\xbb\xbfhello"
        self.assertEqual(wiz._decode_csv_bytes(content), "hello")

    def test_09_decode_csv_bytes_empty(self):
        wiz = self._empty_wizard()
        self.assertEqual(wiz._decode_csv_bytes(b""), "")

    def test_10_decode_csv_bytes_none(self):
        wiz = self._empty_wizard()
        self.assertEqual(wiz._decode_csv_bytes(None), "")

    def test_11_decode_csv_bytes_latin1_fallback(self):
        """Bytes that fail UTF-8 decoding fall back to latin1."""
        wiz = self._empty_wizard()
        # 0xe9 is valid in latin1 ('é') but invalid as a leading byte
        # in UTF-8 on its own. Avoid 0x00 (UTF-16 routing) and 0xff 0xfe
        # (UTF-16 BOM).
        content = b"caf\xe9 plain"
        result = wiz._decode_csv_bytes(content)
        self.assertIsInstance(result, str)
        self.assertIn("plain", result)

    # ------------------------------------------------------------------
    # action_parse_and_check: NUL bytes in CSV path
    # ------------------------------------------------------------------
    def test_12_action_parse_csv_with_nul_bytes_raises(self):
        wiz = self._empty_wizard()
        wiz.write({"file_data": base64.b64encode(b"\x00name,email\n\x00")})
        with self.assertRaises(UserError):
            wiz.action_parse_and_check()

    # ------------------------------------------------------------------
    # _resolve_partner: child_ids branch where the actual contact is found
    # ------------------------------------------------------------------
    def test_13_resolve_partner_via_email_child_with_actual(self):
        """Email match on a child_ids child resolves to the actual child."""
        company = self.env["res.partner"].create(
            {"name": "Email Child Co", "is_company": True}
        )
        self.env["res.partner"].create(
            {
                "name": "Other Child",
                "email": "other@x.com",
                "parent_id": company.id,
            }
        )
        target = self.env["res.partner"].create(
            {
                "name": "Right Child",
                "email": "right@x.com",
                "parent_id": company.id,
            }
        )
        wiz = self._empty_wizard()
        person, company_ret = wiz._resolve_partner("right@x.com", "", "")
        self.assertEqual(person, target)
        self.assertEqual(company_ret, company)

    def test_14_resolve_partner_via_name_child_with_actual(self):
        """Name match on a child_ids child resolves to the actual child."""
        company = self.env["res.partner"].create(
            {"name": "Name Child Co", "is_company": True}
        )
        self.env["res.partner"].create({"name": "Other Name", "parent_id": company.id})
        target = self.env["res.partner"].create(
            {"name": "Target Name", "parent_id": company.id}
        )
        wiz = self._empty_wizard()
        person, company_ret = wiz._resolve_partner("", "Target Name", "")
        self.assertEqual(person, target)
        self.assertEqual(company_ret, company)

    # ------------------------------------------------------------------
    # action_import_leads: partner match but person is a company only
    # ------------------------------------------------------------------
    def test_15_action_import_leads_company_with_only_company_partner(self):
        """When the matched partner is a company (no separate person), the
        lead is attached to the company as the partner_id."""
        company = self.env["res.partner"].create(
            {"name": "Import Co Only", "is_company": True}
        )
        csv_bytes = self._csv(
            ["name", "partner_name"],
            [{"name": "Orphan Lead", "partner_name": "Import Co Only"}],
        )
        wiz = self.env["splitstudio.lead.import.wizard"].create(
            {
                "name": "File Parsing",
                "team_id": self.team.id,
                "file_data": csv_bytes,
                "file_name": "test.csv",
                "state": "draft",
            }
        )
        wiz.action_parse_and_check()
        line = wiz.line_ids[0]
        line.write({"partner_company_id": company.id})
        wiz.action_import_leads()
        lead = self.env["crm.lead"].search([("name", "=", "Orphan Lead")])
        self.assertEqual(lead.partner_id, company)

    # ------------------------------------------------------------------
    # _compute_pipeline_count when no partner
    # ------------------------------------------------------------------
    def test_16_compute_pipeline_count_without_partner(self):
        """A line with no partner has zero opportunities and leads."""
        csv_bytes = self._csv(
            ["name", "email"],
            [{"name": "No Partner Line", "email": "np@x.com"}],
        )
        wiz = self.env["splitstudio.lead.import.wizard"].create(
            {
                "name": "File Parsing",
                "team_id": self.team.id,
                "file_data": csv_bytes,
                "file_name": "test.csv",
                "state": "draft",
            }
        )
        wiz.action_parse_and_check()
        line = wiz.line_ids[0]
        line._compute_pipeline_count()
        self.assertEqual(line.opportunity_count, 0)
        self.assertEqual(line.lead_count, 0)
        self.assertFalse(line.opportunity_ids)
        self.assertFalse(line.lead_record_ids)

    def test_16b_compute_pipeline_count_empty_email_and_name_skips(self):
        """A line with no partner, no email, and no name skips the fallback."""
        csv_bytes = self._csv(
            ["name", "email"],
            [{"name": "Some Name", "email": "some@x.com"}],
        )
        wiz = self.env["splitstudio.lead.import.wizard"].create(
            {
                "name": "Empty Line",
                "team_id": self.team.id,
                "file_data": csv_bytes,
                "file_name": "test.csv",
                "state": "draft",
            }
        )
        wiz.action_parse_and_check()
        line = wiz.line_ids[0]
        line.write({"name": "", "email": ""})
        line._compute_pipeline_count()
        self.assertEqual(line.opportunity_count, 0)
        self.assertEqual(line.lead_count, 0)

    def test_17_compute_pipeline_count_matches_by_email(self):
        """A line without partner matches an existing lead by email."""
        lead = self.env["crm.lead"].create(
            {
                "name": "Existing Lead",
                "type": "lead",
                "email_from": "match@x.com",
                "team_id": self.team.id,
            }
        )
        csv_bytes = self._csv(
            ["name", "email"],
            [{"name": "Import Line", "email": "match@x.com"}],
        )
        wiz = self.env["splitstudio.lead.import.wizard"].create(
            {
                "name": "Email Match",
                "team_id": self.team.id,
                "file_data": csv_bytes,
                "file_name": "test.csv",
                "state": "draft",
            }
        )
        wiz.action_parse_and_check()
        line = wiz.line_ids[0]
        line._compute_pipeline_count()
        self.assertEqual(line.lead_count, 1)
        self.assertIn(lead, line.lead_record_ids)

    def test_18_compute_pipeline_count_matches_by_name(self):
        """A line without partner matches an existing lead by name."""
        lead = self.env["crm.lead"].create(
            {
                "name": "Known Prospect",
                "type": "lead",
                "team_id": self.team.id,
            }
        )
        csv_bytes = self._csv(
            ["name", "email"],
            [{"name": "Known Prospect", "email": "unknown@x.com"}],
        )
        wiz = self.env["splitstudio.lead.import.wizard"].create(
            {
                "name": "Name Match",
                "team_id": self.team.id,
                "file_data": csv_bytes,
                "file_name": "test.csv",
                "state": "draft",
            }
        )
        wiz.action_parse_and_check()
        line = wiz.line_ids[0]
        line._compute_pipeline_count()
        self.assertEqual(line.lead_count, 1)
        self.assertIn(lead, line.lead_record_ids)

    def test_19_compute_pipeline_count_matches_by_email_and_name(self):
        """A line without partner matches an opportunity by both email and name."""
        opp = self.env["crm.lead"].create(
            {
                "name": "Big Deal",
                "type": "opportunity",
                "email_from": "deal@x.com",
                "team_id": self.team.id,
            }
        )
        csv_bytes = self._csv(
            ["name", "email"],
            [{"name": "Big Deal", "email": "deal@x.com"}],
        )
        wiz = self.env["splitstudio.lead.import.wizard"].create(
            {
                "name": "Both Match",
                "team_id": self.team.id,
                "file_data": csv_bytes,
                "file_name": "test.csv",
                "state": "draft",
            }
        )
        wiz.action_parse_and_check()
        line = wiz.line_ids[0]
        line._compute_pipeline_count()
        self.assertEqual(line.opportunity_count, 1)
        self.assertIn(opp, line.opportunity_ids)

    def test_20_compute_pipeline_count_empty_name_skips_name_domain(self):
        """A line with empty name only searches by email."""
        lead = self.env["crm.lead"].create(
            {
                "name": "Some Lead",
                "type": "lead",
                "email_from": "solo@x.com",
                "team_id": self.team.id,
            }
        )
        csv_bytes = self._csv(
            ["name", "email"],
            [{"name": "", "email": "solo@x.com"}],
        )
        wiz = self.env["splitstudio.lead.import.wizard"].create(
            {
                "name": "Email Only",
                "team_id": self.team.id,
                "file_data": csv_bytes,
                "file_name": "test.csv",
                "state": "draft",
            }
        )
        wiz.action_parse_and_check()
        line = wiz.line_ids[0]
        line._compute_pipeline_count()
        self.assertEqual(line.lead_count, 1)
        self.assertIn(lead, line.lead_record_ids)

    def test_21_compute_pipeline_count_empty_email_skips_email_domain(self):
        """A line with empty email only searches by name."""
        lead = self.env["crm.lead"].create(
            {
                "name": "Name Only Lead",
                "type": "lead",
                "team_id": self.team.id,
            }
        )
        csv_bytes = self._csv(
            ["name", "email"],
            [{"name": "Name Only Lead", "email": ""}],
        )
        wiz = self.env["splitstudio.lead.import.wizard"].create(
            {
                "name": "Name Only",
                "team_id": self.team.id,
                "file_data": csv_bytes,
                "file_name": "test.csv",
                "state": "draft",
            }
        )
        wiz.action_parse_and_check()
        line = wiz.line_ids[0]
        line._compute_pipeline_count()
        self.assertEqual(line.lead_count, 1)
        self.assertIn(lead, line.lead_record_ids)
