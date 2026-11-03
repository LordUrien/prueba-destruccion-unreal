"""Tiempos de cada hechizo y hojas de contacto de una toma con registro.

Uso: python hoja_contacto.py <carpeta de la toma> [--video mudo.mp4] [--fotos 6] [--antes 1.2]

La carpeta debe tener sucesos.jsonl (con sucesos «Marca» y «Lanzar») y el vídeo.
Escribe tiempos.json y hojas/hojaN.jpg: una fila por hechizo, de 1,2 s antes de
lanzarlo hasta la marca siguiente. Necesita ffmpeg en el PATH y Pillow.
"""
import argparse, json, pathlib, subprocess
from PIL import Image, ImageDraw

a = argparse.ArgumentParser()
a.add_argument("toma")
a.add_argument("--video", default="mudo.mp4")
a.add_argument("--fotos", type=int, default=6)
a.add_argument("--antes", type=float, default=1.2)
o = a.parse_args()

R = pathlib.Path(o.toma)
H = R / "hojas"; H.mkdir(exist_ok=True)
lanz, marcas = {}, []
for l in open(R / "sucesos.jsonl", encoding="utf8"):
    e = json.loads(l)
    if e["suceso"] == "Lanzar": lanz[e["tipo"]] = e["t"]
    if e["suceso"] == "Marca": marcas.append((e["texto"], e["t"]))

filas, tiempos = [], {}
for (n, t), (_, s) in zip(marcas, marcas[1:]):
    l = lanz.get(n)
    if l is None: continue  # la marca no corresponde a ningún hechizo lanzado
    tiempos[n] = dict(marca=t, lanza=l, sigue=s)
    print(f"{n:14} marca {t:6.2f}  lanza {l:6.2f}  sigue {s:6.2f}")
    ini = l - o.antes
    filas.append((n, ini, (s - ini) / o.fotos))
json.dump(tiempos, open(R / "tiempos.json", "w", encoding="utf8"), indent=1)

W, Hh = 300, 169
for b in range(0, len(filas), 5):
    hoja = Image.new("RGB", (W * o.fotos, Hh * 5))
    for y, (n, ini, paso) in enumerate(filas[b:b + 5]):
        for x in range(o.fotos):
            f = H / "t.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ini + x * paso:.2f}", "-i", str(R / o.video),
                            "-frames:v", "1", "-vf", f"scale={W}:{Hh}", "-q:v", "3", str(f)], check=True)
            i = Image.open(f).convert("RGB")
            if x == 0: ImageDraw.Draw(i).text((6, 6), n, fill="yellow")
            hoja.paste(i, (x * W, y * Hh))
    hoja.save(H / f"hoja{b // 5}.jpg", quality=85)
(H / "t.jpg").unlink(missing_ok=True)
