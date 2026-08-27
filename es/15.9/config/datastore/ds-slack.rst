==================================
Conector de Slack
==================================

Visión General
==============

El conector de Slack proporciona funcionalidad para obtener mensajes de canales del espacio de trabajo de Slack
y registrarlos en el índice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-slack``.

Contenido Soportado
===================

- Mensajes de canales públicos
- Mensajes de canales privados
- Mensajes de respuesta en hilos (obtenidos mediante ``conversations.replies``)
- Archivos adjuntos (opcional)

Lo siguiente queda fuera del alcance:

- Los mensajes de eventos del sistema (``channel_join``, ``channel_topic``, ``pinned_item``,
  etc.) se excluyen de la indexación de forma predeterminada (``ignore_system_events``)
- Mensajes directos (DM) y DM de grupo
- Transcripciones de Huddle y Clips (Slack no ofrece una API pública para estos, por lo que no
  se pueden rastrear)

Requisitos Previos
==================

1. Se requiere la instalación del plugin
2. Se requiere la creación de una Slack App y configuración de permisos
3. Se requiere la obtención del OAuth Access Token

Instalación del Plugin
----------------------

Instale desde "Sistema" -> "Plugins" en la pantalla de administración:

1. Descargue ``fess-ds-slack-X.X.X.jar`` desde Maven Central
2. Cargue e instale desde la pantalla de gestión de plugins
3. Reinicie |Fess|

O consulte :doc:`../../admin/plugin-guide` para más detalles.

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
     - Company Slack
   * - Nombre del manejador
     - SlackDataStore
   * - Habilitado
     - Activado

Configuración de Parámetros
---------------------------

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random
    file_crawl=false
    include_private=false

Lista de Parámetros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parámetro
     - Requerido
     - Descripción
   * - ``token``
     - Sí
     - OAuth Access Token de la Slack App
   * - ``channels``
     - No
     - Canales a rastrear (separados por comas, o ``*all``). Si no se especifica, se obtienen todos los canales (mismo comportamiento que ``*all``)
   * - ``file_crawl``
     - No
     - Rastrear archivos también (predeterminado: ``false``)
   * - ``include_private``
     - No
     - Incluir canales privados (predeterminado: ``false``)
   * - ``number_of_threads``
     - No
     - Número de hilos de procesamiento paralelo (predeterminado: ``1``)
   * - ``max_filesize``
     - No
     - Tamaño máximo de archivo en bytes (predeterminado: ``10000000``)
   * - ``ignore_error``
     - No
     - Continuar procesamiento en caso de error (predeterminado: ``true``)
   * - ``supported_mimetypes``
     - No
     - Regex para tipos MIME permitidos (predeterminado: ``.*``)
   * - ``include_pattern``
     - No
     - Patrón regex para URLs a incluir
   * - ``exclude_pattern``
     - No
     - Patrón regex para URLs a excluir
   * - ``proxy_host``
     - No
     - Host del proxy HTTP
   * - ``proxy_port``
     - No
     - Puerto del proxy HTTP (requerido cuando se especifica ``proxy_host``)
   * - ``file_types``
     - No
     - Filtro de tipo de archivo para la API de Slack (predeterminado: ``all``)
   * - ``channel_count``
     - No
     - Número de canales por página de API (predeterminado: ``100``)
   * - ``message_count``
     - No
     - Número de mensajes por página de API (predeterminado: ``100``)
   * - ``file_count``
     - No
     - Número de archivos por página de API (predeterminado: ``20``)
   * - ``user_count``
     - No
     - Número de usuarios por página de API (predeterminado: ``100``)
   * - ``user_cache_size``
     - No
     - Número máximo de entradas en la caché de información de usuarios (predeterminado: ``10000``)
   * - ``bot_cache_size``
     - No
     - Número máximo de entradas en la caché de información de bots (predeterminado: ``10000``)
   * - ``channel_cache_size``
     - No
     - Número máximo de entradas en la caché de información de canales (predeterminado: ``10000``)

Parámetros Avanzados
~~~~~~~~~~~~~~~~~~~~

Los siguientes parámetros controlan el comportamiento de conexión y reintentos, el ámbito
detallado del rastreo, y la sincronización de permisos:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parámetro
     - Descripción
   * - ``connection_timeout``
     - Tiempo de espera de conexión para cada solicitud a la API de Slack (milisegundos, predeterminado: ``20000``)
   * - ``read_timeout``
     - Tiempo de espera de lectura para cada solicitud a la API de Slack (milisegundos, predeterminado: ``20000``)
   * - ``max_retry_count``
     - Número máximo de reintentos tras una respuesta ``429`` (límite de tasa) o ``5xx`` (predeterminado: ``3``)
   * - ``retry_interval``
     - Tiempo de espera en milisegundos antes del primer reintento cuando la respuesta no incluye un encabezado ``Retry-After`` (predeterminado: ``3000``). Se duplica en cada intento posterior, con un tope de ``60000`` milisegundos. Si la respuesta incluye un encabezado ``Retry-After``, se usa ese valor (en segundos) en su lugar
   * - ``executor_timeout``
     - Segundos de espera, al finalizar un rastreo, para que se completen las tareas pendientes en la cola antes de forzar el cierre (predeterminado: ``60``)
   * - ``exclude_archived``
     - Si se deben excluir los canales archivados de los resultados de ``conversations.list`` (predeterminado: ``false``). Con ``true``, un canal archivado especificado por nombre en ``channels`` ya no puede resolverse (véase Solución de Problemas para más detalles)
   * - ``ignore_system_events``
     - Si se deben excluir de la indexación los mensajes de administración de canal generados automáticamente por Slack (``channel_join``, ``channel_topic``, ``pinned_item``, etc.) (predeterminado: ``true``)
   * - ``read_interval``
     - Tiempo de espera en milisegundos tras procesar cada mensaje o archivo (predeterminado: ``0`` = sin espera). Úselo para ralentizar el rastreo frente a un espacio de trabajo con un límite de tasa estricto
   * - ``max_content_length``
     - Número máximo de caracteres que el extractor de contenido (Tika) puede extraer de un archivo (predeterminado: sin definir, se aplica entonces el límite de |Fess| específico para cada tipo MIME). ``max_filesize`` es el límite del lado de la transferencia que rechaza archivos por tamaño antes de la descarga, mientras que ``max_content_length`` es el límite del lado de la extracción sobre la cantidad de texto extraído después de la descarga; ambos funcionan de forma independiente. Reducir ``max_filesize`` no sustituye a ``max_content_length`` (por ejemplo, un archivo comprimido de 1MB puede expandirse a mucho más texto al extraerse)
   * - ``permission_sync``
     - Si se debe convertir la membresía de canales privados en permisos de búsqueda (roles) (predeterminado: ``false``). Véase "Sincronización de Permisos (ACL)" más adelante para más detalles
   * - ``default_permissions``
     - Permisos adicionales aplicados a todos los documentos indexados independientemente de la membresía del canal (formato ``{user}``/``{group}``/``{role}``, separados por comas, predeterminado: vacío). Se aplica solo cuando ``permission_sync`` está habilitado

.. note::

   ``ignore_system_events`` tiene como valor predeterminado ``true``. Incluso una configuración
   de rastreo existente que no defina este parámetro dejará, tras actualizar |Fess|, de indexar
   mensajes de eventos del sistema como ``channel_join`` -- el número de documentos indexados
   disminuirá sin ningún error ni advertencia. Especifique ``ignore_system_events=false``
   explícitamente para seguir indexando estos mensajes como antes.

Configuración de Script
-----------------------

::

    title=message.user + " #" + message.channel
    digest=message.text + "\n" + message.attachments
    content=message.text
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

Campos Disponibles
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripción
   * - ``message.title``
     - Título (cadena vacía para mensajes, nombre y título del archivo para entradas de archivo)
   * - ``message.text``
     - Contenido de texto del mensaje (para entradas de archivo, el nombre del archivo y el cuerpo del archivo extraído)
   * - ``message.user``
     - Nombre para mostrar del remitente del mensaje (si no está configurado, se resuelve en el orden de nombre real, nombre de usuario y luego ID de usuario)
   * - ``message.channel``
     - Nombre del canal donde se envió el mensaje
   * - ``message.timestamp``
     - Fecha/hora de envío del mensaje
   * - ``message.permalink``
     - Enlace permanente del mensaje
   * - ``message.attachments``
     - Información de respaldo de archivos adjuntos
   * - ``message.roles``
     - Lista de permisos de búsqueda (roles) autorizados a ver este mensaje o archivo. Solo está presente cuando ``permission_sync=true``. A menos que el script asigne ``role=message.roles``, los roles calculados nunca se reflejan en el documento indexado

Configuración de Slack App
==========================

1. Crear Slack App
------------------

Acceda a https://api.slack.com/apps:

1. Haga clic en "Create New App"
2. Seleccione "From scratch"
3. Ingrese el nombre de la aplicación (ej: Fess Crawler)
4. Seleccione el espacio de trabajo
5. Haga clic en "Create App"

2. Configurar OAuth & Permissions
---------------------------------

En el menú "OAuth & Permissions":

**Agregue a Bot Token Scopes**:

Ámbitos básicos (siempre requeridos):

- ``channels:history`` - Lectura de mensajes de canales públicos
- ``channels:read`` - Lectura de información de canales públicos
- ``users:read`` - Lectura de información de usuario (requerido para resolución de nombre para mostrar)
- ``team:read`` - Lectura de información del espacio de trabajo. ``team.info`` se invoca en cada
  rastreo, por lo que este ámbito es obligatorio; sin él, este conector recurre a una llamada
  adicional a ``chat.getPermalink`` por cada mensaje, incrementando notablemente el número de
  llamadas a la API

Al incluir también canales privados (``include_private=true``):

- ``groups:history`` - Lectura de mensajes de canales privados
- ``groups:read`` - Lectura de información de canales privados

Al rastrear también archivos (``file_crawl=true``):

- ``files:read`` - Lectura de contenido de archivos

Al sincronizar también los permisos de canales privados (``permission_sync=true``):

- ``users:read.email`` - Lectura de las direcciones de correo de los miembros (requerido para
  la sincronización de permisos)

3. Instalar la Aplicación
-------------------------

En el menú "Install App":

1. Haga clic en "Install to Workspace"
2. Verifique los permisos y haga clic en "Permitir"
3. Copie el "Bot User OAuth Token" (comienza con ``xoxb-``)

.. note::
   Normalmente se usa el Bot User OAuth Token que comienza con ``xoxb-``,
   pero también se puede usar el User OAuth Token que comienza con ``xoxp-`` en los parámetros.

4. Agregar a Canales
--------------------

Agregue la App a los canales que desea rastrear:

1. Abra el canal en Slack
2. Haga clic en el nombre del canal
3. Seleccione la pestaña "Integraciones"
4. Haga clic en "Agregar una aplicación"
5. Agregue la aplicación creada

Sincronización de Permisos (ACL)
================================

El conector de Slack puede convertir la membresía de un canal privado en permisos de búsqueda
(roles) de |Fess|, de modo que solo los miembros de ese canal puedan buscar su contenido. Esta
función está deshabilitada de forma predeterminada.

.. note::

   ``permission_sync`` solo calcula los roles; no los aplica automáticamente. Solo después de
   agregar ``role=message.roles`` al script, los roles calculados se reflejan en los documentos
   indexados. Olvidar este mapeo igualmente incurre en las llamadas adicionales a la API y en la
   omisión de canales privados que provoca ``permission_sync=true``, sin proporcionar ningún
   control de acceso.

Habilitarlo
-----------

1. Agregue el ámbito ``users:read.email`` a la Slack App (requerido para resolver las
   direcciones de correo de los miembros)
2. Establezca ``permission_sync=true`` en los parámetros
3. Agregue ``role=message.roles`` al script

Parámetros:

::

    include_private=true
    permission_sync=true

Script:

::

    role=message.roles

Comportamiento de Fallo Cerrado (Fail-Closed)
---------------------------------------------

Un canal privado no se indexa en absoluto en un rastreo dado si se da alguno de los siguientes
casos (esto es un comportamiento "fail-closed": el riesgo es una indexación incompleta, nunca
exponer contenido accidentalmente a todos):

- No se pudo obtener la lista de miembros del canal
- La lista de miembros volvió vacía (esto ocurre cuando el propio usuario bot del token de
  rastreo no es miembro de ese canal privado)
- El canal tiene miembros, pero no se pudo resolver la dirección de correo de ninguno de ellos
  (generalmente porque falta el ámbito ``users:read.email``)

Los canales públicos nunca invocan ``conversations.members`` y siempre se consideran visibles
para todos.

Coincidencia del Nombre de Principal
------------------------------------

La verificación de permisos en tiempo de búsqueda utiliza el nombre de inicio de sesión de
|Fess| (el nombre de principal). Dado que los roles que calcula esta función se derivan de las
direcciones de correo de Slack, el nombre de inicio de sesión de |Fess| debe coincidir con la
dirección de correo de Slack. Slack normaliza las direcciones de correo a minúsculas, por lo
que mantenga también en minúsculas los nombres de inicio de sesión de |Fess|. Una discrepancia
no expone el contenido de otro usuario -- simplemente hace que las búsquedas del usuario
afectado siempre devuelvan cero resultados, lo cual puede confundirse fácilmente con un error
no relacionado.

Otras Notas
-----------

- No se utilizan los grupos de usuarios (User Group) de Slack; los permisos se calculan
  directamente a partir de la dirección de correo de cada miembro
- ``default_permissions`` le permite otorgar permisos adicionales a todos los documentos
  independientemente de la membresía del canal (se aplica solo cuando ``permission_sync=true``)
- Dejar ``permission_sync=false`` mientras se establece ``include_private=true`` indexa el
  contenido de canales privados usando únicamente los permisos configurados en el campo
  "Permiso" del almacén de datos; si ese campo se deja vacío, el contenido queda efectivamente
  público para todos
- Habilitar ``permission_sync`` más tarde no asegura de forma retroactiva el contenido ya
  indexado por un rastreo anterior sin restricciones. Para aplicar roles a ese contenido,
  establezca ``permission_sync=true`` y ``role=message.roles``, y vuelva a rastrear. Del mismo
  modo, deshabilitar ``permission_sync`` más adelante no elimina los roles ya aplicados a los
  documentos indexados previamente

Ejemplos de Uso
===============

Rastrear Canales Específicos
----------------------------

Parámetros:

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random,tech-discussion
    file_crawl=false
    include_private=false

Script:

::

    title=message.user + " #" + message.channel
    digest=message.text + "\n" + message.attachments
    content=message.text
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

Rastrear Todos los Canales
--------------------------

Parámetros:

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    file_crawl=false
    include_private=false

Script:

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink

Rastrear Incluyendo Canales Privados
------------------------------------

Parámetros:

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    file_crawl=false
    include_private=true

Script:

::

    title=message.user + " #" + message.channel
    digest=message.text
    content=message.text + "\nAdjunto: " + message.attachments
    created=message.timestamp
    url=message.permalink

Rastrear Incluyendo Archivos
----------------------------

Parámetros:

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random
    file_crawl=true
    include_private=false

Script:

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink

Incluir Información Detallada de Mensajes
-----------------------------------------

Script:

::

    title="[" + message.channel + "] " + message.user
    content=message.text
    digest=message.text.substring(0, Math.min(200, message.text.length()))
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

Rastrear con Sincronización de Permisos
---------------------------------------

Restringe el contenido de canales privados de modo que solo los miembros de ese canal puedan
buscarlo. Agregue de antemano el ámbito ``users:read.email`` a la Slack App.

Parámetros:

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    include_private=true
    permission_sync=true

Script:

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink
    role=message.roles

.. note::

   Si olvida ``role=message.roles``, los roles calculados nunca se reflejarán en los documentos
   indexados. Véase "Sincronización de Permisos (ACL)" para más detalles.

Solución de Problemas
=====================

Cómo Funciona el Manejo de Errores
----------------------------------

El conector de Slack clasifica los errores de la API de Slack en tres tipos:

- **Errores fatales**\ (``invalid_auth``, ``token_revoked``, ``account_inactive``,
  ``missing_scope``, ``not_authed``, ``token_expired``): el token en sí no se puede usar, por
  lo que falla todo el trabajo de rastreo
- **Errores transitorios**\ (``ratelimited``, ``internal_error``, ``fatal_error``,
  ``service_unavailable``, ``request_timeout``): si los reintentos no resuelven el error, falla
  todo el trabajo de rastreo (véase "Límite de Tasa de API" más adelante para el comportamiento
  de reintento)
- **Errores por canal**\ (``channel_not_found``, ``not_in_channel``, etc.): solo se omite ese
  canal con una advertencia, y el rastreo continúa con el siguiente canal

En versiones anteriores, un error fatal aún podía reportarse como un rastreo "exitoso" que
indexaba silenciosamente cero documentos o solo algunos. Esta división en tres tipos ahora
garantiza que los errores fatales y transitorios siempre se reporten como un fallo del trabajo.

Error de Autenticación
----------------------

**Síntoma**: ``invalid_auth`` o ``not_authed``

**Verificar**:

1. Verificar que el token se haya copiado correctamente
2. Verificar el formato del token:

   - Bot User OAuth Token: comienza con ``xoxb-``
   - User OAuth Token: comienza con ``xoxp-``

3. Verificar que la aplicación esté instalada en el espacio de trabajo
4. Verificar que se hayan otorgado los permisos necesarios

Canal No Encontrado
-------------------

**Síntoma**: ``channel_not_found``

**Verificar**:

1. Verificar que el nombre del canal sea correcto (sin #)
2. Verificar que la aplicación esté agregada al canal
3. Para canales privados, establecer ``include_private=true``
4. Verifique si ``exclude_archived=true`` está configurado. De forma predeterminada
   (``exclude_archived=false``), los canales archivados se siguen listando y rastreando; solo
   al establecerlo en ``true`` deja de poder resolverse un canal archivado especificado por
   nombre en ``channels``

No se Pueden Obtener Mensajes
-----------------------------

**Síntoma**: El rastreo tiene éxito, pero se indexan pocos documentos o ninguno

**Verificar**:

1. ``ignore_system_events`` tiene como valor predeterminado ``true``. Si los mensajes de un
   canal son todos eventos del sistema como ``channel_join``, no se indexará ningún documento
   para él (véase "Parámetros Avanzados")
2. Verificar que existan mensajes en el canal
3. Verificar que la aplicación esté agregada al canal
4. Con ``permission_sync=true``, un canal privado cuya membresía no pueda resolverse no se
   indexa en ese rastreo (fail-closed; véase "Sincronización de Permisos (ACL)")

.. note::

   En versiones anteriores, un ámbito faltante (``missing_scope``) aún podía dejar que el
   rastreo "tuviera éxito" con cero mensajes. Los errores fatales, incluido ``missing_scope``,
   ahora hacen fallar todo el trabajo de rastreo. Si su trabajo está fallando, consulte "Error
   de Permisos Insuficientes" más adelante en lugar de esta sección.

Error de Permisos Insuficientes
-------------------------------

**Síntoma**: ``missing_scope`` (hace fallar todo el trabajo de rastreo)

**Solución**:

1. Agregar los ámbitos necesarios en la configuración de la Slack App:

   **Básico**\ (siempre requerido):

   - ``channels:history``
   - ``channels:read``
   - ``users:read``
   - ``team:read``

   **Canales Privados**:

   - ``groups:history``
   - ``groups:read``

   **Archivos**:

   - ``files:read``

   **Sincronización de Permisos**\ (``permission_sync=true``):

   - ``users:read.email``

2. Reinstalar la aplicación
3. Reiniciar |Fess|

No se Pueden Rastrear Archivos
------------------------------

**Síntoma**: No se obtienen archivos aunque ``file_crawl=true``

**Verificar**:

1. Verificar que se haya otorgado el ámbito ``files:read``
2. Verificar que realmente se hayan publicado archivos en el canal
3. Verificar los permisos de acceso a los archivos
4. Un archivo que supere ``max_filesize`` no se descarga (verifique el registro en busca de
   una advertencia)

Límite de Tasa de API
---------------------

**Síntoma**: ``ratelimited`` (hace fallar todo el trabajo de rastreo)

**Solución**:

1. Si los valores predeterminados de ``max_retry_count`` y ``retry_interval`` no resuelven el
   problema, auméntelos
2. Establezca ``read_interval`` para ralentizar el rastreo
3. Reduzca el número de canales, o divida en varios almacenes de datos y distribuya los
   horarios

Un error ``ratelimited`` de la API de Slack se reintenta automáticamente: usando el valor del
encabezado ``Retry-After``, en segundos, cuando está presente, o en su defecto un retroceso
exponencial a partir de ``retry_interval`` (hasta ``max_retry_count`` intentos, con un tope de
60 segundos). Si el límite de tasa persiste tras agotar todos los reintentos, falla todo el
trabajo de rastreo.

Niveles (tiers) de la API de Slack (límites de frecuencia de llamadas):

- Nivel 1: 1+ solicitudes/minuto
- Nivel 2: 20+ solicitudes/minuto -- ``conversations.list``, ``users.list`` (se obtienen por
  completo de forma incondicional al inicio de cada rastreo, lo que hace que este nivel sea el
  más propenso a agotarse)
- Nivel 3: 50+ solicitudes/minuto -- ``conversations.history``, ``conversations.replies``,
  ``files.list``
- Nivel 4: 100+ solicitudes/minuto -- ``conversations.members`` (solo cuando
  ``permission_sync=true``), ``files.info`` (actualmente no invocado por el rastreo de este
  conector)

.. note::

   El endurecimiento del límite de tasa de Slack del 29 de mayo de 2025 (que limita
   ``conversations.history`` y ``conversations.replies`` a 50+ solicitudes/minuto) se aplica
   solo a aplicaciones distribuidas fuera del espacio de trabajo que las creó, como a través
   del Slack Marketplace. No se aplica a una aplicación interna creada para |Fess| que se
   instala únicamente en el espacio de trabajo que la creó.

Gran Volumen de Mensajes
------------------------

**Síntoma**: El rastreo tarda mucho tiempo o se agota el tiempo de espera

**Solución**:

1. Dividir los canales y configurar múltiples almacenes de datos
2. Distribuir la programación de rastreo

Ejemplos Avanzados de Script
============================

Procesamiento de Mensajes
-------------------------

Digest de mensajes largos:

::

    title=message.user + " #" + message.channel
    content=message.text
    digest=message.text.length() > 100 ? message.text.substring(0, 100) + "..." : message.text
    created=message.timestamp
    url=message.permalink

Formato del nombre del canal:

::

    title="[Slack: " + message.channel + "] " + message.user
    content=message.text
    created=message.timestamp
    url=message.permalink

Información de Referencia
=========================

- :doc:`ds-overview` - Visión general de conectores de almacén de datos
- :doc:`ds-atlassian` - Conector de Atlassian
- :doc:`../../admin/dataconfig-guide` - Guía de configuración de almacén de datos
- :doc:`../security-role` - Guía de configuración de búsqueda basada en roles
- `Slack API Documentation <https://api.slack.com/>`_
- `Slack Bot Token Scopes <https://api.slack.com/scopes>`_
- `Slack API Rate Limits <https://docs.slack.dev/apis/web-api/rate-limits>`_
