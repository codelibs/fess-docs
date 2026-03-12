==========================
API de Plugin
==========================

Vision General
==============

La API de Plugin es para gestionar plugins de |Fess|.
Puede operar instalacion, activacion, desactivacion y eliminacion de plugins.

URL Base
========

::

    /api/admin/plugin

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Metodo
     - Ruta
     - Descripcion
   * - GET
     - /
     - Obtener lista de plugins
   * - POST
     - /install
     - Instalar plugin
   * - DELETE
     - /{id}
     - Eliminar plugin

Obtener Lista de Plugins
========================

Solicitud
---------

::

    GET /api/admin/plugin

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "plugins": [
          {
            "id": "analysis-kuromoji",
            "name": "Japanese (kuromoji) Analysis Plugin",
            "version": "2.11.0",
            "description": "Japanese language analysis plugin",
            "enabled": true,
            "installed": true
          },
          {
            "id": "analysis-icu",
            "name": "ICU Analysis Plugin",
            "version": "2.11.0",
            "description": "Unicode normalization and collation",
            "enabled": true,
            "installed": true
          }
        ],
        "total": 2
      }
    }

Campos de Respuesta
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripcion
   * - ``id``
     - ID del plugin
   * - ``name``
     - Nombre del plugin
   * - ``version``
     - Version del plugin
   * - ``description``
     - Descripcion del plugin
   * - ``enabled``
     - Estado de activacion
   * - ``installed``
     - Estado de instalacion

Instalar Plugin
===============

Solicitud
---------

::

    POST /api/admin/plugin/install
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "url": "https://example.com/plugins/my-plugin-1.0.0.zip"
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripcion
   * - ``url``
     - Si
     - URL de descarga del plugin

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Plugin installed successfully. Restart required.",
        "pluginId": "my-plugin"
      }
    }

Eliminar Plugin
===============

Solicitud
---------

::

    DELETE /api/admin/plugin/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Plugin deleted successfully. Restart required."
      }
    }

Ejemplos de Uso
===============

Obtener Lista de Plugins
------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN"

Instalar un Plugin
------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/plugin/install" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "url": "https://artifacts.opensearch.org/releases/plugins/analysis-icu/2.11.0/analysis-icu-2.11.0.zip"
         }'

Eliminar un Plugin
------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/plugin/analysis-icu" \
         -H "Authorization: Bearer YOUR_TOKEN"

Notas Importantes
=================

- Despues de instalar o eliminar un plugin, es necesario reiniciar Fess
- Instalar plugins incompatibles puede impedir que Fess se inicie
- Tenga cuidado al eliminar plugins. Si hay dependencias, puede afectar al sistema

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-systeminfo` - API de informacion del sistema
- :doc:`../../admin/plugin-guide` - Guia de gestion de plugins
