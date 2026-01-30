==========================
Configuracion de la funcionalidad de chat RAG
==========================

Descripcion general
===================

El chat RAG (Retrieval-Augmented Generation) es una funcionalidad que extiende los resultados de busqueda de |Fess| con LLM (Modelo de Lenguaje Grande),
proporcionando informacion en formato de dialogo. Los usuarios pueden hacer preguntas en lenguaje natural
y obtener respuestas detalladas basadas en los resultados de busqueda.

Como funciona el chat RAG
=========================

El chat RAG opera con el siguiente flujo de multiples etapas.

1. **Fase de analisis de intencion**: Analiza la pregunta del usuario y extrae las palabras clave mas adecuadas para la busqueda
2. **Fase de busqueda**: Busca documentos usando el motor de busqueda de |Fess| con las palabras clave extraidas
3. **Fase de evaluacion**: Evalua la relevancia de los resultados de busqueda y selecciona los documentos mas apropiados
4. **Fase de generacion**: El LLM genera una respuesta basada en los documentos seleccionados
5. **Fase de salida**: Devuelve la respuesta y la informacion de fuentes al usuario

Este flujo permite respuestas de alta calidad con comprension del contexto, superiores a la simple busqueda por palabras clave.

Configuracion basica
====================

Configuracion basica para habilitar la funcionalidad de chat RAG.

``app/WEB-INF/conf/system.properties``:

::

    # Habilitar la funcionalidad de chat RAG
    rag.chat.enabled=true

    # Seleccionar el proveedor LLM (ollama, openai, gemini)
    rag.llm.type=ollama

Para la configuracion detallada de proveedores LLM, consulte:

- :doc:`llm-ollama` - Configuracion de Ollama
- :doc:`llm-openai` - Configuracion de OpenAI
- :doc:`llm-gemini` - Configuracion de Google Gemini

Parametros de generacion
========================

Parametros que controlan el comportamiento de generacion del LLM.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.chat.max.tokens``
     - Numero maximo de tokens a generar
     - ``4096``
   * - ``rag.chat.temperature``
     - Aleatoriedad de la generacion (0.0-1.0)
     - ``0.7``

Configuracion de temperature
----------------------------

- **0.0**: Respuestas deterministicas (siempre la misma respuesta para la misma entrada)
- **0.3-0.5**: Respuestas consistentes (apropiado para preguntas basadas en hechos)
- **0.7**: Respuestas equilibradas (predeterminado)
- **1.0**: Respuestas creativas (apropiado para lluvia de ideas, etc.)

Configuracion de contexto
=========================

Configuracion del contexto pasado al LLM desde los resultados de busqueda.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.chat.context.max.documents``
     - Numero maximo de documentos a incluir en el contexto
     - ``5``
   * - ``rag.chat.context.max.chars``
     - Numero maximo de caracteres del contexto
     - ``4000``
   * - ``rag.chat.content.fields``
     - Campos a obtener de los documentos
     - ``title,url,content,...``
   * - ``rag.chat.evaluation.max.relevant.docs``
     - Numero maximo de documentos relevantes a seleccionar en la fase de evaluacion
     - ``3``

Campos de contenido
-------------------

Campos que pueden especificarse en ``rag.chat.content.fields``:

- ``title`` - Titulo del documento
- ``url`` - URL del documento
- ``content`` - Cuerpo del documento
- ``doc_id`` - ID del documento
- ``content_title`` - Titulo del contenido
- ``content_description`` - Descripcion del contenido

Prompt del sistema
==================

El prompt del sistema define el comportamiento basico del LLM.

Configuracion predeterminada
----------------------------

::

    rag.chat.system.prompt=You are an AI assistant for Fess search engine. Answer questions based on the search results provided. Always cite your sources using [1], [2], etc.

Ejemplos de personalizacion
---------------------------

Para priorizar respuestas en espanol:

::

    rag.chat.system.prompt=Eres un asistente de IA para el motor de busqueda Fess. Responde las preguntas basandote en los resultados de busqueda proporcionados. Responde en espanol y siempre cita las fuentes usando [1], [2], etc.

Personalizacion para campo especializado:

::

    rag.chat.system.prompt=You are a technical documentation assistant. Provide detailed and accurate answers based on the search results. Include code examples when relevant. Always cite your sources using [1], [2], etc.

Gestion de sesiones
===================

Configuracion relacionada con la gestion de sesiones de chat.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.chat.session.timeout.minutes``
     - Tiempo de timeout de sesion (minutos)
     - ``30``
   * - ``rag.chat.session.max.size``
     - Numero maximo de sesiones simultaneas
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - Numero maximo de mensajes a mantener en el historial de conversacion
     - ``20``

Comportamiento de sesiones
--------------------------

- Cuando un usuario inicia un nuevo chat, se crea una nueva sesion
- El historial de conversacion se guarda en la sesion, permitiendo dialogo con contexto mantenido
- Las sesiones se eliminan automaticamente despues del tiempo de timeout
- Cuando el historial de conversacion excede el numero maximo de mensajes, los mensajes antiguos se eliminan

Limite de tasa
==============

Configuracion de limite de tasa para prevenir sobrecarga de la API.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.chat.rate.limit.enabled``
     - Habilitar limite de tasa
     - ``true``
   * - ``rag.chat.rate.limit.requests.per.minute``
     - Numero maximo de solicitudes por minuto
     - ``10``

Consideraciones del limite de tasa
----------------------------------

- Considere tambien los limites de tasa del proveedor LLM al configurar
- En entornos de alta carga, se recomiendan limites mas estrictos
- Cuando se alcanza el limite de tasa, se muestra un mensaje de error al usuario

Uso de la API
=============

La funcionalidad de chat RAG esta disponible a traves de la API REST.

API sin streaming
-----------------

Endpoint: ``POST /api/v1/chat``

Parametros:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parametro
     - Requerido
     - Descripcion
   * - ``message``
     - Si
     - Mensaje del usuario
   * - ``sessionId``
     - No
     - ID de sesion (para continuar la conversacion)
   * - ``clear``
     - No
     - ``true`` para limpiar la sesion

Ejemplo de solicitud:

::

    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=Por favor explicame como instalar Fess"

Ejemplo de respuesta:

::

    {
      "status": "ok",
      "sessionId": "abc123",
      "content": "El metodo de instalacion de Fess es...",
      "sources": [
        {"title": "Guia de instalacion", "url": "https://..."}
      ]
    }

API con streaming
-----------------

Endpoint: ``POST /api/v1/chat/stream``

Transmite respuestas en formato Server-Sent Events (SSE).

Parametros:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parametro
     - Requerido
     - Descripcion
   * - ``message``
     - Si
     - Mensaje del usuario
   * - ``sessionId``
     - No
     - ID de sesion (para continuar la conversacion)

Ejemplo de solicitud:

::

    curl -X POST "http://localhost:8080/api/v1/chat/stream" \
         -d "message=Por favor explicame las caracteristicas de Fess" \
         -H "Accept: text/event-stream"

Eventos SSE:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Evento
     - Descripcion
   * - ``session``
     - Informacion de sesion (sessionId)
   * - ``phase``
     - Inicio/fin de fase de procesamiento (intent_analysis, search, evaluation, generation)
   * - ``chunk``
     - Fragmento de texto generado
   * - ``sources``
     - Informacion de documentos de referencia
   * - ``done``
     - Procesamiento completado (sessionId, htmlContent)
   * - ``error``
     - Informacion de error

Para documentacion detallada de la API, consulte :doc:`../api/api-chat`.

Interfaz web
============

En la interfaz web de |Fess|, puede usar la funcionalidad de chat RAG desde la pantalla de busqueda.

Iniciar chat
------------

1. Acceda a la pantalla de busqueda de |Fess|
2. Haga clic en el icono de chat
3. Se mostrara el panel de chat

Usar chat
---------

1. Ingrese una pregunta en el cuadro de texto
2. Haga clic en el boton de enviar o presione la tecla Enter
3. Se mostrara la respuesta del asistente de IA
4. La respuesta incluye enlaces a las fuentes de referencia

Continuar conversacion
----------------------

- Puede continuar la conversacion dentro de la misma sesion de chat
- Las respuestas consideran el contexto de las preguntas anteriores
- Hacer clic en "Nuevo chat" reinicia la sesion

Solucion de problemas
=====================

El chat RAG no se habilita
--------------------------

**Verificaciones**:

1. Si ``rag.chat.enabled=true`` esta configurado
2. Si el proveedor LLM esta configurado correctamente
3. Si la conexion al proveedor LLM es posible

Baja calidad de respuestas
--------------------------

**Mejoras**:

1. Usar un modelo LLM de mayor rendimiento
2. Aumentar ``rag.chat.context.max.documents``
3. Personalizar el prompt del sistema
4. Ajustar ``rag.chat.temperature``

Respuestas lentas
-----------------

**Mejoras**:

1. Usar un modelo LLM mas rapido (ej: Gemini Flash)
2. Reducir ``rag.chat.max.tokens``
3. Reducir ``rag.chat.context.max.chars``

Sesiones no se mantienen
------------------------

**Verificaciones**:

1. Si el sessionId se esta enviando correctamente del lado del cliente
2. Configuracion de ``rag.chat.session.timeout.minutes``
3. Capacidad del almacenamiento de sesiones

Configuracion de depuracion
---------------------------

Para investigar problemas, puede ajustar el nivel de log para obtener logs detallados.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm" level="DEBUG"/>
    <Logger name="org.codelibs.fess.api.chat" level="DEBUG"/>
    <Logger name="org.codelibs.fess.chat" level="DEBUG"/>

Informacion de referencia
=========================

- :doc:`llm-overview` - Descripcion general de integracion LLM
- :doc:`llm-ollama` - Configuracion de Ollama
- :doc:`llm-openai` - Configuracion de OpenAI
- :doc:`llm-gemini` - Configuracion de Google Gemini
- :doc:`../api/api-chat` - Referencia de Chat API
- :doc:`../user/chat-search` - Guia de busqueda con chat para usuarios finales
