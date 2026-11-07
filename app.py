"""Interfaz de catálogo, análisis y consulta del Archivo Omnitrix."""

import json
from base64 import b64encode
import streamlit as st
from PIL import Image

from almacenamiento import (
    ErrorCatalogo, ErrorOpiniones, RAIZ_PROYECTO, RUTA_OPINIONES,
    cargar_aliens, crear_registro, guardar_opinion, cargar_opiniones, consultar_opiniones,
)
from analisis import ErrorAnalisis, analizar_opinion
from pantalla_inicio import mostrar_inicio


def cargar_imagen_local(ruta: str | None) -> Image.Image | None:
    """Lee una imagen del proyecto; un recurso ausente o dañado admite alternativa."""
    if ruta is None:
        return None
    try:
        archivo = (RAIZ_PROYECTO / ruta).resolve()
        if not archivo.is_relative_to(RAIZ_PROYECTO):
            return None
        with Image.open(archivo) as imagen:
            imagen.load()
            return imagen.copy()
    except (OSError, ValueError, RuntimeError, Image.DecompressionBombError):
        return None


def mostrar_ficha(alien: dict):
    """Presenta datos del catálogo e imagen local, sin consultar modelos ni la red."""
    with st.container(border=True, key="ficha_alien"):
        st.caption("ALIEN SELECCIONADO")
        st.subheader(alien["nombre"])
        columna_imagen, columna_datos = st.columns([1, 1.4], gap="large")
        with columna_imagen:
            with st.container(key="imagen_alien"):
                imagen = cargar_imagen_local(alien["imagen"])
                if imagen is not None:
                    st.image(imagen, caption=f"Imagen de {alien['nombre']}", width="stretch")
                    st.caption(
                        "Diseño de Omniverse · "
                        "[Fuente](https://ben10db.weebly.com/omniverse.html)"
                    )
                else:
                    try:
                        alternativa = (RAIZ_PROYECTO / "assets/aliens/sin_imagen.svg").read_text(
                            encoding="utf-8"
                        )
                    except (OSError, UnicodeError):
                        st.info("Imagen no disponible.")
                    else:
                        st.image(alternativa, caption="Imagen no disponible", width="stretch")
        with columna_datos, st.container(key="datos_alien"):
            st.caption("SERIE DE INTRODUCCIÓN")
            st.text(alien["serie_origen"])
            st.caption("NOMBRE ORIGINAL")
            st.text(alien["nombre_original"])
            st.markdown("**Habilidades**")
            st.write(alien["descripcion"])


def conservar_seleccion():
    """Conserva el ID aunque el selector deje de mostrarse al navegar."""
    st.session_state["alien_id"] = st.session_state["selector_alien"]


def guardar_envio(opinion: dict):
    """Conserva el mismo registro ante reintentos sin volver a analizar."""
    try:
        if "registro" not in opinion:
            opinion["registro"] = crear_registro(
                {"id": opinion["alien_id"], "nombre": opinion["alien_nombre"]},
                opinion["opinion_original"], opinion["analisis"],
                opinion["modelo"], opinion["version_prompt"],
            )
        guardar_opinion(RUTA_OPINIONES, opinion["registro"])
    except ErrorOpiniones as error:
        opinion["error_guardado"] = str(error)
    else:
        opinion["guardada"] = True
        opinion.pop("error_guardado", None)


def mostrar_opiniones(alien: dict):
    """Captura y analiza envíos; guarda los pertinentes y conserva el chat en sesión."""
    historial = st.session_state.setdefault("opiniones_sesion", [])
    st.subheader("Comparte tu opinión")
    st.info(
        "Cada envío se analiza de forma independiente con IA. "
        "Las opiniones pertinentes se guardan en el archivo local. "
        "Nueva conversación limpia el chat y conserva el archivo."
    )
    if st.button("Nueva conversación", key="nueva_conversacion"):
        historial.clear()
        st.session_state.pop("opinion_rechazada", None)

    texto = st.chat_input(
        f"Opina sobre {alien['nombre']} (5 a 1000 caracteres)",
        key="opinion_actual",
    )
    if texto is not None:
        # Validar sin truncar; conservar el texto original para su recuperación.
        if not 5 <= len(texto.strip()) <= 1000:
            st.session_state["opinion_rechazada"] = {
                "alien_nombre": alien["nombre"], "texto": texto,
            }
        else:
            opinion = {
                "alien_id": alien["id"],
                "alien_nombre": alien["nombre"],
                "opinion_original": texto,
            }
            historial.append(opinion)
            st.session_state.pop("opinion_rechazada", None)
            with st.spinner("Analizando la opinión…"):
                try:
                    opinion.update(analizar_opinion(dict(alien), texto))
                except ErrorAnalisis as error:
                    opinion["error_analisis"] = str(error)
            if opinion.get("analisis", {}).get("es_pertinente") is True:
                guardar_envio(opinion)

    for opinion in historial:
        with st.chat_message("user"):
            st.caption(f"Opinión sobre {opinion['alien_nombre']}")
            st.text(opinion["opinion_original"])
        if "error_analisis" in opinion:
            st.error(opinion["error_analisis"])
        elif "analisis" in opinion:
            resultado = opinion["analisis"]
            with st.chat_message("assistant"):
                if resultado["es_pertinente"]:
                    st.write(f"Sentimiento: {resultado['sentimiento']}")
                    st.text(resultado["razon"])
                else:
                    st.warning("Opinión no pertinente. No se guardará en el archivo.")
                    st.text(resultado["razon"])
        else:
            st.caption("Pendiente de análisis")
        if "error_guardado" in opinion:
            registro = opinion.get("registro")
            if registro is not None and st.button(
                "Reintentar guardado", key=f"guardar_{registro['id']}",
            ):
                guardar_envio(opinion)
        if opinion.get("guardada"):
            st.success("Opinión guardada en el Archivo Omnitrix")
        else:
            st.caption("Sin guardar en el archivo")
            if "error_guardado" in opinion:
                st.error(opinion["error_guardado"])

    rechazada = st.session_state.get("opinion_rechazada")
    if rechazada is not None:
        st.error(
            "La opinión debe tener entre 5 y 1000 caracteres después de quitar "
            "los espacios exteriores. Corrígela y vuelve a enviarla."
        )
        with st.chat_message("user"):
            st.caption(f"Texto no aceptado sobre {rechazada['alien_nombre']}")
            st.text(rechazada["texto"])


def mostrar_archivo():
    """Consulta el JSON persistente sin cargar el catálogo, escribir ni llamar a la IA."""
    st.header("Consultar archivo")
    st.caption(
        "Explora las opiniones guardadas. Los totales corresponden únicamente "
        "a este archivo y respetan los filtros seleccionados."
    )
    try:
        registros = cargar_opiniones(RUTA_OPINIONES)
    except ErrorOpiniones as error:
        st.error(str(error))
        return

    # Usar los IDs del archivo permite consultar datos aunque cambie o falle el catálogo.
    nombres = {registro["alien_id"]: registro["alien_nombre"] for registro in registros}
    ids = [None, *sorted(nombres, key=lambda identificador: (nombres[identificador].casefold(), identificador))]
    categorias = ("positivo", "negativo", "neutro", "mixto")
    if st.session_state.get("filtro_alien") not in ids:
        st.session_state["filtro_alien"] = None
    if st.session_state.get("filtro_sentimiento") not in (None, *categorias):
        st.session_state["filtro_sentimiento"] = None
    columnas = st.columns(2)
    with columnas[0]:
        alien_id = st.selectbox(
            "Filtrar por alien", options=ids, key="filtro_alien",
            format_func=lambda valor: "Todos los aliens" if valor is None else f"{nombres[valor]} ({valor})",
        )
    with columnas[1]:
        sentimiento = st.selectbox(
            "Filtrar por sentimiento", options=(None, *categorias), key="filtro_sentimiento",
            format_func=lambda valor: "Todos los sentimientos" if valor is None else valor.capitalize(),
        )

    filtrados = consultar_opiniones(registros, alien_id, sentimiento)
    columnas = st.columns(5)
    columnas[0].metric("Total de opiniones", len(filtrados))
    for columna, categoria in zip(columnas[1:], categorias):
        columna.metric(categoria.capitalize(), sum(r["sentimiento"] == categoria for r in filtrados))

    if not registros:
        st.info("Todavía no hay opiniones guardadas. Envía una opinión pertinente en Analizar opinión.")
    elif not filtrados:
        st.info("No hay opiniones que coincidan con los filtros seleccionados.")
    else:
        # Una única selección alimenta tabla, recuentos y descarga.
        st.dataframe({
            "Fecha UTC": [r["fecha_utc"] for r in filtrados],
            "Alien": [r["alien_nombre"] for r in filtrados],
            "ID del alien": [r["alien_id"] for r in filtrados],
            "Opinión original": [r["opinion_original"] for r in filtrados],
            "Sentimiento": [r["sentimiento"] for r in filtrados],
            "Razón": [r["razon"] for r in filtrados],
        }, hide_index=True, width="stretch")

    st.download_button(
        "Descargar resultados filtrados (JSON)",
        data=json.dumps({"version": 1, "opiniones": filtrados}, ensure_ascii=False, indent=2).encode("utf-8"),
        file_name="opiniones_omnitrix_filtradas.json", mime="application/json",
        key="descargar_opiniones", on_click="ignore",
    )
    st.caption("La descarga incluye los registros completos de la selección, con sus IDs y metadatos.")


def main():
    ruta_simbolo = RAIZ_PROYECTO / "assets/omnitrix.png"
    st.set_page_config(page_title="Archivo Omnitrix", page_icon=str(ruta_simbolo), layout="wide")
    simbolo_omnitrix = b64encode(ruta_simbolo.read_bytes()).decode("ascii")
    estilos = (RAIZ_PROYECTO / "assets" / "estilos.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{estilos}</style>", unsafe_allow_html=True)

    if mostrar_inicio(simbolo_omnitrix):
        return

    with st.sidebar:
        st.markdown(
            '<div class="omnitrix-marca">'
            f'<img src="data:image/png;base64,{simbolo_omnitrix}" alt="" aria-hidden="true">'
            '<div>ARCHIVO<strong>OMNITRIX</strong></div></div>',
            unsafe_allow_html=True,
        )
        st.caption("Tu conexión con el universo Ben 10.")
        st.divider()
        seccion = st.radio(
            "Secciones",
            ("Analizar opinión", "Consultar archivo"),
            key="seccion",
        )
        st.divider()
        st.caption("Versión en desarrollo · Catálogo, fichas y análisis de opiniones.")

    st.title("Archivo Omnitrix")
    st.caption("Explora las transformaciones de Ben 10.")

    if seccion == "Consultar archivo":
        mostrar_archivo()
        return

    st.markdown(
        f"""
        <div class="omnitrix-portada">
            <div class="omnitrix-portada-texto">
                <p class="omnitrix-etiqueta">EL ARCHIVO DE LAS TRANSFORMACIONES</p>
                <p class="omnitrix-lema">El universo está<br><span>en tus manos.</span></p>
                <p class="omnitrix-invitacion">Descubre sus habilidades. Encuentra tu transformación.</p>
            </div>
            <div class="omnitrix-nucleo" aria-hidden="true">
                <img class="omnitrix-emblema" src="data:image/png;base64,{simbolo_omnitrix}" alt="">
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.header("Analizar opinión")

    try:
        aliens = cargar_aliens()
    except ErrorCatalogo as error:
        st.error(f"No se pudo mostrar el catálogo. {error}")
        st.info("Revisa el archivo del catálogo antes de seleccionar una transformación.")
        st.stop()

    catalogo = {alien["id"]: alien for alien in aliens}
    ids = list(catalogo)
    if st.session_state.get("alien_id") not in catalogo:
        st.session_state["alien_id"] = ids[0]

    st.caption(
        f"{len(aliens)} transformaciones · "
        f"{len({alien['serie_origen'] for alien in aliens})} series"
    )
    alien_id = st.selectbox(
        "Selecciona un alien",
        options=ids,
        index=ids.index(st.session_state["alien_id"]),
        format_func=lambda identificador: catalogo[identificador]["nombre"],
        key="selector_alien",
        on_change=conservar_seleccion,
    )
    alien = catalogo[alien_id]

    mostrar_ficha(alien)

    mostrar_opiniones(alien)


if __name__ == "__main__":
    main()
