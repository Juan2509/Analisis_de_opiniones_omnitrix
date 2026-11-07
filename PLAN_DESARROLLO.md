# Plan y estado actual — Archivo Omnitrix

Actualizado el 7 de noviembre de 2026. El [plan histórico](docs/PLAN_HISTORICO.md) conserva el desarrollo por commits, estados intermedios y hashes registrados. Este documento resume lo implementado y las comprobaciones que faltan.

## Plan original

| Paso | Resultado implementado |
| --- | --- |
| 1. Alcance y requisitos | Adaptación académica a Ben 10 y contratos funcionales. |
| 2. Estructura y configuración | Módulos, dependencias, entorno y exclusión de secretos. |
| 3. Catálogo | Inicialmente 20; ampliado a 63 fichas con IDs estables. |
| 4. Lectura y validación | Catálogo UTF-8, esquema, rutas e IDs comprobados. |
| 5. Navegación | Aplicación Streamlit en navegador. |
| 6. Fichas e imágenes | Recursos locales, habilidades, origen y alternativa de imagen. |
| 7. Captura de opiniones | Validación, asociación e historial de sesión. |
| 8. Clasificación | LangChain/Pydantic y Gemini con configuración local. |
| 9. Persistencia | JSON versionado, guardado y reintentos idempotentes. |
| 10. Consulta/exportación | Filtros, tabla, recuentos y descarga JSON coherentes. |
| 11. Inicio gráfico | VBS y controlador de Windows; arranque manual documentado. |
| 12. Datos y verificación | Ejemplos, casos, pruebas y evidencias; evaluación semántica pendiente. |
| 13. Documentación | Guías actuales de uso, instalación, arquitectura, verificación y entrega. |

Implementado no significa que toda aceptación manual o compatibilidad esté cerrada. Los pendientes están al final y en [VERIFICACION.md](VERIFICACION.md).

## Ampliaciones posteriores

| Ampliación | Estado actual | Commit sugerido |
| --- | --- | --- |
| Uso de Gemini sin pagos | Integración y errores, sin fallback; usuario confirmó funcionamiento. | `feat(analisis): integrar Gemini para uso en modalidad gratuita` |
| Identidad del Omnitrix | Imagen local en portada, marca, favicon y entrada. | `feat(ui): integrar símbolo del Omnitrix` |
| Entrada audiovisual | Dos pulsaciones, sonidos locales, pantalla verde y sidebar cubierto. | `feat(ui): activar el Omnitrix en dos pulsaciones con sonidos` |
| Catálogo completo del alcance | 63 fichas, imágenes/fuentes y datos originales conservados. | `feat(catalogo): ampliar a 63 transformaciones de Ben 10` |
| Desafíos | Evaluación de situaciones y estado de sesión. | `feat(desafios): agregar desafíos del Omnitrix evaluados con Gemini` |
| Submodos | Control maestro, Héroe bajo presión y Adaptabilidad. | `feat(desafios): agregar adaptabilidad y cierre de rondas` |
| Comparación de opciones | Tres fichas consultables en pestañas antes de elegir. | `feat(desafios): mostrar fichas de los tres aliens disponibles` |
| Situaciones | 32 en total, incluidas 20 nuevas de combate/seguridad/rescate. | `feat(desafios): agregar 20 situaciones de combate seguridad y rescate` |
| Consolidación documental | Windows/Linux, detalles actuales y separación del historial. | `docs: actualizar guías de Windows Linux y funciones actuales` |

Las sugerencias no implican que esos commits se hayan ejecutado. Revisar Git para conocer el estado confirmado y conservar cambios existentes.

## Comprobaciones realizadas

Última ejecución completa archivada: 87 pruebas Windows. Después se comprobaron las fichas comparables con 15 pruebas del juego y 20 de interfaz, y la ampliación a 32 situaciones con 15 del juego. El recorrido de rondas en los tres submodos se comprobó en escritorio/móvil con evaluaciones simuladas y sin API real. El historial de resultados menores y evidencias se conserva en [VERIFICACION.md](VERIFICACION.md).

## Pendientes reales

- Ejecutar y registrar una evaluación real de opiniones: cuatro sentimientos, texto ajeno, ironía e instrucciones incrustadas, con resultados y discrepancias frente a referencias humanas.
- Registrar evaluación real de estrategias en los tres submodos, incluyendo alternativas creativas y limitaciones del alien asignado.
- Cerrar el recorrido manual de envío, reinicio, recuperación, descarga desde navegador y cierre del controlador.
- Instalar y comprobar la versión actual en Linux. El procedimiento de terminal está documentado; el lanzador gráfico Linux no está implementado.
- Preparar la entrega sin secretos, entornos ni datos privados y revisar procedencia de recursos de terceros.

## Forma de continuar

1. Leer [contexto](CONTEXTO_PROYECTO.md), [instalación](INSTALACION.md) y [verificación](VERIFICACION.md).
2. Revisar código, datos, evidencias y cambios de Git antes de retomar etapas.
3. Mantener el requisito de no pagar y separar opiniones persistentes de partidas de sesión.
4. Comprobar cada cambio con pruebas proporcionadas a su alcance; no usar simulaciones como evidencia de precisión real.
5. Actualizar la documentación y proponer un Conventional Commit sin ejecutar commit/push automáticamente.

Formato de commit: `tipo(alcance opcional): descripción`; ejemplos de tipos: feat, fix, docs, test, chore y refactor.
