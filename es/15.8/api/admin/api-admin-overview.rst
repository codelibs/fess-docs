===========================
Visión General de Admin API
===========================

Visión General
==============

|Fess| Admin API es una API RESTful para acceder programáticamente a las funciones de administración.
Puede ejecutar a través de la API la mayoría de las operaciones disponibles en el panel de administración, como la configuración de rastreo, la gestión de usuarios y el control del programador.

Al utilizar esta API, puede automatizar la configuración de |Fess| o integrarse con sistemas externos.

URL Base
========

La URL base de Admin API tiene el siguiente formato:

::

    http://<Nombre del Servidor>/api/admin/

Por ejemplo, en un entorno local:

::

    http://localhost:8080/api/admin/

Autenticación
=============

Para acceder a Admin API, se requiere autenticación mediante un token de acceso.

Obtención del Token de Acceso
-----------------------------

1. Inicie sesión en el panel de administración
2. Vaya a "Sistema" -> "Tokens de Acceso"
3. Haga clic en "Crear Nuevo"
4. Ingrese el nombre del token y configure en el campo "Permisos" los permisos que desea otorgar al token (para usar Admin API, ingrese ``{role}admin-api``)
5. Haga clic en "Crear" para obtener el token

Uso del Token
-------------

Incluya el token de acceso en el encabezado de la solicitud:

::

    Authorization: Bearer <token de acceso>

También puede omitir ``Bearer`` y especificar solo el token:

::

    Authorization: <token de acceso>

La especificación mediante parámetro de consulta también es posible, pero está deshabilitada de forma predeterminada. Si configura un nombre de parámetro en
``api.access.token.request.parameter`` de ``fess_config.properties``, podrá pasar el
token con ese nombre (como el valor predeterminado está vacío, solo es válida la especificación mediante el encabezado).
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

El acceso a Admin API se controla mediante un único conjunto de permisos, no por función. Para utilizar
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

Los recursos que tienen configuraciones (webconfig, user, role, etc.) siguen el siguiente patrón CRUD común.
Sin embargo, algunos recursos (systeminfo, stats, storage, plugin, log, backup, documents, suggest, la raíz de dict, etc.)
tienen una estructura de endpoints propia distinta de este patrón común, por lo que debe consultar la página de cada recurso.

Obtener Lista (GET /settings)
-----------------------------

Obtiene una lista de configuraciones.

Solicitud
~~~~~~~~~

::

    GET /api/admin/<recurso>/settings

Parámetros (paginación):

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parámetro
     - Tipo
     - Descripción
   * - ``size``
     - Integer
     - Número de elementos por página (predeterminado: 25. Modificable mediante ``paging.page.size`` de ``fess_config.properties``)
   * - ``page``
     - Integer
     - Número de página (comienza en 1. Predeterminado: 1. Si se especifica un valor menor o igual a 0, se trata como 1)

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
   que indica la versión del producto (por ejemplo, ``"15.8.0"``). En los ejemplos siguientes
   puede omitirse por brevedad.

Obtener Configuración Individual (GET /setting/{id})
----------------------------------------------------

Obtiene una configuración individual especificando el ID.

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

Crea una nueva configuración.

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

Actualiza una configuración existente.

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

Elimina una configuración.

Solicitud
~~~~~~~~~

::

    DELETE /api/admin/<recurso>/setting/{id}

Respuesta
~~~~~~~~~

El formato de la respuesta de eliminación difiere según el recurso (acción). Muchos recursos
devuelven solo ``status``.

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

En algunos recursos, el resultado de la eliminación se devuelve como ``ApiUpdateResponse``, con
el ``id`` de la configuración eliminada y ``created`` (``false`` al eliminar).

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_id",
        "created": false
      }
    }

Además, en los recursos que devuelven ``ApiDeleteResponse`` puede agregarse ``count``,
que indica el número de elementos eliminados (valor predeterminado ``1``). Consulte la página de cada recurso para conocer el formato real.

Formato de Respuesta
====================

Todas las respuestas se envuelven en un objeto ``response`` que incluye siempre
``version``, que indica la versión del producto, y ``status``, que indica el resultado del procesamiento.

Los valores de ``status`` son los siguientes.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Valor
     - Descripción
   * - ``0``
     - OK (éxito)
   * - ``1``
     - BAD_REQUEST (solicitud inválida)
   * - ``2``
     - SYSTEM_ERROR (error del sistema)
   * - ``3``
     - UNAUTHORIZED (error de autenticación)
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

``status: 0`` indica éxito.

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

Códigos de Estado HTTP
----------------------

Admin API devuelve en la mayoría de los casos el estado HTTP ``200``, y el resultado del procesamiento se indica
en el campo ``status`` del cuerpo de la respuesta. Por lo tanto, no determine el éxito o el fallo por el código de estado HTTP,
sino por el valor de ``status`` del cuerpo.

Los códigos de estado HTTP que se devuelven realmente son los siguientes.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Código
     - Descripción
   * - 200
     - Respuesta normal. Además del caso de éxito (``status: 0``), la mayoría de los errores también se
       devuelven con este código. Por ejemplo, si el token de acceso no se especifica o es inválido, o si los permisos son insuficientes, se devuelve
       ``status: 3``; y un error del sistema se devuelve como ``status: 2``, ambos con HTTP ``200``.
   * - 400
     - Error de validación de los parámetros de la solicitud. El ``status`` del cuerpo de la respuesta será ``1``.
       Este código también se devuelve cuando se intenta obtener un recurso inexistente.
   * - 401
     - Cuando ocurre una excepción relacionada con la autenticación de inicio de sesión. El ``status`` del cuerpo de la respuesta será ``3``.
       Tenga en cuenta que, si el token de acceso no se especifica o es inválido, no se devuelve este código, sino HTTP ``200`` con
       ``status: 3``.

.. note::

   Admin API no devuelve códigos de estado HTTP como ``403``, ``404`` o ``500``.
   Tanto los permisos insuficientes como la inexistencia de un recurso se indican mediante el
   ``status`` incluido en el cuerpo de la respuesta HTTP ``200`` o ``400``.

APIs Disponibles
================

|Fess| proporciona las siguientes Admin APIs.

Configuración de Rastreo
------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Descripción
   * - :doc:`api-admin-webconfig`
     - Configuración de rastreo web
   * - :doc:`api-admin-fileconfig`
     - Configuración de rastreo de archivos
   * - :doc:`api-admin-dataconfig`
     - Configuración de almacén de datos

.. note::

   Además, los siguientes recursos relacionados con credenciales de autenticación y control de rastreo
   también se ofrecen como API (actualmente no tienen una página propia): ``webauth`` (autenticación web), ``fileauth`` (autenticación de archivos),
   ``reqheader`` (encabezados de solicitud), ``pathmap`` (mapeo de rutas),
   ``duplicatehost`` (hosts duplicados), ``searchlist`` (operaciones de búsqueda/lista de documentos).

Gestión de Índices
------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Descripción
   * - :doc:`api-admin-documents`
     - Operaciones masivas de documentos
   * - :doc:`api-admin-crawlinginfo`
     - Información de rastreo
   * - :doc:`api-admin-failureurl`
     - Gestión de URLs fallidas
   * - :doc:`api-admin-backup`
     - Copia de seguridad/Restauración

Programador
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Descripción
   * - :doc:`api-admin-scheduler`
     - Programación de trabajos
   * - :doc:`api-admin-joblog`
     - Obtención de registros de trabajos

Gestión de Usuarios y Permisos
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Descripción
   * - :doc:`api-admin-user`
     - Gestión de usuarios
   * - :doc:`api-admin-role`
     - Gestión de roles
   * - :doc:`api-admin-group`
     - Gestión de grupos
   * - :doc:`api-admin-accesstoken`
     - Gestión de tokens API

Ajuste de Búsqueda
------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Descripción
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
     - Gestión de sugerencias

Sistema
-------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Descripción
   * - :doc:`api-admin-general`
     - Configuración general
   * - :doc:`api-admin-systeminfo`
     - Información del sistema
   * - :doc:`api-admin-stats`
     - Estadísticas del sistema
   * - :doc:`api-admin-log`
     - Obtención de registros
   * - :doc:`api-admin-searchlist`
     - Búsqueda y gestión de documentos
   * - :doc:`api-admin-storage`
     - Gestión de almacenamiento
   * - :doc:`api-admin-plugin`
     - Gestión de plugins

Diccionario
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Descripción
   * - :doc:`api-admin-dict`
     - Gestión de diccionarios (sinónimos, palabras vacías, etc.)

Ejemplos de Uso
===============

Crear Configuración de Rastreo Web
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

   Al crear una configuración de rastreo web, son obligatorios ``name``, ``urls``, ``userAgent``, ``numOfThread``,
   ``intervalTime``, ``boost``, ``available`` y ``sortOrder``. Si se omiten,
   se produce un error de validación (``status: 1``). ``available`` se especifica como una cadena de texto y
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

Información de Referencia
=========================

- :doc:`../api-overview` - Visión general de API
- :doc:`../../admin/accesstoken-guide` - Guía de gestión de tokens de acceso
