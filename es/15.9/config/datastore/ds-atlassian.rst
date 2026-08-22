==================================
Conector de Atlassian
==================================

Descripción General
===================

El conector de Atlassian proporciona funcionalidad para obtener datos de productos Atlassian
(Jira, Confluence) y registrarlos en el índice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-atlassian``.

Productos Compatibles
=====================

- Jira (Cloud / Server / Data Center)
- Confluence (Cloud / Server / Data Center)

Requisitos Previos
==================

1. Se requiere instalación del plugin
2. Se requieren credenciales de autenticación apropiadas para productos Atlassian
3. Para la versión Cloud, se puede usar OAuth 2.0; para Server, OAuth 1.0a o autenticación básica

Instalación del Plugin
----------------------

Instale desde la consola de administración en "Sistema" -> "Plugins":

1. Descargue ``fess-ds-atlassian-X.X.X.jar`` de Maven Central
2. Cargue e instale desde la pantalla de administración de plugins
3. Reinicie |Fess|

Método de Configuración
=======================

Configure desde la consola de administración en "Rastreador" -> "Almacén de Datos" -> "Crear Nuevo".

Configuración Básica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Elemento
     - Ejemplo de Configuración
   * - Nombre
     - Company Jira/Confluence
   * - Nombre del Manejador
     - JiraDataStore o ConfluenceDataStore
   * - Habilitado
     - Activado

Configuración de Parámetros
---------------------------

Ejemplo versión Cloud (OAuth 2.0):

::

    home=https://yourcompany.atlassian.net
    is_cloud=true
    auth_type=oauth2
    oauth2.client_id=your_client_id
    oauth2.client_secret=your_client_secret
    oauth2.access_token=your_access_token
    oauth2.refresh_token=your_refresh_token

Ejemplo versión Server (Autenticación Básica):

::

    home=https://jira.yourcompany.com
    is_cloud=false
    auth_type=basic
    basic.username=admin
    basic.password=your_password

Ejemplo versión Server (OAuth 1.0a):

::

    home=https://jira.yourcompany.com
    is_cloud=false
    auth_type=oauth
    oauth.consumer_key=OauthKey
    oauth.private_key=-----BEGIN RSA PRIVATE KEY-----\nMIIE...=\n-----END RSA PRIVATE KEY-----
    oauth.secret=verification_code
    oauth.access_token=your_access_token

Lista de Parámetros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parámetro
     - Requerido
     - Descripción
   * - ``home``
     - Sí
     - URL de la instancia de Atlassian
   * - ``is_cloud``
     - No
     - ``true`` para Cloud, ``false`` para Server (predeterminado: ``true``). Solo se utiliza para la selección del endpoint durante la autenticación OAuth 2.0; se ignora en la autenticación Básica y OAuth 1.0a.
   * - ``auth_type``
     - Sí
     - Tipo de autenticación: ``oauth``, ``oauth2``, ``basic``
   * - ``oauth.consumer_key``
     - Para OAuth 1.0a
     - Clave del consumidor (normalmente ``OauthKey``)
   * - ``oauth.private_key``
     - Para OAuth 1.0a
     - Clave privada RSA (formato PEM)
   * - ``oauth.secret``
     - Para OAuth 1.0a
     - Código de verificación
   * - ``oauth.access_token``
     - Para OAuth 1.0a
     - Token de acceso
   * - ``oauth2.client_id``
     - Para OAuth 2.0
     - ID de cliente
   * - ``oauth2.client_secret``
     - Para OAuth 2.0
     - Secreto del cliente
   * - ``oauth2.access_token``
     - Para OAuth 2.0
     - Token de acceso
   * - ``oauth2.refresh_token``
     - No
     - Token de actualización (OAuth 2.0)
   * - ``oauth2.token_url``
     - No
     - URL del token (OAuth 2.0, predeterminado: ``https://auth.atlassian.com/oauth/token``)
   * - ``basic.username``
     - Para autenticación básica
     - Nombre de usuario
   * - ``basic.password``
     - Para autenticación básica
     - Contraseña
   * - ``issue.jql``
     - No
     - JQL (solo Jira, condiciones de búsqueda avanzadas). Si no se especifica, se procesan todas las incidencias (``created is not empty``).
   * - ``issue_max_results``
     - No
     - Resultados máximos por solicitud de API de Jira (predeterminado: ``50``, solo Jira)
   * - ``content_limit``
     - No
     - Elementos máximos por solicitud de API de Confluence (predeterminado: ``25``, solo Confluence)
   * - ``ignore_error``
     - No
     - Continuar procesamiento en caso de error (predeterminado: ``true``)
   * - ``include_pattern``
     - No
     - Patrón de inclusión de URL (regex)
   * - ``exclude_pattern``
     - No
     - Patrón de exclusión de URL (regex)
   * - ``number_of_threads``
     - No
     - Número de hilos para procesamiento paralelo (predeterminado: ``1``)
   * - ``proxy_host``
     - No
     - Nombre de host del proxy HTTP
   * - ``proxy_port``
     - No
     - Número de puerto del proxy HTTP
   * - ``connection_timeout``
     - No
     - Tiempo de espera de conexión HTTP (milisegundos)
   * - ``read_timeout``
     - No
     - Tiempo de espera de lectura HTTP (milisegundos)
   * - ``readInterval``
     - No
     - Intervalo entre el procesamiento de cada documento (en milisegundos, predeterminado: ``0``)

Configuración de Script
-----------------------

Para Jira
~~~~~~~~~

::

    url=issue.view_url
    title=issue.summary
    content=issue.description + "\n\n" + issue.comments
    last_modified=issue.last_modified

Campos disponibles:

- ``issue.view_url`` - URL de la incidencia
- ``issue.summary`` - Resumen de la incidencia
- ``issue.description`` - Descripción de la incidencia
- ``issue.comments`` - Comentarios de la incidencia
- ``issue.last_modified`` - Fecha de última modificación

Para Confluence
~~~~~~~~~~~~~~~

::

    url=content.view_url
    title=content.title
    content=content.body + "\n\n" + content.comments
    last_modified=content.last_modified

Campos disponibles:

- ``content.view_url`` - URL de la página
- ``content.title`` - Título de la página
- ``content.body`` - Cuerpo de la página
- ``content.comments`` - Comentarios de la página
- ``content.last_modified`` - Fecha de última modificación

.. note::
   El conector de Confluence recupera tanto páginas regulares (page) como entradas de blog (blogpost).

Configuración de Autenticación OAuth 2.0
========================================

Para la Versión Cloud (Recomendado)
-----------------------------------

1. Cree una aplicación en Atlassian Developer Console
2. Obtenga credenciales de OAuth 2.0
3. Configure los alcances requeridos:

   - Jira: ``read:jira-work``, ``read:jira-user``
   - Confluence: ``read:confluence-content.all``, ``read:confluence-user``

4. Obtenga tokens de acceso y actualización

Configuración de Autenticación OAuth 1.0a
=========================================

Para la Versión Server
----------------------

1. Cree un Application Link en Jira o Confluence
2. Genere un par de claves RSA:

   ::

       openssl genrsa -out private_key.pem 2048
       openssl rsa -in private_key.pem -pubout -out public_key.pem

3. Registre la clave pública en el Application Link
4. Configure la clave privada en los parámetros

Configuración de Autenticación Básica
=====================================

Configuración Simple para Versión Server
----------------------------------------

.. warning::
   La autenticación básica no se recomienda por razones de seguridad. Use autenticación OAuth siempre que sea posible.

Al usar autenticación básica:

1. Prepare una cuenta de usuario con permisos de administrador
2. Configure el nombre de usuario y contraseña en los parámetros
3. Asegure una conexión segura usando HTTPS

Búsqueda Avanzada con JQL
=========================

Filtrar Incidencias de Jira con JQL
-----------------------------------

Rastree solo incidencias que coincidan con condiciones específicas:

::

    # Solo un proyecto especifico
    issue.jql=project = "MYPROJECT"

    # Excluir estados especificos
    issue.jql=project = "MYPROJECT" AND status != "Closed"

    # Especificar periodo
    issue.jql=updated >= -30d

    # Combinacion de multiples condiciones
    issue.jql=project IN ("PROJ1", "PROJ2") AND updated >= -90d AND status != "Done"

Para más detalles sobre JQL, consulte la `Documentación JQL de Atlassian <https://confluence.atlassian.com/jirasoftwarecloud/advanced-searching-764478330.html>`_.

Ejemplos de Uso
===============

Rastreo de Jira Cloud
---------------------

Parámetros:

::

    home=https://yourcompany.atlassian.net
    is_cloud=true
    auth_type=oauth2
    oauth2.client_id=Abc123DefGhi456
    oauth2.client_secret=xyz789uvw456rst123
    oauth2.access_token=eyJhbGciOiJIUzI1...
    oauth2.refresh_token=def456ghi789jkl012
    issue.jql=project = "SUPPORT" AND status != "Closed"

Script:

::

    url=issue.view_url
    title=issue.summary
    content=issue.description + "\n\nComentarios:\n" + issue.comments
    last_modified=issue.last_modified

Rastreo de Confluence Server
----------------------------

Parámetros:

::

    home=https://wiki.yourcompany.com
    is_cloud=false
    auth_type=basic
    basic.username=crawler_user
    basic.password=secure_password

Script:

::

    url=content.view_url
    title=content.title
    content=content.body + "\n\nComentarios:\n" + content.comments
    last_modified=content.last_modified
    digest=content.title

Solución de Problemas
=====================

Errores de Autenticación
------------------------

**Síntoma**: ``401 Unauthorized`` o ``403 Forbidden``

**Verifique**:

1. Verifique que las credenciales de autenticación sean correctas
2. Para la versión Cloud, verifique que los alcances apropiados estén configurados
3. Para la versión Server, verifique que el usuario tenga los permisos apropiados
4. Para OAuth 2.0, verifique la expiración del token

Errores de Conexión
-------------------

**Síntoma**: ``Connection refused`` o tiempo de espera de conexión

**Verifique**:

1. Verifique que la URL ``home`` sea correcta
2. Verifique la configuración del firewall
3. Verifique que la instancia de Atlassian esté en ejecución
4. Verifique que el parámetro ``is_cloud`` esté configurado correctamente

No Se Pueden Obtener Datos
--------------------------

**Síntoma**: El rastreo tiene éxito pero hay 0 documentos

**Verifique**:

1. Verifique que JQL no esté filtrando demasiado
2. Verifique que el usuario tenga permisos de lectura en los proyectos/espacios
3. Verifique la configuración del script
4. Revise los logs en busca de errores

Actualización de Token OAuth 2.0
--------------------------------

**Síntoma**: Ocurren errores de autenticación después de un tiempo

**Solución**:

Los tokens de acceso OAuth 2.0 tienen fechas de expiración. Configure el token de actualización para permitir la renovación automática:

::

    oauth2.refresh_token=your_refresh_token

Cuando los tokens se renuevan, el nuevo token de acceso y el token de actualización se guardan automáticamente en la configuración del almacén de datos, por lo que los rastreos posteriores utilizan los tokens actualizados sin necesidad de actualizarlos manualmente.

Información de Referencia
=========================

- :doc:`ds-overview` - Descripción General de Conectores de Almacén de Datos
- :doc:`ds-database` - Conector de Base de Datos
- :doc:`../../admin/dataconfig-guide` - Guía de Configuración de Almacén de Datos
- `Atlassian Developer <https://developer.atlassian.com/>`_
