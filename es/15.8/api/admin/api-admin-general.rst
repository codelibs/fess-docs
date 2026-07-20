==========================
API de General
==========================

Descripción General
===================

La API de General es una API para gestionar la configuración general de |Fess|
(configuración de todo el sistema). Puede obtener y actualizar configuraciones
relacionadas con el rastreo, el registro, la visualización de resultados de
búsqueda, las sugerencias, los períodos de retención de registros, las
notificaciones, la autenticación (LDAP / SSO) y la integración con
almacenamiento en la nube. Estas configuraciones corresponden a los ajustes
"General" en la interfaz de administración (:doc:`../../admin/general-guide`).

URL Base
========

::

    /api/admin/general

Para acceder a esta API se requiere un token de acceso con el permiso
``Radmin-api``. Consulte :doc:`api-admin-overview` para obtener detalles sobre
la autenticación.

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Método
     - Ruta
     - Descripción
   * - GET
     - /
     - Obtener configuración general
   * - PUT
     - /
     - Actualizar configuración general

Obtener Configuración General
==============================

Solicitud
---------

::

    GET /api/admin/general

Este endpoint no acepta parámetros de consulta.

Respuesta
---------

``response.setting`` contiene la configuración general actual. La respuesta
incluye todos los campos de configuración actualizables; el ejemplo a
continuación muestra solo los campos representativos. Los ajustes de
activación/desactivación se expresan como las cadenas ``"true"`` /
``"false"``, mientras que valores como los días de retención y el número de
hilos se expresan como números.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
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

   Lo anterior muestra solo campos representativos a modo de ejemplo. El objeto ``setting``
   real en la respuesta contiene todos los campos de configuración general (rastreo, búsqueda,
   notificaciones, LDAP, SSO, almacenamiento, etc.). Consulte la página de ajustes "General"
   en la interfaz de administración para la lista completa.

.. note::

   Por razones de seguridad, los campos que contienen credenciales no se devuelven con sus
   valores reales.

   - La contraseña del administrador LDAP ``ldapAdminSecurityCredentials`` siempre se
     devuelve como ``null``.
   - Otros secretos (``storageAccessKey`` / ``storageSecretKey`` /
     ``oicClientId`` / ``oicClientSecret`` / ``spnegoPreauthPassword`` /
     ``entraidClientId`` / ``entraidClientSecret``) se devuelven enmascarados como
     ``"**********"`` cuando están configurados, o como una cadena vacía (``""``) cuando
     no lo están.

Actualizar Configuración General
=================================

Solicitud
---------

::

    PUT /api/admin/general
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

Las actualizaciones se procesan como una actualización parcial (merge). El
servidor carga la configuración actual y luego sobreescribe únicamente los
campos no nulos (no ``null``) incluidos en la solicitud. Los campos no
incluidos en la solicitud, y los campos establecidos como ``null``, conservan
sus valores existentes.

.. warning::

   Los siguientes cuatro campos son requeridos y DEBEN incluirse en CADA solicitud PUT,
   incluso en una actualización parcial:

   - ``dayForCleanup``
   - ``crawlingThreadCount``
   - ``failureCountThreshold``
   - ``csvFileEncoding``

   Si falta alguno de ellos, la solicitud falla la validación y la API devuelve HTTP 400
   con ``status: 1`` y un ``message`` de error. Dado que el valor enviado sobreescribe la
   configuración existente, para mantener un valor sin cambios primero recupérelo con
   ``GET`` y envíelo tal cual. Todos los demás campos son opcionales; los campos omitidos
   conservan sus valores existentes.

.. note::

   Los campos numéricos tienen validación de tipo y rango. Enviar un valor que no pueda
   interpretarse como un entero, o un valor fuera del rango permitido, falla la validación
   (HTTP 400 con ``status: 1``). El rango válido de cada campo numérico se indica en la
   tabla de campos a continuación.

.. note::

   Para los campos de activación/desactivación (tipo ``available``), solo ``"true"`` o
   ``"on"`` (ambos sin distinción de mayúsculas y minúsculas) significan habilitado.
   Cualquier otro valor (como ``"false"`` o una cadena vacía) se trata como deshabilitado
   (``false``). El valor existente se mantiene únicamente cuando el campo se omite (no se
   envía). En la respuesta GET, estos campos se devuelven como las cadenas ``"true"`` /
   ``"false"``.

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

Los elementos de configuración son muy variados. A continuación se muestran
los campos representativos (todos los campos corresponden a los ajustes
"General" en la interfaz de administración). Los ajustes de
activación/desactivación se especifican como las cadenas ``"true"`` /
``"false"``.

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Campo
     - Requerido
     - Descripción
   * - ``incrementalCrawling``
     - No
     - Habilitar/deshabilitar el rastreo incremental
   * - ``dayForCleanup``
     - Sí
     - Número de días que se conservan los documentos rastreados (-1=limpieza deshabilitada; rango: -1 a 1000)
   * - ``crawlingThreadCount``
     - Sí
     - Número de hilos usados para el rastreo (rango: 0 a 100)
   * - ``failureCountThreshold``
     - Sí
     - Umbral del número de fallos para detener el rastreo de una URL (-1=deshabilitado; rango: -1 a 10000)
   * - ``csvFileEncoding``
     - Sí
     - Codificación de la exportación CSV
   * - ``searchLog``
     - No
     - Habilitar/deshabilitar el registro de consultas de búsqueda
   * - ``userInfo``
     - No
     - Habilitar/deshabilitar el registro de información de usuario
   * - ``userFavorite``
     - No
     - Habilitar/deshabilitar la función de favoritos
   * - ``webApiJson``
     - No
     - Habilitar/deshabilitar la Web API JSON
   * - ``appValue``
     - No
     - Valor de configuración adicional específico de la aplicación
   * - ``virtualHostValue``
     - No
     - Configuración de host virtual (para entornos multi-tenant)
   * - ``popularWord``
     - No
     - Habilitar/deshabilitar la agregación y visualización de palabras populares
   * - ``defaultLabelValue``
     - No
     - Valor de etiqueta predeterminado
   * - ``defaultSortValue``
     - No
     - Orden de clasificación predeterminado
   * - ``appendQueryParameter``
     - No
     - Agregar parámetros de consulta a la URL de los resultados de búsqueda
   * - ``loginRequired``
     - No
     - Si se requiere inicio de sesión para buscar
   * - ``loginLink``
     - No
     - Habilitar o deshabilitar la visualización del enlace de inicio de sesión en la pantalla de búsqueda
   * - ``thumbnail``
     - No
     - Habilitar/deshabilitar la generación de miniaturas
   * - ``resultCollapsed``
     - No
     - Habilitar o deshabilitar el colapso de documentos similares en los resultados de búsqueda
   * - ``ignoreFailureType``
     - No
     - Tipos de fallo de rastreo a ignorar
   * - ``crawlingUserAgent``
     - No
     - Cadena User-Agent enviada durante el rastreo
   * - ``purgeSearchLogDay``
     - No
     - Número de días que se conservan los registros de búsqueda (-1=deshabilitado; rango: -1 a 100000)
   * - ``purgeJobLogDay``
     - No
     - Número de días que se conservan los registros de trabajos (-1=deshabilitado; rango: -1 a 100000)
   * - ``purgeUserInfoDay``
     - No
     - Número de días que se conserva la información de usuario (-1=deshabilitado; rango: -1 a 100000)
   * - ``purgeSuggestSearchLogDay``
     - No
     - Número de días que se conservan los registros de búsqueda de sugerencias (0=deshabilitado; rango: 0 a 100000)
   * - ``purgeByBots``
     - No
     - User-Agent de bots cuyos registros de búsqueda se descartan
   * - ``notificationTo``
     - No
     - Dirección de correo electrónico de destino de las notificaciones del sistema
   * - ``notificationLogin``
     - No
     - Mensaje de notificación que se muestra en la página de inicio de sesión
   * - ``notificationSearchTop``
     - No
     - Mensaje de notificación que se muestra en la página principal de búsqueda
   * - ``notificationAdvanceSearch``
     - No
     - Mensaje de notificación que se muestra en la página de búsqueda avanzada
   * - ``suggestSearchLog``
     - No
     - Habilitar/deshabilitar las sugerencias a partir de los registros de búsqueda
   * - ``suggestDocuments``
     - No
     - Habilitar/deshabilitar las sugerencias a partir de los documentos
   * - ``logLevel``
     - No
     - Nivel de registro del log del sistema
   * - ``logNotificationEnabled``
     - No
     - Habilitar/deshabilitar la notificación de logs ERROR/WARN
   * - ``logNotificationLevel``
     - No
     - Nivel de notificación de logs
   * - ``slackWebhookUrls``
     - No
     - URL de Slack Webhook para notificaciones
   * - ``googleChatWebhookUrls``
     - No
     - URL de Google Chat Webhook para notificaciones
   * - ``searchUseBrowserLocale``
     - No
     - Si se utiliza el idioma del navegador para la búsqueda
   * - ``ragLlmName``
     - No
     - Nombre del proveedor LLM utilizado para RAG
   * - ``llmLogLevel``
     - No
     - Nivel de registro para los paquetes relacionados con LLM

Campos Relacionados con Autenticación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Las configuraciones relacionadas con LDAP y SSO (OpenID Connect, SAML,
SPNEGO, Entra ID) también se gestionan con esta API. A continuación se
muestran los campos representativos (todos los campos corresponden a los
ajustes "General" en la interfaz de administración).

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Campo
     - Descripción
   * - ``ldapProviderUrl``
     - URL de conexión LDAP
   * - ``ldapBaseDn``
     - DN base de LDAP
   * - ``ldapSecurityPrincipal``
     - Principal de seguridad para el enlace (bind) LDAP
   * - ``ldapAdminSecurityPrincipal``
     - Principal de seguridad para operaciones administrativas LDAP
   * - ``ldapAdminSecurityCredentials``
     - Contraseña del administrador LDAP (se reemplaza por ``null`` en la respuesta)
   * - ``ldapAccountFilter`` / ``ldapGroupFilter``
     - Filtros de búsqueda de usuarios/grupos
   * - ``ldapMemberofAttribute``
     - Nombre del atributo LDAP que indica la pertenencia a un grupo
   * - ``ssoType``
     - Tipo de SSO (``none`` / ``oic`` / ``saml`` / ``spnego`` / ``entraid``)
   * - ``oicClientId`` / ``oicClientSecret`` / ``oicAuthServerUrl`` y otros
     - Configuración de OpenID Connect
   * - ``samlIdpEntityid`` / ``samlSpEntityid`` y otros
     - Configuración de SAML
   * - ``spnegoKrb5Conf`` / ``spnegoLoginConf`` y otros
     - Configuración de SPNEGO
   * - ``entraidClientId`` / ``entraidTenant`` y otros
     - Configuración de Microsoft Entra ID

Campos Relacionados con Almacenamiento
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

También se puede gestionar la configuración de integración con almacenamiento
en la nube (S3 / GCS).

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Campo
     - Descripción
   * - ``storageType``
     - Tipo de almacenamiento (``auto`` / ``s3`` / ``gcs``)
   * - ``storageEndpoint``
     - URL del endpoint del almacenamiento
   * - ``storageAccessKey`` / ``storageSecretKey``
     - Clave de acceso/clave secreta para la autenticación
   * - ``storageBucket``
     - Nombre del bucket
   * - ``storageRegion``
     - Región de S3
   * - ``storageProjectId`` / ``storageCredentialsPath``
     - ID de proyecto de GCS / ruta del archivo de credenciales

.. note::

   Los campos de tipo secreto como ``ldapAdminSecurityCredentials``,
   ``storageAccessKey`` / ``storageSecretKey``, ``oicClientId`` / ``oicClientSecret``,
   ``entraidClientId`` / ``entraidClientSecret`` y ``spnegoPreauthPassword`` conservan su
   valor almacenado (no se actualizan) cuando se envía el valor enmascarado ``"**********"``
   tal cual. Envíe el valor real solo cuando desee cambiarlo.

   Dado que esta comprobación se basa en si la cadena queda vacía tras eliminar los
   asteriscos, enviar una cadena vacía (``""``) o un valor compuesto únicamente de
   asteriscos tampoco actualiza el valor. Por lo tanto, estos campos de tipo secreto no
   pueden borrarse a un valor vacío mediante la API.

Respuesta
---------

En caso de actualización exitosa, solo se devuelven ``version`` y ``status``
(no se incluyen ``id`` ni ``created``).

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

Si la actualización falla (por ejemplo, debido a un error de validación), la API
devuelve HTTP 400 y ``status`` se establece en un valor distinto de cero (``1``
para un error de validación), y ``message`` contiene los detalles del error.
Consulte :doc:`api-admin-overview` para la lista de valores de ``status``.

Ejemplos de Uso
===============

.. note::

   Los ejemplos a continuación incluyen los campos requeridos (``dayForCleanup``,
   ``crawlingThreadCount``, ``failureCountThreshold``, ``csvFileEncoding``). Como estos
   deben enviarse siempre independientemente de lo que se desee cambiar, recupere los
   valores actuales con ``GET`` e inclúyalos en la operación real (los ejemplos a
   continuación usan los valores predeterminados).

Actualizar la Configuración de Rastreo
---------------------------------------

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

Actualizar el Período de Retención de Registros
-------------------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "dayForCleanup": -1,
           "crawlingThreadCount": 5,
           "failureCountThreshold": -1,
           "csvFileEncoding": "UTF-8",
           "purgeSearchLogDay": 90,
           "purgeJobLogDay": 90,
           "purgeUserInfoDay": 90
         }'

Actualizar la Configuración de Sugerencias
-------------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "dayForCleanup": -1,
           "crawlingThreadCount": 5,
           "failureCountThreshold": -1,
           "csvFileEncoding": "UTF-8",
           "suggestSearchLog": "true",
           "suggestDocuments": "true"
         }'

Información de Referencia
==========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-systeminfo` - API de información del sistema
- :doc:`../../admin/general-guide` - Guía de configuración general
