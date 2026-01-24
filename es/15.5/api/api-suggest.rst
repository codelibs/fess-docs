==================
API de sugerencias
==================

Obtención de lista de palabras sugeridas
=========================================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v1/suggest-words``
==================  ====================================================

Al enviar una solicitud como ``http://<Server Name>/api/v1/suggest-words?q=palabra sugerida`` a |Fess|, puede recibir una lista de las palabras sugeridas registradas en |Fess| en formato JSON.
Para usar la API de palabras sugeridas, debe habilitar "Sugerir desde documentos" o "Sugerir desde palabras de búsqueda" en Sistema > Configuración general de la consola de administración.

Parámetros de solicitud
-----------------------

Los parámetros de solicitud disponibles son los siguientes:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Parámetros de solicitud

   * - q
     - Palabra clave para realizar sugerencias. (Ejemplo) ``q=fess``
   * - num
     - Número de palabras sugeridas. Predeterminado 10. (Ejemplo) ``num=20``
   * - label
     - Nombre de etiqueta filtrada. (Ejemplo) ``label=java``
   * - fields
     - Nombre de campo para filtrar el objetivo de sugerencia. Sin filtro predeterminado. (Ejemplo) ``fields=content,title``
   * - lang
     - Especificación del idioma de búsqueda. (Ejemplo) ``lang=en``


Respuesta
---------

Se devuelve una respuesta como la siguiente:

::

    {
      "query_time": 18,
      "record_count": 355,
      "page_size": 10,
      "data": [
        {
          "text": "fess",
          "labels": [
            "java",
            "python"
          ]
        }
      ]
    }

Los elementos son los siguientes:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Información de respuesta

   * - query_time
     - Tiempo de procesamiento de consulta (en milisegundos).
   * - record_count
     - Número de palabras sugeridas registradas.
   * - page_size
     - Tamaño de página.
   * - data
     - Elemento principal de resultados de búsqueda.
   * - text
     - Palabra sugerida.
   * - labels
     - Array de valores de etiquetas.

Respuesta de error
==================

Si la API de sugerencias falla, se devuelve una respuesta de error como la siguiente:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 400 Bad Request
     - Cuando los parámetros de solicitud son incorrectos
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor
