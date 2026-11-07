# Entrega y sustentación — Archivo Omnitrix

Actualizado el 7 de noviembre de 2026. La implementación del plan de 13 pasos y sus ampliaciones está preparada. El estado de las pruebas y las comprobaciones pendientes se detalla en [VERIFICACION.md](VERIFICACION.md).

## Objetivo académico

Adaptar el taller Tribuna Global de opiniones sobre futbolistas a una aplicación de opiniones sobre aliens de Ben 10. Según lo comunicado por el estudiante, se permitió cambiar la temática. Se conservaron catálogo, asociación de opiniones, LangChain, validación estructurada, persistencia y consulta/exportación.

| Requisito conservado | Implementación |
| --- | --- |
| Catálogo de al menos 20 personajes con IDs únicos | 63 fichas locales, imágenes y metadatos; los 20 IDs iniciales permanecen. |
| Opinión asociada al personaje elegido | Selección capturada en cada envío; longitud de 5–1000 caracteres y original conservado. |
| Prompt y análisis con LangChain | `ChatPromptTemplate`, mensajes system/human, operador `|`, salida estructurada e `invoke`. |
| Cuatro sentimientos y justificación | Positivo, negativo, neutro y mixto; pertinencia y esquema Pydantic. |
| Errores y texto ajeno | Avisos visibles, sin categoría inventada ni guardado de rechazos. |
| Guardado persistente | JSON versionado, UUID/fecha, reemplazo y reintento idempotente. |
| Consulta y filtros | Alien/sentimiento combinados; tabla, recuentos y descarga de la misma selección. |
| Ejemplos y documentación | 16 opiniones manuales sobre cuatro aliens/cuatro categorías, seis casos adicionales y guías. |

La rúbrica conservada del taller distribuye: catálogo/asociación 10, prompt 20, validación/errores 15, persistencia 25, consultas/descarga 15 y pruebas/documentación/explicación 15 puntos. No se asigna una nota automática ni se sustituye la revisión del profesor.

## Ampliaciones incluidas

- Identidad visual local, símbolo en portada/sidebar/favicon y entrada de dos pulsaciones con audio.
- Inicio gráfico por doble clic en Windows; guía de arranque por terminal para Windows y Linux.
- 63 transformaciones de la continuidad clásica, con fichas y fuentes.
- 32 situaciones de combate, seguridad, rescate y conflictos creativos.
- Desafíos con Control maestro, Héroe bajo presión y Adaptabilidad.
- Tres fichas consultables antes de elegir en Héroe bajo presión.
- Cierre de ronda, resultado fijo, rejuego con otra situación y retorno al menú.

Estas ampliaciones complementan el trabajo de sentimientos y persistencia. Las partidas de desafíos permanecen en sesión; no se mezclan con las opiniones guardadas. No se añadió un modo de opiniones de otras personas.

## Material para entregar

| Material | Ubicación |
| --- | --- |
| Presentación y uso | [README](README.md) |
| Comandos Windows/Linux y configuración | [Instalación](INSTALACION.md) y [Gemini](GEMINI_GRATIS.md) |
| Arquitectura, contratos y pruebas | [Desarrollo](DESARROLLO.md) |
| Evidencia y pendientes | [Verificación](VERIFICACION.md) y `evidencias/` |
| Continuidad e historial | [Contexto](CONTEXTO_PROYECTO.md), [plan](PLAN_DESARROLLO.md) y `docs/` |
| Datos y procedencia | [Catálogo/situaciones](datos/README.md), [ejemplos](datos/ejemplos/README.md), [imágenes](assets/aliens/README.md) y [recursos visuales](assets/README.md) |

Incluye código, `requirements.txt`, `.env.example`, `.streamlit`, datos, recursos y fuentes. Excluye `.env`, secretos, `.venv`, `.python-runtime`, `.herramientas` y logs privados. Revisa si las opiniones de uso contienen datos personales antes de compartirlas. Las imágenes y audios son material de terceros/proporcionado por el usuario; conservarlos no acredita una licencia libre de redistribución.

## Recorrido sugerido de demostración

1. Abrir el VBS en Windows o arrancar Streamlit desde la terminal según la guía Linux.
2. Activar el símbolo dos veces y mostrar la continuidad de la transición sobre ambos paneles.
3. Seleccionar un alien, explicar los campos de la ficha y enviar una opinión.
4. Identificar sentimiento/razón y mostrar la confirmación de guardado.
5. Consultar el registro, aplicar filtros y descargar el JSON.
6. Reiniciar y recuperar el registro desde Consultar archivo.
7. Abrir Desafíos y presentar los tres submodos. Mostrar las fichas de las tres opciones en Héroe bajo presión y la asignación única de Adaptabilidad.
8. Evaluar una estrategia, explicar la incertidumbre de IA y mostrar las acciones finales.
9. Explicar qué se conserva en JSON, qué permanece en sesión y qué llamadas consumen cuota.
10. Detener el servidor con el controlador o Ctrl+C, según el arranque utilizado.

Si no hay acceso a Gemini, se puede demostrar catálogo y consulta de registros existentes. Las pruebas con datos manuales o el servidor visual simulado deben identificarse como tales. No presentarlas como resultados obtenidos del modelo.

## Qué explicar del código

- `analisis.py`: separación de instrucciones/datos, contratos, llamada compartida a Gemini y errores seguros.
- `almacenamiento.py`: identidad del envío, fecha UTC, reintento sin duplicación y límites de concurrencia.
- `interfaz_desafios.py`: menú, sorteo estable, asignación de 63/3/1, estado activo/terminado y nuevas rondas.
- `desafios.py`: 32 escenarios originales y evaluación contextual del plan con `desafios-v2`.
- `pantalla_inicio.py`: componente local, dos gestos para los audios y continuidad entre vistas.
- Pruebas: diferencia entre ejecutar transporte/parser/archivos reales y obtener respuestas semánticas reales de Gemini.

## Pendientes antes de declarar aceptación completa

El usuario confirmó que Gemini funciona; falta registrar una evaluación sistemática de las 16 opiniones y seis casos, con modelo/versión de prompt, respuestas y discrepancias. También debe documentarse calidad de estrategias en los tres submodos; hoy sus comprobaciones automatizadas usan evaluadores simulados.

Quedan por cerrar las evidencias manuales de envío/reapertura/descarga y cierre desde el controlador en el recorrido de entrega, y la verificación integral de la versión actual en Linux. No se identifica un lanzador gráfico Linux como implementado.

Las reflexiones sobre dos ambigüedades están en [VERIFICACION.md](VERIFICACION.md). Para presentarlas como errores observados de IA hay que ejecutar y registrar los resultados correspondientes.
