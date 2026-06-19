=====================
API des clics
=====================

Ce document décrit l'API des journaux de clics v2 de |Fess|.
Pour l'enveloppe de réponse commune, le modèle d'erreur et les jetons CSRF, voir :doc:`api-overview`.

L'URL de base est ``http://<Server Name>/api/v2/`` (exemple en environnement local : ``http://localhost:8080/api/v2``).

Enregistrement d'un clic
=========================

Requête
-------

====================  ====================================================
Méthode HTTP          POST
Point de terminaison  ``/api/v2/click``
====================  ====================================================

Enregistre un clic sur un résultat de recherche dans le journal de recherche.
Pour les appelants anonymes et les installations où la fonctionnalité de journal de recherche est désactivée, la réponse de succès retourne ``logged: false`` (aucune erreur n'est générée).

Cette requête modifiant l'état, l'en-tête ``X-Fess-CSRF-Token`` est requis (voir :doc:`api-overview`).

Corps de la requête
-------------------

Envoyez un JSON (ClickRequest) avec ``Content-Type: application/json`` contenant les champs suivants.

::

    {
      "doc_id": "a1b2c3d4e5f6",
      "query_id": "f8b1c2d3e4a5",
      "rank": 1,
      "rt": 1717142400000
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Corps de la requête

   * - ``doc_id``
     - Identifiant du document (str, obligatoire, motif ``^[A-Za-z0-9_-]+$``). Identifie le document dont le clic est enregistré.
   * - ``query_id``
     - Le ``query_id`` retourné par l'API de recherche (``/search``) (str, facultatif). Associe le clic à la requête de recherche d'origine.
   * - ``rank``
     - Position dans la liste de résultats (à base 1, int, facultatif).
   * - ``rt``
     - Epoch en millisecondes de la requête de recherche d'origine (int64, facultatif). Si non spécifié, l'heure courante du serveur est utilisée par défaut.

Tableau : Corps de la requête

Réponse
-------

En cas de succès (200), les champs suivants sont retournés directement sous ``response`` dans l'enveloppe commune.

::

    {
      "response": {
        "status": 0,
        "ok": true,
        "logged": true
      }
    }

Les détails de chaque champ sont les suivants.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Champs de réponse

   * - ``ok``
     - Toujours ``true`` (bool).
   * - ``logged``
     - Vaut ``false`` si la persistance du journal de recherche est désactivée ou si l'appelant est anonyme (bool). Une réponse ``200`` est malgré tout retournée dans ce cas.

Tableau : Champs de réponse

.. note::

   ``logged: true`` indique que le clic a été accepté dans la file d'attente du journal de recherche. La persistance est effectuée de manière asynchrone.

Réponse d'erreur
~~~~~~~~~~~~~~~~

Pour le détail du modèle d'erreur, voir :doc:`api-overview`. Les statuts HTTP retournés par ce point de terminaison sont les suivants.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur

   * - Code de statut
     - Description
   * - 400 Bad Request
     - Le corps de la requête n'est pas un JSON valide, ou ``doc_id`` est absent ou ne correspond pas au motif.
   * - 403 Forbidden
     - Non autorisé (jeton CSRF manquant ou expiré, etc.).
   * - 404 Not Found
     - Aucun document correspondant au ``doc_id`` spécifié n'a été trouvé.
   * - 405 Method Not Allowed
     - Une méthode HTTP autre que ``POST`` a été utilisée (un en-tête ``Allow: POST`` est retourné).
   * - 413 Payload Too Large
     - Le corps de la requête dépasse la limite de taille (2 Kio).
   * - 415 Unsupported Media Type
     - Le ``Content-Type`` n'est pas ``application/json`` (UTF-8 est requis).
   * - 500 Internal Server Error
     - Une erreur interne s'est produite sur le serveur.

Tableau : Réponses d'erreur
