"""Unidad 3 en estilo pizarra blanca dibujada a mano.

Motor: cada capítulo es una composición con un SVG de 1080×1920. Los
trazos se dibujan con stroke-dashoffset y una mano con marcador sigue
la punta del trazo (puntos muestreados con svgpathtools). Los textos se
revelan de izquierda a derecha detrás de la mano. Entre ideas, la mano
pasa el borrador. Los tiempos salen de tiempos.json (segundos absolutos).
"""
import json
from pathlib import Path

from PIL import ImageFont
from svgpathtools import parse_path

BASE = Path(__file__).parent
OUT = BASE / "proyecto"
FONT = str(OUT / "assets/fonts/PatrickHand-Regular.ttf")
TT = {x["n"]: (x["ini"], x["fin"]) for x in json.loads((BASE / "tiempos.json").read_text())}
TOTAL = round(TT[max(TT)][1] + 1.8, 2)
K, B, R = "#222222", "#1e6fd9", "#e03b3b"
REST = (1260, 1560)


def L(n):
    return TT[n][0]


def W(n, f):
    a, b = TT[n]
    return round(a + (b - a) * f, 2)


_fonts = {}


def tw(txt, size):
    if size not in _fonts:
        _fonts[size] = ImageFont.truetype(FONT, size)
    return _fonts[size].getlength(txt)


# ------------------------------------------------------------ geometría
def rr(x, y, w, h, r=18):
    return (f"M{x + r},{y} L{x + w - r},{y} Q{x + w},{y} {x + w},{y + r} L{x + w},{y + h - r} "
            f"Q{x + w},{y + h} {x + w - r},{y + h} L{x + r},{y + h} Q{x},{y + h} {x},{y + h - r} "
            f"L{x},{y + r} Q{x},{y} {x + r},{y}")


def circ(cx, cy, r):
    return f"M{cx - r},{cy} a{r},{r} 0 1,0 {2 * r},0 a{r},{r} 0 1,0 {-2 * r},0"


def ell(cx, cy, rx, ry):
    return f"M{cx - rx},{cy} a{rx},{ry} 0 1,0 {2 * rx},0 a{rx},{ry} 0 1,0 {-2 * rx},0"


def ln(x1, y1, x2, y2):
    return f"M{x1},{y1} L{x2},{y2}"


def arrow(x1, y1, x2, y2, c=K, w=5, bend=0):
    import math
    if bend:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        n = math.hypot(dx, dy) or 1
        cx, cy = mx - dy / n * bend, my + dx / n * bend
        d = f"M{x1},{y1} Q{cx:.1f},{cy:.1f} {x2},{y2}"
        ang = math.atan2(y2 - cy, x2 - cx)
    else:
        d = ln(x1, y1, x2, y2)
        ang = math.atan2(y2 - y1, x2 - x1)
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    h = f"M{x2 + 26 * math.cos(a1):.1f},{y2 + 26 * math.sin(a1):.1f} L{x2},{y2} L{x2 + 26 * math.cos(a2):.1f},{y2 + 26 * math.sin(a2):.1f}"
    return [P(d, c, w), P(h, c, w)]


def check(x, y, s=1.0, c=B):
    return [P(f"M{x - 22 * s},{y} L{x - 6 * s},{y + 18 * s} L{x + 26 * s},{y - 22 * s}", c, 7)]


def cross(x, y, s=1.0, c=R):
    return [P(ln(x - 22 * s, y - 22 * s, x + 22 * s, y + 22 * s), c, 7), P(ln(x + 22 * s, y - 22 * s, x - 22 * s, y + 22 * s), c, 7)]


def stick(x, y, s=1.0, c=K):
    r = 22 * s
    return [P(circ(x, y, r), c, 5), P(f"M{x},{y + r} L{x},{y + r + 70 * s}", c, 5),
            P(f"M{x - 34 * s},{y + r + 28 * s} L{x},{y + r + 14 * s} L{x + 34 * s},{y + r + 28 * s}", c, 5),
            P(f"M{x - 28 * s},{y + r + 118 * s} L{x},{y + r + 70 * s} L{x + 28 * s},{y + r + 118 * s}", c, 5)]


def building(x, y, w=150, h=110, c=K):
    return [P(f"M{x - 12},{y} L{x + w / 2},{y - 52} L{x + w + 12},{y} Z", c, 5), P(rr(x, y, w, h, 4), c, 5),
            P(f"M{x + w * 0.22},{y + 18} L{x + w * 0.22},{y + h} M{x + w * 0.5},{y + 18} L{x + w * 0.5},{y + h} M{x + w * 0.78},{y + 18} L{x + w * 0.78},{y + h}", c, 4)]


def house(x, y, s=1.0, c=K):
    return [P(f"M{x - 50 * s},{y} L{x},{y - 44 * s} L{x + 50 * s},{y}", c, 5), P(rr(x - 40 * s, y, 80 * s, 66 * s, 3), c, 5), P(rr(x - 12 * s, y + 30 * s, 24 * s, 36 * s, 2), c, 4)]


def coin(cx, cy, r=26, c=K):
    return [P(circ(cx, cy, r), c, 5), P(f"M{cx + 9},{cy - 10} Q{cx - 12},{cy - 16} {cx - 8},{cy - 2} Q{cx + 12},{cy + 6} {cx - 9},{cy + 12} M{cx},{cy - 20} L{cx},{cy + 20}", c, 4)]


def magnifier(cx, cy, r=34, c=K):
    return [P(circ(cx, cy, r), c, 6), P(ln(cx + r * 0.7, cy + r * 0.7, cx + r * 1.6, cy + r * 1.6), c, 9)]


def shield(cx, cy, s=1.0, c=B):
    return [P(f"M{cx},{cy - 60 * s} L{cx + 52 * s},{cy - 40 * s} L{cx + 52 * s},{cy + 6 * s} Q{cx + 52 * s},{cy + 50 * s} {cx},{cy + 70 * s} Q{cx - 52 * s},{cy + 50 * s} {cx - 52 * s},{cy + 6 * s} L{cx - 52 * s},{cy - 40 * s} Z", c, 6)]


def gear(cx, cy, r=34, c=K):
    import math
    teeth = " ".join(f"M{cx + (r + 2) * math.cos(a):.1f},{cy + (r + 2) * math.sin(a):.1f} L{cx + (r + 14) * math.cos(a):.1f},{cy + (r + 14) * math.sin(a):.1f}"
                     for a in [k * math.pi / 4 for k in range(8)])
    return [P(circ(cx, cy, r), c, 6), P(teeth, c, 7), P(circ(cx, cy, r * 0.35), c, 4)]


def scale_icon(cx, cy, s=1.0, c=K):
    return [P(ln(cx, cy - 60 * s, cx, cy + 60 * s), c, 6), P(ln(cx - 90 * s, cy - 50 * s, cx + 90 * s, cy - 50 * s), c, 6),
            P(f"M{cx - 120 * s},{cy + 10 * s} L{cx - 90 * s},{cy - 50 * s} L{cx - 60 * s},{cy + 10 * s} Q{cx - 90 * s},{cy + 34 * s} {cx - 120 * s},{cy + 10 * s}", c, 5),
            P(f"M{cx + 60 * s},{cy + 10 * s} L{cx + 90 * s},{cy - 50 * s} L{cx + 120 * s},{cy + 10 * s} Q{cx + 90 * s},{cy + 34 * s} {cx + 60 * s},{cy + 10 * s}", c, 5),
            P(ln(cx - 40 * s, cy + 60 * s, cx + 40 * s, cy + 60 * s), c, 6)]


def card(x, y, c=K):
    return [P(rr(x, y, 120, 80, 8), c, 5), P(circ(x + 32, y + 32, 14), c, 4), P(f"M{x + 60},{y + 26} L{x + 104},{y + 26} M{x + 60},{y + 46} L{x + 96},{y + 46} M{x + 14},{y + 64} L{x + 104},{y + 64}", c, 4)]


def piggy(cx, cy, c=K):
    return [P(ell(cx, cy, 64, 46), c, 5), P(ln(cx - 14, cy - 46, cx + 14, cy - 46), R, 6),
            P(f"M{cx - 36},{cy + 40} L{cx - 36},{cy + 62} M{cx + 34},{cy + 40} L{cx + 34},{cy + 62} M{cx + 64},{cy - 6} L{cx + 82},{cy - 6}", c, 5)]


def gavel(cx, cy, c=K):
    return [P(rr(cx - 46, cy - 46, 70, 40, 6), c, 5), P(ln(cx - 4, cy - 10, cx + 46, cy + 40), c, 7), P(ln(cx - 50, cy + 56, cx + 30, cy + 56), c, 6)]


def folder(x, y, w=150, h=100, c=K):
    return [P(f"M{x},{y + 16} L{x},{y + h} L{x + w},{y + h} L{x + w},{y + 16} L{x + w * 0.5},{y + 16} L{x + w * 0.42},{y} L{x + 6},{y} Z", c, 5)]


def book(cx, cy, w=360, h=220, c=K):
    return [P(f"M{cx},{cy - h / 2 + 20} Q{cx - w / 4},{cy - h / 2 - 10} {cx - w / 2},{cy - h / 2 + 10} L{cx - w / 2},{cy + h / 2} Q{cx - w / 4},{cy + h / 2 - 24} {cx},{cy + h / 2} Q{cx + w / 4},{cy + h / 2 - 24} {cx + w / 2},{cy + h / 2} L{cx + w / 2},{cy - h / 2 + 10} Q{cx + w / 4},{cy - h / 2 - 10} {cx},{cy - h / 2 + 20} L{cx},{cy + h / 2}", c, 6)]


def cart(cx, cy, c=K):
    return [P(f"M{cx - 90},{cy - 50} L{cx - 62},{cy - 50} L{cx - 40},{cy + 30} L{cx + 60},{cy + 30} L{cx + 80},{cy - 26} L{cx - 50},{cy - 26}", c, 6), P(circ(cx - 26, cy + 52, 12), c, 5), P(circ(cx + 46, cy + 52, 12), c, 5)]


def umbrella(cx, cy, c=B):
    return [P(f"M{cx - 150},{cy} Q{cx},{cy - 150} {cx + 150},{cy} Q{cx + 112},{cy - 22} {cx + 75},{cy} Q{cx + 38},{cy - 22} {cx},{cy} Q{cx - 38},{cy - 22} {cx - 75},{cy} Q{cx - 112},{cy - 22} {cx - 150},{cy}", c, 6), P(ln(cx, cy - 75, cx, cy + 10), c, 5)]


def car(cx, cy, c=K):
    return [P(f"M{cx - 70},{cy + 20} L{cx - 70},{cy - 6} L{cx - 40},{cy - 10} L{cx - 22},{cy - 40} L{cx + 30},{cy - 40} L{cx + 50},{cy - 10} L{cx + 72},{cy - 4} L{cx + 72},{cy + 20} Z", c, 5), P(circ(cx - 38, cy + 24, 14), c, 5), P(circ(cx + 40, cy + 24, 14), c, 5)]


def cylinder(cx, cy, w=360, h=300, c=K):
    rx, ry = w / 2, 44
    return [P(ell(cx, cy - h / 2, rx, ry), c, 6),
            P(f"M{cx - rx},{cy - h / 2} L{cx - rx},{cy + h / 2} A{rx},{ry} 0 0,0 {cx + rx},{cy + h / 2} L{cx + rx},{cy - h / 2}", c, 6),
            P(f"M{cx - rx},{cy} A{rx},{ry} 0 0,0 {cx + rx},{cy}", c, 4)]


def eye(cx, cy, c=K):
    return [P(f"M{cx - 60},{cy} Q{cx},{cy - 50} {cx + 60},{cy} Q{cx},{cy + 50} {cx - 60},{cy}", c, 5), P(circ(cx, cy, 16), c, 6)]


def cloud(cx, cy, w, h, c=B):
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    return [P(f"M{x0 + 60},{y1} Q{x0 - 40},{y1} {x0},{cy} Q{x0 - 30},{y0 + 20} {x0 + 90},{y0 + 10} Q{x0 + 160},{y0 - 60} {cx},{y0} "
              f"Q{x1 - 120},{y0 - 60} {x1 - 60},{y0 + 20} Q{x1 + 40},{y0 + 40} {x1},{cy} Q{x1 + 30},{y1} {x1 - 60},{y1} Z", c, 6)]


def birrete(cx, cy, c=K):
    return [P(f"M{cx - 60},{cy} L{cx},{cy - 24} L{cx + 60},{cy} L{cx},{cy + 24} Z", c, 5), P(f"M{cx + 50},{cy + 4} L{cx + 50},{cy + 40}", c, 4)]


# ------------------------------------------------------------ primitivas
class P:
    def __init__(self, d, c=K, w=5):
        self.d, self.c, self.w = d, c, w


class TX:
    def __init__(self, x, y, txt, size=44, c=K, anchor="start"):
        self.x, self.y, self.txt, self.size, self.c = x, y, txt, size, c
        self.width = tw(txt, size)
        self.x0 = x - self.width / 2 if anchor == "middle" else x


class FILL:
    def __init__(self, d, c, op=1.0, rot=0, cx=0, cy=0):
        self.d, self.c, self.op, self.rot, self.cx, self.cy = d, c, op, rot, cx, cy


def flat(items):
    out = []
    for it in items:
        if isinstance(it, list):
            out.extend(flat(it))
        else:
            out.append(it)
    return out


# ------------------------------------------------------------ capítulo
class Ch:
    def __init__(self, cid, t0, t1, num, title):
        self.cid, self.t0, self.t1 = cid, t0, t1
        self.svg = []  # (scene_id, markup)
        self.js = []
        self.hand = []  # eventos: (t0, t1, tipo, puntos)
        self.cursor = t0 + 0.15
        self.k = 0
        self.scenes = []
        self.scene = None
        self.visible = []
        self.new_scene("t")
        if title:
            items = [P(circ(150, 352, 46), B, 6), TX(150, 372, str(num), 56, B, "middle"), TX(222, 378, title, 58, K)]
            items.append(P(f"M222,404 Q{222 + tw(title, 58) / 2},{396} {222 + tw(title, 58) + 10},{406}", B, 6))
            self.burst(t0 + 0.2, items)
        self.new_scene()

    def nid(self):
        self.k += 1
        return f"{self.cid}-e{self.k}"

    def new_scene(self, tag=None):
        sid = f"{self.cid}-s{len(self.scenes)}"
        self.scenes.append(sid)
        self.scene = sid
        self.visible.append(sid)
        self.svg.append((sid, []))

    def add(self, markup):
        self.svg[-1][1].append(markup)

    def note(self, t, kind):
        """Post-it «EJEMPLO DEL APUNTE» o «PARA ENTENDERLO» arriba a la derecha."""
        txt, col = ("EJEMPLO DEL APUNTE", "#ffe27a") if kind == "ej" else ("PARA ENTENDERLO", "#b9e0ff")
        self.burst(t, [FILL(rr(596, 422, 372, 64, 8), col, 1, -2, 782, 454), TX(782, 466, txt, 36, K, "middle")])

    def burst(self, t, items):
        if self.cursor + 0.08 - t > 0.7:
            print(f"  atraso {self.cid}: pedido {t:.2f}, sale {self.cursor + 0.08:.2f}")
        t = max(t, self.cursor + 0.08)
        for it in flat(items):
            eid = self.nid()
            if isinstance(it, P):
                path = parse_path(it.d)
                length = max(path.length(), 1)
                d = min(max(length / 1500, 0.1), 0.85)
                n = max(2, int(d * 30))
                pts = [path.point(i / n) for i in range(n + 1)]
                self.add(f'<path id="{eid}" class="h" d="{it.d}" fill="none" stroke="{it.c}" stroke-width="{it.w}" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" />')
                self.js.append(f'tl.set("#{eid}", {{ opacity: 1 }}, A({t:.2f})); tl.to("#{eid}", {{ strokeDashoffset: 0, duration: {d:.2f}, ease: "none" }}, A({t:.2f}));')
                self.hand.append((t, t + d, "draw", [(round(p.real), round(p.imag)) for p in pts]))
                t += d + 0.03
            elif isinstance(it, TX):
                d = min(max(len(it.txt) * 0.026, 0.22), 1.0)
                h = it.size * 1.4
                self.add(f'<clipPath id="{eid}-c"><rect id="{eid}-r" x="{it.x0 - 4:.0f}" y="{it.y - it.size * 1.05:.0f}" width="0" height="{h:.0f}" /></clipPath>'
                         f'<text id="{eid}" clip-path="url(#{eid}-c)" x="{it.x0:.0f}" y="{it.y}" font-size="{it.size}" fill="{it.c}">{it.txt}</text>')
                self.js.append(f'tl.to("#{eid}-r", {{ attr: {{ width: {it.width + 12:.0f} }}, duration: {d:.2f}, ease: "none" }}, A({t:.2f}));')
                n = max(2, int(d * 14))
                pts = [(round(it.x0 + it.width * i / n), round(it.y - it.size * 0.3 + (8 if i % 2 else -6))) for i in range(n + 1)]
                self.hand.append((t, t + d, "draw", pts))
                t += d + 0.03
            elif isinstance(it, FILL):
                rot = f' transform="rotate({it.rot} {it.cx} {it.cy})"' if it.rot else ""
                self.add(f'<g{rot}><path id="{eid}" class="h" d="{it.d}" fill="{it.c}" stroke="{K}" stroke-width="3" /></g>')
                self.js.append(f'tl.to("#{eid}", {{ opacity: {it.op}, duration: 0.25 }}, A({t:.2f}));')
                t += 0.15
        self.cursor = t
        return t

    def erase(self, t, all_=False):
        """La mano pasa el borrador y la pizarra queda limpia."""
        t = max(t, self.cursor + 0.05)
        targets = [s for s in self.visible if all_ or s != f"{self.cid}-s0"]
        if targets:
            sel = ", ".join("#" + s for s in targets)
            self.js.append(f'tl.to([{", ".join(repr("#" + s) for s in targets)}], {{ opacity: 0, duration: 0.7, ease: "power1.in" }}, A({t + 0.1:.2f}));')
        zz = [(220, 560), (900, 640), (200, 780), (880, 880), (220, 1020), (900, 1120), (300, 1200)]
        if all_:
            zz = [(260, 330)] + zz
        self.hand.append((t, t + 0.85, "erase", zz))
        self.visible = [s for s in self.visible if s not in targets]
        self.cursor = t + 0.9
        if not all_:
            self.new_scene()

    def build(self, last=False):
        if not last:
            self.erase(self.t1 - 1.0, all_=True)
        # Mano: viajes entre trazos, descansos fuera de cuadro y borrador
        js_h = [f'tl.set("#{self.cid}-hand", {{ x: {REST[0]}, y: {REST[1]} }}, 0);']
        pos = REST
        prev_end = 0.0
        mode = "mk"
        for (a, b, kind, pts) in sorted(self.hand):
            gap = a - prev_end
            start = pts[0]
            if gap > 1.6 and pos != REST:
                js_h.append(f'tl.to("#{self.cid}-hand", {{ x: {REST[0]}, y: {REST[1]}, duration: 0.45, ease: "power2.in" }}, A({prev_end + 0.05:.2f}));')
                pos = REST
            want = "er" if kind == "erase" else "mk"
            if want != mode:
                js_h.append(f'tl.set("#{self.cid}-mk", {{ opacity: {1 if want == "mk" else 0} }}, A({a - 0.3:.2f})); tl.set("#{self.cid}-er", {{ opacity: {1 if want == "er" else 0} }}, A({a - 0.3:.2f}));')
                mode = want
            tr = 0.4 if pos == REST else min(0.3, max(gap - 0.02, 0.05))
            js_h.append(f'tl.to("#{self.cid}-hand", {{ x: {start[0]}, y: {start[1]}, duration: {tr:.2f}, ease: "power2.inOut" }}, A({a - tr:.2f}));')
            seg = (b - a) / max(1, len(pts) - 1)
            kf = ", ".join(f"{{ x: {x}, y: {y}, duration: {seg:.3f}, ease: 'none' }}" for x, y in pts[1:])
            js_h.append(f'tl.to("#{self.cid}-hand", {{ keyframes: [{kf}] }}, A({a:.2f}));')
            pos = pts[-1]
            prev_end = b
        js_h.append(f'tl.to("#{self.cid}-hand", {{ x: {REST[0]}, y: {REST[1]}, duration: 0.45, ease: "power2.in" }}, A({prev_end + 0.05:.2f}));')
        groups = "".join(f'\n      <g id="{sid}">{"".join(m)}</g>' for sid, m in self.svg)
        hand = f"""
      <g id="{self.cid}-hand">
        <g transform="rotate(-32)">
          <g id="{self.cid}-mk">
            <path d="M0,0 L-11,28 L11,28 Z" fill="#222222" />
            <rect x="-15" y="28" width="30" height="150" rx="6" fill="#222222" />
            <rect x="-15" y="60" width="30" height="22" fill="{B}" />
          </g>
          <g id="{self.cid}-er" opacity="0">
            <rect x="-70" y="-24" width="140" height="48" rx="10" fill="#9aa4ad" stroke="#222222" stroke-width="4" />
            <rect x="-62" y="24" width="124" height="56" rx="10" fill="#1e6fd9" stroke="#222222" stroke-width="4" />
          </g>
          <path d="M-34,110 Q-46,150 -28,196 L40,206 Q62,160 46,112 Q30,92 6,100 Q-16,90 -34,110 Z" fill="#f6d2b5" stroke="#222222" stroke-width="4" stroke-linejoin="round" />
          <path d="M-30,128 Q-8,124 18,132 M-28,150 Q-4,146 26,154 M-24,172 Q0,168 30,176" fill="none" stroke="#222222" stroke-width="3" stroke-linecap="round" />
          <path d="M-36,196 L-46,420 L74,420 L44,204 Z" fill="#dfe6ee" stroke="#222222" stroke-width="4" stroke-linejoin="round" />
        </g>
      </g>"""
        dur = round(self.t1 - self.t0, 3)
        html = f"""<template>
  <style>
    @font-face {{ font-family: "Patrick Hand"; src: url("assets/fonts/PatrickHand-Regular.ttf") format("truetype"); }}
    #root {{ position: absolute; inset: 0; }}
    #{self.cid}-svg {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }}
    #{self.cid}-svg text {{ font-family: "Patrick Hand", sans-serif; }}
    .h {{ opacity: 0; }}
  </style>
  <div id="root" data-composition-id="{self.cid}" data-width="1080" data-height="1920">
    <svg id="{self.cid}-svg" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg" data-layout-allow-overlap>{groups}{hand}
    </svg>
  </div>
  <script>
    const T0 = {self.t0};
    const tl = gsap.timeline({{ paused: true }});
    const A = (t) => Math.max(0, +(t - T0).toFixed(3));
    {chr(10).join("    " + j for j in self.js).strip()}
    {chr(10).join("    " + j for j in js_h).strip()}
    tl.set({{}}, {{}}, {dur});
    window.__timelines["{self.cid}"] = tl;
  </script>
</template>
"""
        (OUT / "compositions" / f"{self.cid}.html").write_text(html)
        return (self.cid, self.t0, dur)


chapters = []
Bd = [0, 23.2, 66.4, 105.9, 151.8, 204.7, 230.1, 274.8, 337.9, 422.7, TOTAL]

# ================================================================ INTRO
c = Ch("c0", Bd[0], Bd[1], 0, None)
c.burst(0.1, [P(rr(380, 560, 320, 380, 10)), TX(540, 650, "PLAN", 64, B, "middle"),
              P("M420,720 L660,720 M420,780 L640,780 M420,840 L600,840", K, 4),
              TX(800, 640, "?", 140, R, "middle")])
c.burst(W(1, 0.45), [house(250, 1120, 1.0), house(830, 1120, 1.0), TX(540, 1130, "¿mismas reglas?", 48, R, "middle")])
c.erase(L(2) - 0.6)
c.burst(L(2), [book(540, 640, 420, 240), TX(540, 625, "LEY 4938", 66, B, "middle")])
c.burst(W(2, 0.45), [arrow(420, 770, 250, 1000), arrow(540, 780, 540, 1030), arrow(660, 770, 830, 1000),
                    house(250, 1080, 0.9), house(540, 1110, 0.9), house(830, 1080, 0.9)])
c.erase(L(3) - 0.7)
c.burst(L(3), [TX(540, 600, "Ley 4938", 70, B, "middle"), P("M370,630 Q540,616 710,632", B, 6)])
c.burst(W(3, 0.2), [P("M150,700 Q120,700 120,760 L120,1080 Q120,1140 150,1140", K, 5), TX(170, 770, "1. Administración financiera", 50)])
c.burst(W(3, 0.45), [TX(170, 900, "2. Contrataciones y", 50), TX(210, 960, "administración de bienes", 50)])
c.burst(W(3, 0.78), [TX(170, 1090, "3. Sistemas de control", 50)])
c.erase(L(4) - 0.4)
c.burst(L(4), [TX(540, 760, "UNIDAD 3", 120, B, "middle"), P("M300,800 Q540,780 780,804", R, 7),
               TX(540, 900, "Régimen financiero y contable", 52, K, "middle"), TX(540, 966, "del sector público", 52, K, "middle")])
chapters.append(c.build())

# ================================================================ C1
c = Ch("c1", Bd[1], Bd[2], 1, "La administración financiera")
c.burst(L(6), [TX(540, 560, "conjunto de sistemas para...", 48, K, "middle")])
c.burst(W(6, 0.3), [P(rr(130, 640, 340, 150)), TX(300, 705, "obtener", 48, B, "middle"), TX(300, 760, "recursos", 48, B, "middle"),
                    coin(220, 880), coin(300, 900), coin(380, 880)])
c.burst(W(6, 0.62), [arrow(480, 690, 600, 690, B, 6, -30), P(rr(610, 640, 340, 150)), TX(780, 705, "aplicarlos", 48, B, "middle"),
                     TX(780, 760, "a sus funciones", 40, K, "middle"), arrow(600, 760, 480, 760, B, 6, -30), house(780, 900, 1.0)])
c.erase(L(7) - 0.4)
c.burst(L(7), [TX(540, 560, "3 grandes áreas", 58, B, "middle"), TX(540, 630, "art. 3 · Ley 4938", 42, R, "middle"),
               P("M540,660 L540,720 M270,720 L810,720 M270,720 L270,760 M540,720 L540,760 M810,720 L810,760", K, 5)])
c.burst(L(8), [P(rr(130, 760, 280, 220)), TX(270, 840, "Administración", 40, K, "middle"), TX(270, 890, "financiera", 40, K, "middle")])
c.burst(W(8, 0.36), [P(rr(410, 760, 260, 220)), TX(540, 840, "Contrataciones", 38, K, "middle"), TX(540, 890, "y bienes", 38, K, "middle")])
c.burst(W(8, 0.72), [P(rr(680, 760, 270, 220)), TX(815, 840, "Sistemas", 40, K, "middle"), TX(815, 890, "de control", 40, K, "middle")])
c.erase(L(9) - 0.4)
c.burst(L(9), [TX(540, 560, "¿A quién se aplica?", 52, B, "middle"), P(ell(540, 880, 420, 300), B, 6),
               TX(540, 640, "sector público provincial", 44, B, "middle")])
items10 = ["administración central", "organismos descentralizados", "seguridad social", "empresas y sociedades del Estado"]
for i, (txt, f) in enumerate(zip(items10, [0.05, 0.3, 0.55, 0.72])):
    c.burst(W(10, f), [P(circ(220, 708 + i * 62, 6), K, 6), TX(240, 720 + i * 62, txt, 40)])
items11 = ["Poder Legislativo", "Poder Judicial", "entidades con subsidio para un fin"]
for i, (txt, f) in enumerate(zip(items11, [0.1, 0.28, 0.5])):
    c.burst(W(11, f), [P(circ(220, 956 + i * 62, 6), K, 6), TX(240, 968 + i * 62, txt, 40)])
c.note(W(11, 0.78), "pe")
c.burst(W(11, 0.82), [coin(960, 1260, 24, R), arrow(930, 1236, 860, 1130, R, 5)])
chapters.append(c.build())

# ================================================================ C2
c = Ch("c2", Bd[2], Bd[3], 2, "Los sujetos")
c.burst(L(13), [TX(300, 540, "Entidad", 60, B, "middle"), P(rr(130, 580, 340, 260)), card(170, 620), piggy(380, 680)])
c.burst(W(13, 0.55), [TX(300, 790, "personalidad jurídica", 34, K, "middle"), TX(300, 830, "y patrimonio propio", 34, K, "middle")])
c.burst(L(14), [house(180, 930, 0.8), TX(180, 1050, "bienes", 36, K, "middle")])
c.burst(W(14, 0.35), [P("M260,980 Q280,940 300,980 Q320,1020 340,970 L360,990", K, 5), TX(310, 1050, "contrata", 36, K, "middle")])
c.burst(W(14, 0.66), [gavel(440, 960), TX(440, 1050, "demandada", 36, K, "middle")])
c.burst(L(15), [P(rr(560, 520, 400, 480), K, 4), TX(760, 570, "administración central", 34, K, "middle"),
                P(rr(610, 620, 300, 150), B, 6), TX(760, 710, "Jurisdicción", 50, B, "middle")])
c.burst(W(15, 0.55), [TX(760, 840, "sin personalidad", 38, R, "middle"), TX(760, 885, "jurídica propia", 38, R, "middle"), cross(760, 940, 0.8)])
c.erase(L(16) - 0.4)
c.burst(L(16), [TX(540, 560, "Son jurisdicciones:", 54, B, "middle")])
for i, (txt, f) in enumerate(zip(["Poder Legislativo", "Poder Judicial", "Gobernación", "ministerios y secretarías", "Tribunal de Cuentas"], [0.1, 0.27, 0.43, 0.6, 0.8])):
    y = 660 + i * 100
    c.burst(W(16, f), [P(rr(150, y - 44, 56, 56, 6)), check(178, y - 16, 0.9), TX(240, y, txt, 48)])
c.erase(L(17) - 0.4)
c.note(L(17), "ej")
c.burst(W(17, 0.1), [P(rr(110, 560, 380, 460, 10), K, 3), TX(300, 600, "adm. central", 32, K, "middle"),
                     building(225, 700, 150, 110), TX(300, 890, "Ministerio", 44, K, "middle"), TX(300, 940, "de Educación", 44, K, "middle")])
c.burst(W(17, 0.7), [arrow(300, 1030, 300, 1110, R, 5), TX(300, 1170, "jurisdicción", 52, R, "middle")])
c.burst(L(18), [building(610, 700, 110, 90), TX(665, 850, "IPV", 48, B, "middle"), building(790, 700, 110, 90), TX(845, 850, "OSEP", 48, B, "middle")])
c.burst(W(18, 0.45), [card(640, 890), piggy(860, 930), arrow(755, 1030, 755, 1110, R, 5), TX(755, 1170, "entidades", 52, R, "middle")])
chapters.append(c.build())

# ================================================================ C3
c = Ch("c3", Bd[3], Bd[4], 3, "Objetivos de la ley")
c.burst(W(19, 0.55), [TX(150, 470, "art. 4 · Ley 4938", 40, R)])
rows = [(20, 580, scale_icon(260, 610, 0.5), ["regularidad, legalidad,", "economicidad, eficiencia y eficacia"]),
        (21, 760, gear(260, 790, 28), ["sistematizar programación,", "gestión y evaluación"]),
        (22, 940, [P(rr(212, 920, 96, 70, 6)), TX(260, 968, "$", 40, K, "middle")], ["contrataciones con libre concurrencia,", "publicidad y transparencia"])]
for i, (n, y, icon, lines) in enumerate(rows):
    c.burst(W(n, 0.05), [P(circ(150, y + 20, 30), B, 5), TX(150, y + 38, str(i + 1), 46, B, "middle"), icon])
    c.burst(W(n, 0.25), [TX(330, y + 20, lines[0], 40), TX(330, y + 70, lines[1], 40)])
c.erase(L(23) - 0.35)
c.note(L(23), "pe")
c.burst(W(23, 0.08), [P(rr(380, 560, 320, 190, 10), R, 6), TX(540, 640, "COMPRA", 64, R, "middle"), TX(540, 710, "publicada", 40, K, "middle"),
                      P("M540,750 L540,800", K, 5)])
c.burst(W(23, 0.3), [stick(220, 920, 1.0), stick(540, 960, 1.0), stick(860, 920, 1.0),
                      arrow(260, 900, 400, 790, B, 5), arrow(540, 930, 540, 815, B, 5), arrow(820, 900, 680, 790, B, 5)])
c.erase(L(24) - 0.35)
c.burst(L(24), [P(circ(150, 600, 30), B, 5), TX(150, 618, "4", 46, B, "middle"), shield(260, 600, 0.6), TX(330, 615, "resguardar el patrimonio del Estado", 40)])
c.burst(L(25), [P(circ(150, 740, 30), B, 5), TX(150, 758, "5", 46, B, "middle"), magnifier(255, 738, 22), TX(330, 755, "responsabilizar a los funcionarios", 40),
                TX(330, 805, "por su gestión, recursos y resultados", 36)])
c.note(L(26), "pe")
c.burst(W(26, 0.1), [stick(380, 920, 1.1), coin(470, 1020, 30), arrow(520, 990, 690, 990, R, 6), TX(780, 1005, "responde", 48, R, "middle"),
                     magnifier(470, 1020, 56)])
chapters.append(c.build())

# ================================================================ C4
c = Ch("c4", Bd[4], Bd[5], 4, "Los cuatro sistemas")
c.burst(W(27, 0.45), [TX(540, 540, "cada sistema → su órgano rector", 46, B, "middle")])
sis = [(28, "Presupuesto", ["Subsecretaría de Presupuesto"]), (29, "Tesorería", ["Tesorería General", "de la Provincia"]),
       (30, "Crédito público", ["Oficina Provincial", "de Crédito Público"]), (31, "Contabilidad", ["Contaduría General", "de la Provincia"])]
for i, (n, s, rect) in enumerate(sis):
    y = 620 + i * 150
    its = [P(rr(120, y - 10, 300, 100)), TX(270, y + 54, s, 40, B, "middle"), arrow(430, y + 40, 500, y + 40, K, 5)]
    its += [TX(520, y + 30 + (22 if len(rect) == 1 else 0), rect[0], 38)] + ([TX(520, y + 76, rect[1], 38)] if len(rect) > 1 else [])
    c.burst(L(n) + 0.05, its)
c.erase(L(32) - 0.4)
c.burst(L(32), [TX(540, 560, "en cada jurisdicción:", 44, K, "middle")])
c.burst(W(32, 0.5), [P(rr(430, 820, 300, 130), B, 7), TX(580, 905, "SAF", 72, B, "middle"),
                     TX(580, 1000, "Servicio Administrativo Financiero", 34, K, "middle")])
c.burst(W(33, 0.05), [arrow(520, 1020, 420, 1100), arrow(580, 1020, 580, 1100), arrow(640, 1020, 740, 1100),
                      P(rr(340, 1100, 140, 70, 8)), P(rr(510, 1100, 140, 70, 8)), P(rr(680, 1100, 140, 70, 8)),
                      TX(580, 1225, "unidades ejecutoras", 36, K, "middle")])
c.burst(W(33, 0.55), [P(rr(130, 620, 190, 70, 8)), P(rr(340, 620, 190, 70, 8)), P(rr(550, 620, 190, 70, 8)), P(rr(760, 620, 190, 70, 8)),
                      TX(225, 668, "Presup.", 34, K, "middle"), TX(435, 668, "Tesorería", 34, K, "middle"), TX(645, 668, "Crédito", 34, K, "middle"), TX(855, 668, "Contab.", 34, K, "middle"),
                      P("M480,820 L225,690 M540,820 L435,690 M620,820 L645,690 M680,820 L855,690", K, 4), TX(870, 770, "sujeto a", 34, R, "middle")])
c.burst(L(34), [P(rr(100, 860, 300, 120, 10), R, 5), TX(250, 905, "Ministerio de", 32, K, "middle"), TX(250, 945, "Hacienda y Finanzas", 32, K, "middle"),
                P("M400,885 L430,885", R, 5), TX(250, 1030, "coordina · art. 5", 34, R, "middle")])
c.erase(L(35) - 0.4)
c.note(L(35), "ej")
c.burst(W(35, 0.1), [P(rr(360, 760, 360, 170, 12), B, 7), TX(540, 830, "SAF", 64, B, "middle"), TX(540, 890, "Ministerio de Salud", 38, K, "middle")])
for i, (txt, (fx, fy), f) in enumerate(zip(["presupuesto", "compras", "contabilidad", "tesorería"], [(140, 560), (760, 560), (140, 1040), (760, 1040)], [0.08, 0.3, 0.5, 0.7])):
    ax, ay = (fx + 90, fy + 100) if fy < 800 else (fx + 90, fy)
    c.burst(W(36, f), [folder(fx, fy, 180, 110), TX(fx + 90, fy + (150 if fy < 800 else -24), txt, 38, K, "middle"),
                       arrow(540 + (-90 if fx < 500 else 90), 760 if fy < 800 else 930, ax, ay + (40 if fy < 800 else 0), K, 4)])
c.burst(W(36, 0.86), [TX(540, 1240, "siguiendo las normas de cada órgano rector", 38, R, "middle")])
chapters.append(c.build())

# ================================================================ C5
c = Ch("c5", Bd[5], Bd[6], 5, "Contrataciones y bienes")
c.burst(L(38), [cloud(540, 790, 760, 380, B), TX(540, 660, "macrosistema", 44, B, "middle"),
                P(rr(190, 720, 320, 120, 12)), TX(350, 795, "Contrataciones", 40, K, "middle")])
c.burst(W(38, 0.6), [P(rr(560, 720, 330, 120, 12)), TX(725, 775, "Administración", 38, K, "middle"), TX(725, 818, "de bienes", 38, K, "middle")])
c.burst(L(39), [TX(540, 530, "coordina: Ministerio de Hacienda y Finanzas", 38, R, "middle")])
c.burst(W(39, 0.68), [TX(820, 1010, "→ Unidad 8", 42, R, "middle")])
c.note(L(40), "pe")
c.burst(W(40, 0.12), [cart(330, 1080), arrow(330, 1010, 340, 860, B, 5), TX(330, 1210, "comprar", 40, K, "middle")])
c.burst(W(40, 0.58), [umbrella(720, 1060), building(620, 1100, 100, 70), car(830, 1130), TX(720, 1240, "cuidar lo que ya tiene", 38, K, "middle")])
chapters.append(c.build())

# ================================================================ C6
c = Ch("c6", Bd[6], Bd[7], 6, "Sistemas de control")
c.burst(L(42), [P(rr(110, 520, 620, 640, 16), K, 6), TX(140, 570, "Poder Ejecutivo", 42, K)])
c.burst(W(42, 0.25), [P(rr(150, 610, 360, 120, 10), B, 5), TX(330, 660, "Contaduría General", 38, B, "middle"), TX(330, 705, "órgano rector", 32, R, "middle")])
c.burst(W(42, 0.6), [magnifier(210, 820, 28), magnifier(360, 820, 28), magnifier(510, 820, 28),
                     TX(380, 930, "Unidades de Auditoría Interna", 36, K, "middle")])
c.burst(L(43), [P("M640,640 A50,50 0 1,1 590,690", B, 6), P("M582,668 L590,692 L612,680", B, 6),
                TX(420, 1010, "se controla a sí mismo:", 38, B, "middle"), TX(420, 1060, "detecta y corrige errores", 38, B, "middle")])
c.burst(L(44), [P(rr(760, 700, 200, 180, 10), R, 6), TX(860, 770, "Tribunal", 40, R, "middle"), TX(860, 815, "de Cuentas", 40, R, "middle"),
                arrow(760, 800, 735, 800, R, 5), TX(860, 940, "fuera del", 36, K, "middle"), TX(860, 980, "Ejecutivo", 36, K, "middle"),
                TX(420, 1130, "control interno", 40, B, "middle"), TX(860, 1060, "control externo", 36, R, "middle")])
c.erase(L(45) - 0.4)
c.note(L(45), "ej")
c.burst(W(45, 0.08), [P("M140,860 L940,860", K, 6), coin(540, 860, 34), TX(540, 950, "pago", 44, K, "middle"), TX(540, 590, "auditoría interna", 46, B, "middle")])
c.burst(W(45, 0.5), [magnifier(380, 720, 40), TX(380, 660, "antes", 40, B, "middle")])
c.burst(W(45, 0.78), [magnifier(700, 720, 40), TX(700, 660, "después", 40, B, "middle")])
c.burst(L(46), [magnifier(840, 1050, 40), TX(700, 1150, "Tribunal de Cuentas", 44, R, "middle"), TX(700, 1210, "¿conforme a la ley?", 40, R, "middle")])
c.burst(W(46, 0.82), check(910, 1180, 1.0, R))
c.erase(L(47) - 0.4)
c.burst(L(47), [TX(540, 560, "integral e integrado", 60, B, "middle"), TX(540, 625, "art. 124 · Ley 4938", 38, R, "middle")])
c.burst(W(47, 0.35), [P(circ(410, 880, 220), K, 5), TX(330, 860, "sistemas", 40, K, "middle"), TX(330, 905, "administrativos", 40, K, "middle")])
c.burst(W(47, 0.62), [P(circ(670, 880, 220), K, 5), TX(760, 860, "producción de", 40, K, "middle"), TX(760, 905, "bienes y servicios", 40, K, "middle"), eye(540, 1000)])
chapters.append(c.build())

# ================================================================ C7
c = Ch("c7", Bd[7], Bd[8], 7, "Sistema presupuestario")
c.burst(L(49), [P(rr(130, 540, 820, 170, 14), B, 7), TX(540, 520, "órgano rector · dicta normas", 38, R, "middle")])
c.burst(W(49, 0.45), [TX(540, 610, "Dirección Provincial de", 48, B, "middle"), TX(540, 670, "Programación Presupuestaria", 48, B, "middle")])
c.burst(L(50), [P(rr(150, 780, 780, 260, 14), R, 4), TX(540, 840, "en la tabla figura como", 40, K, "middle"),
                TX(540, 900, "«Subsecretaría de Presupuesto»", 44, R, "middle")])
c.burst(W(50, 0.55), [P(circ(220, 980, 26), R, 5), TX(220, 995, "!", 40, R, "middle"),
                      TX(560, 995, "la denominación puede haber cambiado", 38, K, "middle")])
c.erase(L(51) - 0.4)
c.burst(L(51), [P(rr(270, 520, 540, 110, 12), B, 6), TX(540, 590, "Dirección (rector)", 46, B, "middle")])
c.burst(W(51, 0.15), [arrow(400, 640, 260, 780), arrow(540, 640, 540, 780), arrow(680, 640, 820, 780),
                     P(rr(130, 790, 260, 120, 10)), P(rr(410, 790, 260, 120, 10)), P(rr(690, 790, 260, 120, 10)),
                     TX(540, 980, "unidades sectoriales", 44, K, "middle"), TX(540, 1040, "en cada jurisdicción · aplican", 40, R, "middle")])
c.erase(L(52) - 0.4)
c.burst(L(52), [stick(250, 760, 1.4), birrete(250, 712), TX(400, 680, "título universitario", 44), TX(400, 735, "en Ciencias Económicas", 44, B)])
c.burst(W(52, 0.5), [TX(400, 880, "5 años de experiencia", 46, R)] + [P(ln(420 + k * 40, 920, 420 + k * 40, 990), K, 6) for k in range(4)] + [P(ln(400, 980, 590, 930), R, 6)])
c.burst(W(52, 0.75), [TX(400, 1070, "financiero-contable", 40), TX(400, 1120, "en la administración pública", 40)])
c.erase(L(53) - 0.4)
c.burst(L(53), [TX(320, 540, "Órgano rector", 46, B, "middle"), P("M540,500 L540,1160", K, 4)])
for i, (txt, f) in enumerate(zip(["política financiera", "normas técnicas", "proyecto de ley", "analiza anteproyectos"], [0.25, 0.45, 0.65, 0.83])):
    c.burst(W(53, f), [P(circ(140, 618 + i * 80, 6), K, 6), TX(160, 630 + i * 80, txt, 38)])
c.burst(L(54), [TX(760, 540, "Unid. sectoriales", 46, B, "middle")])
for i, (txt, f) in enumerate(zip(["asesoran", "coordinan anteproyectos", "registran ejec. física", "indicadores de gestión"], [0.15, 0.32, 0.6, 0.82])):
    c.burst(W(54, f), [P(circ(575, 618 + i * 80, 6), K, 6), TX(595, 630 + i * 80, txt, 36)])
c.erase(L(55) - 0.4)
c.note(L(55), "ej")
c.burst(W(55, 0.1), [P(rr(300, 520, 480, 100, 12), B, 6), TX(540, 585, "Dirección: dicta normas", 42, B, "middle")])
c.burst(W(55, 0.55), [book(540, 700, 200, 110), TX(540, 700, "normas", 34, K, "middle"), arrow(540, 760, 540, 830, K, 5)])
c.burst(L(56), [P(rr(270, 840, 540, 100, 12)), TX(540, 905, "unidad sectorial del ministerio", 38, K, "middle")])
c.burst(W(56, 0.45), [arrow(540, 940, 540, 990, K, 5), P(rr(400, 1000, 280, 230, 8))] + [P(ln(430, 1040 + k * 40, 650 - (k % 2) * 60, 1040 + k * 40), K, 4) for k in range(5)]
        + [TX(840, 1090, "antepro-", 38, R, "middle"), TX(840, 1135, "yecto", 38, R, "middle")])
chapters.append(c.build())

# ================================================================ C8
c = Ch("c8", Bd[8], Bd[9], 8, "Inversión pública")
c.burst(L(58), [P(circ(330, 640, 130), B, 7), TX(330, 640, "Ley 4968", 54, B, "middle"), TX(330, 695, "(1998)", 40, K, "middle")])
c.burst(W(58, 0.62), [arrow(470, 640, 600, 640, K, 5), TX(760, 610, "modificada por", 38, K, "middle"), TX(760, 670, "Ley 5643", 56, R, "middle")])
c.burst(L(59), [P(circ(280, 960, 150), K, 5), TX(280, 945, "administración", 34, K, "middle"), TX(280, 985, "financiera", 34, K, "middle"),
                P(circ(800, 960, 150), B, 6), TX(800, 945, "inversión", 38, B, "middle"), TX(800, 985, "pública", 38, B, "middle")])
c.burst(W(59, 0.55), [P("M430,960 L650,960", R, 5), TX(540, 935, "presupuesto", 34, R, "middle")])
c.erase(L(60) - 0.4)
c.burst(L(60), [TX(540, 560, "objetivo:", 48, B, "middle"), TX(540, 630, "las inversiones más rentables", 48, K, "middle")])
c.burst(W(60, 0.5), [scale_icon(540, 870, 1.6), TX(390, 1020, "económico", 42, K, "middle"), TX(690, 1020, "social", 42, K, "middle")])
c.erase(L(61) - 0.4)
c.burst(L(61), [P(rr(150, 520, 780, 150, 14), B, 7), TX(540, 585, "Ministerio de Planificación", 44, B, "middle"), TX(540, 640, "y Modernización", 44, B, "middle")])
c.burst(W(61, 0.55), [TX(540, 720, "órgano rector · dicta las reglas", 38, R, "middle")])
c.burst(L(62), [P("M540,740 L540,770 M255,770 L825,770 M255,770 L255,800 M540,770 L540,800 M825,770 L825,800", K, 4),
                P(rr(140, 800, 230, 110, 10)), P(rr(425, 800, 230, 110, 10)), P(rr(710, 800, 230, 110, 10)),
                TX(255, 870, "USI", 50, B, "middle"), TX(540, 870, "USI", 50, B, "middle"), TX(825, 870, "USI", 50, B, "middle"),
                TX(540, 960, "en cada jurisdicción", 36, K, "middle")])
c.burst(W(62, 0.62), [P(rr(250, 1020, 210, 90, 10), K, 4), P(rr(620, 1020, 210, 90, 10), K, 4),
                      TX(355, 1080, "UMI", 46, R, "middle"), TX(725, 1080, "UMI", 46, R, "middle"), TX(540, 1170, "municipios que adhieran", 36, R, "middle")])
c.erase(L(63) - 0.4)
c.note(L(63), "pe")
c.burst(W(63, 0.25), [house(190, 560, 0.9), TX(260, 570, "el proyecto de una escuela", 44, B)])
steps = [(64, ["la jurisdicción lo formula y evalúa"]), (65, ["la USI lo eleva a la máxima autoridad", "decide si conviene → al Ministerio"]),
         (66, ["Ministerio: informe de pertinencia técnica"]), (67, ["análisis técnico y económico", "→ informe de resultados a la Dirección"]),
         (68, ["la Dirección verifica al asignar recursos"])]
ys = [680, 790, 930, 1040, 1180]
for i, ((n, lines), y) in enumerate(zip(steps, ys)):
    its = [P(circ(150, y - 12, 28), B, 5), TX(150, y + 4, str(i + 1), 40, B, "middle")]
    if i:
        its.insert(0, P(ln(150, ys[i - 1] + 16, 150, y - 40), K, 3))
    its += [TX(200, y + 2, lines[0], 38)]
    c.burst(L(n) + 0.05, its)
    if len(lines) > 1:
        c.burst(W(n, 0.55), [TX(200, y + 50, lines[1], 34, R)])
c.burst(W(68, 0.85), check(870, 1170, 1.1, B))
c.erase(L(69) - 0.4)
c.burst(L(69), [cylinder(540, 860, 380, 300), TX(540, 900, "BIP", 90, B, "middle"), TX(540, 560, "Banco Integrado de Proyectos", 46, K, "middle")])
c.burst(W(69, 0.45), [TX(540, 620, "base de datos oficial de la provincia", 38, R, "middle"), house(540, 700, 0.6)])
c.burst(W(69, 0.72), [TX(170, 1110, "avance físico", 38), P(rr(430, 1080, 420, 40, 20)), P("M440,1100 L700,1100", B, 22),
                      TX(170, 1190, "avance financiero", 38), P(rr(470, 1160, 380, 40, 20)), P("M480,1180 L640,1180", R, 22)])
chapters.append(c.build())

# ================================================================ CIERRE
c = Ch("c9", Bd[9], Bd[10], "?", "Pregunta de repaso")
c.burst(L(71), [TX(540, 560, "Si el proyecto de una escuela", 50, K, "middle"), TX(540, 625, "no pasa por la USI,", 50, K, "middle"),
                TX(540, 700, "¿puede avanzar? ¿Por qué?", 56, R, "middle")])
c.burst(W(71, 0.6), [P(ln(180, 880, 900, 880), K, 4)] + [P(circ(180 + k * 180, 880, 30), B, 5) for k in range(5)] + cross(360, 880, 1.2) + [TX(860, 1040, "?", 130, R, "middle")])
c.burst(L(72), [TX(540, 1180, "Respondé en los comentarios", 50, B, "middle")])
chapters.append(c.build(last=True))

# ================================================================ INDEX
hosts = "".join(
    f"""
      <div id="{cid}" style="z-index: 2" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html"
        data-start="{t0}" data-duration="{dur}" data-track-index="1" data-track-kind="graphics"
        data-width="1080" data-height="1920"></div>"""
    for cid, t0, dur in chapters)
(OUT / "index.html").write_text(f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #fbfbf8; }}
      #root {{ width: 100%; height: 100%; position: relative; }}
      #pizarra {{ position: absolute; inset: 0; background: radial-gradient(ellipse at 30% 20%, #ffffff 0%, #f7f7f3 60%, #eeeee9 100%); }}
      #marco {{ position: absolute; inset: 18px; border: 6px solid #c9ccd1; border-radius: 26px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="pizarra"></div>
      <div id="marco"></div>{hosts}
      <audio id="voz" class="clip" src="assets/voz.wav" data-start="0" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
for ch in chapters:
    print(ch)
print("TOTAL", TOTAL)
