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

   Lo anterior muestra solo campos representativos a modo de ejemplo. El objeto ``setting``
   real en la respuesta contiene todos los campos de configuracion general (rastreo, busqueda,
   notificaciones, LDAP, SSO, almacenamiento, etc.). Consulte ``EditForm.java`` para la lista
   completa.

.. note::

   Por razones de seguridad, los campos que contienen credenciales no se devuelven con sus
   valores reales.

   - La contrasena del administrador LDAP ``ldapAdminSecurityCredentials`` siempre se
     reemplaza por ``null``.
   - Otros secretos (``storageAccessKey`` / ``storageSecretKey`` /
     ``oicClientId`` / ``oicClientSecret`` / ``spnegoPreauthPassword`` /
     ``entraidClientId`` / ``entraidClientSecret``) se devuelven enmascarados como
     ``"**********"`` cuando estan configurados.

Actualizar Configuracion General
================================

Solicitud
---------

::

    PUT /api/admin/general
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

Las actualizaciones se procesan como una combinacion parcial (merge): los valores del
request se fusionan con la configuracion actual; los campos no incluidos (campos con
valor ``null``) se ignoran y los valores existentes se mantienen.

.. warning::

   Los siguientes cuatro campos tienen la restriccion ``@Required`` y DEBEN incluirse en
   CADA solicitud PUT. Omitirlos resulta en un error de validacion (HTTP 400).

   - ``dayForCleanup``
   - ``crawlingThreadCount``
   - ``failureCountThreshold``
   - ``csvFileEncoding``

   No pueden omitirse ni siquiera en una actualizacion parcial. Dado que el valor enviado
   sobreescribe la configuracion existente, si no desea cambiar un valor, primero recupere
   el valor actual con ``GET`` y envielo tal cual. Todos los demas campos son opcionales;
   los campos omitidos conservan sus valores existentes.

.. note::

   Los campos numericos tienen validacion de tipo y rango. Enviar un valor que no pueda
   interpretarse como un entero, o un valor fuera del rango permitido, resulta en un error
   de validacion (HTTP 400).

   - ``dayForCleanup``: ``-1`` a ``1000``
   - ``crawlingThreadCount``: ``0`` a ``100``
   - ``failureCountThreshold``: ``-1`` a ``10000``
   - ``purgeSearchLogDay`` / ``purgeJobLogDay`` / ``purgeUserInfoDay``: ``-1`` a ``100000``
   - ``purgeSuggestSearchLogDay``: ``0`` a ``100000``

.. note::

   Para los campos de activacion/desactivacion (tipo ``available``), solo ``"true"`` o
   ``"on"`` (ambos sin distincion de mayusculas y minusculas) significan habilitado.
   Cualquier otro valor (como ``"false"`` o una cadena vacia) se trata como deshabilitado
   (``false``). El valor existente se mantiene unicamente cuando el campo se omite (no se
   envia). Tenga en cuenta que en la respuesta GET, estos campos se devuelven como las
   cadenas ``"true"`` / ``"false"``.

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
(para todos los campos consulte ``EditForm.java``). El cuerpo de la solicitud/respuesta de la API es
``EditBody``, que extiende ``EditForm``, pero las definiciones de campos se encuentran en ``EditForm``.
Las configuraciones de activacion/desactivacion del tipo ``available``
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

.. note::

   Dado que los cuatro campos ``dayForCleanup``, ``crawlingThreadCount``,
   ``failureCountThreshold`` y ``csvFileEncoding`` son obligatorios en las solicitudes PUT,
   todos los ejemplos a continuacion los incluyen. Como los valores enviados sobreescriben
   la configuracion existente, en un uso real envie los valores actuales obtenidos con
   ``GET`` (los ejemplos a continuacion usan los valores predeterminados).

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
           "dayForCleanup": -1,
           "crawlingThreadCount": 5,
           "failureCountThreshold": -1,
           "csvFileEncoding": "UTF-8",
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
           "dayForCleanup": -1,
           "crawlingThreadCount": 5,
           "failureCountThreshold": -1,
           "csvFileEncoding": "UTF-8",
           "suggestSearchLog": "true",
           "suggestDocuments": "true"
         }'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-systeminfo` - API de informacion del sistema
- :doc:`../../admin/general-guide` - Guia de configuracion general
