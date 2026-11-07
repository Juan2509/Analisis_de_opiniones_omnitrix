"""Catálogo y persistencia JSON local para un único escritor."""

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath, PureWindowsPath
from uuid import UUID, uuid4
from urllib.parse import urlsplit


RAIZ_PROYECTO = Path(__file__).resolve().parent
RUTA_CATALOGO = RAIZ_PROYECTO / "datos" / "aliens.json"
RUTA_OPINIONES = RAIZ_PROYECTO / "datos" / "opiniones.json"
CAMPOS_TEXTO = ("id", "nombre", "nombre_original", "serie_origen", "descripcion")
CAMPOS_ESPECIE = ("especie", "estado_especie", "fuentes_especie")


class ErrorCatalogo(ValueError):
    """El catálogo no se puede leer o no cumple su contrato de datos."""


def _validar_catalogo(datos: object) -> list[dict]:
    """Comprueba la versión 1 y devuelve los aliens sin modificar sus datos."""
    if not isinstance(datos, dict):
        raise ErrorCatalogo("La raíz del catálogo debe ser un objeto JSON.")

    # bool es una subclase de int en Python; true no es una versión válida.
    if type(datos.get("version")) is not int or datos["version"] != 1:
        raise ErrorCatalogo("El catálogo debe indicar version como el entero 1.")

    aliens = datos.get("aliens")
    if not isinstance(aliens, list):
        raise ErrorCatalogo("El campo 'aliens' debe ser una lista.")
    if len(aliens) < 20:
        raise ErrorCatalogo("El catálogo debe contener al menos 20 aliens.")

    ids = set()
    for posicion, alien in enumerate(aliens, start=1):
        referencia = f"Alien en la posición {posicion}"
        if not isinstance(alien, dict):
            raise ErrorCatalogo(f"{referencia}: debe ser un objeto JSON.")

        for campo in (*CAMPOS_TEXTO, "imagen"):
            if campo not in alien:
                raise ErrorCatalogo(f"{referencia}: falta el campo '{campo}'.")

        for campo in CAMPOS_TEXTO:
            valor = alien[campo]
            if not isinstance(valor, str) or not valor.strip():
                raise ErrorCatalogo(
                    f"{referencia}: '{campo}' debe ser texto no vacío."
                )

        # Extensión compatible con catálogos v1 anteriores. Una ficha que
        # incorpore especies debe incluir el bloque completo y su procedencia.
        if any(campo in alien for campo in CAMPOS_ESPECIE):
            for campo in CAMPOS_ESPECIE:
                if campo not in alien:
                    raise ErrorCatalogo(f"{referencia}: falta el campo '{campo}'.")
            if not isinstance(alien["especie"], str) or not alien["especie"].strip():
                raise ErrorCatalogo(f"{referencia}: 'especie' debe ser texto no vacío.")
            if alien["estado_especie"] not in (
                "identificada", "sin_nombre_confirmado", "hibrida"
            ):
                raise ErrorCatalogo(f"{referencia}: 'estado_especie' no es válido.")
            fuentes = alien["fuentes_especie"]
            if not isinstance(fuentes, list) or not fuentes:
                raise ErrorCatalogo(f"{referencia}: 'fuentes_especie' requiere enlaces HTTPS.")
            for fuente in fuentes:
                try:
                    url = urlsplit(fuente) if isinstance(fuente, str) else None
                    valida = (
                        url is not None and url.scheme == "https" and url.hostname
                        and not url.username and not url.password
                        and not any(c.isspace() for c in fuente)
                        and not any(c in fuente for c in "<>\\\"()")
                    )
                except ValueError:
                    valida = False
                if not valida:
                    raise ErrorCatalogo(f"{referencia}: 'fuentes_especie' requiere enlaces HTTPS.")

        alien_id = alien["id"]
        if alien_id != alien_id.strip():
            raise ErrorCatalogo(f"{referencia}: el ID no debe tener espacios exteriores.")
        if alien_id in ids:
            raise ErrorCatalogo(f"{referencia}: ID repetido '{alien_id}'.")
        ids.add(alien_id)

        imagen = alien["imagen"]
        if imagen is None:
            continue
        if not isinstance(imagen, str) or not imagen.strip():
            raise ErrorCatalogo(
                f"{referencia}: 'imagen' debe ser una ruta relativa o null."
            )

        ruta_imagen = Path(imagen)
        if (
            ruta_imagen.is_absolute()
            or PurePosixPath(imagen).is_absolute()
            or PureWindowsPath(imagen).drive
            or "\\" in imagen
            or "\x00" in imagen
            or "://" in imagen
            or ".." in ruta_imagen.parts
        ):
            raise ErrorCatalogo(
                f"{referencia}: 'imagen' debe ser una ruta local relativa "
                "dentro del proyecto, usando '/' y sin '..'."
            )

    return aliens


def cargar_aliens(ruta: str | Path = RUTA_CATALOGO) -> list[dict]:
    """Lee un catálogo UTF-8 y devuelve su lista de aliens validada.

    Las rutas relativas se interpretan desde la raíz del proyecto. Las rutas
    absolutas permiten cargar otro catálogo, por ejemplo durante las pruebas.
    Ante errores lanza ErrorCatalogo; nunca crea ni sobrescribe archivos.
    La existencia de las imágenes se comprobará al mostrar las fichas.
    """
    ruta = Path(ruta)
    if not ruta.is_absolute():
        ruta = RAIZ_PROYECTO / ruta

    try:
        contenido = ruta.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise ErrorCatalogo(f"No se encontró el catálogo: {ruta}.") from error
    except UnicodeError as error:
        raise ErrorCatalogo(f"El catálogo debe estar codificado en UTF-8: {ruta}.") from error
    except OSError as error:
        raise ErrorCatalogo(f"No se pudo leer el catálogo: {ruta}.") from error

    try:
        datos = json.loads(contenido)
    except json.JSONDecodeError as error:
        raise ErrorCatalogo(
            f"El catálogo contiene JSON inválido: {ruta} "
            f"(línea {error.lineno}, columna {error.colno})."
        ) from error

    return _validar_catalogo(datos)


class ErrorOpiniones(ValueError):
    """El archivo de opiniones no se puede leer, validar o guardar."""


def _validar_registro(registro: object) -> dict:
    campos = {
        "id", "fecha_utc", "alien_id", "alien_nombre", "opinion_original",
        "sentimiento", "razon", "modelo", "version_prompt",
    }
    if not isinstance(registro, dict) or set(registro) != campos:
        raise ErrorOpiniones("Un registro de opiniones contiene campos ausentes o inesperados.")
    if any(not isinstance(valor, str) or not valor.strip() for valor in registro.values()):
        raise ErrorOpiniones("Los campos del registro deben ser textos no vacíos.")
    try:
        if str(UUID(registro["id"])) != registro["id"]:
            raise ValueError
        fecha = datetime.fromisoformat(registro["fecha_utc"].replace("Z", "+00:00"))
        if fecha.utcoffset() is None or fecha.utcoffset().total_seconds() != 0:
            raise ValueError
    except ValueError:
        raise ErrorOpiniones("El registro debe tener un UUID válido y una fecha con zona UTC.") from None
    if registro["alien_id"] != registro["alien_id"].strip():
        raise ErrorOpiniones("El ID del alien no debe tener espacios exteriores.")
    if not 5 <= len(registro["opinion_original"].strip()) <= 1000:
        raise ErrorOpiniones("La opinión debe tener entre 5 y 1000 caracteres.")
    if registro["sentimiento"] not in ("positivo", "negativo", "neutro", "mixto"):
        raise ErrorOpiniones("El sentimiento del registro no es válido.")
    if not 1 <= len(registro["razon"].strip()) <= 300:
        raise ErrorOpiniones("La razón debe tener entre 1 y 300 caracteres.")
    return registro


def crear_registro(alien: dict, texto: str, analisis: dict, modelo: str, version_prompt: str) -> dict:
    """Genera identidad y fecha en la aplicación; solo admite análisis pertinentes."""
    if not isinstance(analisis, dict) or analisis.get("es_pertinente") is not True:
        raise ErrorOpiniones("Solo se pueden guardar opiniones pertinentes con análisis válido.")
    registro = {
        "id": str(uuid4()),
        "fecha_utc": datetime.now(timezone.utc).isoformat(),
        "alien_id": alien["id"],
        "alien_nombre": alien["nombre"],
        "opinion_original": texto,
        "sentimiento": analisis.get("sentimiento"),
        "razon": analisis.get("razon"),
        "modelo": modelo,
        "version_prompt": version_prompt,
    }
    return _validar_registro(registro)


def _ruta_opiniones(ruta: str | Path) -> Path:
    ruta = Path(ruta)
    return ruta if ruta.is_absolute() else RAIZ_PROYECTO / ruta


def cargar_opiniones(ruta: str | Path = RUTA_OPINIONES) -> list[dict]:
    """Lee y valida sin modificar archivos. Un archivo ausente representa un archivo vacío."""
    ruta = _ruta_opiniones(ruta)
    try:
        datos = json.loads(ruta.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    except (OSError, UnicodeError, json.JSONDecodeError):
        raise ErrorOpiniones("No se pudo leer el archivo de opiniones. Revisa permisos, UTF-8 y JSON; no se modificó.") from None
    if (
        not isinstance(datos, dict) or set(datos) != {"version", "opiniones"}
        or type(datos["version"]) is not int or datos["version"] != 1
        or not isinstance(datos["opiniones"], list)
    ):
        raise ErrorOpiniones("El archivo de opiniones no cumple el esquema de versión 1; se conserva intacto.")
    ids = set()
    for registro in datos["opiniones"]:
        _validar_registro(registro)
        if registro["id"] in ids:
            raise ErrorOpiniones("El archivo de opiniones contiene IDs repetidos; se conserva intacto.")
        ids.add(registro["id"])
    return datos["opiniones"]


def guardar_opinion(ruta: str | Path, registro: dict) -> bool:
    """Añade atómicamente. Devuelve False si ya existe el mismo envío idéntico.

    No evita pérdidas por escritores concurrentes: usar solo un escritor local.
    """
    _validar_registro(registro)
    ruta = _ruta_opiniones(ruta)
    registros = cargar_opiniones(ruta)
    for existente in registros:
        if existente["id"] == registro["id"]:
            if existente != registro:
                raise ErrorOpiniones("El ID del envío ya existe con otros datos; no se sobrescribió.")
            return False
    contenido = json.dumps({"version": 1, "opiniones": [*registros, registro]}, ensure_ascii=False, indent=2)
    temporal = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=ruta.parent,
            prefix=f".{ruta.name}.", suffix=".tmp", delete=False,
        ) as archivo:
            temporal = Path(archivo.name)
            archivo.write(contenido + "\n")
            archivo.flush()
            os.fsync(archivo.fileno())
        os.replace(temporal, ruta)
    except (OSError, UnicodeError):
        raise ErrorOpiniones("No se pudo guardar la opinión. Revisa permisos y espacio disponible; puedes reintentar.") from None
    finally:
        if temporal is not None:
            try:
                temporal.unlink(missing_ok=True)
            except OSError:
                pass
    return True


def consultar_opiniones(
    registros: list[dict], alien_id: str | None = None, sentimiento: str | None = None,
) -> list[dict]:
    """Filtra registros ya validados por ID y categoría, sin E/S ni mutaciones.

    None significa todos. Los dos filtros se combinan con AND y mantienen
    el orden del archivo; nombres repetidos no mezclan identidades.
    """
    if sentimiento is not None and sentimiento not in ("positivo", "negativo", "neutro", "mixto"):
        raise ErrorOpiniones("El filtro de sentimiento no es válido.")
    return [dict(registro) for registro in registros if (
        (alien_id is None or registro["alien_id"] == alien_id)
        and (sentimiento is None or registro["sentimiento"] == sentimiento)
    )]
