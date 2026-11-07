# Interpretación alienígena

Una sección recreativa con dos submodos. Primero selecciona uno en el menú y pulsa **Iniciar**. Consultar archivo sigue al final del panel lateral.

## Mi alien favorito

Elige entre las 63 transformaciones, consulta su ficha y explica por qué te gusta, qué admiras o para qué usarías sus capacidades (10–1000 caracteres). Pulsa **Interpretar mi elección**.

La IA conserva el alien elegido y relaciona tus motivos con valores y un estilo de héroe. La explicación tiene más peso que la elección: preferir un diseño no basta para concluir rasgos personales. El resultado incluye conexiones con lo que escribiste, límites y una pregunta para reflexionar.

## Tu afinidad alienígena

El banco local `interpretacion.json` contiene **30 preguntas originales**, cinco por tema:

| Tema | Qué exploran las preguntas |
| --- | --- |
| Resolución de problemas | Cómo abordas dificultades y alternativas. |
| Colaboración | Cómo participas, escuchas y buscas acuerdos. |
| Valores | Qué principios o aportaciones te importan. |
| Riesgos | Cómo decides ante incertidumbre y consecuencias. |
| Aprendizaje ante errores | Cómo revisas, aprendes y vuelves a intentar. |
| Motivación | Qué te impulsa y qué te gustaría aportar. |

Se sortea **una por tema: seis preguntas por partida**, una a la vez. No hay temporizador, sonidos de cuenta atrás, pistas, opciones cerradas ni puntuación. Cada respuesta admite 10–1000 caracteres. No se piden datos privados ni ejemplos personales obligatorios; puedes responder con situaciones imaginadas.

Usa **Anterior** y **Siguiente** para revisar. Después de la sexta aparece una pantalla con las seis respuestas y un botón para editar cada una. **Descubrir mi afinidad** solicita el análisis de todas juntas. Leer preguntas, escribir, editar y navegar no usa la API.

La IA elige un **alien principal y una alternativa diferente** entre las 63 fichas del catálogo. El resultado muestra sus imágenes, las razones, valores, estilo de héroe y una conexión con cada respuesta, además de límites y una pregunta abierta. La asociación es simbólica con las capacidades descritas, no una afirmación de que una especie o quien la elige tenga determinada personalidad.

## Límites y datos

Es una interpretación lúdica; no un test de personalidad validado, diagnóstico ni evaluación psicológica. No hay porcentajes de afinidad ni certezas personales. El prompt pide reconocer información escasa o contradictoria, sin inventar experiencias, poderes ni rasgos sensibles. El modelo puede equivocarse o producir analogías poco convincentes; el jugador puede discrepar.

Se usa la misma configuración Gemini Free Tier, sin cambio de modelo/proveedor ni activación de facturación. Cada botón de análisis hace una solicitud; un error conserva el texto y permite un reintento manual. Ver resultados otra vez no vuelve a consultar el modelo. La app no confirma que la cuenta tenga cuota disponible.

La selección, respuestas y resultados viven solo en `st.session_state`, separados de `opiniones.json`. Cambiar de sección conserva la partida; volver al menú descarta esa partida. Reiniciar el servidor o abrir una sesión nueva puede perderla. **Volver a intentarlo** prepara otra interpretación y, en afinidad, sortea preguntas distintas a las de la partida inmediatamente anterior.

## Implementación y pruebas

- `interpretacion.py`: carga/valida el banco, sortea por temas, construye el prompt `interpretacion-v1`, usa un esquema API sencillo y valida la salida con Pydantic. Comprueba IDs del catálogo, alternativa distinta, conservación del favorito y una conexión por cada respuesta, sin omisiones ni IDs ajenos.
- `interfaz_interpretacion.py`: menú, ficha del favorito, seis preguntas editables, revisión y presentación del resultado. Los textos del usuario y del modelo se muestran como texto, sin ejecutarlos.
- `tests/test_interpretacion.py`: banco, entradas/salidas, estado de interfaz y adaptador Gemini real con transporte interceptado. No acredita calidad semántica real del modelo ni consume cuota.
- `tests/app_interpretacion_visual.py`: servidor exclusivo de revisión, con resultados marcados como simulados. Nunca sustituye a `app.py` en la entrega.

Pruebas locales:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_interpretacion.py -v
```

Para la revisión de navegador, inicia el servidor simulado y, en otra terminal con Playwright Core y Brave preparados, ejecuta el verificador:

```powershell
.\.venv\Scripts\python.exe -m streamlit run tests/app_interpretacion_visual.py --server.address 127.0.0.1 --server.port 54167 --browser.gatherUsageStats false
```

```powershell
node tests/verificar_interpretacion.cjs http://127.0.0.1:54167 --simulado
```

En Linux, las pruebas Python usan `.venv/bin/python` y el navegador del verificador debe indicarse mediante `OMNITRIX_BROWSER`. Esto documenta el procedimiento; la verificación integral de la aplicación actual en Linux sigue pendiente.
