=======================
Solución de Problemas
=======================

Esta página describe los problemas comunes y sus soluciones durante la instalación, inicio y operación de |Fess|.

Problemas Durante la Instalación
=================================

Java no Reconocido
------------------

**Síntoma:**

::

    -bash: java: command not found

O::

    'java' is not recognized as an internal or external command

**Causa:**

Java no está instalado, o la variable de entorno PATH no está configurada correctamente.

**Solución:**

1. Verificar si Java está instalado::

       $ which java
       $ java -version

2. Si no está instalado, instale Java 21::

       # Ubuntu/Debian
       $ sudo apt-get update
       $ sudo apt-get install openjdk-21-jdk

       # RHEL/CentOS
       $ sudo yum install java-21-openjdk

3. Configure la variable de entorno JAVA_HOME::

       $ export JAVA_HOME=/path/to/java
       $ export PATH=$JAVA_HOME/bin:$PATH

   Para configurar permanentemente, agregue a ``~/.bashrc`` o ``/etc/profile``.

Falla la Instalación de Plugin
-------------------------------

**Síntoma:**

::

    ERROR: Plugin installation failed

**Causa:**

- Problema de conexión de red
- La versión del plugin no coincide con la versión de OpenSearch
- Problema de permisos

**Solución:**

1. Verificar la versión de OpenSearch::

       $ /path/to/opensearch/bin/opensearch --version

2. Hacer coincidir la versión del plugin con la versión de OpenSearch::

       $ /path/to/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.0

3. Verificar permisos::

       $ sudo /path/to/opensearch/bin/opensearch-plugin install ...

4. Para instalar a través de proxy::

       $ export ES_JAVA_OPTS="-Dhttp.proxyHost=proxy.example.com -Dhttp.proxyPort=8080"
       $ /path/to/opensearch/bin/opensearch-plugin install ...

Problemas Durante el Inicio
============================

Fess no Inicia
--------------

**Síntoma:**

Aparece un error al ejecutar el comando de inicio de Fess, o termina inmediatamente.

**Elementos a Verificar:**

1. **Verificar que OpenSearch esté en ejecución**::

       $ curl http://localhost:9200/

   Si es normal, se devuelve una respuesta JSON.

2. **Verificar conflicto de número de puerto**::

       $ sudo netstat -tuln | grep 8080

   Si el puerto 8080 ya está en uso, cambie el número de puerto en el archivo de configuración.

3. **Verificar archivo de registro**::

       $ tail -f /path/to/fess/logs/fess.log

   Identifique la causa a partir de los mensajes de error.

4. **Verificar versión de Java**::

       $ java -version

   Verifique que esté instalado Java 21 o posterior.

5. **Verificar falta de memoria**::

       $ free -h

   Si falta memoria, ajuste el tamaño del heap o expanda la memoria del sistema.

OpenSearch no Inicia
---------------------

**Síntoma:**

::

    ERROR: bootstrap checks failed

**Causa:**

La configuración del sistema no cumple con los requisitos de OpenSearch.

**Solución:**

1. **Configuración de vm.max_map_count**::

       $ sudo sysctl -w vm.max_map_count=262144

   Para configurar permanentemente::

       $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
       $ sudo sysctl -p

2. **Aumentar el límite de descriptores de archivo**::

       $ sudo vi /etc/security/limits.conf

   Agregue lo siguiente::

       opensearch  -  nofile  65535
       opensearch  -  nproc   4096

3. **Configuración de bloqueo de memoria**::

       $ sudo vi /etc/security/limits.conf

   Agregue lo siguiente::

       opensearch  -  memlock  unlimited

4. Reinicie OpenSearch::

       $ sudo systemctl restart opensearch

Conflicto de Número de Puerto
------------------------------

**Síntoma:**

::

    Address already in use

**Solución:**

1. Verificar puerto en uso::

       $ sudo netstat -tuln | grep 8080
       $ sudo lsof -i :8080

2. Detenga el proceso en uso, o cambie el número de puerto de Fess

   Cambie el número de puerto en el archivo de configuración (``system.properties``)::

       server.port=9080

Problemas de Conexión
======================

Fess no Puede Conectarse a OpenSearch
--------------------------------------

**Síntoma:**

Aparecen errores como los siguientes en el registro::

    Connection refused
    o
    No route to host

**Solución:**

1. **Verificar que OpenSearch esté en ejecución**::

       $ curl http://localhost:9200/

2. **Verificar URL de conexión**

   Verifique que la URL configurada en ``fess.in.sh`` o ``fess.in.bat`` sea correcta::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200

3. **Verificar cortafuegos**::

       $ sudo firewall-cmd --list-all

   Verifique que el puerto 9200 esté abierto.

4. **Verificar conexión de red**

   Si ejecuta OpenSearch en otro host::

       $ ping opensearch-host
       $ telnet opensearch-host 9200

No se Puede Acceder a Fess desde el Navegador
----------------------------------------------

**Síntoma:**

No se puede acceder a http://localhost:8080/ desde el navegador.

**Solución:**

1. **Verificar que Fess esté en ejecución**::

       $ ps aux | grep fess

2. **Intentar acceso en localhost**::

       $ curl http://localhost:8080/

3. **Verificar cortafuegos**::

       $ sudo firewall-cmd --list-all

   Verifique que el puerto 8080 esté abierto.

4. **Al acceder desde otro host**

   Verifique que Fess esté escuchando en algo distinto de localhost::

       $ netstat -tuln | grep 8080

   Si es ``127.0.0.1:8080``, cambie la configuración para escuchar en ``0.0.0.0:8080`` o una dirección IP específica.

Problemas de Rendimiento
=========================

La Búsqueda es Lenta
--------------------

**Causa:**

- El tamaño del índice es grande
- Falta de memoria
- E/S de disco lenta
- Consulta compleja

**Solución:**

1. **Aumentar tamaño del heap**

   Edite ``fess.in.sh``::

       FESS_HEAP_SIZE=4g

   Ajuste también el tamaño del heap de OpenSearch::

       export OPENSEARCH_JAVA_OPTS="-Xms4g -Xmx4g"

2. **Optimización del índice**

   Ejecute periódicamente la optimización desde la pantalla de administración en "Sistema" → "Programador".

3. **Usar SSD**

   Si la E/S de disco es un cuello de botella, migre a SSD.

4. **Habilitar caché**

   Habilite la caché de consultas en el archivo de configuración.

El Rastreo es Lento
-------------------

**Causa:**

- Intervalo de rastreo largo
- Respuesta lenta del sitio objetivo
- Número reducido de hilos

**Solución:**

1. **Ajustar intervalo de rastreo**

   Acorte el "Intervalo" de la configuración de rastreo en la pantalla de administración (en milisegundos).

   .. warning::

      Si el intervalo es demasiado corto, pondrá carga en el sitio objetivo. Configure un valor apropiado.

2. **Aumentar número de hilos**

   Aumente el número de hilos de rastreo en el archivo de configuración::

       crawler.thread.count=10

3. **Ajustar valores de tiempo de espera**

   Para sitios con respuesta lenta, aumente los valores de tiempo de espera.

Problemas de Datos
===================

No se Muestran Resultados de Búsqueda
--------------------------------------

**Causa:**

- No se ha creado el índice
- El rastreo ha fallado
- La consulta de búsqueda es incorrecta

**Solución:**

1. **Verificar índice**::

       $ curl http://localhost:9200/_cat/indices?v

   Verifique que exista el índice de |Fess|.

2. **Verificar registro de rastreo**

   Verifique el registro de rastreo en "Sistema" → "Registro" de la pantalla de administración para ver si hay errores.

3. **Volver a ejecutar rastreo**

   Ejecute "Default Crawler" desde "Sistema" → "Programador" en la pantalla de administración.

4. **Simplificar consulta de búsqueda**

   Primero busque con palabras clave simples para verificar si se devuelven resultados.

El Índice Está Corrupto
-----------------------

**Síntoma:**

Ocurren errores durante la búsqueda, o se devuelven resultados inesperados.

**Solución:**

1. **Eliminar y recrear índice**

   .. warning::

      Si elimina el índice, se perderán todos los datos de búsqueda. Asegúrese de hacer un respaldo.

   ::

       $ curl -X DELETE http://localhost:9200/fess*

2. **Volver a ejecutar rastreo**

   Ejecute "Default Crawler" desde la pantalla de administración para recrear el índice.

Problemas Específicos de Docker
================================

Los Contenedores no Inician
----------------------------

**Síntoma:**

Los contenedores no inician con ``docker compose up``.

**Solución:**

1. **Verificar registros**::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs

2. **Verificar falta de memoria**

   Aumente la memoria asignada a Docker (desde la configuración de Docker Desktop).

3. **Verificar conflicto de puertos**::

       $ docker ps

   Verifique que otros contenedores no estén usando los puertos 8080 o 9200.

4. **Verificar archivo Docker Compose**

   Verifique que no haya errores de sintaxis en el archivo YAML::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml config

Los Contenedores Inician pero no se Puede Acceder a Fess
---------------------------------------------------------

**Solución:**

1. **Verificar estado de contenedores**::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

2. **Verificar registros**::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs fess

3. **Verificar configuración de red**::

       $ docker network ls
       $ docker network inspect <network_name>

Problemas Específicos de Windows
=================================

Problema de Ruta
----------------

**Síntoma:**

Ocurren errores si la ruta contiene espacios o japonés.

**Solución:**

Instale en un directorio que no contenga espacios o japonés en la ruta.

Ejemplo::

    C:\opensearch  (recomendado)
    C:\Program Files\opensearch  (no recomendado)

No se Puede Registrar como Servicio
------------------------------------

**Solución:**

Use herramientas de terceros como NSSM para registrar como servicio de Windows.

Para más detalles, consulte :doc:`install-windows`.

Otros Problemas
===============

Cambio de Nivel de Registro
----------------------------

Para ver registros detallados, cambie el nivel de registro a DEBUG.

Edite ``log4j2.xml``::

    <Logger name="org.codelibs.fess" level="debug"/>

Reinicio de Base de Datos
--------------------------

Para restablecer la configuración, elimine el índice de OpenSearch::

    $ curl -X DELETE http://localhost:9200/.fess_config*

.. warning::

   Ejecutar este comando eliminará todos los datos de configuración.

Información de Soporte
======================

Si el problema no se resuelve, utilice los siguientes recursos de soporte:

Soporte de la Comunidad
------------------------

- **Issues**: https://github.com/codelibs/fess/issues

  Al informar problemas, incluya la siguiente información:

  - Versión de Fess
  - Versión de OpenSearch
  - SO y versión
  - Mensaje de error (extracto del registro)
  - Pasos para reproducir

- **Foro**: https://discuss.codelibs.org/

Soporte Comercial
-----------------

Si necesita soporte comercial, consulte a N2SM, Inc.:

- **Web**: https://www.n2sm.net/

Recopilación de Información de Depuración
==========================================

Al informar problemas, es útil recopilar la siguiente información:

1. **Información de versión**::

       $ cat /path/to/fess/VERSION
       $ /path/to/opensearch/bin/opensearch --version
       $ java -version

2. **Información del sistema**::

       $ uname -a
       $ cat /etc/os-release
       $ free -h
       $ df -h

3. **Archivos de registro**::

       $ tar czf fess-logs.tar.gz /path/to/fess/logs/

4. **Archivos de configuración** (después de eliminar información confidencial)::

       $ tar czf fess-config.tar.gz /path/to/fess/app/WEB-INF/conf/

5. **Estado de OpenSearch**::

       $ curl http://localhost:9200/_cluster/health?pretty
       $ curl http://localhost:9200/_cat/indices?v
