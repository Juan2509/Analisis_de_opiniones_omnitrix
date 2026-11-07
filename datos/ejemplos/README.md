# Datos ficticios de aceptación

`opiniones_demo.json` contiene 16 opiniones inventadas: cuatro aliens y una opinión por cada categoría para cada uno. Las razones, categorías, UUID y fechas fueron preparados manualmente. `modelo: manual:no-ejecutado` y `version_prompt: demo-manual-v1` identifican su procedencia; no son análisis obtenidos de una API.

El archivo respeta el contrato de persistencia para probar lectura, filtros y exportación. No se incorpora automáticamente a `datos/opiniones.json`, que conserva los datos de uso. Las pruebas trabajan con copias en carpetas temporales; no hace falta sustituir el archivo real.

`casos_evaluacion.json` añade ironía, una clasificación ambigua, texto ajeno, instrucciones embebidas y contexto implícito. Sus resultados esperados son referencias humanas para discutir con el modelo elegido, no garantías de exactitud. La evaluación real debe registrar modelo, versión del prompt, resultado obtenido y discrepancias. Ver `VERIFICACION.md` en la raíz para resultados y pendientes.
