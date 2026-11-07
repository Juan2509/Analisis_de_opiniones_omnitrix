"""Inicio gráfico de Windows. Usa solo biblioteca estándar hasta iniciar Streamlit."""

import ctypes
from ctypes import wintypes
from hashlib import sha256
from pathlib import Path
import socket
import subprocess
import sys
import time
import webbrowser
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener


RAIZ = Path(__file__).resolve().parent
RUTA_LOG = RAIZ / "inicio.log"


def tomar_instancia():
    """Retiene un mutex por carpeta del proyecto mientras viva el lanzador."""
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateMutexW.argtypes = (wintypes.LPVOID, wintypes.BOOL, wintypes.LPCWSTR)
    kernel.CreateMutexW.restype = wintypes.HANDLE
    kernel.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel.CloseHandle.restype = wintypes.BOOL
    identificador = sha256(str(RAIZ.resolve()).casefold().encode("utf-8")).hexdigest()[:24]
    handle = kernel.CreateMutexW(None, False, f"Local\\ArchivoOmnitrix_{identificador}")
    error = ctypes.get_last_error()
    if not handle:
        raise OSError("No se pudo reservar el inicio de la aplicación.")
    if error == 183:  # ERROR_ALREADY_EXISTS
        kernel.CloseHandle(handle)
        return None
    return kernel, handle


def comando_servidor(puerto: int) -> list[str]:
    """No usa shell ni interpola rutas dentro de comandos."""
    return [
        sys.executable, "-m", "streamlit", "run", str(RAIZ / "app.py"),
        "--server.address=127.0.0.1", f"--server.port={puerto}",
        "--server.headless=true", "--browser.gatherUsageStats=false",
    ]


def puerto_disponible() -> int:
    with socket.socket() as conexion:
        conexion.bind(("127.0.0.1", 0))
        return conexion.getsockname()[1]


def servidor_listo(url: str) -> bool:
    # La comprobación local no debe pasar por proxies configurados en el equipo.
    try:
        with build_opener(ProxyHandler({})).open(f"{url}/_stcore/health", timeout=0.3) as respuesta:
            return respuesta.status == 200 and respuesta.read(32).strip() == b"ok"
    except (OSError, URLError):
        return False


def detener_proceso(proceso):
    """Solo detiene el proceso creado por esta ventana, nunca un PID externo."""
    if proceso is not None and proceso.poll() is None:
        proceso.terminate()
        try:
            proceso.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proceso.kill()
            proceso.wait(timeout=5)


def main() -> int:
    import tkinter as tk
    from tkinter import messagebox, ttk

    ventana = tk.Tk()
    ventana.withdraw()
    ventana.title("Archivo Omnitrix · Inicio")
    instancia = None
    proceso = None
    registro_log = None
    try:
        esperado = RAIZ / ".venv" / "Scripts" / "python.exe"
        if Path(sys.executable).resolve() != esperado.resolve():
            messagebox.showerror("Archivo Omnitrix", "Abre Iniciar Archivo Omnitrix.vbs para usar el entorno del proyecto.")
            return 1
        instancia = tomar_instancia()
        if instancia is None:
            messagebox.showinfo("Archivo Omnitrix", "El proyecto ya tiene una ventana de inicio abierta. Usa sus botones para abrir el navegador o detenerlo.")
            return 0

        ventana.geometry("570x250")
        ventana.minsize(470, 250)
        contenedor = ttk.Frame(ventana, padding=20)
        contenedor.pack(fill="both", expand=True)
        ttk.Label(contenedor, text="Archivo Omnitrix", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        estado = tk.StringVar(value="Comprobando las dependencias del proyecto…")
        ttk.Label(contenedor, textvariable=estado, wraplength=500).pack(anchor="w", pady=(12, 8))
        ttk.Label(contenedor, text="Cerrar esta ventana detiene el servidor. Cerrar el navegador no lo detiene.", wraplength=500).pack(anchor="w")
        botones = ttk.Frame(contenedor)
        botones.pack(anchor="w", pady=16)
        abrir = ttk.Button(botones, text="Abrir en navegador", state="disabled")
        abrir.pack(side="left", padx=(0, 10))
        ttk.Button(botones, text="Detener y cerrar", command=ventana.destroy).pack(side="left")
        ventana.protocol("WM_DELETE_WINDOW", ventana.destroy)
        ventana.deiconify()
        ventana.update()

        registro_log = RUTA_LOG.open("w", encoding="utf-8")
        # Son las bibliotecas que importa la app; no se crea ningún cliente de IA.
        proceso = subprocess.Popen(
            [sys.executable, "-c", "import streamlit, PIL, dotenv, pydantic, langchain_core, langchain_google_genai; import tkinter"],
            cwd=RAIZ, stdout=registro_log, stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        puerto = puerto_disponible()
        url = f"http://127.0.0.1:{puerto}"
        fase = "dependencias"
        limite = time.monotonic() + 30
        listo = False

        def abrir_navegador():
            try:
                if not webbrowser.open(url):
                    raise OSError
            except (OSError, webbrowser.Error):
                messagebox.showwarning("Navegador", f"No se pudo abrir el navegador automáticamente. La aplicación está disponible en {url}")

        abrir.configure(command=abrir_navegador)

        def comprobar():
            nonlocal listo, proceso, fase, limite
            if fase == "dependencias":
                codigo = proceso.poll()
                if codigo is None:
                    if time.monotonic() >= limite:
                        detener_proceso(proceso)
                        estado.set("La comprobación tardó demasiado. Consulta inicio.log.")
                        messagebox.showerror("Tiempo de espera", "No se pudieron comprobar las dependencias a tiempo. Consulta inicio.log.")
                        return
                    ventana.after(200, comprobar)
                    return
                if codigo != 0:
                    estado.set("No se pudieron importar las dependencias. Consulta inicio.log.")
                    messagebox.showerror("Faltan dependencias", "Prepara .venv con requirements.txt según README.md. El diagnóstico está en inicio.log.")
                    return
                try:
                    proceso = subprocess.Popen(
                        comando_servidor(puerto), cwd=RAIZ, stdout=registro_log,
                        stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW,
                    )
                except OSError:
                    estado.set("No se pudo ejecutar Streamlit. Revisa .venv e inicio.log.")
                    messagebox.showerror("No se pudo iniciar", "No se pudo ejecutar Streamlit desde el entorno del proyecto.")
                    return
                fase = "servidor"
                limite = time.monotonic() + 45
                estado.set("Iniciando el servidor local…")
            if proceso.poll() is not None:
                estado.set("El servidor se ha detenido. Revisa inicio.log antes de volver a iniciar.")
                abrir.configure(state="disabled")
                messagebox.showerror("Servidor detenido", "Streamlit no pudo continuar. Consulta inicio.log y cierra esta ventana para volver a iniciar.")
                return
            if not listo:
                if servidor_listo(url):
                    listo = True
                    estado.set(f"Aplicación disponible en {url}")
                    abrir.configure(state="normal")
                    abrir_navegador()
                elif time.monotonic() >= limite:
                    detener_proceso(proceso)
                    estado.set("El servidor no estuvo listo a tiempo. Consulta inicio.log.")
                    messagebox.showerror("Tiempo de espera", "El servidor no respondió a tiempo. Consulta inicio.log y vuelve a iniciar.")
                    return
            ventana.after(500, comprobar)

        ventana.after(100, comprobar)
        ventana.mainloop()
        return 0
    except (OSError, subprocess.SubprocessError) as error:
        messagebox.showerror("No se pudo iniciar", f"No se pudo iniciar el servidor local. Revisa .venv y los permisos de la carpeta. Detalle: {error}")
        return 1
    finally:
        detener_proceso(proceso)
        if registro_log is not None:
            registro_log.close()
        if instancia is not None:
            instancia[0].CloseHandle(instancia[1])
        try:
            ventana.destroy()
        except tk.TclError:
            pass


if __name__ == "__main__":
    try:
        codigo_salida = main()
    except Exception:
        # También informa si Tkinter no está instalado o no puede abrir su ventana.
        ctypes.windll.user32.MessageBoxW(
            None, "No se pudo abrir el inicio gráfico. Revisa que .venv use Python de Windows con Tkinter y consulta README.md.",
            "Archivo Omnitrix", 16,
        )
        codigo_salida = 1
    raise SystemExit(codigo_salida)
