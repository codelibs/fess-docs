==========================
RelatedContent API
==========================

Visión General
==============

La API de RelatedContent es una API para gestionar el contenido relacionado de |Fess|.
Permite mostrar contenido personalizado relacionado con palabras clave específicas.

URL Base
========

::

    /api/admin/relatedcontent

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
     - Listar contenido relacionado
   * - GET
     - /setting/{id}
     - Obtener contenido relacionado
   * - POST
     - /setting
     - Crear contenido relacionado
   * - PUT
     - /setting
     - Actualizar contenido relacionado
   * - DELETE
     - /setting/{id}
     - Eliminar contenido relacionado

Listar Contenido Relacionado
============================

Solicitud
---------

::

    GET /api/admin/relatedcontent/settings

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
     - Número de elementos por página (predeterminado: 25; configurable mediante ``paging.page.size`` en ``fess_config.properties``)
   * - ``page``
     - Integer
     - No
     - Número de página (comienza en 1, predeterminado: 1; los valores de 0 o menos se tratan como 1)
   * - ``term``
     - String
     - No
     - Filtrar por palabra clave de búsqueda (búsqueda con comodines)
   * - ``content``
     - String
     - No
     - Filtrar por cuerpo del contenido (búsqueda con comodines)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "content_id_1",
            "term": "fess",
            "content": "<div>Fess is an open source search server.</div>",
            "virtualHost": "",
            "sortOrder": 0,
            "createdBy": "admin",
            "createdTime": 1700000000000,
            "updatedBy": "admin",
            "updatedTime": 1700000000000,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   Cada elemento de ``settings`` y el objeto ``setting`` devuelto por el endpoint de
   obtención contienen los campos de la entidad almacenada tal como están. Además de
   ``term``, ``content``, ``sortOrder`` y ``virtualHost``, también se devuelven los campos
   de auditoría ``createdBy``, ``createdTime``, ``updatedBy``, ``updatedTime`` y el campo
   de bloqueo optimista ``versionNo``. ``createdTime`` y ``updatedTime`` se expresan como
   milisegundos desde el epoch (números). Los campos que no están establecidos (null) se
   omiten de la respuesta. Además, el objeto ``response`` de todas las respuestas incluye
   siempre ``version``, que indica la versión del producto (consulte :doc:`api-admin-overview`
   para más detalles).

Obtener Contenido Relacionado
=============================

Solicitud
---------

::

    GET /api/admin/relatedcontent/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "id": "content_id_1",
          "term": "fess",
          "content": "<div>Fess is an open source search server.</div>",
          "virtualHost": "",
          "sortOrder": 0,
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

.. note::

   El valor de ``versionNo`` necesario al actualizar (PUT) es el valor incluido en
   esta respuesta de obtención.

Crear Contenido Relacionado
===========================

Solicitud
---------

::

    POST /api/admin/relatedcontent/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "search",
      "content": "<div class='related'><h3>About Search</h3><p>Learn more about search features...</p></div>",
      "sortOrder": 0,
      "virtualHost": ""
    }

Descripción de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Campo
     - Requerido
     - Descripción
   * - ``term``
     - Sí
     - Palabra clave de búsqueda (máx. 10000 caracteres)
   * - ``content``
     - Sí
     - Contenido HTML a mostrar (máx. 10000 caracteres)
   * - ``sortOrder``
     - No
     - Orden de visualización (entero entre 0 y 2147483647)
   * - ``virtualHost``
     - No
     - Host virtual (máx. 1000 caracteres)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "new_content_id",
        "created": true
      }
    }

Actualizar Contenido Relacionado
================================

Solicitud
---------

::

    PUT /api/admin/relatedcontent/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_content_id",
      "term": "search",
      "content": "<div class='related updated'><h3>About Search</h3><p>Updated information...</p></div>",
      "sortOrder": 0,
      "virtualHost": "",
      "versionNo": 1
    }

Descripción de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Campo
     - Requerido
     - Descripción
   * - ``id``
     - Sí
     - ID del contenido relacionado a actualizar (máx. 1000 caracteres)
   * - ``term``
     - Sí
     - Palabra clave de búsqueda (máx. 10000 caracteres)
   * - ``content``
     - Sí
     - Contenido HTML a mostrar (máx. 10000 caracteres)
   * - ``sortOrder``
     - No
     - Orden de visualización (entero entre 0 y 2147483647)
   * - ``virtualHost``
     - No
     - Host virtual (máx. 1000 caracteres)
   * - ``versionNo``
     - Sí
     - Número de versión para el bloqueo optimista. Especifique el valor incluido en la respuesta de ``setting/{id}``.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "existing_content_id",
        "created": false
      }
    }

.. note::

   Los campos de auditoría como ``createdBy``, ``createdTime``, ``updatedBy``,
   ``updatedTime`` y ``crudMode`` se ignoran aunque se incluyan en el cuerpo de la
   solicitud, ya que son establecidos automáticamente en el lado del servidor. No es
   necesario especificarlos al crear o actualizar.

Eliminar Contenido Relacionado
==============================

Solicitud
---------

::

    DELETE /api/admin/relatedcontent/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Ejemplos de Uso
===============

Contenido Relacionado de Información de Producto
------------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedcontent/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "content": "<div class=\"product-info\"><h3>Our Products</h3><ul><li>Product A</li><li>Product B</li></ul></div>",
           "sortOrder": 0
         }'

Contenido Relacionado de Información de Soporte
-----------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedcontent/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "support",
           "content": "<div><p>Need help? Contact: support@example.com</p></div>",
           "sortOrder": 0
         }'

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión General de Admin API
- :doc:`api-admin-relatedquery` - API de Consultas Relacionadas
- :doc:`../../admin/relatedcontent-guide` - Guía de Gestión de Contenido Relacionado
