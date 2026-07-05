==========================
Procédure de mise à niveau
==========================

Cette page décrit la procédure de mise à niveau de |Fess| d'une version antérieure vers la dernière version.

.. warning::

   **Notes importantes avant la mise à niveau**

   - Veuillez obligatoirement effectuer une sauvegarde avant la mise à niveau
   - Il est fortement recommandé de valider la mise à niveau dans un environnement de test au préalable
   - Le service s'arrêtera pendant la mise à niveau, veuillez donc définir une fenêtre de maintenance appropriée
   - Selon les versions, le format des fichiers de configuration peut avoir changé

Versions compatibles
====================

Cette procédure de mise à niveau est compatible avec les mises à niveau entre les versions suivantes :

- Fess 14.x → Fess 15.8
- Fess 15.x → Fess 15.8

.. note::

   Pour une mise à niveau depuis des versions plus anciennes (13.x ou antérieures), une mise à niveau progressive peut être nécessaire.
   Veuillez consulter les notes de version pour plus de détails.

Préparation avant la mise à niveau
====================================

Vérification de la compatibilité des versions
----------------------------------------------

Vérifiez la compatibilité entre la version de destination et la version actuelle.

- `Notes de version <https://github.com/codelibs/fess/releases>`__
- `Guide de mise à niveau <https://fess.codelibs.org/ja/>`__

Planification du temps d'arrêt
-------------------------------

La mise à niveau nécessite l'arrêt du système. Planifiez le temps d'arrêt en tenant compte des éléments suivants :

- Temps de sauvegarde : 10 minutes à plusieurs heures (selon la quantité de données)
- Temps de mise à niveau : 10 à 30 minutes
- Temps de vérification du fonctionnement : 30 minutes à 1 heure
- Temps de réserve : 30 minutes

**Fenêtre de maintenance recommandée** : Total de 2 à 4 heures

Étape 1 : Sauvegarde des données
==================================

Avant la mise à niveau, sauvegardez toutes les données.

Sauvegarde des données de configuration
----------------------------------------

1. **Sauvegarde depuis l'écran d'administration**

   Connectez-vous à l'écran d'administration et cliquez sur « Informations système » → « Sauvegarde ».

   La page de sauvegarde affiche une liste des données de configuration suivantes, article par article.
   Cliquez sur chaque lien pour télécharger (il ne s'agit pas d'un fichier ZIP unique, mais de fichiers individuels par article).

   - ``fess_basic_config.bulk`` - Configuration de base (paramètres généraux)
   - ``fess_config.bulk`` - Informations de configuration : paramètres d'exploration, planificateur, étiquettes, correspondances de clés, etc.
   - ``fess_user.bulk`` - Utilisateurs, rôles, groupes
   - ``system.properties`` - Paramètres système
   - ``fess.json`` / ``doc.json`` - Paramètres d'index (mappage)

   .. note::

      Les données de journaux tels que les journaux de recherche et les journaux de clics (``search_log.ndjson``, ``click_log.ndjson``,
      ``favorite_log.ndjson``, ``user_info.ndjson``) peuvent également être téléchargées depuis la même page.
      Elles ne sont pas nécessaires si vous ne sauvegardez que la configuration.

2. **Sauvegarde des fichiers de configuration**

   Version TAR.GZ/ZIP ::

       $ cp /path/to/fess/app/WEB-INF/conf/system.properties /backup/
       $ cp /path/to/fess/app/WEB-INF/classes/fess_config.properties /backup/

   Version RPM/DEB ::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/

3. **Fichiers de configuration personnalisés**

   Si vous avez des fichiers de configuration personnalisés, sauvegardez-les également ::

       $ cp /path/to/fess/app/WEB-INF/classes/log4j2.xml /backup/

Sauvegarde des données d'index
-------------------------------

Sauvegardez les données d'index d'OpenSearch.

Méthode 1 : Utilisation de la fonction de snapshot (recommandé)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sauvegardez l'index en utilisant la fonction de snapshot d'OpenSearch.

.. note::

   Pour enregistrer un dépôt de système de fichiers (``fs``), vous devez au préalable spécifier le répertoire de destination de sauvegarde dans
   ``path.repo`` du fichier ``opensearch.yml`` d'OpenSearch, puis redémarrer OpenSearch.

1. Configuration du dépôt ::

       $ curl -X PUT "http://localhost:9200/_snapshot/fess_backup" -H 'Content-Type: application/json' -d'
       {
         "type": "fs",
         "settings": {
           "location": "/backup/opensearch/snapshots"
         }
       }'

2. Création du snapshot ::

       $ curl -X PUT "http://localhost:9200/_snapshot/fess_backup/snapshot_1?wait_for_completion=true"

3. Vérification du snapshot ::

       $ curl -X GET "http://localhost:9200/_snapshot/fess_backup/snapshot_1"

Méthode 2 : Sauvegarde du répertoire entier
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Après avoir arrêté OpenSearch, sauvegardez le répertoire de données.

::

    $ sudo systemctl stop opensearch
    $ sudo tar czf /backup/opensearch-data-$(date +%Y%m%d).tar.gz /var/lib/opensearch/data
    $ sudo systemctl start opensearch

Sauvegarde de la version Docker
--------------------------------

Les données d'OpenSearch sont stockées dans des volumes Docker. Dans ``compose-opensearch3.yaml``,
deux volumes sont définis : ``search01_data`` pour les données d'index, et ``search01_dictionary``
pour les fichiers de dictionnaire.

.. note::

   Le nom réel du volume est préfixé par le nom de projet Compose (par défaut, le nom du répertoire
   où le fichier Compose est placé). Vérifiez le nom exact avec la commande suivante ::

       $ docker volume ls

Arrêtez les conteneurs, puis sauvegardez les volumes ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ docker run --rm -v search01_data:/data -v $(pwd):/backup ubuntu tar czf /backup/search01-data-backup.tar.gz /data
    $ docker run --rm -v search01_dictionary:/data -v $(pwd):/backup ubuntu tar czf /backup/search01-dictionary-backup.tar.gz /data
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml start

Étape 2 : Arrêt de la version actuelle
=========================================

Arrêtez Fess et OpenSearch.

Version TAR.GZ/ZIP ::

    $ kill <fess_pid>
    $ kill <opensearch_pid>

Version RPM/DEB (systemd) ::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Version Docker ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Étape 3 : Installation de la nouvelle version
================================================

Les procédures diffèrent selon la méthode d'installation.

Version TAR.GZ/ZIP
------------------

1. Téléchargez et décompressez la nouvelle version ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.8.0/fess-15.8.0.tar.gz
       $ tar -xzf fess-15.8.0.tar.gz

2. Copiez la configuration de l'ancienne version ::

       $ cp /path/to/old-fess/app/WEB-INF/conf/system.properties /path/to/fess-15.8.0/app/WEB-INF/conf/
       $ cp /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.8.0/bin/

3. Vérifiez les différences de configuration et ajustez si nécessaire

Version RPM/DEB
---------------

Installez le package de la nouvelle version ::

    # RPM
    $ sudo rpm -Uvh fess-15.8.0.rpm

    # DEB
    $ sudo dpkg -i fess-15.8.0.deb

.. note::

   Les fichiers de configuration (``/etc/fess/*``) sont automatiquement conservés.
   Cependant, si de nouvelles options de configuration ont été ajoutées, un ajustement manuel peut être nécessaire.

Version Docker
--------------

1. Obtenez les fichiers Compose de la nouvelle version ::

       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose.yaml
       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose-opensearch3.yaml

2. Récupérez la nouvelle image ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

Étape 4 : Mise à niveau d'OpenSearch (si nécessaire)
=======================================================

Si vous mettez également à niveau OpenSearch, suivez les procédures suivantes.

.. note::

   Cette procédure s'applique aux cas où OpenSearch est géré manuellement avec les versions TAR.GZ/ZIP et RPM/DEB.
   Pour la version Docker, l'obtention de la nouvelle image à l'étape 3 met également à jour OpenSearch et ses plugins
   simultanément ; cette étape n'est donc pas nécessaire.

.. warning::

   Procédez avec précaution lors d'une mise à niveau majeure d'OpenSearch.
   Des problèmes de compatibilité d'index peuvent survenir.

1. Installez la nouvelle version d'OpenSearch

2. Réinstallez les plugins ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

   .. note::

      La version de ces plugins doit correspondre à la version d'OpenSearch utilisée.
      Fess 15.8 est compatible avec OpenSearch 3.7.0. Si les versions ne correspondent pas,
      l'installation du plugin échouera.

3. Démarrez OpenSearch ::

       $ sudo systemctl start opensearch.service

Étape 5 : Démarrage de la nouvelle version
============================================

Version TAR.GZ/ZIP ::

    $ cd /path/to/fess-15.8.0
    $ ./bin/fess -d

Version RPM/DEB ::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Version Docker ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Étape 6 : Vérification du fonctionnement
==========================================

1. **Vérification des journaux**

   Vérifiez qu'il n'y a pas d'erreurs ::

       $ tail -f /path/to/fess/logs/fess.log

2. **Accès à l'interface Web**

   Accédez à http://localhost:8080/ via un navigateur.

3. **Connexion à l'écran d'administration**

   Accédez à http://localhost:8080/admin et connectez-vous avec le compte administrateur.

4. **Vérification de la version**

   Dans l'écran d'administration, cliquez sur « Informations système » → « Informations de configuration » et vérifiez que
   ``fess.version`` affiché dans « Propriétés système » correspond bien à la nouvelle version.

5. **Vérification du fonctionnement de la recherche**

   Effectuez une recherche sur l'écran de recherche et vérifiez que les résultats sont retournés normalement.

Étape 7 : Recréation de l'index (recommandé)
==============================================

En cas de mise à niveau majeure, il est recommandé de recréer l'index.

1. Vérifiez la planification d'exploration existante
2. Exécutez « Default Crawler » depuis « Système » → « Planificateur »
3. Attendez la fin de l'exploration
4. Vérifiez les résultats de recherche

Procédure de retour arrière
============================

En cas d'échec de la mise à niveau, vous pouvez revenir en arrière avec les procédures suivantes.

Étape 1 : Arrêt de la nouvelle version
---------------------------------------

::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Étape 2 : Restauration de l'ancienne version
---------------------------------------------

Restaurez les fichiers de configuration et les données depuis la sauvegarde.

Version RPM/DEB ::

    $ sudo rpm -Uvh --oldpackage fess-<old-version>.rpm

Ou ::

    $ sudo dpkg -i fess-<old-version>.deb

Étape 3 : Restauration des données
------------------------------------

Restauration depuis le snapshot ::

    $ curl -X POST "http://localhost:9200/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true"

Ou restauration du répertoire depuis la sauvegarde ::

    $ sudo systemctl stop opensearch
    $ sudo rm -rf /var/lib/opensearch/data/*
    $ sudo tar xzf /backup/opensearch-data-backup.tar.gz -C /
    $ sudo systemctl start opensearch

.. note::

   Les données de configuration téléchargées depuis l'écran d'administration (fichiers ``*.bulk``) peuvent être restaurées
   en les réimportant via la fonction de téléversement de la page « Informations système » → « Sauvegarde » après le démarrage de Fess.

Étape 4 : Démarrage et vérification du service
-----------------------------------------------

::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Vérifiez le fonctionnement et confirmez le retour à la normale.

Questions fréquemment posées
==============================

Q : Peut-on effectuer une mise à niveau sans temps d'arrêt ?
--------------------------------------------------------------

R : La mise à niveau de Fess nécessite l'arrêt du service. Pour minimiser le temps d'arrêt, envisagez ce qui suit :

- Vérifier les procédures dans un environnement de test au préalable
- Effectuer la sauvegarde à l'avance
- Assurer suffisamment de temps pour la fenêtre de maintenance

Q : Est-il nécessaire de mettre à niveau OpenSearch également ?
----------------------------------------------------------------

R : La version d'OpenSearch compatible est déterminée pour chaque version de Fess.
Fess 15.8 est compatible avec OpenSearch 3.7.0.
Les plugins OpenSearch pour Fess tels que ``opensearch-analysis-fess`` doivent correspondre exactement à la version d'OpenSearch ;
si vous mettez à niveau OpenSearch, veuillez également mettre à jour les plugins vers la version correspondante (3.7.0).

Q : Est-il nécessaire de recréer l'index ?
-------------------------------------------

R : Pour une mise à niveau mineure, ce n'est généralement pas nécessaire, mais pour une mise à niveau majeure, la recréation est recommandée.

Q : Les résultats de recherche ne s'affichent pas après la mise à niveau
--------------------------------------------------------------------------

R : Vérifiez les points suivants :

1. Vérifiez qu'OpenSearch est démarré
2. Vérifiez que l'index existe (``curl http://localhost:9200/_cat/indices``)
3. Réexécutez l'exploration

Étapes suivantes
================

Une fois la mise à niveau terminée :

- :doc:`run` - Vérification du démarrage et de la configuration initiale
- :doc:`security` - Révision de la configuration de sécurité
- Vérifiez les nouvelles fonctionnalités dans les notes de version
