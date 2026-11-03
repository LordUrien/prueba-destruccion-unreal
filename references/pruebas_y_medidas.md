# Unreal sin ventana, máquinas, guiones y medidas

Conviene tener desde el primer día un pequeño juego de scripts para:

- compilar;
- empaquetar;
- subir el paquete a otra máquina y lanzarlo allí;
- grabar una toma;
- medir;
- resumir las medidas.

## Unreal sin ventana y entre sesiones

- **Mutex:** UBT y UAT solo admiten una instancia. Si varias sesiones compilan, usa `-WaitMutex -WaitForUATMutex`.
- **Caché:** no compartas Zen (`bUseZenStore=False`). Lleva la DDC a un disco con espacio mediante `UE-LocalDataCachePath`. Como el nombre lleva guion, se pasa con `env` o desde PowerShell.
- **Procesos largos:** empaqueta sin recompilar si el código no ha cambiado. Lanza en segundo plano las órdenes que tardan, con prioridad `BelowNormal`.
- **Contenido que C++ carga por ruta:** añade `+DirectoriesToAlwaysCook=(Path="/<Plugin>")` en `DefaultGame.ini`.
- **Para jugar sin ventana:** `-RenderOffscreen -windowed -nosound -unattended -nosplash -cvar=t.MaxFPS=55`. Baja a 30 si la GPU tarda más de 18 ms por fotograma.
- **Banderas repetidas:** `FParse::Value` se queda con la primera aparición de cada bandera.
- **Discos:** un disco mecánico es un cuello de botella al compilar y cocinar. El motor, la caché y lo compilado van mejor en un SSD, enlazados con *junctions* si hace falta.

## Máquinas

- **Grabar y probar:** en una GPU grande, por SSH o WinRM. El script de lanzamiento no debe arrancar nada si la GPU no está libre: uso de hasta el 30 % y memoria por debajo de un límite propio de cada máquina. Para pasar ficheros grandes por SSH, tar es más fiable que scp.
- **Medir:** en la gráfica habitual del usuario y en la gama de sus jugadores, con la misma comprobación previa.
- **PC de trabajo:** usa un cerrojo común para que dos sesiones no ocupen la GPU a la vez.
- **Comprobar si una máquina está viva:** el ping no basta, porque algunas no responden a ping y sí a WinRM.
- **Accesos:** no instales claves ni accesos permanentes en máquinas ajenas sin permiso explícito.

## Guiones del personaje

Cada guion es un fichero `.guion` con una orden por línea. Las coordenadas son de la sala, en metros: x de la puerta al fondo, y de lado a lado, z desde el suelo.

```
marca <nombre>          # marca en el registro; sirve para cortar clips
hechizo <ficha>         # elige hechizo
mira x y z [s]          # gira la vista hacia un punto
anda x y [s]            # camina hasta un punto
carga s                 # mantiene el botón s segundos y suelta
cancela s
espera s
espera_enfriar
salta [s] | agacha [s] | dash delante|atras|izquierda|derecha | rueda
fin
```

Guiones que hicieron falta:

| Guion | Para qué |
|---|---|
| `prueba` | Recorrido corto que debe acabar con salida 0 |
| `tanda1`, `tanda23` | Lanzar varias veces cada hechizo nuevo |
| `poder` | Cargas largas y cámara |
| `demo` | Recorrido largo para el vídeo |
| `escaparate` | Los quince hechizos en una toma, de menos a más, con una `marca` antes de cada uno y Reconstruir al final |

## Qué se mide y con qué topes

Fija los topes antes de mirar los resultados:

- **Rendimiento** (Shipping, 1080p, TSR al 75 %):
  - fps medios, p95 y p99;
  - fotograma más lento y p99 de la GPU;
  - fotogramas por encima de 33 ms.

  Mide con la caché de sombreadores caliente, con un calentamiento previo, y dilo en el informe.
- **Mareo**, con la telemetría de la cámara:
  - campo de visión entre 78 y 104°;
  - ángulo hasta 4°;
  - balanceo hasta 3°;
  - vaivén hasta 0,3°;
  - el parón más largo.

  Con Movimiento a 0, todo debe quedar quieto.
- **Luz:**
  - el salto de luma no puede pasar de 25 en 0,2 s;
  - cuenta los parpadeos de un solo fotograma.
- **Destrucción:**
  - piezas que quedan en pie tras N impactos;
  - impactos que aguanta un tramo;
  - lo que queda flotando.
- **Cierre:**
  - cada guion termina con código 0;
  - cada hechizo publica sus sucesos (compruébalo en el JSONL).

Cifras de referencia de la prueba original, con 15 hechizos y la sala derrumbándose:

- Quadro P5000: 63–76 fps.
- RTX 3060: 89–106 fps.

Sirven para saber si algo ha empeorado.

## Revisión visual

1. **Hojas de contacto.** Saca hojas de contacto con `scripts/hoja_contacto.py`: 6 fotogramas por hechizo, desde 1,2 s antes del lanzamiento hasta la marca siguiente. También vale tomar unos 49 fotogramas alrededor de cada lanzamiento.
2. **Revisor limpio.** Dáselas a un subagente que no sepa qué se ha cambiado, junto con una guía de revisión visual: qué mirar en geometría, materiales, composición y sombras.
3. **Fallos.** Pide cada fallo con su gravedad (A, M o B) y el segundo exacto. Comprueba uno a uno los graves antes de darlos por ciertos.
