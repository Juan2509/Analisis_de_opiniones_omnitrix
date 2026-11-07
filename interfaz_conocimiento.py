"""Menú, ronda cronometrada y revisión escrita; estado aislado por sesión."""

import math
from time import monotonic
from uuid import uuid4

import streamlit as st

from almacenamiento import ErrorCatalogo, cargar_aliens
from analisis import ErrorAnalisis
from audio_cuestionario import mostrar_aviso
from conocimiento import DURACION, MODOS, evaluar_respuestas, generar_preguntas, resumir_resultados


def iniciar_ronda(catalogo, modo):
    preguntas = generar_preguntas(catalogo, modo)
    st.session_state["conocimiento_ronda"] = {
        "id": uuid4().hex, "modo": modo, "preguntas": preguntas, "respuestas": [],
        "limite": monotonic() + DURACION, "estado": "jugando",
    }


def conservar_modo():
    st.session_state["conocimiento_modo_elegido"] = st.session_state.get("modo_conocimiento")


@st.fragment(run_every="1s")
def mostrar_reloj():
    ronda = st.session_state.get("conocimiento_ronda")
    if not ronda or ronda["estado"] != "jugando":
        return
    restantes = max(0, math.ceil(ronda["limite"] - monotonic()))
    if restantes == 0:
        ronda.update(estado="finalizada", motivo="Tiempo agotado")
        st.rerun(scope="app")
    st.metric("Tiempo restante", f"{restantes} s")
    st.progress(restantes / DURACION)
    mostrar_aviso(ronda["id"], restantes)


def mostrar_conocimiento(cargar_imagen):
    st.header("Conocimiento alienígena")
    try:
        catalogo = cargar_aliens()
    except ErrorCatalogo as error:
        st.error(str(error))
        return
    ronda = st.session_state.get("conocimiento_ronda")
    if not ronda:
        st.caption("Identifica transformaciones y demuestra cuánto sabes del Omnitrix.")
        for nombre, descripcion in (
            ("Nombres", "Reconoce al alien de la imagen. Puedes escribir nombres en español, inglés o alias conocidos."),
            ("Habilidades", "Explica con tus palabras una habilidad característica del alien mostrado."),
            ("Especie", "Identifica su especie. Solo aparecen fichas con una especie identificada."),
            ("General", "Una mezcla de preguntas de nombres, habilidades y especies."),
        ):
            with st.container(border=True):
                st.subheader(nombre)
                st.write(descripcion)
        st.info("Tienes 60 segundos para responder una pregunta a la vez. Al terminar podrás pedir a la IA una revisión de todas tus respuestas. No hay pistas.")
        elegido = st.session_state.get("conocimiento_modo_elegido")
        modo = st.radio("Elige tu categoría", MODOS,
                        index=MODOS.index(elegido) if elegido in MODOS else None,
                        key="modo_conocimiento", on_change=conservar_modo)
        if st.button("Iniciar", key="iniciar_conocimiento", type="primary", disabled=modo is None):
            try:
                iniciar_ronda(catalogo, modo)
            except ErrorAnalisis as error:
                st.error(str(error))
            else:
                st.rerun()
        return

    st.caption(f"Categoría: {ronda['modo']} · Ronda de {DURACION} segundos")
    if ronda["estado"] == "jugando" and monotonic() >= ronda["limite"]:
        ronda.update(estado="finalizada", motivo="Tiempo agotado")
    if ronda["estado"] == "jugando":
        mostrar_reloj()
        indice = len(ronda["respuestas"])
        pregunta = ronda["preguntas"][indice]
        alien = next((a for a in catalogo if a["id"] == pregunta["alien_id"]), None)
        if alien is None:
            ronda.update(estado="finalizada", motivo="El catálogo cambió")
            st.rerun()
        st.caption(f"{indice} respuestas guardadas · Pregunta {indice + 1} · {pregunta['categoria']}")
        with st.container(border=True, key="pregunta_conocimiento"):
            imagen = cargar_imagen(alien["imagen"])
            if imagen is not None:
                st.image(imagen, caption="Transformación por identificar", width=260)
            else:
                st.error("No se pudo cargar la imagen de esta pregunta.")
            st.subheader(pregunta["enunciado"])
            with st.form(f"respuesta_conocimiento_{ronda['id']}_{indice}", clear_on_submit=True):
                texto = st.text_input("Tu respuesta", max_chars=500, key=f"conocimiento_texto_{indice}")
                enviar = st.form_submit_button("Enviar y siguiente", type="primary", disabled=imagen is None)
            if enviar:
                # La hora del servidor decide: un envío tardío no suma aunque la
                # pestaña haya estado inactiva o el reloj visual se haya retrasado.
                if monotonic() >= ronda["limite"]:
                    ronda.update(estado="finalizada", motivo="Tiempo agotado")
                    st.rerun()
                elif not texto.strip():
                    st.warning("Escribe una respuesta antes de continuar.")
                else:
                    ronda["respuestas"].append({"pregunta_id": pregunta["id"], "respuesta": texto.strip()})
                    if len(ronda["respuestas"]) == len(ronda["preguntas"]):
                        ronda.update(estado="finalizada", motivo="Todas las preguntas completadas")
                    st.rerun()
        st.caption("Solo cuentan las respuestas enviadas antes de que termine el tiempo. El reloj continúa si cambias de sección.")
        if st.button("Terminar ronda", key="terminar_conocimiento"):
            ronda.update(estado="finalizada", motivo="Ronda terminada por el jugador")
            st.rerun()
        return

    st.subheader(ronda["motivo"])
    st.write(f"Respuestas enviadas: **{len(ronda['respuestas'])}**")
    if not ronda["respuestas"]:
        st.info("No enviaste respuestas en esta ronda. Puedes volver a intentarlo.")
    elif "evaluacion" not in ronda:
        st.info("Tus respuestas están guardadas en esta sesión. La revisión se solicita una sola vez para toda la ronda y admite alias, traducciones y respuestas con tus propias palabras.")
        if st.button("Evaluar respuestas con IA", key="evaluar_conocimiento", type="primary"):
            ronda.pop("error", None)
            with st.spinner("La IA está revisando tus respuestas…"):
                try:
                    ronda["evaluacion"] = evaluar_respuestas(catalogo, ronda["preguntas"], ronda["respuestas"])
                except ErrorAnalisis as error:
                    ronda["error"] = str(error)
            if "evaluacion" in ronda:
                st.rerun()
        if ronda.get("error"):
            st.error(ronda["error"])
        st.caption("Esta acción utiliza la cuota de tu proyecto Gemini Free Tier. Si falla, puedes reintentar; no se cambia de proveedor ni se inventan resultados.")
    else:
        evaluacion = ronda["evaluacion"]
        resumen = resumir_resultados(evaluacion["correcciones"])
        columnas = st.columns(4)
        for col, campo, titulo in zip(columnas, ("correcta", "parcial", "incorrecta", "no_evaluable"),
                                      ("Correctas", "Parciales", "Incorrectas", "Por revisar")):
            col.metric(titulo, resumen[campo])
        if resumen["porcentaje"] is not None:
            st.write(f"**Puntuación: {resumen['puntos']:g} / {resumen['evaluables']} · {resumen['porcentaje']} %**")
        else:
            st.info("No fue posible puntuar las respuestas con suficiente certeza.")
        st.caption("Correcta: 1 punto; parcial: 0,5; incorrecta: 0. Las respuestas por revisar quedan fuera de la puntuación. La evaluación de IA puede equivocarse.")
        preguntas = {p["id"]: p for p in ronda["preguntas"]}
        aliens = {a["id"]: a for a in catalogo}
        etiquetas = {"correcta": "Correcta", "parcial": "Parcial", "incorrecta": "Incorrecta", "no_evaluable": "Por revisar"}
        for n, (respuesta, correccion) in enumerate(zip(ronda["respuestas"], evaluacion["correcciones"]), 1):
            pregunta = preguntas[respuesta["pregunta_id"]]
            alien = aliens.get(pregunta["alien_id"])
            with st.expander(f"{n}. {alien['nombre'] if alien else pregunta['alien_id']} · {etiquetas[correccion['veredicto']]}", expanded=n == 1):
                if alien:
                    imagen = cargar_imagen(alien["imagen"])
                    if imagen is not None:
                        st.image(imagen, width=140)
                st.write(pregunta["enunciado"])
                st.markdown("**Tu respuesta**")
                st.text(respuesta["respuesta"])
                st.markdown("**Respuesta de referencia**")
                st.text(correccion["respuesta_esperada"])
                st.text(correccion["explicacion"])
                if alien and pregunta["categoria"] == "Especie":
                    for fuente in alien.get("fuentes_especie", []):
                        st.caption(f"[Fuente de especie]({fuente})")
        st.caption(f"Modelo: {evaluacion['modelo']} · Evaluación: {evaluacion['version_prompt']}")
    columnas = st.columns(2)
    with columnas[0]:
        if st.button("Volver a jugar", key="rejugar_conocimiento"):
            try:
                iniciar_ronda(catalogo, ronda["modo"])
            except ErrorAnalisis as error:
                st.error(str(error))
            else:
                st.rerun()
    with columnas[1]:
        if st.button("Volver al menú de modos", key="menu_conocimiento"):
            st.session_state.pop("conocimiento_ronda", None)
            st.rerun()
