# Vídeo con sonido, GIF, alojamiento y post para foro

## 1. Toma de escaparate

Graba el guion `escaparate` en la máquina de render con estos parámetros:

- `-guion=escaparate.guion`
- `-video=mudo.mp4 -ffmpeg=<ruta>`
- `-registro=sucesos.jsonl`
- `-telemetria=camara.csv`
- un calentamiento previo de la caché

Después:

1. Mezcla la pista desde el registro de sucesos, con un script propio que coloque cada sonido en su tiempo, ponga topes de voces y pase un limitador al final. Debe dar `pista.wav`.
2. Une vídeo y pista: `ffmpeg -i mudo.mp4 -i pista.wav -c:v copy -c:a aac -b:a 256k -shortest demo.mp4`.

En el informe de la mezcla, revisa cuántas voces se descartaron y cuánto redujo el limitador. Aun así, **nadie ha escuchado la pista**: dilo al entregarla.

## 2. Tiempos de cada hechizo

`scripts/hoja_contacto.py <carpeta de la toma>` lee las `marca` y los `Lanzar` del registro, escribe `tiempos.json` y saca hojas de contacto.

Con esos tiempos se escribe la lista de cortes: cada corte empieza 1–2 s antes del lanzamiento y acaba cuando el efecto ya se entiende. Revísala en las hojas antes de cortar.

## 3. GIF y vídeos

`scripts/cortar_clips.py --video demo.mp4 --cortes cortes.json --salida <carpeta>` saca:

- **Un GIF por corte**, de menos de 9,5 MB.
  - Prueba a 640 px y 15 fps, y va bajando (560 y 480 px; 12 y 10 fps) hasta que cabe.
  - Usa una paleta de 128 colores con `stats_mode=diff` y tramado bayer.
  - Los hechizos largos o con mucho detalle acaban más pequeños.
- **La toma entera** en H.264: crf 23, tope de 14 Mb/s, audio aac a 192k y `+faststart`.
- **Con `--montaje`**, un montaje de menos de 60 s con los mismos cortes y fundidos de audio de 40–60 ms, por si el sitio limita la duración.

## 4. Subir a imgur (solo con permiso explícito)

Se sube con la cuenta del usuario en su navegador, mediante Claude in Chrome.

1. Copia los ficheros a una carpeta que el navegador pueda leer, porque `file_upload` solo admite rutas permitidas.
2. `file_upload` admite como mucho 10 MB **por llamada y por lote**. Sube los GIF de uno en uno, cada uno en su llamada, no en `browser_batch`.
3. Para ficheros de más de 10 MB:
   - Crea en la página un `input type=file` propio y pásale trozos de 9 MB (`split -b 9m`), cada uno en una llamada distinta.
   - Recompón el fichero con `new File(partes, nombre, {type})`.
   - Asígnalo con `DataTransfer` al input de subida de imgur y dispara `change` con `bubbles`. En un post ya creado, ese input aparece al pulsar «Add more images».
4. Para conservar el sonido del vídeo, pulsa «Yes, keep the audio». imgur aceptó 84 s con sonido, pero lo **recodificó a 854×480**.
5. Los enlaces directos están en `api.imgur.com/post/v1/albums/<id>?client_id=<el de la página>&include=media`.
   - Casa cada enlace con su fichero por orden y nombre.
   - Comprueba que los GIF descargados coinciden byte a byte (SHA-256) con los locales.
6. No compartas el post con la comunidad de imgur. Desde imgur, no hagas `fetch` a `127.0.0.1`: se queda colgado por el permiso de red local.

## 5. Licencias antes de publicar

- Los GIF no llevan sonido, así que no hay nada que revisar en ellos.
- El vídeo sí lo lleva. Si usa muestras de Sonniss, ojo: su licencia prohíbe distribuir los efectos como tales. Un vídeo de juego no debería ser ese caso, pero díselo al usuario y que decida él.
- Si los paquetes de sonido se bajaron de una réplica, vuelve a bajarlos de la fuente oficial antes de publicar nada.

## 6. El post

BBCode de foro, como en Mediavida:

- `[b]` para la negrita;
- `[list][*]…[/list]` para las listas;
- `[img]https://i.imgur.com/<id>.gif[/img]` para cada GIF;
- `[media]https://i.imgur.com/<id>.mp4[/media]` para el vídeo;
- una línea en negrita para cada título de sección.

El tono, cercano y en el idioma del usuario. Cuenta lo que falla igual que lo que sale bien.

Este orden funcionó:

1. Qué es y por qué.
2. El vídeo.
3. Cada pieza con su GIF.
4. Cómo se ha hecho.
5. Los números.
6. Lo que falla.
7. Lo que viene.
8. Una pregunta al foro.
