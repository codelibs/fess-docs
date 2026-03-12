==================================
Conector de Atlassian
==================================

Descripcion General
===================

El conector de Atlassian proporciona funcionalidad para obtener datos de productos Atlassian
(Jira, Confluence) y registrarlos en el indice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-atlassian``.

Productos Compatibles
=====================

- Jira (Cloud / Server / Data Center)
- Confluence (Cloud / Server / Data Center)

Requisitos Previos
==================

1. Se requiere instalacion del plugin
2. Se requieren credenciales de autenticacion apropiadas para productos Atlassian
3. Para la version Cloud, se puede usar OAuth 2.0; para Server, OAuth 1.0a o autenticacion basica

Instalacion del Plugin
----------------------

Instale desde la consola de administracion en "Sistema" -> "Plugins":

1. Descargue ``fess-ds-atlassian-X.X.X.jar`` de Maven Central
2. Cargue e instale desde la pantalla de administracion de plugins
3. Reinicie |Fess|

Metodo de Configuracion
=======================

Configure desde la consola de administracion en "Rastreador" -> "Almacen de Datos" -> "Crear Nuevo".

Configuracion Basica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Elemento
     - Ejemplo de Configuracion
   * - Nombre
     - Company Jira/Confluence
   * - Nombre del Manejador
     - JiraDataStore o ConfluenceDataStore
   * - Habilitado
     - Activado

Configuracion de Parametros
---------------------------

Ejemplo version Cloud (OAuth 2.0):

::

    home=https://yourcompany.atlassian.net
    is_cloud=true
    auth_type=oauth2
    oauth2.client_id=your_client_id
    oauth2.client_secret=your_client_secret
    oauth2.access_token=your_access_token
    oauth2.refresh_token=your_refresh_token

Ejemplo version Server (Autenticacion Basica):

::

    home=https://jira.yourcompany.com
    is_cloud=false
    auth_type=basic
    basic.username=admin
    basic.password=your_password

Ejemplo version Server (OAuth 1.0a):

::

    home=https://jira.yourcompany.com
    is_cloud=false
    auth_type=oauth
    oauth.consumer_key=OauthKey
    oauth.private_key=-----BEGIN RSA PRIVATE KEY-----\\nMIIE...=\\n-----END RSA PRIVATE KEY-----
    oauth.secret=verification_code
    oauth.access_token=your_access_token

Lista de Parametros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametro
     - Requerido
     - Descripcion
   * - ``home``
     - Si
     - URL de la instancia de Atlassian
   * - ``is_cloud``
     - Si
     - ``true`` para version Cloud, ``false`` para Server
   * - ``auth_type``
     - Si
     - Tipo de autenticacion: ``oauth``, ``oauth2``, ``basic``
   * - ``oauth.consumer_key``
     - Para OAuth 1.0a
     - Clave del consumidor (normalmente ``OauthKey``)
   * - ``oauth.private_key``
     - Para OAuth 1.0a
     - Clave privada RSA (formato PEM)
   * - ``oauth.secret``
     - Para OAuth 1.0a
     - Codigo de verificacion
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
     - Token de actualizacion (OAuth 2.0)
   * - ``oauth2.token_url``
     - No
     - URL del token (OAuth 2.0, tiene valor predeterminado)
   * - ``basic.username``
     - Para autenticacion basica
     - Nombre de usuario
   * - ``basic.password``
     - Para autenticacion basica
     - Contrasena
   * - ``issue.jql``
     - No
     - JQL (solo Jira, condiciones de busqueda avanzadas)

Configuracion de Script
-----------------------

Para Jira
~~~~~~~~~

::

    url=issue.view_url
    title=issue.summary
    content=issue.description + "\\n\\n" + issue.comments
    last_modified=issue.last_modified

Campos disponibles:

- ``issue.view_url`` - URL de la incidencia
- ``issue.summary`` - Resumen de la incidencia
- ``issue.description`` - Descripcion de la incidencia
- ``issue.comments`` - Comentarios de la incidencia
- ``issue.last_modified`` - Fecha de ultima modificacion

Para Confluence
~~~~~~~~~~~~~~~

::

    url=content.view_url
    title=content.title
    content=content.body + "\\n\\n" + content.comments
    last_modified=content.last_modified

Campos disponibles:

- ``content.view_url`` - URL de la pagina
- ``content.title`` - Titulo de la pagina
- ``content.body`` - Cuerpo de la pagina
- ``content.comments`` - Comentarios de la pagina
- ``content.last_modified`` - Fecha de ultima modificacion

Configuracion de Autenticacion OAuth 2.0
========================================

Para la Version Cloud (Recomendado)
-----------------------------------

1. Cree una aplicacion en Atlassian Developer Console
2. Obtenga credenciales de OAuth 2.0
3. Configure los alcances requeridos:

   - Jira: ``read:jira-work``, ``read:jira-user``
   - Confluence: ``read:confluence-content.all``, ``read:confluence-user``

4. Obtenga tokens de acceso y actualizacion

Configuracion de Autenticacion OAuth 1.0a
=========================================

Para la Version Server
----------------------

1. Cree un Application Link en Jira o Confluence
2. Genere un par de claves RSA:

   ::

       openssl genrsa -out private_key.pem 2048
       openssl rsa -in private_key.pem -pubout -out public_key.pem

3. Registre la clave publica en el Application Link
4. Configure la clave privada en los parametros

Configuracion de Autenticacion Basica
=====================================

Configuracion Simple para Version Server
----------------------------------------

.. warning::
   La autenticacion basica no se recomienda por razones de seguridad. Use autenticacion OAuth siempre que sea posible.

Al usar autenticacion basica:

1. Prepare una cuenta de usuario con permisos de administrador
2. Configure el nombre de usuario y contrasena en los parametros
3. Asegure una conexion segura usando HTTPS

Busqueda Avanzada con JQL
=========================

Filtrar Incidencias de Jira con JQL
-----------------------------------

Rastree solo incidencias que coincidan con condiciones especificas:

::

    # Solo un proyecto especifico
    issue.jql=project = "MYPROJECT"

    # Excluir estados especificos
    issue.jql=project = "MYPROJECT" AND status != "Closed"

    # Especificar periodo
    issue.jql=updated >= -30d

    # Combinacion de multiples condiciones
    issue.jql=project IN ("PROJ1", "PROJ2") AND updated >= -90d AND status != "Done"

Para mas detalles sobre JQL, consulte la `Documentacion JQL de Atlassian <https://confluence.atlassian.com/jirasoftwarecloud/advanced-searching-764478330.html>`_.

Ejemplos de Uso
===============

Rastreo de Jira Cloud
---------------------

Parametros:

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
    title="[" + issue.key + "] " + issue.summary
    content=issue.description + "\\n\\nComentarios:\\n" + issue.comments
    last_modified=issue.last_modified

Rastreo de Confluence Server
----------------------------

Parametros:

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
    content=content.body + "\\n\\nComentarios:\\n" + content.comments
    last_modified=content.last_modified
    digest=content.title

Solucion de Problemas
=====================

Errores de Autenticacion
------------------------

**Sintoma**: ``401 Unauthorized`` o ``403 Forbidden``

**Verifique**:

1. Verifique que las credenciales de autenticacion sean correctas
2. Para la version Cloud, verifique que los alcances apropiados esten configurados
3. Para la version Server, verifique que el usuario tenga los permisos apropiados
4. Para OAuth 2.0, verifique la expiracion del token

Errores de Conexion
-------------------

**Sintoma**: ``Connection refused`` o tiempo de espera de conexion

**Verifique**:

1. Verifique que la URL ``home`` sea correcta
2. Verifique la configuracion del firewall
3. Verifique que la instancia de Atlassian este en ejecucion
4. Verifique que el parametro ``is_cloud`` este configurado correctamente

No Se Pueden Obtener Datos
--------------------------

**Sintoma**: El rastreo tiene exito pero hay 0 documentos

**Verifique**:

1. Verifique que JQL no este filtrando demasiado
2. Verifique que el usuario tenga permisos de lectura en los proyectos/espacios
3. Verifique la configuracion del script
4. Revise los logs en busca de errores

Actualizacion de Token OAuth 2.0
--------------------------------

**Sintoma**: Ocurren errores de autenticacion despues de un tiempo

**Solucion**:

Los tokens de acceso OAuth 2.0 tienen fechas de expiracion. Configure el token de actualizacion para permitir la renovacion automatica:

::

    oauth2.refresh_token=your_refresh_token

Informacion de Referencia
=========================

- :doc:`ds-overview` - Descripcion General de Conectores de Almacen de Datos
- :doc:`ds-database` - Conector de Base de Datos
- :doc:`../../admin/dataconfig-guide` - Guia de Configuracion de Almacen de Datos
- `Atlassian Developer <https://developer.atlassian.com/>`_
