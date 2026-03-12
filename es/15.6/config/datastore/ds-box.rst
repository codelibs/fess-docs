==================================
Conector de Box
==================================

Descripcion General
===================

El conector de Box proporciona funcionalidad para obtener archivos del almacenamiento
en la nube Box.com y registrarlos en el indice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-box``.

Requisitos Previos
==================

1. Se requiere instalacion del plugin
2. Se requiere una cuenta de desarrollador de Box y la creacion de una aplicacion
3. Se requiere configuracion de autenticacion JWT (JSON Web Token) u OAuth 2.0

Instalacion del Plugin
----------------------

Metodo 1: Colocar archivo JAR directamente

::

    # Descargar de Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-box/X.X.X/fess-ds-box-X.X.X.jar

    # Colocar
    cp fess-ds-box-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # o
    cp fess-ds-box-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Metodo 2: Instalar desde la consola de administracion

1. Abra "Sistema" -> "Plugins"
2. Cargue el archivo JAR
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
     - Company Box Storage
   * - Nombre del Manejador
     - BoxDataStore
   * - Habilitado
     - Activado

Configuracion de Parametros
---------------------------

Ejemplo de autenticacion JWT (recomendado):

::

    client_id=hdf8a7sd9f8a7sdf9a87sdf98a7sd
    client_secret=kMN7sd8f7a9sd8f7a9sd8f7a9sd8f
    public_key_id=4tg5h6j7
    private_key=<YOUR_PRIVATE_KEY>
    passphrase=7ba8sd9f7a9sd8f7a9sd8f7a9sd8f
    enterprise_id=1923456

Lista de Parametros
~~~~~~~~~~~~~~~~~~~

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
     - Clave privada (formato PEM, saltos de linea como ``\\n``)
   * - ``passphrase``
     - Si
     - Frase de contrasena de la clave privada
   * - ``enterprise_id``
     - Si
     - ID de empresa de Box

Configuracion de Script
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

Campos Disponibles
~~~~~~~~~~~~~~~~~~

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
     - Fecha de creacion
   * - ``file.modified_at``
     - Fecha de ultima modificacion

Para mas detalles, consulte el `Objeto File de Box <https://developer.box.com/reference#file-object>`_.

Configuracion de Autenticacion de Box
=====================================

Pasos de Configuracion de Autenticacion JWT
-------------------------------------------

1. Crear una aplicacion en Box Developer Console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Acceda a https://app.box.com/developers/console:

1. Haga clic en "Create New App"
2. Seleccione "Custom App"
3. Seleccione "Server Authentication (with JWT)" como metodo de autenticacion
4. Ingrese el nombre de la aplicacion y cree

2. Configuracion de la Aplicacion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure en la pestana "Configuration":

**Application Scopes**:

- Marque "Read all files and folders stored in Box"

**Advanced Features**:

- Haga clic en "Generate a Public/Private Keypair"
- Descargue el archivo JSON generado (importante!)

**App Access Level**:

- Seleccione "App + Enterprise Access"

3. Aprobar en la Empresa
~~~~~~~~~~~~~~~~~~~~~~~~

En la consola de administracion de Box:

1. Abra "Apps" -> "Custom Apps"
2. Apruebe la aplicacion creada

4. Obtener Credenciales de Autenticacion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Formato de Clave Privada
~~~~~~~~~~~~~~~~~~~~~~~~

Reemplace los saltos de linea de ``private_key`` con ``\\n`` para hacerla una sola linea:

::

    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\\nMIIFDjBABgk...=\\n-----END ENCRYPTED PRIVATE KEY-----\\n


Ejemplos de Uso
===============

Rastrear Todo el Almacenamiento Box de la Empresa
-------------------------------------------------

Parametros:

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\\n-----END ENCRYPTED PRIVATE KEY-----\\n
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

Rastrear Solo Archivos PDF
--------------------------

Filtrado por tipo MIME en el script:

::

    if (file.mimetype == "application/pdf") {
        url=file.url
        title=file.name
        content=file.contents
        mimetype=file.mimetype
        filename=file.name
        created=file.created_at
        last_modified=file.modified_at
    }

Solucion de Problemas
=====================

Errores de Autenticacion
------------------------

**Sintoma**: ``Authentication failed`` o ``Invalid grant``

**Verifique**:

1. Verifique que ``client_id`` y ``client_secret`` sean correctos
2. Verifique que la clave privada se haya copiado correctamente (saltos de linea como ``\\n``)
3. Verifique que la frase de contrasena sea correcta
4. Verifique que la aplicacion este aprobada en la consola de administracion de Box
5. Verifique que ``enterprise_id`` sea correcto

Error de Formato de Clave Privada
---------------------------------

**Sintoma**: ``Invalid private key format``

**Solucion**:

Verifique que los saltos de linea de la clave privada esten convertidos correctamente a ``\\n``:

::

    # Formato correcto
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\\nMIIFDj...\\n-----END ENCRYPTED PRIVATE KEY-----\\n

    # Formato incorrecto (contiene saltos de linea reales)
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----
    MIIFDj...
    -----END ENCRYPTED PRIVATE KEY-----

No Se Pueden Obtener Archivos
-----------------------------

**Sintoma**: El rastreo tiene exito pero hay 0 archivos

**Verifique**:

1. Verifique que "Read all files and folders" este habilitado en Application Scopes
2. Verifique que App Access Level sea "App + Enterprise Access"
3. Verifique que realmente existan archivos en el almacenamiento de Box
4. Verifique que la cuenta de servicio tenga los permisos apropiados

Cuando Hay un Gran Numero de Archivos
-------------------------------------

**Sintoma**: El rastreo toma mucho tiempo o se agota el tiempo

**Solucion**:

Divida el procesamiento en la configuracion del almacen de datos:

1. Ajuste el intervalo de rastreo
2. Configure multiples almacenes de datos (por unidad de carpeta, etc.)
3. Distribuya la carga con configuracion de programacion

Permisos y Control de Acceso
============================

Reflejar Permisos de Archivos de Box
------------------------------------

.. note::
   La implementacion actual no obtiene informacion detallada de permisos de Box.
   Puede configurar el control de acceso usando el campo ``role`` segun sea necesario.

Configurar permisos predeterminados:

::

    # Parametros
    default_permissions={role}box-users

Configurar permisos en el script:

::

    url=file.url
    title=file.name
    content=file.contents
    role=["box-users"]
    mimetype=file.mimetype
    filename=file.name
    created=file.created_at
    last_modified=file.modified_at

Informacion de Referencia
=========================

- :doc:`ds-overview` - Descripcion General de Conectores de Almacen de Datos
- :doc:`ds-dropbox` - Conector de Dropbox
- :doc:`ds-gsuite` - Conector de Google Workspace
- :doc:`../../admin/dataconfig-guide` - Guia de Configuracion de Almacen de Datos
- `Documentacion para Desarrolladores de Box <https://developer.box.com/>`_
- `Autenticacion de Box Platform <https://developer.box.com/guides/authentication/>`_
