=================================================
Buscar archivos en Google Drive, SharePoint y Box
=================================================

Introducción
============

Cuando cada departamento usa Google Drive, SharePoint Online o Box según le convenga, cada vez se dedica más tiempo a recordar dónde se guardó un documento.
Con los plugins de almacén de datos de Fess, los archivos de los tres servicios se pueden encontrar desde una sola página de búsqueda.

Sin embargo, en el almacenamiento en la nube conviven archivos con permisos de acceso distintos.
Un error de configuración puede hacer que archivos confidenciales, como contratos, aparezcan en los resultados de búsqueda de usuarios que ni siquiera han iniciado sesión.
Este artículo explica, para cada servicio, una configuración mínima que funciona tal cual, y cómo trasladar a Fess los permisos originales.

Los pasos comunes a todos los almacenes de datos —instalar los plugins, los nombres de manejador, los parámetros, cómo escribir los scripts y cómo crear los trabajos— se recogen en :doc:`datastore-basics`.
Léalo antes de continuar.
Los valores de configuración de este artículo corresponden a Fess 15.9 y a la versión 15.9.0 de cada plugin.

Lo que vamos a construir
========================

.. list-table::
   :header-rows: 1
   :widths: 18 22 22 38

   * - Servicio
     - Plugin
     - Nombre del manejador
     - Qué hay que preparar en el servicio
   * - Google Drive
     - ``fess-ds-gsuite``
     - ``GoogleDriveDataStore``
     - Una clave JSON de una cuenta de servicio y la delegación en todo el dominio
   * - SharePoint Online
     - ``fess-ds-microsoft365``
     - ``OneDriveDataStore``
     - Un registro de aplicación en Entra ID (secreto de cliente) y permisos de aplicación de Microsoft Graph
   * - Box
     - ``fess-ds-box``
     - ``BoxDataStore``
     - Una aplicación personalizada de Box con autenticación JWT

Si ejecuta Fess en Docker, puede enumerar los nombres y versiones de los plugins, separados por espacios, en la variable de entorno ``FESS_PLUGINS`` para instalarlos todos al arrancar.

.. code-block:: yaml

    environment:
      - FESS_PLUGINS=fess-ds-gsuite:15.9.0 fess-ds-microsoft365:15.9.0 fess-ds-box:15.9.0

Si los instala desde la interfaz de administración o con ``fess-setup``, debe reiniciar Fess después de la instalación (``FESS_PLUGINS`` instala los plugins antes de que arranque Fess, por lo que no hace falta reiniciar).

Primero decida quién puede ver los resultados
=============================================

Al crear una nueva configuración de almacén de datos, el campo "Permisos" ya contiene ``{role}guest``.
Si este valor se queda, los archivos importados podrán encontrarlos usuarios que no han iniciado sesión.
Los tres plugins colocan en ``file.roles`` los roles generados a partir de la configuración de uso compartido original.
Por eso la configuración es la misma en los tres en estos dos puntos:

- Borrar ``{role}guest`` del campo "Permisos" y dejarlo vacío
- Escribir ``role=file.roles`` en el script

Ambos puntos son necesarios porque cada plugin trata el campo "Permisos" de forma distinta.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Plugin
     - Valor del campo "Permisos"
     - Parámetro ``default_permissions``
   * - Google Drive
     - No se usa si escribe ``role=file.roles``. Si no lo escribe, el valor del campo (inicialmente ``{role}guest``) se asigna tal cual a todos los archivos
     - Solo se usa para los archivos de los que no se obtuvo nada de la ACL de Drive. Si tampoco está definido, esos archivos no se importan
   * - SharePoint (OneDriveDataStore)
     - Se combina con ``file.roles``. Si deja ``{role}guest``, todos los archivos quedan públicos
     - Se añade a todos los archivos
   * - Box
     - Se combina con ``file.roles``. Si deja ``{role}guest``, todos los archivos quedan públicos
     - Se añade a todos los archivos

``file.roles`` contiene cadenas que representan a los usuarios y grupos de cada servicio.

- Google Drive: los usuarios y grupos son direcciones de correo electrónico, y los propietarios de los archivos usan el mismo formato. El uso compartido con el dominio se convierte en ``{group}<nombre-de-dominio>`` (configurable con ``domain_permission_format``), y el uso compartido público que se puede encontrar mediante búsqueda (``anyone``) se convierte en el rol ``guest``. El uso compartido solo con quienes tienen el enlace no se convierte en ningún rol.
- SharePoint: los usuarios son su ID de objeto y su UPN, y los grupos, su ID y su nombre para mostrar. Un vínculo para compartir dirigido a "personas de su organización" se convierte en el grupo ``EVERYONE_IN_TENANT``.
- Box: los usuarios son su ID de usuario de Box y su inicio de sesión (dirección de correo electrónico), y los grupos, su ID de grupo de Box. Además de las colaboraciones del propio archivo, se incluyen las colaboraciones y los propietarios de las carpetas superiores.

Durante la búsqueda, estos valores se comparan con el nombre de usuario y los nombres de grupo del usuario que ha iniciado sesión en Fess.
Por ejemplo, para que se apliquen los permisos de usuario de Google Drive, el nombre de usuario de Fess debe coincidir con la dirección de correo electrónico.
Consulte :doc:`guide-05` para el concepto de roles y :doc:`guide-15` para el inicio de sesión mediante SSO.

La configuración de almacén de datos no tiene un campo propio para las etiquetas que permiten filtrar los resultados por servicio.
Añada al script una línea como ``label="box"`` o cree una etiqueta que coincida con las URL (para más detalles, consulte :doc:`datastore-basics`).
Los valores de etiqueta solo pueden contener caracteres alfanuméricos y ``_``, por lo que no se puede crear un valor con guion como ``google-drive``.

Google Drive: importar unidades compartidas
===========================================

Preparación en Google
---------------------

En la versión 15.9, ``fess-ds-gsuite`` funciona por defecto con ``crawl_target=shared_drives``.
Este modo lee todas las unidades compartidas del dominio suplantando a un administrador del dominio.

1. Cree un proyecto en la consola de Google Cloud y habilite la API de Google Drive
2. Cree una cuenta de servicio y, en la pestaña [Keys], cree y descargue una clave en formato JSON
3. Habilite la delegación en todo el dominio para la cuenta de servicio y anote su ID de cliente de OAuth 2
4. En la consola de administración de Google Workspace, en [Security] > [Access and data control] > [API controls] > [Domain-wide delegation], autorice para ese ID de cliente el ámbito ``https://www.googleapis.com/auth/drive.readonly``

La cuenta indicada en ``impersonate_user`` debe ser administrador del dominio de Google Workspace.
Si ``crawl_target`` no es ``legacy`` y falta ``impersonate_user``, el rastreo se detiene con un error al iniciarse.

Parámetros y script
-------------------

En [Rastreador] > [Almacén de datos] > [Crear nuevo], seleccione ``GoogleDriveDataStore`` como "Nombre del manejador" y vacíe el campo "Permisos".
Copie en ``private_key``, ``private_key_id`` y ``client_email`` los valores del mismo nombre de la clave JSON.
Escriba ``private_key`` en una sola línea, dejando los saltos de línea como ``\n``.

.. code-block:: properties

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBg...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com
    impersonate_user=admin@example.com
    crawl_target=shared_drives
    script_type=javascript

.. code-block:: properties

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created_time
    last_modified=file.modified_time
    role=file.roles

``file.url`` es el ``webViewLink`` del archivo.
Para reflejar las eliminaciones se presupone que la URL indexada contiene el ID de archivo de Drive.
Por eso, use ``url`` tal cual, sin reescribirlo.

Los demás ámbitos de importación son los siguientes.

- ``crawl_target=users``: lee la unidad "Mi unidad" de todos los usuarios. Debe habilitar la API Admin SDK y añadir el ámbito ``https://www.googleapis.com/auth/admin.directory.user.readonly`` (tanto en la delegación como en el parámetro ``scopes``).
- ``crawl_target=legacy``: lee solo los archivos compartidos directamente con la dirección de la cuenta de servicio. No se necesitan la delegación ni ``impersonate_user``.

Rastreo incremental
-------------------

Si añade ``incremental=true``, a partir del segundo rastreo solo se lee el flujo de cambios de Drive.
En este modo, ``delete_old_docs`` se fuerza a ``false``, y los archivos eliminados de Drive pueden quedarse en el índice.
Además, los archivos sin cambios no se vuelven a registrar, de modo que, si no se hace nada más, desaparecen de los resultados de búsqueda cuando pasan los días indicados en "Eliminar documentos anteriores" (3 días por defecto) (consulte la sección sobre la caducidad de los documentos en :doc:`datastore-basics`).

Si usa el rastreo incremental, combínelo de la siguiente manera.

- Cree también una configuración de rastreo completo sin ``incremental`` y ejecútela periódicamente, por ejemplo una vez por semana
- Indique en ambas configuraciones un ``time_to_live`` algo más largo que el intervalo del rastreo completo (para un rastreo completo semanal, ``time_to_live=11520``, es decir, 8 días)

Los archivos eliminados de Drive desaparecen de los resultados de búsqueda cuando vence este plazo.
El plugin vuelve a escribir la posición del flujo de cambios en el campo "Parámetro"; no edite el valor que escribe.

SharePoint Online: importar archivos de bibliotecas de documentos
=================================================================

Qué manejador usar
------------------

Para buscar en el contenido de los archivos de las bibliotecas de documentos de SharePoint, use ``OneDriveDataStore`` de ``fess-ds-microsoft365``.

- ``SharePointDocLibDataStore`` solo registra cada biblioteca como un único documento y no importa los archivos que contiene.
- ``fess-ds-sharepoint`` (``SharePointDataStore``) está pensado para SharePoint Server local. No es compatible con Microsoft Graph, y su documentación indica que para SharePoint Online se use ``fess-ds-microsoft365``.

Preparación en Entra ID
-----------------------

1. Cree un registro nuevo en [App registrations] en Azure Portal
2. En [Certificates & secrets], cree un secreto de cliente nuevo y anote su valor (aquí se decide su caducidad)
3. En [API permissions] > [Microsoft Graph] > [Application permissions], añada los cuatro permisos indicados abajo
4. Ejecute [Grant admin consent]

Añada los siguientes permisos de aplicación.

- ``Files.Read.All``
- ``User.Read.All``, ``Group.Read.All``: necesarios en cualquier ámbito de importación para obtener los nombres de usuario y de grupo de las ACL
- ``Sites.Read.All``: necesario para enumerar los sitios con ``shared_documents_drive_crawler=true``

Parámetros y script
-------------------

Si no se especifica nada, ``OneDriveDataStore`` lee todos los sitios de SharePoint y, además, el OneDrive de todos los usuarios y las unidades de todos los grupos de Microsoft 365.
Para limitarse a SharePoint, indique explícitamente los tres indicadores.

.. code-block:: properties

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your-client-secret
    shared_documents_drive_crawler=true
    user_drive_crawler=false
    group_drive_crawler=false
    script_type=javascript

.. code-block:: properties

    url=file.web_url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created
    last_modified=file.last_modified
    role=file.roles

Para limitarse a bibliotecas concretas, ponga los tres indicadores a ``false`` e indique el ID de la unidad en ``drive_id``.
El ID de la unidad se obtiene con ``GET /sites/{site-id}/drives`` de Microsoft Graph.
Si especifica solo ``drive_id`` y mantiene los indicadores, esa unidad simplemente se "añade" a la importación general.

Permisos que faltan y reintentos
--------------------------------

La ACL de cada archivo se obtiene con una llamada a Graph por archivo.
Lo que ocurre cuando esta llamada falla lo determina ``permission_failure_policy``.
Con el valor por defecto ``skip``, el archivo no se registra y queda anotado en [Información del sistema] > [URL de fallo] y en un registro WARN.
Si lo cambia a ``index_without_acl``, los archivos se registran con una ACL incompleta, por lo que en bibliotecas muy confidenciales es más seguro mantener el valor por defecto.

Los reintentos de las llamadas a Graph se ajustan con ``max_retry_count`` (3 por defecto, 10 como máximo) y ``retry_interval`` (en segundos, 3 por defecto, 180 como máximo).
``OneDriveDataStore`` no tiene opción de rastreo incremental y lee todo cada vez.

Box: importar una carpeta de contratos con sus permisos
=======================================================

Preparación en Box
------------------

``fess-ds-box`` solo admite la autenticación de servidor con JWT.

1. En Box Developer Console, cree una "Custom App" y elija "Server Authentication (with JWT)" como método de autenticación
2. En la pestaña [Configuration], active "Read all files and folders stored in Box" en Application Scopes
3. Elija "App + Enterprise Access" como App Access Level
4. Genere un par de claves con [Generate a Public/Private Keypair] y guarde el archivo JSON
5. Autorice la aplicación en la consola de administración de Box

Los valores ``clientID``, ``clientSecret``, ``publicKeyID``, ``privateKey``, ``passphrase`` y ``enterpriseID`` del archivo JSON corresponden, respectivamente, a ``client_id``, ``client_secret``, ``public_key_id``, ``private_key``, ``passphrase`` y ``enterprise_id``.
Los seis son obligatorios.

Limitar la importación a una sola carpeta
-----------------------------------------

Cuando el destino está definido, como los contratos del departamento jurídico, lea una sola carpeta con ``root_folder_id``.
En este modo el plugin no suplanta a los usuarios, sino que lee la carpeta como la cuenta de servicio de la aplicación.
Por eso hay que añadir la cuenta de servicio como colaboradora de la carpeta de destino.
El ID de carpeta es el número que aparece al final de la URL al abrir la carpeta en la interfaz web de Box.

.. code-block:: properties

    client_id=hdf8a7sd9f8a7sdf9a87sdf98a7sd
    client_secret=kMN7sd8f7a9sd8f7a9sd8f7a9sd8f
    public_key_id=4tg5h6j7
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDj...\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=7ba8sd9f7a9sd8f7a9sd8f7a9sd8f
    enterprise_id=1923456
    root_folder_id=123456789
    default_permissions={group}legal
    script_type=javascript

.. code-block:: properties

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at
    role=file.roles

No olvide borrar ``{role}guest`` del campo "Permisos".
En Box el valor del campo se combina con ``file.roles``, así que, si lo deja, los contratos podrán encontrarlos usuarios que no han iniciado sesión.

Los grupos de Box se convierten en roles como ID de grupo, por lo que no coinciden directamente con los nombres de grupo de Fess.
En este ejemplo, ``default_permissions={group}legal`` hace que todos los archivos sean visibles para el grupo ``legal`` de Fess.
Los usuarios con quienes se ha compartido un archivo individualmente en Box también pueden encontrarlo, siempre que su inicio de sesión (dirección de correo electrónico) coincida con su nombre de usuario de Fess.
Para añadir un rol a los archivos que tienen un vínculo compartido para toda la empresa, use ``company_shared_link_role``.

Leer los archivos de todos los usuarios
---------------------------------------

Si omite ``root_folder_id``, el plugin enumera todos los usuarios de la empresa y lee sus archivos suplantándolos uno a uno.
Puede acotar los usuarios afectados con ``filter_term``.
Las llamadas a la API mediante suplantación deben estar permitidas en la configuración de la aplicación en Box, así que compruebe la configuración en la documentación para desarrolladores de Box.

Cómo tratar los límites de frecuencia
-------------------------------------

El número de reintentos para las respuestas ``429`` y ``5xx`` es ``max_retry_attempts`` (5 por defecto).
``max_retry_count`` (10 por defecto) es el número de veces que se vuelve a crear la conexión ante una respuesta ``401`` y no tiene relación con los límites de frecuencia.
Para espaciar las llamadas a la API, establezca una espera por elemento con ``readInterval`` (en milisegundos).
``fess-ds-box`` no tiene opción de rastreo incremental.

Aspectos de operación
=====================

Caducidad de las credenciales
-----------------------------

- Un secreto de cliente de Entra ID tiene la caducidad elegida al crearlo. Cuando caduca, la autenticación falla y no se importa nada, así que cree un secreto nuevo antes de la caducidad y sustituya ``client_secret`` en los parámetros.
- Los tokens de acceso de Google los renueva automáticamente la biblioteca que usa el plugin. En la versión 15.9, ``refresh_token_interval`` se ignora y se registra una advertencia.
- Los tokens de acceso de Box se renuevan automáticamente cada ``refresh_token_interval`` segundos (3540 por defecto).

Si no se importa todo
---------------------

Al final de cada rastreo, los tres plugins esperan por defecto 60 segundos a que terminen sus hilos de trabajo, y lo que no haya terminado no se importa.
Si faltan documentos en un inquilino grande, amplíe el tiempo de espera.
El parámetro se llama ``thread_pool_timeout_seconds`` en Google Drive, ``executor_shutdown_timeout`` en SharePoint y ``thread_pool_await_timeout`` en Box (todos en segundos).

En Google Drive, las respuestas 429, 500, 502, 503 y 504, así como las respuestas 403 causadas por límites de frecuencia, se reintentan con espera exponencial.
Los reintentos se ajustan con ``max_retries`` (5 por defecto), ``retry_initial_interval_ms`` (1000 por defecto) y ``max_backoff_ms`` (32000 por defecto).

Comprobar el funcionamiento
===========================

Cómo leer los resultados de los trabajos y los registros se explica en :doc:`datastore-basics`.
En el rastreo de almacenes de datos, un trabajo puede mostrarse como "OK" aunque haya fallado la obtención de archivos, así que juzgue por el número de documentos y por los registros.
Con la configuración de este artículo, compruebe además los tres puntos siguientes.

1. Sin iniciar sesión, busque una palabra contenida en un archivo importado y confirme que no aparece ningún resultado (para asegurarse de que no olvidó vaciar el campo "Permisos")
2. Inicie sesión con un usuario con quien se haya compartido el archivo y confirme que aparece el mismo archivo
3. En la configuración de Google Drive, compruebe que ``fess-crawler.log`` no contiene ``Skipped ... because no permission could be resolved`` (son archivos que no se importaron porque su ACL estaba vacía)

Si el archivo no aparece en el paso 2, revise si el nombre de usuario y los nombres de grupo del usuario coinciden con los valores de ``file.roles``.

Resumen
=======

- Importe el contenido de los archivos de SharePoint con ``OneDriveDataStore`` y ponga a ``false`` OneDrive y las unidades de grupo si no los necesita.
- En los tres servicios, borre ``{role}guest`` del campo "Permisos" y escriba ``role=file.roles`` en el script.
- ``default_permissions`` sustituye a una ACL vacía en Google Drive y se añade a todos los archivos en SharePoint y Box.
- Solo Google Drive ofrece rastreo incremental (``incremental=true``). Si lo usa, combínelo con una configuración de rastreo completo e indique ``time_to_live`` en ambas.

Referencias
===========

- `Conector de Google Workspace <https://fess.codelibs.org/es/stable/config/datastore/ds-gsuite.html>`__
- `Conector de Microsoft 365 <https://fess.codelibs.org/es/stable/config/datastore/ds-microsoft365.html>`__
- `Conector de Box <https://fess.codelibs.org/es/stable/config/datastore/ds-box.html>`__
- `Configuración del almacén de datos <https://fess.codelibs.org/es/stable/admin/dataconfig-guide.html>`__
- `README de fess-ds-microsoft365 15.9.0 (lista de permisos de Graph) <https://github.com/codelibs/fess-ds-microsoft365/blob/fess-ds-microsoft365-15.9.0/README.md>`__
- `README de fess-ds-box 15.9.0 (file.roles y root_folder_id) <https://github.com/codelibs/fess-ds-box/blob/fess-ds-box-15.9.0/README.md>`__
