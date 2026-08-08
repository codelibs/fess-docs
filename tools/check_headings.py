#!/usr/bin/env python3
"""Report reStructuredText section titles whose overline and underline differ.

docutils requires the overline and underline of an over+underline section
title to be the same length. When they differ it refuses to build the
section, and the next section silently becomes the document title.
"""
import re
import sys
from pathlib import Path

ADORNMENT = re.compile(r'^([=\-`:.\'"~^_*+#])\1{1,}\s*$')


def find_mismatches(path):
    lines = Path(path).read_text(encoding='utf-8').split('\n')
    out = []
    i = 0
    while i < len(lines) - 2:
        over, title, under = lines[i], lines[i + 1], lines[i + 2]
        # The middle line must not itself be an adornment line, or a run of
        # adornment lines (e.g. a horizontal rule followed by a real
        # heading) gets misread as a heading and the fast path skips past
        # the genuine heading that follows it.
        if (ADORNMENT.match(over) and title.strip()
                and not ADORNMENT.match(title) and ADORNMENT.match(under)):
            if over.rstrip() != under.rstrip():
                out.append((i + 1, len(over.rstrip()),
                            len(under.rstrip()), title.strip()))
            i += 3
            continue
        i += 1
    return out


def main(argv):
    targets = []
    for arg in argv or ['.']:
        p = Path(arg)
        targets.extend(sorted(p.rglob('*.rst')) if p.is_dir() else [p])
    bad = 0
    for path in targets:
        for line, over, under, title in find_mismatches(path):
            print('{}:{} over={} under={} title={!r}'.format(
                path, line, over, under, title))
            bad += 1
    if bad:
        print('{} mismatched section title(s)'.format(bad), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
