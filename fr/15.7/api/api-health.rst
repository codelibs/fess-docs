===========
API Health
===========

Obtention de l'état
===================

Requête
-------

==================  ====================================================
Méthode HTTP        GET
Point de terminaison ``/api/v1/health``
==================  ====================================================

En envoyant une requête à |Fess| de type ``http://<Nom du serveur>/api/v1/health``, vous pouvez recevoir l'état du serveur |Fess| au format JSON.

Paramètres de requête
---------------------

Aucun paramètre de requête ne peut être spécifié.

Réponse
-------

Une réponse comme celle-ci est retournée.

::

    {
      "data": {
        "status": "green",
        "timed_out": false
      }
    }

Les éléments sont les suivants :

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Informations de réponse

   * - data
     - Élément parent des résultats de recherche.
   * - status
     - État du système. ``green`` est retourné en cas de fonctionnement normal, ``yellow`` en cas d'avertissement, et ``red`` en cas d'erreur.
   * - timed_out
     - Présence ou non d'un timeout. ``false`` est retourné si la réponse est retournée dans le délai spécifié, ``true`` en cas de timeout.

Réponse d'erreur
================

Lorsque l'API Health échoue, une réponse d'erreur comme celle-ci est retournée.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponse d'erreur

   * - Code de statut
     - Description
   * - 500 Internal Server Error
     - Lorsqu'une erreur interne du serveur s'est produite
