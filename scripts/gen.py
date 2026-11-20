"""Generates the animated SVG assets for iliass-elguaari's profile README.

Theme: "Floodlights" — a night match. Red LED stadium scoreboard
(the red of a referee's card) over a floodlit pitch.
"""
import math
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets"

AMBER = "#FF2D3D"  # red-card red (kept the name so the code reads the same)
AMBER_DIM = "#3A0A0E"
GREEN = "#C9D3CD"  # chalk, for the HOME / AWAY row
PITCH = "#0E4D32"
PITCH2 = "#12603F"
NIGHT = "#06090F"
NIGHT2 = "#0B1220"
CHALK = "#F4F8F2"

# ---------------------------------------------------------------- 5x7 LED font
F = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "10001", "11001", "10101", "10011", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    " ": ["00000"] * 7,
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    ",": ["00000", "00000", "00000", "00000", "01100", "00100", "01000"],
    ":": ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    "/": ["00001", "00001", "00010", "00100", "01000", "10000", "10000"],
    "'": ["00100", "00100", "01000", "00000", "00000", "00000", "00000"],
    "!": ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    "·": ["00000", "00000", "00000", "01100", "01100", "00000", "00000"],
    "°": ["01100", "10010", "10010", "01100", "00000", "00000", "00000"],
    "*": ["00100", "10101", "01110", "11111", "01110", "10101", "00100"],
    ">": ["01000", "00100", "00010", "00001", "00010", "00100", "01000"],
    "<": ["00010", "00100", "01000", "10000", "01000", "00100", "00010"],
    "+": ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    "#": ["01010", "01010", "11111", "01010", "11111", "01010", "01010"],
    "&": ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
    "%": ["11001", "11010", "00010", "00100", "01000", "01011", "10011"],
    "(": ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ")": ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
}


def text_cols(s):
    return len(s) * 6 - 1


def led_path(s, x0, y0, pitch):
    """One path whose round-capped zero-length segments draw each lit LED."""
    parts = []
    for i, ch in enumerate(s.upper()):
        g = F.get(ch, F[" "])  # unknown characters render as a blank cell
        for r, row in enumerate(g):
            for c, bit in enumerate(row):
                if bit == "1":
                    x = x0 + (i * 6 + c) * pitch
                    y = y0 + r * pitch
                    parts.append(f"M{x:g} {y:g}h0")
    return "".join(parts)


def led_text(s, cx, y0, pitch, color, cls="", dot=None, anchor="middle"):
    dot = dot or pitch * 0.72
    w = (text_cols(s) - 1) * pitch
    x0 = cx - w / 2 if anchor == "middle" else cx
    d = led_path(s, x0, y0, pitch)
    return (f'<path class="{cls}" d="{d}" stroke="{color}" stroke-width="{dot:g}" '
            f'stroke-linecap="round" fill="none"/>')


def unlit_grid(x, y, w, h, pitch, color, pid):
    r = pitch * 0.36
    return (f'<pattern id="{pid}" x="{x - pitch / 2:g}" y="{y - pitch / 2:g}" width="{pitch:g}" height="{pitch:g}" '
            f'patternUnits="userSpaceOnUse"><circle cx="{pitch / 2:g}" cy="{pitch / 2:g}" r="{r:g}" fill="{color}"/></pattern>',
            f'<rect x="{x - pitch / 2:g}" y="{y - pitch / 2:g}" width="{w:g}" height="{h:g}" fill="url(#{pid})"/>')


# ---------------------------------------------------------------- banner.svg
def banner():
    """Stadium 'lights on' intro: blackout, floodlights bang on bank by bank,
    the LED name slams onto the board with a red flash, then the crowd keeps
    flashing cameras. Final state is the base style, so a paused or
    non-animating viewer still sees the finished banner."""
    import random
    W, H = 1200, 420
    random.seed(11)
    T = 7  # intro length in seconds (plays once per page load)
    defs, body = [], []

    defs.append(f'''
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#020306"/><stop offset=".55" stop-color="#090D16"/><stop offset="1" stop-color="#14070A"/>
</linearGradient>
<radialGradient id="bloom" cx=".5" cy=".5" r=".5">
  <stop offset="0" stop-color="#FFFFFF"/><stop offset=".25" stop-color="#FFF4D8" stop-opacity=".9"/><stop offset="1" stop-color="#FFF4D8" stop-opacity="0"/>
</radialGradient>
<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#FFF6DD" stop-opacity=".42"/><stop offset=".7" stop-color="#FFF6DD" stop-opacity=".06"/><stop offset="1" stop-color="#FFF6DD" stop-opacity="0"/>
</linearGradient>
<radialGradient id="redglow" cx=".5" cy=".5" r=".5">
  <stop offset="0" stop-color="{AMBER}" stop-opacity=".9"/><stop offset=".55" stop-color="{AMBER}" stop-opacity=".25"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="panel" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#0D1118"/><stop offset="1" stop-color="#04060A"/>
</linearGradient>
<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".18"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
</linearGradient>
<linearGradient id="grass" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#0F5A3A"/><stop offset="1" stop-color="#041A10"/>
</linearGradient>
<filter id="glow" x="-10%" y="-40%" width="120%" height="180%">
  <feGaussianBlur stdDeviation="4" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="softglow" x="-10%" y="-50%" width="120%" height="200%">
  <feGaussianBlur stdDeviation="1.6" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<clipPath id="screen"><rect x="160" y="96" width="880" height="214" rx="6"/></clipPath>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" opacity=".22"/></pattern>''')

    css = f'''
.blackout{{opacity:0;animation:bo {T}s ease-out}}
@keyframes bo{{0%,10%{{opacity:1}}20%{{opacity:.85}}30%{{opacity:.55}}42%,100%{{opacity:0}}}}
.bankL{{animation:bankL {T}s linear}}
@keyframes bankL{{0%,12%{{opacity:0}}12.5%{{opacity:1}}100%{{opacity:1}}}}
.bankR{{animation:bankR {T}s linear}}
@keyframes bankR{{0%,21%{{opacity:0}}21.5%{{opacity:1}}100%{{opacity:1}}}}
.bloomL{{opacity:0;animation:bloomL {T}s ease-out}}
@keyframes bloomL{{0%,12%{{opacity:0}}13%{{opacity:1}}24%,100%{{opacity:0}}}}
.bloomR{{opacity:0;animation:bloomR {T}s ease-out}}
@keyframes bloomR{{0%,21%{{opacity:0}}22%{{opacity:1}}33%,100%{{opacity:0}}}}
.board{{animation:board {T}s linear}}
@keyframes board{{0%,30%{{opacity:.15}}31%{{opacity:.6}}32%{{opacity:.2}}34%,100%{{opacity:1}}}}
.name{{transform-origin:600px 175px;animation:slam {T}s cubic-bezier(.2,1.6,.4,1)}}
@keyframes slam{{0%,44%{{opacity:0;transform:scale(1.6)}}45%{{opacity:1;transform:scale(1.25)}}52%,100%{{opacity:1;transform:scale(1)}}}}
.flash{{opacity:0;animation:flash {T}s ease-out}}
@keyframes flash{{0%,45%{{opacity:0}}46%{{opacity:.75}}60%,100%{{opacity:0}}}}
.sub{{animation:sub {T}s ease-out}}
@keyframes sub{{0%,55%{{opacity:0}}62%,100%{{opacity:1}}}}
.beam{{animation:flick 9s infinite}}
.beam.r{{animation-delay:-3.1s}}
@keyframes flick{{0%,100%{{opacity:1}}46%{{opacity:1}}47%{{opacity:.6}}48%{{opacity:1}}50%{{opacity:.75}}51%{{opacity:1}}}}
.cam{{opacity:0;animation:cam 4s infinite}}
@keyframes cam{{0%,94%,100%{{opacity:0}}95%{{opacity:1}}97%{{opacity:.3}}}}
.sweep{{animation:sweep 5s ease-in-out infinite}}
@keyframes sweep{{0%{{transform:translateX(-300px)}}60%,100%{{transform:translateX(1300px)}}}}
.live{{animation:blink 1.1s steps(2,start) infinite}}
@keyframes blink{{to{{visibility:hidden}}}}
.pulse{{animation:pulse 2.4s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}
'''

    body.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
    # stars
    body.append("".join(f'<circle cx="{random.randint(0, W)}" cy="{random.randint(0, 70)}" r="{random.choice([.6, .9])}" fill="#fff" opacity="{random.choice([.25, .45])}"/>' for _ in range(40)))

    # crowd bowl: two tiers of dim heads
    crowd = []
    for row in range(9):
        y = 150 + row * 13
        for x in range(4 + (row % 2) * 6, W, 12):
            crowd.append(f"M{x} {y}h0")
    body.append(f'<path d="M0 140 L1200 140 L1200 270 L0 270Z" fill="#0B0F17"/>')
    body.append(f'<path d="{"".join(crowd)}" stroke="#1C2230" stroke-width="7" stroke-linecap="round"/>')
    # camera flashes in the crowd
    flashes = []
    for _ in range(46):
        x = random.randint(10, W - 10)
        y = random.randint(146, 262)
        if 150 < x < 1050 and y < 320:  # mostly hidden behind the board; still nice at the edges
            if random.random() < .55:
                continue
        dur = random.choice([2.7, 3.3, 3.9, 4.6, 5.2, 6.1])
        flashes.append(f'<g class="cam" style="animation-duration:{dur}s;animation-delay:-{random.uniform(0, dur):.2f}s">'
                       f'<circle cx="{x}" cy="{y}" r="7" fill="url(#bloom)"/><circle cx="{x}" cy="{y}" r="1.8" fill="#fff"/></g>')
    body.append("".join(flashes))

    # floodlight beams (on after their bank ignites)
    body.append('<g class="bankL"><path class="beam" d="M70 40 L470 420 L170 420Z" fill="url(#beam)"/></g>')
    body.append('<g class="bankR"><path class="beam r" d="M1130 40 L1030 420 L730 420Z" fill="url(#beam)"/></g>')
    # towers
    for x, cls in ((70, "L"), (1130, "R")):
        lamps = "".join(f'<rect x="{-30 + c * 13}" y="{14 + r * 14}" width="10" height="10" rx="2" fill="#FFF6D6"/>'
                        for r in range(3) for c in range(5))
        body.append(f'<g transform="translate({x} 0)"><path d="M-3 60 L3 60 L7 {H} L-7 {H}Z" fill="#161C28"/>'
                    f'<rect x="-34" y="10" width="68" height="46" rx="3" fill="#161C28"/>'
                    f'<g fill="#3A3F4A">{lamps.replace("#FFF6D6", "#3A3F4A")}</g>'
                    f'<g class="bank{cls}">{lamps}</g>'
                    f'<circle class="bloom{cls}" cx="0" cy="33" r="160" fill="url(#bloom)"/></g>')

    # pitch
    body.append(f'<rect x="0" y="340" width="{W}" height="80" fill="url(#grass)"/>')
    for i in range(0, 12, 2):
        body.append(f'<rect x="{i * 100}" y="340" width="100" height="80" fill="#000" opacity=".12"/>')
    body.append(f'<rect x="0" y="340" width="{W}" height="2" fill="{CHALK}" opacity=".55"/>')
    body.append(f'<path d="M600 342 V420" stroke="{CHALK}" stroke-opacity=".45" stroke-width="2"/>')
    body.append(f'<ellipse cx="600" cy="420" rx="120" ry="34" fill="none" stroke="{CHALK}" stroke-opacity=".45" stroke-width="2"/>')
    body.append(f'<ellipse class="pulse" cx="600" cy="352" rx="520" ry="26" fill="url(#redglow)" opacity=".7"/>')

    # scoreboard
    board = []
    board.append(f'<ellipse class="pulse" cx="600" cy="205" rx="660" ry="210" fill="url(#redglow)"/>')
    board.append('<rect x="585" y="324" width="12" height="20" fill="#161C28"/><rect x="603" y="324" width="12" height="20" fill="#161C28"/>')
    board.append(f'<rect x="144" y="80" width="912" height="246" rx="14" fill="#141A24" stroke="#2A3445" stroke-width="2"/>')
    board.append(f'<rect x="160" y="96" width="880" height="214" rx="6" fill="url(#panel)"/>')
    for bx, by in ((156, 92), (1044, 92), (156, 314), (1044, 314)):
        board.append(f'<circle cx="{bx}" cy="{by}" r="3.5" fill="#3A4558"/>')
    g = []
    p_big = 9
    name = "ILIASS EL GUAARI"
    w_name = (text_cols(name) - 1) * p_big
    x0 = 600 - w_name / 2
    pat, rect = unlit_grid(x0, 148, w_name + p_big, 72, p_big, "#200A0D", "u1")
    defs.append(pat)
    g.append(rect)
    g.append(f'<g class="name"><g filter="url(#glow)">{led_text(name, 600, 156, p_big, AMBER, dot=8)}</g></g>')
    p_s = 3
    left, right = "OTTAWA, ON · EN / FR", "SUMMER 2027 CO-OP"
    g.append(f'<g filter="url(#softglow)">'
             f'{led_text(left, 180, 114, p_s, GREEN, anchor="start", dot=2.6)}'
             f'{led_text(right, 1020 - (text_cols(right) - 1) * p_s, 114, p_s, GREEN, anchor="start", dot=2.6)}</g>')
    g.append(f'<circle class="live" cx="596" cy="123" r="5" fill="#FF3B3B"/>')
    g.append(f'<g filter="url(#softglow)">{led_text("LIVE", 642, 114, p_s, "#F4F8F2", dot=2.6)}</g>')
    g.append('<rect x="176" y="250" width="848" height="1.5" fill="#2A3445"/>')
    g.append(f'<g class="sub" filter="url(#softglow)">{led_text("SOFTWARE ENGINEERING · UOTTAWA", 600, 264, 4.4, CHALK, dot=3.5)}</g>')
    g.append('<rect class="sweep" x="0" y="96" width="220" height="214" fill="url(#sweep)"/>')
    board.append(f'<g clip-path="url(#screen)">{"".join(g)}</g>')
    board.append('<rect x="160" y="96" width="880" height="214" rx="6" fill="url(#scan)"/>')
    body.append(f'<g class="board">{"".join(board)}</g>')

    # intro overlays
    body.append(f'<rect class="flash" width="{W}" height="{H}" fill="{AMBER}"/>')
    body.append(f'<rect class="blackout" width="{W}" height="{H}" fill="#000"/>')

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
           f'aria-label="Iliass El Guaari, Software Engineering at uOttawa, on a floodlit stadium scoreboard">'
           f'<defs>{"".join(defs)}</defs><style>{css}</style>{"".join(body)}</svg>')
    open(f"{OUT}/banner.svg", "w").write(svg)


# ---------------------------------------------------------------- ticker.svg
def ticker():
    W, H = 1200, 96
    msg = ("   *   OPEN TO A SUMMER 2027 SOFTWARE CO-OP   *   SOFTWARE ENGINEERING · UNIVERSITY OF OTTAWA"
           "   *   JAVA · PYTHON · JAVASCRIPT   *   PROJECTS: SCOUTIQ · TRIPPILOT AI   *   ENGLISH / FRENCH  ")
    p = 6
    w_msg = len(msg) * 6 * p
    y0 = (H - 6 * p) / 2
    d = led_path(msg, 0, y0, p)
    speed = 90  # px per second
    dur = w_msg / speed
    pat, rect = unlit_grid(p / 2, y0 - p * 2, W, 11 * p, p, "#1C0A0C", "ut")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Scrolling scoreboard ticker: open to a Summer 2027 software co-op">
<defs>{pat}
<filter id="g" x="-5%" y="-40%" width="110%" height="180%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#05070B"/><stop offset=".06" stop-color="#05070B" stop-opacity="0"/><stop offset=".94" stop-color="#05070B" stop-opacity="0"/><stop offset="1" stop-color="#05070B"/></linearGradient>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" opacity=".25"/></pattern>
</defs>
<style>.run{{animation:run {dur:.2f}s linear infinite}}@keyframes run{{to{{transform:translateX(-{w_msg}px)}}}}</style>
<rect width="{W}" height="{H}" rx="10" fill="#05070B"/>
{rect}
<g filter="url(#g)"><g class="run">
<path d="{d}" stroke="{AMBER}" stroke-width="{p * .74:g}" stroke-linecap="round" fill="none"/>
<path transform="translate({w_msg} 0)" d="{d}" stroke="{AMBER}" stroke-width="{p * .74:g}" stroke-linecap="round" fill="none"/>
</g></g>
<rect width="{W}" height="{H}" fill="url(#scan)"/>
<rect width="{W}" height="{H}" fill="url(#fade)"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="10" fill="none" stroke="#2A3445" stroke-width="2"/>
</svg>'''
    open(f"{OUT}/ticker.svg", "w").write(svg)


# ---------------------------------------------------------------- starting-xi.svg
def starting_xi():
    W, H = 1200, 700
    px0, py0, pw, ph = 60, 70, 1080, 540  # pitch rect
    # 4-3-3 attacking left→right. Order = ScoutIQ Formation.create433()
    # (GK, LB, CB1, CB2, RB, CM1, CM2, CAM, LW, ST, RW).
    xi = [
        ("GK", "GIT", 0.07, 0.50),
        ("LB", "HTML", 0.27, 0.14),
        ("CB", "JAVA", 0.24, 0.38),
        ("CB", "PYTHON", 0.24, 0.62),
        ("RB", "CSS", 0.27, 0.86),
        ("CM", "OOP", 0.50, 0.30),
        ("CM", "DSA", 0.50, 0.70),
        ("CAM", "JAVASCRIPT", 0.62, 0.50),
        ("LW", "STREAMLIT", 0.80, 0.16),
        ("ST", "OPENAI API", 0.86, 0.50),
        ("RW", "GITHUB", 0.80, 0.84),
    ]
    pts = [(px0 + fx * pw, py0 + fy * ph) for _, _, fx, fy in xi]
    step = 1.0
    cycle = step * (len(xi) + 3)  # 11 fills, shot, hold

    css = [f".p{{transform-box:fill-box;transform-origin:center}}"]
    for i in range(len(xi)):
        on = (i * step + 0.35) / cycle * 100
        off = (cycle - 0.4) / cycle * 100
        css.append(
            f"@keyframes f{i}{{0%,{on - 0.01:.2f}%{{fill:#0B1220;stroke:#F4F8F2}}"
            f"{on:.2f}%{{fill:{AMBER};stroke:{AMBER};transform:scale(1.35)}}"
            f"{on + 3:.2f}%,{off:.2f}%{{fill:{AMBER};stroke:{AMBER};transform:scale(1)}}"
            f"100%{{fill:#0B1220;stroke:#F4F8F2}}}}"
            f".p{i}{{animation:f{i} {cycle}s infinite}}"
            f"@keyframes t{i}{{0%,{on - 0.01:.2f}%{{fill:#9FB3A7}}{on:.2f}%,{off:.2f}%{{fill:#FFFFFF}}100%{{fill:#9FB3A7}}}}"
            f".t{i}{{animation:t{i} {cycle}s infinite}}"
        )
    goal_t = (len(xi) * step + 0.6) / cycle * 100
    css.append(f"@keyframes net{{0%,{goal_t:.2f}%{{opacity:0}}{goal_t + 1:.2f}%{{opacity:1}}{goal_t + 14:.2f}%{{opacity:1}}{goal_t + 16:.2f}%,100%{{opacity:0}}}}.goal{{animation:net {cycle}s infinite}}")
    css.append(f"@keyframes ripple{{0%,{goal_t:.2f}%{{transform:translateX(0)}}{goal_t + 2:.2f}%{{transform:translateX(10px)}}{goal_t + 5:.2f}%,100%{{transform:translateX(0)}}}}.netr{{animation:ripple {cycle}s infinite;transform-box:fill-box}}")

    # ball path through the 11 spots, then a shot into the goal
    goal = (px0 + pw + 18, py0 + ph / 2 - 20)
    path_pts = pts + [goal, goal]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in path_pts)
    seg = [math.dist(path_pts[i], path_pts[i + 1]) for i in range(len(path_pts) - 1)]
    total = sum(seg)
    # keyPoints at arrival of each node; time uniformly stepped per pass
    kp, kt, acc = ["0"], ["0"], 0
    for i, s in enumerate(seg[:-1]):
        acc += s
        kp.append(f"{acc / total:.4f}")
        kt.append(f"{min((i + 1) * step / cycle, 1):.4f}")
    kp.append("1")
    kt.append("1")
    # hold during the end: make last segment zero (goal->goal) so kp stays at goal

    stripes = "".join(
        f'<rect x="{px0 + i * pw / 12:.1f}" y="{py0}" width="{pw / 12 + .5:.1f}" height="{ph}" fill="{PITCH if i % 2 else PITCH2}"/>'
        for i in range(12))
    L = f'stroke="{CHALK}" stroke-opacity=".75" stroke-width="3" fill="none"'
    lines = (
        f'<rect x="{px0}" y="{py0}" width="{pw}" height="{ph}" {L}/>'
        f'<line x1="{px0 + pw / 2}" y1="{py0}" x2="{px0 + pw / 2}" y2="{py0 + ph}" {L}/>'
        f'<circle cx="{px0 + pw / 2}" cy="{py0 + ph / 2}" r="72" {L}/>'
        f'<circle cx="{px0 + pw / 2}" cy="{py0 + ph / 2}" r="4" fill="{CHALK}"/>'
        + "".join(
            f'<rect x="{x}" y="{py0 + ph / 2 - 160}" width="150" height="320" {L}/>'
            f'<rect x="{x2}" y="{py0 + ph / 2 - 75}" width="55" height="150" {L}/>'
            for x, x2 in ((px0, px0), (px0 + pw - 150, px0 + pw - 55)))
        + f'<rect x="{px0 - 18}" y="{py0 + ph / 2 - 45}" width="18" height="90" {L}/>'
        f'<g class="netr"><rect x="{px0 + pw}" y="{py0 + ph / 2 - 45}" width="18" height="90" {L}/>'
        f'<path d="' + "".join(f"M{px0 + pw} {py0 + ph / 2 - 45 + k * 15}h18" for k in range(1, 6)) + f'" stroke="{CHALK}" stroke-opacity=".35"/></g>'
    )
    # passing lane (dashed) in fill order
    lane = (f'<path d="M' + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) +
            f'" stroke="{AMBER}" stroke-opacity=".28" stroke-width="2" stroke-dasharray="6 8" fill="none"/>')
    players = []
    for i, ((pos, label, _, _), (x, y)) in enumerate(zip(xi, pts)):
        players.append(
            f'<g><circle class="p p{i}" cx="{x:.1f}" cy="{y:.1f}" r="27" fill="#0B1220" stroke="{CHALK}" stroke-width="3"/>'
            f'<text class="t{i}" x="{x:.1f}" y="{y + 6:.1f}" text-anchor="middle" font-size="17" font-weight="800" fill="#9FB3A7">{pos}</text>'
            f'<rect x="{x - (len(label) * 6.2 + 18) / 2:.1f}" y="{y + 34:.1f}" width="{len(label) * 6.2 + 18:.1f}" height="22" rx="4" fill="#06090F" fill-opacity=".82"/>'
            f'<text x="{x:.1f}" y="{y + 50:.1f}" text-anchor="middle" font-size="12" font-weight="700" letter-spacing="1" fill="{CHALK}">{label}</text></g>')
    ball = (f'<g><circle r="9" fill="#fff" stroke="#06090F" stroke-width="2"/>'
            f'<path d="M-3 -4l3-2 3 2-1 4h-4z" fill="#06090F"/>'
            f'<animateMotion dur="{cycle}s" repeatCount="indefinite" calcMode="linear" '
            f'keyPoints="{";".join(kp)}" keyTimes="{";".join(kt)}" path="{d}"/></g>')
    goal_txt = (f'<g class="goal"><rect x="{px0 + pw - 330}" y="{py0 + 14}" width="300" height="46" rx="6" fill="{AMBER}"/>'
                f'<text x="{px0 + pw - 180}" y="{py0 + 45}" text-anchor="middle" font-size="22" font-weight="900" letter-spacing="3" fill="#FFFFFF">GOAL · SHIPPED</text></g>')
    head = (f'<text x="{px0}" y="44" font-size="22" font-weight="900" letter-spacing="3" fill="{AMBER}">TECH STACK · 4-3-3</text>'
            f'<text x="{px0 + pw}" y="44" text-anchor="end" font-size="14" letter-spacing="1.5" fill="#9FB3A7">FILLED IN THE ORDER OF  Formation.create433()  FROM SCOUTIQ</text>')
    bench = (f'<text x="{px0}" y="{py0 + ph + 52}" font-size="15" font-weight="800" letter-spacing="2" fill="{AMBER}">ALSO IN THE SQUAD</text>'
             + "".join(
                 f'<g transform="translate({px0 + 270 + k * 195} {py0 + ph + 34})"><rect width="175" height="26" rx="13" fill="none" stroke="#9FB3A7" stroke-dasharray="4 4"/>'
                 f'<text x="87.5" y="18" text-anchor="middle" font-size="13" font-weight="700" letter-spacing="1.5" fill="{CHALK}">{n}</text></g>'
                 for k, n in enumerate(["SQL · POSTGRESQL", "SPRING", "REACT"])))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="My tech stack as a 4-3-3 starting eleven on a soccer pitch" font-family="'Segoe UI',Helvetica,Arial,sans-serif">
<style>{"".join(css)}</style>
<rect width="{W}" height="{H}" rx="14" fill="{NIGHT}"/>
{head}
{stripes}{lines}{lane}
{"".join(players)}
{ball}
{bench}
</svg>'''
    open(f"{OUT}/starting-xi.svg", "w").write(svg)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    banner()
    ticker()
    starting_xi()
    for f in ("banner.svg", "ticker.svg", "starting-xi.svg"):
        print(f, os.path.getsize(f"{OUT}/{f}"))
