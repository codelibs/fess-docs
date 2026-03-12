==================================
Conector de Microsoft 365
==================================

Vision General
==============

El conector de Microsoft 365 proporciona funcionalidad para obtener datos de servicios de Microsoft 365
(OneDrive, OneNote, Teams, SharePoint) y registrarlos en el indice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-microsoft365``.

Servicios Soportados
====================

- **OneDrive**: Unidades de usuario, unidades de grupo, documentos compartidos
- **OneNote**: Cuadernos (sitio, usuario, grupo)
- **Teams**: Canales, mensajes, chats
- **SharePoint Document Libraries**: Metadatos de bibliotecas de documentos
- **SharePoint Lists**: Listas y elementos de lista
- **SharePoint Pages**: Paginas del sitio, articulos de noticias

Requisitos Previos
==================

1. Se requiere la instalacion del plugin
2. Se requiere el registro de la aplicacion en Azure AD
3. Se requieren permisos de Microsoft Graph API y consentimiento de administrador
4. Java 21 o superior, Fess 15.2.0 o superior

Instalacion del Plugin
----------------------

Metodo 1: Colocar el archivo JAR directamente

::

    # Descargar desde Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-microsoft365/X.X.X/fess-ds-microsoft365-X.X.X.jar

    # Colocar
    cp fess-ds-microsoft365-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # o
    sudo cp fess-ds-microsoft365-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Metodo 2: Construir desde el codigo fuente

::

    git clone https://github.com/codelibs/fess-ds-microsoft365.git
    cd fess-ds-microsoft365
    mvn clean package
    cp target/fess-ds-microsoft365-*.jar $FESS_HOME/app/WEB-INF/lib/

Despues de la instalacion, reinicie |Fess|.

Metodo de Configuracion
=======================

Configure desde la pantalla de administracion en "Rastreador" -> "Almacen de datos" -> "Nuevo".

Configuracion Basica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Elemento
     - Ejemplo
   * - Nombre
     - Microsoft 365 OneDrive
   * - Nombre del manejador
     - OneDriveDataStore / OneNoteDataStore / TeamsDataStore / SharePointDocLibDataStore / SharePointListDataStore / SharePointPageDataStore
   * - Habilitado
     - Activado

Configuracion de Parametros (Comun)
-----------------------------------

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=abcdefghijklmnopqrstuvwxyz123456
    number_of_threads=1
    ignore_error=false

Lista de Parametros Comunes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametro
     - Requerido
     - Descripcion
   * - ``tenant``
     - Si
     - ID de tenant de Azure AD
   * - ``client_id``
     - Si
     - ID de cliente del registro de aplicacion
   * - ``client_secret``
     - Si
     - Secreto de cliente del registro de aplicacion
   * - ``number_of_threads``
     - No
     - Numero de hilos para procesamiento paralelo (predeterminado: 1)
   * - ``ignore_error``
     - No
     - Continuar procesando en caso de error (predeterminado: false)
   * - ``include_pattern``
     - No
     - Patron de expresion regular para contenido a incluir
   * - ``exclude_pattern``
     - No
     - Patron de expresion regular para contenido a excluir
   * - ``default_permissions``
     - No
     - Asignacion de rol predeterminado

Registro de Aplicacion en Azure AD
==================================

1. Registrar aplicacion en Azure Portal
---------------------------------------

Abra Azure Active Directory en https://portal.azure.com:

1. Haga clic en "Registros de aplicaciones" -> "Nuevo registro"
2. Ingrese el nombre de la aplicacion
3. Seleccione los tipos de cuenta compatibles
4. Haga clic en "Registrar"

2. Crear secreto de cliente
---------------------------

En "Certificados y secretos":

1. Haga clic en "Nuevo secreto de cliente"
2. Configure la descripcion y la fecha de expiracion
3. Copie el valor del secreto (no podra verlo posteriormente)

3. Agregar permisos de API
--------------------------

En "Permisos de API":

1. Haga clic en "Agregar un permiso"
2. Seleccione "Microsoft Graph"
3. Seleccione "Permisos de aplicacion"
4. Agregue los permisos necesarios (ver abajo)
5. Haga clic en "Conceder consentimiento de administrador"

Permisos Necesarios por Almacen de Datos
========================================

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

O ``Sites.Selected`` (cuando se especifica site_id, configuracion necesaria por sitio)

SharePointListDataStore / SharePointPageDataStore
-------------------------------------------------

Permisos requeridos:

- ``Sites.Read.All``

O ``Sites.Selected`` (cuando se especifica site_id, configuracion necesaria por sitio)

Configuracion de Script
=======================

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
- ``file.description`` - Descripcion del archivo
- ``file.contents`` - Contenido de texto
- ``file.mimetype`` - Tipo MIME
- ``file.filetype`` - Tipo de archivo
- ``file.created`` - Fecha de creacion
- ``file.last_modified`` - Ultima fecha de modificacion
- ``file.size`` - Tamano del archivo
- ``file.web_url`` - URL para abrir en el navegador
- ``file.roles`` - Permisos de acceso

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

- ``message.title`` - Titulo del mensaje
- ``message.content`` - Contenido del mensaje
- ``message.created_date_time`` - Fecha de creacion
- ``message.last_modified_date_time`` - Ultima fecha de modificacion
- ``message.web_url`` - URL para abrir en el navegador
- ``message.roles`` - Permisos de acceso
- ``message.from`` - Informacion del remitente

Solucion de Problemas
=====================

Error de Autenticacion
----------------------

**Sintoma**: ``Authentication failed`` o ``Insufficient privileges``

**Verificar**:

1. Verificar que el ID de tenant, ID de cliente y secreto de cliente sean correctos
2. Verificar que los permisos de API necesarios esten otorgados en Azure Portal
3. Verificar que se haya otorgado el consentimiento de administrador
4. Verificar la fecha de expiracion del secreto de cliente

Error de Limite de Tasa de API
------------------------------

**Sintoma**: ``429 Too Many Requests``

**Solucion**:

1. Reducir ``number_of_threads`` (establecer en 1 o 2)
2. Aumentar el intervalo de rastreo
3. Establecer ``ignore_error=true`` para continuar el procesamiento

Informacion de Referencia
=========================

- :doc:`ds-overview` - Vision general de conectores de almacen de datos
- :doc:`ds-gsuite` - Conector de Google Workspace
- :doc:`../../admin/dataconfig-guide` - Guia de configuracion de almacen de datos
- `Microsoft Graph API <https://docs.microsoft.com/en-us/graph/>`_
- `Azure AD App Registration <https://docs.microsoft.com/en-us/azure/active-directory/develop/>`_
