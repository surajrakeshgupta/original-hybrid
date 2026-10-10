"""Tagline, career log and toolkit panels, in the same terminal style as the
info card. Edit the content blocks below, then run:

    python scripts/make_extras.py            # writes tagline.svg, career-log.svg, toolkit.svg
    STATIC=1 python scripts/make_extras.py   # frozen frames for previews
"""
import os
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- content ---
PROMPT = "suraj@dublin:~$"
COMMAND = "whoami --role"
ROLES = [
    "SOC Analyst",
    "Security Analyst",
    "Phishing Detection Researcher",
    "CEH Practical certified",
]

# newest first: (summary, detail or "")
CAREER = [
    ("Open to full-time cyber security roles in Ireland", ""),
    ("Senior Sales Executive / Energy Advisor, SSE Airtricity, Dublin", "2025-26"),
    ("MSc Cyber Security, National College of Ireland, 2:1", "2025"),
    ("  dissertation: Detecting Cross-Cultural Phishing Attacks", ""),
    ("Associate Cyber Security Analyst, 24/7 SOC, Mindtickle, Pune", "2022-23"),
    ("BE Information Technology, Pune University", "2022"),
]
CERTS = ["certs/ceh-practical"]

# (package, where I used it, status)  status: "certified" gets a pill
TOOLKIT = [
    ("ceh-practical",  "EC-Council hands-on ethical hacking exam",       "certified"),
    ("soc-operations", "24/7 SOC at Mindtickle, Jul 2022 - Nov 2023",    "used"),
    ("python",         "security log analysis and ML notebooks",         "used"),
    ("scikit-learn",   "Random Forest, Naive Bayes, DBSCAN on logs",     "used"),
    ("pandas",         "parsing HDFS and Windows event logs",            "used"),
    ("jupyter",        "federated learning research notebook",           "used"),
    ("javascript",     "Cyrillic homoglyph URL detector",                "used"),
    ("bootstrap",      "Cyrillic-Guard web front end",                   "used"),
    ("vercel",         "Cyrillic-Guard live demo hosting",               "used"),
    ("php",            "TeachersAssistant web app (2021)",               "used"),
]
# ----------------------------------------------------------------------------

W = 860
PAD = 22
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,DejaVu Sans Mono,Liberation Mono,monospace"
FS = 12.5
CW = FS * 0.6          # monospace advance
LINE_H = 21
BG = "#0d1117"
BAR_BG = "#161b22"
BORDER = "#30363d"
TEXT = "#c9d1d9"
DIM = "#8b949e"
BLUE = "#58a6ff"
GREEN = "#39d353"
MINT = "#69f0a0"
YELLOW = "#d29922"
CYAN = "#39c5cf"
PILL_BG = "#0e2a17"
STEP = float(os.environ.get("EXTRA_STEP", 0.28))
START = float(os.environ.get("EXTRA_START", 0.6))
STATIC = os.environ.get("STATIC") == "1"


def window(h: int, title: str, body: list[str], css: str = "") -> str:
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" aria-label="{escape(title)}">',
        css,
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
        f'<path d="M0.5 10.5 a10 10 0 0 1 10 -10 h{W-21} a10 10 0 0 1 10 10 v18 h-{W-1} z" fill="{BAR_BG}"/>',
        f'<line x1="0.5" y1="28.5" x2="{W-0.5}" y2="28.5" stroke="{BORDER}"/>',
        '<circle cx="16" cy="14.5" r="5" fill="#f85149"/>',
        '<circle cx="32" cy="14.5" r="5" fill="#d29922"/>',
        '<circle cx="48" cy="14.5" r="5" fill="#39d353"/>',
        f'<text x="{W/2}" y="18.5" text-anchor="middle" font-family="{FONT}" font-size="11" fill="{DIM}">{escape(title)}</text>',
        f'<g font-family="{FONT}" font-size="{FS}">',
        *body,
        "</g></svg>",
    ])


FADE_CSS = "" if STATIC else (
    "<style>.l{opacity:0;transform:translateX(-6px);animation:in .6s ease-out forwards}"
    "@keyframes in{to{opacity:1;transform:translateX(0)}}</style>"
)


def line(i: int, inner: str) -> str:
    if STATIC:
        return f"<g>{inner}</g>"
    return f'<g class="l" style="animation-delay:{START + i * STEP:.2f}s">{inner}</g>'


def pill(x: float, y: float, label: str) -> tuple[str, float]:
    w = len(label) * CW + 18
    svg = (f'<rect x="{x:.1f}" y="{y - 14}" width="{w:.1f}" height="20" rx="10" fill="{PILL_BG}" stroke="{GREEN}"/>'
           f'<text x="{x + 9:.1f}" y="{y}" fill="{MINT}">{escape(label)}</text>')
    return svg, w


# ------------------------------------------------------------------ tagline --
def tagline() -> None:
    """One prompt line that types each role, holds it, deletes it, and loops."""
    h = 56
    y = 33
    prompt_w = (len(PROMPT) + 1) * CW
    cmd_x = PAD + prompt_w
    role_x = cmd_x + (len(COMMAND) + 1) * CW

    type_s, hold, del_s, gap = 0.075, 2.2, 0.035, 0.45   # seconds
    phases, t = [], 0.0
    for r in ROLES:
        phases.append(t)
        t += len(r) * (type_s + del_s) + hold + gap
    total = t

    defs, texts, cursor_keys = [], [], []
    for k, (role, start) in enumerate(zip(ROLES, phases)):
        n = len(role)
        keys = [(0.0, 0)]
        keys += [(start + c * type_s, c) for c in range(1, n + 1)]
        typed_end = start + n * type_s + hold
        keys += [(typed_end + (n - c) * del_s, c) for c in range(n - 1, -1, -1)]
        times = ";".join(f"{tt / total:.5f}" for tt, _ in keys) + ";1"
        vals = ";".join(f"{c * CW:.1f}" for _, c in keys) + ";0"
        defs.append(
            f'<clipPath id="r{k}"><rect x="{role_x:.1f}" y="{y - 14}" height="20" width="0">'
            f'<animate attributeName="width" dur="{total:.2f}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{times}" values="{vals}"/></rect></clipPath>'
        )
        texts.append(f'<text x="{role_x:.1f}" y="{y}" fill="{MINT}" font-weight="bold" clip-path="url(#r{k})">{escape(role)}</text>')
        cursor_keys += [(tt, c) for tt, c in keys[1:]]

    cursor_keys.sort()
    ct = ";".join(["0"] + [f"{tt / total:.5f}" for tt, _ in cursor_keys] + ["1"])
    cv = ";".join([f"{role_x + 1:.1f}"] + [f"{role_x + c * CW + 1:.1f}" for _, c in cursor_keys] + [f"{role_x + 1:.1f}"])

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" '
        f'aria-label="{escape(PROMPT)} {escape(COMMAND)}: {escape(", ".join(ROLES))}">',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
        f'<g font-family="{FONT}" font-size="{FS}">',
        f'<text x="{PAD}" y="{y}" fill="{GREEN}">{escape(PROMPT)}</text>',
        f'<text x="{cmd_x:.1f}" y="{y}" fill="{TEXT}">{escape(COMMAND)}</text>',
    ]
    if STATIC:
        out.append(f'<text x="{role_x:.1f}" y="{y}" fill="{MINT}" font-weight="bold">{escape(ROLES[0])}</text>')
        out.append(f'<rect x="{role_x + len(ROLES[0]) * CW + 1:.1f}" y="{y - 12}" width="{CW:.1f}" height="15" fill="{MINT}"/>')
    else:
        out.append("<defs>" + "".join(defs) + "</defs>")
        out += texts
        out.append(
            f'<rect y="{y - 12}" width="{CW:.1f}" height="15" fill="{MINT}" x="{role_x + 1:.1f}">'
            f'<animate attributeName="x" dur="{total:.2f}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{ct}" values="{cv}"/>'
            '<animate attributeName="opacity" values="1;0" keyTimes="0;0.5" calcMode="discrete" dur="1s" repeatCount="indefinite"/>'
            "</rect>"
        )
    out.append("</g></svg>")
    (ROOT / "tagline.svg").write_text("\n".join(out), encoding="utf-8")


# --------------------------------------------------------------- career log --
def career_log() -> None:
    hashes = ["e3c41a9", "b07d2f6", "9a51c3e", "", "4f8e0b2", "1c6d7a4"]
    y = 54
    body, i = [], 0
    body.append(line(i, f'<text x="{PAD}" y="{y}"><tspan fill="{GREEN}">$</tspan>'
                        f'<tspan fill="{TEXT}"> git log --oneline --graph</tspan></text>'))
    y += LINE_H
    i += 1
    for k, ((summary, when), h) in enumerate(zip(CAREER, hashes)):
        parts = []
        if h:
            parts.append(f'<text x="{PAD}" y="{y}" fill="{GREEN}">*</text>')
            parts.append(f'<text x="{PAD + 2 * CW:.1f}" y="{y}" fill="{YELLOW}">{h}</text>')
            x = PAD + 10 * CW
            if k == 0:
                head = (f'<tspan fill="{YELLOW}">(</tspan><tspan fill="{CYAN}" font-weight="bold">HEAD</tspan>'
                        f'<tspan fill="{DIM}"> -&gt; </tspan><tspan fill="{GREEN}" font-weight="bold">main</tspan>'
                        f'<tspan fill="{YELLOW}">)</tspan> ')
                parts.append(f'<text x="{x:.1f}" y="{y}">{head}<tspan fill="{TEXT}">{escape(summary)}</tspan></text>')
            else:
                parts.append(f'<text x="{x:.1f}" y="{y}" fill="{TEXT}">{escape(summary)}</text>')
        else:
            parts.append(f'<text x="{PAD}" y="{y}" fill="{GREEN}">|</text>')
            parts.append(f'<text x="{PAD + 10 * CW:.1f}" y="{y}" fill="{DIM}">{escape(summary.strip())}</text>')
        if when:
            parts.append(f'<text x="{W - PAD}" y="{y}" text-anchor="end" fill="{DIM}">{escape(when)}</text>')
        body.append(line(i, "".join(parts)))
        y += LINE_H
        i += 1
    y += 12
    body.append(line(i, f'<text x="{PAD}" y="{y}"><tspan fill="{GREEN}">$</tspan>'
                        f'<tspan fill="{TEXT}"> git tag --list "certs/*"</tspan></text>'))
    y += LINE_H + 4
    i += 1
    x = PAD
    pills = []
    for c in CERTS:
        svg, w = pill(x, y, c)
        pills.append(svg)
        x += w + 10
    body.append(line(i, "".join(pills)))
    h = int(y + 26)
    (ROOT / "career-log.svg").write_text(window(h, "~/career (main)", body, FADE_CSS), encoding="utf-8")


# ------------------------------------------------------------------ toolkit --
def toolkit() -> None:
    col2 = PAD + 18 * CW
    col3 = W - PAD - 90
    y = 54
    body, i = [], 0
    body.append(line(i, f'<text x="{PAD}" y="{y}"><tspan fill="{GREEN}">$</tspan>'
                        f'<tspan fill="{TEXT}"> pip list --user --verbose</tspan></text>'))
    y += LINE_H
    i += 1
    body.append(line(i,
        f'<text x="{PAD}" y="{y}" fill="{DIM}">Package</text>'
        f'<text x="{col2:.1f}" y="{y}" fill="{DIM}">Where I used it</text>'
        f'<text x="{col3:.1f}" y="{y}" fill="{DIM}">Status</text>'
        f'<line x1="{PAD}" y1="{y + 6}" x2="{W - PAD}" y2="{y + 6}" stroke="{BORDER}"/>'))
    y += LINE_H
    i += 1
    for pkg, where, status in TOOLKIT:
        parts = [
            f'<text x="{PAD}" y="{y}" fill="{BLUE}">{escape(pkg)}</text>',
            f'<text x="{col2:.1f}" y="{y}" fill="{TEXT}">{escape(where)}</text>',
        ]
        if status == "certified":
            svg, _ = pill(col3 - 9, y, status)
            parts.append(svg)
        else:
            parts.append(f'<text x="{col3:.1f}" y="{y}" fill="{DIM}">{escape(status)}</text>')
        body.append(line(i, "".join(parts)))
        y += LINE_H
        i += 1
    h = int(y + 12)
    (ROOT / "toolkit.svg").write_text(window(h, "~/toolkit", body, FADE_CSS), encoding="utf-8")


if __name__ == "__main__":
    tagline()
    career_log()
    toolkit()
    print("wrote tagline.svg, career-log.svg, toolkit.svg")
