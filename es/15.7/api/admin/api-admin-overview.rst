==========================
Vision General de Admin API
==========================

Vision General
==============

|Fess| Admin API es una API RESTful para acceder programaticamente a las funciones de administracion.
A traves de esta API, puede ejecutar la mayoria de las operaciones disponibles en el panel de administracion, como configuracion de rastreo, gestion de usuarios y control del programador.

Al utilizar esta API, puede automatizar la configuracion de |Fess| o integrarse con sistemas externos.

URL Base
========

La URL base de Admin API tiene el siguiente formato:

::

    http://<Nombre del Servidor>/api/admin/

Por ejemplo, en un entorno local:

::

    http://localhost:8080/api/admin/

Autenticacion
=============

Para acceder a Admin API, se requiere autenticacion mediante token de acceso.

Obtencion del Token de Acceso
-----------------------------

1. Inicie sesion en el panel de administracion
2. Vaya a "Sistema" -> "Tokens de Acceso"
3. Haga clic en "Crear Nuevo"
4. Ingrese el nombre del token y seleccione los permisos necesarios
5. Haga clic en "Crear" para obtener el token

Uso del Token
-------------

Incluya el token de acceso en el encabezado de la solicitud:

::

    Authorization: Bearer <token de acceso>

O especifique como parametro de consulta:

::

    ?token=<token de acceso>

Ejemplo con cURL
~~~~~~~~~~~~~~~~

.. code-block:: bash

    curl -H "Authorization: Bearer YOUR_TOKEN" \
         "http://localhost:8080/api/admin/scheduler/settings"

Permisos Requeridos
-------------------

Para usar Admin API, el token necesita los siguientes permisos:

- ``admin-*`` - Acceso a todas las funciones de administracion
- ``admin-scheduler`` - Solo gestion del programador
- ``admin-user`` - Solo gestion de usuarios
- Otros permisos especificos por funcion

Patrones Comunes
================

Los recursos que tienen configuraciones (webconfig, user, role, etc.) siguen el siguiente patron CRUD comun.
Sin embargo, algunos recursos (systeminfo, stats, storage, plugin, log, backup, documents, suggest, la raiz de dict, etc.)
tienen una estructura de endpoints propia distinta de este patron comun, por lo que debe consultar la pagina de cada recurso.

Obtener Lista (GET /settings)
-----------------------------

Obtiene una lista de configuraciones.

Solicitud
~~~~~~~~~

::

    GET /api/admin/<recurso>/settings

Parametros (paginacion):

.. list-table::
   :header-rows: 1
   :widths: 20 15.75

   * - Parametro
     - Tipo
     - Descripcion
   * - ``size``
     - Integer
     - Numero de elementos por pagina (predeterminado: 20)
   * - ``page``
     - Integer
     - Numero de pagina (comienza en 0)

Respuesta
~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [...],
        "total": 100
      }
    }

.. note::

   El objeto ``response`` de todas las respuestas incluye siempre ``version``,
   que indica la version del producto (por ejemplo, ``"15.7.0"``). En los ejemplos siguientes
   puede omitirse por brevedad.

Obtener Configuracion Individual (GET /setting/{id})
----------------------------------------------------

Obtiene una configuracion individual especificando el ID.

Solicitud
~~~~~~~~~

::

    GET /api/admin/<recurso>/setting/{id}

Respuesta
~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {...}
      }
    }

Crear Nuevo (POST /setting)
---------------------------

Crea una nueva configuracion.

Solicitud
~~~~~~~~~

::

    POST /api/admin/<recurso>/setting
    Content-Type: application/json

    {
      "name": "...",
      "...": "..."
    }

Respuesta
~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "created_id",
        "created": true
      }
    }

Actualizar (PUT /setting)
-------------------------

Actualiza una configuracion existente.

Solicitud
~~~~~~~~~

::

    PUT /api/admin/<recurso>/setting
    Content-Type: application/json

    {
      "id": "...",
      "name": "...",
      "...": "..."
    }

Respuesta
~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "updated_id",
        "created": false
      }
    }

Eliminar (DELETE /setting/{id})
-------------------------------

Elimina una configuracion.

Solicitud
~~~~~~~~~

::

    DELETE /api/admin/<recurso>/setting/{id}

Respuesta
~~~~~~~~~

El formato de la respuesta de eliminacion difiere segun el recurso (accion). Muchos recursos
devuelven solo ``status``.

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

En algunos recursos, el resultado de la eliminacion se devuelve como ``ApiUpdateResponse``, con
el ``id`` de la configuracion eliminada y ``created`` (``false`` al eliminar).

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_id",
        "created": false
      }
    }

Ademas, en los recursos que devuelven ``ApiDeleteResponse`` puede agregarse ``count``,
que indica el numero de elementos eliminados (valor predeterminado ``1``). Consulte la pagina de cada recurso para conocer el formato real.

Formato de Respuesta
====================

Todas las respuestas se envuelven en un objeto ``response`` que incluye siempre
``version``, que indica la version del producto, y ``status``, que indica el resultado del procesamiento.

Los valores de ``status`` son los siguientes.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Valor
     - Descripcion
   * - ``0``
     - OK (exito)
   * - ``1``
     - BAD_REQUEST (solicitud invalida)
   * - ``2``
     - SYSTEM_ERROR (error del sistema)
   * - ``3``
     - UNAUTHORIZED (error de autenticacion)
   * - ``9``
     - FAILED (procesamiento fallido)

Respuesta Exitosa
-----------------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "...": "..."
      }
    }

``status: 0`` indica exito.

Respuesta de Error
------------------

En caso de error, ``status`` se establece en un valor distinto de 0 y ``message``
contiene el mensaje de error.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 1,
        "message": "Failed to process the request."
      }
    }

Codigos de Estado HTTP
----------------------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Codigo
     - Descripcion
   * - 200
     - Solicitud exitosa
   * - 400
     - Parametros de solicitud invalidos
   * - 401
     - Se requiere autenticacion (sin token o token invalido)
   * - 403
     - Sin permisos de acceso
   * - 404
     - Recurso no encontrado
   * - 500
     - Error interno del servidor

APIs Disponibles
================

|Fess| proporciona las siguientes Admin APIs.

Configuracion de Rastreo
------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Descripcion
   * - :doc:`api-admin-webconfig`
     - Configuracion de rastreo web
   * - :doc:`api-admin-fileconfig`
     - Configuracion de rastreo de archivos
   * - :doc:`api-admin-dataconfig`
     - Configuracion de almacen de datos

.. note::

   Ademas, los siguientes recursos relacionados con credenciales de autenticacion y control de rastreo
   tambien se ofrecen como API (actualmente no tienen una pagina propia): ``webauth`` (autenticacion web), ``fileauth`` (autenticacion de archivos),
   ``reqheader`` (encabezados de solicitud), ``pathmap`` (mapeo de rutas),
   ``duplicatehost`` (hosts duplicados), ``searchlist`` (operaciones de busqueda/lista de documentos).

Gestion de Indices
------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Descripcion
   * - :doc:`api-admin-documents`
     - Operaciones masivas de documentos
   * - :doc:`api-admin-crawlinginfo`
     - Informacion de rastreo
   * - :doc:`api-admin-failureurl`
     - Gestion de URLs fallidas
   * - :doc:`api-admin-backup`
     - Copia de seguridad/Restauracion

Programador
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Descripcion
   * - :doc:`api-admin-scheduler`
     - Programacion de trabajos
   * - :doc:`api-admin-joblog`
     - Obtencion de registros de trabajos

Gestion de Usuarios y Permisos
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Descripcion
   * - :doc:`api-admin-user`
     - Gestion de usuarios
   * - :doc:`api-admin-role`
     - Gestion de roles
   * - :doc:`api-admin-group`
     - Gestion de grupos
   * - :doc:`api-admin-accesstoken`
     - Gestion de tokens API

Ajuste de Busqueda
------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Descripcion
   * - :doc:`api-admin-labeltype`
     - Tipos de etiqueta
   * - :doc:`api-admin-keymatch`
     - Coincidencia de claves
   * - :doc:`api-admin-boostdoc`
     - Impulso de documentos
   * - :doc:`api-admin-elevateword`
     - Palabras elevadas
   * - :doc:`api-admin-badword`
     - Palabras prohibidas
   * - :doc:`api-admin-relatedcontent`
     - Contenido relacionado
   * - :doc:`api-admin-relatedquery`
     - Consultas relacionadas
   * - :doc:`api-admin-suggest`
     - Gestion de sugerencias

Sistema
-------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Descripcion
   * - :doc:`api-admin-general`
     - Configuracion general
   * - :doc:`api-admin-systeminfo`
     - Informacion del sistema
   * - :doc:`api-admin-stats`
     - Estadisticas del sistema
   * - :doc:`api-admin-log`
     - Obtencion de registros
   * - :doc:`api-admin-searchlist`
     - Busqueda y gestion de documentos
   * - :doc:`api-admin-storage`
     - Gestion de almacenamiento
   * - :doc:`api-admin-plugin`
     - Gestion de plugins

Diccionario
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Descripcion
   * - :doc:`api-admin-dict`
     - Gestion de diccionarios (sinonimos, palabras vacias, etc.)

Ejemplos de Uso
===============

Crear Configuracion de Rastreo Web
----------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Example Site",
           "urls": "https://example.com/",
           "includedUrls": ".*example.com.*",
           "excludedUrls": "",
           "maxAccessCount": 1000,
           "depth": 3,
           "available": true
         }'

Iniciar Trabajo Programado
--------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtener Lista de Usuarios
-------------------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/user/settings?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informacion de Referencia
=========================

- :doc:`../api-overview` - Vision general de API
- :doc:`../../admin/accesstoken-guide` - Guia de gestion de tokens de acceso
