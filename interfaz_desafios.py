"""Modo de juego: estado de sesión, elección y evaluación explícita."""

import random

import streamlit as st

from almacenamiento import ErrorCatalogo, cargar_aliens
from analisis import ErrorAnalisis
from desafios import MODOS, cargar_desafios, elegir_desafio, evaluar_desafio


def conservar_modo():
    st.session_state["desafio_modo_elegido"] = st.session_state.get("modo_desafio")


def preparar_mision(situaciones, catalogo, anterior=None):
    """Sortear solo al iniciar/cambiar misión; conservar el sorteo entre reejecuciones."""
    st.session_state["desafio_actual"] = elegir_desafio(situaciones, anterior)["id"]
    modo = st.session_state["desafio_modo_activo"]
    cantidad = {"Héroe bajo presión": 3, "Adaptabilidad": 1}.get(modo)
    opciones = random.sample(list(catalogo), cantidad) if cantidad else list(catalogo)
    st.session_state["desafio_opciones"] = opciones
    st.session_state["desafio_alien"] = opciones[0] if modo == "Adaptabilidad" else None
    st.session_state["selector_desafio"] = None
    st.session_state["desafio_plan"] = ""
    st.session_state["plan_desafio"] = ""
    st.session_state.pop("evaluacion_desafio", None)
    st.session_state.pop("error_desafio", None)


def conservar_respuesta():
    if st.session_state.get("desafio_modo_activo") != "Adaptabilidad":
        st.session_state["desafio_alien"] = st.session_state.get("selector_desafio")
    st.session_state["desafio_plan"] = st.session_state.get("plan_desafio", "")
    st.session_state.pop("evaluacion_desafio", None)
    st.session_state.pop("error_desafio", None)


def mostrar_desafios(mostrar_ficha):
    st.header("Desafíos del Omnitrix")
    try:
        situaciones = cargar_desafios()
        catalogo = {a["id"]: a for a in cargar_aliens()}
    except (ErrorAnalisis, ErrorCatalogo) as error:
        st.error(str(error))
        return
    if st.session_state.get("desafio_modo_activo") not in MODOS:
        st.caption("Elige cómo quieres afrontar las misiones del Omnitrix.")
        with st.container(border=True):
            st.subheader("Control maestro")
            st.write(f"Accede a las {len(catalogo)} transformaciones y elige la que mejor encaje con cada situación.")
        with st.container(border=True):
            st.subheader("Héroe bajo presión")
            st.write("Solo tendrás tres aliens elegidos completamente al azar por situación. Resuelve la misión con lo que te toque.")
        with st.container(border=True):
            st.subheader("Adaptabilidad")
            st.write("El Omnitrix te asignará un único alien al azar. Explica cómo resolverías la situación aprovechando sus capacidades.")
        elegido = st.session_state.get("desafio_modo_elegido")
        modo = st.radio("Elige tu modo", MODOS,
                        index=MODOS.index(elegido) if elegido in MODOS else None,
                        key="modo_desafio", on_change=conservar_modo)
        if st.button("Iniciar", key="iniciar_desafio", type="primary", disabled=modo is None):
            st.session_state["desafio_modo_activo"] = modo
            preparar_mision(situaciones, catalogo)
            st.rerun()
        return
    modo = st.session_state["desafio_modo_activo"]
    st.caption(f"Modo: {modo}")
    disponibles = {d["id"]: d for d in situaciones}
    opciones = st.session_state.get("desafio_opciones", [])
    limite = {"Héroe bajo presión": 3, "Adaptabilidad": 1}.get(modo, len(catalogo))
    if (st.session_state.get("desafio_actual") not in disponibles or len(opciones) != limite
            or len(set(opciones)) != limite or any(a not in catalogo for a in opciones)):
        preparar_mision(situaciones, catalogo)
    opciones = st.session_state["desafio_opciones"]
    st.caption("Un alien asignado para esta misión." if modo == "Adaptabilidad"
               else f"{len(opciones)} transformaciones disponibles para esta misión.")
    situacion = disponibles[st.session_state["desafio_actual"]]
    with st.container(border=True):
        st.caption("MISIÓN ACTUAL")
        st.subheader(situacion["titulo"])
        st.text(situacion["situacion"])
        st.markdown("**Tu objetivo**")
        st.text(situacion["objetivo"])
    respuesta = st.session_state.get("evaluacion_desafio")
    # Mantener resultados de sesiones abiertas antes del cierre por rondas.
    if respuesta and "alien_id" not in respuesta:
        anterior = st.session_state.get("desafio_alien")
        if anterior in catalogo:
            respuesta.update(alien_id=anterior, plan=st.session_state.get("desafio_plan", ""))
        else:
            st.session_state.pop("evaluacion_desafio", None)
            respuesta = None
    if respuesta:
        mostrar_ficha(catalogo[respuesta["alien_id"]])
        if respuesta["plan"].strip():
            st.markdown("**Tu estrategia**")
            st.text(respuesta["plan"])
        resultado = respuesta["resultado"]
        st.subheader(f"Evaluación de {respuesta['alien_nombre']}")
        etiquetas = ({"adecuado": "Estrategia sólida", "arriesgado": "Estrategia arriesgada", "poco_adecuado": "Estrategia poco viable"}
                     if modo == "Adaptabilidad" else
                     {"adecuado": "Buena elección", "arriesgado": "Viable con precauciones", "poco_adecuado": "Elección poco adecuada"})
        st.write(f"**{etiquetas[resultado['veredicto']]}**")
        st.text(resultado["resumen"])
        for campo, titulo in (("ventajas", "A tu favor"), ("riesgos", "Lo que podría complicarse"), ("resolucion", "Una posible resolución")):
            st.markdown(f"**{titulo}**")
            st.text(resultado[campo])
        st.caption("Evaluación generada por IA para este escenario ficticio. No es un resultado garantizado.")
        columnas = st.columns(2)
        with columnas[0]:
            if st.button("Volver a jugar", key="volver_jugar_desafio", type="primary"):
                preparar_mision(situaciones, catalogo, situacion["id"])
                st.rerun()
        with columnas[1]:
            if st.button("Volver al menú de modos", key="menu_modos_desafio"):
                st.session_state.pop("desafio_modo_activo", None)
                st.session_state.pop("evaluacion_desafio", None)
                st.rerun()
        return
    st.info("Explica cómo aprovecharías las capacidades del alien asignado. Puede haber varias soluciones válidas."
            if modo == "Adaptabilidad" else "Elige un alien y, si quieres, explica tu estrategia. Puede haber varias soluciones válidas.")
    ids = [None, *opciones]
    conservado = st.session_state.get("desafio_alien")
    if conservado not in ids:
        conservado = None
    if modo == "Adaptabilidad":
        alien_id = opciones[0]
        st.write(f"**Tu alien asignado: {catalogo[alien_id]['nombre']}**")
    else:
        alien_id = st.selectbox("Tu transformación", ids, index=ids.index(conservado),
                            format_func=lambda valor: "Elige un alien…" if valor is None else catalogo[valor]["nombre"],
                            key="selector_desafio", on_change=conservar_respuesta)
    if alien_id:
        mostrar_ficha(catalogo[alien_id])
    plan = st.text_area("¿Cómo lo resolverías?" if modo == "Adaptabilidad" else "¿Cómo lo resolverías? (opcional)",
                        value=st.session_state.get("desafio_plan", ""), max_chars=1000,
                        placeholder="Explica cómo aprovecharías sus habilidades…",
                        key="plan_desafio", on_change=conservar_respuesta)
    deshabilitado = alien_id is None or (modo == "Adaptabilidad" and len(plan.strip()) < 5)
    if st.button("Evaluar mi estrategia" if modo == "Adaptabilidad" else "Evaluar mi elección",
                 key="evaluar_desafio", type="primary", disabled=deshabilitado):
        st.session_state.pop("error_desafio", None)
        st.session_state.pop("evaluacion_desafio", None)
        with st.spinner("Evaluando tu estrategia…"):
            try:
                respuesta = evaluar_desafio(catalogo[alien_id], situacion, plan, modo=modo)
                st.session_state["evaluacion_desafio"] = {
                    **respuesta, "alien_nombre": catalogo[alien_id]["nombre"],
                    "alien_id": alien_id, "plan": plan,
                }
            except ErrorAnalisis as error:
                st.session_state["error_desafio"] = str(error)
        if st.session_state.get("evaluacion_desafio"):
            st.rerun()
    if st.session_state.get("error_desafio"):
        st.error(st.session_state["error_desafio"])
    st.caption("La ronda se conserva durante esta sesión. Completa la evaluación para volver a jugar o regresar al menú de modos.")
