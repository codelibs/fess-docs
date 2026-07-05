===========================
Vision General de Admin API
===========================

Vision General
==============

|Fess| Admin API es una API RESTful para acceder programaticamente a las funciones de administracion.
Puede ejecutar a traves de la API la mayoria de las operaciones disponibles en el panel de administracion, como la configuracion de rastreo, la gestion de usuarios y el control del programador.

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

Para acceder a Admin API, se requiere autenticacion mediante un token de acceso.

Obtencion del Token de Acceso
-----------------------------

1. Inicie sesion en el panel de administracion
2. Vaya a "Sistema" -> "Tokens de Acceso"
3. Haga clic en "Crear Nuevo"
4. Ingrese el nombre del token y configure en el campo "Permisos" los permisos que desea otorgar al token (para usar Admin API, ingrese ``{role}admin-api``)
5. Haga clic en "Crear" para obtener el token

Uso del Token
-------------

Incluya el token de acceso en el encabezado de la solicitud:

::

    Authorization: Bearer <token de acceso>

Tambien puede omitir ``Bearer`` y especificar solo el token:

::

    Authorization: <token de acceso>

La especificacion mediante parametro de consulta tambien es posible, pero esta deshabilitada de forma predeterminada. Si configura un nombre de parametro en
``api.access.token.request.parameter`` de ``fess_config.properties``, podra pasar el
token con ese nombre (como el valor predeterminado esta vacio, solo es valida la especificacion mediante el encabezado).
Por ejemplo, si configura ``api.access.token.request.parameter=token``:

::

    ?token=<token de acceso>

Ejemplo con cURL
~~~~~~~~~~~~~~~~

.. code-block:: bash

    curl -H "Authorization: Bearer YOUR_TOKEN" \
         "http://localhost:8080/api/admin/scheduler/settings"

Permisos Requeridos
-------------------

El acceso a Admin API se controla mediante un unico conjunto de permisos, no por funcion. Para utilizar
cualquiera de los endpoints de Admin API, el token de acceso debe tener otorgado alguno de los permisos
configurados en ``api.admin.access.permissions`` de ``fess_config.properties``.

El valor predeterminado es ``Radmin-api``, que es la forma codificada del rol ``admin-api``
(la ``R`` inicial es el valor de ``role.search.role.prefix``). Al crear el token de acceso, si ingresa
``{role}admin-api`` en el campo de permisos, se almacena internamente como ``Radmin-api``.

.. note::

   No existen permisos distintos por cada recurso individual (como ``admin-scheduler`` o ``admin-user``)
   ni comodines (``admin-*``). Un token que tenga el permiso configurado puede acceder a
   todos los endpoints de Admin API. Si desea cambiar los permisos que conceden acceso,
   modifique el valor de ``api.admin.access.permissions``.

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
   :widths: 20 15 65

   * - Parametro
     - Tipo
     - Descripcion
   * - ``size``
     - Integer
     - Numero de elementos por pagina (predeterminado: 25. Modificable mediante ``paging.page.size`` de ``fess_config.properties``)
   * - ``page``
     - Integer
     - Numero de pagina (comienza en 1. Predeterminado: 1. Si se especifica un valor menor o igual a 0, se trata como 1)

Respuesta
~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [...],
        "total": 100
      }
    }

.. note::

   El objeto ``response`` de todas las respuestas incluye siempre ``version``,
   que indica la version del producto (por ejemplo, ``"15.8.0"``). En los ejemplos siguientes
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
        "version": "15.8.0",
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
        "version": "15.8.0",
        "status": 1,
        "message": "Failed to process the request."
      }
    }

Codigos de Estado HTTP
----------------------

Admin API devuelve en la mayoria de los casos el estado HTTP ``200``, y el resultado del procesamiento se indica
en el campo ``status`` del cuerpo de la respuesta. Por lo tanto, no determine el exito o el fallo por el codigo de estado HTTP,
sino por el valor de ``status`` del cuerpo.

Los codigos de estado HTTP que se devuelven realmente son los siguientes.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Codigo
     - Descripcion
   * - 200
     - Respuesta normal. Ademas del caso de exito (``status: 0``), la mayoria de los errores tambien se
       devuelven con este codigo. Por ejemplo, si el token de acceso no se especifica o es invalido, o si los permisos son insuficientes, se devuelve
       ``status: 3``; y un error del sistema se devuelve como ``status: 2``, ambos con HTTP ``200``.
   * - 400
     - Error de validacion de los parametros de la solicitud. El ``status`` del cuerpo de la respuesta sera ``1``.
       Este codigo tambien se devuelve cuando se intenta obtener un recurso inexistente.
   * - 401
     - Cuando ocurre una excepcion relacionada con la autenticacion de inicio de sesion. El ``status`` del cuerpo de la respuesta sera ``3``.
       Tenga en cuenta que, si el token de acceso no se especifica o es invalido, no se devuelve este codigo, sino HTTP ``200`` con
       ``status: 3``.

.. note::

   Admin API no devuelve codigos de estado HTTP como ``403``, ``404`` o ``500``.
   Tanto los permisos insuficientes como la inexistencia de un recurso se indican mediante el
   ``status`` incluido en el cuerpo de la respuesta HTTP ``200`` o ``400``.

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
           "userAgent": "Mozilla/5.0 (compatible; Fess)",
           "numOfThread": 1,
           "intervalTime": 1000,
           "boost": 1.0,
           "maxAccessCount": 1000,
           "depth": 3,
           "sortOrder": 1,
           "available": "true"
         }'

.. note::

   Al crear una configuracion de rastreo web, son obligatorios ``name``, ``urls``, ``userAgent``, ``numOfThread``,
   ``intervalTime``, ``boost``, ``available`` y ``sortOrder``. Si se omiten,
   se produce un error de validacion (``status: 1``). ``available`` se especifica como una cadena de texto y
   se establece en ``"true"`` o ``"false"``.

Iniciar Trabajo Programado
--------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtener Lista de Usuarios
-------------------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/user/settings?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informacion de Referencia
=========================

- :doc:`../api-overview` - Vision general de API
- :doc:`../../admin/accesstoken-guide` - Guia de gestion de tokens de acceso
