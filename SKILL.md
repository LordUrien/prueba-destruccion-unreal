---
name: prueba-destruccion-unreal
description: Monta en Unreal 5.x, sin abrir ventanas, una prueba jugable de destrucción con un mago en primera persona (manos visibles, hechizos con carga, cámara, efectos, sonido, muros y muebles que se rompen y se reconstruyen), repartida en talleres paralelos con un bus de sucesos, medida en varias gráficas y con vídeo, GIF y post de foro al final. Úsala siempre que el usuario pida una sala o demo de destrucción, hechizos, poderes, física de roturas, un «mago que lo rompa todo», ampliar hechizos de una prueba así o sacar su vídeo y sus GIF, aunque no diga «skill» ni «destrucción».
---

# Prueba de destrucción con hechizos en Unreal

Esta skill recoge cómo se hizo en unos dos días, con Claude Code, una prueba desechable en Unreal 5.8: un mago en primera persona con quince hechizos convierte en ruinas una sala abovedada y después la reconstruye. Se empaquetó en Shipping, se midió en tres gráficas y se publicó en quince GIF y un vídeo con sonido. Úsala como receta y como lista de trampas en las que ya se cayó.

## Reglas de trabajo

Con estas reglas la prueba salió sin sustos. Ajústalas a lo que pida tu usuario:

- **Nada de ventanas 3D en el PC de trabajo.** Unreal con `-RenderOffscreen` o `-nullrhi` y Blender con `-b`. El paquete jugable lo abre el usuario.
- **Coste cero y licencias comprobadas.** Todo propio o gratuito con licencia válida: Poly Haven CC0, MPFB/MakeHuman CC0, Sonniss GDC, Freesound CC0 o CC BY. Cada taller anota el origen en su `LICENCIAS.md`. Mejor sonido grabado de verdad que sintetizado, sin voces de TTS y sin estridencias: graves con cuerpo y agudos contenidos.
- **Gráficas compartidas.** Antes de usar una GPU, comprueba que esté libre. Trabaja con prioridad baja, sin colas ni tareas programadas, y cede la máquina si otro la necesita.
- **Nada se publica sin preguntar.** Subir a un servicio externo o escribir en un foro requiere permiso explícito para cada subida.

## Cómo está organizada

Un solo agente no puede con todo en un tiempo razonable. Funcionó así: **un Núcleo que integra y cinco talleres en paralelo**. Cada taller trabaja en su propia sesión de Claude Code y en su propia copia del proyecto de Unreal, y todos hablan solo a través de un plugin común de sucesos.

| Taller | Entrega | Qué se aprendió |
|---|---|---|
| Núcleo | Plugin del personaje: entrada, hechizos en fichas, cámara, guion, vídeo, registro, integración y paquete | Decide qué está listo. Publica la carga, el lanzamiento, los proyectiles y los impactos |
| Manos | Brazos en primera persona, con un gesto por hechizo | La malla, aplastada hacia la cámara, no atraviesa los muros. El hechizo sale en el fotograma que marca el gesto |
| Efectos | Todo lo visual, solo escuchando | Niagara no se puede montar sin el editor. Se usó un sistema propio con `FDynamicMeshBuilder` y flipbooks de Mantaflow hechos con Blender `-b` |
| Estructura | Muros, bóveda, arcos y vidrieras, pieza a pieza | Piezas sueltas con un grafo de apoyos, no Geometry Collection. Topes de cuerpos físicos, y el escombro dormido pasa a instancias |
| Objetos | Muebles troceados en dos niveles, cada uno con su ficha | Muebles CC0 troceados por script con semillas fijas. Los estados (arde, carbón, hielo) van en Custom Primitive Data |
| Sonido | Banco de sonidos y mezcla, solo escuchando | Se comprueba con números porque nadie escucha. El usuario juzga cómo suena |

Antes de arrancar los talleres, escribe el contrato con [references/contrato.md](references/contrato.md): reparto, carpetas, bus de sucesos, cifras de partida de cada hechizo y reglas de calidad y rendimiento. Lo que cada taller necesita saber de su oficio está en [references/talleres.md](references/talleres.md).

## Pasos

1. **Acordar el alcance con el usuario:** qué hechizos, qué controles, qué sala, qué gráficas de referencia y qué permisos. Si pide hechizos nuevos, dale primero una lista con una línea por hechizo y deja que elija. Agrúpalos en tandas que se puedan entregar jugables una a una.
2. **Escribir el contrato y abrir los talleres.** Escribe `CONTRATO.md` y abre una sesión por taller con un encargo que se entienda solo. Cada taller entrega pronto y a menudo en `entrega/<Plugin>/`, con un `LEEME.md` que diga qué hace, cómo se activa, qué falta y qué cuesta.
3. **Integrar sin parar (Núcleo).** Integra lo que haya en cada momento, compila y empaqueta en Shipping. Los detalles de Unreal sin ventana (mutex de UBT, cocinado por ruta, `t.MaxFPS`, DDC, Zen) están en [references/pruebas_y_medidas.md](references/pruebas_y_medidas.md).
4. **Probar sin ventana con un guion.** El personaje se mueve con un `.guion` de órdenes sencillas. Si un guion no acaba con salida 0, es un fallo. Mide fps, p95, p99, parones, mareo de cámara y saltos de luz con los topes fijados *antes* de mirar.
5. **Pasar la imagen a un revisor limpio.** La autocrítica visual no es fiable. Escribe antes qué debe verse, saca vistas fijas repetibles (hojas de contacto) y dáselas a un subagente que no conozca el trabajo, junto con una guía de revisión visual. No des nada por bueno porque compile.
6. **Grabar la toma de escaparate con sonido.** Un solo guion con todos los hechizos, de menos a más, grabado a 1080p60 por tubería a ffmpeg. El registro de sucesos en JSONL alimenta una mezcla de sonido hecha después, fuera del juego. Ver [references/video_y_publicacion.md](references/video_y_publicacion.md).
7. **Sacar GIF, vídeo y post.** Un GIF de menos de 10 MB por hechizo con `scripts/cortar_clips.py` y una hoja de contacto con `scripts/hoja_contacto.py`. Súbelo todo a un alojamiento de imágenes solo con permiso y escribe el post en el formato del foro.
8. **Escribir el informe.** Un `INFORME.md` que separe lo medido, lo visto y lo no probado, y que termine con lo que harías en otra vuelta, por orden de importancia.

## Trampas en las que ya se cayó

- **Un derrumbe congelaba el juego:** cada rotura pedía un parón de cámara, y los parones se encadenaban cada 0,48 s durante 24 s. Limítalos a uno cada 4 s.
- **Sucesos sin oyente:** las velas no volvían a encenderse tras Reconstruir porque nadie escuchaba `AlEncender`. Comprueba en el registro que cada suceso nuevo tiene quien lo oiga.
- **`-RenderOffscreen` sin `Present`:** la CPU se adelanta a la GPU, las medidas salen falsas y el juego acaba en «Out of video memory». Usa `-cvar=t.MaxFPS=55`, o 30 si la GPU pasa de 18 ms por fotograma.
- **Contenido que C++ carga por ruta:** si falta `+DirectoriesToAlwaysCook` en `DefaultGame.ini`, el paquete sale sin esos materiales y nada avisa.
- **Tirones la primera vez que se lanza un hechizo:** son sombreadores que se compilan en el primer uso. Si no hay catálogo de PSO, mide con la caché caliente y dilo.
- **Destellos:** fuego, onda y meteoro llenan la pantalla de luz. Mide el salto de luma (el tope usado fue 25 en 0,2 s) y pon en el menú opciones para quitar el movimiento de cámara y los destellos.
- **Efectos que no se leen:** un hechizo que funciona pero cuyo efecto nace fuera de cuadro o pegado a la cámara (Duplicar), o que no da una señal clara (Tiempo lento, Haz), parece torpe. Diseña cada efecto para que se lea desde la cámara del jugador.
- **`FParse::Value` se queda con la primera aparición de cada bandera:** no repitas una bandera esperando que gane la última.
- **imgur:** recodifica el vídeo a 854×480, y `file_upload` no pasa de 10 MB por llamada. El método para subir está en la referencia de publicación.

## Skills y herramientas que ayudaron

- `superpowers:brainstorming`: para cerrar el diseño con el usuario antes de tocar código.
- `anthropic-skills:deep-research`: para investigar Unreal 5.8, las licencias de recursos para un juego público, Lumen por software en gráficas modestas y cómo modelar con Claude sin ventana.
- `workflow-authoring` (herramienta Workflow): para que varios agentes contrastaran a la vez un método de modelado 3D publicado por terceros.
- `anthropic-skills:chrome-browser`: para leer referencias con la sesión del usuario y subir los GIF y el vídeo a su cuenta.
- Subagentes como revisores limpios, y sesiones paralelas de Claude Code para los talleres.
- Valoradas y no usadas en la prueba: Loom (texturas estilizadas; útil si hacen falta runas o materiales propios), Kiln (mallas low-poly, descartada para lo que se ve en pantalla) y blender-skills (no se instaló; solo se aprovechó la idea de los kits modulares).
