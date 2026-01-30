==================================
Conector de Dropbox
==================================

Descripcion General
===================

El conector de Dropbox proporciona funcionalidad para obtener archivos del almacenamiento
en la nube Dropbox y registrarlos en el indice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-dropbox``.

Servicios Compatibles
=====================

- Dropbox (almacenamiento de archivos)
- Dropbox Paper (documentos)

Requisitos Previos
==================

1. Se requiere instalacion del plugin
2. Se requiere una cuenta de desarrollador de Dropbox y la creacion de una aplicacion
3. Se requiere obtener un token de acceso

Instalacion del Plugin
----------------------

Instale desde la consola de administracion en "Sistema" -> "Plugins":

1. Descargue ``fess-ds-dropbox-X.X.X.jar`` de Maven Central
2. Cargue e instale desde la pantalla de administracion de plugins
3. Reinicie |Fess|

O consulte :doc:`../../admin/plugin-guide` para mas detalles.

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
     - Company Dropbox
   * - Nombre del Manejador
     - DropboxDataStore o DropboxPaperDataStore
   * - Habilitado
     - Activado

Configuracion de Parametros
---------------------------

::

    access_token=sl.AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEfGhIj
    basic_plan=false

Lista de Parametros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametro
     - Requerido
     - Descripcion
   * - ``access_token``
     - Si
     - Token de acceso de Dropbox (generado en App Console)
   * - ``basic_plan``
     - No
     - ``true`` para plan Basic (predeterminado: ``false``)

Configuracion de Script
-----------------------

Para Archivos de Dropbox
~~~~~~~~~~~~~~~~~~~~~~~~

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    last_modified=file.client_modified
    role=file.roles

Campos disponibles:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripcion
   * - ``file.url``
     - Enlace de vista previa del archivo
   * - ``file.contents``
     - Contenido de texto del archivo
   * - ``file.mimetype``
     - Tipo MIME del archivo
   * - ``file.filetype``
     - Tipo de archivo
   * - ``file.name``
     - Nombre del archivo
   * - ``file.path_display``
     - Ruta del archivo
   * - ``file.size``
     - Tamano del archivo (bytes)
   * - ``file.client_modified``
     - Fecha de ultima modificacion del lado del cliente
   * - ``file.server_modified``
     - Fecha de ultima modificacion del lado del servidor
   * - ``file.roles``
     - Permisos de acceso del archivo

Para Dropbox Paper
~~~~~~~~~~~~~~~~~~

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype
    role=paper.roles

Campos disponibles:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripcion
   * - ``paper.url``
     - Enlace de vista previa del documento Paper
   * - ``paper.contents``
     - Contenido de texto del documento Paper
   * - ``paper.mimetype``
     - Tipo MIME
   * - ``paper.filetype``
     - Tipo de archivo
   * - ``paper.title``
     - Titulo del documento Paper
   * - ``paper.owner``
     - Propietario del documento Paper
   * - ``paper.roles``
     - Permisos de acceso del documento

Configuracion de Autenticacion de Dropbox
=========================================

Pasos para Obtener Token de Acceso
----------------------------------

1. Crear una aplicacion en Dropbox App Console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Acceda a https://www.dropbox.com/developers/apps:

1. Haga clic en "Create app"
2. Seleccione "Scoped access" para el tipo de API
3. Seleccione "Full Dropbox" o "App folder" para el tipo de acceso
4. Ingrese el nombre de la aplicacion y cree

2. Configuracion de Permisos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

En la pestana "Permissions", seleccione los permisos requeridos:

**Permisos requeridos para rastreo de archivos**:

- ``files.metadata.read`` - Lectura de metadatos de archivos
- ``files.content.read`` - Lectura de contenido de archivos
- ``sharing.read`` - Lectura de informacion de uso compartido

**Permisos adicionales requeridos para rastreo de Paper**:

- ``files.content.read`` - Lectura de documentos Paper

3. Generar Token de Acceso
~~~~~~~~~~~~~~~~~~~~~~~~~~

En la pestana "Settings":

1. Desplacese hasta la seccion "Generated access token"
2. Haga clic en el boton "Generate"
3. Copie el token generado (este token se muestra solo una vez)

.. warning::
   Guarde el token de acceso de forma segura. Con este token,
   es posible acceder a la cuenta de Dropbox.

4. Configurar el Token
~~~~~~~~~~~~~~~~~~~~~~

Configure el token obtenido en los parametros:

::

    access_token=sl.AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEfGhIj

Configuracion para Plan Basic
=============================

Limitaciones del Plan Basic de Dropbox
--------------------------------------

Para el plan Basic de Dropbox, los limites de API son diferentes.
Configure el parametro ``basic_plan`` como ``true``:

::

    access_token=sl.AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEfGhIj
    basic_plan=true

Esto permite el procesamiento adaptado a los limites de tasa de API.

Ejemplos de Uso
===============

Rastrear Todos los Archivos de Dropbox
--------------------------------------

Parametros:

::

    access_token=sl.AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEfGhIj
    basic_plan=false

Script:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    last_modified=file.client_modified

Rastrear Documentos de Dropbox Paper
------------------------------------

Parametros:

::

    access_token=sl.AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEfGhIj
    basic_plan=false

Script:

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype

Rastrear Solo Tipos de Archivo Especificos
------------------------------------------

Filtrado en el script:

::

    # Solo PDF y archivos Word
    if (file.mimetype == "application/pdf" || file.mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document") {
        url=file.url
        title=file.name
        content=file.contents
        mimetype=file.mimetype
        filename=file.name
        last_modified=file.client_modified
    }

Solucion de Problemas
=====================

Errores de Autenticacion
------------------------

**Sintoma**: ``Invalid access token`` o ``401 Unauthorized``

**Verifique**:

1. Verifique que el token de acceso se haya copiado correctamente
2. Verifique que el token no haya expirado (use token de larga duracion)
3. Verifique que los permisos requeridos esten otorgados en Dropbox App Console
4. Verifique que la aplicacion no este desactivada

No Se Pueden Obtener Archivos
-----------------------------

**Sintoma**: El rastreo tiene exito pero hay 0 archivos

**Verifique**:

1. Verifique que el "Access type" de la aplicacion sea apropiado:

   - "Full Dropbox": Puede acceder a todo Dropbox
   - "App folder": Solo puede acceder a una carpeta especifica

2. Verifique que los permisos requeridos esten otorgados:

   - ``files.metadata.read``
   - ``files.content.read``
   - ``sharing.read``

3. Verifique que existan archivos en la cuenta de Dropbox

Errores de Limite de Tasa de API
--------------------------------

**Sintoma**: Error ``429 Too Many Requests``

**Solucion**:

1. Para el plan Basic, configure ``basic_plan=true``
2. Aumente el intervalo de rastreo
3. Distribuya la carga usando multiples tokens de acceso

No Se Pueden Obtener Documentos Paper
-------------------------------------

**Sintoma**: Los documentos Paper no se rastrean

**Verifique**:

1. Verifique que el nombre del manejador sea ``DropboxPaperDataStore``
2. Verifique que se incluya el permiso ``files.content.read``
3. Verifique que realmente existan documentos Paper

Cuando Hay un Gran Numero de Archivos
-------------------------------------

**Sintoma**: El rastreo toma mucho tiempo o se agota el tiempo

**Solucion**:

1. Divida los almacenes de datos en multiples (por unidad de carpeta, etc.)
2. Distribuya la carga con configuracion de programacion
3. Para el plan Basic, tenga en cuenta los limites de tasa de API

Permisos y Control de Acceso
============================

Reflejar Permisos de Uso Compartido de Dropbox
----------------------------------------------

Puede reflejar la configuracion de uso compartido de Dropbox en los permisos de Fess:

Parametros:

::

    access_token=sl.AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEfGhIj
    default_permissions={role}dropbox-users

Script:

::

    url=file.url
    title=file.name
    content=file.contents
    role=file.roles
    mimetype=file.mimetype
    filename=file.name
    last_modified=file.client_modified

``file.roles`` o ``paper.roles`` contienen informacion de uso compartido de Dropbox.

Informacion de Referencia
=========================

- :doc:`ds-overview` - Descripcion General de Conectores de Almacen de Datos
- :doc:`ds-box` - Conector de Box
- :doc:`ds-gsuite` - Conector de Google Workspace
- :doc:`../../admin/dataconfig-guide` - Guia de Configuracion de Almacen de Datos
- `Desarrolladores de Dropbox <https://www.dropbox.com/developers>`_
- `Documentacion de API de Dropbox <https://www.dropbox.com/developers/documentation>`_
