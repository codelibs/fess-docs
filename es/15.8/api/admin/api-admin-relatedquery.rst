==========================
API de RelatedQuery
==========================

Visión General
==============

La API de RelatedQuery es una API para gestionar las consultas relacionadas de |Fess|.
Permite registrar y administrar candidatos de palabras clave de búsqueda relacionadas
(``queries``) para las palabras clave de búsqueda (``term``) que introduce el usuario.
Las consultas relacionadas registradas se muestran como sugerencias de búsqueda relacionadas
en la pantalla de búsqueda.

Para obtener información detallada sobre la autenticación, el formato de respuesta común
(el campo ``version`` y los códigos ``status``), la paginación y las respuestas de error,
consulte :doc:`api-admin-overview`.

URL Base
========

::

    /api/admin/relatedquery

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Método
     - Ruta
     - Descripción
   * - GET
     - /settings
     - Obtener lista de consultas relacionadas
   * - GET
     - /setting/{id}
     - Obtener consulta relacionada
   * - POST
     - /setting
     - Crear consulta relacionada
   * - PUT
     - /setting
     - Actualizar consulta relacionada
   * - DELETE
     - /setting/{id}
     - Eliminar consulta relacionada

Obtener Lista de Consultas Relacionadas
=======================================

Solicitud
---------

::

    GET /api/admin/relatedquery/settings

Parámetros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parámetro
     - Tipo
     - Requerido
     - Descripción
   * - ``size``
     - Integer
     - No
     - Número de elementos por página (predeterminado: 25. Modificable mediante ``paging.page.size`` de ``fess_config.properties``)
   * - ``page``
     - Integer
     - No
     - Número de página (comienza en 1. Predeterminado: 1)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": "query_id_1",
            "term": "fess",
            "queries": "fess tutorial\nfess installation\nfess configuration",
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   Cada configuración incluye ``versionNo`` (número de versión para el bloqueo optimista). Los campos
   ``virtualHost`` y los campos de auditoría (``createdBy``, ``createdTime``, ``updatedBy``, ``updatedTime``)
   se incluyen únicamente cuando tienen un valor asignado. Un ``virtualHost`` vacío no se incluye
   en la respuesta.

Obtener Consulta Relacionada
============================

Solicitud
---------

::

    GET /api/admin/relatedquery/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "setting": {
          "id": "query_id_1",
          "term": "fess",
          "queries": "fess tutorial\nfess installation\nfess configuration",
          "virtualHost": "site1.example.com",
          "versionNo": 1
        }
      }
    }

Crear Consulta Relacionada
==========================

Solicitud
---------

::

    POST /api/admin/relatedquery/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "search",
      "queries": "search tutorial\nsearch syntax\nadvanced search",
      "virtualHost": ""
    }

Descripción de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Campo
     - Requerido
     - Descripción
   * - ``term``
     - Sí
     - Palabra clave de búsqueda (máximo 10000 caracteres)
   * - ``queries``
     - Sí
     - Consultas relacionadas. Cadena separada por saltos de línea, una por línea (las líneas vacías se ignoran; máximo 10000 caracteres)
   * - ``virtualHost``
     - No
     - Host virtual (máximo 1000 caracteres)

.. note::

   ``crudMode`` es configurado automáticamente por la API, por lo que no es necesario incluirlo en el cuerpo de la solicitud.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "new_query_id",
        "created": true
      }
    }

Actualizar Consulta Relacionada
===============================

Solicitud
---------

::

    PUT /api/admin/relatedquery/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_query_id",
      "term": "search",
      "queries": "search tutorial\nsearch syntax\nadvanced search\nsearch tips",
      "virtualHost": "",
      "versionNo": 1
    }

Descripción de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Campo
     - Requerido
     - Descripción
   * - ``id``
     - Sí
     - ID de la consulta relacionada a actualizar (máximo 1000 caracteres)
   * - ``term``
     - Sí
     - Palabra clave de búsqueda (máximo 10000 caracteres)
   * - ``queries``
     - Sí
     - Consultas relacionadas. Cadena separada por saltos de línea, una por línea (las líneas vacías se ignoran; máximo 10000 caracteres)
   * - ``virtualHost``
     - No
     - Host virtual (máximo 1000 caracteres)
   * - ``versionNo``
     - Sí
     - Número de versión para el bloqueo optimista. Debe especificarse el valor incluido en la respuesta de la consulta de obtención

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "existing_query_id",
        "created": false
      }
    }

Eliminar Consulta Relacionada
=============================

Solicitud
---------

::

    DELETE /api/admin/relatedquery/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

Respuesta de Error
==================

Cuando una solicitud falla, ``status`` se establece en un valor distinto de 0 y ``message``
contiene el detalle del error. Por ejemplo, en errores de validación como la ausencia de campos
obligatorios, ``status`` toma el valor ``1``.
Para consultar la lista de códigos de estado, vea :doc:`api-admin-overview`.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 1,
        "message": "..."
      }
    }

Ejemplos de Uso
===============

Consultas Relacionadas con Productos
------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "queries": "product features\nproduct pricing\nproduct comparison\nproduct reviews"
         }'

Consultas Relacionadas con Ayuda
---------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "queries": "help center\nhelp documentation\nhelp contact support"
         }'

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-relatedcontent` - API de contenido relacionado
- :doc:`api-admin-suggest` - API de gestión de sugerencias
- :doc:`../../admin/relatedquery-guide` - Guía de gestión de consultas relacionadas
