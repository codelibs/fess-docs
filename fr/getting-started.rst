======
Utilisation
======

Cette page explique l'utilisation de base de Fess.
Si vous n'avez pas encore installé Fess, veuillez consulter :doc:`setup` ou :doc:`quick-start`.

À propos de l'interface utilisateur de Fess
===================

Fess propose les interfaces utilisateur suivantes.

-  Interface de recherche et d'affichage des résultats via navigateur (pour les utilisateurs généraux)
-  Interface d'administration via navigateur (pour les administrateurs)

Écran de recherche (pour les utilisateurs généraux)
===========================

Accès à l'écran de recherche
------------------

Interface permettant aux utilisateurs généraux de rechercher des documents indexés par Fess.

En accédant à http://localhost:8080/, le champ de saisie de recherche et le bouton de recherche s'affichent.

Recherche de base
----------

Entrez un mot à rechercher et cliquez sur le bouton de recherche pour afficher les résultats de recherche.

|Affichage des résultats de recherche dans le navigateur|

Les résultats de recherche affichent les informations suivantes :

- Titre
- URL
- Extrait du contenu (les mots-clés de recherche sont mis en surbrillance)
- Date de dernière mise à jour
- Taille du fichier (pour les documents)

Recherche avancée
--------

**Recherche AND**

En entrant plusieurs mots-clés séparés par des espaces, vous recherchez les documents contenant tous les mots-clés.

Exemple : ``Fess recherche`` → Documents contenant à la fois « Fess » et « recherche »

**Recherche OR**

En entrant ``OR`` entre les mots-clés, vous recherchez les documents contenant l'un ou l'autre des mots-clés.

Exemple : ``Fess OR Elasticsearch`` → Documents contenant « Fess » ou « Elasticsearch »

**Recherche NOT**

En ajoutant ``-`` devant un mot-clé à exclure, vous recherchez les documents ne contenant pas ce mot-clé.

Exemple : ``Fess -Elasticsearch`` → Documents contenant « Fess » mais pas « Elasticsearch »

**Recherche de phrases**

En entourant les mots-clés de ``""``, vous effectuez une recherche de correspondance exacte de cette phrase.

Exemple : ``"recherche en texte intégral"`` → Documents contenant le mot « recherche en texte intégral »

Options de recherche
------------

Les options suivantes sont disponibles sur l'écran de recherche :

- **Recherche par étiquette** : Rechercher uniquement les documents ayant une étiquette spécifique
- **Spécification de période** : Rechercher uniquement les documents mis à jour pendant une période spécifique
- **Spécification de format de fichier** : Rechercher uniquement des formats de fichiers spécifiques (PDF, Word, etc.)

Écran d'administration (pour les administrateurs)
====================

Accès à l'écran d'administration
------------------

Interface permettant aux administrateurs de gérer Fess.

En accédant à http://localhost:8080/admin/, l'écran de connexion s'affiche.

Compte administrateur par défaut :

- **Nom d'utilisateur** : ``admin``
- **Mot de passe** : ``admin``

.. warning::

   **Note importante concernant la sécurité**

   Veuillez absolument changer le mot de passe par défaut.
   En particulier en environnement de production, il est fortement recommandé de changer le mot de passe immédiatement après la première connexion.

.. note::

   L'interface d'administration ne supporte pas le Responsive Web Design.
   L'accès depuis un navigateur de PC est recommandé.

Principales fonctions d'administration
----------

En vous connectant, vous pouvez accéder aux fonctions de configuration et de gestion suivantes :

**Configuration du crawler**

- Configuration de l'exploration web
- Configuration de l'exploration du système de fichiers
- Configuration de l'exploration du datastore

**Configuration système**

- Configuration générale (fuseau horaire, configuration des e-mails, etc.)
- Gestion des utilisateurs et des rôles
- Configuration du planificateur
- Configuration du design

**Configuration de recherche**

- Gestion des étiquettes
- Ajustement de la pertinence des mots-clés
- Gestion des synonymes et des dictionnaires

Pour les méthodes de gestion détaillées, veuillez consulter le guide de l'utilisateur.

Prochaines étapes
==========

Après avoir compris l'utilisation de base, vous pouvez en apprendre davantage en consultant les documents suivants :

- **Guide de l'utilisateur** : Détails sur la configuration de l'exploration et de la recherche
- **Documentation API** : Intégration de la recherche via l'API REST
- **Guide du développeur** : Développement de personnalisations et de fonctionnalités d'extension

.. |Affichage des résultats de recherche dans le navigateur| image:: ../resources/images/en/fess_search_result.png
