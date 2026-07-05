==========================
API de LabelType
==========================

Descripción general
===================

La API de LabelType es una API para gestionar los tipos de etiqueta de |Fess|.
Los tipos de etiqueta permiten clasificar los resultados de búsqueda según las rutas rastreadas
o el host virtual, y utilizarlos para filtrar (refinar) los resultados en la pantalla de búsqueda por etiqueta.

Para conocer el método de autenticación y las especificaciones comunes de la Respuesta
(código ``status``, campo ``version``, formato de errores, códigos de estado HTTP, etc.),
consulte :doc:`api-admin-overview`.
Para acceder a esta API, es necesario especificar un token de acceso con el permiso de Admin API
(``admin-api``) en el encabezado ``Authorization: Bearer <token de acceso>``.

URL base
========

::

    /api/admin/labeltype

Lista de endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Método
     - Ruta
     - Descripción
   * - GET
     - /settings
     - Obtener lista de tipos de etiqueta
   * - GET
     - /setting/{id}
     - Obtener tipo de etiqueta
   * - POST
     - /setting
     - Crear tipo de etiqueta
   * - PUT
     - /setting
     - Actualizar tipo de etiqueta
   * - DELETE
     - /setting/{id}
     - Eliminar tipo de etiqueta

Obtener lista de tipos de etiqueta
===================================

Solicitud
---------

::

    GET /api/admin/labeltype/settings

Parámetros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parámetro
     - Tipo
     - Obligatorio
     - Descripción
   * - ``size``
     - Integer
     - No
     - Número de elementos por página. El valor predeterminado es el configurado en ``paging.page.size`` (normalmente ``25``).
   * - ``page``
     - Integer
     - No
     - Número de página (comienza en 1). El valor predeterminado es ``1``.
   * - ``name``
     - String
     - No
     - Filtrar por nombre de visualización (búsqueda con comodines).
   * - ``value``
     - String
     - No
     - Filtrar por valor de etiqueta (búsqueda con comodines).

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": "label_id_1",
            "name": "Documentation",
            "value": "docs",
            "includedPaths": ".*docs\\.example\\.com.*",
            "excludedPaths": "",
            "permissions": "{role}admin",
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

   Cada objeto de configuración también incluye ``createdBy`` / ``createdTime`` / ``updatedBy`` /
   ``updatedTime`` para auditoría, y ``versionNo`` para bloqueo optimista (los campos con valor
   ``null`` se omiten). El objeto ``response`` siempre contiene ``version``, que indica la versión
   del producto, aunque en los ejemplos siguientes puede omitirse por brevedad.

Obtener tipo de etiqueta
========================

Solicitud
---------

::

    GET /api/admin/labeltype/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "label_id_1",
          "name": "Documentation",
          "value": "docs",
          "includedPaths": ".*docs\\.example\\.com.*",
          "excludedPaths": "",
          "permissions": "{role}admin",
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

Crear tipo de etiqueta
======================

Solicitud
---------

::

    POST /api/admin/labeltype/setting
    Content-Type: application/json

Cuerpo de la solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "News",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/news/.*",
      "excludedPaths": ".*/(archive|old)/.*",
      "sortOrder": 1,
      "permissions": "{role}guest"
    }

Descripción de campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - Campo
     - Tipo
     - Obligatorio
     - Descripción
   * - ``name``
     - String
     - Sí
     - Nombre de visualización de la etiqueta (máximo 100 caracteres).
   * - ``value``
     - String
     - Sí
     - Valor de la etiqueta (utilizado con el parámetro ``label`` en las búsquedas). Solo se permiten caracteres alfanuméricos ASCII y guión bajo (``_``), y debe coincidir con la expresión regular ``^[a-zA-Z0-9_]+$`` (máximo 100 caracteres).
   * - ``includedPaths``
     - String
     - No
     - Expresión regular de las rutas a las que se aplica la etiqueta. Si se especifican varias, sepárelas con salto de línea (``\n``).
   * - ``excludedPaths``
     - String
     - No
     - Expresión regular de las rutas excluidas de la etiqueta. Si se especifican varias, sepárelas con salto de línea (``\n``).
   * - ``permissions``
     - String
     - No
     - Roles, grupos o usuarios con permiso de acceso (por ejemplo: ``{role}admin``). Si se especifican varios, sepárelos con salto de línea (``\n``).
   * - ``sortOrder``
     - Integer
     - No
     - Orden de visualización (entero mayor o igual a 0). El valor predeterminado es ``0``.
   * - ``virtualHost``
     - String
     - No
     - Host virtual (máximo 1000 caracteres).

.. note::

   Los campos de auditoría como ``createdBy`` / ``createdTime`` son establecidos automáticamente
   por el servidor, por lo que no es necesario especificarlos en la solicitud.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_label_id",
        "created": true
      }
    }

Si la creación es exitosa, ``created`` será ``true``.

Actualizar tipo de etiqueta
===========================

Solicitud
---------

::

    PUT /api/admin/labeltype/setting
    Content-Type: application/json

Cuerpo de la solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_label_id",
      "name": "News Articles",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/(news|articles)/.*",
      "excludedPaths": ".*/(archive|old|draft)/.*",
      "sortOrder": 1,
      "permissions": "{role}guest",
      "versionNo": 1
    }

En la actualización, además de los campos de creación, los siguientes campos son obligatorios.

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - Campo
     - Tipo
     - Obligatorio
     - Descripción
   * - ``id``
     - String
     - Sí
     - ID del tipo de etiqueta a actualizar.
   * - ``versionNo``
     - Integer
     - Sí
     - Número de versión para bloqueo optimista. Especifique el valor de ``versionNo`` incluido en la respuesta al obtener el registro. Si la versión especificada no coincide con la actual, la actualización fallará.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_label_id",
        "created": false
      }
    }

En caso de actualización, ``created`` será ``false``.

Eliminar tipo de etiqueta
=========================

Solicitud
---------

::

    DELETE /api/admin/labeltype/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Ejemplos de uso
===============

Crear etiqueta para documentación
----------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/labeltype/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Technical Documentation",
           "value": "tech_docs",
           "includedPaths": ".*docs\\.example\\.com.*\n.*example\\.com/documentation/.*",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

Obtener lista de tipos de etiqueta
-----------------------------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/labeltype/settings?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Búsqueda usando etiqueta
------------------------

.. code-block:: bash

    # Filtrar por etiqueta
    curl "http://localhost:8080/json/?q=search&label=tech_docs"

Véase también
=============

- :doc:`api-admin-overview` - Descripción general de Admin API
- :doc:`../api-search` - API de búsqueda
- :doc:`../../admin/labeltype-guide` - Guía de gestión de tipos de etiqueta
