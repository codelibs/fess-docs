===========================
Conector de Box
===========================

Descripción general
===================

El conector de Box proporciona la funcionalidad de obtener archivos del almacenamiento
en la nube Box.com y registrarlos en el índice de |Fess|.

Este conector se conecta a la empresa mediante JWT (Server Authentication) y rastreo
recursivo de los archivos accesibles para cada usuario de la empresa suplantando su
identidad (impersonation). Los usuarios a rastrear pueden acotarse mediante el
parámetro ``filter_term``.

Esta funcionalidad requiere el plugin ``fess-ds-box``.

Requisitos previos
==================

1. Se requiere la instalación del plugin
2. Se requiere una cuenta de desarrollador de Box y la creación de una aplicación
3. Se requiere la configuración de autenticación JWT (JSON Web Token)

Instalación del plugin
----------------------

Método 1: Colocar el archivo JAR directamente

::

    # Descargar desde Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-box/X.X.X/fess-ds-box-X.X.X.jar

    # Colocar
    cp fess-ds-box-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # o
    cp fess-ds-box-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Método 2: Instalar desde la consola de administración

1. Abra "Sistema" -> "Plugins"
2. Cargue el archivo JAR
3. Reinicie |Fess|

Método de configuración
=======================

Configure desde la consola de administración en "Rastreador" -> "Almacén de datos" -> "Crear nuevo".

Configuración básica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Elemento
     - Ejemplo de configuración
   * - Nombre
     - Company Box Storage
   * - Nombre del manejador
     - BoxDataStore
   * - Habilitado
     - Activado

Configuración de parámetros
----------------------------

Ejemplo de autenticación JWT:

::

    client_id=hdf8a7sd9f8a7sdf9a87sdf98a7sd
    client_secret=kMN7sd8f7a9sd8f7a9sd8f7a9sd8f
    public_key_id=4tg5h6j7
    private_key=<YOUR_PRIVATE_KEY>
    passphrase=7ba8sd9f7a9sd8f7a9sd8f7a9sd8f
    enterprise_id=1923456

Lista de parámetros
~~~~~~~~~~~~~~~~~~~

Parámetros de autenticación (obligatorios)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parámetro
     - Requerido
     - Descripción
   * - ``client_id``
     - Sí
     - ID de cliente de la aplicación Box
   * - ``client_secret``
     - Sí
     - Secreto de cliente de la aplicación Box
   * - ``public_key_id``
     - Sí
     - ID de la clave pública
   * - ``private_key``
     - Sí
     - Clave privada (formato PEM, los saltos de línea se representan con ``\n``)
   * - ``passphrase``
     - Sí
     - Frase de contraseña de la clave privada
   * - ``enterprise_id``
     - Sí
     - ID de empresa de Box

Parámetros de rastreo (opcionales)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Parámetro
     - Valor predeterminado
     - Descripción
   * - ``max_size``
     - ``10000000``
     - Tamaño máximo de archivo a rastrear (bytes). El valor predeterminado es 10 MB.
   * - ``supported_mimetypes``
     - ``.*``
     - Tipos MIME a rastrear (expresión regular). Se pueden especificar varios separados por comas.
   * - ``include_pattern``
     - (ninguno)
     - Patrón de URL a incluir en el rastreo
   * - ``exclude_pattern``
     - (ninguno)
     - Patrón de URL a excluir del rastreo
   * - ``number_of_threads``
     - ``1``
     - Número de hilos del proceso de rastreo
   * - ``ignore_folder``
     - ``true``
     - Indica si las carpetas deben quedar fuera del índice. En la implementación actual, las carpetas en sí mismas no se indexan (solo los archivos son el objetivo), por lo que este parámetro no tiene efecto.
   * - ``ignore_error``
     - ``true``
     - Indica si se debe continuar el procesamiento cuando ocurre un error
   * - ``filter_term``
     - (ninguno)
     - Condición de filtro para acotar los usuarios de la empresa a rastrear. Si no se específica, se incluyen todos los usuarios de la empresa.
   * - ``fields``
     - (todos los campos)
     - Especificación de los campos a obtener desde la API de Box

Parámetros de conexión (opcionales)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Parámetro
     - Valor predeterminado
     - Descripción
   * - ``base_url``
     - ``https://app.box.com``
     - URL base para construir la URL de apertura del archivo en el navegador (``file.url``). No afecta a los endpoints de la API utilizados por el SDK de Box.
   * - ``max_retry_count``
     - ``10``
     - Número máximo de reintentos de la llamada a la API
   * - ``proxy_host``
     - (ninguno)
     - Nombre de host del proxy HTTP
   * - ``proxy_port``
     - (ninguno)
     - Número de puerto del proxy HTTP
   * - ``refresh_token_interval``
     - ``3540``
     - Intervalo de actualizacion del token (segundos). El valor predeterminado es 59 minutos.

Configuración de script
-----------------------

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

Campos disponibles
~~~~~~~~~~~~~~~~~~

Campos principales
^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripción
   * - ``file.url``
     - Enlace para abrir el archivo en el navegador
   * - ``file.contents``
     - Contenido de texto del archivo
   * - ``file.mimetype``
     - Tipo MIME del archivo
   * - ``file.filetype``
     - Tipo de archivo
   * - ``file.name``
     - Nombre del archivo
   * - ``file.size``
     - Tamaño del archivo (bytes)
   * - ``file.created_at``
     - Fecha y hora de creación
   * - ``file.modified_at``
     - Fecha y hora de última modificación
   * - ``file.download_url``
     - URL de descarga directa de Box
   * - ``file.id``
     - ID de elemento de Box
   * - ``file.description``
     - Descripción del archivo
   * - ``file.extension``
     - Extensión del archivo
   * - ``file.sha1``
     - Hash SHA1 del archivo
   * - ``file.path_collection``
     - Lista de rutas de carpeta

Campos de metadatos
^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripción
   * - ``file.type``
     - Tipo de elemento ("file" o "folder")
   * - ``file.file_version``
     - Información de versión del archivo
   * - ``file.sequence_id``
     - ID de secuencia
   * - ``file.etag``
     - Hash ETag
   * - ``file.trashed_at``
     - Fecha y hora de traslado a la papelera
   * - ``file.purged_at``
     - Fecha y hora de eliminación definitiva
   * - ``file.content_created_at``
     - Fecha y hora de creación del contenido
   * - ``file.content_modified_at``
     - Fecha y hora de modificación del contenido
   * - ``file.created_by``
     - Información del creador
   * - ``file.modified_by``
     - Información del modificador
   * - ``file.owned_by``
     - Información del propietario
   * - ``file.shared_link``
     - Información del enlace compartido
   * - ``file.parent``
     - Información de la carpeta padre
   * - ``file.item_status``
     - Estado del elemento
   * - ``file.version_number``
     - Número de versión
   * - ``file.comment_count``
     - Número de comentarios
   * - ``file.permissions``
     - Información de permisos
   * - ``file.tags``
     - Información de etiquetas
   * - ``file.lock``
     - Información de bloqueo
   * - ``file.is_package``
     - Indicador de paquete
   * - ``file.is_watermark``
     - Indicador de marca de agua
   * - ``file.collections``
     - Información de colecciones
   * - ``file.representations``
     - Información de representaciones
   * - ``file.api``
     - Objeto BoxFileAPI (para obtener información de colaboración y permisos)

Para más detalles, consulte el `Objeto File de Box <https://developer.box.com/reference#file-object>`_.

Configuración de autenticación de Box
======================================

Pasos de configuración de autenticación JWT
--------------------------------------------

1. Crear una aplicación en Box Developer Console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Acceda a https://app.box.com/developers/console:

1. Haga clic en "Create New App"
2. Seleccione "Custom App"
3. Seleccione "Server Authentication (with JWT)" como método de autenticación
4. Ingrese el nombre de la aplicación y cree

2. Configuración de la aplicación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure en la pestaña "Configuration":

**Application Scopes**:

- Marque "Read all files and folders stored in Box"

**Advanced Features**:

- Haga clic en "Generate a Public/Private Keypair"
- Descargue el archivo JSON generado (importante!)

**App Access Level**:

- Seleccione "App + Enterprise Access"

3. Aprobar en la empresa
~~~~~~~~~~~~~~~~~~~~~~~~~

En la consola de administración de Box:

1. Abra "Apps" -> "Custom Apps"
2. Apruebe la aplicación creada

4. Obtener las credenciales de autenticación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Obtenga la siguiente información del archivo JSON descargado:

::

    {
      "boxAppSettings": {
        "clientID": "hdf8a7sd...",         // client_id
        "clientSecret": "kMN7sd8f...",      // client_secret
        "appAuth": {
          "publicKeyID": "4tg5h6j7",        // public_key_id
          "privateKey": "-----BEGIN...",    // private_key
          "passphrase": "7ba8sd9f..."       // passphrase
        }
      },
      "enterpriseID": "1923456"             // enterprise_id
    }

Formato de la clave privada
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Reemplace los saltos de línea de ``private_key`` con ``\n`` para convertirla en una sola línea:

::

    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgk...=\n-----END ENCRYPTED PRIVATE KEY-----\n

Ejemplos de uso
===============

Rastrear todo el almacenamiento Box de la empresa
--------------------------------------------------

Parámetros:

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
    enterprise_id=123456789

Script:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

Rastrear solo una carpeta específica
-------------------------------------

Es posible filtrar por ruta de carpeta mediante el parámetro ``include_pattern``.

Parámetros:

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
    enterprise_id=123456789
    include_pattern=.*Documents/Projects/.*

Script:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

Rastrear solo archivos PDF
--------------------------

Es posible filtrar por tipo MIME mediante el parámetro ``supported_mimetypes``.

Parámetros:

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
    enterprise_id=123456789
    supported_mimetypes=application/pdf

Script:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

Solución de problemas
=====================

Errores de autenticación
------------------------

**Síntoma**: ``Authentication failed`` o ``Invalid grant``

**Verifique**:

1. Verifique que ``client_id`` y ``client_secret`` sean correctos
2. Verifique que la clave privada se haya copiado correctamente (los saltos de línea estén como ``\n``)
3. Verifique que la frase de contraseña sea correcta
4. Verifique que la aplicación esté aprobada en la consola de administración de Box
5. Verifique que ``enterprise_id`` sea correcto

Error de formato de clave privada
----------------------------------

**Síntoma**: ``Invalid private key format``

**Solución**:

Verifique que los saltos de línea de la clave privada estén correctamente convertidos a ``\n``:

::

    # Formato correcto
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDj...\n-----END ENCRYPTED PRIVATE KEY-----\n

    # Formato incorrecto (contiene saltos de linea reales)
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----
    MIIFDj...
    -----END ENCRYPTED PRIVATE KEY-----

No se pueden obtener archivos
------------------------------

**Síntoma**: El rastreo finaliza con éxito pero hay 0 archivos

**Verifique**:

1. Verifique que "Read all files and folders" esté habilitado en Application Scopes
2. Verifique que App Access Level sea "App + Enterprise Access"
3. Verifique que realmente existan archivos en el almacenamiento de Box
4. Verifique que la cuenta de servicio tenga los permisos apropiados

Cuando hay un gran número de archivos
--------------------------------------

**Síntoma**: El rastreo tarda mucho tiempo o se agota el tiempo de espera

**Solución**:

Divida el procesamiento en la configuración del almacén de datos:

1. Ajuste el intervalo de rastreo
2. Configure múltiples almacenes de datos (por unidad de carpeta, etc.)
3. Aumente el número de hilos con el parámetro ``number_of_threads``
4. Distribuya la carga con la configuración de programación

Permisos y control de acceso
=============================

Reflejar los permisos de colaboración de Box
---------------------------------------------

Mediante el objeto ``BoxFileAPI`` proporcionado por el campo ``file.api``, es posible
asignar la información de colaboración de Box a los roles de búsqueda de |Fess|.
``file.api.collaborationRoles`` devuelve una lista de roles de búsqueda correspondientes
a los usuarios y grupos que tienen acceso al archivo.

Establecer los permisos en el script:

::

    url=file.url
    title=file.name
    content=file.contents
    role=file.api.collaborationRoles
    mimetype=file.mimetype
    filename=file.name
    created=file.created_at
    last_modified=file.modified_at

.. note::
   ``file.api.collaborationRoles`` obtiene la información de colaboración de cada archivo,
   lo que incrementa el número de llamadas a la API de Box y puede hacer que el rastreo
   tarde más tiempo.

Para asignar un rol fijo a todos los archivos, especifíquelo de la siguiente manera:

::

    role="{role}box-users"

Información de referencia
==========================

- :doc:`ds-overview` - Descripción general de conectores de almacén de datos
- :doc:`ds-dropbox` - Conector de Dropbox
- :doc:`ds-gsuite` - Conector de Google Workspace
- :doc:`../../admin/dataconfig-guide` - Guía de configuración de almacén de datos
- `Documentación para desarrolladores de Box <https://developer.box.com/>`_
- `Autenticación de Box Platform <https://developer.box.com/guides/authentication/>`_
