# Archivo Omnitrix

Aplicación académica para explorar 63 transformaciones de Ben 10, opinar sobre ellos y clasificar el sentimiento con un modelo de lenguaje. Adapta el taller de opiniones sobre futbolistas; según lo comunicado por el estudiante, en clase se permitió cambiar la temática conservando los requisitos técnicos.

Python y Streamlit construyen la interfaz negra, verde neón y blanca; LangChain y Pydantic coordinan y validan el análisis. Las opiniones pertinentes se guardan en JSON local.

## Estado de la entrega

Implementación y documentación de los 13 pasos preparadas. **68 pruebas automatizadas aprobadas** tras adaptar el análisis a Gemini, en Windows con Python 3.14.4 y Streamlit 1.67.0; `pip check` sin incompatibilidades. Se comprobaron persistencia entre procesos, filtros/exportación, mutex y arranque/respuesta/detención de un servidor real.

**Uso sin pago:** seguir [GEMINI_GRATIS.md](GEMINI_GRATIS.md), usando únicamente un proyecto Google AI Studio **Free Tier sin facturación vinculada**. No se utiliza la clave anterior de OpenAI. La app no puede comprobar el estado de facturación de tu proyecto: esa elección debe hacerse en AI Studio. La cuota gratuita y disponibilidad dependen de la cuenta/modelo.

**La aceptación completa sigue pendiente:** falta configurar y evaluar un modelo real y completar la revisión manual de la página, descarga y cierre desde el controlador. Computer Use detuvo la inspección de Brave al no poder verificar su URL. Las pruebas del análisis usan respuestas simuladas y no demuestran precisión semántica. Ver [resultados, reflexiones y límites](VERIFICACION.md).

Los 16 ejemplos y los seis casos de evaluación tienen referencias humanas explícitas. No se mezclan automáticamente con las opiniones de uso ni se presentan como resultados obtenidos de una API.

## Inicio gráfico

En este equipo ya están preparados Python y `.venv`. Abrir [Iniciar Archivo Omnitrix.vbs](<Iniciar Archivo Omnitrix.vbs>) con doble clic. El controlador comprueba dependencias, inicia el servidor local y abre el navegador cuando responde.

- **Abrir en navegador:** vuelve a abrir la aplicación si se cerró su pestaña.
- **Detener y cerrar:** cierra el controlador y detiene su servidor. Cerrar solo la pestaña deja el servidor activo.
- Una segunda apertura de esta carpeta en la misma sesión de Windows muestra un aviso; utilizar la ventana de control existente.

La dirección usa `127.0.0.1` y un puerto disponible, que puede cambiar en cada inicio. El lanzador resuelve las rutas desde el proyecto, utiliza exclusivamente `.venv\Scripts\python.exe` y carga el tema de `.streamlit/config.toml`. Requiere Windows Script Host y Python de Windows con Tkinter. No se afirma compatibilidad del lanzador con otros sistemas.

## Preparación de otro equipo

Esta preparación es técnica y se realiza una vez. El uso posterior es mediante doble clic, sin comandos.

1. Obtener el repositorio completo con `datos/`, `assets/` y `.streamlit/`.
2. Disponer de Python para Windows con Tkinter. La versión comprobada es **3.14.4**. El código requiere Python 3.10 o superior; las otras combinaciones no se volvieron a verificar en esta entrega.
3. Crear un entorno nuevo e instalar dependencias desde PowerShell en la raíz:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

Si `py` no está disponible, usar la ruta al `python.exe` instalado en el primer comando. En este equipo se puede reconstruir el entorno con `.\.python-runtime\python.exe -m venv .venv`. El runtime local y `.venv` están excluidos de Git: no copiarlos como sustituto de una instalación en otro equipo. Si se mueve el proyecto, reconstruir el entorno.

`requirements.txt` fija las dependencias directas y selecciona Streamlit según Python. La [instantánea de versiones de Windows](evidencias/dependencias-windows.txt) incluye las transitivas utilizadas. Para reproducir exactamente esa combinación con Python 3.14.4 en Windows, puede instalarse esa instantánea dentro de un entorno nuevo en lugar del archivo inicial:

```powershell
.\.venv\Scripts\python.exe -m pip install -r evidencias\dependencias-windows.txt
```

No se instalan programas ni paquetes automáticamente al abrir el lanzador. El catálogo y la consulta funcionan sin credenciales de IA.

## Configurar el análisis con IA

Copiar `.env.example` a `.env` en la raíz y completar localmente:

| Variable | Configuración |
| --- | --- |
| `GOOGLE_API_KEY` | Clave de Google AI Studio de un proyecto Free Tier sin facturación. El archivo está excluido de Git. |
| `GEMINI_MODEL` | `gemini-3.5-flash-lite`, modelo preparado para esta entrega. No hay cambio automático de modelo. |
| `GEMINI_TEMPERATURE` | Vacío: utiliza la configuración recomendada por la integración para Gemini 3.x. |

No incluir claves reales en código, capturas, documentación o commits. Las variables del sistema tienen prioridad sobre `.env`. Reiniciar el controlador después de cambiar configuración. No se ha confirmado el acceso o cuota gratuita de tu cuenta. Las variables antiguas de OpenAI se ignoran. Si AI Studio solicita pagos, no activarlos; consultar la guía gratuita antes de continuar.

El prompt `omnitrix-v1` recibe solo los datos del alien y la opinión actual, sin historial. Pydantic valida pertinencia, categoría y razón de 1 a 300 caracteres. Una opinión pertinente exige categoría; una ajena exige sentimiento `null` y no se guarda. Las instrucciones incrustadas se tratan como datos. Estos mecanismos necesitan evaluación real y no garantizan que toda clasificación sea correcta.

## Uso

### Analizar opinión

1. Elegir un alien y revisar su ficha e imagen local. Si la imagen falla, se muestra una alternativa.
2. Enviar una opinión de **5 a 1000 caracteres** después de quitar espacios exteriores. Se conserva el texto original, sin truncarlo.
3. Consultar sentimiento y justificación, o el aviso de falta de pertinencia o error.
4. Buscar «Opinión guardada en el Archivo Omnitrix»: aparece únicamente tras guardar o comprobar que ese mismo envío ya existe.

Categorías: `positivo` (favorable), `negativo` (desfavorable), `neutro` (descripción sin valoración clara) y `mixto` (elogios y críticas relevantes). El resultado describe el comentario; no determina objetivamente qué alien es mejor.

Cada envío captura el alien seleccionado. Cambiarlo no modifica opiniones anteriores. **Nueva conversación** limpia el chat temporal y los rechazos, conservando selección y archivo persistente. No hay borrado del archivo desde la interfaz.

Si falla el análisis, el comentario queda visible y no se inventa una categoría. Reenviar cuenta como un envío nuevo. Si falla la escritura, **Reintentar guardado** conserva UUID, fecha y análisis, sin llamar nuevamente a la IA. Navegar o cambiar filtros no repite el análisis ni el guardado.

### Consultar archivo

Elegir alien y/o sentimiento, o dejar «Todos». Los aliens disponibles son los presentes en los registros guardados y se identifican por ID. La tabla muestra fecha UTC, alien/ID, texto original, sentimiento y razón. Total, cuatro recuentos y descarga usan exactamente los mismos resultados filtrados.

**Descargar resultados filtrados (JSON)** exporta registros completos, con UUID y metadatos, en UTF-8. Los estados vacíos son informativos y permiten descargar una lista vacía. Consultar funciona aunque falle el catálogo, sin llamar al modelo ni escribir. Un JSON dañado muestra un error sin sustituirlo por datos vacíos.

### Desafíos del Omnitrix

El panel izquierdo muestra **Analizar opinión**, **Desafíos del Omnitrix** y **Consultar archivo**, en ese orden. Al abrir Desafíos aparece un menú: elegir **Control maestro** (las 63 transformaciones), **Héroe bajo presión** (tres aliens distintos elegidos al azar) o **Adaptabilidad** (un único alien asignado al azar) y pulsar **Iniciar**. No se presenta una misión antes de iniciar.

Se sortea una de 32 situaciones locales (incendio en un hangar, rescate submarino, robots descontrolados y otras). El sorteo se conserva al editar o navegar. No se permite saltar la situación durante la ronda. En los modos aleatorios los aliens no se eligen por sus poderes ni su adecuación a la misión.

En Control maestro y Héroe bajo presión se elige un alien y la estrategia es opcional. En Adaptabilidad no hay selector: se muestra el alien asignado y se debe explicar cómo resolver la situación, con entre 5 y 1000 caracteres. La IA evalúa el uso de sus capacidades, sin penalizar al jugador por no poder elegir otro alien. El botón Evaluar consulta Gemini una vez y muestra un veredicto, ventajas, riesgos y una posible resolución. Puede haber varias soluciones válidas. La evaluación es una interpretación de IA de un juego de ficción, no una simulación física ni opiniones de otros jugadores.

En Héroe bajo presión, las tres fichas se pueden consultar antes de elegir: cada pestaña muestra la imagen, habilidades, nombre original y serie del alien correspondiente. Consultar estas fichas no usa la IA ni cambia el sorteo.

Al recibir una evaluación válida termina la ronda y la respuesta queda fija. Al final aparecen **Volver a jugar**, que sortea una situación diferente y renueva los aliens aleatorios, y **Volver al menú de modos**. La nueva ronda limpia la elección y la explicación. Si falla la API, no termina la ronda: conserva los datos para corregir o reintentar explícitamente. La partida y el resultado se conservan al navegar durante la sesión; no se escriben en `datos/opiniones.json`. Utiliza la misma configuración Gemini y cuota del análisis de opiniones.

## Datos, respaldo y alcance

`datos/opiniones.json` usa `{"version": 1, "opiniones": []}`. Cada registro contiene UUID, fecha UTC, alien/ID capturado, opinión original, sentimiento, razón, modelo y versión del prompt. La aplicación genera identidad y fecha; no las elige el modelo.

La escritura valida los registros y usa temporal en el mismo directorio, sincronización y reemplazo final. Un ID repetido con los mismos datos no se duplica; con datos distintos se rechaza. Dos envíos independientes con texto idéntico pueden ser dos registros válidos.

Para respaldar o trasladar opiniones, detener el servidor y copiar `datos/opiniones.json`. Conservar catálogo e imágenes al trasladar el proyecto. Si el archivo está dañado, preservarlo y revisar una copia; no reemplazarlo por ejemplos. Las pruebas y el generador de evidencias usan carpetas temporales.

La versión base admite **un único escritor local**. El reemplazo atómico y el mutex del lanzador no constituyen soporte multiusuario. No incluye cuentas, RAG, agentes, combate ni chatbot general. Las imágenes son material de terceros para el proyecto académico; ver [créditos y límites de procedencia](assets/aliens/README.md).

## Archivos principales

| Archivo o carpeta | Responsabilidad |
| --- | --- |
| `app.py` | Navegación, fichas, chat, resultados, filtros y descarga. |
| `analisis.py` | Configuración, prompt, esquema y análisis estructurado. |
| `almacenamiento.py` | Validación de catálogo/registros, escritura y consultas. |
| `desafios.py` e `interfaz_desafios.py` | Situaciones, estado del juego y evaluación estructurada de estrategias. |
| `datos/desafios.json` | 32 situaciones de ficción preparadas localmente, sin respuestas obligatorias. |
| `iniciar.py` y el VBS | Controlador gráfico y ciclo de vida del servidor Windows. |
| `datos/aliens.json` | 63 fichas con IDs estables y nombres latinos, incluyendo ambas variantes de Upchuck; sin formas supremas ni reboot. |
| `datos/opiniones.json` | Opiniones de uso persistentes. |
| `datos/ejemplos/` | 16 registros y seis casos con expectativas manuales. |
| `assets/` y `.streamlit/` | Estilos, imágenes locales, fuentes y tema. |
| `tests/` | Pruebas de contrato, interfaz, persistencia, consultas, inicio y aceptación. |
| `scripts/generar_evidencias.py` | Evidencia de persistencia y filtro con datos manuales aislados. |

## Pruebas y evidencias

Al abrir una sesión aparece el símbolo del Omnitrix hundido, sin reproducir audio. El primer clic o Enter levanta el selector y reproduce `sonidos/core-ready.mp3`. Una segunda pulsación reproduce `sonidos/omnitrix-transform.mp3`, hunde el símbolo y pone toda la pantalla en verde. Ambos audios empiezan dentro de un gesto del usuario. La capa se mantiene durante la carga y revela suavemente el dashboard y su barra lateral cuando están listos. La entrada aparece una vez por sesión; navegar y limpiar la conversación no la reinician. Respeta la preferencia del sistema de reducir movimiento.

Con `.venv` preparado, desde la raíz:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip check
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests\comprobar_inicio_windows.ps1
.\.venv\Scripts\python.exe scripts\generar_evidencias.py
```

La política indicada afecta solo al proceso PowerShell de la prueba. La suite usa archivos temporales y dobles del modelo, sin consumir API. Incluye servidor local real y otro proceso Python para demostrar persistencia. El generador tampoco consume API ni modifica opiniones de uso.

La comprobación opcional de la entrada en navegador está en `tests/verificar_intro.cjs`. Requiere Node, `npm install --prefix .herramientas/browser-check playwright-core` y Brave (o la ruta de Chromium en `OMNITRIX_BROWSER`). Con el servidor abierto, ejecutar `node tests/verificar_intro.cjs http://127.0.0.1:PUERTO`. Usa un perfil temporal, comprueba clic/Enter/móvil/movimiento reducido, reproducción de MP3, cobertura del panel lateral y continuidad con autoplay bloqueado; guarda capturas en `.herramientas/browser-check/` y no envía opiniones a la API. Tras editar recursos de la entrada, reiniciar el servidor para recargar el componente.

- [Registro de pruebas, límites y dos ambigüedades](VERIFICACION.md).
- [Salida de las 68 pruebas aprobadas con Gemini](evidencias/pruebas-gemini-windows.txt).
- [Salida de las 71 pruebas con la pantalla de activación](evidencias/pruebas-inicio-windows.txt).
- [Salida de las 72 pruebas con el catálogo ampliado a 63 fichas](evidencias/pruebas-catalogo-ampliado-windows.txt).
- [Salida de las 82 pruebas con Desafíos del Omnitrix](evidencias/pruebas-desafios-windows.txt).
- [Salida de las 85 pruebas con menú y submodos de desafíos](evidencias/pruebas-submodos-windows.txt).
- [Salida de las 87 pruebas con rondas cerradas y Adaptabilidad](evidencias/pruebas-rondas-adaptabilidad-windows.txt).
- [Tres submodos, final de ronda, rejuego y retorno al menú en escritorio/móvil](evidencias/navegador-rondas-adaptabilidad.json). Evaluaciones simuladas, sin API. Para reproducir: iniciar un servidor separado con `streamlit run tests/app_desafios_visual.py --server.port 54167` y ejecutar `node tests/verificar_desafios.cjs http://127.0.0.1:54167 --simulado`. El servidor de prueba rotula sus resultados como simulados y no es la aplicación de entrega.
- [Revisión de menú, Control maestro y Héroe bajo presión en escritorio y móvil](evidencias/navegador-submodos.json).
- [Comprobación histórica del modo Desafíos en escritorio y móvil](evidencias/navegador-desafios.json). Corresponde a la versión anterior al cierre por rondas; el script vigente se ejecuta contra el servidor visual simulado indicado arriba.
- [Comprobación en navegador: clic, Enter, móvil y movimiento reducido](evidencias/navegador-inicio.json).
- [Comprobación de audio y transición continua, incluido bloqueo de autoplay](evidencias/navegador-inicio-audio.json).
- [Registro histórico de 65 pruebas anterior a Gemini](evidencias/pruebas-windows.txt).
- [Versiones instaladas](evidencias/dependencias-windows.txt).
- [Evidencia de persistencia y filtrado](evidencias/persistencia-y-filtro.json).
- [JSON filtrado: XLR8, mixto](evidencias/consulta-xlr8-mixto.json), con análisis manual explícito.
- [Guía de sustentación y cierre de aceptación](ENTREGA.md).

La persistencia y los filtros se ejecutaron realmente sobre datos ficticios; las categorías siguen siendo manuales. No equivalen a evaluar un modelo.

## Problemas frecuentes

| Situación | Acción |
| --- | --- |
| Falta `.venv\Scripts\python.exe` | Preparar un entorno de Windows en esta carpeta. |
| Faltan dependencias o el servidor no inicia | Revisar `inicio.log`, requisitos y `pip check`. |
| Ya hay un controlador abierto | Usar Abrir en navegador y detenerlo antes de iniciar otra instancia. |
| Configuración incompleta o API rechazada | Revisar `.env`, acceso al modelo, compatibilidad y cuota; no publicar claves. |
| Error de guardado | Revisar permisos/espacio y reintentar el mismo registro desde el chat. |
| Archivo inválido | Preservarlo y revisar estructura o respaldo; no se repara automáticamente. |
| Consulta vacía | Comprobar que hubo guardado exitoso y revisar los filtros. |

## Continuidad

[CONTEXTO_PROYECTO.md](CONTEXTO_PROYECTO.md) conserva decisiones y contratos; [PLAN_DESARROLLO.md](PLAN_DESARROLLO.md) registra etapas y pendientes. El [historial anterior](docs/HISTORIAL_DESARROLLO.md) es referencia, no guía vigente de uso.

La documentación del paso 13 está preparada. Antes de declarar la entrega completamente aceptada, completar la evaluación del modelo y las observaciones manuales pendientes en `VERIFICACION.md`. No se ejecutaron commits ni push automáticamente.
