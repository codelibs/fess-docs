================
Notificacion de Registros
================

Descripcion General
====================

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
2. Los eventos capturados se acumulan en un bufer en memoria (maximo 1,000 eventos).
3. Un temporizador escribe los eventos del bufer en un indice de OpenSearch (``fess_log.notification_queue``) cada 30 segundos.
4. Un trabajo programado lee los eventos de OpenSearch cada 5 minutos, los agrupa por nivel de registro y envia las notificaciones.
5. Despues del envio de la notificacion, los eventos procesados se eliminan del indice.

.. note::
   Los registros de la propia funcionalidad de notificacion (``LogNotificationHelper``, ``LogNotificationJob``, etc.)
   se excluyen de la notificacion para prevenir bucles infinitos.

Configuracion
=============

Habilitacion
------------

Habilitacion desde la Pantalla de Administracion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Inicie sesion en la pantalla de administracion.
2. Seleccione "General" del menu "Sistema".
3. Active la casilla de verificacion "Notificacion de Registros".
4. Seleccione el nivel objetivo de notificacion en "Nivel de Notificacion de Registros" (``ERROR``, ``WARN``, ``INFO``, ``DEBUG``, ``TRACE``).
5. Haga clic en el boton "Actualizar".

.. note::
   Por defecto, solo se notifica el nivel ``ERROR``.
   Si selecciona ``WARN``, se notificaran tanto ``WARN`` como ``ERROR``.

Habilitacion mediante Propiedades del Sistema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tambien puede habilitar la funcionalidad configurando directamente las propiedades del sistema que se guardan en la configuracion "General" de la pantalla de administracion.

::

    log.notification.enabled=true
    fess.log.notification.level=ERROR

Configuracion del Destino de Notificacion
------------------------------------------

Notificacion por Correo Electronico
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para utilizar la notificacion por correo electronico, es necesaria la siguiente configuracion.

1. Configuracion del servidor de correo (``fess_env.properties``):

   ::

       mail.smtp.server.main.host.and.port=smtp.example.com:587

2. Introduzca la direccion de correo electronico en "Destino de Notificacion" en la configuracion "General" de la pantalla de administracion. Puede especificar varias direcciones separadas por comas.

Notificacion por Slack
~~~~~~~~~~~~~~~~~~~~~~

Puede enviar notificaciones a un canal de Slack configurando la URL del Incoming Webhook de Slack.

Notificacion por Google Chat
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Puede enviar notificaciones a un espacio de Google Chat configurando la URL del Webhook de Google Chat.

Propiedades de Configuracion
=============================

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
     - Intervalo de ejecucion del trabajo de notificacion (segundos)
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
   Los cambios en estas propiedades se aplican despues de reiniciar |Fess|.

Formato del Mensaje de Notificacion
=====================================

Notificacion por Correo Electronico
------------------------------------

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
    Total: 5 event(s) in the last 300 seconds

    --- Log Details ---
    [2025-03-26T10:30:45.123] ERROR org.codelibs.fess.crawler - Connection timeout
    [2025-03-26T10:30:46.456] ERROR org.codelibs.fess.app.web - Failed to process request

    Note: See the log files for full details.

.. note::
   Los eventos ERROR y WARN se envian como notificaciones separadas por cada nivel.

Notificacion por Slack / Google Chat
-------------------------------------

Las notificaciones de Slack y Google Chat tambien se envian como mensajes con el mismo contenido.

Guia de Operacion
==================

Configuracion Recomendada
--------------------------

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
---------------------

La funcionalidad de notificacion de registros utiliza el indice ``fess_log.notification_queue`` para el almacenamiento temporal de eventos.
Este indice se crea automaticamente la primera vez que se utiliza la funcionalidad.
Dado que los eventos se eliminan despues del envio de la notificacion, normalmente el tamano del indice no crece significativamente.

Resolucion de Problemas
=========================

Las Notificaciones no se Envian
--------------------------------

1. **Verificar la habilitacion**

   Verifique que "Notificacion de Registros" este habilitada en la configuracion "General" de la pantalla de administracion.

2. **Verificar el destino de notificacion**

   En el caso de notificacion por correo electronico, verifique que se haya configurado una direccion de correo electronico en "Destino de Notificacion".

3. **Verificar la configuracion del servidor de correo**

   Verifique que el servidor de correo este configurado correctamente en ``fess_env.properties``.

4. **Verificar los registros**

   Verifique los mensajes de error relacionados con la notificacion en ``fess.log``.

   ::

       grep -i "notification" /var/log/fess/fess.log

Se Reciben Demasiadas Notificaciones
--------------------------------------

1. **Elevar el nivel de registro**

   Cambie el nivel de notificacion de ``WARN`` a ``ERROR``.

2. **Resolver la causa raiz**

   Si se producen errores con frecuencia, investigue la causa raiz de los errores.

El Contenido de la Notificacion se Trunca
-------------------------------------------

Ajuste las siguientes propiedades.

- ``log.notification.max.details.length``: Numero maximo de caracteres en la seccion de detalles
- ``log.notification.max.display.events``: Numero maximo de eventos a mostrar
- ``log.notification.max.message.length``: Numero maximo de caracteres por mensaje

Informacion de Referencia
==========================

- :doc:`admin-logging` - Configuracion de registros
- :doc:`setup-memory` - Configuracion de memoria
