==========================
API de RelatedQuery
==========================

Vision General
==============

La API de RelatedQuery es una API para gestionar las consultas relacionadas de |Fess|.
Permite registrar y administrar candidatos de palabras clave de busqueda relacionadas
(``queries``) para las palabras clave de busqueda (``term``) que introduce el usuario.
Las consultas relacionadas registradas se muestran como sugerencias de busqueda relacionadas
en la pantalla de busqueda.

Para obtener informacion detallada sobre la autenticacion, el formato de respuesta comun
(el campo ``version`` y los codigos ``status``), la paginacion y las respuestas de error,
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

   * - Metodo
     - Ruta
     - Descripcion
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

Parametros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametro
     - Tipo
     - Requerido
     - Descripcion
   * - ``size``
     - Integer
     - No
     - Numero de elementos por pagina (predeterminado: 25. Modificable mediante ``paging.page.size`` de ``fess_config.properties``)
   * - ``page``
     - Integer
     - No
     - Numero de pagina (comienza en 1. Predeterminado: 1)

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

   Cada configuracion incluye ``versionNo`` (numero de version para el bloqueo optimista). Los campos
   ``virtualHost`` y los campos de auditoria (``createdBy``, ``createdTime``, ``updatedBy``, ``updatedTime``)
   se incluyen unicamente cuando tienen un valor asignado. Un ``virtualHost`` vacio no se incluye
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

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Campo
     - Requerido
     - Descripcion
   * - ``term``
     - Si
     - Palabra clave de busqueda (maximo 10000 caracteres)
   * - ``queries``
     - Si
     - Consultas relacionadas. Cadena separada por saltos de linea, una por linea (las lineas vacias se ignoran; maximo 10000 caracteres)
   * - ``virtualHost``
     - No
     - Host virtual (maximo 1000 caracteres)

.. note::

   ``crudMode`` es configurado automaticamente por la API, por lo que no es necesario incluirlo en el cuerpo de la solicitud.

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

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Campo
     - Requerido
     - Descripcion
   * - ``id``
     - Si
     - ID de la consulta relacionada a actualizar (maximo 1000 caracteres)
   * - ``term``
     - Si
     - Palabra clave de busqueda (maximo 10000 caracteres)
   * - ``queries``
     - Si
     - Consultas relacionadas. Cadena separada por saltos de linea, una por linea (las lineas vacias se ignoran; maximo 10000 caracteres)
   * - ``virtualHost``
     - No
     - Host virtual (maximo 1000 caracteres)
   * - ``versionNo``
     - Si
     - Numero de version para el bloqueo optimista. Debe especificarse el valor incluido en la respuesta de la consulta de obtencion

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
contiene el detalle del error. Por ejemplo, en errores de validacion como la ausencia de campos
obligatorios, ``status`` toma el valor ``1``.
Para consultar la lista de codigos de estado, vea :doc:`api-admin-overview`.

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

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-relatedcontent` - API de contenido relacionado
- :doc:`api-admin-suggest` - API de gestion de sugerencias
- :doc:`../../admin/relatedquery-guide` - Guia de gestion de consultas relacionadas
