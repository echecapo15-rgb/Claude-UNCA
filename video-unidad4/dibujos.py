"""Dibujos grandes reutilizables para la pizarra de la Unidad 4."""
import math

import pizarra as pz
from pizarra import (B, K, R, TX, FILL, P, arrow, book, building, circ, cloud, coin, cross, check,
                     ell, gavel, house, ln, magnifier, piggy, rr, shield, stick)

# ------------------------------------------------------------ dibujos grandes
def face(cx, cy, r, mood="happy", c=K):
    e = r * 0.38
    out = [P(circ(cx, cy, r), c, 5), P(circ(cx - e, cy - r * 0.15, 3), c, 6), P(circ(cx + e, cy - r * 0.15, 3), c, 6)]
    if mood == "happy":
        out.append(P(f"M{cx - r * 0.45},{cy + r * 0.25} Q{cx},{cy + r * 0.65} {cx + r * 0.45},{cy + r * 0.25}", c, 4))
    elif mood == "worried":
        out.append(P(f"M{cx - r * 0.4},{cy + r * 0.5} Q{cx},{cy + r * 0.2} {cx + r * 0.4},{cy + r * 0.5}", c, 4))
        out.append(P(f"M{cx - e - 10},{cy - r * 0.45} L{cx - e + 10},{cy - r * 0.35} M{cx + e + 10},{cy - r * 0.45} L{cx + e - 10},{cy - r * 0.35}", c, 4))
    elif mood == "surprised":
        out.append(P(circ(cx, cy + r * 0.4, r * 0.16), c, 4))
    return out


def person(x, y, s=1.4, mood="happy", arms="down", c=K):
    r = 24 * s
    out = face(x, y, r, mood, c) + [P(f"M{x},{y + r} L{x},{y + r + 80 * s}", c, 5)]
    if arms == "up":
        out.append(P(f"M{x - 44 * s},{y - 10 * s} L{x},{y + r + 18 * s} L{x + 44 * s},{y - 10 * s}", c, 5))
    elif arms == "carry":
        out.append(P(f"M{x - 40 * s},{y + r + 40 * s} L{x},{y + r + 18 * s} L{x + 46 * s},{y + r + 24 * s}", c, 5))
    elif arms == "point":
        out.append(P(f"M{x - 36 * s},{y + r + 46 * s} L{x},{y + r + 18 * s} L{x + 58 * s},{y + r - 6 * s}", c, 5))
    else:
        out.append(P(f"M{x - 36 * s},{y + r + 46 * s} L{x},{y + r + 18 * s} L{x + 36 * s},{y + r + 46 * s}", c, 5))
    out.append(P(f"M{x - 30 * s},{y + r + 130 * s} L{x},{y + r + 80 * s} L{x + 30 * s},{y + r + 130 * s}", c, 5))
    return out


def sweat(x, y):
    return [P(f"M{x},{y} Q{x + 12},{y + 22} {x},{y + 30} Q{x - 12},{y + 22} {x},{y}", B, 4)]


def dome(cx, base, w=320, c=K, label=None):
    h = w * 0.42
    x0 = cx - w / 2
    out = [P(ln(x0 - 20, base, x0 + w + 20, base), c, 6), P(rr(x0, base - h, w, h, 4), c, 5),
           P(f"M{x0 + 10},{base - h} L{cx},{base - h - 40} L{x0 + w - 10},{base - h}", c, 5),
           P(f"M{cx - w * 0.22},{base - h - 30} A{w * 0.22},{w * 0.2} 0 0,1 {cx + w * 0.22},{base - h - 30}", c, 5),
           P(ln(cx, base - h - 30 - w * 0.2, cx, base - h - 30 - w * 0.2 - 30), c, 4)]
    cols = " ".join(f"M{x0 + w * k / 6},{base - h + 14} L{x0 + w * k / 6},{base}" for k in range(1, 6))
    out.append(P(cols, c, 4))
    if label:
        out.append(TX(cx, base + 52, label, 40, c, "middle"))
    return out


def ministry(cx, base, w=300, c=K, label=None):
    h = w * 0.6
    x0 = cx - w / 2
    out = [P(rr(x0, base - h, w, h, 4), c, 5), P(ln(x0 - 20, base, x0 + w + 20, base), c, 6),
           P(" ".join(f"M{x0 + 30 + i * (w - 60) / 3},{base - h + 30} l40,0 l0,40 l-40,0 Z" for i in range(4)), c, 3),
           P(rr(cx - 30, base - 80, 60, 80, 4), c, 4), P(ln(cx, base - h, cx, base - h - 90), c, 4),
           P(f"M{cx},{base - h - 90} l60,15 l-60,15", R, 4)]
    if label:
        out.append(TX(cx, base + 52, label, 40, c, "middle"))
    return out


def factory(cx, base, c=K):
    return [P(f"M{cx - 150},{base} L{cx - 150},{base - 120} L{cx - 90},{base - 160} L{cx - 90},{base - 120} L{cx - 30},{base - 160} L{cx - 30},{base - 120} L{cx + 30},{base - 160} L{cx + 30},{base - 120} L{cx + 150},{base - 120} L{cx + 150},{base} Z", c, 5),
            P(rr(cx + 90, base - 230, 34, 110, 3), c, 4), P(circ(cx + 120, base - 260, 16), "#888", 4)]


def register(cx, cy, c=K):
    return [P(rr(cx - 60, cy - 40, 120, 80, 8), c, 5), P(rr(cx - 40, cy - 80, 80, 40, 6), c, 4), TX(cx, cy - 50, "$", 34, c, "middle")]


def megaphone(cx, cy, c=K):
    return [P(f"M{cx - 60},{cy - 18} L{cx - 60},{cy + 18} L{cx - 20},{cy + 18} L{cx + 50},{cy + 52} L{cx + 50},{cy - 52} L{cx - 20},{cy - 18} Z", c, 5),
            P(f"M{cx + 70},{cy - 30} Q{cx + 90},{cy} {cx + 70},{cy + 30} M{cx + 86},{cy - 48} Q{cx + 116},{cy} {cx + 86},{cy + 48}", B, 4)]


def target(cx, cy, c=R):
    return [P(circ(cx, cy, 60), c, 5), P(circ(cx, cy, 36), c, 5), P(circ(cx, cy, 12), c, 6), P(ln(cx + 70, cy - 70, cx + 4, cy - 4), K, 5)]


def crane(cx, base, c=K):
    return [P(f"M{cx - 40},{base} L{cx - 40},{base - 220} L{cx + 160},{base - 220} M{cx - 40},{base - 220} L{cx - 90},{base - 220} M{cx - 40},{base - 190} L{cx + 10},{base - 220}", c, 5),
            P(f"M{cx + 130},{base - 220} L{cx + 130},{base - 120}", c, 3), P(rr(cx + 105, base - 120, 50, 40, 3), c, 4)]


def clock(cx, cy, r=46, c=K):
    return [P(circ(cx, cy, r), c, 5), P(f"M{cx},{cy - r * 0.6} L{cx},{cy} L{cx + r * 0.45},{cy + r * 0.2}", c, 5)]


def jar(cx, top, w=260, h=380, c=K):
    return [P(f"M{cx - w / 2},{top + 30} L{cx - w / 2},{top + h - 20} Q{cx - w / 2},{top + h} {cx - w / 2 + 20},{top + h} L{cx + w / 2 - 20},{top + h} Q{cx + w / 2},{top + h} {cx + w / 2},{top + h - 20} L{cx + w / 2},{top + 30}", c, 6),
            P(rr(cx - w / 2 - 18, top - 10, w + 36, 40, 8), R, 7)]


def envelope(cx, cy, w=360, h=230, c=K):
    x0, y0 = cx - w / 2, cy - h / 2
    return [P(rr(x0, y0, w, h, 8), c, 6), P(f"M{x0},{y0} L{cx},{cy + 20} L{x0 + w},{y0}", c, 5)]


def stamp_box(cx, cy, txt, c=R, size=58, rot=-8):
    w = pz.tw(txt, size) + 50
    return [P(rr(cx - w / 2, cy - size * 0.85, w, size * 1.3, 10), c, 6), TX(cx, cy + size * 0.22, txt, size, c, "middle")]


def wallet(cx, cy, c=K):
    return [P(rr(cx - 80, cy - 50, 160, 100, 12), c, 5), P(f"M{cx + 30},{cy - 20} L{cx + 80},{cy - 20} L{cx + 80},{cy + 20} L{cx + 30},{cy + 20} Z", c, 4), TX(cx - 20, cy + 18, "0", 48, R, "middle")]


def copier(cx, cy, c=K):
    return [P(rr(cx - 140, cy - 60, 280, 150, 10), c, 6), P(rr(cx - 150, cy - 90, 300, 30, 6), c, 5),
            P(rr(cx + 140, cy + 20, 70, 50, 4), c, 4), P(ln(cx - 100, cy + 40, cx + 40, cy + 40), B, 6)]


def sack(cx, cy, c=K):
    return [P(f"M{cx - 30},{cy - 70} Q{cx},{cy - 50} {cx + 30},{cy - 70} L{cx + 20},{cy - 46} Q{cx + 90},{cy} {cx + 60},{cy + 60} L{cx - 60},{cy + 60} Q{cx - 90},{cy} {cx - 20},{cy - 46} Z", c, 5), TX(cx, cy + 34, "$", 50, c, "middle")]


def hourglass(cx, cy, s=1.0, c=K):
    return [P(f"M{cx - 60 * s},{cy - 90 * s} L{cx + 60 * s},{cy - 90 * s} L{cx - 60 * s},{cy + 90 * s} L{cx + 60 * s},{cy + 90 * s} Z", c, 6),
            P(f"M{cx - 22 * s},{cy + 70 * s} L{cx + 22 * s},{cy + 70 * s} L{cx},{cy + 40 * s} Z", B, 4)]


def sheet(cx, cy, w=280, h=360, lines=6, c=K):
    out = [P(rr(cx - w / 2, cy - h / 2, w, h, 6), c, 5)]
    out += [P(ln(cx - w / 2 + 30, cy - h / 2 + 50 + k * (h - 90) / lines, cx + w / 2 - 30 - (k % 3) * 30, cy - h / 2 + 50 + k * (h - 90) / lines), K, 4) for k in range(lines)]
    return out


def scissors(cx, cy, c=R):
    return [P(circ(cx - 40, cy + 30, 18), c, 5), P(circ(cx - 40, cy - 30, 18), c, 5), P(f"M{cx - 24},{cy + 20} L{cx + 70},{cy - 20} M{cx - 24},{cy - 20} L{cx + 70},{cy + 20}", c, 6)]


def pie23(cx, cy, r=70, c=B):
    a = math.radians(-90 + 240)
    sector = f"M{cx},{cy} L{cx},{cy - r} A{r},{r} 0 1,1 {cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f} Z"
    return [FILL(sector, "#bcd6fb", 1), P(circ(cx, cy, r), c, 5), P(f"M{cx},{cy - r} L{cx},{cy} L{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}", c, 4), TX(cx, cy + r + 50, "2/3", 46, B, "middle")]


def newspaper(cx, cy, c=K):
    return [P(rr(cx - 110, cy - 80, 220, 160, 6), c, 5), P(rr(cx - 90, cy - 60, 80, 60, 3), c, 3),
            P(f"M{cx + 10},{cy - 56} L{cx + 90},{cy - 56} M{cx + 10},{cy - 30} L{cx + 90},{cy - 30} M{cx - 90},{cy + 20} L{cx + 90},{cy + 20} M{cx - 90},{cy + 46} L{cx + 60},{cy + 46}", c, 3)]


def calendar_page(cx, cy, top, big, w=280, h=280, c=K, cbig=R):
    return [P(rr(cx - w / 2, cy - h / 2, w, h, 12), c, 6), P(f"M{cx - w / 2},{cy - h / 2 + 70} L{cx + w / 2},{cy - h / 2 + 70}", c, 5),
            P(f"M{cx - 60},{cy - h / 2 - 16} L{cx - 60},{cy - h / 2 + 16} M{cx + 60},{cy - h / 2 - 16} L{cx + 60},{cy - h / 2 + 16}", c, 6),
            TX(cx, cy - h / 2 + 52, top, 40, c, "middle"), TX(cx, cy + h / 2 - 50, big, 110, cbig, "middle")]


def wrench(cx, cy, c=B):
    return [P(f"M{cx - 70},{cy + 70} L{cx + 20},{cy - 20}", c, 14), P(f"M{cx + 10},{cy - 40} A36,36 0 1,1 {cx + 40},{cy - 10} L{cx + 50},{cy - 50} Z", c, 6)]


def podium(cx, base, c=K):
    return [P(f"M{cx - 90},{base} L{cx - 90},{base - 50} L{cx - 30},{base - 50} L{cx - 30},{base - 90} L{cx + 30},{base - 90} L{cx + 30},{base - 30} L{cx + 90},{base - 30} L{cx + 90},{base}", c, 5),
            TX(cx, base - 55, "1", 40, R, "middle"), TX(cx - 60, base - 12, "2", 34, c, "middle"), TX(cx + 60, base - 4, "3", 30, c, "middle")]


def chart(cx, cy, c=B):
    return [P(f"M{cx - 80},{cy - 70} L{cx - 80},{cy + 60} L{cx + 90},{cy + 60}", K, 5), P(f"M{cx - 70},{cy + 30} L{cx - 30},{cy - 10} L{cx + 10},{cy + 10} L{cx + 70},{cy - 50}", c, 6)]


def funnel(cx, top, w=620, h=360, c=K):
    return [P(f"M{cx - w / 2},{top} L{cx + w / 2},{top} L{cx + 50},{top + h - 90} L{cx + 50},{top + h} L{cx - 50},{top + h} L{cx - 50},{top + h - 90} Z", c, 7)]


def mini_sheet(cx, cy, c=K, rot=0, mark=None):
    out = [P(rr(cx - 45, cy - 55, 90, 110, 5), c, 4), P(f"M{cx - 28},{cy - 25} L{cx + 28},{cy - 25} M{cx - 28},{cy} L{cx + 20},{cy}", c, 3)]
    if mark:
        out.append(TX(cx, cy + 40, mark, 30, R, "middle"))
    return out


