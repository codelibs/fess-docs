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

   Los repositorios estándar de Debian 12 no incluyen el paquete ``openjdk-21-jdk``. En Debian 12, instale en su lugar Eclipse Temurin 21 siguiendo las instrucciones para Debian de la `guía de instalación de Adoptium para Linux <https://adoptium.net/installation/linux/>`__.

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

       $ /path/to/opensearch/bin/opensearch-plugin install https://maven.codelibs.org/release/org/codelibs/opensearch/opensearch-analysis-fess/3.9.0/opensearch-analysis-fess-3.9.0.zip

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

   Cuando ningún OpenSearch responde, |Fess| lo reintenta durante aproximadamente un minuto y
   después deja de iniciarse, con el siguiente mensaje en la consola y en ``logs/fess.log``::

       The search engine at http://localhost:9200 did not become available within 60221ms. Check that OpenSearch is running and reachable. If there is none yet, run bin/fess-setup install opensearch to set one up.

   Inicie OpenSearch o compruebe ``SEARCH_ENGINE_HTTP_URL``. Una instalación ZIP nueva no tiene
   OpenSearch hasta que se configura uno con ``bin/fess-setup install opensearch``; consulte
   :doc:`install-linux`.

2. **Verificar conflicto de número de puerto**::

       $ sudo ss -tuln | grep 8080

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

No se Puede Crear el Índice (Ruta de los Archivos de Diccionario)
-----------------------------------------------------------------

**Síntoma:**

Al acceder a |Fess| se devuelve HTTP 404, y se registra el siguiente error en ``fess.log``::

    Failed to create index: index=fess, path=fess_indices/fess.json
    ... reason=Resource path must be inside config directory: /var/lib/opensearch/data/config/ja/mapping.txt

**Causa:**

OpenSearch 3.8.0 y versiones posteriores rechazan la creación de índices cuando los archivos de diccionario están fuera del directorio de configuración de OpenSearch.
``configsync.config_path`` y ``FESS_DICTIONARY_PATH`` apuntan fuera del directorio de configuración (como ``data/config/``).

**Solución:**

1. Cambie ``configsync.config_path`` y ``FESS_DICTIONARY_PATH`` a un directorio dentro del directorio de configuración de OpenSearch.

   - Versión RPM/DEB: ``/etc/opensearch/dictionary/``
   - Versión ZIP: ``/path/to/opensearch-3.9.0/config/dictionary/``

2. Si tiene archivos de diccionario existentes, cópielos al nuevo directorio.
3. Reinicie OpenSearch y, a continuación, |Fess|.

Para más detalles, consulte :doc:`install-linux`.

Conflicto de Número de Puerto
------------------------------

**Síntoma:**

::

    Address already in use

**Solución:**

1. Verificar puerto en uso::

       $ sudo ss -tuln | grep 8080
       $ sudo lsof -i :8080

2. Detenga el proceso en uso, o cambie el número de puerto de Fess

    Para cambiar el número de puerto, consulte :doc:`Configuración de Puerto y Red <../config/setup-port-network>`.

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

       $ ss -tuln | grep 8080

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

   Inicie |Fess| pasando ``FESS_HEAP_SIZE`` como variable de entorno::

       $ FESS_HEAP_SIZE=4g bin/fess

   Si lo configura en ``bin/fess.in.sh``, escriba ``FESS_HEAP_SIZE=4g`` **antes** de la línea que establece el valor predeterminado de ``FESS_MIN_MEM`` (la línea que determina el tamaño del montón). Si lo añade al final del archivo, no tendrá efecto, porque el tamaño del montón ya se ha determinado en ese punto. En las ediciones RPM/DEB, configúrelo en ``/etc/sysconfig/fess`` (en la edición DEB, ``/etc/default/fess``).

   Ajuste también el tamaño del heap de OpenSearch::

       export OPENSEARCH_JAVA_OPTS="-Xms4g -Xmx4g"

2. **Usar SSD**

   Si la E/S de disco es un cuello de botella, migre a SSD.

3. **Habilitar caché**

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

   Aumente en la pantalla de administración el "Número de hilos" de la configuración de rastreo. El valor predeterminado es 1 para el rastreo Web y 5 para el rastreo del sistema de archivos.

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

   Descargue el registro de rastreo (``fess-crawler.log``) desde "Información del sistema" → "Archivo de registro" de la pantalla de administración y compruebe si hay errores.

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

2. **Reiniciar Fess**

   Los índices se crean al iniciar |Fess|. Justo después de eliminarlos, también se ha perdido el índice de información de usuarios, por lo que no es posible iniciar sesión en la pantalla de administración (``/api/v2/health`` sigue devolviendo ``200``). Al reiniciar |Fess|, se vuelven a crear los índices, los trabajos predeterminados y el usuario inicial (``admin``).

3. **Volver a ejecutar rastreo**

   Ejecute "Default Crawler" desde la pantalla de administración para volver a registrar los documentos objeto de búsqueda.

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

    $ curl -X DELETE 'http://localhost:9200/fess_config.*'

.. warning::

   Ejecutar este comando eliminará todos los datos de configuración.

Contraseña de administrador olvidada
------------------------------------

Si olvidó la contraseña del administrador, puede restablecerla actualizando directamente el documento del usuario en el índice ``fess_user.user`` de OpenSearch. La contraseña se guarda en el campo ``password`` como un hash con la forma ``{bcrypt}$2a$...``. El cambio surte efecto sin reiniciar |Fess|.

1. Cree el hash de la nueva contraseña. |Fess| solo acepta hashes bcrypt que empiecen por ``$2a$``, así que sustituya el ``$2y$`` que genera ``htpasswd`` (incluido en el paquete ``apache2-utils`` o ``httpd-tools``) por ``$2a$``. Sustituya ``NewPassword`` por la nueva contraseña::

       $ HASH=$(htpasswd -bnBC 10 "" 'NewPassword' | tr -d ':\n' | sed 's/^\$2y/$2a/')

2. Actualice la contraseña en el documento del usuario administrador. El ID del documento del usuario administrador en el estado inicial es ``YWRtaW4=``::

       $ curl -X POST 'http://localhost:9200/fess_user.user/_update/YWRtaW4=?refresh=true' \
              -H 'Content-Type: application/json' \
              -d "{\"doc\":{\"password\":\"{bcrypt}${HASH}\"}}"

   Para restablecer la contraseña de otro usuario, busque el ``_id`` con ``curl 'http://localhost:9200/fess_user.user/_search?q=name:USUARIO'`` y utilice ese ID. Si la autenticación está habilitada en OpenSearch, añada las credenciales a curl.

3. Compruebe que puede iniciar sesión en la pantalla de administración con la nueva contraseña. Si la contraseña queda en el historial de comandos, vuelva a establecerla después de iniciar sesión en [Usuario > Usuario].

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

1. **Información de versión** (``bin/fess -v`` está disponible desde la 15.9)::

       $ /path/to/fess/bin/fess -v
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
