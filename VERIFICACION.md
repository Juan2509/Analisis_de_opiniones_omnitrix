# Verificación y límites de la entrega

Estado consolidado el 7 de noviembre de 2026. El [registro histórico](docs/VERIFICACION_HISTORICA.md) conserva resultados intermedios y detalles anteriores. Los comandos actuales están en [DESARROLLO.md](DESARROLLO.md).

## Resumen vigente

Interpretación alienígena: **118 pruebas aprobadas** en Windows, 123,126 s ([registro](evidencias/pruebas-interpretacion-windows.txt)), incluidas 11 nuevas de banco/sorteo, entradas y salidas, adaptador real con transporte interceptado, menús, edición/revisión, conservación al navegar, resultado fijo, rejuego y error/reintento. Tras ajustar los botones para poder continuar sin desenfocar manualmente el campo, las 11 del módulo volvieron a pasar en 24,378 s (salida observada sin log adicional). No se consumió cuota de IA; queda pendiente comprobar la calidad de interpretaciones reales, incluida la cautela ante datos vagos o contradictorios. [Uso y límites](datos/INTERPRETACION.md).

Navegador de interpretación: cuatro recorridos aprobados (dos submodos, escritorio 1440×1000 y móvil 390×1000), con servidor visual simulado identificado. Se comprobaron selección/Iniciar, favorito y motivos, seis respuestas, navegación anterior con texto conservado, revisión, resultado e imagen decodificada, alternativa y retorno al menú; sin desbordamiento, errores JavaScript ni peticiones externas. Se inspeccionaron capturas de resultado de escritorio y revisión móvil. [Registro](evidencias/navegador-interpretacion.json). Los módulos auxiliares requirieron reiniciar el servidor visual tras el ajuste del formulario.

Umbral vigente: **cuatro segundos**, por petición posterior del usuario. La prueba aislada del renderer verifica silencio a cinco, reproducción única a cuatro, salto a tres, rejuego y desbloqueo por gesto. Las comprobaciones de umbrales anteriores que siguen se conservan como historial.

Umbral del aviso ajustado posteriormente de cinco a **tres segundos**. La prueba `node tests/verificar_aviso_tiempo.cjs` comprueba silencio a cinco/cuatro, reproducción única a tres, salto a dos, rejuego y desbloqueo por gesto. El registro de navegador del párrafo siguiente corresponde a la versión anterior de cinco segundos; no se presenta como una nueva ejecución del umbral de tres.

Aviso de cinco segundos: las 16 pruebas del cuestionario pasaron en 17,560 s tras conectar el audio (salida observada, sin log adicional). `node tests/verificar_aviso_tiempo.cjs` comprobó ausencia de sonido antes del umbral, reproducción única entre ticks/remontajes, salto a cuatro segundos, nueva ronda y desbloqueo por gesto. En navegador se comprobaron dos rondas por pantalla (1440 y 390 píxeles), con la llamada de reproducción interceptada: aviso en los últimos cinco segundos, ninguna repetición al enviar y otro aviso al rejugar; cero errores JS y solicitudes externas ([registro](evidencias/navegador-aviso-tiempo.json)). No se comprobó volumen físico ni permisos de sonido de cada navegador; no hubo consultas a IA.

Corrección del fallo genérico al evaluar Nombres: **107 pruebas aprobadas** en Windows, 88,987 s ([registro](evidencias/pruebas-correccion-evaluacion-conocimiento-windows.txt)). El cuestionario usa ahora un esquema de transporte explícito sencillo y mantiene la validación estricta local; `conocimiento-v2` pide textos más breves. Tres pruebas nuevas ejercitan el adaptador Gemini instalado con transporte interceptado: 63 correcciones completas, corte por tokens/JSON inválido/longitud inválida y error HTTP 400 convertido por LangChain. Se conservan una solicitud por evaluación y reintentos manuales, sin exponer respuestas privadas. La excepción original del usuario no se registró y no pudo reproducirse con una respuesta simulada válida: la causa concreta y la resolución del caso real siguen pendientes de confirmar al probar con Gemini. No se consumió cuota ni se cambiaron credenciales/modelo/facturación.

Conocimiento alienígena: **104 pruebas aprobadas** en Windows, 119,213 s ([salida](evidencias/pruebas-conocimiento-windows.txt)). Son las 91 anteriores más 13 del cuestionario: categorías, especies elegibles, alias enviados como contexto, contrato/IDs, puntuación, menú, respuestas escritas, plazo, navegación, cierre, reintento explícito y conservación de resultados sin duplicar llamadas. Se prueba la integración LangChain con transporte simulado; no se gastó cuota ni se acredita precisión semántica real de Gemini. Reglas y límites en [datos/CONOCIMIENTO.md](datos/CONOCIMIENTO.md).

Ajuste posterior: un envío vacío muestra el aviso y conserva disponible Terminar ronda. Las 13 pruebas del cuestionario volvieron a pasar en 17,275 s, incluida esa comprobación; salida observada durante el desarrollo, sin un log permanente adicional. No se repitió toda la suite por ese ajuste del formulario.

Navegador del cuestionario: **ocho recorridos aprobados**, las cuatro categorías en escritorio 1440×1000 y móvil 390×844. Se verificaron selección antes de Iniciar, imagen cargada sin revelar nombre/especie, reloj con actualizaciones reales, borrador e imagen conservados entre ticks, envío escrito, cierre, revisión simulada, rejuego y menú. En General se adelantó el reloj del servidor exclusivo de prueba para comprobar el cierre por plazo sin esperar un minuto. Sin errores JavaScript, peticiones externas ni llamadas a IA. Se inspeccionaron capturas de pregunta/resultados; [registro](evidencias/navegador-conocimiento.json). El test espera al desmontaje del formulario antes de pulsar el menú para evitar clics sobre controles antiguos durante una reejecución.

Especies: **91 pruebas aprobadas** en Windows, 72,562 s, con servicios de IA simulados y archivos temporales ([salida completa](evidencias/pruebas-especies-windows.txt)). Incluye las 63 selecciones de ficha, nuevos estados/fuentes y compatibilidad con catálogos v1 anteriores. Las 63 fichas conservan todos sus datos previos y añaden 55 especies identificadas, siete sin nombre confirmado y un híbrido ([auditoría](evidencias/catalogo-especies.json)). Comprobación en navegador de Nanomech/Atomix en escritorio y móvil, con fuentes visibles, sin errores JavaScript ni peticiones externas; capturas inspeccionadas ([registro](evidencias/navegador-especies.json)). Las pruebas validan los datos y la presentación; la justificación editorial y sus límites están en [la investigación](datos/ESPECIES.md).

Fondo ambiental: tres casos aprobados (escritorio, móvil y movimiento reducido), con movimiento real comprobado por cambios en las transformaciones CSS, capas sin eventos y detrás del contenido, ausencia de desbordamiento, imágenes decodificadas, selección de Diamante y acceso al menú de desafíos. En movimiento reducido las animaciones se detienen; móvil muestra una sola capa. Sin errores JavaScript, peticiones externas ni consultas a IA. [Registro del fondo](evidencias/navegador-fondo.json).

La entrada se volvió a comprobar con el fondo en cinco casos: clic, Enter, móvil, movimiento reducido y audio bloqueado. Se conservaron sonidos/transición/cobertura del sidebar, título desde arriba tras una espera y desplazamiento manual posterior. Se ajustó la espera de finalización de Streamlit y la confirmación de posición al retirar el verde para estabilizar la entrada móvil. [Registro de entrada con fondo](evidencias/navegador-inicio-con-fondo.json). Se inspeccionaron capturas de escritorio y móvil.

Corrección posterior de posición inicial: cinco casos del navegador aprobados (clic, Enter, móvil, movimiento reducido y primer audio bloqueado). Al terminar la entrada se comprobó desplazamiento principal en cero, título visible tras una espera y desplazamiento manual posterior operativo. Sin errores JavaScript, peticiones externas ni consultas al modelo. [Registro de posición inicial](evidencias/navegador-inicio-posicion.json). Se inspeccionó la captura del dashboard desde arriba.

| Comprobación | Resultado y alcance |
| --- | --- |
| Última suite completa archivada | **118 pruebas aprobadas** en Windows, 123,126 s. [Salida](evidencias/pruebas-interpretacion-windows.txt). |
| Fichas comparables posteriores | 15 pruebas del juego y 20 de interfaz aprobadas; correspondencia de las tres pestañas, imagen y habilidades. Revisión de escritorio/móvil correcta. Salidas observadas durante el desarrollo, sin un archivo adicional de log permanente. |
| Ampliación posterior de situaciones | 15 pruebas del juego aprobadas, 33,647 s; 32 situaciones válidas, IDs/títulos únicos y las 12 originales intactas. Salida observada durante el desarrollo, sin log permanente adicional. |
| Catálogo | 63 fichas/PNG; hashes, dimensiones y correspondencia revisados; los 20 registros originales conservados. [Suite de ampliación](evidencias/pruebas-catalogo-ampliado-windows.txt). |
| Rondas en navegador | Tres submodos en escritorio 1440×1000 y móvil 390×844: evaluación, cierre, rejuego y menú correctos, con evaluador simulado. [Registro](evidencias/navegador-rondas-adaptabilidad.json). |
| Entrada audiovisual | Dos gestos, audio local, transición uniforme y cobertura del sidebar comprobados. [Registro de audio](evidencias/navegador-inicio-audio.json). |
| Persistencia/filtro | Archivos temporales y lectura desde otro proceso; reintento sin duplicaciones y exportación coherente. [Resumen](evidencias/persistencia-y-filtro.json). |
| Gemini real | El usuario confirmó que funciona. No se dispone de una evaluación sistemática archivada de exactitud ni de calidad de estrategias. |
| Linux actual | Procedimiento de instalación/arranque documentado y núcleo con rutas portables; verificación integral en Linux pendiente. El lanzador usa APIs Windows. |

Las suites históricas de 87 y 91 pruebas corresponden a las rondas de desafíos y la incorporación de especies, respectivamente. La ejecución de 104 incluye el cuestionario; no sustituye las comprobaciones visuales específicas de cada efecto ni una evaluación semántica real de Gemini.

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
