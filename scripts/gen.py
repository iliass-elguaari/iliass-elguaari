"""Generates the animated SVG assets for iliass-elguaari's profile README.

Theme: red circuit board. Traces, a chip with the name on it, and the core
stack drawn as the chip's pinout. Run: python3 scripts/gen.py assets
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
    """Red circuit board: traces draw themselves in from the edges, the chip
    powers on, the name glitches in, then data pulses keep flowing into the
    chip. Base styles are the finished state, so a viewer that doesn't
    animate still shows the full banner."""
    import random
    random.seed(4)
    W, H = 1200, 420
    T = 6
    CX0, CX1, CY0, CY1 = 280, 920, 118, 302  # chip body
    RED_HI = "#FF6B75"
    defs, body = [], []

    defs.append(f'''
<radialGradient id="bg" cx=".5" cy=".45" r=".75">
  <stop offset="0" stop-color="#140A0D"/><stop offset=".6" stop-color="#08080C"/><stop offset="1" stop-color="#040406"/>
</radialGradient>
<pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="1" fill="#1B1D26"/></pattern>
<radialGradient id="halo" cx=".5" cy=".5" r=".5">
  <stop offset="0" stop-color="{AMBER}" stop-opacity=".55"/><stop offset=".6" stop-color="{AMBER}" stop-opacity=".12"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="chip" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#15171E"/><stop offset="1" stop-color="#0A0B10"/>
</linearGradient>
<filter id="glow" x="-20%" y="-60%" width="140%" height="220%">
  <feGaussianBlur stdDeviation="3.5" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="tglow" x="-5%" y="-5%" width="110%" height="110%">
  <feGaussianBlur stdDeviation="2" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>''')

    css = f'''
.blackout{{opacity:0;animation:bo {T}s linear}}
@keyframes bo{{0%,6%{{opacity:1}}14%,100%{{opacity:0}}}}
.draw{{stroke-dasharray:1;stroke-dashoffset:0;animation:draw {T}s cubic-bezier(.6,0,.3,1)}}
@keyframes draw{{0%,8%{{stroke-dashoffset:1}}42%,100%{{stroke-dashoffset:0}}}}
.via{{animation:via {T}s linear}}
@keyframes via{{0%,10%{{opacity:0}}16%,100%{{opacity:1}}}}
.chipon{{animation:chipon {T}s linear}}
@keyframes chipon{{0%,40%{{opacity:.15}}43%{{opacity:1}}45%{{opacity:.3}}48%,100%{{opacity:1}}}}
.halo{{animation:halo 3s ease-in-out infinite}}
@keyframes halo{{0%,100%{{opacity:.65}}50%{{opacity:1}}}}
.flash{{opacity:0;animation:flash {T}s ease-out}}
@keyframes flash{{0%,47%{{opacity:0}}48%{{opacity:.55}}62%,100%{{opacity:0}}}}
.name{{animation:nm {T}s steps(1,end)}}
@keyframes nm{{0%,47%{{opacity:0}}48%{{opacity:1;transform:translate(-14px,0)}}50%{{transform:translate(9px,-3px)}}52%{{opacity:.3;transform:translate(-4px,2px)}}54%{{opacity:1;transform:translate(3px,0)}}56%,100%{{opacity:1;transform:translate(0,0)}}}}
.ghostA{{opacity:0;animation:ga {T}s steps(1,end)}}
@keyframes ga{{0%,47%{{opacity:0}}48%{{opacity:.8;transform:translate(10px,-2px)}}51%{{transform:translate(-8px,3px)}}54%{{opacity:.6;transform:translate(5px,0)}}57%,100%{{opacity:0}}}}
.ghostB{{opacity:0;animation:gb {T}s steps(1,end)}}
@keyframes gb{{0%,47%{{opacity:0}}48%{{opacity:.7;transform:translate(-12px,3px)}}51%{{transform:translate(7px,-2px)}}54%{{opacity:.5;transform:translate(-3px,0)}}57%,100%{{opacity:0}}}}
.late{{animation:late {T}s ease-out}}
@keyframes late{{0%,56%{{opacity:0}}66%,100%{{opacity:1}}}}
.pulse{{stroke-dasharray:.06 .94;animation:pulse 2.6s linear infinite}}
@keyframes pulse{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-1}}}}
.glitch{{animation:glitch 7s steps(1,end) infinite}}
@keyframes glitch{{0%,93%,100%{{transform:translate(0,0)}}94%{{transform:translate(6px,0)}}95%{{transform:translate(-4px,1px)}}96%{{transform:translate(2px,0)}}}}
.blink{{animation:blink 1.1s steps(2,start) infinite}}
@keyframes blink{{to{{visibility:hidden}}}}
'''

    body.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    body.append(f'<rect width="{W}" height="{H}" fill="url(#dots)"/>')
    body.append(f'<ellipse class="halo" cx="600" cy="210" rx="520" ry="230" fill="url(#halo)"/>')

    # ------------------------------------------------ traces (edge -> chip pin)
    traces, vias = [], []

    def route_vertical(px, top):
        sgn = -1 if top else 1
        y_pin = CY0 if top else CY1
        side = 1 if px > 600 else -1
        k = abs(px - 600) / 300
        y1 = y_pin + sgn * (16 + 10 * k)
        shift = side * (20 + 70 * k)
        y2 = y1 + sgn * abs(shift)
        x2 = px + shift
        end_y = -10 if top else H + 10
        if random.random() < .35:  # stop at a via instead of the edge
            end_y = (random.randint(18, 45) if top else random.randint(H - 50, H - 18))
            vias.append((x2, end_y))
        return f"M{x2:.0f} {end_y} L{x2:.0f} {y2:.0f} L{px:.0f} {y1:.0f} L{px:.0f} {y_pin}"

    def route_horizontal(py, left):
        sgn = -1 if left else 1
        x_pin = CX0 if left else CX1
        side = 1 if py > 210 else -1
        k = abs(py - 210) / 90
        x1 = x_pin + sgn * (18 + 14 * k)
        shift = side * (14 + 40 * k)
        x2 = x1 + sgn * abs(shift)
        y2 = py + shift
        end_x = -10 if left else W + 10
        if random.random() < .3:
            end_x = (random.randint(120, 220) if left else random.randint(W - 220, W - 120))
            vias.append((end_x, y2))
        return f"M{end_x} {y2:.0f} L{x2:.0f} {y2:.0f} L{x1:.0f} {py:.0f} L{x_pin} {py:.0f}"

    pins = []
    for px in range(CX0 + 40, CX1 - 20, 40):
        traces.append(route_vertical(px, True)); pins.append((px, CY0, "v"))
        traces.append(route_vertical(px, False)); pins.append((px, CY1, "v"))
    for py in range(CY0 + 26, CY1 - 10, 26):
        traces.append(route_horizontal(py, True)); pins.append((CX0, py, "h"))
        traces.append(route_horizontal(py, False)); pins.append((CX1, py, "h"))

    tr = []
    for i, d in enumerate(traces):
        tr.append(f'<path class="draw" pathLength="1" d="{d}" stroke="#6B1520" stroke-width="3" fill="none" stroke-linejoin="round"/>')
    body.append(f'<g>{"".join(tr)}</g>')
    pulses = []
    for i, d in enumerate(traces):
        if random.random() < .55:
            dur = random.choice([1.8, 2.2, 2.6, 3.1, 3.7, 4.4])
            pulses.append(f'<path class="pulse" pathLength="1" d="{d}" stroke="{RED_HI}" stroke-width="3" fill="none" '
                          f'stroke-linecap="round" style="animation-duration:{dur}s;animation-delay:-{random.uniform(0, dur):.2f}s"/>')
    body.append(f'<g class="late" filter="url(#tglow)">{"".join(pulses)}</g>')
    body.append('<g class="via">' + "".join(
        f'<circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="#08080C" stroke="#7A1A24" stroke-width="3"/>' for x, y in vias) + '</g>')

    # ------------------------------------------------ chip
    chip = []
    for x, y, o in pins:
        if o == "v":
            chip.append(f'<rect x="{x - 6}" y="{y - (10 if y == CY0 else 0)}" width="12" height="10" fill="#9AA0AA"/>')
        else:
            chip.append(f'<rect x="{x - (10 if x == CX0 else 0)}" y="{y - 6}" width="10" height="12" fill="#9AA0AA"/>')
    chip.append(f'<rect x="{CX0}" y="{CY0}" width="{CX1 - CX0}" height="{CY1 - CY0}" rx="10" fill="url(#chip)" stroke="#2A2E3A" stroke-width="2"/>')
    chip.append(f'<circle cx="{CX0 + 22}" cy="{CY0 + 22}" r="6" fill="#20232D"/>')
    body.append(f'<g class="chipon">{"".join(chip)}</g>')

    name = "ILIASS EL GUAARI"
    p = 6
    def name_path(color, cls):
        d = led_path(name, 600 - (text_cols(name) - 1) * p / 2, 168, p)
        return (f'<path class="{cls}" d="{d}" stroke="{color}" stroke-width="{p * .82:g}" '
                f'stroke-linecap="square" fill="none"/>')
    body.append(f'<g class="ghostA">{name_path("#FFFFFF", "")}</g>')
    body.append(f'<g class="ghostB">{name_path("#00E5FF", "")}</g>')
    body.append(f'<g class="name"><g class="glitch" filter="url(#glow)">{name_path(AMBER, "")}</g></g>')

    small = 2.6
    top = "U1 · ILIASS-ELGUAARI · REV 2026"
    sub = "SOFTWARE ENGINEERING · UOTTAWA"
    body.append(f'<g class="late">'
                f'{led_text(top, 600, 136, small, "#8A93A6", dot=2.2)}'
                f'<circle class="blink" cx="{CX1 - 26}" cy="{CY0 + 22}" r="5" fill="{AMBER}"/>'
                f'<g filter="url(#tglow)">{led_text(sub, 600, 252, 3, CHALK, dot=2.6)}</g>'
                f'</g>')
    # silkscreen labels on the board
    body.append(f'<g class="late">'
                f'{led_text("OTTAWA, ON · EN / FR", 34, H - 34, 2.4, "#6E7688", anchor="start", dot=2)}'
                f'{led_text("SUMMER 2027 INTERNSHIP", W - 34 - (text_cols("SUMMER 2027 INTERNSHIP") - 1) * 2.4, H - 34, 2.4, AMBER, anchor="start", dot=2)}'
                f'</g>')

    body.append(f'<rect class="flash" width="{W}" height="{H}" fill="{AMBER}"/>')
    body.append(f'<rect class="blackout" width="{W}" height="{H}" fill="#000"/>')

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
           f'aria-label="Iliass El Guaari, Software Engineering at uOttawa, on a red circuit board">'
           f'<defs>{"".join(defs)}</defs><style>{css}</style>{"".join(body)}</svg>')
    open(f"{OUT}/banner.svg", "w").write(svg)


# ---------------------------------------------------------------- ticker.svg
def ticker():
    W, H = 1200, 96
    msg = ("   *   NOW: FULL-STACK DEVELOPER · NEXT ROOM INC.   *   OPEN TO A SUMMER 2027 SOFTWARE INTERNSHIP"
           "   *   INCOMING SOFTWARE ENGINEER · STATISTICS CANADA"
           "   *   SOFTWARE ENGINEERING · UNIVERSITY OF OTTAWA   *   JAVA · PYTHON · SPRING · POSTGRESQL"
           "   *   PROJECTS: SCOUTIQ · TRIPPILOT AI · LISTINGS API   *   ENGLISH / FRENCH  ")
    p = 6
    w_msg = len(msg) * 6 * p
    y0 = (H - 6 * p) / 2
    d = led_path(msg, 0, y0, p)
    speed = 90  # px per second
    dur = w_msg / speed
    pat, rect = unlit_grid(p / 2, y0 - p * 2, W, 11 * p, p, "#1C0A0C", "ut")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Scrolling LED ticker: Software Developer at Next Room Inc., open to a Summer 2027 software internship">
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


# ---------------------------------------------------------------- stack.svg
def stack_board():
    """Reactor: a pulsing red core with the name on it and three counter-
    rotating rings of skills orbiting it. Labels counter-rotate so they
    stay upright. Energy bolts fire from the core."""
    import random
    random.seed(9)
    W, H = 1200, 700
    cx, cy = 600, 350
    rings = [
        ((215, 118), 26, 1, ["JAVA", "PYTHON", "JAVASCRIPT", "C", "C++", "SQL"]),
        ((375, 196), 40, -1, ["SPRING", "POSTGRESQL", "STREAMLIT", "OPENAI API", "ANDROID", "REACT"]),
        ((530, 272), 56, 1, ["GIT", "GITHUB", "INTELLIJ", "VS CODE", "BASH", "HTML / CSS", "DOCKER"]),
    ]
    parts = []
    # backdrop grid + rays
    rays = "".join(
        f'<line x1="{cx}" y1="{cy}" x2="{cx + 700 * math.cos(math.radians(a)):.0f}" y2="{cy + 700 * math.sin(math.radians(a)):.0f}" '
        f'stroke="{AMBER}" stroke-opacity=".07" stroke-width="2"/>' for a in range(0, 360, 15))
    parts.append(f'<g class="spin" style="animation-duration:120s">{rays}</g>')

    for ri, (r, dur, direction, names) in enumerate(rings):
        rx, ry = r
        ell = f"M{cx + rx} {cy} A{rx} {ry} 0 1 1 {cx - rx} {cy} A{rx} {ry} 0 1 1 {cx + rx} {cy}"
        kp = 'keyPoints="0;1"' if direction > 0 else 'keyPoints="1;0"'
        track = (f'<path class="flow" d="{ell}" fill="none" stroke="{AMBER}" stroke-opacity=".45" stroke-width="2" '
                 f'stroke-dasharray="2 9" style="animation-duration:{dur / 4:.1f}s;animation-direction:{"normal" if direction > 0 else "reverse"}"/>')
        comet = (f'<g><animateMotion dur="{dur / 1.6:.1f}s" repeatCount="indefinite" {kp} keyTimes="0;1" calcMode="linear" path="{ell}"/>'
                 f'<circle r="9" fill="url(#coreglow)"/><circle r="4" fill="#FFFFFF" filter="url(#glow)"/></g>')
        labels = []
        for k, nm in enumerate(names):
            phase = (k / len(names) + ri * .07) % 1
            w = len(nm) * 9.2 + 26
            labels.append(
                f'<g><animateMotion dur="{dur}s" begin="-{phase * dur:.2f}s" repeatCount="indefinite" {kp} keyTimes="0;1" calcMode="linear" path="{ell}"/>'
                f'<rect x="{-w / 2:.1f}" y="-15" width="{w:.1f}" height="30" rx="15" fill="#0B0C11" stroke="{AMBER}" stroke-width="2"/>'
                f'<text y="5" text-anchor="middle" font-size="13" font-weight="800" letter-spacing="2" fill="#FFFFFF">{nm}</text></g>')
        parts.append(track + comet + "".join(labels))

    # energy bolts from the core to random points
    bolts = []
    for i in range(7):
        a = random.uniform(0, 2 * math.pi)
        pts = [(cx + 70 * math.cos(a), cy + 70 * math.sin(a))]
        rr = 70
        while rr < 240:
            rr += random.uniform(25, 45)
            aa = a + random.uniform(-.12, .12)
            pts.append((cx + rr * math.cos(aa), cy + rr * math.sin(aa)))
        d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts)
        dur = random.choice([2.3, 2.9, 3.4, 4.1, 4.7])
        bolts.append(f'<path class="bolt" d="{d}" stroke="#FFD6DA" stroke-width="2.2" fill="none" filter="url(#glow)" '
                     f'style="animation-duration:{dur}s;animation-delay:-{random.uniform(0, dur):.2f}s"/>')
    parts.insert(1, "".join(bolts))

    # core
    core = (f'<circle class="pulse" cx="{cx}" cy="{cy}" r="190" fill="url(#coreglow)"/>'
            f'<circle cx="{cx}" cy="{cy}" r="78" fill="#120407" stroke="{AMBER}" stroke-width="3"/>'
            f'<circle cx="{cx}" cy="{cy}" r="66" fill="none" stroke="{AMBER}" stroke-opacity=".5" stroke-width="1.5" stroke-dasharray="4 6">'
            f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="-360 {cx} {cy}" dur="12s" repeatCount="indefinite"/></circle>'
            f'<g filter="url(#glow)">{led_text("IEG", cx, cy - 20, 6, AMBER, dot=5)}</g>'
            f'{led_text("CORE ONLINE", cx, cy + 34, 2, "#FFB3BA", dot=1.7)}')
    parts.append(core)

    head = (f'<text x="40" y="44" font-size="22" font-weight="900" letter-spacing="3" fill="{AMBER}">STACK REACTOR</text>'
            f'<text x="{W - 40}" y="44" text-anchor="end" font-size="13" letter-spacing="1.5" fill="#6E7688">INNER: LANGUAGES · MIDDLE: FRAMEWORKS &amp; DATA · OUTER: TOOLS</text>')
    css = (".spin{transform-origin:600px 350px;animation:spin 120s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}"
           ".pulse{animation:pulse 2.2s ease-in-out infinite}@keyframes pulse{0%,100%{opacity:.65}50%{opacity:1}}"
           ".flow{animation:flow 10s linear infinite}@keyframes flow{to{stroke-dashoffset:-110}}"
           ".bolt{opacity:0;animation:bolt 3s steps(1,end) infinite}@keyframes bolt{0%,88%,100%{opacity:0}89%{opacity:1}91%{opacity:.2}92%{opacity:.9}94%{opacity:0}}")
    trails = "".join(
        f'<linearGradient id="trail{i}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></linearGradient>'
        for i in range(3))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="My tech stack as rings of skills orbiting a glowing red reactor core" font-family="'Segoe UI',Helvetica,Arial,sans-serif">
<defs>
<radialGradient id="bg" cx=".5" cy=".5" r=".7"><stop offset="0" stop-color="#1A070B"/><stop offset=".55" stop-color="#08080C"/><stop offset="1" stop-color="#040406"/></radialGradient>
<pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="1" fill="#1B1D26"/></pattern>
<radialGradient id="coreglow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FF6B75" stop-opacity=".95"/><stop offset=".45" stop-color="{AMBER}" stop-opacity=".45"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
{trails}
</defs>
<style>{css}</style>
<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>
<rect width="{W}" height="{H}" rx="14" fill="url(#dots)"/>
{head}
{"".join(parts)}
</svg>'''
    open(f"{OUT}/stack.svg", "w").write(svg)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    banner()
    ticker()
    stack_board()
    for f in ("banner.svg", "ticker.svg", "stack.svg"):
        print(f, os.path.getsize(f"{OUT}/{f}"))
