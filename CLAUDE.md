# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the documentation repository for Fess, an open-source full-text search server. The documentation is built using Sphinx and supports multiple languages and versions.

## Repository Structure

- `ja/`, `en/`, `de/`, `fr/`, `es/`, `zh-cn/`: Language-specific documentation directories
- Each language directory contains version subdirectories (e.g., `15.3/`, `15.2/`, `14.15/`)
- Within each version: `install/`, `admin/`, `user/`, `api/`, `config/` sections
- `conf/`: Shared Sphinx configuration files
  - `conf.py`: Main Sphinx configuration
  - `Makefile`: Build targets for Sphinx
  - `ext.py`, `ogtag.py`: Custom Sphinx extensions
- `libs/`: JAR files for HTML/JS/CSS minification (htmlcompressor, yuicompressor)
- `resources/`: Shared resources like images

## Build Commands

### Build HTML for all languages
```bash
bash ./build.sh
```

### Build HTML for a specific language
```bash
cd ja  # or en, de, fr, es, zh-cn
bash ./build_html.sh
```

### Build PDF documentation (Japanese example)
```bash
cd ja
bash ./build_pdf.sh
```

### Using Makefile directly
From within a version directory (e.g., `ja/15.3/install/`):
```bash
make SPHINXOPTS="-c ${CONFDIR}" BUILDDIR="${BUILDDIR}" SPHINX_LANG="${DOCLANG}" SPHINX_PROJECT="${PROJECT}" SPHINX_TITLE="${TITLE}" SPHINX_AUTHOR="${AUTHOR}" SPHINX_RELEASE="${RELEASE}" -f ${CONFDIR}/Makefile html
```

## Documentation Format

- All documentation files use reStructuredText (`.rst`) format
- Sphinx directives and roles are used throughout
- Images are referenced from `../resources/images/`
- Use `|Fess|` substitution for the Fess name with proper formatting

## Build Process Details

The build process:
1. Uses Sphinx to generate HTML from RST files
2. Applies the `sphinx_rtd_theme` (Read the Docs theme)
3. Post-processes HTML with htmlcompressor for minification
4. Optionally compresses JS/CSS with yuicompressor (currently commented out)
5. Output goes to `_build/html/` within each language directory

## Multi-language and Multi-version Architecture

- Each language maintains its own complete documentation tree
- Versions are independent subdirectories within each language
- Build scripts at the language level iterate through documentation types (install, user, admin, api) for PDF generation
- Environment variables control build parameters: `SPHINX_LANG`, `SPHINX_PROJECT`, `SPHINX_TITLE`, `SPHINX_AUTHOR`, `SPHINX_RELEASE`

## Common Documentation Sections

1. **install**: Installation guides (prerequisites, platform-specific installation, docker, running, upgrading, uninstalling, troubleshooting)
2. **admin**: Administrator guides (configuration management, crawling, security, system settings)
3. **user**: User guides (search syntax, advanced search features)
4. **api**: API documentation (search API, GSA API, etc.)
5. **config**: Configuration guides (crawler setup, search customization, security roles)

## Working with Translations

When updating documentation across languages:
- The Japanese (`ja/`) documentation is typically the source/primary version
- Other languages follow the same structure and file naming
- Version numbers should be consistent across languages
- Check recent git commits for translation patterns (see commit history showing French, Spanish, German translations)

## Important Notes

- The git status shows recent directory rename: `zh-CN/` → `zh-cn/` (lowercase)
- HTML builds include minification for production deployment
- PDF builds use Japanese LaTeX engine (`latexpdfja`) for Japanese docs, regular `latexpdf` for others
- Theme configuration in `conf.py` includes GitHub integration and custom navigation settings
