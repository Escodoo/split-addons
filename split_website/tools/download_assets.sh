#!/usr/bin/env bash
# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
# Downloads and optimises the pictures listed in assets.tsv into
# static/src/binary/ir_attachment/, then regenerates data/ir_attachment_pre.xml.
#
# Requires: curl, python3 with Pillow.
set -euo pipefail

MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="${MODULE_DIR}/tools/assets.tsv"
TARGET_DIR="${MODULE_DIR}/static/src/binary/ir_attachment"

mkdir -p "${TARGET_DIR}"

while IFS=$'\t' read -r name max_width url; do
    [[ -z "${name}" || "${name}" == \#* ]] && continue
    tmp_file="$(mktemp)"
    if ! curl -fsSL --max-time 60 -A "Mozilla/5.0" "${url}" -o "${tmp_file}"; then
        echo "FAILED ${name} <- ${url}" >&2
        rm -f "${tmp_file}"
        continue
    fi
    python3 "${MODULE_DIR}/tools/optimize_asset.py" \
        "${tmp_file}" "${TARGET_DIR}" "${name}" "${max_width}"
    rm -f "${tmp_file}"
done <"${MANIFEST}"

# The website logo field is a raster image field, so the vector brand mark also
# needs a PNG rendition.
if command -v magick >/dev/null 2>&1; then
    magick -background none -density 600 "${TARGET_DIR}/brand_logo.svg" \
        -resize 700x "${TARGET_DIR}/brand_logo_png.png" 2>/dev/null
else
    echo "magick not found, keeping the current brand_logo_png.png" >&2
fi

python3 "${MODULE_DIR}/tools/build_attachment_xml.py"

echo "Done. Total size:"
du -sh "${TARGET_DIR}"
