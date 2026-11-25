"""Genera compositions/cN.html (un archivo por capítulo) y el index.html.

Cada capítulo trae: cartel de título grande sobre el pizarrón, píldora chica
arriba, ficha «EJEMPLO DEL APUNTE» y el contenido animado del pizarrón
(SVG de 880×470 colocado sobre el pizarrón que dibuja estudiante.html).
Los tiempos se escriben en segundos absolutos del vídeo (los de tiempos.json).
"""
from pathlib import Path

OUT = Path(__file__).parent / "proyecto"
TOTAL = 300.0

CSS = """
    #root { position: absolute; inset: 0; font-family: Nunito, sans-serif; }
    .h { opacity: 0; }
    .brd { position: absolute; left: 100px; top: 430px; width: 880px; height: 470px; }
    .brd svg { position: absolute; left: 0; top: 0; width: 880px; height: 470px; overflow: visible; }
    .brd text { font-family: Nunito, sans-serif; }
    .b { font-weight: 900; }
    .m { font-weight: 700; }
    .ttl { position: absolute; left: 100px; top: 430px; width: 880px; height: 470px; border-radius: 22px;
      display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px;
      color: #ffffff; text-align: center; }
    .ttl-n { font-size: 40px; font-weight: 700; letter-spacing: 0.06em; opacity: 0.9; }
    .ttl-t { font-size: 66px; font-weight: 900; line-height: 1.05; max-width: 760px; }
    .pill-slot { position: absolute; left: 0; right: 0; top: 300px; display: flex; justify-content: center; }
    .pill { display: flex; align-items: center; gap: 14px; padding: 12px 28px; border-radius: 999px;
      background: rgba(16, 18, 42, 0.82); color: #ffffff; font-size: 34px; font-weight: 900; max-width: 840px; }
    .pill-n { font-size: 30px; font-weight: 900; padding: 3px 14px; border-radius: 999px; color: #10122a; }
    .ej { position: absolute; left: 130px; top: 396px; padding: 8px 20px; border-radius: 12px;
      background: #ffd166; color: #2d2200; font-size: 28px; font-weight: 900; letter-spacing: 0.04em;
      box-shadow: 0 5px 0 rgba(0, 0, 0, 0.18); }
"""

JS_HELPERS = """
    const tl = gsap.timeline({ paused: true });
    const A = (t) => Math.max(0, +(t - T0).toFixed(3));
    const C = "50% 50%";
    function show(s, t, d) {
      tl.set(s, { scale: 0.85, transformOrigin: C }, A(t));
      tl.to(s, { opacity: 1, scale: 1, duration: d || 0.35, ease: "back.out(2)" }, A(t));
    }
    function fade(s, t, d) {
      tl.to(s, { opacity: 1, duration: d || 0.3, ease: "power1.out" }, A(t));
    }
    function hide(s, t) {
      tl.to(s, { opacity: 0, duration: 0.25, ease: "power2.in" }, A(t - 0.25));
    }
    function draw(s, t, d) {
      tl.to(s, { strokeDashoffset: 0, duration: d || 0.8, ease: "power1.inOut" }, A(t));
    }
    function pulse(s, t) {
      tl.to(s, { scale: 1.12, transformOrigin: C, duration: 0.18, yoyo: true, repeat: 1, ease: "sine.inOut" }, A(t));
    }
"""


def chapter(cid, t0, t1, num, title, accent, badge, title_end, ejemplos, svg, js, pill_extra=""):
    dur = round(t1 - t0, 3)
    title_html = ""
    title_js = ""
    if title_end:
        n_html = f'<div class="ttl-n">{num}</div>' if num else ""
        title_html = f"""
    <div id="{cid}-ttl" class="ttl" style="background: {accent}">
      {n_html}<div class="ttl-t">{title}</div>
    </div>"""
        title_js = f"""
    tl.fromTo("#{cid}-ttl", {{ opacity: 1, scale: 0.94, transformOrigin: C }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, 0);
    hide("#{cid}-ttl", {title_end});
    show("#{cid}-pill", {title_end - 0.1});
    hide("#{cid}-pill", {t1 - 0.05});"""
    ej_js = "".join(f'\n    show("#{cid}-ej", {a});\n    hide("#{cid}-ej", {b});' for a, b in ejemplos)
    pill_badge = f'<span class="pill-n" style="background: {badge}">Cap. {num[-1]}/6</span>' if num.startswith("Capítulo") else ""
    html = f"""<template>
  <style>{CSS}
    #{cid}-pill .pill-n {{ background: {badge}; }}
    .acc {{ fill: {accent}; }}
    .accs {{ stroke: {accent}; }}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
    <div class="brd"><svg viewBox="0 0 880 470" xmlns="http://www.w3.org/2000/svg">{svg}
    </svg></div>{title_html}
    <div class="pill-slot"><div id="{cid}-pill" class="pill h">{pill_badge}{title}</div></div>{pill_extra}
    <div id="{cid}-ej" class="ej h">EJEMPLO DEL APUNTE</div>
  </div>
  <script>
    const T0 = {t0};{JS_HELPERS}{title_js}{ej_js}
{js}
    tl.set({{}}, {{}}, {dur});
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""
    (OUT / "compositions" / f"{cid}.html").write_text(html)
    return cid, t0, dur


def T(x, y, s, txt, cls="m", anchor="middle", fill="#2d3436", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{s}" class="{cls}" text-anchor="{anchor}" fill="{fill}" {extra}>{txt}</text>'


chapters = []

# ---------------------------------------------------------------- INTRO
svg = f"""
      <g id="c0-a">
        {T(440, 200, 62, "¿Qué es la", "b")}
        {T(440, 290, 74, "hacienda pública?", "b", fill="#5b4bd6")}
        <g fill="#fdcb6e" stroke="#e1a940" stroke-width="5">
          <circle cx="120" cy="360" r="34" /><circle cx="170" cy="390" r="34" /><circle cx="760" cy="370" r="34" />
        </g>
      </g>
      <g id="c0-b" class="h">
        <rect x="330" y="70" width="220" height="58" rx="29" fill="#5b4bd6" />
        {T(440, 110, 34, "UNIDAD 1", "b", fill="#ffffff")}
        {T(440, 215, 60, "Hacienda pública", "b")}
        {T(440, 285, 46, "y administración del Estado", "b", fill="#5b4bd6")}
        {T(440, 360, 30, "Administración y Contabilidad Pública", "m", fill="#636e72")}
      </g>"""
js = """
    hide("#c0-a", 1.77);
    show("#c0-b", 1.77);
    hide("#c0-b", 6.67);"""
chapters.append(chapter("c0", 0, 6.67, "", "Unidad 1", "#5b4bd6", "#c3baff", None, [], svg, js))

# ---------------------------------------------------------------- C1
ACC1 = "#6c5ce7"
tiles = [
    ("Erogativa", "gasta para", "cumplir sus fines", 27.6,
     '<rect x="-30" y="-18" width="60" height="36" rx="6" fill="#00b894"/><circle r="10" fill="#ffffff"/>'),
    ("Coactiva", "exige tributos", "por ley", 30.27,
     '<rect x="-24" y="4" width="48" height="16" rx="4" fill="#d63031"/><rect x="-7" y="-26" width="14" height="32" fill="#636e72"/><circle cy="-30" r="12" fill="#2d3436"/>'),
    ("Perdurable", "sigue aunque", "cambie el gobierno", 34.01,
     '<circle r="26" fill="#ffffff" stroke="#2d3436" stroke-width="6"/><path d="M0,-14 L0,0 L12,8" stroke="#2d3436" stroke-width="5" fill="none" stroke-linecap="round"/>'),
    ("Dependiente", "sirve a los", "tres poderes", 37.29,
     '<path d="M-30,-14 L0,-30 L30,-14 Z" fill="#636e72"/><rect x="-24" y="-10" width="10" height="32" fill="#636e72"/><rect x="-5" y="-10" width="10" height="32" fill="#636e72"/><rect x="14" y="-10" width="10" height="32" fill="#636e72"/>'),
    ("Formal", "todo queda", "por escrito", 41.09,
     '<rect x="-20" y="-28" width="40" height="54" rx="5" fill="#ffffff" stroke="#2d3436" stroke-width="5"/><path d="M-10,-12 L10,-12 M-10,0 L10,0 M-10,12 L4,12" stroke="#2d3436" stroke-width="4"/>'),
    ("Divisa", "se divide en partes", "para cada necesidad", 44.63,
     '<circle r="26" fill="#fdcb6e"/><path d="M0,0 L0,-26 A26,26 0 0,1 22.5,13 Z" fill="#e17055"/><path d="M0,0 L22.5,13 A26,26 0 0,1 -22.5,13 Z" fill="#74b9ff"/>'),
]
tile_svg = ""
tile_js = ""
for i, (name, d1, d2, t, icon) in enumerate(tiles):
    x = 20 + (i % 3) * 283
    y = 78 + (i // 3) * 196
    tile_svg += f"""
        <g id="c1-t{i}" class="h">
          <rect x="{x}" y="{y}" width="268" height="184" rx="18" fill="#efeafe" />
          <g transform="translate({x + 134} {y + 40})">{icon}</g>
          {T(x + 134, y + 104, 32, name, "b", fill=ACC1)}
          {T(x + 134, y + 140, 28, d1)}
          {T(x + 134, y + 172, 28, d2)}
        </g>"""
    tile_js += f'\n    show("#c1-t{i}", {t});'
svg = f"""
      <g id="c1-a" class="h">
        <rect x="40" y="40" width="340" height="230" rx="20" fill="#efeafe" />
        <path d="M150,120 L210,90 L270,120 Z" fill="{ACC1}" /><rect x="160" y="124" width="100" height="70" fill="{ACC1}" />
        <rect x="176" y="136" width="14" height="58" fill="#ffffff" /><rect x="203" y="136" width="14" height="58" fill="#ffffff" /><rect x="230" y="136" width="14" height="58" fill="#ffffff" />
        {T(210, 245, 36, "Estado", "b")}
        <rect x="500" y="40" width="340" height="230" rx="20" fill="#f1f2f6" />
        <rect x="610" y="120" width="120" height="74" fill="#636e72" /><path d="M600,120 L740,120 L728,96 L612,96 Z" fill="#e17055" />
        <rect x="652" y="146" width="36" height="48" fill="#ffffff" />
        {T(670, 245, 36, "Empresa privada", "b")}
        <circle cx="440" cy="155" r="40" fill="#2d3436" />
        {T(440, 168, 34, "vs", "b", fill="#ffffff")}
        <g id="c1-a2" class="h">
          <rect x="150" y="310" width="580" height="80" rx="40" fill="#4a3bbf" />
          {T(440, 362, 38, "La diferencia: el FIN", "b", fill="#ffffff")}
        </g>
      </g>
      <g id="c1-b" class="h">
        {T(440, 80, 48, "Hacienda pública", "b", fill=ACC1)}
        {T(440, 135, 32, "conjunto de actividades económicas del Estado")}
        <g id="c1-b1" class="h">
          <circle cx="150" cy="232" r="32" fill="#00b894" />
          <path d="M134,232 L146,244 L168,220" stroke="#ffffff" stroke-width="8" fill="none" stroke-linecap="round" />
          {T(200, 244, 34, "satisfacer necesidades colectivas", "b", "start")}
          <circle cx="150" cy="330" r="32" fill="#d63031" />
          <path d="M138,318 L162,342 M162,318 L138,342" stroke="#ffffff" stroke-width="8" stroke-linecap="round" />
          {T(200, 342, 34, "ganancias para repartir", "m", "start", "#636e72")}
          <path id="c1-strike" d="M196,331 L560,331" stroke="#d63031" stroke-width="6" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" />
        </g>
      </g>
      <g id="c1-c" class="h">
        {T(440, 50, 36, "6 características", "b")}{tile_svg}
      </g>
      <g id="c1-d" class="h">
        <g transform="translate(140 130)">
          <rect x="-50" y="-60" width="100" height="120" rx="8" fill="#ffffff" stroke="#2d3436" stroke-width="5" />
          <path d="M-30,-30 L30,-30 M-30,-8 L30,-8 M-30,14 L14,14" stroke="#b2bec3" stroke-width="6" />
          <path d="M-50,60 L-36,48 L-22,60 L-8,48 L6,60 L20,48 L34,60 L50,48" fill="none" stroke="#2d3436" stroke-width="5" />
        </g>
        {T(140, 250, 30, "Ingresos Brutos", "b")}
        {T(140, 285, 28, "(cobra)", "m", fill="#636e72")}
        <g transform="translate(440 130)">
          <path d="M-80,-24 L0,-64 L80,-24 Z" fill="{ACC1}" /><rect x="-70" y="-20" width="140" height="84" fill="{ACC1}" />
          <rect x="-50" y="-6" width="18" height="70" fill="#ffffff" /><rect x="-9" y="-6" width="18" height="70" fill="#ffffff" /><rect x="32" y="-6" width="18" height="70" fill="#ffffff" />
        </g>
        {T(440, 250, 30, "Provincia", "b")}
        <g transform="translate(740 130)">
          <rect x="-70" y="-62" width="140" height="90" rx="6" fill="#2d6a4f" stroke="#a86e45" stroke-width="8" />
          <path d="M-46,-36 L10,-36 M-46,-14 L-6,-14" stroke="#ffffff" stroke-width="5" />
          <circle cx="44" cy="10" r="22" fill="#f5c9a0" /><path d="M24,70 Q44,30 64,70 Z" fill="#ff7675" />
        </g>
        {T(740, 250, 30, "Sueldos docentes", "b")}
        {T(740, 285, 28, "(paga)", "m", fill="#636e72")}
        <path d="M215,130 L355,130" stroke="#b2bec3" stroke-width="6" stroke-dasharray="12 10" />
        <path d="M525,130 L655,130" stroke="#b2bec3" stroke-width="6" stroke-dasharray="12 10" />
        <g fill="#fdcb6e" stroke="#e1a940" stroke-width="4">
          <circle id="c1-k1" class="h" cx="215" cy="130" r="18" /><circle id="c1-k2" class="h" cx="215" cy="130" r="18" /><circle id="c1-k3" class="h" cx="215" cy="130" r="18" />
          <circle id="c1-k4" class="h" cx="525" cy="130" r="18" /><circle id="c1-k5" class="h" cx="525" cy="130" r="18" /><circle id="c1-k6" class="h" cx="525" cy="130" r="18" />
        </g>
        <g id="c1-d2" class="h">
          <rect x="70" y="330" width="740" height="84" rx="42" fill="{ACC1}" />
          {T(440, 384, 34, "recurso coactivo → necesidad colectiva", "b", fill="#ffffff")}
        </g>
      </g>"""
js = f"""
    show("#c1-a", 9.72);
    show("#c1-a2", 15.84);
    hide("#c1-a", 17.6);
    show("#c1-b", 17.6);
    show("#c1-b1", 21.01);
    draw("#c1-strike", 23.6, 0.5);
    hide("#c1-b", 25.6);
    fade("#c1-c", 25.66);{tile_js}
    hide("#c1-c", 50.5);
    show("#c1-d", 50.57);
    ["#c1-k1", "#c1-k2", "#c1-k3"].forEach((k, i) => {{
      tl.to(k, {{ opacity: 1, duration: 0.1 }}, A(51.6 + i * 0.3));
      tl.to(k, {{ x: 140, duration: 0.55, ease: "power1.inOut" }}, A(51.6 + i * 0.3));
      tl.to(k, {{ opacity: 0, duration: 0.1 }}, A(52.1 + i * 0.3));
    }});
    ["#c1-k4", "#c1-k5", "#c1-k6"].forEach((k, i) => {{
      tl.to(k, {{ opacity: 1, duration: 0.1 }}, A(53.4 + i * 0.3));
      tl.to(k, {{ x: 130, duration: 0.55, ease: "power1.inOut" }}, A(53.4 + i * 0.3));
      tl.to(k, {{ opacity: 0, duration: 0.1 }}, A(53.9 + i * 0.3));
    }});
    show("#c1-d2", 55.54);
    pulse("#c1-d2", 59.4);"""
chapters.append(chapter("c1", 6.67, 61.55, "Capítulo 1", "Concepto y características", ACC1, "#c3baff", 9.62, [(50.57, 61.3)], svg, js))

# ---------------------------------------------------------------- C2
ACC2 = "#1f9d6f"
svg = f"""
      <g id="c2-a" class="h">
        {T(440, 62, 42, "1 · Regulación", "b", fill=ACC2)}
        {T(440, 112, 30, "fija reglas para la economía")}
        <g id="c2-a2" class="h">
          <rect x="150" y="200" width="300" height="200" fill="#dfe6e9" />
          <path d="M130,200 L470,200 L450,150 L150,150 Z" fill="#e17055" />
          <path d="M190,150 L178,200 M250,150 L245,200 M310,150 L312,200 M370,150 L379,200 M430,150 L446,200" stroke="#ffffff" stroke-width="12" />
          <rect x="250" y="270" width="90" height="130" fill="#a86e45" />
          {T(300, 248, 28, "COMERCIO", "b")}
          <g id="c2-perm">
            <rect x="520" y="170" width="220" height="240" rx="10" fill="#ffffff" stroke="#2d3436" stroke-width="5" />
            {T(630, 222, 32, "PERMISO", "b")}
            <path d="M556,260 L704,260 M556,292 L704,292 M556,324 L660,324" stroke="#b2bec3" stroke-width="6" />
          </g>
          <g id="c2-sello" class="h" transform="rotate(-12 630 370)">
            <rect x="535" y="335" width="190" height="64" rx="10" fill="none" stroke="#d63031" stroke-width="7" />
            {T(630, 380, 32, "APROBADO", "b", fill="#d63031")}
          </g>
        </g>
      </g>
      <g id="c2-b" class="h">
        {T(440, 62, 40, "2 · Producción de bienes y servicios", "b", fill=ACC2)}
        <g id="c2-b1" class="h">
          <path d="M70,220 L150,170 L230,220 Z" fill="#e17055" /><rect x="85" y="220" width="130" height="110" fill="#fdcb6e" />
          <rect x="130" y="270" width="40" height="60" fill="#a86e45" /><rect x="100" y="236" width="24" height="24" fill="#ffffff" /><rect x="176" y="236" width="24" height="24" fill="#ffffff" />
          {T(150, 385, 32, "Escuelas", "b")}
        </g>
        <g id="c2-b2" class="h">
          <rect x="370" y="180" width="140" height="150" fill="#ffffff" stroke="#2d3436" stroke-width="5" />
          <rect x="425" y="200" width="30" height="80" fill="#d63031" /><rect x="400" y="225" width="80" height="30" fill="#d63031" />
          <rect x="420" y="290" width="40" height="40" fill="#74b9ff" />
          {T(440, 385, 32, "Hospitales", "b")}
        </g>
        <g id="c2-b3" class="h">
          <path d="M730,170 Q690,240 690,270 A40,40 0 0,0 770,270 Q770,240 730,170 Z" fill="#0984e3" />
          <circle cx="716" cy="270" r="10" fill="#ffffff" opacity="0.7" />
          {T(730, 385, 32, "Agua potable", "b")}
        </g>
      </g>
      <g id="c2-c" class="h">
        {T(440, 62, 42, "3 · Inversión física", "b", fill=ACC2)}
        {T(440, 112, 30, "obras que duran muchos años")}
        <path id="c2-ruta" d="M40,380 C260,380 300,240 520,240 S760,200 840,200" fill="none" stroke="#636e72" stroke-width="46" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" />
        <path id="c2-ruta2" d="M40,380 C260,380 300,240 520,240 S760,200 840,200" fill="none" stroke="#ffffff" stroke-width="5" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" />
        <g id="c2-esc" class="h">
          <path d="M120,250 L200,200 L280,250 Z" fill="#e17055" /><rect x="135" y="250" width="130" height="90" fill="#fdcb6e" />
          <rect x="180" y="290" width="40" height="50" fill="#a86e45" />
          {T(200, 225, 28, "", "b")}
        </g>
        {T(620, 330, 28, "una ruta · un edificio escolar", "m", fill="#636e72")}
      </g>
      <g id="c2-d" class="h">
        {T(440, 62, 42, "4 · Financiamiento", "b", fill=ACC2)}
        {T(440, 112, 30, "¿de dónde sale el dinero?")}
        <g id="c2-d1" class="h">
          <rect x="20" y="160" width="250" height="150" rx="18" fill="#e3f7ef" />
          {T(145, 222, 34, "Tributos", "b", fill=ACC2)}
          {T(145, 270, 28, "primero")}
        </g>
        <g id="c2-d2" class="h">
          <path d="M282,235 L310,235" stroke="#2d3436" stroke-width="6" />
          <rect x="315" y="160" width="250" height="150" rx="18" fill="#e3f7ef" />
          {T(440, 222, 34, "Crédito público", "b", fill=ACC2)}
          {T(440, 270, 28, "si no alcanzan")}
        </g>
        <g id="c2-d3" class="h">
          <path d="M577,235 L605,235" stroke="#2d3436" stroke-width="6" />
          <rect x="610" y="160" width="250" height="150" rx="18" fill="#fde8e4" />
          {T(735, 214, 32, "Emisión", "b", fill="#c0392b")}
          {T(735, 250, 32, "de moneda", "b", fill="#c0392b")}
          {T(735, 290, 28, "casos extremos")}
        </g>
        <g id="c2-d4" class="h">
          <rect x="590" y="330" width="290" height="64" rx="32" fill="#d63031" />
          {T(735, 373, 30, "costo: inflación ↑", "b", fill="#ffffff")}
        </g>
      </g>"""
js = """
    show("#c2-a", 65.68);
    show("#c2-a2", 68.8);
    tl.set("#c2-sello", { scale: 1.8, transformOrigin: C }, A(69.6));
    tl.to("#c2-sello", { opacity: 1, scale: 1, duration: 0.15, ease: "power4.in" }, A(69.6));
    pulse("#c2-perm", 69.75);
    hide("#c2-a", 72.05);
    fade("#c2-b", 72.11);
    show("#c2-b1", 74.1);
    show("#c2-b2", 74.8);
    show("#c2-b3", 75.5);
    hide("#c2-b", 76.22);
    fade("#c2-c", 76.27);
    draw("#c2-ruta", 76.9, 1.4);
    draw("#c2-ruta2", 77.1, 1.4);
    show("#c2-esc", 79.0);
    hide("#c2-c", 81.43);
    fade("#c2-d", 81.48);
    show("#c2-d1", 84.1);
    show("#c2-d2", 85.9);
    show("#c2-d3", 87.79);
    show("#c2-d4", 89.7);
    pulse("#c2-d4", 90.6);"""
chapters.append(chapter("c2", 61.55, 91.86, "Capítulo 2", "Acciones de la hacienda pública", ACC2, "#9ff0cf", 65.55, [(68.8, 72.0)], svg, js))

# ---------------------------------------------------------------- C3
ACC3 = "#2f78c4"
svg = f"""
      <g id="c3-l" class="h">
        <g transform="translate(215 100)">
          <rect x="-90" y="10" width="180" height="70" fill="#dfe6e9" stroke="#2d3436" stroke-width="5" />
          <path d="M-50,10 A50,50 0 0,1 50,10 Z" fill="{ACC3}" /><rect x="-4" y="-62" width="8" height="24" fill="#2d3436" />
          <rect x="-70" y="24" width="16" height="56" fill="#b2bec3" /><rect x="-30" y="24" width="16" height="56" fill="#b2bec3" /><rect x="14" y="24" width="16" height="56" fill="#b2bec3" /><rect x="54" y="24" width="16" height="56" fill="#b2bec3" />
        </g>
        {T(215, 225, 34, "Poder Legislativo", "b")}
        {T(215, 262, 28, "órgano volitivo · decide", "b", fill=ACC3)}
      </g>
      <g id="c3-l2" class="h">
        {T(215, 312, 28, "sanciona leyes")}
        {T(215, 346, 28, "aprueba el presupuesto")}
        {T(215, 380, 28, "y la cuenta de inversión")}
      </g>
      <g id="c3-art" class="h">
        <rect x="15" y="398" width="400" height="54" rx="27" fill="{ACC3}" />
        {T(215, 435, 30, "Art. 110 · Const. de Catamarca", "b", fill="#ffffff")}
      </g>
      <g id="c3-r" class="h">
        <g transform="translate(665 100)">
          <path d="M-100,0 L0,-50 L100,0 Z" fill="#636e72" /><rect x="-90" y="0" width="180" height="80" fill="#dfe6e9" stroke="#2d3436" stroke-width="5" />
          <rect x="-70" y="12" width="20" height="68" fill="#b2bec3" /><rect x="-30" y="12" width="20" height="68" fill="#b2bec3" /><rect x="10" y="12" width="20" height="68" fill="#b2bec3" /><rect x="50" y="12" width="20" height="68" fill="#b2bec3" />
        </g>
        {T(665, 225, 34, "Poder Ejecutivo", "b")}
        {T(665, 262, 28, "órgano directivo · ejecuta", "b", fill=ACC3)}
      </g>
      <g id="c3-r2" class="h">
        {T(665, 312, 28, "administra · cobra · paga")}
        {T(665, 346, 28, "propone el presupuesto")}
      </g>
      <g id="c3-ley" class="h">
        <rect x="140" y="300" width="150" height="110" rx="8" fill="#ffffff" stroke="#2d3436" stroke-width="5" />
        {T(215, 340, 28, "LEY DE", "b")}
        {T(215, 375, 28, "PRESUPUESTO", "b")}
      </g>
      <g id="c3-ok" class="h">
        <circle cx="300" cy="300" r="26" fill="#00b894" />
        <path d="M288,300 L298,310 L314,290" stroke="#ffffff" stroke-width="7" fill="none" stroke-linecap="round" />
      </g>
      <g id="c3-cp" class="h">
        <rect x="540" y="300" width="250" height="52" rx="26" fill="#00b894" />
        {T(665, 336, 28, "cobra los recursos", "b", fill="#ffffff")}
        <rect x="540" y="364" width="250" height="52" rx="26" fill="#e17055" />
        {T(665, 400, 28, "paga los gastos", "b", fill="#ffffff")}
      </g>"""
js = """
    show("#c3-l", 94.74);
    show("#c3-l2", 100.31);
    show("#c3-art", 104.11);
    show("#c3-r", 107.8);
    show("#c3-r2", 111.81);
    hide("#c3-l2", 115.1);
    hide("#c3-r2", 115.1);
    hide("#c3-art", 115.1);
    show("#c3-ley", 115.2);
    show("#c3-ok", 116.1);
    tl.to("#c3-ley", { x: 450, duration: 0.9, ease: "power2.inOut" }, A(117.4));
    tl.to("#c3-ley", { y: -60, duration: 0.45, ease: "sine.out", yoyo: true, repeat: 1 }, A(117.4));
    hide("#c3-ley", 119.0);
    show("#c3-cp", 119.2);"""
chapters.append(chapter("c3", 91.86, 122.45, "Capítulo 3", "Órganos del Estado", ACC3, "#a8d1ff", 94.6, [(115.1, 122.3)], svg, js))

# ---------------------------------------------------------------- C4
ACC4 = "#d9761e"
tipos = [
    ("Liberal o gendarme", "interviene lo mínimo:", "orden y propiedad", 125.33,
     '<path d="M-26,-22 L0,-32 L26,-22 L26,4 Q26,26 0,34 Q-26,26 -26,4 Z" fill="#2d3436"/>'),
    ("Subsidiario", "solo si el particular", "no puede", 131.2,
     '<circle r="30" fill="#636e72"/><text y="11" font-size="32" text-anchor="middle" fill="#ffffff" class="b">2°</text>'),
    ("De bienestar", "garantiza derechos", "sociales", 134.8,
     '<path d="M0,26 L-28,-2 A16,16 0 0,1 0,-22 A16,16 0 0,1 28,-2 Z" fill="#e84393"/>'),
    ("Socialista", "planifica y controla", "la producción", 139.82,
     '<circle r="22" fill="none" stroke="#d63031" stroke-width="12" stroke-dasharray="10 7"/><circle r="9" fill="#d63031"/>'),
]
tsvg = ""
tjs = ""
for i, (n, d1, d2, t, ic) in enumerate(tipos):
    x = 15 + (i % 2) * 430
    y = 20 + (i // 2) * 220
    tsvg += f"""
        <g id="c4-t{i}" class="h">
          <rect x="{x}" y="{y}" width="420" height="205" rx="18" fill="#fff1e3" />
          <g transform="translate({x + 58} {y + 62})">{ic}</g>
          {T(x + 105, y + 74, 32, n, "b", "start", ACC4)}
          {T(x + 30, y + 135, 30, d1, "m", "start")}
          {T(x + 30, y + 175, 30, d2, "m", "start")}
        </g>"""
    tjs += f'\n    show("#c4-t{i}", {t});'
sel = ["Liberal", "Subsidiario", "Bienestar", "Socialista"]
sel_svg = "".join(T(110 + i * 220, 58, 28, s, "b", fill="#636e72") for i, s in enumerate(sel))
svg = f"""
      <g id="c4-a">{tsvg}
      </g>
      <g id="c4-b" class="h">
        <rect id="c4-hl" x="15" y="20" width="190" height="56" rx="28" fill="{ACC4}" opacity="0.25" />
        {sel_svg}
        <g id="c4-r0" class="h">{T(440, 125, 32, "No interviene", "b", fill=ACC4)}</g>
        <g id="c4-r1" class="h">{T(440, 125, 30, "Interviene solo si ningún privado la construye", "b", fill=ACC4)}</g>
        <g id="c4-r2" class="h">{T(440, 125, 30, "La construye y la financia como derecho social", "b", fill=ACC4)}</g>
        <g id="c4-r3" class="h">{T(440, 125, 32, "Planifica toda la educación", "b", fill=ACC4)}</g>
        <path d="M20,400 L860,400" stroke="#2d3436" stroke-width="6" />
        <g fill="#74b9ff">
          <path d="M40,330 L90,290 L140,330 Z" fill="#e17055"/><rect x="50" y="330" width="80" height="70" />
          <path d="M150,340 L195,305 L240,340 Z" fill="#e17055"/><rect x="160" y="340" width="70" height="60" />
          <path d="M660,330 L710,290 L760,330 Z" fill="#e17055"/><rect x="670" y="330" width="80" height="70" />
          <path d="M770,340 L815,305 L860,340 Z" fill="#e17055"/><rect x="780" y="340" width="70" height="60" />
        </g>
        <g id="c4-lote">
          <rect x="300" y="380" width="280" height="20" fill="#c8a27a" />
          <rect x="436" y="300" width="8" height="80" fill="#a86e45" />
          <rect x="350" y="250" width="180" height="60" rx="8" fill="#ffffff" stroke="#2d3436" stroke-width="4" />
          {T(440, 290, 28, "falta escuela", "b")}
        </g>
        <g id="c4-priv" class="h">
          <circle cx="620" cy="230" r="34" fill="#ffffff" stroke="#2d3436" stroke-width="4" />
          {T(620, 244, 36, "?", "b")}
          {T(620, 190, 28, "¿un privado?", "m", fill="#636e72")}
        </g>
        <g id="c4-esc" class="h">
          <path d="M320,260 L440,190 L560,260 Z" fill="#e17055" /><rect x="335" y="260" width="210" height="140" fill="#fdcb6e" />
          <rect x="415" y="320" width="50" height="80" fill="#a86e45" /><rect x="355" y="280" width="40" height="34" fill="#ffffff" /><rect x="485" y="280" width="40" height="34" fill="#ffffff" />
        </g>
        <g id="c4-plan" class="h">
          <rect x="20" y="160" width="840" height="240" fill="#0984e3" opacity="0.16" />
          <path d="M20,220 L860,220 M20,280 L860,280 M20,340 L860,340 M230,160 L230,400 M440,160 L440,400 M650,160 L650,400" stroke="#0984e3" stroke-width="3" stroke-dasharray="10 8" />
        </g>
      </g>"""
js = f"""{tjs}
    hide("#c4-a", 142.95);
    fade("#c4-b", 143.02);
    show("#c4-r0", 146.18);
    hide("#c4-r0", 148.3);
    tl.to("#c4-hl", {{ x: 220, duration: 0.35, ease: "power2.inOut" }}, A(148.35));
    show("#c4-r1", 148.35);
    show("#c4-priv", 148.6);
    hide("#c4-r1", 151.9);
    hide("#c4-priv", 151.9);
    tl.to("#c4-hl", {{ x: 440, duration: 0.35, ease: "power2.inOut" }}, A(151.94));
    show("#c4-r2", 151.94);
    hide("#c4-lote", 152.2);
    tl.set("#c4-esc", {{ scaleY: 0, transformOrigin: "50% 100%" }}, A(152.2));
    tl.to("#c4-esc", {{ opacity: 1, scaleY: 1, duration: 1.1, ease: "power2.out" }}, A(152.2));
    hide("#c4-r2", 155.8);
    tl.to("#c4-hl", {{ x: 660, duration: 0.35, ease: "power2.inOut" }}, A(155.82));
    show("#c4-r3", 155.82);
    fade("#c4-plan", 156.0, 0.5);"""
chapters.append(chapter("c4", 122.45, 158.81, "Capítulo 4", "Tipos de Estado", ACC4, "#ffd3a8", 125.2, [(143.02, 158.6)], svg, js))

# ---------------------------------------------------------------- C5
ACC5 = "#c2405f"
def box(x, y, w, h, txt, fill="#fde4ea", tc="#2d3436", s=28, idv=""):
    i = f' id="{idv}"' if idv else ""
    return f'<g{i}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" />{T(x + w / 2, y + h / 2 + s * 0.35, s, txt, "b", fill=tc)}</g>'
svg = f"""
      <g id="c5-a" class="h">
        {T(440, 70, 44, "Administración pública", "b", fill=ACC5)}
        {T(440, 125, 32, "organismos que ejecutan")}
        {T(440, 165, 32, "las decisiones del Estado")}
        <g id="c5-a2" class="h">
          {T(440, 245, 38, "Contabilidad pública", "b", fill=ACC5)}
          {T(440, 292, 30, "registra y expone sus operaciones para:")}
        </g>
        <g id="c5-a3" class="h">{box(80, 320, 220, 60, "decidir", ACC5, "#ffffff", 30)}</g>
        <g id="c5-a4" class="h">{box(330, 320, 220, 60, "informar", ACC5, "#ffffff", 30)}</g>
        <g id="c5-a5" class="h">{box(580, 320, 220, 60, "controlar", ACC5, "#ffffff", 30)}</g>
      </g>
      <g id="c5-q" class="h">{T(440, 230, 48, "¿Cómo se organiza?", "b", fill=ACC5)}{T(440, 290, 34, "Hay tres formas", "m")}</g>
      <g id="c5-cen" class="h">
        {T(440, 52, 40, "Centralización", "b", fill=ACC5)}
        {box(300, 90, 280, 70, "Poder central", ACC5, "#ffffff", 32)}
        <g stroke="#2d3436" stroke-width="5">
          <path d="M120,290 L400,165 M280,290 L420,165 M440,290 L440,165 M600,290 L460,165 M760,290 L480,165" />
        </g>
        {box(60, 290, 120, 60, "")}{box(220, 290, 120, 60, "")}{box(380, 290, 120, 60, "")}{box(540, 290, 120, 60, "")}{box(700, 290, 120, 60, "")}
        {T(440, 410, 32, "una sola cabeza decide", "b")}
      </g>
      <g id="c5-des" class="h">
        {T(440, 52, 40, "Desconcentración", "b", fill=ACC5)}
        <rect x="30" y="78" width="820" height="300" rx="26" fill="none" stroke="{ACC5}" stroke-width="6" stroke-dasharray="18 12" />
        {T(70, 116, 28, "Ministerio", "b", "start", ACC5)}
        {box(310, 96, 260, 64, "Ministro", ACC5, "#ffffff", 30)}
        <path d="M440,160 L440,200 M160,200 L720,200 M160,200 L160,240 M440,200 L440,240 M720,200 L720,240" stroke="#2d3436" stroke-width="5" fill="none" />
        {box(60, 240, 200, 110, "")}{box(340, 240, 200, 110, "")}{box(620, 240, 200, 110, "")}
        {T(160, 290, 28, "Oficina", "b")}{T(160, 324, 28, "del interior", "m")}
        {T(440, 290, 28, "Oficina", "b")}{T(440, 324, 28, "del interior", "m")}
        {T(720, 290, 28, "Oficina", "b")}{T(720, 324, 28, "del interior", "m")}
        <g id="c5-des2" class="h">{T(440, 420, 28, "misma jerarquía · sin personalidad jurídica propia", "b", fill=ACC5)}</g>
        <g id="c5-des3" class="h">
          <circle cx="240" cy="250" r="22" fill="#00b894" /><circle cx="520" cy="250" r="22" fill="#00b894" /><circle cx="800" cy="250" r="22" fill="#00b894" />
          <path d="M230,250 L238,258 L252,242 M510,250 L518,258 L532,242 M790,250 L798,258 L812,242" stroke="#ffffff" stroke-width="5" fill="none" stroke-linecap="round" />
        </g>
      </g>
      <g id="c5-dsc" class="h">
        {T(440, 52, 40, "Descentralización", "b", fill=ACC5)}
        {box(30, 150, 300, 100, "", ACC5)}{T(180, 192, 30, "Administración", "b", fill="#ffffff")}{T(180, 230, 30, "central", "b", fill="#ffffff")}
        <rect x="550" y="120" width="300" height="160" rx="18" fill="#ffffff" stroke="{ACC5}" stroke-width="6" />
        <g id="c5-ente">{T(700, 210, 32, "Ente separado", "b")}</g>
        <g id="c5-ipv" class="h">{T(700, 195, 40, "IPV · OSEP", "b", fill=ACC5)}{T(700, 240, 28, "patrimonio propio")}</g>
        <path id="c5-h1" d="M330,200 L440,200" stroke="#2d3436" stroke-width="7" />
        <path id="c5-h2" d="M440,200 L550,200" stroke="#2d3436" stroke-width="7" />
        <g id="c5-ley" class="h">{T(700, 320, 28, "creado por ley", "b", fill=ACC5)}</g>
        <g id="c5-ctrl" class="h">
          <path d="M330,250 Q440,330 550,250" fill="none" stroke="#636e72" stroke-width="5" stroke-dasharray="12 10" />
          <ellipse cx="440" cy="292" rx="34" ry="20" fill="#ffffff" stroke="#2d3436" stroke-width="5" /><circle cx="440" cy="292" r="9" fill="#2d3436" />
          {T(440, 360, 30, "solo lo controla", "b")}
        </g>
      </g>
      <g id="c5-aut" class="h">
        <rect x="20" y="40" width="405" height="340" rx="22" fill="#fde4ea" />
        {T(222, 105, 40, "Autarquía", "b", fill=ACC5)}
        {T(222, 170, 30, "se administra")}
        {T(222, 210, 30, "a sí mismo")}
        {T(222, 300, 30, "ej.: el IPV", "b")}
        <g id="c5-aut2" class="h">
          <rect x="455" y="40" width="405" height="340" rx="22" fill="#fde4ea" />
          {T(657, 105, 40, "Autonomía", "b", fill=ACC5)}
          {T(657, 170, 30, "dicta sus")}
          {T(657, 210, 30, "propias normas")}
          {T(657, 285, 30, "ej.: un municipio", "b")}
          {T(657, 328, 30, "(ordenanzas)", "m", fill="#636e72")}
        </g>
      </g>"""
js = """
    show("#c5-a", 161.98);
    show("#c5-a2", 165.95);
    show("#c5-a3", 168.6);
    show("#c5-a4", 169.3);
    show("#c5-a5", 170.0);
    hide("#c5-a", 171.62);
    show("#c5-q", 171.67);
    hide("#c5-q", 173.92);
    fade("#c5-cen", 173.97);
    hide("#c5-cen", 178.75);
    fade("#c5-des", 178.8);
    show("#c5-des2", 183.23);
    show("#c5-des3", 188.6);
    hide("#c5-des", 194.64);
    fade("#c5-dsc", 194.69);
    hide("#c5-ente", 200.05);
    show("#c5-ipv", 200.05);
    show("#c5-ley", 201.2);
    tl.to("#c5-h1", { x: -30, rotation: -12, transformOrigin: "100% 50%", opacity: 0.25, duration: 0.4, ease: "power2.out" }, A(205.5));
    tl.to("#c5-h2", { x: 30, rotation: 12, transformOrigin: "0% 50%", opacity: 0.25, duration: 0.4, ease: "power2.out" }, A(205.5));
    show("#c5-ctrl", 206.6);
    hide("#c5-dsc", 209.09);
    fade("#c5-aut", 209.14);
    show("#c5-aut2", 212.79);"""
chapters.append(chapter("c5", 158.81, 217.43, "Capítulo 5", "Administración pública", ACC5, "#ffc2d1", 161.9, [(187.59, 194.5), (200.05, 208.9)], svg, js))

# ---------------------------------------------------------------- C6
ACC6 = "#138a8e"
names = [("Economía", 228.61), ("Eficiencia", 233.48), ("Eficacia", 238.53), ("Ejecutividad", 244.55), ("Efectividad", 248.67)]
lsvg = "".join(T(40, 130 + i * 62, 30, n, "b", "start", "#2d3436", f'id="c6-n{i}" opacity="0.35"') for i, (n, _) in enumerate(names))
svg = f"""
      <g id="c6-a" class="h">
        <g id="c6-h1">{T(440, 52, 38, "5 principios de la gestión pública", "b", fill=ACC6)}</g>
        <g id="c6-h2" class="h">{T(440, 52, 34, "Campaña de vacunación · 10.000 dosis", "b", fill=ACC6)}</g>
        <rect id="c6-hl" x="25" y="98" width="250" height="46" rx="23" fill="{ACC6}" opacity="0" />
        {lsvg}
        <path d="M300,90 L300,420" stroke="#dfe6e9" stroke-width="4" />
        <g id="c6-p0" class="h">
          {T(580, 140, 36, "gastar menos", "b", fill=ACC6)}
          <g transform="translate(580 240)"><path d="M-70,-40 L40,-40 L80,0 L40,40 L-70,40 Z" fill="#fdcb6e" /><circle cx="44" cy="0" r="10" fill="#ffffff" />{T(-15, 14, 40, "$", "b")}</g>
          <path d="M700,200 L700,280 M684,264 L700,282 L716,264" stroke="#00b894" stroke-width="8" fill="none" stroke-linecap="round" />
          {T(580, 340, 30, "menor precio,")}{T(580, 378, 30, "sin perder calidad")}
        </g>
        <g id="c6-p1" class="h">
          {T(580, 140, 36, "gastar bien", "b", fill=ACC6)}
          <rect x="350" y="180" width="460" height="70" rx="35" fill="#e0f4f4" />{T(580, 226, 30, "dosis por cada peso", "b")}
          <rect x="350" y="270" width="460" height="70" rx="35" fill="#e0f4f4" />{T(580, 316, 30, "dosis por cada enfermero", "b")}
        </g>
        <g id="c6-p2" class="h">
          {T(580, 140, 36, "gastar sabiamente", "b", fill=ACC6)}
          <rect x="340" y="190" width="480" height="56" rx="28" fill="#dfe6e9" />
          <rect id="c6-bar" x="340" y="190" width="432" height="56" rx="28" fill="#00b894" />
          {T(580, 300, 32, "9.000 de 10.000", "b")}
          <g id="c6-90" class="h">{T(580, 360, 40, "90 % de la meta", "b", fill=ACC6)}</g>
        </g>
        <g id="c6-p3" class="h">
          {T(580, 140, 36, "gastar a tiempo", "b", fill=ACC6)}
          <rect x="420" y="170" width="160" height="150" rx="14" fill="#ffffff" stroke="#2d3436" stroke-width="5" /><rect x="420" y="170" width="160" height="40" rx="10" fill="#74b9ff" />
          <path d="M500,232 L500,300 M470,248 L530,284 M530,248 L470,284" stroke="#74b9ff" stroke-width="7" stroke-linecap="round" />
          <circle cx="680" cy="245" r="40" fill="#00b894" /><path d="M660,245 L674,259 L700,231" stroke="#ffffff" stroke-width="8" fill="none" stroke-linecap="round" />
          {T(580, 380, 30, "las dosis llegan antes del invierno", "b")}
        </g>
        <g id="c6-p4" class="h">
          {T(580, 140, 36, "gastar satisfactoriamente", "b", fill=ACC6)}
          <path d="M360,170 L360,330 L820,330" stroke="#2d3436" stroke-width="5" fill="none" />
          <path id="c6-curva" d="M370,190 C470,200 520,240 600,270 S740,316 810,320" stroke="#d63031" stroke-width="8" fill="none" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" />
          {T(580, 385, 30, "baja la enfermedad", "b")}
        </g>
      </g>
      <g id="c6-b" class="h">
        <rect x="20" y="30" width="405" height="160" rx="20" fill="#f1f2f6" />
        {T(222, 90, 32, "Modelo burocrático", "b")}{T(222, 140, 30, "mira procedimientos", "m", fill="#636e72")}
        <rect x="455" y="30" width="405" height="160" rx="20" fill="#e0f4f4" />
        {T(657, 90, 32, "Modelo gerencial", "b", fill=ACC6)}{T(657, 140, 30, "mira resultados", "b", fill=ACC6)}
        <g id="c6-b2" class="h">
          <rect x="140" y="230" width="120" height="140" rx="6" fill="#ffffff" stroke="#2d3436" stroke-width="5" /><rect x="160" y="216" width="120" height="140" rx="6" fill="#ffffff" stroke="#2d3436" stroke-width="5" />
          <path d="M180,250 L260,250 M180,280 L260,280 M180,310 L240,310" stroke="#b2bec3" stroke-width="6" />
          {T(222, 410, 28, "recetas firmadas", "b", fill="#636e72")}
          <path id="c6-x" d="M120,220 L320,380 M320,220 L120,380" stroke="#d63031" stroke-width="10" pathLength="2" stroke-dasharray="2" stroke-dashoffset="2" />
        </g>
        <g id="c6-b3" class="h">
          <circle cx="657" cy="280" r="60" fill="#f5c9a0" /><circle cx="637" cy="268" r="7" fill="#2d3436" /><circle cx="677" cy="268" r="7" fill="#2d3436" />
          <path d="M630,298 Q657,322 684,298" stroke="#7a3b3b" stroke-width="7" fill="none" stroke-linecap="round" />
          <path d="M740,240 L724,224 A10,10 0 0,1 740,212 A10,10 0 0,1 756,224 Z" fill="#e84393" transform="scale(1.4) translate(-210 -66)" />
          {T(657, 410, 28, "pacientes que mejoraron", "b", fill=ACC6)}
        </g>
      </g>
      <g id="c6-c" class="h">
        <rect x="40" y="30" width="800" height="120" rx="20" fill="#e0f4f4" />
        <rect x="70" y="48" width="64" height="84" rx="6" fill="#ffffff" stroke="#2d3436" stroke-width="4" />
        <path d="M84,72 L120,72 M84,90 L120,90 M84,108 L110,108" stroke="#b2bec3" stroke-width="5" />
        {T(160, 85, 34, "Decreto Acuerdo 984/2016", "b", "start", ACC6)}
        {T(160, 125, 28, "Catamarca adhiere al plan nacional", "m", "start")}
        <g id="c6-e1" class="h">{box(40, 170, 800, 56, "Gobierno digital y abierto", ACC6, "#ffffff", 28)}</g>
        <g id="c6-e2" class="h">{box(40, 236, 800, 56, "Gestión integral de recursos humanos y calidad", ACC6, "#ffffff", 28)}</g>
        <g id="c6-e3" class="h">{box(40, 302, 800, 56, "Gestión por resultados y planificación estratégica", ACC6, "#ffffff", 28)}</g>
        <g id="c6-e4" class="h">{T(440, 410, 30, "Coordina: Secretaría General de Gobernación", "b")}</g>
      </g>"""
js = """
    fade("#c6-a", 220.97);
    hide("#c6-h1", 223.79);
    show("#c6-h2", 223.79);"""
prev = None
for i, (n, t) in enumerate(names):
    y = 98 + i * 62
    js += f'\n    tl.to("#c6-hl", {{ y: {y - 98}, opacity: 0.2, duration: 0.3, ease: "power2.inOut" }}, A({t}));'
    js += f'\n    tl.to("#c6-n{i}", {{ opacity: 1, duration: 0.2 }}, A({t}));'
    if prev is not None:
        js += f'\n    hide("#c6-p{prev}", {t});'
    js += f'\n    show("#c6-p{i}", {t});'
    prev = i
js += """
    tl.set("#c6-bar", { scaleX: 0, transformOrigin: "0% 50%" }, A(238.53));
    tl.to("#c6-bar", { scaleX: 1, duration: 2.2, ease: "power2.out" }, A(239.6));
    show("#c6-90", 242.3);
    draw("#c6-curva", 249.9, 2.0);
    hide("#c6-a", 254.55);
    fade("#c6-b", 254.6);
    show("#c6-b2", 259.72);
    draw("#c6-x", 261.2, 0.5);
    show("#c6-b3", 262.2);
    hide("#c6-b", 264.9);
    fade("#c6-c", 264.95);
    show("#c6-e1", 274.0);
    show("#c6-e2", 275.9);
    show("#c6-e3", 278.2);
    show("#c6-e4", 280.91);"""
chapters.append(chapter("c6", 217.43, 284.85, "Capítulo 6", "Gestión pública y modernización", ACC6, "#9fe6e8", 220.9, [(223.79, 254.5), (259.72, 264.85)], svg, js))

# ---------------------------------------------------------------- CIERRE
ACC7 = "#5b4bd6"
svg = f"""
      <g id="c7-a" class="h">
        {T(440, 80, 32, "Un hospital público gasta el presupuesto completo,")}
        {T(440, 125, 32, "pero atiende a la mitad de los pacientes previstos.")}
        <g id="c7-q" class="h">
          <rect x="80" y="180" width="720" height="110" rx="55" fill="{ACC7}" />
          {T(440, 250, 42, "¿Qué principio de gestión falla?", "b", fill="#ffffff")}
        </g>
        <g id="c7-c" class="h">{T(440, 360, 34, "Respondé en los comentarios", "b", fill=ACC7)}</g>
      </g>"""
extra = """
    <div class="pill-slot"><div id="c7-save" class="pill h"><svg width="30" height="38" viewBox="0 0 34 42"><path d="M3,3 H31 V39 L17,29 L3,39 Z" fill="#ffd166" /></svg>Guardá este video para el examen</div></div>"""
js = """
    show("#c7-a", 287.41);
    show("#c7-q", 292.2);
    pulse("#c7-q", 293.6);
    show("#c7-c", 294.86);
    hide("#c7-pill", 294.8);
    show("#c7-save", 295.6);
    pulse("#c7-save", 297.2);"""
chapters.append(chapter("c7", 284.85, 300.0, "Repaso", "Pregunta de repaso", ACC7, "#c3baff", 287.3, [], svg, js, extra))

# ---------------------------------------------------------------- INDEX
hosts = "".join(
    f"""
      <div id="{cid}" style="z-index: 2" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html"
        data-start="{t0}" data-duration="{dur}" data-track-index="2" data-track-kind="graphics"
        data-width="1080" data-height="1920"></div>"""
    for cid, t0, dur in chapters
)
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
