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

import hashlib
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

# The career is drawn as `git log --graph`: every role is a commit on main,
# growing upwards from the first job, and the M.Sc. is a branch that forks
# at the university internship and merges back in.

# (role, organisation, tag, years shown, start, end or None for current)
# Newest first. Dates are year + (month - 1) / 12 and only size the uptime bars.
CAREER = [
    ("IT Engineer", "Kontinental Establishment", "HEAD → main", "2023 — now", 2023.25, None),
    ("M.Sc. Data Science", "University of Göttingen", "merge", "2023 — 2025", 2023.0, 2025.92),
    ("IT Engineer", "TestSolutions GmbH", "contract", "2023 — 2024", 2023.08, 2024.92),
    ("DevSecOps Intern · Scientific Computing", "University of Göttingen", "internship", "2022 — 2023", 2022.83, 2023.08),
    ("IT Specialist", "Liberty Books", "", "2022", 2022.42, 2022.75),
    ("IT Specialist", "KTDMC", "", "2021 — 2022", 2021.75, 2022.33),
    ("IT Specialist", "Target Logistics International", "", "2020 — 2021", 2020.5, 2021.67),
    ("IT Engineer", "The Active Solutions", "init", "2019 — 2020", 2019.25, 2020.17),
]
MERGE_ROW, FORK_ROW = 1, 3


def timeline() -> None:
    w, row_h, top = 880, 46, 100
    n = len(CAREER)
    h = top + row_h * (n - 1) + 92
    trunk_x, lane_x, text_x = 58, 98, 196
    today = date.today()
    now = today.year + (today.month - 1) / 12
    longest = max((e or now) - s for *_, s, e in CAREER)
    step = 0.17  # seconds between commits appearing, oldest first

    def y(i: int) -> int:
        return top + i * row_h

    def delay(i: int) -> float:
        return 0.25 + (n - 1 - i) * step

    y_first, y_last = y(0), y(n - 1)
    trunk_len = y_last - y_first
    trunk = f"M{trunk_x},{y_last} L{trunk_x},{y_first}"
    yf, ym = y(FORK_ROW), y(MERGE_ROW)
    branch = (
        f"M{trunk_x},{yf} C{trunk_x},{yf - 22} {lane_x},{yf - 16} {lane_x},{yf - 36} "
        f"L{lane_x},{ym + 36} C{lane_x},{ym + 16} {trunk_x},{ym + 22} {trunk_x},{ym}"
    )

    rows = []
    for i, (role, org, tag, years, s, e) in enumerate(CAREER):
        yc = y(i)
        d = delay(i)
        sha = hashlib.sha1(f"{role}{org}{s}".encode()).hexdigest()[:7]
        head, edu = i == 0, i == MERGE_ROW
        if head:
            node = (
                f'<circle cx="{trunk_x}" cy="{yc}" r="7" fill="none" stroke="{ACCENT}" stroke-width="1.5" opacity="0">'
                f'<animate attributeName="r" values="7;22" dur="2.2s" begin="{d + 0.4:.2f}s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0.9;0" dur="2.2s" begin="{d + 0.4:.2f}s" repeatCount="indefinite"/></circle>'
                f'<circle cx="{trunk_x}" cy="{yc}" r="7" fill="{ACCENT}" class="n" style="animation-delay:{d:.2f}s" filter="url(#glow)"/>'
            )
        elif edu:
            node = f'<circle cx="{trunk_x}" cy="{yc}" r="6" fill="{BG}" stroke="{TEXT}" stroke-width="2" class="n" style="animation-delay:{d:.2f}s"/>'
        else:
            node = f'<circle cx="{trunk_x}" cy="{yc}" r="5" fill="{BG}" stroke="{ACCENT}" stroke-width="2" class="n" style="animation-delay:{d:.2f}s"/>'

        chip = ""
        if tag:
            cw = len(tag) * 6.3 + 16
            cx0 = text_x + len(role) * 7.2 + 12
            if tag == "HEAD → main":
                chip = (f'<rect x="{cx0:.1f}" y="{yc - 17}" width="{cw:.1f}" height="17" rx="8.5" fill="{ACCENT}"/>'
                        f'<text x="{cx0 + cw / 2:.1f}" y="{yc - 5}" text-anchor="middle" class="chip" fill="{BG}" font-weight="700">{escape(tag)}</text>')
            else:
                col = ACCENT if tag == "internship" else MUTED
                chip = (f'<rect x="{cx0:.1f}" y="{yc - 17}" width="{cw:.1f}" height="17" rx="8.5" fill="none" stroke="{col}" stroke-opacity=".7"/>'
                        f'<text x="{cx0 + cw / 2:.1f}" y="{yc - 5}" text-anchor="middle" class="chip" fill="{col}">{escape(tag)}</text>')

        span = (e or now) - s
        bw = max(8.0, 120 * span / longest)
        bar_col = ACCENT if head else ("#484f58" if edu else "#6e7681")
        bar = (f'<rect x="{w - 150}" y="{yc + 7}" width="120" height="4" rx="2" fill="{PANEL}"/>'
               f'<rect x="{w - 30 - bw:.1f}" y="{yc + 7}" width="{bw:.1f}" height="4" rx="2" fill="{bar_col}" class="bar" style="animation-delay:{d + 0.2:.2f}s"/>')
        yrs_fill = f' fill="{ACCENT}"' if head else ""
        prefix = "degree · " if edu else "@ "
        rows.append(
            f'<g class="r" style="animation-delay:{d:.2f}s">'
            f'<text x="{trunk_x + 58}" y="{yc + 4}" class="sha">{sha}</text>'
            f'<text x="{text_x}" y="{yc - 4}" class="role">{escape(role)}</text>{chip}'
            f'<text x="{text_x}" y="{yc + 13}" class="org">{prefix}{escape(org)}</text>'
            f'<text x="{w - 30}" y="{yc - 3}" text-anchor="end" class="yrs"{yrs_fill}>{years}</text>'
            f"{bar}</g>{node}"
        )

    packet = delay(0) + 0.6
    fy = h - 30
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Career as a git log, newest first">
  <title>Career</title>
  <defs>
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{LINE}" opacity=".55"/></pattern>
    <radialGradient id="halo" cx="0.06" cy="0.14" r="0.6"><stop offset="0" stop-color="{ACCENT}" stop-opacity=".09"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>
    <linearGradient id="trunkfade" gradientUnits="userSpaceOnUse" x1="0" y1="{y_last}" x2="0" y2="{y_first}"><stop offset="0" stop-color="{ACCENT}" stop-opacity=".3"/><stop offset="1" stop-color="{ACCENT}"/></linearGradient>
    <filter id="glow" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="3.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <style>
    text {{ font-family: {SANS}; }}
    .sha, .chip, .yrs, .cmd, .meta, .foot, .lane {{ font-family: {MONO}; }}
    .cmd {{ font-size: 13px; fill: {TEXT}; }}
    .meta {{ font-size: 11px; fill: {MUTED}; letter-spacing: .4px; }}
    .sha {{ font-size: 11.5px; fill: {MUTED}; }}
    .role {{ font-size: 14px; font-weight: 600; fill: {TEXT}; }}
    .org {{ font-size: 12px; fill: {MUTED}; }}
    .chip {{ font-size: 10px; }}
    .yrs {{ font-size: 11.5px; fill: {TEXT}; }}
    .lane {{ font-size: 9.5px; fill: {MUTED}; letter-spacing: 1px; }}
    .foot {{ font-size: 11px; fill: {MUTED}; }}
    .r {{ animation: rin .55s ease-out both; }}
    .n {{ transform-box: fill-box; transform-origin: center; animation: pop .45s cubic-bezier(.3,1.7,.5,1) both; }}
    .bar {{ transform-box: fill-box; transform-origin: right; animation: grow .9s ease-out both; }}
    .trunk {{ stroke-dasharray: {trunk_len}; animation: draw {step * n + 0.3:.2f}s linear .2s both; }}
    .branch {{ stroke-dasharray: 5 5; animation: flow 1.2s linear infinite; }}
    .branchwrap {{ animation: fade .6s ease-out {delay(FORK_ROW) + 0.2:.2f}s both; }}
    .cur {{ animation: blink 1.05s steps(1) infinite; }}
    .live {{ animation: blink 1.6s ease-in-out infinite; }}
    @keyframes rin {{ from {{ opacity: 0; transform: translateX(-12px); }} }}
    @keyframes pop {{ from {{ transform: scale(0); }} }}
    @keyframes grow {{ from {{ transform: scaleX(0); }} }}
    @keyframes draw {{ from {{ stroke-dashoffset: {trunk_len}; }} to {{ stroke-dashoffset: 0; }} }}
    @keyframes flow {{ to {{ stroke-dashoffset: -10; }} }}
    @keyframes fade {{ from {{ opacity: 0; }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
  </style>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{BG}" stroke="{LINE}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="url(#dots)"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="url(#halo)"/>

  <text x="28" y="40" class="cmd"><tspan fill="{ACCENT}">~/career</tspan><tspan fill="{MUTED}"> $ </tspan>git log --graph --all</text>
  <rect x="{28 + 32 * 7.8 + 6:.0f}" y="29" width="8" height="14" fill="{ACCENT}" class="cur"/>
  <text x="{w - 30}" y="40" text-anchor="end" class="meta">branch <tspan fill="{ACCENT}">main</tspan> · 7 roles · 1 degree · since 2019</text>
  <line x1="28" y1="58" x2="{w - 28}" y2="58" stroke="{LINE}"/>
  <text x="{w - 30}" y="{top - 26}" text-anchor="end" class="lane">UPTIME</text>

  <path d="{trunk}" fill="none" stroke="url(#trunkfade)" stroke-width="2.5" stroke-linecap="round" class="trunk"/>
  <g class="branchwrap">
    <path d="{branch}" fill="none" stroke="{MUTED}" stroke-width="2" class="branch"/>
    <text transform="translate({lane_x + 14},{(yf + ym) / 2:.0f}) rotate(-90)" text-anchor="middle" class="lane">edu/msc</text>
  </g>
  {"".join(rows)}

  <circle r="4" fill="{ACCENT}" filter="url(#glow)" opacity="0">
    <animateMotion path="{trunk}" dur="2.8s" begin="{packet:.2f}s" repeatCount="indefinite" keyPoints="0;1" keyTimes="0;1" calcMode="spline" keySplines=".45 0 .55 1"/>
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.85;1" dur="2.8s" begin="{packet:.2f}s" repeatCount="indefinite"/>
  </circle>
  <circle r="3" fill="{TEXT}" opacity="0">
    <animateMotion path="{branch}" dur="2.8s" begin="{packet + 1.4:.2f}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;.9;.9;0" keyTimes="0;.1;.85;1" dur="2.8s" begin="{packet + 1.4:.2f}s" repeatCount="indefinite"/>
  </circle>

  <line x1="28" y1="{fy - 22}" x2="{w - 28}" y2="{fy - 22}" stroke="{LINE}" stroke-dasharray="3 5"/>
  <circle cx="34" cy="{fy - 4}" r="4" fill="{ACCENT}" class="live"/>
  <text x="46" y="{fy}" class="foot">continuously deployed since 2019</text>
  <text x="{w - 30}" y="{fy}" text-anchor="end" class="foot">next commit: <tspan fill="{ACCENT}">open to roles worldwide</tspan> ▸</text>
</svg>"""
    write("timeline.svg", svg)


if __name__ == "__main__":
    terminal()
    for project in PROJECTS:
        card(project)
    timeline()
