==================================================================
Partie 11 : Étendre les systèmes existants avec l'API de recherche
==================================================================

Introduction
=============

Fess peut être utilisé non seulement comme un système de recherche autonome, mais aussi comme un "microservice de recherche" qui fournit des fonctionnalités de recherche aux systèmes métier existants.

Cet article présente des patrons concrets d'intégration avec des systèmes existants en utilisant l'API de Fess.
Il couvre des scénarios d'intégration pratiques tels que l'intégration de la recherche de documents clients dans un CRM, la création d'un widget de recherche FAQ et la construction d'un portail documentaire.

Public cible
=============

- Personnes souhaitant ajouter des fonctionnalités de recherche à des systèmes métier existants
- Personnes intéressées par l'intégration de systèmes via l'API de Fess
- Personnes ayant des connaissances de base en développement d'applications web

Vue d'ensemble de l'API Fess
==============================

Voici un résumé des principales API fournies par Fess.

.. list-table:: Liste des API Fess
   :header-rows: 1
   :widths: 25 45 30

   * - API
     - Utilisation
     - Endpoint
   * - API de recherche
     - Recherche plein texte de documents
     - ``/api/v1/documents``
   * - API de labels
     - Récupération des labels disponibles
     - ``/api/v1/labels``
   * - API de suggestions
     - Récupération des candidats d'auto-complétion
     - ``/api/v1/suggest-words``
   * - API de mots populaires
     - Récupération des mots-clés de recherche populaires
     - ``/api/v1/popular-words``
   * - API de santé
     - Vérification de l'état opérationnel du système
     - ``/api/v1/health``
   * - API d'administration
     - Opérations de configuration (CRUD)
     - ``/api/admin/*``

Jetons d'accès
----------------

Lors de l'utilisation de l'API, l'authentification par jetons d'accès est recommandée.

1. Créez un jeton d'accès dans [Système] > [Jeton d'accès] de la console d'administration
2. Incluez le jeton dans l'en-tête de la requête API

::

    Authorization: Bearer {jeton_d_acces}

Des rôles peuvent être attribués aux jetons, et le contrôle des résultats de recherche basé sur les rôles s'applique également aux recherches effectuées via l'API.

Patron 1 : Intégration de la recherche dans un CRM
====================================================

Scénario
--------

Ajouter une fonction de recherche de documents liés aux clients dans le système CRM utilisé par l'équipe commerciale.
Permettre la recherche transversale de propositions, comptes-rendus de réunions, contrats et plus encore depuis l'écran client du CRM.

Approche d'implémentation
--------------------------

Intégrer un widget de recherche dans l'écran client du CRM.
Envoyer le nom du client comme requête de recherche à l'API Fess et afficher les résultats dans l'écran du CRM.

.. code-block:: javascript

    // Widget de recherche dans l'ecran du CRM
    async function searchCustomerDocs(customerName) {
      const params = new URLSearchParams({
        q: customerName,
        num: '5',
        'fields.label': 'sales-docs'
      });
      const url = `https://fess.example.com/api/v1/documents?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      return await response.json();
    }

Points clés
------------

- Utilisez ``fields.label`` pour limiter les résultats aux documents liés aux ventes
- Utilisez ``num`` pour limiter le nombre de résultats affichés (adapté à l'espace disponible dans l'écran du CRM)
- Il est utile de permettre la recherche non seulement par nom de client, mais aussi par nom de projet ou numéro de projet

Patron 2 : Widget de recherche FAQ
====================================

Scénario
--------

Ajouter un widget de recherche FAQ au système interne de gestion des demandes.
Avant que les employés ne soumettent une demande, les encourager à trouver une solution par eux-mêmes en recherchant les FAQ pertinentes.

Approche d'implémentation
--------------------------

Combiner l'API de suggestions et l'API de recherche pour afficher des candidats en temps réel pendant la saisie.

.. code-block:: javascript

    // Suggestions pendant la saisie
    async function getSuggestions(query) {
      const params = new URLSearchParams({ q: query, num: '5' });
      const url = `https://fess.example.com/api/v1/suggest-words?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      const data = await response.json();
      return data.data;
    }

L'API de suggestions est utilisée pour afficher des candidats pendant que l'utilisateur saisit des mots-clés.
Lorsque l'utilisateur confirme un mot-clé et exécute la recherche, l'API de recherche récupère des résultats de recherche détaillés.

Points clés
------------

- La réactivité en temps réel étant cruciale pour l'API de suggestions, vérifiez la vitesse de réponse
- Gérez les catégories de FAQ avec des labels et proposez un filtrage par catégorie
- Affichez les "mots-clés les plus recherchés" via l'API de mots populaires pour aider les utilisateurs dans leur recherche

Patron 3 : Portail documentaire
=================================

Scénario
--------

Construire un portail interne de gestion de documents.
Fournir une interface combinant la navigation par catégories et la recherche plein texte.

Approche d'implémentation
--------------------------

Utiliser l'API de labels pour récupérer la liste des catégories et l'API de recherche pour récupérer les documents au sein de chaque catégorie.

.. code-block:: javascript

    // Recuperation de la liste des labels
    async function getLabels() {
      const url = 'https://fess.example.com/api/v1/labels';
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      const data = await response.json();
      return data.data;
    }

    // Recherche filtree par label
    async function searchByLabel(query, label) {
      const params = new URLSearchParams({
        q: query || '*',
        'fields.label': label,
        num: '20',
        sort: 'last_modified.desc'
      });
      const url = `https://fess.example.com/api/v1/documents?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      return await response.json();
    }

Points clés
------------

- L'API de labels récupère la liste des catégories de manière dynamique (les ajouts et suppressions de labels sont immédiatement reflétés côté API)
- Utilisez ``sort=last_modified.desc`` pour afficher les documents les plus récents en haut
- La navigation sans mots-clés (récupération de tous les éléments) est également possible avec ``q=*``

Patron 4 : API d'indexation de contenu
========================================

Scénario
--------

Enregistrer dans l'index Fess des données générées par des systèmes externes (journaux, rapports, enregistrements de réponses de chatbots, etc.) pour les rendre recherchables.

Approche d'implémentation
--------------------------

Grâce à l'API d'administration de Fess, il est possible d'enregistrer des documents dans l'index depuis des sources externes.

Utilisez le endpoint de documents de l'API d'administration pour envoyer des informations telles que le titre, l'URL et le corps du texte via une requête POST.

Points clés
------------

- Efficace pour l'intégration de sources de données qui ne peuvent pas être obtenues par le crawl
- Le traitement par lots peut également être utilisé pour enregistrer plusieurs documents en une seule fois
- Définissez les permissions du jeton d'accès de manière appropriée et limitez les permissions d'écriture

Bonnes pratiques pour l'intégration API
=========================================

Gestion des erreurs
--------------------

Dans le cadre de l'intégration API, la gestion des erreurs tenant compte des pannes réseau et de la maintenance du serveur Fess est importante.

- Configuration des délais d'attente : Définissez des délais d'attente appropriés pour les appels à l'API de recherche
- Logique de nouvelles tentatives : Implémentez des nouvelles tentatives pour les erreurs transitoires (environ 3 tentatives maximum)
- Solution de repli : Fournissez un affichage alternatif lorsque Fess ne répond pas (par exemple, "Le service de recherche est actuellement indisponible")

Considérations de performance
-------------------------------

- Mise en cache des réponses : Mettez en cache les résultats de la même requête pendant une courte période
- Limitation du nombre de résultats : Récupérez uniquement le nombre de résultats nécessaire (paramètre ``num``)
- Spécification des champs : Récupérez uniquement les champs nécessaires pour réduire la taille de la réponse

Sécurité
---------

- Utilisation de la communication HTTPS
- Rotation des jetons d'accès
- Définir les permissions des jetons au minimum nécessaire (par exemple, lecture seule)
- Configurer CORS de manière appropriée

Synthèse
=========

Cet article a présenté des patrons d'intégration avec des systèmes existants en utilisant l'API de Fess.

- **Intégration CRM** : Recherche de documents associés depuis l'écran client
- **Widget FAQ** : Affichage de candidats en temps réel avec suggestions + recherche
- **Portail documentaire** : Navigation par catégories via l'API de labels
- **Indexation de contenu** : Enregistrement de données externes via l'API

L'API de Fess est basée sur REST et simple, ce qui facilite l'intégration avec divers systèmes.
La possibilité d'ajouter des fonctionnalités de recherche aux systèmes existants en tant qu'ajout ultérieur est l'un des plus grands atouts de Fess.

Dans le prochain article, nous aborderons les scénarios permettant de rendre recherchables les données de SaaS et de bases de données.

Références
==========

- `API de recherche Fess <https://fess.codelibs.org/ja/15.5/api/api-search.html>`__

- `API d'administration Fess <https://fess.codelibs.org/ja/15.5/api/api-admin.html>`__
