============================================
API de exportación de resultados de búsqueda
============================================

Este documento describe la API de exportación v2 de |Fess|, que descarga los resultados de búsqueda
como un archivo CSV o JSON. Para el sobre de respuesta común y el modelo de errores, consulte
:doc:`api-overview`.

La URL base es ``http://<Server Name>/api/v2/`` (ejemplo en entorno local: ``http://localhost:8080/api/v2``).

.. note::

   La exportación está deshabilitada de forma predeterminada. Para usarla, configure
   ``api.search.export=true`` en ``fess_config.properties``. Cuando está habilitada, el tema incluido
   ``bootstrap`` muestra un menú de exportación (CSV / JSON) junto al número de resultados.
   ``features.search_export`` de ``/api/v2/ui/config`` indica el estado.

Descargar los resultados de búsqueda
====================================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v2/documents/export``
==================  ====================================================

Devuelve los documentos que coinciden con la búsqueda como una descarga de archivo
(``Content-Disposition: attachment``, con el nombre ``search_results.csv`` o ``search_results.json``).

- Se aplica el mismo filtro de roles que en ``/api/v2/search``. Con ``login.required=true``, se puede
  usar un token de acceso igual que con ``/api/v2/search``.
- Se exportan como máximo ``api.search.export.max.size`` (predeterminado: ``1000``) documentos. Los
  parámetros de paginación (``start``, ``num``) no se usan.
- Se exportan los campos de ``api.search.export.fields`` (predeterminado:
  ``title,url_link,last_modified,content_length,filetype``) que también pueden aparecer en las
  respuestas de la API.
- Las solicitudes se limitan a ``api.search.export.rate.limit.per.minute`` (predeterminado: ``10``;
  ``0`` significa sin límite) por minuto, contadas por usuario con sesión iniciada o, para un
  invitado, por IP de cliente. Por encima del límite, el endpoint responde ``429`` con una cabecera
  ``Retry-After``.
- Una exportación no se registra en el registro de búsqueda.

Parámetros de solicitud
-----------------------

Se pueden indicar los mismos parámetros de condición de búsqueda que en ``/api/v2/documents/all``,
como ``q``, ``ex_q``, ``fields.*``, ``sort`` y ``lang`` (consulte :doc:`api-search`). Además:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Parámetros de solicitud

   * - ``format``
     - Formato del archivo: ``csv`` (predeterminado) o ``json``. Cualquier otro valor produce ``invalid_request`` (400).

Tabla: Parámetros de solicitud

Respuesta
---------

El archivo CSV tiene una fila de encabezado con los nombres de los campos y se escribe con la
codificación de ``csv.file.encoding`` (un archivo UTF-8 empieza con una marca de orden de bytes). Un
valor que empieza por ``=``, ``+``, ``-``, ``@``, un tabulador o un retorno de carro recibe un ``'``
inicial para que una hoja de cálculo no lo ejecute como fórmula. Un campo con varios valores se une
con un espacio.

::

    "title","url_link","last_modified","content_length","filetype"
    "Example","https://example.com/","2025-01-01T00:00:00.000Z","1234","html"

El archivo JSON tiene la forma ``{"data":[{...},...]}`` y los campos con varios valores siguen siendo
arrays.

Un fallo antes de que empiece el archivo devuelve el sobre de error habitual. Un fallo posterior no se
puede indicar en el archivo, por lo que la descarga termina antes de tiempo: un CSV truncado o un
JSON que no se puede analizar.

Respuesta de error
------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 400 Bad Request
     - Una consulta mal formada, un ``format`` distinto de ``csv`` / ``json``, o la exportación
       deshabilitada con ``api.search.export=false``.
   * - 401 Unauthorized
     - Cuando se requiere autenticación (por ejemplo, una llamada anónima con ``login.required=true``).
   * - 405 Method Not Allowed
     - Cuando el método HTTP no está permitido.
   * - 429 Too Many Requests
     - Cuando se supera el límite de solicitudes por minuto.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.

Tabla: Respuesta de error
