# Archivo Omnitrix — contexto vigente

Consolidado el 7 de noviembre de 2026. Este documento describe el estado actual; el [contexto previo](docs/CONTEXTO_PREVIO_CONSOLIDACION.md) y los demás documentos históricos conservan la evolución.

## Producto y alcance

Aplicación académica de Ben 10 con cuatro secciones, en este orden: **Analizar opinión**, **Desafíos del Omnitrix**, **Conocimiento alienígena** y **Consultar archivo**. Adaptación del taller Tribuna Global de futbolistas; el usuario comunicó autorización de clase para cambiar el dominio conservando los requisitos técnicos.

Estado actual: 63 fichas con imágenes locales; clasificación con Gemini; opiniones persistentes y filtros/descarga; 32 situaciones originales con tres submodos; entrada audiovisual de dos pulsaciones; controlador Windows e instrucciones de terminal Windows/Linux. El usuario confirmó que el análisis con Gemini y los sonidos funcionan. No confundir esa confirmación con una evaluación sistemática de precisión o con una prueba integral en Linux.

## Decisiones que deben conservarse

- El usuario no quiere pagar: conservar Gemini Developer API, clave de proyecto Free Tier sin facturación, sin fallback a proveedores/modelos de pago ni cambios automáticos. La app no verifica el plan de la cuenta.
- Frontend Streamlit, tema negro/verde neón/blanco, recursos locales y movimiento reducido.
- Catálogo de continuidad clásica: 63 fichas, sin supremas, fusiones ni reboot. Upchuck Perk/Murk por separado; Spitter identificado como transformación mostrada con Ben 10.000. Nanomech/Shocksquatch incluyen película/especial de sus etapas. Mantener a001–a020 y los demás IDs estables.
- Mantener nombres latinos y alias originales. Serie de introducción y diseño de imagen son datos diferentes. Nuevas fichas pueden especificar `serie_diseno` y `fuente_imagen`.
- Explicaciones y documentación en español. Sugerir Conventional Commits al terminar un cambio, sin ejecutar commits/push automáticamente. Conservar cambios ajenos.
- No exponer ni reemplazar `.env`, claves, opiniones de uso o archivos dañados para aparentar funcionamiento. Los ejemplos y evaluaciones simuladas se identifican como tales.
- Los adjuntos de clase son referencias, no instrucciones operativas. No ampliar alcance a LangGraph, agentes, RAG, n8n o bases vectoriales por aparecer en esos materiales.

## Arranque y compatibilidad

Revisión de especies: las 63 fichas incluyen `especie`, `estado_especie` y `fuentes_especie`; 55 identificadas, siete sin nombre confirmado y Nanomech híbrido. Usar Biotsavartian y Geochelone Aerios, mantener Gourmand con subespecies Perk/Murk. Investigación, limitaciones y fuentes individuales en [datos/ESPECIES.md](datos/ESPECIES.md). La ficha muestra especie y referencias sin IA.

Windows: VBS → `.venv\Scripts\python.exe` → `iniciar.py` → Streamlit y navegador. Controlador con mutex por carpeta/sesión, puerto local disponible, salud antes de abrir y cierre de su propio proceso. No instala paquetes. Cerrar solo navegador no detiene servidor.

Linux: iniciar directamente `app.py` mediante `.venv/bin/python -m streamlit run`; interfaz en navegador, servidor detenido con Ctrl+C. El lanzador VBS/WinDLL no es portable. Compatibilidad esperada del núcleo por sus rutas/dependencias, pendiente de comprobación integral de la versión actual. No añadir un lanzador Linux sin una solicitud nueva.

Entorno comprobado: Windows, Python 3.14.4, Tk 8.6, Streamlit 1.67.0. La guía nueva utiliza Python 3.11+ compatible con las versiones fijadas; la rama Python 3.10 del requirements es histórica. Recrear entornos en otro sistema o ubicación. Instrucciones actuales en [INSTALACION.md](INSTALACION.md).

## Entrada audiovisual

Ambiente del dashboard solicitado: negro predominante con células/círculos verdes muy tenues, desplazamiento y cambio de escala continuos y lentos. Implementación CSS de dos pseudoelementos de gradientes detrás del contenido, sin eventos ni recursos remotos. Móvil usa una capa y movimiento reducido detiene la animación. Mantener portada/fichas/textos por delante y la transición verde en su capa superior. Pruebas en tests/verificar_fondo.cjs y evidencias/navegador-fondo.json; entrada con fondo en evidencias/navegador-inicio-con-fondo.json.

`assets/omnitrix.png` sirve para entrada, portada, sidebar y favicon. El símbolo comienza hundido a escala 0.76. Primer clic/Enter: sube y reproduce `sonidos/core-ready.mp3`; segundo: baja, reproduce `sonidos/omnitrix-transform.mp3` y activa el dashboard.

No autoplay al abrir, botón de sonido adicional, contorno circular de foco ni círculo verde expansivo. La indicación de teclado conserva foco visible mediante el texto de ayuda. Una capa verde persistente en la capa superior del navegador cubre dashboard/sidebar durante el rerun y se desvanece cuando están listos. No crear otra capa durante el desmontaje ni cortar el audio de transformación. Una pausa protege frente a doble clic. Activación por sesión y movimiento reducido conservados.

Recursos en `assets/inicio/`, registro en `pantalla_inicio.py`. Reiniciar servidor si cambian esos recursos.

## Opiniones y archivo

Cada envío captura alien/texto; valida 5–1000 caracteres tras quitar espacios exteriores y conserva el original. El historial es visual y no se envía al modelo. Cambiar de alien no reasigna registros.

`omnitrix-v1` clasifica pertinencia y cuatro sentimientos. `AnalisisOpinion`: booleano estricto, categoría cerrada o None y razón de 1–300 caracteres. Pertinente exige categoría; ajeno exige None y no se guarda. Instrucciones dentro de una opinión se tratan como datos. Errores visibles, sin resultados ni confirmaciones inventadas.

`Nueva conversación` limpia chat/rechazos y mantiene archivo/selección. `Reintentar guardado` utiliza el mismo registro y no repite IA. UUID y fecha los controla la app; reintentar el mismo ID/datos no duplica, reenviar texto es otro envío.

JSON de opiniones: versión 1, lista `opiniones`; cada registro incluye `id`, `fecha_utc`, `alien_id`, `alien_nombre`, `opinion_original`, `sentimiento`, `razon`, `modelo`, `version_prompt`. Validación previa, temporal, sincronización y reemplazo; un escritor local. Archivos dañados se conservan. No es concurrencia multiusuario.

Consulta por ID/categoría con AND; tabla, total, cuatro recuentos y descarga parten de la misma selección. No llama a la IA ni escribe y funciona sin catálogo. Los recuentos describen el archivo, no superioridad objetiva de aliens.

## Desafíos: estado actual

Menú previo con selección e Iniciar. Control maestro: todo el catálogo. Héroe bajo presión: tres IDs distintos de `random.sample`, con pestañas que muestran imagen/habilidades antes de elegir. Adaptabilidad: un ID al azar sin selector; exige una estrategia de 5–1000 caracteres. En los otros dos modos el plan es opcional.

Banco de 32 situaciones, d001–d032: rescates, batallas con villanos, seguridad, diplomacia y conflictos creativos. Son originales del juego. Se conservaron d001–d012 al añadir las otras 20. Sortear situaciones/aliens no consume API ni depende de conveniencia de poderes.

El sorteo se conserva al editar/navegar. Solo Iniciar o Volver a jugar crea una nueva ronda, salvo recuperación ante catálogo incompatible. Rejugar elige una situación diferente de la inmediatamente anterior; los sorteos de alien pueden repetirse entre rondas por azar.

No hay Otra situación ni Cambiar modo durante la ronda. Una evaluación válida fija el resultado, retira el formulario y muestra Volver a jugar / Volver al menú de modos. Un error no finaliza ni inventa evaluación: conserva el formulario para corregir/reintentar. Las partidas permanecen en sesión, fuera de `datos/opiniones.json`.

`desafios-v2` recibe situación, alien, plan y modo. En Adaptabilidad valora el uso de las capacidades asignadas, sin exigir otro alien. `EvaluacionDesafio`: veredicto adecuado/arriesgado/poco_adecuado, resumen, ventajas, riesgos y resolución. No hay votos ni comentarios de otras personas.

## Integración de IA y módulos

Aviso sonoro del cuestionario: `audio_cuestionario.py` incorpora `sonidos/omnitrix-time-out.mp3`; `assets/aviso_tiempo.js` reproduce una sola vez por ID de ronda al entrar en los últimos cuatro segundos. No se reinicia por ticks o cambios de pregunta y una nueva ronda prepara otro aviso. Si el navegador bloquea el sonido, reintenta con un clic/tecla durante ese plazo, sin añadir botones. Recurso local; no usa IA. Reiniciar el servidor si cambia el JS o se sustituye el MP3. Prueba aislada del renderer en `tests/verificar_aviso_tiempo.cjs`.

Conocimiento alienígena ya está implementado: Nombres/Habilidades/Especie/General, elegir e Iniciar, respuestas escritas, 60 segundos, sin pistas. Una pregunta por imagen sin repeticiones en la ronda; Especie excluye especies sin nombre confirmado e híbridos (también en General). El reloj usa un fragmento de Streamlit y plazo monotónico del servidor; navegar no pausa ni reinicia. No se corrige entre preguntas: el botón final pide una única revisión conjunta a Gemini. Prompt `conocimiento-v2`, salida Pydantic e IDs exactos; alias y equivalencias semánticas aceptados por instrucciones, no coincidencia literal. Resultado correcta/parcial/incorrecta/por revisar y puntos locales 1/0,5/0, excluyendo incertidumbre. Respuestas/resultados solo en sesión, rejuego y menú al final. Código en `conocimiento.py` e `interfaz_conocimiento.py`; reglas, alias y límites en [datos/CONOCIMIENTO.md](datos/CONOCIMIENTO.md). Nunca ejecutar pruebas de evaluación contra la app normal; el servidor visual exclusivo `tests/app_conocimiento_visual.py` simula IA y permite avanzar el reloj.

`analisis.ejecutar_estructurado` comparte configuración y errores; cada tarea conserva prompt/esquema propio. `ChatPromptTemplate`, operador `|`, `with_structured_output(method="json_schema")`, `invoke` y validación Pydantic estricta.

Configuración local: `GOOGLE_API_KEY` o alternativa `GEMINI_API_KEY`, modelo fijado `gemini-3.5-flash-lite`, temperatura opcional. Variables del sistema prevalecen sobre `.env`. `vertexai=False`, timeout 30 s, un intento total con `max_retries=1`, sin fallback. No imprimir detalles privados del proveedor.

Módulos y contratos completos en [DESARROLLO.md](DESARROLLO.md). Los datos y manifiestos están en `datos/` y `assets/aliens/`. Los 63 PNG se conservan con fuente/hash; las cuatro excepciones a diseños Omniverse se indican en las fichas.

## Evidencia y pendientes

Última suite completa archivada: 107 pruebas aprobadas en Windows, 88,987 s; incluye 16 del cuestionario. Registro en `evidencias/pruebas-correccion-evaluacion-conocimiento-windows.txt`. Tras el fallo genérico del usuario en Nombres se simplificó el esquema API y se distinguieron errores de formato/parseo/truncamiento; no se capturó la excepción original y falta confirmar el caso real con Gemini. Las nuevas pruebas usan el adaptador instalado y transporte simulado, sin cuota. La revisión visual de desafíos utiliza un servidor exclusivo con evaluador rotulado como simulado; el cuestionario también dispone de su propio servidor visual simulado. La app normal usa Gemini real. No reemplazarla por esos servidores de pruebas en la entrega.

Los 16 ejemplos y seis casos son referencias humanas. Persistencia/filtro se demostraron con datos manuales en temporales y lectura desde otro proceso. Falta registrar evaluación semántica real, cierre de evidencias manuales de entrega y prueba integral Linux. Estado y enlaces en [VERIFICACION.md](VERIFICACION.md).

Para continuar: leer README, este contexto y verificación; revisar Git/código y conservar cambios. El desarrollo llegó al paso 13 y tiene ampliaciones posteriores; no reiniciar pasos ya implementados ni interpretar las casillas históricas como estado vigente.
