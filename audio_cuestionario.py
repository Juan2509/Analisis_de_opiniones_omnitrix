"""Aviso local del cuestionario, con reproducción única por ronda en el navegador."""

from base64 import b64encode
from functools import lru_cache
from pathlib import Path

import streamlit.components.v2 as componentes


RAIZ = Path(__file__).resolve().parent
AVISO = componentes.component(
    "omnitrix_aviso_tiempo",
    html='<span hidden aria-hidden="true"></span>',
    js=(RAIZ / "assets" / "aviso_tiempo.js").read_text(encoding="utf-8"),
    isolate_styles=False,
)


@lru_cache(maxsize=1)
def audio_local():
    try:
        return "data:audio/mpeg;base64," + b64encode(
            (RAIZ / "sonidos" / "omnitrix-time-out.mp3").read_bytes()
        ).decode("ascii")
    except OSError:
        # Un recurso ausente no debe detener el reloj ni la partida.
        return None


def mostrar_aviso(ronda_id: str, restantes: int):
    audio = audio_local()
    if audio:
        AVISO(data={"ronda": ronda_id, "restantes": restantes, "audio": audio},
              key="aviso_tiempo_conocimiento")
