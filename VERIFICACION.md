# Verificación y límites de la entrega

Estado consolidado el 7 de noviembre de 2026. El [registro histórico](docs/VERIFICACION_HISTORICA.md) conserva resultados intermedios y detalles anteriores. Los comandos actuales están en [DESARROLLO.md](DESARROLLO.md).

## Resumen vigente

| Comprobación | Resultado y alcance |
| --- | --- |
| Última suite completa archivada | **87 pruebas aprobadas** en Windows, 95,726 s. [Salida](evidencias/pruebas-rondas-adaptabilidad-windows.txt). |
| Fichas comparables posteriores | 15 pruebas del juego y 20 de interfaz aprobadas; correspondencia de las tres pestañas, imagen y habilidades. Revisión de escritorio/móvil correcta. Salidas observadas durante el desarrollo, sin un archivo adicional de log permanente. |
| Ampliación posterior de situaciones | 15 pruebas del juego aprobadas, 33,647 s; 32 situaciones válidas, IDs/títulos únicos y las 12 originales intactas. Salida observada durante el desarrollo, sin log permanente adicional. |
| Catálogo | 63 fichas/PNG; hashes, dimensiones y correspondencia revisados; los 20 registros originales conservados. [Suite de ampliación](evidencias/pruebas-catalogo-ampliado-windows.txt). |
| Rondas en navegador | Tres submodos en escritorio 1440×1000 y móvil 390×844: evaluación, cierre, rejuego y menú correctos, con evaluador simulado. [Registro](evidencias/navegador-rondas-adaptabilidad.json). |
| Entrada audiovisual | Dos gestos, audio local, transición uniforme y cobertura del sidebar comprobados. [Registro de audio](evidencias/navegador-inicio-audio.json). |
| Persistencia/filtro | Archivos temporales y lectura desde otro proceso; reintento sin duplicaciones y exportación coherente. [Resumen](evidencias/persistencia-y-filtro.json). |
| Gemini real | El usuario confirmó que funciona. No se dispone de una evaluación sistemática archivada de exactitud ni de calidad de estrategias. |
| Linux actual | Procedimiento de instalación/arranque documentado y núcleo con rutas portables; verificación integral en Linux pendiente. El lanzador usa APIs Windows. |

La suite completa de 87 es anterior a los ajustes de fichas y al banco de 32 situaciones. Las comprobaciones posteriores indicadas cubren esos cambios; no se presenta el log de 87 como una nueva ejecución de todo el estado actual. Esta consolidación documental no volvió a ejecutar toda la aplicación solo para reescribir guías.

## Entorno comprobado

Windows, Python 3.14.4, Tk 8.6 y Streamlit 1.67.0. Las versiones directas y sus marcadores están en `requirements.txt`; el último `pip check` registrado no encontró incompatibilidades. La [instantánea Windows](evidencias/dependencias-windows.txt) conserva las transitivas de aquel entorno y no equivale a una instalación Linux verificada.

La rama histórica de Streamlit 1.65.0/Python 3.10 no ha recibido una verificación integral de todas las ampliaciones actuales. La instalación nueva se documenta con Python 3.11+ compatible con las versiones fijadas.

## Qué verifican las pruebas

- Catálogo: esquema, campos, IDs, rutas locales, contenido y lectura independiente del directorio de inicio.
- Recursos/interfaz: imágenes ausentes o dañadas, manifiestos/hashes, navegación, selección, historial y fichas de las tres opciones.
- Opiniones: validación de longitud, captura del alien, pertinencia, categorías, razón y manejo de errores sin resultados ficticios.
- Gemini: adaptador/parser reales con transporte simulado, Developer API, timeout, un intento y ausencia de fallback.
- Persistencia: JSON/UTF-8, IDs y conflictos, guardado/lectura, idempotencia, temporales y recuperación desde otro proceso.
- Consulta: filtros combinados, tabla, recuentos y bytes de descarga coherentes.
- Inicio: comandos, salud/cierre de servidor real y mutex Windows; diagnóstico VBS/PowerShell según los registros anteriores.
- Desafíos: banco local, azar sin repetición inmediata, 63/3/1 opciones, elección/inicio explícitos, asignación fija, estrategia requerida en Adaptabilidad y modo enviado al evaluador.
- Rondas: ausencia de salto de situación, resultado fijo tras éxito, formulario conservado ante error, rejuego limpio y retorno al menú.

Las escrituras de pruebas se aíslan y no se consumen llamadas reales a Gemini. Los scripts de navegador usan perfiles temporales. El servidor `tests/app_desafios_visual.py` sustituye el evaluador por una respuesta rotulada como simulada y es exclusivo de pruebas; `app.py` conserva el proveedor real.

## Qué no demuestran

Una respuesta simulada correcta no acredita que Gemini detecte siempre ironía, resista instrucciones incrustadas o evalúe justamente todas las estrategias. Un parser validado solo demuestra forma/contrato, no verdad de lo generado. Las misiones son ficción y no una simulación física de resultados.

La prueba automática de los bytes exportados no sustituye una evidencia manual completa de descarga desde el navegador. La detención automática de un proceso servidor no equivale por sí sola a haber pulsado y observado el cierre del controlador en el recorrido final de entrega.

El bloqueo anterior de una inspección de Brave por Computer Use pertenece al historial. Posteriormente hubo revisiones de navegador independientes en escritorio/móvil; esa limitación histórica ya no debe presentarse como ausencia total de revisión visual.

## Evidencias conservadas

| Registro | Etapa |
| --- | --- |
| [65 pruebas](evidencias/pruebas-windows.txt) | Antes de la migración a Gemini. |
| [68 pruebas](evidencias/pruebas-gemini-windows.txt) | Integración Gemini. |
| [71 pruebas](evidencias/pruebas-inicio-windows.txt) | Entrada de activación. |
| [72 pruebas](evidencias/pruebas-catalogo-ampliado-windows.txt) | Catálogo de 63 fichas. |
| [82 pruebas](evidencias/pruebas-desafios-windows.txt) | Modo de desafíos inicial. |
| [85 pruebas](evidencias/pruebas-submodos-windows.txt) | Dos submodos y menú. |
| [87 pruebas](evidencias/pruebas-rondas-adaptabilidad-windows.txt) | Cierre por rondas y Adaptabilidad. |
| [Navegador inicial](evidencias/navegador-inicio.json) y [audio](evidencias/navegador-inicio-audio.json) | Entrada visual y evolución de sus sonidos. |
| [Desafíos iniciales](evidencias/navegador-desafios.json) y [dos submodos](evidencias/navegador-submodos.json) | Flujos anteriores al cierre por rondas. |
| [Rondas y Adaptabilidad](evidencias/navegador-rondas-adaptabilidad.json) | Seis recorridos con evaluación simulada. |
| [Persistencia/filtro](evidencias/persistencia-y-filtro.json) y [JSON exportado](evidencias/consulta-xlr8-mixto.json) | Ejemplos humanos guardados/consultados en procesos reales. |

Los 16 ejemplos de `datos/ejemplos/opiniones_demo.json` y los seis casos de `casos_evaluacion.json` contienen referencias humanas. Los campos `modelo: manual:no-ejecutado` identifican los ejemplos como manuales. No se incorporan automáticamente al archivo de opiniones de uso ni son métricas obtenidas de IA.

Las capturas y herramientas temporales de algunas revisiones permanecen en `.herramientas/browser-check/`, carpeta excluida de Git. No deben describirse como archivos de entrega si no se incorporan deliberadamente sin datos privados.

## Evaluación real pendiente

1. Registrar modelo y versión de prompt de cada prueba, sin claves.
2. Ejecutar las 16 opiniones y seis casos de referencia: cuatro categorías, ambigüedad, ironía, texto ajeno e instrucciones incrustadas.
3. Guardar resultados observados y discutir discrepancias; no asumir que la referencia humana es infalible.
4. Evaluar estrategias en Control maestro, Héroe bajo presión y Adaptabilidad, incluyendo opciones creativas y poco adecuadas.
5. Comprobar envío pertinente/ajeno, guardado, cierre/reapertura, recuperación, filtros, descarga y cierre del controlador en el recorrido de entrega.
6. Ejecutar instalación, pruebas y uso real de la versión actual en Linux; documentar distribución, Python, dependencias y cualquier fallo. No marcar el lanzador gráfico como portable.

## Dos ambigüedades para discutir

Son reflexiones preparadas, no errores observados y medidos de Gemini:

- **Querer más apariciones de XLR8:** «Me encanta su velocidad y su diseño, pero siento que podría aparecer más». La referencia mixta interpreta elogio e inconformidad; una lectura positiva puede entender la segunda parte como entusiasmo por el personaje. Registrar ambas interpretaciones si el modelo discrepa.
- **Ironía frente a elogio literal:** «Sí, claro, XLR8 es rapidísimo... justo por eso sus escenas se me hacen eternas de lo aburridas que son». La referencia negativa valora la crítica del comentario completo; contar automáticamente «rapidísimo» como elogio podría generar un mixto injustificado.

## Revisión documental de esta actualización

Se consolidaron README, instalación Windows/Linux, arquitectura, entrega, contexto, plan y guía Gemini; los registros anteriores se archivaron con enlaces ajustados. La validación documental comprueba destinos locales, referencias de archivos y coherencia de recuentos contra los JSON. No representa una ejecución de los comandos Linux ni una evaluación del proveedor.

Resultado de esa revisión en [revision-documentacion.json](evidencias/revision-documentacion.json): documentos y enlaces locales sin destinos ausentes, 63 imágenes del catálogo presentes y 32 situaciones. Los ejemplos PowerShell se revisaron sintácticamente; los comandos Linux se contrastaron con documentación oficial y permanecen sin ejecución en este equipo Windows.
