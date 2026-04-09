===========================================================================
Partie 11 : Etendre les systemes existants avec l'API de recherche -- Recueil de patrons d'integration avec CRM et systemes internes
===========================================================================

Introduction
=============

Fess peut etre utilise non seulement comme un systeme de recherche autonome, mais aussi comme un "microservice de recherche" qui fournit des fonctionnalites de recherche aux systemes metier existants.

Cet article presente des patrons concrets d'integration avec des systemes existants en utilisant l'API de Fess.
Il couvre des scenarios d'integration pratiques tels que l'integration de la recherche de documents clients dans un CRM, la creation d'un widget de recherche FAQ et la construction d'un portail documentaire.

Public cible
=============

- Personnes souhaitant ajouter des fonctionnalites de recherche a des systemes metier existants
- Personnes interessees par l'integration de systemes via l'API de Fess
- Personnes ayant des connaissances de base en developpement d'applications web

Vue d'ensemble de l'API Fess
==============================

Voici un resume des principales API fournies par Fess.

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
     - Recuperation des labels disponibles
     - ``/api/v1/labels``
   * - API de suggestions
     - Recuperation des candidats d'auto-completion
     - ``/api/v1/suggest-words``
   * - API de mots populaires
     - Recuperation des mots-cles de recherche populaires
     - ``/api/v1/popular-words``
   * - API de sante
     - Verification de l'etat operationnel du systeme
     - ``/api/v1/health``
   * - API d'administration
     - Operations de configuration (CRUD)
     - ``/api/admin/*``

Jetons d'acces
----------------

Lors de l'utilisation de l'API, l'authentification par jetons d'acces est recommandee.

1. Creez un jeton d'acces dans [Systeme] > [Jeton d'acces] de la console d'administration
2. Incluez le jeton dans l'en-tete de la requete API

::

    Authorization: Bearer {jeton_d_acces}

Des roles peuvent etre attribues aux jetons, et le controle des resultats de recherche base sur les roles s'applique egalement aux recherches effectuees via l'API.

Patron 1 : Integration de la recherche dans un CRM
====================================================

Scenario
--------

Ajouter une fonction de recherche de documents lies aux clients dans le systeme CRM utilise par l'equipe commerciale.
Permettre la recherche transversale de propositions, comptes-rendus de reunions, contrats et plus encore depuis l'ecran client du CRM.

Approche d'implementation
--------------------------

Integrer un widget de recherche dans l'ecran client du CRM.
Envoyer le nom du client comme requete de recherche a l'API Fess et afficher les resultats dans l'ecran du CRM.

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

Points cles
------------

- Utilisez ``fields.label`` pour limiter les resultats aux documents lies aux ventes
- Utilisez ``num`` pour limiter le nombre de resultats affiches (adapte a l'espace disponible dans l'ecran du CRM)
- Il est utile de permettre la recherche non seulement par nom de client, mais aussi par nom de projet ou numero de projet

Patron 2 : Widget de recherche FAQ
====================================

Scenario
--------

Ajouter un widget de recherche FAQ au systeme interne de gestion des demandes.
Avant que les employes ne soumettent une demande, les encourager a trouver une solution par eux-memes en recherchant les FAQ pertinentes.

Approche d'implementation
--------------------------

Combiner l'API de suggestions et l'API de recherche pour afficher des candidats en temps reel pendant la saisie.

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

L'API de suggestions est utilisee pour afficher des candidats pendant que l'utilisateur saisit des mots-cles.
Lorsque l'utilisateur confirme un mot-cle et execute la recherche, l'API de recherche recupere des resultats de recherche detailles.

Points cles
------------

- La reactivite en temps reel etant cruciale pour l'API de suggestions, verifiez la vitesse de reponse
- Gerez les categories de FAQ avec des labels et proposez un filtrage par categorie
- Affichez les "mots-cles les plus recherches" via l'API de mots populaires pour aider les utilisateurs dans leur recherche

Patron 3 : Portail documentaire
=================================

Scenario
--------

Construire un portail interne de gestion de documents.
Fournir une interface combinant la navigation par categories et la recherche plein texte.

Approche d'implementation
--------------------------

Utiliser l'API de labels pour recuperer la liste des categories et l'API de recherche pour recuperer les documents au sein de chaque categorie.

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

Points cles
------------

- L'API de labels recupere la liste des categories de maniere dynamique (les ajouts et suppressions de labels sont immediatement refletes cote API)
- Utilisez ``sort=last_modified.desc`` pour afficher les documents les plus recents en haut
- La navigation sans mots-cles (recuperation de tous les elements) est egalement possible avec ``q=*``

Patron 4 : API d'indexation de contenu
========================================

Scenario
--------

Enregistrer dans l'index Fess des donnees generees par des systemes externes (journaux, rapports, enregistrements de reponses de chatbots, etc.) pour les rendre recherchables.

Approche d'implementation
--------------------------

Grace a l'API d'administration de Fess, il est possible d'enregistrer des documents dans l'index depuis des sources externes.

Utilisez le endpoint de documents de l'API d'administration pour envoyer des informations telles que le titre, l'URL et le corps du texte via une requete POST.

Points cles
------------

- Efficace pour l'integration de sources de donnees qui ne peuvent pas etre obtenues par le crawl
- Le traitement par lots peut egalement etre utilise pour enregistrer plusieurs documents en une seule fois
- Definissez les permissions du jeton d'acces de maniere appropriee et limitez les permissions d'ecriture

Bonnes pratiques pour l'integration API
=========================================

Gestion des erreurs
--------------------

Dans le cadre de l'integration API, la gestion des erreurs tenant compte des pannes reseau et de la maintenance du serveur Fess est importante.

- Configuration des delais d'attente : Definissez des delais d'attente appropries pour les appels a l'API de recherche
- Logique de nouvelles tentatives : Implementez des nouvelles tentatives pour les erreurs transitoires (environ 3 tentatives maximum)
- Solution de repli : Fournissez un affichage alternatif lorsque Fess ne repond pas (par exemple, "Le service de recherche est actuellement indisponible")

Considerations de performance
-------------------------------

- Mise en cache des reponses : Mettez en cache les resultats de la meme requete pendant une courte periode
- Limitation du nombre de resultats : Recuperez uniquement le nombre de resultats necessaire (parametre ``num``)
- Specification des champs : Recuperez uniquement les champs necessaires pour reduire la taille de la reponse

Securite
---------

- Utilisation de la communication HTTPS
- Rotation des jetons d'acces
- Definir les permissions des jetons au minimum necessaire (par exemple, lecture seule)
- Configurer CORS de maniere appropriee

Synthese
=========

Cet article a presente des patrons d'integration avec des systemes existants en utilisant l'API de Fess.

- **Integration CRM** : Recherche de documents associes depuis l'ecran client
- **Widget FAQ** : Affichage de candidats en temps reel avec suggestions + recherche
- **Portail documentaire** : Navigation par categories via l'API de labels
- **Indexation de contenu** : Enregistrement de donnees externes via l'API

L'API de Fess est basee sur REST et simple, ce qui facilite l'integration avec divers systemes.
La possibilite d'ajouter des fonctionnalites de recherche aux systemes existants en tant qu'ajout ulterieur est l'un des plus grands atouts de Fess.

Dans le prochain article, nous aborderons les scenarios permettant de rendre recherchables les donnees de SaaS et de bases de donnees.

References
==========

- `API de recherche Fess <https://fess.codelibs.org/ja/15.5/api/api-search.html>`__

- `API d'administration Fess <https://fess.codelibs.org/ja/15.5/api/api-admin.html>`__
