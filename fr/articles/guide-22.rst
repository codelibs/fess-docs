=====================================================================================================
Partie 22 : Dessiner une carte des connaissances organisationnelles à partir des données de recherche
=====================================================================================================

Introduction
=============

Un système de recherche est un outil pour "trouver" des informations, mais les journaux de recherche eux-mêmes constituent également une précieuse source d'informations.
"Que recherche-t-on ?", "Que ne trouve-t-on pas ?", "Quelles informations sont fréquemment consultées ?" -- ces données servent de miroir reflétant les besoins informationnels et les lacunes de connaissances de l'organisation.

Dans cet article, nous combinons les journaux de recherche de Fess avec OpenSearch Dashboards pour construire un tableau de bord analytique qui visualise l'état d'utilisation des connaissances de l'organisation.

Public cible
=============

- Les personnes souhaitant comprendre quantitativement l'utilisation de leur système de recherche
- Les personnes souhaitant collecter des données pour des stratégies d'utilisation de l'information
- Les personnes souhaitant apprendre les opérations de base d'OpenSearch Dashboards

La valeur des données de recherche
====================================

Ce que les journaux de recherche peuvent révéler
---------------------------------------------------

Les journaux de recherche sont un type de données rare permettant de comprendre quantitativement les besoins informationnels d'une organisation.

.. list-table:: Informations tirées des données de recherche
   :header-rows: 1
   :widths: 30 70

   * - Données
     - Information
   * - Mots-clés de recherche
     - Ce que les employés recherchent (besoins informationnels)
   * - Requêtes sans résultats
     - Informations manquantes dans l'organisation (lacunes de connaissances)
   * - Journaux de clics
     - Quels résultats de recherche ont été utiles (valeur du contenu)
   * - Fréquence de recherche dans le temps
     - Évolution des besoins informationnels (tendances)
   * - Mots populaires
     - Sujets d'intérêt dans l'ensemble de l'organisation

Données collectées par Fess
==============================

Fess collecte et stocke automatiquement les données suivantes.

Journaux de recherche (``fess_log.search_log``)
--------------------------------------------------

Ils peuvent être consultés dans la console d'administration sous [Informations système] > [Journal de recherche].
Ils sont stockés dans l'index OpenSearch ``fess_log.search_log``.

Champs principaux :

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Nom du champ
     - Type
     - Description
   * - ``searchWord``
     - keyword
     - Mot-clé de recherche
   * - ``requestedAt``
     - date
     - Date et heure de la recherche
   * - ``hitCount``
     - long
     - Nombre de résultats de recherche (0 indique une requête sans résultats)
   * - ``queryTime``
     - long
     - Temps d'exécution de la requête (millisecondes)
   * - ``responseTime``
     - long
     - Temps de réponse total (millisecondes)
   * - ``userAgent``
     - keyword
     - Agent utilisateur
   * - ``clientIp``
     - keyword
     - Adresse IP du client
   * - ``accessType``
     - keyword
     - Type d'accès (web, json, gsa, admin, etc.)
   * - ``queryId``
     - keyword
     - ID de requête (utilisé pour le lien avec les journaux de clics)

Journaux de clics (``fess_log.click_log``)
--------------------------------------------

Ce sont les enregistrements des clics sur les liens des résultats de recherche.
Ils sont stockés dans l'index OpenSearch ``fess_log.click_log``.

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Nom du champ
     - Type
     - Description
   * - ``url``
     - keyword
     - URL cliquée
   * - ``queryId``
     - keyword
     - queryId du journal de recherche (identifie quelle recherche a conduit au clic)
   * - ``order``
     - integer
     - Position d'affichage dans les résultats de recherche
   * - ``requestedAt``
     - date
     - Date et heure du clic
   * - ``docId``
     - keyword
     - ID du document

Mots populaires
-----------------

Les mots populaires affichés sur l'écran de recherche sont agrégés à partir des journaux de recherche dans l'index suggest de Fess.
Les requêtes dépassant un certain nombre de résultats de recherche sont classées en fonction du nombre de recherches.

Visualisation avec OpenSearch Dashboards
==========================================

Les journaux de recherche de Fess étant stockés dans OpenSearch, une visualisation avancée est possible avec OpenSearch Dashboards.

Configuration d'OpenSearch Dashboards
----------------------------------------

Ajoutez OpenSearch Dashboards à votre configuration Docker Compose.

.. code-block:: yaml

    services:
      opensearch-dashboards:
        image: public.ecr.aws/opensearchproject/opensearch-dashboards:3.6.0
        ports:
          - "5601:5601"
        environment:
          OPENSEARCH_HOSTS: '["http://opensearch:9200"]'
          DISABLE_SECURITY_DASHBOARDS_PLUGIN: "true"

Accédez à ``http://localhost:5601`` pour utiliser l'interface de Dashboards.

Création de modèles d'index
------------------------------

Pour visualiser les données de journaux Fess dans OpenSearch Dashboards, vous devez d'abord créer des modèles d'index.

1. Accédez à Dashboards et sélectionnez [Stack Management] > [Index Patterns] dans le menu de gauche
2. Cliquez sur [Create index pattern]
3. Créez les modèles d'index suivants

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - Modèle d'index
     - Champ temporel
     - Utilisation
   * - ``fess_log.search_log``
     - ``requestedAt``
     - Analyse des journaux de recherche
   * - ``fess_log.click_log``
     - ``requestedAt``
     - Analyse des journaux de clics

Conception du tableau de bord
===============================

Concevez le tableau de bord selon les perspectives analytiques suivantes.
Créez chaque visualisation depuis [Visualize] dans le menu de gauche et regroupez-les dans un [Dashboard].

Aperçu de l'utilisation de la recherche
-----------------------------------------

**Évolution du nombre de recherches quotidiennes**

Comprenez comment l'utilisation de la recherche évolue dans le temps.

- Modèle d'index : ``fess_log.search_log``
- Visualisation : Line (graphique en courbes)
- Axe X : Date Histogram (champ : ``requestedAt``, intervalle : 1d)
- Axe Y : Count

Si l'utilisation augmente, cela prouve que le système de recherche s'est implanté ; si elle diminue, des améliorations sont nécessaires.

**Nombre de recherches par tranche horaire**

Comprenez à quels moments de la journée les recherches sont les plus nombreuses.

- Visualisation : Vertical Bar (graphique en barres)
- Axe X : Date Histogram (champ : ``requestedAt``, intervalle : 1h)
- Axe Y : Count

Si les recherches sont fréquentes au début de la journée de travail ou après le déjeuner, cela indique que la collecte d'informations est devenue une partie intégrante du travail quotidien.

Analyse de la qualité de recherche
-------------------------------------

**Évolution du taux de requêtes sans résultats**

Le taux de requêtes sans résultats est un indicateur important de la qualité de recherche.
Les enregistrements où le champ ``hitCount`` du journal de recherche vaut ``0`` correspondent aux requêtes sans résultats.

- Modèle d'index : ``fess_log.search_log``
- Filtre : Ajouter ``hitCount: 0`` pour extraire les requêtes sans résultats
- Visualisation : Line (graphique en courbes)
- Axe X : Date Histogram (champ : ``requestedAt``, intervalle : 1d)
- Axe Y : Count

Si le taux de requêtes sans résultats est élevé, il est nécessaire d'ajouter des synonymes ou d'élargir la portée de l'exploration (voir la Partie 8).

Notez que vous pouvez également consulter la liste des requêtes sans résultats dans la console d'administration sous [Informations système] > [Journal de recherche].

**Nuage de mots des requêtes sans résultats**

L'affichage des requêtes sans résultats sous forme de nuage de mots offre un aperçu rapide des informations manquantes.

- Filtre : ``hitCount: 0``
- Visualisation : Tag Cloud
- Champ : Terms Aggregation (champ : ``searchWord``, taille : 50)

Analyse de la valeur du contenu
---------------------------------

**Résultats de recherche les plus cliqués**

Les résultats de recherche fréquemment cliqués représentent un contenu à forte valeur pour l'organisation.

- Modèle d'index : ``fess_log.click_log``
- Visualisation : Data Table
- Champ : Terms Aggregation (champ : ``url``, taille : 20, tri : Count décroissant)

Donnez la priorité à la maintenance et à la mise à jour de ces contenus.

**Distribution des positions de clic**

Examinez la distribution des positions dans les résultats de recherche où les clics ont lieu.

- Modèle d'index : ``fess_log.click_log``
- Visualisation : Vertical Bar (graphique en barres)
- Axe X : Histogram (champ : ``order``, intervalle : 1)
- Axe Y : Count

Si les positions 1 à 3 reçoivent le plus de clics, la qualité de recherche est bonne ; si les positions 10 et au-delà reçoivent beaucoup de clics, des améliorations du classement sont nécessaires.

Analyse des tendances des besoins informationnels
----------------------------------------------------

**Classement des mots-clés populaires**

Comprenez ce qui intéresse l'organisation dans son ensemble.

- Modèle d'index : ``fess_log.search_log``
- Visualisation : Data Table
- Champ : Terms Aggregation (champ : ``searchWord``, taille : 20, tri : Count décroissant)

Les changements dans les mots-clés populaires reflètent les évolutions des défis et des centres d'intérêt de l'organisation.

Exploitation des résultats d'analyse
=======================================

Les résultats de l'analyse des données de recherche peuvent être appliqués aux initiatives suivantes.

Stratégie de contenu
----------------------

- **Requêtes sans résultats** : Identifier le contenu manquant et en demander la création
- **Mots-clés populaires** : Enrichir l'information sur les sujets fréquemment recherchés
- **Résultats à faible taux de clics** : Envisager l'amélioration ou la suppression du contenu

Amélioration de la qualité de recherche
-----------------------------------------

- **Ajout de synonymes** : Découvrir des candidats synonymes à partir des requêtes sans résultats
- **Configuration de Key Match** : Définir des résultats optimaux pour les requêtes populaires
- **Ajustement du Boost** : Améliorer le classement en fonction des taux de clics

Décisions d'investissement IT
-------------------------------

- **Augmentation de l'utilisation** : Planifier le renforcement des ressources serveur
- **Nouveaux besoins informationnels** : Envisager la connexion de sources de données supplémentaires
- **Besoins en fonctionnalités IA** : Décider de l'introduction du mode de recherche IA (voir la Partie 19)

Création de rapports périodiques
==================================

Résumez les résultats d'analyse dans des rapports périodiques et partagez-les avec les parties prenantes.

Exemple d'éléments du rapport mensuel
-----------------------------------------

1. Résumé de l'utilisation de la recherche (nombre total de recherches, comparaison avec le mois précédent)
2. Évolution du taux de requêtes sans résultats et état des améliorations
3. Top 10 des mots-clés populaires
4. Lacunes de connaissances nouvellement découvertes
5. Mesures d'amélioration mises en œuvre et leurs effets
6. Plans d'amélioration pour le mois suivant

Conclusion
===========

Dans cet article, nous avons expliqué comment visualiser l'utilisation des connaissances organisationnelles à l'aide des journaux de recherche.

- Informations tirées des journaux de recherche (besoins informationnels, lacunes de connaissances, valeur du contenu)
- Construction de tableaux de bord de visualisation avec OpenSearch Dashboards
- Application des résultats d'analyse à la stratégie de contenu, à l'amélioration de la qualité de recherche et aux investissements IT
- Amélioration continue grâce aux rapports périodiques

Les données de recherche sont un actif précieux pour dessiner une "carte des connaissances organisationnelles."
Ceci conclut la section sur l'IA et la recherche de nouvelle génération. Dans le prochain et dernier volet, nous présenterons un bilan global de la série.

Références
===========

- `Journal de recherche Fess <https://fess.codelibs.org/ja/15.5/admin/searchlog.html>`__

- `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/>`__
