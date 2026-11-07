"""Aceptación con datos manuales y procesos reales; no evalúa semántica de un LLM."""

from collections import Counter
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from almacenamiento import RAIZ_PROYECTO, cargar_aliens, cargar_opiniones, consultar_opiniones, guardar_opinion


class PruebasAceptacion(unittest.TestCase):
    def setUp(self):
        self.registros = cargar_opiniones("datos/ejemplos/opiniones_demo.json")

    def test_datos_ficticios_cubren_cuatro_aliens_y_categorias(self):
        catalogo = {alien["id"]: alien for alien in cargar_aliens()}
        self.assertEqual(len(self.registros), 16)
        self.assertEqual(len({r["alien_id"] for r in self.registros}), 4)
        self.assertEqual(Counter(r["sentimiento"] for r in self.registros), {
            "positivo": 4, "negativo": 4, "neutro": 4, "mixto": 4,
        })
        for registro in self.registros:
            self.assertEqual(registro["alien_nombre"], catalogo[registro["alien_id"]]["nombre"])
            self.assertEqual(registro["modelo"], "manual:no-ejecutado")
            self.assertEqual(registro["version_prompt"], "demo-manual-v1")

    def test_persistencia_tras_terminar_y_abrir_otro_proceso(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "opiniones.json"
            for registro in self.registros:
                guardar_opinion(ruta, registro)
            # Otra ejecución de Python lee el disco desde un cwd distinto.
            codigo = (
                "import sys,json; sys.path.insert(0,sys.argv[1]); "
                "from almacenamiento import cargar_opiniones; "
                "print(json.dumps(cargar_opiniones(sys.argv[2])))"
            )
            resultado = subprocess.run(
                [sys.executable, "-c", codigo, str(RAIZ_PROYECTO), str(ruta)],
                cwd=carpeta, capture_output=True, text=True, encoding="utf-8",
                timeout=30, check=True,
            )
            self.assertEqual(json.loads(resultado.stdout), self.registros)
            # Reintentar los mismos envíos no cambia el contenido.
            anterior = ruta.read_bytes()
            for registro in self.registros:
                self.assertFalse(guardar_opinion(ruta, registro))
            self.assertEqual(ruta.read_bytes(), anterior)

    def test_filtros_y_exportacion_reutilizan_registros_completos(self):
        filtrados = consultar_opiniones(self.registros, "a003", "mixto")
        self.assertEqual(len(filtrados), 1)
        exportados = json.loads(json.dumps({"version": 1, "opiniones": filtrados}, ensure_ascii=False))
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "seleccion.json"
            ruta.write_text(json.dumps(exportados, ensure_ascii=False), encoding="utf-8")
            self.assertEqual(cargar_opiniones(ruta), filtrados)

    def test_casos_de_evaluacion_tienen_expectativas_coherentes_y_no_resultados_reales(self):
        corpus = json.loads((RAIZ_PROYECTO / "datos/ejemplos/casos_evaluacion.json").read_text(encoding="utf-8"))
        self.assertIn("manualmente", corpus["origen"])
        self.assertEqual(len({c["id"] for c in corpus["casos"]}), 6)
        ids = {a["id"] for a in cargar_aliens()}
        for caso in corpus["casos"]:
            self.assertIn(caso["alien_id"], ids)
            self.assertTrue(5 <= len(caso["texto"].strip()) <= 1000)
            esperado = caso["esperado"]
            self.assertEqual(esperado["es_pertinente"], esperado["sentimiento"] is not None)
            self.assertNotIn("resultado_obtenido", caso)


if __name__ == "__main__":
    unittest.main()
