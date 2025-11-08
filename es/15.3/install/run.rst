====================================
Inicio, Detención y Configuración Inicial
====================================

Esta página describe los procedimientos de inicio, detención y configuración inicial del servidor |Fess|.

.. important::

   Antes de iniciar |Fess|, asegúrese de iniciar OpenSearch.
   Si OpenSearch no está en ejecución, |Fess| no funcionará correctamente.

Métodos de Inicio
==================

Los procedimientos de inicio varían según el método de instalación.

En Caso de Versión TAR.GZ
--------------------------

Inicio de OpenSearch
~~~~~~~~~~~~~~~~~~~~

::

    $ cd /path/to/opensearch-3.3.2
    $ ./bin/opensearch

Para iniciar en segundo plano::

    $ ./bin/opensearch -d

Inicio de Fess
~~~~~~~~~~~~~~

::

    $ cd /path/to/fess-15.3.2
    $ ./bin/fess

Para iniciar en segundo plano::

    $ ./bin/fess -d

.. note::

   El inicio puede tardar varios minutos.
   Puede verificar el estado de inicio en el archivo de registro (``logs/fess.log``).

En Caso de Versión ZIP (Windows)
---------------------------------

Inicio de OpenSearch
~~~~~~~~~~~~~~~~~~~~

1. Abra el directorio de instalación de OpenSearch
2. Haga doble clic en ``opensearch.bat`` dentro de la carpeta ``bin``

O desde el Símbolo del sistema::

    C:\> cd C:\opensearch-3.3.2
    C:\opensearch-3.3.2> bin\opensearch.bat

Inicio de Fess
~~~~~~~~~~~~~~

1. Abra el directorio de instalación de Fess
2. Haga doble clic en ``fess.bat`` dentro de la carpeta ``bin``

O desde el Símbolo del sistema::

    C:\> cd C:\fess-15.3.2
    C:\fess-15.3.2> bin\fess.bat

En Caso de Versión RPM/DEB (chkconfig)
---------------------------------------

Inicio de OpenSearch::

    $ sudo service opensearch start

Inicio de Fess::

    $ sudo service fess start

Verificación del estado de inicio::

    $ sudo service fess status

En Caso de Versión RPM/DEB (systemd)
-------------------------------------

Inicio de OpenSearch::

    $ sudo systemctl start opensearch.service

Inicio de Fess::

    $ sudo systemctl start fess.service

Verificación del estado de inicio::

    $ sudo systemctl status fess.service

Habilitar inicio automático del servicio::

    $ sudo systemctl enable opensearch.service
    $ sudo systemctl enable fess.service

En Caso de Versión Docker
--------------------------

Iniciar usando Docker Compose::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Verificación del estado de inicio::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

Verificación de registros::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess

Verificación del Inicio
========================

Verifique que |Fess| se haya iniciado normalmente.

Verificación de Salud
---------------------

Acceda a la siguiente URL desde un navegador o usando el comando curl::

    http://localhost:8080/

Si se ha iniciado normalmente, se mostrará la pantalla de búsqueda de Fess.

Verificación desde la línea de comandos::

    $ curl -I http://localhost:8080/

Si devuelve ``HTTP/1.1 200 OK``, se ha iniciado normalmente.

Verificación de Registros
--------------------------

Verifique el registro de inicio para confirmar que no hay errores.

Para versiones TAR.GZ/ZIP::

    $ tail -f /path/to/fess-15.3.2/logs/fess.log

Para versiones RPM/DEB::

    $ sudo tail -f /var/log/fess/fess.log

O usando journalctl::

    $ sudo journalctl -u fess.service -f

Para versión Docker::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess

.. tip::

   Si se inició normalmente, aparecerá un mensaje como el siguiente en el registro::

       INFO  Boot - Fess is ready.

Acceso desde el Navegador
==========================

Acceda a la interfaz Web visitando las siguientes URL.

Pantalla de Búsqueda
---------------------

**URL**: http://localhost:8080/

Se mostrará la pantalla de búsqueda de Fess. En el estado inicial, como no se ha realizado ninguna configuración de rastreo, no se mostrarán resultados de búsqueda.

Pantalla de Administración
---------------------------

**URL**: http://localhost:8080/admin

Cuenta de administrador predeterminada:

- **Nombre de usuario**: ``admin``
- **Contraseña**: ``admin``

.. warning::

   **Nota Importante sobre Seguridad**

   Asegúrese de cambiar la contraseña predeterminada.
   Especialmente en entornos de producción, se recomienda encarecidamente cambiar la contraseña inmediatamente después del primer inicio de sesión.

Configuración Inicial
=====================

Después de iniciar sesión en la pantalla de administración, realice la siguiente configuración inicial.

Paso 1: Cambio de Contraseña de Administrador
----------------------------------------------

1. Inicie sesión en la pantalla de administración (http://localhost:8080/admin)
2. Haga clic en "Sistema" → "Usuario" en el menú izquierdo
3. Haga clic en el usuario ``admin``
4. Ingrese una nueva contraseña en el campo "Contraseña"
5. Haga clic en el botón "Confirmar"
6. Haga clic en el botón "Actualizar"

.. important::

   Se recomienda que la contraseña cumpla con las siguientes condiciones:

   - 8 caracteres o más
   - Combinar letras mayúsculas, minúsculas, números y símbolos
   - Difícil de adivinar

Paso 2: Creación de Configuración de Rastreo
---------------------------------------------

Cree una configuración para rastrear sitios o sistemas de archivos que desee buscar.

1. Haga clic en "Rastreador" → "Web" en el menú izquierdo
2. Haga clic en el botón "Crear nuevo"
3. Ingrese la información necesaria:

   - **Nombre**: Nombre de la configuración de rastreo (ejemplo: Sitio web de la empresa)
   - **URL**: URL del objetivo de rastreo (ejemplo: https://www.example.com/)
   - **Número máximo de accesos**: Límite superior del número de páginas a rastrear
   - **Intervalo**: Intervalo de rastreo (milisegundos)

4. Haga clic en el botón "Crear"

Paso 3: Ejecución del Rastreo
------------------------------

1. Haga clic en "Sistema" → "Programador" en el menú izquierdo
2. Haga clic en el botón "Iniciar ahora" del trabajo "Default Crawler"
3. Espere hasta que se complete el rastreo (puede verificar el progreso en el panel de control)

Paso 4: Verificación de la Búsqueda
------------------------------------

1. Acceda a la pantalla de búsqueda (http://localhost:8080/)
2. Ingrese una palabra clave de búsqueda
3. Verifique que se muestren los resultados de búsqueda

.. note::

   El rastreo puede tardar tiempo.
   Para sitios grandes, puede tardar desde varias horas hasta varios días.

Otras Configuraciones Recomendadas
===================================

Si va a operar en un entorno de producción, considere también las siguientes configuraciones.

Configuración del Servidor de Correo
-------------------------------------

Configure un servidor de correo para recibir notificaciones de fallos e informes por correo electrónico.

1. Haga clic en "Sistema" → "General" en el menú izquierdo
2. Haga clic en la pestaña "Correo"
3. Ingrese la información del servidor SMTP
4. Haga clic en el botón "Actualizar"

Configuración de Zona Horaria
------------------------------

1. Haga clic en "Sistema" → "General" en el menú izquierdo
2. Configure "Zona horaria" al valor apropiado (ejemplo: Asia/Tokyo)
3. Haga clic en el botón "Actualizar"

Ajuste del Nivel de Registro
-----------------------------

En entornos de producción, puede ajustar el nivel de registro para reducir el uso de disco.

Edite el archivo de configuración (``app/WEB-INF/classes/log4j2.xml``).

Para más detalles, consulte la guía del administrador.

Métodos de Detención
=====================

En Caso de Versión TAR.GZ/ZIP
------------------------------

Detención de Fess
~~~~~~~~~~~~~~~~~

Elimine el proceso::

    $ ps aux | grep fess
    $ kill <PID>

O puede detenerlo con ``Ctrl+C`` desde la consola (si está ejecutándose en primer plano).

Detención de OpenSearch::

    $ ps aux | grep opensearch
    $ kill <PID>

En Caso de Versión RPM/DEB (chkconfig)
---------------------------------------

Detención de Fess::

    $ sudo service fess stop

Detención de OpenSearch::

    $ sudo service opensearch stop

En Caso de Versión RPM/DEB (systemd)
-------------------------------------

Detención de Fess::

    $ sudo systemctl stop fess.service

Detención de OpenSearch::

    $ sudo systemctl stop opensearch.service

En Caso de Versión Docker
--------------------------

Detención de contenedores::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop

Detención y eliminación de contenedores::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   Agregue la opción ``-v`` al comando ``down`` si también desea eliminar los volúmenes.
   En este caso, tenga cuidado ya que se eliminarán todos los datos.

Métodos de Reinicio
====================

En Caso de Versión TAR.GZ/ZIP
------------------------------

Detenga y luego inicie.

En Caso de Versión RPM/DEB
---------------------------

Con chkconfig::

    $ sudo service fess restart

Con systemd::

    $ sudo systemctl restart fess.service

En Caso de Versión Docker
--------------------------

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml restart

Solución de Problemas
======================

Si no Inicia
------------

1. **Verificar que OpenSearch esté en ejecución**

   ::

       $ curl http://localhost:9200/

   Si OpenSearch no está en ejecución, primero inicie OpenSearch.

2. **Verificar conflictos de números de puerto**

   ::

       $ sudo netstat -tuln | grep 8080

   Si el puerto 8080 ya está en uso, cambie el número de puerto en el archivo de configuración.

3. **Verificar registros**

   Verifique los mensajes de error para identificar el problema.

4. **Verificar versión de Java**

   ::

       $ java -version

   Verifique que esté instalado Java 21 o posterior.

Para solución de problemas detallada, consulte :doc:`troubleshooting`.

Próximos Pasos
==============

Una vez que |Fess| se haya iniciado normalmente, consulte la siguiente documentación para comenzar la operación:

- **Guía del Administrador**: Detalles sobre configuración de rastreo, configuración de búsqueda y configuración del sistema
- :doc:`security` - Configuración de seguridad para entornos de producción
- :doc:`troubleshooting` - Problemas comunes y soluciones
- :doc:`upgrade` - Procedimientos de actualización de versión
- :doc:`uninstall` - Procedimientos de desinstalación
