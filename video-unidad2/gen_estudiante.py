"""Genera compositions/estudiante.html de la Unidad 2.

Reusa el dibujo de la estudiante de la Unidad 1, le suma accesorios
(lápiz, moneda, escudo, birrete, curita) y escribe su actuación,
sincronizada con tiempos.json. Entre acciones toma apuntes o sigue el
pizarrón con la mirada, así nunca queda quieta.
"""
import json
import re
from pathlib import Path

BASE = Path(__file__).parent
U1 = (BASE.parent / "video-unidad1/proyecto/compositions/estudiante.html").read_text()
svg = re.search(r'(<svg id="est-svg".*?</svg>)', U1, re.S).group(1)

svg = svg.replace(
    '<circle cx="588" cy="1172" r="26" fill="#f5c9a0" />',
    '''<g id="est-lapiz" class="est-h">
            <path d="M590,1176 L556,1104" stroke="#fdcb6e" stroke-width="12" stroke-linecap="round" />
            <path d="M556,1104 L550,1090" stroke="#2d3436" stroke-width="6" stroke-linecap="round" />
            <path d="M594,1184 L590,1176" stroke="#ff7675" stroke-width="12" />
          </g>
          <g id="est-moneda" class="est-h">
            <circle cx="588" cy="1126" r="26" fill="#fdcb6e" stroke="#e1a940" stroke-width="5" />
            <text x="588" y="1137" font-size="30" text-anchor="middle" fill="#b7791f" font-family="Nunito" font-weight="900">$</text>
          </g>
          <circle cx="588" cy="1172" r="26" fill="#f5c9a0" />''', 1)
svg = svg.replace(
    '<circle cx="492" cy="1172" r="26" fill="#f5c9a0" />',
    '''<g id="est-escudo" class="est-h">
            <path d="M492,1080 L548,1100 L548,1150 Q548,1196 492,1218 Q436,1196 436,1150 L436,1100 Z" fill="#0984e3" stroke="#ffffff" stroke-width="6" />
            <path d="M470,1150 L488,1168 L518,1130" stroke="#ffffff" stroke-width="9" fill="none" stroke-linecap="round" />
          </g>
          <circle cx="492" cy="1172" r="26" fill="#f5c9a0" />''', 1)
svg = svg.replace(
    '<g id="est-casco" class="est-h">',
    '''<g id="est-birrete" class="est-h">
            <path d="M540,612 L680,660 L540,708 L400,660 Z" fill="#2d3436" />
            <rect x="470" y="672" width="140" height="44" fill="#2d3436" />
            <path d="M650,650 L650,720" stroke="#fdcb6e" stroke-width="6" />
            <circle cx="650" cy="724" r="9" fill="#fdcb6e" />
          </g>
          <g id="est-curita" class="est-h">
            <rect x="590" y="856" width="64" height="24" rx="12" fill="#ffeaa7" transform="rotate(-20 622 868)" />
            <rect x="612" y="858" width="20" height="20" rx="4" fill="#fab1a0" transform="rotate(-20 622 868)" />
          </g>
          <g id="est-casco" class="est-h">''', 1)
svg = svg.replace('id="est-svg"', 'id="est-svg"')

T = {x["n"]: (x["ini"], x["fin"]) for x in json.loads((BASE / "tiempos.json").read_text())}


def W(n, frac):
    a, b = T[n]
    return round(a + (b - a) * frac, 2)


TOTAL = 345.6
WALLS = [  # (inicio del capítulo, pared, piso)
    (12.16, "#7c6cf2", "#4a3fa8"),
    (54.51, "#2fb383", "#1f7d5b"),
    (95.08, "#3d8bd9", "#255f9c"),
    (160.9, "#3478c2", "#20578f"),
    (197.95, "#f39c4a", "#b96a22"),
    (258.26, "#e0607e", "#a33f59"),
    (310.12, "#20a4a8", "#137478"),
    (331.49, "#7c6cf2", "#4a3fa8"),
]

acts = []  # líneas de JS
a = acts.append
for t, w, f in WALLS:
    a(f'tl.to("#est-wall", {{ fill: "{w}", duration: 0.6 }}, {round(t - 0.6, 2)});')
    a(f'tl.to("#est-floor", {{ fill: "{f}", duration: 0.6 }}, {round(t - 0.6, 2)});')

# ---------- INTRO ----------
a('tl.fromTo("#est-eyes", { x: 0, y: -10 }, { x: -8, y: -10, duration: 0.4 }, 0);')
a('armR(-150, 0.3, 0.6);')
a('mouth("open", 0.5);')
a('armR(-20, 1.65, 0.2);')
a('surprised(1.65, 2.6);')
a('shake(3.2);')
a('look(0, -10, 4.3); nod(5.6);')
a('write(6.9, 9.5);')
a('aha(9.6); vis("#est-bulb", 11.6, false);')
# ---------- C1 ----------
a('look(0, -10, 12.3);')
a('write(15.0, 19.5);')
a(f'follow([[-12, -8], [12, -8], [-6, -10], [10, -10]], {W(6, 0.05)}, {W(6, 0.95)});')
a(f'look(-12, -9, {W(7, 0.1)}); look(12, -9, {W(7, 0.6)}); nod({W(7, 0.85)});')
a(f'stamp({W(8, 0.25)}, "#est-sello");')
a(f'tl.to("#est-head", {{ rotation: 6, svgOrigin: NECK, duration: 0.45, yoyo: true, repeat: 7, ease: "sine.inOut" }}, {W(9, 0.05)});')
a(f'write({W(10, 0.0)}, {W(12, 0.3)});')
a('coverMouth(47.2, 49.0);')
a(f'nod({W(13, 0.1)}); write({W(13, 0.4)}, 54.2);')
# ---------- C2 ----------
a('look(0, -10, 54.6);')
a(f'write({W(15, 0.05)}, {W(15, 0.95)});')
a(f'typing({W(16, 0.1)}, {W(16, 0.98)});')
a(f'nod({W(17, 0.2)}); nod({W(17, 0.6)});')
a(f'look(0, -10, {W(18, 0.0)}); stamp({W(18, 0.8)}, "#est-sello");')
a(f'follow([[-14, -6], [14, -6], [-14, -6], [14, -6], [0, -8]], {W(19, 0.05)}, {W(19, 0.98)});')
a(f'write({W(20, 0.05)}, {W(20, 0.98)});')
a(f'guard({W(21, 0.05)}, {W(21, 0.98)});')
a(f'look(0, -10, {W(22, 0.0)}); nod({W(22, 0.65)});')
# ---------- C3 (1.ª parte) ----------
a('look(0, -10, 95.2);')
a(f'push({W(24, 0.2)}, {W(24, 0.55)}); mouth("smile", {W(24, 0.8)});')
a(f'tl.to("#est-head", {{ rotation: -5, svgOrigin: NECK, duration: 0.6, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {W(25, 0.05)});')
a(f'nod({W(26, 0.85)});')
a(f'worried({W(27, 0.15)}, {W(27, 0.85)});')
a(f'think({W(28, 0.05)}, {W(28, 0.98)});')
a(f'write({W(29, 0.05)}, {W(29, 0.6)}); aha({W(29, 0.7)}); vis("#est-bulb", {W(29, 0.98)}, false);')
a(f'look(0, -10, {W(30, 0.0)});')
a(f'follow([[-14, -6], [0, -9], [14, -6]], {W(31, 0.05)}, {W(31, 0.98)});')
a(f'write({W(32, 0.02)}, {W(32, 0.5)}); shake({W(32, 0.62)});')
a(f'nod({W(33, 0.5)});')
a(f'follow([[-12, -10], [-6, 0], [0, 4], [8, -4]], {W(34, 0.0)}, {W(34, 0.98)});')
a(f'look(0, -10, {W(35, 0.0)}); nod({W(35, 0.6)});')
a(f'carryCoin({W(36, 0.2)}, {W(36, 0.97)});')
# ---------- C3 (2.ª parte) ----------
a('surprised(161.0, 162.4);')
a(f'point({W(37, 0.05)}, {W(37, 0.9)});')
a(f'think({W(38, 0.02)}, {W(38, 0.4)}); aha({W(38, 0.42)}); vis("#est-bulb", {W(38, 0.98)}, false);')
a(f'write({W(39, 0.02)}, {W(39, 0.6)}); coverMouth({W(39, 0.75)}, {W(39, 0.99)});')
a(f'follow([[-14, -8], [-5, -9], [5, -9], [14, -8]], {W(40, 0.05)}, {W(40, 0.98)});')
a(f'shrug({W(41, 0.55)}, {W(41, 0.98)});')
a(f'write({W(42, 0.05)}, {W(42, 0.95)});')
a(f'cheer({W(43, 0.12)}, {W(43, 0.42)}); shake({W(43, 0.62)});')
# ---------- C4 ----------
a('look(0, -10, 198.1);')
a(f'write({W(45, 0.05)}, {W(45, 0.95)});')
a(f'point({W(46, 0.05)}, {W(46, 0.95)});')
a(f'follow([[0, -12], [-12, -4], [0, -4], [12, -4]], {W(47, 0.02)}, {W(47, 0.98)});')
a(f'nod({W(48, 0.3)}); nod({W(48, 0.75)});')
a(f'look(-10, -8, {W(49, 0.0)}); nod({W(49, 0.75)});')
a(f'follow([[-12, -10], [-12, -2], [10, -10], [10, -2], [0, -8]], {W(50, 0.02)}, {W(50, 0.98)});')
a(f'look(0, -10, {W(51, 0.0)}); mouth("smile", {W(51, 0.1)});')
a(f'think({W(52, 0.05)}, {W(52, 0.95)});')
a(f'point({W(53, 0.05)}, {W(53, 0.95)});')
a(f'follow([[-14, -6], [-5, -6], [5, -6], [14, -6]], {W(54, 0.05)}, {W(54, 0.98)});')
a(f'brrr({W(55, 0.02)}, {W(55, 0.98)});')
# ---------- C5 ----------
a('look(0, -10, 258.4);')
a(f'write({W(57, 0.05)}, {W(57, 0.95)});')
a(f'look(-8, -9, {W(58, 0.0)}); surprised({W(58, 0.45)}, {W(58, 0.72)}); shrug({W(58, 0.75)}, {W(58, 0.99)});')
a(f'look(0, -10, {W(59, 0.0)}); nod({W(59, 0.6)});')
a(f'point({W(60, 0.25)}, {W(60, 0.6)}); cheer({W(60, 0.68)}, {W(60, 0.97)});')
a(f'think({W(61, 0.02)}, {W(61, 0.4)}); surprised({W(61, 0.45)}, {W(61, 0.8)});')
a(f'write({W(62, 0.02)}, {W(62, 0.55)}); worried({W(62, 0.6)}, {W(62, 0.99)});')
a(f'look(0, -10, {W(63, 0.0)}); nod({W(63, 0.7)});')
a(f'pop("#est-curita", {W(64, 0.15)}); mouth("smile", {W(64, 0.2)}); point({W(64, 0.4)}, {W(64, 0.9)});')
a(f'vis("#est-curita", {W(64, 0.99)}, false);')
# ---------- C6 ----------
a('look(0, -10, 310.3);')
a(f'think({W(66, 0.02)}, {W(66, 0.98)});')
a(f'look(-12, -8, {W(67, 0.1)});')
a(f'nod({W(68, 0.2)}); look(0, -9, {W(68, 0.3)}); nod({W(68, 0.55)}); look(12, -9, {W(68, 0.6)}); nod({W(68, 0.85)});')
a(f'pop("#est-birrete", {W(68, 0.9)});')
a(f'cheer({W(69, 0.05)}, {W(69, 0.6)}); nod({W(69, 0.8)});')
# ---------- CIERRE ----------
a('vis("#est-birrete", 331.4, false);')
a('look(0, -10, 331.6);')
a(f'think({W(71, 0.02)}, {W(71, 0.98)});')
a(f'armR(-150, {W(72, 0.05)}, 0.45); vis("#est-thumb", {W(72, 0.12)}, true); mouth("open", {W(72, 0.05)});')
a(f'tl.to("#est-arm-r", {{ rotation: -140, svgOrigin: SH_R, duration: 0.25, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {W(72, 0.3)});')
a('mouth("smile", 344.2);')

RIG = r"""
    const tl = gsap.timeline({ paused: true });
    const C = "50% 50%";
    const SH_L = "432 1002";
    const SH_R = "648 1002";
    const NECK = "540 930";
    function pop(sel, t) {
      tl.set(sel, { scale: 0, transformOrigin: C }, t);
      tl.to(sel, { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.4)" }, t);
    }
    function vis(sel, t, on) { tl.to(sel, { opacity: on ? 1 : 0, duration: 0.12 }, t); }
    function mouth(state, t) {
      tl.to("#est-m-smile", { opacity: state === "smile" ? 1 : 0, duration: 0.1 }, t);
      tl.to("#est-m-flat", { opacity: state === "flat" ? 1 : 0, duration: 0.1 }, t);
      tl.to("#est-m-open", { opacity: state === "open" ? 1 : 0, duration: 0.1 }, t);
    }
    function armR(rot, t, d) { tl.to("#est-arm-r", { rotation: rot, svgOrigin: SH_R, duration: d || 0.4, ease: "back.out(1.7)" }, t); }
    function armL(rot, t, d) { tl.to("#est-arm-l", { rotation: rot, svgOrigin: SH_L, duration: d || 0.4, ease: "back.out(1.7)" }, t); }
    function head(rot, y, t, d) { tl.to("#est-head", { rotation: rot, y: y, svgOrigin: NECK, duration: d || 0.35, ease: "power2.out" }, t); }
    function look(x, y, t) { tl.to("#est-eyes", { x: x, y: y, duration: 0.25, ease: "power2.out" }, t); }
    function brows(y, t) { tl.to("#est-brows", { y: y, duration: 0.2, ease: "back.out(3)" }, t); }
    function follow(pts, t0, t1) {
      const step = (t1 - t0) / pts.length;
      pts.forEach((p, i) => look(p[0], p[1], t0 + i * step));
    }
    function nod(t) { tl.to("#est-head", { y: 10, svgOrigin: NECK, duration: 0.16, yoyo: true, repeat: 3, ease: "sine.inOut" }, t); }
    function shake(t) { tl.to("#est-head", { rotation: 7, svgOrigin: NECK, duration: 0.12, yoyo: true, repeat: 5, ease: "sine.inOut" }, t); }
    // Toma apuntes: lápiz en la mano, vista abajo, brazo que va y viene
    function write(t0, t1) {
      if (t1 - t0 < 0.8) return;
      vis("#est-lapiz", t0, true);
      look(-4, 14, t0);
      head(3, 4, t0);
      armR(-6, t0, 0.25);
      const n = Math.max(1, Math.floor((t1 - t0 - 0.5) / 0.3));
      tl.to("#est-arm-r", { rotation: -13, svgOrigin: SH_R, duration: 0.15, yoyo: true, repeat: n % 2 ? n : n - 1, ease: "sine.inOut" }, t0 + 0.25);
      armR(0, t1 - 0.25, 0.25);
      vis("#est-lapiz", t1 - 0.1, false);
      look(0, -8, t1 - 0.2);
      head(0, 0, t1 - 0.2);
    }
    function typing(t0, t1) {
      pop("#est-calcu", t0);
      look(14, 8, t0 + 0.2);
      armR(-14, t0 + 0.2, 0.2);
      const n = Math.max(1, Math.floor((t1 - t0 - 0.8) / 0.28));
      tl.to("#est-arm-r", { rotation: -6, svgOrigin: SH_R, duration: 0.14, yoyo: true, repeat: n % 2 ? n : n - 1, ease: "sine.inOut" }, t0 + 0.45);
      armR(0, t1 - 0.3, 0.3);
      vis("#est-calcu", t1, false);
      look(0, -8, t1 - 0.2);
    }
    function point(t, until) {
      look(6, -10, t);
      armR(-160, t, 0.45);
      vis("#est-thumb", t + 0.15, true);
      tl.to("#est-arm-r", { rotation: -150, svgOrigin: SH_R, duration: 0.25, yoyo: true, repeat: 1, ease: "sine.inOut" }, t + 0.6);
      vis("#est-thumb", until - 0.1, false);
      armR(0, until, 0.45);
      look(0, -8, until);
    }
    function think(t, until) {
      armR(105, t, 0.45);
      look(-8, -9, t);
      head(-5, 0, t);
      mouth("flat", t);
      vis("#est-q", t + 0.1, true);
      tl.to("#est-q", { y: -8, duration: 0.4, yoyo: true, repeat: 1, ease: "sine.inOut" }, t + 0.2);
      vis("#est-q", until - 0.1, false);
      armR(0, until, 0.45);
      look(0, -8, until);
      head(0, 0, until);
    }
    function aha(t) {
      vis("#est-bulb", t, true);
      tl.set("#est-bulb", { scale: 0.6, transformOrigin: C }, t);
      tl.to("#est-bulb", { scale: 1, duration: 0.35, ease: "back.out(3)" }, t);
      brows(-8, t);
      mouth("smile", t + 0.05);
      tl.to("#est-head", { y: -10, svgOrigin: NECK, duration: 0.15, yoyo: true, repeat: 1 }, t);
      brows(0, t + 1.2);
    }
    function surprised(t, until) {
      tl.to("#est-eyes", { scale: 1.2, svgOrigin: "540 818", duration: 0.15, ease: "back.out(3)" }, t);
      brows(-10, t);
      mouth("open", t);
      tl.to("#est-eyes", { scale: 1, svgOrigin: "540 818", duration: 0.25 }, until);
      brows(0, until);
      mouth("smile", until);
    }
    function coverMouth(t, until) {
      armR(115, t, 0.3);
      tl.to("#est-eyes", { scale: 1.2, svgOrigin: "540 818", duration: 0.15 }, t);
      brows(-9, t);
      armR(0, until, 0.4);
      tl.to("#est-eyes", { scale: 1, svgOrigin: "540 818", duration: 0.2 }, until);
      brows(0, until);
    }
    function shrug(t, until) {
      armL(28, t, 0.35);
      armR(-28, t + 0.06, 0.35);
      head(-8, 0, t);
      brows(-9, t);
      mouth("flat", t);
      armL(0, until, 0.4);
      armR(0, until + 0.06, 0.4);
      head(0, 0, until);
      brows(0, until);
      mouth("smile", until);
    }
    function cheer(t, until) {
      armL(160, t, 0.5);
      armR(-150, t + 0.14, 0.5);
      mouth("open", t + 0.1);
      head(-4, -8, t);
      tl.to("#est-body", { y: -14, duration: 0.18, yoyo: true, repeat: 3, ease: "sine.inOut" }, t + 0.2);
      armR(0, until, 0.45);
      armL(0, until + 0.12, 0.45);
      mouth("smile", until);
      head(0, 0, until);
    }
    function worried(t, until) {
      mouth("flat", t);
      brows(6, t);
      tl.set("#est-sweat", { y: 0 }, t);
      pop("#est-sweat", t + 0.1);
      tl.to("#est-sweat", { y: 30, duration: 0.8, ease: "power1.in" }, t + 0.5);
      vis("#est-sweat", until - 0.1, false);
      brows(0, until);
      mouth("smile", until);
    }
    function stamp(t, prop) {
      vis(prop, t - 0.6, true);
      armR(-40, t - 0.45, 0.3);
      tl.to("#est-arm-r", { rotation: 4, svgOrigin: SH_R, duration: 0.12, ease: "power4.in" }, t - 0.12);
      tl.to("#est-body", { y: 6, duration: 0.06, yoyo: true, repeat: 1 }, t);
      armR(0, t + 0.25, 0.25);
      vis(prop, t + 0.5, false);
    }
    function push(t, until) {
      armL(70, t, 0.3);
      tl.to("#est-arm-l", { rotation: 55, svgOrigin: SH_L, duration: 0.12, yoyo: true, repeat: 3 }, t + 0.35);
      mouth("open", t);
      armL(0, until, 0.35);
      mouth("flat", until);
    }
    function guard(t, until) {
      vis("#est-escudo", t, true);
      armL(55, t, 0.35);
      brows(5, t);
      mouth("flat", t);
      tl.to("#est-arm-l", { rotation: 48, svgOrigin: SH_L, duration: 0.2, yoyo: true, repeat: 3 }, t + 0.8);
      armL(0, until - 0.3, 0.3);
      vis("#est-escudo", until, false);
      brows(0, until);
      mouth("smile", until);
    }
    function carryCoin(t, until) {
      vis("#est-moneda", t, true);
      armR(-90, t + 0.1, 0.4);
      look(-10, -8, t + 0.1);
      tl.to("#est-arm-r", { rotation: -150, svgOrigin: SH_R, duration: (until - t) * 0.6, ease: "sine.inOut" }, t + 0.6);
      look(12, -10, t + 0.6 + (until - t) * 0.4);
      vis("#est-moneda", until - 0.4, false);
      armR(0, until - 0.3, 0.3);
      nod(until - 0.2);
    }
    function brrr(t, until) {
      armL(40, t, 0.3);
      armR(-40, t + 0.05, 0.3);
      mouth("open", t);
      const n = Math.max(1, Math.floor((until - t - 0.6) / 0.24));
      tl.to("#est-arm-l", { rotation: 30, svgOrigin: SH_L, duration: 0.12, yoyo: true, repeat: n % 2 ? n : n - 1 }, t + 0.35);
      tl.to("#est-arm-r", { rotation: -50, svgOrigin: SH_R, duration: 0.12, yoyo: true, repeat: n % 2 ? n : n - 1 }, t + 0.35);
      tl.to("#est-m-open", { scaleY: 0.5, svgOrigin: "540 892", duration: 0.08, yoyo: true, repeat: n % 2 ? n : n - 1 }, t + 0.35);
      armL(0, until, 0.3);
      armR(0, until, 0.3);
      mouth("smile", until);
    }
"""

ACTS = "\n    ".join(acts)
html = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; background: #4b4e8c; }}
    #est-svg {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }}
    .est-h {{ opacity: 0; }}
  </style>
  <div id="root" data-composition-id="estudiante" data-width="1080" data-height="1920">
    {svg}
  </div>
  <script>{RIG}
    // Balanceo y respiración permanentes (cuerpo entero sobre la silla)
    tl.fromTo("#est-body", {{ rotation: -1.2, svgOrigin: "540 1200" }}, {{ rotation: 1.2, svgOrigin: "540 1200", duration: 2.6, ease: "sine.inOut", yoyo: true, repeat: 131 }}, 0);
    tl.fromTo("#est-girl", {{ y: 0 }}, {{ y: -5, duration: 1.2, ease: "sine.inOut", yoyo: true, repeat: 287 }}, 0);
    tl.fromTo("#est-q", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.2 }}, 1.4);

    {ACTS}

    for (let t = 2.6, i = 0; t < {TOTAL - 1}; t += 3.1 + (i % 3) * 0.6, i++) {{
      tl.to("#est-eyes-open", {{ scaleY: 0.1, svgOrigin: "540 818", duration: 0.06 }}, t);
      tl.to("#est-eyes-open", {{ scaleY: 1, svgOrigin: "540 818", duration: 0.09 }}, t + 0.08);
    }}
    tl.set({{}}, {{}}, {TOTAL});
    window.__timelines["estudiante"] = tl;
  </script>
</template>
"""
# Un grupo extra (#est-body) envuelve a la estudiante para balanceo y saltos,
# separado de #est-girl (respiración), así no se pisan las animaciones de y.
html = html.replace('<g id="est-girl">', '<g id="est-body"><g id="est-girl">', 1)
html = html.replace("<!-- Escritorio -->", "</g>\n\n      <!-- Escritorio -->", 1)
(BASE / "proyecto/compositions/estudiante.html").write_text(html)
print("ok", len(acts), "acciones")
