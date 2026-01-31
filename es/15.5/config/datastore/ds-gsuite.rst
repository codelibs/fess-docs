==================================
Conector de Google Workspace
==================================

Vision General
==============

El conector de Google Workspace proporciona funcionalidad para obtener archivos de Google Drive
(anteriormente G Suite) y registrarlos en el indice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-gsuite``.

Servicios Soportados
====================

- Google Drive (Mi unidad, Unidades compartidas)
- Documentos de Google, Hojas de calculo, Presentaciones, Formularios, etc.

Requisitos Previos
==================

1. Se requiere la instalacion del plugin
2. Se requiere la creacion de un proyecto en Google Cloud Platform
3. Se requiere la creacion de una cuenta de servicio y la obtencion de credenciales
4. Se requiere la configuracion de delegacion de dominio de Google Workspace

Instalacion del Plugin
----------------------

Metodo 1: Colocar el archivo JAR directamente

::

    # Descargar desde Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-gsuite/X.X.X/fess-ds-gsuite-X.X.X.jar

    # Colocar
    cp fess-ds-gsuite-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # o
    cp fess-ds-gsuite-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Metodo 2: Instalar desde la pantalla de administracion

1. Abra "Sistema" -> "Plugins"
2. Cargue el archivo JAR
3. Reinicie |Fess|

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
     - Company Google Drive
   * - Nombre del manejador
     - GSuiteDataStore
   * - Habilitado
     - Activado

Configuracion de Parametros
---------------------------

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com

Lista de Parametros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametro
     - Requerido
     - Descripcion
   * - ``private_key``
     - Si
     - Clave privada de la cuenta de servicio (formato PEM, saltos de linea como ``\n``)
   * - ``private_key_id``
     - Si
     - ID de la clave privada
   * - ``client_email``
     - Si
     - Direccion de correo de la cuenta de servicio

Configuracion de Script
-----------------------

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.url
    thumbnail=file.thumbnail_link
    content_length=file.size
    filetype=file.filetype
    role=file.roles
    filename=file.name

Campos Disponibles
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripcion
   * - ``file.name``
     - Nombre del archivo
   * - ``file.description``
     - Descripcion del archivo
   * - ``file.contents``
     - Contenido de texto del archivo
   * - ``file.mimetype``
     - Tipo MIME del archivo
   * - ``file.filetype``
     - Tipo de archivo
   * - ``file.created_time``
     - Fecha de creacion
   * - ``file.modified_time``
     - Ultima fecha de modificacion
   * - ``file.web_view_link``
     - Enlace para abrir en el navegador
   * - ``file.url``
     - URL del archivo
   * - ``file.thumbnail_link``
     - Enlace de miniatura (valido por tiempo limitado)
   * - ``file.size``
     - Tamano del archivo (bytes)
   * - ``file.roles``
     - Permisos de acceso

Para mas detalles, consulte `Google Drive Files API <https://developers.google.com/drive/api/v3/reference/files>`_.

Configuracion de Google Cloud Platform
======================================

1. Crear Proyecto
-----------------

Acceda a https://console.cloud.google.com/:

1. Cree un nuevo proyecto
2. Ingrese el nombre del proyecto
3. Seleccione la organizacion y la ubicacion

2. Habilitar Google Drive API
-----------------------------

En "APIs y servicios" -> "Biblioteca":

1. Busque "Google Drive API"
2. Haga clic en "Habilitar"

3. Crear Cuenta de Servicio
---------------------------

En "APIs y servicios" -> "Credenciales":

1. Seleccione "Crear credenciales" -> "Cuenta de servicio"
2. Ingrese el nombre de la cuenta de servicio (ej: fess-crawler)
3. Haga clic en "Crear y continuar"
4. El rol no es necesario (omitir)
5. Haga clic en "Listo"

4. Crear Clave de Cuenta de Servicio
------------------------------------

En la cuenta de servicio creada:

1. Haga clic en la cuenta de servicio
2. Abra la pestana "Claves"
3. "Agregar clave" -> "Crear nueva clave"
4. Seleccione el formato JSON
5. Guarde el archivo JSON descargado

5. Habilitar Delegacion de Dominio
----------------------------------

En la configuracion de la cuenta de servicio:

1. Marque "Habilitar delegacion de dominio"
2. Haga clic en "Guardar"
3. Copie el "ID de cliente OAuth 2"

6. Autorizar en la Consola de Administracion de Google Workspace
----------------------------------------------------------------

Acceda a https://admin.google.com/:

1. Abra "Seguridad" -> "Acceso y control de datos" -> "Controles de API"
2. Seleccione "Delegacion de dominio"
3. Haga clic en "Agregar nuevo"
4. Ingrese el ID de cliente
5. Ingrese los ambitos OAuth:

   ::

       https://www.googleapis.com/auth/drive.readonly

6. Haga clic en "Autorizar"

Configuracion de Credenciales
=============================

Obtener Informacion del Archivo JSON
------------------------------------

Archivo JSON descargado:

::

    {
      "type": "service_account",
      "project_id": "your-project-id",
      "private_key_id": "46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgk...\n-----END PRIVATE KEY-----\n",
      "client_email": "fess-crawler@your-project.iam.gserviceaccount.com",
      "client_id": "123456789012345678901",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
    }

Configure la siguiente informacion en los parametros:

- ``private_key_id`` -> ``private_key_id``
- ``private_key`` -> ``private_key`` (los saltos de linea permanecen como ``\n``)
- ``client_email`` -> ``client_email``

Formato de Clave Privada
~~~~~~~~~~~~~~~~~~~~~~~~

``private_key`` mantiene los saltos de linea como ``\n``:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG...\n-----END PRIVATE KEY-----\n

Solucion de Problemas
=====================

Error de Autenticacion
----------------------

**Sintoma**: ``401 Unauthorized`` o ``403 Forbidden``

**Verificar**:

1. Verificar que las credenciales de la cuenta de servicio sean correctas:

   - Los saltos de linea de ``private_key`` estan como ``\n``
   - ``private_key_id`` es correcto
   - ``client_email`` es correcto

2. Verificar que Google Drive API este habilitada
3. Verificar que la delegacion de dominio este configurada
4. Verificar que este autorizado en la consola de administracion de Google Workspace
5. Verificar que el ambito OAuth sea correcto (``https://www.googleapis.com/auth/drive.readonly``)

Error de Delegacion de Dominio
------------------------------

**Sintoma**: ``Not Authorized to access this resource/api``

**Solucion**:

1. Verificar la autorizacion en la consola de administracion de Google Workspace:

   - El ID de cliente esta registrado correctamente
   - El ambito OAuth es correcto (``https://www.googleapis.com/auth/drive.readonly``)

2. Verificar que la delegacion de dominio este habilitada en la cuenta de servicio

No se Pueden Obtener Archivos
-----------------------------

**Sintoma**: El rastreo tiene exito pero hay 0 archivos

**Verificar**:

1. Verificar que existan archivos en Google Drive
2. Verificar que la cuenta de servicio tenga permisos de lectura
3. Verificar que la delegacion de dominio este configurada correctamente
4. Verificar que se pueda acceder al Drive del usuario objetivo

Informacion de Referencia
=========================

- :doc:`ds-overview` - Vision general de conectores de almacen de datos
- :doc:`ds-microsoft365` - Conector de Microsoft 365
- :doc:`ds-box` - Conector de Box
- :doc:`../../admin/dataconfig-guide` - Guia de configuracion de almacen de datos
- `Google Drive API <https://developers.google.com/drive/api>`_
- `Google Cloud Platform <https://console.cloud.google.com/>`_
- `Google Workspace Admin <https://admin.google.com/>`_
