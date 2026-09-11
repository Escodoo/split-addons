# Link orphan opportunities (partner_id IS NULL) to the matching
# res.partner by name. Run via:
#   Get-Content tools/link_orphans.py -Raw | docker compose -f
#   "\\wsl.localhost\Ubuntu\home\polloskki\~projetos\odoo-doodba\devel.yaml"
#   exec -T odoo odoo shell -d splitstudio --no-http --log-level=warn

# ruff: noqa: F821  # `env` is provided by `odoo shell`.
import logging

_logger = logging.getLogger(__name__)

Lead = env["crm.lead"]  # noqa: F821
Partner = env["res.partner"]  # noqa: F821

orphans = Lead.search(
    [
        ("type", "=", "opportunity"),
        ("partner_id", "=", False),
        "|",
        ("active", "=", True),
        ("active", "=", False),
    ]
)
_logger.info("Found %s orphan opportunities", len(orphans))

linked = 0
for opp in orphans:
    target_name = opp.contact_name or opp.partner_name
    if not target_name:
        _logger.info("Skipped opp %s (no contact_name / partner_name)", opp.id)
        continue
    partner = Partner.search([("name", "=ilike", target_name)], limit=1)
    if partner:
        opp.write({"partner_id": partner.id})
        linked += 1
        _logger.info(
            "Linked opp %s (%r) -> partner %s (%r)",
            opp.id,
            opp.name,
            partner.id,
            partner.display_name,
        )
    else:
        _logger.info("No match for opp %s (target_name=%r)", opp.id, target_name)

env.cr.commit()  # noqa: F821
_logger.info("Done. Linked %s of %s orphans.", linked, len(orphans))
