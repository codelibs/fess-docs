==========================
Notificación de Registros
==========================

Descripción General
===================

|Fess| dispone de una funcionalidad que captura automáticamente los eventos de registro de nivel ERROR o WARN y notifica a los administradores.
Esta funcionalidad permite detectar rápidamente anomalías en el sistema e iniciar la respuesta ante incidencias de forma temprana.

Características principales:

- **Canales de notificación compatibles**: Correo electrónico, Slack, Google Chat
- **Procesos objetivo**: Aplicación principal, rastreador, generación de sugerencias, generación de miniaturas
- **Deshabilitado por defecto**: Al ser un sistema de activación voluntaria (opt-in), es necesario habilitarlo explícitamente

Funcionamiento
==============

La notificación de registros funciona según el siguiente flujo.

1. El ``LogNotificationAppender`` de Log4j2 captura los eventos de registro que igualan o superan el nivel configurado.
2. Los eventos capturados se acumulan en un búfer en memoria (máximo 1,000 eventos por defecto). Si el búfer supera su límite, los eventos se descartan empezando por el más antiguo.
3. Un temporizador escribe los eventos del búfer en un índice de OpenSearch (``fess_log.notification_queue``) cada 30 segundos.
4. El trabajo programado "Log Notification" lee los eventos de OpenSearch cada 5 minutos, los agrupa por nivel de registro y envía una notificación por cada nivel.
5. Después del envío de la notificación, los eventos procesados se eliminan del índice.

.. note::
   Cada nodo notifica únicamente los registros que el mismo ha generado (los eventos se filtran por ``hostname``).
   En una configuración en cluster, se envía una notificación individual por cada nodo.

.. note::
   Para evitar bucles infinitos, se excluyen de la notificación los registros de los loggers
   relacionados con la propia funcionalidad de notificación
   (``LogNotificationAppender``, ``LogNotificationHelper``, ``LogNotificationTarget``,
   ``LogNotificationJob``, ``NotificationHelper`` y ``org.codelibs.curl``, utilizado para
   la comunicación HTTP).

Configuración
=============

Habilitación
------------

Habilitación desde la Pantalla de Administración
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Inicie sesión en la pantalla de administración.
2. Seleccione "General" del menú "Sistema".
3. Active la casilla de verificación "Log Notification".
4. Seleccione el nivel objetivo de notificación en "Log Notification Level" (``ERROR``, ``WARN``, ``INFO``, ``DEBUG``, ``TRACE``).
5. Haga clic en el botón "Actualizar".

.. note::
   Por defecto, solo se notifica el nivel ``ERROR``.
   Si selecciona ``WARN``, se notificarán tanto ``WARN`` como ``ERROR``.

Habilitación mediante Propiedades del Sistema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

También puede configurar directamente las propiedades del sistema (``system.properties``) que se guardan en la configuración "General" de la pantalla de administración.

::

    log.notification.enabled=true
    fess.log.notification.level=ERROR

Configuración del Destino de Notificación
-----------------------------------------

Los destinos de notificación (la dirección de correo, las URL de Webhook de Slack / Google Chat) se configuran todos
en la configuración "Sistema" -> "General" de la pantalla de administración. Configure al menos un destino de notificación.
Si no se ha configurado ningún destino de notificación, el trabajo de notificación de registros finaliza sin enviar nada.

Notificación por Correo Electrónico
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para utilizar la notificación por correo electrónico, es necesaria la siguiente configuración.

1. Configuración del servidor de correo (``fess_env.properties``):

   ::

       mail.smtp.server.main.host.and.port=smtp.example.com:587

2. Introduzca la dirección de correo electrónico en "Correo de notificación" en la configuración "General" de la pantalla de administración.
   Puede especificar varias direcciones separadas por comas.

Notificación por Slack
~~~~~~~~~~~~~~~~~~~~~~~

Introduzca la URL del Incoming Webhook de Slack en "Slack Webhook URLs" en la configuración "General" de la pantalla de administración.
Puede especificar varias URL separadas por comas o espacios.
Este valor se guarda como la propiedad del sistema ``slack.webhook.urls``.

Notificación por Google Chat
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Introduzca la URL del Webhook de Google Chat en "Google Chat Webhook URLs" en la configuración "General" de la pantalla de administración.
Puede especificar varias URL separadas por comas o espacios.
Este valor se guarda como la propiedad del sistema ``google.chat.webhook.urls``.

.. note::
   Si configura únicamente la URL de Webhook de Slack o Google Chat sin configurar "Correo de notificación",
   no se enviará correo electrónico y solo se realizarán las notificaciones a Slack / Google Chat.
   A Slack / Google Chat se les envía como mensaje el mismo asunto y cuerpo que la notificación por correo.

Propiedades de Configuración
============================

Las siguientes propiedades se pueden configurar en ``fess_config.properties``.

.. list-table:: Propiedades de Configuración de Notificación de Registros
   :header-rows: 1
   :widths: 40 15 45

   * - Propiedad
     - Valor Predeterminado
     - Descripción
   * - ``log.notification.flush.interval``
     - ``30``
     - Intervalo de vaciado del búfer a OpenSearch (segundos)
   * - ``log.notification.buffer.size``
     - ``1000``
     - Número máximo de eventos almacenados en el búfer en memoria
   * - ``log.notification.interval``
     - ``300``
     - Período de agregación (segundos) mostrado en el mensaje de notificación. Es un valor únicamente de visualización y no representa el intervalo real de ejecución del trabajo (véase la nota más abajo).
   * - ``log.notification.search.size``
     - ``1000``
     - Número máximo de eventos obtenidos de OpenSearch por ejecución del trabajo
   * - ``log.notification.max.display.events``
     - ``50``
     - Número máximo de eventos incluidos en un solo mensaje de notificación
   * - ``log.notification.max.message.length``
     - ``200``
     - Número máximo de caracteres por mensaje de registro (el exceso se trunca)
   * - ``log.notification.max.details.length``
     - ``3000``
     - Número máximo de caracteres en la sección de detalles del mensaje de notificación

.. note::
   Los cambios en ``log.notification.flush.interval`` se aplican después de reiniciar |Fess|.
   El resto de propiedades se aplican a partir del siguiente ciclo de notificación.

.. note::
   ``log.notification.interval`` es el valor utilizado para el texto "en los últimos N segundos" que se
   muestra dentro del mensaje de notificación, y no modifica la frecuencia de ejecución del trabajo.
   El intervalo real de ejecución lo determina la configuración cron del trabajo programado "Log Notification"
   (por defecto, cada 5 minutos). Si desea cambiar el intervalo de ejecución del trabajo, modifique la expresión
   cron de este trabajo en "Sistema" -> "Programador" y ajuste también ``log.notification.interval`` para que la
   visualización coincida con la realidad.

Formato del Mensaje de Notificación
===================================

Notificación por Correo Electrónico
-----------------------------------

La notificación por correo electrónico se envía con el siguiente formato.

**Asunto:**

::

    [FESS] ERROR Log Alert: hostname

**Cuerpo:**

::

    --- Server Info ---
    Host Name: hostname

    --- Log Summary ---
    Level: ERROR
    Total: 2 event(s) in the last 300 seconds

    --- Log Details ---
    Total: 2 event(s)

    [2025-03-26T10:30:45.123] ERROR org.codelibs.fess.crawler - Connection timeout
    [2025-03-26T10:30:46.456] ERROR org.codelibs.fess.app.web - Failed to process request

    Note: See the log files for full details.

.. note::
   Los eventos ERROR y WARN se envían como notificaciones separadas por cada nivel.

.. note::
   Si el número de eventos a mostrar supera ``log.notification.max.display.events``, el inicio de la
   sección de detalles será ``Total: N event(s) (showing M)`` y al final se añadirá ``... and X more``.
   Cada mensaje de registro que supere ``log.notification.max.message.length`` se trunca al final con ``...``,
   y cuando la sección de detalles completa supera ``log.notification.max.details.length`` el resto se descarta.

Notificación por Slack / Google Chat
------------------------------------

Las notificaciones de Slack y Google Chat también se envían como mensajes con el mismo contenido.

Guía de Operación
=================

Configuración Recomendada
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Entorno
     - Nivel Recomendado
     - Razón
   * - Entorno de Producción
     - ``ERROR``
     - Notificar solo errores importantes y reducir el ruido
   * - Entorno de Staging
     - ``WARN``
     - Notificar incluyendo problemas potenciales
   * - Entorno de Desarrollo
     - Deshabilitado
     - Verificar directamente los archivos de registro

Índice de OpenSearch
--------------------

La funcionalidad de notificación de registros utiliza el índice ``fess_log.notification_queue`` para el almacenamiento
temporal de eventos (el nombre del índice se forma añadiendo ``.notification_queue`` al valor de ``index.log``,
``fess_log`` por defecto). Este índice se crea automáticamente la primera vez que se utiliza la funcionalidad.
Dado que los eventos se eliminan después del envío de la notificación, normalmente el tamaño del índice no crece significativamente.

.. note::
   El número de eventos procesados en una sola ejecución del trabajo tiene como límite ``log.notification.search.size``
   (1,000 eventos por defecto). Los eventos acumulados que superen este límite se descartan en conjunto después del envío
   de la notificación y no se trasladan a las ejecuciones posteriores. En entornos donde se genera una gran cantidad de
   registros en poco tiempo, aumente ``log.notification.search.size`` según sea necesario.

Resolución de Problemas
=======================

Las Notificaciones no se Envían
-------------------------------

1. **Verificar la habilitación**

   Verifique que "Log Notification" esté habilitada en la configuración "General" de la pantalla de administración.

2. **Verificar el destino de notificación**

   Verifique que se haya configurado al menos un destino de notificación ("Correo de notificación",
   "Slack Webhook URLs" o "Google Chat Webhook URLs"). Si ninguno está configurado, el trabajo
   genera ``No notification targets configured.`` y no envía nada.

3. **Verificar la configuración del servidor de correo**

   Si utiliza la notificación por correo electrónico, verifique que el servidor de correo esté
   configurado correctamente en ``fess_env.properties``.

4. **Verificar el trabajo programado**

   Verifique que el trabajo "Log Notification" esté habilitado en "Sistema" -> "Programador".
   Si este trabajo está deshabilitado, no se enviarán notificaciones.

5. **Verificar los registros**

   Verifique los mensajes de error relacionados con la notificación en ``fess.log``.

   ::

       grep -i "notification" /var/log/fess/fess.log

Se Reciben Demasiadas Notificaciones
------------------------------------

1. **Elevar el nivel de registro**

   Cambie el nivel de notificación de ``WARN`` a ``ERROR``.

2. **Resolver la causa raíz**

   Si se producen errores con frecuencia, investigue la causa raíz de los errores.

El Contenido de la Notificación se Trunca
-----------------------------------------

Ajuste las siguientes propiedades.

- ``log.notification.max.details.length``: Número máximo de caracteres en la sección de detalles
- ``log.notification.max.display.events``: Número máximo de eventos a mostrar
- ``log.notification.max.message.length``: Número máximo de caracteres por mensaje

Información de Referencia
=========================

- :doc:`admin-logging` - Configuración de registros
- :doc:`setup-memory` - Configuración de memoria
