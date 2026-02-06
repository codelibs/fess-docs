==========================================
Fess vs autres solutions de recherche
==========================================

Introduction
============

Lors du choix d'un système de recherche plein texte, diverses options sont disponibles.
Cette page compare Fess avec les principales solutions de recherche, en expliquant les caractéristiques et les cas d'utilisation appropriés pour chacune.

.. note::

   Cette comparaison est basée sur les informations disponibles en janvier 2026.
   Pour les dernières fonctionnalités et modifications, veuillez vous référer à la documentation officielle de chaque projet.

----

Fess vs OpenSearch/Elasticsearch autonome
==========================================

Aperçu
-------

OpenSearch et Elasticsearch sont des moteurs de recherche puissants, mais leur utilisation autonome nécessite un développement supplémentaire pour créer un « système de recherche » complet.
Fess utilise OpenSearch/Elasticsearch comme backend tout en fournissant un système de recherche complet prêt à l'emploi.

Comparaison
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Fonctionnalité
     - Fess
     - OpenSearch/Elasticsearch autonome
   * - Interface de recherche
     - ✅ Intégrée
     - ❌ Nécessite un développement
   * - Interface d'administration
     - ✅ Panneau d'administration web
     - ❌ Nécessite un développement ou des outils séparés
   * - Explorateur (Crawler)
     - ✅ Intégré (Web/Fichier/BD)
     - ❌ Nécessite un développement ou des outils séparés
   * - Temps de déploiement
     - Minutes (Docker)
     - Semaines à mois (développement inclus)
   * - Personnalisabilité
     - Moyenne (personnalisation JSP/CSS)
     - Élevée (développement entièrement personnalisé possible)
   * - Coût initial
     - Faible
     - Élevé (coûts de développement)
   * - Coût opérationnel
     - Faible à moyen
     - Moyen à élevé
   * - Évolutivité
     - Élevée
     - Élevée
   * - Compétences requises
     - Connaissances informatiques de base
     - Programmation et expertise en moteurs de recherche

Quand choisir Fess
------------------

- **Lorsque vous devez construire un système de recherche rapidement**
- **Lorsque les ressources de développement sont limitées**
- **Lorsque les fonctionnalités de recherche standard sont suffisantes**
- **Lorsque l'exploration web et la recherche de fichiers sont les principaux cas d'utilisation**

Quand choisir OpenSearch/Elasticsearch autonome
-------------------------------------------------

- **Lorsque vous avez besoin d'une expérience de recherche entièrement personnalisée**
- **Lorsque vous intégrez la recherche dans une application existante**
- **Lorsqu'une logique de recherche spéciale est requise**
- **Lorsque votre équipe possède une expertise en moteurs de recherche**

.. tip::

   Après avoir déployé Fess, vous pouvez également construire une interface de recherche personnalisée en utilisant l'API.
   Envisagez de commencer avec Fess et de personnaliser selon vos besoins.

----

Fess vs Apache Solr
====================

Aperçu
-------

Apache Solr est une plateforme de recherche open source basée sur Lucene.
Elle offre une grande personnalisabilité, mais nécessite plus d'expertise pour le déploiement et l'exploitation par rapport à Fess.

Comparaison
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Fonctionnalité
     - Fess
     - Apache Solr
   * - Interface de recherche
     - ✅ Intégrée
     - ❌ Nécessite un développement
   * - Interface d'administration
     - ✅ Interface web intuitive
     - △ Interface d'administration technique
   * - Explorateur (Crawler)
     - ✅ Intégré
     - ❌ Nécessite un outil séparé (Nutch, etc.)
   * - Difficulté de mise en place
     - Faible
     - Moyenne à élevée
   * - Documentation
     - ✅ Complète
     - ✅ Complète
   * - Support cloud
     - ✅ Docker/Kubernetes
     - ✅ SolrCloud
   * - Communauté
     - Centrée sur le Japon
     - Mondiale

Quand choisir Fess
------------------

- **Lorsque l'exploration Web/Fichier est le principal cas d'utilisation**
- **Lorsque la gestion par interface graphique est importante**
- **Lorsque la facilité de déploiement est une priorité**

Quand choisir Solr
------------------

- **Lorsque vous avez déjà une expertise Solr**
- **Lorsque la recherche distribuée SolrCloud est nécessaire**
- **Lorsque des plugins Solr spécifiques sont requis**

----

Fess vs Google Site Search / Custom Search
==========================================

Aperçu
-------

Google Site Search (GSS) a été arrêté en 2018.
Son successeur, Google Custom Search (Programmable Search Engine), présente des limitations.
Fess est une cible de migration idéale depuis GSS.

Comparaison
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Fonctionnalité
     - Fess
     - Google Custom Search
   * - Affichage de publicités
     - ✅ Aucune
     - ❌ Affichées (offre gratuite)
   * - Emplacement des données
     - ✅ Auto-géré
     - ❌ Serveurs Google
   * - Contrôle de l'index
     - ✅ Contrôle total
     - △ Limité
   * - Personnalisation
     - ✅ Librement personnalisable
     - △ Limitée
   * - Recherche de contenu interne
     - ✅ Prise en charge
     - ❌ Non prise en charge
   * - Coût mensuel
     - Coûts du serveur uniquement
     - Gratuit (avec publicités) à payant
   * - Réglage de la pertinence
     - ✅ Réglage détaillé possible
     - △ Limité

Quand choisir Fess
------------------

- **Lorsque vous ne souhaitez pas afficher de publicités**
- **Lorsque le contenu interne doit être recherchable**
- **Lorsque vous souhaitez contrôler les résultats de recherche**
- **Lorsque vous souhaitez gérer vos données vous-même**

.. tip::

   Avec Fess Site Search (FSS), vous pouvez implémenter la recherche de site
   en intégrant simplement du JavaScript, tout comme Google Site Search.

----

Fess vs produits de recherche commerciaux
==========================================

Aperçu
-------

Comparaison avec des produits commerciaux tels que Microsoft SharePoint Search, Autonomy et Google Cloud Search.

Comparaison
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Fonctionnalité
     - Fess
     - Produits commerciaux (général)
   * - Coût de licence
     - ✅ Gratuit (OSS)
     - ❌ Coûteux
   * - Dépendance au fournisseur
     - ✅ Aucune
     - ❌ Oui
   * - Personnalisation
     - ✅ Code source disponible
     - △ Limitée
   * - Richesse fonctionnelle
     - ○ Basique à intermédiaire
     - ✅ Fonctionnalités avancées
   * - Support
     - △ Communauté + Commercial
     - ✅ Support fournisseur
   * - Fonctionnalités IA/ML
     - △ Suggestion basique
     - ✅ Fonctionnalités IA avancées
   * - Intégration entreprise
     - ○ Systèmes majeurs pris en charge
     - ✅ Intégration large

Quand choisir Fess
------------------

- **Lorsque vous souhaitez minimiser les coûts**
- **Lorsque vous souhaitez éviter la dépendance au fournisseur**
- **Lorsque les fonctionnalités de recherche basiques sont suffisantes**
- **Lorsque vous souhaitez tirer parti de l'open source**

Quand choisir les produits commerciaux
---------------------------------------

- **Lorsque des fonctionnalités IA/ML avancées sont nécessaires**
- **Lorsqu'un support fournisseur complet est requis**
- **Lorsque l'intégration avec des écosystèmes commerciaux existants est nécessaire**

.. note::

   La version commerciale de Fess, `N2 Search <https://www.n2sm.net/products/n2search.html>`__,
   fournit des fonctionnalités entreprise supplémentaires et un support.

----

Guide de sélection
====================

Utilisez l'organigramme suivant pour sélectionner la solution optimale :

::

    Disposez-vous de ressources de développement suffisantes ?
          │
    ┌─────┴─────┐
    │           │
   Oui        Non
    │           │
    ▼           ▼
  Les exigences    →  Envisagez Fess
  sont-elles
  spécialisées ?
    │
    ├── Oui → OpenSearch/Elasticsearch autonome
    │         ou produits commerciaux
    │
    └── Non → Fess est-il suffisant ?
              │
              ├── Oui → Fess
              │
              └── Non → Réévaluez les exigences

Résumé
=======

Fess est un choix optimal en tant que « système de recherche prêt à l'emploi » pour de nombreux cas.

**Points forts de Fess** :

- Déploiement en quelques minutes
- Construction d'un système de recherche sans développement
- Open source et gratuit

**Prochaines étapes** :

1. Essayez Fess avec le `Guide de démarrage rapide <../quick-start.html>`__
2. Évaluez par rapport à vos exigences
3. Consultez le `support commercial <../support-services.html>`__ si nécessaire
