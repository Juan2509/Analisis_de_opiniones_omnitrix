# Usar Gemini gratuitamente en Archivo Omnitrix

La aplicación está adaptada a Gemini Developer API mediante LangChain. No utiliza la clave anterior de OpenAI, no llama a Vertex AI y no cambia automáticamente de proveedor o modelo. Para mantener el uso sin pago, la clave debe pertenecer a un proyecto **Free Tier sin facturación vinculada**.

## 1. Abrir Google AI Studio

Entrar en [Google AI Studio — claves](https://aistudio.google.com/apikey) e iniciar sesión con una cuenta Google que permita usar el servicio. Aceptar las condiciones si aparecen. No es necesario contratar Google AI Pro o Ultra para este proyecto.

La [guía oficial de claves](https://ai.google.dev/gemini-api/docs/api-key) explica que, para usuarios nuevos, AI Studio puede crear un proyecto y una clave predeterminados después de aceptar las condiciones. Si ya hay una clave en un proyecto gratuito, se puede utilizar; no hace falta crear claves repetidas.

## 2. Crear o elegir una clave gratuita

En la página de claves, buscar **Create API key / Crear clave de API**. Si ya hay un proyecto predeterminado gratuito, seleccionarlo. Si el diálogo permite crear un proyecto, usar un nombre como `Archivo Omnitrix`. La posición exacta de los botones puede variar.

Antes de copiar la clave, revisar la columna **Plan / Quota tier / Nivel de cuota** del proyecto. Debe indicar **Free Tier** o **Free / Gratuito**. Un enlace o botón **Set up billing** invita a cambiar de modalidad: no pulsarlo. No introducir tarjeta, comprar créditos ni vincular una cuenta de facturación.

Si aparece **Paid**, **Payment needed**, **Free tier unavailable**, **Restricted** o se exige activar pagos para continuar, detener ese recorrido y revisar el aviso. Crear una clave no garantiza por sí solo cuota gratuita. No cambiar al plan de pago para resolverlo. Si se comparte una captura para recibir ayuda, ocultar clave y datos personales.

La [documentación de facturación](https://ai.google.dev/gemini-api/docs/billing) distingue proyectos Free Tier y Paid Tier; la modalidad depende del proyecto al que pertenece la clave. La app no puede verificar tu estado de facturación con esa clave, de modo que elegir un proyecto gratuito es necesario. La adaptación de código por sí sola no convierte en gratuita una cuenta de pago.

## 3. Pegar la clave únicamente en el archivo local

En VS Code, abrir `.env` en la misma carpeta que `app.py`. Si no existe, copiar `.env.example` y nombrar la copia exactamente `.env`. Completar:

```dotenv
GOOGLE_API_KEY=PEGA_AQUI_LA_CLAVE_DE_GOOGLE
GEMINI_MODEL=gemini-3.5-flash-lite
GEMINI_TEMPERATURE=
```

Reemplazar `PEGA_AQUI_LA_CLAVE_DE_GOOGLE` por el valor real. No añadir espacios alrededor de `=`. Guardar con Ctrl+S. La temperatura queda vacía para utilizar la configuración recomendada de la integración para Gemini 3.x.

Las antiguas líneas `OPENAI_API_KEY`, `OPENAI_MODEL` y `OPENAI_TEMPERATURE`, si existen, ya no son leídas por el clasificador. No es necesario compartirlas ni copiarlas a los nuevos campos. No pegar claves en el chat, capturas o commits. `.env` está excluido de Git. Si hay variables del sistema con estos mismos nombres, tienen prioridad sobre `.env`.

El modelo preparado es `gemini-3.5-flash-lite`; admite [salida estructurada](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite). Revisar en AI Studio que tenga cuota gratuita disponible para el proyecto. La disponibilidad y los límites pueden cambiar; la [tabla de precios](https://ai.google.dev/gemini-api/docs/pricing) distingue columnas gratuitas y pagadas. No elegir otros modelos o habilitar pagos si no hay acceso gratuito.

## 4. Reiniciar y probar

1. En la ventana de inicio, pulsar **Detener y cerrar**.
2. Abrir `Iniciar Archivo Omnitrix.vbs` con doble clic.
3. Elegir Fuego y enviar: «Fuego es el mejor alien».
4. Revisar sentimiento y razón, y confirmar que aparezca «Opinión guardada en el Archivo Omnitrix».
5. En Consultar archivo, filtrar por Fuego y comprobar el registro.

Se conserva el contrato del taller: `ChatPromptTemplate`, composición con `|`, `invoke`, Pydantic, pertinencia, cuatro sentimientos y persistencia. Los ejemplos no sustituyen a los resultados reales.

## 5. Si falla

- **GOOGLE_API_KEY sin configurar:** comprobar nombre del archivo, campo y guardado. No usar la clave de OpenAI en ese campo.
- **Credenciales o acceso rechazados:** comprobar que la clave es de AI Studio y el proyecto tiene acceso Free Tier. No activar pagos si el aviso los solicita.
- **Límite o cuota:** revisar las [cuotas del proyecto](https://aistudio.google.com/rate-limit). Esperar el restablecimiento que indique el servicio; reenviar continuamente consume solicitudes y no garantiza acceso. No pasar al plan pagado.
- **Modelo no disponible:** compartir solo el mensaje de error para revisar una alternativa gratuita compatible; la aplicación no elige otra automáticamente.

La modalidad gratuita tiene límites: no es uso ilimitado ni se garantiza disponibilidad para todas las cuentas o regiones. Si tu cuenta no ofrece acceso sin pagos, queda por evaluar una alternativa local. No es necesario pagar para completar esa evaluación de alternativas.

## Cambios y comprobación

Se reemplazó `langchain-openai` por `langchain-google-genai==4.4.3`, se adaptaron mensajes/errores y se actualizó el diagnóstico del lanzador. `vertexai=False` fuerza Gemini Developer API; `max_retries=1` significa un solo intento total en esta integración. Timeout: 30 segundos. El adaptador y su parser se prueban con transporte simulado, sin inferencias reales ni consumo de cuota.

La instalación de paquetes no habilita facturación. La configuración de una clave propia y la evaluación real quedan pendientes del usuario. La implementación se basa en la [integración oficial de LangChain](https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai).
