"""Pruebas del cargador con archivos temporales y sin servicios externos."""

from copy import deepcopy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from almacenamiento import ErrorCatalogo, RUTA_CATALOGO, cargar_aliens


class PruebasCatalogo(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.ruta = Path(self.temporal.name) / "catalogo.json"
        self.datos = json.loads(RUTA_CATALOGO.read_text(encoding="utf-8"))

    def escribir(self, datos):
        self.ruta.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")

    def comprobar_rechazo(self, datos, mensaje):
        self.escribir(datos)
        contenido = self.ruta.read_bytes()
        with self.assertRaisesRegex(ErrorCatalogo, mensaje):
            cargar_aliens(self.ruta)
        self.assertEqual(self.ruta.read_bytes(), contenido)

    def test_catalogo_real(self):
        contenido = RUTA_CATALOGO.read_bytes()
        aliens = cargar_aliens()
        self.assertEqual(aliens, self.datos["aliens"])
        self.assertEqual(len(aliens), 63)
        self.assertEqual(len({alien["id"] for alien in aliens}), 63)
        self.assertEqual(RUTA_CATALOGO.read_bytes(), contenido)

    def test_catalogo_puede_crecer_sin_cambiar_ids_existentes(self):
        nuevo = deepcopy(self.datos["aliens"][0])
        nuevo.update(id="a064", nombre="Alien de prueba")
        self.datos["aliens"].append(nuevo)
        self.escribir(self.datos)
        self.assertEqual(cargar_aliens(self.ruta), self.datos["aliens"])

    def test_especies_cubren_catalogo_y_distinguen_incertidumbre(self):
        aliens = {a["id"]: a for a in cargar_aliens()}
        desconocidos = {"a020", "a055", "a057", "a058", "a059", "a061", "a062"}
        self.assertEqual({a["id"] for a in aliens.values()
                          if a["estado_especie"] == "sin_nombre_confirmado"}, desconocidos)
        self.assertEqual({a["id"] for a in aliens.values()
                          if a["estado_especie"] == "hibrida"}, {"a045"})
        for alien in aliens.values():
            self.assertTrue(alien["especie"].strip())
            self.assertTrue(alien["fuentes_especie"])
        for alien_id, especie in {
            "a014": "Geochelone Aerios", "a019": "Orthopterran",
            "a031": "Gourmand (subespecie Perk)", "a035": "Sphoeroid",
            "a043": "Biotsavartian", "a046": "Gourmand (subespecie Murk)",
            "a063": "Vladat",
        }.items():
            self.assertEqual(aliens[alien_id]["especie"], especie)

    def test_extension_especies_conserva_compatibilidad_con_catalogo_anterior(self):
        for alien in self.datos["aliens"]:
            for campo in ("especie", "estado_especie", "fuentes_especie"):
                del alien[campo]
        self.escribir(self.datos)
        self.assertEqual(cargar_aliens(self.ruta), self.datos["aliens"])

    def test_rechaza_metadatos_de_especies_invalidos(self):
        for campo, valores in {
            "especie": (None, "", " ", 10, []),
            "estado_especie": (None, "", "inventada", [], True),
            "fuentes_especie": (None, [], "https://ejemplo.com", [None],
                                ["javascript:alert(1)"], ["http://ejemplo.com"],
                                ["https:///sin-host"], ["https://ejemplo.com/ )"]),
        }.items():
            for valor in valores:
                with self.subTest(campo=campo, valor=valor):
                    datos = deepcopy(self.datos)
                    datos["aliens"][0][campo] = valor
                    self.comprobar_rechazo(datos, campo)

    def test_rutas_independientes_del_directorio_de_inicio(self):
        anterior = Path.cwd()
        try:
            os.chdir(self.temporal.name)
            self.assertEqual(cargar_aliens(), self.datos["aliens"])
            self.assertEqual(cargar_aliens("datos/aliens.json"), self.datos["aliens"])
        finally:
            os.chdir(anterior)

    def test_archivo_ausente_no_se_crea(self):
        with self.assertRaisesRegex(ErrorCatalogo, "No se encontró"):
            cargar_aliens(self.ruta)
        self.assertFalse(self.ruta.exists())

    def test_json_danado_se_conserva(self):
        contenido = '{"version": 1, "aliens": ['
        self.ruta.write_text(contenido, encoding="utf-8")
        with self.assertRaisesRegex(ErrorCatalogo, "JSON inválido.*línea 1"):
            cargar_aliens(self.ruta)
        self.assertEqual(self.ruta.read_text(encoding="utf-8"), contenido)

    def test_codificacion_invalida_se_conserva(self):
        self.ruta.write_bytes(b"\xff\xfe")
        with self.assertRaisesRegex(ErrorCatalogo, "UTF-8"):
            cargar_aliens(self.ruta)
        self.assertEqual(self.ruta.read_bytes(), b"\xff\xfe")

    def test_error_de_permisos(self):
        with patch.object(Path, "read_text", side_effect=PermissionError):
            with self.assertRaisesRegex(ErrorCatalogo, "No se pudo leer"):
                cargar_aliens(self.ruta)

    def test_directorio_en_lugar_de_archivo(self):
        with self.assertRaisesRegex(ErrorCatalogo, "No se pudo leer"):
            cargar_aliens(self.ruta.parent)

    def test_raiz_invalida(self):
        for raiz in ([], None, "catálogo", 1):
            with self.subTest(raiz=raiz):
                self.comprobar_rechazo(raiz, "raíz")

    def test_version_invalida_o_ausente(self):
        for version in (None, 2, "1", True, 1.0):
            with self.subTest(version=version):
                datos = deepcopy(self.datos)
                datos["version"] = version
                self.comprobar_rechazo(datos, "version")
        del self.datos["version"]
        self.comprobar_rechazo(self.datos, "version")

    def test_lista_invalida_o_ausente(self):
        for valor in (None, {}, "aliens"):
            with self.subTest(valor=valor):
                datos = deepcopy(self.datos)
                datos["aliens"] = valor
                self.comprobar_rechazo(datos, "debe ser una lista")
        del self.datos["aliens"]
        self.comprobar_rechazo(self.datos, "debe ser una lista")

    def test_minimo_de_veinte_aliens(self):
        for cantidad in (0, 19):
            with self.subTest(cantidad=cantidad):
                datos = deepcopy(self.datos)
                datos["aliens"] = datos["aliens"][:cantidad]
                self.comprobar_rechazo(datos, "al menos 20")

    def test_registro_invalido(self):
        self.datos["aliens"][0] = []
        self.comprobar_rechazo(self.datos, "posición 1.*objeto JSON")

    def test_campos_obligatorios(self):
        for campo in self.datos["aliens"][0]:
            with self.subTest(campo=campo):
                datos = deepcopy(self.datos)
                del datos["aliens"][0][campo]
                self.comprobar_rechazo(datos, f"falta el campo '{campo}'")

    def test_campos_de_texto_invalidos(self):
        for campo in ("id", "nombre", "nombre_original", "serie_origen", "descripcion"):
            for valor in (None, 1, True, [], "", "   "):
                with self.subTest(campo=campo, valor=valor):
                    datos = deepcopy(self.datos)
                    datos["aliens"][0][campo] = valor
                    self.comprobar_rechazo(datos, f"'{campo}' debe ser texto no vacío")

    def test_ids_repetidos(self):
        self.datos["aliens"][1]["id"] = self.datos["aliens"][0]["id"]
        self.comprobar_rechazo(self.datos, "ID repetido 'a001'")

    def test_id_con_espacios_exteriores(self):
        self.datos["aliens"][0]["id"] = " a001 "
        self.comprobar_rechazo(self.datos, "ID no debe tener espacios exteriores")

    def test_imagenes_pendientes_o_locales_ausentes_permitidas(self):
        self.datos["aliens"][0]["imagen"] = "assets/aliens/imagen-pendiente.png"
        self.escribir(self.datos)
        self.assertEqual(cargar_aliens(self.ruta), self.datos["aliens"])

    def test_imagen_invalida(self):
        for imagen in (
            "", "  ", 1, True, [], "/tmp/fuego.png", "../fuego.png",
            "assets/../../fuego.png", "https://ejemplo.com/fuego.png",
            "C:/aliens/fuego.png", "C:\\aliens\\fuego.png", "\\\\servidor\\fuego.png",
            "assets/aliens/\x00.png",
        ):
            with self.subTest(imagen=imagen):
                datos = deepcopy(self.datos)
                datos["aliens"][0]["imagen"] = imagen
                self.comprobar_rechazo(datos, "'imagen' debe ser")


if __name__ == "__main__":
    unittest.main()
