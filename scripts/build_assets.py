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
        "flow": ["git push", "OIDC", "terraform", "AWS · 2 AZ"],
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
        "flow": ["ticket", "embed", "FAISS", "local LLM", "answer"],
        "stack": ["FastAPI", "FAISS", "PyTorch", "React"],
        "proof": "3,531 tickets · 5 languages",
    },
    {
        "slug": "pfSense-Firewall-Lab",
        "kind": "NETWORK SECURITY",
        "title": "pfSense-Firewall-Lab",
        "lines": [
            "Firewall policy as code, rendered to pfSense XML",
            "and audited for risky rules before deployment.",
        ],
        "flow": ["policy.toml", "render", "audit", "pfSense"],
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
        "flow": ["visitor", "SSR", "Vercel edge", "SMTP", "inbox"],
        "stack": ["React 19", "TanStack Start", "SSR", "Vercel"],
        "proof": "live · nova2labs.com",
    },
    {
        "slug": "velqatechnologies",
        "kind": "WEB · EDGE",
        "title": "velqatechnologies",
        "lines": [
            "Company website for a BPO firm: 33 statically",
            "exported routes served from the edge.",
        ],
        "flow": ["next build", "33 routes", "edge CDN", "visitor"],
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
        "flow": None,  # drawn as a curve and its ReLU approximation
        "stack": ["PyTorch", "NumPy", "Python"],
        "proof": "33 tests · O(n⁻²)",
    },
]


def chip_width(label: str) -> int:
    return int(len(label) * 7.1) + 20


def card_defs(uid: str) -> str:
    return f"""
  <defs>
    <pattern id="{uid}-dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{LINE}" opacity=".5"/></pattern>
    <radialGradient id="{uid}-halo" cx="0.95" cy="0" r="0.8"><stop offset="0" stop-color="{ACCENT}" stop-opacity=".08"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>
    <filter id="{uid}-glow" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="2.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>"""


def flow_diagram(uid: str, nodes: list[str], cy: int, x0: int, x1: int) -> str:
    """A pipeline of boxes with a packet travelling through them."""
    widths = [len(t) * 6.5 + 18 for t in nodes]
    gap = (x1 - x0 - sum(widths)) / (len(nodes) - 1)
    xs, x = [], float(x0)
    for wd in widths:
        xs.append(x)
        x += wd + gap
    first, last = xs[0] + widths[0] / 2, xs[-1] + widths[-1] / 2
    out = [f'<line x1="{first:.1f}" y1="{cy}" x2="{last:.1f}" y2="{cy}" stroke="{MUTED}" stroke-opacity=".55" stroke-width="1.5" class="wire"/>']
    out.append(
        f'<circle r="3.2" fill="{ACCENT}" filter="url(#{uid}-glow)" opacity="0">'
        f'<animateMotion path="M{first:.1f},{cy} L{last:.1f},{cy}" dur="3s" begin="1.2s" repeatCount="indefinite" calcMode="spline" keyPoints="0;1" keyTimes="0;1" keySplines=".4 0 .6 1"/>'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.08;.9;1" dur="3s" begin="1.2s" repeatCount="indefinite"/></circle>'
    )
    for i, (t, bx, wd) in enumerate(zip(nodes, xs, widths)):
        end = i == len(nodes) - 1
        stroke = ACCENT if end else LINE
        fill_t = ACCENT if end else TEXT
        out.append(
            f'<g class="node" style="animation-delay:{0.2 + i * 0.14:.2f}s">'
            f'<rect x="{bx:.1f}" y="{cy - 13}" width="{wd:.1f}" height="26" rx="6" fill="{BG}" stroke="{stroke}"/>'
            f'<text x="{bx + wd / 2:.1f}" y="{cy + 4}" text-anchor="middle" class="nd" fill="{fill_t}">{escape(t)}</text></g>'
        )
    return "".join(out)


def relu_diagram(uid: str, cy: int, x0: int, x1: int) -> str:
    """A smooth target function and the piecewise-linear ReLU net that approximates it."""
    import math

    top, bot = cy - 20, cy + 20

    def f(t: float) -> float:
        return 0.5 + 0.32 * math.sin(2 * math.pi * 1.15 * t + 0.4) + 0.12 * math.sin(2 * math.pi * 3 * t)

    def pt(t: float) -> tuple[float, float]:
        return x0 + t * (x1 - x0 - 70), bot - f(t) * (bot - top)

    smooth = " ".join(f"{'M' if i == 0 else 'L'}{pt(i / 80)[0]:.1f},{pt(i / 80)[1]:.1f}" for i in range(81))
    knots = [pt(i / 8) for i in range(9)]
    relu = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}" for i, (x, y) in enumerate(knots))
    dots = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{BG}" stroke="{ACCENT}" stroke-width="1.5" class="node" style="animation-delay:{0.9 + i * 0.08:.2f}s"/>'
        for i, (x, y) in enumerate(knots)
    )
    return (
        f'<path d="{smooth}" fill="none" stroke="{MUTED}" stroke-opacity=".6" stroke-width="1.5" stroke-dasharray="2 3"/>'
        f'<path d="{relu}" fill="none" stroke="{ACCENT}" stroke-width="2" pathLength="100" class="drawn" filter="url(#{uid}-glow)"/>'
        f"{dots}"
        f'<text x="{x1}" y="{cy - 6}" text-anchor="end" class="nd" fill="{MUTED}">f(x)</text>'
        f'<text x="{x1}" y="{cy + 12}" text-anchor="end" class="nd" fill="{ACCENT}">ReLU net</text>'
    )


def card(p: dict) -> None:
    w, h = 430, 236
    uid = p["slug"].lower()
    chips, x = [], 22
    for i, s in enumerate(p["stack"]):
        cw = chip_width(s)
        chips.append(
            f'<g class="chipg" style="animation-delay:{0.6 + i * 0.08:.2f}s">'
            f'<rect x="{x}" y="194" width="{cw}" height="24" rx="12" fill="{PANEL}" stroke="{LINE}"/>'
            f'<text x="{x + cw / 2}" y="210" text-anchor="middle" class="chip">{escape(s)}</text></g>'
        )
        x += cw + 8
    desc = "".join(
        f'<text x="22" y="{88 + i * 19}" class="d">{escape(line)}</text>' for i, line in enumerate(p["lines"])
    )
    band_y, cy = 124, 153
    diagram = flow_diagram(uid, p["flow"], cy, 34, w - 34) if p["flow"] else relu_diagram(uid, cy, 34, w - 34)
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(p['title'])}">
  <title>{escape(p['title'])}</title>
  {card_defs(uid)}
  <style>
    text {{ font-family: {SANS}; }}
    .k, .t, .chip, .p, .nd {{ font-family: {MONO}; }}
    .k {{ font-size: 10.5px; letter-spacing: 1.4px; fill: {MUTED}; }}
    .t {{ font-size: 20px; fill: {TEXT}; font-weight: 700; }}
    .d {{ font-size: 12.5px; fill: {MUTED}; }}
    .chip {{ font-size: 11px; fill: {TEXT}; }}
    .p {{ font-size: 11px; fill: {ACCENT}; }}
    .nd {{ font-size: 10.5px; }}
    .led {{ animation: led 1.8s ease-in-out infinite; }}
    .node, .chipg {{ animation: pop .45s cubic-bezier(.3,1.6,.5,1) both; transform-box: fill-box; transform-origin: center; }}
    .wire {{ stroke-dasharray: 4 5; animation: flow .9s linear infinite; }}
    .drawn {{ stroke-dasharray: 100; animation: draw 1.6s ease-out .3s both; }}
    @keyframes led {{ 50% {{ opacity: .25; }} }}
    @keyframes pop {{ from {{ opacity: 0; transform: scale(.6); }} }}
    @keyframes flow {{ to {{ stroke-dashoffset: -9; }} }}
    @keyframes draw {{ from {{ stroke-dashoffset: 100; }} to {{ stroke-dashoffset: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
  </style>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" fill="{BG}" stroke="{LINE}"/>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" fill="url(#{uid}-dots)"/>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" fill="url(#{uid}-halo)"/>
  <circle cx="26" cy="28" r="3.5" fill="{ACCENT}" class="led"/>
  <text x="38" y="32" class="k">{escape(p['kind'])}</text>
  <text x="{w - 22}" y="32" text-anchor="end" class="p">{escape(p['proof'])}</text>
  <text x="22" y="64" class="t">{escape(p['title'])}</text>
  {desc}
  <rect x="16" y="{band_y}" width="{w - 32}" height="58" rx="9" fill="{PANEL}" fill-opacity=".55" stroke="{LINE}" stroke-dasharray="2 4"/>
  {diagram}
  {"".join(chips)}
</svg>"""
    write(f"projects/{p['slug']}.svg", svg)


# --------------------------------------------------------------------------
# Impact panel
# --------------------------------------------------------------------------

IMPACT = [
    ("25 h/wk", ["onboarding, provisioning", "and patching automated"], "KONTINENTAL"),
    ("−75%", ["device setup time on", "180+ endpoints, 12 sites"], "KONTINENTAL"),
    ("4h→35m", ["ML infrastructure", "deploys through CI/CD"], "UNI GÖTTINGEN"),
    ("−85%", ["vulnerabilities, through", "automated scan gates"], "UNI GÖTTINGEN"),
    ("265+", ["government endpoints at", "100% patch compliance"], "KTDMC"),
]


def impact() -> None:
    w, top, th, gap = 880, 64, 126, 10
    h = top + th + 24
    tw = (w - 56 - gap * (len(IMPACT) - 1)) / len(IMPACT)
    tiles = []
    for i, (metric, lines, where) in enumerate(IMPACT):
        x = 28 + i * (tw + gap)
        d = 0.2 + i * 0.13
        body = "".join(
            f'<text x="{x + 14:.1f}" y="{top + 70 + j * 16}" class="lb">{escape(line)}</text>' for j, line in enumerate(lines)
        )
        tiles.append(
            f'<g class="tile" style="animation-delay:{d:.2f}s">'
            f'<rect x="{x:.1f}" y="{top}" width="{tw:.1f}" height="{th}" rx="10" fill="{PANEL}" fill-opacity=".7" stroke="{LINE}"/>'
            f'<rect x="{x + 14:.1f}" y="{top}" width="{tw - 28:.1f}" height="2" fill="{ACCENT}" class="bar" style="animation-delay:{d + 0.25:.2f}s"/>'
            f'<text x="{x + 14:.1f}" y="{top + 44}" class="m">{escape(metric)}</text>'
            f"{body}"
            f'<text x="{x + 14:.1f}" y="{top + th - 14}" class="wh">{escape(where)}</text></g>'
        )
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Selected impact">
  <title>Selected impact</title>
  <defs>
    <pattern id="i-dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{LINE}" opacity=".55"/></pattern>
    <radialGradient id="i-halo" cx="0.5" cy="0" r="0.7"><stop offset="0" stop-color="{ACCENT}" stop-opacity=".07"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>
  </defs>
  <style>
    text {{ font-family: {SANS}; }}
    .cmd, .m, .wh, .meta {{ font-family: {MONO}; }}
    .cmd {{ font-size: 13px; fill: {TEXT}; }}
    .meta {{ font-size: 11px; fill: {MUTED}; }}
    .m {{ font-size: 25px; font-weight: 700; fill: {ACCENT}; }}
    .lb {{ font-size: 11.5px; fill: {TEXT}; opacity: .85; }}
    .wh {{ font-size: 9.5px; letter-spacing: 1.3px; fill: {MUTED}; }}
    .tile {{ animation: up .55s ease-out both; }}
    .bar {{ transform-box: fill-box; transform-origin: left; animation: grow .8s ease-out both; }}
    .cur {{ animation: blink 1.05s steps(1) infinite; }}
    @keyframes up {{ from {{ opacity: 0; transform: translateY(10px); }} }}
    @keyframes grow {{ from {{ transform: scaleX(0); }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
  </style>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{BG}" stroke="{LINE}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="url(#i-dots)"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="url(#i-halo)"/>
  <text x="28" y="38" class="cmd"><tspan fill="{ACCENT}">~/impact</tspan><tspan fill="{MUTED}"> $ </tspan>cat outcomes.log</text>
  <rect x="{28 + 27 * 7.8 + 6:.0f}" y="27" width="8" height="14" fill="{ACCENT}" class="cur"/>
  <text x="{w - 30}" y="38" text-anchor="end" class="meta">measured in production</text>
  {"".join(tiles)}
</svg>"""
    write("impact.svg", svg)


# --------------------------------------------------------------------------
# Certifications
# --------------------------------------------------------------------------

# (name, issuer, year, badge letters, credential id or None)
CERTS = [
    ("System Administration and IT Infrastructure Services", "Google · Coursera", 2025, "G", "29N5ZLK6BVWW"),
    ("Full Stack Software Developer Assessment", "IBM · Coursera", 2023, "IBM", "74NSF2JALFZV"),
    ("Discovering Computer Networks: hands-on in the Open Networking Lab", "The Open University", 2023, "OU", None),
    ("Successful IT Systems", "The Open University", 2023, "OU", None),
    ("Information Security Basics for IT Support Technicians", "Udemy", 2022, "U", None),
]


def certs() -> None:
    import math

    w, row_h, top = 880, 54, 104
    n = len(CERTS)
    h = top + row_h * (n - 1) + 88
    hx = 60
    verified = sum(1 for c in CERTS if c[4])

    def hexagon(cx: float, cy: float, r: float) -> str:
        return " ".join(
            f"{cx + r * math.cos(math.radians(60 * k - 90)):.1f},{cy + r * math.sin(math.radians(60 * k - 90)):.1f}" for k in range(6)
        )

    rows = []
    for i, (name, issuer, year, mark, cred) in enumerate(CERTS):
        yc = top + i * row_h
        d = 0.25 + i * 0.14
        ok = cred is not None
        badge = (
            f'<g class="hx" style="animation-delay:{d:.2f}s">'
            f'<polygon points="{hexagon(hx, yc, 19)}" fill="{ACCENT if ok else BG}" fill-opacity="{".14" if ok else "1"}" '
            f'stroke="{ACCENT if ok else LINE}" stroke-width="1.6"{f" filter={chr(34)}url(#c-glow){chr(34)}" if ok else ""}/>'
            f'<text x="{hx}" y="{yc + 4}" text-anchor="middle" class="mk" fill="{ACCENT if ok else MUTED}">{mark}</text></g>'
        )
        if ok:
            status = (
                f'<rect x="{w - 30 - 104}" y="{yc - 19}" width="104" height="20" rx="10" fill="{ACCENT}" fill-opacity=".1" stroke="{ACCENT}" stroke-opacity=".6"/>'
                f'<path d="M{w - 30 - 90},{yc - 9} l4,4 l8,-8" fill="none" stroke="{ACCENT}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" pathLength="10" class="tick" style="animation-delay:{d + 0.4:.2f}s"/>'
                f'<text x="{w - 30 - 44}" y="{yc - 5}" text-anchor="middle" class="st" fill="{ACCENT}">verified</text>'
                f'<text x="{w - 30}" y="{yc + 15}" text-anchor="end" class="id">coursera.org/verify/{cred}</text>'
            )
        else:
            status = (
                f'<rect x="{w - 30 - 104}" y="{yc - 19}" width="104" height="20" rx="10" fill="none" stroke="{LINE}"/>'
                f'<text x="{w - 30 - 52}" y="{yc - 5}" text-anchor="middle" class="st" fill="{MUTED}">on file</text>'
                f'<text x="{w - 30}" y="{yc + 15}" text-anchor="end" class="id">{"statement of participation" if "Open" in issuer else "certificate of completion"}</text>'
            )
        rows.append(
            f'{badge}<g class="r" style="animation-delay:{d:.2f}s">'
            f'<text x="{hx + 36}" y="{yc - 3}" class="nm">{escape(name)}</text>'
            f'<text x="{hx + 36}" y="{yc + 15}" class="is">{escape(issuer)} · {year}</text>'
            f"{status}</g>"
        )

    band_top, band_bot = top - 30, top + row_h * (n - 1) + 30
    fy = h - 28
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Certifications">
  <title>Certifications</title>
  <defs>
    <pattern id="c-dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{LINE}" opacity=".55"/></pattern>
    <radialGradient id="c-halo" cx="0.04" cy="0.1" r="0.6"><stop offset="0" stop-color="{ACCENT}" stop-opacity=".08"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>
    <linearGradient id="c-scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/><stop offset=".85" stop-color="{ACCENT}" stop-opacity=".07"/><stop offset="1" stop-color="{ACCENT}" stop-opacity=".45"/></linearGradient>
    <clipPath id="c-clip"><rect x="20" y="{band_top}" width="{w - 40}" height="{band_bot - band_top}"/></clipPath>
    <filter id="c-glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <style>
    text {{ font-family: {SANS}; }}
    .cmd, .meta, .mk, .st, .id, .foot {{ font-family: {MONO}; }}
    .cmd {{ font-size: 13px; fill: {TEXT}; }}
    .meta {{ font-size: 11px; fill: {MUTED}; }}
    .nm {{ font-size: 14px; font-weight: 600; fill: {TEXT}; }}
    .is {{ font-size: 12px; fill: {MUTED}; }}
    .mk {{ font-size: 10.5px; font-weight: 700; }}
    .st {{ font-size: 10.5px; }}
    .id {{ font-size: 10.5px; fill: {MUTED}; }}
    .foot {{ font-size: 11px; fill: {MUTED}; }}
    .r {{ animation: rin .55s ease-out both; }}
    .hx {{ transform-box: fill-box; transform-origin: center; animation: spin .7s cubic-bezier(.3,1.5,.5,1) both; }}
    .tick {{ stroke-dasharray: 10; animation: tick .5s ease-out both; }}
    .scan {{ animation: scan 4.5s ease-in-out 1.4s infinite; }}
    .cur {{ animation: blink 1.05s steps(1) infinite; }}
    @keyframes rin {{ from {{ opacity: 0; transform: translateX(-12px); }} }}
    @keyframes spin {{ from {{ opacity: 0; transform: rotate(-90deg) scale(.4); }} }}
    @keyframes tick {{ from {{ stroke-dashoffset: 10; }} to {{ stroke-dashoffset: 0; }} }}
    @keyframes scan {{ from {{ transform: translateY(-80px); }} to {{ transform: translateY({band_bot - band_top}px); }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} .scan {{ display: none; }} }}
  </style>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{BG}" stroke="{LINE}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="url(#c-dots)"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="url(#c-halo)"/>
  <text x="28" y="40" class="cmd"><tspan fill="{ACCENT}">~/certs</tspan><tspan fill="{MUTED}"> $ </tspan>verify --all</text>
  <rect x="{28 + 22 * 7.8 + 6:.0f}" y="29" width="8" height="14" fill="{ACCENT}" class="cur"/>
  <text x="{w - 30}" y="40" text-anchor="end" class="meta"><tspan fill="{ACCENT}">{verified} publicly verifiable</tspan> · {n} credentials</text>
  <line x1="28" y1="58" x2="{w - 28}" y2="58" stroke="{LINE}"/>
  <g clip-path="url(#c-clip)"><rect x="20" y="{band_top}" width="{w - 40}" height="80" fill="url(#c-scan)" class="scan" opacity="0"><set attributeName="opacity" to="1" begin="1.4s"/></rect></g>
  {"".join(rows)}
  <line x1="28" y1="{fy - 22}" x2="{w - 28}" y2="{fy - 22}" stroke="{LINE}" stroke-dasharray="3 5"/>
  <text x="28" y="{fy}" class="foot"><tspan fill="{ACCENT}">+ 20</tspan> completed courses in Python, data science, machine learning, SQL and software development</text>
</svg>"""
    write("certs.svg", svg)


# --------------------------------------------------------------------------
# Career timeline
# --------------------------------------------------------------------------

# The career is drawn as `git log --graph`: every role is a commit on main,
# growing upwards from the first job, and the M.Sc. is a branch that forks
# at the university internship and merges back in.

# (role, organisation, tag, years shown, start, end or None for current)
# Newest first. Dates are year + (month - 1) / 12 and only size the uptime bars.
CAREER = [
    ("IT Engineer", "Kontinental Establishment", "HEAD → main|full-time", "2023 — now", 2023.25, None),
    ("M.Sc. Data Science", "University of Göttingen", "merge", "2023 — 2025", 2023.0, 2025.92),
    ("IT Engineer", "TestSolutions GmbH", "contract", "2023 — 2024", 2023.08, 2024.92),
    ("DevSecOps · Scientific Computing", "University of Göttingen", "internship", "2022 — 2023", 2022.83, 2023.08),
    ("IT Specialist", "Liberty Books", "full-time", "2022", 2022.42, 2022.75),
    ("IT Specialist", "KTDMC", "full-time", "2021 — 2022", 2021.75, 2022.33),
    ("IT Specialist", "Target Logistics International", "full-time", "2020 — 2021", 2020.5, 2021.67),
    ("IT Engineer", "The Active Solutions", "full-time", "2019 — 2020", 2019.25, 2020.17),
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
        cx0 = text_x + len(role) * 7.2 + 12
        for t in filter(None, tag.split("|")):
            cw = len(t) * 6.3 + 16
            if t == "HEAD → main":
                chip += (f'<rect x="{cx0:.1f}" y="{yc - 17}" width="{cw:.1f}" height="17" rx="8.5" fill="{ACCENT}"/>'
                         f'<text x="{cx0 + cw / 2:.1f}" y="{yc - 5}" text-anchor="middle" class="chip" fill="{BG}" font-weight="700">{escape(t)}</text>')
            else:
                chip += (f'<rect x="{cx0:.1f}" y="{yc - 17}" width="{cw:.1f}" height="17" rx="8.5" fill="none" stroke="{LINE}"/>'
                         f'<text x="{cx0 + cw / 2:.1f}" y="{yc - 5}" text-anchor="middle" class="chip" fill="{MUTED}">{escape(t)}</text>')
            cx0 += cw + 6

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
    write("career.svg", svg)


if __name__ == "__main__":
    terminal()
    impact()
    for project in PROJECTS:
        card(project)
    certs()
    timeline()
