# Instalación y ejecución de Archivo Omnitrix

Guía actualizada el 7 de noviembre de 2026. Los comandos se ejecutan desde la carpeta que contiene `app.py` y `requirements.txt`. Sustituye las rutas de ejemplo por la ubicación real del proyecto.

## Requisitos comunes

- Proyecto completo, incluyendo carpetas ocultas como `.streamlit`, `assets`, `datos` y `sonidos`.
- Python 3.11 o posterior compatible con las dependencias fijadas. El entorno probado utiliza Python 3.14.4 en Windows. La rama de Python 3.10 en `requirements.txt` es histórica.
- Navegador con JavaScript y conexión a Internet para instalar paquetes y utilizar Gemini.
- Permiso de escritura en la carpeta `datos` para guardar opiniones.
- Una clave Gemini configurada localmente para analizar opiniones o evaluar desafíos.

El catálogo, los audios y las imágenes no necesitan descargarse durante el uso. Las consultas al modelo sí requieren conexión. Node no es necesario para utilizar el programa; se usa únicamente en revisiones de navegador opcionales.

## Windows

### Preparar Python y el entorno

Instala Python con soporte para Tkinter si utilizarás el controlador gráfico. Abre la carpeta del proyecto en VS Code y selecciona **Terminal → Nueva terminal**, con PowerShell, o abre PowerShell y entra en la carpeta:

```powershell
cd "C:\ruta\An-lisis-de-sentimientos"
py -3 --version
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

El último comando debería informar `No broken requirements found.` Si `py` no existe pero `python --version` corresponde al Python adecuado, utiliza `python -m venv .venv`. También puedes usar la ruta absoluta al intérprete instalado. Comprueba su versión antes de crear el entorno.

Si el equipo ya tiene un entorno funcional en `.venv`, puedes usarlo directamente. No recrees un entorno de otro sistema encima del existente: utiliza una copia del proyecto sin entornos y crea uno nuevo allí.

### Configurar `.env`

Solo si el archivo no existe:

```powershell
Copy-Item -LiteralPath .env.example -Destination .env
```

Abre `.env` en tu editor, completa la clave según la [sección Gemini](#gemini-en-ambos-sistemas) y guarda el archivo. El comando de copia reemplaza un archivo existente: no lo ejecutes sobre una configuración que quieras conservar.

### Abrir con doble clic

Abre **Iniciar Archivo Omnitrix.vbs**. Necesita Windows Script Host y `.venv\Scripts\python.exe`. El controlador comprueba dependencias, reserva una instancia por carpeta/sesión Windows, busca un puerto disponible y espera a que el servidor responda antes de abrir el navegador.

- **Abrir en navegador:** reabre la página sin crear otro servidor.
- **Detener y cerrar:** detiene el servidor creado por el controlador.
- Cerrar la pestaña no detiene el servidor.
- El diagnóstico del controlador se guarda en `inicio.log`.

El controlador no instala dependencias automáticamente. Si Windows bloquea VBS o no está disponible Windows Script Host, utiliza el arranque desde terminal.

### Abrir desde PowerShell

Desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Abre `http://127.0.0.1:8501`. Mantén la terminal abierta y pulsa **Ctrl+C** para detener el servidor. En este método los mensajes se ven en la terminal; `inicio.log` pertenece al controlador gráfico.

No necesitas activar el entorno ni modificar la política de ejecución de PowerShell para estos comandos: llaman directamente a su Python. Evita abrir a la vez el controlador y un servidor manual si ambos van a escribir opiniones en el mismo archivo.

## Linux

El procedimiento utiliza terminal para arrancar el servidor; el uso de la aplicación es gráfico en el navegador. El VBS y `iniciar.py` son específicos de Windows y no se utilizan aquí. Esta guía no representa una prueba integral de la versión actual en Linux: esa verificación sigue pendiente.

### Preparar Python

Comprueba la versión:

```bash
python3 --version
```

Si faltan Python, pip o `venv`, en Ubuntu con repositorios adecuados puedes preparar los paquetes así:

```bash
sudo apt update
sudo apt install python3-full python3-pip
```

`python3-full` incluye soporte para entornos virtuales en Ubuntu. En Debian o instalaciones mínimas puede instalarse el paquete `python3-venv` de la versión elegida. En otras distribuciones usa su gestor de paquetes y documentación; estos comandos `apt` no son universales. Comprueba que el intérprete elegido sea compatible, porque la versión predeterminada depende de la distribución. No sustituyas el Python del sistema para ejecutar el proyecto. Véase la [guía oficial de Ubuntu](https://ubuntu.com/developers/docs/howto/python-setup/).

### Crear un entorno local nuevo

En una copia del proyecto sin el entorno de Windows:

```bash
cd "/ruta/An-lisis-de-sentimientos"
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
```

Si utilizas un intérprete con nombre específico, como `python3.12`, úsalo en el comando de creación de `venv`. Debe estar instalado y disponer de soporte para entornos virtuales. El resto de los comandos sigue utilizando `.venv/bin/python`.

No copies `.venv`, `.python-runtime` ni ejecutables `.exe` de Windows para usarlos en Linux. Los entornos se recrean en el destino, también al cambiar la ubicación del proyecto, como explica [Python](https://docs.python.org/3.14/library/venv.html).

### Configurar y arrancar

Solo si `.env` no existe:

```bash
cp .env.example .env
```

Completa la clave en el editor. No sobrescribas un `.env` ya configurado con ese comando. Después:

```bash
.venv/bin/python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Abre `http://127.0.0.1:8501` en el navegador. La terminal muestra el estado del servidor; mantenla abierta. **Ctrl+C** detiene Streamlit. Para volver a usarlo otro día, entra en la carpeta y ejecuta de nuevo únicamente el comando de arranque; no hace falta reinstalar paquetes.

El comando fija el acceso a la máquina local. Si el puerto está ocupado, cambia `8501` por otro puerto libre, por ejemplo `8502`, y abre la dirección correspondiente. No se configura acceso desde otros equipos en esta guía.

### Activación opcional

Los comandos anteriores funcionan sin activar el entorno. Si prefieres activarlo en Bash:

```bash
source .venv/bin/activate
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Detén el servidor con Ctrl+C y ejecuta `deactivate` para salir del entorno activado. El [procedimiento oficial de Streamlit](https://docs.streamlit.io/get-started/installation/command-line) también utiliza `venv`, pip y el comando `streamlit run`.

## Gemini en ambos sistemas

En `.env`, junto a `app.py`:

```dotenv
GOOGLE_API_KEY=TU_CLAVE_DE_GOOGLE_AI_STUDIO
GEMINI_MODEL=gemini-3.5-flash-lite
GEMINI_TEMPERATURE=
```

Usa una clave de un proyecto AI Studio Free Tier sin facturación vinculada. El modelo es el preparado en el código; los demás IDs se rechazan. La disponibilidad y la cuota se comprueban en AI Studio. La app no verifica el plan de tu cuenta ni activa facturación. Instrucciones detalladas en [GEMINI_GRATIS.md](GEMINI_GRATIS.md).

Las variables del sistema prevalecen sobre `.env`; `GEMINI_API_KEY` es una alternativa a `GOOGLE_API_KEY`. No publiques credenciales. Si modificas configuración o recursos de la pantalla inicial, detén el servidor y vuelve a iniciarlo.

Para comprobar el funcionamiento real: activa el Omnitrix con dos pulsaciones, envía una opinión en Analizar opinión y revisa el guardado; después prueba una estrategia en Desafíos. En Conocimiento alienígena elige categoría, pulsa Iniciar, escribe respuestas y solicita la revisión final con IA. Cada evaluación solicitada consume cuota del mismo proyecto gratuito; el reloj y los envíos del cuestionario no consumen cuota por separado. Las pruebas automatizadas usan respuestas simuladas.

## Actualizar o trasladar el proyecto

1. Detén el servidor y respalda `datos/opiniones.json`.
2. Conserva código, catálogo, situaciones, imágenes, audios y configuración de Streamlit.
3. En otro equipo o sistema, crea un entorno nuevo y configura `.env` localmente.
4. Tras un cambio de dependencias, vuelve a instalar `requirements.txt` con el Python del entorno y ejecuta `pip check`.
5. Arranca desde la raíz del proyecto para cargar también `.streamlit/config.toml`.

La instantánea `evidencias/dependencias-windows.txt` describe el entorno comprobado de Windows. No es un archivo de dependencias universal para Linux; para una instalación nueva utiliza `requirements.txt`.

## Problemas frecuentes

| Mensaje o síntoma | Comprobación |
| --- | --- |
| `python3`, `python` o `py` no existe | Instala/configura Python y utiliza el nombre o ruta del intérprete correcto. |
| No se puede crear `venv` o falta `ensurepip` en Linux | Instala el soporte de entornos virtuales correspondiente a tu distribución y versión de Python. |
| `No module named streamlit` u otro módulo | Ejecuta pip con el Python de `.venv`, instala `requirements.txt` y revisa `pip check`. |
| `externally-managed-environment` | Instala paquetes dentro de `.venv`; no uses pip contra el Python del sistema. |
| Puerto ocupado | Detén tu servidor anterior o elige otro puerto; cambia también la URL. |
| No abre el navegador automáticamente | Abre manualmente la URL que muestra el controlador o la terminal. |
| Falta la clave o Google rechaza el acceso | Revisa `.env`, variables del sistema, clave y acceso al modelo. |
| Límite de uso/cuota | Espera el restablecimiento indicado por el proveedor; no habilites pagos para resolverlo. |
| No se oye el sonido | Comprueba volumen y permisos del sitio; la primera pulsación reproduce `core-ready` y la segunda la transformación. |
| Cambios de la entrada no aparecen | Detén y reinicia el servidor para volver a registrar el componente. |
| Falta una imagen | Conserva las rutas y mayúsculas/minúsculas; Linux distingue ambas. Se mostrará una alternativa si el recurso falla. |
| No se pueden guardar opiniones | Comprueba permisos/espacio en `datos`, respaldo y validez del JSON; reintenta el mismo guardado desde la interfaz. |

Para pruebas, revisión visual y alcance de compatibilidad, consulta [DESARROLLO.md](DESARROLLO.md) y [VERIFICACION.md](VERIFICACION.md).
