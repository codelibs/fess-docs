==========================
API de Plugin
==========================

Vision General
==============

La API de Plugin es para gestionar los plugins (artefactos) de |Fess|.
Permite obtener la lista de plugins instalados y de plugins instalables, asi como instalar y eliminar plugins.

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
     - /installed
     - Obtener lista de plugins instalados
   * - GET
     - /available
     - Obtener lista de plugins instalables
   * - POST
     - /
     - Instalar plugin
   * - DELETE
     - /
     - Eliminar plugin

Obtener Lista de Plugins Instalados
===================================

Devuelve la lista de plugins instalados.

Solicitud
---------

::

    GET /api/admin/plugin/installed

Respuesta
---------

En ``plugins`` se almacena un arreglo de objetos que representan la informacion de los plugins.
Cada objeto es un mapa de claves y valores de tipo cadena que incluye ``name`` (nombre del plugin) y ``version`` (version), entre otros.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "name": "fess-ds-slack",
            "version": "15.7.0"
          }
        ]
      }
    }

Obtener Lista de Plugins Instalables
====================================

Devuelve la lista de plugins instalables.

Solicitud
---------

::

    GET /api/admin/plugin/available

Respuesta
---------

En ``plugins`` se almacena un arreglo de objetos que representan la informacion de los plugins instalables.
Cada objeto es un mapa de claves y valores de tipo cadena, igual que en ``installed``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "name": "fess-ds-slack",
            "version": "15.7.0"
          }
        ]
      }
    }

Instalar Plugin
===============

Instala el plugin con el nombre y la version especificados.

Solicitud
---------

::

    POST /api/admin/plugin
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "fess-ds-slack",
      "version": "15.7.0"
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Campo
     - Requerido
     - Descripcion
   * - ``name``
     - Si
     - Nombre del plugin (maximo 100 caracteres)
   * - ``version``
     - Si
     - Version del plugin (maximo 100 caracteres)

Respuesta
---------

En caso de exito solo se devuelve ``status``.
Si no existe un artefacto que corresponda a ``name`` o ``version``, ``status`` sera ``1`` (BAD_REQUEST) y ``message`` se establecera con ``invalid name or version``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Eliminar Plugin
===============

Elimina el plugin con el nombre y la version especificados.

Solicitud
---------

::

    DELETE /api/admin/plugin
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "fess-ds-slack",
      "version": "15.7.0"
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Campo
     - Requerido
     - Descripcion
   * - ``name``
     - Si
     - Nombre del plugin (maximo 100 caracteres)
   * - ``version``
     - No
     - Version del plugin (maximo 100 caracteres)

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

Obtener Lista de Plugins Instalados
-----------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/plugin/installed" \
         -H "Authorization: Bearer YOUR_TOKEN"

Instalar un Plugin
------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.7.0"
         }'

Eliminar un Plugin
------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.7.0"
         }'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
