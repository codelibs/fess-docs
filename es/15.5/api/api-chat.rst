==========================
Chat API
==========================

Descripcion general
===================

La Chat API es una API RESTful para acceder programaticamente a la funcionalidad de modo IA de |Fess|.
Permite obtener respuestas asistidas por IA basadas en resultados de busqueda.

Esta API proporciona dos endpoints:

- **API sin streaming**: Obtiene la respuesta completa de una vez
- **API con streaming**: Obtiene la respuesta en tiempo real en formato Server-Sent Events (SSE)

Requisitos previos
==================

Para usar la Chat API, se requiere la siguiente configuracion:

1. La funcionalidad de modo IA debe estar habilitada (``rag.chat.enabled=true``)
2. El proveedor LLM debe estar configurado

Para el metodo de configuracion detallado, consulte :doc:`../config/rag-chat`.

API sin streaming
=================

Endpoint
--------

::

    POST /api/v1/chat

Parametros de solicitud
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametro
     - Tipo
     - Requerido
     - Descripcion
   * - ``message``
     - String
     - Si
     - Mensaje (pregunta) del usuario
   * - ``sessionId``
     - String
     - No
     - ID de sesion. Especificar para continuar la conversacion
   * - ``clear``
     - String
     - No
     - Especificar ``"true"`` para limpiar la sesion

Respuesta
---------

**Exito (HTTP 200)**

.. code-block:: json

    {
      "status": "ok",
      "sessionId": "abc123def456",
      "content": "Fess es un servidor de busqueda de texto completo. Sus principales caracteristicas son...",
      "sources": [
        {
          "title": "Descripcion general de Fess",
          "url": "https://fess.codelibs.org/ja/overview.html"
        },
        {
          "title": "Lista de funcionalidades",
          "url": "https://fess.codelibs.org/ja/features.html"
        }
      ]
    }

**Error**

.. code-block:: json

    {
      "status": "error",
      "message": "Message is required"
    }

Codigos de estado HTTP
----------------------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Codigo
     - Descripcion
   * - 200
     - Solicitud exitosa
   * - 400
     - Parametros de solicitud invalidos (mensaje vacio, etc.)
   * - 404
     - Endpoint no encontrado
   * - 405
     - Metodo HTTP no permitido (solo POST permitido)
   * - 500
     - Error interno del servidor

Ejemplos de uso
---------------

cURL
~~~~

.. code-block:: bash

    # Iniciar nuevo chat
    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=Que es Fess?"

    # Continuar conversacion
    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=Por favor explicame el metodo de instalacion" \
         -d "sessionId=abc123def456"

    # Limpiar sesion
    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "sessionId=abc123def456" \
         -d "clear=true"

JavaScript
~~~~~~~~~~

.. code-block:: javascript

    async function chat(message, sessionId = null) {
      const params = new URLSearchParams();
      params.append('message', message);
      if (sessionId) {
        params.append('sessionId', sessionId);
      }

      const response = await fetch('/api/v1/chat', {
        method: 'POST',
        body: params
      });

      return await response.json();
    }

    // Ejemplo de uso
    const result = await chat('Por favor explicame las funcionalidades de Fess');
    console.log(result.content);
    console.log('Session ID:', result.sessionId);

Python
~~~~~~

.. code-block:: python

    import requests

    def chat(message, session_id=None):
        data = {'message': message}
        if session_id:
            data['sessionId'] = session_id

        response = requests.post(
            'http://localhost:8080/api/v1/chat',
            data=data
        )
        return response.json()

    # Ejemplo de uso
    result = chat('Como instalo Fess?')
    print(result['content'])
    print(f"Session ID: {result['sessionId']}")

API con streaming
=================

Endpoint
--------

::

    POST /api/v1/chat/stream
    GET /api/v1/chat/stream

Parametros de solicitud
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametro
     - Tipo
     - Requerido
     - Descripcion
   * - ``message``
     - String
     - Si
     - Mensaje (pregunta) del usuario
   * - ``sessionId``
     - String
     - No
     - ID de sesion. Especificar para continuar la conversacion

Formato de respuesta
--------------------

La API con streaming devuelve respuestas en formato ``text/event-stream`` (Server-Sent Events).

Cada evento tiene el siguiente formato:

::

    event: <nombre_evento>
    data: <datos_JSON>

Eventos SSE
-----------

**session**

Notifica la informacion de sesion. Se envia al inicio del stream.

.. code-block:: json

    {
      "sessionId": "abc123def456"
    }

**phase**

Notifica el inicio/fin de las fases de procesamiento.

.. code-block:: json

    {
      "phase": "intent_analysis",
      "status": "start",
      "message": "Analyzing user intent..."
    }

.. code-block:: json

    {
      "phase": "search",
      "status": "start",
      "message": "Searching documents...",
      "keywords": "Fess instalacion"
    }

.. code-block:: json

    {
      "phase": "search",
      "status": "complete"
    }

Tipos de fase:

- ``intent_analysis`` - Analisis de intencion
- ``search`` - Ejecucion de busqueda
- ``evaluation`` - Evaluacion de resultados
- ``generation`` - Generacion de respuesta

**chunk**

Notifica fragmentos de texto generado.

.. code-block:: json

    {
      "content": "Fess es"
    }

**sources**

Notifica la informacion de los documentos de referencia.

.. code-block:: json

    {
      "sources": [
        {
          "title": "Guia de instalacion",
          "url": "https://fess.codelibs.org/ja/install.html"
        }
      ]
    }

**done**

Notifica la finalizacion del procesamiento.

.. code-block:: json

    {
      "sessionId": "abc123def456",
      "htmlContent": "<p>Fess es un servidor de busqueda de texto completo...</p>"
    }

**error**

Notifica errores.

.. code-block:: json

    {
      "phase": "generation",
      "message": "LLM request failed"
    }

Ejemplos de uso
---------------

cURL
~~~~

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v1/chat/stream" \
         -d "message=Por favor explicame las caracteristicas de Fess" \
         -H "Accept: text/event-stream" \
         --no-buffer

JavaScript (EventSource)
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: javascript

    function streamChat(message, sessionId = null) {
      const params = new URLSearchParams();
      params.append('message', message);
      if (sessionId) {
        params.append('sessionId', sessionId);
      }

      // Usar fetch para solicitudes POST
      return fetch('/api/v1/chat/stream', {
        method: 'POST',
        body: params
      }).then(response => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        function read() {
          return reader.read().then(({ done, value }) => {
            if (done) return;

            const text = decoder.decode(value);
            const lines = text.split('\n');

            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const data = JSON.parse(line.slice(6));
                handleEvent(data);
              }
            }

            return read();
          });
        }

        return read();
      });
    }

    function handleEvent(data) {
      if (data.content) {
        // Mostrar fragmento
        document.getElementById('output').textContent += data.content;
      } else if (data.phase) {
        // Mostrar informacion de fase
        console.log(`Phase: ${data.phase} - ${data.status}`);
      } else if (data.sources) {
        // Mostrar informacion de fuentes
        console.log('Sources:', data.sources);
      }
    }

Python
~~~~~~

.. code-block:: python

    import requests

    def stream_chat(message, session_id=None):
        data = {'message': message}
        if session_id:
            data['sessionId'] = session_id

        response = requests.post(
            'http://localhost:8080/api/v1/chat/stream',
            data=data,
            stream=True,
            headers={'Accept': 'text/event-stream'}
        )

        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    import json
                    data = json.loads(line[6:])
                    yield data

    # Ejemplo de uso
    for event in stream_chat('Por favor explicame las funcionalidades de Fess'):
        if 'content' in event:
            print(event['content'], end='', flush=True)
        elif 'phase' in event:
            print(f"\n[Phase: {event['phase']} - {event['status']}]")

Manejo de errores
=================

Implemente un manejo de errores apropiado al usar la API.

.. code-block:: javascript

    async function chatWithErrorHandling(message, sessionId = null) {
      try {
        const params = new URLSearchParams();
        params.append('message', message);
        if (sessionId) {
          params.append('sessionId', sessionId);
        }

        const response = await fetch('/api/v1/chat', {
          method: 'POST',
          body: params
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.message || 'API request failed');
        }

        const result = await response.json();

        if (result.status === 'error') {
          throw new Error(result.message);
        }

        return result;

      } catch (error) {
        console.error('Chat API error:', error);
        throw error;
      }
    }

Limite de tasa
==============

La Chat API tiene un limite de tasa aplicado.

Configuracion predeterminada:

- 10 solicitudes por minuto

Cuando se excede el limite de tasa, se devuelve un error HTTP 429.

Para la configuracion del limite de tasa, consulte :doc:`../config/rag-chat`.

Seguridad
=========

Notas de seguridad al usar la Chat API:

1. **Autenticacion**: La version actual no requiere autenticacion para la API, pero considere un control de acceso apropiado en entornos de produccion
2. **Limite de tasa**: Habilite el limite de tasa para prevenir ataques DoS
3. **Validacion de entrada**: Realice validacion de entrada tambien del lado del cliente
4. **CORS**: Verifique la configuracion de CORS segun sea necesario

Informacion de referencia
=========================

- :doc:`../config/rag-chat` - Configuracion de la funcionalidad de modo IA
- :doc:`../config/llm-overview` - Descripcion general de integracion LLM
- :doc:`../user/chat-search` - Guia de busqueda con chat para usuarios finales
- :doc:`api-overview` - Descripcion general de API
