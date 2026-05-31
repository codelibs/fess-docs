================
API de favoritos
================

Este documento describe la API de favoritos v2 de |Fess|.
Para el sobre de respuesta común, el modelo de errores y CSRF, consulte :doc:`api-overview`.

La URL base es ``http://<Server Name>/api/v2/`` (ejemplo en entorno local: ``http://localhost:8080/api/v2``).

.. note::

   Para utilizar la función de favoritos, la configuración ``user.favorite`` debe estar habilitada.

Obtención de lista de documentos favoritos
==========================================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v2/favorites``
==================  ====================================================

Devuelve los ID de los documentos que el usuario que realiza la llamada ha marcado como favoritos en los resultados de búsqueda identificados por ``query_id``.
``query_id`` es el identificador opaco (campo ``query_id``) devuelto por la API de búsqueda (``/search``).

Las llamadas anónimas (sin código de usuario vinculado a la sesión) resultan en ``auth_required`` (401).
Cuando la función ``user.favorite`` está deshabilitada, resulta en ``invalid_request`` (400).
Cuando ``query_id`` no coincide con un conjunto de resultados en caché en la sesión, se devuelve ``200`` con un array ``data`` vacío.

Parámetros de solicitud
-----------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Parámetros de solicitud

   * - ``query_id``
     - ``query_id`` opaco devuelto por la API de búsqueda (``/search``) (query, obligatorio, str).

Tabla: Parámetros de solicitud

Respuesta
---------

En caso de éxito (200), se devuelven los siguientes campos directamente bajo ``response`` del sobre común.

::

    {
      "response": {
        "status": 0,
        "record_count": 2,
        "data": [
          { "doc_id": "a1b2c3d4e5f6" },
          { "doc_id": "f6e5d4c3b2a1" }
        ]
      }
    }

Los campos son los siguientes:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Campos de respuesta

   * - ``record_count``
     - Número de documentos favoritos en ``data`` (int).
   * - ``data``
     - Array que devuelve los documentos favoritos en el conjunto de resultados consultado, preservando el orden de los resultados de búsqueda. Cada elemento es ``{doc_id}``.

Tabla: Campos de respuesta

Respuesta de error
------------------

Consulte :doc:`api-overview` para detalles del modelo de errores. Los estados HTTP que devuelve este endpoint son:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 400 Bad Request
     - Cuando la solicitud no es válida (incluye el caso en que la función ``user.favorite`` está deshabilitada).
   * - 401 Unauthorized
     - Cuando se requiere autenticación (llamada anónima).
   * - 405 Method Not Allowed
     - Cuando el método HTTP no está permitido.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.

Tabla: Respuesta de error

Obtención del estado de favorito
=================================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v2/documents/{docId}/favorite``
==================  ====================================================

Obtiene el estado de favorito del documento especificado.

Parámetros de solicitud
-----------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Parámetros de solicitud

   * - ``docId``
     - Identificador del documento (path, obligatorio, patrón ``^[A-Za-z0-9_-]+$``).

Tabla: Parámetros de solicitud

Respuesta
---------

En caso de éxito (200), se devuelven los siguientes campos directamente bajo ``response`` del sobre común.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "favorite": true,
        "count": 5
      }
    }

Los campos son los siguientes:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Campos de respuesta

   * - ``doc_id``
     - ID del documento (str).
   * - ``favorite``
     - Si el documento es favorito del usuario que realiza la llamada (bool).
   * - ``count``
     - Número total de favoritos de este documento (int64).

Tabla: Campos de respuesta

Respuesta de error
------------------

Consulte :doc:`api-overview` para detalles del modelo de errores. Los estados HTTP que devuelve este endpoint son:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 400 Bad Request
     - Cuando la solicitud no es válida.
   * - 404 Not Found
     - Cuando no se encuentra el recurso.
   * - 405 Method Not Allowed
     - Cuando el método HTTP no está permitido.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.

Tabla: Respuesta de error

Registro de favorito
====================

Solicitud
---------

==================  ====================================================
Método HTTP         POST
Endpoint            ``/api/v2/documents/{docId}/favorite``
==================  ====================================================

Registra el documento especificado como favorito.
Al ser una solicitud que modifica el estado, se requiere la cabecera ``X-Fess-CSRF-Token`` (consulte :doc:`api-overview`).

Parámetros de solicitud
-----------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Parámetros de solicitud

   * - ``docId``
     - Identificador del documento (path, obligatorio, patrón ``^[A-Za-z0-9_-]+$``).

Tabla: Parámetros de solicitud

Cuerpo de la solicitud
----------------------

Envíe un JSON (FavoritePostRequest) con ``Content-Type: application/json`` con los siguientes campos:

::

    {
      "query_id": "f8b1c2d3e4a5"
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Cuerpo de la solicitud

   * - ``query_id``
     - ``query_id`` opaco devuelto por la API de búsqueda (``/search``) (str, obligatorio).

Tabla: Cuerpo de la solicitud

Respuesta
---------

En caso de éxito (200), se devuelven los siguientes campos directamente bajo ``response`` del sobre común.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "ok": true,
        "favorite": true,
        "count": 6,
        "already_existed": false
      }
    }

Los campos son los siguientes:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Campos de respuesta

   * - ``doc_id``
     - ID del documento (str).
   * - ``ok``
     - Siempre ``true`` (bool).
   * - ``favorite``
     - Siempre ``true`` (bool). Tanto si es nuevo como si ya existía, el documento es favorito del usuario que realiza la llamada.
   * - ``count``
     - Número actual de favoritos tras la operación (int64). Para un nuevo registro, es el recuento anterior +1 (optimista); para un POST idempotente repetido, refleja el recuento guardado.
   * - ``already_existed``
     - ``true`` si el favorito ya estaba registrado anteriormente (bool, POST idempotente). No existe en el primer POST que registra un favorito nuevo.

Tabla: Campos de respuesta

Respuesta de error
------------------

Consulte :doc:`api-overview` para detalles del modelo de errores. Los estados HTTP que devuelve este endpoint son:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 400 Bad Request
     - Cuando la solicitud no es válida.
   * - 401 Unauthorized
     - Cuando se requiere autenticación.
   * - 403 Forbidden
     - Cuando no está permitido por ausencia o expiración del token CSRF, entre otros motivos.
   * - 404 Not Found
     - Cuando no se encuentra el recurso.
   * - 405 Method Not Allowed
     - Cuando el método HTTP no está permitido.
   * - 413 Payload Too Large
     - Cuando el cuerpo de la solicitud supera el límite de tamaño.
   * - 415 Unsupported Media Type
     - Cuando el ``Content-Type`` no es admitido.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.

Tabla: Respuesta de error
