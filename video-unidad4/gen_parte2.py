"""Unidad 4 · Parte 2 (capítulos 6 a 9) en estilo pizarra, con intro de 5 s.

La voz de la Parte 2 es: intro de 5,0 s + la voz original desde la frase 42
(267,16 s). Por eso los tiempos de tiempos.json se corren -262,16 s.
"""
from pathlib import Path

import pizarra as pz
from dibujos import *  # noqa: F401,F403  (dibujos grandes de la Parte 1)
from pizarra import B, K, R, TX, FILL, P, Ch, arrow, check, circ, coin, cross, ln, magnifier, piggy, rr, house, building, ell, scale_icon

BASE = Path(__file__).parent
pz.OUT = BASE / "parte2" / "proyecto"
SHIFT = 267.16 - 5.0
pz.TT = {n: (round(a - SHIFT, 2), round(b - SHIFT, 2)) for n, (a, b) in pz.TT.items() if n >= 42}
L, W = pz.L, pz.W
TOTAL = round(pz.TT[82][1] + 1.8, 2)


def num(xr, y, txt, size=86, c=K):
    """Número alineado a la derecha en xr (cuenta vertical de cuaderno)."""
    return TX(xr - pz.tw(txt, size), y, txt, size, c)


def thermo(cx, top, h=380, c=K):
    return [P(f"M{cx - 26},{top + h - 40} L{cx - 26},{top + 20} A26,26 0 0,1 {cx + 26},{top + 20} L{cx + 26},{top + h - 40}", c, 6),
            P(f"M{cx - 26},{top + h - 40} A46,46 0 1,0 {cx + 26},{top + h - 40}", c, 6)]


def monitor(cx, cy, c=K):
    return [P(rr(cx - 230, cy - 150, 460, 290, 14), c, 7), P(f"M{cx - 60},{cy + 140} L{cx - 80},{cy + 200} L{cx + 80},{cy + 200} L{cx + 60},{cy + 140}", c, 6)]


def padlock(cx, cy, c=R):
    return [P(rr(cx - 50, cy - 10, 100, 80, 10), c, 6), P(f"M{cx - 32},{cy - 10} L{cx - 32},{cy - 40} A32,32 0 0,1 {cx + 32},{cy - 40} L{cx + 32},{cy - 10}", c, 6)]


def siren(cx, cy, c=R):
    return [P(f"M{cx - 50},{cy + 30} L{cx - 50},{cy} A50,50 0 0,1 {cx + 50},{cy} L{cx + 50},{cy + 30} Z", c, 6), P(rr(cx - 70, cy + 30, 140, 24, 4), K, 5),
            P(f"M{cx - 90},{cy - 40} L{cx - 70},{cy - 25} M{cx},{cy - 80} L{cx},{cy - 60} M{cx + 90},{cy - 40} L{cx + 70},{cy - 25}", c, 5)]


def drawer(x, y, w=230, h=110, label="", c=K):
    return [P(rr(x, y, w, h, 8), c, 5), P(rr(x + w / 2 - 30, y + h / 2 - 8, 60, 16, 6), c, 4), TX(x + w / 2, y + h + 46, label, 36, c, "middle")]


def glass(cx, top, w=170, h=300, c=K):
    return [P(f"M{cx - w / 2},{top} L{cx - w / 2 + 20},{top + h} L{cx + w / 2 - 20},{top + h} L{cx + w / 2},{top}", c, 6)]


def ballot(cx, cy, c=K):
    return [P(rr(cx - 60, cy - 40, 120, 90, 6), c, 5), P(ln(cx - 30, cy - 40, cx + 30, cy - 40), c, 8), P(rr(cx - 24, cy - 80, 48, 50, 3), c, 4)]


def pipe_valve(cx, cy, c=K):
    return [P(f"M{cx - 90},{cy - 16} L{cx + 90},{cy - 16} M{cx - 90},{cy + 16} L{cx + 90},{cy + 16}", c, 5), P(circ(cx, cy, 24), R, 6), P(ln(cx - 18, cy - 18, cx + 18, cy + 18), R, 6)]


def signature(cx, cy, c=K):
    return [P(f"M{cx - 80},{cy} Q{cx - 50},{cy - 50} {cx - 20},{cy} Q{cx + 10},{cy + 40} {cx + 30},{cy - 10} L{cx + 80},{cy + 10}", c, 5), P(ln(cx - 90, cy + 30, cx + 90, cy + 30), c, 3)]


def flag(cx, base, txt, c=B):
    return [P(ln(cx, base, cx, base - 220), K, 6), P(f"M{cx},{base - 220} L{cx + 160},{base - 190} L{cx},{base - 160} Z", c, 5), TX(cx + 10, base + 50, txt, 42, c, "middle")]


def backpack_person(cx, cy):
    return person(cx, cy, 1.6, "worried") + [P(rr(cx - 110, cy + 60, 80, 110, 12), R, 6), TX(cx - 70, cy + 230, "impuestos", 36, R, "middle")]


chapters = []
Bd = [0, 5.0, 115.25, 229.37, 292.61, TOTAL]

# ================================================================ INTRO 5 s
c = Ch("c0", Bd[0], Bd[1], 0, None)
c.burst(0.15, [TX(540, 700, "UNIDAD 4", 120, B, "middle"), P("M280,740 Q540,720 800,744", R, 8), TX(540, 840, "Parte 2", 64, R, "middle")])
c.burst(1.9, [arrow(380, 960, 700, 960, B, 8), TX(540, 1060, "seguimos...", 56, K, "middle")])
chapters.append(c.build())

# ================================================================ C6 Responsabilidad fiscal
c = Ch("c6", Bd[1], Bd[2], 6, "Responsabilidad fiscal")
c.burst(L(43), flag(220, 820, "Catamarca") + [book(560, 700, 260, 170), TX(560, 700, "Ley 5144", 46, B, "middle")])
c.burst(W(43, 0.6), [TX(560, 870, "reglas fiscales", 44, K, "middle"), TX(560, 930, "transparencia", 44, B, "middle")])
c.burst(L(44), [P(ell(560, 1130, 260, 70), K, 6), face(380, 1060, 30), face(480, 1040, 30), face(640, 1040, 30), face(740, 1060, 30),
                arrow(280, 900, 340, 1040, B, 5), TX(560, 1250, "Consejo Federal", 44, B, "middle")])
c.erase(L(45) - 0.4)
c.burst(L(45), sack(540, 900) + [TX(540, 560, "universalidad", 56, B, "middle")])
c.burst(W(45, 0.3), coin(300, 700) + coin(780, 680) + [mini_sheet(380, 640), mini_sheet(700, 760), arrow(330, 740, 450, 860, K, 4), arrow(740, 720, 620, 860, K, 4)])
c.burst(W(45, 0.75), [TX(540, 1180, "todo, por su monto íntegro", 46, R, "middle")])
c.erase(L(46) - 0.4)
c.burst(L(46), [TX(540, 540, "plurianual", 56, B, "middle")] + calendar_page(230, 760, "año 1", "", 200, 200) + calendar_page(540, 760, "año 2", "", 200, 200) + calendar_page(850, 760, "año 3", "", 200, 200))
c.burst(W(46, 0.45), magnifier(400, 1010, 50) + [TX(400, 1170, "informativo", 46, B, "middle")] + dome(780, 1130, 220) + cross(780, 980, 1.2))
c.erase(L(47) - 0.4)
c.burst(L(47), monitor(540, 720) + [TX(540, 700, "web", 80, B, "middle"), TX(540, 780, "presupuesto · proyecciones", 34, K, "middle")])
c.burst(W(47, 0.55), [P(rr(130 + k * 210, 1000, 190, 110, 10), K, 5) for k in range(4)] + [TX(225 + k * 210, 1070, f"T{k + 1}", 44, B, "middle") for k in range(4)]
        + [TX(540, 1180, "ejecución · deuda · empleo", 42, R, "middle")])
c.erase(L(48) - 0.4)
c.burst(L(48), backpack_person(560, 760) + [arrow(800, 1000, 800, 700, R, 8), cross(800, 850, 1.5), TX(540, 560, "presión tributaria", 52, B, "middle")])
c.burst(W(48, 0.6), [TX(560, 1210, "trabajo · producción", 44, K, "middle")])
c.erase(L(49) - 0.4)
c.burst(L(49), thermo(330, 600) + thermo(750, 600) + [TX(330, 1080, "IPC", 52, B, "middle"), TX(750, 1080, "gasto", 52, K, "middle"), TX(540, 540, "gasto corriente primario", 48, B, "middle")])
c.note(L(50), "ej")
c.burst(W(50, 0.15), [FILL(rr(310, 760, 40, 220, 10), "#bcd6fb"), P("M260,760 L820,760", R, 5), TX(540, 740, "30 %", 56, R, "middle")])
c.burst(W(50, 0.55), [FILL(rr(730, 760, 40, 220, 10), "#ffd0d0"), arrow(860, 820, 860, 700, R, 6), cross(860, 700, 1.1)])
c.burst(L(51), padlock(540, 1170) + [TX(240, 1190, "déficit", 44, R, "middle"), TX(840, 1190, "deuda > 15 %", 44, R, "middle")])
c.erase(L(52) - 0.4)
c.burst(L(52), scale_icon(540, 820, 2.0) + person(330, 620, 0.7) + person(400, 620, 0.7) + house(700, 690, 0.8) + house(790, 690, 0.8)
        + [TX(360, 940, "cargos", 42, K, "middle"), TX(740, 940, "habitantes", 42, K, "middle"), TX(540, 540, "empleo público", 52, B, "middle")])
c.burst(W(52, 0.65), calendar_page(540, 1130, "base", "", 280, 170) + [TX(540, 1170, "31/12/2017", 50, R, "middle")])
c.erase(L(53) - 0.4)
c.burst(L(53), hourglass(280, 800, 1.3) + [TX(280, 1050, "últimos 2", 42, R, "middle"), TX(280, 1100, "trimestres", 42, R, "middle"), TX(540, 540, "fin de mandato", 52, B, "middle")])
c.burst(W(53, 0.4), person(720, 720, 1.4, "happy", "up") + [P(rr(800, 620, 190, 90, 8), K, 5), TX(895, 680, "+ sueldos", 40, K, "middle"), cross(800, 1000, 1.6)])
c.erase(L(54) - 0.4)
c.burst(L(54), [P(rr(250, 600, 140, 560, 10), K, 6), FILL(rr(256, 900, 128, 254, 8), "#bcd6fb"), P("M200,830 L440,830", R, 6), TX(540, 845, "15 %", 64, R),
                TX(540, 540, "servicios de la deuda", 50, B, "middle")])
c.burst(W(54, 0.45), [arrow(320, 790, 320, 640, R, 6), P(rr(560, 900, 380, 80, 10), R, 6), TX(750, 955, "deuda nueva", 40, R, "middle"), cross(910, 940, 0.9)])
c.burst(W(54, 0.75), check(590, 1080, 1.0, B) + [TX(640, 1095, "refinanciar mejorando", 38, B)])
c.erase(L(55) - 0.4)
c.burst(L(55), [TX(540, 540, "sanciones", 60, R, "middle")] + megaphone(270, 720) + [TX(300, 840, "se publica", 38, K, "middle")])
c.burst(W(55, 0.35), ballot(780, 720) + cross(780, 720, 1.4) + [TX(780, 840, "voto", 38, K, "middle")])
c.burst(W(55, 0.6), signature(270, 1040) + cross(270, 1040, 1.3) + [TX(270, 1130, "avales", 38, K, "middle")])
c.burst(W(55, 0.8), pipe_valve(780, 1040) + [TX(780, 1130, "transferencias", 38, K, "middle")])
chapters.append(c.build())

# ================================================================ C7 Cálculos
c = Ch("c7", Bd[2], Bd[3], 7, "Cálculos del resultado")
XR = 700
c.burst(L(57), [TX(540, 560, "resultado económico", 56, B, "middle"), TX(540, 640, "recursos ctes. − gastos ctes.", 44, K, "middle")])
c.note(L(58), "ej")
c.burst(W(58, 0.25), [num(XR, 820, "100")])
c.burst(W(58, 0.45), [num(XR, 920, "− 80")])
c.burst(W(58, 0.62), [P(ln(XR - 260, 950, XR + 10, 950), K, 6), num(XR, 1050, "20", 96, B), TX(780, 1040, "ahorro", 52, B)] + piggy(300, 1000))
c.erase(L(59) - 0.4)
c.burst(L(59), [TX(540, 560, "resultado financiero", 56, B, "middle"), TX(540, 640, "económico + rec. capital", 42, K, "middle"), TX(540, 700, "− gastos de capital", 42, K, "middle")])
c.note(L(60), "ej")
c.burst(W(60, 0.25), [num(XR, 820, "20")])
c.burst(W(60, 0.4), [num(XR, 910, "+ 10")])
c.burst(W(60, 0.55), [num(XR, 1000, "− 50")])
c.burst(W(60, 0.7), [P(ln(XR - 260, 1030, XR + 10, 1030), K, 6), num(XR, 1130, "−20", 96, R), TX(780, 1120, "déficit", 52, R)] + piggy(300, 1060) + [P("M290,1010 L310,1050 L295,1090", R, 5)])
c.erase(L(61) - 0.4)
c.burst(L(61), [TX(540, 560, "necesidad de financiamiento", 52, B, "middle"), TX(540, 640, "financiero + fuentes", 42, K, "middle"), TX(540, 700, "− aplicaciones", 42, K, "middle")])
c.note(L(62), "pe")
c.burst(W(62, 0.3), [num(XR, 840, "−20")])
c.burst(W(62, 0.45), [num(XR, 930, "+ 30"), TX(740, 920, "fuentes", 40, B)])
c.burst(W(62, 0.65), [num(XR, 1020, "− 10"), TX(740, 1010, "aplicaciones", 40, B)])
c.burst(W(62, 0.85), [P(ln(XR - 260, 1050, XR + 10, 1050), K, 6), num(XR, 1150, "0", 96, B)])
c.erase(L(63) - 0.4)
c.burst(L(63), [TX(320, 560, "devengado", 52, B, "middle"), TX(760, 560, "caja", 52, R, "middle"), P("M540,520 L540,960", K, 4)])
c.burst(W(63, 0.25), [TX(320, 660, "recursos percibidos", 36, K, "middle"), TX(760, 660, "recursos percibidos", 36, K, "middle")])
c.burst(W(63, 0.6), [TX(320, 760, "gastos devengados", 38, B, "middle"), TX(760, 760, "gastos pagados", 38, R, "middle")])
c.erase(L(64) - 0.4)
c.note(L(64), "ej")
c.burst(W(64, 0.15), sheet(540, 700, 220, 260, 4) + [TX(540, 800, "factura", 40, K, "middle")])
c.burst(W(64, 0.5), calendar_page(250, 1020, "DIC", "", 220, 200) + calendar_page(830, 1020, "ENE", "", 220, 200))
c.burst(L(65), [arrow(470, 820, 330, 930, B, 7), TX(260, 1080, "devengado", 40, B, "middle")])
c.burst(W(65, 0.55), [arrow(610, 820, 750, 930, R, 7), TX(830, 1080, "caja", 44, R, "middle")])
c.erase(L(66) - 0.4)
c.burst(L(66), [TX(540, 560, "resultado primario", 56, B, "middle"), TX(540, 640, "financiero sin intereses", 44, K, "middle")])
c.note(L(67), "ej")
c.burst(W(67, 0.25), [num(XR, 840, "−20"), TX(740, 830, "déficit", 44, R)])
c.burst(W(67, 0.5), [num(XR, 940, "5"), TX(740, 930, "intereses", 44, K), P(ln(420, 912, 980, 912), R, 6)])
c.burst(W(67, 0.75), [P(ln(XR - 260, 970, XR + 10, 970), K, 6), num(XR, 1080, "−15", 96, B), TX(740, 1070, "primario", 48, B)])
c.erase(L(68) - 0.4)
c.burst(L(68), [P(rr(300, 520, 480, 140, 14), B, 7), TX(540, 580, "gasto corriente", 44, B, "middle"), TX(540, 630, "primario", 44, B, "middle")])
c.burst(W(68, 0.35), [arrow(380, 670, 230, 800, R, 5), TX(230, 860, "préstamos", 36, K, "middle"), TX(230, 900, "internacionales", 36, K, "middle")])
c.burst(W(68, 0.58), [arrow(540, 670, 540, 800, R, 5), TX(540, 860, "transferencias", 36, K, "middle"), TX(540, 900, "a municipios", 36, K, "middle")])
c.burst(W(68, 0.8), [arrow(700, 670, 850, 800, R, 5), TX(850, 860, "aportes no", 36, K, "middle"), TX(850, 900, "automáticos", 36, K, "middle")])
c.erase(L(69) - 0.3)
c.note(L(69), "pe")
c.burst(W(69, 0.25), [num(XR, 680, "100")])
c.burst(W(69, 0.4), [num(XR, 770, "− 10")])
c.burst(W(69, 0.52), [num(XR, 860, "− 20")])
c.burst(W(69, 0.65), [num(XR, 950, "− 5")])
c.burst(W(69, 0.8), [P(ln(XR - 260, 980, XR + 10, 980), K, 6), num(XR, 1090, "65", 96, B), TX(740, 1080, "neto", 52, B)])
c.erase(L(70) - 0.4)
c.burst(L(70), [TX(540, 560, "indicador de endeudamiento", 50, B, "middle"), TX(540, 680, "servicios de la deuda", 42, K, "middle"),
                P(ln(240, 710, 840, 710), K, 6), TX(540, 770, "recursos ctes. netos", 42, K, "middle")])
c.note(L(71), "ej")
c.burst(W(71, 0.15), [TX(360, 940, "120", 86, K, "middle"), P(ln(250, 970, 470, 970), K, 6), TX(360, 1060, "1.000", 86, K, "middle")])
c.burst(W(71, 0.45), [TX(560, 1000, "=", 86, K, "middle"), TX(730, 1010, "12 %", 96, B, "middle")])
c.burst(W(71, 0.7), [P(rr(160, 1140, 760, 50, 25), K, 5), P("M170,1165 L620,1165", B, 30), P("M730,1120 L730,1210", R, 6), TX(760, 1250, "tope 15 %", 40, R, "middle")] + check(950, 1100, 1.0, B))
chapters.append(c.build())

# ================================================================ C8 Reestructuraciones
c = Ch("c8", Bd[3], Bd[4], 8, "Reestructuraciones")
c.note(L(72), "ej")
c.burst(W(72, 0.4), [book(540, 780, 420, 250), TX(540, 760, "Presupuesto", 46, B, "middle"), TX(540, 820, "2023", 64, R, "middle")])
c.erase(L(73) - 0.4)
c.burst(L(73), [TX(540, 540, "Poder Ejecutivo", 52, B, "middle")] + drawer(90, 630, label="personal") + drawer(420, 630, label="transferencias") + drawer(750, 630, label="deuda"))
c.burst(W(73, 0.7), [TX(540, 900, "∞", 130, B, "middle"), TX(540, 960, "sin límite", 44, B, "middle")])
c.burst(L(74), [TX(300, 1110, "resto de incisos", 42, K, "middle"), P(rr(560, 1040, 260, 110, 12), R, 6), TX(690, 1115, "máx. 36", 54, R, "middle")])
c.burst(W(74, 0.65), siren(920, 1080) + [P(ln(570, 1150, 810, 1045), K, 5), TX(900, 1220, "emergencia", 38, R, "middle")])
c.erase(L(75) - 0.4)
c.burst(L(75), [P(rr(130, 600, 320, 300, 14), K, 5), P(rr(630, 600, 320, 300, 14), K, 5), TX(290, 950, "área A", 40, K, "middle"), TX(790, 950, "área B", 40, K, "middle")]
        + [P(rr(170 + (k % 3) * 90, 640 + (k // 3) * 90, 70, 70, 6), B, 4) for k in range(5)] + [arrow(460, 750, 620, 750, B, 6), TX(540, 1040, "= total", 60, R, "middle")])
c.burst(W(75, 0.6), calendar_page(330, 1180, "últimos 6 meses", "", 340, 160) + [person(800, 1080, 0.7, "worried"), cross(800, 1150, 1.2), TX(820, 1290, "no contratar", 38, R, "middle")])
c.erase(L(76) - 0.4)
c.burst(L(76), dome(220, 880, 220) + building(440, 790, 200, 110) + ministry(860, 880, 240)
        + [TX(220, 950, "Legislativo", 36, K, "middle"), TX(540, 950, "Judicial", 36, K, "middle"), TX(860, 950, "Trib. Cuentas", 36, K, "middle")])
c.burst(W(76, 0.45), [TX(540, 1050, "= total de su jurisdicción", 46, R, "middle")])
c.burst(W(76, 0.7), envelope(380, 1180, 220, 140) + [arrow(510, 1180, 620, 1180, B, 6), TX(800, 1195, "Dirección", 44, B, "middle")])
c.erase(L(77) - 0.4)
c.burst(L(77), sack(300, 820) + [TX(300, 960, "deuda nueva", 44, B, "middle")] + sack(780, 820) + [TX(780, 960, "deuda vieja", 44, K, "middle"), arrow(410, 800, 650, 800, B, 7), TX(540, 760, "cancela", 40, B, "middle")])
c.burst(W(77, 0.6), [TX(540, 1120, "o la reestructura", 50, R, "middle")])
c.erase(L(78) - 0.4)
c.burst(L(78), jar(540, 600, 360, 440) + [TX(540, 580, "autorizado", 44, R, "middle"), arrow(460, 860, 620, 760, B, 6), arrow(620, 940, 460, 1000, B, 6)])
c.burst(W(78, 0.6), [P(rr(780, 860, 180, 100, 10), R, 5), TX(870, 925, "+ $", 50, R, "middle"), cross(870, 910, 1.4)])
c.erase(L(79) - 0.4)
c.note(L(79), "ej")
c.burst(W(79, 0.1), glass(330, 640) + glass(750, 640) + [FILL("M262,760 L276,940 L384,940 L398,760 Z", "#bcd6fb"), FILL("M688,820 L700,940 L800,940 L812,820 Z", "#ffe27a"),
                                                          TX(330, 1000, "servicios", 42, K, "middle"), TX(750, 1000, "bienes de consumo", 40, K, "middle")])
c.burst(W(79, 0.45), [arrow(420, 720, 650, 720, B, 7), P("M120,1080 L960,1080", R, 4), TX(540, 1150, "el total no cambia", 48, R, "middle")])
chapters.append(c.build())

# ================================================================ CIERRE
c = Ch("c9", Bd[4], Bd[5], "?", "Pregunta de repaso")
c.burst(L(80), [TX(540, 520, "una pregunta del apunte", 46, B, "middle")])
c.burst(L(81), house(250, 700, 1.4) + [P(ln(250, 640, 250, 580), K, 4), P("M250,580 l50,14 l-50,14", R, 4), TX(250, 840, "municipio", 40, K, "middle")])
c.burst(W(81, 0.2), [TX(470, 640, "recursos ctes. $100", 42, K), TX(470, 710, "gastos ctes. $120", 42, K), TX(470, 780, "intereses $10", 42, K)])
c.burst(W(81, 0.65), [TX(540, 980, "100 − 120 = ?", 96, R, "middle"), TX(540, 1080, "resultado económico", 46, B, "middle")])
c.burst(L(82), [TX(540, 1220, "Hacé la cuenta y respondé", 48, B, "middle")])
chapters.append(c.build(last=True))

# ================================================================ INDEX
hosts = "".join(
    f"""
      <div id="{cid}" style="z-index: 2" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html"
        data-start="{t0}" data-duration="{dur}" data-track-index="1" data-track-kind="graphics"
        data-width="1080" data-height="1920"></div>"""
    for cid, t0, dur in chapters)
(pz.OUT / "index.html").write_text((BASE / "parte1/proyecto/index.html").read_text().split('<div id="c0"')[0].replace('data-duration="268.0"', f'data-duration="{TOTAL}"').rstrip()
                                   + hosts + """
      <audio id="voz" class="clip" src="assets/voz.wav" data-start="0" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
""")
for ch in chapters:
    print(ch)
print("TOTAL", TOTAL)
