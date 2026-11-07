"""Modo de juego: estado de sesión, elección y evaluación explícita."""

import streamlit as st

from almacenamiento import ErrorCatalogo, cargar_aliens
from analisis import ErrorAnalisis
from desafios import cargar_desafios, elegir_desafio, evaluar_desafio


def conservar_respuesta():
    st.session_state["desafio_alien"] = st.session_state.get("selector_desafio")
    st.session_state["desafio_plan"] = st.session_state.get("plan_desafio", "")
    st.session_state.pop("evaluacion_desafio", None)
    st.session_state.pop("error_desafio", None)


def mostrar_desafios(mostrar_ficha):
    st.header("Desafíos del Omnitrix")
    st.info("Elige un alien y, si quieres, explica tu estrategia. Puede haber varias soluciones válidas.")
    try:
        situaciones = cargar_desafios()
        catalogo = {a["id"]: a for a in cargar_aliens()}
    except (ErrorAnalisis, ErrorCatalogo) as error:
        st.error(str(error))
        return
    st.caption(f"Una situación. {len(catalogo)} transformaciones. ¿A cuál recurrirías?")
    disponibles = {d["id"]: d for d in situaciones}
    if st.session_state.get("desafio_actual") not in disponibles:
        st.session_state["desafio_actual"] = elegir_desafio(situaciones)["id"]
        st.session_state.pop("evaluacion_desafio", None)
    if st.button("Otra situación", key="otro_desafio"):
        st.session_state["desafio_actual"] = elegir_desafio(situaciones, st.session_state["desafio_actual"])["id"]
        st.session_state["desafio_plan"] = ""
        st.session_state["plan_desafio"] = ""
        st.session_state.pop("evaluacion_desafio", None)
        st.session_state.pop("error_desafio", None)
    situacion = disponibles[st.session_state["desafio_actual"]]
    with st.container(border=True):
        st.caption("MISIÓN ACTUAL")
        st.subheader(situacion["titulo"])
        st.text(situacion["situacion"])
        st.markdown("**Tu objetivo**")
        st.text(situacion["objetivo"])
    ids = [None, *catalogo]
    conservado = st.session_state.get("desafio_alien")
    if conservado not in ids:
        conservado = None
    alien_id = st.selectbox("Tu transformación", ids, index=ids.index(conservado),
                            format_func=lambda valor: "Elige un alien…" if valor is None else catalogo[valor]["nombre"],
                            key="selector_desafio", on_change=conservar_respuesta)
    if alien_id:
        mostrar_ficha(catalogo[alien_id])
    plan = st.text_area("¿Cómo lo resolverías? (opcional)",
                        value=st.session_state.get("desafio_plan", ""), max_chars=1000,
                        placeholder="Explica cómo aprovecharías sus habilidades…",
                        key="plan_desafio", on_change=conservar_respuesta)
    if st.button("Evaluar mi elección", key="evaluar_desafio", type="primary", disabled=alien_id is None):
        st.session_state.pop("error_desafio", None)
        st.session_state.pop("evaluacion_desafio", None)
        with st.spinner("Evaluando tu estrategia…"):
            try:
                respuesta = evaluar_desafio(catalogo[alien_id], situacion, plan)
                st.session_state["evaluacion_desafio"] = {
                    **respuesta, "alien_nombre": catalogo[alien_id]["nombre"],
                }
            except ErrorAnalisis as error:
                st.session_state["error_desafio"] = str(error)
    if st.session_state.get("error_desafio"):
        st.error(st.session_state["error_desafio"])
    respuesta = st.session_state.get("evaluacion_desafio")
    if respuesta:
        resultado = respuesta["resultado"]
        st.subheader(f"Evaluación de {respuesta['alien_nombre']}")
        etiquetas = {"adecuado": "Buena elección", "arriesgado": "Viable con precauciones", "poco_adecuado": "Elección poco adecuada"}
        st.write(f"**{etiquetas[resultado['veredicto']]}**")
        st.text(resultado["resumen"])
        for campo, titulo in (("ventajas", "A tu favor"), ("riesgos", "Lo que podría complicarse"), ("resolucion", "Una posible resolución")):
            st.markdown(f"**{titulo}**")
            st.text(resultado[campo])
        st.caption("Evaluación generada por IA para este escenario ficticio. No es un resultado garantizado.")
    st.caption("Las partidas se conservan durante esta sesión. Otra situación inicia un nuevo desafío.")
