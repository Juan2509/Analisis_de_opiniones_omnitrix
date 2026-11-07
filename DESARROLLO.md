# Desarrollo y arquitectura

Estado documentado: 7 de noviembre de 2026. Instalación y arranque en [INSTALACION.md](INSTALACION.md); uso en el [README](README.md).

## Organización

| Módulo | Responsabilidad |
| --- | --- |
| `app.py` | Navegación, fichas reutilizables, chat, guardado desde la interfaz y consulta/exportación. |
| `analisis.py` | Configuración Gemini, transporte compartido, prompt de sentimientos y validación de resultados. |
| `almacenamiento.py` | Validación de catálogo y registros, UUID/fecha, JSON persistente y filtros. |
| `desafios.py` | Banco de situaciones, sorteo y contrato/prompt de evaluación de estrategias. |
| `interfaz_desafios.py` | Menú de submodos, asignaciones, formulario, cierre de ronda y rejuego. |
| `conocimiento.py` | Preguntas por categoría, alias, prompt/esquema de corrección y puntuación local. |
| `interfaz_conocimiento.py` | Menú, ronda escrita de 60 segundos, reloj independiente y revisión final. |
| `interpretacion.py` | Banco de 30 preguntas, sorteo de seis temas, prompt y contrato de afinidad simbólica. |
| `interfaz_interpretacion.py` | Submodos favorito/afinidad, navegación editable, revisión y resultado de sesión. |
| `audio_cuestionario.py` y `assets/aviso_tiempo.js` | Audio local de los últimos cuatro segundos; deduplicación por ronda en el documento. |
| `pantalla_inicio.py` | Componente Streamlit v2 con imagen/audio embebidos y activación de sesión. |
| `assets/inicio/` | HTML, CSS y JavaScript de las dos pulsaciones y la transición. |
| `iniciar.py` y `Iniciar Archivo Omnitrix.vbs` | Arranque gráfico, servidor y cierre en Windows. |
| `tests/` | Pruebas unitarias, de integración, interfaz y revisiones de navegador. |

Streamlit ejecuta Python en el servidor local y presenta la interfaz en el navegador. Las reejecuciones no deben volver a consultar el modelo ni guardar datos sin una acción explícita del usuario. Las rutas de datos/recursos se resuelven desde el proyecto; el arranque desde la raíz permite cargar también el tema `.streamlit`.

## Dependencias

Las versiones directas están en `requirements.txt`: Streamlit 1.67.0 para Python 3.11+, LangChain Core 1.7.6, integración Google 4.4.3, python-dotenv 1.2.4, Pydantic 2.14.3 y Pillow 12.3.0. El archivo conserva Streamlit 1.65.0 para Python 3.10 como rama histórica, sin una nueva validación integral de las últimas ampliaciones en esa rama.

La instantánea de versiones instaladas está en [dependencias de Windows](evidencias/dependencias-windows.txt). Para instalar en otro sistema utiliza `requirements.txt` y un entorno nuevo. No se necesitan LangGraph, RAG, bases vectoriales, React, Docker o un servidor de base de datos para esta entrega.

## Análisis de opiniones

Flujo: selección de alien → opinión → validación → Gemini → validación Pydantic → guardado si es pertinente → resultado visible.

El prompt `omnitrix-v1` usa `ChatPromptTemplate` con mensajes system/human y datos JSON. La cadena se compone mediante `|`, `with_structured_output(method="json_schema")` e `invoke`. Se envían la opinión actual y los datos relevantes del alien; el historial visual permanece fuera del prompt.

Contrato `AnalisisOpinion`:

| Campo | Regla |
| --- | --- |
| `es_pertinente` | Booleano estricto. |
| `sentimiento` | `positivo`, `negativo`, `neutro`, `mixto` o `None`. |
| `razon` | Texto en español, entre 1 y 300 caracteres tras quitar espacios exteriores. |

Una respuesta pertinente exige sentimiento; una ajena exige `None`. Se rechazan campos adicionales y combinaciones incoherentes. Los textos incrustados que intenten cambiar instrucciones se tratan como datos en el prompt; la eficacia real de esta defensa requiere evaluación del modelo.

`ejecutar_estructurado` comparte configuración y manejo seguro de errores entre opiniones y desafíos. Lee `.env` y entorno, crea Gemini Developer API con `vertexai=False`, timeout de 30 segundos y un intento total (`max_retries=1` en esta integración). El modelo fijado es `gemini-3.5-flash-lite`; no hay fallback. El programa no publica respuestas privadas de excepciones del proveedor.

## Persistencia y consultas

El catálogo incorpora `especie`, `estado_especie` (`identificada`, `sin_nombre_confirmado` o `hibrida`) y `fuentes_especie` (lista de enlaces HTTPS). Se muestran en la ficha reutilizada por catálogo y desafíos, sin consultas al modelo. El bloque es opcional para leer catálogos v1 antiguos, pero debe estar completo si aparece cualquiera de sus campos. Las 63 fichas actuales lo incluyen. Nombres originales de especie, decisiones editoriales y referencias en [Especies](datos/ESPECIES.md). Una especie sin nombre confirmado no equivale a ausencia de especie.

`datos/opiniones.json` tiene esta estructura:

```json
{"version": 1, "opiniones": []}
```

Cada registro contiene `id`, `fecha_utc`, `alien_id`, `alien_nombre`, `opinion_original`, `sentimiento`, `razon`, `modelo` y `version_prompt`. La aplicación genera UUID y fecha y captura la selección; el modelo no elige esos campos.

Se valida el archivo completo antes de escribir. El guardado utiliza un temporal en la misma carpeta, sincronización y reemplazo. El mismo ID/datos es idempotente; un ID con datos diferentes se rechaza. Un JSON dañado se conserva y genera un error visible. El reemplazo atómico no sustituye el control de concurrencia: la entrega admite un escritor local.

La consulta aplica filtros por ID y sentimiento combinados con AND. Tabla, total, recuentos y JSON descargable parten de la misma lista. Consultar no escribe ni invoca IA y no necesita que el catálogo pueda cargarse.

## Desafíos y estados de ronda

El banco local tiene 32 situaciones con `id`, `titulo`, `situacion` y `objetivo`, bajo `version: 1`. `Situacion` valida longitud y tipos; el cargador exige al menos dos entradas e IDs únicos.

Flujo de juego:

```text
Menú de modos → elegir modo → Iniciar → situación y opciones asignadas
→ elegir alien cuando corresponda → estrategia → Evaluar
→ resultado válido y ronda cerrada → Volver a jugar / Volver al menú de modos
```

Control maestro usa todos los IDs. Héroe bajo presión usa `random.sample` con tres IDs distintos; Adaptabilidad usa uno y no permite cambiarlo. El sorteo ocurre al iniciar o rejugar y permanece estable al editar/navegar. Se repone si el catálogo se vuelve incompatible con la asignación de sesión. Rejugar evita repetir inmediatamente la situación anterior; una situación o alien puede reaparecer en rondas posteriores.

La estrategia es opcional en los dos primeros submodos y obligatoria (5–1000 caracteres) en Adaptabilidad. Antes de elegir en Héroe bajo presión se muestran las tres fichas en pestañas; se reutiliza `mostrar_ficha` con claves de contenedor únicas. Esos recursos proceden del catálogo y no generan consultas a Gemini.

El prompt `desafios-v2` recibe situación, alien, estrategia y modo. En Adaptabilidad valora cómo se aprovechan las capacidades asignadas, sin exigir otra transformación. `EvaluacionDesafio` admite `adecuado`, `arriesgado` o `poco_adecuado`, más resumen (1–500), ventajas (1–400), riesgos (1–400) y resolución (1–700 caracteres). Se valida la salida, sin simular votos u opiniones de personas.

Una evaluación válida guarda en sesión el resultado, alien y plan y retira el formulario. Las acciones finales aparecen solo entonces. Un error conserva los datos para reintentar; no se inventa un final. Volver a jugar limpia respuesta/error/selección/plan y sortea otra situación; volver al menú exige Iniciar para comenzar otra ronda. Las partidas no se escriben en el JSON de opiniones.

## Conocimiento alienígena

Menú de cuatro categorías con selección e Iniciar. `generar_preguntas` sortea una pregunta por imagen (máximo 63), fija el orden en sesión y usa enunciados locales. Especie solo incluye las 55 fichas identificadas; General aplica el mismo filtro al elegir esa categoría. No se llama al modelo para generar preguntas.

`conocimiento_ronda` conserva ID de ronda, categoría, preguntas, respuestas enviadas, plazo monotónico, estado y evaluación/error. El formulario de cada pregunta conserva el borrador mientras un `st.fragment(run_every="1s")` actualiza únicamente el reloj. El plazo no se reinicia al navegar; se comprueba también al enviar para rechazar respuestas tardías. Las rondas se cierran al agotar 60 segundos, terminar manualmente o completar el banco. No se escriben en `opiniones.json`.

Al pulsar Evaluar respuestas con IA, `evaluar_respuestas` envía todas las respuestas de esa ronda en una solicitud a `ejecutar_estructurado`. `conocimiento-v2` distingue instrucciones de datos, acepta alias/traducciones y evalúa habilidades por significado. Cada entrada recibe ID, categoría, texto y ficha compacta con nombres, habilidades, especie, estado y alias. No se envían imágenes, credenciales, opiniones ni partidas anteriores.

`EvaluacionConocimiento` valida entre 1 y 63 correcciones, con ID y veredicto (`correcta`, `parcial`, `incorrecta`, `no_evaluable`), explicación (1–400 caracteres) y referencia (1–300). Se exige correspondencia exacta de IDs, sin duplicados ni omisiones; se recompone el orden local. La app calcula 1/0,5/0 puntos y excluye los casos no evaluables. No se repite IA al mostrar/navegar resultados; un error conserva respuestas y permite un reintento explícito. Desde `conocimiento-v2` se usa `ESQUEMA_API` explícito y sencillo, mediante el parámetro opcional `esquema_api` de `ejecutar_estructurado`; las restricciones detalladas siguen en Pydantic local. `include_raw=True` permite comprobar finalización por tokens y errores de parseo sin mostrar ni persistir el contenido privado. Las llamadas anteriores de opiniones/desafíos conservan su ruta por defecto. Límites semánticos, alias y guía de pruebas visuales en [datos/CONOCIMIENTO.md](datos/CONOCIMIENTO.md).

## Interpretación alienígena

`datos/interpretacion.json` tiene versión 1 y exactamente 30 preguntas, cinco por cada uno de los seis temas definidos en `interpretacion.TEMAS`. Se valida el banco sin modificarlo. `sortear_preguntas` elige una por tema y al repetir excluye las seis anteriores. El modo favorito no necesita cargar el banco.

`interpretacion_ronda` conserva modo, ID, etapa, índice, preguntas, respuestas, favorito/motivo y evaluación. Las etapas son favorito o preguntas → revisión (afinidad) → resultado. Callbacks conservan texto al navegar; el resultado usa una instantánea del envío. No hay temporizador ni escritura en el archivo de opiniones.

`interpretar` envía una ficha en favorito, o el catálogo compacto de 63 en afinidad, con la explicación o seis respuestas. Usa `ejecutar_estructurado` con esquema API explícito sencillo, validación estricta `Interpretacion` y prompt `interpretacion-v1`. Se exige conservar el favorito, principal existente, alternativa diferente en afinidad y cobertura exacta de los IDs de respuestas. La IA explica analogías recreativas con capacidades, sin diagnosticar ni inferir rasgos sensibles; no se usa puntuación. Fallos conservan la edición/revisión y solo un clic explícito reintenta. [Guía y pruebas](datos/INTERPRETACION.md).

## Entrada audiovisual

El fondo ambiental del dashboard está en `assets/estilos.css`: dos pseudoelementos fijos detrás del contenido, con siete formas de gradientes radiales. Las animaciones de transformación trasladan, escalan y giran las dos capas en ciclos lentos distintos. No se crean temporizadores de Python ni consultas a IA para animarlo. `pointer-events: none`, nivel negativo y aislamiento mantienen los controles y textos por delante; portada y fichas conservan sus fondos. En móvil se utiliza una sola capa y con movimiento reducido se detienen las animaciones. La capa superior verde de la transición sigue por encima del ambiente.

El símbolo `assets/omnitrix.png` también se usa en la portada, sidebar y favicon. En la entrada comienza a escala 0.76. La primera interacción lo levanta y reproduce `core-ready.mp3`; la segunda lo presiona y reproduce `omnitrix-transform.mp3`.

No se usa autoplay al cargar. El JavaScript evita activaciones repetidas durante la animación y crea una única capa verde persistente en la capa superior del navegador para cubrir el sidebar y el dashboard durante la reejecución. Se desvanece cuando el contenido está listo. El segundo audio continúa durante el desmontaje del componente. Se contempla movimiento reducido y una salida de seguridad de la capa para no dejar la interfaz bloqueada indefinidamente.

La activación se guarda en `st.session_state`; navegar o limpiar el chat no repite la entrada. Cambiar los archivos de recursos requiere reiniciar el servidor para registrar el componente de nuevo.

Antes de retirar la capa verde se enfoca el título con `preventScroll` y se restablece a cero el desplazamiento del contenedor principal (`main.stMain`), evitando que el chat deje el dashboard inicialmente abajo. Se aplica solo en esa entrada y no bloquea el desplazamiento manual posterior. La revisión de navegador comprueba la posición al terminar y tras una espera, además de verificar que se pueda bajar normalmente.

La revelación espera también a que Streamlit termine su ejecución; al terminar el desvanecimiento confirma una última vez la posición inicial antes de retirar la capa. De ese modo los cambios de foco/altura pendientes del chat no desplazan el inicio bajo carga.

## Ampliar contenido

### Aliens

Conserva los IDs existentes y añade nuevos en `datos/aliens.json`. Campos obligatorios: `id`, `nombre`, `nombre_original`, `serie_origen`, `descripcion`, `imagen`. Las rutas deben ser locales relativas y `imagen` admite `null` para utilizar la alternativa.

Registra fuente, URL, dimensiones y hash en `assets/aliens/fuentes.json` y actualiza los créditos. Los campos opcionales `serie_diseno` y `fuente_imagen` permiten identificar diseños de otras series; los registros originales conservan Omniverse como valor predeterminado. No cambies la identidad del alien de una opinión al cambiar un nombre o imagen.

### Situaciones

Añade IDs únicos después de d032 en `datos/desafios.json`, títulos distintos y objetivos abiertos. Mantén los límites de `Situacion`, redacta capacidades/contexto necesarios y evita exigir una respuesta única. Las misiones son ficción original; no se presentan como episodios oficiales. Actualiza recuentos de documentación y la prueba del banco cuando cambie su tamaño.

## Pruebas desde terminal

En Windows:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip check
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests\comprobar_inicio_windows.ps1
.\.venv\Scripts\python.exe scripts\generar_evidencias.py
```

El ajuste de política del comando PowerShell solo afecta a ese proceso de prueba. No cambia la política general del equipo.

Comandos propuestos para verificar en Linux:

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m pip check
.venv/bin/python scripts/generar_evidencias.py
```

La prueba del mutex está marcada para omitirse fuera de Windows; el script `.ps1` no forma parte del recorrido Linux. Esa ejecución completa todavía no se ha realizado en Linux. Revisa [VERIFICACION.md](VERIFICACION.md) antes de afirmar compatibilidad comprobada.

Las pruebas aíslan escrituras y simulan el modelo. El generador de evidencias usa ejemplos manuales en una carpeta temporal, demuestra lectura desde otro proceso y exporta resultados a `evidencias/`; no consume API ni modifica opiniones de uso.

## Revisión de navegador opcional

Requiere Node, un Chromium/Brave compatible y Playwright Core instalado localmente:

```text
npm install --prefix .herramientas/browser-check playwright-core
```

El navegador predeterminado del script es Brave en Windows. En otro equipo configura `OMNITRIX_BROWSER` con la ruta de su ejecutable. Ejemplo Linux, si Chromium está instalado en esa ruta:

```bash
export OMNITRIX_BROWSER="/usr/bin/chromium"
```

Para la entrada audiovisual, arranca la aplicación normal en un puerto local y ejecuta:

```text
node tests/verificar_intro.cjs http://127.0.0.1:8501
```

El script comprueba dos pulsaciones, audio local, cobertura del sidebar y movimiento reducido, sin enviar opiniones.

Para verificar el ambiente y los controles con el servidor normal abierto:

```text
node tests/verificar_fondo.cjs http://127.0.0.1:8501
```

Comprueba movimiento, posición detrás del contenido, imágenes, selección y navegación en escritorio/móvil, además del estado estático con movimiento reducido. No envía opiniones ni estrategias a la IA.

Para verificar el final de rondas sin consumir cuota, arranca **exclusivamente el servidor de pruebas**:

```powershell
.\.venv\Scripts\python.exe -m streamlit run tests/app_desafios_visual.py --server.address 127.0.0.1 --server.port 54167 --server.headless true
```

Equivalente Linux propuesto:

```bash
.venv/bin/python -m streamlit run tests/app_desafios_visual.py --server.address 127.0.0.1 --server.port 54167 --server.headless true
```

En otra terminal:

```text
node tests/verificar_desafios.cjs http://127.0.0.1:54167 --simulado
```

El servidor de prueba reemplaza solo el evaluador del juego por datos rotulados como simulados y presenta un marcador que exige el script. La aplicación de entrega sigue siendo `app.py` con Gemini real. Las capturas y resultados temporales se guardan en `.herramientas/browser-check/`; los perfiles de prueba son independientes del navegador personal.

## Contribuciones y seguridad de datos

Respeta `.gitignore`: no publiques `.env`, claves, entornos, runtimes, herramientas temporales ni logs privados. Revisa también si el archivo de opiniones contiene datos que no deban entregarse. Los recursos de terceros conservan sus fuentes y no tienen una licencia libre acreditada.

Los commits se sugieren con Conventional Commits; no se ejecutan ni publican automáticamente. Materiales de clase y documentos históricos aportan contexto, sin ampliar por sí solos el alcance autorizado.
