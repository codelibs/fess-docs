============
Vue d'ensemble de l'API
============


API fournies par |Fess|
========================

Ce document décrit les API fournies par |Fess|.
En utilisant les API, vous pouvez intégrer |Fess| comme serveur de recherche dans vos systèmes Web existants.

URL de base
===========

Les points de terminaison de l'API de |Fess| sont fournis avec l'URL de base suivante :

::

    http://<Nom du serveur>/api/v1/

Par exemple, si l'application s'exécute dans un environnement local, l'URL sera :

::

    http://localhost:8080/api/v1/

Authentification
================

Dans la version actuelle, aucune authentification n'est requise pour utiliser les API.
Cependant, vous devez activer les API dans les différents paramètres de l'interface d'administration.

Méthode HTTP
============

Tous les points de terminaison de l'API sont accessibles via la méthode **GET**.

Format de réponse
=================

Toutes les réponses de l'API sont retournées au **format JSON** (à l'exception de l'API compatible GSA).
Le ``Content-Type`` de la réponse est ``application/json``.

Gestion des erreurs
===================

Lorsqu'une requête API échoue, un code de statut HTTP approprié est retourné avec les informations d'erreur.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Codes de statut HTTP

   * - 200
     - La requête a été traitée avec succès.
   * - 400
     - Les paramètres de la requête sont invalides.
   * - 404
     - La ressource demandée n'a pas été trouvée.
   * - 500
     - Une erreur interne du serveur s'est produite.

Tableau : Codes de statut HTTP

Types d'API
===========

|Fess| fournit les API suivantes :

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - search
     - API pour obtenir les résultats de recherche.
   * - popularword
     - API pour obtenir les mots populaires.
   * - label
     - API pour obtenir la liste des étiquettes créées.
   * - health
     - API pour obtenir l'état du serveur.
   * - suggest
     - API pour obtenir les suggestions de mots.

Tableau : Types d'API
