=======================
API des mots populaires
=======================

Obtention de la liste des mots populaires
==========================================

Requête
-------

==================  ====================================================
Méthode HTTP        GET
Point de terminaison ``/api/v1/popular-words``
==================  ====================================================

En envoyant une requête à |Fess| de type ``http://<Nom du serveur>/api/v1/popular-words?seed=123``, vous pouvez recevoir la liste des mots populaires enregistrés dans |Fess| au format JSON.
Pour utiliser l'API des mots populaires, vous devez activer la réponse des mots populaires dans les paramètres généraux du système dans l'interface d'administration.

Paramètres de requête
---------------------

Les paramètres de requête disponibles sont les suivants :

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Paramètres de requête

   * - seed
     - Seed pour obtenir les mots populaires (cette valeur permet d'obtenir différents ensembles de mots)
   * - label
     - Nom de l'étiquette filtrée
   * - field
     - Nom du champ pour générer les mots populaires


Réponse
-------

Une réponse comme celle-ci est retournée.

::

    {
      "record_count": 3,
      "data": [
        "python",
        "java",
        "javascript"
      ]
    }

Les éléments sont les suivants :

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Informations de réponse

   * - record_count
     - Nombre de mots populaires enregistrés
   * - data
     - Tableau des mots populaires

Réponse d'erreur
================

Lorsque l'API des mots populaires échoue, une réponse d'erreur comme celle-ci est retournée.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponse d'erreur

   * - Code de statut
     - Description
   * - 400 Bad Request
     - Lorsque les paramètres de requête sont invalides
   * - 500 Internal Server Error
     - Lorsqu'une erreur interne du serveur s'est produite
