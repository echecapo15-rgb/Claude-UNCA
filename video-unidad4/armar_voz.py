"""Une las frases de voz/lNN.wav con pausas y escribe tiempos.json.

Pausa corta entre frases y pausa larga al cambiar de capítulo.
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

BASE = Path(__file__).parent
GAP_FRASE = float(sys.argv[1]) if len(sys.argv) > 1 else 0.35
GAP_CAPITULO = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
# Silencio extra antes de ciertas frases: "37:1.6,40:0.5"
EXTRA = {int(k): float(v) for k, v in (x.split(":") for x in sys.argv[3].split(","))} if len(sys.argv) > 3 else {}

lineas = [l.split("\t") for l in (BASE / "guion.tsv").read_text().splitlines() if l.strip()]
frames = []
tiempos = []
t = 0.0
rate = None
prev_cap = None
for i, (cap, texto) in enumerate(lineas, 1):
    with wave.open(str(BASE / "voz" / f"l{i:02d}.wav")) as w:
        rate = rate or w.getframerate()
        assert w.getframerate() == rate and w.getnchannels() == 1
        data = w.readframes(w.getnframes())
        dur = w.getnframes() / rate
    if prev_cap is not None:
        gap = (GAP_CAPITULO if cap != prev_cap else GAP_FRASE) + EXTRA.get(i, 0.0)
        frames.append(b"\x00\x00" * int(gap * rate))
        t += int(gap * rate) / rate
    tiempos.append({"n": i, "cap": cap, "ini": round(t, 2), "fin": round(t + dur, 2), "texto": texto})
    frames.append(data)
    t += dur
    prev_cap = cap

with wave.open(str(BASE / "voz.wav"), "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(rate)
    w.writeframes(b"".join(frames))

(BASE / "tiempos.json").write_text(json.dumps(tiempos, ensure_ascii=False, indent=1))
caps = {}
for x in tiempos:
    c = caps.setdefault(x["cap"], [x["ini"], x["fin"]])
    c[1] = x["fin"]
for k, (a, b) in caps.items():
    print(f"{k:7s} {a:7.2f} -> {b:7.2f}  ({b - a:5.1f} s)")
print(f"TOTAL {t:.2f} s")
