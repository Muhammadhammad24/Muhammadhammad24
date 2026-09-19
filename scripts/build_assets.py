"""Generate the SVG graphics used in the profile README.

Everything is drawn from the data below, so updating a role or a project
means editing one list and re-running:

    python scripts/build_assets.py

The palette is deliberately quiet: GitHub-dark neutrals and one accent,
the lime used on the portfolio.
SVGs use system fonts only, because GitHub serves them as images and blocks
external font loading.
"""

from __future__ import annotations

from datetime import date
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets"

BG = "#0d1117"
PANEL = "#161b22"
LINE = "#30363d"
TEXT = "#e6edf3"
MUTED = "#8b949e"
ACCENT = "#b1eb21"
BLUE = MUTED
BLUE_SOFT = TEXT
AMBER = ACCENT
GREEN = ACCENT

SANS = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'Cascadia Mono', Consolas, 'Liberation Mono', monospace"


def write(name: str, svg: str) -> None:
    (OUT / name).parent.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(svg.strip() + "\n", encoding="utf-8", newline="\n")
    print(f"wrote assets/{name}")


def gradient_defs(uid: str) -> str:
    """Flat frame paints: a hairline border and no glow."""
    return f"""
  <defs>
    <linearGradient id="{uid}-edge"><stop offset="0" stop-color="{LINE}"/></linearGradient>
    <linearGradient id="{uid}-glow"><stop offset="0" stop-color="{BG}" stop-opacity="0"/></linearGradient>
  </defs>"""


# --------------------------------------------------------------------------
# Terminal card
# --------------------------------------------------------------------------

TERMINAL = [
    ("cmd", "whoami"),
    ("out", "Muhammad Hammad · IT Infrastructure Engineer · Göttingen, Germany"),
    ("cmd", "cat focus.txt"),
    ("out", "Cloud infrastructure (Azure / AWS) · DevOps & automation"),
    ("out", "Network engineering · Systems administration · Security"),
    ("cmd", "cat principles.md"),
    ("out", "Automate the second time · No SSH, no long-lived keys · Every alarm has a runbook"),
    ("cmd", "ls ~/now"),
    ("now", "it-engineer@kontinental   msc-data-science@uni-goettingen   open-to-roles: worldwide"),
]


def terminal() -> None:
    width, line_h, top = 880, 24, 62
    height = top + line_h * len(TERMINAL) + 34
    rows = []
    for i, (kind, text) in enumerate(TERMINAL):
        y = top + i * line_h
        delay = 0.35 + i * 0.45
        if kind == "cmd":
            body = (
                f'<tspan fill="{ACCENT}">$ </tspan>'
                f'<tspan fill="{TEXT}">{escape(text)}</tspan>'
            )
        elif kind == "now":
            body = f'<tspan fill="{AMBER}">{escape(text)}</tspan>'
        else:
            body = f'<tspan fill="{MUTED}">{escape(text)}</tspan>'
        rows.append(
            f'<text class="l" style="animation-delay:{delay:.2f}s" x="28" y="{y}">{body}</text>'
        )
    cursor_y = top + line_h * len(TERMINAL)
    cursor_delay = 0.35 + len(TERMINAL) * 0.45
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="whoami: Muhammad Hammad, IT Infrastructure Engineer">
  <title>whoami</title>
  {gradient_defs("t")}
  <style>
    text {{ font-family: {MONO}; font-size: 14px; }}
    .l {{ opacity: 0; animation: in .35s ease-out forwards; }}
    .cur {{ opacity: 0; animation: in .1s linear {cursor_delay:.2f}s forwards, blink 1s steps(1) {cursor_delay:.2f}s infinite; }}
    @keyframes in {{ from {{ opacity: 0; transform: translateX(-6px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .l, .cur {{ animation: none; opacity: 1; }} }}
  </style>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="14" fill="{BG}" stroke="url(#t-edge)"/>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="14" fill="url(#t-glow)"/>
  <rect x="24" y="19" width="8" height="8" rx="1" fill="{ACCENT}"/>
  <text x="40" y="28" fill="{MUTED}" style="font-size:12px">~/muhammad-hammad</text>
  <text x="{width - 24}" y="28" text-anchor="end" fill="{MUTED}" style="font-size:12px">bash</text>
  <line x1="1" y1="44" x2="{width - 1}" y2="44" stroke="{LINE}"/>
  {"".join(rows)}
  <text class="cur" x="28" y="{cursor_y}"><tspan fill="{ACCENT}">$ </tspan><tspan fill="{TEXT}">▌</tspan></text>
</svg>"""
    write("terminal.svg", svg)


# --------------------------------------------------------------------------
# Project cards
# --------------------------------------------------------------------------

PROJECTS = [
    {
        "slug": "aws-terraform-platform",
        "kind": "PLATFORM · DEVSECOPS",
        "title": "aws-terraform-platform",
        "lines": [
            "Self-healing AWS in Terraform across two AZs.",
            "Keyless OIDC CI/CD, KMS, GuardDuty, CloudTrail.",
        ],
        "stack": ["Terraform", "AWS", "GitHub Actions", "Checkov"],
        "proof": "15 tests · 0 failed checks",
    },
    {
        "slug": "Infotech-Wizard",
        "kind": "AIOPS · RAG",
        "title": "Infotech-Wizard",
        "lines": [
            "Private GenAI helpdesk: retrieval over 3,531",
            "resolved tickets in 5 languages, local LLM.",
        ],
        "stack": ["FastAPI", "FAISS", "PyTorch", "React"],
        "proof": "tested API",
    },
    {
        "slug": "pfSense-Firewall-Lab",
        "kind": "NETWORK SECURITY",
        "title": "pfSense-Firewall-Lab",
        "lines": [
            "Firewall policy as code, rendered to pfSense XML",
            "and audited for risky rules before deployment.",
        ],
        "stack": ["pfSense", "Python", "OpenVPN", "CI"],
        "proof": "22 tests · 0 findings",
    },
    {
        "slug": "nova2labs",
        "kind": "FULL-STACK · CLOUD",
        "title": "nova2labs",
        "lines": [
            "AI and cloud engineering studio: server-rendered",
            "React, generative artwork, SMTP lead pipeline.",
        ],
        "stack": ["React 19", "TanStack Start", "SSR", "Vercel"],
        "proof": "live",
    },
    {
        "slug": "velqatechnologies",
        "kind": "WEB · EDGE",
        "title": "velqatechnologies",
        "lines": [
            "Company website for a BPO firm: 33 statically",
            "exported routes served from the edge.",
        ],
        "stack": ["Next.js", "TypeScript", "Tailwind"],
        "proof": "live · CI",
    },
    {
        "slug": "nnapprox",
        "kind": "AI RESEARCH",
        "title": "nnapprox",
        "lines": [
            "Deep ReLU network approximation: closed-form",
            "constructions against greedy growing axons.",
        ],
        "stack": ["PyTorch", "NumPy", "Python"],
        "proof": "33 tests",
    },
]


def chip_width(label: str) -> int:
    return int(len(label) * 7.1) + 20


def card(p: dict) -> None:
    w, h = 430, 176
    uid = p["slug"].lower()
    chips, x = [], 22
    for s in p["stack"]:
        cw = chip_width(s)
        chips.append(
            f'<rect x="{x}" y="128" width="{cw}" height="24" rx="4" fill="{PANEL}" stroke="{LINE}"/>'
            f'<text x="{x + cw / 2}" y="144" text-anchor="middle" class="chip">{escape(s)}</text>'
        )
        x += cw + 8
    desc = "".join(
        f'<text x="22" y="{82 + i * 20}" class="d">{escape(line)}</text>' for i, line in enumerate(p["lines"])
    )
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(p['title'])}">
  <title>{escape(p['title'])}</title>
  {gradient_defs(uid)}
  <style>
    text {{ font-family: {SANS}; }}
    .k {{ font-family: {MONO}; font-size: 10.5px; letter-spacing: 1.4px; fill: {MUTED}; }}
    .t {{ font-size: 20px; fill: {TEXT}; font-weight: 700; }}
    .d {{ font-size: 13px; fill: {MUTED}; }}
    .t {{ font-family: {MONO}; }}
    .chip {{ font-family: {MONO}; font-size: 11.5px; fill: {TEXT}; }}
    .p {{ font-family: {MONO}; font-size: 11px; fill: {ACCENT}; }}
  </style>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" fill="{BG}" stroke="{LINE}"/>
  <rect x="0.5" y="22" width="3" height="40" fill="{ACCENT}"/>
  <text x="22" y="32" class="k">{escape(p['kind'])}</text>
  <text x="{w - 22}" y="32" text-anchor="end" class="p">{escape(p['proof'])}</text>
  <text x="22" y="58" class="t">{escape(p['title'])}</text>
  {desc}
  {"".join(chips)}
</svg>"""
    write(f"projects/{p['slug']}.svg", svg)


# --------------------------------------------------------------------------
# Career timeline
# --------------------------------------------------------------------------

START, END = 2019.0, 2027.0

# (role, organisation, start, end or None for current, colour)
PAST = "#6e7681"
EDU = "#484f58"

# Newest first, as on LinkedIn. Dates are year + (month - 1) / 12.
TIMELINE = [
    ("DevSecOps · Scientific Computing", "University of Göttingen", 2024.25, 2024.67, PAST),
    ("IT Engineer", "Kontinental Establishment", 2023.25, None, ACCENT),
    ("IT Engineer · contract", "TestSolutions GmbH", 2023.08, 2024.92, PAST),
    ("M.Sc. Data Science", "University of Göttingen", 2023.0, 2025.92, EDU),
    ("IT Specialist", "Liberty Books", 2022.42, 2022.75, PAST),
    ("IT Specialist", "KTDMC", 2021.75, 2022.33, PAST),
    ("IT Specialist", "Target Logistics International", 2020.5, 2021.67, PAST),
    ("IT Engineer", "The Active Solutions", 2019.25, 2020.17, PAST),
]


def timeline() -> None:
    w, label_w, right = 880, 300, 28
    row_h, top = 30, 70
    h = top + row_h * len(TIMELINE) + 40
    axis0, axis1 = label_w, w - right
    today = date.today()
    now = today.year + (today.month - 1) / 12

    def x(year: float) -> float:
        return axis0 + (year - START) / (END - START) * (axis1 - axis0)

    grid = []
    for yr in range(int(START), int(END) + 1):
        xx = x(yr)
        grid.append(f'<line x1="{xx:.1f}" y1="{top - 16}" x2="{xx:.1f}" y2="{top + row_h * len(TIMELINE) - 8}" stroke="{LINE}"/>')
        if yr < END:
            grid.append(f'<text x="{xx + 3:.1f}" y="{top + row_h * len(TIMELINE) + 12}" class="yr">{str(yr)[2:]}</text>')
    rows = []
    for i, (role, org, s, e, colour) in enumerate(TIMELINE):
        y = top + i * row_h
        end = e if e is not None else now
        x0, x1 = x(s), x(end)
        delay = 0.15 + i * 0.12
        live = f'<circle cx="{x1:.1f}" cy="{y - 4}" r="4.5" fill="{colour}" class="pulse"/>' if e is None else ""
        rows.append(
            f'<g class="row" style="animation-delay:{delay:.2f}s">'
            f'<text x="28" y="{y}" class="lb">{escape(role)}</text>'
            f'<text x="28" y="{y + 13}" class="sb">{escape(org)}</text>'
            f'<rect x="{x0:.1f}" y="{y - 10}" width="{max(x1 - x0, 5):.1f}" height="12" rx="2" fill="{colour}"/>'
            f"{live}</g>"
        )
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Career timeline from 2019 to today">
  <title>Career timeline</title>
  {gradient_defs("tl")}
  <style>
    text {{ font-family: {SANS}; }}
    .h {{ font-family: {MONO}; font-size: 11px; letter-spacing: 1.6px; fill: {MUTED}; }}
    .yr {{ font-family: {MONO}; font-size: 10.5px; fill: {MUTED}; }}
    .lg {{ font-family: {MONO}; font-size: 10.5px; }}
    .lb {{ font-size: 12.5px; fill: {TEXT}; font-weight: 600; }}
    .sb {{ font-size: 11px; fill: {MUTED}; }}
    .row {{ opacity: 0; animation: in .45s ease-out forwards; }}
    .pulse {{ animation: pulse 1.6s ease-in-out infinite; }}
    @keyframes in {{ from {{ opacity: 0; transform: translateX(-8px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes pulse {{ 50% {{ opacity: .2; }} }}
    @media (prefers-reduced-motion: reduce) {{ .row, .pulse {{ animation: none; opacity: 1; }} }}
  </style>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{BG}" stroke="url(#tl-edge)"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="url(#tl-glow)"/>
  <text x="28" y="34" class="h">CAREER 2019 → TODAY</text>
  <text x="{w - right}" y="34" text-anchor="end" class="lg"><tspan fill="{ACCENT}">■ current</tspan><tspan fill="{PAST}">   ■ past roles</tspan><tspan fill="{EDU}">   ■ education</tspan></text>
  {"".join(grid)}
  {"".join(rows)}
</svg>"""
    write("timeline.svg", svg)


if __name__ == "__main__":
    terminal()
    for project in PROJECTS:
        card(project)
    timeline()
