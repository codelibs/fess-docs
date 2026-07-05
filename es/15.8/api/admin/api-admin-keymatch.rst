==========================
API de KeyMatch
==========================

Visión General
==============

La API de KeyMatch es para gestionar las coincidencias de claves (vinculación de palabras clave de búsqueda con resultados) de |Fess|.
Permite que documentos específicos aparezcan en los primeros lugares para determinadas palabras clave.

URL Base
========

::

    /api/admin/keymatch

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
     - Obtener lista de coincidencias de claves
   * - GET
     - /setting/{id}
     - Obtener coincidencia de clave
   * - POST
     - /setting
     - Crear coincidencia de clave
   * - PUT
     - /setting
     - Actualizar coincidencia de clave
   * - DELETE
     - /setting/{id}
     - Eliminar coincidencia de clave

Obtener Lista de Coincidencias de Claves
========================================

Solicitud
---------

::

    GET /api/admin/keymatch/settings

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
     - Número de elementos por página (predeterminado: 25; valor de configuración de ``paging.page.size``)
   * - ``page``
     - Integer
     - No
     - Número de página (comienza en 1, predeterminado: 1)
   * - ``term``
     - String
     - No
     - Filtrado por palabra clave de búsqueda (coincidencia con comodín)
   * - ``query``
     - String
     - No
     - Filtrado por consulta de condición de coincidencia (coincidencia con comodín)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "keymatch_id_1",
            "term": "download",
            "query": "title:download OR content:download",
            "maxSize": 10,
            "boost": 10.0,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   En ``total`` se establece el número total de elementos que coinciden con los criterios de filtrado (no el número de elementos de la página actual).
   Además de los campos indicados, cada objeto de configuración puede incluir ``virtualHost``,
   ``createdBy``, ``createdTime``, ``updatedBy`` y ``updatedTime`` cuando dichos valores estén definidos.

Obtener Coincidencia de Clave
=============================

Solicitud
---------

::

    GET /api/admin/keymatch/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "keymatch_id_1",
          "term": "download",
          "query": "title:download OR content:download",
          "maxSize": 10,
          "boost": 10.0,
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

.. note::

   ``versionNo`` es el número de versión para el bloqueo optimista. Al actualizar una coincidencia de clave,
   especifique el ``versionNo`` obtenido en la solicitud de obtención en el cuerpo de la solicitud.
   Si el ID especificado no existe, se devuelve un error.

Crear Coincidencia de Clave
===========================

Solicitud
---------

::

    POST /api/admin/keymatch/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "pricing",
      "query": "url:*/pricing* OR title:pricing",
      "maxSize": 5,
      "boost": 20.0
    }

Descripción de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Campo
     - Tipo
     - Requerido
     - Descripción
   * - ``term``
     - String
     - Sí
     - Palabra clave de búsqueda (máximo 100 caracteres)
   * - ``query``
     - String
     - Sí
     - Consulta de condición de coincidencia (la longitud máxima sigue el valor de configuración de ``form.admin.max.input.size``)
   * - ``maxSize``
     - Integer
     - Sí
     - Número máximo de resultados mostrados (entero mayor o igual a 0; valor inicial en la pantalla de administración: 10)
   * - ``boost``
     - Float
     - Sí
     - Valor de impulso (valor inicial en la pantalla de administración: 100.0)
   * - ``virtualHost``
     - String
     - No
     - Nombre del host virtual (máximo 1000 caracteres; especifíquelo cuando desee alternar las coincidencias de claves por host virtual)

.. note::

   ``maxSize`` y ``boost`` son obligatorios a través de la API. Los valores iniciales son los que se muestran en el formulario
   de la pantalla de administración y no se aplican en la API. Si se omiten, se producirá un error de validación.
   Tenga en cuenta que ``createdBy`` y ``createdTime``, aunque se especifiquen en la solicitud, serán sobrescritos por el servidor.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_keymatch_id",
        "created": true
      }
    }

Actualizar Coincidencia de Clave
================================

Solicitud
---------

::

    PUT /api/admin/keymatch/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_keymatch_id",
      "term": "pricing",
      "query": "url:*/pricing* OR title:pricing OR content:price",
      "maxSize": 10,
      "boost": 15.0,
      "versionNo": 1
    }

Descripción de Campos
~~~~~~~~~~~~~~~~~~~~~

Además de los campos de creación (``term``, ``query``, ``maxSize``, ``boost``, ``virtualHost``),
se deben especificar los siguientes campos.

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Campo
     - Tipo
     - Requerido
     - Descripción
   * - ``id``
     - String
     - Sí
     - ID de la coincidencia de clave a actualizar (máximo 1000 caracteres)
   * - ``versionNo``
     - Integer
     - Sí
     - Número de versión para el bloqueo optimista; especifique el valor obtenido en la solicitud de obtención

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_keymatch_id",
        "created": false
      }
    }

Eliminar Coincidencia de Clave
==============================

Solicitud
---------

::

    DELETE /api/admin/keymatch/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Ejemplos de Uso
===============

Crear Coincidencia de Clave para Página de Producto
----------------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/keymatch/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product features",
           "query": "url:*/products/* AND (title:features OR content:features)",
           "maxSize": 10,
           "boost": 15.0
         }'

Coincidencia de Clave para Página de Soporte
--------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/keymatch/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "query": "url:*/support/* OR url:*/help/* OR url:*/faq/*",
           "maxSize": 5,
           "boost": 20.0
         }'

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-elevateword` - API de palabras elevadas
- :doc:`../../admin/keymatch-guide` - Guía de gestión de coincidencias de claves
