================================
Procedimientos de Actualización
================================

Esta página describe los procedimientos para actualizar |Fess| de versiones anteriores a la versión más reciente.

.. warning::

   **Notas Importantes Antes de la Actualización**

   - Asegúrese de hacer un respaldo antes de la actualización
   - Se recomienda encarecidamente validar la actualización en un entorno de prueba con anticipación
   - El servicio se detendrá durante la actualización, por lo que configure un tiempo de mantenimiento apropiado
   - Dependiendo de la versión, el formato del archivo de configuración puede haber cambiado

Versiones Compatibles
=====================

Estos procedimientos de actualización son compatibles con actualizaciones entre las siguientes versiones:

- Fess 14.x → Fess 15.9
- Fess 15.x → Fess 15.9

.. important::

   |Fess| 14.x es compatible con la serie OpenSearch 2.x, mientras que |Fess| 15.9 es compatible
   con OpenSearch 3.8.0. Los plugins de OpenSearch para |Fess| deben coincidir exactamente con la
   versión de OpenSearch, por lo que si actualiza desde la versión 14.x también es obligatorio
   actualizar la versión principal de OpenSearch. Consulte :ref:`upgrade-opensearch`.

.. note::

   Si actualiza desde versiones más antiguas (13.x o anteriores), puede ser necesaria una actualización gradual.
   Para más detalles, verifique las notas de lanzamiento.

Preparación Antes de la Actualización
======================================

Verificación de Compatibilidad de Versiones
--------------------------------------------

Verifique la compatibilidad entre la versión de destino de actualización y la versión actual.

- `Notas de Lanzamiento <https://github.com/codelibs/fess/releases>`__
- :doc:`prerequisites` - Entorno de ejecución de |Fess| 15.9 (versiones de Java y OpenSearch)

Planificación del Tiempo de Inactividad
----------------------------------------

La actualización requiere la detención del sistema. Planifique el tiempo de inactividad considerando lo siguiente:

- Tiempo de respaldo: 10 minutos ~ varias horas (según la cantidad de datos)
- Tiempo de actualización: 10 ~ 30 minutos
- Tiempo de verificación de funcionamiento: 30 minutos ~ 1 hora
- Tiempo de reserva: 30 minutos

**Tiempo de mantenimiento recomendado**: Total 2 ~ 4 horas

Paso 1: Respaldo de Datos
==========================

Antes de la actualización, haga un respaldo de todos los datos.

Respaldo de Datos de Configuración
------------------------------------

1. **Respaldo desde la pantalla de administración**

   Inicie sesión en la pantalla de administración y haga clic en "Información del sistema" → "Copia de seguridad".

   En la página de Copia de seguridad se listan los siguientes datos de configuración como elementos individuales.
   Haga clic en cada fila para descargarlos (son archivos individuales por elemento, no un único archivo ZIP.
   No existe una función de descarga masiva, por lo que debe descargar los elementos necesarios uno por uno).

   - ``fess_basic_config.bulk`` - Índices de configuración (ajustes de rastreo, programador, etiquetas,
     coincidencias de clave, roles, autenticación web/de archivos, entre 19 índices)
   - ``fess_config.bulk`` - Además de los 19 índices anteriores, incluye 25 índices con datos de
     ejecución, como información de rastreo, URL con errores, registros de tareas y colas de miniaturas
   - ``fess_user.bulk`` - Usuarios, roles y grupos
   - ``system.properties`` - Configuración del sistema, incluidos los ajustes generales
   - ``fess.json`` - Configuración del índice (número de shards, ``index.knn``, etc.)
   - ``doc.json`` - Mapeo de documentos (definiciones de campos)

   .. note::

      ``fess_config.bulk`` incluye el contenido de ``fess_basic_config.bulk``. Como respaldo de
      configuración antes de la actualización, basta con ``fess_basic_config.bulk``, ``fess_user.bulk``
      y ``system.properties``.

   .. note::

      Los datos de registro como los registros de búsqueda y clics (``search_log.ndjson``, ``click_log.ndjson``,
      ``favorite_log.ndjson``, ``user_info.ndjson``) también pueden descargarse desde la misma página.
      No son necesarios si solo desea hacer un respaldo de la configuración. Tenga en cuenta que estos
      archivos ``*.ndjson`` no se pueden restaurar cargándolos desde la página de copia de seguridad
      (consulte "Procedimientos de Reversión").

2. **Respaldo de archivos de configuración**

   Versión ZIP::

       $ cp /path/to/fess/app/WEB-INF/conf/system.properties /backup/
       $ cp /path/to/fess/app/WEB-INF/classes/fess_config.properties /backup/
       $ cp /path/to/fess/bin/fess.in.sh /backup/

   Versión RPM::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/
       $ sudo cp /etc/sysconfig/fess /backup/

   Versión DEB::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/
       $ sudo cp /etc/default/fess /backup/

   .. note::

      ``/etc/sysconfig/fess`` (versión RPM) y ``/etc/default/fess`` (versión DEB) son archivos de
      variables de entorno que especifican ``FESS_PORT``, ``FESS_HEAP_SIZE``, ``SEARCH_ENGINE_HTTP_URL``,
      ``FESS_DICTIONARY_PATH`` y otros valores. En la versión ZIP, la configuración
      equivalente se encuentra en ``bin/fess.in.sh``.

3. **Archivos de configuración personalizados**

   Si tiene archivos de configuración personalizados, también haga un respaldo de ellos::

       $ cp /path/to/fess/app/WEB-INF/classes/log4j2.xml /backup/

   .. note::

      ``app/WEB-INF/classes/log4j2.xml`` es la configuración de registro del proceso principal
      (Web) de |Fess|. Los procesos hijos, como el rastreador, usan archivos independientes
      (``app/WEB-INF/env/crawler/resources/log4j2.xml``, entre otros: ``crawler``, ``suggest``,
      ``thumbnail`` y ``chunk``, 4 en total). Si los ha modificado, incluya también estos
      archivos en el respaldo.

Respaldo de Datos de Índice
-----------------------------

Haga un respaldo de los datos de índice de OpenSearch.

Método 1: Usar Función de Instantánea (Recomendado)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use la función de instantánea de OpenSearch para hacer un respaldo del índice.

.. note::

   Para registrar un repositorio del sistema de archivos (``fs``), es necesario especificar previamente el
   directorio de destino del respaldo en ``path.repo`` del archivo ``opensearch.yml`` de OpenSearch
   y reiniciar OpenSearch.

1. Configuración del repositorio::

       $ curl -X PUT "http://localhost:9200/_snapshot/fess_backup" -H 'Content-Type: application/json' -d'
       {
         "type": "fs",
         "settings": {
           "location": "/backup/opensearch/snapshots"
         }
       }'

2. Creación de instantánea::

       $ curl -X PUT "http://localhost:9200/_snapshot/fess_backup/snapshot_1?wait_for_completion=true"

3. Verificación de instantánea::

       $ curl -X GET "http://localhost:9200/_snapshot/fess_backup/snapshot_1"

Método 2: Respaldo de Todo el Directorio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Después de detener OpenSearch, haga un respaldo del directorio de datos.

::

    $ sudo systemctl stop opensearch
    $ sudo tar czf /backup/opensearch-data-$(date +%Y%m%d).tar.gz /var/lib/opensearch/data
    $ sudo systemctl start opensearch

Respaldo de Versión Docker
---------------------------

Los datos de OpenSearch se almacenan en volúmenes Docker. En ``compose-opensearch3.yaml`` se definen
dos volúmenes: ``search01_data`` para los datos del índice y ``search01_dictionary`` para los archivos
de diccionario.

.. note::

   El nombre real del volumen lleva como prefijo el nombre del proyecto Compose (por defecto, el nombre
   del directorio donde se encuentra el archivo Compose). Para obtener el nombre exacto, ejecute::

       $ docker volume ls

Detenga los contenedores y luego haga un respaldo de los volúmenes. En el ``-v`` de ``docker run``,
especifique el nombre real del volumen, incluido el prefijo::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ PROJECT=$(basename "$(pwd)")
    $ docker run --rm -v ${PROJECT}_search01_data:/data -v $(pwd):/backup ubuntu tar czf /backup/search01-data-backup.tar.gz /data
    $ docker run --rm -v ${PROJECT}_search01_dictionary:/data -v $(pwd):/backup ubuntu tar czf /backup/search01-dictionary-backup.tar.gz /data
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml start

.. warning::

   Si especifica ``search01_data`` sin el prefijo en ``-v``, Docker no hará referencia al volumen
   existente, sino que creará uno nuevo y vacío con el mismo nombre. El comando no producirá ningún
   error, pero generará un archivo comprimido vacío, por lo que puede parecer que el respaldo se
   realizó correctamente cuando en realidad no contiene datos.

.. note::

   El contenedor principal de |Fess| (``fess01``) no tiene un volumen dedicado, por lo que los
   únicos elementos que deben respaldarse son los dos anteriores. Sin embargo, los ajustes
   generales modificados desde la pantalla de administración y los plugins instalados desde ella
   se almacenan únicamente dentro del contenedor y se perderán si este se recrea. Persístalos
   especificándolos mediante ``FESS_JAVA_OPTS`` o ``FESS_PLUGINS`` en el archivo Compose.

Paso 2: Detención de la Versión Actual
========================================

Detenga Fess y OpenSearch.

La versión ZIP no incluye un script para detener el servicio. Si inició ``bin/fess`` con
la opción ``-p``, deténgalo usando el archivo PID::

    $ kill $(cat /path/to/fess/fess.pid)
    $ kill <opensearch_pid>

Si lo inició sin especificar ``-p``, verifique el ID del proceso y ejecute ``kill`` manualmente
(con ``-d`` solo no se crea ningún archivo PID).

Versión RPM/DEB (systemd)::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Versión Docker::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Paso 3: Instalación de la Nueva Versión
=========================================

Los procedimientos varían según el método de instalación.

Versión ZIP
-------------------

1. Descargue y extraiga la nueva versión::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.9.0/fess-15.9.0.zip
       $ unzip fess-15.9.0.zip

   .. note::

      La versión archivo de |Fess| se distribuye únicamente en formato ZIP
      (no se ofrece ``fess-15.9.0.tar.gz``).

2. Copie la configuración de la versión antigua::

       $ cp /path/to/old-fess/app/WEB-INF/conf/system.properties /path/to/fess-15.9.0/app/WEB-INF/conf/
       $ cp /path/to/old-fess/app/WEB-INF/classes/fess_config.properties /path/to/fess-15.9.0/app/WEB-INF/classes/
       $ cp /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.9.0/bin/

   .. warning::

      Si se copian enteros, ``fess_config.properties`` y ``fess.in.sh`` conservan sus valores
      antiguos, incluidos aquellos cuyo valor predeterminado cambió en 15.9: por ejemplo, los
      trabajos creados después usan Groovy de forma predeterminada. Antes de ejecutar las dos
      últimas órdenes, compare cada archivo con el de ``fess-15.9.0`` y traslade solo los valores
      que haya cambiado usted. Consulte :ref:`upgrade-159-carried-over-config` para saber qué
      revisar.

3. Si tiene personalizaciones, copie también lo siguiente::

       # Configuración de registro
       $ cp /path/to/old-fess/app/WEB-INF/classes/log4j2.xml /path/to/fess-15.9.0/app/WEB-INF/classes/
       # Plugins instalados
       $ cp -r /path/to/old-fess/app/WEB-INF/plugin/. /path/to/fess-15.9.0/app/WEB-INF/plugin/
       # Tema
       $ cp -r /path/to/old-fess/app/themes/. /path/to/fess-15.9.0/app/themes/

   .. warning::

      No copie directamente los JSP editados desde "Diseño" en la pantalla de administración
      (``app/WEB-INF/view/``). Si la estructura de los JSP cambió en la nueva versión, la pantalla
      podría dejar de mostrarse correctamente. Vuelva a aplicar sus cambios sobre los JSP de la
      nueva versión.

   .. note::

      Los plugins copiados de ``app/WEB-INF/plugin/`` se compilaron para la versión antigua.
      Después de copiarlos, ejecute ``bin/fess-setup upgrade plugins`` en ``fess-15.9.0`` para
      sustituir cada uno por la versión compilada para 15.9; consulte
      :ref:`upgrade-plugin-versions`.

4. Verifique las diferencias de configuración y ajuste según sea necesario

Versión RPM/DEB
---------------

Instale el paquete de la nueva versión::

    # RPM
    $ sudo rpm -Uvh fess-15.9.0.rpm

    # DEB
    $ sudo dpkg -i fess-15.9.0.deb

.. note::

   En la versión RPM, los archivos de configuración de ``/etc/fess/*`` están registrados como
   ``%config(noreplace)``, por lo que se conservan durante la actualización (los nuevos archivos
   predeterminados se colocan junto a ellos con la extensión ``.rpmnew``). Si se han agregado
   nuevas opciones de configuración, es necesario ajustarlas manualmente. Un
   ``/etc/fess/fess_config.properties`` que haya modificado conserva sus valores antiguos en 15.9,
   igual que un archivo copiado en el procedimiento ZIP; consulte
   :ref:`upgrade-159-carried-over-config`.

.. warning::

   En la versión DEB, ``/etc/fess/*`` no está registrado como conffile (los únicos conffile son
   ``/etc/default/fess``, ``/etc/init.d/fess`` y ``/usr/lib/systemd/system/fess.service``). Por lo
   tanto, al ejecutar ``dpkg -i``, archivos como ``/etc/fess/fess_config.properties`` se sobrescriben
   con los de la nueva versión, sin preguntar y sin conservar una copia de los anteriores, así que
   respáldelos antes (Paso 1). Después de la actualización, vuelva a aplicar sus cambios sobre los
   archivos nuevos en lugar de restaurar los archivos antiguos completos (consulte
   :ref:`upgrade-159-carried-over-config`). Tenga en cuenta que ``/etc/fess/system.properties`` es
   un archivo generado en tiempo de ejecución que no forma parte del paquete, por lo que no se
   sobrescribe.

Versión Docker
--------------

1. Obtenga el archivo Compose de la nueva versión::

       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose.yaml
       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-opensearch3.yaml

2. Obtenga la nueva imagen::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

.. _upgrade-opensearch:

Paso 4: Actualización de OpenSearch
====================================

|Fess| 15.9 es compatible con OpenSearch 3.8.0. Si el OpenSearch al que se conecta es una versión
anterior, actualícelo siguiendo estos procedimientos.

.. note::

   Este procedimiento corresponde a los casos en que OpenSearch se gestiona manualmente en las versiones
   ZIP y RPM/DEB. En la versión Docker, al obtener las nuevas imágenes en el Paso 3, OpenSearch
   y los plugins se actualizan conjuntamente, por lo que este paso no es necesario.

.. important::

   |Fess| 15.9 incluye siempre ``index.knn`` en la configuración del índice de búsqueda y
   ``content_chunk_vector`` (de tipo ``knn_vector``) en el mapeo, independientemente de si se
   utiliza la búsqueda por vector de chunks (búsqueda semántica). Por lo tanto, el OpenSearch al
   que se conecta **debe tener instalado el plugin k-NN**.

   - Viene incluido en la distribución estándar de OpenSearch y en la imagen de la versión Docker.
   - **No está incluido en la distribución minimal, por lo que la creación del índice fallará y
     |Fess| no podrá iniciarse.**
   - La configuración del índice también envía siempre ``knn.derived_source.enabled``. En un
     OpenSearch antiguo que no reconozca esta opción, la creación del índice fallará
     independientemente de si el plugin k-NN está instalado.

   Para más detalles, consulte los "Requisitos previos" de :doc:`../config/search-semantic`.

.. warning::

   Realice con cuidado las actualizaciones de versión principal de OpenSearch.
   Pueden surgir problemas de compatibilidad del índice.
   |Fess| 14.x utiliza la serie OpenSearch 2.x, por lo que una actualización desde 14.x siempre
   corresponde a este caso.

1. Instale la nueva versión de OpenSearch

2. Reinstale los plugins::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.8.0

   .. note::

      La versión de estos plugins debe coincidir con la versión de OpenSearch que se utiliza.
      |Fess| 15.9 es compatible con OpenSearch 3.8.0. Si las versiones no coinciden,
      la instalación de los plugins fallará.

3. Inicie OpenSearch::

       $ sudo systemctl start opensearch.service

Paso 5: Inicio de la Nueva Versión
====================================

Versión ZIP::

    $ cd /path/to/fess-15.9.0
    $ ./bin/fess -d -p /path/to/fess-15.9.0/fess.pid

.. note::

   Si especifica ``-p``, se crea un archivo PID que permite detener el servicio la próxima vez
   con ``kill $(cat /path/to/fess-15.9.0/fess.pid)``.

Versión RPM/DEB::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Versión Docker::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Paso 6: Verificación de Funcionamiento
========================================

1. **Verificación de registros**

   Verifique que no haya errores.

   Versión ZIP::

       $ tail -f /path/to/fess/logs/fess.log

   Versión RPM/DEB::

       $ sudo tail -f /var/log/fess/fess.log

   Versión Docker::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

   .. note::

      En el mismo directorio de registros también se generan ``fess-crawler.log`` (procesamiento
      de rastreo), ``audit.log`` (autenticación y operaciones de administración) y
      ``searchlog.log`` (solicitudes de búsqueda).

2. **Acceso a la interfaz Web**

   Acceda a http://localhost:8080/ desde el navegador.

3. **Inicio de sesión en la pantalla de administración**

   Acceda a http://localhost:8080/admin e inicie sesión con la cuenta de administrador.

4. **Verificación de la versión**

   En la pantalla de administración, haga clic en "Información del sistema" → "Información de configuración"
   y verifique que ``fess.version`` que se muestra en "Propiedades del sistema" corresponda a la nueva versión.

5. **Verificación de funcionamiento de búsqueda**

   Ejecute una búsqueda en la pantalla de búsqueda y verifique que se devuelvan resultados normalmente.

Paso 7: Recreación del Índice (Recomendado)
=============================================

Para actualizaciones de versión principal, se recomienda recrear el índice.

.. note::

   Los pasos siguientes vuelven a ejecutar el rastreo; no actualizan el mapeo del índice
   (definiciones de campos). Si necesita una reindexación que actualice el mapeo — por ejemplo,
   para habilitar recién la búsqueda por vector de chunks (búsqueda semántica) —, ejecute por
   separado la "Reindexación" en "Información del sistema" → "Mantenimiento" en la interfaz de
   administración. Consulte :ref:`semantic-search-migration` (:doc:`../config/search-semantic`)
   para más detalles.

1. Verifique los programas de rastreo existentes
2. Ejecute "Default Crawler" desde "Sistema" → "Programador"
3. Espere hasta que se complete el rastreo
4. Verifique los resultados de búsqueda

.. warning::

   Dado que la reindexación reconstruye el índice con el nuevo mapeo, fallará en un OpenSearch
   sin el plugin k-NN. Consulte las notas del Paso 4.

Actualización de 15.8 a 15.9
============================

Si actualiza desde 15.8, los cambios siguientes no son retrocompatibles.

Eliminación del OpenSearch integrado
------------------------------------

Hasta 15.8, iniciar ``bin/fess`` sin definir ``SEARCH_ENGINE_HTTP_URL`` hacía que |Fess|
ejecutara un nodo OpenSearch dentro de su propia JVM. Esa configuración desaparece en 15.9: el
motor de búsqueda es siempre un servidor independiente.

``bin/fess.in.sh`` ahora establece ``SEARCH_ENGINE_HTTP_URL=http://localhost:9200`` de forma
predeterminada. |Fess| no se inicia si no hay ningún OpenSearch accesible.
``bin/fess-setup install opensearch`` instala uno (solo Linux y Windows; OpenSearch no publica
una versión para macOS, así que utilice Homebrew o Docker en ese caso).

También se han eliminado:

- el directorio ``es/`` (``es/modules``, ``es/plugins`` y ``es/data``)
- ``-Dfess.es.dir`` y ``SEARCH_ENGINE_HOME``
- ``bin/module.xml`` y ``bin/plugin.xml``
- los valores de reserva de las antiguas claves de configuración ``elasticsearch.*``

Un motor anterior a OpenSearch 3 también detiene el inicio, mientras que 15.8 registraba un error
y continuaba. Esas versiones no implementan la ordenación ``_shard_doc`` de la que dependen todas
las operaciones que recorren el conjunto completo de resultados, y por HTTP una petición así se
queda colgada en lugar de fallar.

.. warning::

   Los datos de índice de una instalación integrada no se pueden conservar. Construya un nuevo
   servidor OpenSearch externo, traslade la configuración con la página de copia de seguridad de
   la administración y vuelva a rastrear. La copia de seguridad incluye la configuración de
   rastreo, los usuarios y los registros; **no** contiene los documentos rastreados.

El rastreador de Playwright pasa a un plugin
--------------------------------------------

El rastreador de Playwright, y los ejecutables de Node.js que utiliza, ya no forman parte de la
distribución. En ``fess-15.8.0.zip`` (457,1 MiB), el paquete de controladores de Playwright que
contenía los ejecutables de Node.js ocupaba 204,3 MiB.

Si alguna configuración de rastreo indica el cliente de Playwright, por ejemplo con
``client.crawlerClients=playwright:http://.*`` en sus parámetros de configuración, instale tanto
el plugin como Node.js. El plugin también puede instalarse desde la página
**Sistema > Plugin** de la pantalla de administración. ``bin/fess.in.sh`` detecta Node.js y
establece ``PLAYWRIGHT_NODEJS_PATH``.

::

    $ bin/fess-setup install plugin fess-crawler-playwright
    $ bin/fess-setup install nodejs

Sin el plugin, esa configuración se sigue rastreando, pero con el cliente HTTP normal, de modo
que el texto que solo genera JavaScript no se indexa. El trabajo de rastreo termina igualmente
con éxito y no se registra ninguna URL con errores. En cada rastreo, ``fess-crawler.log`` registra
una advertencia por cada configuración de rastreo, con el nombre del plugin y las dos órdenes
anteriores.

Si no utiliza el rastreador de Playwright, no hay nada que hacer.

Google Cloud Storage pasa a un plugin
-------------------------------------

El SDK de Google Cloud Storage ya no forma parte de la distribución, por lo que el rastreo de
``gcs://`` y el tipo de almacenamiento ``gcs`` provienen ahora del plugin ``fess-storage-gcs``.
Instálelo desde la página **Sistema > Plugin** de la pantalla de administración o con la
orden siguiente.

::

    $ bin/fess-setup install plugin fess-storage-gcs

``gcs`` también ha salido del valor distribuido de ``crawler.file.protocols``, que ahora es
``file,smb,smb1,ftp``; el plugin lo vuelve a añadir al instalarse. Hasta entonces, una
configuración de rastreo de archivos cuya ruta empieza por ``gcs:`` se registra como
advertencia y no recupera nada. Una instalación que se actualiza conserva su propio
``crawler.file.protocols``, por lo que la ruta se sigue aceptando pero ningún cliente de
rastreo la atiende; en una instalación nueva ``gcs:`` no es un protocolo configurado, así que
la pantalla de administración rechaza guardar la ruta y una ruta guardada antes se lee como
ruta de archivo local. La página de almacenamiento también registra una advertencia y muestra
el fallo como un error con el nombre del plugin que hay que instalar, donde antes solo
mostraba una lista de archivos vacía.

Si no utiliza Google Cloud Storage, no hay nada que hacer. Amazon S3 y el almacenamiento
compatible con S3, como MinIO, han pasado a un plugin de la misma manera; consulte la sección
siguiente.

Amazon S3 pasa a un plugin
--------------------------

El SDK de AWS ya no forma parte de la distribución, por lo que el rastreo de ``s3://`` y los
tipos de almacenamiento ``s3`` y ``s3_compat`` provienen ahora del plugin
``fess-storage-s3``. Instálelo desde la página **Sistema > Plugin** de la pantalla de
administración o con la orden siguiente.

::

    $ bin/fess-setup install plugin fess-storage-s3

``s3`` también ha salido del valor distribuido de ``crawler.file.protocols``, que ahora es
``file,smb,smb1,ftp``; el plugin lo vuelve a añadir al instalarse. ``storage.type`` sigue
teniendo el valor predeterminado ``auto``, que se resuelve como S3 cuando no hay ningún punto
final configurado, así que la página de almacenamiento de la pantalla de administración no
funciona hasta que se instala el plugin, aunque nunca haya indicado ``s3`` explícitamente. Sus
valores ``storage.*`` se conservan, porque están en ``WEB-INF/conf/system.properties``, y un
``crawler.file.protocols`` existente tampoco se sustituye en la actualización.

Si no utiliza Amazon S3 ni almacenamiento compatible con S3 como MinIO, no hay nada que hacer.

La autenticación SSO pasa a plugins
-----------------------------------

Ninguno de los cuatro autenticadores SSO forma parte ya de la distribución; cada valor de
``sso.type`` proviene ahora de su propio plugin, que incluye la biblioteca de identidad que
necesita: ``saml`` de ``fess-sso-saml``, ``spnego`` de ``fess-sso-spnego``, ``entraid`` (y el
antiguo ``aad``) de ``fess-sso-entraid`` y ``oic`` de ``fess-sso-oidc``. Fíjese en el último
par: el plugin se llama ``fess-sso-oidc`` mientras que el valor de ``sso.type`` sigue siendo
``oic``, el único lugar en el que ambos difieren. Instale el que utilice desde la página
**Sistema > Plugin** de la pantalla de administración o con la orden siguiente.

::

    $ bin/fess-setup install plugin fess-sso-saml

Sus valores de configuración se conservan, porque ``sso.type`` y las claves ``saml.*``,
``spnego.*``, ``entraid.*``, ``aad.*`` y ``oic.*`` están en
``WEB-INF/conf/system.properties``. Además, "Sistema" → "General" de la pantalla de
administración sigue ofreciendo los cuatro tipos y sigue mostrando sus ajustes, porque un
plugin no puede proporcionar un JSP, así que nada en esa pantalla indica que falte un plugin.

Hasta que se instala el plugin, una petición a ``/sso/`` se redirige de vuelta a la página de
inicio de sesión, que informa de que el inicio de sesión SSO ha fallado, y nadie puede iniciar
sesión mediante SSO. 15.9 registra en ``fess.log`` una advertencia con el nombre del componente
que ha buscado y el del plugin que lo proporciona, donde hasta 15.8 no se registraba nada en
ningún nivel.

Si no utiliza SSO, es decir, si ``sso.type`` es ``none`` o no está definido, no hay nada que
hacer.

El motor de scripting integrado pasa de Groovy a JavaScript
-----------------------------------------------------------

Hasta 15.8 el motor de scripting integrado era Groovy y ``job.default.script`` tenía el valor
predeterminado ``groovy``. En 15.9 el motor integrado es JavaScript y el valor predeterminado es
``javascript``. Groovy ya no está integrado: lo proporciona el plugin ``fess-script-groovy``, que
debe estar instalado para que un ``scriptType`` con valor ``groovy`` se pueda resolver.

Una actualización no cambia el motor almacenado con cada ajuste, y un ajuste guardado antes de 15.9
que no registra ningún motor cuenta como ``groovy``. Sin el plugin, deja de funcionar lo siguiente:

- Los trabajos programados guardados como ``groovy``. **Esto incluye los trabajos que creó el
  propio 15.8:** Default Crawler, Suggest Indexer, Config Reloader, Log Aggregator, Doc Purger y
  los demás trabajos incluidos están guardados como ``groovy``, y al iniciarse 15.9 solo añade los
  trabajos incluidos que todavía no existen, así que no los modifica. Cada uno de ellos falla cada
  vez que se ejecuta según su programación, de modo que Default Crawler deja de rastrear. La
  mayoría de los trabajos incluidos tienen desactivado "Registro", por lo que sus fallos no
  aparecen en el registro de trabajos, sino solo como advertencias ``Failed to execute job`` en
  ``fess.log``.
- Las configuraciones de rastreo web y de archivos con scripts de campo
  (``field.script.<nombre del campo>``) en "Parámetro de configuración". Todos los documentos de
  una configuración así fallan con una ``ScriptEngineException`` y se registran como URL con
  errores, mientras que el propio trabajo de rastreo termina correctamente.
- Las configuraciones de almacén de datos con un "Script". Los valores que no son solo un nombre de
  parámetro no se pueden evaluar; consulte :doc:`../config/datastore/ds-overview`.
- Las reglas de impulso de documentos. Una regla así no impulsa nada.
- Los mapeos de rutas cuyo "Reemplazo" empieza por ``groovy:``. Un mapeo así no se aplica y las
  URL quedan sin cambios.

Después del primer inicio, busque en ``fess.log`` una advertencia que empiece por
``Settings use the script engine groovy, which is not registered``. |Fess| comprueba los ajustes
anteriores una vez al iniciarse e indica, para cada tipo, cuántos usan un motor que ningún plugin
proporciona. También menciona ``job.default.script`` cuando un ``fess_config.properties`` traído
de 15.8 sigue indicando ``groovy``; en ese caso, los trabajos creados después de la actualización
también usan Groovy (consulte :ref:`upgrade-159-carried-over-config`). Resuélvalo de una de estas
dos maneras:

- Instale el plugin y reinicie |Fess|. Los scripts de Groovy almacenados se ejecutan entonces sin
  cambios y la advertencia deja de registrarse. El plugin también puede instalarse desde
  "Sistema" → "Plugin" en la pantalla de administración.

  ::

      $ bin/fess-setup install plugin fess-script-groovy

- Pase cada ajuste a JavaScript. Primero reescriba la sintaxis que solo acepta Groovy y después
  seleccione JavaScript:

  - Trabajos programados: en "Sistema" → "Programador", cambie "Tipo de ejecución" a
    ``javascript``. Los scripts de los trabajos incluidos son JavaScript válido tal como están, con
    dos excepciones: Thumbnail Purger usa el literal ``long`` de Groovy ``1000L``, que JavaScript
    rechaza (escriba ``1000``), e Index Exporter necesita el cambio descrito en
    :ref:`upgrade-159-index-exporter`. Un literal de array de JavaScript se convierte
    automáticamente en un ``String[]`` de Java, por lo que se omiten las conversiones
    ``as String[]`` de la forma Groovy:

    ::

        return container.getComponent("crawlJob").logLevel("info").webConfigIds(["1", "2"]).fileConfigIds(["1"]).dataConfigIds([]).execute(executor);

  - Configuraciones de rastreo web y de archivos: añada ``config.script.type=javascript`` a
    "Parámetro de configuración".
  - Configuraciones de almacén de datos: añada ``script_type=javascript`` a "Parámetro".
  - Reglas de impulso de documentos: cambie "Tipo de Script" a ``javascript``.
  - Mapeos de rutas: empiece el "Reemplazo" por ``javascript:`` en lugar de ``groovy:``.
  - ``job.default.script``: establézcalo en ``javascript`` en un ``fess_config.properties``
    traído de 15.8.

``crawler.default.script`` se ha eliminado
------------------------------------------

``crawler.default.script`` ya no existe en ``fess_config.properties``. Elimínelo de su
configuración; un valor que permanezca con ese nombre no tiene ningún efecto.

El protocolo de rastreo ``storage`` se ha eliminado
---------------------------------------------------

``storage`` ya no se admite en ``crawler.file.protocols``; el valor incluido es
``file,smb,smb1,ftp``. Utilice ``s3`` en su lugar y cambie a una ruta ``s3:`` cualquier
configuración de rastreo de archivos cuya ruta empiece por ``storage:``. ``s3`` necesita el
plugin ``fess-storage-s3``.

.. _upgrade-159-index-exporter:

El trabajo Index Exporter hace referencia a un paquete eliminado
----------------------------------------------------------------

15.9 ya no incluye las clases ``org.opensearch``; los constructores de consultas que usan los
scripts de los trabajos están ahora en ``org.codelibs.fesen.opensearch``. El script que 15.8
guardó para el trabajo Index Exporter hace referencia a
``org.opensearch.index.query.QueryBuilders``, y la actualización no lo sustituye, así que el
trabajo falla incluso con ``fess-script-groovy`` instalado. El trabajo se distribuye desactivado y
sin programación, por lo que solo le afecta si lo ejecuta. Ábralo en "Sistema" → "Programador" y
cambie el paquete de su script por el de 15.9:

::

    return new org.codelibs.fess.job.IndexExportJob().query(org.codelibs.fesen.opensearch.index.query.QueryBuilders.matchAllQuery()).execute()

Cambie de la misma manera cualquier script propio que haga referencia a
``org.opensearch.index.query``. Consulte :doc:`../config/admin-index-export` para ver más ejemplos
de consultas.

.. _upgrade-159-carried-over-config:

Archivos de configuración traídos de 15.8
-----------------------------------------

El procedimiento ZIP del Paso 3 copia ``fess_config.properties`` y ``bin/fess.in.sh`` de la
instalación antigua, y una actualización RPM conserva un ``/etc/fess/fess_config.properties`` que
haya modificado (el archivo de 15.9 se coloca junto a él como ``fess_config.properties.rpmnew``).
En ambos casos, 15.9 funciona después con los valores de 15.8, incluidos aquellos cuyo valor
distribuido cambió en 15.9. Revise al menos las claves siguientes.

.. list-table::
   :header-rows: 1

   * - Clave
     - 15.8.0
     - 15.9
     - Efecto de conservar el valor de 15.8
   * - ``job.default.script``
     - ``groovy``
     - ``javascript``
     - Los trabajos creados en "Sistema" → "Programador" usan ``groovy`` de forma predeterminada y
       fallan sin el plugin ``fess-script-groovy``.
   * - ``job.template.script``
     - Forma Groovy con ``as String[]``
     - Forma JavaScript
     - Un trabajo creado a partir de una configuración de rastreo recibe un script de Groovy.
   * - ``crawler.file.protocols``
     - ``file,smb,smb1,ftp,storage,s3,gcs``
     - ``file,smb,smb1,ftp``
     - Una ruta que empieza por ``s3:`` o ``gcs:`` se sigue aceptando sin su plugin y se omite con
       una advertencia al rastrear. ``storage`` ya no se admite.
   * - ``search_engine.http.url``
     - ``http://localhost:9201``
     - ``http://localhost:9200``
     - Se usa cuando ``SEARCH_ENGINE_HTTP_URL`` no está definido, como en un ``bin/fess.in.sh``
       copiado de 15.8 en el que no lo definió. |Fess| busca entonces OpenSearch en el puerto 9201,
       el del OpenSearch integrado que 15.9 eliminó.
   * - ``jvm.crawler.options``, ``jvm.thumbnail.options``
     - ``-Djcifs.smb.client.*``, ``-Djcifs.smb1.smb.client.*``
     - ``-Djcifs.client.*``
     - Los tiempos de espera de SMB siguen con los valores predeterminados de jcifs; consulte
       :ref:`upgrade-159-jcifs`.
   * - ``crawler.default.script``, ``theme.allowed.archive.extensions``,
       ``theme.assets.cache.max.age``, ``theme.assets.precompressed``,
       ``rag.chat.message.max.length``
     - Presentes
     - Eliminadas
     - Ningún efecto; elimínelas.

A un ``bin/fess.in.sh`` copiado de 15.8 también le faltan dos cosas que sí tiene el archivo de
15.9. Deja ``SEARCH_ENGINE_HTTP_URL`` sin definir salvo que lo haya definido usted, mientras que
15.9 define ``http://localhost:9200``, y no busca el Node.js instalado con
``bin/fess-setup install nodejs``, por lo que el rastreador de Playwright no encuentra Node.js a
menos que defina ``PLAYWRIGHT_NODEJS_PATH``.

En lugar de copiar cualquiera de los dos archivos entero, parta del archivo distribuido con 15.9 y
vuelva a aplicar los valores que haya cambiado. ``diff`` los muestra::

    $ diff /path/to/old-fess/app/WEB-INF/classes/fess_config.properties /path/to/fess-15.9.0/app/WEB-INF/classes/fess_config.properties
    $ diff /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.9.0/bin/fess.in.sh

En una actualización RPM, compare de la misma manera ``/etc/fess/fess_config.properties`` con
``/etc/fess/fess_config.properties.rpmnew``. Una actualización DEB, en cambio, sobrescribe
``/etc/fess/fess_config.properties`` (consulte el Paso 3), así que se parte de los valores de 15.9
y solo hay que volver a aplicar sus propios cambios.

.. _upgrade-159-jcifs:

Los tiempos de espera de SMB usan los nombres de propiedad de jcifs 3
---------------------------------------------------------------------

jcifs, la biblioteca que |Fess| utiliza para rastrear servidores de archivos SMB, cambió el nombre
de sus propiedades en la versión 3: ``jcifs.smb.client.*`` pasó a ser ``jcifs.client.*``, y los
nombres separados ``jcifs.smb1.smb.client.*`` para SMB1 se unificaron en las mismas propiedades.
Hasta 15.8, ``jvm.crawler.options`` y ``jvm.thumbnail.options`` seguían pasando los nombres
antiguos, que jcifs ignora, por lo que los rastreos SMB se ejecutaban con los valores
predeterminados de jcifs. 15.9 pasa los nombres nuevos:

::

    -Djcifs.client.responseTimeout=30000
    -Djcifs.client.soTimeout=35000
    -Djcifs.client.connTimeout=60000
    -Djcifs.client.sessionTimeout=60000

Por tanto, los tiempos de espera de conexión y de sesión surten efecto por primera vez y pasan del
valor predeterminado de jcifs de 35 segundos a 60 segundos: un rastreo espera ahora hasta 60
segundos a un servidor SMB que no responde. Los tiempos de espera de respuesta y de socket
coinciden con los valores predeterminados de jcifs, así que no cambian.

Si cambió estos tiempos de espera, cambie sus nombres en ambas opciones. Con los nombres antiguos
tampoco tenían efecto en 15.8. Un ``fess_config.properties`` traído de 15.8 conserva los nombres
antiguos y, con ellos, los valores predeterminados de jcifs.

Se han eliminado cuatro propiedades sin efecto
----------------------------------------------

Las siguientes claves ya no existen en ``fess_config.properties``. |Fess| nunca las leyó de ese
archivo, así que un valor que permanezca con estos nombres sigue sin tener efecto.

- ``theme.allowed.archive.extensions``
- ``theme.assets.cache.max.age``
- ``theme.assets.precompressed``
- ``rag.chat.message.max.length``

El límite que establece ``rag.chat.message.max.length`` sigue funcionando, pero se lee como
propiedad del sistema: defínalo en ``app/WEB-INF/conf/system.properties`` o con
``-Dfess.system.rag.chat.message.max.length``, como se describe en :doc:`../config/rag-chat`.

Migración Específica de 15.9
==============================

Si actualiza desde la versión 15.7 o anterior a la 15.9, es posible que deba realizar las
siguientes tareas según las funciones que utilice.

Si Utilizaba la Búsqueda Semántica
------------------------------------

El plugin ``fess-webapp-semantic-search``, que proporcionaba la búsqueda semántica en las
versiones 15.7 y anteriores, ya no es necesario (y queda obsoleto) porque se integró en el
núcleo en la versión 15.9. Debe eliminar el plugin, eliminar ``-Dfess.semantic_search.*`` y
``-Drank.fusion.searchers=default,semantic``, y separar el antiguo ingest pipeline. Consulte
:ref:`semantic-search-migration` (:doc:`../config/search-semantic`) para conocer el
procedimiento.

Si Utilizaba el Modo de Búsqueda con IA (Chat RAG)
-----------------------------------------------------

A partir de la versión 15.9, la función del modo de búsqueda con IA (chat RAG) se separó en
plugins independientes, como ``fess-llm-ollama``, ``fess-llm-openai`` y ``fess-llm-gemini``.
Instale el plugin correspondiente al proveedor que utilice desde "Sistema" → "Plugin" en la
pantalla de administración.

Si Utilizaba SPNEGO (Autenticación Integrada de Windows)
--------------------------------------------------------

A partir de la versión 15.9, un inicio de sesión SPNEGO se rechaza cuando el reino Kerberos del
principal del cliente difiere del reino del servidor. Si sus usuarios inician sesión desde un
dominio secundario de un árbol de dominios de AD o desde un bosque de confianza, indique esos
reinos, separados por comas, en ``spnego.allowed.realms`` desde "Sistema" → "General" en la
pantalla de administración o en ``app/WEB-INF/conf/system.properties``. De lo contrario, los
usuarios que podían iniciar sesión hasta la versión 15.7 son rechazados con
``Kerberos realm is not allowed``. Consulte :doc:`../config/sso-spnego` para conocer más
detalles.

Además, en la versión 15.9 los valores predeterminados definidos en el código de
``spnego.allow.unsecure.basic`` y ``spnego.allow.localhost`` cambiaron de ``true`` a ``false``.
Una instalación en la que estas claves no estén presentes en
``app/WEB-INF/conf/system.properties`` adopta el comportamiento más estricto al actualizar. En
particular, con ``spnego.allow.unsecure.basic=false`` la biblioteca SPNEGO solo ofrece la
autenticación básica en las peticiones en las que ``HttpServletRequest#isSecure()`` devuelve
``true``, por lo que, detrás de un proxy inverso que termina TLS y reenvía la petición por HTTP,
los clientes que antes recurrían a la autenticación básica ya no pueden iniciar sesión. En ese
caso, establezca ``tomcat.secure=true`` en ``tomcat_config.properties``; consulte
:doc:`../config/sso-spnego` para conocer más detalles.

.. warning::

   Un valor predeterminado definido en el código solo se aplica mientras la clave está ausente, y
   "Sistema" → "General" de la pantalla de administración escribe todas las claves ``spnego.*``
   cada vez que se guarda. Por lo tanto, una instalación en la que alguna vez se pulsó Actualizar
   en esa pantalla con la versión 15.7 sigue teniendo almacenados
   ``spnego.allow.unsecure.basic=true`` y ``spnego.allow.localhost=true``, y actualizar a 15.9 no
   la refuerza: mantiene el comportamiento permisivo de forma silenciosa y 15.9 solo registra una
   advertencia en ``fess.log`` al inicializar SPNEGO. Abra "Sistema" → "General" (o edite
   ``system.properties``) y desactive ambas opciones de forma deliberada.
   ``spnego.allow.localhost=true`` es la más peligrosa de las dos: la biblioteca SPNEGO autentica
   las peticiones procedentes del mismo host como el usuario del sistema operativo del servidor,
   sin ninguna verificación de Kerberos, lo que resulta inseguro detrás de un proxy inverso
   situado en el mismo host.

Si Utilizaba la Autenticación SAML (SSO)
----------------------------------------

A partir de la versión 15.9, |Fess| vincula cada respuesta SAML al identificador de la
AuthnRequest que envió, por lo que el SSO iniciado por el IdP (no solicitado) ya no funciona. Un
inicio de sesión que comienza en un icono de |Fess| dentro de un portal del IdP, como el panel de
Okta o el portal "Mis aplicaciones" de Microsoft Entra ID, no tiene ninguna AuthnRequest con la
que emparejarse y se rechaza. Hasta la versión 15.7 funcionaba porque |Fess| devolvía al IdP la
respuesta que no podía emparejar y el IdP entregaba de inmediato una aserción solicitada. Si
coloca un icono en el lado del IdP, haga que apunte al endpoint ``/sso/`` de |Fess| para que el
inicio de sesión lo inicie el SP.

Además, el IdP devuelve la aserción mediante un POST entre sitios, por lo que
``tomcat.sameSiteCookies`` debe establecerse en ``none`` en ``tomcat_config.properties``. Con el
valor predeterminado ``lax`` que se incluye, la cookie de sesión no se envía en esa petición y el
inicio de sesión SAML no puede completarse. Este archivo se encuentra en ``lib/classes/`` en el
paquete ZIP y en ``/etc/fess/`` en los paquetes DEB/RPM, y es necesario reiniciar |Fess| tras el
cambio. Los navegadores solo aceptan ``none`` en una cookie que además tenga el atributo
``Secure``, por lo que |Fess| debe servirse mediante HTTPS. Hasta la versión 15.7, esta
configuración incorrecta no producía un error claro, sino un bucle interminable de redirecciones
al IdP, así que compruebe el ajuste incluso en un sitio que parecía funcionar; en la versión 15.9
falla una sola vez en lugar de entrar en bucle. Consulte :doc:`../config/sso-saml` para conocer
más detalles.

Si Utilizaba Microsoft Entra ID (Azure AD)
------------------------------------------

A partir de la versión 15.9, el modo de respuesta solicitado al endpoint de autorización es
``query`` por defecto, en lugar de ``form_post``. Hasta la versión 15.7 el callback se devolvía
como un POST entre sitios, y con el valor por defecto de |Fess| ``tomcat.sameSiteCookies = lax``
la cookie de sesión no se envía en esa petición, por lo que era necesario
``tomcat.sameSiteCookies = none``. Si estableció ``none`` únicamente por ese motivo, puede volver
al valor por defecto. Para mantener el comportamiento anterior, establezca
``entraid.response.mode=form_post`` y conserve ``tomcat.sameSiteCookies = none``. Los navegadores
solo aceptan ``none`` en una cookie que además tenga el atributo ``Secure``, por lo que esa vía
también exige servir |Fess| mediante HTTPS.

A partir de la versión 15.9, |Fess| también resuelve la pertenencia a grupos y roles del usuario
en segundo plano una vez completado el inicio de sesión, en lugar de bloquear el inicio de sesión
a la espera de Microsoft Graph. Hasta que la resolución termina — o si no se completa del todo —,
el usuario solo tiene su propio permiso a nivel de usuario y lo que aporten
``entraid.default.groups`` y ``entraid.default.roles``. Si no se ha configurado ninguno de los
dos —el valor por defecto que se incluye—, una búsqueda hecha en esa ventana no devuelve ningún
documento, porque una configuración de rastreo creada con los valores por defecto que se incluyen
concede ``{role}guest`` y un usuario con la sesión iniciada no tiene ese rol. Mientras la
resolución está en curso, la pantalla de búsqueda lo indica, y muestra otro mensaje distinto si no
se completó del todo: la resolución solo se considera correcta si han tenido éxito tanto la
consulta de pertenencias directas como el recorrido de los grupos anidados. La resolución se
reintenta cada vez que se renueva el token de acceso, y un éxito posterior hace desaparecer el
mensaje, por lo que un fallo no es definitivo en una sesión que dura más que el token; para
reintentarlo de inmediato, cierre la sesión y vuelva a iniciarla. Consulte
:doc:`../config/sso-entraid` para conocer más detalles.

Una consecuencia de resolver en segundo plano: hasta que la resolución llega, los roles resueltos
del usuario todavía no se conocen. Por eso, un administrador es redirigido a la pantalla de
búsqueda en lugar de al panel de administración, y si abre una página del panel de administración
durante esa ventana vuelve a la pantalla de búsqueda. La ventana dura hasta aproximadamente un
segundo de retardo de planificación más las propias llamadas a Microsoft Graph — una para las
pertenencias directas y luego una más por cada uno de esos grupos para recorrer los grupos
anidados, emitidas una tras otra con la caché fría —, por lo que crece con el número de grupos a
los que pertenece el usuario. En esa ventana el acceso solo se deniega, nunca se concede, y no
hace falta ninguna configuración para superarla: la autorización se evalúa de nuevo en cada
petición de la misma sesión, así que una vez terminada la resolución las pantallas de
administración se abren con normalidad, sin volver a iniciar sesión.

.. warning::

   No acorte esa ventana poniendo el rol de administrador de |Fess| en ``entraid.default.roles``.
   Esa propiedad es un valor global único que |Fess| aplica a todos los usuarios de Entra ID al
   iniciar sesión y vuelve a aplicar en cada resolución posterior, por lo que concedería a todos
   los usuarios del inquilino permisos permanentes de administrador de |Fess|.

Si Utiliza LDAP / Active Directory
----------------------------------

A partir de 15.9, el nombre de permiso de un grupo o rol es el valor del RDN de la entrada y no un
fragmento del texto del DN. Por tanto, un grupo cuyo CN contiene un carácter que el DN escapa --la
coma es el caso habitual-- obtiene un nombre de permiso distinto al de 15.7.

.. list-table::
   :header-rows: 1

   * - DN de la entrada del grupo
     - Nombre de permiso hasta 15.7
     - Nombre de permiso en 15.9
   * - ``CN=Sales\, EMEA,CN=Users,...``
     - ``2Sales``
     - ``2Sales, EMEA``
   * - ``CN=Sales\, APAC,CN=Users,...``
     - ``2Sales``
     - ``2Sales, APAC``

Hasta 15.7, varios grupos que coincidían hasta la coma se reducían a un mismo nombre de permiso, de
modo que los miembros de ``Sales, EMEA`` y ``Sales, APAC`` podían leer los documentos del otro grupo
y los del grupo ``Sales``. En 15.9 cada uno obtiene su propio nombre de permiso y ese acceso entre
grupos no se produce.

A cambio, **los documentos indexados con el nombre de permiso antiguo dejan de ser visibles para los
miembros de ese grupo**. Si la configuración de permisos de un rastreo contiene un nombre de permiso
antiguo, actualícelo al nuevo y vuelva a rastrear (o reindexar). Si no utiliza ningún grupo cuyo CN
contenga una coma u otro carácter escapado, ningún nombre de permiso cambia.

Cambio en ``ldap.role.search.user.enabled``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hasta 15.7, el permiso derivado del nombre de usuario (``role.search.user.prefix`` seguido del
nombre de usuario) se concedía incluso con ``ldap.role.search.user.enabled=false``. A partir de 15.9
la opción surte efecto y el permiso no se concede cuando está desactivada.

En una instalación que la tenga en ``false``, los usuarios pierden tras la actualización el permiso
que lleva su propio nombre, por lo que los documentos asignados a un usuario concreto dejan de
aparecer para ese usuario. Para mantener el comportamiento anterior, restaure el valor
predeterminado ``true``.

Si Había Modificado las Claves de Configuración de /api/v2
----------------------------------------------------------

En 15.8.0, cuatro claves de configuración perdieron su prefijo ``api.v2.``. Sus valores, valores
predeterminados y comportamiento no cambian, pero **no se conserva ningún alias retrocompatible**:
una configuración que permanezca con su nombre antiguo se ignora sin ninguna advertencia y se
aplica el valor predeterminado incluido.

.. list-table::
   :header-rows: 1

   * - Hasta 15.7
     - 15.8.0 en adelante
     - Valor predeterminado
   * - ``api.v2.chat.stream.keepalive.interval.ms``
     - ``api.chat.stream.keepalive.interval.ms``
     - ``15000``
   * - ``api.v2.param.max.length``
     - ``api.param.max.length``
     - ``1000``
   * - ``api.v2.param.max.array.size``
     - ``api.param.max.array.size``
     - ``100``
   * - ``api.v2.click.max.rt``
     - ``api.click.max.timestamp``
     - ``9999999999999``

Si estableció alguna de ellas en ``fess_config.properties`` o como argumento de JVM
``-Dfess.config.<clave>``, cámbieles el nombre. Solo se ven afectadas las configuraciones
explícitas; una instalación que nunca las modificó no requiere ninguna acción.

La primera clave controla con qué frecuencia se envía una trama de keep-alive mientras
``POST /api/v2/chat/stream`` espera al modelo, por lo que el modo de búsqueda con IA es donde se
nota una configuración perdida. La última clave también se renombró por precisión: limita el
valor ``rt`` que puede llevar un registro de clic, que es una marca de tiempo y no un tiempo de
respuesta.


.. _upgrade-plugin-versions:

Actualización de la Versión de los Plugins
---------------------------------------------

Los plugins instalados en ``app/WEB-INF/plugin/`` deben reemplazarse por los correspondientes a
la versión de |Fess|. ``bin/fess-setup upgrade plugins`` lo hace para todos los plugins
instalados: instala la versión compilada para este |Fess| y elimina la anterior. Después, reinicie
|Fess|. A continuación, ``bin/fess-setup check`` informa sobre OpenSearch, sus plugins y los
plugins de |Fess| instalados, y termina con el código 1 cuando algo va mal.

::

    $ bin/fess-setup upgrade plugins
    $ bin/fess-setup check

``upgrade plugins`` solo trata los plugins que ya están instalados. Instale con
``bin/fess-setup install plugin``, como se indica en las secciones anteriores, los plugins que
sustituyen a partes eliminadas de la distribución en 15.9, como ``fess-script-groovy``.

Si utiliza ``FESS_PLUGINS`` en la versión Docker, actualice la parte de la versión, por ejemplo a
``fess-ds-wikipedia:15.9.0``.

Procedimientos de Reversión
=============================

Si la actualización falla, puede revertir con los siguientes procedimientos.

Paso 1: Detención de la Nueva Versión
--------------------------------------

::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Paso 2: Restauración de la Versión Antigua
-------------------------------------------

Restaure los archivos de configuración y datos desde el respaldo.

Para versión RPM/DEB::

    $ sudo rpm -Uvh --oldpackage fess-<old-version>.rpm

O::

    $ sudo dpkg -i fess-<old-version>.deb

Paso 3: Restauración de Datos
------------------------------

Restaure desde instantánea::

    $ curl -X POST "http://localhost:9200/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true"

O restaure el directorio desde el respaldo::

    $ sudo systemctl stop opensearch
    $ sudo rm -rf /var/lib/opensearch/data/*
    $ sudo tar xzf /backup/opensearch-data-backup.tar.gz -C /
    $ sudo systemctl start opensearch

En la versión Docker, vuelva al archivo Compose de la versión anterior y restaure el contenido
de los volúmenes::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down
    $ PROJECT=$(basename "$(pwd)")
    $ docker run --rm -v ${PROJECT}_search01_data:/data -v $(pwd):/backup ubuntu \
        sh -c "rm -rf /data/* && tar xzf /backup/search01-data-backup.tar.gz -C /"
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   Los datos de configuración descargados desde la pantalla de administración pueden reimportarse
   desde la función de carga en la página "Información del sistema" → "Copia de seguridad" después
   de iniciar |Fess|. Solo se pueden cargar archivos ``*.bulk``, archivos ``*.properties`` que
   comiencen con ``system``, archivos ``*.xml`` que comiencen con ``gsa``, archivos ``*.json`` que
   comiencen con ``fess`` y archivos ``*.json`` que comiencen con ``doc``, y solo un archivo por
   operación. Los archivos ``*.ndjson``, como los registros de búsqueda, no se aceptan y producen
   un error.

.. warning::

   Cargar ``fess.json`` y ``doc.json`` sobrescribe los propios archivos de definición de índice
   incluidos con |Fess|. Si después de la actualización carga la versión antigua de ``fess.json``
   o ``doc.json``, se perderán la configuración y el mapeo del índice de la nueva versión. No los
   cargue salvo con fines de reversión.

.. note::

   El archivo ``system.properties`` cargado se lee únicamente en memoria y no se escribe en disco.
   Por lo tanto, su contenido se pierde al reiniciar |Fess|. Para restaurarlo de forma fiable,
   coloque directamente el archivo respaldado en su ubicación correspondiente (``app/WEB-INF/conf/``
   en la versión ZIP, ``/etc/fess/`` en la versión RPM/DEB) antes de iniciar el servicio.

.. note::

   La importación se ejecuta de forma asíncrona y la pantalla solo muestra que se inició el
   proceso. Para confirmar si realmente se completó con éxito, consulte ``fess.log``.

Paso 4: Inicio y Verificación del Servicio
-------------------------------------------

::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Verifique el funcionamiento y confirme que volvió a la normalidad.

Preguntas Frecuentes
====================

P: ¿Se puede actualizar sin tiempo de inactividad?
---------------------------------------------------

R: La actualización de Fess requiere la detención del servicio. Para minimizar el tiempo de inactividad, considere:

- Verificar los procedimientos con anticipación en un entorno de prueba
- Hacer el respaldo con anticipación
- Asegurar suficiente tiempo de mantenimiento

P: ¿Es necesario actualizar también OpenSearch?
------------------------------------------------

R: Cada versión de |Fess| requiere una versión específica de OpenSearch.
|Fess| 15.9 es compatible con OpenSearch 3.8.0.
Los plugins de OpenSearch para |Fess|, como ``opensearch-analysis-fess``, deben coincidir exactamente con
la versión de OpenSearch; por lo tanto, si actualiza OpenSearch, actualice también los plugins a la
versión correspondiente (3.8.0).

Tenga en cuenta que |Fess| 15.9 requiere el plugin k-NN y siempre envía
``knn.derived_source.enabled`` en la configuración del índice. Con un OpenSearch antiguo, la
creación de nuevos índices fallará, por lo que en la práctica es necesario actualizar OpenSearch.
Para más detalles, consulte el Paso 4.

P: ¿Es necesario recrear el índice?
------------------------------------

R: Para una actualización de versión menor de |Fess| (15.x → 15.9) en la que no se utilice la
búsqueda por vector de chunks, generalmente no es necesario. El índice existente puede seguir
utilizándose tal cual, y como ``content_chunker.enabled`` y otras opciones similares están
deshabilitadas de forma predeterminada, el comportamiento no cambia.

En los siguientes casos sí es necesario recrear el índice y reindexar:

- **Si habilita recién la búsqueda por vector de chunks (búsqueda semántica)**: el índice
  existente no adopta el nuevo mapeo, por lo que la reindexación es obligatoria. Para más
  detalles, consulte :ref:`semantic-search-migration` (:doc:`../config/search-semantic`).
- **Si actualiza desde 14.x**: dado que OpenSearch pasa de la serie 2.x a la 3.x (actualización
  de versión principal), se recomienda recrear el índice.

.. warning::

   Las operaciones que crean un índice nuevo (incluida la reindexación) fallarán en un OpenSearch
   sin el plugin k-NN. Consulte las notas del Paso 4.

P: Después de la actualización, no se muestran los resultados de búsqueda
--------------------------------------------------------------------------

R: Verifique lo siguiente:

1. Verifique que OpenSearch esté en ejecución
2. Verifique que exista el índice (``curl http://localhost:9200/_cat/indices``)
3. Vuelva a ejecutar el rastreo

Próximos Pasos
==============

Una vez completada la actualización:

- :doc:`run` - Verificación de inicio y configuración inicial
- :doc:`security` - Revisión de configuración de seguridad
- :doc:`../config/search-semantic` - Configuración y pasos de migración de la búsqueda por
  vector de chunks (búsqueda semántica)
- Verifique las notas de lanzamiento para nuevas funciones
