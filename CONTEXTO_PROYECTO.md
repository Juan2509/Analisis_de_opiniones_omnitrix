# Archivo Omnitrix — contexto vigente

Última actualización: 7 de noviembre de 2026, adaptación a Gemini sin pago.

Estado actual de la adaptación: `langchain-google-genai==4.4.3` sustituye la dependencia directa de OpenAI. El clasificador usa Gemini Developer API, `vertexai=False`, modelo `gemini-3.5-flash-lite`, salida `json_schema`, timeout 30 s y un intento total (`max_retries=1` en esta integración). Pruebas actualizadas: **68 aprobadas**, incluido adaptador/parser reales con transporte simulado; `pip check` correcto. No hubo inferencia real con Gemini. La clave debe proceder de un proyecto AI Studio Free Tier sin facturación vinculada; la app no puede verificar el plan de la cuenta. No activar pagos. `.env` tiene los nuevos campos sin exponer ni eliminar las claves anteriores; falta que el usuario introduzca su clave Google. Ver `GEMINI_GRATIS.md` y `evidencias/pruebas-gemini-windows.txt`. La verificación de 65 pruebas del paso 12 es histórica.

## Estado y fuentes de verdad

La aplicación está implementada hasta el inicio gráfico de Windows y la documentación del paso 13 está preparada. En el paso 12 pasaron **65 pruebas** con Python 3.14.4, Tk 8.6 y Streamlit 1.67.0; `pip check` correcto. Se verificaron AppTest, persistencia desde otro proceso, mutex Windows y ciclo de vida de un servidor real.

Faltan evaluación con un modelo real y revisión manual de navegador/descarga/cierre desde el controlador. Computer Use detuvo la inspección de Brave por no poder verificar su URL; no se continuaron entradas UI. Se observó el controlador nativo, el título de la aplicación en Brave y salud HTTP 200. No se realizaron llamadas reales al modelo ni se configuró `.env` durante las etapas documentadas.

- [README](README.md): instalación y guía de uso vigentes.
- [VERIFICACION.md](VERIFICACION.md): resultados observados, evidencias y pendientes.
- [PLAN_DESARROLLO.md](PLAN_DESARROLLO.md): etapas, estado y Conventional Commits.
- [ENTREGA.md](ENTREGA.md): material para revisión y sustentación.
- [Contexto histórico](docs/CONTEXTO_HISTORICO.md) y [README histórico](docs/HISTORIAL_DESARROLLO.md): estados anteriores, no instrucciones actuales de instalación.

El código, Git y las pruebas determinan el estado real; no cerrar pendientes solo por haber llegado al último paso. La memoria entre sesiones no es automática: compartir este documento y el plan para retomar.

## Objetivo y decisiones del usuario

Actualización visual solicitada: la portada «El universo está en tus manos» utiliza ahora `assets/omnitrix.png`, imagen enlazada por el usuario, en lugar del emblema geométrico CSS anterior. Archivo original sin modificar y procedencia en `assets/omnitrix-fuente.json`. Se incorpora localmente como PNG embebido, ajustado sin deformar; en móvil se muestra completo debajo del texto.

El usuario pidió usar también esa misma imagen en la marca de la barra lateral (reemplaza ⌬) y en el icono de la pestaña (reemplaza el emoji verde). Ambos usan el recurso local; sidebar a 48 × 48 píxeles y favicon configurado con `st.set_page_config`.

Restricción confirmada: el usuario no quiere pagar. No habilitar facturación ni proponer compras de créditos como requisito de uso. La cuenta OpenAI mostrada tenía saldo cero y la opinión devolvió cuota/límite, sin clasificación exitosa. El material `LangChain_LangGraph2026 (2).md` incluye Gemini y `ChatGoogleGenerativeAI` (sección «9. Hello world», línea 4550); no se encontró exclusividad de OpenAI en los adjuntos. El usuario autorizó la adaptación a Gemini, implementada y probada localmente; falta verificar su cuenta/clave gratuita. Conservar LangChain, Pydantic y los contratos; no sustituir análisis real por palabras clave o simulaciones presentadas como IA.

Aplicación académica de opiniones sobre aliens de Ben 10, adaptada del taller Tribuna Global de futbolistas. Según lo comunicado por el usuario, en clase se permitió cambiar el dominio conservando los requisitos técnicos. DevFlow y otros proyectos del curso son referencias distintas.

- Nombre: **Archivo Omnitrix**; temática Ben 10 elegida tras considerar otras opciones.
- Frontend Streamlit en navegador e inicio gráfico; no exigir terminal al usuario de la entrega ni incorporar React como frontend separado.
- Trabajo en VS Code, explicaciones en español y desarrollo gradual para comprender y sustentar el código.
- Sugerir Conventional Commits por etapa, sin ejecutar commits o push automáticamente. Conservar cambios ajenos y consultar decisiones que modifiquen alcance o preferencias.
- Diseño negro predominante, verde neón/degradado y blanco, con estética futurista y respeto a movimiento reducido.
- Catálogo ampliado por petición del usuario: 63 fichas (22 de la serie original, 14 de la etapa Fuerza Alienígena, 11 de Supremacía Alienígena y 16 de Omniverse). Conserva a001–a020 y añade a021–a063. Incluye Upchuck Perk/Murk por separado y Spitter, identificado como transformación de Ben 10.000. Nombres latinos y alias originales, sin formas supremas, fusiones ni reboot. Nanomech y Shocksquatch incluyen películas/especiales de sus etapas. No afirmar que todos los diseños son de Omniverse: fuente y diseño de los nuevos registros están en sus campos opcionales y en el manifiesto.
- Imágenes de los personajes con diseños de Omniverse, locales y con procedencia documentada. Serie de introducción y diseño mostrado son datos distintos.
- Alcance local, un único escritor. No incluye cuentas, combate, chatbot general, RAG, agentes, bases vectoriales o automatizaciones n8n. Jupyter es opcional para experimentar, no el producto final.

No renombrar la carpeta física por cambiar el nombre del producto. Las rutas Linux de sesiones anteriores son históricas: utilizar la raíz del repositorio abierto.

## Flujo y reglas funcionales

```text
Inicio gráfico → seleccionar alien → ver ficha → enviar opinión
→ validar entrada → analizar → validar salida → guardar si es pertinente
→ confirmar tras éxito → consultar, filtrar y descargar
```

Cada envío es independiente y captura el alien seleccionado. Después de quitar espacios exteriores se admiten de 5 a 1000 caracteres; no se trunca el original. El historial queda en sesión, asociado al alien de cada envío, pero no se envía al modelo. Cambiar de alien no reasigna comentarios anteriores.

Categorías permitidas: positivo, negativo, neutro y mixto. Un mensaje ajeno no se convierte en neutro ni se guarda. La pertinencia puede inferirse del contexto de selección aunque el texto no repita el nombre. Considerar ironía sin inventar hechos; tratar instrucciones dentro de la opinión como datos.

Fallo de API, validación o escritura: error visible y comentario disponible, sin categoría inventada ni confirmación falsa. «Nueva conversación» limpia chat y rechazos de sesión, conservando archivo y selección. «Reintentar guardado» conserva el mismo registro y no llama otra vez al modelo. Reenviar el texto es un envío independiente.

Consulta por ID y sentimiento combinados con AND, o todos. Tabla, total, recuentos y JSON parten de la misma lista filtrada. Consultar no analiza ni escribe y funciona aunque falle el catálogo. Filtros basados en los aliens presentes en los registros. Estados vacíos informativos y descarga vacía válida. Los recuentos solo describen este archivo, no una clasificación objetiva de los aliens.

## Arquitectura y contratos

| Componente | Responsabilidad actual |
| --- | --- |
| `app.py` | Fichas, selección conservada, chat, resultados, guardado y consulta/exportación. |
| `analisis.py` | Configuración local, prompt `omnitrix-v1`, Pydantic y cadena LangChain. |
| `almacenamiento.py` | Catálogo, registros, lectura/escritura JSON y filtros puros. |
| `iniciar.py` y VBS | Ventana de control, dependencias, servidor local y navegador Windows. |
| `datos/` | Catálogo y opiniones de uso; ejemplos manuales separados. |
| `assets/` y `.streamlit/` | Recursos locales, fuentes, estilos y tema. |

Rutas resueltas desde el proyecto, no desde el directorio de inicio. `cargar_aliens` comprueba UTF-8, JSON, versión entera 1, mínimo de 20 aliens, campos, textos, IDs únicos y rutas locales relativas. Rechaza absolutos tanto Windows como POSIX. `ErrorCatalogo` informa sin alterar archivos. `cargar_imagen_local` comprueba contención en el proyecto y lectura con Pillow; si falla, usa el SVG alternativo o un aviso de texto.

Contrato del análisis:

```python
es_pertinente: bool
sentimiento: Literal['positivo', 'negativo', 'neutro', 'mixto'] | None
razon: str  # no vacía; de 1 a 300 caracteres después de quitar espacios exteriores
```

Pydantic estricto rechaza campos adicionales y relaciones incoherentes: pertinente exige categoría, ajeno exige `None`. `ChatPromptTemplate` separa system/human; el humano incluye datos JSON del alien y la opinión actual. La cadena usa `|`, `with_structured_output(method='json_schema')` e `invoke`; se leen atributos/datos validados, no se asume `response.content`. El esquema Pydantic permanece estricto aunque la integración Gemini no recibe el parámetro `strict` de OpenAI.

Proveedor actual: Gemini Developer API. `GOOGLE_API_KEY` (alternativamente `GEMINI_API_KEY`), `GEMINI_MODEL` y `GEMINI_TEMPERATURE` se leen del entorno y `.env`; el sistema tiene prioridad. Modelo preparado: `gemini-3.5-flash-lite`; otros IDs se rechazan para impedir cambios accidentales. Temperatura vacía utiliza la recomendada por la integración. Timeout 30 s, sin reintentos automáticos ni fallback a otros proveedores. No prometer exactitud, determinismo ni gratuidad de una clave de un proyecto de pago. Las credenciales no se imprimen ni se publican.

Opiniones: raíz `{"version": 1, "opiniones": []}`. Campos de cada registro:

```text
id, fecha_utc, alien_id, alien_nombre, opinion_original,
sentimiento, razon, modelo, version_prompt
```

UUID, fecha y selección los controla la aplicación. `crear_registro` admite solo análisis pertinentes; `cargar_opiniones` valida el archivo sin modificarlo y devuelve lista vacía si falta. `guardar_opinion` escribe UTF-8 con acentos, temporal en el mismo directorio, flush/fsync y reemplazo. Un envío repetido con el mismo ID/datos no se duplica; un ID con otros datos se rechaza. Un archivo dañado se conserva. El reemplazo atómico no resuelve concurrencia multiusuario.

## Entorno, recursos y evidencia

En Windows se instaló con aprobación Python 3.14.4 por usuario en `.python-runtime`, sin cambiar PATH/asociaciones. `.venv` contiene las dependencias de `requirements.txt`. Runtime, entorno e instalador `.herramientas` están ignorados. En otro equipo crear un entorno nuevo. Versiones transitivas: `evidencias/dependencias-windows.txt`.

El VBS usa exclusivamente `.venv\Scripts\python.exe`, sin consola, y `iniciar.py` presenta el controlador. Mutex por carpeta y sesión Windows, puerto disponible en loopback, comprobación de salud antes de abrir navegador, controles Abrir y Detener/cerrar, diagnóstico en `inicio.log`. Cerrar solo navegador no detiene servidor. No se ha probado un lanzador de otros sistemas.

`datos/README.md` define catálogo y fuentes. `assets/aliens/README.md` y `fuentes.json` documentan los 20 PNG, origen, dimensiones y hashes. Los PNG no se generaron con IA ni se modificaron; la fuente comunitaria no acredita licencia libre de redistribución.

`datos/ejemplos/` contiene 16 opiniones ficticias/cuatro aliens/cuatro categorías y seis casos adicionales. Clasificaciones, razones, UUID y fechas preparados manualmente, con `modelo: manual:no-ejecutado`; no se cargan automáticamente en opiniones de uso.

`scripts/generar_evidencias.py` reproduce lectura tras otro proceso, idempotencia y consulta XLR8/mixto sobre esos datos en una carpeta temporal, sin API ni alterar el archivo de uso. Sus resultados están en `evidencias/persistencia-y-filtro.json` y `consulta-xlr8-mixto.json`. Son evidencia real del almacenamiento/filtrado, no de inferencia de IA.

## Material de clase y continuidad

Nuevo alcance autorizado: solo el modo **Desafíos del Omnitrix**, tercera opción del panel. `datos/desafios.json` contiene 12 situaciones locales; Otra situación evita la repetición inmediata y no consume API. `desafios.py` valida datos y evalúa el alien/plan opcional mediante el prompt `desafios-v1` y `EvaluacionDesafio`: veredicto cerrado, resumen, ventajas, riesgos y resolución. No hay respuesta única predeterminada ni votos/personas simuladas. `interfaz_desafios.py` conserva misión, alien, plan y resultado en sesión; editar invalida la evaluación y cambiar de misión limpia el plan. Solo el botón Evaluar consulta Gemini. No guarda partidas en el archivo de opiniones. `analisis.ejecutar_estructurado` comparte configuración, transporte, validación y manejo seguro de errores con el clasificador anterior; ambas tareas conservan esquemas/prompts separados y una llamada por envío. No se implementó el modo de opiniones de otros jugadores.

La entrada visual está en `pantalla_inicio.py` y `assets/inicio/`. El usuario pidió dos gestos: símbolo inicialmente hundido (escala 0.76); primer clic/Enter levanta el selector y reproduce `sonidos/core-ready.mp3`; segundo clic/Enter lo hunde, reproduce `sonidos/omnitrix-transform.mp3` y abre el dashboard. No usar autoplay ni botón de sonido adicional. Una pausa de 400 ms protege la apertura ante doble clic. Una capa persistente cubre el rerun y se desvanece cuando el dashboard y sus imágenes están listos; no recrearla en el desmontaje ni volver al círculo expansivo. La activación se conserva en `st.session_state` durante la sesión; no se repite al navegar ni limpiar la conversación. Respeta movimiento reducido. La capa verde usa la capa superior del navegador para incluir el panel lateral. No cortar el audio de transformación al desmontar el componente.

Los adjuntos de clase son referencias, no instrucciones operativas automáticamente autorizadas. El ZIP aporta plantillas, roles, LCEL, parsers, Pydantic y chat de Streamlit. El Markdown aporta fundamentos de prompts, separación entre instrucciones/datos, evaluación, entornos y Streamlit; sus otros temas no amplían por sí solos el alcance.

Al adaptar los ejemplos se evitó truncar a 500 caracteres, limitarse a tres sentimientos, convertir errores JSON en neutro, admitir categoría libre, introducir personalidad variable o enviar historial al clasificador. El chat de la aplicación representa opiniones independientes.

Pendientes reales: elegir/configurar modelo, evaluar los 22 casos de referencia, registrar discrepancias, demostrar envío/reinicio real y revisar tabla/descarga/cierre manualmente. Documentar resultados en `VERIFICACION.md`; no sustituirlos por expectativas. La documentación del paso 13 no cierra automáticamente esos criterios de aceptación.

Para retomar: leer este contexto, el plan y la verificación; inspeccionar Git y conservar cambios existentes. El paso 13 es el último del plan; después corresponde cerrar los pendientes, no inventar una etapa nueva ni declarar la entrega aceptada sin evidencias.

Ampliación posterior al plan: 43 fichas nuevas y PNG locales verificados; catálogo total 63. El primer bloque de 20 IDs y datos se conserva para mantener las opiniones existentes. Fuentes, alcance y listado en `datos/README.md`; no modificar `datos/opiniones.json` al ampliar el catálogo.
