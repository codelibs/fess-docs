==========================
Configuracion de la funcionalidad de modo de búsqueda IA
==========================

Descripcion general
===================

El modo de búsqueda IA (RAG: Retrieval-Augmented Generation) es una funcionalidad que extiende los resultados de busqueda de |Fess| con LLM (Modelo de Lenguaje Grande),
proporcionando informacion en formato de dialogo. Los usuarios pueden hacer preguntas en lenguaje natural
y obtener respuestas detalladas basadas en los resultados de busqueda.

En |Fess| 15.7, la funcionalidad LLM ha sido separada como plugins ``fess-llm-*``.
La configuracion del nucleo y la configuracion especifica del proveedor LLM se realizan en ``fess_config.properties``,
y la seleccion del proveedor LLM (``rag.llm.name``) se realiza desde ``system.properties`` o la pantalla de administracion.

Como funciona el modo de búsqueda IA
========================

El modo de búsqueda IA opera con el siguiente flujo de multiples etapas.

1. **Fase de analisis de intencion**: Analiza la pregunta del usuario y extrae las palabras clave mas adecuadas para la busqueda
2. **Fase de busqueda**: Busca documentos usando el motor de busqueda de |Fess| con las palabras clave extraidas
3. **Fallback de regeneracion de consulta**: Cuando no se encuentran resultados, el LLM regenera la consulta y reintenta
4. **Fase de evaluacion**: Evalua la relevancia de los resultados de busqueda y selecciona los documentos mas apropiados
5. **Fase de generacion**: El LLM genera una respuesta basada en los documentos seleccionados
6. **Fase de salida**: Devuelve la respuesta y la informacion de fuentes al usuario (con renderizado Markdown)

Este flujo permite respuestas de alta calidad con comprension del contexto, superiores a la simple busqueda por palabras clave.
La regeneracion de consultas mejora la cobertura de respuestas cuando la consulta de busqueda inicial no es optima.

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

Referencia rapida de rutas de configuracion
===========================================

En |Fess| 15.7 los parametros estan divididos en dos familias: la familia FessConfig
(``fess_config.properties``) y la familia SystemProperty (``system.properties``,
persistida en OpenSearch). Las rutas de configuracion difieren; no las mezcle.

.. list-table::
   :header-rows: 1
   :widths: 35 18 32 15

   * - Propiedad
     - Familia
     - Paso via Docker / opciones JVM
     - UI Admin
   * - ``rag.chat.enabled``
     - FessConfig
     - ``-Dfess.config.rag.chat.enabled=true``
     - No
   * - ``rag.llm.name``
     - SystemProperty
     - ``-Dfess.system.rag.llm.name=gemini`` (solo como valor inicial por defecto)
     - Si (Configuracion general)
   * - ``rag.llm.gemini.api.key``
     - FessConfig
     - ``-Dfess.config.rag.llm.gemini.api.key=...``
     - Si
   * - ``rag.llm.gemini.model``
     - FessConfig
     - ``-Dfess.config.rag.llm.gemini.model=...``
     - Si
   * - ``rag.llm.openai.api.key``
     - FessConfig
     - ``-Dfess.config.rag.llm.openai.api.key=...``
     - Si
   * - ``rag.llm.openai.model``
     - FessConfig
     - ``-Dfess.config.rag.llm.openai.model=...``
     - Si
   * - ``rag.llm.ollama.api.url``
     - FessConfig
     - ``-Dfess.config.rag.llm.ollama.api.url=...``
     - Si

.. note::

   ``rag.llm.type`` es el nombre de propiedad heredado de |Fess| 15.5 y anteriores.
   En 15.7 y posteriores se renombro a ``rag.llm.name``; los valores escritos bajo
   ``rag.llm.type`` no se leen.

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
     - ``30``
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
     - Tipo de contenido a incluir en el historial del asistente ( ``full`` / ``smart_summary`` / ``source_titles`` / ``source_titles_and_urls`` / ``truncated`` / ``none`` )
     - ``smart_summary``

Parametros de generacion
========================

En |Fess| 15.7, los parametros de generacion (numero maximo de tokens, temperature, etc.) se configuran por proveedor
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

En |Fess| 15.7, los prompts del sistema estan definidos en el DI XML (``fess_llm++.xml``) de cada plugin ``fess-llm-*``,
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
     - ``30``

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

Modo de historial de conversacion
==================================

``rag.chat.history.assistant.content`` controla como se almacenan las respuestas del asistente en el historial de conversacion.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Modo
     - Descripcion
   * - ``smart_summary``
     - (Predeterminado) Preserva el inicio (60%) y el final (40%) de la respuesta, reemplazando el medio con un marcador de omision. Los titulos de las fuentes tambien se adjuntan
   * - ``full``
     - Preserva la respuesta completa tal cual
   * - ``source_titles``
     - Preserva solo los titulos de las fuentes
   * - ``source_titles_and_urls``
     - Preserva los titulos y URLs de las fuentes
   * - ``truncated``
     - Trunca la respuesta al limite maximo de caracteres
   * - ``none``
     - No preserva el historial

.. note::

   En el modo ``smart_summary``, el contexto de respuestas largas se preserva eficientemente mientras se reduce el uso de tokens.
   Los pares de mensajes de usuario y asistente se agrupan como turnos y se empaquetan optimamente dentro de un presupuesto de caracteres.
   Los limites maximos de caracteres para el historial y el resumen son controlados por la implementacion ``LlmClient`` de cada plugin ``fess-llm-*``.

Regeneracion de consulta
========================

Cuando no se encuentran resultados de busqueda o no se identifican resultados relevantes, el LLM regenera automaticamente la consulta y reintenta la busqueda.

- Con cero resultados de busqueda: Regeneracion de consulta con razon ``no_results``
- Cuando no se encuentran documentos relevantes: Regeneracion de consulta con razon ``no_relevant_results``
- Recurre a la consulta original si la regeneracion falla

Esta funcionalidad esta habilitada por defecto e integrada en los flujos RAG sincronos y de streaming.
Los prompts de regeneracion de consulta se definen en cada plugin ``fess-llm-*``.

Renderizado Markdown
====================

Las respuestas del modo de busqueda IA se renderizan en formato Markdown.

- Las respuestas del LLM se analizan como Markdown y se convierten a HTML
- El HTML convertido se sanitiza, permitiendo solo etiquetas y atributos seguros
- Soporta encabezados, listas, bloques de codigo, tablas, enlaces y otras sintaxis Markdown
- Del lado del cliente se usa ``marked.js`` y ``DOMPurify``; del lado del servidor se usa el sanitizador OWASP

Uso de la API
=============

La funcionalidad de modo de búsqueda IA esta disponible a traves de la API REST.

API sin streaming
-----------------

Endpoint: ``POST /api/v1/chat``

Parametros:

.. list-table::
   :header-rows: 1
   :widths: 20 15.75

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
   :widths: 20 15.75

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
   * - ``phase``
     - Inicio/fin de fase de procesamiento (intent_analysis, search, evaluation, generation)
   * - ``chunk``
     - Fragmento de texto generado
   * - ``sources``
     - Informacion de documentos de referencia
   * - ``done``
     - Procesamiento completado (sessionId, htmlContent). htmlContent contiene el string HTML renderizado desde Markdown
   * - ``error``
     - Informacion de error. Proporciona mensajes especificos para timeout, longitud de contexto excedida, modelo no encontrado, respuesta invalida y errores de conexion

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

El boton del modo IA no aparece en la pantalla de busqueda
----------------------------------------------------------

**Sintoma**: El boton del modo IA no aparece en el encabezado de los resultados
de busqueda y al acceder a ``/chat`` se redirige a la pagina principal.

**Lista de verificacion**: revise los siguientes puntos en orden.

1. ¿Esta ``rag.chat.enabled=true`` configurado?

   - Docker: ¿``-Dfess.config.rag.chat.enabled=true`` esta incluido en ``FESS_JAVA_OPTS``?
   - Instalacion por paquete: ¿esta escrito en ``app/WEB-INF/conf/fess_config.properties``?

2. ¿Esta instalado el plugin ``fess-llm-*`` correspondiente?

   - Docker: ``FESS_PLUGINS=fess-llm-gemini:15.7.0`` (o ``fess-llm-openai`` / ``fess-llm-ollama``) debe estar definido
   - Instalacion por paquete: el JAR debe estar en ``app/WEB-INF/plugin/``
   - El log de inicio debe incluir ``Installing fess-llm-XXX-15.7.0.jar``

3. ¿Coincide ``rag.llm.name`` con un plugin instalado?

   - El valor por defecto es ``ollama``. Si solo el plugin Gemini esta instalado, debe definir explicitamente ``gemini`` (igualmente ``openai`` para el plugin OpenAI)
   - Metodo (a): editar ``rag.llm.name`` desde Administracion > Sistema > General (seccion RAG) y guardar
   - Metodo (b): incluir ``-Dfess.system.rag.llm.name=gemini`` en ``FESS_JAVA_OPTS`` al inicio. Solo actua como valor inicial por defecto antes de que se persista un valor en OpenSearch

4. ¿Aparece repetidamente un WARN como ``[LLM] LlmClient not found. componentName=ollamaLlmClient`` en el log?

   - Sintoma tipico cuando ``rag.llm.name`` sigue siendo ``ollama`` pero el plugin Ollama no esta instalado
   - Definir ``rag.llm.name`` al proveedor realmente usado lo resuelve
   - De forma similar, ``componentName=geminiLlmClient`` indica que ``rag.llm.name=gemini`` esta definido pero el plugin ``fess-llm-gemini`` no esta instalado

5. ¿Esta configurada la clave de API especifica del proveedor?

   - Si ``rag.llm.gemini.api.key`` / ``rag.llm.openai.api.key`` esta vacia, ``checkAvailabilityNow`` devuelve ``false`` y el modo IA queda desactivado
   - Activar DEBUG en ``org.codelibs.fess.llm.gemini`` en ``log4j2.xml`` muestra mensajes como ``[LLM:GEMINI] Gemini is not available. apiKey is blank``

6. ¿Puede el host de Fess alcanzar al proveedor LLM?

   - Para APIs cloud (Gemini / OpenAI), el contenedor debe tener acceso saliente a Internet
   - Si se requiere un proxy, agregue ``-Dhttps.proxyHost=... -Dhttps.proxyPort=...`` a ``FESS_JAVA_OPTS``

.. note::

   La pagina "General" no expone una casilla para ``rag.chat.enabled`` (por diseño).
   Es una propiedad de la familia FessConfig y solo puede definirse a traves de
   ``fess_config.properties`` o ``-Dfess.config.rag.chat.enabled=true``.

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

Los mensajes de log usan el prefijo ``[RAG]``, con subprefijos como ``[RAG:INTENT]``, ``[RAG:EVAL]`` y ``[RAG:ANSWER]`` para cada fase.
A nivel INFO, se emiten logs de finalizacion de chat (tiempo transcurrido, cantidad de fuentes). A nivel DEBUG, se emiten detalles de uso de tokens, control de concurrencia y empaquetado del historial.

Registro de busqueda y tipo de acceso
--------------------------------------

Las busquedas a traves del modo de busqueda IA se registran con el nombre del proveedor LLM (por ejemplo, ``ollama``, ``openai``, ``gemini``) como tipo de acceso en los registros de busqueda. Esto permite distinguir las busquedas del modo IA de las busquedas web o API regulares en los analisis.

Informacion de referencia
=========================

- :doc:`llm-overview` - Descripcion general de integracion LLM
- :doc:`llm-ollama` - Configuracion de Ollama
- :doc:`llm-openai` - Configuracion de OpenAI
- :doc:`llm-gemini` - Configuracion de Google Gemini
- :doc:`../api/api-chat` - Referencia de Chat API
- :doc:`../user/chat-search` - Guia de busqueda con chat para usuarios finales
