#!/usr/bin/env python3
"""Regenerate the maintenance tables in <lang>/eol.rst from versions.json.

The same table -- which Fess versions are supported, and when each one reaches
end of life -- appears in all seven translations. Keeping seven copies in step
by hand is how they drift, so the rows are generated here and only the wording
around them is translated.

What each file records:

  versions.json   which versions are supported and when they end. Edit this.
  <lang>/eol.rst  the surrounding prose, headings and column labels, plus the
                  generated rows between the GENERATED markers. Edit everything
                  except what is between the markers.

Whether a version is supported is stated in versions.json, not worked out from
its date. A version does not stop being supported because a date passed while
nobody was looking -- someone decides, and the decision is a commit. The dates
are still checked against that decision, and a version whose date has gone by
while it is still listed as supported is reported so it can be dealt with.

Usage:
    python3 tools/update_eol.py            rewrite the tables
    python3 tools/update_eol.py --check    report what would change, change nothing
"""
from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
VERSIONS = ROOT / "versions.json"

BEGIN = ".. GENERATED-BEGIN: {name} -- from versions.json via tools/update_eol.py"
END = ".. GENERATED-END: {name}"

# Column labels and status wording per language. Everything here is prose, so it
# lives with the translations rather than in versions.json.
LABELS = {
    "ja": {
        "supported_header": ["Fess", "EOL日付", "ステータス"],
        "eol_header": ["Fess", "EOL日付"],
        "release": "🟢 最新版（推奨）",
        "supported": "🟢 サポート中",
        "nearing": "🟡 サポート終了間近",
    },
    "en": {
        "supported_header": ["Fess", "EOL Date", "Status"],
        "eol_header": ["Fess", "EOL Date"],
        "release": "🟢 Latest (Recommended)",
        "supported": "🟢 Supported",
        "nearing": "🟡 Nearing End of Support",
    },
    "de": {
        "supported_header": ["Fess", "EOL-Datum", "Status"],
        "eol_header": ["Fess", "EOL-Datum"],
        "release": "🟢 Neueste (Empfohlen)",
        "supported": "🟢 Unterstützt",
        "nearing": "🟡 Support-Ende naht",
    },
    "es": {
        "supported_header": ["Fess", "Fecha de EOL", "Estado"],
        "eol_header": ["Fess", "Fecha de EOL"],
        "release": "🟢 Ultima (Recomendada)",
        "supported": "🟢 Con soporte",
        "nearing": "🟡 Proximo al fin de soporte",
    },
    "fr": {
        "supported_header": ["Fess", "Date EOL", "Statut"],
        "eol_header": ["Fess", "Date EOL"],
        "release": "🟢 Dernière version (recommandée)",
        "supported": "🟢 Prise en charge",
        "nearing": "🟡 Fin de support proche",
    },
    "zh-cn": {
        "supported_header": ["Fess", "EOL 日期", "状态"],
        "eol_header": ["Fess", "EOL 日期"],
        "release": "🟢 最新版（推荐）",
        "supported": "🟢 支持中",
        "nearing": "🟡 即将终止支持",
    },
    "ko": {
        "supported_header": ["Fess", "EOL 날짜", "상태"],
        "eol_header": ["Fess", "EOL 날짜"],
        "release": "🟢 최신 (권장)",
        "supported": "🟢 지원 중",
        "nearing": "🟡 지원 종료 임박",
    },
}

VERSION_RE = re.compile(r"^(\d+\.\d+|9\.x)$")


class ConfigError(Exception):
    pass


def version_key(version: str) -> tuple:
    return tuple(99 if part == "x" else int(part) for part in version.split("."))


def load_versions(path: pathlib.Path = VERSIONS) -> dict:
    """Read versions.json and refuse anything self-contradictory.

    A table generated from a file that disagrees with itself would look just as
    authoritative as a correct one, so the disagreement stops here.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ConfigError(f"{path.name}: {exc}") from exc

    for name in ("release", "development"):
        value = data.get(name)
        if not isinstance(value, str) or not VERSION_RE.match(value):
            raise ConfigError(f"{name} is not a version: {value!r}")
    for name in ("supported", "eol", "nearing"):
        value = data.get(name)
        if not isinstance(value, list):
            raise ConfigError(f"{name} must be a list")
        for item in value:
            if not isinstance(item, str) or not VERSION_RE.match(item):
                raise ConfigError(f"{name} contains something that is not a version: {item!r}")

    supported, eol, nearing = set(data["supported"]), set(data["eol"]), set(data["nearing"])
    if supported & eol:
        raise ConfigError("listed as both supported and eol: " + ", ".join(sorted(supported & eol)))
    if not nearing <= supported:
        raise ConfigError("nearing must be a subset of supported: " + ", ".join(sorted(nearing - supported)))
    if data["release"] not in supported:
        raise ConfigError(f"release {data['release']} is not in supported")
    if data["release"] in nearing:
        raise ConfigError(f"release {data['release']} cannot also be nearing end of support")
    if data["development"] in eol:
        raise ConfigError(f"development {data['development']} is listed as eol")

    schedule = data.get("schedule")
    if not isinstance(schedule, list):
        raise ConfigError("schedule must be a list")
    seen = set()
    for entry in schedule:
        directory, date = entry.get("dir"), entry.get("eol")
        if not isinstance(directory, str) or not VERSION_RE.match(directory):
            raise ConfigError(f"schedule entry has no usable dir: {entry!r}")
        if directory in seen:
            raise ConfigError(f"schedule lists {directory} twice")
        seen.add(directory)
        if not isinstance(date, str) or not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
            raise ConfigError(f"schedule entry for {directory} has no usable eol date: {date!r}")

    missing = (supported | eol) - seen
    if missing:
        raise ConfigError("no schedule entry for: " + ", ".join(sorted(missing, key=version_key)))
    return data


def warnings_for(data: dict, today: datetime.date) -> list:
    """Report what the dates say that the lists do not."""
    notes = []
    dates = {e["dir"]: e["eol"] for e in data["schedule"]}
    for version in sorted(data["supported"], key=version_key):
        raw = dates[version]
        try:
            due = datetime.date.fromisoformat(raw)
        except ValueError:
            # 2018-02-30 exists in the published table today. Reporting it beats
            # guessing a correction, and beats crashing on data already shipped.
            notes.append(f"{version}: {raw} is not a real date")
            continue
        if due < today and version not in data["nearing"]:
            notes.append(f"{version}: end of life was {raw} but it is still listed as supported")
        elif due < today:
            notes.append(f"{version}: end of life was {raw}; move it to eol")
    for entry in data["schedule"]:
        try:
            datetime.date.fromisoformat(entry["eol"])
        except ValueError:
            if entry["dir"] not in data["supported"]:
                notes.append(f"{entry['dir']}: {entry['eol']} is not a real date")
    return notes


def render_rows(cells_per_row) -> list:
    lines = []
    for cells in cells_per_row:
        lines.append(f"   * - {cells[0]}")
        lines.extend(f"     - {cell}" for cell in cells[1:])
    return lines


def render_supported(data: dict, labels: dict) -> list:
    rows = [labels["supported_header"]]
    dates = {e["dir"]: e for e in data["schedule"]}
    for version in sorted(data["supported"], key=version_key, reverse=True):
        entry = dates[version]
        if version == data["release"]:
            status = labels["release"]
        elif version in data["nearing"]:
            status = labels["nearing"]
        else:
            status = labels["supported"]
        rows.append([entry.get("label", version), entry["eol"], status])
    return [
        ".. tabularcolumns:: |p{3cm}|p{4cm}|p{3cm}|",
        ".. list-table::",
        "   :header-rows: 1",
        "   :widths: 25 35 40",
        "",
    ] + render_rows(rows)


def render_eol(data: dict, labels: dict) -> list:
    rows = [labels["eol_header"]]
    # Directories without a label are not versions readers ever saw named -- the
    # 9.x tree is one -- so they stay out of the table while remaining in the
    # lists the build reads.
    entries = [e for e in data["schedule"] if e["dir"] in set(data["eol"]) and e.get("label")]
    for entry in sorted(entries, key=lambda e: version_key(e["dir"]), reverse=True):
        rows.append([entry["label"], entry["eol"]])
    return [
        ".. tabularcolumns:: |p{4cm}|p{8cm}|",
        ".. list-table::",
        "",
    ] + render_rows(rows)


def replace_block(text: str, name: str, body: list, path: pathlib.Path) -> str:
    begin, end = BEGIN.format(name=name), END.format(name=name)
    if text.count(begin) != 1 or text.count(end) != 1:
        raise ConfigError(f"{path}: expected exactly one {name} marker pair")
    head, rest = text.split(begin, 1)
    _, tail = rest.split(end, 1)
    return head + begin + "\n" + "\n".join(body) + "\n" + end + tail


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="report what would change and change nothing")
    args = parser.parse_args(argv)

    try:
        data = load_versions()
    except ConfigError as exc:
        sys.stderr.write(f"ERROR: {exc}\n")
        return 2

    for note in warnings_for(data, datetime.date.today()):
        sys.stderr.write(f"[eol] {note}\n")

    stale = []
    for lang, labels in LABELS.items():
        path = ROOT / lang / "eol.rst"
        if not path.exists():
            sys.stderr.write(f"ERROR: {path} does not exist\n")
            return 2
        before = path.read_text(encoding="utf-8")
        try:
            after = replace_block(before, "supported-versions", render_supported(data, labels), path)
            after = replace_block(after, "eol-versions", render_eol(data, labels), path)
        except ConfigError as exc:
            sys.stderr.write(f"ERROR: {exc}\n")
            return 2
        if after == before:
            continue
        stale.append(lang)
        if not args.check:
            path.write_text(after, encoding="utf-8")

    if args.check:
        if stale:
            sys.stderr.write("ERROR: out of date with versions.json: " + ", ".join(stale) + "\n")
            sys.stderr.write("       Run: python3 tools/update_eol.py\n")
            return 1
        print("[eol] every translation matches versions.json")
        return 0

    print(f"[eol] updated {len(stale)} of {len(LABELS)} translations"
          + (": " + ", ".join(stale) if stale else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
