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
----------------------------

::

    access_token=sl.your-dropbox-token-here
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
     - ``true`` para cuenta individual, ``false`` para cuenta de equipo (predeterminado: ``false``)
   * - ``max_size``
     - No
     - Tamano maximo de archivo para indexacion en bytes (predeterminado: ``10000000``)
   * - ``number_of_threads``
     - No
     - Numero de hilos para rastreo (predeterminado: ``1``)
   * - ``ignore_folder``
     - No
     - Indica si se omiten los metadatos de carpetas (predeterminado: ``true``)
   * - ``ignore_error``
     - No
     - Indica si se ignoran los errores durante la extraccion de contenido (predeterminado: ``true``)
   * - ``supported_mimetypes``
     - No
     - Patrones regex para tipos MIME permitidos, separados por comas (predeterminado: ``.*``)
   * - ``include_pattern``
     - No
     - Patron de URL a incluir en el rastreo
   * - ``exclude_pattern``
     - No
     - Patron de URL a excluir del rastreo
   * - ``default_permissions``
     - No
     - Permisos predeterminados para documentos indexados, separados por comas
   * - ``max_cached_content_size``
     - No
     - Tamano maximo de contenido almacenado en cache en memoria en bytes. El contenido que supere este limite se escribe en un archivo temporal (predeterminado: ``1048576``)
   * - ``readInterval``
     - No
     - Tiempo de espera en milisegundos entre el procesamiento de cada registro (predeterminado: ``0``)

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
   * - ``file.id``
     - ID del archivo de Dropbox
   * - ``file.path_lower``
     - Ruta del archivo en minusculas
   * - ``file.parent_shared_folder_id``
     - ID de la carpeta compartida principal
   * - ``file.content_hash``
     - Hash del contenido
   * - ``file.rev``
     - Revision del archivo

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
   * - ``paper.revision``
     - Revision del documento Paper

Configuracion de Autenticacion de Dropbox
==========================================

Tipo de Cuenta y Token de Acceso
---------------------------------

Este conector alterna entre dos modos de operacion segun el parametro ``basic_plan``.
Dado que el tipo de aplicacion y de token de acceso que se debe crear difiere, verifiquelo primero.

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Modo
     - ``basic_plan``
     - Descripcion
   * - Cuenta de equipo (predeterminado)
     - ``false``
     - Destinado a cuentas Dropbox Business (equipo). Requiere un token de acceso con permisos de administrador del equipo, y rastrea archivos de los miembros del equipo y carpetas de equipo de forma transversal.
   * - Cuenta individual
     - ``true``
     - Destinado a cuentas individuales (no de equipo). Utiliza un token de acceso con alcance estandar y rastrea directamente los archivos dentro de esa cuenta.

.. note::
   Con la configuracion predeterminada (``basic_plan=false``), se utilizan las API de administracion de equipos
   (lista de miembros, acceso a archivos por miembro, carpetas de equipo), por lo que es obligatorio
   disponer de una cuenta Dropbox Business y un token con permisos de administrador del equipo.
   Si utiliza una cuenta individual, asegurese de configurar ``basic_plan=true``.

Pasos para Obtener el Token de Acceso
--------------------------------------

1. Crear una aplicacion en Dropbox App Console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Acceda a https://www.dropbox.com/developers/apps:

1. Haga clic en "Create app"
2. Seleccione "Scoped access" para el tipo de API
3. Seleccione el tipo de acceso (se recomienda "Full Dropbox" para rastrear cuentas de equipo de forma transversal)
4. Ingrese el nombre de la aplicacion y cree

2. Configuracion de Permisos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

En la pestana "Permissions", seleccione los permisos requeridos:

**Permisos necesarios para el rastreo de archivos y Paper**:

- ``files.metadata.read`` - Lectura de metadatos de archivos
- ``files.content.read`` - Lectura de contenido de archivos y documentos Paper
- ``sharing.read`` - Lectura de informacion de uso compartido

**Permisos adicionales requeridos para cuentas de equipo (``basic_plan=false``)**:

- ``members.read`` - Lectura de la lista de miembros del equipo
- Permisos de acceso a datos de equipo y espacios de equipo (necesarios para rastrear archivos por miembro y carpetas de equipo)

.. note::
   En el modo de cuenta de equipo, se accede a cada miembro y carpeta de equipo como administrador del equipo.
   Habilite los permisos de equipo mencionados en la pestana Permissions y genere un token de administrador del equipo.

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

    access_token=sl.your-dropbox-token-here

Configuracion para Cuenta Individual
=====================================

Uso con Cuentas Individuales
-----------------------------

Para cuentas individuales (no cuentas de equipo),
configure el parametro ``basic_plan`` como ``true``:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=true

Cuando es ``false`` (predeterminado), opera como cuenta de equipo y rastrea archivos de miembros y carpetas del equipo.
Cuando es ``true``, opera como cuenta individual y rastrea archivos directamente de la cuenta.

Ejemplos de Uso
===============

Rastrear Todos los Archivos de Dropbox
---------------------------------------

Parametros:

::

    access_token=sl.your-dropbox-token-here
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
--------------------------------------

Parametros:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

Script:

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype

Rastrear con Permisos
----------------------

Parametros:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false
    default_permissions={role}admin

Script (archivos de Dropbox):

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filename=file.name
    content_length=file.size
    last_modified=file.client_modified
    role=file.roles

Script (Dropbox Paper):

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype
    role=paper.roles

Rastrear Solo Tipos de Archivo Especificos
-------------------------------------------

Para indexar unicamente tipos MIME especificos, especifique en el parametro ``supported_mimetypes``
las expresiones regulares de los tipos MIME permitidos, separadas por comas.

.. note::
   Los scripts del almacen de datos evaluan cada linea como una expresion independiente con el formato ``campo=expresion``.
   Por ello, no es posible asignar multiples campos en un bloque ``if`` de varias lineas.
   El filtrado por tipo MIME debe realizarse mediante el parametro ``supported_mimetypes``, no con scripts.

Parametros (solo PDF y archivos Word):

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false
    supported_mimetypes=application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document

Script:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filename=file.name
    last_modified=file.client_modified

Solucion de Problemas
======================

Errores de Autenticacion
-------------------------

**Sintoma**: ``Invalid access token`` o ``401 Unauthorized``

**Verifique**:

1. Verifique que el token de acceso se haya copiado correctamente
2. Verifique que el token no haya expirado (use token de larga duracion)
3. Verifique que los permisos requeridos esten otorgados en Dropbox App Console
4. Verifique que la aplicacion no este desactivada

No Se Pueden Obtener Archivos
------------------------------

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
----------------------------------

**Sintoma**: Error ``429 Too Many Requests``

**Solucion**:

1. Configure ``readInterval`` para aumentar el intervalo de procesamiento entre archivos
2. Reduzca ``number_of_threads`` para disminuir el numero de solicitudes simultaneas
3. Divida el almacen de datos en varios (por carpeta u otro criterio) y escalone los horarios de ejecucion

.. note::
   ``basic_plan`` es un parametro que alterna el tipo de cuenta (equipo/individual)
   y no afecta al ajuste de los limites de tasa. Configurelo correctamente segun su cuenta.

No Se Pueden Obtener Documentos Paper
---------------------------------------

**Sintoma**: Los documentos Paper no se rastrean

**Verifique**:

1. Verifique que el nombre del manejador sea ``DropboxPaperDataStore``
2. Verifique que se incluya el permiso ``files.content.read``
3. Verifique que realmente existan documentos Paper

Cuando Hay un Gran Numero de Archivos
---------------------------------------

**Sintoma**: El rastreo toma mucho tiempo o se agota el tiempo

**Solucion**:

1. Divida los almacenes de datos en multiples (por unidad de carpeta, etc.)
2. Distribuya la carga con configuracion de programacion
3. En el plan Basic, tenga en cuenta los limites de tasa de API

Permisos y Control de Acceso
==============================

Reflejar Permisos de Uso Compartido de Dropbox
------------------------------------------------

Puede reflejar la configuracion de uso compartido de Dropbox en los permisos de Fess:

Parametros:

::

    access_token=sl.your-dropbox-token-here
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
==========================

- :doc:`ds-overview` - Descripcion General de Conectores de Almacen de Datos
- :doc:`ds-box` - Conector de Box
- :doc:`ds-gsuite` - Conector de Google Workspace
- :doc:`../../admin/dataconfig-guide` - Guia de Configuracion de Almacen de Datos
- `Desarrolladores de Dropbox <https://www.dropbox.com/developers>`_
- `Documentacion de API de Dropbox <https://www.dropbox.com/developers/documentation>`_
