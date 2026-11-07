"""Reproduce persistencia y consulta con datos manuales, sin API ni datos de uso."""

from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile


RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from almacenamiento import cargar_opiniones, consultar_opiniones, guardar_opinion


def generar():
    fuente = RAIZ / "datos/ejemplos/opiniones_demo.json"
    uso = RAIZ / "datos/opiniones.json"
    anterior_uso = uso.read_bytes() if uso.exists() else None
    registros = cargar_opiniones(fuente)
    if len(registros) < 12 or any(r["modelo"] != "manual:no-ejecutado" for r in registros):
        raise ValueError("Se requieren al menos doce registros de demostración identificados como manuales.")

    with tempfile.TemporaryDirectory(prefix="omnitrix-evidencia-") as carpeta:
        ruta = Path(carpeta) / "opiniones.json"
        for registro in registros:
            guardar_opinion(ruta, registro)
        antes_reintento = ruta.read_bytes()
        codigo = (
            "import sys,json; sys.path.insert(0,sys.argv[1]); "
            "from almacenamiento import cargar_opiniones; "
            "print(json.dumps(cargar_opiniones(sys.argv[2])))"
        )
        proceso = subprocess.run(
            [sys.executable, "-c", codigo, str(RAIZ), str(ruta)], cwd=carpeta,
            capture_output=True, text=True, encoding="utf-8", timeout=30, check=True,
        )
        recuperados = json.loads(proceso.stdout)
        if recuperados != registros:
            raise ValueError("La lectura desde otro proceso no coincide con los datos guardados.")
        nuevos_al_reintentar = sum(guardar_opinion(ruta, r) for r in registros)
        if nuevos_al_reintentar or ruta.read_bytes() != antes_reintento:
            raise ValueError("Los reintentos modificaron el archivo.")

    filtrados = consultar_opiniones(recuperados, "a003", "mixto")
    if len(filtrados) != 1:
        raise ValueError("La selección de referencia debe contener una opinión mixta de XLR8.")
    if (uso.read_bytes() if uso.exists() else None) != anterior_uso:
        raise ValueError("El archivo de uso cambió durante la comprobación.")

    evidencia = {
        "fecha_ejecucion_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version.split()[0],
        "origen": "Datos y análisis preparados manualmente; persistencia y filtros ejecutados realmente. Sin llamadas a API.",
        "fuente": "datos/ejemplos/opiniones_demo.json",
        "registros_guardados": len(registros),
        "registros_recuperados_en_otro_proceso": len(recuperados),
        "lectura_identica": recuperados == registros,
        "registros_nuevos_al_reintentar": nuevos_al_reintentar,
        "archivo_uso_sin_cambios": True,
        "filtros": {"alien_id": "a003", "sentimiento": "mixto"},
        "total_filtrado": len(filtrados),
        "recuentos_filtrados": {c: Counter(r["sentimiento"] for r in filtrados)[c] for c in ("positivo", "negativo", "neutro", "mixto")},
        "ids_filtrados": [r["id"] for r in filtrados],
        "exportacion": "evidencias/consulta-xlr8-mixto.json",
    }
    destino = RAIZ / "evidencias"
    destino.mkdir(exist_ok=True)
    for nombre, datos in (
        ("persistencia-y-filtro.json", evidencia),
        ("consulta-xlr8-mixto.json", {"version": 1, "opiniones": filtrados}),
    ):
        (destino / nombre).write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Evidencias generadas: persistencia entre procesos, reintentos sin duplicados y filtro XLR8/mixto. Sin modificar opiniones de uso.")


if __name__ == "__main__":
    generar()
