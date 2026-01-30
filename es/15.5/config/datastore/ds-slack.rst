==================================
Conector de Slack
==================================

Vision General
==============

El conector de Slack proporciona funcionalidad para obtener mensajes de canales del espacio de trabajo de Slack
y registrarlos en el indice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-slack``.

Contenido Soportado
===================

- Mensajes de canales publicos
- Mensajes de canales privados
- Archivos adjuntos (opcional)

Requisitos Previos
==================

1. Se requiere la instalacion del plugin
2. Se requiere la creacion de una Slack App y configuracion de permisos
3. Se requiere la obtencion del OAuth Access Token

Instalacion del Plugin
----------------------

Instale desde "Sistema" -> "Plugins" en la pantalla de administracion:

1. Descargue ``fess-ds-slack-X.X.X.jar`` desde Maven Central
2. Cargue e instale desde la pantalla de gestion de plugins
3. Reinicie |Fess|

O consulte :doc:`../../admin/plugin-guide` para mas detalles.

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
     - Company Slack
   * - Nombre del manejador
     - SlackDataStore
   * - Habilitado
     - Activado

Configuracion de Parametros
---------------------------

::

    token=xoxp-your-token-here
    channels=general,random
    file_crawl=false
    include_private=false

Lista de Parametros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametro
     - Requerido
     - Descripcion
   * - ``token``
     - Si
     - OAuth Access Token de la Slack App
   * - ``channels``
     - Si
     - Canales a rastrear (separados por comas, o ``*all``)
   * - ``file_crawl``
     - No
     - Rastrear archivos tambien (predeterminado: ``false``)
   * - ``include_private``
     - No
     - Incluir canales privados (predeterminado: ``false``)

Configuracion de Script
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
     - Descripcion
   * - ``message.text``
     - Contenido de texto del mensaje
   * - ``message.user``
     - Nombre para mostrar del remitente del mensaje
   * - ``message.channel``
     - Nombre del canal donde se envio el mensaje
   * - ``message.timestamp``
     - Fecha/hora de envio del mensaje
   * - ``message.permalink``
     - Enlace permanente del mensaje
   * - ``message.attachments``
     - Informacion de respaldo de archivos adjuntos

Configuracion de Slack App
==========================

1. Crear Slack App
------------------

Acceda a https://api.slack.com/apps:

1. Haga clic en "Create New App"
2. Seleccione "From scratch"
3. Ingrese el nombre de la aplicacion (ej: Fess Crawler)
4. Seleccione el espacio de trabajo
5. Haga clic en "Create App"

2. Configurar OAuth & Permissions
---------------------------------

En el menu "OAuth & Permissions":

**Agregue a Bot Token Scopes**:

Para solo canales publicos:

- ``channels:history`` - Lectura de mensajes de canales publicos
- ``channels:read`` - Lectura de informacion de canales publicos

Para incluir canales privados (``include_private=true``):

- ``channels:history``
- ``channels:read``
- ``groups:history`` - Lectura de mensajes de canales privados
- ``groups:read`` - Lectura de informacion de canales privados

Para rastrear archivos tambien (``file_crawl=true``):

- ``files:read`` - Lectura de contenido de archivos

3. Instalar la Aplicacion
-------------------------

En el menu "Install App":

1. Haga clic en "Install to Workspace"
2. Verifique los permisos y haga clic en "Permitir"
3. Copie el "Bot User OAuth Token" (comienza con ``xoxb-``)

.. note::
   Normalmente se usa el Bot User OAuth Token que comienza con ``xoxb-``,
   pero tambien se puede usar el User OAuth Token que comienza con ``xoxp-`` en los parametros.

4. Agregar a Canales
--------------------

Agregue la App a los canales que desea rastrear:

1. Abra el canal en Slack
2. Haga clic en el nombre del canal
3. Seleccione la pestana "Integraciones"
4. Haga clic en "Agregar una aplicacion"
5. Agregue la aplicacion creada

Ejemplos de Uso
===============

Rastrear Canales Especificos
----------------------------

Parametros:

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

Parametros:

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

Parametros:

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

Solucion de Problemas
=====================

Error de Autenticacion
----------------------

**Sintoma**: ``invalid_auth`` o ``not_authed``

**Verificar**:

1. Verificar que el token se haya copiado correctamente
2. Verificar el formato del token:

   - Bot User OAuth Token: comienza con ``xoxb-``
   - User OAuth Token: comienza con ``xoxp-``

3. Verificar que la aplicacion este instalada en el espacio de trabajo
4. Verificar que se hayan otorgado los permisos necesarios

Canal No Encontrado
-------------------

**Sintoma**: ``channel_not_found``

**Verificar**:

1. Verificar que el nombre del canal sea correcto (sin #)
2. Verificar que la aplicacion este agregada al canal
3. Para canales privados, establecer ``include_private=true``
4. Verificar que el canal exista y no este archivado

No se Pueden Obtener Mensajes
-----------------------------

**Sintoma**: El rastreo tiene exito pero hay 0 mensajes

**Verificar**:

1. Verificar que se hayan otorgado los ambitos necesarios:

   - ``channels:history``
   - ``channels:read``
   - Para canales privados: ``groups:history``, ``groups:read``

2. Verificar que existan mensajes en el canal
3. Verificar que la aplicacion este agregada al canal
4. Verificar que la Slack App este habilitada

Limite de Tasa de API
---------------------

**Sintoma**: ``rate_limited``

**Solucion**:

1. Aumentar el intervalo de rastreo
2. Reducir el numero de canales
3. Dividir en multiples almacenes de datos y distribuir la programacion

Limites de la API de Slack:

- Metodos de nivel 3: 50+ solicitudes/minuto
- Metodos de nivel 4: 100+ solicitudes/minuto

Informacion de Referencia
=========================

- :doc:`ds-overview` - Vision general de conectores de almacen de datos
- :doc:`ds-atlassian` - Conector de Atlassian
- :doc:`../../admin/dataconfig-guide` - Guia de configuracion de almacen de datos
- `Slack API Documentation <https://api.slack.com/>`_
- `Slack Bot Token Scopes <https://api.slack.com/scopes>`_
