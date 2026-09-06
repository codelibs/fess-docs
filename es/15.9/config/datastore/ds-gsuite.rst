==================================
Conector de Google Workspace
==================================

Visión General
==============

El conector de Google Workspace proporciona funcionalidad para obtener archivos de Google Drive
(anteriormente G Suite) y registrarlos en el índice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-gsuite``.

Cambios en la Versión 15.9
==========================

El conector se ha rediseñado en profundidad en |Fess| 15.9. Lea esta sección antes de
actualizar una configuración de almacén de datos existente.

.. warning::

   ``crawl_target`` ahora tiene el valor predeterminado ``shared_drives``, y cualquier valor
   distinto de ``legacy`` requiere ``impersonate_user``. Por tanto, una configuración
   existente que se actualice sin cambios **falla al iniciarse** con una
   ``DataStoreException`` en lugar de ejecutarse.

   Esto es deliberado: el comportamiento anterior solo alcanzaba los archivos compartidos
   explícitamente con la cuenta de servicio, de modo que la alternativa sería un rastreo que
   no indexa nada de forma silenciosa. Establezca ``impersonate_user`` en una cuenta de
   administrador del dominio, o establezca ``crawl_target=legacy`` para mantener el
   comportamiento anterior.

Cambios de Comportamiento
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Cambio
     - Acción necesaria
   * - ``crawl_target`` tiene el valor predeterminado ``shared_drives`` y requiere ``impersonate_user``
     - Establezca ``impersonate_user`` o ``crawl_target=legacy``. De lo contrario, el rastreo falla al iniciarse.
   * - El ámbito OAuth predeterminado se ha reducido de ``https://www.googleapis.com/auth/drive`` a ``https://www.googleapis.com/auth/drive.readonly``
     - Actualice la entrada de delegación de dominio en la consola de administración de Google Workspace, que enumera los ámbitos de forma explícita.
   * - ``crawl_target=users`` y ``crawl_target=both`` requieren además ``https://www.googleapis.com/auth/admin.directory.user.readonly``
     - Añada el ámbito tanto al parámetro ``scopes`` como a la entrada de delegación. Esto se valida al iniciarse.
   * - La URL indexada es ahora ``webViewLink`` (el enlace que se abre en el navegador) en lugar del enlace de descarga
     - Realice un rastreo completo para adoptar las nuevas URL.
   * - ``default_permissions`` es ahora un valor de reserva, no un añadido
     - Un documento cuya ACL puede resolverse recibe únicamente esa ACL, ya no la unión con ``default_permissions``. El resultado es estrictamente más restrictivo.
   * - Compartir solo mediante enlace ya no concede un rol de búsqueda
     - Un permiso ``domain`` o ``anyone`` con ``allowFileDiscovery=false`` significa "cualquier persona con el enlace", algo que Drive tampoco hace localizable mediante la búsqueda.
   * - Un documento cuya ACL no resuelve nada se omite en lugar de indexarse sin roles
     - Establezca ``default_permissions`` para seguir indexando esos documentos. Antes eran visibles para todos los usuarios, porque una lista de roles vacía desactiva el filtro de permisos.
   * - ``fields`` ya no tiene el valor predeterminado ``*``, sino una lista de campos explícita
     - Un script de rastreo que haga referencia a un campo poco habitual leerá ahora null. Establezca ``fields=*`` para restaurar la proyección anterior.
   * - Los Documentos de Google se exportan como Markdown en lugar de texto plano, y las Hojas de cálculo como TSV en lugar de CSV
     - El texto indexado de cada Documento de Google contiene ahora caracteres de sintaxis Markdown. Realice un rastreo completo.
   * - ``refresh_token_interval`` se ignora
     - La renovación de los tokens la realiza la biblioteca de autenticación. Una configuración existente sigue funcionando y se registra una advertencia.
   * - Los Formularios de Google y Google Sites se indexan solo con sus metadatos
     - No tienen formato de exportación en la API de Drive. Antes, cada uno de ellos producía un error de rastreo.

Nuevas Funcionalidades
----------------------

- ``crawl_target`` selecciona qué se rastrea: la vista propia de la cuenta de servicio
  (``legacy``), todas las unidades compartidas del dominio (``shared_drives``), Mi unidad
  de cada usuario del directorio (``users``) o ambas (``both``). Consulte
  `Objetivo de Rastreo`_.
- Los elementos de las unidades compartidas obtienen ahora la ACL correcta.
- Rastreo incremental mediante el feed de cambios de Drive. Consulte
  `Rastreo Incremental`_.
- Límite de velocidad con retroceso exponencial que respeta ``Retry-After``, y una unidad
  compartida o un usuario con errores que ya no interrumpen todo el rastreo. Consulte
  `Límite de Velocidad y Reintentos`_.
- ``proxy_username`` y ``proxy_password`` para un proxy con autenticación.

Servicios Soportados
====================

- Google Drive (Mi unidad, Unidades compartidas)
- Documentos de Google, Hojas de cálculo, Presentaciones, Dibujos, Apps Script
- Formularios de Google y Google Sites (solo metadatos; no tienen formato de exportación)

Requisitos Previos
==================

1. Se requiere la instalación del plugin
2. Se requiere la creación de un proyecto en Google Cloud Platform
3. Se requiere la creación de una cuenta de servicio y la obtención de credenciales
4. Se requiere la configuración de delegación de dominio de Google Workspace
5. Salvo que se use ``crawl_target=legacy``, se requiere una cuenta de administrador de
   Google Workspace cuya identidad se suplantará

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
    impersonate_user=admin@example.com

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
   * - ``impersonate_user``
     - Condicional
     - La cuenta de Google Workspace cuya identidad se suplanta mediante la delegación de dominio. Requerido salvo que se use ``crawl_target=legacy``; sin él, el rastreo falla al iniciarse. ``shared_drives`` y ``both`` enumeran las unidades compartidas con acceso de administrador del dominio, por lo que esta cuenta debe ser administradora del dominio.
   * - ``crawl_target``
     - No
     - Qué se rastrea: ``legacy``, ``shared_drives``, ``users`` o ``both``. Predeterminado: ``shared_drives``. Consulte `Objetivo de Rastreo`_.
   * - ``scopes``
     - No
     - Ámbitos OAuth, separados por comas. Predeterminado: ``https://www.googleapis.com/auth/drive.readonly``. ``crawl_target=users`` y ``crawl_target=both`` requieren además ``https://www.googleapis.com/auth/admin.directory.user.readonly``.
   * - ``user_query``
     - No
     - ``query`` del Admin SDK usada para acotar los usuarios que enumeran ``crawl_target=users`` y ``crawl_target=both``. Predeterminado: sin especificar (todos los usuarios del cliente).
   * - ``query``
     - No
     - Cadena de consulta de búsqueda de la API de Google Drive. No se aplica al feed de cambios que utiliza el rastreo incremental.
   * - ``corpora``
     - No
     - Corpora a buscar. Predeterminado: ``allDrives``. Solo lo consume ``crawl_target=legacy``, por lo que no tiene efecto con el objetivo predeterminado: ``shared_drives`` lista cada unidad con ``drive`` y ``users`` lista cada Mi unidad con ``user``, ambos fijos.
   * - ``spaces``
     - No
     - Espacios a buscar (parámetro ``spaces`` de la API de Google Drive, p. ej. ``drive``, ``appDataFolder``). Predeterminado: sin especificar (valor predeterminado de la API). Lo usan ``crawl_target=legacy`` y ``users``; se ignora en ``shared_drives``.
   * - ``fields``
     - No
     - Campos de archivo que se solicitan a la API de Google Drive. El valor predeterminado **no** es ``*``, sino una lista de campos explícita. Cubre todos los campos que necesitan el contexto del script, la resolución de la ACL, la URL del índice y el rastreo incremental; un campo que no figure en ella se lee como null en el script de rastreo. Establezca ``fields=*`` para solicitar todos los campos, como en versiones anteriores.
   * - ``default_permissions``
     - No
     - Permisos utilizados cuando la ACL de Drive de un documento no resuelve nada (separados por comas, p. ej. ``{role}drive-users``). Es un valor de reserva, no un añadido: un documento cuya ACL puede resolverse recibe únicamente esa ACL.
   * - ``max_size``
     - No
     - Tamaño máximo de archivo a indexar (en bytes). Predeterminado: ``10000000`` (aprox. 10MB)
   * - ``number_of_threads``
     - No
     - Número de hilos de procesamiento en paralelo. Predeterminado: ``1``
   * - ``incremental``
     - No
     - Si se rastrea mediante el feed de cambios de Drive en lugar de listarlo todo. Predeterminado: ``false``. Se lee directamente del campo de parámetros de la configuración del almacén de datos, antes de que comience el rastreo. Consulte `Rastreo Incremental`_.

Parámetros Avanzados
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parámetro
     - Descripción
   * - ``domain_permission_format``
     - Formato de rol aplicado a un permiso de Drive de tipo ``domain``. ``{domain}`` se sustituye por el nombre del dominio. Predeterminado: ``{group}{domain}``
   * - ``thread_pool_timeout_seconds``
     - Cuánto se espera a que terminen los hilos de trabajo al finalizar un rastreo (segundos). Predeterminado: ``60``
   * - ``page_size``
     - Tamaño de página para ``files.list`` y ``changes.list``. Predeterminado: ``1000``; los valores superiores a ``1000`` se recortan a ese límite.
   * - ``permission_page_size``
     - Tamaño de página para ``permissions.list`` y ``drives.list``. Predeterminado: ``100``; los valores superiores a ``100`` se recortan a ese límite.
   * - ``max_cached_content_size``
     - Tamaño máximo (en bytes) del contenido mantenido en memoria; el contenido mayor se vuelca a un archivo temporal. Predeterminado: ``1048576`` (1MB).
   * - ``max_retries``
     - Número máximo de reintentos para una llamada a la API de Drive limitada o fallida de forma transitoria. Predeterminado: ``5``
   * - ``retry_initial_interval_ms``
     - Intervalo de retroceso inicial antes del primer reintento (milisegundos). Predeterminado: ``1000``
   * - ``max_backoff_ms``
     - Límite superior de una espera individual (milisegundos). Predeterminado: ``32000``
   * - ``read_timeout``
     - Tiempo de espera de lectura HTTP (en milisegundos). Predeterminado: ``20000``
   * - ``connect_timeout``
     - Tiempo de espera de conexión HTTP (en milisegundos). Predeterminado: ``20000``
   * - ``proxy_host``
     - Nombre de host del servidor proxy. El proxy solo se usa cuando ``proxy_host`` y ``proxy_port`` están ambos definidos; uno solo no tiene efecto.
   * - ``proxy_port``
     - Número de puerto del servidor proxy. Consulte ``proxy_host``.
   * - ``proxy_username``
     - Nombre de usuario para un proxy con autenticación. Si se define, se añade una cabecera ``Proxy-Authorization`` a cada petición. Consulte `Limitaciones`_ para saber qué autentica y qué no.
   * - ``proxy_password``
     - Contraseña para un proxy con autenticación
   * - ``ignore_folder``
     - Si se deben omitir las carpetas. Predeterminado: ``true``
   * - ``ignore_error``
     - Si se debe continuar el procesamiento cuando ocurre un error. Predeterminado: ``true``
   * - ``supported_mimetypes``
     - Tipos MIME a indexar (expresión regular, separados por comas). Predeterminado: ``.*`` (todos los tipos)
   * - ``include_pattern``
     - Patrón de expresión regular para las URL que se incluyen en el índice
   * - ``exclude_pattern``
     - Patrón de expresión regular para las URL que se excluyen
   * - ``refresh_token_interval``
     - Se ignora desde la versión 15.9. Los tokens de acceso los renueva la biblioteca de autenticación. Un valor existente sigue funcionando y se registra una advertencia.

.. note::

   ``private_key``, ``private_key_id``, ``client_email``, ``proxy_username`` y
   ``proxy_password`` se eliminan del contexto de evaluación del script, de modo que un
   script de rastreo no puede indexarlos y ningún resultado de búsqueda puede revelarlos.

.. note::

   Cuando el rastreo incremental está habilitado, el conector reescribe
   ``start_page_tokens`` y ``crawl_signature`` en el campo de parámetros de la
   configuración del almacén de datos. Son valores gestionados por el conector y aparecen
   junto a los parámetros que usted define; no los modifique. Editarlos o eliminarlos hace
   que la siguiente ejecución rastree por completo cada ámbito.

Objetivo de Rastreo
-------------------

Una cuenta de servicio no tiene un Drive propio ni pertenece a ningún grupo de Google, por
lo que un rastreo que se autentica como la propia cuenta de servicio solo alcanza los
archivos compartidos explícitamente con su dirección. Por eso ``crawl_target`` selecciona
qué vista de Drive se rastrea.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Valor
     - Descripción
   * - ``legacy``
     - La vista propia de la cuenta de servicio, como en versiones anteriores. ``impersonate_user`` no es necesario. Solo se encuentran los archivos compartidos explícitamente con la cuenta de servicio.
   * - ``shared_drives``
     - Predeterminado. Se enumeran todas las unidades compartidas del dominio y cada una se recorre por separado.
   * - ``users``
     - Se enumeran todos los usuarios del directorio mediante el Admin SDK y se recorre Mi unidad de cada uno suplantando su identidad.
   * - ``both``
     - ``shared_drives`` seguido de ``users``. Un archivo presente en varios ámbitos se indexa una sola vez.

Lo siguiente se valida al iniciarse el rastreo, y una combinación no válida lanza una
``DataStoreException`` en lugar de ejecutarse:

1. ``crawl_target`` debe ser ``legacy``, ``shared_drives``, ``users`` o ``both``.
2. ``impersonate_user`` debe estar definido salvo que se use ``crawl_target=legacy``.
3. ``scopes`` debe contener ``https://www.googleapis.com/auth/admin.directory.user.readonly``
   cuando ``crawl_target`` es ``users`` o ``both``.

.. note::

   ``shared_drives`` y ``both`` enumeran las unidades compartidas con acceso de
   administrador del dominio, por lo que la cuenta indicada en ``impersonate_user`` debe ser
   administradora del dominio de Google Workspace. Esta enumeración determina todo el
   alcance del rastreo, de modo que un fallo permanente interrumpe el rastreo en lugar de
   registrarse y omitirse: un rastreo que no ha podido enumerar ninguna unidad no ha tenido
   un éxito parcial y no debe poder informar de éxito mientras no indexa nada.

Rastreo Incremental
-------------------

Establecer ``incremental=true`` hace que cada ámbito -- una unidad compartida, o la vista de
un usuario cuya identidad se suplanta -- lea el feed de cambios de Drive en lugar de
listarlo todo. Un ámbito sin token almacenado se lista por completo y su feed de cambios
queda anclado para la siguiente ejecución.

::

    crawl_target=shared_drives
    impersonate_user=admin@example.com
    incremental=true

.. warning::

   ``delete_old_docs`` se fuerza a ``false`` en toda ejecución incremental, y un
   ``delete_old_docs=true`` explícito se sobrescribe en lugar de respetarse (se registra una
   advertencia). La eliminación de documentos obsoletos borra todos los documentos de la
   configuración que el rastreo actual no ha tocado, lo que presupone un rastreo completo;
   una ejecución incremental solo toca los documentos que han cambiado, por lo que esa
   eliminación borraría el resto del índice.

   Para eliminar los documentos que han desaparecido de Drive, programe una configuración de
   almacén de datos aparte con ``incremental=false``.

Los tokens solo se guardan cuando el rastreo ha finalizado y los hilos de trabajo han
terminado. Un rastreo detenido deja los tokens intactos y la siguiente ejecución vuelve a
leer los mismos cambios.

Los tokens también se descartan, y cada ámbito se rastrea por completo, cuando cambia la
configuración que determina lo que produce un ámbito, es decir, cualquiera de
``crawl_target``, ``impersonate_user``, ``user_query``, ``query``, ``corpora`` o ``spaces``.
Un token almacenado solo describe el conjunto sobre el que se tomó, y reanudarlo tras un
cambio así dejaría un hueco permanente en el índice.

Límite de Velocidad y Reintentos
--------------------------------

Una llamada a la API de Drive limitada o fallida de forma transitoria se reintenta con un
retroceso exponencial, acotado por ``max_retries``, ``retry_initial_interval_ms`` y
``max_backoff_ms``. Una cabecera ``Retry-After`` prevalece sobre la espera exponencial, pero
queda limitada por ``max_backoff_ms`` para que una cabecera errónea no pueda detener el
rastreo durante horas. Solo se respeta la forma en segundos de ``Retry-After``; una fecha
HTTP recae en la espera exponencial.

``429``, ``500``, ``502``, ``503`` y ``504`` se reintentan siempre. Un ``403`` solo se
reintenta cuando se trata de un error de límite de velocidad; cualquier otro ``403`` es un
fallo de autorización que un reintento no puede resolver, y se informa de inmediato.

Un listado de archivos que no ha podido completarse ya no interrumpe todo el rastreo: las
unidades compartidas y los usuarios restantes se siguen rastreando, y el fallo queda
registrado en el log del rastreador y en la lista de URL fallidas de la pantalla de
administración.

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
     - URL del archivo. Es ``webViewLink``; cuando un archivo no lo tiene, se usa ``https://drive.google.com/open?id=<ID del archivo>``.
   * - ``file.thumbnail_link``
     - Enlace de miniatura (válido por tiempo limitado)
   * - ``file.size``
     - Tamaño del archivo (bytes)
   * - ``file.roles``
     - Permisos de acceso

.. note::

   Solo se rellenan los campos indicados en el parámetro ``fields``. Un campo que no se haya
   solicitado se lee como null en el script. Establezca ``fields=*`` para solicitar todos los
   campos, como en versiones anteriores.

Para más detalles, consulte `Google Drive Files API <https://developers.google.com/drive/api/v3/reference/files>`_.

Extracción de Texto de los Tipos Nativos de Google
--------------------------------------------------

Un tipo nativo de Google no puede descargarse y debe exportarse. El destino de exportación
se elige entre los formatos de exportación que la API de Drive comunica realmente, no a
partir de una tabla fija, y una exportación está limitada a 10MB.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Tipo
     - Exportado como
   * - Documentos de Google
     - Markdown (``text/markdown``); en su defecto, texto plano y después HTML
   * - Hojas de cálculo de Google
     - TSV (``text/tab-separated-values``); en su defecto, CSV
   * - Presentaciones de Google
     - Texto plano
   * - Dibujos de Google
     - PNG. No hay texto que indexar, por lo que solo se indexan los metadatos.
   * - Apps Script
     - El paquete JSON exportado, del que se indexan las fuentes de los scripts
   * - Formularios de Google, Google Sites
     - No exportables. Se indexan los metadatos y no se informa de ningún error.

.. note::

   Dado que los Documentos de Google se exportan ahora como Markdown, el texto indexado de
   cada Documento de Google contiene caracteres de sintaxis Markdown. Es necesario un
   rastreo completo para que el cambio alcance a los documentos ya indexados.

.. note::

   Los destinos de exportación se leen de la API de Drive una vez por rastreo. Si esa
   llamada falla, el conector recae en las conversiones que Drive siempre ha admitido --
   texto plano para los Documentos de Google y CSV para las Hojas de cálculo -- y registra
   una advertencia.

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
3. Habilite también "Admin SDK API" cuando ``crawl_target`` sea ``users`` o ``both``

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

       https://www.googleapis.com/auth/drive.readonly

   Cuando ``crawl_target`` sea ``users`` o ``both``, ingrese ambos ámbitos:

   ::

       https://www.googleapis.com/auth/drive.readonly,https://www.googleapis.com/auth/admin.directory.user.readonly

6. Haga clic en "Autorizar"

.. warning::

   La entrada de delegación enumera los ámbitos de forma explícita, por lo que actualizar
   desde una versión anterior obliga a modificarla. El ámbito predeterminado se redujo en
   15.9 de ``https://www.googleapis.com/auth/drive`` a
   ``https://www.googleapis.com/auth/drive.readonly``, y los ámbitos concedidos aquí deben
   coincidir con el parámetro ``scopes`` de la configuración del almacén de datos.

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

El Rastreo No Se Inicia
-----------------------

**Síntoma**: El rastreo termina de inmediato con una ``DataStoreException``

**Solución**:

1. ``parameter 'crawl_target' must be one of ...``: el valor de ``crawl_target`` no es
   ``legacy``, ``shared_drives``, ``users`` ni ``both``.
2. ``parameter 'impersonate_user' is required when 'crawl_target' is not 'legacy'``:
   establezca ``impersonate_user`` en una cuenta de administrador del dominio, o establezca
   ``crawl_target=legacy``.
3. ``parameter 'scopes' must include 'https://www.googleapis.com/auth/admin.directory.user.readonly'``:
   añada ese ámbito a ``scopes`` y a la entrada de delegación de dominio.

Este es el resultado esperado al actualizar una configuración existente sin cambios.
Consulte `Cambios en la Versión 15.9`_.

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
5. Verificar que el ámbito OAuth sea correcto
   (``https://www.googleapis.com/auth/drive.readonly``, más
   ``https://www.googleapis.com/auth/admin.directory.user.readonly`` para
   ``crawl_target=users`` o ``both``)

Error de Delegación de Dominio
------------------------------

**Síntoma**: ``Not Authorized to access this resource/api``

**Solución**:

1. Verificar la autorización en la consola de administración de Google Workspace:

   - El ID de cliente está registrado correctamente
   - Los ámbitos OAuth son correctos. La entrada de delegación los enumera de forma
     explícita, por lo que la reducción introducida en 15.9 obliga a actualizarla.

2. Verificar que la delegación de dominio esté habilitada en la cuenta de servicio
3. Verificar que la cuenta indicada en ``impersonate_user`` sea administradora del dominio
   cuando ``crawl_target`` sea ``shared_drives`` o ``both``

No se Pueden Obtener Archivos
-----------------------------

**Síntoma**: El rastreo tiene éxito pero hay 0 archivos

**Verificar**:

1. Verificar que ``crawl_target`` sea el que usted pretende. Con ``legacy`` solo se
   encuentran los archivos compartidos explícitamente con la cuenta de servicio, porque una
   cuenta de servicio no tiene un Drive propio ni pertenece a ningún grupo.
2. Verificar que existan archivos en Google Drive
3. Verificar que la cuenta de servicio tenga permisos de lectura
4. Verificar que la delegación de dominio esté configurada correctamente
5. Verificar que se pueda acceder al Drive del usuario objetivo

Documentos Omitidos
-------------------

**Síntoma**: ``Skipped ... because no permission could be resolved`` en el log del rastreador

**Solución**:

La ACL de Drive del documento no resolvió ningún rol de búsqueda, por lo que se omitió en
lugar de indexarse. Indexar un documento sin ningún rol desactiva el filtro de permisos de
|Fess| para ese documento y lo hace visible para todos los usuarios; por eso se omite. Un
documento omitido no es un fallo de rastreo, así que aparece solo en el log del rastreador y
no en la lista de URL fallidas.

1. Establezca ``default_permissions`` para indexar esos documentos con un permiso de reserva
2. Verifique que la cuenta indicada en ``impersonate_user`` sea administradora del dominio,
   para que puedan leerse las ACL de las unidades compartidas
3. Compruebe si el documento se comparte solo mediante enlace. Un permiso ``domain`` o
   ``anyone`` con ``allowFileDiscovery=false`` no concede ningún rol de búsqueda, porque
   Drive tampoco hace localizable ese documento mediante la búsqueda.

Limitaciones
============

- La señal de "eliminado" de Drive abarca tanto la pérdida de acceso como el borrado. Con
  ``crawl_target=users`` o ``both``, revocar el acceso de un usuario a un documento lo
  elimina del índice aunque otro usuario todavía pueda leerlo. Vuelve con el siguiente
  cambio de ese archivo, o en el siguiente rastreo completo.
- Cuando un ámbito recae en un rastreo completo durante una ejecución incremental, la
  eliminación de documentos obsoletos sigue desactivada, por lo que los documentos borrados
  de Drive mientras un ámbito no estaba anclado permanecen en el índice. El remedio es una
  configuración aparte con ``incremental=false``, cuyo rastreo completo los elimina.
- La propagación de un borrado presupone que la URL indexada contiene el ID del archivo de
  Drive, lo cual se cumple para ``webViewLink`` y para la URL de reserva. Un script de
  rastreo que reescriba ``url`` a un valor sin el ID del archivo impide que se propaguen los
  borrados.
- El feed de cambios no se filtra por ``query``. Con ``query`` definido e
  ``incremental=true``, un archivo modificado que no coincide con la consulta se indexa de
  todos modos.
- ``crawl_target=both`` en un dominio grande genera aproximadamente
  ``2 + (número de unidades compartidas) + (número de usuarios)`` secuencias de listado. La
  mitigación práctica consiste en repartir las unidades compartidas y los usuarios en
  configuraciones de almacén de datos distintas.
- ``proxy_username`` y ``proxy_password`` se envían como cabecera de petición
  ``Proxy-Authorization``, que solo autentica una petición HTTP en claro. Todo el tráfico de
  las API de Google es HTTPS, y una conexión HTTPS a través de un proxy con autenticación se
  establece mediante un intercambio ``CONNECT`` que el JDK gestiona con
  ``java.net.Authenticator`` y no mediante una cabecera de petición. Un entorno así necesita
  en su lugar la opción de JVM ``-Djdk.http.auth.tunneling.disabledSchemes=`` y un
  ``Authenticator``.

Información de Referencia
=========================

- :doc:`ds-overview` - Visión general de conectores de almacén de datos
- :doc:`ds-microsoft365` - Conector de Microsoft 365
- :doc:`ds-box` - Conector de Box
- :doc:`../../admin/dataconfig-guide` - Guía de configuración de almacén de datos
- `Google Drive API <https://developers.google.com/drive/api>`_
- `Google Cloud Platform <https://console.cloud.google.com/>`_
- `Google Workspace Admin <https://admin.google.com/>`_
