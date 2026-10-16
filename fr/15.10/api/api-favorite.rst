==================
API des favoris
==================

Ce document décrit l'API des favoris v2 de |Fess|.
Pour l'enveloppe de réponse commune, le modèle d'erreur et les jetons CSRF, voir :doc:`api-overview`.

L'URL de base est ``http://<Server Name>/api/v2/`` (exemple en environnement local : ``http://localhost:8080/api/v2``).

.. note::

   Pour utiliser la fonctionnalité de favoris, le paramètre ``user.favorite`` doit être activé (désactivé par défaut).

Liste des documents favoris
============================

Requête
-------

====================  ====================================================
Méthode HTTP          GET
Point de terminaison  ``/api/v2/favorites``
====================  ====================================================

Retourne les identifiants des documents que l'utilisateur appelant a préalablement mis en favoris parmi les résultats de recherche identifiés par ``query_id``.
``query_id`` est l'identifiant opaque (champ ``query_id``) retourné par l'API de recherche (``/search``).

Un appelant anonyme (sans code utilisateur associé à la session) recevra ``auth_required`` (401).
Si la fonctionnalité ``user.favorite`` est désactivée, une erreur ``invalid_request`` (400) est retournée.
Si ``query_id`` ne correspond pas à un ensemble de résultats en cache dans la session, une réponse ``200`` avec un tableau ``data`` vide est retournée.

Paramètres de requête
---------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Paramètres de requête

   * - ``query_id``
     - Identifiant opaque ``query_id`` retourné par l'API de recherche (``/search``) (query, obligatoire, str).

Tableau : Paramètres de requête

Réponse
-------

En cas de succès (200), les champs suivants sont retournés directement sous ``response`` dans l'enveloppe commune.

::

    {
      "response": {
        "status": 0,
        "record_count": 2,
        "data": [
          { "doc_id": "a1b2c3d4e5f6" },
          { "doc_id": "f6e5d4c3b2a1" }
        ]
      }
    }

Les détails de chaque champ sont les suivants.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Champs de réponse

   * - ``record_count``
     - Nombre de documents favoris dans ``data`` (int).
   * - ``data``
     - Tableau des documents favoris parmi l'ensemble de résultats de la requête, retournés dans l'ordre des résultats de recherche. Chaque élément est de la forme ``{doc_id}``.

Tableau : Champs de réponse

Réponse d'erreur
~~~~~~~~~~~~~~~~

Pour le détail du modèle d'erreur, voir :doc:`api-overview`. Les statuts HTTP retournés par ce point de terminaison sont les suivants.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur

   * - Code de statut
     - Description
   * - 400 Bad Request
     - La requête est incorrecte (y compris si la fonctionnalité ``user.favorite`` est désactivée).
   * - 401 Unauthorized
     - Authentification requise (appelant anonyme).
   * - 405 Method Not Allowed
     - La méthode HTTP n'est pas autorisée.
   * - 500 Internal Server Error
     - Une erreur interne s'est produite sur le serveur.

Tableau : Réponses d'erreur

Récupération de l'état favori d'un document
============================================

Requête
-------

====================  ====================================================
Méthode HTTP          GET
Point de terminaison  ``/api/v2/documents/{docId}/favorite``
====================  ====================================================

Récupère l'état favori du document spécifié.

Les appelants anonymes (non authentifiés) peuvent également utiliser ce point de terminaison. Dans ce cas, ``favorite`` retourne ``false``, mais ``count`` reflète néanmoins le nombre de favoris enregistré (pour cette raison, ce point de terminaison ne retourne pas ``401``).

Lorsque la fonctionnalité de favoris (``user.favorite``) est désactivée, le point de terminaison répond avec ``invalid_request`` (400).

Paramètres de requête
---------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Paramètres de requête

   * - ``docId``
     - Identifiant du document (path, obligatoire, motif ``^[A-Za-z0-9_-]+$``).

Tableau : Paramètres de requête

Réponse
-------

En cas de succès (200), les champs suivants sont retournés directement sous ``response`` dans l'enveloppe commune.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "favorite": true,
        "count": 5
      }
    }

Les détails de chaque champ sont les suivants.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Champs de réponse

   * - ``doc_id``
     - Identifiant du document (str).
   * - ``favorite``
     - Indique si le document est dans les favoris de l'utilisateur appelant (bool).
   * - ``count``
     - Nombre de fois que ce document a été mis en favori (int64).

Tableau : Champs de réponse

Réponse d'erreur
~~~~~~~~~~~~~~~~

Pour le détail du modèle d'erreur, voir :doc:`api-overview`. Les statuts HTTP retournés par ce point de terminaison sont les suivants.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur

   * - Code de statut
     - Description
   * - 400 Bad Request
     - La requête est incorrecte.
   * - 404 Not Found
     - Ressource introuvable.
   * - 405 Method Not Allowed
     - La méthode HTTP n'est pas autorisée.
   * - 500 Internal Server Error
     - Une erreur interne s'est produite sur le serveur.

Tableau : Réponses d'erreur

Ajout aux favoris
=================

Requête
-------

====================  ====================================================
Méthode HTTP          POST
Point de terminaison  ``/api/v2/documents/{docId}/favorite``
====================  ====================================================

Ajoute le document spécifié aux favoris.
Cette requête modifiant l'état, l'en-tête ``X-Fess-CSRF-Token`` est requis (voir :doc:`api-overview`). De plus, l'utilisateur appelant doit être authentifié ; les appelants anonymes reçoivent ``auth_required`` (401).

Le ``query_id`` est utilisé pour confirmer que le document cible appartient à un résultat de recherche récent. Lorsque ``query_id`` ne correspond à aucun ensemble de résultats mis en cache dans la session, le point de terminaison répond avec ``invalid_request`` (400) ; lorsque ``docId`` n'est pas contenu dans cet ensemble de résultats, il répond avec ``not_found`` (404).

Paramètres de requête
---------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Paramètres de requête

   * - ``docId``
     - Identifiant du document (path, obligatoire, motif ``^[A-Za-z0-9_-]+$``).

Tableau : Paramètres de requête

Corps de la requête
-------------------

Envoyez un JSON (FavoritePostRequest) avec ``Content-Type: application/json`` (charset UTF-8) contenant les champs suivants. La taille maximale du corps de la requête est de 1 Kio (1024 octets) ; la dépasser entraîne une réponse ``payload_too_large`` (413).

::

    {
      "query_id": "f8b1c2d3e4a5"
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Corps de la requête

   * - ``query_id``
     - Identifiant opaque ``query_id`` retourné par l'API de recherche (``/search``) (str, obligatoire).

Tableau : Corps de la requête

Réponse
-------

En cas de succès (200), les champs suivants sont retournés directement sous ``response`` dans l'enveloppe commune.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "ok": true,
        "favorite": true,
        "count": 6
      }
    }

Les détails de chaque champ sont les suivants. L'exemple ci-dessus correspond à un nouvel enregistrement ; si le favori était déjà présent (un re-POST idempotent), la réponse inclut en outre le champ ``already_existed`` (positionné à ``true``).

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Champs de réponse

   * - ``doc_id``
     - Identifiant du document (str).
   * - ``ok``
     - Toujours ``true`` (bool).
   * - ``favorite``
     - Toujours ``true`` (bool). Que ce soit un nouvel ajout ou un doublon, le document est dans les favoris de l'utilisateur appelant.
   * - ``count``
     - Nombre actuel de favoris après l'opération (int64). Pour un nouvel ajout, vaut le comptage avant mise à jour + 1 (optimiste) ; pour un POST idempotent en doublon, reflète le comptage enregistré.
   * - ``already_existed``
     - Vaut ``true`` si le favori existait déjà (bool, POST idempotent en doublon). N'est pas présent lors du premier POST qui ajoute le favori.

Tableau : Champs de réponse

Réponse d'erreur
~~~~~~~~~~~~~~~~

Pour le détail du modèle d'erreur, voir :doc:`api-overview`. Les statuts HTTP retournés par ce point de terminaison sont les suivants.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur

   * - Code de statut
     - Description
   * - 400 Bad Request
     - La requête est incorrecte.
   * - 401 Unauthorized
     - Authentification requise.
   * - 403 Forbidden
     - Non autorisé (jeton CSRF manquant ou expiré, etc.).
   * - 404 Not Found
     - Ressource introuvable.
   * - 405 Method Not Allowed
     - La méthode HTTP n'est pas autorisée.
   * - 413 Payload Too Large
     - Le corps de la requête dépasse la limite de taille.
   * - 415 Unsupported Media Type
     - ``Content-Type`` non pris en charge.
   * - 500 Internal Server Error
     - Une erreur interne s'est produite sur le serveur.

Tableau : Réponses d'erreur
