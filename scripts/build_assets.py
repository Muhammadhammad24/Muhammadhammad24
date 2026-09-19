"""Generate the SVG graphics used in the profile README.

Everything is drawn from the data below, so updating a role or a project
means editing one list and re-running:

    python scripts/build_assets.py

The palette follows the banner: near-black, deep blue, and an amber accent.
SVGs use system fonts only, because GitHub serves them as images and blocks
external font loading.
"""

from __future__ import annotations

from datetime import date
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets"

BG = "#0a0d14"
PANEL = "#0f1522"
LINE = "#1d2a40"
TEXT = "#e6ebf5"
MUTED = "#8b97ad"
BLUE = "#3b82f6"
BLUE_SOFT = "#60a5fa"
AMBER = "#f0a04b"
GREEN = "#34d399"

SANS = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'Cascadia Mono', Consolas, 'Liberation Mono', monospace"


def write(name: str, svg: str) -> None:
    (OUT / name).parent.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(svg.strip() + "\n", encoding="utf-8", newline="\n")
    print(f"wrote assets/{name}")


def gradient_defs(uid: str) -> str:
    return f"""
  <defs>
    <linearGradient id="{uid}-edge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{BLUE}"/>
      <stop offset="1" stop-color="{AMBER}"/>
    </linearGradient>
    <radialGradient id="{uid}-glow" cx="0.85" cy="0" r="0.9">
      <stop offset="0" stop-color="{BLUE}" stop-opacity="0.22"/>
      <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
    </radialGradient>
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
    ("now", "it-engineer@kontinental   msc-data-science@uni-goettingen   aws-terraform-platform/"),
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
                f'<tspan fill="{GREEN}">hammad</tspan><tspan fill="{MUTED}">@</tspan>'
                f'<tspan fill="{BLUE_SOFT}">ops</tspan><tspan fill="{MUTED}"> ~ $ </tspan>'
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
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="14" fill="{BG}" stroke="url(#t-edge)" stroke-opacity=".55"/>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="14" fill="url(#t-glow)"/>
  <circle cx="26" cy="24" r="6" fill="#ff5f57"/><circle cx="46" cy="24" r="6" fill="#febc2e"/><circle cx="66" cy="24" r="6" fill="#28c840"/>
  <text x="{width / 2}" y="29" text-anchor="middle" fill="{MUTED}" style="font-size:12px">hammad@ops — zsh</text>
  <line x1="1" y1="44" x2="{width - 1}" y2="44" stroke="{LINE}"/>
  {"".join(rows)}
  <text class="cur" x="28" y="{cursor_y}"><tspan fill="{GREEN}">hammad</tspan><tspan fill="{MUTED}">@</tspan><tspan fill="{BLUE_SOFT}">ops</tspan><tspan fill="{MUTED}"> ~ $ </tspan><tspan fill="{TEXT}">▌</tspan></text>
</svg>"""
    write("terminal.svg", svg)


# --------------------------------------------------------------------------
# Project cards
# --------------------------------------------------------------------------

PROJECTS = [
    {
        "slug": "aws-terraform-platform",
        "kind": "INFRASTRUCTURE AS CODE",
        "title": "AWS Terraform Platform",
        "lines": [
            "HA across two AZs, self-healing Auto Scaling, OIDC",
            "CI/CD with no stored keys, KMS, GuardDuty, CloudTrail.",
        ],
        "stack": ["Terraform", "AWS", "GitHub Actions", "Checkov"],
        "proof": "15 tests · Checkov 0 failed",
    },
    {
        "slug": "Infotech-Wizard",
        "kind": "AIOPS · RAG",
        "title": "Infotech Wizard",
        "lines": [
            "Helpdesk assistant: multilingual retrieval over 3.5k",
            "resolved tickets, answers from a local LLM.",
        ],
        "stack": ["FastAPI", "FAISS", "PyTorch", "React"],
        "proof": "5 languages · tested API",
    },
    {
        "slug": "pfSense-Firewall-Lab",
        "kind": "NETWORK SECURITY",
        "title": "pfSense Firewall Lab",
        "lines": [
            "Firewall policy as code: TOML rendered to pfSense",
            "XML and audited for risky rules in CI.",
        ],
        "stack": ["pfSense", "Python", "OpenVPN", "CI"],
        "proof": "22 tests · 0 findings",
    },
    {
        "slug": "nnapprox",
        "kind": "RESEARCH · NUMERICS",
        "title": "nnapprox",
        "lines": [
            "Function approximation with ReLU networks:",
            "closed-form baselines vs. greedy growing axons.",
        ],
        "stack": ["PyTorch", "NumPy", "Nevergrad"],
        "proof": "33 tests · error bounds",
    },
    {
        "slug": "velqatechnologies",
        "kind": "PRODUCTION WEB",
        "title": "Velqa Technologies",
        "lines": [
            "Marketing site for a BPO company: 33 statically",
            "exported routes, SEO, deployed on Vercel.",
        ],
        "stack": ["Next.js", "TypeScript", "Tailwind"],
        "proof": "live · CI",
    },
    {
        "slug": "portfolio",
        "kind": "PERSONAL SITE",
        "title": "Portfolio",
        "lines": [
            "Animated specialisation diagrams, skills matrix,",
            "OG image and structured data.",
        ],
        "stack": ["Next.js 15", "React 19", "Framer Motion"],
        "proof": "live · CI",
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
            f'<rect x="{x}" y="128" width="{cw}" height="24" rx="12" fill="{PANEL}" stroke="{LINE}"/>'
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
    .k {{ font-size: 10.5px; letter-spacing: 1.6px; fill: {AMBER}; font-weight: 600; }}
    .t {{ font-size: 20px; fill: {TEXT}; font-weight: 700; }}
    .d {{ font-size: 13px; fill: {MUTED}; }}
    .chip {{ font-family: {MONO}; font-size: 11.5px; fill: {BLUE_SOFT}; }}
    .p {{ font-family: {MONO}; font-size: 11px; fill: {GREEN}; }}
  </style>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{BG}" stroke="url(#{uid}-edge)" stroke-opacity=".6"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="url(#{uid}-glow)"/>
  <text x="22" y="32" class="k">{escape(p['kind'])}</text>
  <text x="{w - 22}" y="32" text-anchor="end" class="p">● {escape(p['proof'])}</text>
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
TIMELINE = [
    ("IT Engineer", "The Active Solutions", 2019.25, 2020.2, BLUE),
    ("IT Specialist", "Target Logistics International", 2020.5, 2021.7, BLUE),
    ("IT Specialist", "KTDMC", 2021.75, 2022.4, BLUE),
    ("IT Specialist", "Liberty Books", 2022.42, 2022.8, BLUE),
    ("IT Engineer · contract", "TestSolutions GmbH", 2023.08, 2024.95, BLUE_SOFT),
    ("M.Sc. Data Science", "University of Göttingen", 2023.0, 2025.95, MUTED),
    ("IT Engineer", "Kontinental Establishment", 2023.25, None, AMBER),
    ("DevSecOps · Scientific Computing", "University of Göttingen", 2024.25, 2024.7, GREEN),
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
            f'<rect x="{x0:.1f}" y="{y - 10}" width="{max(x1 - x0, 5):.1f}" height="12" rx="6" fill="{colour}"/>'
            f"{live}</g>"
        )
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Career timeline from 2019 to today">
  <title>Career timeline</title>
  {gradient_defs("tl")}
  <style>
    text {{ font-family: {SANS}; }}
    .h {{ font-size: 11px; letter-spacing: 1.8px; fill: {AMBER}; font-weight: 600; }}
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
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{BG}" stroke="url(#tl-edge)" stroke-opacity=".5"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="url(#tl-glow)"/>
  <text x="28" y="34" class="h">CAREER · 2019 → TODAY</text>
  <text x="{w - right}" y="34" text-anchor="end" class="lg"><tspan fill="{AMBER}">● current</tspan><tspan fill="{BLUE_SOFT}">   ● industry</tspan><tspan fill="{GREEN}">   ● research</tspan><tspan fill="{MUTED}">   ● education</tspan></text>
  {"".join(grid)}
  {"".join(rows)}
</svg>"""
    write("timeline.svg", svg)


if __name__ == "__main__":
    terminal()
    for project in PROJECTS:
        card(project)
    timeline()
