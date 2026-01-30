==========================
API Backup
==========================

Vue d'ensemble
==============

L'API Backup permet de sauvegarder et restaurer les donnees de configuration de |Fess|.
Vous pouvez exporter et importer les configurations de crawl, les utilisateurs, les roles, les dictionnaires, etc.

URL de base
===========

::

    /api/admin/backup

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Chemin
     - Description
   * - GET
     - /export
     - Exportation des donnees de configuration
   * - POST
     - /import
     - Importation des donnees de configuration

Exportation des donnees de configuration
========================================

Requete
-------

::

    GET /api/admin/backup/export

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``types``
     - String
     - Non
     - Elements a exporter (separes par des virgules, par defaut : all)

Types d'exportation
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Type
     - Description
   * - ``webconfig``
     - Configuration de crawl Web
   * - ``fileconfig``
     - Configuration de crawl de fichiers
   * - ``dataconfig``
     - Configuration datastore
   * - ``scheduler``
     - Configuration du planificateur
   * - ``user``
     - Configuration des utilisateurs
   * - ``role``
     - Configuration des roles
   * - ``group``
     - Configuration des groupes
   * - ``labeltype``
     - Configuration des types de labels
   * - ``keymatch``
     - Configuration Key Match
   * - ``dict``
     - Donnees de dictionnaire
   * - ``all``
     - Toutes les configurations (par defaut)

Reponse
-------

Donnees binaires (format ZIP)

Content-Type: ``application/zip``
Content-Disposition: ``attachment; filename="fess-backup-20250129-100000.zip"``

Contenu du fichier ZIP
~~~~~~~~~~~~~~~~~~~~~~

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

Importation des donnees de configuration
========================================

Requete
-------

::

    POST /api/admin/backup/import
    Content-Type: multipart/form-data

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    --boundary
    Content-Disposition: form-data; name="file"; filename="fess-backup.zip"
    Content-Type: application/zip

    [donnees binaires]
    --boundary
    Content-Disposition: form-data; name="overwrite"

    true
    --boundary--

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``file``
     - Oui
     - Fichier ZIP de sauvegarde
   * - ``overwrite``
     - Non
     - Ecraser les configurations existantes (par defaut : false)
   * - ``types``
     - Non
     - Elements a importer (separes par des virgules, par defaut : all)

Reponse
-------

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

Exemples d'utilisation
======================

Exportation de toutes les configurations
----------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/export" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess-backup.zip

Exportation de configurations specifiques
-----------------------------------------

.. code-block:: bash

    # Exporter uniquement les configurations de crawl Web et les utilisateurs
    curl -X GET "http://localhost:8080/api/admin/backup/export?types=webconfig,user" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess-backup-partial.zip

Importation de configurations
-----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "overwrite=false"

Importation avec ecrasement des configurations existantes
---------------------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "overwrite=true"

Importation de configurations specifiques uniquement
----------------------------------------------------

.. code-block:: bash

    # Importer uniquement les utilisateurs et les roles
    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "types=user,role" \
         -F "overwrite=false"

Automatisation des sauvegardes
------------------------------

.. code-block:: bash

    #!/bin/bash
    # Exemple de script pour effectuer une sauvegarde quotidienne a 2h du matin

    DATE=$(date +%Y%m%d)
    BACKUP_DIR="/backup/fess"

    curl -X GET "http://localhost:8080/api/admin/backup/export" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o "${BACKUP_DIR}/fess-backup-${DATE}.zip"

    # Supprimer les sauvegardes de plus de 30 jours
    find "${BACKUP_DIR}" -name "fess-backup-*.zip" -mtime +30 -delete

Notes importantes
=================

- Les sauvegardes contiennent des informations de mot de passe, conservez-les de maniere securisee
- Specifier ``overwrite=true`` lors de l'importation ecrasera les configurations existantes
- L'exportation/importation de configurations volumineuses peut prendre du temps
- L'importation entre des versions differentes de Fess peut causer des problemes de compatibilite

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`../../admin/backup-guide` - Guide de gestion des sauvegardes
- :doc:`../../admin/maintenance-guide` - Guide de maintenance
