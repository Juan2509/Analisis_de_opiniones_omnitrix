# Conocimiento alienígena

Sección de preguntas escritas con cuatro categorías: **Nombres**, **Habilidades**, **Especie** y **General**. Selecciona una y pulsa **Iniciar**, igual que en el menú de desafíos. Consultar archivo sigue siendo la última sección del panel.

## Cómo se juega

- Cada ronda dura **60 segundos**. Aparece una imagen y una pregunta a la vez.
- Cuando quedan **cuatro segundos**, suena `omnitrix-time-out.mp3` una sola vez por ronda en las cuatro categorías. No se repite al enviar ni al actualizar el reloj. Depende de los permisos de sonido del navegador.
- Escribe de 1 a 500 caracteres y pulsa **Enviar y siguiente**, o Enter desde el campo de respuesta. No hay opciones de respuesta, pistas ni corrección durante la ronda.
- Nombres acepta nombres en español, inglés y alias reconocibles. Habilidades pide una capacidad característica, explicada con tus palabras. Especie pide el nombre de la especie; no el planeta. General mezcla las tres categorías.
- Las imágenes se sortean una sola vez al iniciar y no se repiten dentro de la ronda. Hay hasta 63 preguntas; Especie usa las 55 fichas con especie identificada. Las siete sin nombre confirmado y Nanomech híbrido quedan fuera de las preguntas de especie, también en General.
- El reloj sigue al cambiar de sección. El servidor rechaza envíos recibidos después del plazo, aunque el navegador esté en segundo plano. Solo se guardan respuestas enviadas; un borrador al agotarse el tiempo no cuenta.
- Puedes terminar anticipadamente con **Terminar ronda**. Al agotar el tiempo o completar el banco se cierra el formulario.
- Pulsa **Evaluar respuestas con IA** para obtener una corrección conjunta. Se hace una solicitud a Gemini por revisión, sin bloquear el tiempo de juego entre respuestas. Un error conserva la ronda y permite reintentar manualmente.
- Después puedes revisar cada imagen, tu respuesta, una referencia y la explicación. **Volver a jugar** inicia otro sorteo en la misma categoría; **Volver al menú de modos** permite elegir otra.

## Evaluación y puntuación

La IA recibe las respuestas junto con los nombres, especie y descripción de habilidades de las fichas correspondientes. Se instruye para aceptar variaciones de tildes, mayúsculas, signos, errores menores y traducciones o alias inequívocos. No se exige repetir una frase literal. En Habilidades basta una capacidad válida; la descripción local no se trata como una lista exhaustiva.

Veredictos: correcta (1 punto), parcial (0,5), incorrecta (0) y por revisar (`no_evaluable`). Los casos inciertos se excluyen del denominador. La aplicación calcula la puntuación; el modelo no la asigna. Se comprueba que la respuesta estructurada cubra exactamente todos los IDs enviados, sin repeticiones ni preguntas ajenas. Una respuesta incompleta no genera notas inventadas.

La IA puede cometer errores, especialmente con alias poco documentados o poderes secundarios. Sus explicaciones y referencias son generadas por el modelo; no son citas oficiales ni una búsqueda web en tiempo real. Los resultados automatizados de prueba no demuestran exactitud semántica real de Gemini. Conviene comprobar manualmente nombres alternativos, descripciones equivalentes e instrucciones incrustadas durante la sustentación.

### Formato de la evaluación y errores

`conocimiento-v2` pide explicaciones y referencias concisas. La solicitud usa un esquema JSON explícito sencillo (objeto, lista, campos obligatorios y veredictos). Las restricciones más detalladas de longitud/cantidad, campos extra y correspondencia de IDs permanecen en la validación local Pydantic. Se inspecciona también la finalización de la respuesta: una salida cortada por límite de tokens, JSON ausente/inválido, rechazo de solicitud y salida que incumple el contrato generan mensajes distintos. Ninguno provoca reintentos automáticos.

Este ajuste responde al fallo genérico comunicado por el usuario en Nombres. No se conservó la excepción original, por lo que no está confirmada su causa concreta. La reproducción con transporte simulado permite verificar el adaptador y los nuevos mensajes, pero no confirma por sí sola que Gemini acepte una solicitud real. No se modifican clave, modelo ni facturación. Si el servidor mantiene módulos anteriores cargados, reinícialo; una sesión nueva pierde la ronda anterior.

## Alias iniciales y fuentes

Los 63 nombres españoles y originales ya están en el catálogo. Además, `conocimiento.ALIAS` incorpora equivalencias iniciales para las fichas con nombres históricos:

- Blitzwolfer: Benwolf / Ben Wolf / Ben Lobo. [Referencia](https://ben10.fandom.com/wiki/Blitzwolfer).
- Snare-oh: Momia / Ben Momia / Benmummy / Ben Mummy. [Referencia](https://ben10.fandom.com/wiki/Snare-Oh).
- Frankentrueno: Benvicktor / Ben Viktor. [Referencia](https://ben10.fandom.com/wiki/Frankenstrike).
- Bátore: Megawatt / Megawatts. Se acepta como denominación común solicitada por el usuario para jugar; no se presenta como nombre propio canónico exclusivo de la transformación. La especie sigue siendo Nosedeenian. [Referencia del alien](https://ben10.fandom.com/wiki/Buzzshock_%28Classic%29).

Es una lista inicial orientativa, no una lista cerrada de respuestas válidas. La IA puede reconocer otros alias; si no puede verificarlos con confianza, el prompt pide marcarlos por revisar. Las referencias son fuentes comunitarias secundarias; sus contenidos se consultaron mediante índices de búsqueda cuando Fandom bloqueó la apertura directa. Las [fuentes de especies](ESPECIES.md) y los nombres originales permiten contrastar las fichas.

## Datos y coste

La ronda, respuestas y evaluación viven en `st.session_state`; no se añaden a `opiniones.json` ni se guardan permanentemente. Una sesión nueva o el reinicio del servidor puede perderlos. Generar preguntas, mostrar imágenes, avanzar el reloj y enviar respuestas durante el juego no consumen cuota de IA. Evaluar o reintentar sí consume la cuota del proyecto Gemini Free Tier configurado; el programa no activa facturación ni utiliza otro proveedor como alternativa.

Código: `conocimiento.py` (banco, prompt, contrato, evaluación y puntuación) e `interfaz_conocimiento.py` (menú, formulario, reloj y resultados). El reloj usa un fragmento de Streamlit que se actualiza cada segundo sin reconstruir el formulario.

Las pruebas unitarias y de interfaz están en `tests/test_conocimiento.py`. La revisión de navegador debe ejecutarse **exclusivamente** contra `tests/app_conocimiento_visual.py`, que identifica las correcciones simuladas y permite adelantar el tiempo sin esperar un minuto. Ese servidor no es la aplicación de entrega.

```powershell
.\.venv\Scripts\python.exe -m streamlit run tests/app_conocimiento_visual.py --server.address 127.0.0.1 --server.port 54167 --browser.gatherUsageStats false
```

En otra terminal, con Playwright Core y un navegador compatible preparados según `tests/verificar_conocimiento.cjs`:

```powershell
node tests/verificar_conocimiento.cjs http://127.0.0.1:54167 --simulado
```
