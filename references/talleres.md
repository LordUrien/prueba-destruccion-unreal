# Lo que cada taller tiene que saber

Resumen de lo que aprendió cada taller en la prueba original.

## Núcleo: el personaje

- **Movimiento:** dash de 4,5 m en 0,14 s, con 1,1 s de enfriamiento.
- **Hechizos:** cada uno es una ficha de datos. La carga dura lo que dura el gesto de las manos.
- **Cuándo sale el hechizo:** en el fotograma que marcan las manos (`AlMomentoLanzar`). Si esa señal no llega en 0,8 s, sale igual.
- **Cámara:** cada hechizo tiene su propia tensión al cargar y su propia patada al soltar. Encima van la respiración, el balanceo, una sacudida que depende de la distancia y parones breves. Los resortes corren a 240 Hz, independientes de los fotogramas.
- **Tiempo lento:** dilatación global del tiempo. El mago se compensa con `CustomTimeDilation` para no frenarse.
- **Exposición:** automática por histograma, porque la sala pasa de luz de velas a cielo abierto.
- **Ajustes:** todo se cambia por línea de órdenes (`-mago.<hechizo>.<campo>=`, `-cam.<campo>=`, `-ojo.*`).
- **Banco:**
  - juega un guion (`-guion=`);
  - mide (`-medir=`);
  - graba vídeo por tubería a ffmpeg (`-video= -ffmpeg=`);
  - saca telemetría de la cámara (`-telemetria=`);
  - registra cada suceso en JSONL (`-registro=`).
- **Menú de accesibilidad:** `Movimiento` y `Destellos`, de 0 a 1. A 0 quitan por completo el movimiento de cámara, los parones y los destellos.

## Manos

- **Malla:** MPFB/MakeHuman (CC0), con rig y animación propios hechos en Blender `-b`.
- **Gestos:** uno por hechizo. Los principales tienen dos variantes de remate que se alternan.
- **Primera persona:** la malla se aplasta hacia la cámara (escala 0,4) para no atravesar muros, y usa su propio campo de visión.
- **Enganches para los efectos:** palmas, yemas y foco. Se recolocan cada fotograma con la corrección de primera persona.
- **Materiales:** dos parámetros. `Escarcha` cubre la piel de hielo. `Invisible` deja solo un contorno que ondula.
- **Piel:** `MSM_SUBSURFACE_PROFILE` deja ver el fondo a través de la mano en primera persona, así que se usa piel preintegrada.
- **Coste:** unos 0,4 a 0,7 ms en una Quadro P5000.

## Efectos

- **Sin Niagara:** desde Python no se pueden añadir emisores ni módulos, y los emisores ligeros no tienen colisión.
- **Sistema propio:** dibuja con `FDynamicMeshBuilder`, con un lote por material ordenado de atrás hacia delante. Es determinista, así que el banco se repite igual fotograma a fotograma.
- **Recursos:**
  - flipbooks simulados con Mantaflow en Blender `-b`;
  - materiales escritos en HLSL;
  - un commandlet que crea las texturas y los materiales.
- **Banco:** `-banco=<efecto> -bvista=mano|lado|cerca|sala`. Saca imágenes, vídeo o medidas.
- **Exposición al medir:** una entrega salió hasta 8 veces más oscura de lo esperado con la exposición real del juego. Mide los efectos con esa exposición, no con una fija.

## Estructura

- **Piezas:** la sala tiene 2.845 piezas reales (sillares, relleno, bóveda, nervios, arcos y vidrieras), no Geometry Collection. Los tramos intactos se pintan con 108 mallas fundidas, y las piezas aparecen con el primer daño.
- **Daño:** se acumula por pieza y pasa por tres estados: grieta (0,3), floja (0,6) y rota (1).
- **Apoyos:** un grafo que se recalcula a 10 Hz.
  - Una pieza carga sobre la de abajo si su centro queda encima del apoyo.
  - En voladizo, una pieza aguanta como mucho 60 cm.
  - Un lienzo que pierde la mitad de sus sillares se desploma y deja un resto bajo.
- **Topes:** 160 cuerpos físicos a la vez. Lo que no cabe cae sin colisión, guiado por trazas. Lo que lleva más de 3 s dormido por debajo de 1,5 m pasa a escombro instanciado.
- **Luz:** `AjustarLuz` baja el sol, el cielo y la niebla según lo abierto que esté el techo. Sin esto, a cielo abierto la imagen se quema.
- **Sillares flotantes:** salieron. Hace falta un registro de lo que queda en el aire y un revisor que lo busque.
- **Reconstruir:** las piezas vuelven a su sitio por oleadas en 9 s y los cascotes se encogen. Una pieza que caería sobre el jugador espera, sin colisión, a que se aparte.

## Objetos

- **Catálogo:** 39 modelos CC0 colocados en 213 sitios. Se trocean por script, con semillas fijas, en 610 piezas de nivel 1 y 1.763 de nivel 2.
- **Formato de las piezas:**
  - glTF con una ficha JSON (cm, kg, J);
  - uniones con la fuerza que aguantan, en julios;
  - formas de colisión;
  - variante doblada para el hierro.
- **Estados:** carbón, brasa y hielo van en Custom Primitive Data. Lo congelado se hace añicos con cualquier golpe.
- **Topes:** 60 cuerpos activos, 700 restos, 24 fuegos y 6 roturas por fotograma.
- **Telequinesis:** la velocidad del lanzamiento la calcula Objetos según la masa, y el daño se mide en julios.

## Sonido

- **Banco:** grabaciones reales troceadas en muestras. Cada hechizo tiene, por nombre: carga en bucle, inicio, carga llena, cancelar, lanzar, vuelo en bucle e impacto.
- **Mezcla en juego:**
  - Doppler en cada fotograma;
  - truenos que ruedan por la sala;
  - roturas por material, en tres tamaños;
  - un lecho de escombro que crece con la densidad;
  - topes de voces simultáneas.
- **Dash:** inspirado en el teletransporte de Dragon Ball, pero hecho con material propio y con licencia; nada sale de la serie.
- **Comprobación:** solo con números (picos, LUFS, bandas y repetición). Cómo suena de verdad lo decide el usuario al jugar.
- **Mezcla del vídeo:** las tomas van con `-nosound`, así que el sonido del vídeo se mezcla después, fuera del juego, a partir del registro de sucesos.
- **Si el usuario no oye nada:** Unreal silencia por defecto las ventanas sin foco. Compruébalo primero.
