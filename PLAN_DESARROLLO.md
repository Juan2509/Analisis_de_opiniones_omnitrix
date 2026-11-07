# Archivo Omnitrix — plan de desarrollo por commits

## Cómo retomar en una nueva sesión

Modo adicional solicitado: Desafíos del Omnitrix implementado como tercera sección, con 12 situaciones aleatorias locales y elección entre 63 aliens. Gemini evalúa solo al pulsar Evaluar; plan opcional, estado conservado al navegar, evaluación anterior invalidada al editar y errores sin resultados inventados. Partidas de sesión separadas del JSON de opiniones. 82 pruebas aprobadas, sin llamadas reales al proveedor. Commit sugerido: `feat(desafios): agregar desafíos del Omnitrix evaluados con Gemini`.

Ampliación posterior solicitada por el usuario: catálogo de 63 fichas y 63 PNG locales. Se conservaron a001–a020 y se añadieron a021–a063, sin supremas, reboot ni fusiones; Upchuck Perk/Murk por separado y Spitter identificado como transformación de Ben 10.000. 72 pruebas aprobadas, con todos los selectores/fichas, hashes de recursos y guardado/consulta de un alien nuevo. Evidencia en `evidencias/pruebas-catalogo-ampliado-windows.txt`. Commit sugerido: `feat(catalogo): ampliar a 63 transformaciones de Ben 10`.

Actualización posterior al paso 13: adaptación a Gemini solicitada por el usuario, con condición de no pagar. `langchain-google-genai==4.4.3`, Gemini Developer API sin Vertex ni fallback, modelo `gemini-3.5-flash-lite`, configuración Google local y guía `GEMINI_GRATIS.md`. 68 pruebas aprobadas y `pip check` correcto. Solo usar clave de un proyecto Free Tier sin facturación; disponibilidad/cuota de la cuenta e inferencia real pendientes. Conservar los resultados anteriores como históricos. Commit sugerido: `feat(analisis): integrar Gemini para uso en modalidad gratuita`.

Estado más reciente (2026-11-07, Windows): paso 13 de documentación completado. README de entrega reorganizado, contexto consolidado, guía `ENTREGA.md` y evidencias reproducibles de persistencia/filtro preparadas; documentos anteriores archivados en `docs/`. Python 3.14.4 y `.venv` disponibles, 65 pruebas aprobadas en el paso 12 y `pip check` correcto. Pasos 8, 10, 11 y 12 conservan pendientes de API o revisión manual en `VERIFICACION.md`; completar la documentación no los cierra. No hubo llamadas reales al modelo. Los estados del 2026-11-06 son históricos.

1. Leer `CONTEXTO_PROYECTO.md` para conocer el alcance, la temática de Ben 10, las reglas del taller y las decisiones del usuario.
2. Leer este plan y revisar los archivos, el historial Git y los cambios sin confirmar. El historial y el código determinan qué está terminado; las casillas son una ayuda.
3. Identificar el primer paso pendiente y explicar en español qué se construirá y cómo se comprobará.
4. Implementar por etapas, revisar y verificar cada avance antes de preparar su commit.
5. Actualizar este documento con el estado real y las comprobaciones realizadas. No marcar como completado algo que solo está diseñado.

Estado verificado el 2026-11-06: pasos 1 a 6 completados. Los pasos 1 y 2 están confirmados en `e3abb73`; el catálogo del paso 3, en `ed93656`; el cargador del paso 4, en `c39644f`; la navegación del paso 5, en `f297ae7`; las fichas e imágenes del paso 6, en `dc3da8c`. Después del paso 6 se realizó un refinamiento visual solicitado por el usuario: negro predominante, verde neón/degradado y blanco, con estética futurista. Este rediseño queda pendiente de commit. El siguiente es el paso 7: captura de opiniones e historial visual. No se ha hecho commit ni push durante esta sesión.

Entorno de esta copia: `.venv` reconstruido con Python 3.10.12, dependencias instaladas e importadas y `pip check` correcto. Se ajustó `requirements.txt`: Streamlit 1.65.0 para Python 3.10 y 1.67.0 para Python 3.11+. La verificación anterior con Python 3.14.4 corresponde al equipo previo; esta interfaz se comprobó aquí con Streamlit 1.65.0. No se hicieron llamadas a la IA.

## Reglas de trabajo

- Producto: Archivo Omnitrix, una aplicación visual de opiniones sobre aliens de Ben 10.
- Base propuesta: Python, Streamlit, LangChain, Pydantic y archivos JSON.
- Interacción desde navegador e inicio gráfico; no exigir comandos al usuario para utilizar la entrega.
- Cada commit debe contener un cambio coherente y describir trabajo realmente realizado.
- Incluir un commit sugerido con Conventional Commits al comunicar cada cambio, según la preferencia del usuario. Sugerirlo no implica ejecutarlo.
- Revisar el diff y preparar solo los archivos relacionados; conservar cambios ajenos.
- No subir `.env`, claves, entornos virtuales ni archivos temporales. `.env.example` contiene marcadores.
- No afirmar que una prueba pasó si no se ejecutó. Distinguir comprobaciones locales de evaluaciones con el modelo real.
- El plan no autoriza por sí solo publicar cambios, hacer push o modificar el remoto: seguir la petición de la sesión para esas acciones.
- Evitar commits vacíos o duplicar cambios ya presentes. Ajustar el tamaño de cada etapa si hace falta.

## Plan secuencial

### 1. Documentar alcance y requisitos

- [x] Alcance y requisitos revisados en el repositorio; README de presentación preparado. La confirmación Git de estos cambios se realiza por separado.

Contenido: contexto del proyecto, adaptación del taller a Ben 10, requisitos, flujo visual y límites de alcance.

Comprobar: distingue decisiones, propuestas y trabajo pendiente; conserva los criterios de evaluación del taller.

Commit sugerido: `docs: definir alcance de Archivo Omnitrix`

Si el contexto ya está confirmado, no repetir el commit. Este plan puede incorporarse mediante `docs: agregar plan de desarrollo por commits`.

### 2. Preparar estructura y configuración

- [x] Completado y verificado: estructura, configuración y entorno aislado con dependencias instaladas.

Contenido: carpetas, dependencias, `.gitignore`, `.env.example` e instrucciones iniciales. Seleccionar un entorno aislado y comprobar compatibilidad de las versiones utilizadas.

Comprobar: credenciales y entorno virtual quedan excluidos de Git; no hay secretos en los archivos preparados.

Commit: `chore: preparar estructura y configuración del proyecto`

### 3. Crear el catálogo

- [x] Completado y verificado estáticamente: 20 aliens, cinco por cada serie, nombres latinos y sin versiones supremas.

Contenido: `datos/aliens.json` con versión, al menos 20 aliens, IDs estables y únicos, nombres y descripciones breves revisadas. Definir nombres localizados y variantes para evitar duplicidades conceptuales.

Comprobar: JSON válido, catálogo suficiente e información coherente. Las rutas de imágenes son relativas al proyecto.

Commit: `feat(catalogo): agregar veinte aliens del Omnitrix`

### 4. Leer y validar el catálogo

- [x] Completado y verificado: `cargar_aliens`, errores claros y 19 pruebas automatizadas correctas con Python 3.10.12.

Contenido: carga del catálogo con validación de estructura, campos e identificadores.

Comprobar: carga válida y errores claros ante archivo ausente, JSON dañado, campos faltantes o IDs repetidos.

Commit: `feat(catalogo): validar y cargar las transformaciones`

### 5. Crear navegación y selección visual

- [x] Completado y verificado: navegación, selector de los 20 aliens, selección conservada entre secciones, tema verde y oscuro y errores de catálogo visibles.

Contenido: interfaz Streamlit con identidad visual verde y oscura, secciones Analizar opinión y Consultar archivo, selector de alien.

Comprobar: navegación y selección operativas; etiquetas legibles; las funciones pendientes no se presentan como implementadas.

Verificación: 24 pruebas correctas (19 de catálogo y 5 con AppTest), importación de dependencias y `pip check` correcto. Servidor local con HTTP 200 y revisión en Chrome a 1440 y 390 píxeles, sin desbordamiento horizontal. La consulta indica su estado pendiente; no se implementaron todavía fichas con imágenes, envío, clasificación ni persistencia. Detalles de inicio técnico en README.md; el lanzador gráfico sigue en el paso 11.

Commit: `feat(ui): crear navegación y selector de aliens`

### 6. Mostrar fichas e imágenes

- [x] Completado y verificado: fichas con nombre, alias, serie y habilidades del catálogo; 20 PNG locales y SVG alternativo ante imágenes ausentes, dañadas o ilegibles.

Contenido: imagen local, nombre y habilidades del alien seleccionado; recurso alternativo si falta una imagen. Definir y documentar origen de los recursos utilizados.

Comprobar: la ficha cambia con la selección; la ausencia de una imagen no bloquea el flujo. La ficha usa datos revisados, sin llamadas al modelo.

Preferencia confirmada: imágenes de los personajes de la serie. Se descargaron 20 diseños de Omniverse desde Ben 10 DB (Weebly), sin alterar los IDs ni la serie de introducción. La interfaz identifica el diseño mostrado. Procedencia y límites en `assets/aliens/README.md`; URLs, dimensiones y SHA-256 en `assets/aliens/fuentes.json`. Las imágenes no se descargan durante el uso de la aplicación.

Verificación: 28 pruebas correctas (19 de catálogo y 9 de interfaz/recursos), `pip check` correcto y revisión visual de los 20 PNG. Incluye cambio de ficha, archivos ausentes/dañados, permisos simulados, fuentes y hashes, y funcionamiento sin peticiones HTTP externas. Servidor con HTTP 200, PNG servido desde /media local y revisión en Chrome a 1440/390 píxeles sin desbordamiento horizontal. Pillow se declara como dependencia directa porque se usa para leer las imágenes. Las opiniones siguen pendientes.

Commit: `feat(ui): mostrar fichas e imágenes de los aliens`

Las imágenes definitivas no deben bloquear el desarrollo: puede emplearse un recurso alternativo y añadirlas en otro commit coherente.

### 7. Capturar opiniones y mantener historial visual

- [x] Completado y verificado con AppTest en el paso 12.

Implementado el 2026-11-07 y comprobado durante el paso 12: captura sin truncar, longitud tras `strip`, texto original e identidad del alien, historial al navegar y limpieza del chat sin modificar el archivo. La prueba del texto de solo espacios verifica su conservación en sesión y su presentación normalizada por Streamlit. Suite completa: 65 pruebas aprobadas.

Contenido: `st.chat_input`, `st.chat_message`, historial en `st.session_state`, asociación del envío con el alien y botón Nueva conversación.

Comprobar: longitud de 5 a 1000 caracteres después de quitar espacios exteriores, sin truncamiento silencioso. Cambiar de alien no modifica envíos anteriores. Limpiar el chat no borra datos persistentes.

Commit: `feat(chat): capturar opiniones y conservar el historial de sesión`

En esta etapa todavía no simular clasificación o confirmación de guardado. Presentar claramente el estado de desarrollo hasta integrar esas funciones.

### 8. Implementar clasificación estructurada

- [ ] Completado y verificado.

Implementado y comprobado con seis pruebas de análisis y pruebas AppTest, dentro de la suite de 65 aprobadas. Esquema estricto, `omnitrix-v1`, salida `json_schema`, errores sanitizados y análisis solo del envío actual. Incluye autenticación, cuota y tiempo de espera con dobles; no demuestra exactitud semántica. Mantener abierta la etapa hasta configurar y evaluar un modelo real. Configuración en README y `.env.example`.

Contenido: prompt system/human mediante `ChatPromptTemplate`, cadena LangChain, esquema Pydantic y `with_structured_output` con `invoke`. Configurar proveedor/modelo compatible mediante entorno.

Comprobar: categorías positivo, negativo, neutro y mixto; razón de 1 a 300 caracteres; relación coherente entre pertinencia y categoría. Analizar únicamente alien y opinión actuales, sin historial. Tratar instrucciones dentro de comentarios como datos. Mensajes ajenos y fallos no se convierten en neutro.

Commit: `feat(analisis): clasificar opiniones con salida estructurada`

Registrar qué comprobaciones usaron un modelo real. Si faltan credenciales, documentar la limitación y no presentar análisis simulados como resultados reales.

### 9. Implementar persistencia

- [x] Completado y verificado localmente en el paso 12.

Siete pruebas de almacenamiento y pruebas AppTest aprobadas; se demostró además lectura de las 16 opiniones desde otro proceso Python y otro cwd, sin duplicar reintentos. Validación, UTF-8, UUID/UTC, temporal/reemplazo, conflictos, fallos de escritura y conservación de archivos dañados comprobados. No se modificó el archivo de uso. La demostración manual con un envío de API real forma parte de la aceptación final. Alcance: un único escritor local.

Contenido: `datos/opiniones.json`, UUID, fecha UTC, alien, texto original, análisis y metadatos del modelo/prompt. Escritura UTF-8 mediante temporal en el mismo directorio y reemplazo final.

Comprobar: conserva registros tras reinicio, añade sin perder anteriores y evita duplicar el mismo envío. Conserva archivos dañados e informa errores. Confirma guardado únicamente tras escritura exitosa; mantiene la opinión visible ante fallos.

Commit: `feat(almacenamiento): guardar opiniones de forma persistente`

Alcance: un único escritor local; no afirmar soporte concurrente por utilizar reemplazo atómico.

### 10. Consultar y exportar opiniones

- [ ] Completado y verificado.

Tres pruebas de filtros y cuatro de interfaz aprobadas: tabla/recuentos/bytes exportados coherentes, consultas sin IA ni escritura, vacíos, errores y opciones actualizadas. La revisión visual y descarga real en Brave siguen pendientes: Computer Use no pudo determinar la URL y detuvo la inspección. Ver `VERIFICACION.md`.

Contenido: filtros por alien/sentimiento o todos, tabla, total, recuentos y descarga JSON.

Comprobar: todos los resultados respetan los mismos filtros; estado vacío informativo; consultas sin llamadas al modelo; reejecuciones sin duplicación de registros.

Commit: `feat(consultas): filtrar y exportar opiniones registradas`

### 11. Preparar inicio gráfico

- [ ] Completado y verificado.

Implementado para Windows y comprobado con siete pruebas Python, incluido mutex real y arranque/salud/detención de servidor real. La prueba PowerShell del VBS pasó. También se observó la ventana del controlador con dirección local y botones, HTTP 200 y título de la aplicación en Brave. Pendiente revisar la página y el clic de cierre: Computer Use detuvo esa inspección por no poder determinar la URL del navegador. El controlador abierto puede cerrarse manualmente. No se asegura portabilidad a otros sistemas.

Contenido: acceso directo o mecanismo gráfico adecuado al sistema de destino, con instrucciones claras.

Comprobar: abre la aplicación en el navegador sin escribir comandos, utiliza el entorno correcto y resuelve rutas desde el proyecto. No prometer que el mismo lanzador funciona en todos los sistemas sin comprobarlo.

Commit: `feat(inicio): agregar acceso gráfico a la aplicación`

### 12. Preparar datos y verificar aceptación

- [ ] Completado y verificado.

Datos y verificación local preparados el 2026-11-07: 16 opiniones ficticias, cuatro aliens/categorías, análisis manuales identificados y seis casos de evaluación. Python 3.14.4 local y `.venv` instalados con aprobación; `pip check` correcto. 65 pruebas aprobadas, incluidas persistencia entre procesos, errores de API simulados, mutex y servidor real. Se corrigió la validación de rutas POSIX en Windows y una aserción sobre espacios normalizados. Evidencias y reflexiones en `VERIFICACION.md`. Mantener abierta esta casilla hasta evaluar un modelo real y completar la revisión manual de navegador limitada por Computer Use. Los datos de uso no se sustituyeron por ejemplos.

Contenido: al menos 12 opiniones ficticias entre 4 aliens y las 4 categorías; pruebas relevantes y registro de resultados observados. Identificar datos de ejemplo y cualquier análisis preparado manualmente.

Comprobar: elogios, críticas, neutralidad, mixtos, ironía, pertinencia, entradas inválidas, instrucciones embebidas, persistencia, cambios de alien, limpieza del chat, errores de API/validación/escritura, JSON dañado, filtros y ausencia de duplicados.

Commit: `test: verificar los flujos y requisitos del taller`

Las pruebas se realizan también durante las etapas anteriores. Este paso consolida la evaluación completa; no posterga todas las verificaciones hasta el final. Si conviene, separar los datos ficticios en `chore(datos): agregar opiniones ficticias de demostración`.

### 13. Documentar la entrega

- [x] Documentación completada y revisada; aceptación funcional pendiente según `VERIFICACION.md`.

Preparado el 2026-11-07: README de instalación/configuración/inicio/uso/respaldo/errores, versiones y pruebas; contexto consolidado; `ENTREGA.md` para revisión y sustentación; historial anterior archivado en `docs/`. `scripts/generar_evidencias.py` reprodujo 16 registros recuperados desde otro proceso, cero duplicados al reintentar y filtro XLR8/mixto de un registro, sin API ni cambios al archivo de uso. Resultados JSON en `evidencias/` y reflexiones en `VERIFICACION.md`. Se revisaron enlaces locales y consistencia de los archivos. La suite previa de 65 pruebas no se repitió por cambios documentales. No se afirma aceptación completa: faltan modelo real y revisión manual de navegador/descarga/cierre. No hubo commit ni push automático.

Contenido: README de instalación, configuración, versiones comprobadas, inicio visual y uso; evidencias reales de persistencia y filtros; reflexión sobre dos errores o ambigüedades; contexto actualizado.

Comprobar: otra persona puede entender y reproducir la entrega. No incluir secretos en capturas; no presentar funciones o resultados pendientes como completados.

Commit: `docs: documentar instalación pruebas y entrega final`

## Conventional Commits

Formato: `tipo(alcance opcional): descripción`.

| Tipo | Uso |
| --- | --- |
| feat | Funcionalidad nueva |
| fix | Corrección de un fallo |
| docs | Documentación |
| test | Pruebas |
| chore | Configuración y mantenimiento |
| refactor | Reorganización del código sin cambiar su comportamiento |
| style | Formato del código sin cambio funcional |

Ejemplo de corrección posterior: `fix(almacenamiento): evitar duplicados al cambiar los filtros`.

No usar `style` como categoría automática de toda mejora visual: una función nueva de interfaz puede ser `feat(ui)` y un defecto visual corregido, `fix(ui)`.

## Registro para próximas sesiones

Actualizar al finalizar cada etapa con evidencia breve. No inventar hashes ni resultados.

| Fecha | Etapa | Avance real | Verificación y pendientes | Commit, si existe |
| --- | --- | --- | --- | --- |
| 2026-11-07 | Paso 13 | Guía de entrega, contexto consolidado, archivo histórico y evidencias JSON reproducibles | Generador ejecutado; enlaces/archivos revisados; conserva pendientes de API y revisión manual | Pendiente de commit |
| 2026-11-07 | Paso 12 | 16 opiniones y seis casos manuales; entorno Windows preparado; corrección de ruta POSIX | 65 pruebas aprobadas, pip check y VBS correctos; servidor/mutex reales comprobados; API y revisión manual pendientes | Pendiente de commit |
| 2026-11-07 | Paso 11 | Inicio por doble clic y ventana de control para Windows, proceso local y exclusión de duplicados | Diagnóstico VBS y prueba PowerShell correctos; Python, GUI, servidor y cierre reales pendientes | Pendiente de commit |
| 2026-11-07 | Paso 10 | Consulta visual, filtros combinados, tabla/recuentos y descarga de la misma selección | Diff correcto; siete pruebas nuevas sin ejecutar por falta de Python; revisión de navegador pendiente | Pendiente de commit |
| 2026-11-07 | Paso 9 | Registros persistentes, validación JSON, escritura atómica y reintento del mismo envío | Revisión del diff correcta; ocho pruebas añadidas sin ejecutar por falta de Python; reinicio real pendiente | Pendiente de commit |
| 2026-11-07 | Paso 8 | Clasificación estructurada, pertinencia, resultados y errores visibles; metadatos en sesión | Pruebas locales añadidas sin ejecutar; evaluación con API y configuración pendientes; no persiste opiniones | Pendiente de commit |
| 2026-11-07 | Paso 7 | Captura, validación, asociación al alien e historial temporal; limpieza del chat | Revisión del diff correcta; pruebas añadidas pero sin ejecutar por falta de Python y `.venv` en Windows | Pendiente de commit |
| 2026-11-06 | Planificación | Contexto y plan ya registrados | Historial y estado local inspeccionados; árbol limpio al iniciar | `34b28f7`, `41aeb15` |
| 2026-11-06 | Refinamiento visual solicitado | Negro predominante, verde neón/degradado y blanco; portada futurista, navegación resaltada y fichas iluminadas | 28 pruebas correctas; Chrome a 1440/390 px sin desbordamiento, navegación e imagen local comprobadas; movimiento reducido desactiva la órbita. Sigue pendiente el paso 7 | Pendiente de commit |
| 2026-11-06 | Paso 6 | Fichas del catálogo, 20 PNG locales con fuentes y alternativa SVG | 28 pruebas correctas; imágenes verificadas visualmente, hashes y dimensiones registrados, errores de imagen sin bloquear la ficha | `dc3da8c` |
| 2026-11-06 | Paso 5 | Interfaz Streamlit con dos secciones, selector, tema y selección conservada; entorno local reconstruido | 24 pruebas correctas al cerrar la etapa; `pip check` correcto, HTTP 200 y Chrome a 1440/390 px | `f297ae7` |
| 2026-11-06 | Paso 4 | Cargador UTF-8 con validación de versión, estructura, campos, IDs y rutas de imágenes | 19 pruebas correctas al cerrar la etapa. Incluye errores de lectura, archivos dañados conservados y carga desde otro directorio | `c39644f` |
| 2026-11-06 | Paso 3 | Catálogo con nombres latinos, cuatro series y sin formas supremas | JSON válido, 20 registros únicos, cinco por serie; imágenes null | `ed93656` |
| 2026-11-06 | Paso 2 | Estructura, .gitignore, .env.example, dependencias y .venv | Python 3.14.4; instalación, pip check e importaciones correctas. Siguiente: catálogo | `e3abb73` |
| 2026-11-06 | Paso 1 | Alcance revisado, ruta corregida, README de presentación y seguimiento actualizados | Revisión documental; no corresponde ejecutar pruebas de aplicación. Siguiente: paso 2 | `e3abb73` |

Mensaje para retomar:

> Lee CONTEXTO_PROYECTO.md y PLAN_DESARROLLO.md. Revisa los archivos y el historial Git para identificar el primer paso pendiente de Archivo Omnitrix. Continúa por etapas, explica los cambios en español y comprueba cada avance antes de proponer su Conventional Commit.
