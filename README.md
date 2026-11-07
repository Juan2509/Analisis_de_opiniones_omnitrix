# Archivo Omnitrix

Aplicación académica de Ben 10 para explorar **63 transformaciones**, analizar opiniones con Gemini y resolver **32 situaciones** en tres submodos de desafíos. La interfaz funciona en el navegador y utiliza Python, Streamlit, LangChain, Pydantic y archivos JSON locales.

Actualizado el 7 de noviembre de 2026.

## Documentación

| Guía | Contenido |
| --- | --- |
| [Instalación y ejecución](INSTALACION.md) | Windows, Linux, comandos, configuración, puertos y problemas frecuentes. |
| [Gemini sin pago](GEMINI_GRATIS.md) | Clave de AI Studio, proyecto gratuito y límites de uso. |
| [Desarrollo y arquitectura](DESARROLLO.md) | Módulos, contratos, datos, pruebas y ampliaciones. |
| [Verificación](VERIFICACION.md) | Resultados comprobados, evidencias y pendientes. |
| [Entrega y sustentación](ENTREGA.md) | Requisitos académicos, demostración y material de entrega. |
| [Catálogo y situaciones](datos/README.md) | Lista de los 63 aliens y alcance de las 32 misiones. |
| [Contexto](CONTEXTO_PROYECTO.md) y [plan](PLAN_DESARROLLO.md) | Estado vigente, decisiones y continuidad. |

## Qué incluye

- Pantalla inicial del Omnitrix con dos pulsaciones, sonidos locales y transición verde que cubre el dashboard y el panel lateral.
- Catálogo con imágenes, habilidades, nombres latinos/originales y serie de introducción.
- Análisis de opiniones: positivo, negativo, neutro o mixto, con una justificación breve.
- Guardado local, consulta, filtros, recuentos y descarga JSON de opiniones.
- Desafíos de combate, seguridad, rescate y resolución creativa; incluyen escenarios originales con Vilgax y otros villanos.
- Tres submodos: **Control maestro**, **Héroe bajo presión** y **Adaptabilidad**.

Se adapta el taller de opiniones sobre futbolistas a Ben 10; según lo comunicado por el estudiante, en clase se permitió cambiar el tema manteniendo los requisitos técnicos. Los desafíos y la presentación audiovisual son ampliaciones posteriores.

## Windows: inicio rápido

Desde PowerShell, en una copia del proyecto sin entorno preparado:

```powershell
cd "C:\ruta\An-lisis-de-sentimientos"
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

Configura `.env` como se explica más abajo. Después abre [Iniciar Archivo Omnitrix.vbs](<Iniciar Archivo Omnitrix.vbs>) con doble clic. El controlador abre el navegador y ofrece **Abrir en navegador** y **Detener y cerrar**. Cerrar solo la pestaña no detiene el servidor.

También puedes arrancar desde PowerShell:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Abre `http://127.0.0.1:8501`. Si arrancaste desde terminal, detén el servidor con **Ctrl+C**. La [guía detallada](INSTALACION.md) explica cómo preparar Python y qué hacer si `py` no está disponible.

## Linux: inicio desde terminal

La aplicación principal está preparada con rutas portables; la versión actual **todavía no tiene una verificación integral en Linux**. El VBS y `iniciar.py` utilizan funciones de Windows. En Linux se propone iniciar Streamlit directamente y utilizar la misma interfaz en el navegador.

Con Python compatible instalado, desde una copia sin entorno de Windows:

```bash
cd "/ruta/An-lisis-de-sentimientos"
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
```

Configura `.env` y arranca:

```bash
.venv/bin/python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Abre `http://127.0.0.1:8501` y mantén la terminal abierta. **Ctrl+C** detiene el servidor. No se necesita activar el entorno porque se llama a su intérprete directamente. Consulta [instalación Linux](INSTALACION.md#linux) para paquetes de Ubuntu/Debian, activación opcional y resolución de errores.

Utiliza Python **3.11 o posterior compatible con las versiones fijadas**; el entorno comprobado es Windows con Python **3.14.4** y Streamlit **1.67.0**. `requirements.txt` conserva una rama histórica para Python 3.10, que no se volvió a validar con todas las ampliaciones. Crea un entorno nuevo al cambiar de sistema o ubicación: `.venv` y `.python-runtime` de Windows no se trasladan a Linux.

## Configuración de Gemini

Si `.env` no existe, copia `.env.example` con ese nombre en la raíz y completa:

```dotenv
GOOGLE_API_KEY=TU_CLAVE_DE_GOOGLE_AI_STUDIO
GEMINI_MODEL=gemini-3.5-flash-lite
GEMINI_TEMPERATURE=
```

El modelo indicado es el ID fijado en el código; no hay cambio automático de modelo o proveedor. La temperatura vacía deja el valor predeterminado de la integración. También se acepta `GEMINI_API_KEY` como alternativa; las variables del sistema prevalecen sobre `.env`.

Usa una clave de un proyecto **Free Tier sin facturación vinculada**, conforme a la [guía gratuita](GEMINI_GRATIS.md). La aplicación no verifica el plan de la cuenta. Las cuotas y la disponibilidad dependen del servicio: no se promete uso ilimitado ni se habilitan pagos desde el programa. Las antiguas claves de OpenAI se ignoran.

El catálogo, las fichas y las consultas locales funcionan sin clave. Analizar opiniones y evaluar estrategias requieren conexión y acceso a Gemini. La misma configuración se utiliza en Windows y Linux. `.env` está excluido de Git.

## Cómo utilizarlo

### Entrada del Omnitrix

El símbolo comienza hundido. El primer clic o Enter levanta el selector y reproduce `sonidos/core-ready.mp3`; el segundo lo presiona, reproduce `sonidos/omnitrix-transform.mp3` y muestra el dashboard mediante una transición verde continua. Ambos audios se inician con una interacción del usuario, sin botón de sonido adicional.

La entrada aparece una vez por sesión de Streamlit y respeta la preferencia de movimiento reducido. Los recursos son locales. Reinicia el servidor después de modificar los recursos del componente inicial. El volumen y los permisos de sonido del navegador pueden afectar la reproducción.

### Analizar opinión

1. Selecciona un alien y consulta su ficha.
2. Envía una opinión de **5 a 1000 caracteres**, descontando espacios exteriores.
3. Revisa sentimiento y razón. Una opinión ajena al alien se rechaza y no se guarda.
4. Comprueba el mensaje **Opinión guardada en el Archivo Omnitrix**.

Cada envío se analiza independientemente; el historial no se envía al modelo. El texto original y el alien del envío se conservan. **Nueva conversación** limpia el chat de sesión y mantiene el archivo persistente.

Si falla el análisis, no se inventa un resultado. Si falla el guardado, **Reintentar guardado** conserva el registro y no vuelve a consultar Gemini. Dos envíos independientes del mismo texto pueden producir dos registros; reintentar el mismo guardado no lo duplica.

### Desafíos del Omnitrix

Elige un submodo en el menú y pulsa **Iniciar**:

| Submodo | Aliens disponibles | Estrategia |
| --- | --- | --- |
| Control maestro | Las 63 transformaciones. | Opcional, hasta 1000 caracteres. |
| Héroe bajo presión | Tres aliens distintos al azar por ronda. | Opcional, hasta 1000 caracteres. |
| Adaptabilidad | Un único alien asignado al azar, sin selector. | Obligatoria, entre 5 y 1000 caracteres. |

En Héroe bajo presión puedes consultar las tres fichas antes de elegir, mediante pestañas con imagen, habilidades y datos de cada alien. Consultarlas no cambia el sorteo ni usa la IA.

Las **32 situaciones** se comparten entre los tres submodos. Los sorteos se conservan al editar y navegar; los aliens aleatorios no se eligen por conveniencia para la misión. Puede haber varias soluciones válidas.

Pulsa **Evaluar mi elección** o **Evaluar mi estrategia**. Gemini devuelve un veredicto, ventajas, riesgos y una posible resolución. En Adaptabilidad evalúa el aprovechamiento del alien asignado. Es una interpretación de un escenario ficticio, con posibles errores.

Una evaluación válida termina la ronda y fija la respuesta. Al final aparecen:

- **Volver a jugar:** otra situación distinta de la anterior y nuevos sorteos en los modos aleatorios.
- **Volver al menú de modos:** permite elegir submodo e iniciar otra partida.

Durante la ronda no hay botón para saltar de situación. Si la API falla, el formulario permanece disponible para corregir o reintentar. Las partidas se conservan en sesión y no se escriben en el archivo de opiniones.

### Consultar archivo

Es la última opción del panel, después de Analizar opinión y Desafíos. Filtra por alien y/o sentimiento, o selecciona Todos. La tabla, los recuentos y **Descargar resultados filtrados (JSON)** utilizan la misma selección. Consultar no llama a la IA ni escribe datos.

## Datos y recursos

| Archivo o carpeta | Contenido |
| --- | --- |
| `datos/aliens.json` | 63 fichas con IDs estables; [catálogo completo](datos/README.md). |
| `datos/desafios.json` | 32 situaciones originales, IDs d001–d032 y objetivos. |
| `datos/opiniones.json` | Opiniones pertinentes guardadas y sus metadatos. |
| `datos/ejemplos/` | 16 opiniones ficticias y seis casos de evaluación, con referencias humanas. |
| `assets/aliens/` | 63 PNG, alternativa local y [fuentes](assets/aliens/README.md). |
| `assets/omnitrix.png`, `assets/inicio/`, `sonidos/` | Símbolo, componente de entrada y dos MP3. |
| `.streamlit/config.toml` | Tema y configuración local de Streamlit. |

El catálogo cubre las cuatro series clásicas y transformaciones de películas/especiales de esas etapas. Incluye Upchuck Perk y Murk por separado y aclara el caso de Spitter con Ben 10.000. Se excluyen reboot, supremas y fusiones. Los 20 IDs iniciales se conservaron al ampliar el catálogo. Las imágenes mantienen su procedencia y sus límites de licencia; no se atribuye autoría propia.

Detén el servidor y respalda `datos/opiniones.json` antes de trasladar datos. Conserva su estructura e IDs y recrea el entorno en el destino. Los ejemplos manuales permanecen separados de las opiniones reales.

## Arquitectura y verificación

`app.py` presenta la aplicación; `analisis.py` gestiona Gemini y el análisis estructurado; `almacenamiento.py` valida y guarda JSON; `desafios.py` e `interfaz_desafios.py` implementan el juego; `pantalla_inicio.py` y sus recursos implementan la entrada. Más detalle en [DESARROLLO.md](DESARROLLO.md).

La última suite completa registrada aprobó **87 pruebas** en Windows. Después pasaron las **35 pruebas de interfaz/juego** al añadir las fichas comparables y las **15 del juego** al ampliar a 32 situaciones. La revisión de los tres submodos en escritorio/móvil usa evaluaciones explícitamente simuladas. El usuario confirmó el funcionamiento real de Gemini; todavía falta una evaluación sistemática documentada de su calidad. Consulta [VERIFICACION.md](VERIFICACION.md) para no confundir pruebas funcionales con precisión del modelo.

## Límites y pendientes

La entrega es local y admite un único escritor. No incluye cuentas, comentarios de otros jugadores ni sincronización de partidas. La persistencia JSON no proporciona concurrencia multiusuario. Las batallas son situaciones narrativas evaluadas por IA; no hay simulador de combate.

Pendientes: comprobar la versión actual en Linux, registrar resultados reales de los casos de evaluación y cerrar las evidencias manuales de descarga/reapertura/cierre del controlador. La apariencia terminada y las pruebas simuladas no sustituyen esas comprobaciones.

Los documentos de `docs/` que contienen estados previos se conservan como historial; las instrucciones actuales están en este README y en [INSTALACION.md](INSTALACION.md).
