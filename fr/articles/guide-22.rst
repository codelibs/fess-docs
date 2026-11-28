====================================================
Les journaux de recherche dans OpenSearch Dashboards
====================================================

Introduction
============

Dans Fess 15.9, [Informations système] > [Journal de recherche] de l'interface d'administration affiche le taux de zéro résultat, le taux de clics, la répartition des positions de clic, les temps de réponse, le nombre de recherches par jour de la semaine et par heure, ainsi que le nombre de recherches par rôle et par groupe.
Chaque tableau peut être téléchargé au format CSV.
La démarche consistant à repérer les termes de recherche problématiques puis à les corriger avec des synonymes ou des correspondances de clé est décrite dans :doc:`guide-08`.

En revanche, cet écran ne permet pas les agrégations suivantes :

- Les tendances sur des périodes de plus de 366 jours (la période « Personnalisée » de l'écran est limitée à 366 jours)
- Les termes qui ne donnent aucun résultat, ventilés par rôle ou par étiquette
- Les URL réellement ouvertes pour chaque terme de recherche
- Un tableau de bord réunissant des graphiques selon les axes de votre choix

Les journaux de recherche et de clics sont stockés dans des index OpenSearch ; vous pouvez donc les agréger directement dans OpenSearch Dashboards.
Cet article démarre OpenSearch Dashboards avec les fichiers Compose de docker-fess, importe le tableau de bord fourni avec Fess, examine les champs des journaux, puis construit les quatre agrégations ci-dessus.

Avant de commencer : restreindre l'accès
========================================

Dans docker-fess, OpenSearch Dashboards fonctionne sans le plugin de sécurité, tout comme OpenSearch lui-même.
Toute personne qui peut atteindre le port 5601 peut lire, sans se connecter, tous les champs des journaux de recherche (identifiants d'utilisateur, adresses IP, etc.).
De plus, depuis Dev Tools, elle peut modifier ou supprimer n'importe quel index, y compris les index de Fess contenant les utilisateurs et les paramètres.

Rendez donc le port 5601 (et le 9200) accessible uniquement depuis les postes des administrateurs.
Si vous souhaitez montrer les statistiques des journaux de recherche à des personnes qui ne sont pas administrateurs, ne publiez pas OpenSearch Dashboards : créez plutôt, dans Fess, un rôle nommé ``admin-searchlog-view`` sous [Utilisateur] > [Rôle] et attribuez-le à ces personnes.
Ce rôle permet de consulter [Informations système] > [Journal de recherche], mais pas de supprimer les journaux.

Démarrer OpenSearch Dashboards
==============================

Ajoutez les fichiers de Dashboards dans le répertoire où vous avez placé ``compose.yaml`` et ``compose-opensearch3.yaml`` en suivant :doc:`guide-02`.
``compose-dashboards3.yaml`` construit son image à partir du Dockerfile du répertoire ``dashboards/`` ; trois fichiers sont donc nécessaires.

::

    $ cd fess-docker
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-dashboards3.yaml
    $ mkdir dashboards
    $ curl -L -o dashboards/Dockerfile https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/dashboards/Dockerfile
    $ curl -L -o dashboards/opensearch_dashboards.yml https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/dashboards/opensearch_dashboards.yml

Démarrez en indiquant les trois fichiers Compose.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-dashboards3.yaml up -d

Au premier ``up``, une image est construite à partir de ``opensearch-dashboards:3.9.0`` en supprimant le plugin ``securityDashboards``.
Le conteneur se connecte à ``OPENSEARCH_HOSTS='["http://search01:9200"]'`` sur le réseau ``search_net`` et publie le port 5601.

Ouvrez ``http://localhost:5601`` dans un navigateur ; si la page d'accueil s'affiche, le service est démarré.
Pour l'arrêt ou la vérification de l'état aussi, indiquez les trois fichiers avec ``-f``.
Les objets enregistrés, comme les tableaux de bord, sont stockés dans l'index ``.kibana`` d'OpenSearch ; si vous supprimez les volumes avec ``down -v``, ils disparaissent également.

Importer le tableau de bord fourni
==================================

Fess est livré avec une définition de tableau de bord pour les journaux de recherche, ``fess_log.ndjson``.
Avec Docker, copiez-la depuis le conteneur.
Dans la version ZIP, elle se trouve dans ``extension/kibana/fess_log.ndjson`` du répertoire décompressé.

::

    $ docker cp fess01:/usr/share/fess/extension/kibana/fess_log.ndjson .

Vous pouvez aussi récupérer le même fichier sur GitHub à l'adresse ``https://raw.githubusercontent.com/codelibs/fess/fess-15.9.0/src/main/assemblies/extension/kibana/fess_log.ndjson``.

1. Ouvrez [Dashboards Management] dans le menu de gauche et choisissez [Saved objects]
2. Cliquez sur [Import], sélectionnez ``fess_log.ndjson`` et importez-le
3. Ouvrez le tableau de bord ``fess_log`` depuis [Dashboards] dans le menu de gauche

L'import enregistre le modèle d'index ``fess_log*`` (champ de temps ``requestedAt``), six visualisations et le tableau de bord ``fess_log``.
Comme le modèle d'index est inclus, il n'est pas nécessaire de créer ``fess_log*`` manuellement au préalable.
Si vous le créez manuellement puis importez le fichier, vous obtenez deux modèles portant le même nom.

Attention à la façon de compter du tableau de bord fourni
---------------------------------------------------------

``fess_log*`` couvre tous les index dont le nom commence par ``fess_log``, et les visualisations fournies ne filtrent pas par index.
En 15.9, les journaux de clics contiennent le terme de recherche (``searchWord``) et ``requestedAt`` ; le nombre affiché dans « search-term-rank », par exemple, additionne donc les recherches et les clics.
Si vous utilisez le mode Recherche IA, les journaux de chat (``fess_log.chat_log``) se mêlent aussi aux nombres et aux temps de réponse.

Pour ne compter que les recherches, saisissez la condition suivante dans la barre de recherche en haut du tableau de bord avant de le consulter.

::

    _index : "fess_log.search_log"

Par ailleurs, la liste des champs enregistrée dans ``fess_log*`` date d'une ancienne version et ne contient pas les champs plus récents comme ``rank``.
Pour vos propres agrégations, utilisez les modèles d'index de la section suivante.

Créer des modèles d'index pour les agrégations
==============================================

En séparant les journaux de recherche et de clics dans des modèles d'index distincts, ils ne se mélangent pas et tous les champs actuels sont disponibles.

1. Dans [Dashboards Management] > [Index patterns], cliquez sur [Create index pattern]
2. Saisissez ``fess_log.search_log`` dans « Index pattern name » et cliquez sur [Next step]
3. Choisissez ``requestedAt`` dans « Time field » et cliquez sur [Create index pattern]
4. Créez de la même manière ``fess_log.click_log`` (champ de temps ``requestedAt``)

Si des champs apparaissent par la suite (par exemple lorsque la première recherche filtrée par étiquette est enregistrée), cliquez sur [Refresh field list] dans l'écran du modèle d'index.

Gestion de l'heure
------------------

Fess enregistre les dates et heures en UTC.
Par défaut, OpenSearch Dashboards les affiche dans le fuseau horaire du navigateur et découpe aussi les journées selon celui-ci.
Pour les afficher dans un autre fuseau horaire, remplacez ``dateFormat:tz`` dans [Dashboards Management] > [Advanced settings] par votre fuseau horaire, par exemple ``Asia/Tokyo``.

L'écran [Journal de recherche] de Fess découpe les journées selon le fuseau horaire du serveur.
Les conteneurs docker-fess sont en UTC par défaut ; si vous comparez les chiffres quotidiens des deux côtés, ils peuvent donc différer en raison du décalage des limites de journée.

Champs des journaux
===================

Le journal de recherche (``fess_log.search_log``) contient une entrée par recherche.
Les champs les plus utilisés pour les agrégations sont les suivants.

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Type
     - Contenu
   * - ``queryId``
     - keyword
     - Identifiant de chaque recherche. Correspond au ``queryId`` du journal de clics
   * - ``searchWord``
     - keyword
     - Le terme de recherche. Pour une recherche filtrée par étiquette, il inclut aussi la condition, par exemple ``demande label:"hr"``
   * - ``searchField.*``
     - keyword
     - Le terme de recherche découpé par champ. Les termes ordinaires vont dans ``searchField._default``, les filtres d'étiquette dans ``searchField.label``
   * - ``requestedAt``
     - date
     - Date et heure de la recherche (enregistrées en UTC)
   * - ``hitCount``
     - long
     - Nombre de résultats. ``0`` correspond à une recherche sans résultat
   * - ``responseTime`` / ``queryTime``
     - long
     - Temps de traitement de l'ensemble de la recherche, et temps de recherche dans OpenSearch (millisecondes)
   * - ``queryOffset`` / ``queryPageSize``
     - integer
     - Position de départ et nombre de résultats par page. À partir de la deuxième page, ``queryOffset`` est supérieur à 0
   * - ``accessType``
     - keyword
     - L'une des valeurs ``json``, ``gsa``, ``admin``, ``other`` et ``web``. La page de recherche du thème par défaut appelle ``/api/v2/search`` et donne donc ``json`` ; les recherches effectuées depuis [Informations système] > [Rechercher] de l'interface d'administration donnent ``admin``
   * - ``user`` / ``roles``
     - keyword
     - L'identifiant de l'utilisateur connecté et la liste des rôles utilisés pour la recherche. Le premier caractère d'une valeur de ``roles`` indique son type : ``R`` pour un rôle, ``2`` pour un groupe et ``1`` pour un utilisateur (exemple : ``Rguest``)
   * - ``userSessionId`` / ``clientIp`` / ``userAgent`` / ``referer`` / ``virtualHost``
     - keyword
     - La valeur du cookie qui identifie l'utilisateur, l'adresse IP, le navigateur, la page de provenance et l'hôte virtuel

Le journal de clics (``fess_log.click_log``) est enregistré lorsqu'un lien des résultats de recherche est ouvert via ``/go/``.
Toutefois, il n'est pas enregistré pour les requêtes dont le navigateur n'a pas de session Fess (n'envoie pas de cookie de session valide).

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Type
     - Contenu
   * - ``queryId``
     - keyword
     - ``queryId`` de la recherche d'où provient le clic
   * - ``url`` / ``docId``
     - keyword
     - URL et identifiant du document ouvert
   * - ``rank``
     - integer
     - Position dans l'ensemble des résultats (la première place vaut 1). Le premier résultat de la deuxième page vaut 11
   * - ``order``
     - integer
     - Position dans la page (le premier vaut 0). Pour agréger les positions, utilisez ``rank``
   * - ``searchWord`` / ``accessType``
     - keyword
     - Terme de recherche et type d'accès recopiés depuis la recherche d'origine. Vous pouvez agréger par terme de recherche sans joindre le journal de recherche
   * - ``requestedAt`` / ``queryRequestedAt``
     - date
     - Date et heure du clic, et de la recherche d'origine

``searchWord``, ``accessType`` et ``rank`` figurent dans le journal de clics à partir de 15.9.
Les clics enregistrés auparavant ne les contiennent pas.

Recettes d'agrégation
=====================

Nous construisons ici les quatre « agrégations impossibles dans l'écran » citées au début.
La première est créée avec Visualize ; les autres sont exécutées avec l'API de recherche depuis [Dev Tools] dans le menu de gauche.

URL ouvertes pour chaque terme de recherche
-------------------------------------------

Ce tableau montre, pour chaque terme de recherche, quels documents ont été ouverts et à quelle position.
Il aide à choisir des candidats pour la correspondance de clé ou le boost de document.

1. Dans [Visualize] du menu de gauche, cliquez sur [Create visualization] et choisissez « Data Table »
2. Choisissez ``fess_log.click_log`` comme source
3. Sous Metrics, ajoutez une Metric avec [Add], puis choisissez « Average » pour « Aggregation » et ``rank`` pour « Field »
4. Sous Buckets, choisissez [Add] > [Split rows], puis réglez « Aggregation » sur « Terms », « Field » sur ``searchWord`` et « Size » sur 20
5. Ajoutez un autre [Split rows] avec « Terms », « Field » réglé sur ``url`` et « Size » sur 5
6. Cliquez sur [Update], choisissez la période en haut à droite et enregistrez

Les combinaisons dont la position moyenne est élevée correspondent à des documents que les utilisateurs ont ouverts après être descendus loin dans les résultats.

Termes sans résultat par rôle
-----------------------------

Si vous attribuez les rôles par service, vérifiez ce que les recherches de chaque service ne trouvent pas.

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": {
        "bool": {
          "filter": [
            { "term": { "hitCount": 0 } },
            { "range": { "requestedAt": { "gte": "now-90d/d" } } }
          ]
        }
      },
      "aggs": {
        "roles": {
          "terms": { "field": "roles", "size": 20, "exclude": "1.*" },
          "aggs": {
            "words": { "terms": { "field": "searchWord", "size": 10 } }
          }
        }
      }
    }

``exclude`` écarte les valeurs commençant par ``1`` (utilisateurs individuels) afin de ne lister que les rôles et les groupes.
Une même recherche est comptée pour chacun des rôles et groupes de l'utilisateur.
Les recherches des utilisateurs non connectés sont comptées dans ``Rguest``.

Nombre de recherches et de recherches sans résultat par étiquette
-----------------------------------------------------------------

Pour chaque étiquette, comptez le nombre de recherches effectuées avec cette étiquette sélectionnée sur la page de recherche, et combien d'entre elles n'ont donné aucun résultat.

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": { "range": { "requestedAt": { "gte": "now-90d/d" } } },
      "aggs": {
        "labels": {
          "terms": { "field": "searchField.label", "size": 20 },
          "aggs": {
            "zero_hit": { "filter": { "term": { "hitCount": 0 } } }
          }
        }
      }
    }

Si aucune recherche filtrée par étiquette n'a encore été enregistrée, le champ ``searchField.label`` n'existe pas encore et les buckets de ``labels`` sont vides.

Taux de zéro résultat par mois (deux ans)
-----------------------------------------

Observez, au-delà de la limite de période de l'écran, l'évolution à long terme du taux de zéro résultat (un ratio, et non un nombre).

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": {
        "bool": {
          "filter": [ { "range": { "requestedAt": { "gte": "now-2y/d" } } } ],
          "must_not": [ { "term": { "accessType": "admin" } } ]
        }
      },
      "aggs": {
        "per_month": {
          "date_histogram": {
            "field": "requestedAt",
            "calendar_interval": "month",
            "time_zone": "Asia/Tokyo"
          },
          "aggs": {
            "zero_hit": { "filter": { "term": { "hitCount": 0 } } },
            "zero_hit_rate": {
              "bucket_script": {
                "buckets_path": { "zero": "zero_hit>_count", "total": "_count" },
                "script": "params.zero / params.total"
              }
            }
          }
        }
      }
    }

Chaque bucket mensuel renvoie le nombre de recherches (``doc_count``), le nombre de recherches sans résultat (``zero_hit.doc_count``) et le taux de zéro résultat (``zero_hit_rate.value``, entre 0 et 1).
Grâce à ``time_zone``, les mois commencent à minuit dans le fuseau horaire indiqué (ici ``Asia/Tokyo`` ; remplacez-le par le vôtre), et ``must_not`` exclut les recherches effectuées depuis l'interface d'administration.
La disponibilité de deux ans de journaux dépend des paramètres de conservation décrits dans la section suivante.

Conservation et données personnelles
====================================

Par défaut, les journaux de recherche sont conservés indéfiniment.
En effet, « Supprimer les anciens journaux de recherche » dans [Système] > [Général] vaut ``-1`` (ne pas supprimer) par défaut.
Si vous indiquez un nombre de jours, la tâche « Log Purger », exécutée chaque jour à minuit, supprime les journaux de recherche plus anciens que ce nombre de jours.
Les journaux de clics, de favoris et de chat sont supprimés après le même nombre de jours.
Les enregistrements des utilisateurs relèvent d'un autre paramètre, « Supprimer les anciens journaux utilisateur », qui vaut lui aussi ``-1`` par défaut.

Fixez le nombre de jours en tenant compte à la fois de la profondeur d'historique souhaitée pour les tendances et des règles de votre organisation en matière de données personnelles.
Les journaux de recherche contiennent l'identifiant de l'utilisateur connecté (``user`` et les valeurs de ``roles`` commençant par ``1``), l'adresse IP et le User-Agent.
En outre, par défaut, les URL et titres des documents affichés dans les résultats de recherche sont enregistrés dans le champ ``documents`` (``logging.search.docs.enabled=true``).
Toutes ces informations sont visibles dans OpenSearch Dashboards ; respectez donc les restrictions d'accès décrites au début.

Dépannage
=========

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Symptôme
     - Points à vérifier
   * - Aucune donnée n'apparaît dans Discover ou dans les visualisations
     - La période en haut à droite couvre-t-elle les dates des journaux ? Après une recherche, l'écriture du journal peut prendre environ une minute (c'est la tâche « Log Aggregator », exécutée chaque minute, qui l'écrit)
   * - Impossible de sélectionner ``rank`` ou ``searchField.label``
     - Utilisez-vous ``fess_log*`` ? Créez un modèle d'index dédié ou cliquez sur [Refresh field list]
   * - Les nombres sont plus élevés que dans l'écran [Journal de recherche]
     - ``fess_log*`` compte-t-il aussi les journaux de clics ou de chat ? Le filtre sur le type d'accès et le fuseau horaire des limites de journée sont-ils identiques ?
   * - Le nombre de clics est faible
     - Les liens ne passent pas par ``/go/``, « Journal de recherche » est désactivé dans [Général], ou le navigateur ouvre ``/go/`` sans session Fess. Vérifiez aussi les prérequis de :doc:`guide-08`

Pour aller plus loin
====================

- Améliorer les termes de recherche repérés avec des synonymes ou des correspondances de clé : :doc:`guide-08`
- Revoir la conception des rôles et des groupes : :doc:`guide-05`
- Mettre en place une exploitation incluant la surveillance et la sauvegarde : :doc:`guide-10`
- Décider de ce qu'il faut mesurer à chaque étape d'un déploiement à l'échelle de l'entreprise : :doc:`guide-23`

Références
==========

- `Journal de recherche <https://fess.codelibs.org/fr/stable/admin/searchlog-guide.html>`__
- `Configuration de la visualisation des journaux de recherche <https://fess.codelibs.org/fr/stable/config/admin-opensearch-dashboards.html>`__
- `Général <https://fess.codelibs.org/fr/stable/admin/general-guide.html>`__
- `Installation avec Docker (Détails) <https://fess.codelibs.org/fr/stable/install/install-docker.html>`__
- `Fichiers Compose de docker-fess (GitHub) <https://github.com/codelibs/docker-fess/tree/v15.9.0/compose>`__
- `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/index/>`__
