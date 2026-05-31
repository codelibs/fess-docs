================
API de caché
================

Este documento describe la API de caché v2 de |Fess|.
Para el sobre de respuesta común, el modelo de errores y CSRF, consulte :doc:`api-overview`.

La URL base es ``http://<Server Name>/api/v2/`` (ejemplo en entorno local: ``http://localhost:8080/api/v2``).

Obtención de documento en caché
================================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v2/cache/{docId}``
==================  ====================================================

Devuelve el HTML en caché (con resaltado aplicado) del documento.

Cuando ``app.login.required=true`` y el llamante es anónimo, resulta en ``auth_required`` (401).

Parámetros de solicitud
-----------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Parámetros de solicitud

   * - ``docId``
     - Identificador del documento (path, obligatorio, patrón ``^[A-Za-z0-9_-]+$``).
   * - ``hq``
     - Término de consulta para resaltado (query). Se puede repetir (array).

Tabla: Parámetros de solicitud

Respuesta
---------

En caso de éxito (200), se devuelven los siguientes campos directamente bajo ``response`` del sobre común.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "mimetype": "text/html",
        "content": "<html><body>...</body></html>",
        "url": "https://example.com/",
        "created": "2024-05-31T12:00:00.000Z",
        "charset": "UTF-8"
      }
    }

Los campos son los siguientes:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Campos de respuesta

   * - ``doc_id``
     - ID del documento (str).
   * - ``mimetype``
     - Tipo MIME (enum: ``text/html``).
   * - ``content``
     - Contenido HTML en caché (str).
   * - ``url``
     - URL del documento (str). Si existe el campo ``url_link``, se usa ese; de lo contrario, la URL sin procesar del índice. Se omite cuando no hay ninguno.
   * - ``created``
     - Marca de tiempo de creación del documento en el índice (str). Se omite cuando no existe.
   * - ``charset``
     - Juego de caracteres analizado del mimetype del documento (str). Cuando no está disponible, el valor predeterminado es ``UTF-8``.

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
     - Cuando se requiere autenticación (``app.login.required=true`` y llamante anónimo).
   * - 404 Not Found
     - Cuando no se encuentra el recurso.
   * - 405 Method Not Allowed
     - Cuando el método HTTP no está permitido.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.

Tabla: Respuesta de error
