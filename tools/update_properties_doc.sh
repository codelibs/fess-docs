#!/bin/bash
# Regenerate <lang>/<version>/config/properties.rst from a fess checkout.
#
# The page lists every configuration property Fess reads. Kept by hand it rotted, so it
# is generated and only the prose around the tables is written by a person.
#
#   fess_config.properties     the keys, defaults, English descriptions, headings and
#                              order. It lives in the fess repository. Edit this.
#   <lang>/.../properties.po   the translations, per language and per version. Edit these
#                              and run this script again; existing translations are kept.
#   <lang>/.../properties.rst  the page. Generated between the GENERATED markers.
#
# fess_config.properties is not copied into this repository, so this script needs a fess
# checkout. CI cannot run it, and does not: it runs `--check`, which validates the seven
# pages against each other and against their catalogues without needing fess.
#
# Usage:
#     tools/update_properties_doc.sh [path-to-fess-checkout]
#     FESS_DIR=/somewhere/fess tools/update_properties_doc.sh
#
# The version written is the "development" value in versions.json.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FESS_DIR="${1:-${FESS_DIR:-$ROOT/../fess}}"
PROPERTIES="$FESS_DIR/src/main/resources/fess_config.properties"

if [ ! -f "$PROPERTIES" ]; then
    echo "fess_config.properties not found at: $PROPERTIES" >&2
    echo "Pass the path to a fess checkout: tools/update_properties_doc.sh /path/to/fess" >&2
    exit 1
fi

exec python3 "$ROOT/tools/gen_properties_doc.py" --properties "$PROPERTIES"
