================================
API de l'historique de recherche
================================

Ce document décrit l'API de l'historique de recherche v2 de |Fess|.
Pour l'enveloppe de réponse commune et le modèle d'erreur, voir :doc:`api-overview`.

L'URL de base est ``http://<Server Name>/api/v2/`` (exemple en environnement local : ``http://localhost:8080/api/v2``).

.. note::

   L'historique de recherche est disponible tant que ``search.history.enabled`` (par défaut :
   ``true``) et le journal de recherche sont activés. ``features.search_history`` de
   ``/api/v2/ui/config`` indique l'état.

Obtenir les recherches récentes
===============================

Requête
-------

====================  ====================================================
Méthode HTTP          GET
Point de terminaison  ``/api/v2/search-history``
====================  ====================================================

Renvoie les recherches récentes que l'utilisateur connecté a lancées avec ``/api/v2/search`` sur
l'hôte virtuel courant, de la plus récente à la plus ancienne. Un client peut relancer l'une d'elles
avec les conditions renvoyées.

- Seules les recherches de la première page sont listées. Les recherches aux conditions identiques
  sont fusionnées dans la plus récente, et les recherches sans requête sont omises.
- Au plus ``search.history.size`` (par défaut : ``10``) recherches sont renvoyées.
- Les journaux de recherche sont écrits par un job exécuté chaque minute ; une recherche peut donc
  mettre environ une minute à apparaître.
- L'historique est lié à l'utilisateur connecté de la session. Les appelants anonymes reçoivent
  ``auth_required`` (401) ; un jeton d'accès ne remplace pas une connexion.
- Si l'historique de recherche est désactivé, l'endpoint répond ``invalid_request`` (400).

Il n'y a pas de paramètres de requête.

Réponse
-------

En cas de succès (200), les champs suivants sont renvoyés directement sous ``response`` de l'enveloppe commune.

::

    {
      "response": {
        "status": 0,
        "record_count": 1,
        "data": [
          {
            "q": "fess",
            "fields": { "label": ["docs"] },
            "sort": "last_modified.desc",
            "requested_at": "2026-10-01T09:00:00Z",
            "hit_count": 42
          }
        ]
      }
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Champs de réponse

   * - ``record_count``
     - Nombre de recherches dans ``data`` (int).
   * - ``data``
     - Les recherches récentes, de la plus récente à la plus ancienne. Les clés des conditions sont
       les noms des paramètres de ``/api/v2/search`` ; une clé est omise si la recherche ne l'a pas
       utilisée.
   * - ``data[].q``
     - La requête (str).
   * - ``data[].fields``
     - Conditions de champ données avec ``fields.<name>``, par nom de champ, avec leurs valeurs.
   * - ``data[].ex_q``
     - Requêtes supplémentaires (tableau de str).
   * - ``data[].sort``
     - Ordre de tri (str).
   * - ``data[].lang``
     - Langues demandées avec ``lang`` (tableau de str).
   * - ``data[].requested_at``
     - Date de la recherche (UTC, ISO-8601).
   * - ``data[].hit_count``
     - Nombre de résultats de la recherche (int64).

Tableau : Champs de réponse

Réponses d'erreur
-----------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur

   * - Code de statut
     - Description
   * - 400 Bad Request
     - Lorsque l'historique de recherche est désactivé.
   * - 401 Unauthorized
     - Lorsque l'appelant n'est pas connecté.
   * - 405 Method Not Allowed
     - Lorsque la méthode HTTP n'est pas autorisée.
   * - 500 Internal Server Error
     - Lorsqu'une erreur interne du serveur se produit.

Tableau : Réponses d'erreur

Dans le thème fourni
====================

Dans le thème fourni ``bootstrap``, un utilisateur connecté voit ses recherches récentes dans la liste
de suggestions lorsqu'il clique dans la zone de recherche vide ou y appuie sur la flèche vers le bas.
Choisir une entrée relance la même recherche, conditions comme les étiquettes comprises. Les journaux
de recherche enregistrés avant |Fess| 15.9 ne contiennent pas de conditions et ne sont pas listés.
