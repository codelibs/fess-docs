============================================================
Partie 22 : Dessiner une carte des connaissances organisationnelles a partir des donnees de recherche -- Comprendre l'utilisation de l'information via le tableau de bord analytique
============================================================

Introduction
=============

Un systeme de recherche est un outil pour "trouver" des informations, mais les journaux de recherche eux-memes constituent egalement une precieuse source d'informations.
"Que recherche-t-on ?", "Que ne trouve-t-on pas ?", "Quelles informations sont frequemment consultees ?" -- ces donnees servent de miroir refletant les besoins informationnels et les lacunes de connaissances de l'organisation.

Dans cet article, nous combinons les journaux de recherche de Fess avec OpenSearch Dashboards pour construire un tableau de bord analytique qui visualise l'etat d'utilisation des connaissances de l'organisation.

Public cible
=============

- Les personnes souhaitant comprendre quantitativement l'utilisation de leur systeme de recherche
- Les personnes souhaitant collecter des donnees pour des strategies d'utilisation de l'information
- Les personnes souhaitant apprendre les operations de base d'OpenSearch Dashboards

La valeur des donnees de recherche
====================================

Ce que les journaux de recherche peuvent reveler
---------------------------------------------------

Les journaux de recherche sont un type de donnees rare permettant de comprendre quantitativement les besoins informationnels d'une organisation.

.. list-table:: Informations tirees des donnees de recherche
   :header-rows: 1
   :widths: 30 70

   * - Donnees
     - Information
   * - Mots-cles de recherche
     - Ce que les employes recherchent (besoins informationnels)
   * - Requetes sans resultats
     - Informations manquantes dans l'organisation (lacunes de connaissances)
   * - Journaux de clics
     - Quels resultats de recherche ont ete utiles (valeur du contenu)
   * - Frequence de recherche dans le temps
     - Evolution des besoins informationnels (tendances)
   * - Mots populaires
     - Sujets d'interet dans l'ensemble de l'organisation

Donnees collectees par Fess
==============================

Fess collecte et stocke automatiquement les donnees suivantes.

Journaux de recherche (``fess_log.search_log``)
--------------------------------------------------

Ils peuvent etre consultes dans la console d'administration sous [Informations systeme] > [Journal de recherche].
Ils sont stockes dans l'index OpenSearch ``fess_log.search_log``.

Champs principaux :

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Nom du champ
     - Type
     - Description
   * - ``searchWord``
     - keyword
     - Mot-cle de recherche
   * - ``requestedAt``
     - date
     - Date et heure de la recherche
   * - ``hitCount``
     - long
     - Nombre de resultats de recherche (0 indique une requete sans resultats)
   * - ``queryTime``
     - long
     - Temps d'execution de la requete (millisecondes)
   * - ``responseTime``
     - long
     - Temps de reponse total (millisecondes)
   * - ``userAgent``
     - keyword
     - Agent utilisateur
   * - ``clientIp``
     - keyword
     - Adresse IP du client
   * - ``accessType``
     - keyword
     - Type d'acces (web, json, gsa, admin, etc.)
   * - ``queryId``
     - keyword
     - ID de requete (utilise pour le lien avec les journaux de clics)

Journaux de clics (``fess_log.click_log``)
--------------------------------------------

Ce sont les enregistrements des clics sur les liens des resultats de recherche.
Ils sont stockes dans l'index OpenSearch ``fess_log.click_log``.

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Nom du champ
     - Type
     - Description
   * - ``url``
     - keyword
     - URL cliquee
   * - ``queryId``
     - keyword
     - queryId du journal de recherche (identifie quelle recherche a conduit au clic)
   * - ``order``
     - integer
     - Position d'affichage dans les resultats de recherche
   * - ``requestedAt``
     - date
     - Date et heure du clic
   * - ``docId``
     - keyword
     - ID du document

Mots populaires
-----------------

Les mots populaires affiches sur l'ecran de recherche sont agreges a partir des journaux de recherche dans l'index suggest de Fess.
Les requetes depassant un certain nombre de resultats de recherche sont classees en fonction du nombre de recherches.

Visualisation avec OpenSearch Dashboards
==========================================

Les journaux de recherche de Fess etant stockes dans OpenSearch, une visualisation avancee est possible avec OpenSearch Dashboards.

Configuration d'OpenSearch Dashboards
----------------------------------------

Ajoutez OpenSearch Dashboards a votre configuration Docker Compose.

.. code-block:: yaml

    services:
      opensearch-dashboards:
        image: opensearchproject/opensearch-dashboards:3.6.0
        ports:
          - "5601:5601"
        environment:
          OPENSEARCH_HOSTS: '["http://opensearch:9200"]'
          DISABLE_SECURITY_DASHBOARDS_PLUGIN: "true"

Accedez a ``http://localhost:5601`` pour utiliser l'interface de Dashboards.

Creation de modeles d'index
------------------------------

Pour visualiser les donnees de journaux Fess dans OpenSearch Dashboards, vous devez d'abord creer des modeles d'index.

1. Accedez a Dashboards et selectionnez [Stack Management] > [Index Patterns] dans le menu de gauche
2. Cliquez sur [Create index pattern]
3. Creez les modeles d'index suivants

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - Modele d'index
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
Creez chaque visualisation depuis [Visualize] dans le menu de gauche et regroupez-les dans un [Dashboard].

Apercu de l'utilisation de la recherche
-----------------------------------------

**Evolution du nombre de recherches quotidiennes**

Comprenez comment l'utilisation de la recherche evolue dans le temps.

- Modele d'index : ``fess_log.search_log``
- Visualisation : Line (graphique en courbes)
- Axe X : Date Histogram (champ : ``requestedAt``, intervalle : 1d)
- Axe Y : Count

Si l'utilisation augmente, cela prouve que le systeme de recherche s'est implante ; si elle diminue, des ameliorations sont necessaires.

**Nombre de recherches par tranche horaire**

Comprenez a quels moments de la journee les recherches sont les plus nombreuses.

- Visualisation : Vertical Bar (graphique en barres)
- Axe X : Date Histogram (champ : ``requestedAt``, intervalle : 1h)
- Axe Y : Count

Si les recherches sont frequentes au debut de la journee de travail ou apres le dejeuner, cela indique que la collecte d'informations est devenue une partie integrante du travail quotidien.

Analyse de la qualite de recherche
-------------------------------------

**Evolution du taux de requetes sans resultats**

Le taux de requetes sans resultats est un indicateur important de la qualite de recherche.
Les enregistrements ou le champ ``hitCount`` du journal de recherche vaut ``0`` correspondent aux requetes sans resultats.

- Modele d'index : ``fess_log.search_log``
- Filtre : Ajouter ``hitCount: 0`` pour extraire les requetes sans resultats
- Visualisation : Line (graphique en courbes)
- Axe X : Date Histogram (champ : ``requestedAt``, intervalle : 1d)
- Axe Y : Count

Si le taux de requetes sans resultats est eleve, il est necessaire d'ajouter des synonymes ou d'elargir la portee de l'exploration (voir la Partie 8).

Notez que vous pouvez egalement consulter la liste des requetes sans resultats dans la console d'administration sous [Informations systeme] > [Journal de recherche].

**Nuage de mots des requetes sans resultats**

L'affichage des requetes sans resultats sous forme de nuage de mots offre un apercu rapide des informations manquantes.

- Filtre : ``hitCount: 0``
- Visualisation : Tag Cloud
- Champ : Terms Aggregation (champ : ``searchWord``, taille : 50)

Analyse de la valeur du contenu
---------------------------------

**Resultats de recherche les plus cliques**

Les resultats de recherche frequemment cliques representent un contenu a forte valeur pour l'organisation.

- Modele d'index : ``fess_log.click_log``
- Visualisation : Data Table
- Champ : Terms Aggregation (champ : ``url``, taille : 20, tri : Count decroissant)

Donnez la priorite a la maintenance et a la mise a jour de ces contenus.

**Distribution des positions de clic**

Examinez la distribution des positions dans les resultats de recherche ou les clics ont lieu.

- Modele d'index : ``fess_log.click_log``
- Visualisation : Vertical Bar (graphique en barres)
- Axe X : Histogram (champ : ``order``, intervalle : 1)
- Axe Y : Count

Si les positions 1 a 3 recoivent le plus de clics, la qualite de recherche est bonne ; si les positions 10 et au-dela recoivent beaucoup de clics, des ameliorations du classement sont necessaires.

Analyse des tendances des besoins informationnels
----------------------------------------------------

**Classement des mots-cles populaires**

Comprenez ce qui interesse l'organisation dans son ensemble.

- Modele d'index : ``fess_log.search_log``
- Visualisation : Data Table
- Champ : Terms Aggregation (champ : ``searchWord``, taille : 20, tri : Count decroissant)

Les changements dans les mots-cles populaires refletent les evolutions des defis et des centres d'interet de l'organisation.

Exploitation des resultats d'analyse
=======================================

Les resultats de l'analyse des donnees de recherche peuvent etre appliques aux initiatives suivantes.

Strategie de contenu
----------------------

- **Requetes sans resultats** : Identifier le contenu manquant et en demander la creation
- **Mots-cles populaires** : Enrichir l'information sur les sujets frequemment recherches
- **Resultats a faible taux de clics** : Envisager l'amelioration ou la suppression du contenu

Amelioration de la qualite de recherche
-----------------------------------------

- **Ajout de synonymes** : Decouvrir des candidats synonymes a partir des requetes sans resultats
- **Configuration de Key Match** : Definir des resultats optimaux pour les requetes populaires
- **Ajustement du Boost** : Ameliorer le classement en fonction des taux de clics

Decisions d'investissement IT
-------------------------------

- **Augmentation de l'utilisation** : Planifier le renforcement des ressources serveur
- **Nouveaux besoins informationnels** : Envisager la connexion de sources de donnees supplementaires
- **Besoins en fonctionnalites IA** : Decider de l'introduction du mode de recherche IA (voir la Partie 19)

Creation de rapports periodiques
==================================

Resumez les resultats d'analyse dans des rapports periodiques et partagez-les avec les parties prenantes.

Exemple d'elements du rapport mensuel
-----------------------------------------

1. Resume de l'utilisation de la recherche (nombre total de recherches, comparaison avec le mois precedent)
2. Evolution du taux de requetes sans resultats et etat des ameliorations
3. Top 10 des mots-cles populaires
4. Lacunes de connaissances nouvellement decouvertes
5. Mesures d'amelioration mises en oeuvre et leurs effets
6. Plans d'amelioration pour le mois suivant

Conclusion
===========

Dans cet article, nous avons explique comment visualiser l'utilisation des connaissances organisationnelles a l'aide des journaux de recherche.

- Informations tirees des journaux de recherche (besoins informationnels, lacunes de connaissances, valeur du contenu)
- Construction de tableaux de bord de visualisation avec OpenSearch Dashboards
- Application des resultats d'analyse a la strategie de contenu, a l'amelioration de la qualite de recherche et aux investissements IT
- Amelioration continue grace aux rapports periodiques

Les donnees de recherche sont un actif precieux pour dessiner une "carte des connaissances organisationnelles."
Ceci conclut la section sur l'IA et la recherche de nouvelle generation. Dans le prochain et dernier volet, nous presenterons un bilan global de la serie.

References
===========

- `Journal de recherche Fess <https://fess.codelibs.org/ja/15.5/admin/searchlog.html>`__

- `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/>`__
