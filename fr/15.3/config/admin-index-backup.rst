========================
Gestion des index
========================

Aperçu
====

Les données gérées par |Fess| sont stockées sous forme d'index OpenSearch.
La sauvegarde et la restauration des index de recherche sont essentielles pour une exploitation stable du système.
Cette section explique les procédures de sauvegarde, de restauration et de migration des index.

Structure des index
==================

|Fess| utilise les index suivants.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Nom de l'index
     - Description
   * - ``fess.{date}``
     - Index des documents à rechercher (créé quotidiennement)
   * - ``fess_log``
     - Journaux de recherche et de clics
   * - ``fess_user``
     - Informations utilisateur
   * - ``fess_config``
     - Informations de configuration système
   * - ``configsync``
     - Informations de synchronisation de configuration

Sauvegarde et restauration des index
====================================

Vous pouvez effectuer des sauvegardes et des restaurations d'index en utilisant la fonctionnalité de snapshot d'OpenSearch.

Configuration du référentiel de snapshots
--------------------------------

Tout d'abord, configurez un référentiel pour stocker les données de sauvegarde.

**Pour un référentiel de système de fichiers :**

1. Ajoutez le chemin du référentiel au fichier de configuration d'OpenSearch (``config/opensearch.yml``).

::

    path.repo: ["/var/opensearch/backup"]

2. Redémarrez OpenSearch.

3. Enregistrez le référentiel.

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
   Dans la configuration par défaut de |Fess|, OpenSearch démarre sur le port 9201.

**Pour un référentiel AWS S3 :**

Pour utiliser S3 comme destination de sauvegarde, installez et configurez le plugin ``repository-s3``.

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

Création de snapshots (sauvegarde)
------------------------------------

Sauvegarde de tous les index
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sauvegarder tous les index.

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_1?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Sauvegarde d'index spécifiques
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sauvegarder uniquement des index spécifiques.

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_fess_only?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.*,fess_config",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Sauvegarde automatique régulière
~~~~~~~~~~~~~~~~~~~~~~~~

Vous pouvez exécuter des sauvegardes régulières en utilisant cron ou similaire.

::

    #!/bin/bash
    DATE=$(date +%Y%m%d_%H%M%S)
    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_${DATE}?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Vérification des snapshots
----------------------

Vérifier la liste des snapshots créés.

::

    curl -X GET "localhost:9201/_snapshot/fess_backup/_all?pretty"

Vérifier les détails d'un snapshot spécifique.

::

    curl -X GET "localhost:9201/_snapshot/fess_backup/snapshot_1?pretty"

Restauration à partir de snapshots
------------------------------

Restauration de tous les index
~~~~~~~~~~~~~~~~~~~~~~~~

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Restauration d'index spécifiques
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Restauration avec renommage de l'index
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Vous pouvez également modifier le nom de l'index lors de la restauration.

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101",
      "rename_pattern": "fess.(.+)",
      "rename_replacement": "restored_fess.$1",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Suppression de snapshots
----------------------

Vous pouvez supprimer d'anciens snapshots pour économiser de l'espace de stockage.

::

    curl -X DELETE "localhost:9201/_snapshot/fess_backup/snapshot_1"

Sauvegarde des fichiers de configuration
==========================

Outre les index OpenSearch, sauvegardez également les fichiers de configuration suivants.

Fichiers à sauvegarder
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Fichier/Répertoire
     - Description
   * - ``app/WEB-INF/conf/system.properties``
     - Configuration système (installation zip)
   * - ``/etc/fess/system.properties``
     - Configuration système (paquets RPM/DEB)
   * - ``app/WEB-INF/classes/fess_config.properties``
     - Configuration détaillée de Fess
   * - ``/etc/fess/fess_config.properties``
     - Configuration détaillée de Fess (paquets RPM/DEB)
   * - ``app/WEB-INF/classes/log4j2.xml``
     - Configuration des journaux
   * - ``/etc/fess/log4j2.xml``
     - Configuration des journaux (paquets RPM/DEB)
   * - ``app/WEB-INF/classes/fess_indices/``
     - Fichiers de définition d'index
   * - ``thumbnail/``
     - Images miniatures (si nécessaire)

Exemple de sauvegarde des fichiers de configuration
----------------------------

::

    #!/bin/bash
    BACKUP_DIR="/backup/fess/$(date +%Y%m%d_%H%M%S)"
    mkdir -p ${BACKUP_DIR}

    # Copie des fichiers de configuration
    cp -r /etc/fess/ ${BACKUP_DIR}/
    cp -r /var/lib/fess/app/WEB-INF/conf/ ${BACKUP_DIR}/
    cp -r /var/lib/fess/app/WEB-INF/classes/fess_indices/ ${BACKUP_DIR}/

    # Option : Images miniatures
    # cp -r /var/lib/fess/thumbnail/ ${BACKUP_DIR}/

    echo "Backup completed: ${BACKUP_DIR}"

Migration de données
==========

Procédure de migration vers un autre environnement
------------------

1. **Créer une sauvegarde sur l'environnement source**

   - Créez un snapshot OpenSearch.
   - Sauvegardez les fichiers de configuration.

2. **Préparer l'environnement de destination**

   - Installez |Fess| dans le nouvel environnement.
   - Démarrez OpenSearch.

3. **Restaurer les fichiers de configuration**

   - Copiez les fichiers de configuration sauvegardés dans le nouvel environnement.
   - Modifiez les chemins, noms d'hôte, etc. si nécessaire.

4. **Restaurer les index**

   - Configurez le référentiel de snapshots.
   - Restaurez les index à partir du snapshot.

5. **Vérifier le fonctionnement**

   - Démarrez |Fess|.
   - Accédez à l'interface d'administration et vérifiez la configuration.
   - Vérifiez que la fonction de recherche fonctionne correctement.

Précautions lors de la mise à niveau de version
----------------------------

Lors de la migration de données entre différentes versions de |Fess|, prenez en compte les points suivants.

- Si la version majeure d'OpenSearch est différente, des problèmes de compatibilité peuvent survenir.
- Si la structure de l'index a été modifiée, une réindexation peut être nécessaire.
- Pour plus de détails, consultez le guide de mise à niveau de chaque version.

Dépannage
======================

Échec de la création de snapshot
--------------------------------

1. Vérifiez les permissions pour le chemin du référentiel.
2. Vérifiez qu'il y a suffisamment d'espace disque.
3. Vérifiez les messages d'erreur dans les fichiers journaux d'OpenSearch.

Échec de la restauration
------------------

1. Vérifiez qu'un index du même nom n'existe pas déjà.
2. Vérifiez que la version d'OpenSearch est compatible.
3. Vérifiez que le snapshot n'est pas corrompu.

Impossible de rechercher après la restauration
------------------------

1. Vérifiez que l'index a été restauré correctement : ``curl -X GET "localhost:9201/_cat/indices?v"``
2. Vérifiez qu'il n'y a pas d'erreurs dans les fichiers journaux de |Fess|.
3. Vérifiez que les fichiers de configuration sont correctement restaurés.

Informations de référence
========

Pour des informations détaillées, consultez la documentation officielle d'OpenSearch.

- `Fonctionnalité de snapshot <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`_
- `Configuration de référentiel <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/>`_
- `Référentiel S3 <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/plugins/#s3-repository>`_
