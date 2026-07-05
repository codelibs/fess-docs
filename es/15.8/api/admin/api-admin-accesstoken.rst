==========================
AccessToken API
==========================

Vision General
==============

La API de AccessToken es una API para gestionar los tokens de acceso a la API de |Fess|.
Permite ejecutar la creacion, obtencion, actualizacion y eliminacion de tokens.

Los tokens de acceso se utilizan para la autenticacion al invocar la API de busqueda
o la Admin API de |Fess| de forma programatica.
Para conocer las especificaciones comunes de la Admin API (metodo de autenticacion, formato de respuesta,
valores de ``status``, respuestas de error y codigos de estado HTTP), incluyendo esta API,
consulte :doc:`api-admin-overview`.

.. note::

   Para acceder a esta API, el token de acceso utilizado en la solicitud debe tener un permiso
   que coincida con ``api.admin.access.permissions``
   (valor predeterminado: ``{role}admin-api``).

URL Base
========

::

    /api/admin/accesstoken

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
     - Obtener lista de tokens de acceso
   * - GET
     - /setting/{id}
     - Obtener token de acceso
   * - POST
     - /setting
     - Crear token de acceso
   * - PUT
     - /setting
     - Actualizar token de acceso
   * - DELETE
     - /setting/{id}
     - Eliminar token de acceso

Obtener Lista de Tokens de Acceso
=================================

Solicitud
---------

::

    GET /api/admin/accesstoken/settings

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
     - Numero de elementos por pagina (predeterminado: 25; puede cambiarse con ``paging.page.size``)
   * - ``page``
     - Integer
     - No
     - Numero de pagina (comienza en 1; predeterminado: 1)
   * - ``id``
     - String
     - No
     - Filtro para obtener unicamente el token con el ID especificado

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": "token_id_1",
            "name": "API Token 1",
            "token": "abcd1234efgh5678",
            "parameterName": "permission",
            "permissions": "{role}admin-api",
            "expires": "2026-01-01T00:00:00",
            "createdBy": "admin",
            "createdTime": 1735689600000,
            "updatedBy": "admin",
            "updatedTime": 1735689600000,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   Cada objeto de token incluye tambien informacion de auditoria y version:
   ``createdBy``, ``createdTime``, ``updatedBy``, ``updatedTime`` y ``versionNo``.
   ``createdTime`` y ``updatedTime`` se expresan en milisegundos desde la epoca (valor numerico).
   Los campos con valor ``null`` se excluyen de la respuesta.
   ``permissions`` se devuelve como una cadena separada por saltos de linea (``\n``).

Obtener Token de Acceso
=======================

Solicitud
---------

::

    GET /api/admin/accesstoken/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "token_id_1",
          "name": "API Token 1",
          "token": "abcd1234efgh5678",
          "parameterName": "permission",
          "permissions": "{role}admin-api",
          "expires": "2026-01-01T00:00:00",
          "createdBy": "admin",
          "createdTime": 1735689600000,
          "updatedBy": "admin",
          "updatedTime": 1735689600000,
          "versionNo": 1
        }
      }
    }

Crear Token de Acceso
=====================

Solicitud
---------

::

    POST /api/admin/accesstoken/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Integration API Token",
      "permissions": "{role}admin-api",
      "expires": "2026-01-01T00:00:00"
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
     - Nombre del token (maximo 1000 caracteres)
   * - ``permissions``
     - No
     - Permisos otorgados a este token. Se pueden especificar multiples valores separados por saltos de linea (``\n``) (ejemplo: ``{role}admin-api``). Los tokens que invocan la Admin API deben tener un permiso que coincida con ``api.admin.access.permissions`` (valor predeterminado: ``{role}admin-api``).
   * - ``parameterName``
     - No
     - Nombre del parametro de solicitud para pasar permisos adicionales. Si una solicitud autenticada con este token incluye un parametro con el nombre aqui especificado, su valor se agrega a ``permissions``. Si se omite, no se configura.
   * - ``expires``
     - No
     - Fecha de expiracion. Se especifica como cadena en formato ``YYYY-MM-DDTHH:MM:SS`` (ejemplo: ``2026-01-01T00:00:00``). Si se omite, el token no tiene fecha de expiracion.

.. note::

   La cadena del token (``token``) se genera automaticamente en el servidor. Si se especifica
   ``token`` en el cuerpo de la solicitud, sera ignorado. Como la respuesta de creacion no incluye
   la cadena del token generada, obtenga el token mediante "Obtener Token de Acceso"
   (``GET /setting/{id}``).

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_token_id",
        "created": true
      }
    }

Actualizar Token de Acceso
==========================

Solicitud
---------

::

    PUT /api/admin/accesstoken/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_token_id",
      "name": "Updated API Token",
      "permissions": "{role}admin-api\n{role}user",
      "expires": "2026-01-01T00:00:00",
      "versionNo": 1
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

En la actualizacion se utilizan los mismos campos que en la creacion, mas los siguientes campos adicionales.

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Campo
     - Requerido
     - Descripcion
   * - ``id``
     - Si
     - ID del token a actualizar
   * - ``versionNo``
     - Si
     - Numero de version para el bloqueo optimista. Especifique el ``versionNo`` del token obtenido previamente.

.. note::

   La cadena del token (``token``) no puede actualizarse. Si se especifica ``token``
   en el cuerpo de la solicitud, sera ignorado y se mantendra el valor existente.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_token_id",
        "created": false
      }
    }

Eliminar Token de Acceso
========================

Solicitud
---------

::

    DELETE /api/admin/accesstoken/setting/{id}

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

Crear Token API
---------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/accesstoken/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Search API Token",
           "permissions": "{role}guest"
         }'

Llamada a la API Usando el Token
---------------------------------

El token creado se utiliza para la autenticacion al invocar la API de busqueda u otras APIs.

.. code-block:: bash

    # Usar el token como encabezado Authorization
    curl "http://localhost:8080/api/v2/search?q=test" \
         -H "Authorization: Bearer your_token_here"

    # Usar el token como parametro de consulta (requiere configurar api.access.token.request.parameter)
    curl "http://localhost:8080/api/v2/search?q=test&token=your_token_here"

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API (autenticacion, formato de respuesta y errores)
- :doc:`../api-search` - API de busqueda
- :doc:`../../admin/accesstoken-guide` - Guia de gestion de tokens de acceso
