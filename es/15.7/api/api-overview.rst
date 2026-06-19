=============================
Descripción general de la API
=============================


API proporcionadas por |Fess|
==============================

Este documento describe las API Web (v2) que proporciona |Fess|.
Utilizando las API, puede usar |Fess| como servidor de búsqueda desde sistemas web existentes y aplicaciones de página única (SPA), entre otros.

.. note::

   En |Fess| 15.7, la API ha sido renovada a la versión **v2**. La API de búsqueda
   JSON y la API de chat de ``/api/v1`` han sido eliminadas e integradas en ``/api/v2``.
   Los clientes que utilizaban ``/api/v1`` deben migrar a ``/api/v2``.

URL base
========

Los endpoints de la API v2 de |Fess| se proporcionan con la siguiente URL base:

::

    http://<Server Name>/api/v2/

Por ejemplo, en un entorno local sería:

::

    http://localhost:8080/api/v2/

Sobre de respuesta
==================

Todas las respuestas JSON de v2 se devuelven con una estructura de sobre común.

::

    {
      "response": {
        "status": 0,
        ...
      }
    }

``response.status`` representa el resultado del procesamiento y sigue las convenciones de v1.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Valores de status

   * - 0
     - Éxito
   * - 1
     - Error de cliente
   * - 9
     - Error del sistema

Tabla: Valores de status

Tenga en cuenta que ``response.status >= 1`` y que el código de estado HTTP sea ``400`` o superior siempre son coincidentes.

Nombres de campos
-----------------

Todos los campos JSON, incluyendo el cuerpo de la solicitud, el cuerpo de la respuesta y los datos de eventos SSE, utilizan ``snake_case`` de forma uniforme.

Respuesta de error
==================

En caso de error, se añade un objeto ``error`` al sobre.

::

    {
      "response": {
        "status": 1,
        "error": {
          "code": "invalid_request",
          "message": "..."
        }
      }
    }

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Elementos de error

   * - code
     - Código de error estable (``snake_case``). Se recomienda que los clientes realicen la localización basándose en este valor.
   * - message
     - Mensaje de error legible por humanos (en inglés). Al mostrarlo, localice en el lado del cliente basándose en ``code``.
   * - details
     - Objeto opcional que contiene información estructurada adicional (puede omitirse). Solo algunos endpoints lo incluyen. Por ejemplo, :doc:`api-health` incorpora una instantánea del clúster del motor de búsqueda en ``error.details.engine``.

Tabla: Elementos de error

Códigos de error y códigos de estado HTTP
-----------------------------------------

El código de estado HTTP predeterminado se determina según ``error.code``.

.. tabularcolumns:: |p{5cm}|p{3cm}|p{7cm}|
.. list-table:: Lista de códigos de error

   * - error.code
     - Estado HTTP
     - Descripción
   * - ``invalid_request``
     - 400
     - La solicitud no es válida.
   * - ``auth_required``
     - 401
     - Se requiere autenticación o las credenciales son inválidas.
   * - ``forbidden``
     - 403
     - No está permitido (token CSRF ausente, expirado, etc.).
   * - ``not_found``
     - 404
     - No se encontró el recurso.
   * - ``method_not_allowed``
     - 405
     - El método HTTP no está permitido. Los métodos admitidos se enumeran en la cabecera ``Allow``.
   * - ``not_acceptable``
     - 406
     - La solicitud no es aceptable.
   * - ``conflict``
     - 409
     - Se produjo un conflicto de recursos.
   * - ``payload_too_large``
     - 413
     - El cuerpo de la solicitud excede el límite de tamaño.
   * - ``unsupported_media_type``
     - 415
     - ``Content-Type`` no admitido (la mayoría de los endpoints requieren ``application/json``).
   * - ``rate_limited``
     - 429
     - Se superó el límite de velocidad. La cabecera ``Retry-After`` indica los segundos que se deben esperar.
   * - ``internal_error``
     - 500
     - Se produjo un error interno en el servidor.
   * - ``service_unavailable``
     - 503
     - El servicio no está disponible temporalmente.

Tabla: Lista de códigos de error

.. note::

   La respuesta ``method_not_allowed`` incluye una cabecera ``Allow`` que enumera
   los métodos HTTP admitidos.

Autenticación y sesión
======================

La API v2 utiliza autenticación basada en sesión.
El inicio de sesión se realiza mediante ``POST /auth/login``; si tiene éxito, se establece una sesión y se emite un token CSRF.
El estado de autenticación actual puede verificarse con ``GET /auth/me``. Consulte :doc:`api-auth` para más detalles.

Los endpoints que no requieren inicio de sesión, como la búsqueda, pueden utilizarse de forma anónima (dependiendo de la opción "Inicio de sesión obligatorio" en la Configuración del sistema).

Token CSRF
----------

Las solicitudes que modifican el estado (``POST`` / ``PUT`` / ``DELETE``) requieren la cabecera ``X-Fess-CSRF-Token``.
El token CSRF se puede obtener de las siguientes formas:

- Campo ``csrf_token`` en la respuesta de ``POST /auth/login``
- Respuesta de ``GET /ui/config`` (campo ``csrf_token`` cuando ``csrf_required=true``)

El token se rota en cada inicio de sesión, cierre de sesión y cambio de contraseña.

.. note::

   La validación CSRF se realiza **antes** que la autenticación. Por lo tanto, una
   solicitud de cambio de estado sin sesión válida ni token CSRF válido recibirá
   ``403 forbidden`` en lugar de ``401 auth_required``. ``/auth/login`` está
   excluido de la validación CSRF porque el token no existe antes del inicio de sesión.

Formatos de streaming
=====================

Algunos endpoints devuelven respuestas en formato de streaming en lugar de JSON ordinario.

.. tabularcolumns:: |p{4cm}|p{4cm}|p{7cm}|
.. list-table:: Formatos de streaming

   * - Endpoint
     - Content-Type
     - Descripción
   * - ``/chat/stream``
     - ``text/event-stream``
     - Server-Sent Events (SSE). Consulte :doc:`api-chat` para más detalles.
   * - ``/documents/all``
     - ``application/x-ndjson``
     - NDJSON (cada línea es un documento con formato ``{"data":{...}}``. Solo cuando hay un fallo a mitad del stream, la última línea será ``{"error":{...}}``). Consulte :doc:`api-search` para más detalles.

Tabla: Formatos de streaming

Tipos de API
============

|Fess| proporciona las siguientes API v2:

.. tabularcolumns:: |p{3cm}|p{4cm}|p{8cm}|
.. list-table::

   * - Tipo
     - Endpoints principales
     - Descripción
   * - :doc:`search <api-search>`
     - ``/search`` , ``/documents/all``
     - API para buscar documentos y obtener todos los documentos (scroll).
   * - :doc:`label <api-label>`
     - ``/labels``
     - API para obtener la lista de etiquetas configuradas.
   * - :doc:`suggest <api-suggest>`
     - ``/suggest-words``
     - API para obtener palabras sugeridas.
   * - :doc:`popularword <api-popularword>`
     - ``/popular-words``
     - API para obtener palabras populares.
   * - :doc:`related <api-related>`
     - ``/related-queries`` , ``/related-content``
     - API para obtener consultas relacionadas y contenido relacionado.
   * - :doc:`health <api-health>`
     - ``/health``
     - API para obtener el estado del clúster del motor de búsqueda.
   * - :doc:`auth <api-auth>`
     - ``/auth/login`` , ``/auth/logout`` , ``/auth/me`` , ``/auth/password``
     - API para operaciones de autenticación y sesión (inicio de sesión, cierre de sesión, obtención del estado de autenticación, cambio de contraseña).
   * - :doc:`ui <api-uiconfig>`
     - ``/ui/config``
     - API para obtener la configuración inicial (configuración de interfaz de usuario) para SPA.
   * - :doc:`favorite <api-favorite>`
     - ``/favorites`` , ``/documents/{docId}/favorite``
     - API para gestionar documentos favoritos.
   * - :doc:`click <api-click>`
     - ``/click``
     - API para registrar clics en resultados de búsqueda.
   * - :doc:`cache <api-cache>`
     - ``/cache/{docId}``
     - API para obtener el contenido en caché de documentos.
   * - :doc:`chat <api-chat>`
     - ``/chat`` , ``/chat/stream``
     - API para utilizar la función de modo de búsqueda con IA (chat RAG).

Tabla: Tipos de API
