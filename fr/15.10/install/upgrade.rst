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

- Fess 14.x → Fess 15.10
- Fess 15.x → Fess 15.10

.. important::

   |Fess| 14.x est compatible avec la série OpenSearch 2.x, tandis que |Fess| 15.10 est compatible
   avec OpenSearch 3.9.0. Les plugins OpenSearch pour |Fess| doivent correspondre exactement à la
   version d'OpenSearch ; une mise à niveau depuis la 14.x implique donc obligatoirement une mise
   à niveau majeure d'OpenSearch également. Voir :ref:`upgrade-opensearch`.

.. note::

   Pour une mise à niveau depuis des versions plus anciennes (13.x ou antérieures), une mise à niveau progressive peut être nécessaire.
   Veuillez consulter les notes de version pour plus de détails.

Préparation avant la mise à niveau
====================================

Vérification de la compatibilité des versions
----------------------------------------------

Vérifiez la compatibilité entre la version de destination et la version actuelle.

- `Notes de version <https://github.com/codelibs/fess/releases>`__
- :doc:`prerequisites` - Configuration requise pour |Fess| 15.10 (versions de Java et d'OpenSearch)

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
   Cliquez sur chaque ligne pour télécharger (il ne s'agit pas d'un fichier ZIP unique, mais de
   fichiers individuels par article. Il n'existe pas de fonction de téléchargement groupé ;
   téléchargez donc les articles nécessaires un par un).

   - ``fess_basic_config.bulk`` - Index de configuration (paramètres d'exploration, planificateur,
     étiquettes, correspondances de clés, rôles, authentification Web/fichiers, etc. ; 19 index)
   - ``fess_config.bulk`` - En plus des 19 index ci-dessus, données d'exécution telles que les
     informations d'exploration, les URL en échec, les journaux de tâches, la file d'attente des
     miniatures, etc. (25 index jusqu'à la 15.8 ; la 15.9 ajoute l'index ``tag_type`` qui contient
     les tags des utilisateurs, soit 26)
   - ``fess_user.bulk`` - Utilisateurs, rôles, groupes
   - ``system.properties`` - Paramètres système, y compris les paramètres généraux
   - ``fess.json`` - Paramètres d'index (nombre de shards, ``index.knn``, etc.)
   - ``doc.json`` - Mappage des documents (définitions des champs)

   .. note::

      ``fess_config.bulk`` inclut ``fess_basic_config.bulk``. Pour la sauvegarde de configuration
      avant la mise à niveau, ``fess_basic_config.bulk``, ``fess_user.bulk`` et
      ``system.properties`` suffisent. Toutefois, si la source est en 15.9 ou ultérieure et que vous utilisez des tags utilisateur, téléchargez aussi ``fess_config.bulk`` : l'index ``tag_type``, qui contient les tags utilisateur, n'est pas inclus dans ``fess_basic_config.bulk`` (voir :doc:`../admin/tagtype-guide`).

   .. note::

      Les données de journaux tels que les journaux de recherche et les journaux de clics (``search_log.ndjson``, ``click_log.ndjson``,
      ``favorite_log.ndjson``, ``user_info.ndjson`` ; la 15.9 propose aussi ``chat_log.ndjson``)
      peuvent également être téléchargées depuis la même page.
      Elles ne sont pas nécessaires si vous ne sauvegardez que la configuration. Notez que ces
      fichiers ``*.ndjson`` ne peuvent pas être restaurés en les téléversant depuis la page de
      sauvegarde (voir « Procédure de retour arrière »).

2. **Sauvegarde des fichiers de configuration**

   Version ZIP ::

       $ cp /path/to/fess/app/WEB-INF/conf/system.properties /backup/
       $ cp /path/to/fess/app/WEB-INF/classes/fess_config.properties /backup/
       $ cp /path/to/fess/bin/fess.in.sh /backup/

   Version RPM ::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/
       $ sudo cp /etc/sysconfig/fess /backup/

   Version DEB ::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/
       $ sudo cp /etc/default/fess /backup/

   .. note::

      ``/etc/sysconfig/fess`` (version RPM) et ``/etc/default/fess`` (version DEB) sont des
      fichiers de variables d'environnement qui définissent notamment ``FESS_PORT``,
      ``FESS_HEAP_SIZE``, ``SEARCH_ENGINE_HTTP_URL`` et ``FESS_DICTIONARY_PATH``.
      Pour la version ZIP, les réglages équivalents se trouvent dans ``bin/fess.in.sh``.

3. **Fichiers de configuration personnalisés**

   Si vous avez des fichiers de configuration personnalisés, sauvegardez-les également ::

       $ cp /path/to/fess/app/WEB-INF/classes/log4j2.xml /backup/
       $ cp /path/to/fess/lib/classes/tomcat_config.properties /backup/

   .. note::

      ``app/WEB-INF/classes/log4j2.xml`` correspond à la configuration des journaux du processus
      principal (Web) de |Fess|. Les processus enfants tels que le crawler utilisent des fichiers
      distincts (par exemple ``app/WEB-INF/env/crawler/resources/log4j2.xml``, pour les quatre
      processus ``crawler``, ``suggest``, ``thumbnail`` et ``chunk``) ; si vous les avez
      personnalisés, pensez à les sauvegarder également.

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

Arrêtez les conteneurs, puis sauvegardez les volumes. Pour l'option ``-v`` de ``docker run``,
indiquez le nom réel du volume, préfixe inclus ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ PROJECT=$(basename "$(pwd)")
    $ docker run --rm -v ${PROJECT}_search01_data:/data -v $(pwd):/backup ubuntu tar czf /backup/search01-data-backup.tar.gz /data
    $ docker run --rm -v ${PROJECT}_search01_dictionary:/data -v $(pwd):/backup ubuntu tar czf /backup/search01-dictionary-backup.tar.gz /data
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml start

.. warning::

   Si vous indiquez ``search01_data`` sans préfixe pour ``-v``, Docker ne référence pas le volume
   existant : il en crée un nouveau, vide, portant le même nom. La commande ne renvoie aucune
   erreur mais produit une archive vide, ce qui peut donner l'illusion que la sauvegarde a réussi.

.. note::

   Le conteneur principal de |Fess| (``fess01``) n'a pas de volume dédié ; seuls les deux volumes
   ci-dessus doivent donc être sauvegardés. Notez toutefois que les paramètres généraux modifiés
   depuis l'écran d'administration, ainsi que les plugins installés depuis l'écran
   d'administration, ne sont stockés que dans le conteneur et seraient perdus si celui-ci était
   recréé. Pour les rendre persistants, spécifiez-les via ``FESS_JAVA_OPTS`` ou ``FESS_PLUGINS``
   dans le fichier Compose.

Étape 2 : Arrêt de la version actuelle
=========================================

Arrêtez Fess et OpenSearch.

La version ZIP ne fournit pas de script d'arrêt. Si vous aviez démarré ``bin/fess`` avec
l'option ``-p``, arrêtez-le à l'aide du fichier PID ::

    $ kill $(cat /path/to/fess/fess.pid)
    $ kill <opensearch_pid>

Si vous l'aviez démarré sans ``-p``, identifiez le PID du processus et exécutez ``kill``
manuellement (``-d`` seul ne crée pas de fichier PID).

Version RPM/DEB (systemd) ::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Version Docker ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   Assurez-vous que |Fess| est arrêté avant de commencer l'étape 3, et ne remplacez ni le paquet ni
   les fichiers d'un |Fess| encore en cours d'exécution. Après le remplacement du paquet DEB d'un
   |Fess| 15.8 en cours d'exécution par celui de la 15.10, l'écran de recherche a répondu ``404``
   jusqu'au redémarrage de |Fess|. Pour les versions des paquets, vérifiez avec
   ``systemctl status fess.service``.

Étape 3 : Installation de la nouvelle version
================================================

Les procédures diffèrent selon la méthode d'installation.

Version ZIP
------------------

1. Téléchargez et décompressez la nouvelle version ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.10.0/fess-15.10.0.zip
       $ unzip fess-15.10.0.zip

   .. note::

      La version archive de |Fess| n'est distribuée qu'au format ZIP (``fess-15.10.0.tar.gz``
      n'est pas fourni).

2. Copiez la configuration de l'ancienne version ::

       $ cp /path/to/old-fess/app/WEB-INF/conf/system.properties /path/to/fess-15.10.0/app/WEB-INF/conf/
       $ cp /path/to/old-fess/app/WEB-INF/classes/fess_config.properties /path/to/fess-15.10.0/app/WEB-INF/classes/
       $ cp /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.10.0/bin/

   .. warning::

      Copiés tels quels, ``fess_config.properties`` et ``fess.in.sh`` conservent leurs anciennes
      valeurs, y compris celles dont la valeur par défaut a changé en 15.9 : par exemple, les
      tâches créées ensuite utilisent Groovy par défaut. Avant d'exécuter les deux dernières
      commandes, comparez chaque fichier avec celui de ``fess-15.10.0`` et ne reportez que les
      valeurs que vous avez modifiées vous-même. Voir :ref:`upgrade-159-carried-over-config` pour
      les éléments à vérifier.

3. Si vous avez des personnalisations, copiez également ce qui suit ::

       # Paramètres de Tomcat (le paramètre SAML tomcat.sameSiteCookies=none se trouve ici)
       $ cp /path/to/old-fess/lib/classes/tomcat_config.properties /path/to/fess-15.10.0/lib/classes/
       # Plugins installés
       $ cp -r /path/to/old-fess/app/WEB-INF/plugin/. /path/to/fess-15.10.0/app/WEB-INF/plugin/
       # Thèmes que vous avez téléversés vous-même (un répertoire par thème ; jamais bootstrap)
       $ cp -r /path/to/old-fess/app/themes/<your-theme> /path/to/fess-15.10.0/app/themes/

   .. warning::

      Sans le ``tomcat_config.properties`` de l'ancienne installation, ``tomcat.sameSiteCookies``
      revient silencieusement à la valeur par défaut ``lax`` et la connexion SAML cesse de
      fonctionner (voir :ref:`upgrade-159-saml`). Le fichier fourni est identique en 15.8.0 et en
      15.10 ; il peut donc être copié tel quel.

   .. warning::

      Ne copiez pas ``log4j2.xml`` par-dessus le fichier de la 15.10. Le fichier de la 15.10 maintient
      le logger ``RequestLoggingFilter`` au niveau ``warn``, et un fichier copié depuis la 15.8
      supprime ce réglage : avec le niveau de journalisation DEBUG, les en-têtes de requête (y
      compris ``Authorization``) et les paramètres de requête (y compris le mot de passe saisi dans
      le formulaire de connexion) sont alors écrits dans le journal. Comparez les deux fichiers avec
      ``diff`` et ne réappliquez au fichier de la 15.10 que les modifications que vous avez faites
      vous-même.

   .. warning::

      Ne copiez pas l'intégralité du répertoire ``app/themes/``. Il contient aussi ``bootstrap``,
      le thème fourni avec |Fess|, et le copier par-dessus celui de la 15.10 remplace l'écran de
      recherche de la 15.10 par la version 15.8 du thème. Copiez uniquement les répertoires des
      thèmes que vous avez créés vous-même. Pour un thème publié par le projet |Fess|, installez
      plutôt la version construite pour la 15.10, avec ``bin/fess-setup install theme <name>``
      (voir :doc:`fess-setup`).

   .. warning::

      Ne copiez pas les JSP (``app/WEB-INF/view/``) modifiés depuis l'écran d'administration
      « Design ». L'écran de recherche de la 15.10 est un thème et n'utilise plus ces JSP ;
      voir :ref:`upgrade-159-static-theme` pour savoir où ces modifications doivent désormais être
      faites.

   .. note::

      Les plugins copiés depuis ``app/WEB-INF/plugin/`` ont été construits pour l'ancienne version.
      Après les avoir copiés, exécutez ``bin/fess-setup upgrade plugins`` dans ``fess-15.10.0`` pour
      remplacer chacun d'eux par la version construite pour la 15.10 ; voir
      :ref:`upgrade-plugin-versions`.

4. Vérifiez les différences de configuration et ajustez si nécessaire

Version RPM/DEB
---------------

Installez le package de la nouvelle version ::

    # RPM
    $ sudo rpm -Uvh fess-15.10.0.rpm

    # DEB
    $ sudo dpkg -i fess-15.10.0.deb

.. note::

   Dans la version RPM, les fichiers de configuration ``/etc/fess/*`` sont enregistrés en tant que
   ``%config(noreplace)`` et sont donc conservés lors de la mise à niveau (les nouveaux fichiers
   par défaut sont placés à côté avec l'extension ``.rpmnew``). Si de nouvelles options de
   configuration ont été ajoutées, un ajustement manuel peut être nécessaire. Un fichier
   ``/etc/fess/fess_config.properties`` que vous avez modifié conserve ses anciennes valeurs en
   15.10, comme un fichier copié dans la procédure ZIP ; voir :ref:`upgrade-159-carried-over-config`.

.. warning::

   Dans la version DEB, les fichiers situés sous ``/etc/fess`` (tels que ``fess_config.properties``
   et ``tomcat_config.properties``) sont enregistrés en tant que conffiles, comme
   ``/etc/default/fess``, ``/etc/init.d/fess`` et ``/usr/lib/systemd/system/fess.service``. Lors de
   la première mise à niveau depuis la 15.8, ``dpkg`` les traite comme suit :

   - Un fichier que vous n'avez jamais modifié est remplacé par celui de la 15.10 sans question.
   - Pour un fichier que vous avez modifié, ``dpkg`` pose la question. Si vous conservez votre
     fichier (réponse par défaut, ou ``--force-confold``), le fichier de la 15.10 est placé à côté
     sous le nom ``<nom du fichier>.dpkg-dist``. Si vous installez le nouveau fichier (``Y`` ou
     ``--force-confnew``), votre fichier est enregistré sous le nom ``<nom du fichier>.dpkg-old``.
   - ``dpkg -i`` et ``apt-get install -y`` s'arrêtent à la première question lorsque personne ne
     peut y répondre. Pour une mise à niveau sans surveillance, passez ``--force-confold``
     (``--force-confdef`` évite aussi les questions), par exemple
     ``sudo dpkg --force-confold -i fess-15.10.0.deb`` ou
     ``sudo apt-get install -y -o Dpkg::Options::=--force-confold ./fess-15.10.0.deb``.

   Sauvegardez dans tous les cas ``/etc/fess`` au préalable (étape 1). Un fichier que vous
   conservez a toujours ses valeurs de la 15.8 : comparez-le avec le fichier ``.dpkg-dist`` au lieu
   de l'utiliser tel quel (voir :ref:`upgrade-159-carried-over-config`). Notez que
   ``/etc/fess/system.properties`` n'est pas écrasé, car il s'agit d'un fichier généré à
   l'exécution qui n'est pas inclus dans le paquet.

Version Docker
--------------

1. Obtenez les fichiers Compose de la nouvelle version ::

       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.10.0/compose/compose.yaml
       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.10.0/compose/compose-opensearch3.yaml

2. Récupérez la nouvelle image ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

.. _upgrade-opensearch:

Étape 4 : Mise à niveau d'OpenSearch
====================================

|Fess| 15.10 est compatible avec OpenSearch 3.9.0. Si l'OpenSearch auquel vous vous connectez est
antérieur à cette version, effectuez la mise à niveau en suivant la procédure ci-dessous.

.. note::

   Cette procédure s'applique aux cas où OpenSearch est géré manuellement avec les versions ZIP et RPM/DEB.
   Pour la version Docker, l'obtention de la nouvelle image à l'étape 3 met également à jour OpenSearch et ses plugins
   simultanément ; cette étape n'est donc pas nécessaire.

.. important::

   Que la recherche par vecteurs de chunks (recherche sémantique) soit utilisée ou non, |Fess|
   15.10 inclut toujours ``index.knn`` dans les réglages de l'index de recherche, ainsi que le
   champ ``content_chunk_vector`` (de type ``knn_vector``) dans le mapping. Le **plugin k-NN est
   donc obligatoire** sur l'OpenSearch auquel vous vous connectez.

   - Il est inclus dans la distribution standard d'OpenSearch et dans l'image de la version
     Docker.
   - **La distribution minimale ne l'inclut pas : la création d'un nouvel index échoue et
     |Fess| ne peut pas démarrer.**
   - Le réglage d'index ``knn.derived_source.enabled`` est également toujours envoyé. Sur un
     OpenSearch ancien qui ne le reconnaît pas, la création de l'index échoue, que le plugin
     k-NN soit présent ou non.

   Pour plus de détails, consultez la section « Prérequis » de :doc:`../config/search-semantic`.

.. warning::

   Procédez avec précaution lors d'une mise à niveau majeure d'OpenSearch.
   Des problèmes de compatibilité d'index peuvent survenir.
   |Fess| 14.x utilise la série OpenSearch 2.x ; une mise à niveau depuis la 14.x correspond donc
   toujours à ce cas de figure.

   Un snapshot pris avec OpenSearch 3.9.0 ne peut pas être restauré dans OpenSearch 3.8.0 ou
   antérieur. Conservez le snapshot pris avant la mise à niveau au cas où vous devriez revenir en
   arrière.

1. Installez la nouvelle version d'OpenSearch

2. Réinstallez les plugins ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install https://maven.codelibs.org/release/org/codelibs/opensearch/opensearch-analysis-fess/3.9.0/opensearch-analysis-fess-3.9.0.zip
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install https://maven.codelibs.org/release/org/codelibs/opensearch/opensearch-analysis-extension/3.9.0/opensearch-analysis-extension-3.9.0.zip
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install https://maven.codelibs.org/release/org/codelibs/opensearch/opensearch-minhash/3.9.0/opensearch-minhash-3.9.0.zip
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install https://maven.codelibs.org/release/org/codelibs/opensearch/opensearch-configsync/3.9.0/opensearch-configsync-3.9.0.zip

   .. note::

      La version de ces plugins doit correspondre à la version d'OpenSearch utilisée.
      |Fess| 15.10 est compatible avec OpenSearch 3.9.0. Si les versions ne correspondent pas,
      l'installation du plugin échouera.

      Les quatre plugins de |Fess| sont publiés sur maven.codelibs.org ; ils s'installent donc par
      leur URL. La forme ``groupId:artifactId:version`` de ``opensearch-plugin install`` ne cherche
      que dans Maven Central.

3. Déplacez le répertoire des dictionnaires sous le répertoire de configuration d'OpenSearch

   À partir d'OpenSearch 3.8.0, la création d'un index est refusée si les fichiers de dictionnaire se trouvent en dehors du répertoire de configuration d'OpenSearch.
   Si, conformément à l'ancienne procédure, ``configsync.config_path`` pointe vers un emplacement situé en dehors du répertoire de configuration, comme ``/var/lib/opensearch/data/config/`` (``/path/to/opensearch/data/config/`` pour la version ZIP),
   |Fess| ne peut pas créer ses index et ne démarre pas.
   Pour les versions RPM/DEB, copiez les fichiers de dictionnaire vers ``/etc/opensearch/dictionary/`` comme suit ::

       $ sudo install -d -o opensearch -g opensearch -m 0750 /etc/opensearch/dictionary
       $ sudo cp -a /var/lib/opensearch/data/config/. /etc/opensearch/dictionary/
       $ sudo chown -R opensearch:opensearch /etc/opensearch/dictionary

   Modifiez ensuite ``configsync.config_path`` dans ``/etc/opensearch/opensearch.yml`` et ``FESS_DICTIONARY_PATH`` de |Fess| (``/etc/sysconfig/fess`` pour la version RPM, ``/etc/default/fess`` pour la version DEB) pour qu'ils pointent tous deux vers ``/etc/opensearch/dictionary/``.
   Pour la version ZIP, utilisez le répertoire ``config/dictionary/`` d'OpenSearch. Pour plus de détails, consultez :doc:`install-linux`.

4. Démarrez OpenSearch ::

       $ sudo systemctl start opensearch.service

Étape 5 : Démarrage de la nouvelle version
============================================

Version ZIP ::

    $ cd /path/to/fess-15.10.0
    $ ./bin/fess -d -p /path/to/fess-15.10.0/fess.pid

.. note::

   L'option ``-p`` crée un fichier PID, qui permet d'arrêter |Fess| lors du prochain arrêt avec
   ``kill $(cat /path/to/fess-15.10.0/fess.pid)``.

Version RPM/DEB ::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Version Docker ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Étape 6 : Vérification du fonctionnement
==========================================

1. **Vérification des journaux**

   Vérifiez qu'il n'y a pas d'erreurs.

   Version ZIP ::

       $ tail -f /path/to/fess/logs/fess.log

   Version RPM/DEB ::

       $ sudo tail -f /var/log/fess/fess.log

   Version Docker ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

   .. note::

      Le même répertoire de journaux contient également ``fess-crawler.log`` pour le traitement
      d'exploration, ``audit.log`` pour l'authentification et les opérations d'administration, et
      ``searchlog.log`` pour les requêtes de recherche.

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

.. note::

   Les étapes ci-dessous relancent le crawl ; elles ne mettent pas à jour le mapping de l'index
   (définitions des champs). Si vous avez besoin d'une réindexation qui met à jour le mapping —
   par exemple pour activer nouvellement la recherche par vecteurs de chunks (recherche
   sémantique) —, exécutez séparément la « Réindexation » sous « Informations système » →
   « Maintenance » dans l'interface d'administration. Voir :ref:`semantic-search-migration`
   (:doc:`../config/search-semantic`) pour plus de détails.

   Si vous conservez un index de documents créé avec la 15.8 ou antérieure, consultez aussi
   :ref:`upgrade-reindex-new-fields`.

.. warning::

   OpenSearch 3.9.0 refuse des entrées de dictionnaire que la 15.8 acceptait, comme la même entrée
   ``mapping`` enregistrée deux fois ou un token ``kuromoji`` qui contient une espace. Avec une telle
   entrée, la « Réindexation » ne crée pas le nouvel index de documents : ``fess.log`` indique
   seulement ``Failed to create index`` et l'ancien index continue de servir les recherches.
   Téléchargez le dictionnaire sous « Système » → « Dictionnaire », supprimez les lignes en double
   ou invalides, téléversez-le de nouveau, puis relancez la « Réindexation ». Voir
   :ref:`upgrade-159-api-requests` pour les entrées que la 15.10 n'enregistre plus.

1. Vérifiez la planification d'exploration existante
2. Exécutez « Default Crawler » depuis « Système » → « Planificateur »
3. Attendez la fin de l'exploration
4. Vérifiez les résultats de recherche

.. warning::

   La réindexation recrée l'index avec le nouveau mapping ; elle échoue donc sur un OpenSearch
   dépourvu du plugin k-NN. Consultez les remarques de l'étape 4.

Mise à niveau de 15.9 vers 15.10
================================

Les modifications de cette section concernent toute mise à niveau vers 15.10. Si vous venez de la version 15.8 ou d'une version antérieure, lisez aussi la section « Mise à niveau de 15.8 vers 15.10 » qui suit.

.. _upgrade-1510-client-ip:

Adresse IP du client enregistrée dans les journaux
--------------------------------------------------

Jusqu'à la 15.9, le champ ``ip`` du journal d'audit et le champ ``clientIp`` du journal de recherche enregistraient telle quelle la valeur de l'en-tête ``X-Forwarded-For`` de la requête, quelle que soit l'origine de celle-ci. Si l'en-tête contenait plusieurs adresses, toutes étaient enregistrées, et un client pouvait envoyer n'importe quelle valeur.
La 15.10 détermine l'adresse selon les mêmes règles que la limitation de débit (:doc:`../config/rate-limiting`). ``X-Forwarded-For`` (toutes les lignes, s'il est réparti sur plusieurs lignes d'en-tête) et ``X-Real-IP`` ne sont utilisés que si la source de la requête figure dans ``rate.limit.trusted.proxies`` (valeur par défaut ``127.0.0.1,::1``). ``X-Forwarded-For`` est lu à partir de la droite, et la première adresse qui n'est pas celle d'un proxy de confiance est enregistrée. Sinon, l'adresse de la source est enregistrée. Ces règles s'appliquent même si ``rate.limit.enabled`` vaut ``false``.

Derrière un reverse proxy absent de ``rate.limit.trusted.proxies``, toutes les requêtes sont enregistrées avec l'adresse du proxy. Pour enregistrer l'adresse du client d'origine, ajoutez l'adresse du proxy à ``rate.limit.trusted.proxies``.

.. _upgrade-1510-cipher-key:

Avertissement sur ``app.cipher.key``
------------------------------------

Si ``app.cipher.key`` est vide ou conserve la valeur fournie dans ``fess_config.properties`` (``___change__me___``), la 15.10 écrit un avertissement dans ``fess.log`` au démarrage. Les processus de tâches tels que le crawler n'en écrivent pas.
Cette clé chiffre des valeurs telles que les mots de passe enregistrés dans les configurations de crawl et de magasin de données, et la valeur fournie est publique. |Fess| ne modifie pas la clé automatiquement. Après modification, les valeurs chiffrées avec l'ancienne clé ne peuvent plus être déchiffrées ; définissez-la donc avant la mise en exploitation.

Autres changements de comportement
----------------------------------

- « Tout supprimer » dans les écrans « Rechercher » et « Informations sur l'exploration » de l'interface d'administration requiert le rôle d'édition (``admin-searchlist``, ``admin-crawlinginfo``). Jusqu'à la 15.9, seul le bouton était masqué : les requêtes d'un utilisateur ne possédant qu'un rôle de consultation (un rôle portant le suffixe ``-view``) étaient tout de même acceptées.
- Le texte converti (``output``) d'une entrée du dictionnaire de mappage est obligatoire. Jusqu'à la 15.9, l'interface d'administration et l'API d'administration acceptaient une entrée sans ce champ et n'enregistraient rien.
- Dans une recherche, un mot unique entre guillemets doubles (tel que ``"less"``) ne correspond qu'à ce mot. Jusqu'à la 15.9, un mot d'au moins ``query.boost.fuzzy.min.length`` (valeur par défaut ``4``) caractères recevait aussi des conditions de correspondance approximative, de sorte que les documents contenant ``fess`` correspondaient aussi à ``"less"``. Les mots sans guillemets et les mots dont le champ est précisé (tels que ``content:"less"``) ne changent pas.

.. _upgrade-1510-tika:

Apache Tika 4 et ``tika.xml``
-----------------------------

La version 15.9.0 utilisait Apache Tika 3.3.2 ; la version 15.10 utilise Apache Tika 4.1.0.
Tika 4 n'a pas de fichier de configuration XML : |Fess| 15.10 construit donc l'analyseur Tika dans le code et ne lit plus ``tika.xml``.
Les paquets ZIP et RPM/DEB ainsi que les images Docker de la version 15.10 ne contiennent pas ce fichier.

Les paramètres que vous aviez saisis dans ``tika.xml``, tels que ``parser-exclude``, ne sont plus appliqués : un analyseur que vous y aviez exclu s'exécute de nouveau.
Si un fichier ``tika.xml`` d'une version antérieure se trouve dans le répertoire de configuration, |Fess| l'ignore et écrit un avertissement dans ``fess.log`` au démarrage. Supprimez ce fichier.

- Paquet ZIP : dans le ZIP de la version 15.9 et des versions antérieures, le fichier se trouve dans ``app/WEB-INF/classes/tika.xml``. L'avertissement au démarrage de la version 15.10 vérifie à la fois ``app/WEB-INF/classes`` et ``app/WEB-INF/conf``
- Paquet RPM/DEB : ``/etc/fess/tika.xml``

.. _upgrade-1510-tika-metadata:

Noms de métadonnées
-------------------

Tika 4 a renommé de nombreux noms de métadonnées. Par exemple, ``pdf:charsPerPage`` devient ``pdf:chars-per-page``, ``access_permission:*`` devient ``access-permission:*`` et ``Message:*`` devient ``message:*``.
|Fess| rétablit les noms de Tika 3 pour les noms que le ``LegacyKeyMigrationFilter`` de Tika connaît ; une entrée de ``crawler.metadata.name.mapping`` qui utilise l'un de ces noms continue donc de fonctionner.
Un nom que le filtre ne convertit pas est transmis sous son nom Tika 4. Par exemple, ``protected`` d'un fichier Excel devient ``msoffice:excel:protected-worksheet``. Si une entrée de ``crawler.metadata.name.mapping`` utilise un tel nom, remplacez-le par le nom de Tika 4.

Les métadonnées que Tika 4 ajoute sont traitées comme les autres : elles sont ajoutées au contenu, sauf si ``crawler.metadata.content.excludes`` correspond à leur nom.

L'exception concerne les noms qui commencent par ``tk:``, ``X-TIKA:`` ou ``zip:``, que Tika utilise pour sa gestion interne (``X-TIKA:Parsed-By`` de Tika 3 devient ``tk:parsed-by``). |Fess| les supprime avant qu'ils n'atteignent le document. Ils ne sont pas rétablis sous les noms de Tika 3 et ne sont pas ajoutés au contenu, qu'ils figurent ou non dans ``crawler.metadata.content.excludes``. Si vous associez des noms ``X-TIKA:*`` ou ``tk:*`` dans ``crawler.metadata.name.mapping`` ou les utilisez dans un script, vous n'obtenez plus ces valeurs.

Métadonnées des images dans le contenu
--------------------------------------

Jusqu'à la version 15.9, toutes les métadonnées d'un fichier image (PNG, JPEG, TIFF, GIF, BMP, etc.) étaient ajoutées au contenu ; le contenu d'une image était donc une liste de valeurs sur ses pixels, son profil colorimétrique et les réglages de l'appareil photo.
Dans la version 15.10, seules les métadonnées dont le nom correspond à ``crawler.metadata.content.image.includes`` sont ajoutées au contenu d'un document dont le type MIME est ``image/*``. Par défaut, ce sont le titre, la description, le créateur, les mots-clés, les commentaires, le copyright et les noms de lieux d'EXIF, XMP et IPTC, les propriétés de l'Explorateur Windows et les segments de texte d'un PNG.
Les autres métadonnées sont toujours extraites ; elles peuvent donc être utilisées dans ``crawler.metadata.name.mapping`` et dans les scripts. ``crawler.metadata.content.excludes`` s'applique aussi aux noms que la liste retient.

Le contenu d'une image indexée avant la mise à niveau ne change qu'au prochain crawl de cette image.

Fichiers de propriétés Tesseract et PDF d'une configuration de crawl
--------------------------------------------------------------------

Si une configuration de crawl définit ``config.tika.tesseract.config`` ou ``config.tika.pdf.config``, vérifiez les fichiers de propriétés, car Tika 4 a renommé ou supprimé certaines propriétés.
Pour chaque clé qu'il ne peut pas appliquer, |Fess| écrit un avertissement dans ``fess-crawler.log`` et ignore la clé.

- ``timeoutSeconds`` du fichier Tesseract devient ``timeoutMillis``. |Fess| convertit ``timeoutSeconds`` en ``timeoutMillis`` (valeur multipliée par 1000), mais écrivez désormais ``timeoutMillis`` en millisecondes. ``crawler.document.ocr.timeout`` reste exprimé en secondes.
- Des propriétés du fichier PDF, telles que ``ocrStrategy``, ``ocrDPI``, ``ocrImageType``, ``ocrImageFormatName``, ``ocrImageQuality``, ``ocrRenderingStrategy``, ``accessChecker`` et ``renderer``, ont été supprimées de ``PDFParserConfig`` de Tika 4. |Fess| les ignore et écrit un avertissement dans ``fess-crawler.log``. L'OCR des PDF suit alors le comportement par défaut de Tika 4 : automatique, c'est-à-dire que les pages contenant peu de texte passent par l'OCR lorsque ``tesseract`` est disponible et que l'OCR est activé dans |Fess|.
- L'emplacement de ``tesseract`` ne peut plus être défini dans ``tika.xml``, et ``tesseractPath``, ``tessdataPath`` et ``imageMagickPath`` n'ont aucun effet dans le fichier Tesseract. La commande ``tesseract`` (et ImageMagick, si vous l'utilisez) doit être trouvée dans le ``PATH`` du processus du crawler.

Détection de l'encodage des caractères
--------------------------------------

Les noms d'encodage des caractères que Tika 4 indique pour les fichiers texte peuvent différer de ceux de la version 15.9. Par exemple, Shift_JIS est indiqué comme ``windows-31j``, ISO-8859-1 comme ``windows-1252`` et EUC-JP comme ``x-eucJP-Open``.

``Content-Length`` n'est plus ajouté au contenu
-----------------------------------------------

Les versions 15.8.0 et 15.9.0 ajoutaient la valeur de la métadonnée ``Content-Length`` au contenu d'un document. Pour un fichier texte brut, la valeur était ``0`` : le contenu indexé se terminait donc par un espace et ``0``.
La version 15.10 n'ajoute pas ``Content-Length`` au contenu, que ``crawler.metadata.content.excludes`` le mentionne ou non. La valeur est toujours extraite et reste donc utilisable dans ``crawler.metadata.name.mapping`` et dans les scripts.
Le contenu d'un document indexé avant la mise à niveau ne change qu'à la prochaine exploration de ce document.

Limite de tentatives du formulaire de connexion
-----------------------------------------------

Dans la version 15.9, les limites de ``theme.api.login.rate.limit.*`` ne s'appliquaient qu'à ``/api/v2/auth/login`` et non au formulaire de connexion de la page de connexion (``/login/``).
Dans la version 15.10, le formulaire utilise les mêmes limites et les mêmes compteurs. Lorsque les connexions échouées depuis la même adresse IP atteignent 10 par minute, ou que le mot de passe du même nom d'utilisateur est refusé 5 fois depuis la même adresse IP, les connexions depuis cette adresse IP, ou depuis cette combinaison d'adresse IP et de nom d'utilisateur, sont refusées pendant ``theme.api.login.lockout.seconds`` (900 secondes par défaut).
Pendant le blocage, même le bon mot de passe ne permet pas de se connecter, et la page affiche le même message que pour un mot de passe erroné. Une connexion réussie rend la place que la tentative a utilisée.
Tenez compte de cette limite pour les scripts susceptibles d'envoyer un mot de passe erroné et pour les sites où de nombreux utilisateurs partagent une même adresse IP.

Lorsqu'un reverse proxy ajoute ``X-Forwarded-For`` comme ligne d'en-tête distincte (par exemple ``option forwardfor`` de HAProxy), la version 15.10 lit toutes les lignes et utilise comme IP du client la première adresse, en partant de la droite, qui n'est pas un proxy de confiance (voir :doc:`../config/rate-limiting`). Jusqu'à la version 15.9, seule la première ligne, celle envoyée par le client, était lue ; un client pouvait donc choisir l'adresse utilisée par la limite.

(deny) dans le champ des permissions d'une configuration d'exploration
----------------------------------------------------------------------

Si vous écrivez ``(deny)`` suivi d'une espace dans le champ des permissions d'une configuration d'exploration ou d'un paramètre similaire, par exemple ``(deny) {user}name``, la version 15.9 ne l'enregistrait pas comme un refus : elle enregistrait le texte avec l'espace tel quel. Ouvrir cette configuration dans l'écran d'administration puis l'enregistrer la transformait en autorisation (``{user}name``).
La version 15.10 supprime l'espace après ``(deny)`` et ``(allow)`` avant l'enregistrement, et un nouvel enregistrement conserve un refus comme refus. Une ligne ``(deny)`` qui ne contient ni ``{user}``, ni ``{group}``, ni ``{role}`` n'est pas enregistrée.

Un paramètre enregistré dans la version 15.9 ou une version antérieure n'est pas réparé automatiquement. Vérifiez le champ des permissions de chaque configuration d'exploration qui utilise ``(deny)``, réécrivez la ligne sous la forme ``(deny){user}name``, enregistrez-la, puis relancez l'exploration.

Caractères de contrôle dans audit.log
-------------------------------------

Au format LTSV, tout caractère de contrôle d'un champ, ainsi que les séparateurs de ligne Unicode NEL, LS et PS, est remplacé par une espace (une tabulation par un trait de soulignement), de sorte qu'un nom d'utilisateur saisi ne puisse pas commencer un second enregistrement. La version 15.9 ne remplaçait que CR et LF.

Modifications pour les développeurs de plugins
----------------------------------------------

Les modifications suivantes concernent les plugins qui utilisent des classes de ``fess-crawler``. Recompilez un tel plugin pour la version 15.10 (voir :ref:`upgrade-plugin-versions`).

- ``ExtractData`` n'implémente plus les interfaces de Tika (``TikaCoreProperties``, ``HttpHeaders``, etc.). Les constantes de type chaîne ``CONTENT_TYPE`` et ``CONTENT_ENCODING`` sont déclarées par ``ExtractData`` lui-même. ``RESOURCE_NAME_KEY`` vaut toujours ``"resourceName"``.
- ``TikaExtractor.setTikaConfig`` et le composant ``tikaConfig`` de ``fess.xml`` ont été supprimés.
- Au niveau de journalisation ``debug``, ``CrawlJob`` ne transmet plus ``-Dorg.apache.tika.service.error.warn=true`` au crawler, car Tika 4 ne lit plus cette propriété.

Plugins construits pour la version 15.9
---------------------------------------

Des plugins construits pour la version 15.9.0 ont pu être installés, démarrés et utilisés pour explorer sur le war de la version 15.10 sans être reconstruits. Il s'agit du résultat d'une vérification et non d'une garantie de compatibilité, et un plugin qui utilise des classes de ``fess-crawler`` doit toujours être reconstruit, comme indiqué dans « Modifications pour les développeurs de plugins ».

Remplacez malgré tout les plugins par les versions de la 15.10 (voir :ref:`upgrade-plugin-versions`). ``bin/fess-setup check`` signale le jar d'un plugin de la 15.9.0 comme FAIL (« construit pour une autre version ») et renvoie à ``upgrade plugins``.

En particulier, ne conservez pas les jar de la 15.9.0 de ``fess-storage-s3`` et ``fess-storage-gcs``. Ces plugins de la 15.9.0 ne renvoient pas d'erreur lorsque la liste du stockage échoue. Lorsque le stockage est injoignable, que les identifiants sont erronés ou que le bucket n'existe pas, ``/api/admin/storage/list`` de l'API d'administration répond donc quand même par une liste vide réussie, ``{"items":[],"status":0}``. Les plugins de la 15.10 lèvent l'échec sous forme d'exception, et la 15.10 en fait une réponse d'erreur. Si les anciens jar restent en place, cette amélioration de la 15.10 n'a aucun effet.

Mise à niveau de 15.8 vers 15.10
================================

Si vous effectuez une mise à niveau depuis la 15.8, les changements suivants ne sont pas
rétrocompatibles. Si vous effectuez une mise à niveau depuis la 15.7 ou antérieure, ils s'appliquent
aussi à vous : lisez toutes les sections de « Suppression de l'OpenSearch intégré » à « Appliquer
les nouveaux champs et la normalisation des kana à un index de documents existant » (l'OpenSearch
intégré, le moteur de script, les plugins S3 et SSO, la tâche Index Exporter, etc.), puis
« Migrations selon les fonctionnalités » à la fin de cette page.

Suppression de l'OpenSearch intégré
-----------------------------------

Jusqu'à la 15.8, démarrer ``bin/fess`` sans définir ``SEARCH_ENGINE_HTTP_URL`` amenait |Fess| à
exécuter un nœud OpenSearch dans sa propre JVM. Cette configuration disparaît en 15.10 : le moteur
de recherche est toujours un serveur distinct.

``bin/fess.in.sh`` définit désormais ``SEARCH_ENGINE_HTTP_URL=http://localhost:9200`` par défaut.
|Fess| refuse de démarrer si aucun OpenSearch n'est joignable. ``bin/fess-setup install
opensearch`` en installe un (Linux et Windows uniquement ; OpenSearch ne publie pas de version
macOS, utilisez donc Homebrew ou Docker).

|Fess| a également besoin que ``FESS_DICTIONARY_PATH`` corresponde à ``configsync.config_path``
dans le fichier ``opensearch.yml`` de cet OpenSearch ; sans cela, |Fess| ne peut pas créer ses
index. Le ``bin/fess.in.sh`` de la 15.10 (``bin\fess.in.bat`` sous Windows) le définit par lui-même
lorsque ``opensearch/`` dans le répertoire de |Fess| contient exactement un OpenSearch installé par
``bin/fess-setup install opensearch``. Pour tout autre OpenSearch, définissez-le comme décrit dans
:doc:`install-linux` ou :doc:`install-windows`.

Sont également supprimés :

- le répertoire ``es/`` (``es/modules``, ``es/plugins`` et ``es/data``)
- ``-Dfess.es.dir`` et ``SEARCH_ENGINE_HOME``
- ``bin/module.xml`` et ``bin/plugin.xml``
- les valeurs de repli des anciennes clés de configuration ``elasticsearch.*``

Un moteur antérieur à OpenSearch 3 interrompt désormais le démarrage, alors que la 15.8 se
contentait de journaliser une erreur et de poursuivre. Ces versions n'implémentent pas le tri
``_shard_doc`` dont dépendent toutes les opérations parcourant l'ensemble des résultats, et via
HTTP une telle requête reste bloquée au lieu d'échouer.

.. warning::

   Les données d'index d'une installation intégrée ne peuvent pas être reprises. Mettez en place
   un nouveau serveur OpenSearch externe, transférez les paramètres via la page Sauvegarde de
   l'administration, puis relancez une exploration. La sauvegarde couvre les paramètres
   d'exploration, les utilisateurs et les journaux ; elle ne contient **pas** les documents
   explorés.

.. note::

   Deux points à connaître lorsque vous restaurez une sauvegarde de la 15.8 sur le nouveau serveur
   15.10 :

   - Les tâches ne sont restaurées que si elles sont plus récentes que celles du serveur. Les tâches
     fournies que vous n'avez jamais modifiées sous 15.8 gardent donc leur version JavaScript de la
     15.10. Une tâche que vous avez modifiée ou créée sous 15.8 revient avec le moteur de script avec
     lequel elle a été enregistrée, soit ``groovy`` pour une tâche fournie, et sans le plugin
     ``fess-script-groovy`` elle échoue avec ``groovy is not found``. Installez le plugin ou faites
     passer ces tâches à JavaScript ; les deux sont décrits dans :ref:`upgrade-159-script-engine`.
   - Les mots de passe et secrets enregistrés dans les paramètres de l'authentification Web, des
     configurations d'exploration et des configurations DataStore sont chiffrés avec
     ``app.cipher.key``. Définissez la valeur de l'ancienne installation dans le
     ``fess_config.properties`` du nouveau serveur, comme décrit dans
     :ref:`upgrade-159-carried-over-config` ; sinon ils ne peuvent pas être déchiffrés.

Le robot Playwright passe dans un plugin
----------------------------------------

Le robot Playwright, ainsi que les exécutables Node.js qu'il utilise, ne font plus partie de la
distribution. Dans ``fess-15.8.0.zip`` (457,1 Mio), le paquet de pilotes Playwright qui contenait
les exécutables Node.js occupait 204,3 Mio.

Si une configuration d'exploration désigne le client Playwright, par exemple avec
``client.crawlerClients=playwright:http://.*`` dans ses paramètres, installez à la fois le
plugin et Node.js. Le plugin s'installe également depuis la page **Système > Plugin** de l'écran
d'administration. ``bin/fess.in.sh`` détecte Node.js et définit ``PLAYWRIGHT_NODEJS_PATH``.

::

    $ bin/fess-setup install plugin fess-crawler-playwright
    $ bin/fess-setup install nodejs

Sans le plugin, une telle configuration est toujours explorée, mais avec le client HTTP ordinaire :
le texte produit uniquement par JavaScript n'est donc pas indexé. La tâche d'exploration se termine
malgré tout avec succès et aucune URL en échec n'est enregistrée. À chaque exploration,
``fess-crawler.log`` consigne un avertissement par configuration d'exploration, qui nomme le plugin
et les deux commandes ci-dessus.

Le plugin ``fess-thumbnail-playwright``, qui génère avec Playwright les vignettes des pages HTML,
s'exécute lui aussi sur Node.js. Si vous l'utilisez, installez Node.js avec
``bin/fess-setup install nodejs`` ; la même installation sert aux deux plugins.

Rien à faire si vous n'utilisez ni le robot Playwright ni le plugin ``fess-thumbnail-playwright``.

Google Cloud Storage passe dans un plugin
-----------------------------------------

Le SDK Google Cloud Storage ne fait plus partie de la distribution : l'exploration ``gcs://``
et le type de stockage ``gcs`` proviennent désormais du plugin ``fess-storage-gcs``.
Installez-le depuis la page **Système > Plugin** de l'écran d'administration ou avec la
commande ci-dessous.

::

    $ bin/fess-setup install plugin fess-storage-gcs

``gcs`` a également quitté la valeur fournie de ``crawler.file.protocols``, qui est
maintenant ``file,smb,smb1,ftp`` ; le plugin la rétablit lors de son installation.
Jusque-là, une configuration d'exploration de fichiers dont le chemin commence par ``gcs:``
est signalée par un avertissement et ne récupère rien. Une installation mise à niveau conserve
son propre ``crawler.file.protocols``, le chemin est donc toujours accepté mais aucun client
d'exploration ne le prend en charge ; dans une nouvelle installation, ``gcs:`` n'est pas un
protocole configuré, l'écran d'administration refuse donc d'enregistrer le chemin et un chemin
enregistré auparavant est lu comme un chemin de fichier local. La page de stockage journalise
elle aussi un avertissement et affiche l'échec comme une erreur nommant le plugin à installer,
là où elle n'affichait auparavant qu'une liste de fichiers vide.

Rien à faire si vous n'utilisez pas Google Cloud Storage. Amazon S3 et les stockages
compatibles S3 tels que MinIO sont passés dans un plugin de la même manière ; voir la section
suivante.

Amazon S3 passe dans un plugin
------------------------------

Le SDK AWS ne fait plus partie de la distribution : l'exploration ``s3://`` et les types de
stockage ``s3`` et ``s3_compat`` proviennent désormais du plugin ``fess-storage-s3``.
Installez-le depuis la page **Système > Plugin** de l'écran d'administration ou avec la
commande ci-dessous.

::

    $ bin/fess-setup install plugin fess-storage-s3

``s3`` a également quitté la valeur fournie de ``crawler.file.protocols``, qui est maintenant
``file,smb,smb1,ftp`` ; le plugin la rétablit lors de son installation. ``storage.type`` vaut
toujours ``auto`` par défaut, ce qui se résout en S3 lorsque aucun point de terminaison n'est
défini : la page de stockage de l'écran d'administration ne fonctionne donc qu'après
l'installation du plugin, même si vous n'avez jamais indiqué ``s3`` vous-même. Vos valeurs
``storage.*`` sont conservées, car elles se trouvent dans ``WEB-INF/conf/system.properties``,
et un ``crawler.file.protocols`` existant n'est pas non plus remplacé par la mise à niveau.

Rien à faire si vous n'utilisez pas Amazon S3 ni un stockage compatible S3 tel que MinIO.

L'authentification SSO passe dans des plugins
---------------------------------------------

Aucun des quatre authentificateurs SSO ne fait plus partie de la distribution : chaque valeur
de ``sso.type`` provient désormais de son propre plugin, qui embarque la bibliothèque
d'identité dont il a besoin : ``saml`` de ``fess-sso-saml``, ``spnego`` de
``fess-sso-spnego``, ``entraid`` (et l'ancien ``aad``) de ``fess-sso-entraid`` et ``oic`` de
``fess-sso-oidc``. Notez la dernière paire : le plugin s'appelle ``fess-sso-oidc`` alors que la
valeur de ``sso.type`` reste ``oic`` ; c'est le seul endroit où les deux diffèrent. Installez
celui que vous utilisez depuis la page **Système > Plugin** de l'écran d'administration ou avec
la commande ci-dessous.

::

    $ bin/fess-setup install plugin fess-sso-saml

Vos paramètres sont conservés, car ``sso.type`` et les clés ``saml.*``, ``spnego.*``,
``entraid.*``, ``aad.*`` et ``oic.*`` se trouvent dans ``WEB-INF/conf/system.properties``. De
plus, « Système » → « Général » de l'écran d'administration propose toujours les quatre types
et affiche toujours leurs paramètres, car un plugin ne peut pas fournir de JSP : rien sur cet
écran ne signale donc un plugin manquant.

Jusqu'à l'installation du plugin, une requête vers ``/sso/`` est redirigée vers la page de
connexion, qui signale l'échec de la connexion SSO, et personne ne peut se connecter via le
SSO. La 15.10 journalise dans ``fess.log`` un avertissement nommant le composant recherché et le
plugin qui le fournit, là où jusqu'à la 15.8 rien n'était journalisé à aucun niveau.

Le plugin ``oic`` est plus strict que l'authentificateur de la 15.8. ``oic.token.server.url`` doit
être en HTTPS (``http`` uniquement pour ``localhost``, ``127.x.x.x`` et ``::1``), les claims
``aud`` et ``exp`` de l'ID Token sont vérifiés, et ``iss`` est vérifié lorsque la nouvelle clé
``oic.issuer`` est définie. Pour plus de détails, consultez :doc:`../config/sso-oidc`.

En 15.8, ``oic.token.server.url`` pouvait être une URL ``http`` vers n'importe quel hôte. En 15.10, ``http`` vers un nom de service Docker Compose (par exemple ``http://keycloak:8080/...``) ou un nom d'hôte interne est refusé, même s'il désigne la même machine. La connexion échoue alors et ``fess.log`` contient un avertissement commençant par ``Failed to process the OpenID Connect callback: oic.token.server.url must be https``. Passez le endpoint de token en URL HTTPS avant la mise à jour.

Définissez aussi ``oic.issuer`` avec la valeur ``issuer`` du document Discovery de l'OP. Sans cette valeur, ``iss`` n'est pas vérifié et un avertissement est journalisé lors de la première connexion après le démarrage. Définir ``oic.issuer`` n'assouplit pas la règle HTTPS.

Rien à faire si vous n'utilisez pas le SSO, c'est-à-dire si ``sso.type`` vaut ``none`` ou n'est
pas défini.

.. _upgrade-159-script-engine:

Le moteur de script intégré passe de Groovy à JavaScript
--------------------------------------------------------

Jusqu'à la 15.8, le moteur de script intégré était Groovy et ``job.default.script`` avait pour
valeur par défaut ``groovy``. En 15.10, le moteur intégré est JavaScript et la valeur par défaut
est ``javascript``. Groovy n'est plus intégré : il est fourni par le plugin
``fess-script-groovy``, qui doit être installé pour qu'un ``scriptType`` valant ``groovy`` puisse
être résolu.

Une mise à niveau ne modifie pas le moteur enregistré avec un paramètre, et un paramètre enregistré
avant la 15.10 sans moteur compte comme ``groovy``. Sans le plugin, les éléments suivants cessent de
fonctionner :

- Les tâches planifiées enregistrées en ``groovy``. **Cela concerne aussi les tâches que la 15.8 a
  créées elle-même :** Default Crawler, Suggest Indexer, Config Reloader, Log Aggregator, Doc
  Purger et les autres tâches fournies sont toutes enregistrées en ``groovy``, et au démarrage la
  15.10 n'ajoute que les tâches fournies qui n'existent pas encore : elle ne les modifie donc pas.
  Chacune d'elles échoue à chaque déclenchement planifié, si bien que Default Crawler n'explore
  plus rien. La plupart des tâches fournies ont « Journalisation » désactivée : leurs échecs
  n'apparaissent pas dans le journal des tâches, seulement sous la forme d'avertissements
  ``Failed to execute job`` dans ``fess.log``.
- Les configurations d'exploration Web et de fichiers dont les « Paramètres de configuration »
  contiennent des scripts de champ (``field.script.<nom du champ>``). Chaque document d'une telle
  configuration échoue avec une ``ScriptEngineException`` et est enregistré comme URL en échec,
  alors que la tâche d'exploration elle-même se termine avec succès.
- Les configurations DataStore dotées d'un « Script ». Les valeurs qui ne sont pas un simple nom de
  paramètre ne peuvent pas être évaluées ; voir :doc:`../config/datastore/ds-overview`.
- Les règles de boost de document. Une telle règle ne booste rien.
- Les mappages de chemin dont le « Remplacement » commence par ``groovy:``. Un tel mappage n'est
  pas appliqué et les URL restent inchangées.

Après le premier démarrage, recherchez dans ``fess.log`` un avertissement commençant par
``Settings use the script engine groovy, which is not registered``. |Fess| vérifie une fois au
démarrage les paramètres ci-dessus et indique, pour chaque type, combien utilisent un moteur
qu'aucun plugin ne fournit. Il mentionne aussi ``job.default.script`` lorsqu'un
``fess_config.properties`` repris de la 15.8 indique encore ``groovy`` ; dans ce cas, les tâches
créées après la mise à niveau utilisent elles aussi Groovy (voir
:ref:`upgrade-159-carried-over-config`). Deux solutions sont possibles :

- Installez le plugin et redémarrez |Fess|. Les scripts Groovy enregistrés s'exécutent alors sans
  modification et l'avertissement n'est plus journalisé. Le plugin peut aussi être installé depuis
  « Système » → « Plugins » dans l'écran d'administration.

  ::

      $ bin/fess-setup install plugin fess-script-groovy

- Passez chaque paramètre à JavaScript. Réécrivez d'abord toute syntaxe que seul Groovy accepte,
  puis sélectionnez JavaScript :

  - Tâches planifiées : sous « Système » → « Planificateur », réglez « Méthode d'exécution » sur
    ``javascript``. Les scripts des tâches fournies sont du JavaScript valide tels quels, à deux
    exceptions près : Thumbnail Purger utilise le littéral ``long`` Groovy ``1000L``, que
    JavaScript refuse (écrivez ``1000``), et Index Exporter nécessite la modification décrite dans
    :ref:`upgrade-159-index-exporter`. Un littéral de tableau JavaScript est converti
    automatiquement en ``String[]`` Java, ce qui rend inutiles les conversions ``as String[]`` de
    la forme Groovy :

    ::

        return container.getComponent("crawlJob").logLevel("info").webConfigIds(["1", "2"]).fileConfigIds(["1"]).dataConfigIds([]).execute(executor);

  - Configurations d'exploration Web et de fichiers : ajoutez ``config.script.type=javascript``
    aux « Paramètres de configuration ».
  - Configurations DataStore : ajoutez ``script_type=javascript`` aux « Paramètres ».
  - Règles de boost de document : réglez « Type de Script » sur ``javascript``.
  - Mappages de chemin : commencez le « Remplacement » par ``javascript:`` au lieu de
    ``groovy:``.
  - ``job.default.script`` : définissez-le sur ``javascript`` dans un ``fess_config.properties``
    repris de la 15.8.

``crawler.default.script`` a été supprimé
-----------------------------------------

``crawler.default.script`` n'existe plus dans ``fess_config.properties``. Supprimez-le de votre
configuration ; une valeur laissée sous ce nom n'a aucun effet.

Le protocole de crawl ``storage`` a été supprimé
------------------------------------------------

``storage`` n'est plus accepté dans ``crawler.file.protocols`` ; la valeur fournie est
``file,smb,smb1,ftp``. Utilisez ``s3`` à la place et remplacez par un chemin ``s3:`` toute
configuration de crawl de fichiers dont le chemin commence par ``storage:``. ``s3`` nécessite
le plugin ``fess-storage-s3``.

.. _upgrade-159-index-exporter:

La tâche Index Exporter désigne un paquet supprimé
--------------------------------------------------

La 15.10 ne contient plus les classes ``org.opensearch`` ; les constructeurs de requêtes utilisés
par les scripts de tâche se trouvent désormais sous ``org.codelibs.fesen.opensearch``. Le script
que la 15.8 a enregistré pour la tâche Index Exporter désigne
``org.opensearch.index.query.QueryBuilders`` et la mise à niveau ne le remplace pas : la tâche
échoue donc même avec ``fess-script-groovy`` installé. Elle est fournie désactivée et sans
planification, cela ne vous concerne donc que si vous l'exécutez. Ouvrez-la sous « Système » →
« Planificateur » et remplacez le paquet dans son script par celui de la 15.10 :

::

    return new org.codelibs.fess.job.IndexExportJob().query(org.codelibs.fesen.opensearch.index.query.QueryBuilders.matchAllQuery()).execute()

Modifiez de la même manière tout script de votre cru qui désigne ``org.opensearch.index.query``.
Voir :doc:`../config/admin-index-export` pour d'autres exemples de requêtes.

.. _upgrade-159-carried-over-config:

Fichiers de configuration repris de la 15.8
-------------------------------------------

La procédure ZIP de l'étape 3 copie ``fess_config.properties`` et ``bin/fess.in.sh`` depuis
l'ancienne installation, et une mise à niveau RPM conserve un ``/etc/fess/fess_config.properties``
que vous avez modifié (le fichier de la 15.10 est placé à côté sous le nom
``fess_config.properties.rpmnew``). Une mise à niveau DEB fait de même lorsque vous conservez votre
version à la question (le fichier de la 15.10 est placé à côté sous le nom
``fess_config.properties.dpkg-dist``). Dans tous les cas, la 15.10 fonctionne ensuite avec les
valeurs de la 15.8, y compris celles dont la valeur fournie a changé en 15.10. Vérifiez au moins les
clés suivantes.

.. list-table::
   :header-rows: 1

   * - Clé
     - 15.8.0
     - 15.10
     - Effet si la valeur de la 15.8 est conservée
   * - ``job.default.script``
     - ``groovy``
     - ``javascript``
     - Les tâches créées sous « Système » → « Planificateur » utilisent ``groovy`` par défaut et
       échouent sans le plugin ``fess-script-groovy``.
   * - ``job.template.script``
     - Forme Groovy avec ``as String[]``
     - Forme JavaScript
     - Une tâche créée depuis une configuration d'exploration reçoit un script Groovy.
   * - ``crawler.file.protocols``
     - ``file,smb,smb1,ftp,storage,s3,gcs``
     - ``file,smb,smb1,ftp``
     - Un chemin commençant par ``s3:`` ou ``gcs:`` est toujours accepté sans son plugin, puis
       ignoré avec un avertissement lors de l'exploration. ``storage`` n'est plus pris en charge.
   * - ``search_engine.http.url``
     - ``http://localhost:9201``
     - ``http://localhost:9200``
     - Utilisée lorsque ``SEARCH_ENGINE_HTTP_URL`` n'est pas défini, comme dans un
       ``bin/fess.in.sh`` copié de la 15.8 où vous ne l'avez pas défini. |Fess| cherche alors
       OpenSearch sur le port 9201, celui de l'OpenSearch intégré supprimé en 15.10.
   * - ``jvm.crawler.options``, ``jvm.thumbnail.options``
     - ``-Djcifs.smb.client.*``, ``-Djcifs.smb1.smb.client.*``
     - ``-Djcifs.client.*``
     - Les délais d'attente SMB restent aux valeurs par défaut de jcifs ; voir
       :ref:`upgrade-159-jcifs`.
   * - ``response.headers``
     - Contient la ligne ``text/html=Content-Security-Policy: reflected-xss block``
     - Ligne supprimée
     - La page de connexion, l'interface d'administration et les autres pages que |Fess| génère
       lui-même sont envoyées avec un en-tête ``Content-Security-Policy: reflected-xss block``
       qu'aucun navigateur ne reconnaît, et la console du navigateur consigne
       ``Unrecognized Content-Security-Policy directive 'reflected-xss'``. L'en-tête ne restreint
       rien. Supprimez la ligne, comme décrit ci-dessous.
   * - ``app.encrypt.property.pattern``
     - ``.*password|.*key|.*token|.*secret``
     - ``.*password|.*passphrase|.*key|.*token|.*secret``
     - Un paramètre dont le nom se termine par ``passphrase`` (par exemple ``ssh.passphrase`` d'une
       configuration DataStore) est enregistré en clair. Une valeur enregistrée auparavant reste en
       clair jusqu'à ce que le paramètre soit de nouveau enregistré avec le motif de la 15.10.
   * - ``index.backup.log.targets``
     - ``click_log.ndjson,favorite_log.ndjson,search_log.ndjson,user_info.ndjson``
     - ``chat_log.ndjson,click_log.ndjson,favorite_log.ndjson,search_log.ndjson,user_info.ndjson``
     - La page « Informations système » → « Sauvegarde » ne propose pas ``chat_log.ndjson``.
   * - ``index.export.exclude.fields``
     - ``cache``
     - ``cache,tag``
     - Le champ ``tag``, qui contient les tags des utilisateurs, n'est plus exclu des fichiers
       qu'écrit la tâche Index Export.
   * - ``crawler.default.script``, ``theme.allowed.archive.extensions``,
       ``theme.assets.cache.max.age``, ``theme.assets.precompressed``,
       ``rag.chat.message.max.length``, ``supported.uploaded.js.extentions``,
       ``supported.uploaded.css.extentions``, ``supported.uploaded.media.extentions``,
       ``supported.uploaded.files``, ``online.help.name.design``
     - Présentes
     - Supprimées
     - Aucun effet ; supprimez-les.

La valeur fournie de ``response.headers`` contient, de la 15.0 à la 15.8, la ligne
``text/html=Content-Security-Policy: reflected-xss block``. ``reflected-xss`` était une directive d'un
des premiers brouillons de Content-Security-Policy que les navigateurs ne reconnaissent plus ;
l'en-tête ne restreint donc rien et n'ajoute qu'une erreur dans la console. La 15.10 ne fournit plus
cette ligne (les lignes ``X-XSS-Protection`` et ``X-Frame-Options`` ne changent pas), mais un
``response.headers`` repris de la 15.8 la conserve. Supprimez uniquement cette ligne de
``response.headers`` dans ``fess_config.properties``. Le ``\n\`` à la fin de chaque ligne poursuit la
valeur sur la ligne suivante ; si vous supprimez la ligne entière, les autres restent intactes ::

    text/html=Content-Security-Policy: reflected-xss block\n\

Si vous définissez ``response.headers`` avec ``-Dfess.config.response.headers``, supprimez la même
entrée de cette valeur.

Un ``bin/fess.in.sh`` copié de la 15.8 ne contient pas non plus deux éléments présents dans le
fichier de la 15.10. Il laisse ``SEARCH_ENGINE_HTTP_URL`` non défini, sauf si vous l'avez défini
vous-même, alors que la 15.10 définit ``http://localhost:9200``, et il ne recherche pas le Node.js
installé par ``bin/fess-setup install nodejs`` : les plugins Playwright ne trouvent donc Node.js que si
vous définissez ``PLAYWRIGHT_NODEJS_PATH``.

Plutôt que de copier l'un ou l'autre fichier en entier, partez du fichier fourni avec la 15.10 et
réappliquez les valeurs que vous avez modifiées. ``diff`` les affiche ::

    $ diff /path/to/old-fess/app/WEB-INF/classes/fess_config.properties /path/to/fess-15.10.0/app/WEB-INF/classes/fess_config.properties
    $ diff /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.10.0/bin/fess.in.sh

Pour une mise à niveau RPM, comparez de la même manière ``/etc/fess/fess_config.properties`` avec
``/etc/fess/fess_config.properties.rpmnew``, et pour une mise à niveau DEB avec
``/etc/fess/fess_config.properties.dpkg-dist``. Un ``fess_config.properties`` que vous n'avez jamais
modifié est remplacé par le fichier de la 15.10 lors d'une mise à niveau DEB (voir l'étape 3) : il
part donc des valeurs de la 15.10.

``app.cipher.key`` est la seule valeur à reprendre même si la 15.10 ne l'a pas modifiée. C'est la
clé qui chiffre les mots de passe et secrets enregistrés dans les paramètres de l'authentification
Web, des configurations d'exploration et des configurations DataStore. Si la nouvelle installation
fonctionne avec une clé différente de celle qui les a enregistrés, parce que vous avez pris le
``fess_config.properties`` fourni ou restauré une sauvegarde sur un nouveau serveur, ils ne peuvent
pas être déchiffrés : ``fess-crawler.log`` consigne une ``CipherFailureException`` et une
exploration qui inclut une telle configuration peut n'indexer rien.

.. note::

   |Fess| 15.9 enregistre aussi le ``password`` de l'authentification Web et fichier chiffré avec ``app.cipher.key`` ;
   ``fess_basic_config.bulk`` et ``fess_config.bulk`` d'une sauvegarde contiennent donc les valeurs chiffrées. Lorsque
   vous restaurez sur une autre installation, reprenez la même ``app.cipher.key`` ; avec une clé différente, les
   explorations qui utilisent ces identifiants échouent avec une erreur. Une sauvegarde créée avant la 15.9 les contient
   en clair et continue de fonctionner (voir :doc:`../admin/backup-guide`).

.. _upgrade-159-jcifs:

Les délais d'attente SMB utilisent les noms de propriétés de jcifs 3
--------------------------------------------------------------------

jcifs, la bibliothèque qu'utilise |Fess| pour explorer les serveurs de fichiers SMB, a renommé ses
propriétés dans sa version 3 : ``jcifs.smb.client.*`` est devenu ``jcifs.client.*``, et les noms
distincts ``jcifs.smb1.smb.client.*`` pour SMB1 ont été regroupés dans ces mêmes propriétés.
Jusqu'à la 15.8, ``jvm.crawler.options`` et ``jvm.thumbnail.options`` transmettaient encore les
anciens noms, que jcifs ignore : les explorations SMB fonctionnaient donc avec les valeurs par
défaut de jcifs. La 15.10 transmet les nouveaux noms :

::

    -Djcifs.client.responseTimeout=30000
    -Djcifs.client.soTimeout=35000
    -Djcifs.client.connTimeout=60000
    -Djcifs.client.sessionTimeout=60000

Les délais de connexion et de session prennent donc effet pour la première fois et passent de la
valeur par défaut de jcifs, 35 secondes, à 60 secondes : une exploration attend désormais jusqu'à
60 secondes un serveur SMB qui ne répond pas. Les délais de réponse et de socket sont égaux aux
valeurs par défaut de jcifs et ne changent donc pas.

Si vous avez modifié ces délais, renommez-les dans les deux options. Sous les anciens noms, ils
n'avaient pas non plus d'effet en 15.8. Un ``fess_config.properties`` repris de la 15.8 conserve
les anciens noms, et avec eux les valeurs par défaut de jcifs.

Quatre propriétés sans effet ont été supprimées
-----------------------------------------------

Les clés suivantes n'existent plus dans ``fess_config.properties``. |Fess| ne les a jamais lues
dans ce fichier : une valeur laissée sous ces noms reste donc sans effet, comme auparavant.

- ``theme.allowed.archive.extensions``
- ``theme.assets.cache.max.age``
- ``theme.assets.precompressed``
- ``rag.chat.message.max.length``

La limite définie par ``rag.chat.message.max.length`` fonctionne toujours, mais elle est lue comme
propriété système : définissez-la dans ``app/WEB-INF/conf/system.properties`` ou avec
``-Dfess.system.rag.chat.message.max.length``, comme décrit dans :doc:`../config/rag-chat`.

.. _upgrade-159-static-theme:

L'écran de recherche est désormais un thème
----------------------------------------------------

L'écran de recherche est servi par le thème ``bootstrap``, fourni avec |Fess|, sauf si un
autre thème est sélectionné. Cela s'applique à ``/``, ``/search``, ``/advance``, ``/help``,
``/profile``, ``/cache``, ``/chat`` et aux pages d'erreur. Jusqu'à la 15.8, ces pages étaient des
JSP, sauf si un thème par défaut était défini.

Le basculement a également lieu lors de la mise à niveau. Une installation 15.8 qui n'a jamais
défini de thème par défaut n'a pas de ``theme.default`` dans ``system.properties`` : après la mise
à niveau, elle affiche donc le thème ; rien n'est écrit dans la configuration et rien
n'est journalisé. Aucun paramètre ne permet de revenir à l'écran de recherche JSP. Si vous aviez
défini un thème par défaut en 15.8, ce paramètre est conservé ; installez la version 15.10 du thème
(``bin/fess-setup install theme <name>``), car un thème par défaut qui désigne un thème non
installé se rabat sur ``bootstrap``, avec un avertissement dans ``fess.log``.

Si vous avez modifié les JSP, le CSS ou les images de l'écran de recherche, via « Conception de la
page » dans l'écran d'administration ou dans un plugin de thème JAR, ces modifications ne
s'affichent plus. Reportez-les dans un thème : copiez le thème fourni et modifiez la
copie, comme décrit dans :ref:`theme-customize-bundled`, ou installez un thème publié depuis
« Système » → « Thème » dans l'écran d'administration ou avec
``bin/fess-setup install theme <name>``. Une apparence propre à un hôte virtuel est désormais un thème portant le nom de
cet hôte virtuel ; voir :doc:`../config/security-virtual-host`.

Ces deux fonctionnalités ont également disparu :

- L'écran de connexion par hôte virtuel. Jusqu'en 15.8, l'enregistrement de « Système » → « Général »
  copiait les JSP, y compris l'écran de connexion, dans ``WEB-INF/view/<nom de l'hôte virtuel>/``, et
  on pouvait les modifier par hôte virtuel. 15.10 ne crée plus ces copies. L'écran de connexion
  (``/login/``) reste une JSP, mais tous les hôtes virtuels affichent la même, celle de
  ``WEB-INF/view/admin/login/``. Les JSP copiées auparavant ne sont pas utilisées.
- Les plugins de thème JAR (``fess-theme-*``). S'il est installé, un tel plugin est seulement placé
  comme un JAR générique de type ``jar`` et ne modifie aucun écran. Les JAR restants peuvent être
  supprimés depuis la page « Système » → « Plugin » ou avec ``bin/fess-setup remove plugin <name>``
  (voir :doc:`../dev/theme-development`).

Si, en 15.8, vous affichiez vos propres champs dans les résultats de recherche JSP, ajoutez les mêmes
champs à ``query.additional.api.response.fields`` en plus de ``query.additional.response.fields``.
Le thème obtient les résultats de recherche depuis ``/api/v2/search``.
``query.additional.response.fields`` ajoute seulement les champs récupérés depuis le moteur de
recherche, et cette API n'inclut dans sa réponse que les champs listés dans
``query.additional.api.response.fields`` (voir :doc:`../config/search-advanced`). Modifiez aussi le
thème pour qu'il affiche ces champs.

Ce que voient les clients
~~~~~~~~~~~~~~~~~~~~~~~~~

Les erreurs sont désormais rendues sur place, à l'URL demandée et avec le véritable statut HTTP.
Un navigateur (une requête dont l'en-tête ``Accept`` contient ``text/html``) reçoit la page
d'erreur du thème ; tout autre client reçoit un corps ``text/plain`` d'une ligne (par exemple
``Not Found.`` pour ``404``). Jusqu'à la 15.8, la plupart des erreurs répondaient par une
redirection ``302`` vers une page ``/error/...`` qui renvoyait elle-même ``200``. Vérifiez la
supervision, les contrôles de santé et les clients qui suivent les en-têtes ``Location`` ou
attendent des URL ``/error/``.

.. list-table::
   :header-rows: 1

   * - Requête
     - Jusqu'à la 15.8
     - 15.10
   * - ``/go/`` avec un paramètre manquant, ou pour un document qui n'existe pas
     - ``200``, ou ``302`` vers ``/error/``
     - ``400`` ou ``404``
   * - ``/thumbnail/`` avec un paramètre manquant, pour un document inconnu, ou sans vignette
     - ``200`` ou ``302``
     - ``400`` ou ``404``
   * - ``/sso/metadata`` et ``/sso/logout`` lorsque le type SSO configuré ne les prend pas en charge
     - ``302`` vers ``/error/badrequest/``
     - ``400``
   * - ``/api/v1/*``, ``/json`` et toute URL inconnue
     - ``302`` vers ``/error/notfound/``
     - ``404``
   * - Une exception non interceptée, y compris dans l'API d'administration
     - ``302`` vers ``/error/systemerror/``
     - ``500`` avec le corps ``System Error.`` (pas du JSON)
   * - ``/error/notfound/``, ``/error/badrequest/``, ``/error/systemerror/`` eux-mêmes
     - ``200``
     - ``404``, ``400``, ``500``

Avec ``login.required=true``, les pages de recherche ne redirigent plus un utilisateur anonyme.
Elles renvoient ``200`` avec le thème, qui demande à l'utilisateur de se connecter, et ce sont les
données sous-jacentes qui sont refusées : tous les points de terminaison ``/api/v2/`` autres que
``/health``, ``/auth/*`` et ``/ui/config``, y compris ``/api/v2/search``, répondent ``401`` tant
que l'utilisateur ne s'est pas connecté. ``/go/``, ``/thumbnail/`` et ``/osdd`` redirigent toujours
vers la connexion. Un contrôle qui attend une redirection pour une requête anonyme vers ``/`` doit
plutôt vérifier que ``/api/v2/search`` renvoie ``401``.

L'écran de recherche effectue aussi ses recherches via ``/api/v2/search`` : une recherche est donc
journalisée lorsque cette API est appelée, et non lorsque ``/search`` est demandé. Un client qui
n'exécute pas JavaScript reçoit la page sans résultats.

Le HTML de l'écran de recherche porte ``X-Frame-Options: DENY`` et un ``Content-Security-Policy`` avec
``frame-ancestors 'none'`` : aucune autre page ne peut l'afficher dans un cadre. L'écran de recherche JSP de
la 15.8 envoyait ``X-Frame-Options: SAMEORIGIN`` (valeur par défaut de ``response.headers``) et pouvait
s'afficher dans un ``iframe`` d'une page de la même origine. Si vous intégriez l'écran de recherche dans un
``iframe`` de la même origine, réglez ``theme.index.frame.ancestors`` dans ``fess_config.properties`` (par
défaut ``'none'``) sur ``'self'``. Pour l'intégrer depuis une autre origine, indiquez cette origine (voir
:doc:`../dev/theme-development`).

L'éditeur de conception de page a été supprimé
----------------------------------------------

[Système > Conception de la page] ne fait plus partie de l'écran d'administration : les fichiers
JSP, CSS et images de l'écran de recherche ne peuvent plus y être modifiés. Pour changer
l'apparence de l'écran de recherche, utilisez un thème (voir :ref:`theme-customize-bundled`).

Les clés suivantes ont également été supprimées de ``fess_config.properties``. Une valeur laissée
sous ces noms n'est pas utilisée.

- ``supported.uploaded.js.extentions``
- ``supported.uploaded.css.extentions``
- ``supported.uploaded.media.extentions``
- ``supported.uploaded.files``
- ``online.help.name.design``

Les rôles ``admin-design`` et ``admin-design-view`` n'accordent plus aucun droit. Un utilisateur qui
n'a que ces rôles arrive sur l'écran de recherche, et non sur l'écran d'administration, après
s'être connecté.

``api.access.token.required`` a été supprimé
--------------------------------------------

``api.access.token.required`` n'existe plus dans ``fess_config.properties``. Une valeur laissée sous
ce nom n'a aucun effet, y compris dans un ``fess_config.properties`` repris de la 15.8. Avec
``true``, ce paramètre refusait toute requête API d'un utilisateur non connecté. Comme l'écran de
recherche effectue désormais ses recherches via ``/api/v2/search``, il aurait en outre présenté aux
utilisateurs anonymes un écran de recherche sans résultats.

Une installation qui l'avait réglé sur ``true`` répond désormais aux requêtes API des utilisateurs
anonymes avec les rôles invités, comme pour l'écran de recherche. Pour empêcher les utilisateurs
anonymes de rechercher, définissez ``login.required=true``. Les jetons d'accès fonctionnent comme
avant : une requête munie d'un jeton d'accès enregistré reçoit les permissions de ce jeton, et une
requête munie d'un jeton non enregistré ou expiré est refusée.

.. _upgrade-159-api-requests:

Requêtes que l'API refuse désormais
-----------------------------------

La 15.10 refuse les requêtes suivantes, que la 15.8 acceptait. Vérifiez les clients et les scripts que vous
avez écrits pour la 15.8. L'API d'administration répond à un refus par HTTP ``400`` et ``status`` ``1`` dans
le corps.

.. list-table::
   :header-rows: 1

   * - Requête
     - Jusqu'à la 15.8
     - 15.10
   * - ``/api/v2/search`` avec ``facet.field`` ou ``facet.query`` et un ``facet.size`` inférieur ou égal à ``0``, ou un ``facet.size`` ou ``facet.minDocCount`` qui n'est pas un entier
     - ``200``, mais un résultat vide : ``record_count`` vaut ``0`` et ``partial`` vaut ``true``
     - ``400`` (``invalid_request``). ``facet.size`` doit valoir ``1`` ou plus
   * - ``track_total_hits=false``. Si ``query.track.total.hits`` vaut ``false``, toutes les recherches sont concernées
     - ``200``, mais sans résultat
     - La recherche est refusée (``/api/v2/search`` répond ``400`` avec ``invalid_request``). ``true`` et les entiers positifs fonctionnent comme avant
   * - Une entrée des dictionnaires ``mapping`` ou ``kuromoji`` qui répète une entrée existante, créée ou modifiée via l'API d'administration
     - Enregistrée. Le chargement du dictionnaire échoue ensuite, ce qui peut rendre la recherche indisponible
     - ``400``
   * - Une entrée du dictionnaire ``kuromoji`` dont le ``token`` contient une espace, ou dont ``segmentation`` et ``reading`` n'ont pas le même nombre d'éléments séparés par des espaces, créée ou modifiée via l'API d'administration
     - Enregistrée. Le chargement du dictionnaire échoue de la même façon
     - ``400``
   * - ``DELETE /api/admin/searchlist/doc/{doc_id}`` qui ne supprime rien : un ``doc_id`` qui n'existe pas, ou une valeur qui n'est pas un ``doc_id``, comme le ``_id`` de la liste des documents
     - ``200`` (``status`` ``0``) ; le document n'est pas supprimé
     - ``400``
   * - Un nom de rôle ou de groupe dans ``roles`` ou ``groups`` d'un utilisateur de l'API d'administration
     - Enregistré, mais le nom n'agit pas comme un rôle. Pour certains noms, la lecture de l'utilisateur échoue
     - ``400``. Indiquez l'ID du rôle ou du groupe (le ``id`` renvoyé par ``GET /api/admin/role/settings`` et ``GET /api/admin/group/settings``)
   * - Un utilisateur de l'API d'administration dont le mot de passe enfreint la politique de mot de passe (par exemple ``password.min.length``, ``8`` par défaut) ; une création sans mot de passe ; un ``confirm_password`` différent de ``password``
     - Enregistré ; l'utilisateur peut se connecter avec ce mot de passe
     - ``400``
   * - ``GET /api/admin/log/file/{id}`` avec un nom non autorisé pour un fichier journal (par exemple ne se terminant pas par ``.log`` ou ``.log.gz``), ou avec un fichier qui ne se trouve pas dans le répertoire des journaux
     - Nom non autorisé : ``200`` avec une réponse vide
     - ``400``
   * - Une entrée du dictionnaire ``mapping`` sans ``output``, ajoutée ou mise à jour via l'API d'administration
     - ``200`` (``id`` vaut ``0``) ; rien n'est enregistré
     - ``400``
   * - ``GET /api/admin/storage/list`` lorsque le stockage est inaccessible, y compris lorsqu'aucun plugin de client de stockage n'est installé
     - ``200`` (``status`` ``0``) avec une liste vide
     - ``400``. ``message`` indique la cause et, si le plugin est absent, le plugin à installer
   * - Connexions échouées répétées sur le formulaire de connexion (``POST /login/login``) en peu de temps, depuis une même adresse IP ou pour un même utilisateur depuis une même adresse IP
     - Aucune limite
     - Au-delà de la limite par adresse ou par utilisateur (``theme.api.login.rate.limit.per.ip.per.minute``, ``theme.api.login.rate.limit.per.user.per.minute``), les connexions suivantes depuis cette adresse (pour la limite par utilisateur : de cet utilisateur depuis cette adresse) sont refusées pendant ``theme.api.login.lockout.seconds`` secondes, même avec des identifiants corrects. La réponse est la même erreur de connexion qu'avec des identifiants erronés. Les limites et le verrouillage sont partagés avec ``/api/v2/auth/login`` (voir :doc:`../api/api-auth`) Derrière un proxy inverse dont l'adresse ne figure pas dans ``rate.limit.trusted.proxies``, tous les clients sont comptés comme une seule adresse, de sorte que des échecs répétés peuvent verrouiller tous les utilisateurs. Ajoutez l'adresse du proxy à ``rate.limit.trusted.proxies`` (un avertissement est consigné une seule fois dans ``fess.log`` lorsque ``X-Forwarded-For`` provient d'un pair non approuvé).

Les lignes de ``/api/v2/documents/all`` ne portent plus ``score``. Jusqu'à la 15.8, chaque document avait
son score de recherche ; la 15.10 parcourt tout le résultat avec un point in time et ``search_after``, ce qui
ne produit pas de score. ``/json?type=scroll`` et ``/api/v1/documents/all`` des plugins des anciennes API se
comportent de la même façon. Un script qui lit ``score`` doit tolérer son absence.

Les envois de fichiers de l'API d'administration (les six dictionnaires, ``badword``, ``elevateword`` et
``storage``) sont acceptés par ``POST``. La documentation de la 15.8 indiquait ``PUT``, mais un ``PUT`` en
``multipart/form-data`` ne transmet jamais le fichier : en 15.8 comme en 15.10, il échoue avec l'erreur de
validation indiquant que le fichier est obligatoire. Les points de terminaison ``PUT`` subsistent ; utilisez
``POST`` pour les envois.

Les modifications suivantes ne sont pas des refus, mais peuvent affecter les scripts et les clients de l'API et de l'écran d'administration.

- Les requêtes ``GET`` des API d'administration ``webauth`` et ``fileauth`` (``/api/admin/webauth/settings``, ``/api/admin/webauth/setting/{id}`` et les mêmes points d'accès sous ``fileauth``) ne renvoient plus le mot de passe enregistré. Un ``PUT`` qui omet le mot de passe ou l'envoie vide conserve le mot de passe enregistré ; un mot de passe non vide le remplace.
- Un utilisateur connecté est identifié par la session, et non par un paramètre ``userCode`` ou un cookie que porte la requête (par exemple pour l'API des favoris). Les utilisateurs anonymes continuent d'utiliser le paramètre et le cookie.
- « Tout supprimer » sur les écrans « Liste de recherche » et « Informations d'exploration » de l'écran d'administration exige le rôle d'édition (``admin-searchlist``, ``admin-crawlinginfo``). La requête d'un utilisateur qui n'a que le rôle de consultation (le rôle portant le suffixe ``-view``) est refusée.
- Si vous avez activé ``parameterKey``, ``headerKey`` ou ``cookieKey`` dans le composant ``roleQueryHelper`` de ``fess.xml`` sans définir de ``cipher``, et que l'indicateur de chiffrement (``encryptedParameterValue``, ``encryptedHeaderValue`` ou ``encryptedCookieValue``) est resté à ``true``, sa valeur par défaut, la 15.8 lisait la valeur comme une information de rôle non chiffrée. La 15.10 ignore la valeur et écrit un avertissement une seule fois dans le journal. Définissez un ``cipher`` si les valeurs sont chiffrées, ou mettez l'indicateur à ``false`` si elles doivent arriver non chiffrées.
- Une requête dont le ``Content-Type`` indique un jeu de caractères inconnu de la JVM (par exemple ``charset=nope``) est traitée comme une requête sans jeu de caractères. Auparavant, ``/api/v2/search`` répondait ``500`` (``internal_error``).
- Lorsqu'un envoi ou un téléchargement via l'API d'administration échoue pour le dictionnaire ``kuromoji``, ``mapping``, ``stemmeroverride`` ou ``synonym``, le message nomme désormais ce dictionnaire. En 15.8, il indiquait « protwords file » pour chacun d'eux.

``search_engine.type=cloud`` est obsolète
-----------------------------------------

La version 15.9 ajoute la valeur ``vanilla`` à ``search_engine.type`` pour un OpenSearch standard sans les plugins CodeLibs (voir :doc:`../config/search-engine-type`). ``cloud`` devient un alias obsolète de ``vanilla`` : il continue de fonctionner, mais |Fess| consigne un avertissement au démarrage. Remplacez-le par ``vanilla`` dès que l'installation fonctionne en 15.10. ``aws`` continue de fonctionner comme avant.

* ``vanilla`` nécessite la 15.9. |Fess| 15.8 et les versions antérieures ne connaissent pas cette valeur ; conservez donc ``cloud`` tant que vous pouvez encore revenir à la 15.8.
* Les définitions d'index de ``aws`` et de ``cloud`` sont désormais lues dans ``fess_indices/_vanilla/``. Les répertoires ``fess_indices/_aws/`` et ``fess_indices/_cloud/`` fournis n'existent plus, et un répertoire ``fess_indices/_aws/`` ou ``fess_indices/_cloud/`` que vous avez ajouté n'est plus lu. Reportez vos modifications dans ``fess_indices/_vanilla/``. Les index déjà existants ne sont pas modifiés.
* Les paramètres de suggestion que la 15.8 a enregistrés dans le moteur de recherche sont migrés automatiquement ; vous n'avez rien à faire.

Le DataStore CSV analyse les champs entre guillemets
----------------------------------------------------

Le plugin ``fess-ds-csv`` de la 15.10 interprète les guillemets par défaut. Un champ tel que
``"Yamada, Taro"`` forme une seule colonne, alors que le plugin de la 15.8.0 le coupait à la
virgule. Après ``bin/fess-setup upgrade plugins``, vérifiez les configurations DataStore qui lisent
des fichiers CSV contenant des champs entre guillemets. Pour conserver le comportement de la 15.8,
ajoutez ``quote_disabled=true`` aux « Paramètres » ; voir :doc:`../config/datastore/ds-csv`, qui
décrit aussi ce que fait un guillemet sans correspondance.

.. _upgrade-reindex-new-fields:

Appliquer les nouveaux champs et la normalisation des kana à un index de documents existant
-------------------------------------------------------------------------------------------

Au démarrage, la 15.10 ajoute de nouveaux champs aux index de configuration, de journaux et
d'utilisateurs. Dans l'index de documents, elle n'ajoute que le champ ``tag`` (``keyword``), qui
contient les tags des utilisateurs ; le reste du mapping et les paramètres d'analyse ne sont pas
modifiés. Si vous conservez un index de documents créé avec la 15.8 ou antérieure, les changements
suivants de la 15.10 ne prennent pas effet.

- **Propriétaire et dernier modificateur d'un fichier** (``owner``, ``last_modifier``) : nouveaux
  champs indexés par les crawls du système de fichiers, SMB et FTP. L'index de documents existant ne
  les définit pas ; la première valeur crawlée les mappe donc dynamiquement en ``text``, et les
  recherches comme ``owner:alice`` ou ``facet.field=owner`` ne fonctionnent pas comme prévu.
- **ETag** (``etag``) : le champ dans lequel le crawler stocke l'ETag d'une page crawlée, que la
  15.10 renvoie sous la forme ``If-None-Match`` afin qu'une page inchangée ne soit pas récupérée de
  nouveau. L'index de documents existant ne le définit pas non plus ; il est donc mappé
  dynamiquement en ``text`` au lieu du ``keyword`` non indexé fourni. Les requêtes conditionnelles
  fonctionnent quand même avec ce mapping.
- **Normalisation des variantes de kana et des tirets écrits à la place de la marque de voyelle
  longue** (par exemple, ``サ―バ－`` est traité comme le même mot que ``サーバー``) : les règles se
  trouvent dans les paramètres d'analyse de l'index de documents et dans le dictionnaire
  ``mapping.txt`` ; un index existant ne les reçoit donc pas.

Pour appliquer les deux, activez « Remplacer les alias » et « Réinitialiser les dictionnaires » sous
« Informations système » → « Maintenance » dans l'interface d'administration, puis lancez la
« Réindexation ». La réindexation copie les documents existants dans un nouvel index ; il n'est pas
nécessaire de recrawler.

.. warning::

   « Réinitialiser les dictionnaires » écrase les dictionnaires côté OpenSearch avec les fichiers de
   dictionnaire fournis. Si vous avez modifié des synonymes ou d'autres dictionnaires sous
   « Dictionnaire » dans l'interface d'administration, téléchargez-les d'abord et réappliquez-les
   après la réindexation : supprimez les entrées en double ou invalides des fichiers téléchargés
   (voir l'étape 7), téléversez-les, puis cliquez sur « Recharger » sous « Recharger l'index des
   documents » dans « Informations système » → « Maintenance ». Tant que vous ne le faites pas, les
   analyseurs de l'index de documents continuent d'utiliser les dictionnaires fournis et un synonyme
   restauré ne correspond pas, quelle que soit la durée de l'attente. Un dictionnaire qui s'applique
   à l'indexation exige aussi que les documents soient crawlés de nouveau ; voir
   :ref:`dict-apply-changes`.

.. note::

   Les fichiers indexés avec la 15.8 ou antérieure n'ont pas de valeur de propriétaire ni de dernier
   modificateur. Le crawl incrémental ne récupère pas à nouveau les fichiers inchangés ; pour ajouter
   les valeurs, désactivez temporairement « Vérifier la dernière modification » sous « Système » →
   « Général » et lancez un crawl.


Migrations selon les fonctionnalités
====================================

Si vous effectuez une mise à niveau depuis la version 15.7 ou antérieure vers la 15.10, les
actions suivantes sont nécessaires selon les fonctionnalités que vous utilisez.

Si vous utilisiez la recherche sémantique
-----------------------------------------

Le plugin ``fess-webapp-semantic-search``, qui fournissait la recherche sémantique dans les
versions 15.7 et antérieures, n'est plus nécessaire (obsolète) car cette fonctionnalité a été
intégrée au cœur du produit en 15.8. Vous devez supprimer le plugin, retirer
``-Dfess.semantic_search.*`` ainsi que ``-Drank.fusion.searchers=default,semantic``, et détacher
l'ancien pipeline d'ingestion. Pour la procédure, consultez :ref:`semantic-search-migration`
(:doc:`../config/search-semantic`).

Si vous utilisiez le mode de recherche IA (chat RAG)
----------------------------------------------------

À partir de la 15.6, la fonctionnalité du mode de recherche IA (chat RAG) a été séparée en
plugins tels que ``fess-llm-ollama``, ``fess-llm-openai`` et ``fess-llm-gemini``. Installez le
plugin correspondant au fournisseur que vous utilisez depuis « Système » → « Plugins » dans
l'écran d'administration. La 15.9 ajoute également ``fess-llm-bedrock`` pour Amazon Bedrock.

Si vous utilisiez SPNEGO (authentification intégrée Windows)
------------------------------------------------------------

À partir de la 15.8, une connexion SPNEGO est refusée lorsque le domaine Kerberos du principal
client diffère de celui du serveur. Si vos utilisateurs se connectent depuis un domaine enfant
d'une arborescence de domaines AD ou depuis une forêt approuvée, indiquez ces domaines, séparés
par des virgules, dans ``spnego.allowed.realms`` depuis « Système » → « Général » dans
l'écran d'administration ou dans ``app/WEB-INF/conf/system.properties``. Sinon, les utilisateurs
qui pouvaient se connecter jusqu'à la version 15.7 sont refusés avec
``Kerberos realm is not allowed``. Pour plus de détails, consultez
:doc:`../config/sso-spnego`.

Par ailleurs, en 15.8, les valeurs par défaut codées de ``spnego.allow.unsecure.basic`` et
``spnego.allow.localhost`` sont passées de ``true`` à ``false``. Une installation dans laquelle
ces clés sont absentes de ``app/WEB-INF/conf/system.properties`` adopte le comportement plus
strict lors de la mise à niveau. En particulier, avec ``spnego.allow.unsecure.basic=false``, la
bibliothèque SPNEGO ne propose l'authentification Basic que pour les requêtes dont
``HttpServletRequest#isSecure()`` renvoie ``true`` : derrière un proxy inverse qui termine TLS et
transmet la requête en HTTP, les clients qui basculaient jusqu'ici vers l'authentification Basic
ne peuvent plus se connecter. Dans ce cas, définissez ``tomcat.secure=true`` dans
``tomcat_config.properties`` ; pour plus de détails, consultez :doc:`../config/sso-spnego`.

.. warning::

   Une valeur par défaut codée ne s'applique que tant que la clé est absente, et
   « Système » → « Général » de l'écran d'administration écrit toutes les clés ``spnego.*`` à
   chaque enregistrement. Une installation sur laquelle « Mettre à jour » a été cliqué au moins
   une fois depuis cet écran en 15.7 conserve donc ``spnego.allow.unsecure.basic=true`` et
   ``spnego.allow.localhost=true``, et la mise à niveau vers la 15.10 ne la durcit pas : elle
   conserve silencieusement le comportement permissif, et la 15.10 se contente de consigner un
   avertissement dans ``fess.log`` lors de l'initialisation de SPNEGO. Ouvrez
   « Système » → « Général » (ou modifiez ``system.properties``) et désactivez délibérément les
   deux options. ``spnego.allow.localhost=true`` est la plus dangereuse des deux : la bibliothèque
   SPNEGO authentifie alors les requêtes provenant du même hôte en tant qu'utilisateur du système
   d'exploitation du serveur, sans aucune vérification Kerberos, ce qui n'est pas sûr derrière un
   proxy inverse situé sur le même hôte.

.. _upgrade-159-saml:

Si vous utilisiez l'authentification SAML (SSO)
-----------------------------------------------

À partir de la 15.8, |Fess| associe chaque réponse SAML à l'identifiant de l'AuthnRequest qu'il
a émise, si bien que le SSO initié par l'IdP (non sollicité) ne fonctionne plus. Une connexion
démarrée depuis une vignette |Fess| dans un portail IdP, tel que le tableau de bord Okta ou le
portail « Mes applications » de Microsoft Entra ID, n'a aucune AuthnRequest correspondante et est
rejetée. Cela fonctionnait jusqu'à la 15.7 parce que |Fess| renvoyait à l'IdP la réponse qu'il ne
pouvait pas associer et que l'IdP retournait immédiatement une assertion sollicitée. Si vous
placez une vignette côté IdP, faites-la pointer vers le point d'accès ``/sso/`` de |Fess| afin que
la connexion soit initiée par le SP.

Par ailleurs, l'IdP renvoie l'assertion via un POST intersites : ``tomcat.sameSiteCookies`` doit
donc être défini sur ``none`` dans ``tomcat_config.properties``. Avec la valeur par défaut livrée
``lax``, le cookie de session n'est pas envoyé sur cette requête et la connexion SAML ne peut pas
aboutir. Ce fichier se trouve dans ``lib/classes/`` pour le paquet ZIP et dans ``/etc/fess/`` pour
les paquets DEB/RPM, et |Fess| doit être redémarré après la modification. Les navigateurs
n'acceptent ``none`` que sur un cookie portant également l'attribut ``Secure`` : |Fess| doit donc
être servi en HTTPS. Jusqu'à la 15.7, la même erreur de configuration ne provoquait pas d'échec
net mais une boucle de redirections sans fin vers l'IdP ; vérifiez donc le paramètre même sur un
site qui semblait fonctionner. En 15.10, la connexion échoue une seule fois au lieu de boucler.
Pour plus de détails, consultez :doc:`../config/sso-saml`.

Si vous utilisiez Microsoft Entra ID (Azure AD)
-----------------------------------------------

À partir de la 15.8, le mode de réponse demandé au point de terminaison d'autorisation vaut
``query`` par défaut au lieu de ``form_post``. Jusqu'à la 15.7, le callback était renvoyé par un
POST intersite, et la valeur par défaut de |Fess| ``tomcat.sameSiteCookies = lax`` n'envoie pas
le cookie de session avec une telle requête ; ``tomcat.sameSiteCookies = none`` était donc
nécessaire. Si vous aviez défini ``none`` uniquement pour cette raison, vous pouvez revenir à la
valeur par défaut. Pour conserver le comportement précédent, définissez
``entraid.response.mode=form_post`` et laissez ``tomcat.sameSiteCookies = none`` en place. Les
navigateurs n'acceptent ``none`` que sur un cookie portant également l'attribut ``Secure`` : cette
voie impose donc elle aussi de servir |Fess| en HTTPS.

À partir de la 15.8, |Fess| résout également l'appartenance aux groupes et rôles de l'utilisateur
en arrière-plan une fois la connexion terminée, au lieu de bloquer la connexion en attendant
Microsoft Graph. Tant que la résolution n'est pas terminée — ou si elle n'aboutit pas
entièrement —, l'utilisateur ne dispose que de sa propre autorisation au niveau utilisateur et de
ce qu'apportent ``entraid.default.groups`` et ``entraid.default.roles``. Si aucun des deux n'est
défini — la valeur livrée par défaut —, une recherche effectuée pendant cette fenêtre ne renvoie
aucun document, car une configuration d'exploration créée avec les valeurs livrées par défaut
accorde ``{role}guest``, rôle que ne possède pas un utilisateur connecté. Pendant que la
résolution est en cours, l'écran de recherche l'indique, et il affiche un autre message si elle
n'a pas entièrement abouti : la résolution n'est considérée comme réussie que si la requête des
appartenances directes et le parcours des groupes imbriqués ont tous deux abouti. La résolution
est relancée à chaque renouvellement du jeton d'accès, et une réussite ultérieure fait disparaître
le message : un échec n'est donc pas définitif pour une session qui dure plus longtemps que le
jeton. Pour réessayer immédiatement, déconnectez-vous puis reconnectez-vous. Pour plus de détails,
consultez :doc:`../config/sso-entraid`.

Conséquence de cette résolution en arrière-plan : tant qu'elle n'a pas abouti, les rôles résolus
de l'utilisateur ne sont pas encore connus. Un administrateur est donc redirigé vers l'écran de
recherche au lieu du tableau de bord de l'administration, et l'ouverture d'une page de l'écran
d'administration pendant cette fenêtre le ramène à l'écran de recherche. La fenêtre dure jusqu'à
environ une seconde de délai de planification, plus les appels à Microsoft Graph eux-mêmes — un
pour les appartenances directes, puis un de plus pour chacun de ces groupes afin de parcourir les
groupes imbriqués, émis les uns après les autres avec un cache froid — : elle croît donc avec le
nombre de groupes auxquels appartient l'utilisateur. Dans cette fenêtre, l'accès n'est jamais
accordé, seulement refusé, et aucun paramétrage n'est nécessaire pour la franchir : l'autorisation
est réévaluée à chaque requête de la même session, si bien qu'une fois la résolution terminée les
écrans d'administration s'ouvrent normalement, sans avoir à se reconnecter.

.. warning::

   Ne raccourcissez pas cette fenêtre en plaçant le rôle d'administrateur |Fess| dans
   ``entraid.default.roles``. Cette propriété est une valeur globale unique que |Fess| applique à
   tous les utilisateurs Entra ID lors de la connexion et réapplique à chaque résolution
   ultérieure : elle donnerait à tous les utilisateurs du locataire des droits d'administrateur
   |Fess| permanents.

Si Vous Utilisez LDAP / Active Directory
-----------------------------------------

À partir de 15.8, le nom de permission d'un groupe ou d'un rôle correspond à la valeur du RDN de
l'entrée et non plus à une portion du texte du DN. Un groupe dont le CN contient un caractère
échappé dans le DN -- la virgule est le cas courant -- obtient donc un nom de permission différent
de celui de 15.7.

.. list-table::
   :header-rows: 1

   * - DN de l'entrée du groupe
     - Nom de permission jusqu'à 15.7
     - Nom de permission en 15.10
   * - ``CN=Sales\, EMEA,CN=Users,...``
     - ``2Sales``
     - ``2Sales, EMEA``
   * - ``CN=Sales\, APAC,CN=Users,...``
     - ``2Sales``
     - ``2Sales, APAC``

Jusqu'à 15.7, plusieurs groupes identiques jusqu'à la virgule se réduisaient à un même nom de
permission : les membres de ``Sales, EMEA`` et de ``Sales, APAC`` pouvaient donc lire les documents
de l'autre groupe ainsi que ceux du groupe ``Sales``. En 15.10, chacun obtient son propre nom de
permission et cet accès inter-groupes ne se produit plus.

En contrepartie, **les documents indexés sous l'ancien nom de permission ne sont plus visibles par
les membres de ce groupe**. Si le paramètre de permission d'une configuration d'exploration contient
un ancien nom de permission, remplacez-le par le nouveau puis relancez l'exploration (ou la
réindexation). Si vous n'utilisez aucun groupe dont le CN contient une virgule ou un autre caractère
échappé, aucun nom de permission ne change.

Modification de ``ldap.role.search.user.enabled``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Jusqu'à 15.7, la permission dérivée du nom d'utilisateur (``role.search.user.prefix`` suivi du nom
d'utilisateur) était accordée même avec ``ldap.role.search.user.enabled=false``. À partir de 15.8,
le paramètre prend effet et la permission n'est plus accordée lorsqu'il est désactivé.

Dans une installation où il vaut ``false``, les utilisateurs perdent après la mise à niveau la
permission portant leur propre nom : les documents attribués à un utilisateur donné ne remontent
plus pour cet utilisateur. Pour conserver le comportement précédent, rétablissez la valeur par
défaut ``true``.

Si vous aviez modifié les clés de configuration /api/v2
-------------------------------------------------------

En 15.8.0, quatre clés de configuration ont perdu leur préfixe ``api.v2.``. Leurs valeurs, leurs
valeurs par défaut et leur comportement sont inchangés, mais **aucun alias rétrocompatible n'est
conservé** : un paramètre laissé sous son ancien nom est ignoré sans avertissement et la valeur
par défaut fournie s'applique.

.. list-table::
   :header-rows: 1

   * - Jusqu'à 15.7
     - 15.8.0 et versions ultérieures
     - Valeur par défaut
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

Si vous avez défini l'une de ces clés dans ``fess_config.properties`` ou via l'argument JVM
``-Dfess.config.<clé>``, renommez-la. Seuls les paramètres explicites sont concernés ; une
installation qui ne les a jamais modifiés n'a rien à faire.

La première clé détermine la fréquence d'envoi d'une trame keep-alive pendant que
``POST /api/v2/chat/stream`` attend le modèle : c'est donc dans le mode de recherche IA qu'un
paramètre perdu se remarque. La dernière clé a également été renommée par souci d'exactitude :
elle borne la valeur ``rt`` que peut porter un journal de clic, qui est un horodatage et non un
temps de réponse.


.. _upgrade-plugin-versions:

Mise à jour de la version des plugins
-------------------------------------

Les plugins installés dans ``app/WEB-INF/plugin/`` doivent être remplacés par ceux correspondant
à la version de |Fess|. ``bin/fess-setup upgrade plugins`` le fait pour tous les plugins
installés : il installe la version construite pour ce |Fess| et supprime l'ancienne. Redémarrez
ensuite |Fess|. ``bin/fess-setup check`` indique alors l'état d'OpenSearch, de ses plugins et des
plugins |Fess| installés, et se termine avec le code 1 en cas de problème. Il ne lit pas
``bin/fess.in.sh``, ``/etc/sysconfig/fess`` ni ``/etc/default/fess`` : lorsque OpenSearch ne se
trouve pas à ``http://localhost:9200``, passez ``--url`` ou définissez ``SEARCH_ENGINE_HTTP_URL``
dans le shell qui l'exécute ; sinon il signale le moteur comme injoignable.

::

    $ bin/fess-setup upgrade plugins
    $ bin/fess-setup check

``upgrade plugins`` ne traite que les plugins déjà installés. Installez avec
``bin/fess-setup install plugin``, comme indiqué dans les sections précédentes, les plugins qui
remplacent des éléments retirés de la distribution en 15.9, comme ``fess-script-groovy``.

Si vous spécifiez ``FESS_PLUGINS`` pour la version Docker, mettez à jour la partie version, par
exemple ``fess-ds-wikipedia:15.10.0``.

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

    $ sudo rpm -Uvh --oldpackage --nodeps fess-<old-version>.rpm

Ou ::

    $ sudo dpkg -i fess-<old-version>.deb

.. note::

   ``--nodeps`` est nécessaire pour le RPM. Le paquet 15.8.0 exige les utilisateurs et groupes
   ``fess`` et ``opensearch`` ; sans cette option, ``rpm`` refuse le retour à la version antérieure
   avec ``Failed dependencies: group(fess) is needed by fess-15.8.0``.

.. warning::

   Le paquet DEB 15.8.0 n'enregistre pas ``/etc/fess/*`` en tant que conffiles ; ``dpkg -i`` écrase
   donc les fichiers que vous avez modifiés, tels que ``/etc/fess/fess_config.properties``, sans en
   conserver de copie. Restaurez-les depuis la sauvegarde effectuée à l'étape 1.

Étape 3 : Restauration des données
------------------------------------

Restauration depuis le snapshot. OpenSearch doit être en cours d'exécution et |Fess| arrêté :

1. Démarrez OpenSearch ::

       $ sudo systemctl start opensearch.service

2. Un snapshot ne peut pas être restauré par-dessus un index existant ; supprimez donc d'abord tous
   les index Fess, y compris ceux créés après la mise à niveau (par exemple par une
   réindexation), ainsi que l'index ``configsync`` que crée le plugin OpenSearch. Si vous ne
   supprimez que les index présents dans le snapshot, un index créé par la réindexation subsiste,
   ``fess.search`` pointe sur deux index et la 15.8.0 ne démarre pas ::

       $ curl "http://localhost:9200/_cat/indices/fess*,configsync?h=index"
       $ curl -X DELETE "http://localhost:9200/<index name>"

   Exécutez la seconde commande pour chaque index que la première liste.

3. Restaurez le snapshot ::

       $ curl -X POST "http://localhost:9200/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true"

.. note::

   Le répertoire des dictionnaires doit exister comme auparavant (``configsync.config_path``, avec
   les fichiers de dictionnaire). Sur une machine qui l'a perdu, la restauration se termine mais les
   index qui utilisent les dictionnaires restent en rouge.

Ou restauration du répertoire depuis la sauvegarde (utilisez le nom de l'archive que vous avez
créée à l'étape 1) ::

    $ sudo systemctl stop opensearch
    $ sudo rm -rf /var/lib/opensearch/data/*
    $ sudo tar xzf /backup/opensearch-data-<YYYYMMDD>.tar.gz -C /
    $ sudo systemctl start opensearch

Pour la version Docker, revenez au fichier Compose de l'ancienne version, puis restaurez le
contenu du volume ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down
    $ PROJECT=$(basename "$(pwd)")
    $ docker run --rm -v ${PROJECT}_search01_data:/data -v $(pwd):/backup ubuntu \
        sh -c "rm -rf /data/* && tar xzf /backup/search01-data-backup.tar.gz -C /"
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   Les données de configuration téléchargées depuis l'écran d'administration peuvent être
   restaurées en les réimportant via la fonction de téléversement de la page « Informations
   système » → « Sauvegarde », une fois |Fess| démarré. Seuls les fichiers suivants peuvent être
   téléversés, un fichier par opération : ``*.bulk``, les ``*.properties`` commençant par
   ``system``, les ``*.xml`` commençant par ``gsa``, les ``*.json`` commençant par ``fess`` et les
   ``*.json`` commençant par ``doc``. Les fichiers ``*.ndjson`` tels que les journaux de recherche
   ne sont pas acceptés et provoquent une erreur.

.. warning::

   Le téléversement de ``fess.json`` et de ``doc.json`` écrase directement les fichiers de
   définition d'index fournis avec |Fess|. Si vous téléversez après la mise à niveau un
   ``fess.json`` ou un ``doc.json`` d'une ancienne version, les réglages et le mapping d'index de
   la nouvelle version seront perdus. Ne les téléversez pas en dehors d'un retour arrière.

.. note::

   Le fichier ``system.properties`` téléversé n'est chargé qu'en mémoire et n'est jamais écrit sur
   disque : son contenu est donc perdu au redémarrage de |Fess|. Pour une restauration fiable,
   placez directement le fichier de sauvegarde à l'emplacement approprié (``app/WEB-INF/conf/``
   pour la version ZIP, ``/etc/fess/`` pour la version RPM/DEB) avant de démarrer |Fess|.

.. note::

   L'importation s'exécute de façon asynchrone ; l'écran indique seulement qu'elle a démarré.
   Vérifiez ``fess.log`` pour savoir si elle a réellement réussi.

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

R : La version d'OpenSearch compatible est déterminée pour chaque version de |Fess|.
|Fess| 15.10 est compatible avec OpenSearch 3.9.0.
Les plugins OpenSearch pour |Fess| tels que ``opensearch-analysis-fess`` doivent correspondre exactement à la version d'OpenSearch ;
si vous mettez à niveau OpenSearch, mettez également à jour les plugins vers la version correspondante (3.9.0).

Notez par ailleurs que |Fess| 15.10 rend le plugin k-NN obligatoire et envoie toujours
``knn.derived_source.enabled`` dans les réglages de l'index. Avec un OpenSearch ancien, la
création d'un nouvel index échoue : la mise à niveau d'OpenSearch est donc requise dans la
pratique. Voir l'étape 4 pour plus de détails.

Q : Est-il nécessaire de recréer l'index ?
-------------------------------------------

R : Pour une mise à niveau mineure de |Fess| (15.x → 15.10) sans utilisation de la recherche par
vecteurs de chunks, ce n'est en général pas nécessaire. L'index existant peut continuer d'être
utilisé tel quel, et comme ``content_chunker.enabled`` (entre autres) est désactivé par défaut,
le comportement ne change pas.

Une recréation et une réindexation sont nécessaires dans les cas suivants :

- **Activation nouvelle de la recherche par vecteurs de chunks (recherche sémantique)** : l'index
  existant n'adopte pas le nouveau mapping, une réindexation est donc obligatoire. Voir
  :ref:`semantic-search-migration` (:doc:`../config/search-semantic`) pour plus de détails.
- **Mise à niveau depuis la 14.x** : OpenSearch passant de la série 2.x à la série 3.x (mise à
  niveau majeure), la recréation de l'index est recommandée.
- **Recherche par propriétaire ou normalisation des kana avec un index de documents créé avec la 15.8
  ou antérieure** : une réindexation est nécessaire. Voir :ref:`upgrade-reindex-new-fields`.

.. warning::

   Les opérations créant un nouvel index (y compris la réindexation) échouent sur un OpenSearch
   dépourvu du plugin k-NN. Consultez les remarques de l'étape 4.

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
- :doc:`../config/search-semantic` - Configuration et étapes de migration de la recherche par
  vecteurs de chunks (recherche sémantique)
- Vérifiez les nouvelles fonctionnalités dans les notes de version
