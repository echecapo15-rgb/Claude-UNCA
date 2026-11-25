"""Unidad 4 · Parte 1 (capítulos 0 a 5) en estilo pizarra con escenas grandes."""
import math
from pathlib import Path

import pizarra as pz
from pizarra import (B, K, R, TX, FILL, P, Ch, L, W, arrow, book, building, circ, cloud, coin, cross, check,
                     ell, gavel, house, ln, magnifier, piggy, rr, shield, stick)

BASE = Path(__file__).parent
pz.OUT = BASE / "parte1" / "proyecto"
TOTAL = 268.0


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


chapters = []
Bd = [0, 17.2, 61.4, 103.0, 166.2, 212.1, TOTAL]

# ================================================================ INTRO
c = Ch("c0", Bd[0], Bd[1], 0, None)
c.burst(0.1, [calendar_page(290, 700, "NOVIEMBRE", "30")])
c.burst(W(1, 0.3), [person(250, 980, 1.5, "happy", "carry"), book(400, 1060, 150, 100)])
c.burst(W(1, 0.62), [dome(780, 1150, 300), arrow(480, 1060, 610, 1060, B, 6), TX(780, 880, "DIC", 60, B, "middle")])
c.erase(L(2) - 0.35)
c.burst(L(2), [calendar_page(540, 720, "ENERO", "1", 340, 340), P("M380,560 L700,900", R, 7), TX(540, 1260, "¿sin ley?", 64, R, "middle"), face(540, 1090, 70, "worried")])
c.erase(L(3) - 0.3)
c.burst(L(3), [book(470, 760, 520, 300), TX(470, 760, "año anterior", 48, K, "middle"), wrench(820, 1000), TX(540, 1180, "con ajustes", 60, B, "middle")])
c.erase(L(4) - 0.3)
c.burst(L(4), [TX(540, 720, "UNIDAD 4", 130, B, "middle"), P("M260,760 Q540,740 820,764", R, 8), TX(540, 860, "Parte 1", 62, R, "middle"),
               TX(540, 1000, "elaborar · aprobar · controlar", 50, K, "middle")])
chapters.append(c.build())

# ================================================================ C1 Formulación
c = Ch("c1", Bd[1], Bd[2], 1, "La formulación")
c.burst(L(6), [ministry(300, 1080, 340), TX(300, 1135, "Hacienda y Finanzas", 38, K, "middle")])
c.burst(W(6, 0.5), [person(600, 860, 1.3, "happy", "point"), P(rr(680, 600, 270, 200, 10), K, 5), TX(815, 680, "pautas", 52, B, "middle"), TX(815, 750, "del proyecto", 36, K, "middle")])
c.burst(W(7, 0.05), [check(700, 900, 1.2), TX(760, 915, "planes", 40)])
c.burst(W(7, 0.28), [chart(820, 1010), TX(700, 1135, "variables", 38)])
c.burst(W(7, 0.5), [podium(170, 600), TX(170, 640, "prioridades", 36, K, "middle")])
c.burst(W(7, 0.72), [calendar_page(170, 830, "", "", 150, 140), P("M110,800 L230,800 M110,840 L200,840", K, 3), TX(170, 940, "cronograma", 36, K, "middle"), TX(870, 1210, "art. 22", 44, R, "middle")])
c.erase(L(8) - 0.4)
c.burst(L(8), [TX(540, 520, "anteproyectos", 60, B, "middle")])
for i, x in enumerate([170, 355, 540, 725, 910]):
    c.burst(W(8, 0.12 + i * 0.12), [house(x, 1080, 1.0), mini_sheet(x, 820, K, 0, "$?")])
c.burst(W(8, 0.85), [TX(540, 1230, "primer borrador", 48, R, "middle")])
c.erase(L(9) - 0.4)
c.burst(L(9), [funnel(540, 640, 620, 340), TX(540, 720, "Dirección de", 40, K, "middle"), TX(540, 770, "Programación", 40, K, "middle")])
c.burst(W(9, 0.35), [mini_sheet(330, 540), mini_sheet(480, 520), mini_sheet(630, 540)])
c.burst(W(9, 0.7), [mini_sheet(930, 760, K, 0, "Leg."), P("M930,830 Q980,900 900,960", R, 5), TX(880, 1000, "salvo", 40, R, "middle"), TX(870, 1045, "Legislativo", 40, R, "middle")])
c.burst(L(10), [book(400, 1110, 260, 150), TX(400, 1110, "PROYECTO", 40, B, "middle"), arrow(540, 990, 440, 1040, K, 5)])
c.burst(W(10, 0.5), [P(ell(780, 1230, 140, 36), K, 5), face(700, 1160, 30), face(780, 1150, 30), face(860, 1160, 30), TX(780, 1300, "acuerdo de ministros", 36, K, "middle")])
chapters.append(c.build())

# ================================================================ C2 Estructura
c = Ch("c2", Bd[2], Bd[3], 2, "La estructura de la ley")
c.burst(L(11), [book(540, 820, 860, 560), TX(780, 500, "art. 18", 40, R, "middle"), TX(300, 500, "4 títulos", 46, B, "middle")])
c.burst(L(12), [TX(200, 640, "I", 56, B, "middle"), megaphone(340, 700), TX(340, 820, "reglas para todos", 34, K, "middle")])
c.burst(L(13), [TX(600, 640, "II", 56, B, "middle"), building(680, 650, 130, 100), coin(880, 720, 34)])
c.burst(W(13, 0.62), [TX(760, 830, "bruto", 48, R, "middle")])
c.burst(L(14), [TX(200, 900, "III", 56, B, "middle"), building(260, 910, 110, 90), piggy(440, 1000), TX(330, 1100, "sus fondos", 36, K, "middle")])
c.burst(L(15), [TX(600, 900, "IV", 56, B, "middle"), factory(760, 1060), register(880, 1080), TX(760, 1120, "ventas", 36, K, "middle")])
c.erase(L(16) - 0.4)
c.burst(L(16), [TX(540, 520, "además, el proyecto trae:", 48, B, "middle")])
c.burst(W(16, 0.15), [target(270, 700), TX(270, 820, "metas", 44, K, "middle")])
c.burst(W(16, 0.38), [person(700, 640, 0.8), person(800, 640, 0.8), person(900, 640, 0.8), TX(800, 860, "cargos", 44, K, "middle")])
c.burst(W(16, 0.55), [clock(220, 1020), P(rr(290, 980, 120, 80, 4), K, 4), TX(290, 1130, "horas cátedra", 40, K, "middle")])
c.burst(W(16, 0.78), [crane(760, 1110), TX(800, 1170, "inversión", 44, K, "middle")])
chapters.append(c.build())

# ================================================================ C3 Apertura y poderes
c = Ch("c3", Bd[3], Bd[4], 3, "Apertura y poderes")
c.burst(L(18), [jar(300, 620, 300, 420), FILL(rr(170, 760, 260, 270, 14), "#bcd6fb", 1), TX(300, 590, "techo", 50, R, "middle"), TX(300, 1110, "créditos", 44, K, "middle")])
c.burst(W(18, 0.55), [cloud(770, 790, 330, 230, B), TX(770, 800, "$ ?", 60, B, "middle"), TX(770, 990, "recursos", 44, K, "middle"), TX(770, 1040, "estimativos", 44, B, "middle"), TX(800, 1200, "art. 27", 44, R, "middle")])
c.erase(L(19) - 0.4)
c.burst(L(19), [building(120, 820, 220, 160), P(f"M190,760 L250,760 M220,742 L220,760", K, 4), TX(230, 1040, "Judicial", 44, K, "middle"),
                envelope(560, 880, 300, 200), TX(560, 1050, "general", 40, B, "middle"), arrow(350, 880, 400, 880, K, 5)])
c.burst(W(19, 0.55), [person(560, 1130, 1.0, "happy", "carry"), dome(870, 1010, 220), arrow(720, 880, 760, 900, B, 5), TX(870, 1060, "Legislatura", 36, K, "middle")])
c.erase(L(20) - 0.4)
c.burst(L(20), [dome(540, 1120, 420), sheet(540, 700, 220, 260, 4), TX(540, 560, "su propio presupuesto", 44, B, "middle")])
c.burst(W(20, 0.6), [person(170, 900, 0.8), person(260, 900, 0.8), TX(215, 1140, "su personal", 38, K, "middle")])
c.erase(L(21) - 0.4)
c.burst(L(21), [dome(800, 1120, 240), shield(560, 800, 1.3), stamp_box(230, 720, "VETO", R, 56), arrow(340, 720, 470, 760, R, 5)])
c.burst(W(21, 0.25), [cross(420, 820, 1.2)])
c.burst(W(21, 0.5), [wallet(230, 1020), P("M320,1020 Q520,1150 700,1060", R, 4), TX(300, 1150, "sin recursos", 40, R, "middle"), TX(800, 1220, "art. 99 Const.", 40, R, "middle")])
c.erase(L(22) - 0.4)
c.burst(L(22), [calendar_page(250, 700, "ENERO", "1", 240, 240), cross(250, 700, 1.4), TX(250, 880, "sin ley", 44, R, "middle")])
c.burst(W(22, 0.3), [copier(700, 760), book(620, 620, 180, 90), TX(700, 950, "reconducido", 56, B, "middle"), TX(700, 1010, "art. 113", 40, R, "middle")])
c.note(L(23), "ej")
c.burst(W(23, 0.2), [book(820, 1120, 200, 110), wrench(950, 1190, B), TX(700, 1250, "anterior, ajustada", 40, B, "middle")])
c.burst(L(24), [building(160, 1050, 150, 100), P(ln(240, 998, 240, 950), K, 4), P("M240,950 l40,12 l-40,12", R, 4), cross(235, 1110, 1.6), TX(240, 1250, "obra terminada", 40, R, "middle")])
c.erase(L(25) - 0.4)
c.burst(L(25), [funnel(300, 620, 360, 300), TX(300, 690, "todo gasto", 38, K, "middle"), TX(300, 990, "→ ley", 48, B, "middle"), TX(300, 1060, "art. 112", 38, R, "middle")])
c.burst(W(25, 0.5), [sack(720, 720), arrow(720, 800, 720, 920, K, 5), P(rr(590, 930, 260, 90, 10)), TX(720, 990, "gastos ordinarios", 34, K, "middle"),
                     cross(720, 860, 1.4), TX(720, 1100, "art. 111", 38, R, "middle")])
chapters.append(c.build())

# ================================================================ C4 Presentación
c = Ch("c4", Bd[4], Bd[5], 4, "La presentación")
months = ["MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV"]
c.burst(L(26), [P("M130,700 L950,700", K, 7)] + [P(ln(150 + i * 130, 685, 150 + i * 130, 715), K, 5) for i in range(7)]
        + [TX(150 + i * 130, 660, m, 34, K, "middle") for i, m in enumerate(months)])
c.burst(W(26, 0.55), [P(circ(930, 780, 60), R, 6), TX(930, 798, "30", 50, R, "middle")])
c.burst(L(27), [person(300, 870, 1.3, "happy", "carry"), P(rr(380, 960, 140, 110, 6), K, 5), P("M380,1010 L520,1010 M450,960 L450,1070", R, 4)])
c.burst(W(27, 0.25), [P(rr(580, 900, 110, 80, 5), B, 4), TX(635, 1010, "objetivos", 30, B, "middle")])
c.burst(W(27, 0.45), [P(rr(720, 900, 110, 80, 5), B, 4), TX(775, 1010, "metodología", 30, B, "middle")])
c.burst(W(27, 0.65), [P(rr(860, 900, 110, 80, 5), B, 4), TX(915, 1010, "cta. inversión", 30, B, "middle"), TX(800, 1130, "art. 24", 40, R, "middle")])
c.burst(L(28), [FILL(rr(140, 690, 800, 20, 8), "#bcd6fb", 1), TX(540, 590, "sesiones ordinarias", 48, B, "middle"), TX(150, 760, "1 may", 34, B, "middle")])
c.erase(L(29) - 0.4)
c.burst(L(29), [hourglass(780, 800, 1.4), person(330, 820, 1.6, "worried", "carry"), sweat(400, 780), TX(330, 600, "28 o 29 nov", 56, R, "middle")])
c.burst(W(29, 0.55), [P(ln(700, 1260, 700, 1060), K, 6), P(rr(540, 980, 320, 100, 8), R, 6), TX(700, 1045, "extraordinaria", 44, R, "middle")])
c.erase(L(30) - 0.4)
c.burst(L(30), [dome(290, 980, 320), P(rr(250, 900, 80, 80, 4), B, 6), TX(290, 1040, "Diputados", 44, K, "middle"), TX(290, 1095, "iniciadora", 40, B, "middle"),
                arrow(120, 600, 260, 880, B, 6), mini_sheet(110, 560)])
c.burst(W(30, 0.6), [mini_sheet(300, 560, K, 0, "imp."), mini_sheet(440, 560, K, 0, "créd.")])
c.burst(L(31), [dome(790, 980, 320), TX(790, 1040, "Senado", 44, K, "middle"), magnifier(790, 640, 50), TX(790, 1095, "revisora", 40, R, "middle")])
c.burst(L(32), [P(rr(330, 1140, 200, 90, 8)), TX(430, 1200, "+ gasto", 42, R, "middle"), P("M530,1185 Q600,1150 640,1185", K, 4), coin(690, 1185, 40),
                TX(840, 1205, "financiamiento", 36, B, "middle"), TX(170, 1200, "art. 26", 38, R, "middle")])
chapters.append(c.build())

# ================================================================ C5 Trámite
c = Ch("c5", Bd[5], TOTAL, 5, "Trámite y promulgación")
road = "M170,600 C600,560 900,600 900,720 C900,840 200,800 180,930 C160,1060 860,1020 880,1150"
c.burst(L(34), [P(road, "#9aa3ad", 16)] + house(170, 560, 0.9) + [TX(260, 560, "Ejecutivo", 36, K)])
c.burst(W(34, 0.2), [dome(880, 690, 180), TX(700, 660, "Diputados", 40, K, "middle"), TX(700, 760, "mayoría", 36, B, "middle")])
c.burst(W(34, 0.62), [P("M820,620 Q540,500 250,560", R, 5), TX(540, 520, "observaciones", 36, R, "middle")])
c.burst(L(35), [dome(190, 920, 180), TX(370, 930, "Senadores", 40, K, "middle")])
c.burst(W(35, 0.55), stamp_box(760, 1130, "sanciona", B, 46) + [arrow(640, 1190, 500, 1250, B, 5), TX(330, 1260, "→ Ejecutivo", 40, B, "middle")])
c.erase(L(36) - 0.9)
c.burst(L(36) - 0.4, [dome(270, 900, 220), TX(270, 960, "Diputados", 40, K, "middle"), dome(810, 900, 220), TX(810, 960, "Senadores", 40, K, "middle")])
c.burst(W(36, 0.08), [arrow(680, 640, 400, 640, R, 6), TX(540, 610, "modifica", 40, R, "middle")])
c.burst(W(36, 0.62), [check(270, 560, 1.3), TX(380, 560, "acepta → sanciona", 38, B)])
c.burst(L(37), [arrow(400, 720, 680, 720, K, 6), TX(540, 770, "no acepta", 38, K, "middle"), pie23(810, 1110, 60)])
c.burst(L(38), [arrow(680, 820, 400, 820, R, 6), pie23(270, 1110, 60), TX(540, 1250, "dos tercios de sus presentes", 38, R, "middle")])
c.erase(L(39) - 0.4)
c.burst(L(39), [sheet(540, 820, 400, 520, 8), TX(540, 520, "veto parcial", 52, R, "middle")])
c.burst(W(39, 0.3), [P("M300,960 L780,960", R, 5), scissors(860, 960), TX(540, 1050, "objetada", 40, R, "middle")])
c.burst(W(39, 0.68), [check(800, 700, 1.4), TX(880, 790, "vigente", 40, B, "middle")])
c.erase(L(40) - 0.4)
c.burst(L(40), [TX(330, 700, "10", 170, B, "middle"), TX(330, 790, "días", 52, B, "middle"), hourglass(720, 700, 1.0), TX(720, 860, "art. 118", 38, R, "middle")])
c.burst(W(40, 0.5), stamp_box(330, 1000, "ES LEY", R, 64))
c.burst(W(40, 0.78), [newspaper(760, 1040), TX(760, 1170, "publicada", 40, K, "middle")])
c.erase(L(41) - 0.35)
c.burst(L(41) - 0.2, [dome(280, 900, 200), dome(800, 900, 200), TX(540, 560, "insistencia", 56, B, "middle"), TX(540, 640, "art. 120", 40, R, "middle")])
c.burst(W(41, 0.45), [TX(280, 1010, "2/3", 64, R, "middle"), TX(800, 1010, "2/3", 64, R, "middle"), sheet(540, 1110, 140, 160, 3), arrow(410, 1110, 460, 1110, R, 6), arrow(670, 1110, 620, 1110, R, 6)])
chapters.append(c.build(last=True))

# ================================================================ INDEX
hosts = "".join(
    f"""
      <div id="{cid}" style="z-index: 2" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html"
        data-start="{t0}" data-duration="{dur}" data-track-index="1" data-track-kind="graphics"
        data-width="1080" data-height="1920"></div>"""
    for cid, t0, dur in chapters)
(pz.OUT / "index.html").write_text(f"""<!doctype html>
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
