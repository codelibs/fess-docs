==========================
API de General
==========================

Vision General
==============

La API de General es para gestionar la configuracion general de |Fess|.
Puede obtener y actualizar configuraciones relacionadas con todo el sistema.

URL Base
========

::

    /api/admin/general

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
     - Obtener configuracion general
   * - PUT
     - /
     - Actualizar configuracion general

Obtener Configuracion General
=============================

Solicitud
---------

::

    GET /api/admin/general

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "incrementalCrawling": "true",
          "dayForCleanup": -1,
          "crawlingThreadCount": 5,
          "searchLog": "true",
          "userInfo": "true",
          "userFavorite": "false",
          "webApiJson": "true",
          "defaultLabelValue": "",
          "defaultSortValue": "",
          "appendQueryParameter": "false",
          "loginRequired": "false",
          "thumbnail": "true",
          "failureCountThreshold": -1,
          "popularWord": "true",
          "csvFileEncoding": "UTF-8",
          "purgeSearchLogDay": 30,
          "purgeJobLogDay": 30,
          "purgeUserInfoDay": 30,
          "purgeSuggestSearchLogDay": 30,
          "notificationTo": "",
          "suggestSearchLog": "true",
          "suggestDocuments": "true",
          "ldapProviderUrl": "ldap://localhost:389/",
          "ldapBaseDn": "dc=example,dc=com",
          "ldapAdminSecurityPrincipal": "cn=admin,dc=example,dc=com",
          "ldapAdminSecurityCredentials": null,
          "logLevel": "",
          "ssoType": "none",
          "storageType": "",
          "notificationLogin": "",
          "notificationSearchTop": ""
        }
      }
    }

.. note::

   Por razones de seguridad, ``ldapAdminSecurityCredentials``, que es la contrasena del administrador LDAP,
   siempre se reemplaza por ``null`` en la respuesta (fuente:
   ``ApiAdminGeneralAction.java:71``).

Actualizar Configuracion General
================================

Solicitud
---------

::

    PUT /api/admin/general
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

La actualizacion se procesa como una actualizacion parcial (merge). Los campos no incluidos en la solicitud
conservan su valor existente, y los campos con valor ``null`` se ignoran (fuente:
``ApiAdminGeneralAction.java:84-90``).

.. code-block:: json

    {
      "incrementalCrawling": "true",
      "dayForCleanup": -1,
      "crawlingThreadCount": 10,
      "failureCountThreshold": 100,
      "csvFileEncoding": "UTF-8",
      "popularWord": "true"
    }

Campos Principales
~~~~~~~~~~~~~~~~~~

Los elementos de configuracion son muy variados. A continuacion se muestran los campos representativos
(para todos los campos consulte ``EditForm.java``). Las configuraciones de activacion/desactivacion del tipo ``available``
se expresan como cadenas ``"true"`` / ``"false"``.

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Campo
     - Requerido
     - Descripcion
   * - ``incrementalCrawling``
     - No
     - Habilitar/deshabilitar el rastreo incremental
   * - ``dayForCleanup``
     - Si
     - Numero de dias que se conservan los documentos rastreados (-1=limpieza deshabilitada)
   * - ``crawlingThreadCount``
     - Si
     - Numero de hilos usados para el rastreo
   * - ``failureCountThreshold``
     - Si
     - Umbral del numero de fallos para detener el rastreo de una URL (-1=deshabilitado)
   * - ``csvFileEncoding``
     - Si
     - Codificacion de la exportacion CSV
   * - ``searchLog``
     - No
     - Habilitar/deshabilitar el registro de consultas de busqueda
   * - ``userInfo``
     - No
     - Habilitar/deshabilitar el registro de informacion de usuario
   * - ``userFavorite``
     - No
     - Habilitar/deshabilitar la funcion de favoritos
   * - ``webApiJson``
     - No
     - Habilitar/deshabilitar la Web API JSON
   * - ``popularWord``
     - No
     - Habilitar/deshabilitar la agregacion y visualizacion de palabras populares
   * - ``defaultLabelValue``
     - No
     - Valor de etiqueta predeterminado
   * - ``defaultSortValue``
     - No
     - Orden de clasificacion predeterminado
   * - ``appendQueryParameter``
     - No
     - Agregar parametros de consulta a la URL de los resultados de busqueda
   * - ``loginRequired``
     - No
     - Si se requiere inicio de sesion para buscar
   * - ``thumbnail``
     - No
     - Habilitar/deshabilitar la generacion de miniaturas
   * - ``ignoreFailureType``
     - No
     - Tipos de fallo de rastreo a ignorar
   * - ``purgeSearchLogDay``
     - No
     - Numero de dias que se conservan los registros de busqueda (-1=deshabilitado)
   * - ``purgeJobLogDay``
     - No
     - Numero de dias que se conservan los registros de trabajos (-1=deshabilitado)
   * - ``purgeUserInfoDay``
     - No
     - Numero de dias que se conserva la informacion de usuario (-1=deshabilitado)
   * - ``purgeSuggestSearchLogDay``
     - No
     - Numero de dias que se conservan los registros de busqueda de sugerencias (0=deshabilitado)
   * - ``purgeByBots``
     - No
     - User-Agent de bots cuyos registros de busqueda se descartan
   * - ``notificationTo``
     - No
     - Direccion de correo electronico de destino de las notificaciones del sistema
   * - ``notificationLogin``
     - No
     - Mensaje de notificacion que se muestra en la pagina de inicio de sesion
   * - ``notificationSearchTop``
     - No
     - Mensaje de notificacion que se muestra en la pagina principal de busqueda
   * - ``notificationAdvanceSearch``
     - No
     - Mensaje de notificacion que se muestra en la pagina de busqueda avanzada
   * - ``suggestSearchLog``
     - No
     - Habilitar/deshabilitar las sugerencias a partir de los registros de busqueda
   * - ``suggestDocuments``
     - No
     - Habilitar/deshabilitar las sugerencias a partir de los documentos
   * - ``logLevel``
     - No
     - Nivel de registro del log del sistema
   * - ``logNotificationEnabled``
     - No
     - Habilitar/deshabilitar la notificacion de logs ERROR/WARN
   * - ``logNotificationLevel``
     - No
     - Nivel de notificacion de logs
   * - ``slackWebhookUrls``
     - No
     - URL de Slack Webhook para notificaciones
   * - ``googleChatWebhookUrls``
     - No
     - URL de Google Chat Webhook para notificaciones

Campos Relacionados con Autenticacion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Las configuraciones relacionadas con LDAP y SSO (OpenID Connect, SAML, SPNEGO, Entra ID) tambien
se gestionan con esta API. A continuacion se muestran los campos representativos
(para todos los campos consulte ``EditForm.java``).

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Campo
     - Descripcion
   * - ``ldapProviderUrl``
     - URL de conexion LDAP
   * - ``ldapBaseDn``
     - DN base de LDAP
   * - ``ldapSecurityPrincipal``
     - Principal de seguridad para el enlace (bind) LDAP
   * - ``ldapAdminSecurityPrincipal``
     - Principal de seguridad para operaciones administrativas LDAP
   * - ``ldapAdminSecurityCredentials``
     - Contrasena del administrador LDAP (se reemplaza por ``null`` en la respuesta)
   * - ``ldapAccountFilter`` / ``ldapGroupFilter``
     - Filtros de busqueda de usuarios/grupos
   * - ``ssoType``
     - Tipo de SSO (``none`` / ``oic`` / ``saml`` / ``spnego`` / ``entraid``)
   * - ``oicClientId`` / ``oicClientSecret`` / ``oicAuthServerUrl`` y otros
     - Configuracion de OpenID Connect
   * - ``samlIdpEntityid`` / ``samlSpEntityid`` y otros
     - Configuracion de SAML
   * - ``spnegoKrb5Conf`` / ``spnegoLoginConf`` y otros
     - Configuracion de SPNEGO
   * - ``entraidClientId`` / ``entraidTenant`` y otros
     - Configuracion de Microsoft Entra ID

Campos Relacionados con Almacenamiento
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tambien se puede gestionar la configuracion de integracion con almacenamiento en la nube (S3 / GCS).

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Campo
     - Descripcion
   * - ``storageType``
     - Tipo de almacenamiento (``s3`` / ``gcs`` / ``auto``)
   * - ``storageEndpoint``
     - URL del endpoint del almacenamiento
   * - ``storageAccessKey`` / ``storageSecretKey``
     - Clave de acceso/clave secreta para la autenticacion
   * - ``storageBucket``
     - Nombre del bucket
   * - ``storageRegion``
     - Region de S3
   * - ``storageProjectId`` / ``storageCredentialsPath``
     - ID de proyecto de GCS / ruta del archivo de credenciales

Respuesta
---------

En caso de actualizacion exitosa solo se devuelve ``status`` (no se incluyen ``id`` ni ``created``).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Ejemplos de Uso
===============

Actualizar la Configuracion de Rastreo
--------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "incrementalCrawling": "true",
           "crawlingThreadCount": 10,
           "failureCountThreshold": 100,
           "dayForCleanup": -1,
           "csvFileEncoding": "UTF-8"
         }'

Actualizar el Periodo de Retencion de Registros
-----------------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "purgeSearchLogDay": 90,
           "purgeJobLogDay": 90,
           "purgeUserInfoDay": 90
         }'

Actualizar la Configuracion de Sugerencias
------------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestSearchLog": "true",
           "suggestDocuments": "true"
         }'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-systeminfo` - API de informacion del sistema
- :doc:`../../admin/general-guide` - Guia de configuracion general
