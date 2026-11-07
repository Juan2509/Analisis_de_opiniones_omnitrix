"""Servidor de revisión visual con correcciones y avance de reloj simulados."""

from pathlib import Path
import runpy
import sys
from time import monotonic
from unittest.mock import patch

import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))


def reloj_visual():
    return monotonic() + st.session_state.get("avance_reloj_visual", 0)


def evaluacion_simulada(catalogo, preguntas, respuestas):
    st.session_state["evaluaciones_visuales"] = st.session_state.get("evaluaciones_visuales", 0) + 1
    return {"modelo": "simulado-sin-api", "version_prompt": "prueba-visual",
            "correcciones": [{"pregunta_id": r["pregunta_id"], "veredicto": "correcta",
                              "explicacion": "Corrección simulada para revisar la interfaz. No se consultó Gemini.",
                              "respuesta_esperada": "Respuesta de prueba visual."} for r in respuestas]}


import interfaz_conocimiento

# Este módulo vive exclusivamente en el proceso del servidor de prueba. El
# fragmento conserva el mismo reloj entre sus ejecuciones independientes.
interfaz_conocimiento.monotonic = reloj_visual
with patch("interfaz_conocimiento.evaluar_respuestas", side_effect=evaluacion_simulada):
    runpy.run_path(str(RAIZ / "app.py"), run_name="__main__")
    if st.session_state.get("omnitrix_activado"):
        if st.button("Quedan cuatro segundos (prueba visual)", key="cuatro_segundos_visual"):
            ronda = st.session_state.get("conocimiento_ronda")
            if ronda and ronda["estado"] == "jugando":
                st.session_state["avance_reloj_visual"] = ronda["limite"] - monotonic() - 3.9
                st.rerun()
        if st.button("Agotar tiempo (prueba visual)", key="agotar_reloj_visual"):
            st.session_state["avance_reloj_visual"] = st.session_state.get("avance_reloj_visual", 0) + 61
            st.rerun()
        st.caption(f"Correcciones simuladas solicitadas: {st.session_state.get('evaluaciones_visuales', 0)}")
st.caption("Servidor de prueba visual: conocimiento simulado, sin API.")
