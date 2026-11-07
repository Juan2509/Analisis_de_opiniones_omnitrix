"""Entrada al dashboard y persistencia de activación, sin inferencias ni audio."""

import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from almacenamiento import RAIZ_PROYECTO


class PruebasPantallaInicio(unittest.TestCase):
    def nueva_app(self):
        return AppTest.from_file(str(RAIZ_PROYECTO / "app.py"), default_timeout=15)

    def test_sesion_nueva_espera_activacion_sin_cargar_catalogo_ni_ia(self):
        with patch("almacenamiento.cargar_aliens") as cargar, patch("analisis.analizar_opinion") as analizar:
            app = self.nueva_app().run()
            self.assertFalse(app.exception)
            self.assertFalse(app.radio)
            self.assertFalse(app.selectbox)
            self.assertFalse(app.chat_input)
            cargar.assert_not_called()
            analizar.assert_not_called()

    def test_evento_de_activacion_abre_dashboard_y_no_se_repite_al_navegar(self):
        app = self.nueva_app()
        # Simular únicamente el aviso del navegador al terminar su animación.
        with patch("pantalla_inicio.ACTIVACION") as componente:
            componente.side_effect = lambda **opciones: opciones["on_activar_change"]()
            app.run()
            self.assertFalse(app.exception)
            self.assertTrue(app.session_state["omnitrix_activado"])
            self.assertEqual(componente.call_count, 1)
            app.run()
            self.assertEqual(len(app.selectbox[0].options), 20)
            app.radio[0].set_value("Consultar archivo").run()
            app.radio[0].set_value("Analizar opinión").run()
            app.button(key="nueva_conversacion").click().run()
            self.assertFalse(app.exception)
            self.assertTrue(app.session_state["omnitrix_activado"])
            self.assertEqual(componente.call_count, 1)

    def test_otra_sesion_comienza_con_la_pantalla_inicial(self):
        primera = self.nueva_app()
        primera.session_state["omnitrix_activado"] = True
        primera.run()
        self.assertTrue(primera.chat_input)
        segunda = self.nueva_app().run()
        self.assertFalse(segunda.exception)
        self.assertFalse(segunda.chat_input)
        self.assertFalse(segunda.radio)


if __name__ == "__main__":
    unittest.main()
