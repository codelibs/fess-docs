===========================
Conector de Box
===========================

Descripcion general
===================

El conector de Box proporciona la funcionalidad de obtener archivos del almacenamiento
en la nube Box.com y registrarlos en el indice de |Fess|.

Este conector se conecta a la empresa mediante JWT (Server Authentication) y rastreo
recursivo de los archivos accesibles para cada usuario de la empresa suplantando su
identidad (impersonation). Los usuarios a rastrear pueden acotarse mediante el
parametro ``filter_term``.

Esta funcionalidad requiere el plugin ``fess-ds-box``.

Requisitos previos
==================

1. Se requiere la instalacion del plugin
2. Se requiere una cuenta de desarrollador de Box y la creacion de una aplicacion
3. Se requiere la configuracion de autenticacion JWT (JSON Web Token)

Instalacion del plugin
----------------------

Metodo 1: Colocar el archivo JAR directamente

::

    # Descargar desde Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-box/X.X.X/fess-ds-box-X.X.X.jar

    # Colocar
    cp fess-ds-box-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # o
    cp fess-ds-box-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Metodo 2: Instalar desde la consola de administracion

1. Abra "Sistema" -> "Plugins"
2. Cargue el archivo JAR
3. Reinicie |Fess|

Metodo de configuracion
=======================

Configure desde la consola de administracion en "Rastreador" -> "Almacen de datos" -> "Crear nuevo".

Configuracion basica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Elemento
     - Ejemplo de configuracion
   * - Nombre
     - Company Box Storage
   * - Nombre del manejador
     - BoxDataStore
   * - Habilitado
     - Activado

Configuracion de parametros
----------------------------

Ejemplo de autenticacion JWT:

::

    client_id=hdf8a7sd9f8a7sdf9a87sdf98a7sd
    client_secret=kMN7sd8f7a9sd8f7a9sd8f7a9sd8f
    public_key_id=4tg5h6j7
    private_key=<YOUR_PRIVATE_KEY>
    passphrase=7ba8sd9f7a9sd8f7a9sd8f7a9sd8f
    enterprise_id=1923456

Lista de parametros
~~~~~~~~~~~~~~~~~~~

Parametros de autenticacion (obligatorios)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametro
     - Requerido
     - Descripcion
   * - ``client_id``
     - Si
     - ID de cliente de la aplicacion Box
   * - ``client_secret``
     - Si
     - Secreto de cliente de la aplicacion Box
   * - ``public_key_id``
     - Si
     - ID de la clave publica
   * - ``private_key``
     - Si
     - Clave privada (formato PEM, los saltos de linea se representan con ``\n``)
   * - ``passphrase``
     - Si
     - Frase de contrasena de la clave privada
   * - ``enterprise_id``
     - Si
     - ID de empresa de Box

Parametros de rastreo (opcionales)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Parametro
     - Valor predeterminado
     - Descripcion
   * - ``max_size``
     - ``10000000``
     - Tamano maximo de archivo a rastrear (bytes). El valor predeterminado es 10 MB.
   * - ``supported_mimetypes``
     - ``.*``
     - Tipos MIME a rastrear (expresion regular). Se pueden especificar varios separados por comas.
   * - ``include_pattern``
     - (ninguno)
     - Patron de URL a incluir en el rastreo
   * - ``exclude_pattern``
     - (ninguno)
     - Patron de URL a excluir del rastreo
   * - ``number_of_threads``
     - ``1``
     - Numero de hilos del proceso de rastreo
   * - ``ignore_folder``
     - ``true``
     - Indica si las carpetas deben quedar fuera del indice. En la implementacion actual, las carpetas en si mismas no se indexan (solo los archivos son el objetivo), por lo que este parametro no tiene efecto.
   * - ``ignore_error``
     - ``true``
     - Indica si se debe continuar el procesamiento cuando ocurre un error
   * - ``filter_term``
     - (ninguno)
     - Condicion de filtro para acotar los usuarios de la empresa a rastrear. Si no se especifica, se incluyen todos los usuarios de la empresa.
   * - ``fields``
     - (todos los campos)
     - Especificacion de los campos a obtener desde la API de Box

Parametros de conexion (opcionales)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Parametro
     - Valor predeterminado
     - Descripcion
   * - ``base_url``
     - ``https://app.box.com``
     - URL base para construir la URL de apertura del archivo en el navegador (``file.url``). No afecta a los endpoints de la API utilizados por el SDK de Box.
   * - ``max_retry_count``
     - ``10``
     - Numero maximo de reintentos de la llamada a la API
   * - ``proxy_host``
     - (ninguno)
     - Nombre de host del proxy HTTP
   * - ``proxy_port``
     - (ninguno)
     - Numero de puerto del proxy HTTP
   * - ``refresh_token_interval``
     - ``3540``
     - Intervalo de actualizacion del token (segundos). El valor predeterminado es 59 minutos.

Configuracion de script
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
     - Descripcion
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
     - Tamano del archivo (bytes)
   * - ``file.created_at``
     - Fecha y hora de creacion
   * - ``file.modified_at``
     - Fecha y hora de ultima modificacion
   * - ``file.download_url``
     - URL de descarga directa de Box
   * - ``file.id``
     - ID de elemento de Box
   * - ``file.description``
     - Descripcion del archivo
   * - ``file.extension``
     - Extension del archivo
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
     - Descripcion
   * - ``file.type``
     - Tipo de elemento ("file" o "folder")
   * - ``file.file_version``
     - Informacion de version del archivo
   * - ``file.sequence_id``
     - ID de secuencia
   * - ``file.etag``
     - Hash ETag
   * - ``file.trashed_at``
     - Fecha y hora de traslado a la papelera
   * - ``file.purged_at``
     - Fecha y hora de eliminacion definitiva
   * - ``file.content_created_at``
     - Fecha y hora de creacion del contenido
   * - ``file.content_modified_at``
     - Fecha y hora de modificacion del contenido
   * - ``file.created_by``
     - Informacion del creador
   * - ``file.modified_by``
     - Informacion del modificador
   * - ``file.owned_by``
     - Informacion del propietario
   * - ``file.shared_link``
     - Informacion del enlace compartido
   * - ``file.parent``
     - Informacion de la carpeta padre
   * - ``file.item_status``
     - Estado del elemento
   * - ``file.version_number``
     - Numero de version
   * - ``file.comment_count``
     - Numero de comentarios
   * - ``file.permissions``
     - Informacion de permisos
   * - ``file.tags``
     - Informacion de etiquetas
   * - ``file.lock``
     - Informacion de bloqueo
   * - ``file.is_package``
     - Indicador de paquete
   * - ``file.is_watermark``
     - Indicador de marca de agua
   * - ``file.collections``
     - Informacion de colecciones
   * - ``file.representations``
     - Informacion de representaciones
   * - ``file.api``
     - Objeto BoxFileAPI (para obtener informacion de colaboracion y permisos)

Para mas detalles, consulte el `Objeto File de Box <https://developer.box.com/reference#file-object>`_.

Configuracion de autenticacion de Box
======================================

Pasos de configuracion de autenticacion JWT
--------------------------------------------

1. Crear una aplicacion en Box Developer Console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Acceda a https://app.box.com/developers/console:

1. Haga clic en "Create New App"
2. Seleccione "Custom App"
3. Seleccione "Server Authentication (with JWT)" como metodo de autenticacion
4. Ingrese el nombre de la aplicacion y cree

2. Configuracion de la aplicacion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure en la pestana "Configuration":

**Application Scopes**:

- Marque "Read all files and folders stored in Box"

**Advanced Features**:

- Haga clic en "Generate a Public/Private Keypair"
- Descargue el archivo JSON generado (importante!)

**App Access Level**:

- Seleccione "App + Enterprise Access"

3. Aprobar en la empresa
~~~~~~~~~~~~~~~~~~~~~~~~~

En la consola de administracion de Box:

1. Abra "Apps" -> "Custom Apps"
2. Apruebe la aplicacion creada

4. Obtener las credenciales de autenticacion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Obtenga la siguiente informacion del archivo JSON descargado:

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

Reemplace los saltos de linea de ``private_key`` con ``\n`` para convertirla en una sola linea:

::

    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgk...=\n-----END ENCRYPTED PRIVATE KEY-----\n

Ejemplos de uso
===============

Rastrear todo el almacenamiento Box de la empresa
--------------------------------------------------

Parametros:

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

Rastrear solo una carpeta especifica
-------------------------------------

Es posible filtrar por ruta de carpeta mediante el parametro ``include_pattern``.

Parametros:

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

Es posible filtrar por tipo MIME mediante el parametro ``supported_mimetypes``.

Parametros:

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

Solucion de problemas
=====================

Errores de autenticacion
------------------------

**Sintoma**: ``Authentication failed`` o ``Invalid grant``

**Verifique**:

1. Verifique que ``client_id`` y ``client_secret`` sean correctos
2. Verifique que la clave privada se haya copiado correctamente (los saltos de linea esten como ``\n``)
3. Verifique que la frase de contrasena sea correcta
4. Verifique que la aplicacion este aprobada en la consola de administracion de Box
5. Verifique que ``enterprise_id`` sea correcto

Error de formato de clave privada
----------------------------------

**Sintoma**: ``Invalid private key format``

**Solucion**:

Verifique que los saltos de linea de la clave privada esten correctamente convertidos a ``\n``:

::

    # Formato correcto
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDj...\n-----END ENCRYPTED PRIVATE KEY-----\n

    # Formato incorrecto (contiene saltos de linea reales)
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----
    MIIFDj...
    -----END ENCRYPTED PRIVATE KEY-----

No se pueden obtener archivos
------------------------------

**Sintoma**: El rastreo finaliza con exito pero hay 0 archivos

**Verifique**:

1. Verifique que "Read all files and folders" este habilitado en Application Scopes
2. Verifique que App Access Level sea "App + Enterprise Access"
3. Verifique que realmente existan archivos en el almacenamiento de Box
4. Verifique que la cuenta de servicio tenga los permisos apropiados

Cuando hay un gran numero de archivos
--------------------------------------

**Sintoma**: El rastreo tarda mucho tiempo o se agota el tiempo de espera

**Solucion**:

Divida el procesamiento en la configuracion del almacen de datos:

1. Ajuste el intervalo de rastreo
2. Configure multiples almacenes de datos (por unidad de carpeta, etc.)
3. Aumente el numero de hilos con el parametro ``number_of_threads``
4. Distribuya la carga con la configuracion de programacion

Permisos y control de acceso
=============================

Reflejar los permisos de colaboracion de Box
---------------------------------------------

Mediante el objeto ``BoxFileAPI`` proporcionado por el campo ``file.api``, es posible
asignar la informacion de colaboracion de Box a los roles de busqueda de |Fess|.
``file.api.collaborationRoles`` devuelve una lista de roles de busqueda correspondientes
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
   ``file.api.collaborationRoles`` obtiene la informacion de colaboracion de cada archivo,
   lo que incrementa el numero de llamadas a la API de Box y puede hacer que el rastreo
   tarde mas tiempo.

Para asignar un rol fijo a todos los archivos, especifiquelo de la siguiente manera:

::

    role="{role}box-users"

Informacion de referencia
==========================

- :doc:`ds-overview` - Descripcion general de conectores de almacen de datos
- :doc:`ds-dropbox` - Conector de Dropbox
- :doc:`ds-gsuite` - Conector de Google Workspace
- :doc:`../../admin/dataconfig-guide` - Guia de configuracion de almacen de datos
- `Documentacion para desarrolladores de Box <https://developer.box.com/>`_
- `Autenticacion de Box Platform <https://developer.box.com/guides/authentication/>`_
