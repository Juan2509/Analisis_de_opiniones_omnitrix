# Recursos visuales de la aplicación

La entrada utiliza dos pulsaciones: primero levanta el símbolo y reproduce el audio de preparación; después lo presiona y reproduce la transformación. La capa verde cubre dashboard y sidebar y evita el corte entre vistas. Los audios y sus momentos de reproducción se describen en [sonidos](../sonidos/README.md). El foco de teclado no dibuja un contorno circular alrededor de la imagen.

La pantalla inicial reutiliza `omnitrix.png`. Sus recursos locales están en `inicio/`: HTML, CSS y JavaScript. El símbolo empieza hundido; el primer clic o Enter lo levanta y reproduce `sonidos/core-ready.mp3`. La segunda pulsación lo hunde y reproduce `sonidos/omnitrix-transform.mp3`, que continúa durante el cambio de vista. No se usa autoplay ni un botón de sonido adicional. `pantalla_inicio.py` conserva la activación durante la sesión e incorpora los dos MP3 locales. La capa verde cubre tanto el panel lateral como el área central. Respeta la preferencia de movimiento reducido.

`omnitrix.png` es la imagen del símbolo proporcionada por el usuario para la portada «El universo está en tus manos». Se guardó localmente sin alterar sus píxeles, proporciones o transparencia. La aplicación la incorpora como imagen PNG embebida; no necesita descargarla durante el uso.

La misma imagen se usa en la marca de la barra lateral, a 48 × 48 píxeles sin deformación, y como icono de pestaña mediante `st.set_page_config(page_icon=...)`. Sustituye el carácter decorativo y el emoji verde anteriores.

La imagen sustituye el emblema geométrico anterior y su órbita. En pantallas pequeñas se presenta completa debajo del texto, sin recortes. Su procedencia está en `omnitrix-fuente.json`; no se atribuye autoría propia ni una licencia libre no comprobada.

Las imágenes de los personajes conservan sus [créditos y manifiesto](aliens/README.md).
