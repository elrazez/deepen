#!/usr/bin/env python3
"""Generate assets/banner.svg: the four ambitions as a wireframe chart, read along depth.

After Felix Rieseberg's "How to be more ambitious: A tutorial for humans with models":
ambition with models comes in speed, altitude, depth and range. This skill is about depth,
working one level below the task's layer. The four planes under the task are the skill's four
questions. Each one is narrower and more detailed than the one above (deeper, not bigger). The
depth axis lands on the word.

Black and white, lines only. Stdlib only. CSS animations switch off under prefers-reduced-motion.

    python3 scripts/banner.py
"""
import pathlib

W, H = 1200, 800
OX, OY = 420, 272          # origin: the task's layer
LEVEL_GAP = 70
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
FG, MID, DIM, FAINT, BG = "#f5f5f5", "#a3a3a3", "#5c5c5c", "#262626", "#0a0a0a"

GLYPHS = {  # 5 wide; rows 0-2 ascender, 3-7 x-height, 8-9 descender
    "d": ["....#", "....#", "....#", ".####", "#...#", "#...#", "#...#", ".####", ".....", "....."],
    "e": [".....", ".....", ".....", ".###.", "#...#", "#####", "#....", ".####", ".....", "....."],
    "p": [".....", ".....", ".....", "####.", "#...#", "#...#", "#...#", "####.", "#....", "#...."],
    "n": [".....", ".....", ".....", "####.", "#...#", "#...#", "#...#", "#...#", ".....", "....."],
}
QUESTIONS = ["what a top pro would do", "the rawest material", "the instruments they use", "an outside judge"]
# (half-range, grid lines): each level is narrower but denser than the one above
LEVELS = [(250, 5), (190, 7), (150, 9), (116, 11), (86, 13)]
SPEED = (52, -22)  # half-vector of the speed direction (drawn going back, up-right)


def L(x1, y1, x2, y2, stroke=MID, w=1, extra=""):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" '
            f'stroke-width="{w}" {extra}/>')


def T(x, y, s, size=13, fill=MID, anchor="start", extra=""):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>'


def plane(cy, half, n, stroke, cls=""):
    """Wireframe parallelogram in the range x speed plane, centred on the depth axis.

    Corners: 0 front-left, 1 front-right, 2 back-right, 3 back-left.
    """
    sx, sy = SPEED
    c = [(OX - half - sx, cy - sy), (OX + half - sx, cy - sy), (OX + half + sx, cy + sy), (OX - half + sx, cy + sy)]
    out = [f'<g class="{cls}">', f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in c)}" fill="none" '
           f'stroke="{stroke}" stroke-width="1.2"/>']
    for k in range(1, n):  # lines along range
        t = k / n
        p = (c[0][0] + (c[3][0] - c[0][0]) * t, c[0][1] + (c[3][1] - c[0][1]) * t)
        q = (c[1][0] + (c[2][0] - c[1][0]) * t, c[1][1] + (c[2][1] - c[1][1]) * t)
        out.append(L(*p, *q, stroke, .6, 'stroke-opacity=".55"'))
    for k in range(1, n * 2):  # lines along speed
        t = k / (n * 2)
        p = (c[0][0] + (c[1][0] - c[0][0]) * t, c[0][1])
        q = (c[3][0] + (c[2][0] - c[3][0]) * t, c[3][1])
        out.append(L(*p, *q, stroke, .6, 'stroke-opacity=".55"'))
    out.append("</g>")
    return "".join(out), c


def scanline_word(x0, y0, px, step, stair):
    """The word as horizontal scanlines: three lines per pixel row, plus a dim offset echo."""
    face, echo = [], []
    for i, ch in enumerate("deepen"):
        gx, gy = x0 + i * step, y0 + i * stair
        for r, row in enumerate(GLYPHS[ch]):
            c = 0
            while c < 5:
                if row[c] != "#":
                    c += 1
                    continue
                e = c
                while e + 1 < 5 and row[e + 1] == "#":
                    e += 1
                xa, xb = gx + c * px, gx + (e + 1) * px - 2
                for off in (1.5, 5, 8.5):
                    y = gy + r * px + off
                    face.append(L(xa, y, xb, y, FG, 1.6))
                    echo.append(L(xa + 3, y + 3, xb + 3, y + 3, "#333333", 1.1))
                c = e + 1
    return "".join(echo), "".join(face)


def build():
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
      f'aria-labelledby="t d">')
    a('<title id="t">deepen</title>')
    a('<desc id="d">A terminal drawing of four axes of ambition: altitude, range, speed and depth. Below the '
      "task's layer, four narrower but more detailed planes mark the questions: what a top pro would do, the "
      'rawest material, the instruments they use, an outside judge. The depth axis lands on the word deepen. '
      'On the right, the 12-line prompt you get back.</desc>')
    a(f"""<defs>
<pattern id="crt" width="4" height="4" patternUnits="userSpaceOnUse"><line x1="0" y1="0.5" x2="4" y2="0.5" stroke="#ffffff" stroke-opacity=".035"/></pattern>
<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10" fill="none" stroke="{MID}" stroke-width="1.5"/></marker>
<marker id="arrowFG" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10" fill="none" stroke="{FG}" stroke-width="1.8"/></marker>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="12"/></clipPath>
</defs>
<style>
text{{font-family:{MONO}}}
.cursor{{animation:blink 1.1s steps(1) infinite}} @keyframes blink{{50%{{opacity:0}}}}
.scan{{animation:scan 3.2s linear infinite}} @keyframes scan{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-400}}}}
.lvl{{animation:lvl 5s ease-in-out infinite;opacity:.7}} @keyframes lvl{{0%,100%{{opacity:.7}}10%{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.lvl{{opacity:.9}}}}
</style>""")
    a('<g clip-path="url(#frame)">')
    a(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    a('<g fill="#ffffff" fill-opacity=".06">' + "".join(  # faint dot grid
        f'<circle cx="{x}" cy="{y}" r=".8"/>' for x in range(30, W, 30) for y in range(60, H - 40, 30)) + "</g>")
    # terminal chrome
    a(f'<rect width="{W}" height="36" fill="#111111"/>{L(0, 36, W, 36, FAINT)}')
    for cx in (22, 42, 62):
        a(f'<circle cx="{cx}" cy="18" r="5.5" fill="none" stroke="{DIM}" stroke-width="1.2"/>')
    a(T(W / 2, 23, "elrazez/deepen — zsh — 120×40", 12, DIM, "middle"))
    a(T(36, 78, f'<tspan fill="{DIM}">~/project</tspan> <tspan fill="{FG}">❯</tspan> '
                f'<tspan fill="{FG}" font-weight="700">/deepen</tspan> <tspan fill="{MID}">make the page faster</tspan>',
        15))
    a(f'<rect class="cursor" x="400" y="65" width="9" height="17" fill="{FG}"/>')

    # ---- the chart ----
    a(L(OX, OY, OX, 128, MID, 1.2, 'marker-end="url(#arrow)"'))  # altitude, up
    for y in range(OY - 24, 140, -24):
        a(L(OX - 4, y, OX + 4, y, DIM))
    a(T(OX, 112, "altitude", 13, MID, "middle") + T(OX + 40, 112, "· the goal beyond the goal", 11, DIM))
    a(L(OX - 300, OY, OX + 300, OY, MID, 1.2, 'marker-start="url(#arrow)" marker-end="url(#arrow)"'))  # range
    for x in range(OX - 276, OX + 300, 24):
        if x != OX:
            a(L(x, OY - 3, x, OY + 3, DIM))
    a(T(OX - 312, OY + 5, "range", 13, MID, "end"))
    a(T(OX + 312, OY + 5, "range", 13, MID) + T(OX + 312, OY + 21, "other fields", 11, DIM))
    sx, sy = SPEED  # speed, going back
    a(L(OX, OY, OX + sx * 3.4, OY + sy * 3.4, MID, 1.1, 'stroke-dasharray="4 4" marker-end="url(#arrow)"'))
    a(T(OX + sx * 3.4 + 8, OY + sy * 3.4 - 6, "speed", 13, MID) +
      T(OX + sx * 3.4 + 8, OY + sy * 3.4 + 9, "same work, less time", 11, DIM))
    # the task's layer, then four deeper planes
    g, c0 = plane(OY, LEVELS[0][0], LEVELS[0][1], DIM)
    a(g)
    a(T(c0[0][0], c0[0][1] + 18, "lvl 0 · task's layer", 12, MID))
    depth_end = OY + LEVEL_GAP * 4 + 58
    a(L(OX, OY, OX, depth_end, FG, 2, 'marker-end="url(#arrowFG)"'))  # depth axis
    a(L(OX, OY, OX, depth_end - 8, FG, 3, 'stroke-dasharray="26 374" stroke-linecap="round" class="scan"'))
    col = OX + 270
    for i, q in enumerate(QUESTIONS):
        cy = OY + LEVEL_GAP * (i + 1)
        half, n = LEVELS[i + 1]
        shade = ["#8a8a8a", "#b0b0b0", "#d4d4d4", FG][i]
        g, c = plane(cy, half, n, shade, "lvl")
        a(g.replace('class="lvl"', f'class="lvl" style="animation-delay:{.5 + i * .55:.2f}s"', 1))
        right = c[2]  # right-most corner
        a(L(right[0] + 8, cy, col - 12, cy, DIM, 1, 'stroke-dasharray="1 4"'))
        a(T(col, cy + 5, f'<tspan fill="{FG}" font-weight="700">0{i + 1}</tspan>  <tspan fill="{shade}">{q}</tspan>', 15))
        a(T(OX - 8, cy - 26, f"−{i + 1}", 11, DIM, "end"))
    a(T(OX + 14, depth_end - 4, "depth", 13, FG, "start", 'font-weight="700"') +
      T(OX + 62, depth_end - 4, "· how a field-leading expert would do it", 11, MID))

    # the word, at the end of the depth axis; the d's stem sits on the axis
    px = 11
    echo, face = scanline_word(OX - (4 * px + (px - 2) / 2), depth_end + 18, px, 66, 4)
    a(f"<g>{echo}</g><g>{face}</g>")

    # ---- the prompt you get back ----
    bx, by, bw, bh = 952, 140, 218, 262
    a(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" fill="{BG}" stroke="{DIM}" stroke-width="1.2"/>')
    a(L(bx, by + 28, bx + bw, by + 28, FAINT))
    for cx in (bx + 15, bx + 29, bx + 43):
        a(f'<circle cx="{cx}" cy="{by + 14}" r="4" fill="none" stroke="{DIM}"/>')
    a(T(bx + bw - 12, by + 18, "deeper.prompt", 11, DIM, "end"))
    lens = [.92, .78, .86, .6, .95, .7, .83, .55, .9, .74, .66, .4]
    for k, ln in enumerate(lens):
        y = by + 48 + k * 17.5
        hot = k in (0, 3, 6, 10)
        a(T(bx + 24, y + 4, f"{k + 1}", 10, DIM, "end"))
        a(L(bx + 34, y, bx + 34 + ln * (bw - 50), y, FG if hot else DIM, 2.2 if hot else 1.6, 'stroke-linecap="round"'))
    a(T(bx + bw / 2, by + bh + 24, "what you get back · ≤ 12 lines", 12, MID, "middle"))
    yb = OY + LEVEL_GAP * 4 + 28  # flow: down the depth axis, back up as a prompt
    a(f'<polyline points="{OX + 110},{yb} {bx + 40},{yb} {bx + 40},{by + bh + 40}" fill="none" stroke="{DIM}" '
      f'stroke-dasharray="3 5" marker-end="url(#arrow)"/>')
    a(T(bx + 30, yb - 10, "rewrite", 11, DIM, "end"))

    a(T(W - 30, H - 48, "axes after Felix Rieseberg · “How to be more ambitious”", 11, DIM, "end"))
    # status bar
    a(f'<rect y="{H - 30}" width="{W}" height="30" fill="#141414"/>{L(0, H - 30, W, H - 30, FAINT)}')
    a(f'<rect y="{H - 30}" width="96" height="30" fill="{FG}"/>')
    a(T(48, H - 10, "DEEPEN", 12, BG, "middle", 'font-weight="700" letter-spacing="1.5"'))
    a(T(112, H - 10, "4 levels · each narrower, more detailed · deeper, not bigger", 12, MID))
    a(T(W - 16, H - 10, "skills/deepen/SKILL.md   utf-8   ln 12", 12, DIM, "end"))
    a(f'<rect width="{W}" height="{H}" fill="url(#crt)"/>')
    a("</g>")
    a(f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="12" fill="none" stroke="#2a2a2a" '
      f'stroke-width="1.5"/>')
    a("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    out = pathlib.Path(__file__).resolve().parent.parent / "assets" / "banner.svg"
    out.parent.mkdir(exist_ok=True)
    out.write_text(build() + "\n", encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes)")
