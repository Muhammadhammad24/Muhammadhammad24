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

BG = "#09090B"
PANEL = "#141417"
LINE = "#26272B"
TEXT = "#F5F5F7"
MUTED = "#71757F"
ACCENT = "#5B8DEF"
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

OU = "https://www.open.edu/openlearn/"
UDEMY = "https://www.udemy.com/certificate/"
COURSERA = "https://www.coursera.org/account/accomplishments/verify/"

# Featured credentials, grouped into tracks. (name, issuer, mark, year, hours, link, link label)
TRACKS = [
    ("infrastructure · networking · security", [
        ("System Administration and IT Infrastructure Services", "Google · Coursera", "G", 2025, "23 h", COURSERA + "29N5ZLK6BVWW", "verify"),
        ("Discovering Computer Networks: hands-on in the Open Networking Lab", "The Open University", "OU", 2023, "24 h",
         OU + "digital-computing/discovering-computer-networks-hands-on-the-open-networking-lab/content-section-overview", "course"),
        ("Information Security Basics for IT Support Technicians", "Udemy", "U", 2022, "", UDEMY + "UC-7c6ee425-74e1-489d-908c-d0b201c4ff3c/", "verify"),
        ("Successful IT Systems", "The Open University", "OU", 2023, "", OU + "digital-computing/successful-it-systems/content-section-0", "course"),
    ]),
    ("software engineering", [
        ("Full Stack Software Developer Assessment", "IBM · Coursera", "IBM", 2023, "", COURSERA + "74NSF2JALFZV", "verify"),
        ("The Complete React, Redux, Node, Express and MySQL Developer Course", "Udemy", "U", 2022, "8 h", UDEMY + "UC-0b67e267-2b09-40d7-a980-d2f5b62876fe/", "verify"),
        ("The Database Development Life Cycle", "The Open University", "OU", 2023, "12 h", OU + "digital-computing/the-database-development-life-cycle/content-section-0", "course"),
        ("SQL: The Complete Introduction to SQL Programming", "Udemy", "U", 2022, "3.5 h", UDEMY + "UC-be70fe74-aa67-4e6c-afad-5cacc8d371ae/", "verify"),
    ]),
    ("data · machine learning · ai", [
        ("The Data Science Course: Complete Data Science Bootcamp", "Udemy", "U", 2022, "30 h", UDEMY + "UC-b72e7563-4360-4d02-abf9-47bf7b9dc046/", "verify"),
        ("Python for Machine Learning with NumPy, Pandas and Matplotlib", "Udemy", "U", 2022, "7 h", UDEMY + "UC-b6509a21-528b-43bf-b0ae-f7458612d212/", "verify"),
        ("Python: Introduction to Data Science and Machine Learning A–Z", "Udemy", "U", 2022, "7.5 h", UDEMY + "UC-4c5d2d2a-dade-4cee-a7c4-0fd2ad689c90/", "verify"),
        ("Exploring Data: Graphs and Numerical Summaries", "The Open University", "OU", 2023, "20 h",
         OU + "science-maths-technology/mathematics-statistics/exploring-data-graphs-and-numerical-summaries/content-section-0", "course"),
    ]),
]
TOTAL_CREDENTIALS = 29
MORE = "Java · C++ · PHP · R · HTML & CSS · Android · big data · Python ×2 · AI & the future of work · mathematics · modelling"


def _wrap(text: str, limit: int) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        if cur and len(cur) + 1 + len(word) > limit:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    lines.append(cur)
    return lines


def _hexagon(cx: float, cy: float, r: float) -> str:
    import math

    return " ".join(
        f"{cx + r * math.cos(math.radians(60 * k - 90)):.1f},{cy + r * math.sin(math.radians(60 * k - 90)):.1f}" for k in range(6)
    )


_CERT_STYLE = f"""
  <style>
    text {{ font-family: {SANS}; }}
    .m, .cmd, .meta, .tag, .tr, .mk {{ font-family: {MONO}; }}
    .cmd {{ font-size: 13px; fill: {TEXT}; }}
    .meta {{ font-size: 11px; fill: {MUTED}; }}
    .nm {{ font-size: 13px; font-weight: 600; fill: {TEXT}; }}
    .is {{ font-size: 11px; fill: {MUTED}; }}
    .mk {{ font-size: 10px; font-weight: 700; fill: {ACCENT}; }}
    .tag {{ font-size: 10px; fill: {MUTED}; }}
    .tr {{ font-size: 11px; letter-spacing: 1.6px; fill: {MUTED}; }}
    .in {{ animation: rin .5s ease-out both; }}
    .hx {{ animation: rin .5s ease-out both; }}
    .cur {{ animation: blink 1.05s steps(1) infinite; }}
    @keyframes rin {{ from {{ opacity: 0; transform: translateX(-10px); }} }}
    @keyframes spin {{ from {{ opacity: 0; transform: rotate(-90deg) scale(.4); }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
  </style>"""


def _cert_frame(w: int, h: int, uid: str) -> str:
    return f"""
  <defs>
    <pattern id="{uid}-dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{LINE}" opacity=".5"/></pattern>
    <radialGradient id="{uid}-halo" cx="0" cy="0" r="0.9"><stop offset="0" stop-color="{ACCENT}" stop-opacity=".06"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>
  </defs>{_CERT_STYLE}
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" fill="{BG}" stroke="{LINE}"/>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" fill="url(#{uid}-dots)"/>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" fill="url(#{uid}-halo)"/>"""


def certs() -> None:
    """Header, track labels and one small card per credential, laid out as a table in the README."""
    shown = sum(len(items) for _, items in TRACKS)

    w, h = 880, 60
    write("certifications/header.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Certifications">
  <title>Certifications</title>{_cert_frame(w, h, "hd")}
  <text x="26" y="35" class="cmd"><tspan fill="{ACCENT}">~/certs</tspan><tspan fill="{MUTED}"> $ </tspan>ls --featured</text>
  <rect x="{26 + 24 * 7.8 + 6:.0f}" y="24" width="8" height="14" fill="{ACCENT}" class="cur"/>
  <text x="{w - 26}" y="35" text-anchor="end" class="meta">{TOTAL_CREDENTIALS} credentials · Google · IBM · Open University · Udemy · {shown} shown</text>
</svg>""")

    for t, (track, items) in enumerate(TRACKS, 1):
        w, h = 880, 40
        write(f"certifications/track-{t}.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(track)}">
  <title>{escape(track)}</title>{_cert_frame(w, h, f"tr{t}")}
  <text x="20" y="25" class="tr in"><tspan fill="{ACCENT}">{t:02d}</tspan>  {escape(track.upper())}</text>
  <line x1="{20 + (len(track) + 4) * 8.3:.0f}" y1="21" x2="{w - 150}" y2="21" stroke="{LINE}"/>
  <text x="{w - 20}" y="25" text-anchor="end" class="tr">{len(items)} credentials</text>
</svg>""")

        for k, (name, issuer, mark, year, hours, _link, label) in enumerate(items, 1):
            w, h = 430, 92
            uid = f"t{t}c{k}"
            d = 0.1 + (k - 1) * 0.1
            lines = _wrap(name, 46)[:2]
            meta = " · ".join(x for x in (issuer, str(year), hours) if x)
            title = "".join(f'<text x="24" y="{34 + j * 18}" class="nm">{escape(line)}</text>' for j, line in enumerate(lines))
            tag_w = len(label) * 6.2 + 34
            write(f"certifications/{t}-{k}.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(name)}">
  <title>{escape(name)}</title>{_cert_frame(w, h, uid)}
  <g class="hx" style="animation-delay:{d:.2f}s">
    <rect x="0" y="1" width="3" height="{h - 2}" rx="1.5" fill="{ACCENT}"/>
  </g>
  <g class="in" style="animation-delay:{d:.2f}s">
    {title}
    <text x="24" y="{34 + len(lines) * 18 + 4}" class="is">{escape(meta)}</text>
  </g>
  <rect x="{w - 16 - tag_w:.1f}" y="{h - 30}" width="{tag_w:.1f}" height="20" rx="10" fill="none" stroke="{LINE}"/>
  <text x="{w - 16 - tag_w / 2:.1f}" y="{h - 16}" text-anchor="middle" class="tag">{label} ↗</text>
</svg>""")

    w, h = 880, 46
    write("certifications/more.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="More courses">
  <title>More courses</title>{_cert_frame(w, h, "mo")}
  <text x="26" y="28" class="meta"><tspan fill="{ACCENT}">+ {TOTAL_CREDENTIALS - shown} more</tspan>   {escape(MORE)}</text>
</svg>""")


# --------------------------------------------------------------------------
# Career timeline
# --------------------------------------------------------------------------

# The career is drawn as `git log --graph`: every role is a commit on main,
# growing upwards from the first job, and the M.Sc. is a branch that forks
# at the university internship and merges back in.

# (role, organisation, tag, years shown, start, end or None for current)
# Newest first. Dates are year + (month - 1) / 12 and only size the uptime bars.
# Roles only, newest first; education is listed separately below so the
# employment sequence reads straight down without a degree interrupting it.
# (role, organisation, tag, years shown, start, end or None for current)
CAREER = [
    # (role, organisation, location, type, dates shown, start, end or None)
    ("IT Engineer", "Kontinental Establishment", "Germany · remote", "Full-time", "Apr 2023 — now", 2023.25, None),
    ("IT Engineer", "TestSolutions GmbH", "Germany", "Contract", "Jan 2023 — Dec 2024", 2023.08, 2024.92),
    ("DevSecOps · Scientific Computing", "University of Göttingen", "Göttingen, Germany", "Internship", "Nov 2022 — Jan 2023", 2022.83, 2023.08),
    ("IT Specialist", "Liberty Books", "Karachi, Pakistan", "Full-time", "Jun 2022 — Oct 2022", 2022.42, 2022.75),
    ("IT Specialist", "KTDMC", "Karachi, Pakistan", "Full-time", "Oct 2021 — May 2022", 2021.75, 2022.33),
    ("IT Specialist", "Target Logistics International", "Karachi, Pakistan", "Full-time", "Jul 2020 — Sep 2021", 2020.5, 2021.67),
    ("IT Engineer", "The Active Solutions", "Karachi, Pakistan", "Full-time", "Apr 2019 — Mar 2020", 2019.25, 2020.17),
]
CAREER.sort(key=lambda r: r[5], reverse=True)

# (degree, institution, years)
EDUCATION = [
    ("M.Sc. Data Science & Computer Science", "University of Göttingen, Germany", "2023 — 2026"),
    ("B.Sc. Computer Science", "University of Karachi, Pakistan", "2016 — 2018"),
]


def timeline() -> None:
    """Career drawn the way the portfolio draws it: a quiet rail, the year on
    the left, one dot per role. No git-log chrome, no glow."""
    w, row_h, top = 880, 62, 96
    n = len(CAREER)
    edu_h = 34 + len(EDUCATION) * 34
    h = top + row_h * (n - 1) + 56 + edu_h
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
        bw = max(10.0, 110 * span / longest)
        bar = (
            f'<rect x="{w - 140}" y="{yc + 6}" width="110" height="3" rx="1.5" fill="{LINE}"/>'
            f'<rect x="{w - 30 - bw:.1f}" y="{yc + 6}" width="{bw:.1f}" height="3" rx="1.5" '
            f'fill="{ACCENT}" fill-opacity="{1 if head else 0.55}" class="bar" style="animation-delay:{d + 0.15:.2f}s"/>'
        )
        rows.append(
            f'<g class="r" style="animation-delay:{d:.2f}s">'
            f'<text x="{year_x}" y="{yc + 4}" text-anchor="end" class="yrs" '
            f'fill="{ACCENT if head else MUTED}">{years.split(" — ")[0]}</text>'
            f'<text x="{text_x}" y="{yc - 3}" class="role">{escape(role)}</text>{chips}'
            f'<text x="{text_x}" y="{yc + 14}" class="org">{escape(org)} · {escape(loc)}</text>'
            f'<text x="{w - 30}" y="{yc - 3}" text-anchor="end" class="yrs" '
            f'fill="{MUTED}">{years}</text>'
            f'{bar}</g>{node}'
        )

    edu_y = y(n - 1) + 56
    edu_rows = "".join(
        f'<text x="{text_x}" y="{edu_y + 20 + j * 34}" class="role" font-size="13.5">{escape(deg)}</text>'
        f'<text x="{text_x}" y="{edu_y + 36 + j * 34}" class="org">{escape(inst)}</text>'
        f'<text x="{w - 30}" y="{edu_y + 20 + j * 34}" text-anchor="end" class="yrs" fill="{MUTED}">{yrs}</text>'
        f'<circle cx="{rail_x}" cy="{edu_y + 16 + j * 34}" r="3.5" fill="{BG}" stroke="{LINE}" stroke-width="2"/>'
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
    .r {{ animation: rin .45s ease-out both; }}
    .bar {{ transform-box: fill-box; transform-origin: right; animation: grow .7s ease-out both; }}
    @keyframes rin {{ from {{ opacity: 0; transform: translateY(8px); }} }}
    @keyframes grow {{ from {{ transform: scaleX(0); }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
  </style>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{PANEL}" stroke="{LINE}"/>
  <rect x="1" y="1" width="3" height="{h - 2}" rx="1.5" fill="{ACCENT}"/>

  <text x="30" y="44" class="lbl">CAREER</text>
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

    write("career.svg", svg)


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


def toolbox() -> None:
    """Two builds of the same panel; the README picks one with prefers-color-scheme."""
    for mode, t in THEMES.items():
        dark = mode == "dark"
        w, top, row_h, label_w, step = 880, 72, 84, 196, 81
        h = top + row_h * len(TOOLBOX) + 10
        total = sum(len(items) for _, items in TOOLBOX)
        rows = []
        for r, (cat, items) in enumerate(TOOLBOX):
            y = top + r * row_h
            if r:
                rows.append(f'<line x1="26" y1="{y - 10}" x2="{w - 26}" y2="{y - 10}" stroke="{t["line"]}" stroke-dasharray="2 5"/>')
            rows.append(
                f'<g class="in" style="animation-delay:{0.1 + r * 0.08:.2f}s">'
                f'<circle cx="32" cy="{y + 22}" r="3" fill="{t["accent"]}" class="led" style="animation-delay:{r * 0.3:.1f}s"/>'
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
                    for k, part in enumerate(_wrap(label, 12))
                )
                rows.append(f'<g class="logo" style="animation-delay:{d:.2f}s">{logo}{labels}</g>')
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
    .in {{ animation: rin .5s ease-out both; }}
    .logo {{ transform-box: fill-box; transform-origin: center; animation: pop .45s cubic-bezier(.3,1.6,.5,1) both; }}
    .led {{ animation: led 2.4s ease-in-out infinite; }}
    .cur {{ animation: blink 1.05s steps(1) infinite; }}
    @keyframes rin {{ from {{ opacity: 0; transform: translateX(-10px); }} }}
    @keyframes pop {{ from {{ opacity: 0; transform: scale(.5); }} }}
    @keyframes led {{ 50% {{ opacity: .25; }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
  </style>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{t["bg"]}" stroke="{t["line"]}"/>
  <text x="26" y="38" class="cmd"><tspan fill="{t["prompt"]}">~/toolbox</tspan><tspan fill="{t["muted"]}"> $ </tspan>ls --all</text>
  <rect x="{26 + 20 * 7.8 + 6:.0f}" y="27" width="8" height="14" fill="{t["accent"]}" class="cur"/>
  <text x="{w - 26}" y="38" text-anchor="end" class="meta">{total} tools · {len(TOOLBOX)} domains · hands-on</text>
  <line x1="26" y1="54" x2="{w - 26}" y2="54" stroke="{t["line"]}"/>
  {"".join(rows)}
</svg>"""
        write(f"brands-{mode}.svg", svg)


if __name__ == "__main__":
    terminal()
    impact()
    for project in PROJECTS:
        card(project)
    certs()
    timeline()
    toolbox()
