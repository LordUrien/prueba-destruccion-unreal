# Plantilla del contrato común

El contrato es lo único que comparten los talleres. Escríbelo antes de abrir ninguna sesión y guárdalo como `CONTRATO.md` en la raíz de la prueba. Cuando lleguen hechizos nuevos, amplíalo sin cambiar lo que ya hay.

## 1. Qué es y qué no es

Una línea que diga que es una **prueba desechable**, sin historia ni puzles, y de qué sala parte. Si la cuota de uso de Claude se reinicia a una hora conocida, anótala: hay que tener una versión jugable mucho antes de esa hora y mejorarla después.

## 2. Qué se entrega al final

1. Un paquete de Windows que el usuario arranca a mano (`entrega/juego/`, con un `.bat`).
2. Un vídeo de demostración grabado sin ventana, con sonido, a 1080p60, de un recorrido con guion.
3. Las medidas de rendimiento en la gráfica de referencia y, si hay alguna libre, en la gama de los jugadores.

## 3. Controles

Fíjalos desde el principio. Estos fueron los usados:

- WASD y ratón para moverse y mirar.
- Teclas numéricas o rueda del ratón para elegir hechizo.
- Botón izquierdo mantenido para cargar; al soltarlo, se lanza. El derecho cancela.
- Espacio para saltar, Ctrl o C para agacharse y Mayús para el dash.
- Tab para el menú, porque Esc queda reservado.

## 4. Ficha de cada hechizo

Una tabla con carga, viaje, daño, rastro y enfriamiento. Por ejemplo:

| | Fuego | Hielo | Rayo |
|---|---|---|---|
| Carga | Llama que crece entre las manos | Escarcha en los dedos | Arcos eléctricos entre los dedos |
| Viaje | Bola a 28 m/s, con caída | Lanza a 45 m/s, recta | Instantáneo, ramificado |
| Daño | Explosión de 2,5 m; empuja y prende | Impacto de 1,5 m; congela, y lo congelado se rompe con el siguiente golpe | Perfora 2 objetos; salta al hierro |
| Rastro | Hollín y fuego que dura | Hielo que se funde con fuego | Quemadura en estrella |
| Enfriamiento | 0,9 s | 0,7 s | 1,4 s |

Son cifras de partida: quien las cambie lo anota en el contrato.

**Cuánto destruye.** Por ejemplo: un tramo de muro de 3 m cae con 4 o 5 hechizos, y la sala entera queda en ruinas en unos 3 minutos. Lo que pierde sus apoyos cae solo. Lo que no se ve no se rompe sin causa.

## 5. Reparto y carpetas

Cada taller trabaja en `<prueba>/<taller>/`, con su propia copia del proyecto Unreal (sin `Binaries`, `Intermediate`, `Saved`, `DerivedDataCache` ni `Content`). Nadie edita la carpeta de otro taller. Cada plugin se entrega en `entrega/<Plugin>/`, sin binarios, con un `LEEME.md` que diga qué hace, cómo se activa, qué falta y qué cuesta.

## 6. El bus de sucesos

Un plugin común (`HechizosComun`, con un `UHechizosBus` de delegados) es **la única vía de comunicación entre plugins**. Ningún plugin incluye cabeceras de otro, salvo el del personaje con el de las manos.

**Reglas del bus**

- Quien necesite un suceso nuevo lo añade al final, sin tocar los que ya hay, y avisa al Núcleo. Es el único fichero que todos pueden escribir, así que los cambios deben ser pequeños, y hay que volver a leerlo justo antes de tocarlo.
- El enum de hechizos crece siempre por el final, antes de `Cuantos`. Las tablas por tipo de hechizo se dimensionan con esa constante.
- Se usan las unidades de Unreal (cm, kg, s), con Z hacia arriba.

**Quién publica y quién escucha**

- El Núcleo publica carga, lanzamiento, proyectiles e impactos.
- Efectos y Sonido solo escuchan.
- Estructura escucha los impactos y publica roturas, golpes de escombro y cambios de estado.
- Objetos responde cuando se coge o se suelta algo y publica los golpes físicos.

**Sucesos que hicieron falta**

- Lanzamiento: `AlCargar`, `AlCancelar`, `AlLanzar`, `AlCrearProyectil`, `AlImpactar` (tipo, punto, normal, radio y energía) y `AlDescargarRayo`.
- Destrucción: `AlRomper` (material, masa y si es estructural), `AlGolpearEscombro` y `AlCambiarEstado`.
- Movimiento: `AlDash`, `AlSaltar`, `AlAterrizar` y `AlAgacharse`.
- Coger y lanzar objetos: `AlPedirCoger`, `AlCogerObjeto`, `AlMoverCogido`, `AlLanzarCogido`, `AlSoltarObjeto` y `AlGolpeFisico` (en julios; contra un muro, 2.000 J equivalen a energía 1).
- Hechizos con suceso propio: `AlCrearMuroHielo`, `AlTormenta`, `AlCambiarInvisibilidad`, `AlExtraerEsencia`, `AlDuplicarObjeto`, `AlAtraer`, `AlSoltarAtraccion` y `AlTiempoLento`.
- Otros: `AlEncender`.

**Cómo se modelan los hechizos especiales**

- Los sostenidos (haz y aliento) son un proyectil con cuerpo que sigue al punto, más impactos pequeños a frecuencia fija: 15 Hz con energía 0,08 en uno y 10 Hz con 0,05 en el otro.
- La tormenta es una zona que dispara rayos normales de energía baja.
- Reconstruir es un impacto de tipo propio que cada taller interpreta a su manera.

Para probar sin depender de los demás, cada taller lanza los sucesos desde su propio banco de pruebas (`-banco=<lista>`).

## 7. Reglas de calidad

- Escribe antes qué debe verse, comprueba con números todo lo que se pueda, saca vistas fijas repetibles y pásale las imágenes a un revisor limpio.
- El informe separa lo medido, lo visto y lo no probado.

## 8. Rendimiento

La referencia es la gráfica habitual del usuario a 1080p con TSR al 75 %. Durante una explosión se admite que baje, pero nunca de 30 fps. Limita los cuerpos activos y los efectos, y duerme o funde el escombro.

## 9. Tandas

Si hay hechizos nuevos, cada tanda termina en un paquete probado, porque el usuario juega por tandas. Un hechizo flojo se entrega con su fallo dicho, sin bloquear a los demás. El más arriesgado (aquí, Reconstruir) lleva por escrito un plan B.
