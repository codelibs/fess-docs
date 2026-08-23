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
- Archivos adjuntos (opcional)

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
     - Si
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
     - Número máximo de entradas en el caché de información de usuarios (predeterminado: ``10000``)
   * - ``bot_cache_size``
     - No
     - Número máximo de entradas en el caché de información de bots (predeterminado: ``10000``)
   * - ``channel_cache_size``
     - No
     - Número máximo de entradas en el caché de información de canales (predeterminado: ``10000``)

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

Para solo canales públicos:

- ``channels:history`` - Lectura de mensajes de canales públicos
- ``channels:read`` - Lectura de información de canales públicos
- ``users:read`` - Lectura de información de usuario (requerido para resolución de nombre para mostrar)

Para incluir canales privados (``include_private=true``):

- ``channels:history``
- ``channels:read``
- ``groups:history`` - Lectura de mensajes de canales privados
- ``groups:read`` - Lectura de información de canales privados
- ``users:read``

Para rastrear archivos también (``file_crawl=true``):

- ``files:read`` - Lectura de contenido de archivos

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
-----------------------------

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
-------------------------------------------

Script:

::

    title="[" + message.channel + "] " + message.user
    content=message.text
    digest=message.text.substring(0, Math.min(200, message.text.length()))
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

Solución de Problemas
=====================

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
4. Verificar que el canal exista y no esté archivado

No se Pueden Obtener Mensajes
-----------------------------

**Síntoma**: El rastreo tiene éxito pero hay 0 mensajes

**Verificar**:

1. Verificar que se hayan otorgado los ámbitos necesarios:

   - ``channels:history``
   - ``channels:read``
   - Para canales privados: ``groups:history``, ``groups:read``

2. Verificar que existan mensajes en el canal
3. Verificar que la aplicación esté agregada al canal
4. Verificar que la Slack App esté habilitada

Error de Permisos Insuficientes
--------------------------------

**Síntoma**: ``missing_scope``

**Solución**:

1. Agregar los ámbitos necesarios en la configuración de la Slack App:

   **Canales Públicos**:

   - ``channels:history``
   - ``channels:read``

   **Canales Privados**:

   - ``groups:history``
   - ``groups:read``

   **Archivos**:

   - ``files:read``

2. Reinstalar la aplicación
3. Reiniciar |Fess|

No se Pueden Rastrear Archivos
-------------------------------

**Síntoma**: No se obtienen archivos aunque ``file_crawl=true``

**Verificar**:

1. Verificar que se haya otorgado el ámbito ``files:read``
2. Verificar que realmente se hayan publicado archivos en el canal
3. Verificar los permisos de acceso a los archivos

Límite de Tasa de API
---------------------

**Síntoma**: ``rate_limited``

**Solución**:

1. Aumentar el intervalo de rastreo
2. Reducir el número de canales
3. Dividir en múltiples almacenes de datos y distribuir la programación

Límites de la API de Slack:

- Métodos de nivel 3: 50+ solicitudes/minuto
- Métodos de nivel 4: 100+ solicitudes/minuto

Gran Volumen de Mensajes
-------------------------

**Síntoma**: El rastreo tarda mucho tiempo o se agota el tiempo de espera

**Solución**:

1. Dividir los canales y configurar múltiples almacenes de datos
2. Distribuir la programación de rastreo
3. Considerar una configuración para excluir mensajes antiguos

Ejemplos Avanzados de Script
==============================

Procesamiento de Mensajes
--------------------------

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
- `Slack API Documentation <https://api.slack.com/>`_
- `Slack Bot Token Scopes <https://api.slack.com/scopes>`_
