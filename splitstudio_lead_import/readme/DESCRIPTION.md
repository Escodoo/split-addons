## SplitStudio Lead Import

This module provides a wizard for importing leads from CSV or XLSX files
with advanced duplicate checking. Before creating the leads in CRM, it
checks existing records in both `crm.lead` and `res.partner` by:

- Email
- Lead / Contact Name
- Company / Partner Name

If duplicates are found, they are highlighted in red with reasons
provided, giving the user full control to review or skip specific lines
before confirming the import.

Campaigns and tags referenced in the spreadsheet are matched against
existing records and **created on the fly** when missing. The optional
`description` column is stored on the lead and also posted as an
internal note in the chatter, and the optional `priority` column
controls the priority stars shown on the lead form.
