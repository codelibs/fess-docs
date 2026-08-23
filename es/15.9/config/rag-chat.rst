==========================
Configuración de la funcionalidad de modo de búsqueda IA
==========================

Descripción general
===================

El modo de búsqueda IA (RAG: Retrieval-Augmented Generation) es una funcionalidad que extiende los resultados de búsqueda de |Fess| con LLM (Modelo de Lenguaje Grande),
proporcionando información en formato de diálogo. Los usuarios pueden hacer preguntas en lenguaje natural
y obtener respuestas detalladas basadas en los resultados de búsqueda.

En |Fess| 15.9, la funcionalidad LLM ha sido separada como plugins ``fess-llm-*``.
La configuración del núcleo y la configuración específica del proveedor LLM se realizan en ``fess_config.properties``,
y la selección del proveedor LLM (``rag.llm.name``) se realiza desde ``system.properties`` o la pantalla de administración.

Pipeline de recuperación
========================

El modo de búsqueda IA obtiene sus documentos de origen a través del pipeline estándar de búsqueda de |Fess| (rank fusión), con el control de acceso basado en roles y etiquetas habitual de |Fess|. Por defecto se usa búsqueda por palabras clave (BM25); el LLM no realiza por sí mismo la búsqueda, el ranking ni el embedding de los documentos.

Los dos tipos de solicitud ejecutan pipelines ligeramente distintos:

- ``POST /api/v2/chat/stream`` (usado por la interfaz web) ejecuta el flujo completo: **análisis de intención → búsqueda → evaluación de relevancia por el LLM → obtención de contenido → generación de la respuesta** (en streaming).
- ``POST /api/v2/chat`` (sin streaming) ejecuta un flujo más corto: **análisis de intención → búsqueda → generación de la respuesta** (sin fase de evaluación de relevancia ni una fase independiente de obtención de contenido).

En el flujo de streaming, una llamada adicional al LLM **evalúa los resultados de búsqueda** y conserva únicamente los documentos que considera relevantes antes de generar la respuesta.

Cómo funciona el modo de búsqueda IA
========================

El modo de búsqueda IA opera con el siguiente flujo de múltiples etapas.

1. **Fase de análisis de intención**: Analiza la pregunta del usuario y extrae las palabras clave más adecuadas para la búsqueda
2. **Fase de búsqueda**: Busca documentos usando el motor de búsqueda de |Fess| con las palabras clave extraídas
3. **Fallback de regeneración de consulta**: Cuando no se encuentran resultados, el LLM regenera la consulta y reintenta
4. **Fase de evaluación**: Evalúa la relevancia de los resultados de búsqueda y selecciona los documentos más apropiados
5. **Fase de generación**: El LLM genera una respuesta basada en los documentos seleccionados
6. **Fase de salida**: Devuelve la respuesta y la información de fuentes al usuario (con renderizado Markdown)

Este flujo permite respuestas de alta calidad con comprensión del contexto, superiores a la simple búsqueda por palabras clave.
La regeneración de consultas mejora la cobertura de respuestas cuando la consulta de búsqueda inicial no es óptima.

Configuración básica
====================

La configuración de la funcionalidad de modo de búsqueda IA se divide en configuración del núcleo y configuración del proveedor.

Configuración del núcleo (fess_config.properties)
--------------------------------------------------

Configuración básica para habilitar la funcionalidad de modo de búsqueda IA.
Se configura en ``app/WEB-INF/conf/fess_config.properties``.

::

    # Habilitar la funcionalidad de modo de búsqueda IA
    rag.chat.enabled=true

Configuración del proveedor (system.properties / pantalla de administración)
-----------------------------------------------------------------------------

La selección del proveedor LLM se realiza en la pantalla de administración o en las propiedades del sistema.

**Al configurar desde la pantalla de administración**:

Seleccione el proveedor LLM a usar en la pantalla de configuración de Administración > Sistema > General.

**Al configurar en system.properties**:

::

    # Seleccionar el proveedor LLM (ollama, openai, gemini)
    rag.llm.name=ollama

Para la configuración detallada del proveedor LLM, consulte lo siguiente:

- :doc:`llm-ollama` - Configuración de Ollama
- :doc:`llm-openai` - Configuración de OpenAI
- :doc:`llm-gemini` - Configuración de Google Gemini

Referencia rápida de rutas de configuración
===========================================

En |Fess| 15.9 los parámetros están divididos en dos familias: la familia FessConfig
(``fess_config.properties``) y la familia SystemProperty (``system.properties``,
persistida en OpenSearch). Las rutas de configuración difieren; no las mezcle.

.. list-table::
   :header-rows: 1
   :widths: 35 18 32 15

   * - Propiedad
     - Familia
     - Paso vía Docker / opciones JVM
     - UI Admin
   * - ``rag.chat.enabled``
     - FessConfig
     - ``-Dfess.config.rag.chat.enabled=true``
     - No
   * - ``rag.llm.name``
     - SystemProperty
     - ``-Dfess.system.rag.llm.name=gemini`` (solo como valor inicial por defecto)
     - Si (Configuración general)
   * - ``rag.llm.gemini.api.key``
     - FessConfig
     - ``-Dfess.config.rag.llm.gemini.api.key=...``
     - No
   * - ``rag.llm.gemini.model``
     - FessConfig
     - ``-Dfess.config.rag.llm.gemini.model=...``
     - No
   * - ``rag.llm.openai.api.key``
     - FessConfig
     - ``-Dfess.config.rag.llm.openai.api.key=...``
     - No
   * - ``rag.llm.openai.model``
     - FessConfig
     - ``-Dfess.config.rag.llm.openai.model=...``
     - No
   * - ``rag.llm.ollama.api.url``
     - FessConfig
     - ``-Dfess.config.rag.llm.ollama.api.url=...``
     - No

.. note::

   ``rag.llm.type`` es el nombre de propiedad heredado de |Fess| 15.5 y anteriores.
   En 15.9 y posteriores se renombró a ``rag.llm.name``; los valores escritos bajo
   ``rag.llm.type`` no se leen.

Lista de configuración del núcleo
==================================

Lista de configuraciones del núcleo que se pueden configurar en ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``rag.chat.enabled``
     - Habilitar la funcionalidad de modo de búsqueda IA
     - ``false``
   * - ``rag.chat.context.max.documents``
     - Número máximo de documentos a incluir en el contexto
     - ``5``
   * - ``rag.chat.session.timeout.minutes``
     - Tiempo de timeout de sesión (minutos)
     - ``30``
   * - ``rag.chat.session.max.size``
     - Número máximo de sesiones que se pueden mantener simultáneamente
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - Número máximo de mensajes a mantener en el historial de conversación
     - ``30``
   * - ``rag.chat.content.fields``
     - Campos a obtener de los documentos
     - ``title,url,content,doc_id,content_title,content_description``
   * - ``rag.chat.message.max.length``
     - Número máximo de caracteres del mensaje del usuario. Este valor se lee como System Property; el elemento en ``fess_config.properties`` no se utiliza. Configúrelo mediante System Properties o ``-Dfess.system.rag.chat.message.max.length``.
     - ``4000``
   * - ``rag.chat.highlight.fragment.size``
     - Tamaño del fragmento de resaltado de búsqueda
     - ``500``
   * - ``rag.chat.highlight.number.of.fragments``
     - Número de fragmentos de resaltado de búsqueda
     - ``3``
   * - ``rag.chat.content.fulltext.max.length``
     - Umbral por encima del cual los documentos (según ``content_length``) usan pasajes resaltados en lugar del texto completo en el contexto de la respuesta
     - ``3000``
   * - ``rag.chat.answer.highlight.fragment.size``
     - Tamaño del fragmento de resaltado al extraer pasajes de documentos grandes para el contexto de la respuesta
     - ``1000``
   * - ``rag.chat.answer.highlight.number.of.fragments``
     - Número de fragmentos de resaltado al extraer pasajes de documentos grandes para el contexto de la respuesta
     - ``5``
   * - ``rag.chat.history.assistant.content``
     - Tipo de contenido a incluir en el historial del asistente ( ``full`` / ``smart_summary`` / ``source_titles`` / ``source_titles_and_urls`` / ``truncated`` / ``none`` )
     - ``smart_summary``
   * - ``rag.chat.history.titles.max.count``
     - Número máximo de títulos de documentos referenciados que se conservan por turno en el modo ``smart_summary``
     - ``5``

Parámetros de generación
========================

En |Fess| 15.9, los parámetros de generación (número máximo de tokens, temperature, etc.) se configuran por proveedor
y por tipo de prompt. Estas configuraciones se gestionan como configuración de cada plugin ``fess-llm-*``,
no como configuración del núcleo.

Para los detalles, consulte la documentación de cada proveedor:

- :doc:`llm-ollama` - Configuración de parámetros de generación de Ollama
- :doc:`llm-openai` - Configuración de parámetros de generación de OpenAI
- :doc:`llm-gemini` - Configuración de parámetros de generación de Google Gemini

Configuración de contexto
==========================

Configuración del contexto pasado al LLM desde los resultados de búsqueda.

Configuración del núcleo
------------------------

Las siguientes configuraciones se realizan en ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``rag.chat.context.max.documents``
     - Número máximo de documentos a incluir en el contexto
     - ``5``
   * - ``rag.chat.content.fields``
     - Campos a obtener de los documentos
     - ``title,url,content,doc_id,content_title,content_description``

Configuración específica del proveedor
---------------------------------------

Las siguientes configuraciones se realizan en ``fess_config.properties`` por proveedor.

- ``rag.llm.{provider}.{promptType}.context.max.chars`` - Número máximo de caracteres del contexto
- ``rag.llm.{provider}.chat.evaluation.max.relevant.docs`` - Número máximo de documentos relevantes a seleccionar en la fase de evaluación

En ``{provider}`` va el nombre del proveedor como ``ollama``, ``openai``, ``gemini``, etc.
En ``{promptType}`` va el tipo de prompt como ``intent``, ``evaluation``, ``answer``, ``summary``, ``faq``, ``queryregeneration``, ``unclear``, ``noresults``, ``docnotfound``, ``direct``, etc.
Los tipos de prompt soportados están definidos en la implementación ``*LlmClient`` de cada plugin.

Para los detalles, consulte la documentación de cada proveedor.

Campos de contenido
-------------------

Campos que pueden especificarse en ``rag.chat.content.fields``:

- ``title`` - Título del documento
- ``url`` - URL del documento
- ``content`` - Cuerpo del documento
- ``doc_id`` - ID del documento
- ``content_title`` - Título del contenido
- ``content_description`` - Descripción del contenido

Prompt del sistema
==================

En |Fess| 15.9, los prompts del sistema están definidos en el DI XML (``fess_llm++.xml``) de cada plugin ``fess-llm-*``,
no en archivos de propiedades.

Personalización de prompts
--------------------------

Para personalizar los prompts del sistema, anule el ``fess_llm++.xml`` dentro del JAR del plugin.

1. Obtenga ``fess_llm++.xml`` del archivo JAR del plugin en uso
2. Realice los cambios necesarios
3. Colóquelo en el lugar apropiado bajo ``app/WEB-INF/`` para anularlo

Para cada tipo de prompt (análisis de intención, evaluación, generación), están definidos diferentes
prompts del sistema, optimizados según el uso.

Para los detalles, consulte la documentación de cada proveedor:

- :doc:`llm-ollama` - Configuración de prompts de Ollama
- :doc:`llm-openai` - Configuración de prompts de OpenAI
- :doc:`llm-gemini` - Configuración de prompts de Google Gemini

Gestión de sesiones
===================

Configuración relacionada con la gestión de sesiones de chat.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``rag.chat.session.timeout.minutes``
     - Tiempo de timeout de sesión (minutos)
     - ``30``
   * - ``rag.chat.session.max.size``
     - Número máximo de sesiones que se pueden mantener simultáneamente
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - Número máximo de mensajes a mantener en el historial de conversación
     - ``30``

Comportamiento de sesiones
--------------------------

- Cuando un usuario inicia un nuevo chat, se crea una nueva sesión
- El historial de conversación se guarda en la sesión, permitiendo diálogo con contexto mantenido
- Las sesiones se eliminan automáticamente después del tiempo de timeout
- Cuando el historial de conversación excede el número máximo de mensajes, los mensajes antiguos se eliminan

Control de concurrencia
=======================

El número de solicitudes simultáneas al LLM se controla por proveedor en ``fess_config.properties``.

::

    # Numero maximo de solicitudes simultaneas por proveedor (predeterminado: 5)
    rag.llm.ollama.max.concurrent.requests=5
    rag.llm.openai.max.concurrent.requests=5
    rag.llm.gemini.max.concurrent.requests=5

    # Timeout para adquirir un permiso de concurrencia (milisegundos, predeterminado: 30000)
    rag.llm.ollama.concurrency.wait.timeout=30000

Consideraciones del control de concurrencia
--------------------------------------------

- Configure también teniendo en cuenta los límites de tasa del lado del proveedor LLM
- En entornos de alta carga, se recomienda configurar valores más pequeños
- Cuando se alcanza el límite del número de solicitudes simultáneas, las solicitudes entran en cola y se procesan en orden
- Si la espera para adquirir un permiso supera ``concurrency.wait.timeout``, la solicitud falla con un error de timeout

Modo de historial de conversación
==================================

``rag.chat.history.assistant.content`` controla como se almacenan las respuestas del asistente en el historial de conversación.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Modo
     - Descripción
   * - ``smart_summary``
     - (Predeterminado) Omite el cuerpo de la respuesta del asistente y conserva, por turno, únicamente la consulta de búsqueda pasada y los títulos de los documentos referenciados (hasta ``rag.chat.history.titles.max.count`` elementos)
   * - ``full``
     - Preserva la respuesta completa tal cual
   * - ``source_titles``
     - Preserva solo los títulos de las fuentes
   * - ``source_titles_and_urls``
     - Preserva los títulos y URLs de las fuentes
   * - ``truncated``
     - Trunca la respuesta al límite máximo de caracteres
   * - ``none``
     - No preserva el historial

.. note::

   En el modo ``smart_summary``, el cuerpo de la respuesta se reemplaza por la consulta de búsqueda y los títulos referenciados, preservando el contexto de forma eficiente y reduciendo el uso de tokens.
   Los pares de mensajes de usuario y asistente se agrupan como turnos y se empaquetan óptimamente dentro de un presupuesto de caracteres.
   Los límites máximos de caracteres para el historial y el resumen, así como el control por plugin, son gestionados por la implementación ``LlmClient`` de cada plugin ``fess-llm-*``.

Regeneración de consulta
========================

Cuando no se encuentran resultados de búsqueda o no se identifican resultados relevantes, el LLM regenera automáticamente la consulta y reintenta la búsqueda.

- Con cero resultados de búsqueda: Regeneración de consulta con razón ``no_results``
- Cuando no se encuentran documentos relevantes: Regeneración de consulta con razón ``no_relevant_results``
- Recurre a la consulta original si la regeneración falla

Esta funcionalidad está habilitada por defecto e integrada en los flujos RAG síncronos y de streaming.
Los prompts de regeneración de consulta se definen en cada plugin ``fess-llm-*``.

Renderizado Markdown
====================

Las respuestas del modo de búsqueda IA se renderizan en formato Markdown.

- Las respuestas del LLM se analizan como Markdown y se convierten a HTML
- El HTML convertido se sanitiza, permitiendo solo etiquetas y atributos seguros
- Soporta encabezados, listas, bloques de código, tablas, enlaces y otras sintaxis Markdown
- Del lado del cliente se usa ``marked.js`` y ``DOMPurify``; del lado del servidor se usa el sanitizador OWASP

Uso de la API
=============

La funcionalidad de modo de búsqueda IA está disponible a través de la API REST (v2).
La URL base es ``http://<nombre del servidor>/api/v2/``.

La Chat API proporciona los siguientes tres endpoints:

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Endpoint
     - Descripción
   * - ``POST /api/v2/chat``
     - Completado RAG por lotes (sin streaming)
   * - ``POST /api/v2/chat/stream``
     - Streaming de completado RAG (Server-Sent Events)
   * - ``DELETE /api/v2/chat/sessions/{session_id}``
     - Borrar el historial de conversación de una sesión

Las solicitudes se envían con cuerpo JSON usando ``Content-Type: application/json``.
Las solicitudes que modifican el estado (``POST`` / ``DELETE``) requieren el token CSRF (cabecera ``X-Fess-CSRF-Token``).
Las respuestas se almacenan en el sobre común ``response``.

.. note::

   Los endpoints de parámetros de formulario de la familia ``/api/v1/chat`` disponibles en |Fess| 15.5 y anteriores han sido eliminados.
   En la versión 15.9, utilice la API basada en JSON de ``/api/v2/``.

API sin streaming
-----------------

Endpoint: ``POST /api/v2/chat``

Cuerpo de la solicitud (JSON):

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripción
   * - ``message``
     - Si
     - Mensaje del usuario
   * - ``session_id``
     - No
     - ID de sesión (para continuar la conversación). Si se omite, el servidor lo crea y lo devuelve en la respuesta
   * - ``fields``
     - No
     - Campos de filtro opcionales para el paso de recuperación (objeto)
   * - ``fields.label``
     - No
     - Filtro de búsqueda por etiqueta
   * - ``extra_queries``
     - No
     - Expresiones de consulta adicionales para filtros de faceta

Ejemplo de solicitud:

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -d '{"message":"Por favor explicame como instalar Fess"}'

Ejemplo de respuesta:

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session_id": "abc123",
        "content": "El método de instalación de Fess es...",
        "sources": [
          {
            "rank": 1,
            "title": "Guía de instalación",
            "url": "https://...",
            "doc_id": "...",
            "snippet": "..."
          }
        ]
      }
    }

API de streaming
----------------

Endpoint: ``POST /api/v2/chat/stream``

El cuerpo de la solicitud es el mismo que ``POST /api/v2/chat`` (JSON).
La respuesta se transmite en formato Server-Sent Events (SSE).

Ejemplo de solicitud:

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat/stream" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -H "Accept: text/event-stream" \
         --no-buffer \
         -d '{"message":"Por favor explicame las características de Fess"}'

Eventos SSE:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Evento
     - Descripción (payload)
   * - ``phase``
     - Inicio/fin de fase de procesamiento (``{ phase, status, message?, keywords?, hit_count?, ... }``). Fases: ``intent``, ``search``, ``evaluate``, ``fetch``, ``answer``
   * - ``chunk``
     - Fragmento de texto generado (``{ content }``)
   * - ``retry``
     - Notificado cuando se reintenta una solicitud al LLM (``{ phase, operation, attempt, max_attempts, sleep_ms, cause? }``)
   * - ``waiting``
     - Progreso de una fase de larga duración, como la espera para adquirir un permiso de concurrencia (``{ phase, reason, elapsed_ms, timeout_ms }``)
   * - ``fallback``
     - Notificado cuando la consulta se regenera por cero resultados u otras causas (``{ phase, reason, original_query?, new_query? }``, razón: ``no_results`` o ``no_relevant_results``)
   * - ``warning``
     - Notificado al producirse una advertencia recuperable (``{ phase, code, detail? }``, por ejemplo agotamiento de tokens en modelos de razonamiento)
   * - ``sources``
     - Información de documentos de referencia (``{ sources: [...] }``)
   * - ``done``
     - Procesamiento completado (``{ session_id, html_content? }``). ``html_content`` contiene el string HTML renderizado desde Markdown
   * - ``error``
     - Fallo terminal a mitad del stream (``{ phase?, message, error_code }``). Cubre timeout, longitud de contexto excedida, modelo no encontrado, respuesta inválida y errores de conexión

Borrar una sesión
-----------------

Endpoint: ``DELETE /api/v2/chat/sessions/{session_id}``

Borra el historial de conversación de la sesión especificada. Devuelve ``cleared: true`` si tiene éxito.

Para la documentación completa de la API (autenticación, CSRF, límites de tasa, códigos HTTP), consulte :doc:`../api/api-chat`.

Interfaz web
============

En la interfaz web de |Fess|, puede usar la funcionalidad de modo de búsqueda IA desde la pantalla de búsqueda.

Iniciar chat
------------

1. Acceda a la pantalla de búsqueda de |Fess|
2. Haga clic en el icono de chat
3. Se mostrará el panel de chat

Usar chat
---------

1. Ingrese una pregunta en el cuadro de texto
2. Haga clic en el botón de enviar o presione la tecla Enter
3. Se mostrará la respuesta del asistente de IA
4. La respuesta incluye enlaces a las fuentes de referencia

Continuar conversación
----------------------

- Puede continuar la conversación dentro de la misma sesión de chat
- Las respuestas consideran el contexto de las preguntas anteriores
- Hacer clic en "Nuevo chat" reinicia la sesión

Solución de problemas
=====================

El botón del modo IA no aparece en la pantalla de búsqueda
----------------------------------------------------------

**Síntoma**: El botón del modo IA no aparece en el encabezado de los resultados
de búsqueda y al acceder a ``/chat`` se redirige a la página principal.

**Lista de verificación**: revise los siguientes puntos en orden.

1. ¿Está ``rag.chat.enabled=true`` configurado?

   - Docker: ¿``-Dfess.config.rag.chat.enabled=true`` está incluido en ``FESS_JAVA_OPTS``?
   - Instalación por paquete: ¿está escrito en ``app/WEB-INF/conf/fess_config.properties``?

2. ¿Está instalado el plugin ``fess-llm-*`` correspondiente?

   - Docker: ``FESS_PLUGINS=fess-llm-gemini:15.9.0`` (o ``fess-llm-openai`` / ``fess-llm-ollama``) debe estar definido
   - Instalación por paquete: el JAR debe estar en ``app/WEB-INF/plugin/``
   - El log de inicio debe incluir ``Installing fess-llm-XXX-15.9.0.jar``

3. ¿Coincide ``rag.llm.name`` con un plugin instalado?

   - El valor por defecto es ``ollama``. Si solo el plugin Gemini está instalado, debe definir explícitamente ``gemini`` (igualmente ``openai`` para el plugin OpenAI)
   - Método (a): editar ``rag.llm.name`` desde Administración > Sistema > General (sección RAG) y guardar
   - Método (b): incluir ``-Dfess.system.rag.llm.name=gemini`` en ``FESS_JAVA_OPTS`` al inicio. Solo actúa como valor inicial por defecto antes de que se persista un valor en OpenSearch

4. ¿Aparece repetidamente un WARN como ``[LLM] LlmClient not found. componentName=ollamaLlmClient`` en el log?

   - Síntoma típico cuando ``rag.llm.name`` sigue siendo ``ollama`` pero el plugin Ollama no está instalado
   - Definir ``rag.llm.name`` al proveedor realmente usado lo resuelve
   - De forma similar, ``componentName=geminiLlmClient`` indica que ``rag.llm.name=gemini`` está definido pero el plugin ``fess-llm-gemini`` no está instalado

5. ¿Está configurada la clave de API específica del proveedor?

   - Si ``rag.llm.gemini.api.key`` / ``rag.llm.openai.api.key`` está vacía, ``checkAvailabilityNow`` devuelve ``false`` y el modo IA queda desactivado
   - Activar DEBUG en ``org.codelibs.fess.llm.gemini`` en ``log4j2.xml`` muestra mensajes como ``[LLM:GEMINI] Gemini is not available. apiKey is blank``

6. ¿Puede el host de Fess alcanzar al proveedor LLM?

   - Para APIs cloud (Gemini / OpenAI), el contenedor debe tener acceso saliente a Internet
   - Si se requiere un proxy, configure ``http.proxy.host`` / ``http.proxy.port`` (y opcionalmente ``http.proxy.username`` / ``http.proxy.password``) en ``fess_config.properties``. En entornos Docker, agregue ``-Dfess.config.http.proxy.host=... -Dfess.config.http.proxy.port=...`` a ``FESS_JAVA_OPTS`` (desde |Fess| 15.9, los clientes LLM utilizan la configuración de proxy común de |Fess|)

.. note::

   La página "General" no expone una casilla para ``rag.chat.enabled`` (por diseño).
   Es una propiedad de la familia FessConfig y solo puede definirse a través de
   ``fess_config.properties`` o ``-Dfess.config.rag.chat.enabled=true``.

El modo de búsqueda IA no se habilita
--------------------------

**Verificaciones**:

1. Si ``rag.chat.enabled=true`` está configurado
2. Si el proveedor LLM está configurado correctamente en ``rag.llm.name``
3. Si el plugin ``fess-llm-*`` correspondiente está instalado
4. Si es posible la conexión al proveedor LLM

Baja calidad de respuestas
--------------------------

**Mejoras**:

1. Usar un modelo LLM de mayor rendimiento
2. Aumentar ``rag.chat.context.max.documents``
3. Personalizar los prompts del sistema en el DI XML
4. Ajustar la configuración de temperature específica del proveedor (consulte la documentación de cada plugin ``fess-llm-*``)

Respuestas lentas
-----------------

**Mejoras**:

1. Usar un modelo LLM más rápido (ej: Gemini Flash)
2. Reducir la configuración de max.tokens específica del proveedor (consulte la documentación de cada plugin ``fess-llm-*``)
3. Reducir ``rag.chat.context.max.documents``

Sesiones no se mantienen
------------------------

**Verificaciones**:

1. Si el sessionId se está enviando correctamente del lado del cliente
2. Configuración de ``rag.chat.session.timeout.minutes``
3. Capacidad del almacenamiento de sesiones

Configuración de depuración
---------------------------

Para investigar problemas, puede ajustar el nivel de log para obtener logs detallados.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm" level="DEBUG"/>
    <Logger name="org.codelibs.fess.api.v2.handlers" level="DEBUG"/>
    <Logger name="org.codelibs.fess.chat" level="DEBUG"/>

Los mensajes de log usan el prefijo ``[RAG]``, con subprefijos como ``[RAG:INTENT]``, ``[RAG:EVAL]`` y ``[RAG:ANSWER]`` para cada fase.
A nivel INFO, se emiten logs de finalización de chat (tiempo transcurrido, cantidad de fuentes). A nivel DEBUG, se emiten detalles de uso de tokens, control de concurrencia y empaquetado del historial.

Registro de búsqueda y tipo de acceso
--------------------------------------

Las búsquedas a través del modo de búsqueda IA se registran con el nombre del proveedor LLM (por ejemplo, ``ollama``, ``openai``, ``gemini``) como tipo de acceso en los registros de búsqueda. Esto permite distinguir las búsquedas del modo IA de las búsquedas web o API regulares en los análisis.

Información de referencia
=========================

- :doc:`llm-overview` - Descripción general de integración LLM
- :doc:`llm-ollama` - Configuración de Ollama
- :doc:`llm-openai` - Configuración de OpenAI
- :doc:`llm-gemini` - Configuración de Google Gemini
- :doc:`../api/api-chat` - Referencia de Chat API
- :doc:`../user/chat-search` - Guía de búsqueda con chat para usuarios finales
