========================
API de registro de clics
========================

Este documento describe la API de registro de clics v2 de |Fess|.
Para el sobre de respuesta común, el modelo de errores y CSRF, consulte :doc:`api-overview`.

La URL base es ``http://<Server Name>/api/v2/`` (ejemplo en entorno local: ``http://localhost:8080/api/v2``).

Registro de un clic
===================

Solicitud
---------

==================  ====================================================
Método HTTP         POST
Endpoint            ``/api/v2/click``
==================  ====================================================

Registra el clic en un resultado de búsqueda en el registro de búsqueda.
Para llamadas anónimas y en instalaciones donde la función de registro de búsqueda está deshabilitada, se devuelve una respuesta de éxito con ``logged: false`` (sin error).

Al ser una solicitud que modifica el estado, se requiere la cabecera ``X-Fess-CSRF-Token`` (consulte :doc:`api-overview`).

Cuerpo de la solicitud
----------------------

Envíe un JSON (ClickRequest) con ``Content-Type: application/json`` con los siguientes campos:

::

    {
      "doc_id": "a1b2c3d4e5f6",
      "query_id": "f8b1c2d3e4a5",
      "rank": 1,
      "rt": 1717142400000
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Cuerpo de la solicitud

   * - ``doc_id``
     - ID del documento (str, obligatorio, patrón ``^[A-Za-z0-9_-]+$``). Identifica el documento cuyo clic se registra.
   * - ``query_id``
     - El ``query_id`` devuelto por la API de búsqueda (``/search``) (str, opcional). Asocia el clic con la consulta de búsqueda de origen.
   * - ``rank``
     - Posición en la lista de resultados (base 1, int, opcional).
   * - ``rt``
     - Epoch en milisegundos de la solicitud de búsqueda original (int64, opcional). Cuando no se especifica, se usa la hora actual del servidor como valor predeterminado.

Tabla: Cuerpo de la solicitud

Respuesta
---------

En caso de éxito (200), se devuelven los siguientes campos directamente bajo ``response`` del sobre común.

::

    {
      "response": {
        "status": 0,
        "ok": true,
        "logged": true
      }
    }

Los campos son los siguientes:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Campos de respuesta

   * - ``ok``
     - Siempre ``true`` (bool).
   * - ``logged``
     - ``false`` cuando la persistencia del registro de búsqueda está deshabilitada o el llamante es anónimo (bool). Aun así se devuelve una respuesta ``200``.

Tabla: Campos de respuesta

.. note::

   ``logged: true`` indica que el clic fue aceptado en la cola de registro de búsqueda. La persistencia se realiza de forma asíncrona.

Respuesta de error
------------------

Consulte :doc:`api-overview` para detalles del modelo de errores. Los estados HTTP que devuelve este endpoint son:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 400 Bad Request
     - El cuerpo de la solicitud no es JSON válido, o ``doc_id`` está ausente o no coincide con el patrón.
   * - 403 Forbidden
     - Cuando no está permitido por ausencia o expiración del token CSRF, entre otros motivos.
   * - 404 Not Found
     - No se encontró ningún documento correspondiente al ``doc_id`` especificado.
   * - 405 Method Not Allowed
     - Se utilizó un método HTTP distinto de ``POST`` (se devuelve una cabecera ``Allow: POST``).
   * - 413 Payload Too Large
     - El cuerpo de la solicitud supera el límite de tamaño (2 KiB).
   * - 415 Unsupported Media Type
     - El ``Content-Type`` no es ``application/json`` (se requiere UTF-8).
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.

Tabla: Respuesta de error
