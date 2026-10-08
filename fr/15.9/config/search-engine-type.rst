===========================
Type de moteur de recherche
===========================

Présentation
============

|Fess| stocke ses données dans OpenSearch. Le paramètre ``search_engine.type`` indique à |Fess| à quel type d'OpenSearch il est connecté. Cela détermine les définitions d'index que |Fess| crée et les fonctionnalités qu'il propose.

Avec la valeur par défaut, ``default``, |Fess| attend un OpenSearch sur lequel les quatre plugins CodeLibs sont installés (``opensearch-analysis-fess``, ``opensearch-analysis-extension``, ``opensearch-minhash`` et ``opensearch-configsync`` ; voir :doc:`../install/install`). Pour vous connecter à un OpenSearch standard sans ces plugins, par exemple un service géré sur lequel vous ne pouvez pas installer vos propres plugins, définissez la valeur ``vanilla``.

Types
=====

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Valeur
     - Description
   * - ``default``
     - OpenSearch avec les plugins CodeLibs. C'est la valeur par défaut.
   * - ``vanilla``
     - Un OpenSearch standard sans les plugins CodeLibs. Nouveauté de la version 15.9. Les définitions d'index sont lues dans ``fess_indices/_vanilla/``. |Fess| 15.8 et les versions antérieures ne connaissent pas cette valeur ; utilisez ``cloud`` avec elles.
   * - ``aws``
     - Identique à ``vanilla``, prévu pour Amazon OpenSearch Service. Voir :ref:`search-engine-type-aws`.
   * - ``cloud``
     - Un alias obsolète de ``vanilla``. |Fess| consigne un avertissement au démarrage. Remplacez-le par ``vanilla``.
   * - Toute autre valeur
     - Traitée comme ``default``, sauf que les fichiers de définition situés sous ``fess_indices/_<type>/`` ont priorité sur les fichiers du même nom situés sous ``fess_indices/``.

|Fess| ne détecte pas automatiquement les plugins ; c'est à vous de définir le type. Définissez-le avant le premier démarrage. Les définitions d'index sont appliquées lors de la création d'un index ; modifier la valeur par la suite ne change donc pas les index déjà existants.

Fonctionnalités indisponibles sans les plugins
==============================================

Avec ``vanilla`` et ``aws`` (y compris l'ancien ``cloud``), les fonctionnalités suivantes ne sont pas disponibles. Les éléments de l'interface d'administration qui en dépendent sont masqués.

* **Gestion des dictionnaires** : [Système > Dictionnaire] est masqué. Les pages de dictionnaire et l'API d'administration des dictionnaires (``/api/admin/dict/``) ne peuvent pas être utilisées. « Réinitialiser les dictionnaires » et « Recharger l'index des documents » de la page Maintenance sont également masqués. Les analyseurs utilisent les règles contenues dans la définition de l'index, et non des fichiers de dictionnaire.
* **Regroupement des résultats** : « Réduire les résultats en double » dans Général est masqué et le regroupement est toujours désactivé.
* **Détection des doublons** : la signature de contenu qui sert à trouver les documents au contenu identique n'est pas calculée. L'onglet « Doublons » du Rapport de documents est masqué (le rapport des documents inactifs reste disponible), et le paramètre de recherche ``sdh`` (documents similaires) est ignoré.
* **Analyseurs** : le japonais, le coréen et le chinois simplifié sont segmentés par les analyseurs Kuromoji, Nori et SmartCN d'OpenSearch au lieu des tokenizers CodeLibs ; les tokens diffèrent donc de ceux de ``default``. Le vietnamien (champs ``*_vi``) et le chinois traditionnel (champs ``*_zh-tw``) utilisent un analyseur vide qui n'enregistre aucun terme. Les documents dans ces langues sont tout de même indexés dans les champs ``content`` et ``title``, indépendants de la langue.

Plugins OpenSearch requis
=========================

Les définitions d'index de ``vanilla`` et ``aws`` utilisent des analyseurs et un type de champ vectoriel fournis par des plugins OpenSearch officiels. L'OpenSearch auquel vous vous connectez doit disposer de ces plugins :

* ``analysis-kuromoji``
* ``analysis-nori``
* ``analysis-smartcn``
* ``opensearch-knn`` (k-NN)

Les plugins CodeLibs ne sont pas nécessaires. Sur un OpenSearch que vous exploitez vous-même, installez un plugin avec ``opensearch-plugin install``, par exemple ``bin/opensearch-plugin install analysis-nori``. Pour Amazon OpenSearch Service, voir :ref:`search-engine-type-aws`.

Lorsque le type est ``vanilla`` ou ``aws``, |Fess| liste les plugins installés (``GET /_cat/plugins``) au démarrage. Si l'un des plugins ci-dessus est absent, il consigne un avertissement qui nomme les plugins manquants et poursuit le démarrage. Si la requête échoue, par exemple parce que le service ne l'autorise pas, la vérification est ignorée.

Définir le type
===============

Docker
------

Définissez la variable d'environnement ``SEARCH_ENGINE_TYPE`` sur le service ``fess01`` dans ``compose.yaml`` ::

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "SEARCH_ENGINE_TYPE=vanilla"

``vanilla`` peut être utilisé avec les images de |Fess| 15.9 et ultérieures. Avec une image plus ancienne, définissez ``SEARCH_ENGINE_TYPE=cloud``. Pour les autres paramètres Docker, voir :doc:`../install/install-docker`.

Installations hors Docker
-------------------------

``bin/fess.in.sh`` ne lit pas ``SEARCH_ENGINE_TYPE``. Utilisez plutôt l'une des méthodes suivantes.

* Écrivez ``search_engine.type`` dans ``fess_config.properties`` (``app/WEB-INF/classes/fess_config.properties`` dans l'édition ZIP, ``/etc/fess/fess_config.properties`` dans les éditions RPM et DEB).
* Ajoutez une option JVM à ``FESS_JAVA_OPTS`` dans ``bin/fess.in.sh`` de l'édition ZIP (``bin\fess.in.bat`` sous Windows).

::

    # fess_config.properties
    search_engine.type=vanilla

    # bin/fess.in.sh
    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.config.search_engine.type=vanilla"

    REM bin\fess.in.bat
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.config.search_engine.type=vanilla

Redémarrez |Fess| après la modification. Le crawler et les autres processus de tâches reçoivent le paramètre de |Fess| ; il n'est donc pas nécessaire de le définir séparément pour eux.

Paramètres de connexion
=======================

La connexion à OpenSearch se configure de la même manière que pour tout autre type.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Paramètre
     - Description
   * - ``search_engine.http.url``
     - Le point de terminaison HTTP d'OpenSearch. Si la variable d'environnement ``SEARCH_ENGINE_HTTP_URL`` est définie, elle est prioritaire.
   * - ``search_engine.username`` / ``search_engine.password``
     - Le nom d'utilisateur et le mot de passe pour l'authentification HTTP Basic. Ils ne sont utilisés que si les deux sont définis. Dans Docker, utilisez les variables d'environnement ``SEARCH_ENGINE_USERNAME`` et ``SEARCH_ENGINE_PASSWORD``.
   * - ``search_engine.http.ssl.certificate_authorities``
     - Le chemin d'un fichier de certificat d'autorité de certification (X.509) servant à vérifier le certificat du serveur d'un point de terminaison HTTPS. Il est inutile si le certificat est émis par une autorité que Java approuve déjà.

Un élément de ``fess_config.properties`` peut aussi être indiqué sous la forme ``-Dfess.config.<nom de l'élément>`` dans ``FESS_JAVA_OPTS`` (voir :doc:`../install/install-docker`).

.. _search-engine-type-aws:

Amazon OpenSearch Service
=========================

Pour utiliser un domaine Amazon OpenSearch Service, définissez ``search_engine.type`` sur ``aws`` (``vanilla`` se comporte de la même façon).

Prérequis
---------

* Le domaine exécute OpenSearch 3.x. |Fess| vérifie le moteur au démarrage et ne démarre avec aucun autre moteur qu'OpenSearch 3.
* Les plugins listés dans « Plugins OpenSearch requis » sont disponibles sur le domaine. Sur Amazon OpenSearch Service, Nori est un package facultatif : associez-le au domaine avant de démarrer |Fess|.
* Le point de terminaison utilise HTTPS.
* Le contrôle d'accès précis (fine-grained access control) est activé et comporte un utilisateur interne avec lequel |Fess| se connecte (authentification HTTP Basic). La signature des requêtes avec des identifiants AWS IAM (SigV4) n'est pas encore prise en charge ; un domaine qui n'accepte que des requêtes signées par IAM ne peut donc pas être utilisé.

Exemple de configuration
------------------------

::

    search_engine.type=aws
    search_engine.http.url=https://<domain-endpoint>:443
    search_engine.username=<internal-user-name>
    search_engine.password=<password>

Vérifications au démarrage
--------------------------

* La vérification des plugins décrite dans « Plugins OpenSearch requis » s'exécute aussi avec ``aws``. Si vous avez oublié d'associer Nori, un avertissement apparaît dans ``fess.log``.
* Si le domaine rejette une requête avec HTTP 401 ou 403, |Fess| consigne un avertissement. Lorsque cela fait échouer le démarrage, le message d'erreur renvoie au nom d'utilisateur, au mot de passe et à la politique d'accès du domaine.

TTL du cache DNS
----------------

Le point de terminaison d'un service géré peut se résoudre en d'autres adresses IP au fil du temps, et la JVM met en cache le résultat d'une résolution DNS. Une durée de cache courte permet à |Fess| de suivre un tel changement. Définissez ``-Dsun.net.inetaddr.ttl=5`` (secondes) aux deux endroits suivants.

1. Le processus |Fess| : ajoutez-la à ``FESS_JAVA_OPTS``.

   ::

       FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dsun.net.inetaddr.ttl=5"

2. Les processus de tâches : les processus du crawler, des suggestions, des chunks et des miniatures sont lancés par |Fess| comme des JVM distinctes et n'héritent pas de ``FESS_JAVA_OPTS``. Ajoutez la même option à la fin de ``jvm.crawler.options``, ``jvm.suggest.options``, ``jvm.chunk.options`` et ``jvm.thumbnail.options`` dans ``fess_config.properties``. Chacune de ces valeurs contient une option par ligne, et chaque ligne se termine par ``\n\``.

   ::

       jvm.crawler.options=\
       -Djava.awt.headless=true\n\
       ...
       -Dsun.net.inetaddr.ttl=5\n\

   Ajoutez la ligne après les lignes existantes, et faites de même pour les trois autres éléments.

Dans Docker, indiquez ``FESS_JAVA_OPTS`` dans les variables d'environnement du fichier Compose. Pour modifier les éléments ``jvm.*.options``, montez un ``fess_config.properties`` modifié (voir :doc:`../install/install-docker`).
