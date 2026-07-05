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

La lista de etiquetas devuelta se filtra en función del usuario que realiza la solicitud y el contenido de la misma, de la siguiente manera:

- **Filtrado por permisos**: Las etiquetas se filtran en función de los permisos de acceso configurados en cada etiqueta y los roles del usuario. Dado que v2 utiliza autenticación basada en sesión, los usuarios que han iniciado sesión solo pueden obtener las etiquetas accesibles con sus propios roles. Las etiquetas cuyos permisos de acceso no coincidan no se incluyen en la lista.
- **Filtrado por configuración regional**: Las etiquetas pueden registrarse por configuración regional. Se devuelven las etiquetas registradas con una configuración regional que coincida con la cabecera de solicitud ``Accept-Language``, así como las etiquetas registradas sin una configuración regional específica.
- **Filtrado por host virtual**: Cuando se utilizan hosts virtuales, solo se devuelven las etiquetas asignadas al host virtual correspondiente.

Parámetros de solicitud
-----------------------

No hay parámetros de consulta. El filtrado de las etiquetas devueltas se realiza en función de los permisos del usuario autenticado y la cabecera de solicitud ``Accept-Language``, tal como se describe anteriormente.

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
     - Número de etiquetas devueltas (integer).
   * - ``labels``
     - Array de etiquetas.
   * - ``label``
     - Nombre para mostrar de la etiqueta (nombre de la etiqueta).
   * - ``value``
     - Valor de la etiqueta. Al especificar este valor en el parámetro ``fields.label`` de :doc:`api-search`, es posible filtrar los resultados de búsqueda por esa etiqueta.

Tabla: Campos de respuesta

Ejemplos de uso
===============

Ejemplo de solicitud usando el comando curl:

::

    curl "http://localhost:8080/api/v2/labels"

Respuesta de error
==================

Consulte :doc:`api-overview` para detalles del modelo de errores. Los estados HTTP que devuelve este endpoint son los siguientes:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Respuesta de error

   * - Código de estado
     - Descripción
   * - 405 Method Not Allowed
     - Se especificó un método HTTP distinto de GET. El ``error.code`` es ``method_not_allowed`` y la respuesta incluye la cabecera ``Allow: GET``.
   * - 500 Internal Server Error
     - Se produjo un error interno del servidor. El ``error.code`` es ``internal_error``.

Tabla: Respuesta de error
