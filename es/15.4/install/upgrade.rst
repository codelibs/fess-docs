==========================
Procedimientos de Actualización
==========================

Esta página describe los procedimientos para actualizar |Fess| de versiones anteriores a la versión más reciente.

.. warning::

   **Notas Importantes Antes de la Actualización**

   - Asegúrese de hacer un respaldo antes de la actualización
   - Se recomienda encarecidamente validar la actualización en un entorno de prueba con anticipación
   - El servicio se detendrá durante la actualización, por lo que configure un tiempo de mantenimiento apropiado
   - Dependiendo de la versión, el formato del archivo de configuración puede haber cambiado

Versiones Compatibles
======================

Estos procedimientos de actualización son compatibles con actualizaciones entre las siguientes versiones:

- Fess 14.x → Fess 15.4
- Fess 15.x → Fess 15.4

.. note::

   Si actualiza desde versiones más antiguas (13.x o anteriores), puede ser necesaria una actualización gradual.
   Para más detalles, verifique las notas de lanzamiento.

Preparación Antes de la Actualización
======================================

Verificación de Compatibilidad de Versiones
--------------------------------------------

Verifique la compatibilidad entre la versión de destino de actualización y la versión actual.

- `Notas de Lanzamiento <https://github.com/codelibs/fess/releases>`__
- `Guía de Actualización <https://fess.codelibs.org/ja/>`__

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
-----------------------------------

1. **Respaldo desde la pantalla de administración**

   Inicie sesión en la pantalla de administración y haga clic en "Sistema" → "Respaldo".

   Descargue los siguientes archivos:

   - ``fess_basic_config.bulk``
   - ``fess_user.bulk``

2. **Respaldo de archivos de configuración**

   Versión TAR.GZ/ZIP::

       $ cp /path/to/fess/app/WEB-INF/conf/system.properties /backup/
       $ cp /path/to/fess/app/WEB-INF/classes/fess_config.properties /backup/

   Versión RPM/DEB::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/

3. **Archivos de configuración personalizados**

   Si tiene archivos de configuración personalizados, también haga un respaldo de ellos::

       $ cp /path/to/fess/app/WEB-INF/classes/log4j2.xml /backup/

Respaldo de Datos de Índice
----------------------------

Haga un respaldo de los datos de índice de OpenSearch.

Método 1: Usar Función de Instantánea (Recomendado)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use la función de instantánea de OpenSearch para hacer un respaldo del índice.

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

Haga un respaldo de los volúmenes Docker::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ docker run --rm -v fess-es-data:/data -v $(pwd):/backup ubuntu tar czf /backup/fess-es-data-backup.tar.gz /data
    $ docker run --rm -v fess-data:/data -v $(pwd):/backup ubuntu tar czf /backup/fess-data-backup.tar.gz /data
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml start

Paso 2: Detención de la Versión Actual
=======================================

Detenga Fess y OpenSearch.

Versión TAR.GZ/ZIP::

    $ kill <fess_pid>
    $ kill <opensearch_pid>

Versión RPM/DEB (systemd)::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Versión Docker::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Paso 3: Instalación de la Nueva Versión
========================================

Los procedimientos varían según el método de instalación.

Versión TAR.GZ/ZIP
------------------

1. Descargue y extraiga la nueva versión::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.4.0/fess-15.4.0.tar.gz
       $ tar -xzf fess-15.4.0.tar.gz

2. Copie la configuración de la versión antigua::

       $ cp /path/to/old-fess/app/WEB-INF/conf/system.properties /path/to/fess-15.4.0/app/WEB-INF/conf/
       $ cp /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.4.0/bin/

3. Verifique las diferencias de configuración y ajuste según sea necesario

Versión RPM/DEB
---------------

Instale el paquete de la nueva versión::

    # RPM
    $ sudo rpm -Uvh fess-15.4.0.rpm

    # DEB
    $ sudo dpkg -i fess-15.4.0.deb

.. note::

   Los archivos de configuración (``/etc/fess/*``) se conservan automáticamente.
   Sin embargo, si se han agregado nuevas opciones de configuración, es necesario ajustarlas manualmente.

Versión Docker
--------------

1. Obtenga el archivo Compose de la nueva versión::

       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.4.0/compose/compose.yaml
       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.4.0/compose/compose-opensearch3.yaml

2. Obtenga la nueva imagen::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

Paso 4: Actualización de OpenSearch (Si es Necesario)
======================================================

Si también actualiza OpenSearch, siga estos procedimientos.

.. warning::

   Realice con cuidado las actualizaciones de versión principal de OpenSearch.
   Pueden surgir problemas de compatibilidad del índice.

1. Instale la nueva versión de OpenSearch

2. Reinstale los plugins::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.1

3. Inicie OpenSearch::

       $ sudo systemctl start opensearch.service

Paso 5: Inicio de la Nueva Versión
===================================

Versión TAR.GZ/ZIP::

    $ cd /path/to/fess-15.4.0
    $ ./bin/fess -d

Versión RPM/DEB::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Versión Docker::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Paso 6: Verificación de Funcionamiento
=======================================

1. **Verificación de registros**

   Verifique que no haya errores::

       $ tail -f /path/to/fess/logs/fess.log

2. **Acceso a la interfaz Web**

   Acceda a http://localhost:8080/ desde el navegador.

3. **Inicio de sesión en la pantalla de administración**

   Acceda a http://localhost:8080/admin e inicie sesión con la cuenta de administrador.

4. **Verificación de información del sistema**

   Haga clic en "Sistema" → "Información del Sistema" en la pantalla de administración y verifique que la versión se haya actualizado.

5. **Verificación de funcionamiento de búsqueda**

   Ejecute una búsqueda en la pantalla de búsqueda y verifique que se devuelvan resultados normalmente.

Paso 7: Recreación del Índice (Recomendado)
============================================

Para actualizaciones de versión principal, se recomienda recrear el índice.

1. Verifique los programas de rastreo existentes
2. Ejecute "Default Crawler" desde "Sistema" → "Programador"
3. Espere hasta que se complete el rastreo
4. Verifique los resultados de búsqueda

Procedimientos de Reversión
============================

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

R: Dependiendo de la versión de Fess, se requiere una versión específica de OpenSearch.
Verifique la versión recomendada de OpenSearch en las notas de lanzamiento.

P: ¿Es necesario recrear el índice?
------------------------------------

R: Generalmente no es necesario para actualizaciones de versión menor, pero se recomienda la recreación para actualizaciones de versión principal.

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
- Verifique las notas de lanzamiento para nuevas funciones
