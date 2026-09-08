==========================
Usage
==========================

1. Go to **CRM > Pipelines** and open the desired pipeline's **Import
   Leads** action, or use **CRM > Import Sessions** to review previous
   imports.
2. Pick the pipeline (sales team) that will receive the leads.
3. Upload your **XLSX** or **CSV** file.
4. Click **Check Duplicates & Preview**.
5. Review the parsed lines. Potential duplicates are highlighted with
   the reasons why they matched existing records. Each line also shows
   the count of open opportunities and open leads already attached to
   the matched contact; click the list icon to open them in a
   read-only pop-up.
6. Uncheck any lines you do not wish to import, then click **Confirm
   Import**.

Recognised spreadsheet columns
==============================

============================= ============================================
Column                         Notes
============================= ============================================
``oportunidade`` / ``opportunity`` / ``name`` Required: lead/opportunity name.
``contact_name`` / ``Contato``   Used to match an existing contact.
``email`` / ``email_from``       Match priority: email > name.
``partner_name`` / ``Empresa``   Company name; matched against res.partner.
``phone`` / ``Telefone``
``campaign`` / ``campaign_id``   Campaigns that do not exist are created.
``tags`` / ``tag_ids``           Comma- or semicolon-separated; missing
                                  tags are created automatically.
``description``                  Stored on the lead and posted as a
                                  chatter internal note.
``priority``                     ``Low`` / ``Medium`` / ``High`` /
                                  ``Very High`` (or 0/1/2/3) maps to the
                                  priority stars widget.
``website`` / ``Site``
``city`` / ``Cidade``
``country_id`` / ``País``        ISO code (``BR``, ``US``) or full name.
============================= ============================================
