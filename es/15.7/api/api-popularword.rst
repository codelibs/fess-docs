=========================
API de palabras populares
=========================

Obtención de lista de palabras populares
=========================================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v2/popular-words``
==================  ====================================================

Al enviar a |Fess| una solicitud como ``http://<Server Name>/api/v2/popular-words?seed=123``, puede recibir en formato JSON una lista de palabras de búsqueda populares.

Cuando ``web.api.popular.word=false``, esta API devuelve ``invalid_request`` (HTTP 400) (comportamiento equivalente a "unsupported operation" de v1).

Para el sobre de respuesta común y el modelo de errores, consulte :doc:`api-overview`.

Parámetros de solicitud
-----------------------

Los parámetros de solicitud disponibles son los siguientes:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Parámetros de solicitud

   * - seed
     - Semilla para obtener palabras populares (cadena de texto). Este valor permite obtener diferentes patrones de palabras. (Ejemplo) ``seed=123``
   * - label
     - Nombre de etiqueta para filtrar. Se puede repetir para tratarlo como un array. (Ejemplo) ``label=java``
   * - field
     - Nombre de campo para generar palabras populares. Se puede repetir para tratarlo como un array. (Ejemplo) ``field=label``

Respuesta
---------

En caso de éxito, se devuelve una respuesta con el formato de sobre común como la siguiente:

::

    {
      "response": {
        "status": 0,
        "record_count": 3,
        "popular_words": [
          "python",
          "java",
          "javascript"
        ]
      }
    }

Los elementos de ``response`` son los siguientes:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Información de respuesta

   * - record_count
     - Número de palabras populares (entero).
   * - popular_words
     - Array de palabras populares (array de cadenas de texto).

.. note::

   En v2, las palabras populares se devuelven como ``popular_words`` (array de cadenas de texto), no como ``data`` como en v1.

Ejemplos de uso
===============

Ejemplo de solicitud usando el comando curl:

::

    curl "http://localhost:8080/api/v2/popular-words?seed=123"

Respuesta de error
==================

Si la API de palabras populares falla, se devuelve el sobre de error común. Consulte :doc:`api-overview` para detalles del modelo de errores.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 400 Bad Request
     - Cuando la solicitud no es válida (incluye el caso en que la funcionalidad está deshabilitada con ``web.api.popular.word=false``). El ``error.code`` es ``invalid_request``.
   * - 405 Method Not Allowed
     - Cuando se especifica un método HTTP no admitido.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.
