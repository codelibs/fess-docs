==================================
Conector de Google Workspace
==================================

Visión General
==============

El conector de Google Workspace proporciona funcionalidad para obtener archivos de Google Drive
(anteriormente G Suite) y registrarlos en el índice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-gsuite``.

Servicios Soportados
====================

- Google Drive (Mi unidad, Unidades compartidas)
- Documentos de Google, Hojas de cálculo, Presentaciones, Formularios, etc.

Requisitos Previos
==================

1. Se requiere la instalación del plugin
2. Se requiere la creación de un proyecto en Google Cloud Platform
3. Se requiere la creación de una cuenta de servicio y la obtención de credenciales
4. Se requiere la configuración de delegación de dominio de Google Workspace

Instalación del Plugin
----------------------

Método 1: Colocar el archivo JAR directamente

::

    # Descargar desde Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-gsuite/X.X.X/fess-ds-gsuite-X.X.X.jar

    # Colocar
    cp fess-ds-gsuite-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # o
    cp fess-ds-gsuite-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Método 2: Instalar desde la pantalla de administración

1. Abra "Sistema" -> "Plugins"
2. Cargue el archivo JAR
3. Reinicie |Fess|

Método de Configuración
=======================

Configure desde la pantalla de administración en "Rastreador" -> "Almacén de datos" -> "Nuevo".

Configuración Básica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Elemento
     - Ejemplo
   * - Nombre
     - Company Google Drive
   * - Nombre del manejador
     - GoogleDriveDataStore
   * - Habilitado
     - Activado

Configuración de Parámetros
---------------------------

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com

Lista de Parámetros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parámetro
     - Requerido
     - Descripción
   * - ``private_key``
     - Sí
     - Clave privada de la cuenta de servicio (formato PEM, saltos de línea como ``\n``)
   * - ``private_key_id``
     - Sí
     - ID de la clave privada
   * - ``client_email``
     - Sí
     - Dirección de correo de la cuenta de servicio
   * - ``max_size``
     - No
     - Tamaño máximo de archivo a indexar (en bytes). Predeterminado: ``10000000`` (aprox. 10MB)
   * - ``ignore_folder``
     - No
     - Si se deben omitir las carpetas. Predeterminado: ``true``
   * - ``ignore_error``
     - No
     - Si se debe continuar el procesamiento cuando ocurre un error. Predeterminado: ``true``
   * - ``supported_mimetypes``
     - No
     - Tipos MIME a indexar (expresión regular, separados por comas). Predeterminado: ``.*`` (todos los tipos)
   * - ``include_pattern``
     - No
     - Patrón de expresión regular para las URL que se incluyen en el índice
   * - ``exclude_pattern``
     - No
     - Patrón de expresión regular para las URL que se excluyen
   * - ``default_permissions``
     - No
     - Permisos predeterminados (separados por comas, p. ej. ``{role}drive-users``)
   * - ``number_of_threads``
     - No
     - Número de hilos de procesamiento en paralelo. Predeterminado: ``1``
   * - ``query``
     - No
     - Cadena de consulta de búsqueda de la API de Google Drive
   * - ``corpora``
     - No
     - Corpora a buscar. Predeterminado: ``allDrives``
   * - ``spaces``
     - No
     - Espacios a buscar (parámetro ``spaces`` de la API de Google Drive, p. ej. ``drive``, ``appDataFolder``). Predeterminado: sin especificar (valor predeterminado de la API).
   * - ``fields``
     - No
     - Campos de archivo que se solicitan a la API de Google Drive. Predeterminado: ``*`` (todos los campos).
   * - ``read_timeout``
     - No
     - Tiempo de espera de lectura HTTP (en milisegundos). Predeterminado: ``20000``
   * - ``connect_timeout``
     - No
     - Tiempo de espera de conexión HTTP (en milisegundos). Predeterminado: ``20000``
   * - ``refresh_token_interval``
     - No
     - Intervalo (en segundos) para renovar el token de acceso OAuth. Predeterminado: ``3540`` (59 minutos).
   * - ``max_cached_content_size``
     - No
     - Tamaño máximo (en bytes) del contenido mantenido en memoria; el contenido mayor se vuelca a un archivo temporal. Predeterminado: ``1048576`` (1MB).
   * - ``proxy_host``
     - No
     - Nombre de host del servidor proxy
   * - ``proxy_port``
     - No
     - Número de puerto del servidor proxy

Configuración de Script
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
     - Descripción
   * - ``file.name``
     - Nombre del archivo
   * - ``file.description``
     - Descripción del archivo
   * - ``file.contents``
     - Contenido de texto del archivo
   * - ``file.mimetype``
     - Tipo MIME del archivo
   * - ``file.filetype``
     - Tipo de archivo
   * - ``file.created_time``
     - Fecha de creación
   * - ``file.modified_time``
     - Última fecha de modificación
   * - ``file.web_view_link``
     - Enlace para abrir en el navegador
   * - ``file.url``
     - URL del archivo
   * - ``file.thumbnail_link``
     - Enlace de miniatura (válido por tiempo limitado)
   * - ``file.size``
     - Tamaño del archivo (bytes)
   * - ``file.roles``
     - Permisos de acceso

Para más detalles, consulte `Google Drive Files API <https://developers.google.com/drive/api/v3/reference/files>`_.

Configuración de Google Cloud Platform
======================================

1. Crear Proyecto
-----------------

Acceda a https://console.cloud.google.com/:

1. Cree un nuevo proyecto
2. Ingrese el nombre del proyecto
3. Seleccione la organización y la ubicación

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
2. Abra la pestaña "Claves"
3. "Agregar clave" -> "Crear nueva clave"
4. Seleccione el formato JSON
5. Guarde el archivo JSON descargado

5. Habilitar Delegación de Dominio
----------------------------------

En la configuración de la cuenta de servicio:

1. Marque "Habilitar delegación de dominio"
2. Haga clic en "Guardar"
3. Copie el "ID de cliente OAuth 2"

6. Autorizar en la Consola de Administración de Google Workspace
----------------------------------------------------------------

Acceda a https://admin.google.com/:

1. Abra "Seguridad" -> "Acceso y control de datos" -> "Controles de API"
2. Seleccione "Delegación de dominio"
3. Haga clic en "Agregar nuevo"
4. Ingrese el ID de cliente
5. Ingrese los ámbitos OAuth:

   ::

       https://www.googleapis.com/auth/drive

6. Haga clic en "Autorizar"

Configuración de Credenciales
=============================

Obtener Información del Archivo JSON
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

Configure la siguiente información en los parámetros:

- ``private_key_id`` -> ``private_key_id``
- ``private_key`` -> ``private_key`` (los saltos de línea permanecen como ``\n``)
- ``client_email`` -> ``client_email``

Formato de Clave Privada
~~~~~~~~~~~~~~~~~~~~~~~~

``private_key`` mantiene los saltos de línea como ``\n``:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG...\n-----END PRIVATE KEY-----\n

Solución de Problemas
=====================

Error de Autenticación
----------------------

**Síntoma**: ``401 Unauthorized`` o ``403 Forbidden``

**Verificar**:

1. Verificar que las credenciales de la cuenta de servicio sean correctas:

   - Los saltos de línea de ``private_key`` están como ``\n``
   - ``private_key_id`` es correcto
   - ``client_email`` es correcto

2. Verificar que Google Drive API esté habilitada
3. Verificar que la delegación de dominio esté configurada
4. Verificar que esté autorizado en la consola de administración de Google Workspace
5. Verificar que el ámbito OAuth sea correcto (``https://www.googleapis.com/auth/drive``)

Error de Delegación de Dominio
------------------------------

**Síntoma**: ``Not Authorized to access this resource/api``

**Solución**:

1. Verificar la autorización en la consola de administración de Google Workspace:

   - El ID de cliente está registrado correctamente
   - El ámbito OAuth es correcto (``https://www.googleapis.com/auth/drive``)

2. Verificar que la delegación de dominio esté habilitada en la cuenta de servicio

No se Pueden Obtener Archivos
-----------------------------

**Síntoma**: El rastreo tiene éxito pero hay 0 archivos

**Verificar**:

1. Verificar que existan archivos en Google Drive
2. Verificar que la cuenta de servicio tenga permisos de lectura
3. Verificar que la delegación de dominio esté configurada correctamente
4. Verificar que se pueda acceder al Drive del usuario objetivo

Información de Referencia
=========================

- :doc:`ds-overview` - Visión general de conectores de almacén de datos
- :doc:`ds-microsoft365` - Conector de Microsoft 365
- :doc:`ds-box` - Conector de Box
- :doc:`../../admin/dataconfig-guide` - Guía de configuración de almacén de datos
- `Google Drive API <https://developers.google.com/drive/api>`_
- `Google Cloud Platform <https://console.cloud.google.com/>`_
- `Google Workspace Admin <https://admin.google.com/>`_
