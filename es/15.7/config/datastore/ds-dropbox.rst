==================================
Conector de Dropbox
==================================

Descripción General
===================

El conector de Dropbox proporciona funcionalidad para obtener archivos del almacenamiento
en la nube Dropbox y registrarlos en el índice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-dropbox``.

Servicios Compatibles
=====================

- Dropbox (almacenamiento de archivos)
- Dropbox Paper (documentos)

Requisitos Previos
==================

1. Se requiere instalación del plugin
2. Se requiere una cuenta de desarrollador de Dropbox y la creación de una aplicación
3. Se requiere obtener un token de acceso

Instalación del Plugin
----------------------

Instale desde la consola de administración en "Sistema" -> "Plugins":

1. Descargue ``fess-ds-dropbox-X.X.X.jar`` de Maven Central
2. Cargue e instale desde la pantalla de administración de plugins
3. Reinicie |Fess|

O consulte :doc:`../../admin/plugin-guide` para más detalles.

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
     - Company Dropbox
   * - Nombre del Manejador
     - DropboxDataStore o DropboxPaperDataStore
   * - Habilitado
     - Activado

Configuración de Parámetros
----------------------------

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

Lista de Parámetros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parámetro
     - Requerido
     - Descripción
   * - ``access_token``
     - Sí
     - Token de acceso de Dropbox (generado en App Console)
   * - ``basic_plan``
     - No
     - ``true`` para cuenta individual, ``false`` para cuenta de equipo (predeterminado: ``false``)
   * - ``max_size``
     - No
     - Tamaño máximo de archivo para indexación en bytes (predeterminado: ``10000000``)
   * - ``number_of_threads``
     - No
     - Número de hilos para rastreo (predeterminado: ``1``)
   * - ``ignore_folder``
     - No
     - Indica si se omiten los metadatos de carpetas (predeterminado: ``true``)
   * - ``ignore_error``
     - No
     - Indica si se ignoran los errores durante la extracción de contenido (predeterminado: ``true``)
   * - ``supported_mimetypes``
     - No
     - Patrones regex para tipos MIME permitidos, separados por comas (predeterminado: ``.*``)
   * - ``include_pattern``
     - No
     - Patrón de URL a incluir en el rastreo
   * - ``exclude_pattern``
     - No
     - Patrón de URL a excluir del rastreo
   * - ``default_permissions``
     - No
     - Permisos predeterminados para documentos indexados, separados por comas
   * - ``max_cached_content_size``
     - No
     - Tamaño máximo de contenido almacenado en cache en memoria en bytes. El contenido que supere este límite se escribe en un archivo temporal (predeterminado: ``1048576``)
   * - ``readInterval``
     - No
     - Tiempo de espera en milisegundos entre el procesamiento de cada registro (predeterminado: ``0``)

Configuración de Script
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
     - Descripción
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
     - Tamaño del archivo (bytes)
   * - ``file.client_modified``
     - Fecha de última modificación del lado del cliente
   * - ``file.server_modified``
     - Fecha de última modificación del lado del servidor
   * - ``file.roles``
     - Permisos de acceso del archivo
   * - ``file.id``
     - ID del archivo de Dropbox
   * - ``file.path_lower``
     - Ruta del archivo en minúsculas
   * - ``file.parent_shared_folder_id``
     - ID de la carpeta compartida principal
   * - ``file.content_hash``
     - Hash del contenido
   * - ``file.rev``
     - Revisión del archivo

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
     - Descripción
   * - ``paper.url``
     - Enlace de vista previa del documento Paper
   * - ``paper.contents``
     - Contenido de texto del documento Paper
   * - ``paper.mimetype``
     - Tipo MIME
   * - ``paper.filetype``
     - Tipo de archivo
   * - ``paper.title``
     - Título del documento Paper
   * - ``paper.owner``
     - Propietario del documento Paper
   * - ``paper.roles``
     - Permisos de acceso del documento
   * - ``paper.revision``
     - Revisión del documento Paper

Configuración de Autenticación de Dropbox
==========================================

Tipo de Cuenta y Token de Acceso
---------------------------------

Este conector alterna entre dos modos de operación según el parámetro ``basic_plan``.
Dado que el tipo de aplicación y de token de acceso que se debe crear difiere, verifíquelo primero.

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Modo
     - ``basic_plan``
     - Descripción
   * - Cuenta de equipo (predeterminado)
     - ``false``
     - Destinado a cuentas Dropbox Business (equipo). Requiere un token de acceso con permisos de administrador del equipo, y rastrea archivos de los miembros del equipo y carpetas de equipo de forma transversal.
   * - Cuenta individual
     - ``true``
     - Destinado a cuentas individuales (no de equipo). Utiliza un token de acceso con alcance estándar y rastrea directamente los archivos dentro de esa cuenta.

.. note::
   Con la configuración predeterminada (``basic_plan=false``), se utilizan las API de administración de equipos
   (lista de miembros, acceso a archivos por miembro, carpetas de equipo), por lo que es obligatorio
   disponer de una cuenta Dropbox Business y un token con permisos de administrador del equipo.
   Si utiliza una cuenta individual, asegúrese de configurar ``basic_plan=true``.

Pasos para Obtener el Token de Acceso
--------------------------------------

1. Crear una aplicación en Dropbox App Console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Acceda a https://www.dropbox.com/developers/apps:

1. Haga clic en "Create app"
2. Seleccione "Scoped access" para el tipo de API
3. Seleccione el tipo de acceso (se recomienda "Full Dropbox" para rastrear cuentas de equipo de forma transversal)
4. Ingrese el nombre de la aplicación y cree

2. Configuración de Permisos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

En la pestaña "Permissions", seleccione los permisos requeridos:

**Permisos necesarios para el rastreo de archivos y Paper**:

- ``files.metadata.read`` - Lectura de metadatos de archivos
- ``files.content.read`` - Lectura de contenido de archivos y documentos Paper
- ``sharing.read`` - Lectura de información de uso compartido

**Permisos adicionales requeridos para cuentas de equipo (``basic_plan=false``)**:

- ``members.read`` - Lectura de la lista de miembros del equipo
- Permisos de acceso a datos de equipo y espacios de equipo (necesarios para rastrear archivos por miembro y carpetas de equipo)

.. note::
   En el modo de cuenta de equipo, se accede a cada miembro y carpeta de equipo como administrador del equipo.
   Habilite los permisos de equipo mencionados en la pestaña Permissions y genere un token de administrador del equipo.

3. Generar Token de Acceso
~~~~~~~~~~~~~~~~~~~~~~~~~~

En la pestaña "Settings":

1. Desplácese hasta la sección "Generated access token"
2. Haga clic en el botón "Generate"
3. Copie el token generado (este token se muestra solo una vez)

.. warning::
   Guarde el token de acceso de forma segura. Con este token,
   es posible acceder a la cuenta de Dropbox.

4. Configurar el Token
~~~~~~~~~~~~~~~~~~~~~~

Configure el token obtenido en los parámetros:

::

    access_token=sl.your-dropbox-token-here

Configuración para Cuenta Individual
=====================================

Uso con Cuentas Individuales
-----------------------------

Para cuentas individuales (no cuentas de equipo),
configure el parámetro ``basic_plan`` como ``true``:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=true

Cuando es ``false`` (predeterminado), opera como cuenta de equipo y rastrea archivos de miembros y carpetas del equipo.
Cuando es ``true``, opera como cuenta individual y rastrea archivos directamente de la cuenta.

Ejemplos de Uso
===============

Rastrear Todos los Archivos de Dropbox
---------------------------------------

Parámetros:

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

Parámetros:

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

Parámetros:

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

Rastrear Solo Tipos de Archivo Específicos
-------------------------------------------

Para indexar únicamente tipos MIME específicos, especifique en el parámetro ``supported_mimetypes``
las expresiones regulares de los tipos MIME permitidos, separadas por comas.

.. note::
   Los scripts del almacén de datos evalúan cada línea como una expresión independiente con el formato ``campo=expresion``.
   Por ello, no es posible asignar múltiples campos en un bloque ``if`` de varias líneas.
   El filtrado por tipo MIME debe realizarse mediante el parámetro ``supported_mimetypes``, no con scripts.

Parámetros (solo PDF y archivos Word):

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

Solución de Problemas
======================

Errores de Autenticación
-------------------------

**Síntoma**: ``Invalid access token`` o ``401 Unauthorized``

**Verifique**:

1. Verifique que el token de acceso se haya copiado correctamente
2. Verifique que el token no haya expirado (use token de larga duración)
3. Verifique que los permisos requeridos estén otorgados en Dropbox App Console
4. Verifique que la aplicación no esté desactivada

No Se Pueden Obtener Archivos
------------------------------

**Síntoma**: El rastreo tiene éxito pero hay 0 archivos

**Verifique**:

1. Verifique que el "Access type" de la aplicación sea apropiado:

   - "Full Dropbox": Puede acceder a todo Dropbox
   - "App folder": Solo puede acceder a una carpeta específica

2. Verifique que los permisos requeridos estén otorgados:

   - ``files.metadata.read``
   - ``files.content.read``
   - ``sharing.read``

3. Verifique que existan archivos en la cuenta de Dropbox

Errores de Límite de Tasa de API
----------------------------------

**Síntoma**: Error ``429 Too Many Requests``

**Solución**:

1. Configure ``readInterval`` para aumentar el intervalo de procesamiento entre archivos
2. Reduzca ``number_of_threads`` para disminuir el número de solicitudes simultáneas
3. Divida el almacén de datos en varios (por carpeta u otro criterio) y escalone los horarios de ejecución

.. note::
   ``basic_plan`` es un parámetro que alterna el tipo de cuenta (equipo/individual)
   y no afecta al ajuste de los límites de tasa. Configúrelo correctamente según su cuenta.

No Se Pueden Obtener Documentos Paper
---------------------------------------

**Síntoma**: Los documentos Paper no se rastrean

**Verifique**:

1. Verifique que el nombre del manejador sea ``DropboxPaperDataStore``
2. Verifique que se incluya el permiso ``files.content.read``
3. Verifique que realmente existan documentos Paper

Cuando Hay un Gran Número de Archivos
---------------------------------------

**Síntoma**: El rastreo toma mucho tiempo o se agota el tiempo

**Solución**:

1. Divida los almacenes de datos en múltiples (por unidad de carpeta, etc.)
2. Distribuya la carga con configuración de programación
3. En el plan Basic, tenga en cuenta los límites de tasa de API

Permisos y Control de Acceso
==============================

Reflejar Permisos de Uso Compartido de Dropbox
------------------------------------------------

Puede reflejar la configuración de uso compartido de Dropbox en los permisos de Fess:

Parámetros:

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

``file.roles`` o ``paper.roles`` contienen información de uso compartido de Dropbox.

Información de Referencia
==========================

- :doc:`ds-overview` - Descripción General de Conectores de Almacén de Datos
- :doc:`ds-box` - Conector de Box
- :doc:`ds-gsuite` - Conector de Google Workspace
- :doc:`../../admin/dataconfig-guide` - Guía de Configuración de Almacén de Datos
- `Desarrolladores de Dropbox <https://www.dropbox.com/developers>`_
- `Documentación de API de Dropbox <https://www.dropbox.com/developers/documentation>`_
