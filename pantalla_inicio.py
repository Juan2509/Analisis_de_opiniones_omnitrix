"""Pantalla de activación con recursos locales, sin llamadas a modelos."""

from base64 import b64encode
from pathlib import Path

import streamlit as st
import streamlit.components.v2 as componentes


RECURSOS = Path(__file__).resolve().parent / "assets" / "inicio"
ACTIVACION = componentes.component(
    "omnitrix_activacion",
    html=(RECURSOS / "inicio.html").read_text(encoding="utf-8"),
    css=(RECURSOS / "inicio.css").read_text(encoding="utf-8"),
    js=(RECURSOS / "inicio.js").read_text(encoding="utf-8"),
    isolate_styles=False,
)


def activar_omnitrix():
    """La animación terminó: conservar el acceso durante esta sesión de Streamlit."""
    st.session_state["omnitrix_activado"] = True


def mostrar_inicio(simbolo_base64: str) -> bool:
    """Devuelve True mientras se muestra la entrada y el dashboard debe esperar."""
    if st.session_state.get("omnitrix_activado", False):
        return False
    ACTIVACION(
        data={
            "simbolo": f"data:image/png;base64,{simbolo_base64}",
            "inicio_audio": "data:audio/mpeg;base64," + b64encode(
                (RECURSOS.parent.parent / "sonidos" / "core-ready.mp3").read_bytes()
            ).decode("ascii"),
            "transformacion_audio": "data:audio/mpeg;base64," + b64encode(
                (RECURSOS.parent.parent / "sonidos" / "omnitrix-transform.mp3").read_bytes()
            ).decode("ascii"),
        },
        key="inicio_omnitrix",
        on_activar_change=activar_omnitrix,
    )
    return True
