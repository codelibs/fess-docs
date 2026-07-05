================
API de búsqueda
================

Este documento describe la API de búsqueda v2 de |Fess|.
Para el sobre de respuesta común, el modelo de errores y CSRF, consulte :doc:`api-overview`.

La URL base es ``http://<Server Name>/api/v2/`` (ejemplo en entorno local: ``http://localhost:8080/api/v2``).

Búsqueda de documentos
======================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v2/search``
==================  ====================================================

Busca documentos que coincidan con la consulta y devuelve los resultados en el sobre común.
Todos los nombres de campo del payload usan ``snake_case``.

Parámetros de solicitud
~~~~~~~~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Parámetros de solicitud

   * - ``q``
     - Término de búsqueda (codificado en URL).
   * - ``start``
     - Posición de inicio desde 0 (integer, ``>=0``, valor predeterminado ``0``).
   * - ``offset``
     - Desplazamiento desde ``start`` (integer, ``>=0``, valor predeterminado ``0``).
   * - ``num``
     - Tamaño de página (integer, ``>=1``, valor predeterminado ``10``). ``<= 0`` resulta en ``invalid_request``. Los valores que superen el máximo configurado se ajustan silenciosamente. El ajuste puede detectarse comparando ``num`` en la solicitud con ``page_size`` en la respuesta.
   * - ``sort``
     - Ordenación (ejemplo: ``score``).
   * - ``lang``
     - Idioma de búsqueda. Se puede repetir (array). Ejemplo: ``en``.
   * - ``ex_q``
     - Expresión de consulta adicional. Se puede repetir.
   * - ``sdh``
     - Hash de documentos similares (similar-document hash).
   * - ``fields.label``
     - Filtra por nombre de etiqueta. Se puede repetir. Este es el caso más común de la familia genérica ``fields.<name>``: cualquier parámetro de consulta ``fields.<name>`` limita los resultados a documentos donde el campo ``<name>`` coincide con el valor especificado.
   * - ``as.*``
     - Condiciones de búsqueda avanzada. Cualquier ``as.<name>`` (ejemplo: ``as.q``, ``as.filetype``) se pasa al constructor de condiciones de búsqueda avanzada. Se puede repetir por nombre.
   * - ``track_total_hits``
     - Se reenvía al motor de búsqueda para controlar el recuento exacto de resultados (ejemplo: ``true`` o un umbral entero). Afecta si ``record_count_relation`` es ``eq`` o ``gte``.
   * - ``facet.field``
     - Campo de faceta. Se puede repetir (array).
   * - ``facet.query``
     - Consulta de faceta. Se puede repetir (array).
   * - ``facet.size``
     - Número máximo de términos de faceta a devolver (integer).
   * - ``facet.minDocCount``
     - Número mínimo de documentos que debe contener un término de faceta (integer).
   * - ``facet.sort``
     - Ordenación de facetas.
   * - ``facet.missing``
     - Tratamiento de facetas para documentos sin valor.
   * - ``geo.location.point``
     - Punto central de coordenadas geográficas (ejemplo: ``35.0,139.0``).
   * - ``geo.location.distance``
     - Distancia desde el punto central (ejemplo: ``10km``).

Tabla: Parámetros de solicitud

Respuesta
---------

En caso de éxito (200), se devuelven los siguientes campos directamente bajo ``response`` del sobre común.

::

    {
      "response": {
        "status": 0,
        "q": "Fess",
        "query_id": "f8b1c2d3e4a5",
        "exec_time": 0.012,
        "query_time": 8,
        "page_size": 20,
        "page_number": 1,
        "record_count": 42,
        "record_count_relation": "eq",
        "page_count": 3,
        "highlight_params": "&hq=Fess",
        "next_page": true,
        "prev_page": false,
        "start_record_number": 1,
        "end_record_number": 20,
        "page_numbers": ["1", "2", "3"],
        "partial": false,
        "search_query": "title:Fess OR content:Fess",
        "requested_time": 1717142400000,
        "related_query": ["enterprise search"],
        "related_contents": [],
        "data": [
          {
            "doc_id": "a1b2c3d4e5f6",
            "url": "https://example.com/",
            "title": "Example",
            "content_description": "An example document about Fess.",
            "score": 1.2345
          }
        ],
        "facet_field": [
          {
            "name": "label",
            "result": [
              { "value": "news", "count": 12 }
            ]
          }
        ],
        "facet_query": [
          { "value": "filetype:html", "count": 30 }
        ]
      }
    }

Los campos son los siguientes:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Campos de respuesta

   * - ``q``
     - Término de búsqueda (nullable).
   * - ``query_id``
     - Identificador de la consulta.
   * - ``exec_time``
     - Tiempo de ejecución (double, en segundos).
   * - ``query_time``
     - Tiempo de consulta del motor de búsqueda (int64, en milisegundos).
   * - ``page_size``
     - Tamaño de página.
   * - ``page_number``
     - Número de página actual.
   * - ``record_count``
     - Número de resultados encontrados (int64).
   * - ``record_count_relation``
     - Cuando es ``eq``, indica un recuento exacto; cuando es ``gte``, indica que solo se conoce el límite inferior.
   * - ``page_count``
     - Número total de páginas.
   * - ``highlight_params``
     - Cadena de parámetros de consulta para resaltado.
   * - ``next_page``
     - Si existe página siguiente (bool).
   * - ``prev_page``
     - Si existe página anterior (bool).
   * - ``start_record_number``
     - Número de registro de inicio de esta página.
   * - ``end_record_number``
     - Número de registro de fin de esta página.
   * - ``page_numbers``
     - Array de números de página para mostrar en el paginador (cadenas de texto).
   * - ``partial``
     - Si los resultados son parciales (bool).
   * - ``search_query``
     - La consulta de búsqueda que se ejecutó realmente.
   * - ``requested_time``
     - Hora de la solicitud (int64, epoch en milisegundos).
   * - ``related_query``
     - Array de consultas relacionadas (cadenas de texto).
   * - ``related_contents``
     - Array de contenidos relacionados (cadenas de texto).
   * - ``data``
     - Array de resultados de búsqueda. Un elemento por documento. Solo se incluyen los campos permitidos por ``QueryFieldConfig#isApiResponseField``; se excluyen los nulos y las claves vacías.
   * - ``facet_field``
     - Array que solo existe cuando se solicitaron campos de faceta. Cada elemento tiene la forma ``{name, result:[{value, count}]}``.
   * - ``facet_query``
     - Array que solo existe cuando se solicitaron consultas de faceta. Cada elemento tiene la forma ``{value, count}``.

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
   * - 405 Method Not Allowed
     - Cuando el método HTTP no está permitido.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.

Tabla: Respuesta de error

Obtención de todos los documentos (búsqueda por scroll - NDJSON)
================================================================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v2/documents/all``
==================  ====================================================

Transmite en streaming todos los documentos que coincidan con la consulta en formato NDJSON (``application/x-ndjson``).
Cada línea es un objeto ``{"data":{...}}`` que contiene los campos permitidos por ``QueryFieldConfig#isApiResponseField``.

Si se produce un fallo a mitad del stream, se envía y vacía la siguiente línea como línea final:

::

    {"error":{"code":"internal_error","message":"stream error"}}

Por este motivo, el cliente debe verificar la primera clave de la última línea para distinguir entre una finalización normal (``data``) y un error del servidor (``error``).

La consulta se construye con el mismo conjunto de parámetros que ``GET /search`` (``q``, ``sort``, ``num``, ``lang``, ``ex_q``, ``sdh``, ``fields.*``, ``as.*``, ``track_total_hits``, ``facet.*``, ``geo.*``).
Cuando la búsqueda por scroll está deshabilitada con ``api.search.scroll=false``, se devuelve ``invalid_request`` (400).

Parámetros de solicitud
~~~~~~~~~~~~~~~~~~~~~~~

Los parámetros especificados explícitamente en la especificación son los siguientes:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Parámetros de solicitud

   * - ``q``
     - Término de búsqueda.
   * - ``sort``
     - Ordenación.
   * - ``num``
     - Tamaño de página (lote de scroll) (integer, ``>=1``). ``<= 0`` resulta en ``invalid_request``.
   * - ``lang``
     - Idioma de búsqueda. Se puede repetir (array).
   * - ``ex_q``
     - Expresión de consulta adicional. Se puede repetir (array).
   * - ``fields.label``
     - Filtra por nombre de etiqueta. Se puede repetir (array). Forma parte de la familia genérica ``fields.<name>`` (consulte ``GET /search``).
   * - ``sdh``
     - Hash de documentos similares (similar-document hash).

Tabla: Parámetros de solicitud

Respuesta
---------

En caso de éxito (200), el Content-Type es ``application/x-ndjson`` y se devuelve un documento por línea de la siguiente forma:

::

    {"data":{"url":"https://example.com/","title":"Example"}}
    {"data":{"url":"https://example.org/","title":"Example Org"}}

Respuesta de error
------------------

Consulte :doc:`api-overview` para detalles del modelo de errores. Los estados HTTP que devuelve este endpoint son:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 400 Bad Request
     - Consulta inválida, ``num <= 0``, o búsqueda por scroll deshabilitada con ``api.search.scroll=false``.
   * - 405 Method Not Allowed
     - Cuando el método HTTP no está permitido.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.

Tabla: Respuesta de error
