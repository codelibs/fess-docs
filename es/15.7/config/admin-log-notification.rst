==========================
Notificacion de Registros
==========================

Descripcion General
===================

|Fess| dispone de una funcionalidad que captura automaticamente los eventos de registro de nivel ERROR o WARN y notifica a los administradores.
Esta funcionalidad permite detectar rapidamente anomalias en el sistema e iniciar la respuesta ante incidencias de forma temprana.

Caracteristicas principales:

- **Canales de notificacion compatibles**: Correo electronico, Slack, Google Chat
- **Procesos objetivo**: Aplicacion principal, rastreador, generacion de sugerencias, generacion de miniaturas
- **Deshabilitado por defecto**: Al ser un sistema de activacion voluntaria (opt-in), es necesario habilitarlo explicitamente

Funcionamiento
==============

La notificacion de registros funciona segun el siguiente flujo.

1. El ``LogNotificationAppender`` de Log4j2 captura los eventos de registro que igualan o superan el nivel configurado.
2. Los eventos capturados se acumulan en un bufer en memoria (maximo 1,000 eventos por defecto). Si el bufer supera su limite, los eventos se descartan empezando por el mas antiguo.
3. Un temporizador escribe los eventos del bufer en un indice de OpenSearch (``fess_log.notification_queue``) cada 30 segundos.
4. El trabajo programado "Log Notification" lee los eventos de OpenSearch cada 5 minutos, los agrupa por nivel de registro y envia una notificacion por cada nivel.
5. Despues del envio de la notificacion, los eventos procesados se eliminan del indice.

.. note::
   Cada nodo notifica unicamente los registros que el mismo ha generado (los eventos se filtran por ``hostname``).
   En una configuracion en cluster, se envia una notificacion individual por cada nodo.

.. note::
   Para evitar bucles infinitos, se excluyen de la notificacion los registros de los loggers
   relacionados con la propia funcionalidad de notificacion
   (``LogNotificationAppender``, ``LogNotificationHelper``, ``LogNotificationTarget``,
   ``LogNotificationJob``, ``NotificationHelper`` y ``org.codelibs.curl``, utilizado para
   la comunicacion HTTP).

Configuracion
=============

Habilitacion
------------

Habilitacion desde la Pantalla de Administracion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Inicie sesion en la pantalla de administracion.
2. Seleccione "General" del menu "Sistema".
3. Active la casilla de verificacion "Log Notification".
4. Seleccione el nivel objetivo de notificacion en "Log Notification Level" (``ERROR``, ``WARN``, ``INFO``, ``DEBUG``, ``TRACE``).
5. Haga clic en el boton "Actualizar".

.. note::
   Por defecto, solo se notifica el nivel ``ERROR``.
   Si selecciona ``WARN``, se notificaran tanto ``WARN`` como ``ERROR``.

Habilitacion mediante Propiedades del Sistema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tambien puede configurar directamente las propiedades del sistema (``system.properties``) que se guardan en la configuracion "General" de la pantalla de administracion.

::

    log.notification.enabled=true
    fess.log.notification.level=ERROR

Configuracion del Destino de Notificacion
-----------------------------------------

Los destinos de notificacion (la direccion de correo, las URL de Webhook de Slack / Google Chat) se configuran todos
en la configuracion "Sistema" -> "General" de la pantalla de administracion. Configure al menos un destino de notificacion.
Si no se ha configurado ningun destino de notificacion, el trabajo de notificacion de registros finaliza sin enviar nada.

Notificacion por Correo Electronico
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para utilizar la notificacion por correo electronico, es necesaria la siguiente configuracion.

1. Configuracion del servidor de correo (``fess_env.properties``):

   ::

       mail.smtp.server.main.host.and.port=smtp.example.com:587

2. Introduzca la direccion de correo electronico en "Correo de notificacion" en la configuracion "General" de la pantalla de administracion.
   Puede especificar varias direcciones separadas por comas.

Notificacion por Slack
~~~~~~~~~~~~~~~~~~~~~~~

Introduzca la URL del Incoming Webhook de Slack en "Slack Webhook URLs" en la configuracion "General" de la pantalla de administracion.
Puede especificar varias URL separadas por comas o espacios.
Este valor se guarda como la propiedad del sistema ``slack.webhook.urls``.

Notificacion por Google Chat
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Introduzca la URL del Webhook de Google Chat en "Google Chat Webhook URLs" en la configuracion "General" de la pantalla de administracion.
Puede especificar varias URL separadas por comas o espacios.
Este valor se guarda como la propiedad del sistema ``google.chat.webhook.urls``.

.. note::
   Si configura unicamente la URL de Webhook de Slack o Google Chat sin configurar "Correo de notificacion",
   no se enviara correo electronico y solo se realizaran las notificaciones a Slack / Google Chat.
   A Slack / Google Chat se les envia como mensaje el mismo asunto y cuerpo que la notificacion por correo.

Propiedades de Configuracion
============================

Las siguientes propiedades se pueden configurar en ``fess_config.properties``.

.. list-table:: Propiedades de Configuracion de Notificacion de Registros
   :header-rows: 1
   :widths: 40 15 45

   * - Propiedad
     - Valor Predeterminado
     - Descripcion
   * - ``log.notification.flush.interval``
     - ``30``
     - Intervalo de vaciado del bufer a OpenSearch (segundos)
   * - ``log.notification.buffer.size``
     - ``1000``
     - Numero maximo de eventos almacenados en el bufer en memoria
   * - ``log.notification.interval``
     - ``300``
     - Periodo de agregacion (segundos) mostrado en el mensaje de notificacion. Es un valor unicamente de visualizacion y no representa el intervalo real de ejecucion del trabajo (vease la nota mas abajo).
   * - ``log.notification.search.size``
     - ``1000``
     - Numero maximo de eventos obtenidos de OpenSearch por ejecucion del trabajo
   * - ``log.notification.max.display.events``
     - ``50``
     - Numero maximo de eventos incluidos en un solo mensaje de notificacion
   * - ``log.notification.max.message.length``
     - ``200``
     - Numero maximo de caracteres por mensaje de registro (el exceso se trunca)
   * - ``log.notification.max.details.length``
     - ``3000``
     - Numero maximo de caracteres en la seccion de detalles del mensaje de notificacion

.. note::
   Los cambios en ``log.notification.flush.interval`` se aplican despues de reiniciar |Fess|.
   El resto de propiedades se aplican a partir del siguiente ciclo de notificacion.

.. note::
   ``log.notification.interval`` es el valor utilizado para el texto "en los ultimos N segundos" que se
   muestra dentro del mensaje de notificacion, y no modifica la frecuencia de ejecucion del trabajo.
   El intervalo real de ejecucion lo determina la configuracion cron del trabajo programado "Log Notification"
   (por defecto, cada 5 minutos). Si desea cambiar el intervalo de ejecucion del trabajo, modifique la expresion
   cron de este trabajo en "Sistema" -> "Programador" y ajuste tambien ``log.notification.interval`` para que la
   visualizacion coincida con la realidad.

Formato del Mensaje de Notificacion
===================================

Notificacion por Correo Electronico
-----------------------------------

La notificacion por correo electronico se envia con el siguiente formato.

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
   Los eventos ERROR y WARN se envian como notificaciones separadas por cada nivel.

.. note::
   Si el numero de eventos a mostrar supera ``log.notification.max.display.events``, el inicio de la
   seccion de detalles sera ``Total: N event(s) (showing M)`` y al final se anadira ``... and X more``.
   Cada mensaje de registro que supere ``log.notification.max.message.length`` se trunca al final con ``...``,
   y cuando la seccion de detalles completa supera ``log.notification.max.details.length`` el resto se descarta.

Notificacion por Slack / Google Chat
------------------------------------

Las notificaciones de Slack y Google Chat tambien se envian como mensajes con el mismo contenido.

Guia de Operacion
=================

Configuracion Recomendada
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Entorno
     - Nivel Recomendado
     - Razon
   * - Entorno de Produccion
     - ``ERROR``
     - Notificar solo errores importantes y reducir el ruido
   * - Entorno de Staging
     - ``WARN``
     - Notificar incluyendo problemas potenciales
   * - Entorno de Desarrollo
     - Deshabilitado
     - Verificar directamente los archivos de registro

Indice de OpenSearch
--------------------

La funcionalidad de notificacion de registros utiliza el indice ``fess_log.notification_queue`` para el almacenamiento
temporal de eventos (el nombre del indice se forma anadiendo ``.notification_queue`` al valor de ``index.log``,
``fess_log`` por defecto). Este indice se crea automaticamente la primera vez que se utiliza la funcionalidad.
Dado que los eventos se eliminan despues del envio de la notificacion, normalmente el tamano del indice no crece significativamente.

.. note::
   El numero de eventos procesados en una sola ejecucion del trabajo tiene como limite ``log.notification.search.size``
   (1,000 eventos por defecto). Los eventos acumulados que superen este limite se descartan en conjunto despues del envio
   de la notificacion y no se trasladan a las ejecuciones posteriores. En entornos donde se genera una gran cantidad de
   registros en poco tiempo, aumente ``log.notification.search.size`` segun sea necesario.

Resolucion de Problemas
=======================

Las Notificaciones no se Envian
-------------------------------

1. **Verificar la habilitacion**

   Verifique que "Log Notification" este habilitada en la configuracion "General" de la pantalla de administracion.

2. **Verificar el destino de notificacion**

   Verifique que se haya configurado al menos un destino de notificacion ("Correo de notificacion",
   "Slack Webhook URLs" o "Google Chat Webhook URLs"). Si ninguno esta configurado, el trabajo
   genera ``No notification targets configured.`` y no envia nada.

3. **Verificar la configuracion del servidor de correo**

   Si utiliza la notificacion por correo electronico, verifique que el servidor de correo este
   configurado correctamente en ``fess_env.properties``.

4. **Verificar el trabajo programado**

   Verifique que el trabajo "Log Notification" este habilitado en "Sistema" -> "Programador".
   Si este trabajo esta deshabilitado, no se enviaran notificaciones.

5. **Verificar los registros**

   Verifique los mensajes de error relacionados con la notificacion en ``fess.log``.

   ::

       grep -i "notification" /var/log/fess/fess.log

Se Reciben Demasiadas Notificaciones
------------------------------------

1. **Elevar el nivel de registro**

   Cambie el nivel de notificacion de ``WARN`` a ``ERROR``.

2. **Resolver la causa raiz**

   Si se producen errores con frecuencia, investigue la causa raiz de los errores.

El Contenido de la Notificacion se Trunca
-----------------------------------------

Ajuste las siguientes propiedades.

- ``log.notification.max.details.length``: Numero maximo de caracteres en la seccion de detalles
- ``log.notification.max.display.events``: Numero maximo de eventos a mostrar
- ``log.notification.max.message.length``: Numero maximo de caracteres por mensaje

Informacion de Referencia
=========================

- :doc:`admin-logging` - Configuracion de registros
- :doc:`setup-memory` - Configuracion de memoria
