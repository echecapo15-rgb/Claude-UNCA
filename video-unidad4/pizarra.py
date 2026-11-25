"""Motor de pizarra blanca dibujada a mano (reusado de la Unidad 3).

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
OUT = BASE / "proyecto"  # lo fija quien importa
FONT = str(Path(__file__).parent / "fuentes/PatrickHand-Regular.ttf")
TT = {x["n"]: (x["ini"], x["fin"]) for x in json.loads((BASE / "tiempos.json").read_text())}
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
                d = min(max(length / 2300, 0.08), 0.6)
                n = max(2, int(d * 30))
                pts = [path.point(i / n) for i in range(n + 1)]
                self.add(f'<path id="{eid}" class="h" d="{it.d}" fill="none" stroke="{it.c}" stroke-width="{it.w}" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" />')
                self.js.append(f'tl.set("#{eid}", {{ opacity: 1 }}, A({t:.2f})); tl.to("#{eid}", {{ strokeDashoffset: 0, duration: {d:.2f}, ease: "none" }}, A({t:.2f}));')
                self.hand.append((t, t + d, "draw", [(round(p.real), round(p.imag)) for p in pts]))
                t += d + 0.03
            elif isinstance(it, TX):
                d = min(max(len(it.txt) * 0.022, 0.18), 0.8)
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


