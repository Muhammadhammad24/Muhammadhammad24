"""Measure each brand mark's ink, and write scripts/icons/_ink.json.

A logo's viewBox is the square it was published on, not the shape of what is
drawn inside it: Simple Icons sets a wordmark as a thin band across a 24x24
box. Fitting the viewBox therefore sizes the box, and the mark inside it comes
out at whatever height the lettering happens to be. So the panel fits the ink,
and the ink has to be measured by something that can lay the paths out.

Chromium can, through getBBox(), and it is already installed here. Run this
after adding or replacing an icon; the build reads the table, not the browser.
"""
from __future__ import annotations

import glob
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ICONS = Path(__file__).resolve().parent / "icons"
CHROME = next(iter(glob.glob("/opt/pw-browsers/chromium*/chrome-linux/chrome")), None)


def main() -> int:
    if not CHROME:
        print("chromium not found; leaving _ink.json as it is", file=sys.stderr)
        return 1
    marks = [p for p in sorted(ICONS.glob("*.svg")) if not p.name.startswith("_")]
    page = ["<body><div id=o></div>"]
    for p in marks:
        page.append('<div class=h style="position:absolute;visibility:hidden" '
                    'data-n="%s">%s</div>' % (p.stem, p.read_text(encoding="utf-8")))
    page.append("""<script>
const out = {};
document.querySelectorAll('.h').forEach(h => {
  const b = h.querySelector('svg').getBBox();
  out[h.dataset.n] = [b.x, b.y, b.width, b.height].map(v => +v.toFixed(2));
});
document.getElementById('o').textContent = JSON.stringify(out);
</script></body>""")

    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "measure.html"
        src.write_text("\n".join(page), encoding="utf-8")
        dom = subprocess.run(
            [CHROME, "--headless", "--no-sandbox", "--disable-gpu",
             "--virtual-time-budget=5000", "--dump-dom", src.as_uri()],
            capture_output=True, text=True, check=True).stdout

    found = re.search(r'<div id="o">(.*?)</div>', dom, re.S)
    if not found:
        print("chromium returned no measurements", file=sys.stderr)
        return 1
    table = json.loads(found.group(1))
    if len(table) != len(marks):
        print("measured %d of %d marks" % (len(table), len(marks)), file=sys.stderr)
        return 1
    with (ICONS / "_ink.json").open("w", encoding="utf-8") as f:
        json.dump(table, f, indent=1, sort_keys=True)
        f.write("\n")
    print("measured %d marks" % len(table))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
