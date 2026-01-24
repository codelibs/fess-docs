==================
API de suggestions
==================

Obtention de la liste des suggestions de mots
==============================================

Requête
-------

==================  ====================================================
Méthode HTTP        GET
Point de terminaison ``/api/v1/suggest-words``
==================  ====================================================

En envoyant une requête à |Fess| de type ``http://<Nom du serveur>/api/v1/suggest-words?q=mot_suggestion``, vous pouvez recevoir la liste des suggestions de mots enregistrées dans |Fess| au format JSON.
Pour utiliser l'API de suggestions de mots, vous devez activer « Suggérer à partir des documents » ou « Suggérer à partir des mots de recherche » dans les paramètres généraux du système dans l'interface d'administration.

Paramètres de requête
---------------------

Les paramètres de requête disponibles sont les suivants :

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Paramètres de requête

   * - q
     - Mot-clé pour la suggestion. (Exemple) ``q=fess``
   * - num
     - Nombre de mots suggérés. Par défaut 10. (Exemple) ``num=20``
   * - label
     - Nom de l'étiquette filtrée. (Exemple) ``label=java``
   * - fields
     - Nom du champ pour affiner les cibles de suggestion. Par défaut, pas de filtrage. (Exemple) ``fields=content,title``
   * - lang
     - Spécification de la langue de recherche. (Exemple) ``lang=en``


Réponse
-------

Une réponse comme celle-ci est retournée.

::

    {
      "query_time": 18,
      "record_count": 355,
      "page_size": 10,
      "data": [
        {
          "text": "fess",
          "labels": [
            "java",
            "python"
          ]
        }
      ]
    }

Les éléments sont les suivants :

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Informations de réponse

   * - query_time
     - Temps de traitement de la requête (en millisecondes).
   * - record_count
     - Nombre de suggestions de mots enregistrées.
   * - page_size
     - Taille de page.
   * - data
     - Élément parent des résultats de recherche.
   * - text
     - Suggestion de mot.
   * - labels
     - Tableau des valeurs d'étiquettes.

Réponse d'erreur
================

Lorsque l'API de suggestions échoue, une réponse d'erreur comme celle-ci est retournée.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponse d'erreur

   * - Code de statut
     - Description
   * - 400 Bad Request
     - Lorsque les paramètres de requête sont invalides
   * - 500 Internal Server Error
     - Lorsqu'une erreur interne du serveur s'est produite
