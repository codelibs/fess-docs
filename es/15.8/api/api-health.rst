===========
Health API
===========

Este documento describe la API Health v2 de |Fess|.
Para el sobre de respuesta común y el modelo de errores, consulte :doc:`api-overview`.

La URL base es ``http://<Server Name>/api/v2/`` (ejemplo en entorno local: ``http://localhost:8080/api/v2``).

Obtención del estado
====================

Solicitud
---------

==================  ====================================================
Método HTTP         GET
Endpoint            ``/api/v2/health``
==================  ====================================================

Devuelve una instantánea del estado del clúster del motor de búsqueda (etiqueta ``monitor``).
El estado HTTP es 200 cuando el estado del clúster es ``green`` o ``yellow``, y 503 cuando es ``red``.

Este endpoint respeta la invariante del sobre: "``status >= 1`` ⇔ estado HTTP ``>= 400``".

- En caso de ``green`` o ``yellow``: devuelve el sobre de éxito (``status: 0``) con ``engine``.
- En caso de ``red``: devuelve el sobre de error (``status: 9``, ``error.code: service_unavailable``) e incorpora la instantánea del motor bajo ``error.details.engine`` (para que las herramientas de monitoreo puedan analizar los metadatos del clúster).

Los campos de ``engine`` son los siguientes:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Campos de engine

   * - ``cluster_name``
     - Nombre del clúster (str).
   * - ``status``
     - Estado del clúster. Uno de ``green`` / ``yellow`` / ``red``.
   * - ``ping_status``
     - Estado del ping (int). Es ``1`` cuando el clúster está en ``red``, y ``0`` en caso contrario (``green`` / ``yellow``).

Tabla: Campos de engine

Parámetros de solicitud
-----------------------

No hay parámetros de solicitud disponibles.

Respuesta
---------

Cuando el clúster está en estado ``green`` o ``yellow`` (200), se devuelve el sobre de éxito con ``engine``.

::

    {
      "response": {
        "status": 0,
        "engine": {
          "cluster_name": "fess-es",
          "status": "green",
          "ping_status": 0
        }
      }
    }

Cuando el clúster está en estado ``red`` (503), se devuelve el sobre de error y la instantánea del motor se incorpora bajo ``error.details.engine``.

::

    {
      "response": {
        "status": 9,
        "error": {
          "code": "service_unavailable",
          "message": "search engine cluster is red",
          "details": {
            "engine": {
              "cluster_name": "fess-es",
              "status": "red",
              "ping_status": 1
            }
          }
        }
      }
    }

Ejemplos de uso
===============

Ejemplo de solicitud usando el comando curl:

::

    curl "http://localhost:8080/api/v2/health"

Respuesta y respuesta de error
==============================

Consulte :doc:`api-overview` para detalles del modelo de errores. Los estados HTTP que devuelve este endpoint son:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Lista de respuestas

   * - Código de estado
     - Descripción
   * - 200 OK
     - Cuando el clúster está en estado ``green`` o ``yellow`` y es accesible. El sobre de éxito incluye ``engine``.
   * - 405 Method Not Allowed
     - Cuando el método HTTP no está permitido.
   * - 503 Service Unavailable
     - Cuando el clúster está en estado ``red``. El sobre de error (``error.code: service_unavailable``) incluye la instantánea del motor en ``error.details.engine``.

Tabla: Lista de respuestas
