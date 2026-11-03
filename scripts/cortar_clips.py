"""GIF por hechizo, toma entera comprimida y, si se pide, montaje corto.

Uso: python cortar_clips.py --video demo.mp4 --cortes cortes.json --salida <carpeta> [--limite 9.5] [--montaje]

cortes.json es una lista [["01_fuego", inicio, fin], ...] en segundos de la toma.
Cada GIF baja de tamaño (ancho y fps) hasta caber en el límite, en MB, porque
imgur y los foros cortan a 10 MB. Necesita ffmpeg en el PATH.
"""
import argparse, json, pathlib, subprocess

a = argparse.ArgumentParser()
a.add_argument("--video", required=True)
a.add_argument("--cortes", required=True)
a.add_argument("--salida", required=True)
a.add_argument("--limite", type=float, default=9.5)
a.add_argument("--montaje", action="store_true", help="montaje de menos de 60 s con los mismos cortes")
o = a.parse_args()

SRC = o.video
S = pathlib.Path(o.salida); S.mkdir(parents=True, exist_ok=True)
CORTES = json.load(open(o.cortes, encoding="utf8"))
LIM = o.limite * 1e6
X264 = ["-c:v", "libx264", "-preset", "medium", "-crf", "23", "-maxrate", "14M", "-bufsize", "28M",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart"]

for n, ini, fin in CORTES:
    f = S / f"{n}.gif"
    for w, fps in ((640, 15), (560, 15), (480, 15), (480, 12), (400, 12), (360, 10)):
        vf = (f"fps={fps},scale={w}:-2:flags=lanczos,split[a][b];[a]palettegen=max_colors=128:stats_mode=diff[p];"
              f"[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ini), "-t", f"{fin - ini:.2f}", "-i", SRC,
                        "-vf", vf, "-loop", "0", str(f)], check=True)
        if f.stat().st_size <= LIM: break
    print(f"{n:18} {fin - ini:4.1f} s  {w}px {fps} fps  {f.stat().st_size / 1e6:.1f} MB", flush=True)

subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, *X264, str(S / "toma_entera.mp4")], check=True)

if o.montaje:
    fc, m = [], []
    for i, (_, ini, fin) in enumerate(CORTES):
        fc.append(f"[0:v]trim={ini}:{fin},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={ini}:{fin},asetpts=PTS-STARTPTS,"
                  f"afade=t=in:d=0.04,afade=t=out:st={fin - ini - 0.06:.2f}:d=0.06[a{i}]")
        m.append(f"[v{i}][a{i}]")
    fc.append("".join(m) + f"concat=n={len(CORTES)}:v=1:a=1[v][a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", ";".join(fc),
                    "-map", "[v]", "-map", "[a]", *X264, str(S / "montaje.mp4")], check=True)

for f in sorted(S.glob("*.mp4")): print(f.name, f"{f.stat().st_size / 1e6:.1f} MB")
