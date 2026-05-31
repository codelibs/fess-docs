==================
API de sugerencias
==================

Obtención de lista de palabras sugeridas
=========================================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v2/suggest-words``
==================  ====================================================

Al enviar a |Fess| una solicitud como ``http://<Server Name>/api/v2/suggest-words?q=fes``, puede recibir en formato JSON una lista de palabras sugeridas para el prefijo introducido.
Para utilizar la API de sugerencias, debe habilitar "Sugerir desde documentos" o "Sugerir desde palabras de búsqueda" en Sistema > Configuración general de la consola de administración.

Para el sobre de respuesta común y el modelo de errores, consulte :doc:`api-overview`.

Parámetros de solicitud
-----------------------

Los parámetros de solicitud disponibles son los siguientes:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Parámetros de solicitud

   * - q
     - Término de búsqueda (prefijo) para realizar sugerencias. (Ejemplo) ``q=fes``
   * - num
     - Número de palabras sugeridas (entero mayor o igual a 0). Predeterminado ``10``. (Ejemplo) ``num=20``
   * - fn
     - Nombre de campo para filtrar el objetivo de sugerencia. Se puede repetir para tratarlo como un array. (Ejemplo) ``fn=content&fn=title``
   * - lang
     - Idioma de búsqueda. Se puede repetir para tratarlo como un array. (Ejemplo) ``lang=en``
   * - label
     - Nombre de etiqueta para filtrar. Se puede repetir para tratarlo como un array. (Ejemplo) ``label=java``

.. note::

   En v2, el parámetro para especificar nombres de campo es ``fn`` (no ``fields`` como en v1).
   Asimismo, el parámetro para especificar etiquetas es ``label`` (distinto del parámetro ``labels`` de v1).

Respuesta
---------

En caso de éxito, se devuelve una respuesta con el formato de sobre común como la siguiente:

::

    {
      "response": {
        "status": 0,
        "q": "fes",
        "page_size": 10,
        "record_count": 355,
        "query_time": 18,
        "suggest_words": [
          {
            "text": "fess",
            "types": [
              "document",
              "query"
            ]
          }
        ]
      }
    }

Los elementos de ``response`` son los siguientes:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Información de respuesta

   * - q
     - Término de búsqueda solicitado (cadena de texto).
   * - page_size
     - Tamaño de página (entero).
   * - record_count
     - Número de palabras sugeridas encontradas (entero de 64 bits).
   * - query_time
     - Tiempo de procesamiento de consulta. Unidad: milisegundos (entero de 64 bits).
   * - suggest_words
     - Array de palabras sugeridas. Cada elemento tiene ``text`` y ``types``.
   * - text
     - Palabra sugerida (cadena de texto).
   * - types
     - Array de tipos de la palabra sugerida (array de cadenas de texto).

.. note::

   En v2, los campos del elemento de sugerencia son ``text`` y ``types`` (no ``labels`` como en v1).

Ejemplos de uso
===============

Ejemplo de solicitud usando el comando curl:

::

    curl "http://localhost:8080/api/v2/suggest-words?q=fes"

Respuesta de error
==================

Si la API de sugerencias falla, se devuelve el sobre de error común. Consulte :doc:`api-overview` para detalles del modelo de errores.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 405 Method Not Allowed
     - Cuando se especifica un método HTTP no admitido.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.
