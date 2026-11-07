"""Dos submodos recreativos con respuestas revisables y análisis explícito."""

from uuid import uuid4

import streamlit as st

from almacenamiento import ErrorCatalogo, cargar_aliens
from analisis import ErrorAnalisis
from interpretacion import MODOS, PREGUNTA_FAVORITO, cargar_preguntas, interpretar, sortear_preguntas


AVISO = "Interpretación recreativa basada en lo que escribes; no es una evaluación psicológica."


def conservar_modo():
    st.session_state["interpretacion_modo_elegido"] = st.session_state.get("modo_interpretacion")


def iniciar(modo, anteriores=()):
    preguntas = sortear_preguntas(cargar_preguntas(), anteriores) if modo == MODOS[1] else []
    st.session_state["interpretacion_ronda"] = {
        "id": uuid4().hex, "modo": modo, "etapa": "preguntas" if preguntas else "favorito",
        "preguntas": preguntas, "respuestas": {}, "indice": 0,
        "alien_id": None, "motivo": "",
    }


def conservar_respuesta(pregunta_id):
    ronda = st.session_state["interpretacion_ronda"]
    ronda["respuestas"][pregunta_id] = st.session_state.get(f"interpretacion_texto_{pregunta_id}", "")


def conservar_favorito():
    ronda = st.session_state["interpretacion_ronda"]
    ronda["alien_id"] = st.session_state.get("alien_interpretacion")


def conservar_motivo():
    st.session_state["interpretacion_ronda"]["motivo"] = st.session_state.get("motivo_interpretacion", "")


def enviar_analisis(ronda, catalogo):
    if ronda["modo"] == MODOS[0]:
        respuestas = [{"id": "preferencia", "tema": "Preferencia personal", "pregunta": PREGUNTA_FAVORITO,
                       "respuesta": ronda["motivo"]}]
    else:
        respuestas = [{**p, "respuesta": ronda["respuestas"].get(p["id"], "")} for p in ronda["preguntas"]]
    ronda.pop("error", None)
    with st.spinner("La IA está interpretando tus motivos…"):
        try:
            ronda["evaluacion"] = interpretar(catalogo, ronda["modo"], respuestas, ronda["alien_id"])
        except ErrorAnalisis as error:
            ronda["error"] = str(error)
            return
    ronda["envio"] = respuestas
    ronda["etapa"] = "resultado"
    st.rerun()


def mostrar_interpretacion(mostrar_ficha):
    st.header("Interpretación alienígena")
    st.caption(AVISO)
    try:
        catalogo = cargar_aliens()
    except ErrorCatalogo as error:
        st.error(str(error))
        return
    por_id = {a["id"]: a for a in catalogo}
    ronda = st.session_state.get("interpretacion_ronda")
    if not ronda:
        for nombre, texto in (
            (MODOS[0], "Elige tu alien favorito y explica por qué te gusta. La IA relacionará tus motivos con valores y un estilo de héroe."),
            (MODOS[1], "Responde seis preguntas abiertas, una por tema. La IA propondrá un alien afín y una alternativa, explicando sus conexiones con tus respuestas."),
        ):
            with st.container(border=True):
                st.subheader(nombre)
                st.write(texto)
        st.info("Sin temporizador ni puntuaciones. Puedes expresarte con tus propias palabras y revisar las seis respuestas antes del análisis.")
        elegido = st.session_state.get("interpretacion_modo_elegido")
        modo = st.radio("Elige tu submodo", MODOS,
                        index=MODOS.index(elegido) if elegido in MODOS else None,
                        key="modo_interpretacion", on_change=conservar_modo)
        if st.button("Iniciar", key="iniciar_interpretacion", type="primary", disabled=modo is None):
            try:
                iniciar(modo)
            except ErrorAnalisis as error:
                st.error(str(error))
            else:
                st.rerun()
        return

    st.caption(f"Submodo: {ronda['modo']}")
    if ronda["etapa"] == "favorito":
        ids = [None, *por_id]
        elegido = ronda["alien_id"] if ronda["alien_id"] in por_id else None
        alien_id = st.selectbox("Tu alien favorito", ids, index=ids.index(elegido),
                                format_func=lambda i: "Elige un alien…" if i is None else por_id[i]["nombre"],
                                key="alien_interpretacion", on_change=conservar_favorito)
        ronda["alien_id"] = alien_id
        if alien_id:
            mostrar_ficha(por_id[alien_id])
        motivo = st.text_area(PREGUNTA_FAVORITO, value=ronda["motivo"], max_chars=1000,
                              key="motivo_interpretacion", on_change=conservar_motivo,
                              placeholder="Explica qué te atrae de él, qué admiras o qué harías con sus capacidades…")
        ronda["motivo"] = motivo
        st.caption("Entre 10 y 1000 caracteres. Tus motivos importan más que el alien elegido.")
        if st.button("Interpretar mi elección", key="analizar_favorito", type="primary",
                     disabled=alien_id is None):
            if len(motivo.strip()) < 10:
                st.warning("Explica tus motivos en al menos 10 caracteres.")
            else:
                enviar_analisis(ronda, catalogo)
    elif ronda["etapa"] == "preguntas":
        indice = ronda["indice"]
        pregunta = ronda["preguntas"][indice]
        st.progress((indice + 1) / 6)
        st.caption(f"Pregunta {indice + 1} de 6 · {pregunta['tema']}")
        with st.container(border=True):
            st.subheader(pregunta["pregunta"])
            texto = st.text_area("Tu respuesta", value=ronda["respuestas"].get(pregunta["id"], ""),
                                 max_chars=1000, key=f"interpretacion_texto_{pregunta['id']}",
                                 on_change=conservar_respuesta, args=(pregunta["id"],))
            ronda["respuestas"][pregunta["id"]] = texto
            st.caption("Entre 10 y 1000 caracteres. No hay respuestas correctas ni incorrectas.")
        anterior, siguiente = st.columns(2)
        with anterior:
            if st.button("Anterior", key="anterior_interpretacion", disabled=indice == 0):
                ronda["indice"] -= 1
                st.rerun()
        with siguiente:
            if st.button("Revisar mis respuestas" if indice == 5 else "Siguiente",
                         key="siguiente_interpretacion", type="primary"):
                if len(texto.strip()) < 10:
                    st.warning("Escribe al menos 10 caracteres antes de continuar.")
                else:
                    if indice == 5:
                        ronda["etapa"] = "revision"
                    else:
                        ronda["indice"] += 1
                    st.rerun()
    elif ronda["etapa"] == "revision":
        st.subheader("Revisa tus respuestas")
        for i, pregunta in enumerate(ronda["preguntas"]):
            with st.expander(f"{i + 1}. {pregunta['tema']}", expanded=i == 0):
                st.write(pregunta["pregunta"])
                st.text(ronda["respuestas"].get(pregunta["id"], ""))
                if st.button("Editar esta respuesta", key=f"editar_interpretacion_{pregunta['id']}"):
                    ronda.update(etapa="preguntas", indice=i)
                    ronda.pop("error", None)
                    st.rerun()
        completas = all(10 <= len(ronda["respuestas"].get(p["id"], "").strip()) <= 1000 for p in ronda["preguntas"])
        if st.button("Descubrir mi afinidad", key="analizar_afinidad", type="primary", disabled=not completas):
            enviar_analisis(ronda, catalogo)
    else:
        evaluacion = ronda["evaluacion"]
        resultado = evaluacion["resultado"]
        # Una sesión puede sobrevivir a ediciones del catálogo.
        if resultado["alien_principal_id"] not in por_id or (resultado["alien_alternativo_id"] is not None and resultado["alien_alternativo_id"] not in por_id):
            st.error("El catálogo cambió y ya no contiene los aliens de este resultado. Puedes iniciar otra interpretación.")
        else:
            st.subheader("Tu afinidad principal" if ronda["modo"] == MODOS[1] else "Tu conexión con el alien elegido")
            mostrar_ficha(por_id[resultado["alien_principal_id"]], clave="ficha_interpretacion_principal")
            st.text(resultado["resumen"])
            for campo, titulo in (("valores", "Lo que valoras"), ("estilo_heroe", "Tu estilo de héroe")):
                with st.container(border=True):
                    st.subheader(titulo)
                    st.text(resultado[campo])
            conexiones = {c["respuesta_id"]: c["interpretacion"] for c in resultado["conexiones"]}
            st.subheader("La conexión con tus respuestas")
            for respuesta in ronda["envio"]:
                with st.expander(respuesta["tema"]):
                    st.write(respuesta["pregunta"])
                    st.markdown("**Lo que escribiste**")
                    st.text(respuesta["respuesta"])
                    st.markdown("**Interpretación**")
                    st.text(conexiones[respuesta["id"]])
            alternativa = resultado["alien_alternativo_id"]
            if alternativa:
                with st.expander(f"Otra afinidad posible: {por_id[alternativa]['nombre']}"):
                    mostrar_ficha(por_id[alternativa], clave="ficha_interpretacion_alternativa")
                    st.text(resultado["motivo_alternativo"])
            st.markdown("**Lo que esta interpretación no puede concluir**")
            st.text(resultado["limites"])
            st.markdown("**Para reflexionar**")
            st.text(resultado["pregunta_reflexion"])
            st.caption(f"{AVISO} Modelo: {evaluacion['modelo']} · {evaluacion['version_prompt']}")
        if st.button("Volver a intentarlo", key="repetir_interpretacion"):
            try:
                iniciar(ronda["modo"], [p["id"] for p in ronda["preguntas"]])
            except ErrorAnalisis as error:
                st.error(str(error))
            else:
                st.rerun()
    if ronda.get("error"):
        st.error(ronda["error"])
    if ronda["etapa"] != "resultado":
        st.caption("Las respuestas permanecen en esta sesión. Solo el botón de análisis utiliza la cuota de Gemini Free Tier.")
    if st.button("Volver al menú de modos", key="menu_interpretacion"):
        st.session_state.pop("interpretacion_ronda", None)
        st.rerun()
