# Sonidos del Omnitrix

| Archivo | Momento de reproducción |
| --- | --- |
| `core-ready.mp3` | Primer clic o Enter: el símbolo hundido se levanta. |
| `omnitrix-transform.mp3` | Segunda pulsación: se presiona el símbolo y comienza la transición al dashboard. |
| `omnitrix-time-out.mp3` | Cuando quedan cuatro segundos en cualquiera de las cuatro categorías del cuestionario; una reproducción por ronda. |

Los MP3 fueron proporcionados por el usuario. Los de entrada se incorporan localmente mediante `pantalla_inicio.py`; no hay descarga durante el uso ni reproducción automática al cargar la página. El navegador reproduce los audios de entrada dentro de los gestos de activación. El segundo continúa durante el cambio de vista.

El aviso del cuestionario se incorpora mediante `audio_cuestionario.py` y `assets/aviso_tiempo.js`. Se precarga al iniciar la ronda y suena al entrar en los últimos cuatro segundos (también si una actualización salta directamente a tres). No se reinicia al enviar respuestas o actualizar el reloj; puede terminar naturalmente después de agotarse el tiempo. Una nueva ronda prepara un aviso nuevo. Si el navegador bloquea la reproducción automática, el siguiente clic o tecla dentro del plazo puede desbloquearla; no se añade un botón de sonido. No consume cuota de IA.

Para sustituirlos, conserva esos nombres y el formato, detén y reinicia el servidor. Comprueba también el volumen y los permisos de sonido del sitio. No se atribuye autoría propia ni una licencia libre a estos recursos de terceros.

Uso y arranque en el [README](../README.md) y [guía de instalación](../INSTALACION.md).
