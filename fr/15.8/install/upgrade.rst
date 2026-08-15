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

.. important::

   |Fess| 14.x est compatible avec la série OpenSearch 2.x, tandis que |Fess| 15.8 est compatible
   avec OpenSearch 3.8.0. Les plugins OpenSearch pour |Fess| doivent correspondre exactement à la
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
- :doc:`prerequisites` - Configuration requise pour |Fess| 15.8 (versions de Java et d'OpenSearch)

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
     miniatures, etc. (25 index)
   - ``fess_user.bulk`` - Utilisateurs, rôles, groupes
   - ``system.properties`` - Paramètres système, y compris les paramètres généraux
   - ``fess.json`` - Paramètres d'index (nombre de shards, ``index.knn``, etc.)
   - ``doc.json`` - Mappage des documents (définitions des champs)

   .. note::

      ``fess_config.bulk`` inclut ``fess_basic_config.bulk``. Pour la sauvegarde de configuration
      avant la mise à niveau, ``fess_basic_config.bulk``, ``fess_user.bulk`` et
      ``system.properties`` suffisent.

   .. note::

      Les données de journaux tels que les journaux de recherche et les journaux de clics (``search_log.ndjson``, ``click_log.ndjson``,
      ``favorite_log.ndjson``, ``user_info.ndjson``) peuvent également être téléchargées depuis la même page.
      Elles ne sont pas nécessaires si vous ne sauvegardez que la configuration. Notez que ces
      fichiers ``*.ndjson`` ne peuvent pas être restaurés en les téléversant depuis la page de
      sauvegarde (voir « Procédure de retour arrière »).

2. **Sauvegarde des fichiers de configuration**

   Version TAR.GZ/ZIP ::

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
      Pour la version TAR.GZ/ZIP, les réglages équivalents se trouvent dans ``bin/fess.in.sh``.

3. **Fichiers de configuration personnalisés**

   Si vous avez des fichiers de configuration personnalisés, sauvegardez-les également ::

       $ cp /path/to/fess/app/WEB-INF/classes/log4j2.xml /backup/

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

La version TAR.GZ/ZIP ne fournit pas de script d'arrêt. Si vous aviez démarré ``bin/fess`` avec
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

Étape 3 : Installation de la nouvelle version
================================================

Les procédures diffèrent selon la méthode d'installation.

Version TAR.GZ/ZIP
------------------

1. Téléchargez et décompressez la nouvelle version ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.8.0/fess-15.8.0.zip
       $ unzip fess-15.8.0.zip

   .. note::

      La version archive de |Fess| n'est distribuée qu'au format ZIP (``fess-15.8.0.tar.gz``
      n'est pas fourni).

2. Copiez la configuration de l'ancienne version ::

       $ cp /path/to/old-fess/app/WEB-INF/conf/system.properties /path/to/fess-15.8.0/app/WEB-INF/conf/
       $ cp /path/to/old-fess/app/WEB-INF/classes/fess_config.properties /path/to/fess-15.8.0/app/WEB-INF/classes/
       $ cp /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.8.0/bin/

3. Si vous avez des personnalisations, copiez également ce qui suit ::

       # Configuration des journaux
       $ cp /path/to/old-fess/app/WEB-INF/classes/log4j2.xml /path/to/fess-15.8.0/app/WEB-INF/classes/
       # Plugins installés
       $ cp -r /path/to/old-fess/app/WEB-INF/plugin/. /path/to/fess-15.8.0/app/WEB-INF/plugin/
       # Thème
       $ cp -r /path/to/old-fess/app/themes/. /path/to/fess-15.8.0/app/themes/

   .. warning::

      Ne copiez pas tel quel les JSP (``app/WEB-INF/view/``) modifiés depuis l'écran
      d'administration « Design ». Si la structure des JSP de la nouvelle version a changé,
      l'affichage risque d'être incorrect. Réappliquez vos modifications sur les JSP de la
      nouvelle version.

4. Si vous utilisez OpenSearch intégré (configuration démarrant ``bin/fess`` sans définir
   ``SEARCH_ENGINE_HTTP_URL``), copiez également les données d'index ::

       $ cp -r /path/to/old-fess/es/data/. /path/to/fess-15.8.0/es/data/

5. Vérifiez les différences de configuration et ajustez si nécessaire

Version RPM/DEB
---------------

Installez le package de la nouvelle version ::

    # RPM
    $ sudo rpm -Uvh fess-15.8.0.rpm

    # DEB
    $ sudo dpkg -i fess-15.8.0.deb

.. note::

   Dans la version RPM, les fichiers de configuration ``/etc/fess/*`` sont enregistrés en tant que
   ``%config(noreplace)`` et sont donc conservés lors de la mise à niveau (les nouveaux fichiers
   par défaut sont placés à côté avec l'extension ``.rpmnew``). Si de nouvelles options de
   configuration ont été ajoutées, un ajustement manuel peut être nécessaire.

.. warning::

   Dans la version DEB, ``/etc/fess/*`` n'est pas enregistré en tant que conffile (les seuls
   conffiles sont ``/etc/default/fess``, ``/etc/init.d/fess`` et
   ``/usr/lib/systemd/system/fess.service``). Par conséquent, l'exécution de ``dpkg -i`` écrase
   des fichiers tels que ``/etc/fess/fess_config.properties`` avec ceux de la nouvelle version.
   Réappliquez après la mise à niveau la configuration sauvegardée à l'étape 1.
   Notez que ``/etc/fess/system.properties`` n'est pas écrasé, car il s'agit d'un fichier généré
   à l'exécution qui n'est pas inclus dans le paquet.

Version Docker
--------------

1. Obtenez les fichiers Compose de la nouvelle version ::

       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose.yaml
       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose-opensearch3.yaml

2. Récupérez la nouvelle image ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

.. _upgrade-opensearch:

Étape 4 : Mise à niveau d'OpenSearch
====================================

|Fess| 15.8 est compatible avec OpenSearch 3.8.0. Si l'OpenSearch auquel vous vous connectez est
antérieur à cette version, effectuez la mise à niveau en suivant la procédure ci-dessous.

.. note::

   Cette procédure s'applique aux cas où OpenSearch est géré manuellement avec les versions TAR.GZ/ZIP et RPM/DEB.
   Pour la version Docker, l'obtention de la nouvelle image à l'étape 3 met également à jour OpenSearch et ses plugins
   simultanément ; cette étape n'est donc pas nécessaire.

.. important::

   Que la recherche par vecteurs de chunks (recherche sémantique) soit utilisée ou non, |Fess|
   15.8 inclut toujours ``index.knn`` dans les réglages de l'index de recherche, ainsi que le
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

1. Installez la nouvelle version d'OpenSearch

2. Réinstallez les plugins ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.8.0

   .. note::

      La version de ces plugins doit correspondre à la version d'OpenSearch utilisée.
      |Fess| 15.8 est compatible avec OpenSearch 3.8.0. Si les versions ne correspondent pas,
      l'installation du plugin échouera.

3. Démarrez OpenSearch ::

       $ sudo systemctl start opensearch.service

Étape 5 : Démarrage de la nouvelle version
============================================

Version TAR.GZ/ZIP ::

    $ cd /path/to/fess-15.8.0
    $ ./bin/fess -d -p /path/to/fess-15.8.0/fess.pid

.. note::

   L'option ``-p`` crée un fichier PID, qui permet d'arrêter |Fess| lors du prochain arrêt avec
   ``kill $(cat /path/to/fess-15.8.0/fess.pid)``.

Version RPM/DEB ::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Version Docker ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Étape 6 : Vérification du fonctionnement
==========================================

1. **Vérification des journaux**

   Vérifiez qu'il n'y a pas d'erreurs.

   Version TAR.GZ/ZIP ::

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

1. Vérifiez la planification d'exploration existante
2. Exécutez « Default Crawler » depuis « Système » → « Planificateur »
3. Attendez la fin de l'exploration
4. Vérifiez les résultats de recherche

.. warning::

   La réindexation recrée l'index avec le nouveau mapping ; elle échoue donc sur un OpenSearch
   dépourvu du plugin k-NN. Consultez les remarques de l'étape 4.

Migrations spécifiques à la 15.8
================================

Si vous effectuez une mise à niveau depuis la version 15.7 ou antérieure vers la 15.8, les
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

À partir de la 15.8, la fonctionnalité du mode de recherche IA (chat RAG) a été séparée en
plugins tels que ``fess-llm-ollama``, ``fess-llm-openai`` et ``fess-llm-gemini``. Installez le
plugin correspondant au fournisseur que vous utilisez depuis « Système » → « Plugins » dans
l'écran d'administration.

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
   ``spnego.allow.localhost=true``, et la mise à niveau vers la 15.8 ne la durcit pas : elle
   conserve silencieusement le comportement permissif, et la 15.8 se contente de consigner un
   avertissement dans ``fess.log`` lors de l'initialisation de SPNEGO. Ouvrez
   « Système » → « Général » (ou modifiez ``system.properties``) et désactivez délibérément les
   deux options. ``spnego.allow.localhost=true`` est la plus dangereuse des deux : la bibliothèque
   SPNEGO authentifie alors les requêtes provenant du même hôte en tant qu'utilisateur du système
   d'exploitation du serveur, sans aucune vérification Kerberos, ce qui n'est pas sûr derrière un
   proxy inverse situé sur le même hôte.

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
site qui semblait fonctionner. En 15.8, la connexion échoue une seule fois au lieu de boucler.
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

Mise à jour de la version des plugins
-------------------------------------

Les plugins installés dans ``app/WEB-INF/plugin/`` doivent être remplacés par ceux correspondant
à la version de |Fess|. Si vous spécifiez ``FESS_PLUGINS`` pour la version Docker, mettez à jour
la partie version, par exemple ``fess-ds-wikipedia:15.8.0``.

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
   pour la version TAR.GZ/ZIP, ``/etc/fess/`` pour la version RPM/DEB) avant de démarrer |Fess|.

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
|Fess| 15.8 est compatible avec OpenSearch 3.8.0.
Les plugins OpenSearch pour |Fess| tels que ``opensearch-analysis-fess`` doivent correspondre exactement à la version d'OpenSearch ;
si vous mettez à niveau OpenSearch, mettez également à jour les plugins vers la version correspondante (3.8.0).

Notez par ailleurs que |Fess| 15.8 rend le plugin k-NN obligatoire et envoie toujours
``knn.derived_source.enabled`` dans les réglages de l'index. Avec un OpenSearch ancien, la
création d'un nouvel index échoue : la mise à niveau d'OpenSearch est donc requise dans la
pratique. Voir l'étape 4 pour plus de détails.

Q : Est-il nécessaire de recréer l'index ?
-------------------------------------------

R : Pour une mise à niveau mineure de |Fess| (15.x → 15.8) sans utilisation de la recherche par
vecteurs de chunks, ce n'est en général pas nécessaire. L'index existant peut continuer d'être
utilisé tel quel, et comme ``content_chunker.enabled`` (entre autres) est désactivé par défaut,
le comportement ne change pas.

Une recréation et une réindexation sont nécessaires dans les cas suivants :

- **Activation nouvelle de la recherche par vecteurs de chunks (recherche sémantique)** : l'index
  existant n'adopte pas le nouveau mapping, une réindexation est donc obligatoire. Voir
  :ref:`semantic-search-migration` (:doc:`../config/search-semantic`) pour plus de détails.
- **Mise à niveau depuis la 14.x** : OpenSearch passant de la série 2.x à la série 3.x (mise à
  niveau majeure), la recréation de l'index est recommandée.

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
