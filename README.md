# prueba-destruccion-unreal

Skill para Claude Code. Explica cómo montar en Unreal 5.x, sin abrir ventanas, una prueba jugable de destrucción: un mago en primera persona con hechizos que hacen pedazos una sala y la reconstruyen. El trabajo se reparte en talleres paralelos que se comunican por un bus de sucesos, se mide en varias gráficas y termina con vídeo, GIF y un post para el foro.

## Instalación

1. Pulsa **Code → Download ZIP**.
2. Copia la carpeta en `~/.claude/skills/prueba-destruccion-unreal/`. En Windows, la ruta es `C:\Users\<tu usuario>\.claude\skills\prueba-destruccion-unreal\`.
3. Claude la usará solo cuando le pidas una prueba de destrucción, hechizos, o el vídeo y los GIF de una prueba así.

Los scripts necesitan Python 3 con Pillow y ffmpeg en el PATH.

## Contenido

- `SKILL.md`: el método, los pasos, las trampas conocidas y las skills que ayudaron.
- `references/`: plantilla del contrato entre talleres, lecciones de cada taller, pruebas y medidas, y vídeo y publicación.
- `scripts/`: `hoja_contacto.py` (tiempos y hojas de contacto de una toma) y `cortar_clips.py` (GIF de menos de 10 MB y vídeo).
