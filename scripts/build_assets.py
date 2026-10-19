"""Generate the SVG graphics used in the profile README.

Everything is drawn from the data below, so updating a role or a project
means editing one list and re-running:

    python scripts/build_assets.py

The palette matches the portfolio exactly: graphite near-black surfaces and
one electric-blue accent.
SVGs use system fonts only, because GitHub serves them as images and blocks
external font loading.
"""

from __future__ import annotations

import hashlib
from datetime import date
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets"

BG = "#000000"
PANEL = "#0B0B0D"
LINE = "#4A4A55"
TEXT = "#F7F8FA"
MUTED = "#777982"
ACCENT = "#FFFFFF"
BLUE = MUTED
BLUE_SOFT = TEXT
AMBER = ACCENT
GREEN = ACCENT

SANS = "'IBM Plex Sans', 'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'IBM Plex Mono', ui-monospace, SFMono-Regular, 'Cascadia Mono', Consolas, monospace"


# A README SVG renders as an image, so it cannot fetch a webfont from
# anywhere: naming IBM Plex only works for readers who happen to have it
# installed, and everyone else silently gets a different typeface from the
# site. Inlining the woff2 as a data URI is the one way the two actually
# match, because a data URI is not an external fetch.
import base64
from functools import lru_cache

FONT_DIR = Path(__file__).resolve().parent / "fonts"
_FACES = [
    ("IBM Plex Sans", 400, "ibm-plex-sans-latin-400-subset.woff2"),
    ("IBM Plex Sans", 600, "ibm-plex-sans-latin-600-subset.woff2"),
    ("IBM Plex Mono", 400, "ibm-plex-mono-latin-400-subset.woff2"),
    ("IBM Plex Mono", 600, "ibm-plex-mono-latin-600-subset.woff2"),
]


@lru_cache(maxsize=8)
def font_faces(families: tuple) -> str:
    """@font-face rules for just the families this drawing uses."""
    out = []
    for family, weight, fname in _FACES:
        if family not in families:
            continue
        path = FONT_DIR / fname
        if not path.exists():
            continue
        b64 = base64.b64encode(path.read_bytes()).decode("ascii")
        out.append(
            f"@font-face{{font-family:'{family}';font-weight:{weight};font-style:normal;"
            f"font-display:block;src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
        )
    return "".join(out)



def write(name: str, svg: str) -> None:
    svg = svg.strip()
    used = tuple(f for f in ("IBM Plex Sans", "IBM Plex Mono") if f in svg)
    faces = font_faces(used)
    if faces and "<style>" in svg:
        svg = svg.replace("<style>", "<style>" + faces, 1)
    (OUT / name).parent.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(svg + "\n", encoding="utf-8", newline="\n")
    print(f"wrote assets/{name}")


# growing upwards from the first job, and the M.Sc. is a branch that forks
# at the university internship and merges back in.

# (role, organisation, tag, years shown, start, end or None for current)
# Newest first. Dates are year + (month - 1) / 12 and only size the uptime bars.
# Roles only, newest first; education is listed separately below so the
# employment sequence reads straight down without a degree interrupting it.
# (role, organisation, tag, years shown, start, end or None for current)
CAREER = [
    # (role, organisation, location, type, dates shown, start, end or None)
    ("IT Engineer", "Kontinental Establishment", "Germany / US · hybrid", "Full-time", "Jan 2025 — now", 2025.0, None),
    ("IT Engineer", "TestSolutions GmbH", "Frankfurt, Germany · hybrid", "Contract", "Feb 2023 — Dec 2024", 2023.08, 2024.92),
    ("DevOps Engineer", "University of Göttingen", "Göttingen, Germany", "Internship", "Apr 2024 — Sep 2024", 2024.25, 2024.75),
    ("IT Specialist", "Liberty Books", "Karachi, Pakistan", "Full-time", "Jun 2022 — Oct 2022", 2022.42, 2022.75),
    ("IT Specialist", "KTDMC", "Karachi, Pakistan", "Full-time", "Oct 2021 — May 2022", 2021.75, 2022.33),
    ("IT Specialist", "Target Logistics International", "Karachi, Pakistan", "Full-time", "Jul 2020 — Sep 2021", 2020.5, 2021.67),
    ("IT Engineer", "The Active Solutions", "Karachi, Pakistan", "Full-time", "Apr 2019 — Mar 2020", 2019.25, 2020.17),
]
CAREER.sort(key=lambda r: (r[6] is None, r[5]), reverse=True)

# (degree, institution, years)
EDUCATION = [
    ("M.Sc. Data Science & Computer Science", "University of Göttingen, Germany", "2023 — 2026"),
    ("B.Sc (Hons) Computational Mathematics", "University of Karachi, Pakistan", "2016 — 2018"),
]


def timeline() -> None:
    """Career drawn the way the portfolio draws it: a quiet rail, the year on
    the left, one dot per role. No git-log chrome, no glow."""
    w, row_h, top = 900, 62, 96
    n = len(CAREER)
    edu_h = 30 + len(EDUCATION) * 38
    h = top + row_h * (n - 1) + 70 + edu_h + 46
    rail_x, year_x, text_x = 112, 92, 140
    today = date.today()
    now = today.year + (today.month - 1) / 12
    longest = max((e or now) - s for *_, s, e in CAREER)
    step = 0.06

    def y(i: int) -> int:
        return top + i * row_h

    rows = []
    for i, (role, org, loc, kind, years, s, e) in enumerate(CAREER):
        yc = y(i)
        d = 0.15 + i * step
        head = i == 0

        node = (
            f'<circle cx="{rail_x}" cy="{yc}" r="4.5" fill="{ACCENT if head else BG}" '
            f'stroke="{ACCENT if head else LINE}" stroke-width="2"/>'
        )

        cx0 = text_x + len(role) * 7.4 + 14
        cw = len(kind) * 6.3 + 18
        chips = (
            f'<rect x="{cx0:.1f}" y="{yc - 17}" width="{cw:.1f}" height="18" rx="9" '
            f'fill="none" stroke="{ACCENT if head else LINE}"/>'
            f'<text x="{cx0 + cw / 2:.1f}" y="{yc - 4}" text-anchor="middle" class="chip" '
            f'fill="{ACCENT if head else MUTED}">{escape(kind)}</text>'
        )
        months = round(((e or now) - s) * 12)
        dur = f"{months // 12} yr {months % 12} mo" if months >= 12 else f"{months} mo"
        dur = dur.replace(" 0 mo", "")

        span = (e or now) - s

        rows.append(
            f'<g class="r">'
            f'<text x="{year_x}" y="{yc + 4}" text-anchor="end" class="yrs" '
            f'fill="{ACCENT if head else MUTED}">{years.split(" — ")[0]}</text>'
            f'<text x="{text_x}" y="{yc - 3}" class="role">{escape(role)}</text>{chips}'
            f'<text x="{text_x}" y="{yc + 14}" class="org">{escape(org)} · {escape(loc)}</text>'
            f'<text x="{w - 30}" y="{yc - 3}" text-anchor="end" class="yrs" '
            f'fill="{TEXT if head else MUTED}">{years}</text>'
            f'<text x="{w - 30}" y="{yc + 14}" text-anchor="end" class="org">{dur}</text>'
            f'</g>{node}'
        )

    edu_y = y(n - 1) + 62
    edu_rows = "".join(
        f'<text x="{text_x}" y="{edu_y + 20 + j * 38}" class="role" font-size="13.5">{escape(deg)}</text>'
        f'<text x="{text_x}" y="{edu_y + 37 + j * 38}" class="org">{escape(inst)}</text>'
        f'<text x="{w - 30}" y="{edu_y + 20 + j * 38}" text-anchor="end" class="yrs" fill="{MUTED}">{yrs}</text>'
        f'<circle cx="{rail_x}" cy="{edu_y + 16 + j * 38}" r="3.5" fill="{BG}" stroke="{LINE}" stroke-width="2"/>'
        for j, (deg, inst, yrs) in enumerate(EDUCATION)
    )
    fy = h - 30
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Career, newest first">
  <title>Career</title>
  <style>
    text {{ font-family: {SANS}; }}
    .chip, .yrs, .lbl, .foot {{ font-family: {MONO}; }}
    .lbl {{ font-size: 12px; fill: {ACCENT}; letter-spacing: 1.6px; }}
    .role {{ font-size: 14.5px; font-weight: 600; fill: {TEXT}; }}
    .org {{ font-size: 12px; fill: {MUTED}; }}
    .chip {{ font-size: 10px; }}
    .yrs {{ font-size: 11.5px; }}
    .foot {{ font-size: 11px; fill: {MUTED}; }}
  </style>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{PANEL}" stroke="{LINE}"/>


  <text x="30" y="44" class="lbl" font-size="11">INDUSTRY EXPERIENCE</text>
  <text x="{w - 30}" y="44" text-anchor="end" class="foot">{n} roles · since 2019 · open to roles worldwide</text>
  <line x1="30" y1="62" x2="{w - 30}" y2="62" stroke="{LINE}"/>

  <line x1="{rail_x}" y1="{y(0)}" x2="{rail_x}" y2="{y(n - 1)}" stroke="{LINE}" stroke-width="1"/>
  {"".join(rows)}

  <line x1="30" y1="{edu_y - 26}" x2="{w - 30}" y2="{edu_y - 26}" stroke="{LINE}"/>
  <text x="30" y="{edu_y - 6}" class="lbl" font-size="11">EDUCATION</text>
  {edu_rows}

  <line x1="30" y1="{fy - 20}" x2="{w - 30}" y2="{fy - 20}" stroke="{LINE}"/>
  <text x="30" y="{fy + 2}" class="foot">Karachi → Göttingen · 5,617 km</text>
  <text x="{w - 30}" y="{fy + 2}" text-anchor="end" class="foot">muhammadhammad.vercel.app</text>
</svg>"""

    write("career-record.svg", svg)


# --------------------------------------------------------------------------
# Toolbox
# --------------------------------------------------------------------------
# Brand logos are vendored in scripts/icons: Simple Icons (CC0) as "si-*.svg",
# Devicon (MIT) as "dev-*.svg", Microsoft's official Azure and Entra
# architecture icons as "ms-*.svg", and a few supplied as-is. Trademarks belong
# to their owners. The light build shows every logo exactly as published;
# the dark build swaps near-black marks for their light, dark-mode form.

ICONS = Path(__file__).resolve().parent / "icons"

# (category, [(label, icon)])
TOOLBOX = [
    ("Cloud & virtualisation", [
        ("Azure", "dev-azure-original"), ("AWS", "dev-amazonwebservices-original-wordmark"), ("Google Cloud", "dev-googlecloud-original"),
        ("VMware", "vmware"), ("Virtual Desktop", "ms-virtual-desktop"), ("Docker", "si-docker"),
        ("Kubernetes", "dev-kubernetes-original"), ("Terraform", "terraform"),
    ]),
    ("Operating systems", [
        ("Windows", "dev-windows11-original"), ("Linux", "dev-linux-original"), ("Ubuntu", "si-ubuntu"), ("Red Hat", "redhat"),
        ("CentOS", "dev-centos-original"), ("macOS", "dev-apple-original"), ("iOS", "si-ios"), ("Android", "si-android"),
    ]),
    ("Identity & endpoints", [
        ("Entra ID", "ms-entra-id"), ("Active Directory", "ms-active-directory"), ("Intune", "ms-intune"), ("Defender", "ms-defender"),
        ("Jamf Pro", "jamf"), ("Okta", "okta"), ("TeamViewer", "si-teamviewer"),
    ]),
    ("Network & security", [
        ("Cisco", "cisco"), ("Juniper", "si-junipernetworks"), ("Fortinet", "si-fortinet"), ("pfSense", "pfsense"),
        ("SonicWall", "si-sonicwall"), ("Palo Alto", "si-paloaltonetworks"), ("CrowdStrike", "crowdstrike"),
    ]),
    ("Automation & delivery", [
        ("PowerShell", "dev-powershell-original"), ("Python", "dev-python-original"), ("Bash", "bash"), ("Ansible", "si-ansible"),
        ("Chocolatey", "si-chocolatey"), ("YAML", "si-yaml"), ("GitHub Actions", "si-githubactions"), ("Git", "dev-git-original"),
    ]),
    ("Monitoring & backup", [
        ("Splunk", "si-splunk"), ("Datadog", "datadog"), ("New Relic", "si-newrelic"), ("Grafana", "dev-grafana-original"),
        ("Prometheus", "dev-prometheus-original"), ("Wireshark", "wireshark"), ("Veeam", "veeam"),
    ]),
    ("Service & collaboration", [
        ("ServiceNow", "servicenow"), ("Jira", "dev-jira-original"), ("Confluence", "confluence"), ("Zendesk", "si-zendesk"),
        ("Microsoft 365", "ms-365"), ("Google Workspace", "dev-google-original"), ("Slack", "dev-slack-original"), ("Zoom", "si-zoom"),
    ]),
]

# Simple Icons wordmarks sit small in their square; draw them larger.
WORDMARKS = {"vmware", "junipernetworks", "sonicwall", "splunk", "veeam", "zoom"}
WIDE = {"cisco", "crowdstrike", "okta"}  # supplied logos that are wider than tall
KEEP_COLOURS = {"dev-powershell-original", "bash"}  # already designed for dark backgrounds

# Official brand colours for the single-colour Simple Icons marks.
SI_COLOURS = {
    "vmware": "#607078", "ios": "#000000", "junipernetworks": "#84B135", "fortinet": "#EE3124", "sonicwall": "#000000", "githubactions": "#2088FF",
    "paloaltonetworks": "#F04E23", "wireshark": "#1679A7", "splunk": "#000000", "newrelic": "#1CE783", "veeam": "#00B336",
    "zendesk": "#03363D", "zoom": "#0B5CFF", "docker": "#1D63ED", "android": "#34A853", "chocolatey": "#80B5E3", "yaml": "#CB171E",
    "teamviewer": "#050A52", "ubuntu": "#E95420", "ansible": "#EE0000",
}


def _on_dark(hex_colour: str) -> str:
    """Near-black brand colours become light so they read on a dark background."""
    h = hex_colour.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return TEXT if max(r, g, b) < 0.35 else hex_colour


def _logo(icon: str, x: float, y: float, size: float, uid: str, dark: bool) -> str:
    """Inline one brand logo inside a size x size box at (x, y).

    Light mode draws every logo exactly as published. Dark mode swaps only
    near-black parts for their light, dark-mode form.
    """
    import re

    raw = (ICONS / f"{icon}.svg").read_text(encoding="utf-8")
    view = re.search(r'viewBox="([^"]+)"', raw)
    inner = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", raw, flags=re.S)
    inner = re.sub(r"<title>.*?</title>", "", inner, flags=re.S)
    # keep ids unique when several logos share one document
    inner = re.sub(r'id="([^"]+)"', lambda m: f'id="{uid}-{m.group(1)}"', inner)
    inner = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{uid}-{m.group(1)})", inner)
    inner = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{uid}-{m.group(1)}"', inner)
    colour = SI_COLOURS.get(icon[3:], "#000000") if icon.startswith("si-") else "#000000"
    if dark and icon not in KEEP_COLOURS:
        inner = re.sub(r"#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}", lambda m: _on_dark(m.group(0)), inner)
        colour = _on_dark(colour)
    vb = view.group(1) if view else "0 0 24 24"
    return f'<svg x="{x:.1f}" y="{y:.1f}" width="{size}" height="{size}" viewBox="{vb}" fill="{colour}">{inner}</svg>'


# Panel colours per GitHub theme; the logos themselves stay as published.
THEMES = {
    "dark": {"bg": BG, "line": LINE, "text": TEXT, "muted": MUTED, "accent": ACCENT, "prompt": ACCENT},
    "light": {"bg": "#ffffff", "line": "#d0d7de", "text": "#1f2328", "muted": "#59636e", "accent": ACCENT, "prompt": "#4d7c0f"},
}


def _wrap_chars(text: str, limit: int) -> list:
    """Greedy wrap on a character count, for the short labels under each logo."""
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = f"{cur} {wd}".strip()
        if not cur or len(trial) <= limit:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def toolbox() -> None:
    """Two builds of the same panel; the README picks one with prefers-color-scheme."""
    for mode, t in THEMES.items():
        dark = mode == "dark"
        w, top, row_h, label_w, step = 900, 72, 84, 196, 81
        h = top + row_h * len(TOOLBOX) + 10
        total = sum(len(items) for _, items in TOOLBOX)
        rows = []
        for r, (cat, items) in enumerate(TOOLBOX):
            y = top + r * row_h
            if r:
                rows.append(f'<line x1="26" y1="{y - 10}" x2="{w - 26}" y2="{y - 10}" stroke="{t["line"]}" stroke-dasharray="2 5"/>')
            rows.append(
                f'<g class="in">'
                f'<circle cx="32" cy="{y + 22}" r="3" fill="{t["accent"]}" class="led"/>'
                f'<text x="44" y="{y + 26}" class="cat">{escape(cat)}</text>'
                f'<text x="44" y="{y + 44}" class="cnt">{len(items):02d} tools</text></g>'
            )
            for c, (label, icon) in enumerate(items):
                cx = label_w + c * step + step / 2
                d = 0.2 + r * 0.08 + c * 0.04
                if icon == "servicenow":  # long wordmark
                    size = 72
                elif icon[3:] in WORDMARKS or icon in WIDE or icon.endswith("wordmark"):
                    size = 44
                else:
                    size = 32
                logo = _logo(icon, cx - size / 2, y + 20 - size / 2, size, f"{mode[0]}{r}{c}", dark)
                labels = "".join(
                    f'<text x="{cx:.1f}" y="{y + 50 + k * 11}" text-anchor="middle" class="lb">{escape(part)}</text>'
                    for k, part in enumerate(_wrap_chars(label, 12))
                )
                rows.append(f'<g class="logo">{logo}{labels}</g>')
        svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Toolbox">
  <title>Toolbox</title>
  <style>
    text {{ font-family: {SANS}; }}
    .cmd, .meta, .cnt, .lb {{ font-family: {MONO}; }}
    .cmd {{ font-size: 13px; fill: {t["text"]}; }}
    .meta {{ font-size: 11px; fill: {t["muted"]}; }}
    .cat {{ font-size: 13.5px; font-weight: 600; fill: {t["text"]}; }}
    .cnt {{ font-size: 10.5px; fill: {t["muted"]}; }}
    .lb {{ font-size: 9.5px; fill: {t["muted"]}; }}
  </style>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{t["bg"]}" stroke="{t["line"]}"/>
  <text x="{w - 26}" y="38" text-anchor="end" class="meta">{total} tools · {len(TOOLBOX)} domains · hands-on</text>
  <line x1="26" y1="54" x2="{w - 26}" y2="54" stroke="{t["line"]}"/>
  {"".join(rows)}
</svg>"""
        write(f"brands-{mode}.svg", svg)


timeline()
toolbox()


# ---------------------------------------------------------------------------
# Section headings
# ---------------------------------------------------------------------------
# GitHub renders markdown in its own typeface, so a `## Heading` is the one
# place the profile stops matching the site. Drawing them keeps every visible
# word in IBM Plex.

HEADINGS = [
    ("what-i-do", "What I do"),
    ("environment", "The environment I run"),
    ("toolbox", "Toolbox"),
    ("projects", "Projects"),
    ("career", "Career"),
    ("certifications", "Certifications"),
]


def build_headings() -> None:
    for slug, label in HEADINGS:
        w, h = 900, 50
        svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(label)}">
  <style>
    text {{ font-family: {SANS}; }}
    .h {{ font-size: 21px; font-weight: 600; fill: {TEXT}; letter-spacing: -0.4px; }}
  </style>
  <text x="0" y="30" class="h">{escape(label)}</text>
  <line x1="0" y1="43" x2="{w}" y2="43" stroke="{LINE}"/>
</svg>"""
        write(f"headings/{slug}.svg", svg)


build_headings()


# ---------------------------------------------------------------------------
# Prose blocks
# ---------------------------------------------------------------------------
# The last markdown left on the page was its running text, which GitHub sets
# in its own face. Drawing it puts every word in Plex. Blocks whose only link
# is a single destination are wrapped in an <a> in the README, so nothing that
# was clickable stops being clickable.

W_PROSE = 900


# Text is measured, not estimated. Every guess at an average character
# advance was wrong in the same direction -- Plex Sans actually runs near
# 0.445 em, not the 0.515 assumed here for months -- so lines broke early
# and each block stopped well short of the column it sat in. These are the
# same woff2 subsets embedded in the SVGs, so the width computed here is
# the width the browser draws.
from fontTools.ttLib import TTFont


@lru_cache(maxsize=4)
def _metrics(family: str, weight: int):
    fname = next(
        (n for fam, w, n in _FACES if fam == family and w == weight), None
    )
    font = TTFont(FONT_DIR / fname)
    return font["head"].unitsPerEm, font["hmtx"].metrics, font.getBestCmap()


def text_width(text: str, size: float, weight: int = 400, mono: bool = False) -> float:
    """Advance width of `text` in px, from the real font tables."""
    family = "IBM Plex Mono" if mono else "IBM Plex Sans"
    upm, hmtx, cmap = _metrics(family, 600 if weight >= 600 else 400)
    total = 0
    for ch in text:
        glyph = cmap.get(ord(ch))
        total += hmtx[glyph][0] if glyph else int(upm * 0.5)
    return total / upm * size


def _wrap(text: str, size: float, width: int, weight: int = 400) -> list:
    """Greedy wrap on the measured advance width."""
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = f"{cur} {wd}".strip()
        if not cur or text_width(trial, size, weight) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def prose(slug: str, blocks: list, align: str = "middle", label: str = "") -> None:
    """blocks: [(text, size, weight, colour, gap_before)]"""
    inner = W_PROSE - 8
    lines, widest = [], 1.0
    for text, size, weight, colour, gap in blocks:
        chunk = _wrap(text, size, inner, weight)
        for ln in chunk:
            widest = max(widest, text_width(ln, size, weight))
        lines.append((chunk, size, weight, colour, gap))

    # Back on the shared 900 measure that every other asset uses: now that
    # the wrap is measured rather than guessed, the longest line genuinely
    # reaches it instead of stopping short.
    W = W_PROSE
    rows, y = [], 0
    for chunk, size, weight, colour, gap in lines:
        y += gap
        for ln in chunk:
            y += size * 1.55
            x = W / 2 if align == "middle" else 0
            rows.append(
                f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{align}" '
                f'font-size="{size}" font-weight="{weight}" fill="{colour}">{escape(ln)}</text>'
            )
    h = int(y + 10)
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" aria-label="{escape(label)}">
  <style>text {{ font-family: {SANS}; }}</style>
  {"".join(rows)}
</svg>"""
    write(f"prose/{slug}.svg", svg)


def build_prose() -> None:
    prose(
        "title",
        [
            ("Muhammad Hammad · IT Infrastructure Engineer", 25, 600, TEXT, 4),
            ("Cloud infrastructure (Azure / AWS) · DevOps & automation · Network engineering · Systems administration", 14, 400, TEXT, 14),
            ("Germany", 12, 400, MUTED, 6),
        ],
        label="Muhammad Hammad, IT Infrastructure Engineer. Cloud infrastructure (Azure / AWS), DevOps and automation, network engineering, systems administration. Germany.",
    )
    prose(
        "about",
        [
            ('IT Infrastructure Engineer with 7 years of experience bridging traditional system administration and cloud native approaches. I manage 500+ endpoints across Azure, and AWS, with a strong foundation in Windows and Linux server administration, enterprise networking, and GDPR aligned Zero Trust security.', 14.5, 400, TEXT, 0),
            ("I build infrastructure that runs quietly in the background, scales without drama, stays secure, and rarely needs anyone to step in. If your systems feel messy, manual, or held together by too many late night fixes, that is the kind of problem I like solving. Bring me the chaos, I will hand back something clean and self reliant. Reach out anytime, let's build something together.", 14.5, 400, TEXT, 16),
        ],
        align="start",
        label="IT Infrastructure Engineer with 7 years of experience bridging traditional system administration and cloud native approaches. I manage 500+ endpoints across Azure, and AWS, with a strong foundation in Windows and Linux server administration, enterprise networking, and GDPR aligned Zero Trust security. I build infrastructure that runs quietly in the background, scales without drama, stays secure, and rarely needs anyone to step in. If your systems feel messy, manual, or held together by too many late night fixes, that is the kind of problem I like solving. Bring me the chaos, I will hand back something clean and self reliant. Reach out anytime, let's build something together.",
    )
    prose(
        "ci-note",
        [
            ("Every public repository is tested in CI, and each README states what exists and what is on the roadmap. More work at muhammadhammad.vercel.app", 13.5, 400, MUTED, 0),
        ],
        align="start",
        label="Every public repository is tested in CI, and each README states what exists and what is on the roadmap. More work at muhammadhammad.vercel.app",
    )
    prose(
        "footer",
        [
            ("Open to IT infrastructure, cloud and DevOps roles worldwide, remote or on-site, and happy to relocate.", 15, 600, TEXT, 4),
            ("English (C1) · German (B1) · muhammad24997@gmail.com", 12.5, 400, MUTED, 8),
        ],
        label="Open to IT infrastructure, cloud and DevOps roles worldwide, remote or on-site, and happy to relocate. English C1, German B1, muhammad24997@gmail.com",
    )


build_prose()


# ---------------------------------------------------------------------------
# A day on the job
# ---------------------------------------------------------------------------
# The same drawing the portfolio opens with: not the estate, but the person
# running it — the order the work actually happens in, from the first twenty
# minutes of the morning to the note left for tomorrow. Down the left runs the
# half of the job that never stops while any of it is going on.
#
# A box is a thing that happens, a solid line is the day moving forward, a
# dashed line is something running on its own, a dotted frame is a boundary.

# (name, tools, more tools, what the step produced)
DAY = [
    ("Monitoring & alerts", "SRE", "Grafana · Datadog · Splunk",
     "overnight alerts · backup jobs · disk headroom", "all green"),
    ("Service desk", "IT SUPPORT", "Jira SM · ServiceNow · Slack routing",
     "L1–L3 triage · P1–P4 · 40% less manual triage", "sorted by impact"),
    ("Change management", "DEVOPS", "Git · GitHub Actions · Terraform · CI/CD",
     "ITIL change window · tested, staged, rollback first", "shipped safely"),
    ("Automation & IaC", "AUTOMATION", "PowerShell · Python · Ansible · Terraform",
     "onboarding · provisioning · patching, as code", "25 h/week returned"),
    ("Identity & access", "SECURITY", "Entra ID · Active Directory · Okta",
     "RBAC · MFA · GDPR and ISO 27001 controls", "least privilege"),
    ("Incident response", "ON-CALL", "Defender · CrowdStrike · Veeam",
     "isolate · revoke · IDS/IPS · restore to RTO", "contained first"),
    ("Endpoint management", "ENDPOINTS", "Intune · Jamf Pro · Autopilot · MDM",
     "180+ macOS, Windows and iOS · setup 75% faster", "fleet in line"),
]

# One mark per block, on the same 24-unit grid the portfolio draws them on:
# no fill, round caps, one stroke weight. Each draws what its block does
# rather than a company that happens to sell a product for it.
GLYPH = {
    "Monitoring & alerts": ["M2 12h4l2.5-6 3.5 12 2.5-6H22"],
    "Service desk": ["M3 5h18M3 10h18M3 15h11", "M18.5 14.3a3.2 3.2 0 1 0 0 6.4 3.2 3.2 0 0 0 0-6.4Z"],
    "Change management": [
        "M6 2.6a2.4 2.4 0 1 0 0 4.8 2.4 2.4 0 0 0 0-4.8Z",
        "M6 16.6a2.4 2.4 0 1 0 0 4.8 2.4 2.4 0 0 0 0-4.8Z",
        "M18 9.6a2.4 2.4 0 1 0 0 4.8 2.4 2.4 0 0 0 0-4.8Z",
        "M6 7.4v9.2M8.4 5h4.6a2.6 2.6 0 0 1 2.6 2.6v2",
    ],
    "Automation & IaC": ["M8.5 6 3.5 12l5 6M15.5 6l5 6-5 6"],
    "Identity & access": ["M12 3 20 6v6c0 4.4-3.3 7.9-8 9-4.7-1.1-8-4.6-8-9V6Z", "M9.3 12.2l1.9 1.9 3.5-3.8"],
    "Incident response": ["M12 3.5 22 20H2Z", "M12 10v4M12 17h.01"],
    "Endpoint management": [
        "M3.6 4.5h9.8a1.6 1.6 0 0 1 1.6 1.6v6.3a1.6 1.6 0 0 1-1.6 1.6H3.6A1.6 1.6 0 0 1 2 12.4V6.1a1.6 1.6 0 0 1 1.6-1.6Z",
        "M1 18h15",
        "M18.4 9h3.1a1.4 1.4 0 0 1 1.4 1.4v8.2a1.4 1.4 0 0 1-1.4 1.4h-3.1a1.4 1.4 0 0 1-1.4-1.4v-8.2A1.4 1.4 0 0 1 18.4 9Z",
    ],
}


def _glyph(name: str, x: float, y: float, size: float, colour: str) -> str:
    """The block's mark, scaled off its own 24-unit grid."""
    paths = "".join('<path d="%s"/>' % d for d in GLYPH[name])
    return ('<g transform="translate(%.1f %.1f) scale(%.4f)" fill="none" stroke="%s" '
            'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">%s</g>'
            % (x, y, size / 24.0, colour, paths))


ALWAYS = [
    ("Monitor", "Grafana · Datadog"),
    ("Network", "Fortinet · Cisco"),
    ("Systems", "Windows · Linux"),
    ("Cloud", "Azure · AWS"),
]


def day() -> None:
    w, pad = 900, 26
    nx, nw, nh, gap, top = 300, 574, 68, 12, 84
    cx, cw, ch = pad, 196, 54
    rows = []

    cspan = (len(DAY) * (nh + gap) - gap)
    cgap = (cspan - len(ALWAYS) * ch) / (len(ALWAYS) - 1)
    rows.append(
        '<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="none" stroke="%s" stroke-width="1" stroke-dasharray="4 4"/>'
        % (cx - 8, top - 38, cw + 16, cspan + 46, LINE)
    )
    rows.append('<text x="%d" y="%d" class="z">ALWAYS RUNNING</text>' % (cx, top - 24))
    rows.append('<text x="%d" y="%d" class="cs">underneath every hour</text>' % (cx, top - 11))

    for i, (name, sub) in enumerate(ALWAYS):
        y = top + i * (ch + cgap)
        rows.append('<rect x="%d" y="%.0f" width="%d" height="%d" rx="7" fill="%s" stroke="%s"/>' % (cx, y, cw, ch, PANEL, LINE))
        rows.append('<text x="%d" y="%.0f" class="cn">%s</text>' % (cx + 12, y + 23, escape(name)))
        rows.append('<text x="%d" y="%.0f" class="cs">%s</text>' % (cx + 12, y + 40, escape(sub)))
        # Dashed: it happens on its own, underneath the day.
        rows.append('<path d="M%d %.0f H%d" stroke="%s" stroke-width="1" stroke-dasharray="3 3" marker-end="url(#eh)"/>'
                    % (cx + cw, y + ch / 2, nx - 14, LINE))

    n = len(DAY)
    step, hold = 1.1, 0.9
    cycle = n * step + hold
    rail_x = nx - 26
    rows.append('<path d="M%d %d V%d" stroke="%s" stroke-width="1"/>'
                % (rail_x, top + nh // 2, top + (n - 1) * (nh + gap) + nh // 2, LINE))

    frames = []
    for i in range(n):
        a, b = i * step / cycle * 100, (i + 1) * step / cycle * 100
        frames.append(".s%d{animation:lit%d %.2fs step-end infinite;}" % (i, i, cycle))
        frames.append("@keyframes lit%d{0%%,%.3f%%{opacity:0}%.3f%%,%.3f%%{opacity:1}%.3f%%,100%%{opacity:0}}"
                      % (i, max(0.001, a - 0.001), a, b, min(99.999, b + 0.001)))
    dy = nh + gap
    stops = "".join("%.3f%%{transform:translateY(%dpx)}" % (i * step / cycle * 100, i * dy) for i in range(n))
    frames.append(".dot{animation:ride %.2fs step-end infinite;}" % cycle)
    frames.append("@keyframes ride{%s100%%{transform:translateY(%dpx)}}" % (stops, (n - 1) * dy))
    frames.append("@media (prefers-reduced-motion:reduce){.dot,%s{animation:none;opacity:0}}"
                  % ",".join(".s%d" % i for i in range(n)))
    anim_css = "".join(frames)

    for i, (name, tag, sub, sub2, does) in enumerate(DAY):
        y = top + i * (nh + gap)
        if i:
            # The incident is the one hour nobody schedules, so it arrives dashed.
            dash = ' stroke-dasharray="3 3"' if name == "Incident response" else ""
            rows.append('<path d="M%d %d V%.0f" stroke="%s" stroke-width="1"%s marker-end="url(#eh)"/>'
                        % (nx + nw // 2, int(y - gap), y - 3, LINE, dash))
        dash_box = ' stroke-dasharray="6 5"' if name == "Incident response" else ""
        rows.append('<rect x="%d" y="%.0f" width="%d" height="%d" rx="8" fill="%s" stroke="%s"%s/>' % (nx, y, nw, nh, PANEL, LINE, dash_box))
        rows.append('<rect x="%d" y="%.0f" width="3" height="%d" rx="1.5" fill="%s"/>' % (nx, y, nh, LINE))
        rows.append(_glyph(name, nx + 16, y + (nh - 24) / 2, 24, LINE))
        rows.append('<text x="%d" y="%.0f" class="rn">%s</text>' % (nx + 50, y + 25, escape(name)))
        rows.append('<text x="%d" y="%.0f" class="rs">%s</text>' % (nx + 50, y + 43, escape(sub)))
        rows.append('<text x="%d" y="%.0f" class="rs2">%s</text>' % (nx + 50, y + 58, escape(sub2)))
        # The hat worn for this block, the way the portfolio labels them.
        rows.append('<text x="%d" y="%.0f" text-anchor="end" class="ix">%s</text>' % (nx + nw - 14, y + 25, escape(tag)))
        # Lit overlay: the hour the day is in, and what it leaves behind. The
        # patch of panel under it hides the clock while the result is showing.
        rows.append('<g class="s%d"><rect x="%d" y="%.0f" width="%d" height="%d" rx="8" fill="none" stroke="%s"/>'
                    '<rect x="%d" y="%.0f" width="3" height="%d" rx="1.5" fill="%s"/>'
                    '%s'
                    '<rect x="%d" y="%.0f" width="%d" height="16" fill="%s"/>'
                    '<text x="%d" y="%.0f" text-anchor="end" class="dz">%s</text></g>'
                    % (i, nx, y, nw, nh, ACCENT, nx, y, nh, ACCENT,
                       _glyph(name, nx + 16, y + (nh - 24) / 2, 24, ACCENT),
                       nx + nw - 204, y + 13, 190, PANEL,
                       nx + nw - 14, y + 25, escape(does)))

    rows.append('<circle class="dot" cx="%d" cy="%d" r="3.4" fill="%s"/>' % (rail_x, top + nh // 2, ACCENT))
    h = top + cspan + 50
    alt = ("A day in production, in order: " + " then ".join(d[0] for d in DAY) +
           ". Underneath all of it, always running: " + ", ".join(a for a, _ in ALWAYS) + ".")
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="%s">' % (w, h, w, h, escape(alt))
        + '<defs><marker id="eh" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6 z" fill="%s"/></marker></defs>' % LINE
        + "<style>text{font-family:%s;}.z{font-size:9px;letter-spacing:1px;fill:%s;}.cn{font-size:12px;font-weight:600;fill:%s;}"
          ".cs{font-size:9.5px;fill:%s;}.rn{font-size:14px;font-weight:600;fill:%s;}.rs{font-size:10.5px;fill:%s;}"
          ".rs2{font-size:10.5px;fill:%s;}.ix{font-family:%s;font-size:10px;fill:%s;}.ft{font-size:10.5px;fill:%s;}"
          ".dz{font-size:10px;fill:%s;}%s</style>"
          % (SANS, MUTED, TEXT, MUTED, TEXT, MUTED, LINE, MONO, LINE, MUTED, TEXT, anim_css)
        + '<rect x="1" y="1" width="%d" height="%d" rx="14" fill="%s" stroke="%s"/>' % (w - 2, h - 2, BG, LINE)
        + '<text x="%d" y="34" text-anchor="end" class="ft">the order the work actually happens in</text>' % (w - pad)
        + "".join(rows)
        + '<text x="%d" y="%d" class="ft">Dashed lines run on their own; solid lines are the day moving forward. This is the job, step by step.</text>' % (pad, h - 16)
        + "</svg>"
    )
    write("environment.svg", svg)


day()


# ---------------------------------------------------------------------------
# Portfolio cards
# ---------------------------------------------------------------------------
# The site's own project and certificate cards, drawn to the same spec: one
# surface, a 14px radius, a hairline border, the figure in mono. Each is its
# own image so each can keep its link.

import re as _re

CARD_BG, CARD_LINE = "#0B0B0D", "rgba(255,255,255,0.17)"

PROJECT_CARDS = [
    ("aws-terraform-platform", "Platform · DevSecOps", "0 failed", "Checkov checks · 196 passed", "OPEN SOURCE"),
    ("Infotech-Wizard", "AIOps · RAG", "3,531 tickets", "indexed in 5 languages", "OPEN SOURCE"),
    ("pfSense-Firewall-Lab", "Network Security", "0 findings", "on the hardened rule set", "OPEN SOURCE"),
    ("nova2labs", "Full-Stack · Cloud", "29 pages", "server-rendered, SEO-complete", "LIVE"),
    ("velqatechnologies", "Web · Edge", "33 routes", "statically generated", "LIVE"),
    ("nnapprox", "AI Research", "33 tests", "verify the error bounds", "OPEN SOURCE"),
]

CERT_CARDS = [
    ("SysAdmin & IT Infrastructure", "Google", "Verified"),
    ("Full Stack Developer", "IBM", "Verified"),
    ("Computer Networks", "The Open University", "2023"),
    ("Successful IT Systems", "The Open University", "2023"),
    ("Cyber Security", "Udemy", "2022"),
    ("Information Security", "Udemy", "2022"),
    ("Database Development", "The Open University", "2023"),
    ("Computer Systems", "The Open University", "2023"),
]


def _pill(x, y, label, size=9):
    """The site's bordered capsule, measured off the label."""
    w = len(label) * size * 0.68 + 18
    return (
        '<rect x="%.0f" y="%.0f" width="%.0f" height="18" rx="9" fill="none" stroke="%s"/>'
        '<text x="%.0f" y="%.0f" text-anchor="middle" class="pl">%s</text>'
        % (x - w, y - 13, w, CARD_LINE, x - w / 2, y, escape(label))
    )


def _card(w, h, inner):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img">' % (w, h, w, h)
        + "<style>text{font-family:%s;}.ti{font-size:15px;font-weight:600;fill:%s;}.su{font-size:11.5px;fill:%s;}"
          ".mt{font-family:%s;font-size:14px;font-weight:600;fill:%s;}.ml{font-size:10.5px;fill:%s;}"
          ".pl{font-size:9px;fill:%s;letter-spacing:.5px;}.ar{font-size:13px;fill:%s;}</style>"
          % (SANS, TEXT, MUTED, MONO, TEXT, MUTED, MUTED, MUTED)
        + '<rect x="0.5" y="0.5" width="%d" height="%d" rx="14" fill="%s" stroke="%s"/>' % (w - 1, h - 1, CARD_BG, CARD_LINE)
        + inner + "</svg>"
    )


def portfolio_cards() -> None:
    w, h = 900, 112
    for title, cat, metric, label, badge in PROJECT_CARDS:
        inner = (
            '<text x="22" y="34" class="ti">%s</text>' % escape(title)
            + '<text x="%d" y="34" text-anchor="end" class="ar">\u2197</text>' % (w - 20)
            + '<text x="22" y="52" class="su">%s</text>' % escape(cat)
            + '<text x="22" y="92" class="mt">%s</text>' % escape(metric)
            + '<text x="%d" y="92" class="ml">%s</text>' % (22 + len(metric) * 8.6 + 10, escape(label))
            + _pill(22 + len(badge) * 6.1 + 18, 126, badge)
        )
        write("cards/%s.svg" % _re.sub(r"[^A-Za-z0-9-]", "-", title), _card(w, h, inner))

    ch = 80
    for title, issuer, badge in CERT_CARDS:
        inner = (
            '<text x="22" y="34" class="ti">%s</text>' % escape(title)
            + '<text x="22" y="58" class="su">%s</text>' % escape(issuer)
            + _pill(w - 20, 58, badge)
        )
        write("cards/cert-%s.svg" % _re.sub(r"[^A-Za-z0-9-]", "-", title), _card(w, ch, inner))


portfolio_cards()


# ---------------------------------------------------------------------------
# Contact badges
# ---------------------------------------------------------------------------
# These three were shields.io badges, which draw their logo at a fixed 14px.
# Gmail and the Vercel triangle already filled that, so there was no way to
# make the marks any larger without drawing the badges here instead — which
# is what the rest of this profile does anyway. Each is its own image so each
# keeps its own link.

BADGES = [
    ("linkedin", "LinkedIn"),
    ("portfolio", "Portfolio"),
    ("gmail", "Gmail"),
]
BADGE_H, MARK, PAD, GAP, TRACK = 34, 20, 15, 11, 1.4


def contact_badges() -> None:
    for slug, label in BADGES:
        art = (ICONS / ("_badge_%s.svg" % slug)).read_text(encoding="utf-8")
        vb = _re.search(r'viewBox="([^"]+)"', art).group(1)
        inner = _re.sub(r"^.*?<svg[^>]*>", "", art, flags=_re.S)
        inner = _re.sub(r"</svg>\s*$", "", inner, flags=_re.S).strip()

        word = label.upper()
        # Letter-spacing is not in the font metrics, so it is added by hand.
        tw = text_width(word, 12, 600) + TRACK * len(word)
        w = PAD + MARK + GAP + tw + PAD

        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %d" width="%.0f" height="%d" '
            'role="img" aria-label="%s">' % (w, BADGE_H, w, BADGE_H, label)
            + "<style>text{font-family:%s;}</style>" % SANS
            + '<rect x="0.5" y="0.5" width="%.0f" height="%d" rx="6" fill="%s" stroke="%s"/>'
            % (w - 1, BADGE_H - 1, CARD_BG, CARD_LINE)
            + '<svg x="%d" y="%.1f" width="%d" height="%d" viewBox="%s">%s</svg>'
            % (PAD, (BADGE_H - MARK) / 2, MARK, MARK, vb, inner)
            + '<text x="%.1f" y="%.1f" font-size="12" font-weight="600" letter-spacing="%.1f" fill="%s">%s</text>'
            % (PAD + MARK + GAP, BADGE_H / 2 + 4.2, TRACK, TEXT, escape(word))
            + "</svg>"
        )
        write("badges/%s.svg" % slug, svg)


contact_badges()


# ---------------------------------------------------------------------------
# Hero figure
# ---------------------------------------------------------------------------
# The same drawing the portfolio opens with, carried over whole: the estate as
# found at the top, pulled through one waist, and handed back in order along a
# backbone. The markup in scripts/icons/_hero_chaos.svg is the portfolio's own
# render; nothing here redraws it. What this adds is everything the figure got
# from the page it used to live on and cannot get inside a README: the fonts,
# the custom properties its fills refer to, and the keyframes its classes
# name. GitHub serves the file to an <img>, where declarative CSS animation
# runs and script does not — so the motion survives the trip and the figure is
# still correct and complete in its first frame, with animation off.

HERO_VARS = {
    "--bg": "#000000",
    "--bg-card": "#0B0B0D",
    "--text": "#F7F8FA",
    "--text-muted": "#777982",
    "--danger": "#E5484D",
    "--danger-line": "rgba(229,72,77,0.58)",
}

HERO_KEYFRAMES = (
    "@keyframes tangle-in{from{stroke-dashoffset:1;opacity:0}to{stroke-dashoffset:0;opacity:1}}"
    "@keyframes order-in{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}"
    "@keyframes seethe{0%,100%{transform:translate(0,0) rotate(0deg)}"
    "25%{transform:translate(0.7px,-0.5px) rotate(0.4deg)}"
    "50%{transform:translate(-0.4px,0.6px) rotate(-0.3deg)}"
    "75%{transform:translate(0.5px,0.4px) rotate(0.25deg)}}"
    "@keyframes seethe-hot{0%,100%{opacity:0.55}50%{opacity:1}}"
    "@keyframes queue-grow{0%,12%{opacity:0;transform:translateX(3px)}"
    "26%,88%{opacity:1;transform:none}100%{opacity:1;transform:none}}"
    "@keyframes method-step{0%{fill:rgba(255,255,255,0.3)}4%{fill:#ffffff}"
    "15%{fill:#ffffff}26%,100%{fill:rgba(255,255,255,0.3)}}"
    "@keyframes method-pass{0%{stroke-dashoffset:1}88%{stroke-dashoffset:0}"
    "100%{stroke-dashoffset:0;opacity:0}}"
    "@keyframes sys-drop{0%,100%{opacity:0}8%{opacity:0.85}24%{opacity:0}}"
    "@keyframes bus-glow{0%,100%{opacity:0.75}50%{opacity:1}}"
    "@keyframes loop-flow{to{stroke-dashoffset:-16}}"
)

HERO_RULES = (
    ".tangle-in{stroke-dasharray:1;animation:tangle-in 0.9s cubic-bezier(0.35,0,0.5,1) both}"
    ".order-in{stroke-dasharray:1;animation:order-in 0.45s cubic-bezier(0.2,0.9,0.3,1) both}"
    ".seethe{transform-box:fill-box;transform-origin:center;"
    "animation-name:tangle-in,seethe;"
    "animation-duration:0.9s,3.1s;"
    "animation-timing-function:cubic-bezier(0.35,0,0.5,1),ease-in-out;"
    "animation-iteration-count:1,infinite;animation-fill-mode:both,none}"
    ".seethe-hot{animation-name:tangle-in,seethe,seethe-hot;"
    "animation-duration:0.9s,3.1s,2.2s;"
    "animation-timing-function:cubic-bezier(0.35,0,0.5,1),ease-in-out,ease-in-out;"
    "animation-iteration-count:1,infinite,infinite;animation-fill-mode:both,none,none}"
    ".queue-bar{transform-box:fill-box;animation:queue-grow 5.6s ease-out infinite}"
    ".method-step{fill:rgba(255,255,255,0.3);animation:method-step 3.4s linear infinite}"
    ".method-pass{stroke-dasharray:1;animation:method-pass 3.4s linear infinite}"
    ".sys-drop{opacity:0;animation:sys-drop 3.4s ease-out infinite}"
    ".bus-glow{animation:bus-glow 3.4s ease-in-out infinite}"
    ".loop-flow{animation:loop-flow 1.1s linear infinite}"
)

# The figure is readable without motion, so honour the reader's setting.
HERO_STILL = (
    "@media (prefers-reduced-motion:reduce){"
    ".tangle-in,.order-in,.seethe,.seethe-hot,.queue-bar,.method-step,"
    ".method-pass,.sys-drop,.bus-glow,.loop-flow{animation:none}"
    ".tangle-in,.order-in,.method-pass{stroke-dashoffset:0}"
    ".sys-drop{opacity:0}.method-step{fill:rgba(255,255,255,0.72)}"
    ".queue-bar{opacity:1}.sys-sweep{display:none}}"
)

HERO_W, HERO_H = 470, 394


def hero_figure() -> None:
    art = (ICONS / "_hero_chaos.svg").read_text(encoding="utf-8")
    label = (ICONS / "_hero_chaos.txt").read_text(encoding="utf-8").strip()
    variables = "".join("%s:%s;" % kv for kv in HERO_VARS.items())
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
        'role="img" aria-label="%s">' % (HERO_W, HERO_H, HERO_W, HERO_H, escape(label))
        + "<style>"
        + font_faces(("IBM Plex Sans", "IBM Plex Mono"))
        + "svg{%s font-family:%s;}" % (variables, SANS)
        + ".mono{font-family:%s;}" % MONO
        + HERO_KEYFRAMES
        + HERO_RULES
        + HERO_STILL
        + "</style>"
        + '<rect width="%d" height="%d" fill="var(--bg)"/>' % (HERO_W, HERO_H)
        + art
        + "</svg>"
    )
    write("chaos-to-order.svg", svg)


hero_figure()
