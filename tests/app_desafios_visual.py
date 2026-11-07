"""Servidor exclusivo de revisión visual: evaluación explícitamente simulada, sin API.

Ejecutar con streamlit run tests/app_desafios_visual.py, nunca como entrega.
"""

from pathlib import Path
import runpy
import sys
from unittest.mock import patch

import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))


def evaluacion_simulada(alien, situacion, plan, modo="Control maestro"):
    return {
        "resultado": {
            "veredicto": "adecuado",
            "resumen": "Evaluación simulada para pruebas visuales. No se consultó Gemini.",
            "ventajas": "Texto de ejemplo para comprobar la presentación de las ventajas.",
            "riesgos": "Texto de ejemplo para comprobar la presentación de las limitaciones.",
            "resolucion": "Esta resolución es un ejemplo de prueba, no un análisis real del desafío.",
        },
        "modelo": "simulado-sin-api", "version_prompt": "prueba-visual",
    }


with patch("interfaz_desafios.evaluar_desafio", side_effect=evaluacion_simulada):
    runpy.run_path(str(RAIZ / "app.py"), run_name="__main__")
st.caption("Servidor de prueba visual: evaluaciones simuladas, sin API.")
