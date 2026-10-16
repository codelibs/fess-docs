====================
Modo de búsqueda IA
====================

Descripción general
====================

La función de modo de búsqueda IA (chat RAG) de |Fess| le permite buscar información en un
formato de conversación natural, además de la búsqueda tradicional por palabras clave.
Al introducir una pregunta, el asistente de IA busca los documentos relacionados y genera
una respuesta fácil de entender basada en su contenido.

.. note::
   El modo de búsqueda IA está deshabilitado de forma predeterminada. Para poder utilizarlo,
   el administrador del sistema debe habilitar la función y configurar previamente un
   proveedor de LLM (modelo de lenguaje de gran tamaño).
   Consulte :doc:`../config/rag-chat` y :doc:`../config/llm-overview` para obtener información
   sobre cómo configurarlo.

Características del modo de búsqueda IA
=========================================

Búsqueda en formato de conversación
-------------------------------------

En lugar de pensar en palabras clave, puede preguntar como en una conversación cotidiana.

Ejemplos:

- "Explíqueme cómo instalar Fess"
- "¿Cómo hago para rastrear archivos?"
- "¿Qué hacer cuando no se muestran los resultados de búsqueda?"

Respuestas que comprenden el contexto
---------------------------------------

El asistente de IA analiza la intención de la pregunta, busca los documentos relacionados y
extrae la información necesaria de varios resultados de búsqueda, presentándola de forma
organizada en la respuesta.

Indicación clara de las fuentes
-----------------------------------

En la parte inferior de la respuesta se muestra una lista de los documentos en los que se
basa la respuesta, bajo el título "Fuentes". Cada fuente es un enlace numerado; al hacer clic
en él puede consultar directamente el documento original.
Además, el cuerpo de la respuesta puede incluir citas numeradas como ``[1]`` o ``[2]``, que
corresponden a los números de la lista de fuentes.

Continuidad de la conversación
---------------------------------

No es necesario terminar tras una sola pregunta: puede continuar la conversación.
El asistente de IA responde a las preguntas adicionales teniendo en cuenta el contexto de las
preguntas y respuestas anteriores.

Cómo utilizar la búsqueda con chat
====================================

Abrir el modo de búsqueda IA
-------------------------------

1. Abra la pantalla de búsqueda de |Fess|
2. Haga clic en el enlace "Búsqueda IA" (icono de robot) de la barra de navegación superior
3. Se mostrará la pantalla del modo de búsqueda IA

.. note::
   El enlace "Búsqueda IA" solo se muestra cuando el modo de búsqueda IA está habilitado y
   hay un proveedor de LLM disponible. Si el enlace no aparece, consulte
   `Preguntas frecuentes`_.

Introducir una pregunta
--------------------------

1. Introduzca la pregunta en el cuadro de texto de la parte inferior de la pantalla (hasta
   4000 caracteres por pregunta)
2. Haga clic en el botón "Enviar mensaje" (icono de avión de papel) o pulse la tecla Enter
3. El asistente de IA comenzará a generar la respuesta

.. note::
   Si desea insertar un salto de línea, pulse Shift+Enter en lugar de Enter.

.. note::
   La generación de la respuesta puede tardar entre varios segundos y algo más de diez
   segundos. Mientras se procesa, la etapa actual se muestra mediante un indicador de
   progreso (Analizar → Buscar → Evaluar → Obtener → Responder), junto con mensajes como
   "Pensando...", "Buscando...", "Verificando resultados...", "Obteniendo documentos..." o
   "Generando respuesta...". Cuando la búsqueda finaliza, también se muestra el número de
   documentos encontrados.

Comprobar la respuesta
--------------------------

Se muestra la respuesta del asistente de IA. La respuesta incluye la siguiente información:

- **Cuerpo de la respuesta**: la respuesta a la pregunta (con formato Markdown)
- **Fuentes**: una lista de enlaces a los documentos en los que se basa la respuesta
  (enlaces numerados; al hacer clic se abre el documento original en otra pestaña)

El cuerpo de la respuesta puede incluir números de cita como ``[1]`` o ``[2]``, que
corresponden a los números de la lista de fuentes.
Cada respuesta tiene un botón de copiar que permite copiar su contenido al portapapeles.

.. note::
   La IA utiliza como base de la respuesta únicamente los documentos superiores que
   considera más relevantes entre los resultados de búsqueda. Por este motivo, el número de
   fuentes puede ser menor que el número de documentos encontrados en la búsqueda.

Acotar el ámbito de búsqueda
--------------------------------

Según el tema, puede utilizar el botón "Filtro" situado en la parte superior de la pantalla
para acotar el ámbito de búsqueda mediante condiciones como etiquetas, tipo de archivo, fecha
de actualización o tamaño. Esto resulta útil cuando desea consultar a la IA únicamente sobre
un conjunto específico de documentos.

Continuar la conversación
------------------------------

Si tiene preguntas adicionales, puede continuar preguntando sin más:

- "¿Podría explicarlo con más detalle?"
- "¿Hay otra forma de hacerlo?"
- "Más información sobre XXX"

El asistente de IA responde teniendo en cuenta el contexto de la conversación anterior.

Iniciar una nueva conversación
-----------------------------------

Si desea preguntar sobre otro tema, haga clic en el botón "Nueva conversación" (icono +).
Esto borra el historial de la conversación anterior y le permite iniciar una nueva
conversación.

Consejos para hacer preguntas eficaces
========================================

Hacer preguntas específicas
-------------------------------

Las preguntas específicas obtienen respuestas más adecuadas que las preguntas ambiguas.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Pregunta ambigua
     - Pregunta específica
   * - ¿Cómo se configura?
     - ¿Cómo cambio la configuración de memoria de Fess?
   * - Aparece un error
     - Al buscar aparece el error "no se encuentra el índice"
   * - Sobre el crawling
     - ¿Cómo configuro las exclusiones al rastrear un sitio web?

Incluir información de contexto
-----------------------------------

Incluir la situación o el propósito ayuda a obtener respuestas más adecuadas.

Buenos ejemplos:

- "Estoy ejecutando Fess en un entorno Docker. Quiero cambiar la ubicación donde se guardan
  los registros, ¿cómo puedo hacerlo?"
- "Es la primera vez que uso Fess. ¿Qué debo hacer primero?"

Hacer preguntas paso a paso
-------------------------------

Los problemas complejos son más fáciles de entender si se preguntan paso a paso.

1. "¿Puedo rastrear archivos compartidos con Fess?"
2. "Explíqueme cómo conectarme mediante el protocolo SMB"
3. "¿Qué debo hacer si la carpeta compartida requiere autenticación?"

Preguntas frecuentes
======================

P: No se muestra el modo de búsqueda IA
-----------------------------------------

R: Es posible que el modo de búsqueda IA no esté habilitado.
El enlace "Búsqueda IA" solo se muestra cuando la función está habilitada
(``rag.chat.enabled=true``) y hay un proveedor de LLM (OpenAI, Gemini, Ollama, etc.)
configurado y disponible. Consulte con el administrador del sistema si el modo de búsqueda
IA está habilitado y si el proveedor de LLM está configurado correctamente (para más
información, consulte :doc:`../config/rag-chat`).

P: La respuesta tarda en mostrarse
--------------------------------------

R: Como la IA analiza la pregunta y busca y evalúa los documentos antes de generar la
respuesta, el proceso puede tardar entre varios segundos y algo más de diez segundos.
Mientras se procesa, se muestra la etapa actual ("Pensando...", "Buscando...",
"Verificando resultados...", "Obteniendo documentos...", "Generando respuesta...").

P: Las fuentes parecen incorrectas
--------------------------------------

R: Haga clic en el enlace de la fuente para verificar el documento original.
Aunque la IA genera las respuestas a partir de los resultados de búsqueda, puede haber
errores de interpretación. Se recomienda confirmar siempre la información importante en el
documento original.

P: Parece que se ha olvidado la conversación anterior
----------------------------------------------------------

R: Es posible que la sesión de la conversación haya expirado.
Si no se realiza ninguna operación durante un período determinado (30 minutos de forma
predeterminada), el historial de la conversación se borra.
Además, como el historial de la conversación se conserva temporalmente en la memoria del
servidor, también se pierde al reiniciar el servidor.
En ese caso, inicie una nueva conversación.

.. note::
   La "sesión" a la que se hace referencia aquí es la sesión de conversación del modo de
   búsqueda IA, distinta de la sesión de inicio de sesión en |Fess|.

P: No obtengo respuesta para una pregunta concreta
--------------------------------------------------------

R: Existen varias causas posibles:

- No hay información relacionada en los documentos que se están buscando
- La pregunta es ambigua y no permite realizar una búsqueda adecuada
- Se ha alcanzado el límite de tasa (se ha superado el número máximo de solicitudes por
  minuto o el número máximo de ejecuciones simultáneas)

Intente reformular la pregunta o espere un momento antes de volver a intentarlo.

P: ¿Existe un límite de caracteres para la entrada?
---------------------------------------------------------

R: El límite es de 4000 caracteres por pregunta. Debajo del cuadro de texto se muestra un
contador de caracteres, que cambia a una advertencia cuando se acerca al límite. Si la
pregunta es larga, resúmala centrándose en los puntos clave.

P: ¿Puedo hacer preguntas en idiomas distintos al español?
-----------------------------------------------------------

R: Sí, en muchos casos puede hacer preguntas también en inglés o en otros idiomas.
La IA intenta responder en el mismo idioma basándose en el idioma de visualización del
navegador o de la pantalla, en la medida de lo posible. No obstante, esto se realiza sobre
una base de mejor esfuerzo, por lo que, dependiendo de la situación, es posible que la
respuesta no se genere en el idioma esperado.

Notas
======

Sobre las respuestas de la IA
---------------------------------

- Las respuestas de la IA se generan a partir de los resultados de búsqueda
- No se garantiza la exactitud de las respuestas
- Para decisiones importantes, confirme siempre la información en el documento original
  (fuente)
- Para obtener la información más reciente, consulte la documentación oficial

Sobre la privacidad
------------------------

- Las preguntas introducidas se utilizan para la búsqueda y para el procesamiento de IA
  realizado por el proveedor de LLM configurado
- Si se configura para utilizar un servicio de LLM externo (como OpenAI o Gemini), el
  contenido de la pregunta y los resultados de búsqueda se envían a dicho servicio. Si desea
  que el procesamiento se realice únicamente dentro de la organización, consulte con el
  administrador sobre el uso de un proveedor que funcione de forma local (como Ollama)
- El historial de la conversación se conserva temporalmente en la memoria del servidor y se
  elimina cuando la sesión expira, cuando se ejecuta "Nueva conversación", o cuando se
  reinicia el servidor
- Al igual que en la búsqueda, se aplica el control de acceso basado en roles (permisos) y
  etiquetas, por lo que los documentos que no se pueden visualizar no forman parte de la
  respuesta
- Según la configuración del sistema, es posible que se registren logs

Información de referencia
============================

- :doc:`../config/rag-chat` - Configuración de la función de modo de búsqueda IA (para
  administradores)
- :doc:`../config/llm-overview` - Configuración del proveedor de LLM
- :doc:`../api/api-chat` - Chat API (uso mediante programación)
- :doc:`search-and` - Cómo utilizar la búsqueda AND
- :doc:`search-not` - Cómo utilizar la búsqueda NOT
- :doc:`search-field` - Cómo utilizar la búsqueda por campo
- :doc:`advanced-search` - Funciones de búsqueda avanzada
