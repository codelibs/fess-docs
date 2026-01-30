==========================
API de Backup
==========================

Vision General
==============

La API de Backup es para realizar copias de seguridad y restauracion de datos de configuracion de |Fess|.
Puede exportar e importar configuraciones de rastreo, usuarios, roles, diccionarios y otras configuraciones.

URL Base
========

::

    /api/admin/backup

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Metodo
     - Ruta
     - Descripcion
   * - GET
     - /export
     - Exportar datos de configuracion
   * - POST
     - /import
     - Importar datos de configuracion

Exportar Datos de Configuracion
===============================

Solicitud
---------

::

    GET /api/admin/backup/export

Parametros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametro
     - Tipo
     - Requerido
     - Descripcion
   * - ``types``
     - String
     - No
     - Objetivos de exportacion (separados por coma, predeterminado: all)

Tipos de Exportacion
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Tipo
     - Descripcion
   * - ``webconfig``
     - Configuracion de rastreo web
   * - ``fileconfig``
     - Configuracion de rastreo de archivos
   * - ``dataconfig``
     - Configuracion de almacen de datos
   * - ``scheduler``
     - Configuracion de programador
   * - ``user``
     - Configuracion de usuarios
   * - ``role``
     - Configuracion de roles
   * - ``group``
     - Configuracion de grupos
   * - ``labeltype``
     - Configuracion de tipos de etiqueta
   * - ``keymatch``
     - Configuracion de coincidencia de claves
   * - ``dict``
     - Datos de diccionario
   * - ``all``
     - Todas las configuraciones (predeterminado)

Respuesta
---------

Datos binarios (formato ZIP)

Content-Type: ``application/zip``
Content-Disposition: ``attachment; filename="fess-backup-20250129-100000.zip"``

Contenido del Archivo ZIP
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    fess-backup-20250129-100000.zip
    ├── webconfig.json
    ├── fileconfig.json
    ├── dataconfig.json
    ├── scheduler.json
    ├── user.json
    ├── role.json
    ├── group.json
    ├── labeltype.json
    ├── keymatch.json
    ├── dict/
    │   ├── synonym.txt
    │   ├── mapping.txt
    │   └── protwords.txt
    └── metadata.json

Importar Datos de Configuracion
===============================

Solicitud
---------

::

    POST /api/admin/backup/import
    Content-Type: multipart/form-data

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    --boundary
    Content-Disposition: form-data; name="file"; filename="fess-backup.zip"
    Content-Type: application/zip

    [datos binarios]
    --boundary
    Content-Disposition: form-data; name="overwrite"

    true
    --boundary--

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripcion
   * - ``file``
     - Si
     - Archivo ZIP de copia de seguridad
   * - ``overwrite``
     - No
     - Sobrescribir configuracion existente (predeterminado: false)
   * - ``types``
     - No
     - Objetivos de importacion (separados por coma, predeterminado: all)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Backup imported successfully",
        "imported": {
          "webconfig": 5,
          "fileconfig": 3,
          "dataconfig": 2,
          "scheduler": 4,
          "user": 10,
          "role": 5,
          "group": 3,
          "labeltype": 8,
          "keymatch": 12,
          "dict": 3
        }
      }
    }

Ejemplos de Uso
===============

Exportar Todas las Configuraciones
----------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/export" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess-backup.zip

Exportar Configuraciones Especificas
------------------------------------

.. code-block:: bash

    # Exportar solo configuracion de rastreo web y usuarios
    curl -X GET "http://localhost:8080/api/admin/backup/export?types=webconfig,user" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess-backup-partial.zip

Importar Configuraciones
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "overwrite=false"

Importar Sobrescribiendo Configuraciones Existentes
---------------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "overwrite=true"

Importar Solo Configuraciones Especificas
-----------------------------------------

.. code-block:: bash

    # Importar solo usuarios y roles
    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "types=user,role" \
         -F "overwrite=false"

Automatizacion de Copias de Seguridad
-------------------------------------

.. code-block:: bash

    #!/bin/bash
    # Ejemplo de script para copia de seguridad diaria a las 2 AM

    DATE=$(date +%Y%m%d)
    BACKUP_DIR="/backup/fess"

    curl -X GET "http://localhost:8080/api/admin/backup/export" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o "${BACKUP_DIR}/fess-backup-${DATE}.zip"

    # Eliminar copias de seguridad de mas de 30 dias
    find "${BACKUP_DIR}" -name "fess-backup-*.zip" -mtime +30 -delete

Notas Importantes
=================

- Las copias de seguridad incluyen informacion de contrasenas, almacenelas de forma segura
- Al especificar ``overwrite=true`` durante la importacion, las configuraciones existentes seran sobrescritas
- Para configuraciones de gran escala, la exportacion/importacion puede llevar tiempo
- Pueden ocurrir problemas de compatibilidad al importar entre diferentes versiones de Fess

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`../../admin/backup-guide` - Guia de gestion de copias de seguridad
- :doc:`../../admin/maintenance-guide` - Guia de mantenimiento
