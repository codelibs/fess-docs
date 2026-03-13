==========================
Configuracion de la funcionalidad de modo de búsqueda IA
==========================

Descripcion general
===================

El modo de búsqueda IA (RAG: Retrieval-Augmented Generation) es una funcionalidad que extiende los resultados de busqueda de |Fess| con LLM (Modelo de Lenguaje Grande),
proporcionando informacion en formato de dialogo. Los usuarios pueden hacer preguntas en lenguaje natural
y obtener respuestas detalladas basadas en los resultados de busqueda.

En |Fess| 15.6, la funcionalidad LLM ha sido separada como plugins ``fess-llm-*``.
La configuracion del nucleo y la configuracion especifica del proveedor LLM se realizan en ``fess_config.properties``,
y la seleccion del proveedor LLM (``rag.llm.name``) se realiza desde ``system.properties`` o la pantalla de administracion.

Como funciona el modo de búsqueda IA
========================

El modo de búsqueda IA opera con el siguiente flujo de multiples etapas.

1. **Fase de analisis de intencion**: Analiza la pregunta del usuario y extrae las palabras clave mas adecuadas para la busqueda
2. **Fase de busqueda**: Busca documentos usando el motor de busqueda de |Fess| con las palabras clave extraidas
3. **Fase de evaluacion**: Evalua la relevancia de los resultados de busqueda y selecciona los documentos mas apropiados
4. **Fase de generacion**: El LLM genera una respuesta basada en los documentos seleccionados
5. **Fase de salida**: Devuelve la respuesta y la informacion de fuentes al usuario

Este flujo permite respuestas de alta calidad con comprension del contexto, superiores a la simple busqueda por palabras clave.

Configuracion basica
====================

La configuracion de la funcionalidad de modo de búsqueda IA se divide en configuracion del nucleo y configuracion del proveedor.

Configuracion del nucleo (fess_config.properties)
--------------------------------------------------

Configuracion basica para habilitar la funcionalidad de modo de búsqueda IA.
Se configura en ``app/WEB-INF/conf/fess_config.properties``.

::

    # Habilitar la funcionalidad de modo de búsqueda IA
    rag.chat.enabled=true

Configuracion del proveedor (system.properties / pantalla de administracion)
-----------------------------------------------------------------------------

La seleccion del proveedor LLM se realiza en la pantalla de administracion o en las propiedades del sistema.

**Al configurar desde la pantalla de administracion**:

Seleccione el proveedor LLM a usar en la pantalla de configuracion de Administracion > Sistema > General.

**Al configurar en system.properties**:

::

    # Seleccionar el proveedor LLM (ollama, openai, gemini)
    rag.llm.name=ollama

Para la configuracion detallada del proveedor LLM, consulte lo siguiente:

- :doc:`llm-ollama` - Configuracion de Ollama
- :doc:`llm-openai` - Configuracion de OpenAI
- :doc:`llm-gemini` - Configuracion de Google Gemini

Lista de configuracion del nucleo
==================================

Lista de configuraciones del nucleo que se pueden configurar en ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.chat.enabled``
     - Habilitar la funcionalidad de modo de búsqueda IA
     - ``false``
   * - ``rag.chat.context.max.documents``
     - Numero maximo de documentos a incluir en el contexto
     - ``5``
   * - ``rag.chat.session.timeout.minutes``
     - Tiempo de timeout de sesion (minutos)
     - ``30``
   * - ``rag.chat.session.max.size``
     - Numero maximo de sesiones que se pueden mantener simultaneamente
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - Numero maximo de mensajes a mantener en el historial de conversacion
     - ``20``
   * - ``rag.chat.intent.history.max.messages``
     - Numero maximo de mensajes del historial de conversacion usados para el analisis de intencion
     - ``4``
   * - ``rag.chat.content.fields``
     - Campos a obtener de los documentos
     - ``title,url,content,doc_id,content_title,content_description``
   * - ``rag.chat.message.max.length``
     - Numero maximo de caracteres del mensaje del usuario
     - ``4000``
   * - ``rag.chat.highlight.fragment.size``
     - Tamano del fragmento de resaltado
     - ``500``
   * - ``rag.chat.highlight.number.of.fragments``
     - Numero de fragmentos de resaltado
     - ``3``
   * - ``rag.chat.history.assistant.content``
     - Tipo de contenido a incluir en el historial del asistente
     - ``source_titles``
   * - ``rag.chat.history.assistant.max.chars``
     - Numero maximo de caracteres del historial del asistente
     - ``500``
   * - ``rag.chat.history.assistant.summary.max.chars``
     - Numero maximo de caracteres del resumen del historial del asistente
     - ``500``
   * - ``rag.chat.history.max.chars``
     - Numero maximo de caracteres del historial de conversacion
     - ``2000``

Parametros de generacion
========================

En |Fess| 15.6, los parametros de generacion (numero maximo de tokens, temperature, etc.) se configuran por proveedor
y por tipo de prompt. Estas configuraciones se gestionan como configuracion de cada plugin ``fess-llm-*``,
no como configuracion del nucleo.

Para los detalles, consulte la documentacion de cada proveedor:

- :doc:`llm-ollama` - Configuracion de parametros de generacion de Ollama
- :doc:`llm-openai` - Configuracion de parametros de generacion de OpenAI
- :doc:`llm-gemini` - Configuracion de parametros de generacion de Google Gemini

Configuracion de contexto
==========================

Configuracion del contexto pasado al LLM desde los resultados de busqueda.

Configuracion del nucleo
------------------------

Las siguientes configuraciones se realizan en ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rag.chat.context.max.documents``
     - Numero maximo de documentos a incluir en el contexto
     - ``5``
   * - ``rag.chat.content.fields``
     - Campos a obtener de los documentos
     - ``title,url,content,doc_id,content_title,content_description``

Configuracion especifica del proveedor
---------------------------------------

Las siguientes configuraciones se realizan en ``fess_config.properties`` por proveedor.

- ``rag.llm.{provider}.{promptType}.context.max.chars`` - Numero maximo de caracteres del contexto
- ``rag.llm.{provider}.chat.evaluation.max.relevant.docs`` - Numero maximo de documentos relevantes a seleccionar en la fase de evaluacion

En ``{provider}`` va el nombre del proveedor como ``ollama``, ``openai``, ``gemini``, etc.
En ``{promptType}`` va el tipo de prompt como ``chat``, ``intent_analysis``, ``evaluation``, etc.

Para los detalles, consulte la documentacion de cada proveedor.

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

En |Fess| 15.6, los prompts del sistema estan definidos en el DI XML (``fess_llm++.xml``) de cada plugin ``fess-llm-*``,
no en archivos de propiedades.

Personalizacion de prompts
--------------------------

Para personalizar los prompts del sistema, anule el ``fess_llm++.xml`` dentro del JAR del plugin.

1. Obtenga ``fess_llm++.xml`` del archivo JAR del plugin en uso
2. Realice los cambios necesarios
3. Coloquelo en el lugar apropiado bajo ``app/WEB-INF/`` para anularlo

Para cada tipo de prompt (analisis de intencion, evaluacion, generacion), estan definidos diferentes
prompts del sistema, optimizados segun el uso.

Para los detalles, consulte la documentacion de cada proveedor:

- :doc:`llm-ollama` - Configuracion de prompts de Ollama
- :doc:`llm-openai` - Configuracion de prompts de OpenAI
- :doc:`llm-gemini` - Configuracion de prompts de Google Gemini

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
     - Numero maximo de sesiones que se pueden mantener simultaneamente
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

Control de concurrencia
=======================

El numero de solicitudes simultaneas al LLM se controla por proveedor en ``fess_config.properties``.

::

    # Numero maximo de solicitudes simultaneas por proveedor
    rag.llm.ollama.max.concurrent.requests=5
    rag.llm.openai.max.concurrent.requests=10
    rag.llm.gemini.max.concurrent.requests=10

Consideraciones del control de concurrencia
--------------------------------------------

- Configure tambien teniendo en cuenta los limites de tasa del lado del proveedor LLM
- En entornos de alta carga, se recomienda configurar valores mas pequenos
- Cuando se alcanza el limite del numero de solicitudes simultaneas, las solicitudes entran en cola y se procesan en orden

Uso de la API
=============

La funcionalidad de modo de búsqueda IA esta disponible a traves de la API REST.

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

En la interfaz web de |Fess|, puede usar la funcionalidad de modo de búsqueda IA desde la pantalla de busqueda.

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

El modo de búsqueda IA no se habilita
--------------------------

**Verificaciones**:

1. Si ``rag.chat.enabled=true`` esta configurado
2. Si el proveedor LLM esta configurado correctamente en ``rag.llm.name``
3. Si el plugin ``fess-llm-*`` correspondiente esta instalado
4. Si es posible la conexion al proveedor LLM

Baja calidad de respuestas
--------------------------

**Mejoras**:

1. Usar un modelo LLM de mayor rendimiento
2. Aumentar ``rag.chat.context.max.documents``
3. Personalizar los prompts del sistema en el DI XML
4. Ajustar la configuracion de temperature especifica del proveedor (consulte la documentacion de cada plugin ``fess-llm-*``)

Respuestas lentas
-----------------

**Mejoras**:

1. Usar un modelo LLM mas rapido (ej: Gemini Flash)
2. Reducir la configuracion de max.tokens especifica del proveedor (consulte la documentacion de cada plugin ``fess-llm-*``)
3. Reducir ``rag.chat.context.max.documents``

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
