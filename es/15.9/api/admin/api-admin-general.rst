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
        "version": "15.9.0",
        "status": 0,
        "setting": {
          "incremental_crawling": "true",
          "day_for_cleanup": -1,
          "crawling_thread_count": 5,
          "search_log": "true",
          "user_info": "true",
          "user_favorite": "false",
          "web_api_json": "true",
          "default_label_value": "",
          "default_sort_value": "",
          "append_query_parameter": "false",
          "login_required": "false",
          "thumbnail": "true",
          "failure_count_threshold": -1,
          "popular_word": "true",
          "csv_file_encoding": "UTF-8",
          "purge_search_log_day": 30,
          "purge_job_log_day": 30,
          "purge_user_info_day": 30,
          "purge_suggest_search_log_day": 30,
          "notification_to": "",
          "suggest_search_log": "true",
          "suggest_documents": "true",
          "ldap_provider_url": "ldap://localhost:389/",
          "ldap_base_dn": "dc=example,dc=com",
          "ldap_admin_security_principal": "cn=admin,dc=example,dc=com",
          "log_level": "",
          "sso_type": "none",
          "storage_type": "",
          "notification_login": "",
          "notification_search_top": ""
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

   - La contraseña del administrador LDAP ``ldap_admin_security_credentials`` nunca se
     incluye en la respuesta.
   - Otros secretos (``storage_access_key`` / ``storage_secret_key`` /
     ``oic_client_id`` / ``oic_client_secret`` / ``spnego_preauth_password`` /
     ``entraid_client_id`` / ``entraid_client_secret``) se devuelven enmascarados como
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

   - ``day_for_cleanup``
   - ``crawling_thread_count``
   - ``failure_count_threshold``
   - ``csv_file_encoding``

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
      "incremental_crawling": "true",
      "day_for_cleanup": -1,
      "crawling_thread_count": 10,
      "failure_count_threshold": 100,
      "csv_file_encoding": "UTF-8",
      "popular_word": "true"
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
   * - ``incremental_crawling``
     - No
     - Habilitar/deshabilitar el rastreo incremental
   * - ``day_for_cleanup``
     - Sí
     - Número de días que se conservan los documentos rastreados (-1=limpieza deshabilitada; rango: -1 a 1000)
   * - ``crawling_thread_count``
     - Sí
     - Número de hilos usados para el rastreo (rango: 0 a 100)
   * - ``failure_count_threshold``
     - Sí
     - Umbral del número de fallos para detener el rastreo de una URL (-1=deshabilitado; rango: -1 a 10000)
   * - ``csv_file_encoding``
     - Sí
     - Codificación de la exportación CSV
   * - ``search_log``
     - No
     - Habilitar/deshabilitar el registro de consultas de búsqueda
   * - ``user_info``
     - No
     - Habilitar/deshabilitar el registro de información de usuario
   * - ``user_favorite``
     - No
     - Habilitar/deshabilitar la función de favoritos
   * - ``web_api_json``
     - No
     - Habilitar/deshabilitar la Web API JSON
   * - ``app_value``
     - No
     - Valor de configuración adicional específico de la aplicación
   * - ``virtual_host_value``
     - No
     - Configuración de host virtual (para entornos multi-tenant)
   * - ``popular_word``
     - No
     - Habilitar/deshabilitar la agregación y visualización de palabras populares
   * - ``default_label_value``
     - No
     - Valor de etiqueta predeterminado
   * - ``default_sort_value``
     - No
     - Orden de clasificación predeterminado
   * - ``append_query_parameter``
     - No
     - Agregar parámetros de consulta a la URL de los resultados de búsqueda
   * - ``login_required``
     - No
     - Si se requiere inicio de sesión para buscar
   * - ``login_link``
     - No
     - Habilitar o deshabilitar la visualización del enlace de inicio de sesión en la pantalla de búsqueda
   * - ``thumbnail``
     - No
     - Habilitar/deshabilitar la generación de miniaturas
   * - ``result_collapsed``
     - No
     - Habilitar o deshabilitar el colapso de documentos similares en los resultados de búsqueda
   * - ``ignore_failure_type``
     - No
     - Tipos de fallo de rastreo a ignorar
   * - ``crawling_user_agent``
     - No
     - Cadena User-Agent enviada durante el rastreo
   * - ``purge_search_log_day``
     - No
     - Número de días que se conservan los registros de búsqueda (-1=deshabilitado; rango: -1 a 100000)
   * - ``purge_job_log_day``
     - No
     - Número de días que se conservan los registros de trabajos (-1=deshabilitado; rango: -1 a 100000)
   * - ``purge_user_info_day``
     - No
     - Número de días que se conserva la información de usuario (-1=deshabilitado; rango: -1 a 100000)
   * - ``purge_suggest_search_log_day``
     - No
     - Número de días que se conservan los registros de búsqueda de sugerencias (0=deshabilitado; rango: 0 a 100000)
   * - ``purge_by_bots``
     - No
     - User-Agent de bots cuyos registros de búsqueda se descartan
   * - ``notification_to``
     - No
     - Dirección de correo electrónico de destino de las notificaciones del sistema
   * - ``notification_login``
     - No
     - Mensaje de notificación que se muestra en la página de inicio de sesión
   * - ``notification_search_top``
     - No
     - Mensaje de notificación que se muestra en la página principal de búsqueda
   * - ``notification_advance_search``
     - No
     - Mensaje de notificación que se muestra en la página de búsqueda avanzada
   * - ``suggest_search_log``
     - No
     - Habilitar/deshabilitar las sugerencias a partir de los registros de búsqueda
   * - ``suggest_documents``
     - No
     - Habilitar/deshabilitar las sugerencias a partir de los documentos
   * - ``log_level``
     - No
     - Nivel de registro del log del sistema
   * - ``log_notification_enabled``
     - No
     - Habilitar/deshabilitar la notificación de logs ERROR/WARN
   * - ``log_notification_level``
     - No
     - Nivel de notificación de logs
   * - ``slack_webhook_urls``
     - No
     - URL de Slack Webhook para notificaciones
   * - ``google_chat_webhook_urls``
     - No
     - URL de Google Chat Webhook para notificaciones
   * - ``search_use_browser_locale``
     - No
     - Si se utiliza el idioma del navegador para la búsqueda
   * - ``rag_llm_name``
     - No
     - Nombre del proveedor LLM utilizado para RAG
   * - ``llm_log_level``
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
   * - ``ldap_provider_url``
     - URL de conexión LDAP
   * - ``ldap_base_dn``
     - DN base de LDAP
   * - ``ldap_security_principal``
     - Principal de seguridad para el enlace (bind) LDAP
   * - ``ldap_admin_security_principal``
     - Principal de seguridad para operaciones administrativas LDAP
   * - ``ldap_admin_security_credentials``
     - Contraseña del administrador LDAP (nunca se incluye en la respuesta)
   * - ``ldap_account_filter`` / ``ldap_group_filter``
     - Filtros de búsqueda de usuarios/grupos
   * - ``ldap_memberof_attribute``
     - Nombre del atributo LDAP que indica la pertenencia a un grupo
   * - ``sso_type``
     - Tipo de SSO (``none`` / ``oic`` / ``saml`` / ``spnego`` / ``entraid``)
   * - ``oic_client_id`` / ``oic_client_secret`` / ``oic_auth_server_url`` y otros
     - Configuración de OpenID Connect
   * - ``saml_idp_entityid`` / ``saml_sp_entityid`` y otros
     - Configuración de SAML
   * - ``spnego_krb5_conf`` / ``spnego_login_conf`` y otros
     - Configuración de SPNEGO
   * - ``entraid_client_id`` / ``entraid_tenant`` y otros
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
   * - ``storage_type``
     - Tipo de almacenamiento (``auto`` / ``s3`` / ``gcs``)
   * - ``storage_endpoint``
     - URL del endpoint del almacenamiento
   * - ``storage_access_key`` / ``storage_secret_key``
     - Clave de acceso/clave secreta para la autenticación
   * - ``storage_bucket``
     - Nombre del bucket
   * - ``storage_region``
     - Región de S3
   * - ``storage_project_id`` / ``storage_credentials_path``
     - ID de proyecto de GCS / ruta del archivo de credenciales

.. note::

   Los campos de tipo secreto como ``ldap_admin_security_credentials``,
   ``storage_access_key`` / ``storage_secret_key``, ``oic_client_id`` / ``oic_client_secret``,
   ``entraid_client_id`` / ``entraid_client_secret`` y ``spnego_preauth_password`` conservan su
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
        "version": "15.9.0",
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

   Los ejemplos a continuación incluyen los campos requeridos (``day_for_cleanup``,
   ``crawling_thread_count``, ``failure_count_threshold``, ``csv_file_encoding``). Como estos
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
           "incremental_crawling": "true",
           "crawling_thread_count": 10,
           "failure_count_threshold": 100,
           "day_for_cleanup": -1,
           "csv_file_encoding": "UTF-8"
         }'

Actualizar el Período de Retención de Registros
-------------------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "day_for_cleanup": -1,
           "crawling_thread_count": 5,
           "failure_count_threshold": -1,
           "csv_file_encoding": "UTF-8",
           "purge_search_log_day": 90,
           "purge_job_log_day": 90,
           "purge_user_info_day": 90
         }'

Actualizar la Configuración de Sugerencias
-------------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "day_for_cleanup": -1,
           "crawling_thread_count": 5,
           "failure_count_threshold": -1,
           "csv_file_encoding": "UTF-8",
           "suggest_search_log": "true",
           "suggest_documents": "true"
         }'

Información de Referencia
==========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-systeminfo` - API de información del sistema
- :doc:`../../admin/general-guide` - Guía de configuración general
