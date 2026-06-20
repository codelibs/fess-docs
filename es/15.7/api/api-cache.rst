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

Devuelve el HTML en caché de un documento tal como fue almacenado en el momento del rastreo. Cuando se especifica ``hq``, los términos coincidentes se resaltan.

Este endpoint aplica el mismo filtrado de permisos (roles) que la búsqueda. Un documento al que los roles del llamante no tienen acceso devuelve ``not_found`` (404), como si no existiera.

Cuando la configuracion de inicio de sesion obligatorio (la opcion "Inicio de sesion obligatorio" de la configuracion del sistema) esta habilitada y el llamante es anonimo, resulta en ``auth_required`` (401).

Parámetros de solicitud
-----------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Parámetros de solicitud

   * - ``docId``
     - Identificador del documento (path, obligatorio, patrón ``^[A-Za-z0-9_-]+$``).
   * - ``hq``
     - Término a resaltar (query). Cuando se especifica, los términos coincidentes en el HTML en caché se envuelven con etiquetas de resaltado. Se puede especificar varias veces para pasar múltiples términos (array).

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
     - Tipo MIME del cuerpo de la respuesta (str). Siempre fijo a ``text/html``.
   * - ``content``
     - Contenido HTML en caché (str). Cuando se especifica ``hq``, los términos coincidentes se resaltan.
   * - ``url``
     - URL del documento (str). Devuelve el valor del campo ``url_link`` si está presente; de lo contrario, el valor del campo ``url`` del índice. Se omite cuando no hay ninguno.
   * - ``created``
     - Marca de tiempo de creación del documento (str, formato ISO 8601, p. ej. ``2024-05-31T12:00:00.000Z``). Se omite cuando el índice no tiene valor.
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
     - Cuando se requiere autenticación (la configuracion de inicio de sesion obligatorio esta habilitada y el llamante es anonimo).
   * - 404 Not Found
     - El documento no existe, no tiene contenido en caché, o no es accesible con los permisos del llamante.
   * - 405 Method Not Allowed
     - Cuando el método HTTP no está permitido.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.

Tabla: Respuesta de error
