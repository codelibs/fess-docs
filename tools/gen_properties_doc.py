#!/usr/bin/env python3
"""Regenerate <lang>/<version>/config/properties.rst from Fess's fess_config.properties.

The page lists every configuration property Fess reads, with its description and its
default. Kept by hand it rotted: it had drifted to 120 keys short, and it documented ten
keys that no longer exist, several of them under a misspelling. So the rows are
generated, and only the prose around them is written by a person.

What each file records:

  fess_config.properties    the keys, the defaults, the English descriptions, the
                            headings and the order. It lives in the fess repository and
                            is the source for all of it. Edit this.
  <lang>/.../properties.po  the translations of those descriptions and headings, per
                            language and per version. Edit these.
  <lang>/.../properties.rst the page. Everything between the GENERATED markers comes
                            from the two files above -- edit outside the markers only.

fess_config.properties is not copied into this repository, so `--check` cannot compare a
page against it; that comparison happens when someone runs the update script. What
`--check` does verify, offline, is that the seven pages still agree with each other and
with their catalogues, which is what catches a page edited by hand.

Usage:
    tools/update_properties_doc.sh [path-to-fess-checkout]   regenerate
    python3 tools/gen_properties_doc.py --check              report, change nothing
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import unicodedata
from collections import namedtuple

BEGIN = ".. GENERATED-BEGIN: properties -- from fess_config.properties via tools/update_properties_doc.sh"
END = ".. GENERATED-END: properties"
_DO_NOT_EDIT = (
    ".. DO NOT EDIT. Descriptions and headings come from fess_config.properties in the\n"
    ".. fess repository; translations come from properties.po beside this file.\n"
    ".. Regenerate with tools/update_properties_doc.sh."
)
_COLUMNS = ("Name", "Description", "Default")
_EMPTY_DEFAULT = "(empty)"

#: One configuration key: its name, its default, and the English prose describing it.
Entry = namedtuple("Entry", "key default description")
#: Keys under one ``#>`` heading. An untitled group renders without a caption.
Group = namedtuple("Group", "title entries")
#: Groups under one banner. An untitled section renders without a heading.
Section = namedtuple("Section", "title groups")

# A banner is three lines -- a rule, a right-aligned title, and an underline of "=".
# The underline is what identifies it; the title is the line above.
_BANNER_UNDERLINE = re.compile(r"^#\s+=+\s*$")
_KEY = re.compile(r"^([A-Za-z][A-Za-z0-9_.]*)\s*[=:]\s*(.*)$")
_GROUP_MARKER = "#>"

_PROPERTIES_ESCAPES = {"n": "\n", "t": "\t", "r": "\r", "f": "\f", "\\": "\\", ":": ":", "=": "="}


def _properties_unescape(value: str) -> str:
    out = []
    i = 0
    while i < len(value):
        c = value[i]
        if c != "\\" or i + 1 >= len(value):
            out.append(c)
            i += 1
            continue
        nxt = value[i + 1]
        if nxt == "u" and i + 5 < len(value):
            out.append(chr(int(value[i + 2:i + 6], 16)))
            i += 6
            continue
        out.append(_PROPERTIES_ESCAPES.get(nxt, nxt))
        i += 2
    return "".join(out)


def parse_properties(text: str) -> list[Section]:
    """Read fess_config.properties into the sections, groups and entries it already has.

    Three shapes carry the structure. A banner -- a rule, a right-aligned title and an
    "=" underline -- opens a section. A line starting with ``#>`` opens a group; the
    marker is what tells a heading apart from a commented-out configuration example,
    which otherwise has exactly the same shape. Every other comment line directly above a
    key is that key's description, and a blank line ends one.
    """
    lines = text.split("\n")
    sections: list[Section] = [Section("", [Group("", [])])]
    description: list[str] = []
    i = 0

    def group() -> Group:
        return sections[-1].groups[-1]

    while i < len(lines):
        line = lines[i]
        if _BANNER_UNDERLINE.match(line) and i > 0:
            # Empty sections and groups are dropped at the end, so the placeholder this
            # started with disappears unless the file put keys before its first banner.
            sections.append(Section(lines[i - 1].lstrip("#").strip(), [Group("", [])]))
            description = []
            i += 1
            continue
        if not line.strip():
            description = []
            i += 1
            continue
        if line.startswith(_GROUP_MARKER):
            sections[-1].groups.append(Group(line[len(_GROUP_MARKER):].strip(), []))
            description = []
            i += 1
            continue
        if line.startswith("#"):
            body = line.lstrip("#").strip()
            # Skip the decorative rules that frame a banner and the file header.
            if body and not set(body) <= set("_/= -"):
                description.append(body)
            i += 1
            continue
        match = _KEY.match(line)
        if not match:
            description = []
            i += 1
            continue
        raw = match.group(2)
        while raw.endswith("\\") and i + 1 < len(lines):
            i += 1
            raw = raw[:-1] + lines[i]
        group().entries.append(
            Entry(match.group(1), _properties_unescape(raw.strip()), " ".join(description))
        )
        description = []
        i += 1

    for section in sections:
        section.groups[:] = [g for g in section.groups if g.entries]
    return [s for s in sections if s.groups]

# Escapes shared by the .po reader and writer, longest first so that a backslash is
# handled before the sequences that start with one.
PO_ESCAPES = [("\\", "\\\\"), ('"', '\\"'), ("\n", "\\n"), ("\t", "\\t"), ("\r", "\\r")]


def _po_unescape(text: str) -> str:
    out = []
    i = 0
    while i < len(text):
        c = text[i]
        if c == "\\" and i + 1 < len(text):
            nxt = text[i + 1]
            out.append({"n": "\n", "t": "\t", "r": "\r", '"': '"', "\\": "\\"}.get(nxt, nxt))
            i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _po_escape(text: str) -> str:
    for raw, escaped in PO_ESCAPES:
        text = text.replace(raw, escaped)
    return text


def parse_po(text: str) -> dict[str, str]:
    """Read a .po catalogue into {msgid: msgstr}.

    Only entries with a translation are returned: an empty msgstr and a fuzzy entry both
    mean "no translation yet", and the caller renders the English. The header entry,
    whose msgid is empty, is dropped. Python's standard library reads compiled .mo files
    rather than .po, so this covers the subset gettext tools emit -- msgid/msgstr,
    adjacent string continuation, comment and flag lines.
    """
    catalog: dict[str, str] = {}
    msgid: list[str] = []
    msgstr: list[str] = []
    target: list[str] | None = None
    fuzzy = False
    # A flag line introduces the entry that follows it, so it is held here until the
    # msgid line arrives rather than applied to the entry being closed.
    pending_fuzzy = False

    def flush() -> None:
        nonlocal msgid, msgstr, target, fuzzy
        if target is not None:
            key = "".join(msgid)
            value = "".join(msgstr)
            if key and value and not fuzzy:
                catalog[key] = value
        msgid, msgstr, target, fuzzy = [], [], None, False

    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            flush()
            continue
        if stripped.startswith("#"):
            if stripped.startswith("#,") and "fuzzy" in stripped:
                pending_fuzzy = True
            continue
        if stripped.startswith("msgid "):
            flush()
            target = msgid
            fuzzy, pending_fuzzy = pending_fuzzy, False
            stripped = stripped[len("msgid "):]
        elif stripped.startswith("msgstr "):
            target = msgstr
            stripped = stripped[len("msgstr "):]
        if target is None:
            continue
        quoted = re.fullmatch(r'"(.*)"', stripped, re.DOTALL)
        if quoted:
            target.append(_po_unescape(quoted.group(1)))
    flush()
    return catalog


def format_po(msgids: list[str], existing: dict[str, str]) -> str:
    """Render a catalogue holding every msgid, carrying over the translations there are.

    A msgid that has gone from fess_config.properties is dropped rather than kept as a
    stale translation, and the order follows the document so a diff reads like the page.
    """
    out = [
        "# Translations for the generated configuration properties page.",
        "#",
        "# msgid is the English text from fess_config.properties. Leave msgstr empty to",
        "# render the English. Regenerate with tools/update_properties_doc.sh, which adds",
        "# new entries and keeps the translations already here.",
        'msgid ""',
        'msgstr ""',
        '"MIME-Version: 1.0\\n"',
        '"Content-Type: text/plain; charset=UTF-8\\n"',
        '"Content-Transfer-Encoding: 8bit\\n"',
        "",
    ]
    for msgid in msgids:
        out.append('msgid "%s"' % _po_escape(msgid))
        out.append('msgstr "%s"' % _po_escape(existing.get(msgid, "")))
        out.append("")
    return "\n".join(out)


def _display_width(text: str) -> int:
    """Columns the text occupies, so an underline matches a title in any language.

    docutils measures a section title in columns rather than characters, so a Japanese
    title underlined by character count is too short and the section is dropped.
    """
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in text)


def _literal(value: str) -> str:
    """Render a configuration value as RST inline literal markup.

    A default is machine text -- paths, flags, regular expressions -- so it is set as a
    literal both to read correctly and so that a character RST would otherwise interpret
    cannot break the table. A value carrying a backtick cannot go in inline literal
    markup at all, so it falls back to escaping the characters that mean something.
    """
    if "`" in value:
        return re.sub(r"([*|_`\\])", r"\\\1", value)
    return "``%s``" % value


def _prose(text: str) -> str:
    """Escape the characters RST reads as inline markup in a description.

    Descriptions are prose written in a properties file, so they carry things like
    ``Access-Control-*`` and ``api.cors.*``. Left alone those trip docutils' inline
    markup recognition and the build warns; escaped, they render exactly as written.
    """
    return re.sub(r"([*`|\\])", r"\\\1", text)


def _cell(value: str) -> list[str]:
    """The lines of a Default cell, indented for a list-table row."""
    lines = value.split("\n")
    while lines and not lines[-1]:
        lines.pop()
    if not lines:
        # Either genuinely unset, or a value that is nothing but newlines -- which must
        # not reach _literal, where the newlines would break out of the table cell.
        return ["    - " + _EMPTY_DEFAULT]
    if len(lines) == 1:
        return ["    - " + _literal(lines[0])]
    return ["    - | " + _literal(lines[0])] + ["      | " + _literal(line) for line in lines[1:]]


def msgids(sections: list[Section]) -> list[str]:
    """Every translatable string, in document order, without repeats.

    Section titles, group titles and descriptions are prose and are translated. Key names
    and defaults are not -- they are what the reader types into a configuration file.
    """
    seen: dict[str, None] = {}
    for section in sections:
        if section.title:
            seen.setdefault(section.title, None)
        for group in section.groups:
            if group.title:
                seen.setdefault(group.title, None)
            for entry in group.entries:
                if entry.description:
                    seen.setdefault(entry.description, None)
    return list(seen)


def render(sections: list[Section], catalog: dict[str, str]) -> str:
    """Build the generated block: a heading per section, a table per group."""

    def translate(text: str) -> str:
        return catalog.get(text) or text

    out = [_DO_NOT_EDIT]
    for section in sections:
        if section.title:
            title = translate(section.title)
            out += ["", title, "-" * _display_width(title)]
        for group in section.groups:
            caption = translate(group.title) if group.title else ""
            out += ["", (".. list-table:: %s" % caption) if caption else ".. list-table::"]
            out += ["  :header-rows: 1", ""]
            out += ["  * - %s" % _COLUMNS[0], "    - %s" % _COLUMNS[1], "    - %s" % _COLUMNS[2]]
            for entry in group.entries:
                out.append("  * - %s" % entry.key)
                # A key whose comment is missing yields an empty cell; emit it without a
                # trailing space so the page never carries trailing whitespace.
                out.append(("    - %s" % _prose(translate(entry.description))).rstrip())
                out += _cell(entry.default)
    return "\n".join(out)


def replace_block(page: str, body: str) -> str:
    """Swap what is between the markers, leaving the rest of the page alone."""
    pattern = re.compile("^%s$.*?^%s$" % (re.escape(BEGIN), re.escape(END)), re.M | re.S)
    if not pattern.search(page):
        raise ValueError("no GENERATED-BEGIN/END markers in the page")
    return pattern.sub(lambda _: "%s\n%s\n%s" % (BEGIN, body, END), page, count=1)


#: The seven documentation trees, in the order create_version.sh walks them.
LANGUAGES = ["ja", "en", "de", "fr", "es", "zh-cn", "ko"]
#: The language whose page is the reference the others are compared against.
REFERENCE = "en"

ROOT = pathlib.Path(__file__).resolve().parent.parent
VERSIONS = ROOT / "versions.json"


def _tables(block: str) -> list[tuple[str, list[list[list[str]]]]]:
    """Read a rendered block back as (caption, rows), each row a list of cell line-lists.

    Both `--check` comparisons work from this, so neither has to guess which column it is
    looking at from the shape of the text.
    """
    tables: list[tuple[str, list[list[list[str]]]]] = []
    rows: list[list[list[str]]] | None = None
    for line in block.split("\n"):
        if line.startswith(".. list-table::"):
            rows = []
            tables.append((line[len(".. list-table::"):].strip(), rows))
        elif rows is None:
            continue
        elif line.startswith("  * - "):
            rows.append([[line[6:]]])
        elif line.startswith("    - ") and rows:
            rows[-1].append([line[6:]])
        elif line.startswith("      ") and rows and rows[-1]:
            rows[-1][-1].append(line[6:])
    # The first row of every table is the column header, which is not data.
    return [(caption, rows[1:]) for caption, rows in tables]


def structural_key(block: str) -> list:
    """Reduce a rendered block to the parts that must be identical in every language.

    Names, defaults and the shape of the tables are the same everywhere; only headings
    and descriptions are translated. Comparing this rather than the text is what lets
    `--check` tell a translation apart from a page someone edited by hand.
    """
    return [
        [(row[0][0], tuple(row[2])) for row in rows if len(row) > 2]
        for _, rows in _tables(block)
    ]


def _page_block(page: str) -> str:
    match = re.search("^%s$(.*?)^%s$" % (re.escape(BEGIN), re.escape(END)), page, re.M | re.S)
    if not match:
        raise ValueError("no GENERATED-BEGIN/END markers in the page")
    return match.group(1)


def development_version() -> str:
    """The version whose tree is edited, as versions.json states it."""
    return json.loads(VERSIONS.read_text(encoding="utf-8"))["development"]


def _paths(lang: str, version: str) -> tuple[pathlib.Path, pathlib.Path]:
    config = ROOT / lang / version / "config"
    return config / "properties.rst", config / "properties.po"


def generate(properties_path: pathlib.Path, version: str) -> list[str]:
    """Rewrite every page and refresh every catalogue. Returns what changed."""
    sections = parse_properties(properties_path.read_text(encoding="utf-8"))
    ids = msgids(sections)
    changed = []
    for lang in LANGUAGES:
        rst_path, po_path = _paths(lang, version)
        catalog = parse_po(po_path.read_text(encoding="utf-8")) if po_path.exists() else {}
        # English is what fess_config.properties already holds, so the reference language
        # has nothing to translate and gets no catalogue.
        if lang != REFERENCE:
            po = format_po(ids, catalog)
            if not po_path.exists() or po_path.read_text(encoding="utf-8") != po:
                po_path.parent.mkdir(parents=True, exist_ok=True)
                po_path.write_text(po, encoding="utf-8")
                changed.append(str(po_path.relative_to(ROOT)))
        page = rst_path.read_text(encoding="utf-8")
        updated = replace_block(page, render(sections, catalog))
        if updated != page:
            rst_path.write_text(updated, encoding="utf-8")
            changed.append(str(rst_path.relative_to(ROOT)))
    return changed


def check(version: str) -> list[str]:
    """Validate the pages against each other and against their catalogues, offline."""
    problems = []
    blocks = {}
    for lang in LANGUAGES:
        rst_path, po_path = _paths(lang, version)
        if not rst_path.exists():
            problems.append("%s: missing" % rst_path.relative_to(ROOT))
            continue
        try:
            blocks[lang] = _page_block(rst_path.read_text(encoding="utf-8"))
        except ValueError as exc:
            problems.append("%s: %s" % (rst_path.relative_to(ROOT), exc))
    if REFERENCE not in blocks:
        return problems or ["%s has no reference page" % REFERENCE]

    reference = structural_key(blocks[REFERENCE])
    english = set(_strings(blocks[REFERENCE]))
    for lang, block in blocks.items():
        rst_path, po_path = _paths(lang, version)
        if structural_key(block) != reference:
            problems.append(
                "%s: keys, defaults or table layout differ from %s -- regenerate with "
                "tools/update_properties_doc.sh" % (rst_path.relative_to(ROOT), REFERENCE)
            )
            continue
        if lang == REFERENCE:
            continue
        translated = set(parse_po(po_path.read_text(encoding="utf-8")).values()) if po_path.exists() else set()
        for text in _strings(block):
            if text not in english and _prose(text) not in {_prose(t) for t in translated}:
                problems.append(
                    "%s: %r is neither the English text nor a translation in %s"
                    % (rst_path.relative_to(ROOT), text[:60], po_path.relative_to(ROOT))
                )
                break
    return problems


def _strings(block: str) -> list[str]:
    """Every translatable string a rendered block shows: table captions and descriptions.

    Read from the parsed table rather than matched by shape, so a description that
    happens to look like a default cannot be mistaken for one.
    """
    out = []
    for caption, rows in _tables(block):
        if caption:
            out.append(caption)
        for row in rows:
            if len(row) > 1 and row[1] and row[1][0]:
                out.append(row[1][0])
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--properties", type=pathlib.Path,
                        help="path to fess_config.properties in a fess checkout")
    parser.add_argument("--check", action="store_true",
                        help="report problems and change nothing")
    args = parser.parse_args(argv)
    version = development_version()

    if args.check:
        problems = check(version)
        for problem in problems:
            print(problem)
        if problems:
            print("%d problem(s) in the %s configuration properties pages" % (len(problems), version),
                  file=sys.stderr)
            return 1
        print("%s: the %d properties pages agree" % (version, len(LANGUAGES)))
        return 0

    if not args.properties:
        parser.error("--properties is required unless --check is given")
    changed = generate(args.properties, version)
    for path in changed:
        print("updated %s" % path)
    if not changed:
        print("no change")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
