================
API de etiquetas
================

Obtención de etiquetas
======================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v1/labels``
==================  ====================================================

Al enviar una solicitud como ``http://<Server Name>/api/v1/labels`` a |Fess|, puede recibir una lista de las etiquetas registradas en |Fess| en formato JSON.

Parámetros de solicitud
-----------------------

No hay parámetros de solicitud disponibles.


Respuesta
---------

Se devuelve una respuesta como la siguiente:

::

    {
      "record_count": 9,
      "data": [
        {
          "label": "AWS",
          "value": "aws"
        },
        {
          "label": "Azure",
          "value": "azure"
        }
      ]
    }

Los elementos son los siguientes:

.. tabularcolumns:: |p{3cm}|p{12cm}|

.. list-table::

   * - record_count
     - Número de etiquetas registradas.
   * - data
     - Elemento principal de resultados de búsqueda.
   * - label
     - Nombre de la etiqueta.
   * - value
     - Valor de la etiqueta.

Tabla: Información de respuesta

Ejemplos de uso
===============

Ejemplo de solicitud usando el comando curl:

::

    curl "http://localhost:8080/api/v1/labels"

Ejemplo de solicitud usando JavaScript:

::

    fetch('http://localhost:8080/api/v1/labels')
      .then(response => response.json())
      .then(data => {
        console.log('Lista de etiquetas:', data.data);
      });

Respuesta de error
==================

Si la API de etiquetas falla, se devuelve una respuesta de error como la siguiente:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor
