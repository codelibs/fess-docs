==========================
Chat API
==========================

Descripción general
===================

La Chat API es la API v2 para acceder programáticamente a la función de modo de búsqueda con IA (chat RAG) de |Fess|.
Permite obtener respuestas (completaciones) generadas por un LLM basadas en resultados de búsqueda.

Esta API proporciona los siguientes tres endpoints:

.. tabularcolumns:: |p{6cm}|p{9cm}|
.. list-table::
   :header-rows: 1

   * - Endpoint
     - Descripción
   * - ``POST /chat``
     - Completación de chat RAG en lote (sin streaming).
   * - ``POST /chat/stream``
     - Completación de chat RAG en streaming (Server-Sent Events).
   * - ``DELETE /chat/sessions/{session_id}``
     - Borrar el historial de conversación de una sesión de chat.

Para la URL base y el sobre de respuesta común y los códigos de error, consulte :doc:`api-overview`.

::

    http://<Server Name>/api/v2/

Ejemplo en entorno local:

::

    http://localhost:8080/api/v2

Requisitos previos
==================

Para usar la Chat API, se requiere la siguiente configuración:

1. La función de modo de búsqueda con IA (chat RAG) debe estar habilitada (``rag.chat.enabled=true``)
2. El proveedor LLM debe estar configurado

Cuando la función está deshabilitada (``rag.chat.enabled=false``), las solicitudes resultan en un error ``invalid_request``.

Para el método de configuración detallado, consulte :doc:`../config/rag-chat` y :doc:`../config/llm-overview`.

Autenticación y CSRF
====================

Dado que todos los endpoints de la Chat API son solicitudes que modifican el estado (``POST`` / ``DELETE``), se requiere la cabecera ``X-Fess-CSRF-Token``.
Para la obtención del token CSRF y los detalles de autenticación y sesión, consulte :doc:`api-overview`.

Límite de velocidad
===================

``POST /chat`` , ``POST /chat/stream`` y ``DELETE /chat/sessions/{session_id}`` tienen un límite de velocidad por usuario.

- Valor predeterminado: 30 solicitudes por minuto (por usuario)
- Clave de configuración: ``api.v2.chat.rate.limit.per.user.per.minute``
- Establecer el valor en ``0`` o menos desactiva el límite de velocidad.

Cuando se supera el límite de velocidad, se devuelve el error ``rate_limited`` (HTTP 429). La cabecera ``Retry-After`` se establece con un valor fijo de ``60`` (segundos).
Este límite de velocidad es compartido entre ``POST /chat`` , ``POST /chat/stream`` , ``DELETE /chat/sessions/{session_id}``.

.. note::

   El límite de velocidad se aplica únicamente cuando es posible identificar al usuario. En llamadas anónimas en las que no se ha establecido sesión y no se puede resolver el ID de usuario, el límite de velocidad se omite.

POST /chat
==========

Realiza una completación de chat de forma síncrona.
La sesión se identifica mediante ``session_id``. Cuando se omite ``session_id``, el servidor crea una sesión y la devuelve en el ``session_id`` de la respuesta.

Los valores inválidos pasados en ``fields.label`` o ``extra_queries`` se eliminan silenciosamente de la solicitud resuelta y no se reflejan en el sobre de respuesta.

Endpoint
--------

::

    POST /api/v2/chat

Cuerpo de la solicitud
----------------------

Cuerpo JSON con ``Content-Type: application/json``.

El tamaño máximo del cuerpo de la solicitud es de 32 KiB. Si se supera, se produce un error ``payload_too_large`` (HTTP 413).

.. tabularcolumns:: |p{3.5cm}|p{2.5cm}|p{1.5cm}|p{7cm}|
.. list-table:: ChatRequest
   :header-rows: 1

   * - Campo
     - Tipo
     - Obligatorio
     - Descripción
   * - ``message``
     - string
     - Sí
     - Mensaje del usuario (pregunta). La longitud máxima está limitada por ``rag.chat.message.max.length`` (valor predeterminado: 4000). Si se supera, se produce un error ``invalid_request`` (HTTP 400).
   * - ``session_id``
     - string
     - No
     - ID de sesión. Cuando se omite, el servidor lo crea y lo devuelve en la respuesta.
   * - ``fields``
     - object
     - No
     - Campos de filtro opcionales para el paso de recuperación.
   * - ``fields.label``
     - string / array de string
     - No
     - Limita la recuperación a etiquetas de la lista de permitidos.
   * - ``extra_queries``
     - string / array de string
     - No
     - Expresiones de consultas de faceta de la lista de permitidos.

Ejemplo de solicitud:

.. code-block:: json

    {
      "message": "Fessとは何ですか？",
      "session_id": "abc123def456",
      "fields": {
        "label": "news"
      },
      "extra_queries": "label:faq"
    }

Respuesta
---------

**En caso de éxito (HTTP 200, ChatResponse)**

La respuesta se almacena en el sobre común ``response``. ``session_id`` siempre existe.

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: Elementos de response
   :header-rows: 1

   * - Campo
     - Tipo
     - Descripción
   * - ``session_id``
     - string
     - ID de sesión.
   * - ``content``
     - string (nullable)
     - Texto del mensaje generado. Siempre existe, pero puede ser ``null`` si el modelo no generó contenido.
   * - ``sources``
     - array
     - Array de documentos de referencia. Cada elemento es un ChatSource.

**ChatSource**

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: Elementos de ChatSource
   :header-rows: 1

   * - Campo
     - Tipo
     - Descripción
   * - ``rank``
     - integer
     - Posición desde 1 en el conjunto recuperado.
   * - ``title``
     - string (nullable)
     - Título del documento.
   * - ``url``
     - string (nullable)
     - URL del documento.
   * - ``doc_id``
     - string (nullable)
     - ID del documento.
   * - ``snippet``
     - string (nullable)
     - Fragmento del documento.
   * - ``url_link``
     - string (nullable)
     - Enlace URL para visualización.
   * - ``go_url``
     - string (nullable)
     - URL para redirección.

Ejemplo de respuesta:

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session_id": "abc123def456",
        "content": "Fessは全文検索サーバーです。主な特徴として...",
        "sources": [
          {
            "rank": 1,
            "title": "Fessの概要",
            "url": "https://fess.codelibs.org/ja/overview.html",
            "doc_id": "abcdef0123456789",
            "snippet": "Fessは...",
            "url_link": "https://fess.codelibs.org/ja/overview.html",
            "go_url": "/go/?docId=abcdef0123456789"
          }
        ]
      }
    }

Códigos de estado HTTP
----------------------

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - Código
     - Descripción
   * - 200
     - Solicitud exitosa.
   * - 400
     - Solicitud inválida (ausencia de ``message``, longitud de ``message`` que supera el máximo permitido, ``rag.chat.enabled=false``, etc.).
   * - 403
     - Token CSRF ausente o expirado, entre otros motivos.
   * - 405
     - El método HTTP no está permitido.
   * - 413
     - El cuerpo de la solicitud supera el límite de tamaño (32 KiB).
   * - 415
     - ``Content-Type`` no es ``application/json``, está ausente, o el ``charset`` no es UTF-8.
   * - 429
     - Se superó el límite de velocidad.
   * - 500
     - Error interno del servidor.

Ejemplo de cURL
---------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -d '{"message":"Fessとは何ですか？","session_id":"abc123def456"}'

POST /chat/stream
=================

Realiza una completación de chat en formato de streaming.
El cuerpo de la solicitud es el mismo que ``POST /chat`` (ChatRequest).

La respuesta de éxito son eventos con nombre en formato ``text/event-stream`` (Server-Sent Events).
Cada evento se compone de ``event: <nombre>`` y ``data: <JSON>``.

Los fallos de validación previos al stream siguen devolviendo un sobre JSON (con los mismos códigos de error que ``POST /chat``).
Los valores inválidos en ``fields.label`` o ``extra_queries`` se eliminan silenciosamente y no se reflejan en el sobre de respuesta ni en los eventos SSE.

Endpoint
--------

::

    POST /api/v2/chat/stream

Eventos SSE
-----------

.. tabularcolumns:: |p{2.5cm}|p{12.5cm}|
.. list-table::
   :header-rows: 1

   * - Evento
     - Descripción (payload)
   * - ``phase``
     - Transición de fase del pipeline (``{ phase, status, message?, keywords?, hit_count?, ... }``). ``message`` y ``keywords`` se emiten en onPhaseStart. Los campos opcionales adicionales (ejemplo: ``hit_count``) fluyen desde el payload de onPhaseComplete.
   * - ``chunk``
     - Fragmento de texto generado (``{ content }``).
   * - ``sources``
     - Fuentes recuperadas (``{ sources: [ChatSource] }``).
   * - ``retry``
     - Retroceso ante fallo temporal (``{ phase, operation, attempt, max_attempts, sleep_ms, cause? }``).
   * - ``waiting``
     - Progreso de una fase de larga duración (``{ phase, reason, elapsed_ms, timeout_ms }``).
   * - ``fallback``
     - Reescritura de consulta o retroceso de estrategia (``{ phase, reason, original_query?, new_query? }``).
   * - ``warning``
     - Advertencia recuperable (``{ phase, code, detail? }``).
   * - ``done``
     - Fin del stream (``{ session_id, html_content? }``).
   * - ``error``
     - Fallo terminal a mitad del stream (``{ phase?, message, error_code }``). El campo ``message`` tiene la misma cadena que ``error_code``. El cliente debe localizar usando ``error_code``.

Ejemplo de stream SSE:

::

    event: phase
    data: {"phase":"search","status":"start","message":"Searching documents...","keywords":"Fess インストール"}

    event: chunk
    data: {"content":"Fessは"}

    event: sources
    data: {"sources":[{"rank":1,"title":"インストールガイド","url":"https://fess.codelibs.org/ja/install.html"}]}

    event: done
    data: {"session_id":"abc123def456"}

Códigos de estado HTTP
----------------------

Cuando la validación previa al stream falla, se devuelven los siguientes códigos de error en un sobre JSON.

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - Código
     - Descripción
   * - 200
     - Inicio del stream SSE (éxito).
   * - 400
     - Solicitud inválida (ausencia de ``message``, ``rag.chat.enabled=false``, etc.).
   * - 403
     - Token CSRF ausente o expirado, entre otros motivos.
   * - 405
     - El método HTTP no está permitido.
   * - 413
     - El cuerpo de la solicitud supera el límite de tamaño (32 KiB).
   * - 415
     - ``Content-Type`` no es ``application/json``, está ausente, o el ``charset`` no es UTF-8.
   * - 429
     - Se superó el límite de velocidad.
   * - 500
     - Error interno del servidor.

Ejemplo de cURL
---------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat/stream" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -H "Accept: text/event-stream" \
         --no-buffer \
         -d '{"message":"Fessの特徴を教えてください"}'

DELETE /chat/sessions/{session_id}
===================================

Borra el historial de conversación de la sesión de chat especificada.
La sesión se identifica mediante ``session_id`` en la ruta.

Cuando tiene éxito, se devuelve ``cleared: true``. Cuando no se encuentra ninguna sesión activa coincidente, se produce un error ``not_found`` (HTTP 404).

Endpoint
--------

::

    DELETE /api/v2/chat/sessions/{session_id}

Parámetros de ruta
------------------

.. tabularcolumns:: |p{3cm}|p{2cm}|p{10cm}|
.. list-table::
   :header-rows: 1

   * - Parámetro
     - Tipo
     - Descripción
   * - ``session_id``
     - string
     - ID de la sesión a borrar. minLength 1, maxLength 128, patrón ``^[A-Za-z0-9._-]+$``.

Respuesta
---------

**En caso de éxito (HTTP 200, ChatClearResponse)**

La respuesta se almacena en el sobre común ``response``. ``session_id`` y ``cleared`` siempre existen.

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: Elementos de response
   :header-rows: 1

   * - Campo
     - Tipo
     - Descripción
   * - ``session_id``
     - string
     - ID de sesión.
   * - ``cleared``
     - boolean
     - Siempre ``true`` (cuando la sesión fue encontrada y borrada).

Ejemplo de respuesta:

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session_id": "abc123def456",
        "cleared": true
      }
    }

Códigos de estado HTTP
----------------------

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - Código
     - Descripción
   * - 200
     - La sesión fue borrada.
   * - 400
     - La solicitud no es válida (por ejemplo, ``session_id`` no coincide con el patrón ``^[A-Za-z0-9._-]+$`` o con el límite de longitud de 1–128 caracteres, o ``rag.chat.enabled=false``).
   * - 403
     - Token CSRF ausente o expirado, entre otros motivos.
   * - 404
     - No se encontró ninguna sesión activa coincidente.
   * - 405
     - El método HTTP no está permitido.
   * - 429
     - Se superó el límite de velocidad.
   * - 500
     - Error interno del servidor.

Ejemplo de cURL
---------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/v2/chat/sessions/abc123def456" \
         -H "X-Fess-CSRF-Token: <token>"

Seguridad
=========

Notas de seguridad al usar la Chat API:

1. **Autenticación**: La API v2 utiliza autenticación basada en sesión. Consulte :doc:`api-overview` para más detalles.
2. **CSRF**: Las solicitudes que modifican el estado requieren la cabecera ``X-Fess-CSRF-Token``.
3. **Límite de velocidad**: Para prevenir ataques DoS, se aplica un límite de velocidad por usuario (predeterminado 30/min). La clave de configuración es ``api.v2.chat.rate.limit.per.user.per.minute``.

Información de referencia
=========================

- :doc:`../config/rag-chat` - Configuración de la función de modo de búsqueda con IA
- :doc:`../config/llm-overview` - Descripción general de la integración LLM
- :doc:`../user/chat-search` - Guía de búsqueda con chat para usuarios finales
- :doc:`api-overview` - Descripción general de la API
