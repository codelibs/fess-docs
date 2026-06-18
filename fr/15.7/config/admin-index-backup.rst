========================
Gestion des index
========================

Aperçu
======

Les données gérées par |Fess| sont stockées sous forme d'index OpenSearch.
La sauvegarde et la restauration des index de recherche sont essentielles pour une exploitation stable du système.
Cette section explique les procédures de sauvegarde, de restauration et de migration des index à l'aide de la fonctionnalité de snapshot d'OpenSearch.

.. note::
   Indépendamment de la sauvegarde des index par snapshot OpenSearch décrite dans cette section, |Fess| propose également une fonctionnalité d'export/import des informations de configuration (paramètres de crawl, informations utilisateur, paramètres système, etc.) depuis l'interface d'administration. Si vous souhaitez uniquement sauvegarder ou migrer des informations de configuration, consultez :doc:`../admin/backup-guide`. Les snapshots OpenSearch sont adaptés à la sauvegarde physique complète des index, y compris les documents de recherche.

Structure des index
===================

|Fess| utilise les index suivants.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Nom de l'index
     - Description
   * - ``fess.{horodatage}``
     - Index des documents de recherche. Créé au format ``fess.{yyyyMMddHHmmssSSS}`` (horodatage à la milliseconde) lors de la reconstruction de l'index, référencé via les alias ``fess.search`` (pour la recherche) et ``fess.update`` (pour la mise à jour).
   * - ``fess_config.*``
     - Informations de configuration système (composé de plusieurs sous-index tels que ``fess_config.web_config``, ``fess_config.scheduled_job``, ``fess_config.data_config``, etc.)
   * - ``fess_user.*``
     - Informations utilisateur (``fess_user.user``, ``fess_user.role``, ``fess_user.group``)
   * - ``fess_log.*``
     - Journaux de recherche, de clics, etc. (``fess_log.search_log``, ``fess_log.click_log``, ``fess_log.favorite_log``, ``fess_log.user_info``, ``fess_log.notification_queue``)
   * - ``fess_crawler.*``
     - Index temporaires utilisés pendant le crawl (``fess_crawler.queue``, ``fess_crawler.data``, ``fess_crawler.filter``). Ces index ne sont plus nécessaires une fois le crawl terminé et n'ont généralement pas besoin d'être inclus dans la sauvegarde.

Sauvegarde et restauration des index
=====================================

Vous pouvez effectuer des sauvegardes et des restaurations d'index en utilisant la fonctionnalité de snapshot d'OpenSearch.

Configuration du référentiel de snapshots
-----------------------------------------

Tout d'abord, configurez un référentiel pour stocker les données de sauvegarde.

**Pour un référentiel de système de fichiers :**

1. Ajoutez le chemin du référentiel au fichier de configuration d'OpenSearch (``opensearch.yml``).

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
   Dans la configuration par défaut de la version zip/tar.gz de |Fess|, OpenSearch démarre sur le port 9201 (``search_engine.http.url`` dans ``fess_config.properties``). Pour la version paquet RPM/DEB, la connexion est configurée par défaut sur le port 9200 (variable ``SEARCH_ENGINE_HTTP_URL`` dans le fichier de configuration d'environnement ``/etc/sysconfig/fess`` (RPM) ou ``/etc/default/fess`` (DEB)). Adaptez le numéro de port à votre environnement.

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
-----------------------------------

Sauvegarde de tous les index
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Sauvegarder uniquement des index spécifiques. L'exemple suivant cible uniquement les index liés à |Fess| (les index commençant par ``fess``).

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_fess_only?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Sauvegarde automatique régulière
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Vous pouvez exécuter des sauvegardes régulières en utilisant cron ou un outil similaire.

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
----------------------------

Vérifier la liste des snapshots créés.

::

    curl -X GET "localhost:9201/_snapshot/fess_backup/_all?pretty"

Vérifier les détails d'un snapshot spécifique.

::

    curl -X GET "localhost:9201/_snapshot/fess_backup/snapshot_1?pretty"

Restauration à partir de snapshots
------------------------------------

Restauration de tous les index
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Restauration d'index spécifiques
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le nom de l'index des documents de recherche est au format ``fess.{yyyyMMddHHmmssSSS}``. Vérifiez le nom réel de l'index via ``_cat/indices`` ou un outil similaire avant de procéder à la restauration.

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101000000000",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Restauration avec renommage de l'index
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Vous pouvez également modifier le nom de l'index lors de la restauration.

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
   Lorsque vous restaurez l'index des documents de recherche (``fess.{horodatage}``), vérifiez impérativement que les alias ``fess.search`` et ``fess.update`` pointent vers l'index restauré. Les snapshots incluant les informations d'alias, ceux-ci sont généralement restaurés automatiquement lorsque tous les index sont restaurés avec leur nom d'origine. En revanche, si vous avez modifié le nom de l'index via ``rename_pattern`` ou si vous migrez vers un autre cluster, les alias peuvent ne pas être correctement configurés. Dans ce cas, reconfigurez-les manuellement comme suit (remplacez le nom de l'index par le nom réel) :

   ::

       curl -X POST "localhost:9201/_aliases" -H 'Content-Type: application/json' -d'
       {
         "actions": [
           { "add": { "index": "restored_fess.20250101000000000", "alias": "fess.search" } },
           { "add": { "index": "restored_fess.20250101000000000", "alias": "fess.update" } }
         ]
       }'

Suppression de snapshots
--------------------------

Vous pouvez supprimer d'anciens snapshots pour économiser de l'espace de stockage.

::

    curl -X DELETE "localhost:9201/_snapshot/fess_backup/snapshot_1"

Sauvegarde des fichiers de configuration
=========================================

Outre les index OpenSearch, sauvegardez également les fichiers de configuration suivants. L'emplacement des fichiers de configuration varie selon la méthode d'installation.

Fichiers à sauvegarder
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Fichier/Répertoire
     - Méthode d'installation
     - Description
   * - ``app/WEB-INF/conf/system.properties``
     - zip/tar.gz
     - Configuration système (paramètres généraux)
   * - ``/etc/fess/system.properties``
     - RPM/DEB
     - Configuration système (paramètres généraux)
   * - ``app/WEB-INF/classes/fess_config.properties``
     - zip/tar.gz
     - Configuration détaillée de |Fess|
   * - ``/etc/fess/fess_config.properties``
     - RPM/DEB
     - Configuration détaillée de |Fess|
   * - ``app/WEB-INF/classes/log4j2.xml``
     - zip/tar.gz
     - Configuration des journaux
   * - ``/usr/share/fess/app/WEB-INF/classes/log4j2.xml``
     - RPM/DEB
     - Configuration des journaux
   * - ``app/WEB-INF/classes/fess_indices/``
     - zip/tar.gz
     - Fichiers de définition d'index
   * - ``/usr/share/fess/app/WEB-INF/classes/fess_indices/``
     - RPM/DEB
     - Fichiers de définition d'index
   * - ``app/WEB-INF/thumbnails/``
     - zip/tar.gz
     - Images miniatures (si nécessaire)
   * - ``/var/lib/fess/thumbnails/``
     - RPM/DEB
     - Images miniatures (si nécessaire)

.. note::
   Pour la version paquet RPM/DEB, le répertoire ``/etc/fess/`` contient, en plus de ``fess_config.properties``, des fichiers de configuration tels que ``fess_env_crawler.properties`` et d'autres fichiers ``fess_env_*.properties``, ainsi que ``tika.xml``. Il est recommandé de sauvegarder l'intégralité du répertoire ``/etc/fess/``. Le fichier ``system.properties`` est créé ou mis à jour sous ``/etc/fess/system.properties`` lorsque vous enregistrez les paramètres depuis la section « Système > Général » de l'interface d'administration.

Exemple de sauvegarde des fichiers de configuration
-----------------------------------------------------

L'exemple suivant illustre la sauvegarde des fichiers de configuration pour la version paquet RPM/DEB.

::

    #!/bin/bash
    BACKUP_DIR="/backup/fess/$(date +%Y%m%d_%H%M%S)"
    mkdir -p ${BACKUP_DIR}

    # Copie des fichiers de configuration (inclut system.properties, fess_config.properties, etc.)
    cp -r /etc/fess/ ${BACKUP_DIR}/

    # Fichiers de définition d'index et configuration des journaux
    cp -r /usr/share/fess/app/WEB-INF/classes/fess_indices/ ${BACKUP_DIR}/
    cp /usr/share/fess/app/WEB-INF/classes/log4j2.xml ${BACKUP_DIR}/

    # Option : Images miniatures
    # cp -r /var/lib/fess/thumbnails/ ${BACKUP_DIR}/

    echo "Backup completed: ${BACKUP_DIR}"

Migration de données
====================

Procédure de migration vers un autre environnement
---------------------------------------------------

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
   - Après la restauration, vérifiez que les alias ``fess.search`` et ``fess.update`` pointent vers l'index restauré.

5. **Vérifier le fonctionnement**

   - Démarrez |Fess|.
   - Accédez à l'interface d'administration et vérifiez la configuration.
   - Vérifiez que la fonction de recherche fonctionne correctement.

Précautions lors de la mise à niveau de version
------------------------------------------------

Lors de la migration de données entre différentes versions de |Fess|, prenez en compte les points suivants.

- Si la version majeure d'OpenSearch est différente, des problèmes de compatibilité peuvent survenir.
- Si la structure de l'index a été modifiée, une réindexation peut être nécessaire.
- Si vous souhaitez migrer des informations de configuration à travers un changement de structure d'index, envisagez d'utiliser la fonctionnalité de sauvegarde de l'interface d'administration (:doc:`../admin/backup-guide`) pour un export/import logique, plutôt qu'un snapshot OpenSearch.
- Pour plus de détails, consultez le guide de mise à niveau de chaque version.

Dépannage
==========

Échec de la création de snapshot
----------------------------------

1. Vérifiez les permissions pour le chemin du référentiel.
2. Vérifiez qu'il y a suffisamment d'espace disque.
3. Vérifiez les messages d'erreur dans les fichiers journaux d'OpenSearch.

Échec de la restauration
--------------------------

1. Vérifiez qu'un index du même nom n'existe pas déjà en état ouvert. Dans OpenSearch, il n'est pas possible de restaurer vers un index ouvert portant le même nom. Avant la restauration, fermez (``_close``) ou supprimez l'index cible, ou bien restaurez-le sous un autre nom via ``rename_pattern``.
2. Vérifiez que la version d'OpenSearch est compatible.
3. Vérifiez que le snapshot n'est pas corrompu.

Impossible de rechercher après la restauration
-----------------------------------------------

1. Vérifiez que l'index a été restauré correctement : ``curl -X GET "localhost:9201/_cat/indices?v"``
2. Vérifiez que les alias ``fess.search`` et ``fess.update`` pointent vers l'index restauré : ``curl -X GET "localhost:9201/_cat/aliases?v"``. Si les alias ne sont pas configurés, reconfigurez-les via l'API ``_aliases``.
3. Vérifiez qu'il n'y a pas d'erreurs dans les fichiers journaux de |Fess|.
4. Vérifiez que les fichiers de configuration sont correctement restaurés.

Rubriques associées
====================

- :doc:`../admin/backup-guide` - Sauvegarde/restauration des informations de configuration depuis l'interface d'administration
- :doc:`admin-index-export` - Fonctionnalité d'export des index
- :doc:`admin-logging` - Configuration des journaux

Informations de référence
===========================

Pour des informations détaillées, consultez la documentation officielle d'OpenSearch.

- `Fonctionnalité de snapshot <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`_
- `Configuration de référentiel <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/>`_
- `Référentiel S3 <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/plugins/#s3-repository>`_
