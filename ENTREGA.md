# Guía de entrega y sustentación

Último paso del plan: 13, documentación. La documentación está preparada; la aceptación completa permanece condicionada a las comprobaciones reales pendientes de `VERIFICACION.md`.

## Material para revisar

| Material | Ubicación |
| --- | --- |
| Instalación, configuración, inicio y uso | [README](README.md) |
| Decisiones y contratos técnicos | [Contexto](CONTEXTO_PROYECTO.md) |
| Etapas, verificaciones y commits sugeridos | [Plan](PLAN_DESARROLLO.md) |
| Pruebas, limitaciones y dos reflexiones | [Registro de aceptación](VERIFICACION.md) |
| Resultado vigente de 68 pruebas y versiones | [Pruebas Gemini](evidencias/pruebas-gemini-windows.txt), [dependencias](evidencias/dependencias-windows.txt) |
| Configuración para uso sin pago | [Guía de Gemini Free Tier](GEMINI_GRATIS.md) |
| Persistencia entre procesos y filtrado reproducidos | [Registro](evidencias/persistencia-y-filtro.json), [selección exportada](evidencias/consulta-xlr8-mixto.json) |
| 16 opiniones ficticias y seis casos adicionales | [Ejemplos y procedencia manual](datos/ejemplos/README.md) |
| Imágenes locales y sus fuentes | [Créditos](assets/aliens/README.md), [manifiesto](assets/aliens/fuentes.json) |

No incluir `.env`, secretos, `.venv`, `.python-runtime`, `.herramientas` ni logs privados en una entrega del repositorio. Los ejemplos se conservan separados del archivo de opiniones de uso. No hay licencia libre acreditada para las imágenes de terceros.

## Cómo explicar el proyecto

1. Presentar el objetivo: clasificar lo expresado por un aficionado sobre un alien, con persistencia y consulta. La aplicación no mide objetivamente la calidad del personaje.
2. Mostrar el catálogo: 20 IDs estables, cinco transformaciones de cada serie, nombres latinos y diseños locales de Omniverse; la serie de introducción es un dato distinto del diseño mostrado.
3. Explicar el envío: validación de longitud, captura de selección y conservación del original. El historial visual no se envía al clasificador.
4. Recorrer `analisis.py`: mensajes system/human, composición mediante `|`, `invoke`, salida Pydantic, pertinencia y cuatro categorías. Explicar la diferencia entre respuesta del modelo y resultado validado, y entre un error y un sentimiento neutro.
5. Recorrer `almacenamiento.py`: identidad y fecha generadas por la aplicación, JSON versionado, temporal/reemplazo, rechazo de conflictos y límite de un solo escritor. Un reintento conserva el envío; dos envíos independientes iguales tienen IDs distintos.
6. Mostrar que tabla, total, recuentos y descarga proceden de la misma selección filtrada. Consultar no vuelve a analizar ni escribe.
7. Explicar las pruebas: cuáles usan archivos/procesos/servidor reales y cuáles usan respuestas simuladas. Los ejemplos y expectativas manuales no demuestran precisión de un LLM.

## Demostración sin acceso a API

Se puede abrir el catálogo y consultar el archivo existente con el lanzador. Si no hay opiniones de uso, el estado vacío es correcto. No cargar ejemplos en el archivo real para aparentar análisis obtenidos de una API.

Para demostrar persistencia y filtros con los ejemplos, el preparador puede ejecutar:

```powershell
.\.venv\Scripts\python.exe scripts\generar_evidencias.py
```

El script escribe en una carpeta temporal, lee desde otro proceso y exporta la opinión de XLR8/mixto a `evidencias/`. Comprueba que reintentar no duplica registros y que el archivo de uso no cambia. El JSON exportado conserva `modelo: manual:no-ejecutado`; la clasificación fue humana y el procedimiento de almacenamiento/consulta se ejecutó realmente.

## Cierre de aceptación pendiente

| Comprobación pendiente | Evidencia que debe registrarse |
| --- | --- |
| Modelo real compatible | Nombre configurado, versión del prompt y resultados observados, sin claves. |
| Elogio, crítica, neutralidad y mixto | Opinión original, categoría y razón obtenidas; coincidencias y discrepancias frente a la referencia humana. |
| Ironía, ambigüedad y contexto | Lectura del resultado y discusión; no asumir que la referencia es infalible. |
| Texto ajeno e instrucciones embebidas | Resultado observado, rechazo cuando corresponda y ausencia de guardado de rechazos. |
| Envío real, cierre y reapertura | Registro recuperable en Consultar archivo y asociación al alien correcto. |
| Filtros y descarga en navegador | Coincidencia entre tabla, total, categorías y archivo descargado. |
| Cierre desde el controlador | Servidor detenido después de «Detener y cerrar». |

Los casos de referencia están en `datos/ejemplos/casos_evaluacion.json`; todavía no contienen resultados obtenidos. Registrar los resultados reales en una evidencia nueva y actualizar `VERIFICACION.md` antes de cerrar las casillas pendientes. No usar capturas con claves o información privada.

## Estado del repositorio

Los nombres de commit son sugerencias. No se ejecutan commits ni push automáticamente. El paso 13 sugiere:

```text
docs: documentar instalación pruebas y entrega final
```

Los cambios de verificación del paso 12 pueden seguir sin confirmar. Revisar el diff para mantenerlos separados de la documentación cuando se preparen los commits.
