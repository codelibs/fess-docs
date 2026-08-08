import copy
import datetime
import json
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from update_eol import (  # noqa: E402
    ConfigError,
    LABELS,
    load_versions,
    render_eol,
    render_supported,
    replace_block,
    version_key,
    warnings_for,
)

GOOD = {
    "release": "15.7",
    "development": "15.8",
    "supported": ["14.19", "15.0", "15.7"],
    "nearing": ["14.19"],
    "eol": ["8.0", "9.x"],
    "schedule": [
        {"label": "15.7.x", "dir": "15.7", "eol": "2027-12-01"},
        {"label": "15.0.x", "dir": "15.0", "eol": "2026-12-01"},
        {"label": "14.19.x", "dir": "14.19", "eol": "2026-08-01"},
        {"label": "8.x", "dir": "8.0", "eol": "2014-08-23"},
        {"dir": "9.x", "eol": "2016-11-21"},
    ],
}


def written(data):
    handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(data, handle)
    handle.close()
    return pathlib.Path(handle.name)


class LoadTest(unittest.TestCase):
    def broken(self, **changes):
        data = copy.deepcopy(GOOD)
        data.update(changes)
        with self.assertRaises(ConfigError):
            load_versions(written(data))

    def test_a_valid_file_loads(self):
        self.assertEqual(load_versions(written(GOOD))["release"], "15.7")

    def test_supported_and_eol_cannot_overlap(self):
        self.broken(eol=["8.0", "9.x", "15.0"])

    def test_nearing_must_be_supported(self):
        self.broken(nearing=["13.8"])

    def test_release_must_be_supported(self):
        self.broken(release="16.0")

    def test_release_cannot_be_nearing_its_own_end(self):
        self.broken(nearing=["15.7"])

    def test_development_cannot_be_eol(self):
        self.broken(eol=["8.0", "9.x", "15.8"])

    def test_versions_must_look_like_versions(self):
        self.broken(eol=["8.0", "../../etc"])

    def test_schedule_cannot_list_a_version_twice(self):
        data = copy.deepcopy(GOOD)
        data["schedule"].append({"label": "8.x", "dir": "8.0", "eol": "2014-08-23"})
        with self.assertRaises(ConfigError):
            load_versions(written(data))

    def test_every_listed_version_needs_a_schedule_entry(self):
        # Without this the table would quietly omit a version that the build
        # still deletes, and the two would disagree with nothing to show it.
        data = copy.deepcopy(GOOD)
        data["schedule"] = [e for e in data["schedule"] if e["dir"] != "14.19"]
        with self.assertRaises(ConfigError):
            load_versions(written(data))

    def test_dates_must_be_dates(self):
        data = copy.deepcopy(GOOD)
        data["schedule"][0]["eol"] = "soon"
        with self.assertRaises(ConfigError):
            load_versions(written(data))

    def test_unreadable_file_is_an_error(self):
        with self.assertRaises(ConfigError):
            load_versions(pathlib.Path("/nonexistent/versions.json"))


class RenderTest(unittest.TestCase):
    def setUp(self):
        self.labels = LABELS["en"]

    def test_release_row_says_latest(self):
        rows = render_supported(GOOD, self.labels)
        self.assertIn("   * - 15.7.x", rows)
        self.assertIn("     - " + self.labels["release"], rows)

    def test_nearing_version_is_marked(self):
        rows = "\n".join(render_supported(GOOD, self.labels))
        self.assertIn("14.19.x", rows)
        self.assertIn(self.labels["nearing"], rows)

    def test_supported_versions_run_newest_first(self):
        rows = [r for r in render_supported(GOOD, self.labels) if r.startswith("   * - 1")]
        self.assertEqual(rows, ["   * - 15.7.x", "   * - 15.0.x", "   * - 14.19.x"])

    def test_eol_table_skips_directories_with_no_label(self):
        # 9.x is a directory the build knows about but not a version readers
        # were ever given a name for, so it has no row.
        rows = "\n".join(render_eol(GOOD, self.labels))
        self.assertIn("8.x", rows)
        self.assertNotIn("9.x", rows)

    def test_every_language_has_the_labels_it_needs(self):
        for lang, labels in LABELS.items():
            with self.subTest(lang=lang):
                self.assertEqual(len(labels["supported_header"]), 3)
                self.assertEqual(len(labels["eol_header"]), 2)
                for key in ("release", "supported", "nearing"):
                    self.assertTrue(labels[key].strip())


class ReplaceBlockTest(unittest.TestCase):
    TEXT = ("before\n"
            ".. GENERATED-BEGIN: supported-versions -- from versions.json via tools/update_eol.py\n"
            "old\n"
            ".. GENERATED-END: supported-versions\n"
            "after\n")

    def test_only_the_marked_block_changes(self):
        out = replace_block(self.TEXT, "supported-versions", ["new"], pathlib.Path("x"))
        self.assertIn("new", out)
        self.assertNotIn("old", out)
        self.assertTrue(out.startswith("before\n"))
        self.assertTrue(out.endswith("after\n"))

    def test_missing_markers_are_an_error(self):
        with self.assertRaises(ConfigError):
            replace_block("no markers here\n", "supported-versions", ["x"], pathlib.Path("x"))

    def test_duplicate_markers_are_an_error(self):
        with self.assertRaises(ConfigError):
            replace_block(self.TEXT + self.TEXT, "supported-versions", ["x"], pathlib.Path("x"))


class WarningTest(unittest.TestCase):
    def test_a_supported_version_past_its_date_is_reported(self):
        notes = warnings_for(GOOD, datetime.date(2026, 8, 8))
        self.assertTrue(any("14.19" in n for n in notes))

    def test_nothing_is_reported_while_the_dates_still_hold(self):
        self.assertEqual(warnings_for(GOOD, datetime.date(2026, 1, 1)), [])

    def test_an_impossible_date_is_reported_not_raised(self):
        data = copy.deepcopy(GOOD)
        data["schedule"][3]["eol"] = "2018-02-30"
        notes = warnings_for(data, datetime.date(2026, 8, 8))
        self.assertTrue(any("2018-02-30" in n for n in notes))


class VersionKeyTest(unittest.TestCase):
    def test_versions_sort_numerically_not_alphabetically(self):
        versions = ["13.9", "13.16", "9.0", "14.1"]
        self.assertEqual(sorted(versions, key=version_key),
                         ["9.0", "13.9", "13.16", "14.1"])


if __name__ == "__main__":
    unittest.main()
