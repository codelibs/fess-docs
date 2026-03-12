========================
Configuración de Registro
========================

Descripción General
===================

|Fess| genera múltiples archivos de registro para registrar el estado de funcionamiento del sistema y la información de errores.
Una configuración de registro adecuada facilita la resolución de problemas y la supervisión del sistema.

Tipos de Archivos de Registro
==============================

Archivos de Registro Principales
---------------------------------

Los principales archivos de registro generados por |Fess| son los siguientes:

.. list-table:: Lista de Archivos de Registro
   :header-rows: 1
   :widths: 25 75

   * - Nombre del Archivo
     - Contenido
   * - ``fess.log``
     - Registros de operaciones en la pantalla de administración y búsqueda, errores de aplicación y eventos del sistema
   * - ``fess_crawler.log``
     - Registros de ejecución de rastreo, URLs rastreadas, información de documentos obtenidos y errores
   * - ``fess_suggest.log``
     - Registros de generación de sugerencias (candidatos de búsqueda) e información de actualización de índices
   * - ``server_?.log``
     - Registros del sistema del servidor de aplicaciones como Tomcat
   * - ``audit.log``
     - Registros de auditoría de autenticación de usuarios, inicio/cierre de sesión y operaciones importantes

Ubicación de los Archivos de Registro
--------------------------------------

**En caso de instalación ZIP:**

::

    {FESS_HOME}/logs/

**En caso de paquetes RPM/DEB:**

::

    /var/log/fess/

Verificación de Registros para Resolución de Problemas
-------------------------------------------------------

Cuando ocurra un problema, verifique los registros siguiendo estos pasos:

1. **Identificar el tipo de error**

   - Error de aplicación → ``fess.log``
   - Error de rastreo → ``fess_crawler.log``
   - Error de autenticación → ``audit.log``
   - Error del servidor → ``server_?.log``

2. **Verificar los errores más recientes**

   ::

       tail -f /var/log/fess/fess.log

3. **Buscar errores específicos**

   ::

       grep -i "error" /var/log/fess/fess.log
       grep -i "exception" /var/log/fess/fess.log

4. **Verificar el contexto del error**

   Puede identificar la causa verificando los registros antes y después de que ocurra el error.

   ::

       grep -B 10 -A 10 "OutOfMemoryError" /var/log/fess/fess.log

Configuración de Niveles de Registro
=====================================

¿Qué son los Niveles de Registro?
----------------------------------

Los niveles de registro controlan el nivel de detalle de los registros generados.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Nivel
     - Descripción
   * - ``FATAL``
     - Error fatal (la aplicación no puede continuar)
   * - ``ERROR``
     - Error (parte de la funcionalidad no funciona)
   * - ``WARN``
     - Advertencia (problema potencial)
   * - ``INFO``
     - Información (eventos importantes)
   * - ``DEBUG``
     - Información de depuración (registro detallado de operaciones)
   * - ``TRACE``
     - Información de traza (el más detallado)

Niveles de Registro Recomendados
---------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Entorno
     - Nivel Recomendado
     - Razón
   * - Entorno de Producción
     - ``WARN``
     - Prioriza el rendimiento y el espacio en disco
   * - Entorno de Staging
     - ``INFO``
     - Registra eventos importantes
   * - Entorno de Desarrollo
     - ``DEBUG``
     - Se necesita información detallada de depuración
   * - Investigación de Problemas
     - ``DEBUG`` o ``TRACE``
     - Habilita temporalmente registros detallados

Cambios desde la Pantalla de Administración
--------------------------------------------

La forma más sencilla es cambiar desde la pantalla de administración.

1. Inicie sesión en la pantalla de administración.
2. Seleccione "General" del menú "Sistema".
3. Seleccione el nivel deseado en "Nivel de Registro".
4. Haga clic en el botón "Actualizar".

.. note::
   Los cambios realizados desde la pantalla de administración se conservan incluso después de reiniciar |Fess|.

Cambios mediante Archivo de Configuración
------------------------------------------

Para realizar una configuración de registro más detallada, edite el archivo de configuración de Log4j2.

Ubicación del Archivo de Configuración
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Instalación ZIP**: ``app/WEB-INF/classes/log4j2.xml``
- **Paquetes RPM/DEB**: ``/etc/fess/log4j2.xml``

Ejemplos de Configuración Básica
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Nivel de registro predeterminado:**

::

    <Logger name="org.codelibs.fess" level="warn"/>

**Ejemplo: Cambiar al nivel DEBUG**

::

    <Logger name="org.codelibs.fess" level="debug"/>

**Ejemplo: Cambiar el nivel de registro de paquetes específicos**

::

    <Logger name="org.codelibs.fess.crawler" level="info"/>
    <Logger name="org.codelibs.fess.ds" level="debug"/>
    <Logger name="org.codelibs.fess.app.web" level="warn"/>

.. warning::
   Los niveles ``DEBUG`` y ``TRACE`` generan una gran cantidad de registros,
   por lo que no deben utilizarse en entornos de producción. Afectan al espacio en disco y al rendimiento.

Configuración mediante Variables de Entorno
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

También puede especificar el nivel de registro al iniciar el sistema.

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dlog.level=debug"

Configuración de Registros del Rastreador
==========================================

Los registros del rastreador se generan de forma predeterminada en el nivel ``INFO``.

Configuración desde la Pantalla de Administración
--------------------------------------------------

1. Abra la configuración de rastreo objetivo desde el menú "Rastreador" de la pantalla de administración.
2. Seleccione "Script" en la pestaña "Configuración".
3. Agregue lo siguiente en el campo de script:

::

    logLevel("DEBUG")

Valores configurables:

- ``FATAL``
- ``ERROR``
- ``WARN``
- ``INFO``
- ``DEBUG``
- ``TRACE``

Cambiar el Nivel de Registro Solo para Patrones de URL Específicos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    if (url.contains("example.com")) {
        logLevel("DEBUG")
    }

Cambiar el Nivel de Registro de Todo el Proceso del Rastreador
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure en ``fess_config.properties``:

::

    logging.level.org.codelibs.fess.crawler=DEBUG

Rotación de Registros
======================

Descripción General
-------------------

Los archivos de registro crecen con el tiempo, por lo que es necesaria una rotación periódica (gestión generacional).

Rotación Automática mediante Log4j2
------------------------------------

|Fess| utiliza el RollingFileAppender de Log4j2 para realizar automáticamente la rotación de registros.

Configuración Predeterminada
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Tamaño de archivo**: Rotación cuando se superan los 10MB
- **Número de generaciones conservadas**: Máximo 10 archivos

Ejemplo de archivo de configuración (``log4j2.xml``):

::

    <RollingFile name="FessFile"
                 fileName="${log.dir}/fess.log"
                 filePattern="${log.dir}/fess.log.%i">
        <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n"/>
        <Policies>
            <SizeBasedTriggeringPolicy size="10MB"/>
        </Policies>
        <DefaultRolloverStrategy max="10"/>
    </RollingFile>

Configuración de Rotación Diaria
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para rotar diariamente en lugar de por tamaño:

::

    <RollingFile name="FessFile"
                 fileName="${log.dir}/fess.log"
                 filePattern="${log.dir}/fess.log.%d{yyyy-MM-dd}">
        <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n"/>
        <Policies>
            <TimeBasedTriggeringPolicy interval="1" modulate="true"/>
        </Policies>
        <DefaultRolloverStrategy max="30"/>
    </RollingFile>

Configuración de Compresión
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para comprimir automáticamente durante la rotación:

::

    <RollingFile name="FessFile"
                 fileName="${log.dir}/fess.log"
                 filePattern="${log.dir}/fess.log.%d{yyyy-MM-dd}.gz">
        <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n"/>
        <Policies>
            <TimeBasedTriggeringPolicy interval="1" modulate="true"/>
        </Policies>
        <DefaultRolloverStrategy max="30"/>
    </RollingFile>

Rotación mediante logrotate
----------------------------

En entornos Linux, también puede gestionar la rotación de registros usando logrotate.

Ejemplo de ``/etc/logrotate.d/fess``:

::

    /var/log/fess/*.log {
        daily
        rotate 14
        compress
        delaycompress
        missingok
        notifempty
        create 0644 fess fess
        sharedscripts
        postrotate
            systemctl reload fess > /dev/null 2>&1 || true
        endscript
    }

Explicación de la configuración:

- ``daily``: Rotación diaria
- ``rotate 14``: Conservar 14 generaciones
- ``compress``: Comprimir registros antiguos
- ``delaycompress``: No comprimir el registro de la generación anterior (la aplicación puede estar escribiendo)
- ``missingok``: No generar error si no existe el archivo de registro
- ``notifempty``: No rotar archivos de registro vacíos
- ``create 0644 fess fess``: Permisos y propietario del nuevo archivo de registro

Supervisión de Registros
=========================

En entornos de producción, se recomienda supervisar los archivos de registro para detectar errores de forma temprana.

Patrones de Registro que Deben Supervisarse
--------------------------------------------

Patrones de Error Importantes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Registros de nivel ``ERROR`` y ``FATAL``
- ``OutOfMemoryError``
- ``Connection refused``
- ``Timeout``
- ``Exception``
- ``circuit_breaker_exception``
- ``Too many open files``

Patrones que Deben Generar Advertencias
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Registros de nivel ``WARN`` frecuentes
- ``Retrying``
- ``Slow query``
- ``Queue full``

Supervisión en Tiempo Real
---------------------------

Supervisión en tiempo real con el comando tail:

::

    tail -f /var/log/fess/fess.log | grep -i "error\|exception"

Supervisión simultánea de múltiples archivos de registro:

::

    tail -f /var/log/fess/*.log

Ejemplos de Herramientas de Supervisión
----------------------------------------

**Logwatch**

Análisis periódico de archivos de registro e informes.

::

    # Instalación (CentOS/RHEL)
    yum install logwatch

    # Envío de informe diario
    logwatch --service fess --mailto admin@example.com

**Logstash + OpenSearch + OpenSearch Dashboards**

Análisis de registros en tiempo real y visualización.

**Fluentd**

Recopilación y transferencia de registros.

::

    <source>
      @type tail
      path /var/log/fess/fess.log
      pos_file /var/log/fluentd/fess.log.pos
      tag fess.app
      <parse>
        @type multiline
        format_firstline /^\d{4}-\d{2}-\d{2}/
        format1 /^(?<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) \[(?<thread>.*?)\] (?<level>\w+)\s+(?<logger>.*?) - (?<message>.*)/
      </parse>
    </source>

**Prometheus + Grafana**

Supervisión de métricas y alertas.

Configuración de Alertas
-------------------------

Ejemplo de notificación al detectar errores:

::

    # Script simple de notificación por correo electrónico
    tail -n 0 -f /var/log/fess/fess.log | while read line; do
        echo "$line" | grep -i "error\|fatal" && \
        echo "$line" | mail -s "Fess Error Alert" admin@example.com
    done

Formato de Registro
====================

Formato Predeterminado
-----------------------

Formato de registro predeterminado de |Fess|:

::

    %d{ISO8601} [%t] %-5p %c - %m%n

Explicación de cada elemento:

- ``%d{ISO8601}``: Marca de tiempo (formato ISO8601)
- ``[%t]``: Nombre del hilo
- ``%-5p``: Nivel de registro (ancho de 5 caracteres, alineado a la izquierda)
- ``%c``: Nombre del registrador (nombre del paquete)
- ``%m``: Mensaje
- ``%n``: Salto de línea

Ejemplos de Formato Personalizado
----------------------------------

Salida de Registro en Formato JSON
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    <PatternLayout>
        <pattern>{"timestamp":"%d{ISO8601}","thread":"%t","level":"%-5p","logger":"%c","message":"%m"}%n</pattern>
    </PatternLayout>

Incluir Información Más Detallada
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c{1.} [%F:%L] - %m%n"/>

Información adicional:

- ``%c{1.}``: Nombre de paquete abreviado
- ``%F``: Nombre del archivo
- ``%L``: Número de línea

Impacto en el Rendimiento
==========================

La salida de registros afecta al I/O del disco y al rendimiento.

Mejores Prácticas
-----------------

1. **Usar nivel WARN o superior en entornos de producción**

   Evite generar registros detallados innecesarios.

2. **Limpieza periódica de archivos de registro**

   Elimine o comprima archivos de registro antiguos.

3. **Uso de salida de registros asíncrona**

   Utilice el appender asíncrono de Log4j2 para reducir la sobrecarga de la salida de registros.

   ::

       <Async name="AsyncFile">
           <AppenderRef ref="FessFile"/>
       </Async>

4. **Asegurar espacio en disco adecuado**

   Asegure suficiente espacio en disco para los archivos de registro.

5. **Selección adecuada del nivel de registro**

   Configure el nivel de registro según el entorno.

Medición del Rendimiento
-------------------------

Medir el impacto de la salida de registros:

::

    # Verificar la cantidad de salida de registros
    du -sh /var/log/fess/

    # Aumento de registros por hora
    watch -n 3600 'du -sh /var/log/fess/'

Resolución de Problemas
========================

Los Registros no se Generan
----------------------------

**Causas y soluciones:**

1. **Permisos del directorio de registros**

   ::

       ls -ld /var/log/fess/
       # Cambiar permisos si es necesario
       sudo chown -R fess:fess /var/log/fess/
       sudo chmod 755 /var/log/fess/

2. **Espacio en disco**

   ::

       df -h /var/log
       # Si no hay espacio suficiente, eliminar registros antiguos
       find /var/log/fess/ -name "*.log.*" -mtime +30 -delete

3. **Archivo de configuración Log4j2**

   ::

       # Verificar sintaxis del archivo de configuración
       xmllint --noout /etc/fess/log4j2.xml

4. **Verificación de SELinux**

   ::

       # Si SELinux está habilitado
       getenforce
       # Configurar el contexto si es necesario
       restorecon -R /var/log/fess/

Los Archivos de Registro se Hacen Demasiado Grandes
----------------------------------------------------

1. **Ajustar el nivel de registro**

   Configure a ``WARN`` o superior.

2. **Verificar la configuración de rotación de registros**

   ::

       # Verificar configuración de log4j2.xml
       grep -A 5 "RollingFile" /etc/fess/log4j2.xml

3. **Deshabilitar salida de registros innecesaria**

   ::

       # Suprimir registros de paquetes específicos
       <Logger name="org.apache.http" level="error"/>

4. **Medidas temporales**

   ::

       # Comprimir archivos de registro antiguos
       gzip /var/log/fess/fess.log.[1-9]

       # Eliminar archivos de registro antiguos
       find /var/log/fess/ -name "*.log.*" -mtime +7 -delete

No se Encuentra un Registro Específico
---------------------------------------

1. **Verificar el nivel de registro**

   No se generará si el nivel de registro es demasiado bajo.

   ::

       grep "org.codelibs.fess" /etc/fess/log4j2.xml

2. **Verificar la ruta del archivo de registro**

   ::

       # Verificar el destino de salida real del registro
       ps aux | grep fess
       lsof -p <PID> | grep log

3. **Verificar la marca de tiempo**

   Verifique que la hora del sistema sea correcta.

   ::

       date
       timedatectl status

4. **Almacenamiento en búfer de registros**

   Los registros pueden no escribirse inmediatamente.

   ::

       # Forzar el vaciado de registros
       systemctl reload fess

Aparecen Caracteres Corruptos en el Registro
---------------------------------------------

1. **Configuración de codificación**

   Especifique la codificación de caracteres en ``log4j2.xml``:

   ::

       <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n" charset="UTF-8"/>

2. **Configuración de variables de entorno**

   ::

       export LANG=ja_JP.UTF-8
       export LC_ALL=ja_JP.UTF-8

Información de Referencia
==========================

- :doc:`setup-memory` - Configuración de memoria
- :doc:`crawler-advanced` - Configuración avanzada del rastreador
- :doc:`admin-index-backup` - Copia de seguridad de índices
- `Log4j2 Documentation <https://logging.apache.org/log4j/2.x/>`_
