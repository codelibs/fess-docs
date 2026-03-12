==================
Gestión de Índices
==================

Descripción General
===================

Los datos gestionados por |Fess| se almacenan como índices de OpenSearch.
El respaldo y restauración de los índices de búsqueda son esenciales para la operación estable del sistema.
Esta sección describe los procedimientos de respaldo, restauración y migración de índices.

Estructura de Índices
======================

|Fess| utiliza los siguientes índices:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Nombre del Índice
     - Descripción
   * - ``fess.{fecha}``
     - Índice de documentos de búsqueda (creado diariamente)
   * - ``fess_log``
     - Registros de búsqueda y clics
   * - ``fess_user``
     - Información de usuarios
   * - ``fess_config``
     - Información de configuración del sistema
   * - ``configsync``
     - Información de sincronización de configuración

Respaldo y Restauración de Índices
===================================

Puede realizar el respaldo y restauración de índices utilizando la funcionalidad de instantáneas de OpenSearch.

Configuración del Repositorio de Instantáneas
----------------------------------------------

Primero, configure un repositorio para almacenar los datos de respaldo.

**Para repositorio del sistema de archivos:**

1. Agregue la ruta del repositorio al archivo de configuración de OpenSearch (``config/opensearch.yml``).

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
   En la configuración predeterminada de |Fess|, OpenSearch se inicia en el puerto 9201.

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

Respalda solo índices específicos.

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_fess_only?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.*,fess_config",
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
-----------------------------

Verifique la lista de instantáneas creadas.

::

    curl -X GET "localhost:9201/_snapshot/fess_backup/_all?pretty"

Verifique los detalles de una instantánea específica.

::

    curl -X GET "localhost:9201/_snapshot/fess_backup/snapshot_1?pretty"

Restauración desde Instantáneas
--------------------------------

Restauración de Todos los Índices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Restauración de Índices Específicos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Restauración con Cambio de Nombre de Índice
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

También puede cambiar el nombre del índice durante la restauración.

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101",
      "rename_pattern": "fess.(.+)",
      "rename_replacement": "restored_fess.$1",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Eliminación de Instantáneas
----------------------------

Puede eliminar instantáneas antiguas para ahorrar capacidad de almacenamiento.

::

    curl -X DELETE "localhost:9201/_snapshot/fess_backup/snapshot_1"

Respaldo de Archivos de Configuración
======================================

Además de los índices de OpenSearch, también debe respaldar los siguientes archivos de configuración.

Archivos a Respaldar
--------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Archivo/Directorio
     - Descripción
   * - ``app/WEB-INF/conf/system.properties``
     - Configuración del sistema (instalación ZIP)
   * - ``/etc/fess/system.properties``
     - Configuración del sistema (paquetes RPM/DEB)
   * - ``app/WEB-INF/classes/fess_config.properties``
     - Configuración detallada de Fess
   * - ``/etc/fess/fess_config.properties``
     - Configuración detallada de Fess (paquetes RPM/DEB)
   * - ``app/WEB-INF/classes/log4j2.xml``
     - Configuración de registros
   * - ``/etc/fess/log4j2.xml``
     - Configuración de registros (paquetes RPM/DEB)
   * - ``app/WEB-INF/classes/fess_indices/``
     - Archivos de definición de índices
   * - ``thumbnail/``
     - Imágenes de miniaturas (según sea necesario)

Ejemplo de Respaldo de Archivos de Configuración
-------------------------------------------------

::

    #!/bin/bash
    BACKUP_DIR="/backup/fess/$(date +%Y%m%d_%H%M%S)"
    mkdir -p ${BACKUP_DIR}

    # Copiar archivos de configuración
    cp -r /etc/fess/ ${BACKUP_DIR}/
    cp -r /var/lib/fess/app/WEB-INF/conf/ ${BACKUP_DIR}/
    cp -r /var/lib/fess/app/WEB-INF/classes/fess_indices/ ${BACKUP_DIR}/

    # Opcional: imágenes de miniaturas
    # cp -r /var/lib/fess/thumbnail/ ${BACKUP_DIR}/

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

5. **Verificación de funcionamiento**

   - Inicie |Fess|.
   - Acceda a la consola de administración y verifique la configuración.
   - Verifique que la funcionalidad de búsqueda opere correctamente.

Consideraciones para Actualizaciones de Versión
------------------------------------------------

Al migrar datos entre diferentes versiones de |Fess|, tenga en cuenta lo siguiente:

- Si la versión principal de OpenSearch es diferente, pueden surgir problemas de compatibilidad.
- Si la estructura del índice ha cambiado, puede ser necesario reindexar.
- Consulte la guía de actualización de cada versión para obtener más detalles.

Solución de Problemas
======================

Falla en la Creación de Instantáneas
-------------------------------------

1. Verifique los permisos de acceso a la ruta del repositorio.
2. Confirme que haya suficiente espacio en disco.
3. Revise los archivos de registro de OpenSearch para mensajes de error.

Falla en la Restauración
-------------------------

1. Verifique que no exista ya un índice con el mismo nombre.
2. Confirme que la versión de OpenSearch sea compatible.
3. Verifique que la instantánea no esté dañada.

No es Posible Buscar Después de la Restauración
------------------------------------------------

1. Verifique que los índices se hayan restaurado correctamente: ``curl -X GET "localhost:9201/_cat/indices?v"``
2. Revise los archivos de registro de |Fess| para detectar errores.
3. Confirme que los archivos de configuración se hayan restaurado correctamente.

Información de Referencia
==========================

Para información detallada, consulte la documentación oficial de OpenSearch.

- `Funcionalidad de instantáneas <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`_
- `Configuración de repositorio <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/>`_
- `Repositorio S3 <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/plugins/#s3-repository>`_
