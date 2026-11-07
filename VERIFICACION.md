# Registro de aceptación — Archivo Omnitrix

Fecha: 7 de noviembre de 2026. Sistema comprobado: Windows, Python 3.14.4, Tk 8.6 y Streamlit 1.67.0.

## Actualización vigente: Gemini

Tras la solicitud de uso sin pago, se adaptó el clasificador a Gemini Developer API con `langchain-google-genai==4.4.3` y `google-genai==3.0.0`. La nueva ejecución aprobó **68 pruebas en 14,482 segundos** y `pip check` no encontró incompatibilidades. Registro en `evidencias/pruebas-gemini-windows.txt`. Las secciones de 65 pruebas más abajo conservan la ejecución anterior a este cambio.

Las pruebas de análisis pasaron de 6 a 9: comprueban que no se reutilizan claves OpenAI, que no se cambia a otro modelo, y ejecutan el adaptador Gemini y parser reales con transporte simulado. También verifican Developer API (`vertexai=False`), timeout y un solo intento (`max_retries=1`), categorías, pertinencia, cuota, credenciales y errores sin detalles privados. No hubo generación real ni consumo de cuota. El lanzador comprueba la importación de la nueva integración.

La clave del usuario y el acceso gratuito aún deben configurarse/confirmarse siguiendo `GEMINI_GRATIS.md`. No se activó facturación. La app no puede verificar por sí sola el estado de facturación del proyecto; se requiere un proyecto Free Tier sin facturación vinculada. No se garantiza disponibilidad para toda cuenta/región. El requisito de no pagar está registrado en el contexto. La prueba real y revisión manual siguen pendientes.

## Resultado observado

**65 pruebas automatizadas aprobadas, sin fallos ni omisiones**, en 14,501 segundos en la última ejecución. `pip check`: `No broken requirements found.` También pasó `tests/comprobar_inicio_windows.ps1` para los casos de archivos ausentes y presentes simulados, sin ejecutar esos archivos.

La primera ejecución encontró dos fallos: Windows aceptaba una ruta de imagen absoluta POSIX (`/tmp/fuego.png`) y una aserción esperaba que Streamlit mostrara literalmente un texto compuesto solo de espacios. Se corrigió la validación con `PurePosixPath`; la prueba del texto ahora comprueba tanto el contenido original en sesión como la presentación normalizada. La aplicación no recorta el texto almacenado.

El entorno se preparó durante esta etapa: instalación por usuario de Python en `.python-runtime`, sin modificar PATH ni asociaciones, y creación de `.venv` con las dependencias del proyecto. Descarga desde [Python.org](https://www.python.org/downloads/release/python-3144/), con SHA-256 del instalador comprobado: `b571567bd11ea98fd7a2cf85791d2c8557a63b1e04e9d1dae665a275cac87f1b`. Runtime e instalador quedan excluidos de Git.

Evidencias:

- `evidencias/pruebas-windows.txt`: salida de la suite aprobada. PowerShell presenta parte de stderr como `NativeCommandError`; la conclusión de unittest es `Ran 65 tests ... OK` y el proceso terminó con código 0.
- `evidencias/dependencias-windows.txt`: versiones instaladas, incluidas las transitivas; es una instantánea de este entorno.
- `datos/ejemplos/opiniones_demo.json`: 16 opiniones ficticias, cuatro aliens y cuatro categorías. Resultados, UUID y fechas preparados manualmente; no proceden de una API.
- `datos/ejemplos/casos_evaluacion.json`: seis casos adicionales con expectativas humanas y observaciones para evaluar un modelo real.
- `evidencias/persistencia-y-filtro.json`: reproducción ejecutada en el paso 13: 16 registros guardados y recuperados desde otro proceso, cero nuevos al reintentar y archivo de uso sin cambios.
- `evidencias/consulta-xlr8-mixto.json`: exportación real del filtro XLR8/mixto, un registro; la clasificación sigue identificada como manual.

Las dos últimas evidencias se reproducen con `.\.venv\Scripts\python.exe scripts\generar_evidencias.py`. El generador trabaja con datos manuales en un directorio temporal y no llama a una API. Su comprobación se ejecutó correctamente el 7 de noviembre de 2026; complementa la suite anterior, que no se volvió a ejecutar solo por reorganizar la documentación.

## Alcance de las pruebas

| Área | Evidencia y resultado |
| --- | --- |
| Catálogo | 19 pruebas: estructura, campos, IDs, rutas, archivos ausentes/dañados y conservación de datos. Aprobadas. |
| Contrato de análisis | 6 pruebas: cuatro categorías, pertinencia, razón, entradas inválidas, configuración ausente, respuesta inválida y errores de autenticación/cuota/tiempo. Aprobadas con dobles de modelo. |
| Filtros | 3 pruebas: combinaciones AND por ID/categoría, orden, nombres repetidos, copias y vacíos. Aprobadas. |
| Inicio | 7 pruebas: comando, salud, cierre y tiempos; además mutex real de Windows y arranque/salud/detención de un servidor Streamlit real. Aprobadas. |
| Interfaz | 19 pruebas AppTest: catálogo, imágenes, cambios de alien, entradas límite, historial, limpieza, rechazos, fallos/reintento, filtros, tabla, recuentos y bytes de descarga. Aprobadas. |
| Persistencia | 7 pruebas: escritura/lectura, UUID independientes, idempotencia, conflicto de ID, errores, JSON/UTF-8 inválidos y temporales. Aprobadas. |
| Aceptación | 4 pruebas: datos de ejemplo, lectura del archivo por otro proceso Python desde otro directorio, exportación recuperable y coherencia del corpus manual. Aprobadas. |

El servidor real iniciado por la prueba se detiene al terminar. No se llama al modelo en la suite y las escrituras de pruebas se aíslan en carpetas temporales. El archivo `datos/opiniones.json` de uso conserva su estructura vacía; los ejemplos no se incorporaron a él.

## Inicio gráfico observado

Se abrió el VBS real, apareció la ventana «Archivo Omnitrix · Inicio» con la dirección local y los botones «Abrir en navegador» y «Detener y cerrar». El endpoint de salud del servidor devolvió HTTP 200 y `ok`. Se observó una ventana Brave titulada «Archivo Omnitrix - Brave».

La revisión visual de la página se detuvo: Computer Use no pudo determinar la URL de Brave con confianza suficiente para aplicar su política. No se continuó interactuando con esa ventana. Por tanto, esto no acredita una inspección visual completa de la página, descarga real desde el navegador o clic de cierre del controlador. La suite sí verificó el contenido exportado, el mutex y el cierre de un proceso servidor real. La ventana de control abierta para la inspección puede cerrarse manualmente con «Detener y cerrar».

## Evaluación del modelo pendiente

No existe `.env` configurado en esta copia y no se eligió ni evaluó un modelo real. La aprobación de las pruebas con dobles **no demuestra** acierto semántico, resistencia efectiva a instrucciones embebidas o manejo correcto de ironía por un LLM. No se registran métricas de exactitud ficticias.

Para completar la aceptación:

1. Configurar localmente la clave y el modelo compatibles, sin compartir credenciales.
2. Evaluar las 16 opiniones y los seis casos adicionales, registrando modelo, `version_prompt`, resultado observado y discrepancias. Los esperados son referencias humanas, no resultados ya obtenidos.
3. Comprobar en la aplicación un envío real pertinente y uno ajeno, guardado, reinicio y consulta del registro. Confirmar que rechazos y fallos no se guardan.
4. Revisar visualmente tabla/filtros, descargar el JSON en el navegador y cerrar el servidor desde el controlador. Las comprobaciones automáticas complementan estas observaciones.

## Dos ambigüedades para discutir

Estas son reflexiones sobre casos preparados manualmente, no errores observados de un modelo:

- **Querer más apariciones de XLR8:** «Me encanta su velocidad y su diseño, pero siento que podría aparecer más». La referencia es mixta por el elogio y la inconformidad; una lectura positiva puede interpretar el deseo de más presencia como entusiasmo. Debe registrarse la discrepancia sin tratar la referencia humana como una verdad absoluta.
- **Ironía frente a elogio literal:** «Sí, claro, XLR8 es rapidísimo... justo por eso sus escenas se me hacen eternas de lo aburridas que son». La referencia es negativa por la crítica explícita a las escenas. Contar automáticamente «rapidísimo» como elogio puede generar un mixto injustificado; el análisis debe valorar el comentario completo sin inventar episodios o intenciones.

## Reproducción técnica

Desde la raíz, con el entorno preparado:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip check
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests\comprobar_inicio_windows.ps1
```

La etapa 12 tiene datos y verificación local preparados; permanece abierta hasta realizar la evaluación de API y la revisión manual pendientes.

La documentación del paso 13 está preparada en el README, el contexto vigente y `ENTREGA.md`. Los documentos anteriores se conservaron en `docs/` como archivos históricos. El cierre documental no equivale a aceptar las comprobaciones pendientes anteriores.

Comprobación documental realizada: 10 documentos y 41 enlaces locales sin destinos ausentes; JSON exportado validado mediante `cargar_opiniones` y contrastado con el resumen de persistencia/filtro. `git diff --check` correcto, con avisos de normalización LF/CRLF de Git en Windows, sin errores de espacios. Se conservaron los cambios existentes del paso 12 y no se ejecutaron commits ni push.
