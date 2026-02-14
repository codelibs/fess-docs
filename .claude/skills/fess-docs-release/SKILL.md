---
name: fess-docs-release
description: Automate Fess documentation updates across all languages (ja, en, de, es, fr, ko, zh-cn) for a new release. Updates documentation.rst, downloads.rst, index.rst, news.rst, and archives.rst for each language.
---

# Fess Documentation Release Skill

This skill automates documentation updates across all 7 languages when a new Fess version is released.

## Step 1: Collect Parameters

Ask the user for the following parameters:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `VERSION` | New Fess version | `15.5.0` |
| `RELEASE_DATE` | Release date (YYYY-MM-DD) | `2026-01-25` |
| `JAVA_VERSION` | Java version | `21` |
| `OPENSEARCH_VERSION` | OpenSearch version | `3.5.0` |

## Step 2: Derive Values

Calculate these automatically:

- `DOC_VERSION` = Major.Minor from VERSION (e.g., `15.5.0` -> `15.5`)
- `PREV_DOC_VERSION` = Read from `ja/documentation.rst` toctree entries (the version currently referenced, e.g., `15.4`)
- `OPENSEARCH_URL_SLUG` = OPENSEARCH_VERSION with dots replaced by hyphens (e.g., `3.5.0` -> `3-5-0`)
- Today's date = current date for EOL comparison

## Step 3: Target Languages

All 7 languages: `ja`, `en`, `de`, `es`, `fr`, `ko`, `zh-cn`

## Step 4: Update Files

For each language, update the following files in order.

### 4.1: `{lang}/documentation.rst` - Update version references

Replace all occurrences of `PREV_DOC_VERSION` with `DOC_VERSION` in the toctree entries.

**Pattern (all languages have the same structure):**
```rst
.. toctree::

   Label1 <PREV_DOC_VERSION/install/index>
   Label2 <PREV_DOC_VERSION/user/index>
   Label3 <PREV_DOC_VERSION/admin/index>
   API <PREV_DOC_VERSION/api/index>
   Label4 <PREV_DOC_VERSION/config/index>
```

Change `PREV_DOC_VERSION` -> `DOC_VERSION` in each line.

### 4.2: `{lang}/downloads.rst` - Add new version and handle EOL

#### 4.2a: Add new version to stable releases

Add the new version as the **first entry** in the stable releases list. The entry format is:

```
* `Fess VERSION <https://github.com/codelibs/fess/releases/tag/fess-VERSION>`_ (`Java JAVA_VERSION <https://adoptium.net/temurin/releases?version=JAVA_VERSION>`_, `OpenSearch OPENSEARCH_VERSION <https://opensearch.org/versions/opensearch-OPENSEARCH_URL_SLUG.html>`_)
```

Find the first `* \`Fess` line after the stable release section header and insert the new entry before it.

**Language-specific stable release section headers:**

| Language | Section Header |
|----------|---------------|
| ja | `安定版リリース` |
| en | `Stable Release` |
| de | `Stabile Releases` |
| es | `Versiones Estables` |
| fr | `Versions stables` |
| ko | `안정 버전 릴리스` |
| zh-cn | `稳定版发布` |

#### 4.2b: Move EOL versions to Past Releases section

1. Read `ja/eol.rst` and find entries in the "現在サポート中のバージョン" table where the EOL date has passed (EOL date < today's date AND the status contains `サポート終了`).
2. For each EOL version found:
   - Find the corresponding entry line in the stable releases section of downloads.rst (match by version pattern like `Fess 14.17.0`)
   - Remove that line from the stable releases section
   - Add it as the **first entry** in the "Past Releases (EOL)" section

**Language-specific Past Releases section headers:**

| Language | Section Header |
|----------|---------------|
| ja | `過去のリリース(EOL)` |
| en | `Past Releases (EOL)` |
| de | `Vergangene Releases (EOL)` |
| es | `Versiones Anteriores (EOL)` |
| fr | `Versions antérieures (EOL)` |
| ko | `과거 릴리스(EOL)` |
| zh-cn | `过去的发布(EOL)` |

### 4.3: `{lang}/index.rst` - Update download section and news

#### 4.3a: Update download version

Find the line with `:doc:\`Fess PREV_VERSION <downloads>\`` and update the version number to `VERSION`.

**Pattern:**
```rst
- :doc:`Fess VERSION <downloads>` (package description)
```

The package description text varies by language but the `:doc:` reference pattern is the same.

#### 4.3b: Add news entry and maintain 5 entries

Add a new news entry at the **top** of the news section. The news section is identified by the language-specific header followed by entries in this format:

```rst
RELEASE_DATE
    `NEWS_TEXT <https://github.com/codelibs/fess/releases/tag/fess-VERSION>`__
```

**Language-specific news section headers and news text:**

| Language | News Section Header | News Text Format |
|----------|-------------------|-----------------|
| ja | `ニュース` | `Fess {VERSION} リリース` |
| en | `News` | `Fess {VERSION} Released` |
| de | `Nachrichten` | `Fess {VERSION} Release` |
| es | `Noticias` | `Lanzamiento de Fess {VERSION}` |
| fr | `Actualités` | `Version Fess {VERSION}` |
| ko | `뉴스` | `Fess {VERSION} 릴리스` |
| zh-cn | `新闻` | `Fess {VERSION} 发布` |

After adding the new entry, ensure only **5 news entries** remain in index.rst. Remove the oldest (bottom) entry if there are more than 5. Each entry consists of 2 lines (date line + indented link line) plus a blank line separator.

### 4.4: `{lang}/news.rst` - Add news entry

Add the new news entry at the **top** of the news list in news.rst (after the section header underline). Use the same format as index.rst news entries:

```rst
RELEASE_DATE
    `NEWS_TEXT <https://github.com/codelibs/fess/releases/tag/fess-VERSION>`__
```

The news list in news.rst is the section immediately after the title/header. Insert the new entry as the first item (before the existing first date entry).

### 4.5: `{lang}/archives.rst` - Add previous version archive

Add a new archive section for `PREV_DOC_VERSION` at the **top** of the archives list (after the title/header). The format is:

```rst
PREV_DOC_VERSION
~~~~

.. toctree::

   PREV_DOC_VERSION/install/index
   PREV_DOC_VERSION/user/index
   PREV_DOC_VERSION/api/index
   PREV_DOC_VERSION/admin/index
   PREV_DOC_VERSION/config/index
   JavaDocs <https://fess.codelibs.org/PREV_DOC_VERSION/apidocs/index.html>
   XRef <https://fess.codelibs.org/PREV_DOC_VERSION/xref/index.html>
   I/F Doc <https://fess.codelibs.org/PREV_DOC_VERSION/lastadoc-fess.html>
```

**Important:** The tilde underline (`~~~~`) must be at least as long as the version string. For versions like `15.4`, use `~~~~`. For versions like `13.16`, use `~~~~~` (5 tildes).

**Skip this step** if the `PREV_DOC_VERSION` section already exists in the archives.rst file.

## Step 5: Verification

After all updates:

1. Run `git diff` to review all changes
2. Confirm the expected number of files were modified (up to 35 files: 7 languages x 5 file types)
3. Check each file for correct RST formatting (proper indentation, blank lines between entries)
4. Verify no duplicate entries were created

## Important Notes

- The `de` language may sometimes be ahead of other languages (check current state before updating)
- The `ja/archives.rst` has the most entries (back to version 2.0); other languages vary in depth
- Some languages (de, es, fr, zh-cn) may have fewer archive entries than ja/en/ko
- The news entry in `news.rst` does NOT remove old entries (unlike `index.rst` which maintains exactly 5)
- In `downloads.rst`, all languages share the same version entries and URLs; only section headers differ
- The OpenSearch URL format is: `https://opensearch.org/versions/opensearch-X-Y-Z.html` (hyphens, not dots)
- The Fess release URL format is: `https://github.com/codelibs/fess/releases/tag/fess-VERSION`
- The Java download URL format is: `https://adoptium.net/temurin/releases?version=JAVA_VERSION`
