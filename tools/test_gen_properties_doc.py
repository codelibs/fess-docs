"""Tests for tools/gen_properties_doc.py."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gen_properties_doc import (  # noqa: E402
    BEGIN,
    END,
    Entry,
    Group,
    Section,
    format_po,
    msgids,
    parse_po,
    parse_properties,
    render,
    replace_block,
    structural_key,
)
from gen_properties_doc import LANGUAGES  # noqa: E402

SECTIONS = [
    Section(
        "Core",
        [
            Group(
                "Search Engine",
                [
                    Entry("search_engine.type", "default", "The type."),
                    Entry("search_engine.password", "", "The password."),
                    Entry("jvm.crawler.options", "-Xmx512m\n-server\n", "JVM options."),
                ],
            )
        ],
    )
]

SAMPLE = """\
# ========================================================================================
#                                                                                    Core
#                                                                                   ======

#> Search Engine

# The type of search engine backend.
search_engine.type=default
# Username for authenticating.
# Leave empty to disable.
search_engine.username=

#> Job

# Options for the crawler JVM.
jvm.crawler.options=\\
-Djava.awt.headless=true\\n\\
-Xmx512m\\n\\

# ========================================================================================
#                                                                                     Web
#                                                                                    =====

# Not a heading, just commented-out config
#web.crawler.enabled=true

# The number of results.
web.page.size=20
"""


class ParseProperties(unittest.TestCase):
    def setUp(self):
        self.sections = parse_properties(SAMPLE)

    def test_finds_the_banner_sections(self):
        self.assertEqual([s.title for s in self.sections], ["Core", "Web"])

    def test_finds_the_group_headings(self):
        self.assertEqual([g.title for g in self.sections[0].groups], ["Search Engine", "Job"])

    def test_keys_before_any_group_heading_get_an_untitled_group(self):
        self.assertEqual([g.title for g in self.sections[1].groups], [""])

    def test_reads_key_and_default(self):
        entry = self.sections[0].groups[0].entries[0]
        self.assertEqual(entry.key, "search_engine.type")
        self.assertEqual(entry.default, "default")

    def test_joins_a_multi_line_description(self):
        entry = self.sections[0].groups[0].entries[1]
        self.assertEqual(entry.description, "Username for authenticating. Leave empty to disable.")

    def test_reads_an_empty_default(self):
        self.assertEqual(self.sections[0].groups[0].entries[1].default, "")

    def test_unescapes_a_continued_value_into_real_newlines(self):
        entry = self.sections[0].groups[1].entries[0]
        self.assertEqual(entry.default, "-Djava.awt.headless=true\n-Xmx512m\n")

    def test_ignores_commented_out_configuration(self):
        keys = [e.key for g in self.sections[1].groups for e in g.entries]
        self.assertEqual(keys, ["web.page.size"])

    def test_a_blank_line_breaks_the_description(self):
        entry = self.sections[1].groups[0].entries[0]
        self.assertEqual(entry.description, "The number of results.")

    def test_strips_whitespace_around_the_separator(self):
        sections = parse_properties("#> G\n\n# Desc.\ndomain.title = Fess\n")
        self.assertEqual(sections[0].groups[0].entries[0].default, "Fess")

    def test_keys_before_any_banner_land_in_an_untitled_section(self):
        sections = parse_properties("# Desc.\na.b=1\n")
        self.assertEqual([s.title for s in sections], [""])


class ParsePo(unittest.TestCase):
    def test_reads_a_simple_entry(self):
        self.assertEqual(parse_po('msgid "Hello"\nmsgstr "Bonjour"\n'), {"Hello": "Bonjour"})

    def test_skips_an_empty_translation(self):
        self.assertEqual(parse_po('msgid "Hello"\nmsgstr ""\n'), {})

    def test_skips_a_fuzzy_translation(self):
        text = '#, fuzzy\nmsgid "Hello"\nmsgstr "Bonjour"\n'
        self.assertEqual(parse_po(text), {})

    def test_fuzzy_does_not_leak_into_the_next_entry(self):
        text = '#, fuzzy\nmsgid "a"\nmsgstr "A"\n\nmsgid "b"\nmsgstr "B"\n'
        self.assertEqual(parse_po(text), {"b": "B"})

    def test_joins_adjacent_strings(self):
        text = 'msgid ""\n"one "\n"two"\nmsgstr ""\n"un "\n"deux"\n'
        self.assertEqual(parse_po(text), {"one two": "un deux"})

    def test_unescapes(self):
        text = 'msgid "a\\"b\\\\c\\nd"\nmsgstr "x\\ty"\n'
        self.assertEqual(parse_po(text), {'a"b\\c\nd': "x\ty"})

    def test_ignores_the_header_entry(self):
        text = 'msgid ""\nmsgstr "Content-Type: text/plain\\n"\n\nmsgid "Hello"\nmsgstr "Bonjour"\n'
        self.assertEqual(parse_po(text), {"Hello": "Bonjour"})

    def test_ignores_plain_comments(self):
        text = '# a translator note\nmsgid "Hello"\nmsgstr "Bonjour"\n'
        self.assertEqual(parse_po(text), {"Hello": "Bonjour"})

    def test_reads_an_empty_catalogue(self):
        self.assertEqual(parse_po(""), {})


class FormatPo(unittest.TestCase):
    def test_emits_every_msgid_in_order(self):
        out = format_po(["b", "a"], {})
        self.assertLess(out.index('msgid "b"'), out.index('msgid "a"'))

    def test_carries_over_an_existing_translation(self):
        self.assertIn('msgid "a"\nmsgstr "A"\n', format_po(["a"], {"a": "A"}))

    def test_leaves_an_untranslated_entry_empty(self):
        self.assertIn('msgid "a"\nmsgstr ""\n', format_po(["a"], {}))

    def test_drops_a_translation_whose_msgid_is_gone(self):
        self.assertNotIn("B", format_po(["a"], {"a": "A", "b": "B"}))

    def test_escapes_on_the_way_out(self):
        self.assertIn('msgid "a\\"b\\nc"', format_po(['a"b\nc'], {}))

    def test_round_trips(self):
        ids = ["plain", 'with "quotes"', "with\nnewline", "with\\backslash", "with\ttab"]
        wanted = {i: i.upper() for i in ids}
        self.assertEqual(parse_po(format_po(ids, wanted)), wanted)


class Render(unittest.TestCase):
    def test_writes_the_section_as_a_heading(self):
        self.assertIn("Core\n----", render(SECTIONS, {}))

    def test_writes_the_group_as_a_table_caption(self):
        self.assertIn(".. list-table:: Search Engine", render(SECTIONS, {}))

    def test_writes_the_three_columns(self):
        self.assertIn("  * - Name\n    - Description\n    - Default\n", render(SECTIONS, {}))

    def test_renders_a_default_as_an_inline_literal(self):
        self.assertIn("    - ``default``", render(SECTIONS, {}))

    def test_renders_an_empty_default_as_empty(self):
        self.assertIn("    - (empty)", render(SECTIONS, {}))

    def test_renders_a_multi_line_default_as_a_line_block(self):
        self.assertIn("    - | ``-Xmx512m``\n      | ``-server``", render(SECTIONS, {}))

    def test_translates_a_description(self):
        self.assertIn("    - Le type.", render(SECTIONS, {"The type.": "Le type."}))

    def test_translates_a_group_title(self):
        out = render(SECTIONS, {"Search Engine": "Moteur de recherche"})
        self.assertIn(".. list-table:: Moteur de recherche", out)

    def test_falls_back_to_english(self):
        self.assertIn("    - The type.", render(SECTIONS, {}))

    def test_never_translates_a_key_or_a_default(self):
        out = render(SECTIONS, {"search_engine.type": "x", "default": "y"})
        self.assertIn("  * - search_engine.type", out)
        self.assertIn("    - ``default``", out)

    def test_an_untitled_group_gets_no_caption(self):
        out = render([Section("Core", [Group("", [Entry("a.b", "1", "Desc.")])])], {})
        self.assertIn(".. list-table::\n", out)

    def test_escapes_rst_markup_in_a_description(self):
        sections = [Section("Core", [Group("G", [Entry("a.b", "1", "Access-Control-* and api.cors.*")])])]
        self.assertIn("    - Access-Control-\\* and api.cors.\\*", render(sections, {}))

    def test_leaves_no_trailing_whitespace_for_a_missing_description(self):
        sections = [Section("Core", [Group("G", [Entry("a.b", "1", "")])])]
        out = render(sections, {})
        self.assertIn("\n    -\n", out)
        self.assertNotIn(" \n", out)

    def test_a_default_of_only_newlines_renders_as_empty(self):
        sections = [Section("Core", [Group("G", [Entry("a.b", "\n\n", "D.")])])]
        self.assertIn("    - (empty)", render(sections, {}))

    def test_says_it_is_generated(self):
        self.assertIn("DO NOT EDIT", render(SECTIONS, {}))

    def test_underline_matches_the_title_width(self):
        # check_headings.py rejects a section whose underline is a different length.
        out = render([Section("Rate Limiting", [Group("", [Entry("a.b", "1", "D.")])])], {})
        self.assertIn("Rate Limiting\n-------------\n", out)

    def test_a_translated_title_gets_an_underline_of_its_own_width(self):
        out = render(SECTIONS, {"Core": "コア"})
        self.assertIn("コア\n----\n", out)


class Msgids(unittest.TestCase):
    def test_collects_titles_and_descriptions_in_order(self):
        self.assertEqual(
            msgids(SECTIONS), ["Core", "Search Engine", "The type.", "The password.", "JVM options."]
        )

    def test_deduplicates(self):
        sections = [Section("Core", [Group("G", [Entry("a", "", "Same."), Entry("b", "", "Same.")])])]
        self.assertEqual(msgids(sections), ["Core", "G", "Same."])

    def test_skips_an_untitled_group(self):
        sections = [Section("Core", [Group("", [Entry("a", "", "D.")])])]
        self.assertEqual(msgids(sections), ["Core", "D."])


class ReplaceBlock(unittest.TestCase):
    def test_replaces_only_between_the_markers(self):
        page = "Title\n=====\n\nIntro.\n\n%s\nold\n%s\n\nTail.\n" % (BEGIN, END)
        out = replace_block(page, "new")
        self.assertIn("Intro.", out)
        self.assertIn("Tail.", out)
        self.assertIn("%s\nnew\n%s" % (BEGIN, END), out)
        self.assertNotIn("old", out)

    def test_rejects_a_page_without_markers(self):
        with self.assertRaises(ValueError):
            replace_block("no markers here\n", "new")

    def test_is_idempotent(self):
        page = "Intro.\n\n%s\nold\n%s\n" % (BEGIN, END)
        self.assertEqual(replace_block(page, "new"), replace_block(replace_block(page, "new"), "new"))


class Structure(unittest.TestCase):
    def test_ignores_translated_prose(self):
        en = render(SECTIONS, {})
        fr = render(SECTIONS, {"The type.": "Le type.", "Search Engine": "Moteur", "Core": "Coeur"})
        self.assertEqual(structural_key(en), structural_key(fr))

    def test_notices_a_changed_default(self):
        other = [Section("Core", [Group("Search Engine", [
            Entry("search_engine.type", "CHANGED", "The type."),
            Entry("search_engine.password", "", "The password."),
            Entry("jvm.crawler.options", "-Xmx512m\n-server\n", "JVM options."),
        ])])]
        self.assertNotEqual(structural_key(render(SECTIONS, {})), structural_key(render(other, {})))

    def test_notices_a_missing_key(self):
        other = [Section("Core", [Group("Search Engine", [
            Entry("search_engine.type", "default", "The type."),
        ])])]
        self.assertNotEqual(structural_key(render(SECTIONS, {})), structural_key(render(other, {})))

    def test_notices_a_reordered_key(self):
        other = [Section("Core", [Group("Search Engine", [
            Entry("search_engine.password", "", "The password."),
            Entry("search_engine.type", "default", "The type."),
            Entry("jvm.crawler.options", "-Xmx512m\n-server\n", "JVM options."),
        ])])]
        self.assertNotEqual(structural_key(render(SECTIONS, {})), structural_key(render(other, {})))

    def test_notices_a_split_into_two_tables(self):
        other = [Section("Core", [
            Group("A", [Entry("search_engine.type", "default", "The type.")]),
            Group("B", [
                Entry("search_engine.password", "", "The password."),
                Entry("jvm.crawler.options", "-Xmx512m\n-server\n", "JVM options."),
            ]),
        ])]
        self.assertNotEqual(structural_key(render(SECTIONS, {})), structural_key(render(other, {})))

    def test_keeps_the_multi_line_default(self):
        key = structural_key(render(SECTIONS, {}))
        self.assertIn("-server", repr(key))


class Languages(unittest.TestCase):
    def test_lists_the_seven_trees(self):
        self.assertEqual(LANGUAGES, ["ja", "en", "de", "fr", "es", "zh-cn", "ko"])


if __name__ == "__main__":
    unittest.main()
