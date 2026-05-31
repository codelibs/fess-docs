================
API de etiquetas
================

Este documento describe la API de etiquetas v2 de |Fess|.
Para el sobre de respuesta común y el modelo de errores, consulte :doc:`api-overview`.

La URL base es ``http://<Server Name>/api/v2/`` (ejemplo en entorno local: ``http://localhost:8080/api/v2``).

Obtención de etiquetas
======================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v2/labels``
==================  ====================================================

Obtiene la lista de etiquetas configuradas registradas en |Fess| a través del sobre común.

Parámetros de solicitud
-----------------------

No hay parámetros de solicitud disponibles.

Respuesta
---------

En caso de éxito (200), se devuelven los siguientes campos directamente bajo ``response`` del sobre común.

::

    {
      "response": {
        "status": 0,
        "record_count": 2,
        "labels": [
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
    }

Los campos son los siguientes:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Campos de respuesta

   * - ``record_count``
     - Número de etiquetas registradas (integer).
   * - ``labels``
     - Array de etiquetas.
   * - ``label``
     - Nombre de la etiqueta.
   * - ``value``
     - Valor de la etiqueta.

Tabla: Campos de respuesta

Ejemplos de uso
===============

Ejemplo de solicitud usando el comando curl:

::

    curl "http://localhost:8080/api/v2/labels"

Respuesta de error
==================

Consulte :doc:`api-overview` para detalles del modelo de errores. Los estados HTTP que devuelve este endpoint son:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 405 Method Not Allowed
     - Cuando el método HTTP no está permitido.
   * - 500 Internal Server Error
     - Cuando se produce un error interno del servidor.

Tabla: Respuesta de error
