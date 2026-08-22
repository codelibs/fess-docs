==================================
Conector de Microsoft 365
==================================

Descripción general
===================

El conector de Microsoft 365 proporciona la funcionalidad para obtener datos de los servicios de Microsoft 365
(OneDrive, OneNote, Teams, SharePoint) y registrarlos en el índice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-microsoft365``.

Servicios compatibles
=====================

- **OneDrive**: Unidades de usuario, unidades de grupo, documentos compartidos
- **OneNote**: Cuadernos (sitio, usuario, grupo)
- **Teams**: Canales, mensajes, chats
- **SharePoint Document Libraries**: Metadatos de bibliotecas de documentos
- **SharePoint Lists**: Listas y elementos de lista
- **SharePoint Pages**: Páginas del sitio, artículos de noticias

Requisitos previos
==================

1. Se requiere la instalación del plugin
2. Se requiere el registro de la aplicación en Azure AD
3. Se requieren la configuración de permisos de Microsoft Graph API y el consentimiento del administrador
4. Java 21 o superior, Fess 15.2.0 o superior

Instalación del plugin
----------------------

Método 1: Colocar el archivo JAR directamente

::

    # Maven Centralからダウンロード
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-microsoft365/X.X.X/fess-ds-microsoft365-X.X.X.jar

    # 配置
    cp fess-ds-microsoft365-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # または
    sudo cp fess-ds-microsoft365-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Método 2: Compilar desde el código fuente

::

    git clone https://github.com/codelibs/fess-ds-microsoft365.git
    cd fess-ds-microsoft365
    mvn clean package
    cp target/fess-ds-microsoft365-*.jar $FESS_HOME/app/WEB-INF/lib/

Después de la instalación, reinicie |Fess|.

Método de configuración
=======================

Configure desde la pantalla de administración en "Rastreador" -> "Almacén de datos" -> "Nuevo".

Configuración básica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Elemento
     - Ejemplo de configuración
   * - Nombre
     - Microsoft 365 OneDrive
   * - Nombre del manejador
     - OneDriveDataStore / OneNoteDataStore / TeamsDataStore / SharePointDocLibDataStore / SharePointListDataStore / SharePointPageDataStore
   * - Habilitado
     - Activado

Configuración de parámetros (común)
------------------------------------

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=abcdefghijklmnopqrstuvwxyz123456
    number_of_threads=1
    ignore_error=false

Lista de parámetros comunes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parámetro
     - Requerido
     - Descripción
   * - ``tenant``
     - Sí
     - ID de tenant de Azure AD
   * - ``client_id``
     - Sí
     - ID de cliente del registro de aplicación
   * - ``client_secret``
     - Sí
     - Secreto de cliente del registro de aplicación
   * - ``number_of_threads``
     - No
     - Número de hilos para procesamiento paralelo (predeterminado: 1)
   * - ``ignore_error``
     - No
     - Continuar procesando en caso de error (predeterminado: false)
   * - ``max_content_length``
     - No
     - Tamaño máximo del contenido obtenido (predeterminado: -1, sin límite)
   * - ``cache_size``
     - No
     - Tamaño de caché para información de usuarios y grupos (predeterminado: 10000)
   * - ``proxy_host``
     - No
     - Host del proxy HTTP
   * - ``proxy_port``
     - No
     - Puerto del proxy HTTP
   * - ``proxy_username``
     - No
     - Nombre de usuario de autenticación del proxy
   * - ``proxy_password``
     - No
     - Contraseña de autenticación del proxy

Registro de aplicación en Azure AD
====================================

1. Registrar la aplicación en Azure Portal
-------------------------------------------

Abra Azure Active Directory en https://portal.azure.com:

1. Haga clic en "Registros de aplicaciones" -> "Nuevo registro"
2. Ingrese el nombre de la aplicación
3. Seleccione los tipos de cuenta compatibles
4. Haga clic en "Registrar"

2. Crear secreto de cliente
----------------------------

En "Certificados y secretos":

1. Haga clic en "Nuevo secreto de cliente"
2. Configure la descripción y la fecha de vencimiento
3. Copie el valor del secreto (no podrá verlo posteriormente)

3. Agregar permisos de API
---------------------------

En "Permisos de API":

1. Haga clic en "Agregar un permiso"
2. Seleccione "Microsoft Graph"
3. Seleccione "Permisos de aplicación"
4. Agregue los permisos necesarios (ver más abajo)
5. Haga clic en "Conceder consentimiento del administrador"

Permisos necesarios por almacén de datos
=========================================

OneDriveDataStore
-----------------

Permisos requeridos:

- ``Files.Read.All``

Permisos condicionales:

- ``User.Read.All`` - cuando user_drive_crawler=true
- ``Group.Read.All`` - cuando group_drive_crawler=true
- ``Sites.Read.All`` - cuando shared_documents_drive_crawler=true

OneNoteDataStore
----------------

Permisos requeridos:

- ``Notes.Read.All``

Permisos condicionales:

- ``User.Read.All`` - cuando user_note_crawler=true
- ``Group.Read.All`` - cuando group_note_crawler=true
- ``Sites.Read.All`` - cuando site_note_crawler=true

TeamsDataStore
--------------

Permisos requeridos:

- ``Team.ReadBasic.All``
- ``Group.Read.All``
- ``Channel.ReadBasic.All``
- ``ChannelMessage.Read.All``
- ``ChannelMember.Read.All``
- ``User.Read.All``

Permisos condicionales:

- ``Chat.Read.All`` - cuando se especifica chat_id
- ``Files.Read.All`` - cuando append_attachment=true

SharePointDocLibDataStore
-------------------------

Permisos requeridos:

- ``Files.Read.All``
- ``Sites.Read.All``

O ``Sites.Selected`` (cuando se especifica site_id, es necesario configurarlo por sitio)

SharePointListDataStore / SharePointPageDataStore
-------------------------------------------------

Permisos requeridos:

- ``Sites.Read.All``

O ``Sites.Selected`` (cuando se especifica site_id, es necesario configurarlo por sitio)

Configuración de scripts
========================

OneDrive
--------

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created
    last_modified=file.last_modified
    url=file.web_url
    role=file.roles

Campos disponibles:

- ``file.name`` - Nombre del archivo
- ``file.description`` - Descripción del archivo
- ``file.contents`` - Contenido de texto
- ``file.mimetype`` - Tipo MIME
- ``file.filetype`` - Tipo de archivo
- ``file.created`` - Fecha y hora de creación
- ``file.last_modified`` - Fecha y hora de última modificación
- ``file.size`` - Tamaño del archivo
- ``file.web_url`` - URL para abrir en el navegador
- ``file.url`` - URL del archivo
- ``file.id`` - ID del elemento de unidad
- ``file.ctag`` - Etiqueta de cambio (cTag)
- ``file.etag`` - Etiqueta de entidad (eTag)
- ``file.webdav_url`` - URL de WebDAV
- ``file.parent_id`` - ID de la carpeta padre
- ``file.parent_name`` - Nombre de la carpeta padre
- ``file.parent_path`` - Ruta de la carpeta padre
- ``file.roles`` - Permisos de acceso

.. note::

   Además de los anteriores, también están disponibles campos de metadatos de Microsoft Graph como
   ``file.createdby_user``, ``file.last_modifiedby_user``, ``file.image``,
   ``file.video``, ``file.special_folder``, entre otros.

OneNote
-------

::

    title=notebook.name
    content=notebook.contents
    created=notebook.created
    last_modified=notebook.last_modified
    url=notebook.web_url
    role=notebook.roles
    size=notebook.size

Campos disponibles:

- ``notebook.name`` - Nombre del cuaderno
- ``notebook.contents`` - Contenido integrado de secciones y páginas
- ``notebook.size`` - Tamaño del contenido (número de caracteres)
- ``notebook.created`` - Fecha y hora de creación
- ``notebook.last_modified`` - Fecha y hora de última modificación
- ``notebook.web_url`` - URL para abrir en el navegador
- ``notebook.roles`` - Permisos de acceso

Teams
-----

::

    title=message.title
    content=message.content
    created=message.created_date_time
    last_modified=message.last_modified_date_time
    url=message.web_url
    role=message.roles

Campos disponibles:

- ``message.title`` - Título del mensaje
- ``message.content`` - Contenido del mensaje
- ``message.body`` - Cuerpo del mensaje (datos sin procesar, incluido HTML)
- ``message.subject`` - Asunto del mensaje
- ``message.summary`` - Resumen del mensaje
- ``message.importance`` - Importancia
- ``message.from`` - Información del remitente
- ``message.created_date_time`` - Fecha y hora de creación
- ``message.last_modified_date_time`` - Fecha y hora de última modificación
- ``message.last_edited_date_time`` - Fecha y hora de última edición
- ``message.deleted_date_time`` - Fecha y hora de eliminación
- ``message.web_url`` - URL para abrir en el navegador
- ``message.id`` - ID del mensaje
- ``message.etag`` - Etiqueta de entidad
- ``message.locale`` - Configuración regional
- ``message.chat_id`` - ID del chat
- ``message.reply_to_id`` - ID del mensaje al que se responde
- ``message.channel_identity`` - Información de identidad del canal (ID de equipo e ID de canal)
- ``message.mentions`` - Información de menciones
- ``message.attachments`` - Información de archivos adjuntos
- ``message.replies`` - Mensajes de respuesta
- ``message.hosted_contents`` - Contenido en línea (imágenes, etc.)
- ``message.roles`` - Permisos de acceso

Campos de nivel superior (se establecen únicamente para mensajes de canal):

- ``team`` - Equipo (objeto ``Group`` de Microsoft Graph)
- ``channel`` - Canal (objeto ``Channel`` de Microsoft Graph)
- ``parent`` - Mensaje padre (se establece cuando es un mensaje de respuesta)

SharePoint Document Libraries
------------------------------

::

    title=doclib.name
    content=doclib.content
    created=doclib.created
    last_modified=doclib.modified
    url=doclib.url
    role=doclib.roles

Campos disponibles:

- ``doclib.name`` - Nombre de la biblioteca de documentos
- ``doclib.description`` - Descripción de la biblioteca
- ``doclib.content`` - Contenido integrado para búsqueda
- ``doclib.created`` - Fecha y hora de creación
- ``doclib.modified`` - Fecha y hora de última modificación
- ``doclib.url`` - URL de SharePoint
- ``doclib.web_url`` - URL para abrir en el navegador
- ``doclib.id`` - ID de la biblioteca de documentos
- ``doclib.type`` - Tipo de documento
- ``doclib.site_name`` - Nombre del sitio
- ``doclib.site_url`` - URL del sitio
- ``doclib.roles`` - Permisos de acceso

SharePoint Lists
----------------

::

    title=item.title
    content=item.content
    created=item.created
    last_modified=item.modified
    url=item.url
    role=item.roles

Campos disponibles:

- ``item.title`` - Título del elemento de lista
- ``item.content`` - Contenido de texto
- ``item.created`` - Fecha y hora de creación
- ``item.modified`` - Fecha y hora de última modificación
- ``item.url`` - URL de SharePoint
- ``item.web_url`` - URL para abrir en el navegador
- ``item.id`` - ID del elemento de lista
- ``item.content_type`` - Tipo de contenido
- ``item.fields`` - Mapa de todos los campos
- ``item.roles`` - Permisos de acceso

SharePoint Pages
----------------

::

    title=page.title
    content=page.content
    created=page.created
    last_modified=page.modified
    url=page.url
    role=page.roles

Campos disponibles:

- ``page.title`` - Título de la página
- ``page.content`` - Contenido de la página
- ``page.created`` - Fecha y hora de creación
- ``page.modified`` - Fecha y hora de última modificación
- ``page.url`` - URL de SharePoint
- ``page.web_url`` - URL para abrir en el navegador
- ``page.id`` - ID de la página
- ``page.description`` - Descripción de la página
- ``page.author`` - Autor
- ``page.type`` - Tipo de página (news/article/page)
- ``page.site_name`` - Nombre del sitio
- ``page.site_url`` - URL del sitio
- ``page.promotion_state`` - Estado de promoción
- ``page.roles`` - Permisos de acceso

Parámetros adicionales por almacén de datos
============================================

OneDrive
--------

::

    max_content_length=-1
    ignore_folder=true
    supported_mimetypes=.*
    include_pattern=
    exclude_pattern=
    url_filter=
    default_permissions=
    drive_id=
    shared_documents_drive_crawler=true
    user_drive_crawler=true
    group_drive_crawler=true

OneNote
-------

::

    site_note_crawler=true
    user_note_crawler=true
    group_note_crawler=true

Teams
-----

::

    team_id=
    exclude_team_ids=
    include_visibility=
    channel_id=
    chat_id=
    default_permissions=
    ignore_replies=false
    append_attachment=true
    ignore_system_events=true
    title_dateformat=yyyy/MM/dd'T'HH:mm:ss
    title_timezone_offset=Z

SharePoint Document Libraries
-----------------------------

::

    site_id=
    exclude_site_id=
    include_pattern=
    exclude_pattern=
    default_permissions=
    ignore_error=false
    ignore_system_libraries=true

SharePoint Lists
----------------

::

    site_id=hostname,siteCollectionId,siteId
    list_id=
    exclude_list_id=
    list_template_filter=
    include_pattern=
    exclude_pattern=
    default_permissions=
    ignore_error=false
    ignore_system_lists=true

SharePoint Pages
----------------

::

    site_id=
    exclude_site_id=
    include_pattern=
    exclude_pattern=
    default_permissions=
    ignore_error=false
    ignore_system_pages=true
    page_type_filter=

Ejemplos de uso
===============

Rastrear todas las unidades de OneDrive
----------------------------------------

Parámetros:

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    user_drive_crawler=true
    group_drive_crawler=true
    shared_documents_drive_crawler=true

Script:

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created
    last_modified=file.last_modified
    url=file.web_url
    role=file.roles

Rastrear mensajes de Teams de un equipo específico
---------------------------------------------------

Parámetros:

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    team_id=19:abc123def456@thread.tacv2
    ignore_replies=false
    append_attachment=true
    title_timezone_offset=+09:00

Script:

::

    title=message.title
    content=message.content
    created=message.created_date_time
    url=message.web_url
    role=message.roles

Rastrear listas de SharePoint
------------------------------

Parámetros:

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    site_id=contoso.sharepoint.com,686d3f1a-a383-4367-b5f5-93b99baabcf3,12048306-4e53-420e-bd7c-31af611f6d8a
    list_template_filter=100,101
    ignore_system_lists=true

Script:

::

    title=item.title
    content=item.content
    created=item.created
    last_modified=item.modified
    url=item.url
    role=item.roles

Solución de problemas
=====================

Error de autenticación
----------------------

**Síntoma**: ``Authentication failed`` o ``Insufficient privileges``

**Puntos a verificar**:

1. Verificar que el ID de tenant, el ID de cliente y el secreto de cliente sean correctos
2. Verificar que los permisos de API necesarios estén otorgados en Azure Portal
3. Verificar que se haya otorgado el consentimiento del administrador
4. Verificar la fecha de vencimiento del secreto de cliente

Error de límite de tasa de la API
----------------------------------

**Síntoma**: ``429 Too Many Requests``

**Solución**:

1. Reducir ``number_of_threads`` (establecer en 1 o 2)
2. Aumentar el intervalo de rastreo
3. Establecer ``ignore_error=true`` para continuar el procesamiento

No se pueden obtener datos
--------------------------

**Síntoma**: El rastreo se completa correctamente pero hay 0 documentos

**Puntos a verificar**:

1. Verificar que los datos de destino existan
2. Verificar que los permisos de API estén configurados correctamente
3. Verificar la configuración del rastreador de unidades de usuario/grupo
4. Revisar los mensajes de error en los registros

Cómo verificar el ID de sitio de SharePoint
--------------------------------------------

Verificar con PowerShell:

::

    Connect-PnPOnline -Url "https://contoso.sharepoint.com/sites/yoursite" -Interactive
    Get-PnPSite | Select Id

O con Microsoft Graph API:

::

    GET https://graph.microsoft.com/v1.0/sites/contoso.sharepoint.com:/sites/yoursite

Rastrear grandes volúmenes de datos
-------------------------------------

**Solución**:

1. Dividir en múltiples almacenes de datos (por sitio, por unidad, etc.)
2. Distribuir la carga mediante la configuración de horarios
3. Ajustar ``number_of_threads`` para procesamiento paralelo
4. Rastrear únicamente carpetas o sitios específicos

Información de referencia
=========================

- :doc:`ds-overview` - Descripción general de conectores de almacén de datos
- :doc:`ds-gsuite` - Conector de Google Workspace
- :doc:`../../admin/dataconfig-guide` - Guía de configuración del almacén de datos
- `Microsoft Graph API <https://docs.microsoft.com/en-us/graph/>`_
- `Azure AD App Registration <https://docs.microsoft.com/en-us/azure/active-directory/develop/>`_
