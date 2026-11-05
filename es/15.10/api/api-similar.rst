===========================
API de documentos similares
===========================

Este documento describe la API v2 de documentos similares de |Fess|, que lista los documentos que tienen el mismo contenido que un documento dado. Para el sobre de respuesta común y el modelo de errores, consulte :doc:`api-overview`.

La URL base es ``http://<Server Name>/api/v2/`` (ejemplo en entorno local: ``http://localhost:8080/api/v2``).

.. note::

   Esta API encuentra copias y documentos casi idénticos. No encuentra documentos que simplemente traten el mismo tema (consulte "Qué documentos se devuelven" más abajo).

Obtener documentos similares
============================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v2/documents/{docId}/similar``
==================  ====================================================

Devuelve los documentos que tienen la misma firma de contenido que el documento ``docId``, de modo que un cliente pueda ofrecer un enlace de "documentos similares" junto a un resultado.

- Al documento dado y a los documentos devueltos se les aplican el mismo filtro de roles, el mismo filtro de host virtual y la misma consulta adicional que en ``/api/v2/search``. Un documento que no existe y un documento que el llamante no puede ver devuelven ambos ``not_found`` (404). El propio documento dado y cualquier otro documento con la misma URL nunca se devuelven.
- Con ``login.required=true``, un llamante anónimo recibe ``auth_required`` (401). Un token de acceso se puede usar igual que con ``/api/v2/search``.
- Las solicitudes están limitadas a ``api.search.similar.rate.limit.per.minute`` (predeterminado: ``30``; ``0`` significa sin límite) por minuto, contadas por usuario con sesión iniciada o por IP de cliente en el caso de un invitado. Al superar el límite, el endpoint responde ``429`` con una cabecera ``Retry-After``.
- Solo se devuelve una página, ordenada por URL y después por ID de documento. No hay parámetro ``start`` ni desplazamiento.

Qué documentos se devuelven
---------------------------

|Fess| calcula una firma de contenido (``content_minhash_bits``) para cada documento al indexarlo. La API devuelve los documentos cuya firma es igual a la del documento dado. Es la misma agrupación que usan el informe de duplicados (:doc:`../admin/docreport-guide`), el parámetro de búsqueda ``sdh`` y los campos ``similar_docs_*``, pero funciona sin agrupar los resultados.

- Los documentos devueltos son copias o tienen casi el mismo contenido. Un documento cuyo contenido se editó lo suficiente como para cambiar la firma no se devuelve, por lo que no es una búsqueda de documentos sobre un tema parecido.
- ``data`` es una matriz vacía (no un error) cuando el documento dado no tiene contenido o ninguna palabra, y cuando el motor de búsqueda funciona sin los plugins de CodeLibs (``search_engine.type`` con ``vanilla``, ``aws`` o el obsoleto ``cloud``; consulte :doc:`../config/search-engine-type`).

Parámetros de solicitud
-----------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Parámetros de solicitud
   :widths: 27 73
   :header-rows: 1

   * - Parámetro
     - Descripción
   * - ``docId``
     - Identificador del documento (ruta, obligatorio, patrón ``[A-Za-z0-9_-]{1,512}``). Un valor que no coincide produce ``invalid_request`` (400).
   * - ``num``
     - Número de documentos que se devuelven (consulta, ``10`` de forma predeterminada). Un valor superior a ``20`` o a ``paging.search.page.max.size`` se reduce al menor de los dos, y ``page_size`` en la respuesta muestra el resultado. Un valor de ``0`` o menos produce ``invalid_request`` (400). Un valor que no es un número se ignora y se usa el valor predeterminado.

Tabla: Parámetros de solicitud

Respuesta
---------

En caso de éxito (200), los siguientes campos se devuelven directamente bajo ``response`` en el sobre común.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "exec_time": "0.01",
        "query_time": 5,
        "page_size": 10,
        "record_count": 1,
        "record_count_relation": "EQUAL_TO",
        "partial": false,
        "timed_out": false,
        "shard_failed": false,
        "data": [
          {
            "doc_id": "f6e5d4c3b2a1",
            "url": "https://example.com/copy/",
            "title": "Example",
            "content_description": "An example document about Fess."
          }
        ]
      }
    }

Cada campo se describe a continuación.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Campos de la respuesta
   :widths: 27 73
   :header-rows: 1

   * - Campo
     - Descripción
   * - ``doc_id``
     - ID del documento dado.
   * - ``exec_time``
     - Tiempo de ejecución en segundos (una cadena decimal como ``"0.01"``).
   * - ``query_time``
     - Tiempo de consulta del motor de búsqueda (int64, milisegundos).
   * - ``page_size``
     - Número de documentos solicitados, tras aplicar el límite descrito arriba.
   * - ``record_count``
     - Número de documentos que tienen la misma firma, no solo los de ``data``. El recuento exacto solo se registra hasta ``query.track.total.hits`` (predeterminado: ``10000``).
   * - ``record_count_relation``
     - Con ``EQUAL_TO``, el recuento es exacto; con ``GREATER_THAN_OR_EQUAL_TO``, solo se conoce el límite inferior.
   * - ``partial``
     - Indica si el resultado puede estar incompleto (bool). Se aplica el tiempo de espera de consulta (``query.timeout``), como en una búsqueda.
   * - ``timed_out``
     - Indica si se agotó el tiempo de espera de la consulta (bool).
   * - ``shard_failed``
     - Indica si fallaron uno o más shards (bool).
   * - ``data``
     - Matriz de documentos, ordenada por URL y después por ID de documento. Cada elemento tiene los mismos campos que un resultado de ``/api/v2/search`` (consulte :doc:`api-search`), incluido ``tags`` (las etiquetas visibles para el llamante, consulte :doc:`api-tag`). No hay consulta que resaltar, por lo que ``content_description`` es el resumen del contenido, y no hay ``score``.

Tabla: Campos de la respuesta

Respuesta de error
------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error
   :widths: 25 75
   :header-rows: 1

   * - Código de estado
     - Descripción
   * - 400 Bad Request
     - ``docId`` no coincide con el patrón, o ``num`` es ``0`` o menor.
   * - 401 Unauthorized
     - Se requiere autenticación (la opción de inicio de sesión obligatorio está habilitada y el llamante es anónimo, o la solicitud lleva un token de acceso no registrado o caducado).
   * - 404 Not Found
     - El documento dado no existe o no es visible para el llamante (``not_found``).
   * - 405 Method Not Allowed
     - El método HTTP no está permitido.
   * - 429 Too Many Requests
     - Se superó el límite de solicitudes por minuto. Una cabecera ``Retry-After`` indica los segundos que hay que esperar (``60``).
   * - 500 Internal Server Error
     - Se produjo un error interno del servidor.
   * - 503 Service Unavailable
     - El motor de búsqueda no pudo atender la solicitud: no está accesible o la rechazó por falta de capacidad. ``error.code`` es ``service_unavailable`` y una cabecera ``Retry-After`` indica los segundos que hay que esperar (``5``). La solicitud en sí es correcta, así que reintente tras una breve espera.

Tabla: Respuesta de error
