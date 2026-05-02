========================
API de palabras populares
========================

Obtención de lista de palabras populares
=========================================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v1/popular-words``
==================  ====================================================

Al enviar una solicitud como ``http://<Server Name>/api/v1/popular-words?seed=123`` a |Fess|, puede recibir una lista de las palabras populares registradas en |Fess| en formato JSON.
Para usar la API de palabras populares, debe habilitar la respuesta de palabras populares en Sistema > Configuración general de la consola de administración.

Parámetros de solicitud
-----------------------

Los parámetros de solicitud disponibles son los siguientes:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Parámetros de solicitud

   * - seed
     - Semilla para obtener palabras populares (este valor permite obtener diferentes patrones de palabras)
   * - label
     - Nombre de etiqueta filtrada
   * - field
     - Nombre de campo para generar palabras populares


Respuesta
---------

Se devuelve una respuesta como la siguiente:

::

    {
      "record_count": 3,
      "data": [
        "python",
        "java",
        "javascript"
      ]
    }

Los elementos son los siguientes:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Información de respuesta

   * - record_count
     - Número de palabras populares registradas
   * - data
     - Array de palabras populares

Respuesta de error
==================

Si la API de palabras populares falla, se devuelve una respuesta de error como la siguiente:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 400 Bad Request
     - Cuando los parámetros de solicitud son incorrectos
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor
