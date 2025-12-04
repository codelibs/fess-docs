==============
API de búsqueda
==============

Obtención de resultados de búsqueda
====================================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v1/documents``
==================  ====================================================

Al enviar una solicitud como
``http://<Server Name>/api/v1/documents?q=término de búsqueda``
a |Fess|, puede recibir los resultados de búsqueda de |Fess| en formato JSON.
Para usar la API de búsqueda, debe habilitar la respuesta JSON en Sistema > Configuración general de la consola de administración.

Parámetros de solicitud
-----------------------

Al especificar parámetros de solicitud como
``http://<Server Name>/api/v1/documents?q=término de búsqueda&num=50&fields.label=fess``,
puede realizar búsquedas más avanzadas.
Los parámetros de solicitud disponibles son los siguientes:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - q
     - Término de búsqueda. Se pasa con codificación URL.
   * - start
     - Posición inicial del número de resultados. Comienza desde 0.
   * - num
     - Número de resultados a mostrar. El valor predeterminado es 20. Se pueden mostrar hasta 100 resultados.
   * - sort
     - Ordenar. Se utiliza para ordenar los resultados de búsqueda.
   * - fields.label
     - Valor de etiqueta. Se utiliza para especificar una etiqueta.
   * - facet.field
     - Especificación de campo de faceta. (Ejemplo) ``facet.field=label``
   * - facet.query
     - Especificación de consulta de faceta. (Ejemplo) ``facet.query=timestamp:[now/d-1d TO *]``
   * - facet.size
     - Especificación del número máximo de facetas a obtener. Es válido cuando se especifica facet.field.
   * - facet.minDocCount
     - Obtiene facetas con un recuento mayor o igual a este valor. Es válido cuando se especifica facet.field.
   * - geo.location.point
     - Especificación de latitud y longitud. (Ejemplo) ``geo.location.point=35.0,139.0``
   * - geo.location.distance
     - Especificación de la distancia desde el punto central. (Ejemplo) ``geo.location.distance=10km``
   * - lang
     - Especificación del idioma de búsqueda. (Ejemplo) ``lang=en``
   * - preference
     - Cadena que especifica el shard al realizar la búsqueda. (Ejemplo) ``preference=abc``
   * - callback
     - Nombre del callback cuando se utiliza JSONP. No es necesario especificarlo si no se utiliza JSONP.

Tabla: Parámetros de solicitud


Respuesta
---------

| Se devuelve una respuesta como la siguiente:
| (Formato embellecido)

::

    {
      "q": "Fess",
      "query_id": "bd60f9579a494dfd8c03db7c8aa905b0",
      "exec_time": 0.21,
      "query_time": 0,
      "page_size": 20,
      "page_number": 1,
      "record_count": 31625,
      "page_count": 1,
      "highlight_params": "&hq=n2sm&hq=Fess",
      "next_page": true,
      "prev_page": false,
      "start_record_number": 1,
      "end_record_number": 20,
      "page_numbers": [
        "1",
        "2",
        "3",
        "4",
        "5"
      ],
      "partial": false,
      "search_query": "(Fess OR n2sm)",
      "requested_time": 1507822131845,
      "related_query": [
        "aaa"
      ],
      "related_contents": [],
      "data": [
        {
          "filetype": "html",
          "title": "Open Source Enterprise Search Server: Fess — Fess 11.0 documentation",
          "content_title": "Open Source Enterprise Search Server: Fess — Fe...",
          "digest": "Docs » Open Source Enterprise Search Server: Fess Commercial Support Open Source Enterprise Search Server: Fess What is Fess ? Fess is very powerful and easily deployable Enterprise Search Server. ...",
          "host": "fess.codelibs.org",
          "last_modified": "2017-10-09T22:28:56.000Z",
          "content_length": "29624",
          "timestamp": "2017-10-09T22:28:56.000Z",
          "url_link": "https://fess.codelibs.org/",
          "created": "2017-10-10T15.40:48.609Z",
          "site_path": "fess.codelibs.org/",
          "doc_id": "e79fbfdfb09d4bffb58ec230c68f6f7e",
          "url": "https://fess.codelibs.org/",
          "content_description": "Enterprise Search Server: <strong>Fess</strong> Commercial Support Open...Search Server: <strong>Fess</strong> What is <strong>Fess</strong> ? <strong>Fess</strong> is very powerful...You can install and run <strong>Fess</strong> quickly on any platforms...Java runtime environment. <strong>Fess</strong> is provided under Apache...Apache license. Demo <strong>Fess</strong> is OpenSearch-based search",
          "site": "fess.codelibs.org/",
          "boost": "10.0",
          "mimetype": "text/html"
        }
      ]
    }

Los elementos son los siguientes:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Información de respuesta

   * - q
     - Término de búsqueda
   * - exec_time
     - Tiempo de respuesta (en segundos)
   * - query_time
     - Tiempo de procesamiento de consulta (en milisegundos)
   * - page_size
     - Número de resultados mostrados
   * - page_number
     - Número de página
   * - record_count
     - Número de resultados encontrados para el término de búsqueda
   * - page_count
     - Número de páginas de resultados encontrados para el término de búsqueda
   * - highlight_params
     - Parámetros de resaltado
   * - next_page
     - true: existe la página siguiente. false: no existe la página siguiente.
   * - prev_page
     - true: existe la página anterior. false: no existe la página anterior.
   * - start_record_number
     - Posición inicial del número de registro
   * - end_record_number
     - Posición final del número de registro
   * - page_numbers
     - Array de números de página
   * - partial
     - Se establece en true cuando los resultados de búsqueda se truncan debido a un tiempo de espera de búsqueda u otros motivos.
   * - search_query
     - Consulta de búsqueda
   * - requested_time
     - Hora de la solicitud (en milisegundos epoch)
   * - related_query
     - Consulta relacionada
   * - related_contents
     - Consulta de contenido relacionado
   * - facet_field
     - Información de documentos que coinciden con el campo de faceta dado (solo cuando se proporciona ``facet.field`` en los parámetros de solicitud)
   * - facet_query
     - Número de documentos que coinciden con la consulta de faceta dada (solo cuando se proporciona ``facet.query`` en los parámetros de solicitud)
   * - result
     - Elemento principal de resultados de búsqueda
   * - filetype
     - Tipo de archivo
   * - created
     - Fecha y hora de creación del documento
   * - title
     - Título del documento
   * - doc_id
     - ID del documento
   * - url
     - URL del documento
   * - site
     - Nombre del sitio
   * - content_description
     - Descripción del contenido
   * - host
     - Nombre del host
   * - digest
     - Cadena de resumen del documento
   * - boost
     - Valor de impulso del documento
   * - mimetype
     - Tipo MIME
   * - last_modified
     - Fecha y hora de última modificación
   * - content_length
     - Tamaño del documento
   * - url_link
     - URL como resultado de búsqueda
   * - timestamp
     - Fecha y hora de actualización del documento


Búsqueda de todos los documentos
=================================

Para buscar todos los documentos objetivo, envíe la siguiente solicitud:
``http://<Server Name>/api/v1/documents/all?q=término de búsqueda``

Para usar esta funcionalidad, debe establecer api.search.scroll en true en fess_config.properties.

Parámetros de solicitud
-----------------------

Los parámetros de solicitud disponibles son los siguientes:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - q
     - Término de búsqueda. Se pasa con codificación URL.
   * - num
     - Número de resultados a mostrar. El valor predeterminado es 20. Se pueden mostrar hasta 100 resultados.
   * - sort
     - Ordenar. Se utiliza para ordenar los resultados de búsqueda.

Tabla: Parámetros de solicitud

Respuesta de error
==================

Si la API de búsqueda falla, se devuelve una respuesta de error como la siguiente:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 400 Bad Request
     - Cuando los parámetros de solicitud son incorrectos
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor

Ejemplo de respuesta de error:

::

    {
      "message": "Invalid request parameter",
      "status": 400
    }
