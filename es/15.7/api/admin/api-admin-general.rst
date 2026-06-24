==========================
API de General
==========================

Descripcion General
===================

La API de General es una API para gestionar la configuracion general de |Fess|
(configuracion de todo el sistema). Puede obtener y actualizar configuraciones
relacionadas con el rastreo, el registro, la visualizacion de resultados de
busqueda, las sugerencias, los periodos de retencion de registros, las
notificaciones, la autenticacion (LDAP / SSO) y la integracion con
almacenamiento en la nube. Estas configuraciones corresponden a los ajustes
"General" en la interfaz de administracion (:doc:`../../admin/general-guide`).

URL Base
========

::

    /api/admin/general

Para acceder a esta API se requiere un token de acceso con el permiso
``Radmin-api``. Consulte :doc:`api-admin-overview` para obtener detalles sobre
la autenticacion.

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
==============================

Solicitud
---------

::

    GET /api/admin/general

Este endpoint no acepta parametros de consulta.

Respuesta
---------

``response.setting`` contiene la configuracion general actual. La respuesta
incluye todos los campos de configuracion actualizables; el ejemplo a
continuacion muestra solo los campos representativos. Los ajustes de
activacion/desactivacion se expresan como las cadenas ``"true"`` /
``"false"``, mientras que valores como los dias de retencion y el numero de
hilos se expresan como numeros.

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

   Lo anterior muestra solo campos representativos a modo de ejemplo. El objeto ``setting``
   real en la respuesta contiene todos los campos de configuracion general (rastreo, busqueda,
   notificaciones, LDAP, SSO, almacenamiento, etc.). Consulte la pagina de ajustes "General"
   en la interfaz de administracion para la lista completa.

.. note::

   Por razones de seguridad, los campos que contienen credenciales no se devuelven con sus
   valores reales.

   - La contrasena del administrador LDAP ``ldapAdminSecurityCredentials`` siempre se
     devuelve como ``null``.
   - Otros secretos (``storageAccessKey`` / ``storageSecretKey`` /
     ``oicClientId`` / ``oicClientSecret`` / ``spnegoPreauthPassword`` /
     ``entraidClientId`` / ``entraidClientSecret``) se devuelven enmascarados como
     ``"**********"`` cuando estan configurados, o como una cadena vacia (``""``) cuando
     no lo estan.

Actualizar Configuracion General
=================================

Solicitud
---------

::

    PUT /api/admin/general
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

Las actualizaciones se procesan como una actualizacion parcial (merge). El
servidor carga la configuracion actual y luego sobreescribe unicamente los
campos no nulos (no ``null``) incluidos en la solicitud. Los campos no
incluidos en la solicitud, y los campos establecidos como ``null``, conservan
sus valores existentes.

.. warning::

   Los siguientes cuatro campos son requeridos y DEBEN incluirse en CADA solicitud PUT,
   incluso en una actualizacion parcial:

   - ``dayForCleanup``
   - ``crawlingThreadCount``
   - ``failureCountThreshold``
   - ``csvFileEncoding``

   Si falta alguno de ellos, la solicitud falla la validacion y la API devuelve HTTP 400
   con ``status: 1`` y un ``message`` de error. Dado que el valor enviado sobreescribe la
   configuracion existente, para mantener un valor sin cambios primero recuperelo con
   ``GET`` y envielo tal cual. Todos los demas campos son opcionales; los campos omitidos
   conservan sus valores existentes.

.. note::

   Los campos numericos tienen validacion de tipo y rango. Enviar un valor que no pueda
   interpretarse como un entero, o un valor fuera del rango permitido, falla la validacion
   (HTTP 400 con ``status: 1``). El rango valido de cada campo numerico se indica en la
   tabla de campos a continuacion.

.. note::

   Para los campos de activacion/desactivacion (tipo ``available``), solo ``"true"`` o
   ``"on"`` (ambos sin distincion de mayusculas y minusculas) significan habilitado.
   Cualquier otro valor (como ``"false"`` o una cadena vacia) se trata como deshabilitado
   (``false``). El valor existente se mantiene unicamente cuando el campo se omite (no se
   envia). En la respuesta GET, estos campos se devuelven como las cadenas ``"true"`` /
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

Los elementos de configuracion son muy variados. A continuacion se muestran
los campos representativos (todos los campos corresponden a los ajustes
"General" en la interfaz de administracion). Los ajustes de
activacion/desactivacion se especifican como las cadenas ``"true"`` /
``"false"``.

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
     - Numero de dias que se conservan los documentos rastreados (-1=limpieza deshabilitada; rango: -1 a 1000)
   * - ``crawlingThreadCount``
     - Si
     - Numero de hilos usados para el rastreo (rango: 0 a 100)
   * - ``failureCountThreshold``
     - Si
     - Umbral del numero de fallos para detener el rastreo de una URL (-1=deshabilitado; rango: -1 a 10000)
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
   * - ``appValue``
     - No
     - Valor de configuracion adicional especifico de la aplicacion
   * - ``virtualHostValue``
     - No
     - Configuracion de host virtual (para entornos multi-tenant)
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
   * - ``loginLink``
     - No
     - Habilitar o deshabilitar la visualizacion del enlace de inicio de sesion en la pantalla de busqueda
   * - ``thumbnail``
     - No
     - Habilitar/deshabilitar la generacion de miniaturas
   * - ``resultCollapsed``
     - No
     - Habilitar o deshabilitar el colapso de documentos similares en los resultados de busqueda
   * - ``ignoreFailureType``
     - No
     - Tipos de fallo de rastreo a ignorar
   * - ``crawlingUserAgent``
     - No
     - Cadena User-Agent enviada durante el rastreo
   * - ``purgeSearchLogDay``
     - No
     - Numero de dias que se conservan los registros de busqueda (-1=deshabilitado; rango: -1 a 100000)
   * - ``purgeJobLogDay``
     - No
     - Numero de dias que se conservan los registros de trabajos (-1=deshabilitado; rango: -1 a 100000)
   * - ``purgeUserInfoDay``
     - No
     - Numero de dias que se conserva la informacion de usuario (-1=deshabilitado; rango: -1 a 100000)
   * - ``purgeSuggestSearchLogDay``
     - No
     - Numero de dias que se conservan los registros de busqueda de sugerencias (0=deshabilitado; rango: 0 a 100000)
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
   * - ``searchUseBrowserLocale``
     - No
     - Si se utiliza el idioma del navegador para la busqueda
   * - ``ragLlmName``
     - No
     - Nombre del proveedor LLM utilizado para RAG
   * - ``llmLogLevel``
     - No
     - Nivel de registro para los paquetes relacionados con LLM

Campos Relacionados con Autenticacion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Las configuraciones relacionadas con LDAP y SSO (OpenID Connect, SAML,
SPNEGO, Entra ID) tambien se gestionan con esta API. A continuacion se
muestran los campos representativos (todos los campos corresponden a los
ajustes "General" en la interfaz de administracion).

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
   * - ``ldapMemberofAttribute``
     - Nombre del atributo LDAP que indica la pertenencia a un grupo
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

Tambien se puede gestionar la configuracion de integracion con almacenamiento
en la nube (S3 / GCS).

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Campo
     - Descripcion
   * - ``storageType``
     - Tipo de almacenamiento (``auto`` / ``s3`` / ``gcs``)
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

.. note::

   Los campos de tipo secreto como ``ldapAdminSecurityCredentials``,
   ``storageAccessKey`` / ``storageSecretKey``, ``oicClientId`` / ``oicClientSecret``,
   ``entraidClientId`` / ``entraidClientSecret`` y ``spnegoPreauthPassword`` conservan su
   valor almacenado (no se actualizan) cuando se envia el valor enmascarado ``"**********"``
   tal cual. Envie el valor real solo cuando desee cambiarlo.

   Dado que esta comprobacion se basa en si la cadena queda vacia tras eliminar los
   asteriscos, enviar una cadena vacia (``""``) o un valor compuesto unicamente de
   asteriscos tampoco actualiza el valor. Por lo tanto, estos campos de tipo secreto no
   pueden borrarse a un valor vacio mediante la API.

Respuesta
---------

En caso de actualizacion exitosa, solo se devuelven ``version`` y ``status``
(no se incluyen ``id`` ni ``created``).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Si la actualizacion falla (por ejemplo, debido a un error de validacion), la API
devuelve HTTP 400 y ``status`` se establece en un valor distinto de cero (``1``
para un error de validacion), y ``message`` contiene los detalles del error.
Consulte :doc:`api-admin-overview` para la lista de valores de ``status``.

Ejemplos de Uso
===============

.. note::

   Los ejemplos a continuacion incluyen los campos requeridos (``dayForCleanup``,
   ``crawlingThreadCount``, ``failureCountThreshold``, ``csvFileEncoding``). Como estos
   deben enviarse siempre independientemente de lo que se desee cambiar, recupere los
   valores actuales con ``GET`` e incluyalos en la operacion real (los ejemplos a
   continuacion usan los valores predeterminados).

Actualizar la Configuracion de Rastreo
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

Actualizar el Periodo de Retencion de Registros
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

Actualizar la Configuracion de Sugerencias
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

Informacion de Referencia
==========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-systeminfo` - API de informacion del sistema
- :doc:`../../admin/general-guide` - Guia de configuracion general
