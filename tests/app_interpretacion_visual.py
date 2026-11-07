"""Servidor exclusivo de revisión visual, sin llamadas reales a Gemini."""

from pathlib import Path
import runpy
import sys
from unittest.mock import patch

import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))


def interpretar_simulado(catalogo, modo, respuestas, alien_id=None):
    return {"modelo": "simulado-sin-api", "version_prompt": "prueba-visual",
            "resultado": {
                "alien_principal_id": alien_id or "a005", "alien_alternativo_id": None if alien_id else "a002",
                "motivo_alternativo": None if alien_id else "Otra analogía recreativa con tus motivos; resultado simulado.",
                "resumen": "Interpretación simulada para revisar la interfaz. No se consultó Gemini.",
                "valores": "Ejemplo de valores vinculados a tus motivos, sin una conclusión psicológica.",
                "estilo_heroe": "Un estilo de héroe ilustrativo para comprobar la presentación.",
                "conexiones": [{"respuesta_id": r["id"], "interpretacion": "Conexión de ejemplo con la respuesta escrita."} for r in respuestas],
                "limites": "Datos de prueba; no describen la personalidad real del jugador.",
                "pregunta_reflexion": "¿Qué otra forma de colaborar te gustaría explorar?",
            }}


with patch("interfaz_interpretacion.interpretar", side_effect=interpretar_simulado):
    runpy.run_path(str(RAIZ / "app.py"), run_name="__main__")
st.caption("Servidor visual de interpretación: IA simulada, sin API.")
