# Link orphan opportunities (partner_id IS NULL) to the matching
# res.partner by name. Run via:
#   Get-Content tools/link_orphans.py -Raw | docker compose -f
#   "\\wsl.localhost\Ubuntu\home\polloskki\~projetos\odoo-doodba\devel.yaml"
#   exec -T odoo odoo shell -d splitstudio --no-http --log-level=warn

Lead = env["crm.lead"]
Partner = env["res.partner"]

orphans = Lead.search(
    [
        ("type", "=", "opportunity"),
        ("partner_id", "=", False),
        "|",
        ("active", "=", True),
        ("active", "=", False),
    ]
)
print(f"Found {len(orphans)} orphan opportunities")

linked = 0
for opp in orphans:
    # Prefer contact_name (the person) over partner_name (the company).
    # Most leads with partner_id IS NULL have a contact_name set even when
    # partner_name is just a free-text label.
    target_name = opp.contact_name or opp.partner_name
    if not target_name:
        print(f"  Skipped opp {opp.id} (no contact_name / partner_name)")
        continue
    partner = Partner.search([("name", "=ilike", target_name)], limit=1)
    if partner:
        opp.write({"partner_id": partner.id})
        linked += 1
        print(
            f"  Linked opp {opp.id} ({opp.name!r}) -> partner "
            f"{partner.id} ({partner.display_name!r})"
        )
    else:
        print(f"  No match for opp {opp.id} (target_name={target_name!r})")

env.cr.commit()
print(f"\nDone. Linked {linked} of {len(orphans)} orphans.")
