"""Genera compositions/cN.html de la Unidad 2 y el index.html.

Cada capítulo: cartel de título sobre el pizarrón, píldora arriba, ficha
«EJEMPLO DEL APUNTE» o «PARA ENTENDERLO», y escenas animadas en un SVG de
880×470 que se apoya sobre el pizarrón dibujado en estudiante.html.
Todos los tiempos son segundos absolutos del vídeo (de tiempos.json).
"""
import json
from pathlib import Path

BASE = Path(__file__).parent
OUT = BASE / "proyecto"
TOTAL = 345.6
TT = {x["n"]: (x["ini"], x["fin"]) for x in json.loads((BASE / "tiempos.json").read_text())}


def L(n):
    return TT[n][0]


def W(n, frac):
    a, b = TT[n]
    return round(a + (b - a) * frac, 2)


CSS = """
    #root { position: absolute; inset: 0; font-family: Nunito, sans-serif; }
    .h { opacity: 0; }
    .brd { position: absolute; left: 100px; top: 430px; width: 880px; height: 470px; overflow: hidden; border-radius: 22px; }
    .brd svg { position: absolute; left: 0; top: 0; width: 880px; height: 470px; overflow: hidden; }
    .brd text { font-family: Nunito, sans-serif; }
    .b { font-weight: 900; }
    .m { font-weight: 700; }
    .ttl { position: absolute; left: 100px; top: 430px; width: 880px; height: 470px; border-radius: 22px;
      display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px;
      color: #ffffff; text-align: center; overflow: hidden; }
    .ttl-n { font-size: 40px; font-weight: 700; letter-spacing: 0.06em; opacity: 0.9; }
    .ttl-t { font-size: 66px; font-weight: 900; line-height: 1.05; max-width: 760px; }
    .pill-slot { position: absolute; left: 0; right: 0; top: 300px; display: flex; justify-content: center; }
    .pill { display: flex; align-items: center; gap: 14px; padding: 12px 28px; border-radius: 999px;
      background: rgba(16, 18, 42, 0.82); color: #ffffff; font-size: 34px; font-weight: 900; max-width: 840px; }
    .pill-n { font-size: 30px; font-weight: 900; padding: 3px 14px; border-radius: 999px; color: #10122a; }
    .ej { position: absolute; left: 130px; top: 396px; padding: 8px 20px; border-radius: 12px;
      font-size: 28px; font-weight: 900; letter-spacing: 0.04em; box-shadow: 0 5px 0 rgba(0, 0, 0, 0.18); }
    .ej-a { background: #ffd166; color: #2d2200; }
    .ej-p { background: #a5d8ff; color: #0b2540; }
"""

JS = """
    const tl = gsap.timeline({ paused: true });
    const A = (t) => Math.max(0, +(t - T0).toFixed(3));
    const C = "50% 50%";
    function show(s, t, d) {
      tl.set(s, { scale: 0.85, transformOrigin: C }, A(t));
      tl.to(s, { opacity: 1, scale: 1, duration: d || 0.35, ease: "back.out(2)" }, A(t));
    }
    function pop(s, t) {
      tl.set(s, { scale: 0, transformOrigin: C }, A(t));
      tl.to(s, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(3)" }, A(t));
    }
    function hide(s, t) { tl.to(s, { opacity: 0, duration: 0.25, ease: "power2.in" }, A(t - 0.25)); }
    function slideIn(s, t) {
      tl.set(s, { x: 90 }, A(t));
      tl.to(s, { x: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, A(t));
    }
    function slideOut(s, t) { tl.to(s, { x: -90, opacity: 0, duration: 0.35, ease: "power2.in" }, A(t - 0.35)); }
    function drop(s, t) {
      tl.set(s, { y: -160 }, A(t));
      tl.to(s, { y: 0, opacity: 1, duration: 0.55, ease: "bounce.out" }, A(t));
    }
    function draw(s, t, d) { tl.to(s, { strokeDashoffset: 0, duration: d || 0.8, ease: "power1.inOut" }, A(t)); }
    function grow(s, t, d, origin) {
      tl.set(s, { scaleX: 0, transformOrigin: origin || "0% 50%" }, A(t));
      tl.to(s, { scaleX: 1, opacity: 1, duration: d || 0.8, ease: "power2.out" }, A(t));
    }
    function growY(s, t, d) {
      tl.set(s, { scaleY: 0, transformOrigin: "50% 100%" }, A(t));
      tl.to(s, { scaleY: 1, opacity: 1, duration: d || 0.8, ease: "power2.out" }, A(t));
    }
    function pulse(s, t) { tl.to(s, { scale: 1.12, transformOrigin: C, duration: 0.18, yoyo: true, repeat: 1, ease: "sine.inOut" }, A(t)); }
    function reps(span, per) { const n = Math.max(1, Math.floor(span / per)); return n % 2 ? n : n - 1; }
    function bob(s, t0, t1, amp, per) {
      per = per || 0.8;
      tl.to(s, { y: -(amp || 8), duration: per / 2, ease: "sine.inOut", yoyo: true, repeat: reps(t1 - t0, per / 2) }, A(t0));
    }
    function wob(s, t0, t1, deg, per, origin) {
      per = per || 0.8;
      tl.fromTo(s, { rotation: -(deg || 6), transformOrigin: origin || C }, { rotation: deg || 6, duration: per / 2, ease: "sine.inOut", yoyo: true, repeat: reps(t1 - t0, per / 2) }, A(t0));
    }
    function flow(s, t0, t1, speed) {
      tl.to(s, { strokeDashoffset: -(speed || 60) * (t1 - t0), duration: t1 - t0, ease: "none" }, A(t0));
    }
    function spin(s, t0, t1, deg) { tl.to(s, { rotation: deg || 360, transformOrigin: C, duration: t1 - t0, ease: "none" }, A(t0)); }
    function money(v) { return "$" + Math.round(v).toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g, "."); }
    function count(sel, a, b, t, d, fmt) {
      const el = document.querySelector(sel);
      const o = { v: a };
      fmt = fmt || money;
      tl.to(o, { v: b, duration: d || 1, ease: "power1.out", onUpdate: () => { el.textContent = fmt(o.v); } }, A(t));
    }
    function travel(s, t, dx, dy, d, arc) {
      tl.to(s, { x: dx, duration: d || 0.8, ease: "power1.inOut" }, A(t));
      if (arc) {
        tl.to(s, { y: arc, duration: (d || 0.8) / 2, ease: "sine.out" }, A(t));
        tl.to(s, { y: dy, duration: (d || 0.8) / 2, ease: "sine.in" }, A(t + (d || 0.8) / 2));
      } else {
        tl.to(s, { y: dy, duration: d || 0.8, ease: "power1.inOut" }, A(t));
      }
    }
    // Varias monedas que circulan en fila, en loop finito
    function stream(prefix, n, t0, t1, dx, dy, per) {
      for (let i = 0; i < n; i++) {
        const s = prefix + i;
        const st = t0 + (i * per) / n;
        const loops = Math.max(0, Math.floor((t1 - st - per) / per));
        tl.set(s, { x: 0, y: 0, opacity: 1 }, A(st));
        tl.to(s, { x: dx, y: dy, duration: per, ease: "none", repeat: loops }, A(st));
        tl.to(s, { opacity: 0, duration: 0.15 }, A(st + per * (loops + 1) - 0.15));
      }
    }
"""


def T(x, y, s, txt, cls="m", anchor="middle", fill="#2d3436", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{s}" class="{cls}" text-anchor="{anchor}" fill="{fill}" {extra}>{txt}</text>'


def coin(idv, x, y, r=18, cls="h"):
    return f'<circle id="{idv}" class="{cls}" cx="{x}" cy="{y}" r="{r}" fill="#fdcb6e" stroke="#e1a940" stroke-width="4" />'


def coins(prefix, n, x, y, r=16):
    return "".join(coin(f"{prefix}{i}", x, y, r) for i in range(n))


def box(x, y, w, h, txt, fill, tc="#ffffff", s=30, idv="", cls="", rx=16):
    i = f' id="{idv}"' if idv else ""
    c = f' class="{cls}"' if cls else ""
    return f'<g{i}{c}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" />{T(x + w / 2, y + h / 2 + s * 0.35, s, txt, "b", fill=tc)}</g>'


def cross(idv, cx, cy, r=30):
    return f'<g id="{idv}" class="h"><circle cx="{cx}" cy="{cy}" r="{r}" fill="#d63031" /><path d="M{cx - r * 0.4},{cy - r * 0.4} L{cx + r * 0.4},{cy + r * 0.4} M{cx + r * 0.4},{cy - r * 0.4} L{cx - r * 0.4},{cy + r * 0.4}" stroke="#ffffff" stroke-width="{r * 0.25}" stroke-linecap="round" /></g>'


def check(idv, cx, cy, r=30):
    return f'<g id="{idv}" class="h"><circle cx="{cx}" cy="{cy}" r="{r}" fill="#00b894" /><path d="M{cx - r * 0.45},{cy} L{cx - r * 0.1},{cy + r * 0.35} L{cx + r * 0.5},{cy - r * 0.35}" stroke="#ffffff" stroke-width="{r * 0.25}" fill="none" stroke-linecap="round" /></g>'


def arrow(idv, d, color="#2d3436", w=6, cls="", head=True, dash="14 10"):
    c = f' class="{cls}"' if cls else ""
    mk = ' marker-end="url(#ah)"' if head else ""
    return f'<path id="{idv}"{c} d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-dasharray="{dash}" stroke-linecap="round"{mk} />'


def line_draw(idv, d, color="#2d3436", w=6, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<path id="{idv}"{c} d="{d}" fill="none" stroke="{color}" stroke-width="{w}" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" />'


DEFS = '<defs><marker id="ah" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#2d3436" /></marker></defs>'

# Íconos reutilizables (centrados en 0,0)
I_ESCUELA = '<path d="M-70,-20 L0,-62 L70,-20 Z" fill="#e17055"/><rect x="-58" y="-20" width="116" height="80" fill="#fdcb6e"/><rect x="-14" y="18" width="28" height="42" fill="#a86e45"/><rect x="-46" y="-6" width="22" height="20" fill="#ffffff"/><rect x="24" y="-6" width="22" height="20" fill="#ffffff"/>'
I_HOSPITAL = '<rect x="-60" y="-56" width="120" height="116" fill="#ffffff" stroke="#2d3436" stroke-width="5"/><rect x="-12" y="-42" width="24" height="64" fill="#d63031"/><rect x="-32" y="-22" width="64" height="24" fill="#d63031"/><rect x="-16" y="30" width="32" height="30" fill="#74b9ff"/>'
I_DOC = '<rect x="-40" y="-52" width="80" height="104" rx="8" fill="#ffffff" stroke="#2d3436" stroke-width="5"/><path d="M-24,-24 L24,-24 M-24,-4 L24,-4 M-24,16 L10,16" stroke="#b2bec3" stroke-width="6"/>'
I_LEGIS = '<rect x="-80" y="0" width="160" height="62" fill="#dfe6e9" stroke="#2d3436" stroke-width="5"/><path d="M-46,0 A46,46 0 0,1 46,0 Z" fill="#3d8bd9"/><rect x="-62" y="12" width="14" height="50" fill="#b2bec3"/><rect x="-26" y="12" width="14" height="50" fill="#b2bec3"/><rect x="12" y="12" width="14" height="50" fill="#b2bec3"/><rect x="48" y="12" width="14" height="50" fill="#b2bec3"/>'
I_EJEC = '<path d="M-88,0 L0,-44 L88,0 Z" fill="#636e72"/><rect x="-80" y="0" width="160" height="70" fill="#dfe6e9" stroke="#2d3436" stroke-width="5"/><rect x="-62" y="10" width="18" height="60" fill="#b2bec3"/><rect x="-26" y="10" width="18" height="60" fill="#b2bec3"/><rect x="10" y="10" width="18" height="60" fill="#b2bec3"/><rect x="46" y="10" width="18" height="60" fill="#b2bec3"/>'
I_BOVEDA = '<rect x="-70" y="-64" width="140" height="128" rx="14" fill="#636e72"/><circle r="38" fill="#b2bec3" stroke="#2d3436" stroke-width="6"/><path d="M0,-26 L0,26 M-26,0 L26,0" stroke="#2d3436" stroke-width="6"/>'
I_PERSONA = '<circle cy="-26" r="16" fill="#f5c9a0"/><path d="M-22,20 Q-22,-6 0,-6 Q22,-6 22,20 Z" fill="#74b9ff"/>'
I_AUTO = '<rect x="-60" y="-14" width="120" height="34" rx="10" fill="#e17055"/><path d="M-36,-14 L-22,-38 L24,-38 L38,-14 Z" fill="#e17055"/><rect x="-16" y="-32" width="34" height="16" fill="#dff9fb"/><circle cx="-34" cy="22" r="14" fill="#2d3436"/><circle cx="34" cy="22" r="14" fill="#2d3436"/>'
I_AMBU = '<rect x="-70" y="-40" width="110" height="64" rx="8" fill="#ffffff" stroke="#2d3436" stroke-width="4"/><path d="M40,-20 L66,-20 L76,6 L76,24 L40,24 Z" fill="#ffffff" stroke="#2d3436" stroke-width="4"/><rect x="-26" y="-30" width="12" height="40" fill="#d63031"/><rect x="-40" y="-16" width="40" height="12" fill="#d63031"/><circle cx="-40" cy="28" r="13" fill="#2d3436"/><circle cx="50" cy="28" r="13" fill="#2d3436"/><rect x="-6" y="-50" width="20" height="10" rx="3" fill="#0984e3"/>'
I_MARTILLO = '<rect x="-12" y="-6" width="90" height="16" rx="6" fill="#a86e45" transform="rotate(-30)"/><rect x="-40" y="-34" width="56" height="40" rx="8" fill="#6d4c41" transform="rotate(-30)"/>'

chapters = []


def chapter(cid, t0, t1, num, title, accent, badge, title_end, ej, pe, svg, js, pill_extra="", title_sub=""):
    dur = round(t1 - t0, 3)
    n_html = f'<div class="ttl-n">{num}</div>' if num else ""
    sub_html = f'<div class="ttl-n">{title_sub}</div>' if title_sub else ""
    title_html = f"""
    <div id="{cid}-ttl" class="ttl" style="background: {accent}">{n_html}<div class="ttl-t">{title}</div>{sub_html}</div>""" if title_end else ""
    title_js = f"""
    tl.fromTo("#{cid}-ttl", {{ opacity: 1, clipPath: "inset(0% 0% 0% 0% round 22px)" }}, {{ opacity: 1, clipPath: "inset(0% 0% 0% 0% round 22px)", duration: 0.1 }}, 0);
    tl.fromTo("#{cid}-ttl .ttl-t", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(2)" }}, 0.1);
    tl.to("#{cid}-ttl", {{ clipPath: "inset(0% 0% 0% 100% round 22px)", duration: 0.5, ease: "power3.inOut" }}, A({title_end - 0.5}));
    show("#{cid}-pill", {title_end - 0.1});
    hide("#{cid}-pill", {t1 - 0.05});""" if title_end else ""
    for a, b in ej:
        title_js += f'\n    show("#{cid}-ej", {a});\n    hide("#{cid}-ej", {b});'
    for a, b in pe:
        title_js += f'\n    show("#{cid}-pe", {a});\n    hide("#{cid}-pe", {b});'
    pill_badge = f'<span class="pill-n" style="background: {badge}">Cap. {num[-1]}/6</span>' if num.startswith("Capítulo") else ""
    html = f"""<template>
  <style>{CSS}
    .acc {{ fill: {accent}; }}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
    <div class="brd"><svg viewBox="0 0 880 470" xmlns="http://www.w3.org/2000/svg">{DEFS}{svg}
    </svg></div>{title_html}
    <div class="pill-slot"><div id="{cid}-pill" class="pill h">{pill_badge}{title}</div></div>{pill_extra}
    <div id="{cid}-ej" class="ej ej-a h">EJEMPLO DEL APUNTE</div>
    <div id="{cid}-pe" class="ej ej-p h">PARA ENTENDERLO</div>
  </div>
  <script>
    const T0 = {t0};{JS}{title_js}
{js}
    tl.set({{}}, {{}}, {dur});
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""
    (OUT / "compositions" / f"{cid}.html").write_text(html)
    chapters.append((cid, t0, dur))


# Límites de capítulo
B = [0, 12.16, 54.51, 95.08, 160.9, 197.95, 258.26, 310.12, 331.49, TOTAL]

# ================================================================ INTRO
P = "#5b4bd6"
svg = f"""
      <g id="c0-a">
        {T(440, 62, 44, "¿Puede gastar sin ley?", "b", fill=P)}
        <g id="c0-pila">{coin("c0-p1", 130, 330, 30, "")}{coin("c0-p2", 170, 300, 30, "")}{coin("c0-p3", 120, 280, 30, "")}{coin("c0-p4", 160, 250, 30, "")}</g>
        {box(650, 240, 190, 100, "GASTO", "#636e72", s=34)}
        {arrow("c0-flecha", "M220,290 L630,290", "#b2bec3", 8)}
        {coins("c0-m", 3, 220, 290)}
        <g id="c0-candado" class="h">
          <rect x="390" y="270" width="70" height="58" rx="10" fill="#d63031" />
          <path d="M403,272 L403,250 A22,22 0 0,1 447,250 L447,272" fill="none" stroke="#d63031" stroke-width="10" />
        </g>
        <g id="c0-no" class="h" transform="rotate(-10 440 160)">
          <rect x="300" y="110" width="280" height="96" rx="14" fill="none" stroke="#d63031" stroke-width="8" />
          {T(440, 176, 52, "¡NO!", "b", fill="#d63031")}
        </g>
        <g id="c0-ley" class="h">
          <rect x="350" y="200" width="180" height="180" rx="12" fill="#ffffff" stroke="{P}" stroke-width="7" />
          {T(440, 268, 30, "LEY DE", "b", fill=P)}
          {T(440, 306, 30, "PRESUPUESTO", "b", fill=P)}
          <path d="M380,336 L500,336 M380,356 L470,356" stroke="#b2bec3" stroke-width="6" />
        </g>
      </g>
      <g id="c0-b" class="h">
        <g id="c0-col">""" + "".join(
    f'<rect id="c0-v{i}" class="h" x="{150 - (i % 2) * 6}" y="{400 - i * 44}" width="{120 + (i % 2) * 12}" height="34" rx="14" fill="{P if i % 2 else "#8f84ec"}" />'
    for i in range(8)) + f"""</g>
        <g id="c0-tit" class="h">
          <rect x="420" y="120" width="220" height="58" rx="29" fill="{P}" />
          {T(530, 160, 34, "UNIDAD 2", "b", fill="#ffffff")}
          {T(620, 250, 56, "El presupuesto", "b")}
          {T(620, 318, 56, "público", "b", fill=P)}
          {T(620, 380, 30, "la columna vertebral de la hacienda", "m", fill="#636e72")}
        </g>
      </g>"""
js = f"""
    bob("#c0-pila", 0, 3.0, 6, 0.9);
    flow("#c0-flecha", 0, 6.7, 50);
    tl.set("#c0-m0", {{ opacity: 1 }}, 0.2);
    travel("#c0-m0", 0.3, 160, 0, 1.2);
    drop("#c0-candado", 1.4);
    tl.to("#c0-m0", {{ x: 120, duration: 0.25, ease: "power2.out" }}, A(1.75));
    tl.to("#c0-m0", {{ opacity: 0, duration: 0.2 }}, A(2.6));
    wob("#c0-candado", 2.0, 3.6, 8, 0.3);
    tl.set("#c0-no", {{ scale: 2, transformOrigin: C }}, A({L(2)}));
    tl.to("#c0-no", {{ opacity: 1, scale: 1, duration: 0.2, ease: "power4.in" }}, A({L(2)}));
    hide("#c0-no", {W(2, 0.5)});
    hide("#c0-candado", {W(2, 0.45)});
    drop("#c0-ley", {W(2, 0.4)});
    bob("#c0-ley", {W(2, 0.6)}, 6.7, 5, 1.0);
    stream("#c0-m", 3, {W(2, 0.65)}, 6.7, 410, 0, 1.2);
    slideOut("#c0-a", {L(3)});
    tl.set("#c0-b", {{ opacity: 1 }}, A({L(3)}));""" + "".join(
    f'\n    drop("#c0-v{i}", {round(L(3) + 0.1 + i * 0.28, 2)});' for i in range(8)) + f"""
    tl.to("#c0-col", {{ x: 6, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 5 }}, A(9.3));
    slideIn("#c0-tit", {W(3, 0.6)});
    pulse("#c0-tit", 11.2);"""
chapter("c0", 0, B[1], "", "Unidad 2", P, "#c3baff", None, [], [], svg, js)

# ================================================================ C1
P = "#6c5ce7"
svg = f"""
      <g id="c1-a" class="h">
        {T(440, 56, 38, "Desde lo financiero", "b", fill=P)}
        <g transform="translate(160 260)">{I_DOC}</g>
        {T(160, 360, 28, "plan del gobierno", "b")}
        {arrow("c1-a-ar", "M240,250 L390,250", P, 7)}
        """ + "".join(
    f'<g id="c1-a-r{i}" class="h">{T(430, 168 + i * 62, 34, "$", "b", fill=P)}<rect id="c1-a-b{i}" x="460" y="{142 + i * 62}" width="{[300, 220, 340, 180][i]}" height="34" rx="17" fill="#c9c2f8" /></g>'
    for i in range(4)) + f"""
      </g>
      <g id="c1-b" class="h">
        {T(440, 56, 38, "Desde lo político", "b", fill=P)}
        <g id="c1-fab">
          <rect x="60" y="200" width="170" height="140" fill="#636e72" />
          <path d="M60,200 L60,160 L117,200 L117,160 L174,200 L174,120 L230,120 L230,200 Z" fill="#636e72" />
          <circle id="c1-humo1" cx="202" cy="100" r="16" fill="#dfe6e9" /><circle id="c1-humo2" cx="214" cy="80" r="12" fill="#dfe6e9" />
          {T(145, 385, 28, "bienes y servicios", "b")}
        </g>
        {arrow("c1-b-ar", "M245,270 L330,270", P, 7)}
        <g id="c1-esc" class="h"><g transform="translate(440 250)">{I_ESCUELA}</g></g>
        <g id="c1-hos" class="h"><g transform="translate(680 250)">{I_HOSPITAL}</g></g>
        <g id="c1-tag1" class="h"><rect x="360" y="340" width="160" height="40" rx="20" fill="#efeafe" /><rect id="c1-tag1f" x="360" y="340" width="160" height="40" rx="20" fill="{P}" />{T(440, 371, 28, "costo", "b", fill="#ffffff")}</g>
        <g id="c1-tag2" class="h"><rect x="600" y="340" width="160" height="40" rx="20" fill="#efeafe" /><rect id="c1-tag2f" x="600" y="340" width="160" height="40" rx="20" fill="{P}" />{T(680, 371, 28, "costo", "b", fill="#ffffff")}</g>
      </g>
      <g id="c1-c" class="h">
        {T(440, 56, 36, "Acto administrativo-legislativo", "b", fill=P)}
        <g transform="translate(170 200)">{I_EJEC}</g>
        {T(170, 312, 30, "Ejecutivo", "b")}
        <g id="c1-c-e1" class="h">{T(170, 352, 28, "prepara", "b", fill=P)}</g>
        <g id="c1-c-e2" class="h">{T(170, 390, 28, "y ejecuta", "b", fill=P)}</g>
        <g transform="translate(710 200)">{I_LEGIS}</g>
        {T(710, 312, 30, "Legislativo", "b")}
        <g id="c1-c-l1" class="h">{T(710, 352, 28, "aprueba", "b", fill="#3d8bd9")}</g>
        {arrow("c1-c-ar1", "M280,150 Q440,90 600,150", P, 7)}
        {arrow("c1-c-ar2", "M600,280 Q440,340 280,280", "#3d8bd9", 7)}
        <g id="c1-c-doc"><g transform="translate(300 150) scale(0.6)">{I_DOC}</g></g>
        <g id="c1-c-sello" class="h" transform="rotate(-12 600 150)"><rect x="548" y="128" width="104" height="44" rx="8" fill="none" stroke="#d63031" stroke-width="6" />{T(600, 162, 30, "LEY", "b", fill="#d63031")}</g>
        <g id="c1-c-gear" class="h"><circle cx="270" cy="230" r="22" fill="none" stroke="{P}" stroke-width="12" stroke-dasharray="9 7" /></g>
      </g>
      <g id="c1-d" class="h">
        <g id="c1-mart" transform="translate(230 250)">{I_MARTILLO}</g>
        <rect x="150" y="300" width="160" height="30" rx="8" fill="#6d4c41" />
        {T(230, 390, 32, "fuerza de ley", "b", fill=P)}
        <rect x="500" y="110" width="260" height="240" rx="18" fill="#ffffff" stroke="#2d3436" stroke-width="6" />
        <rect x="500" y="110" width="260" height="70" rx="16" fill="{P}" />
        <text id="c1-mes" x="630" y="290" font-size="76" class="b" text-anchor="middle" fill="#2d3436">ENE</text>
        {T(630, 160, 30, "rige 1 año", "b", fill="#ffffff")}
        <rect x="500" y="370" width="260" height="20" rx="10" fill="#efeafe" />
        <rect id="c1-anio" x="500" y="370" width="260" height="20" rx="10" fill="{P}" />
      </g>
      <g id="c1-e" class="h">
        {T(440, 56, 38, "Recursos: estimativos", "b", fill=P)}
        <path d="M200,380 A240,240 0 0,1 680,380" fill="none" stroke="#efeafe" stroke-width="40" />
        <path d="M200,380 A240,240 0 0,1 330,170" fill="none" stroke="#fab1a0" stroke-width="40" />
        <path d="M550,170 A240,240 0 0,1 680,380" fill="none" stroke="#55efc4" stroke-width="40" />
        <path d="M440,140 L440,190" stroke="#2d3436" stroke-width="6" />
        {T(440, 125, 28, "lo estimado", "b")}
        {T(215, 430, 30, "menos", "b", fill="#d63031")}
        {T(665, 430, 30, "más", "b", fill="#00b894")}
        <g id="c1-aguja"><path d="M440,380 L440,190" stroke="#2d3436" stroke-width="10" stroke-linecap="round" /><circle cx="440" cy="380" r="20" fill="#2d3436" /></g>
      </g>
      <g id="c1-f" class="h">
        {T(440, 52, 34, "Gastos: autorización máxima", "b", fill=P)}
        {T(440, 92, 28, "presupuesto de una escuela", "m", fill="#636e72")}
        <g>
          <rect x="120" y="140" width="200" height="250" rx="20" fill="#f1f2f6" stroke="#2d3436" stroke-width="6" />
          <rect id="c1-j1" x="126" y="216" width="188" height="168" rx="14" fill="#fdcb6e" />
          {T(220, 430, 30, "Útiles escolares", "b")}
          <rect x="560" y="140" width="200" height="250" rx="20" fill="#f1f2f6" stroke="#2d3436" stroke-width="6" />
          <rect id="c1-j2" x="566" y="216" width="188" height="168" rx="14" fill="#74b9ff" />
          {T(660, 430, 30, "Sueldos", "b")}
          <path d="M100,214 L340,214 M540,214 L780,214" stroke="#d63031" stroke-width="6" stroke-dasharray="14 8" />
          <g id="c1-tope" class="h">{T(440, 222, 30, "← tope →", "b", fill="#d63031")}</g>
        </g>
        <g id="c1-cuanto" class="h">{box(370, 120, 140, 50, "cuánto", "#d63031", s=28)}</g>
        <g id="c1-enque" class="h">{box(370, 290, 140, 50, "en qué", "#d63031", s=28)}</g>
        {coin("c1-mon", 220, 200, 24)}
        <rect id="c1-muro" class="h" x="430" y="120" width="20" height="280" rx="8" fill="#d63031" />
        {cross("c1-x", 440, 110, 30)}
      </g>
      <g id="c1-g" class="h">
        {T(440, 52, 38, "Especificidad", "b", fill=P)}
        {T(440, 94, 28, "gastos y recursos, por clasificaciones", "m", fill="#636e72")}
        {box(120, 330, 280, 90, "Gastos", "#e17055", s=34)}
        {box(480, 330, 280, 90, "Recursos", "#00b894", s=34)}
        """ + "".join(
    f'{box(220 + (i % 2) * 360, 120, 80, 50, "", "#e17055" if i % 2 == 0 else "#00b894", idv=f"c1-it{i}", cls="h", rx=10)}'
    for i in range(6)) + """
      </g>"""
js = f"""
    slideIn("#c1-a", {L(5)});
    flow("#c1-a-ar", {L(5)}, {W(5, 1)}, 60);
    {"".join(f'show("#c1-a-r{i}", {round(W(5, 0.3) + i * 0.4, 2)}); grow("#c1-a-b{i}", {round(W(5, 0.3) + i * 0.4, 2)}, 0.9);' for i in range(4))}
    {"".join(f'tl.to("#c1-a-b{i}", {{ scaleX: {[1.08, 0.9, 1.05, 0.92][i]}, duration: 0.7, ease: "sine.inOut", yoyo: true, repeat: 3 }}, A({round(W(5, 0.6) + i * 0.1, 2)}));' for i in range(4))}
    slideOut("#c1-a", {L(6)});
    slideIn("#c1-b", {L(6)});
    bob("#c1-humo1", {L(6)}, {W(6, 1)}, 14, 1.0);
    bob("#c1-humo2", {W(6, 0.1)}, {W(6, 1)}, 12, 0.8);
    flow("#c1-b-ar", {L(6)}, {W(6, 1)}, 60);
    tl.set("#c1-esc", {{ x: -200 }}, A({W(6, 0.2)}));
    tl.to("#c1-esc", {{ x: 0, opacity: 1, duration: 0.6, ease: "back.out(1.5)" }}, A({W(6, 0.2)}));
    tl.set("#c1-hos", {{ x: -440 }}, A({W(6, 0.42)}));
    tl.to("#c1-hos", {{ x: 0, opacity: 1, duration: 0.8, ease: "back.out(1.5)" }}, A({W(6, 0.42)}));
    fade = 0;
    show("#c1-tag1", {W(6, 0.62)}); grow("#c1-tag1f", {W(6, 0.62)}, 1.4);
    show("#c1-tag2", {W(6, 0.75)}); grow("#c1-tag2f", {W(6, 0.75)}, 1.4);
    slideOut("#c1-b", {L(7)});
    slideIn("#c1-c", {L(7)});
    flow("#c1-c-ar1", {L(7)}, {W(7, 1)}, 60);
    flow("#c1-c-ar2", {L(7)}, {W(7, 1)}, 60);
    show("#c1-c-e1", {W(7, 0.42)});
    travel("#c1-c-doc", {W(7, 0.45)}, 300, 0, 1.0, -40);
    show("#c1-c-l1", {W(7, 0.78)});
    tl.set("#c1-c-sello", {{ scale: 2, transformOrigin: C }}, A({W(7, 0.8)}));
    tl.to("#c1-c-sello", {{ opacity: 1, scale: 1, duration: 0.18, ease: "power4.in" }}, A({W(7, 0.8)}));
    show("#c1-c-e2", {W(7, 0.62)});
    pop("#c1-c-gear", {W(7, 0.62)});
    spin("#c1-c-gear", {W(7, 0.62)}, {W(7, 1)}, 400);
    slideOut("#c1-c", {L(8)});
    slideIn("#c1-d", {L(8)});
    tl.fromTo("#c1-mart", {{ rotation: -25, transformOrigin: "100% 100%" }}, {{ rotation: 12, duration: 0.18, ease: "power4.in", yoyo: true, repeat: 3, transformOrigin: "100% 100%" }}, A({W(8, 0.1)}));
    count("#c1-mes", 0, 11, {W(8, 0.45)}, {round((TT[8][1] - TT[8][0]) * 0.5, 2)}, (v) => ["ENE","FEB","MAR","ABR","MAY","JUN","JUL","AGO","SEP","OCT","NOV","DIC"][Math.round(v)]);
    grow("#c1-anio", {W(8, 0.45)}, {round((TT[8][1] - TT[8][0]) * 0.5, 2)});
    slideOut("#c1-d", {L(9)});
    slideIn("#c1-e", {L(9)});
    tl.fromTo("#c1-aguja", {{ rotation: -30, svgOrigin: "440 380" }}, {{ rotation: 30, svgOrigin: "440 380", duration: 0.7, ease: "sine.inOut", yoyo: true, repeat: 5 }}, A({W(9, 0.1)}));
    slideOut("#c1-e", {L(10)});
    slideIn("#c1-f", {L(10)});
    growY("#c1-j1", {W(10, 0.3)}, 0.9);
    growY("#c1-j2", {W(10, 0.5)}, 0.9);
    tl.to(["#c1-j1", "#c1-j2"], {{ scaleY: 0.96, duration: 0.25, yoyo: true, repeat: 5, ease: "sine.inOut", transformOrigin: "50% 100%" }}, A({W(11, 0.0)}));
    show("#c1-tope", {W(11, 0.05)});
    pop("#c1-cuanto", {W(11, 0.15)});
    pop("#c1-enque", {W(11, 0.6)});
    hide("#c1-cuanto", {L(12)});
    hide("#c1-enque", {L(12)});
    tl.set("#c1-mon", {{ opacity: 1 }}, A({W(12, 0.35)}));
    pop("#c1-mon", {W(12, 0.35)});
    show("#c1-muro", {W(12, 0.45)});
    travel("#c1-mon", {W(12, 0.55)}, 190, 0, 0.5, -90);
    tl.to("#c1-mon", {{ x: 40, y: 60, duration: 0.5, ease: "power2.out" }}, A({W(12, 0.55) + 0.5}));
    pop("#c1-x", {W(12, 0.66)});
    wob("#c1-muro", {W(12, 0.66)}, {W(12, 0.9)}, 3, 0.15);
    slideOut("#c1-f", {L(13)});
    slideIn("#c1-g", {L(13)});""" + "".join(
    f'\n    tl.set("#c1-it{i}", {{ opacity: 1, y: -60 }}, A({round(W(13, 0.15) + i * 0.45, 2)}));\n    tl.to("#c1-it{i}", {{ y: 230, duration: 0.55, ease: "bounce.out" }}, A({round(W(13, 0.15) + i * 0.45, 2)}));\n    tl.to("#c1-it{i}", {{ opacity: 0, duration: 0.15 }}, A({round(W(13, 0.15) + i * 0.45 + 0.6, 2)}));'
    for i in range(6)) + """
    """
js = js.replace("    fade = 0;\n", "")
chapter("c1", B[1], B[2], "Capítulo 1", "Qué es el presupuesto", P, "#c3baff", 14.8, [(L(12), 49.5)], [(L(10), L(12) - 0.1)], svg, js)

# ================================================================ C2 (cinta de 6 estaciones)
P = "#1f9d6f"
def st(i, inner, nombre):
    x = 440 + i * 880
    return f"""
          <g id="c2-s{i}">
            <circle cx="{x - 300}" cy="56" r="30" fill="{P}" />{T(x - 300, 67, 32, str(i + 1), "b", fill="#ffffff")}
            {T(x - 255, 68, 36, nombre, "b", "start", P)}
            <g transform="translate({x - 440} 0)">{inner}</g>
          </g>"""

s1 = "".join(
    f'<g>{T(170, 160 + k * 90, 30, lab, "b", "start")}<rect x="420" y="{140 + k * 90}" width="320" height="16" rx="8" fill="#d1f2e4" /><circle id="c2-k{k}" cx="460" cy="{148 + k * 90}" r="22" fill="{P}" /></g>'
    for k, lab in enumerate(["nivel", "prioridades", "financiamiento"]))
s2 = f"""<g id="c2-dppp">{T(250, 160, 30, "Dirección Provincial", "b")}{T(250, 198, 30, "de Programación", "b")}{T(250, 236, 30, "Presupuestaria", "b")}</g>
            <g transform="translate(620 230)"><rect x="-90" y="-110" width="180" height="220" rx="10" fill="#ffffff" stroke="#2d3436" stroke-width="5" />{"".join(line_draw(f"c2-tl{k}", f"M-60,{-70 + k * 36} L60,{-70 + k * 36}", "#b2bec3", 8) for k in range(5))}{T(0, 140, 28, "proyecto de ley", "b", fill=P)}</g>
            <g id="c2-min" class="h"><ellipse cx="300" cy="380" rx="200" ry="34" fill="#a86e45" />{"".join(f'<g id="c2-mi{k}" transform="translate({180 + k * 120} 340)">{I_PERSONA}</g>' for k in range(3))}{T(300, 446, 28, "acuerdo de ministros", "b", fill=P)}</g>"""
s3 = f"""<g transform="translate(220 230)">{I_LEGIS}</g>{T(220, 340, 30, "Legislatura", "b")}
            <g transform="translate(600 230)"><rect x="-110" y="-120" width="220" height="240" rx="10" fill="#ffffff" stroke="#2d3436" stroke-width="5" />{"".join(f'<path d="M-80,{-80 + k * 40} L80,{-80 + k * 40}" stroke="#b2bec3" stroke-width="8" />' for k in range(5))}{line_draw("c2-tacha", "M-90,-40 L90,-40", "#d63031", 8)}{line_draw("c2-nueva", "M-80,100 L40,100", P, 8)}</g>
            <g id="c2-ley" class="h" transform="rotate(-12 600 230)"><rect x="520" y="196" width="160" height="70" rx="10" fill="none" stroke="#d63031" stroke-width="8" />{T(600, 248, 44, "LEY", "b", fill="#d63031")}</g>"""
s4 = f"""<g transform="translate(440 250)">{I_BOVEDA}</g>{T(440, 360, 30, "Tesoro", "b")}
            {arrow("c2-in", "M120,250 L350,250", "#00b894", 8)}{arrow("c2-out", "M530,250 L760,250", "#e17055", 8)}
            {T(200, 200, 30, "cobra recursos", "b", fill="#00b894")}{T(680, 200, 30, "hace gastos", "b", fill="#e17055")}
            {coins("c2-ci", 3, 120, 250)}{coins("c2-co", 3, 530, 250)}"""
s5 = f"""<rect x="120" y="130" width="300" height="260" rx="10" fill="#ffffff" stroke="#2d3436" stroke-width="5" /><path d="M270,130 L270,390" stroke="#2d3436" stroke-width="4" />
            {"".join(line_draw(f"c2-lb{k}", f"M140,{170 + k * 40} L250,{170 + k * 40}", P, 7) for k in range(5))}
            {T(270, 430, 28, "se anota mientras ocurre", "b", fill=P)}
            {coins("c2-cr", 3, 470, 250)}
            <g id="c2-esc" class="h"><path d="M640,170 L720,196 L720,260 Q720,320 640,350 Q560,320 560,260 L560,196 Z" fill="#0984e3" /><path d="M610,260 L634,284 L676,236" stroke="#ffffff" stroke-width="12" fill="none" stroke-linecap="round" /></g>
            <g id="c2-fuera" class="h">{coin("c2-cf", 770, 260, 22, "")}{T(770, 330, 28, "fuera del", "b", fill="#d63031")}{T(770, 362, 28, "presupuesto", "b", fill="#d63031")}</g>"""
s6 = f"""{T(250, 400, 30, "previsto", "b")}{T(450, 400, 30, "hecho", "b")}
            <rect id="c2-bp" x="200" y="140" width="100" height="220" rx="10" fill="#b2bec3" />
            <rect id="c2-bh" x="400" y="180" width="100" height="180" rx="10" fill="{P}" />
            <g id="c2-mart" transform="translate(680 250)">{I_MARTILLO}</g><rect x="600" y="300" width="160" height="30" rx="8" fill="#6d4c41" />
            {T(680, 400, 30, "juzgamiento", "b", fill=P)}"""
svg = f"""
      <rect x="0" y="0" width="880" height="470" fill="none" />
      <g id="c2-belt">{st(0, s1, "Política")}{st(1, s2, "Confección del proyecto")}{st(2, s3, "Autorización legal")}{st(3, s4, "Ejecución")}{st(4, s5, "Registración y control")}{st(5, s6, "Evaluación y juzgamiento")}
      </g>
      <g id="c2-proy" class="h"><g transform="translate(800 40) scale(0.45)">{I_DOC}</g></g>"""
stops = [L(15), L(16), L(18), L(19), L(20), L(22)]
js = f"""
    tl.set("#c2-belt", {{ x: 880 }}, 0);
    tl.to("#c2-belt", {{ x: 0, duration: 0.7, ease: "power3.inOut" }}, A({stops[0] - 0.3}));
    show("#c2-proy", {stops[0]});
    bob("#c2-proy", {stops[0]}, 94.5, 6, 0.9);"""
for i, t in enumerate(stops[1:], 1):
    js += f'\n    tl.to("#c2-belt", {{ x: {-880 * i}, duration: 0.7, ease: "power3.inOut" }}, A({round(t - 0.3, 2)}));'
    js += f'\n    tl.to("#c2-proy", {{ rotation: 360, transformOrigin: C, duration: 0.6, ease: "power2.inOut" }}, A({round(t - 0.3, 2)}));'
    js += f'\n    tl.set("#c2-proy", {{ rotation: 0 }}, A({round(t + 0.31, 2)}));'
js += f"""
    {"".join(f'tl.to("#c2-k{k}", {{ x: {[180, 90, 240][k]}, duration: 0.6, ease: "back.out(2)" }}, A({round(W(15, 0.45) + k * 0.5, 2)})); tl.to("#c2-k{k}", {{ x: {[150, 130, 200][k]}, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 3 }}, A({round(W(15, 0.45) + k * 0.5 + 0.7, 2)}));' for k in range(3))}
    {"".join(f'draw("#c2-tl{k}", {round(W(16, 0.45) + k * 0.45, 2)}, 0.4);' for k in range(5))}
    slideIn("#c2-min", {L(17)});
    {"".join(f'tl.to("#c2-mi{k}", {{ y: "+=8", duration: 0.15, yoyo: true, repeat: 3 }}, A({round(W(17, 0.3) + k * 0.25, 2)}));' for k in range(3))}
    draw("#c2-tacha", {W(18, 0.5)}, 0.4);
    draw("#c2-nueva", {W(18, 0.62)}, 0.5);
    tl.set("#c2-ley", {{ scale: 2, transformOrigin: C }}, A({W(18, 0.82)}));
    tl.to("#c2-ley", {{ opacity: 1, scale: 1, duration: 0.18, ease: "power4.in" }}, A({W(18, 0.82)}));
    flow("#c2-in", {L(19)}, {TT[19][1]}, 60);
    flow("#c2-out", {L(19)}, {TT[19][1]}, 60);
    stream("#c2-ci", 3, {W(19, 0.15)}, {TT[19][1]}, 220, 0, 1.0);
    stream("#c2-co", 3, {W(19, 0.35)}, {TT[19][1]}, 220, 0, 1.0);
    {"".join(f'draw("#c2-lb{k}", {round(W(20, 0.25) + k * 0.6, 2)}, 0.4);' for k in range(5))}
    stream("#c2-cr", 3, {W(20, 0.2)}, {TT[21][1]}, -160, 0, 0.6);
    pop("#c2-esc", {L(21)});
    show("#c2-fuera", {W(21, 0.15)});
    tl.to("#c2-cf", {{ x: -70, duration: 0.5, ease: "power2.in" }}, A({W(21, 0.35)}));
    tl.to("#c2-cf", {{ x: 10, duration: 0.4, ease: "power2.out" }}, A({W(21, 0.35) + 0.5}));
    wob("#c2-esc", {W(21, 0.5)}, {W(21, 0.75)}, 5, 0.15);
    growY("#c2-bp", {W(22, 0.25)}, 0.8);
    growY("#c2-bh", {W(22, 0.4)}, 0.8);
    tl.to("#c2-bh", {{ scaleY: 1.12, transformOrigin: "50% 100%", duration: 0.5, yoyo: true, repeat: 1, ease: "sine.inOut" }}, A({W(22, 0.62)}));
    tl.fromTo("#c2-mart", {{ rotation: -25, transformOrigin: "100% 100%" }}, {{ rotation: 12, duration: 0.18, ease: "power4.in", yoyo: true, repeat: 3, transformOrigin: "100% 100%" }}, A({W(22, 0.4)}));"""
chapter("c2", B[2], B[3], "Capítulo 2", "Las seis etapas", P, "#9ff0cf", 56.9, [], [], svg, js)

# ================================================================ C3 (1.ª parte)
P = "#2f78c4"
def phdr(cid, n, nombre, art=""):
    a = f'<g><rect x="640" y="26" width="226" height="44" rx="22" fill="{P}" opacity="0.15" />{T(753, 58, 28, art, "b", fill=P)}</g>' if art else ""
    return f'{T(30, 62, 28, f"{n}/11", "b", "start", "#636e72")}{T(118, 62, 40, nombre, "b", "start", P)}{a}'

svg = f"""
      <g id="c3-p1" class="h">
        {phdr("c3", 1, "Legalidad")}
        <g transform="translate(700 260)">{I_BOVEDA}</g>{T(700, 360, 30, "Tesoro", "b")}
        <g id="c3-mano"><rect x="40" y="236" width="230" height="44" rx="22" fill="#f5c9a0" /><circle cx="280" cy="258" r="34" fill="#f5c9a0" />{T(140, 222, 28, "el gobierno", "b")}</g>
        <g id="c3-reja"><rect x="520" y="150" width="60" height="230" fill="none" stroke="#d63031" stroke-width="8" /><path d="M540,150 L540,380 M560,150 L560,380" stroke="#d63031" stroke-width="8" /></g>
        <g id="c3-ley" class="h"><g transform="translate(440 130) scale(0.7)">{I_DOC}</g>{T(440, 200, 28, "ley", "b", fill=P)}</g>
        {T(440, 440, 30, "limita la arbitrariedad", "b", fill=P)}
      </g>
      <g id="c3-p2" class="h">
        {phdr("c3", 2, "Equilibrio")}
        <path d="M440,190 L410,400 L470,400 Z" fill="#636e72" />
        <g id="c3-viga"><rect x="180" y="176" width="520" height="16" rx="8" fill="#2d3436" /></g>
        <circle cx="440" cy="184" r="14" fill="#2d3436" />
        <g id="c3-pl"><path d="M190,190 L150,280 M190,190 L230,280" stroke="#636e72" stroke-width="4" /><path d="M120,280 L260,280 Q250,320 190,320 Q130,320 120,280 Z" fill="#00b894" />{T(190, 360, 28, "Recursos", "b")}<text id="c3-rv" x="190" y="262" font-size="34" class="b" text-anchor="middle" fill="#00b894">$0</text>
          <g id="c3-deuda" class="h"><rect x="150" y="206" width="80" height="40" rx="8" fill="#e17055" />{T(190, 234, 28, "deuda", "b", fill="#ffffff")}</g></g>
        <g id="c3-pr"><path d="M690,190 L650,280 M690,190 L730,280" stroke="#636e72" stroke-width="4" /><path d="M620,280 L760,280 Q750,320 690,320 Q630,320 620,280 Z" fill="#e17055" />{T(690, 360, 28, "Gastos", "b")}<text id="c3-gv" x="690" y="262" font-size="34" class="b" text-anchor="middle" fill="#e17055">$0</text></g>
        {check("c3-ok", 440, 120, 28)}
        <g id="c3-def" class="h">{box(330, 96, 220, 50, "déficit $20", "#d63031", s=30)}</g>
      </g>
      <g id="c3-p3" class="h">
        {phdr("c3", 3, "Exactitud")}
        {T(440, 110, 28, "mejores métodos para estimar el futuro", "m", fill="#636e72")}
        """ + "".join(f'<rect id="c3-eb{k}" x="{120 + k * 150}" y="{[260, 230, 240, 200][k]}" width="100" height="{[140, 170, 160, 200][k]}" rx="10" fill="#a8d1ff" />' for k in range(4)) + f"""
        <rect id="c3-eb4" x="720" y="170" width="100" height="230" rx="10" fill="none" stroke="{P}" stroke-width="5" stroke-dasharray="12 8" />
        {line_draw("c3-trend", "M170,255 L320,225 L470,235 L620,195 L770,165", P, 6)}
        {T(390, 440, 28, "años anteriores", "b")}{T(770, 440, 28, "año próximo", "b", fill=P)}
        <g id="c3-q">{T(770, 300, 64, "?", "b", fill=P)}</g>
        <g id="c3-eq" class="h">{T(770, 300, 64, "≈", "b", fill=P)}</g>
      </g>
      <g id="c3-p4" class="h">
        {phdr("c3", 4, "Universalidad", "art. 11 Ley 4938")}
        <g transform="translate(440 250)"><rect x="-90" y="-80" width="180" height="160" fill="#dfe6e9" stroke="#2d3436" stroke-width="5" /><path d="M-100,-80 L100,-80 L80,-120 L-80,-120 Z" fill="{P}" />{T(0, 10, 30, "Oficina", "b")}</g>
        {arrow("c3-uin", "M60,200 L330,200", "#00b894", 8)}{arrow("c3-uout", "M550,300 L820,300", "#e17055", 8)}
        {T(170, 170, 28, "tasas", "b", fill="#00b894")}<text id="c3-uv1" x="170" y="250" font-size="34" class="b" text-anchor="middle" fill="#00b894">$0</text>
        {T(700, 270, 28, "papel", "b", fill="#e17055")}<text id="c3-uv2" x="700" y="350" font-size="34" class="b" text-anchor="middle" fill="#e17055">$0</text>
        <g id="c3-neto" class="h">{box(310, 370, 260, 56, "neto $20.000", "#636e72", s=30)}{line_draw("c3-netox", "M300,398 L580,398", "#d63031", 8)}</g>
        <g id="c3-bien" class="h"><rect x="40" y="370" width="800" height="90" rx="16" fill="#e3f0ff" />{T(240, 425, 30, "recurso $100.000", "b", fill="#00b894")}{T(640, 425, 30, "gasto $80.000", "b", fill="#e17055")}</g>
      </g>
      <g id="c3-p5" class="h">
        {phdr("c3", 5, "Unidad", "art. 21 Ley 4938")}
        {box(40, 100, 230, 56, "Ingresos Brutos", "#00b894", s=28)}
        <ellipse cx="400" cy="350" rx="210" ry="70" fill="#a8d1ff" />{T(400, 362, 32, "masa común", "b", fill=P)}
        {coins("c3-un", 4, 155, 160)}
        {box(610, 100, 250, 56, "sueldos docentes", "#e17055", s=28)}
        {arrow("c3-dir", "M270,128 L600,128", "#e17055", 7, head=False)}
        {cross("c3-dirx", 440, 128, 26)}
        {box(660, 320, 200, 70, "todo el gasto", "#636e72", s=28)}
        {arrow("c3-sal", "M610,355 L655,355", P, 8)}
        <g id="c3-valv" class="h"><circle cx="230" cy="300" r="24" fill="#fdcb6e" stroke="#2d3436" stroke-width="4" /><path d="M214,300 L246,300" stroke="#2d3436" stroke-width="6" />{T(160, 450, 28, "salvo afectación por ley", "b", fill="#b7791f")}</g>
      </g>
      <g id="c3-p6" class="h">
        {phdr("c3", 6, "Unidad de caja")}
        {T(440, 110, 28, "un solo órgano central recibe todos los fondos", "m", fill="#636e72")}
        <g transform="translate(160 270)"><rect x="-90" y="-70" width="180" height="140" fill="#dfe6e9" stroke="#2d3436" stroke-width="5" />{T(0, 10, 28, "Dirección", "b")}</g>
        <g transform="translate(720 270)">{I_BOVEDA}</g>{T(720, 380, 30, "Tesorería", "b")}
        <g id="c3-sus" class="h">{box(80, 380, 160, 50, "sus gastos", "#e17055", s=28)}{cross("c3-susx", 250, 405, 24)}</g>
        <g id="c3-bolsa" class="h"><path d="M140,190 Q120,240 150,262 L210,262 Q240,240 220,190 Z" fill="#fdcb6e" stroke="#b7791f" stroke-width="4" />{T(180, 248, 30, "$", "b", fill="#b7791f")}</g>
        {line_draw("c3-camino", "M230,230 Q440,140 640,230", "#b2bec3", 6)}
      </g>"""
js = f"""
    slideIn("#c3-p1", {L(24) - 0.2});
    tl.to("#c3-mano", {{ x: 200, duration: 0.6, ease: "power2.out" }}, A({W(24, 0.15)}));
    tl.set("#c3-reja", {{ y: -260 }}, 0);
    tl.to("#c3-reja", {{ y: 0, duration: 0.35, ease: "bounce.out" }}, A({W(24, 0.28)}));
    tl.to("#c3-mano", {{ x: 120, duration: 0.25 }}, A({W(24, 0.36)}));
    drop("#c3-ley", {W(24, 0.55)});
    tl.to("#c3-reja", {{ y: -260, duration: 0.4, ease: "power2.in" }}, A({W(24, 0.68)}));
    tl.to("#c3-mano", {{ x: 290, duration: 0.6, ease: "power2.out" }}, A({W(24, 0.75)}));
    slideOut("#c3-p1", {L(25)});
    slideIn("#c3-p2", {L(25)});
    tl.fromTo("#c3-viga", {{ rotation: -3, svgOrigin: "440 184" }}, {{ rotation: 3, svgOrigin: "440 184", duration: 0.6, yoyo: true, repeat: 3, ease: "sine.inOut" }}, A({L(25)}));
    tl.to("#c3-viga", {{ rotation: 0, svgOrigin: "440 184", duration: 0.3 }}, A({L(26)}));
    count("#c3-rv", 0, 100, {W(26, 0.3)}, 0.9);
    count("#c3-gv", 0, 100, {W(26, 0.55)}, 0.9);
    pop("#c3-ok", {W(26, 0.85)});
    hide("#c3-ok", {L(27)});
    count("#c3-gv", 100, 120, {W(27, 0.18)}, 0.8);
    tl.to("#c3-viga", {{ rotation: 8, svgOrigin: "440 184", duration: 0.7, ease: "back.out(1.5)" }}, A({W(27, 0.25)}));
    tl.to("#c3-pl", {{ y: -36, duration: 0.7, ease: "back.out(1.5)" }}, A({W(27, 0.25)}));
    tl.to("#c3-pr", {{ y: 36, duration: 0.7, ease: "back.out(1.5)" }}, A({W(27, 0.25)}));
    pop("#c3-def", {W(27, 0.38)});
    drop("#c3-deuda", {W(27, 0.78)});
    tl.to("#c3-viga", {{ rotation: 0, svgOrigin: "440 184", duration: 0.7, ease: "back.out(1.5)" }}, A({W(27, 0.85)}));
    tl.to(["#c3-pl", "#c3-pr"], {{ y: 0, duration: 0.7, ease: "back.out(1.5)" }}, A({W(27, 0.85)}));
    hide("#c3-def", {W(27, 0.95)});
    slideOut("#c3-p2", {L(28)});
    slideIn("#c3-p3", {L(28)});
    {"".join(f'growY("#c3-eb{k}", {round(W(29, 0.05) + k * 0.45, 2)}, 0.6);' for k in range(4))}
    tl.to(["#c3-eb0", "#c3-eb1", "#c3-eb2", "#c3-eb3"], {{ scaleY: 1.04, transformOrigin: "50% 100%", duration: 0.5, yoyo: true, repeat: 5, ease: "sine.inOut", stagger: 0.12 }}, A({W(29, 0.45)}));
    draw("#c3-trend", {W(29, 0.4)}, 1.4);
    wob("#c3-q", {L(28)}, {W(29, 0.65)}, 10, 0.5);
    growY("#c3-eb4", {W(29, 0.55)}, 0.8);
    hide("#c3-q", {W(29, 0.8)});
    pop("#c3-eq", {W(29, 0.8)});
    slideOut("#c3-p3", {L(30)});
    slideIn("#c3-p4", {L(30)});
    flow("#c3-uin", {L(31)}, {TT[32][1]}, 60);
    flow("#c3-uout", {W(31, 0.5)}, {TT[32][1]}, 60);
    count("#c3-uv1", 0, 100000, {W(31, 0.15)}, 1.4);
    count("#c3-uv2", 0, 80000, {W(31, 0.6)}, 1.4);
    show("#c3-neto", {W(32, 0.1)});
    draw("#c3-netox", {W(32, 0.62)}, 0.4);
    hide("#c3-neto", {W(32, 0.78)});
    slideIn("#c3-bien", {W(32, 0.8)});
    slideOut("#c3-p4", {L(33)});
    slideIn("#c3-p5", {L(33)});
    stream("#c3-un", 4, {W(33, 0.2)}, {TT[34][1]}, 200, 170, 1.1);
    flow("#c3-dir", {W(34, 0.0)}, {W(34, 0.3)}, 60);
    pop("#c3-dirx", {W(34, 0.3)});
    flow("#c3-sal", {W(34, 0.5)}, {TT[34][1]}, 60);
    pulse("#c3-p5 ellipse", {W(34, 0.55)});
    pop("#c3-valv", {W(34, 0.8)});
    spin("#c3-valv", {W(34, 0.85)}, {TT[34][1]}, 180);
    slideOut("#c3-p5", {L(35)});
    slideIn("#c3-p6", {L(35)});
    pop("#c3-bolsa", {W(36, 0.05)});
    show("#c3-sus", {W(36, 0.2)});
    tl.to("#c3-bolsa", {{ x: -30, y: 100, duration: 0.4, ease: "power2.inOut" }}, A({W(36, 0.25)}));
    pop("#c3-susx", {W(36, 0.38)});
    tl.to("#c3-bolsa", {{ x: 0, y: 0, duration: 0.3 }}, A({W(36, 0.48)}));
    draw("#c3-camino", {W(36, 0.55)}, 0.5);
    travel("#c3-bolsa", {W(36, 0.62)}, 500, 30, 1.3, -110);
    tl.to("#c3-bolsa", {{ scale: 0, transformOrigin: C, duration: 0.3 }}, A({W(36, 0.62) + 1.35}));
    pulse("#c3-p6 g:nth-of-type(2)", {W(36, 0.9)});"""
chapter("c3", B[3], B[4], "Capítulo 3", "Principios presupuestarios", P, "#a8d1ff", L(24) - 0.25,
        [(L(26), TT[27][1]), (L(31), TT[32][1]), (L(34), TT[34][1]), (L(36), B[4] - 0.05)],
        [(L(29), TT[29][1])], svg, js, title_sub="1.ª parte")

# ================================================================ C3 (2.ª parte)
svg = f"""
      <g id="c3b-p7" class="h">
        {phdr("c3b", 7, "Publicidad")}
        {T(440, 108, 28, "el presupuesto no es secreto", "m", fill="#636e72")}
        <rect x="300" y="130" width="280" height="200" rx="12" fill="#ffffff" stroke="#2d3436" stroke-width="6" />
        <rect x="300" y="130" width="280" height="50" rx="10" fill="{P}" />{T(440, 166, 28, "PRESUPUESTO", "b", fill="#ffffff")}
        """ + "".join(f'<rect id="c3b-pb{k}" x="330" y="{200 + k * 36}" width="{[200, 150, 180][k]}" height="20" rx="10" fill="#a8d1ff" />' for k in range(3)) + "".join(
    f'<g id="c3b-v{k}" class="h"><g transform="translate({[90, 190, 690, 790][k]} {[390, 360, 360, 390][k]}) scale(1.3)">{I_PERSONA}</g></g>' for k in range(4)) + f"""
        <g id="c3b-lupa"><circle cx="400" cy="250" r="40" fill="none" stroke="#2d3436" stroke-width="10" /><path d="M428,278 L470,320" stroke="#2d3436" stroke-width="14" stroke-linecap="round" /></g>
        <g id="c3b-preg" class="h">{box(290, 360, 300, 56, "¿en qué se gasta?", "#2d3436", s=28)}</g>
      </g>
      <g id="c3b-p8" class="h">
        {phdr("c3b", 8, "Claridad")}
        {T(440, 108, 28, "que lo entienda alguien sin formación contable", "m", fill="#636e72")}
        """ + "".join(
    f'<g id="c3b-c{k}">{T(0, 0, 32, lab, "b", fill="#636e72", extra=f"transform=\"translate({x} {y}) rotate({r})\"")}</g>'
    for k, (lab, x, y, r) in enumerate([("3.4.1.2", 150, 200, -20), ("x7-b", 380, 330, 15), ("∑ 0912", 640, 220, -8), ("Inc. 2/b", 260, 410, 10), ("01-a", 720, 400, -15), ("#45.6", 520, 170, 22)])) + "".join(
    f'<g id="c3b-r{k}" class="h"><rect x="120" y="{150 + k * 90}" width="640" height="70" rx="16" fill="#e3f0ff" />{T(150, {0: 195, 1: 285, 2: 375}[k], 32, lab, "b", "start", P)}<rect id="c3b-rb{k}" x="470" y="{170 + k * 90}" width="{[260, 200, 160][k]}" height="30" rx="15" fill="{P}" /></g>'
    for k, lab in enumerate(["Educación", "Salud", "Seguridad"])) + f"""
      </g>
      <g id="c3b-p9" class="h">
        {phdr("c3b", 9, "Especificación")}
        {T(440, 108, 28, "cada autorización tiene un fin claro", "m", fill="#636e72")}
        <rect x="60" y="150" width="340" height="240" rx="20" fill="#e3f0ff" stroke="{P}" stroke-width="6" />
        {T(230, 200, 30, "crédito: Personal", "b", fill=P)}
        """ + "".join(f'<g transform="translate({130 + k * 70} 320) scale(1.2)">{I_PERSONA}</g>' for k in range(4)) + f"""
        <rect id="c3b-barr" class="h" x="420" y="150" width="20" height="240" rx="8" fill="#d63031" />
        <g id="c3b-auto"><g transform="translate(700 320) scale(1.3)">{I_AUTO}</g></g>
        {cross("c3b-x", 520, 190, 30)}
      </g>
      <g id="c3b-p10" class="h">
        {phdr("c3b", 10, "Anualidad", "art. 9 Ley 4938")}
        <rect x="80" y="110" width="300" height="250" rx="18" fill="#ffffff" stroke="#2d3436" stroke-width="6" />
        <rect x="80" y="110" width="300" height="70" rx="16" fill="{P}" />
        {T(230, 158, 30, "año financiero", "b", fill="#ffffff")}
        <text id="c3b-dia" x="230" y="300" font-size="60" class="b" text-anchor="middle" fill="#2d3436">1 ENE</text>
        <rect x="80" y="380" width="300" height="20" rx="10" fill="#e3f0ff" /><rect id="c3b-prog" x="80" y="380" width="300" height="20" rx="10" fill="{P}" />
        <rect x="560" y="140" width="240" height="210" rx="18" fill="#f1f2f6" stroke="#b2bec3" stroke-width="6" stroke-dasharray="14 10" />
        {T(680, 260, 30, "año siguiente", "b", fill="#636e72")}
        {coin("c3b-mon", 330, 330, 26)}
        {cross("c3b-x2", 480, 200, 28)}
      </g>
      <g id="c3b-p11" class="h">
        {phdr("c3b", 11, "Precedencia")}
        {T(440, 108, 28, "se aprueba antes de que empiece el año", "m", fill="#636e72")}
        <path d="M40,300 L840,300" stroke="#2d3436" stroke-width="6" />
        """ + "".join(f'<path d="M{x},288 L{x},312" stroke="#2d3436" stroke-width="5" />{T(x, 350, 28, lab, "b", fill="#d63031" if lab == "1 ene" else "#2d3436")}' for x, lab in [(120, "dic"), (330, "1 ene"), (530, "feb"), (730, "mar")]) + f"""
        <path d="M330,160 L330,300" stroke="#d63031" stroke-width="4" stroke-dasharray="10 8" />
        <g id="c3b-ok" class="h" data-layout-allow-overlap><g transform="rotate(-8 190 210)"><rect x="70" y="170" width="240" height="80" rx="12" fill="#ffffff" stroke="#00b894" stroke-width="7" />{T(190, 205, 28, "Presupuesto 2027", "b", fill="#00b894")}{T(190, 238, 28, "aprobado ✓", "b", fill="#00b894")}</g></g>
        <g id="c3b-mal" class="h" data-layout-allow-overlap><g transform="rotate(8 730 210)"><rect x="610" y="170" width="240" height="80" rx="12" fill="#ffffff" stroke="#d63031" stroke-width="7" />{T(730, 205, 28, "aprobado", "b", fill="#d63031")}{T(730, 238, 28, "en marzo", "b", fill="#d63031")}</g></g>
        {arrow("c3b-back", "M650,270 Q530,410 360,320", "#d63031", 6)}
        <g id="c3b-cub" class="h">{T(520, 440, 28, "«cubrir enero»", "b", fill="#d63031")}</g>
        {cross("c3b-x3", 730, 140, 28)}
      </g>"""
js = f"""
    slideIn("#c3b-p7", {L(37) - 0.1});
    {"".join(f'pop("#c3b-v{k}", {round(W(37, 0.4) + k * 0.25, 2)}); bob("#c3b-v{k}", {round(W(37, 0.5) + k * 0.25, 2)}, {TT[37][1]}, 6, 0.7);' for k in range(4))}
    tl.to("#c3b-lupa", {{ x: 100, y: 30, duration: 0.8, ease: "sine.inOut", yoyo: true, repeat: 3 }}, A({W(37, 0.2)}));
    pop("#c3b-preg", {W(37, 0.7)});
    slideOut("#c3b-p7", {L(38)});
    slideIn("#c3b-p8", {L(38)});
    {"".join(f'wob("#c3b-c{k}", {L(38)}, {W(38, 0.38)}, 6, 0.4);' for k in range(6))}
    {"".join(f'tl.to("#c3b-c{k}", {{ opacity: 0, scale: 0.3, x: {[150, -100, -200, 80, -250, 0][k]}, y: {[-40, -80, 40, -140, -100, 60][k]}, transformOrigin: C, duration: 0.5, ease: "power2.in" }}, A({round(W(38, 0.4) + k * 0.06, 2)}));' for k in range(6))}
    {"".join(f'slideIn("#c3b-r{k}", {round(W(38, 0.5) + k * 0.3, 2)}); grow("#c3b-rb{k}", {round(W(38, 0.55) + k * 0.3, 2)}, 0.8);' for k in range(3))}
    slideOut("#c3b-p8", {L(39)});
    slideIn("#c3b-p9", {L(39)});
    show("#c3b-barr", {W(39, 0.5)});
    tl.to("#c3b-auto", {{ x: -230, duration: 0.8, ease: "power2.in" }}, A({W(39, 0.55)}));
    tl.to("#c3b-auto", {{ x: -110, rotation: 8, transformOrigin: C, duration: 0.5, ease: "power2.out" }}, A({W(39, 0.55) + 0.8}));
    pop("#c3b-x", {W(39, 0.55) + 0.8});
    wob("#c3b-barr", {W(39, 0.55) + 0.8}, {W(39, 0.55) + 1.3}, 3, 0.15);
    slideOut("#c3b-p9", {L(40)});
    slideIn("#c3b-p10", {L(40)});
    count("#c3b-dia", 0, 11, {W(40, 0.2)}, {round((TT[40][1] - TT[40][0]) * 0.75, 2)}, (v) => v >= 10.99 ? "31 DIC" : "1 " + ["ENE","FEB","MAR","ABR","MAY","JUN","JUL","AGO","SEP","OCT","NOV","DIC"][Math.floor(v)]);
    grow("#c3b-prog", {W(40, 0.2)}, {round((TT[40][1] - TT[40][0]) * 0.75, 2)});
    pop("#c3b-mon", {L(41)});
    travel("#c3b-mon", {W(41, 0.15)}, 260, -120, 1.0, -170);
    pop("#c3b-x2", {W(41, 0.5)});
    tl.to("#c3b-mon", {{ opacity: 0, scale: 0.2, transformOrigin: C, duration: 0.5 }}, A({W(41, 0.55)}));
    slideOut("#c3b-p10", {L(42)});
    slideIn("#c3b-p11", {L(42)});
    tl.set("#c3b-ok", {{ y: -200, scale: 1.2, transformOrigin: C }}, A({W(43, 0.12)}));
    tl.to("#c3b-ok", {{ y: 0, scale: 1, opacity: 1, duration: 0.45, ease: "bounce.out" }}, A({W(43, 0.12)}));
    tl.set("#c3b-mal", {{ y: -200 }}, A({W(43, 0.55)}));
    tl.to("#c3b-mal", {{ y: 0, opacity: 1, duration: 0.45, ease: "bounce.out" }}, A({W(43, 0.55)}));
    draw("#c3b-back", {W(43, 0.7)}, 0.6);
    tl.set("#c3b-back", {{ strokeDasharray: "14 10", strokeDashoffset: 0 }}, A({W(43, 0.7)}));
    tl.fromTo("#c3b-back", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, A({W(43, 0.7)}));
    flow("#c3b-back", {W(43, 0.72)}, {TT[43][1]}, 60);
    show("#c3b-cub", {W(43, 0.75)});
    pop("#c3b-x3", {W(43, 0.88)});
    wob("#c3b-ok", {W(43, 0.5)}, {TT[43][1]}, 3, 0.6);"""
js = js.replace('draw("#c3b-back", ' + str(W(43, 0.7)) + ', 0.6);\n', '')
chapter("c3b", B[4], B[5], "Capítulo 3", "Principios presupuestarios", P, "#a8d1ff", L(37) - 0.15,
        [(L(39), TT[39][1]), (L(43), B[5] - 0.05)], [(L(37), TT[38][1])], svg, js, title_sub="2.ª parte")

# ================================================================ C4
P = "#d9761e"
inc = ["personal", "bienes de consumo", "servicios no personales", "bienes de uso", "transferencias",
       "activos financieros", "servicios de la deuda", "otros gastos", "gastos figurativos"]
svg = f"""
      <g id="c4-a" class="h">
        {T(440, 52, 36, "Un cuadro de contabilidad preventiva", "b", fill=P)}
        <rect x="40" y="80" width="800" height="70" rx="14" fill="#fff1e3" />
        {T(240, 126, 30, "Ingresos probables", "b", fill="#00b894")}{T(640, 126, 30, "Gastos", "b", fill="#e17055")}
        <path d="M440,80 L440,420" stroke="#2d3436" stroke-width="5" />
        """ + "".join(f'<rect id="c4-ri{k}" x="80" y="{180 + k * 60}" width="{[280, 220, 250][k]}" height="30" rx="15" fill="#55efc4" /><rect id="c4-rg{k}" x="480" y="{180 + k * 60}" width="{[300, 240, 200][k]}" height="30" rx="15" fill="#fab1a0" /><rect id="c4-tp{k}" class="h" x="{480 + [300, 240, 200][k] + 6}" y="{172 + k * 60}" width="10" height="46" rx="4" fill="#d63031" />' for k in range(3)) + "".join(
    f'<g id="c4-ld{k}" class="h"><g transform="translate({70 + k * 40} 430) scale(0.4)">{I_DOC}</g></g>' for k in range(3)) + f"""
        <g id="c4-otras" class="h">{T(250, 440, 28, "← otras leyes", "b", fill="#00b894")}</g>
        <g id="c4-lim" class="h">{T(640, 440, 28, "límite", "b", fill="#d63031")}</g>
      </g>
      <g id="c4-b" class="h">
        {T(440, 52, 38, "Clasificadores", "b", fill=P)}
        <path d="M340,80 L540,80 L480,180 L400,180 Z" fill="#636e72" />
        <rect x="380" y="180" width="120" height="60" fill="#2d3436" />
        """ + "".join(f'{box(25 + k * 212, 330, 196, 90, "", "#fff1e3", s=28)}{T(123 + k * 212, 366, 28, l1, "b", fill=P)}{T(123 + k * 212, 400, 28, l2, "b", fill=P)}' for k, (l1, l2) in enumerate([("carácter", "económico"), ("procedencia", ""), ("objeto", "del gasto"), ("finalidad", "y función")])) + "".join(
    f'<rect id="c4-cd{k}" class="h" x="415" y="200" width="50" height="34" rx="6" fill="{["#e17055", "#00b894", "#74b9ff", "#fdcb6e"][k]}" />' for k in range(4)) + f"""
        <g id="c4-dec" class="h">{box(560, 110, 290, 56, "decreto acuerdo · cada año", P, s=28)}</g>
      </g>
      <g id="c4-c" class="h">
        {T(440, 52, 38, "Por carácter económico", "b", fill=P)}
        """ + "".join(f'<path d="M{60 + k * 280},250 L{100 + k * 280},420 L{260 + k * 280},420 L{300 + k * 280},250" fill="#fff1e3" stroke="{P}" stroke-width="6" />{T(180 + k * 280, 395, 30, lab, "b", fill=P)}' for k, lab in enumerate(["corrientes", "de capital", "financieros"])) + "".join(
    f'<g id="c4-ce{k}" class="h">{box(80 + k * 280, 110, 200, 56, lab, "#636e72", s=28)}</g>' for k, lab in enumerate(["personal", "ambulancia", "amortización"])) + f"""
      </g>
      <g id="c4-d" class="h">
        {T(440, 52, 38, "Por procedencia u origen", "b", fill=P)}
        <g transform="translate(720 260)">{I_BOVEDA}</g>{T(720, 370, 30, "recursos", "b")}
        {arrow("c4-o1", "M200,150 Q450,150 630,230", "#00b894", 8)}{arrow("c4-o2", "M200,260 L630,260", "#0984e3", 8)}{arrow("c4-o3", "M200,370 Q450,370 630,290", "#636e72", 8)}
        {T(110, 160, 30, "provincial", "b", fill="#00b894")}{T(110, 270, 30, "nacional", "b", fill="#0984e3")}{T(110, 362, 28, "otros", "b", fill="#636e72")}{T(110, 394, 28, "orígenes", "b", fill="#636e72")}
        <g id="c4-iibb" class="h">{coin("c4-ic", 220, 150, 28, "")}{T(220, 110, 28, "Ingresos Brutos", "b", fill="#00b894")}</g>
      </g>
      <g id="c4-e" class="h">
        {T(440, 50, 36, "Por objeto del gasto: 9 incisos", "b", fill=P)}
        """ + "".join(
    f'<g id="c4-i{k}" class="h"><rect x="{20 + (k // 5) * 430}" y="{76 + (k % 5) * 76}" width="410" height="64" rx="12" fill="#fff1e3" /><circle cx="{56 + (k // 5) * 430}" cy="{108 + (k % 5) * 76}" r="22" fill="{P}" />{T(56 + (k // 5) * 430, 118 + (k % 5) * 76, 28, str(k + 1), "b", fill="#ffffff")}{T(92 + (k // 5) * 430, 118 + (k % 5) * 76, 28, lab, "b", "start")}</g>'
    for k, lab in enumerate(inc)) + f"""
      </g>
      <g id="c4-f" class="h">
        {T(440, 52, 38, "Por finalidad y función", "b", fill=P)}
        {T(440, 100, 28, "qué servicios presta el Estado a la comunidad", "m", fill="#636e72")}
        <g id="c4-f1" class="h"><g transform="translate(180 260)">{I_ESCUELA}</g>{T(180, 380, 30, "educación", "b")}</g>
        <g id="c4-f2" class="h"><g transform="translate(440 260)">{I_HOSPITAL}</g>{T(440, 380, 30, "salud", "b")}</g>
        <g id="c4-f3" class="h"><g transform="translate(700 260)"><path d="M-50,-60 L0,-78 L50,-60 L50,0 Q50,52 0,74 Q-50,52 -50,0 Z" fill="#0984e3"/></g>{T(700, 380, 30, "seguridad", "b")}</g>
      </g>
      <g id="c4-g" class="h">
        {T(440, 52, 36, "Una cuenta, varios clasificadores", "b", fill=P)}
        """ + "".join(f'<g id="c4-pt{k}"><rect x="{70 + k * 270}" y="80" width="200" height="56" rx="14" fill="#fff1e3" />{T(170 + k * 270, 117, 28, lab, "b", fill=P)}</g>' for k, lab in enumerate(["Objeto", "Carácter", "Finalidad"])) + "".join(
    f'<path d="M{170 + k * 270},136 L{170 + k * 270},200" stroke="{P}" stroke-width="5" stroke-dasharray="10 8" />' for k in range(3)) + f"""
        <g id="c4-card">
          <rect x="20" y="210" width="330" height="76" rx="16" fill="#2d3436" />
          <text id="c4-ct" x="185" y="259" font-size="30" class="b" text-anchor="middle" fill="#ffffff">Sueldo de un docente</text>
          """ + "".join(f'<g id="c4-tg{k}" class="h"><rect x="20" y="{298 + k * 52}" width="330" height="44" rx="22" fill="{["#c0392b", "#0767b5", "#00785a"][k]}" /><text id="c4-tt{k}" x="185" y="{330 + k * 52}" font-size="28" class="b" text-anchor="middle" fill="#ffffff">{["Personal", "Gasto corriente", "Serv. sociales · Educación"][k]}</text></g>' for k in range(3)) + f"""
        </g>
        <g id="c4-amb" class="h">
          <g transform="translate(185 240) scale(0.9)">{I_AMBU}</g>
          """ + "".join(f'<g id="c4-ag{k}" class="h"><rect x="20" y="{298 + k * 52}" width="330" height="44" rx="22" fill="{["#c0392b", "#0767b5", "#00785a"][k]}" />{T(185, 330 + k * 52, 28, ["Bienes de uso", "Gasto de capital", "Salud"][k], "b", fill="#ffffff")}</g>' for k in range(3)) + f"""
        </g>
      </g>"""
gates = [W(54, 0.25), W(54, 0.55), W(54, 0.85)]
agates = [W(55, 0.38), W(55, 0.62), W(55, 0.85)]
js = f"""
    slideIn("#c4-a", {L(45)});
    {"".join(f'grow("#c4-ri{k}", {round(W(45, 0.3) + k * 0.35, 2)}, 0.7); grow("#c4-rg{k}", {round(W(45, 0.65) + k * 0.35, 2)}, 0.7);' for k in range(3))}
    {"".join(f'drop("#c4-ld{k}", {round(W(46, 0.05) + k * 0.25, 2)}); tl.to("#c4-ld{k}", {{ y: -60 - {k * 60}, x: 60, opacity: 0, duration: 0.6, ease: "power2.in" }}, A({round(W(46, 0.25) + k * 0.25, 2)}));' for k in range(3))}
    {"".join(f'tl.to("#c4-ri{k}", {{ scaleX: 1.1, transformOrigin: "0% 50%", duration: 0.3, yoyo: true, repeat: 1 }}, A({round(W(46, 0.3) + k * 0.25, 2)}));' for k in range(3))}
    show("#c4-otras", {W(46, 0.15)});
    {"".join(f'drop("#c4-tp{k}", {round(W(46, 0.55) + k * 0.2, 2)});' for k in range(3))}
    show("#c4-lim", {W(46, 0.6)});
    slideOut("#c4-a", {L(47)});
    slideIn("#c4-b", {L(47)});
    {"".join(f'tl.set("#c4-cd{k}", {{ x: 0, y: -140, opacity: 1 }}, A({round(W(47, 0.1) + k * 0.7, 2)})); tl.to("#c4-cd{k}", {{ y: 0, duration: 0.35, ease: "power2.in" }}, A({round(W(47, 0.1) + k * 0.7, 2)})); tl.to("#c4-cd{k}", {{ x: {(-317 + k * 212)}, y: 95, duration: 0.5, ease: "power2.inOut" }}, A({round(W(47, 0.1) + k * 0.7 + 0.35, 2)}));' for k in range(4))}
    pop("#c4-dec", {W(47, 0.68)});
    slideOut("#c4-b", {L(48)});
    slideIn("#c4-c", {L(48)});
    {"".join(f'pop("#c4-ce{k}", {round(W(48, 0.25) + k * 0.25, 2)}); tl.to("#c4-ce{k}", {{ y: 170, scale: 0.8, transformOrigin: C, duration: 0.5, ease: "bounce.out" }}, A({round(W(48, 0.25) + k * 0.25 + 0.45, 2)}));' for k in range(3))}
    slideOut("#c4-c", {L(49)});
    slideIn("#c4-d", {L(49)});
    flow("#c4-o1", {L(49)}, {TT[49][1]}, 60);
    flow("#c4-o2", {W(49, 0.15)}, {TT[49][1]}, 60);
    flow("#c4-o3", {W(49, 0.3)}, {TT[49][1]}, 60);
    pop("#c4-iibb", {W(49, 0.62)});
    tl.to("#c4-ic", {{ x: 380, y: 90, duration: 1.2, ease: "power1.inOut" }}, A({W(49, 0.72)}));
    tl.to("#c4-ic", {{ opacity: 0, duration: 0.2 }}, A({W(49, 0.72) + 1.2}));
    slideOut("#c4-d", {L(50)});
    tl.set("#c4-e", {{ opacity: 1 }}, A({L(50)}));
    {"".join(f'slideIn("#c4-i{k}", {round(L(50) + 0.05 + k * 0.17, 2)});' for k in range(9))}
    pulse("#c4-i0", {W(50, 0.42)});
    pulse("#c4-i1", {W(50, 0.6)});
    pulse("#c4-i3", {W(50, 0.78)});
    slideOut("#c4-e", {L(51)});
    tl.set("#c4-f", {{ opacity: 1 }}, A({L(51)}));
    {"".join(f'pop("#c4-f{k + 1}", {round(W(51, 0.3) + k * 0.3, 2)}); bob("#c4-f{k + 1}", {round(W(51, 0.45) + k * 0.3, 2)}, {TT[51][1]}, 8, 0.8);' for k in range(3))}
    slideOut("#c4-f", {L(52)});
    slideIn("#c4-g", {L(52)});
    {"".join(f'pulse("#c4-pt{k}", {round(W(52, 0.35) + k * 0.3, 2)});' for k in range(3))}
    tl.to("#c4-card", {{ x: -40, duration: 0.3 }}, A({W(53, 0.4)}));"""
for k, g in enumerate(gates):
    js += f'\n    tl.to("#c4-card", {{ x: {k * 270 - 15 + 150 - 185 + 20}, duration: 0.7, ease: "power2.inOut" }}, A({round(g - 0.7, 2)}));'
    js += f'\n    tl.set("#c4-tg{k}", {{ y: -20 }}, A({g}));\n    tl.to("#c4-tg{k}", {{ y: 0, opacity: 1, duration: 0.35, ease: "back.out(3)" }}, A({g}));'
    js += f'\n    pulse("#c4-pt{k}", {g});'
js += f'\n    tl.to("#c4-card", {{ x: 700, opacity: 0, duration: 0.5, ease: "power2.in" }}, A({round(L(55) - 0.2, 2)}));'
js += f'\n    tl.set("#c4-amb", {{ x: -300 }}, A({L(55)}));\n    tl.to("#c4-amb", {{ opacity: 1, x: -50, duration: 0.5, ease: "power2.out" }}, A({L(55)}));'
for k, g in enumerate(agates):
    js += f'\n    tl.to("#c4-amb", {{ x: {k * 270 - 15}, duration: 0.5, ease: "power2.inOut" }}, A({round(g - 0.5, 2)}));'
    js += f'\n    tl.set("#c4-ag{k}", {{ y: -20 }}, A({g}));\n    tl.to("#c4-ag{k}", {{ y: 0, opacity: 1, duration: 0.3, ease: "back.out(3)" }}, A({g}));'
    js += f'\n    pulse("#c4-pt{k}", {g});'
js += f'\n    wob("#c4-amb", {L(55)}, {B[6] - 0.2}, 1.5, 0.2);'
chapter("c4", B[5], B[6], "Capítulo 4", "Estructura y clasificadores", P, "#ffd3a8", L(44) + 2.4, [(L(53), B[6] - 0.05)], [(W(49, 0.6), TT[49][1])], svg, js)

# ================================================================ C5
P = "#c2405f"
svg = f"""
      <g id="c5-a" class="h">
        {T(440, 52, 36, "Tradicional o incremental", "b", fill=P)}
        {T(440, 96, 28, "sobre la base del año anterior", "m", fill="#636e72")}
        {T(60, 180, 30, "año pasado", "b", "start")}
        <rect id="c5-b1" x="260" y="150" width="300" height="50" rx="12" fill="#b2bec3" />{T(600, 186, 34, "$100", "b", "start")}
        {T(60, 280, 30, "este año", "b", "start")}
        <rect id="c5-b2" x="260" y="250" width="300" height="50" rx="12" fill="{P}" />
        <text id="c5-v2" x="600" y="286" font-size="34" class="b" text-anchor="start" fill="{P}">$100</text>
        <g id="c5-inf" class="h">{box(300, 206, 230, 40, "inflación +20 %", "#c0392b", s=28, rx=20)}</g>
        <g id="c5-nota" class="h"><rect x="200" y="340" width="480" height="64" rx="12" fill="#ffeaa7" />{T(440, 382, 28, "¿qué hizo con lo anterior?", "b")}{line_draw("c5-notax", "M210,372 L670,372", "#d63031", 8)}</g>
      </g>
      <g id="c5-b" class="h">
        {T(440, 52, 38, "Por programas", "b", fill=P)}
        <g id="c5-l1">{box(30, 140, 210, 56, "sueldos $X", "#636e72", s=28)}</g>
        <g id="c5-l2">{box(30, 220, 210, 56, "útiles $Y", "#636e72", s=28)}</g>
        <rect x="290" y="130" width="280" height="200" rx="20" fill="#fde4ea" stroke="{P}" stroke-width="6" />
        {T(430, 180, 28, "Programa", "b", fill=P)}{T(430, 216, 30, "Alfabetización", "b", fill=P)}
        {arrow("c5-ar", "M580,230 L650,230", P, 8)}
        """ + "".join(f'<g id="c5-k{k}" class="h"><g transform="translate({700 + (k % 2) * 90} {170 + (k // 2) * 110}) scale(1.2)">{I_PERSONA}<rect x="-18" y="-2" width="36" height="22" rx="3" fill="#ffffff" stroke="#2d3436" stroke-width="3"/></g></g>' for k in range(4)) + f"""
        {T(440, 400, 28, "insumo → producto: alumnos que aprenden a leer", "b", fill=P)}
      </g>
      <g id="c5-c" class="h">
        {T(440, 52, 38, "Por programas en base cero", "b", fill=P)}
        <g id="c5-badge">{box(600, 80, 250, 50, "hace 10 años", "#636e72", s=28)}</g>
        """ + "".join(f'<rect id="c5-z{k}" x="{100 + k * 150}" y="{[200, 160, 230][k]}" width="100" height="{[200, 240, 170][k]}" rx="10" fill="{P}" />{check(f"c5-zc{k}", 150 + k * 150, 170, 22)}' for k in range(3)) + f"""
        <text id="c5-anio" x="720" y="230" font-size="40" class="b" text-anchor="middle" fill="{P}">año 1</text>
        <g id="c5-pap">""" + "".join(f'<rect id="c5-pp{k}" class="h" x="{640 + (k % 2) * 8}" y="{400 - k * 18}" width="160" height="14" rx="3" fill="#ffffff" stroke="#b2bec3" stroke-width="3" />' for k in range(8)) + f"""</g>
      </g>
      <g id="c5-d" class="h">
        {T(440, 52, 38, "Por resultados", "b", fill=P)}
        {T(440, 96, 28, "indicadores de resultado e impacto", "m", fill="#636e72")}
        <g id="c5-dos">""" + "".join(f'<g id="c5-j{k}" class="h"><rect x="{60 + (k % 3) * 60}" y="{170 + (k // 3) * 90}" width="22" height="70" rx="5" fill="#dfe6e9" /><rect x="{64 + (k % 3) * 60}" y="{186 + (k // 3) * 90}" width="14" height="44" fill="#74b9ff" /></g>' for k in range(6)) + f"""
          {T(150, 400, 28, "dosis compradas", "b")}</g>
        <circle id="c5-esc" cx="620" cy="270" r="180" fill="#00b894" opacity="0.18" />
        """ + "".join(f'<g id="c5-pe{k}"><g transform="translate({500 + (k % 4) * 80} {230 + (k // 4) * 100}) scale(1.2)">{I_PERSONA}</g></g>' for k in range(8)) + f"""
        {T(620, 450, 28, "población protegida", "b", fill="#00b894")}
        <rect id="c5-foco" x="40" y="140" width="240" height="290" rx="20" fill="none" stroke="#d63031" stroke-width="7" />
      </g>"""
js = f"""
    slideIn("#c5-a", {L(57)});
    grow("#c5-b1", {W(57, 0.5)}, 0.7);
    grow("#c5-b2", {W(58, 0.05)}, 0.7);
    pop("#c5-inf", {W(58, 0.3)});
    wob("#c5-inf", {W(58, 0.35)}, {TT[58][1]}, 4, 0.5);
    tl.to("#c5-b2", {{ scaleX: 1.2, transformOrigin: "0% 50%", duration: 1.0, ease: "back.out(1.5)" }}, A({W(58, 0.5)}));
    tl.to("#c5-v2", {{ x: 60, duration: 1.0, ease: "back.out(1.5)" }}, A({W(58, 0.5)}));
    count("#c5-v2", 100, 120, {W(58, 0.5)}, 1.0);
    show("#c5-nota", {W(58, 0.72)});
    draw("#c5-notax", {W(58, 0.85)}, 0.4);
    slideOut("#c5-a", {L(59)});
    slideIn("#c5-b", {L(59)});
    bob("#c5-l1", {L(59)}, {W(60, 0.3)}, 6, 0.8);
    bob("#c5-l2", {W(59, 0.2)}, {W(60, 0.3)}, 6, 0.9);
    tl.to("#c5-l1", {{ x: 290, y: 50, scale: 0.5, opacity: 0, transformOrigin: C, duration: 0.6, ease: "power2.in" }}, A({W(60, 0.35)}));
    tl.to("#c5-l2", {{ x: 290, y: -30, scale: 0.5, opacity: 0, transformOrigin: C, duration: 0.6, ease: "power2.in" }}, A({W(60, 0.42)}));
    pulse("#c5-b rect:nth-of-type(1)", {W(60, 0.5)});
    flow("#c5-ar", {W(60, 0.5)}, {TT[60][1]}, 60);
    {"".join(f'pop("#c5-k{k}", {round(W(60, 0.62) + k * 0.4, 2)}); bob("#c5-k{k}", {round(W(60, 0.7) + k * 0.4, 2)}, {TT[60][1]}, 6, 0.7);' for k in range(4))}
    slideOut("#c5-b", {L(61)});
    slideIn("#c5-c", {L(61)});
    {"".join(f'tl.to("#c5-z{k}", {{ scaleY: 0, transformOrigin: "50% 100%", duration: 0.5, ease: "power2.in" }}, A({W(61, 0.35)}));' for k in range(3))}
    {"".join(f'pop("#c5-zc{k}", {round(W(61, 0.55) + k * 0.5, 2)}); tl.to("#c5-z{k}", {{ scaleY: 1, transformOrigin: "50% 100%", duration: 0.6, ease: "back.out(1.5)" }}, A({round(W(61, 0.6) + k * 0.5, 2)}));' for k in range(3))}
    pop("#c5-badge", {L(62)});
    count("#c5-anio", 1, 10, {W(62, 0.1)}, 3.0, (v) => "año " + Math.round(v));
    {"".join(f'tl.to("#c5-z{k}", {{ scaleY: 0.05, transformOrigin: "50% 100%", duration: 0.25, yoyo: true, repeat: 5, ease: "power1.inOut" }}, A({round(W(62, 0.15) + k * 0.1, 2)}));' for k in range(3))}
    {"".join(f'drop("#c5-pp{k}", {round(W(62, 0.6) + k * 0.2, 2)});' for k in range(8))}
    wob("#c5-pap", {W(62, 0.75)}, {TT[62][1]}, 2, 0.3);
    slideOut("#c5-c", {L(63)});
    slideIn("#c5-d", {L(63)});
    {"".join(f'pop("#c5-j{k}", {round(W(63, 0.3) + k * 0.25, 2)});' for k in range(6))}
    tl.set("#c5-esc", {{ scale: 0.1, transformOrigin: C }}, A({L(63)}));
    tl.to("#c5-esc", {{ scale: 1, duration: 2.6, ease: "power1.out" }}, A({W(64, 0.2)}));
    {"".join(f'tl.to("#c5-pe{k} path", {{ fill: "#00b894", duration: 0.3 }}, A({round(W(64, 0.25) + k * 0.25, 2)}));' for k in range(8))}
    tl.to("#c5-foco", {{ x: 400, width: 420, duration: 0.8, ease: "power3.inOut" }}, A({W(64, 0.3)}));
    tl.to("#c5-foco", {{ scale: 1.03, transformOrigin: C, duration: 0.4, yoyo: true, repeat: 5, ease: "sine.inOut" }}, A({W(64, 0.45)}));"""
chapter("c5", B[6], B[7], "Capítulo 5", "Sistemas presupuestarios", P, "#ffc2d1", L(56) + 4.0, [(L(58), TT[58][1]), (L(60), TT[60][1]), (L(62), TT[62][1]), (L(64), B[7] - 0.05)], [], svg, js)

# ================================================================ C6
P = "#138a8e"
svg = f"""
      <g id="c6-a" class="h">
        {T(440, 56, 36, "Ningún indicador explica todo solo", "b", fill=P)}
        """ + "".join(f'<g transform="translate({180 + k * 260} 270)"><path d="M-100,0 A100,100 0 0,1 100,0" fill="none" stroke="#e0f4f4" stroke-width="26" /><g id="c6-n{k}"><path d="M0,0 L0,-84" stroke="#2d3436" stroke-width="8" stroke-linecap="round" /></g><circle r="14" fill="#2d3436" /></g>' for k in range(3)) + f"""
        {T(440, 380, 30, "por eso se usan varios", "b", fill=P)}
      </g>
      <g id="c6-b" class="h">
        {T(440, 52, 36, "Una escuela", "b", fill=P)}
        """ + "".join(f'<g transform="translate({60 + k * 50} 200) scale(1.1)">{I_PERSONA}</g>' for k in range(3)) + f"""
        <g id="c6-t1" class="h">{box(30, 260, 200, 50, "insumo", P, s=28)}{T(130, 340, 28, "docentes", "b")}</g>
        {arrow("c6-a1", "M240,200 L320,200", P, 8)}
        <g transform="translate(400 200) scale(0.8)">{I_ESCUELA}</g>
        {arrow("c6-a2", "M480,200 L560,200", P, 8)}
        """ + "".join(f'<g id="c6-al{k}" class="h"><g transform="translate({600 + (k % 2) * 60} {170 + (k // 2) * 70})">{I_PERSONA}</g></g>' for k in range(4)) + f"""
        <g id="c6-t2" class="h">{box(330, 260, 200, 50, "producto", P, s=28)}{T(430, 340, 28, "alumnos atendidos", "b")}</g>
        <g id="c6-t3" class="h">{box(630, 260, 200, 50, "resultado", P, s=28)}{T(730, 340, 28, "tasa de egreso", "b")}</g>
        """ + "".join(f'<g id="c6-bi{k}" class="h"><path d="M{700 + k * 40},{140} l30,10 l-30,10 l-30,-10 Z" fill="#2d3436" /></g>' for k in range(3)) + f"""
        <g id="c6-cal" class="h"><path d="M430,380 l12,26 l28,3 l-21,19 l6,28 l-25,-14 l-25,14 l6,-28 l-21,-19 l28,-3 Z" fill="#fdcb6e" />{T(530, 440, 28, "calidad", "b")}</g>
        <circle id="c6-imp1" class="h" cx="730" cy="200" r="60" fill="none" stroke="{P}" stroke-width="5" />
        <circle id="c6-imp2" class="h" cx="730" cy="200" r="60" fill="none" stroke="{P}" stroke-width="5" />
        <g id="c6-impt" class="h">{T(730, 440, 28, "impacto", "b", fill=P)}</g>
      </g>"""
js = f"""
    slideIn("#c6-a", {L(66)});
    {"".join(f'tl.fromTo("#c6-n{k}", {{ rotation: {-60 + k * 30}, svgOrigin: "0 0" }}, {{ rotation: {50 - k * 20}, svgOrigin: "0 0", duration: {0.6 + k * 0.15}, ease: "sine.inOut", yoyo: true, repeat: 5 }}, A({L(66)}));' for k in range(3))}
    slideOut("#c6-a", {L(67)});
    slideIn("#c6-b", {L(67)});
    flow("#c6-a1", {L(67)}, {TT[69][1]}, 60);
    flow("#c6-a2", {L(67)}, {TT[69][1]}, 60);
    pop("#c6-t1", {W(68, 0.12)});
    {"".join(f'pop("#c6-al{k}", {round(W(68, 0.35) + k * 0.2, 2)});' for k in range(4))}
    pop("#c6-t2", {W(68, 0.42)});
    pop("#c6-t3", {W(68, 0.78)});
    {"".join(f'tl.set("#c6-bi{k}", {{ opacity: 1, y: 60 }}, A({round(W(68, 0.82) + k * 0.15, 2)})); tl.to("#c6-bi{k}", {{ y: -90, rotation: {(k - 1) * 40}, transformOrigin: C, duration: 0.9, ease: "power2.out" }}, A({round(W(68, 0.82) + k * 0.15, 2)})); tl.to("#c6-bi{k}", {{ opacity: 0, duration: 0.3 }}, A({round(W(68, 0.82) + k * 0.15 + 0.9, 2)}));' for k in range(3))}
    pop("#c6-cal", {W(69, 0.15)});
    wob("#c6-cal", {W(69, 0.3)}, {TT[69][1]}, 10, 0.4);
    {"".join(f'tl.set("#c6-imp{k + 1}", {{ opacity: 1, scale: 0.5, transformOrigin: C }}, A({round(W(69, 0.6) + k * 0.5, 2)})); tl.to("#c6-imp{k + 1}", {{ scale: 2.4, opacity: 0, duration: 1.2, ease: "power1.out" }}, A({round(W(69, 0.6) + k * 0.5, 2)}));' for k in range(2))}
    show("#c6-impt", {W(69, 0.6)});"""
chapter("c6", B[7], B[8], "Capítulo 6", "Indicadores de gestión", P, "#9fe6e8", L(65) + 2.6, [(L(67), B[8] - 0.05)], [], svg, js)

# ================================================================ CIERRE
P = "#5b4bd6"
svg = f"""
      <g id="c7-a" class="h">
        {T(440, 60, 30, "Un programa de vacunación informa", "m")}
        {T(440, 100, 30, "cuántas dosis aplicó...", "b")}
        <g id="c7-dos">""" + "".join(f'<g id="c7-j{k}" class="h"><rect x="{120 + k * 50}" y="150" width="22" height="70" rx="5" fill="#dfe6e9" /><rect x="{124 + k * 50}" y="166" width="14" height="44" fill="#74b9ff" /></g>' for k in range(6)) + f"""</g>
        <g id="c7-mort" class="h">{T(640, 175, 30, "mortalidad infantil", "b")}<g id="c7-q">{T(640, 235, 60, "?", "b", fill="#d63031")}</g></g>
        <g id="c7-p" class="h"><rect x="70" y="280" width="740" height="100" rx="50" fill="{P}" />{T(440, 345, 40, "¿Qué tipo de indicador falta?", "b", fill="#ffffff")}</g>
        <g id="c7-c" class="h">{T(440, 435, 32, "Respondé en los comentarios", "b", fill=P)}</g>
      </g>"""
extra = """
    <div class="pill-slot"><div id="c7-save" class="pill h"><svg width="30" height="38" viewBox="0 0 34 42"><path d="M3,3 H31 V39 L17,29 L3,39 Z" fill="#ffd166" /></svg>Guardá este video</div></div>"""
js = f"""
    slideIn("#c7-a", {L(71) - 0.1});
    {"".join(f'pop("#c7-j{k}", {round(W(71, 0.1) + k * 0.25, 2)});' for k in range(6))}
    bob("#c7-dos", {W(71, 0.4)}, {TT[72][1]}, 5, 0.8);
    show("#c7-mort", {W(71, 0.45)});
    wob("#c7-q", {W(71, 0.5)}, {TT[72][1]}, 12, 0.5);
    show("#c7-p", {W(71, 0.75)});
    pulse("#c7-p", {W(71, 0.95)});
    show("#c7-c", {L(72)});
    hide("#c7-pill", {L(72) + 0.6});
    show("#c7-save", {L(72) + 0.9});
    pulse("#c7-save", {L(72) + 2.0});"""
chapter("c7", B[8], B[9], "Repaso", "Pregunta de repaso", P, "#c3baff", L(70) + 1.9, [], [], svg, js, extra)

# ================================================================ INDEX
hosts = "".join(
    f"""
      <div id="{cid}" style="z-index: 2" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html"
        data-start="{t0}" data-duration="{dur}" data-track-index="2" data-track-kind="graphics"
        data-width="1080" data-height="1920"></div>"""
    for cid, t0, dur in chapters)
index = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #4b4e8c; }}
      #root {{ width: 100%; height: 100%; position: relative; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="estudiante" style="z-index: 1" data-composition-id="estudiante" data-composition-src="compositions/estudiante.html"
        data-start="0" data-duration="{TOTAL}" data-track-index="1" data-track-kind="graphics"
        data-width="1080" data-height="1920"></div>{hosts}
      <audio id="voz" class="clip" src="assets/voz.wav" data-start="0" data-track-index="3" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
(OUT / "index.html").write_text(index)
for c in chapters:
    print(c)
