===========
API de salud
===========

Obtención del estado
=====================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v1/health``
==================  ====================================================

Al enviar una solicitud como ``http://<Server Name>/api/v1/health`` a |Fess|, puede recibir el estado del servidor de |Fess| en formato JSON.

Parámetros de solicitud
-----------------------

No se pueden especificar parámetros de solicitud.

Respuesta
---------

Se devuelve una respuesta como la siguiente:

::

    {
      "data": {
        "status": "green",
        "timed_out": false
      }
    }

Los elementos son los siguientes:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Información de respuesta

   * - data
     - Elemento principal de resultados de búsqueda.
   * - status
     - Estado del sistema. Se devuelve ``green`` si es normal, ``yellow`` si hay advertencias, ``red`` si hay errores.
   * - timed_out
     - Presencia de tiempo de espera. Se devuelve ``false`` si la respuesta se devolvió dentro del tiempo especificado, ``true`` si se agotó el tiempo de espera.

Respuesta de error
==================

Si la API de salud falla, se devuelve una respuesta de error como la siguiente:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor
