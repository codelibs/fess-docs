============================
API des documents similaires
============================

Ce document décrit l'API v2 des documents similaires de |Fess|, qui liste les documents ayant le même contenu qu'un document donné. Pour l'enveloppe de réponse commune et le modèle d'erreur, voir :doc:`api-overview`.

L'URL de base est ``http://<Server Name>/api/v2/`` (exemple en environnement local : ``http://localhost:8080/api/v2``).

.. note::

   Cette API trouve les copies et les documents quasi identiques. Elle ne trouve pas les documents qui portent simplement sur le même sujet (voir « Documents renvoyés » ci-dessous).

Lister les documents similaires
===============================

Requête
-------

======================  ====================================================
Méthode HTTP            GET
Point de terminaison    ``/api/v2/documents/{docId}/similar``
======================  ====================================================

Renvoie les documents qui ont la même signature de contenu que le document ``docId``, afin qu'un client puisse proposer un lien « documents similaires » à côté d'un résultat.

- Le même filtre de rôles, le même filtre d'hôte virtuel et la même requête supplémentaire que pour ``/api/v2/search`` s'appliquent au document donné et aux documents renvoyés. Un document inexistant et un document que l'appelant ne peut pas voir renvoient tous deux ``not_found`` (404). Le document donné lui-même, ainsi que tout autre document ayant la même URL, n'est jamais renvoyé.
- Avec ``login.required=true``, un appelant anonyme reçoit ``auth_required`` (401). Un jeton d'accès s'utilise comme pour ``/api/v2/search``.
- Les requêtes sont limitées à ``api.search.similar.rate.limit.per.minute`` (par défaut : ``30`` ; ``0`` signifie illimité) par minute, comptées par utilisateur connecté, ou par IP cliente pour un invité. Au-delà de la limite, le point de terminaison répond ``429`` avec un en-tête ``Retry-After``.
- Une seule page est renvoyée, triée par URL puis par ID de document. Il n'y a ni paramètre ``start`` ni décalage.
- Une requête pour laquelle aucun hôte virtuel n'est déterminé (l'hôte par défaut) ne reçoit pas de filtre d'hôte virtuel ; les documents qui ont une valeur d'hôte virtuel sont donc aussi concernés (comme pour ``/api/v2/search``). Restreignez par rôle les documents que les utilisateurs de l'hôte par défaut ne doivent pas voir.
- Lorsque le contenu d'un document change et qu'il est exploré à nouveau, son ``doc_id`` change. Un ``doc_id`` enregistré peut devenir ``not_found`` (404) après la nouvelle exploration.

Documents renvoyés
------------------

|Fess| calcule une signature de contenu (``content_minhash_bits``) pour chaque document lors de l'indexation. L'API renvoie les documents dont la signature est identique à celle du document donné. C'est le regroupement utilisé par le rapport de doublons (:doc:`../admin/docreport-guide`), le paramètre de recherche ``sdh`` et les champs ``similar_docs_*``, mais il fonctionne sans regroupement des résultats.

- Les documents renvoyés sont des copies ou ont presque le même contenu. Un document dont le contenu a été modifié au point de changer la signature n'est pas renvoyé : ce n'est donc pas une recherche de documents sur un sujet voisin.
- ``data`` est un tableau vide (et non une erreur) lorsque le document donné n'a pas de contenu ou aucun mot, et lorsque le moteur de recherche fonctionne sans les plugins CodeLibs (``search_engine.type`` valant ``vanilla``, ``aws`` ou l'ancien ``cloud`` ; voir :doc:`../config/search-engine-type`).

Paramètres de requête
---------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Paramètres de requête
   :widths: 27 73
   :header-rows: 1

   * - Paramètre
     - Description
   * - ``docId``
     - Identifiant du document (chemin, obligatoire, motif ``[A-Za-z0-9_-]{1,512}``). Une valeur non conforme produit ``invalid_request`` (400).
   * - ``num``
     - Nombre de documents à renvoyer (requête). Les règles sont celles de ``num`` dans :doc:`api-search` : la valeur par défaut est ``10`` (``paging.search.page.size`` n'est pas utilisé). Une valeur supérieure à ``paging.search.page.max.size`` est ramenée à cette limite, et ``page_size`` dans la réponse indique le résultat. Une valeur ``0`` ou négative produit ``invalid_request`` (400). Une valeur qui n'est pas un entier est ignorée et la valeur par défaut est utilisée.

Tableau : Paramètres de requête

Réponse
-------

En cas de succès (200), les champs suivants sont renvoyés directement sous ``response`` dans l'enveloppe commune.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "exec_time": "0.01",
        "query_time": 5,
        "page_size": 10,
        "record_count": 1,
        "record_count_relation": "EQUAL_TO",
        "partial": false,
        "timed_out": false,
        "shard_failed": false,
        "data": [
          {
            "doc_id": "f6e5d4c3b2a1",
            "url": "https://example.com/copy/",
            "title": "Example",
            "content_description": "An example document about Fess."
          }
        ]
      }
    }

Chaque champ est décrit ci-dessous.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Champs de la réponse
   :widths: 27 73
   :header-rows: 1

   * - Champ
     - Description
   * - ``doc_id``
     - ID du document donné.
   * - ``exec_time``
     - Temps d'exécution en secondes (chaîne décimale telle que ``"0.01"``).
   * - ``query_time``
     - Temps de requête du moteur de recherche (int64, millisecondes).
   * - ``page_size``
     - Nombre de documents demandés, après application de la limite décrite plus haut.
   * - ``record_count``
     - Nombre de documents ayant la même signature, et pas seulement ceux de ``data``. Le nombre exact n'est suivi que jusqu'à ``query.track.total.hits`` (par défaut : ``10000``).
   * - ``record_count_relation``
     - Avec ``EQUAL_TO``, le nombre est exact ; avec ``GREATER_THAN_OR_EQUAL_TO``, seule la borne inférieure est connue.
   * - ``partial``
     - Indique si le résultat peut être incomplet (bool). Le délai d'expiration de requête (``query.timeout``) s'applique, comme pour une recherche.
   * - ``timed_out``
     - Indique si le délai d'expiration de requête est écoulé (bool).
   * - ``shard_failed``
     - Indique si un ou plusieurs shards ont échoué (bool).
   * - ``data``
     - Tableau de documents, trié par URL puis par ID de document. Chaque élément a les mêmes champs qu'un résultat de ``/api/v2/search`` (voir :doc:`api-search`), y compris ``tags`` (les tags visibles par l'appelant, voir :doc:`api-tag`). Il n'y a pas de requête à surligner : ``content_description`` est donc le résumé du contenu, et il n'y a pas de ``score``.

Tableau : Champs de la réponse

Réponses d'erreur
-----------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur
   :widths: 25 75
   :header-rows: 1

   * - Code de statut
     - Description
   * - 400 Bad Request
     - ``docId`` ne respecte pas le motif, ou ``num`` vaut ``0`` ou moins.
   * - 401 Unauthorized
     - Une authentification est requise (le paramètre de connexion requise est activé avec un appelant anonyme, ou la requête porte un jeton d'accès non enregistré ou expiré).
   * - 404 Not Found
     - Le document donné n'existe pas ou n'est pas visible par l'appelant (``not_found``).
   * - 405 Method Not Allowed
     - La méthode HTTP n'est pas autorisée.
   * - 429 Too Many Requests
     - La limite de requêtes par minute est dépassée. Un en-tête ``Retry-After`` indique le nombre de secondes à attendre (``60``).
   * - 500 Internal Server Error
     - Une erreur interne du serveur s'est produite.
   * - 503 Service Unavailable
     - Le moteur de recherche n'a pas pu prendre la requête en compte : il est injoignable ou a refusé la requête faute de capacité. ``error.code`` vaut ``service_unavailable`` et un en-tête ``Retry-After`` indique le nombre de secondes à attendre (``5``). La requête elle-même est correcte : réessayez après une courte attente.

Tableau : Réponses d'erreur
