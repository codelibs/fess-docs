==================
Gestión de Índices
==================

Descripción General
===================

Los datos gestionados por |Fess| se almacenan como índices de OpenSearch.
El respaldo y la restauración de los índices de búsqueda son esenciales para la operación estable del sistema.
Esta sección describe los procedimientos de respaldo, restauración y migración de índices mediante la funcionalidad de instantáneas de OpenSearch.

.. note::
   Además del respaldo de índices mediante instantáneas de OpenSearch descrito en esta sección, |Fess| también ofrece una función para exportar/importar información de configuración (configuración de rastreo, información de usuarios, configuración del sistema, etc.) desde la pantalla de administración. Si desea respaldar o migrar únicamente la información de configuración, consulte :doc:`../admin/backup-guide`. Las instantáneas de OpenSearch son adecuadas para realizar un respaldo físico completo de los índices, incluidos los documentos de búsqueda.

Estructura de Índices
======================

|Fess| utiliza los siguientes índices:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Nombre del Índice
     - Descripción
   * - ``fess.{marca_de_tiempo}``
     - Índice de documentos de búsqueda. Se crea con el formato ``fess.{yyyyMMddHHmmssSSS}`` (marca de tiempo con precisión de milisegundos) al reconstruir el índice, y se referencia mediante los alias ``fess.search`` (para búsqueda) y ``fess.update`` (para actualización).
   * - ``fess_config.*``
     - Información de configuración del sistema (compuesto por múltiples subíndices como ``fess_config.web_config``, ``fess_config.scheduled_job``, ``fess_config.data_config``, entre otros)
   * - ``fess_user.*``
     - Información de usuarios (``fess_user.user``, ``fess_user.role``, ``fess_user.group``)
   * - ``fess_log.*``
     - Registros de búsqueda, clics y otros (``fess_log.search_log``, ``fess_log.click_log``, ``fess_log.favorite_log``, ``fess_log.user_info``, ``fess_log.notification_queue``)
   * - ``fess_crawler.*``
     - Índices temporales utilizados durante el proceso de rastreo (``fess_crawler.queue``, ``fess_crawler.data``, ``fess_crawler.filter``). No son necesarios una vez completado el rastreo, por lo que normalmente no es preciso incluirlos en el respaldo.

Respaldo y Restauración de Índices
====================================

Puede realizar el respaldo y la restauración de índices utilizando la funcionalidad de instantáneas de OpenSearch.

Configuración del Repositorio de Instantáneas
----------------------------------------------

Primero, configure un repositorio para almacenar los datos de respaldo.

**Para repositorio del sistema de archivos:**

1. Agregue la ruta del repositorio al archivo de configuración de OpenSearch (``opensearch.yml``).

::

    path.repo: ["/var/opensearch/backup"]

2. Reinicie OpenSearch.

3. Registre el repositorio.

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup" -H 'Content-Type: application/json' -d'
    {
      "type": "fs",
      "settings": {
        "location": "/var/opensearch/backup",
        "compress": true
      }
    }'

.. note::
   En la configuración predeterminada de la versión zip/tar.gz de |Fess|, OpenSearch se inicia en el puerto 9201 (``search_engine.http.url`` en ``fess_config.properties``). En la versión de paquete RPM/DEB, la conexión está configurada por defecto al puerto 9200 (``SEARCH_ENGINE_HTTP_URL`` en el archivo de configuración de entorno ``/etc/sysconfig/fess`` (RPM) o ``/etc/default/fess`` (DEB)). Ajuste el número de puerto según su entorno.

**Para repositorio AWS S3:**

Si utiliza S3 como destino de respaldo, instale y configure el plugin ``repository-s3``.

::

    curl -X PUT "localhost:9201/_snapshot/fess_s3_backup" -H 'Content-Type: application/json' -d'
    {
      "type": "s3",
      "settings": {
        "bucket": "my-fess-backup-bucket",
        "region": "ap-northeast-1",
        "base_path": "fess-snapshots"
      }
    }'

Creación de Instantáneas (Respaldo)
------------------------------------

Respaldo de Todos los Índices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Respalda todos los índices.

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_1?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Respaldo de Índices Específicos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Respalda solo índices específicos. El siguiente es un ejemplo que tiene como objetivo únicamente los índices relacionados con |Fess| (índices que comienzan con ``fess``).

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_fess_only?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Respaldo Automático Periódico
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Puede ejecutar respaldos periódicos utilizando cron u otras herramientas.

::

    #!/bin/bash
    DATE=$(date +%Y%m%d_%H%M%S)
    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_${DATE}?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Verificación de Instantáneas
------------------------------

Verifique la lista de instantáneas creadas.

::

    curl -X GET "localhost:9201/_snapshot/fess_backup/_all?pretty"

Verifique los detalles de una instantánea específica.

::

    curl -X GET "localhost:9201/_snapshot/fess_backup/snapshot_1?pretty"

Restauración desde Instantáneas
---------------------------------

Restauración de Todos los Índices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Restauración de Índices Específicos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El nombre del índice de documentos de búsqueda tiene el formato ``fess.{yyyyMMddHHmmssSSS}``. Verifique el nombre real del índice mediante ``_cat/indices`` u otro método antes de restaurar.

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101000000000",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Restauración con Cambio de Nombre de Índice
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

También puede cambiar el nombre del índice durante la restauración.

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101000000000",
      "rename_pattern": "fess\\.(.+)",
      "rename_replacement": "restored_fess.$1",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

.. note::
   Cuando restaure el índice de documentos de búsqueda (``fess.{marca_de_tiempo}``), asegúrese de que los alias ``fess.search`` y ``fess.update`` apunten al índice restaurado. Dado que las instantáneas incluyen también la información de alias, si restaura todos los índices con sus nombres originales, los alias normalmente también se restauran. Sin embargo, si restauró con un nombre distinto mediante ``rename_pattern``, o si migró a otro clúster, es posible que los alias no queden configurados correctamente. En ese caso, vuelva a configurar los alias manualmente como se muestra a continuación (reemplace el nombre del índice por el real).

   ::

       curl -X POST "localhost:9201/_aliases" -H 'Content-Type: application/json' -d'
       {
         "actions": [
           { "add": { "index": "restored_fess.20250101000000000", "alias": "fess.search" } },
           { "add": { "index": "restored_fess.20250101000000000", "alias": "fess.update" } }
         ]
       }'

Eliminación de Instantáneas
-----------------------------

Puede eliminar instantáneas antiguas para ahorrar capacidad de almacenamiento.

::

    curl -X DELETE "localhost:9201/_snapshot/fess_backup/snapshot_1"

Respaldo de Archivos de Configuración
========================================

Además de los índices de OpenSearch, también debe respaldar los siguientes archivos de configuración. La ubicación de los archivos de configuración varía según el método de instalación.

Archivos a Respaldar
---------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Archivo/Directorio
     - Método de instalación
     - Descripción
   * - ``app/WEB-INF/conf/system.properties``
     - zip/tar.gz
     - Configuración del sistema (configuración general)
   * - ``/etc/fess/system.properties``
     - RPM/DEB
     - Configuración del sistema (configuración general)
   * - ``app/WEB-INF/classes/fess_config.properties``
     - zip/tar.gz
     - Configuración detallada de |Fess|
   * - ``/etc/fess/fess_config.properties``
     - RPM/DEB
     - Configuración detallada de |Fess|
   * - ``app/WEB-INF/classes/log4j2.xml``
     - zip/tar.gz
     - Configuración de registros
   * - ``/usr/share/fess/app/WEB-INF/classes/log4j2.xml``
     - RPM/DEB
     - Configuración de registros
   * - ``app/WEB-INF/classes/fess_indices/``
     - zip/tar.gz
     - Archivos de definición de índices
   * - ``/usr/share/fess/app/WEB-INF/classes/fess_indices/``
     - RPM/DEB
     - Archivos de definición de índices
   * - ``app/WEB-INF/thumbnails/``
     - zip/tar.gz
     - Imágenes de miniaturas (según sea necesario)
   * - ``/var/lib/fess/thumbnails/``
     - RPM/DEB
     - Imágenes de miniaturas (según sea necesario)

.. note::
   En la versión de paquete RPM/DEB, el directorio ``/etc/fess/`` contiene, además de ``fess_config.properties``, otros archivos de configuración como ``fess_env_crawler.properties`` y otros archivos ``fess_env_*.properties``, así como ``tika.xml``. Se recomienda respaldar el directorio ``/etc/fess/`` completo. El archivo ``system.properties`` se crea y actualiza como ``/etc/fess/system.properties`` cuando se guarda la configuración en "Sistema > General" de la pantalla de administración.

Ejemplo de Respaldo de Archivos de Configuración
--------------------------------------------------

El siguiente es un ejemplo de respaldo de archivos de configuración para la versión de paquete RPM/DEB.

::

    #!/bin/bash
    BACKUP_DIR="/backup/fess/$(date +%Y%m%d_%H%M%S)"
    mkdir -p ${BACKUP_DIR}

    # Copiar archivos de configuración (incluye system.properties, fess_config.properties, etc.)
    cp -r /etc/fess/ ${BACKUP_DIR}/

    # Archivos de definición de índices y configuración de registros
    cp -r /usr/share/fess/app/WEB-INF/classes/fess_indices/ ${BACKUP_DIR}/
    cp /usr/share/fess/app/WEB-INF/classes/log4j2.xml ${BACKUP_DIR}/

    # Opcional: imágenes de miniaturas
    # cp -r /var/lib/fess/thumbnails/ ${BACKUP_DIR}/

    echo "Backup completed: ${BACKUP_DIR}"

Migración de Datos
==================

Procedimiento de Migración a Otro Entorno
------------------------------------------

1. **Creación del respaldo en el origen**

   - Cree una instantánea de OpenSearch.
   - Respalde los archivos de configuración.

2. **Preparación del destino**

   - Instale |Fess| en el nuevo entorno.
   - Inicie OpenSearch.

3. **Restauración de archivos de configuración**

   - Copie los archivos de configuración respaldados al nuevo entorno.
   - Modifique rutas, nombres de host, etc., según sea necesario.

4. **Restauración de índices**

   - Configure el repositorio de instantáneas.
   - Restaure los índices desde la instantánea.
   - Tras la restauración, verifique que los alias ``fess.search`` y ``fess.update`` apunten al índice restaurado.

5. **Verificación de funcionamiento**

   - Inicie |Fess|.
   - Acceda a la pantalla de administración y verifique la configuración.
   - Verifique que la funcionalidad de búsqueda opere correctamente.

Consideraciones para Actualizaciones de Versión
-------------------------------------------------

Al migrar datos entre diferentes versiones de |Fess|, tenga en cuenta lo siguiente:

- Si la versión principal de OpenSearch es diferente, pueden surgir problemas de compatibilidad.
- Si la estructura del índice ha cambiado, puede ser necesario reindexar.
- Si desea migrar información de configuración entre versiones con cambios en la estructura del índice, considere utilizar la función de respaldo de la pantalla de administración (:doc:`../admin/backup-guide`) para realizar una exportación/importación lógica en lugar de instantáneas de OpenSearch.
- Consulte la guía de actualización de cada versión para obtener más detalles.

Solución de Problemas
======================

Falla en la Creación de Instantáneas
--------------------------------------

1. Verifique los permisos de acceso a la ruta del repositorio.
2. Confirme que haya suficiente espacio en disco.
3. Revise los archivos de registro de OpenSearch para mensajes de error.

Falla en la Restauración
--------------------------

1. Verifique que no exista ya un índice con el mismo nombre. En OpenSearch no es posible restaurar sobre un índice con el mismo nombre que esté abierto. Antes de restaurar, cierre (``_close``) o elimine el índice en cuestión, o bien restáurelo con un nombre diferente mediante ``rename_pattern``.
2. Confirme que la versión de OpenSearch sea compatible.
3. Verifique que la instantánea no esté dañada.

No es Posible Buscar Después de la Restauración
-------------------------------------------------

1. Verifique que los índices se hayan restaurado correctamente: ``curl -X GET "localhost:9201/_cat/indices?v"``
2. Verifique que los alias ``fess.search`` y ``fess.update`` apunten al índice restaurado: ``curl -X GET "localhost:9201/_cat/aliases?v"``. Si los alias no están configurados, vuelva a configurarlos mediante la API ``_aliases``.
3. Revise los archivos de registro de |Fess| para detectar errores.
4. Confirme que los archivos de configuración se hayan restaurado correctamente.

Temas Relacionados
==================

- :doc:`../admin/backup-guide` - Respaldo/restauración de información de configuración desde la pantalla de administración
- :doc:`admin-index-export` - Función de exportación de índices
- :doc:`admin-logging` - Configuración de registros

Información de Referencia
==========================

Para información detallada, consulte la documentación oficial de OpenSearch.

- `Funcionalidad de instantáneas <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`_
- `Configuración de repositorio <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/>`_
- `Repositorio S3 <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/plugins/#s3-repository>`_
