==============
API de cache
==============

Ce document décrit l'API de cache v2 de |Fess|.
Pour l'enveloppe de réponse commune, le modèle d'erreur et les jetons CSRF, voir :doc:`api-overview`.

L'URL de base est ``http://<Server Name>/api/v2/`` (exemple en environnement local : ``http://localhost:8080/api/v2``).

Récupération d'un document en cache
=====================================

Requête
-------

====================  ====================================================
Méthode HTTP          GET
Point de terminaison  ``/api/v2/cache/{docId}``
====================  ====================================================

Retourne le HTML en cache d'un document tel qu'il a été stocké lors de l'exploration. Lorsque ``hq`` est spécifié, les termes correspondants sont mis en évidence.

Ce point de terminaison applique le même filtrage par permissions (rôles) que la recherche. Un document auquel les rôles de l'appelant n'ont pas accès retourne ``not_found`` (404), comme s'il n'existait pas.

Si le paramètre de connexion obligatoire (« Connexion obligatoire » dans les paramètres système) est activé et que l'appelant est anonyme, une erreur ``auth_required`` (401) est retournée.

Paramètres de requête
---------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Paramètres de requête

   * - ``docId``
     - Identifiant du document (path, obligatoire, motif ``^[A-Za-z0-9_-]+$``).
   * - ``hq``
     - Terme à mettre en évidence (query). Lorsqu'il est spécifié, les termes correspondants dans le HTML en cache sont encadrés par des balises de mise en évidence. Peut être répété pour transmettre plusieurs termes (tableau).

Tableau : Paramètres de requête

Réponse
-------

En cas de succès (200), les champs suivants sont retournés directement sous ``response`` dans l'enveloppe commune.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "mimetype": "text/html",
        "content": "<html><body>...</body></html>",
        "url": "https://example.com/",
        "created": "2024-05-31T12:00:00.000Z",
        "charset": "UTF-8"
      }
    }

Les détails de chaque champ sont les suivants.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Champs de réponse

   * - ``doc_id``
     - Identifiant du document (str).
   * - ``mimetype``
     - Type MIME du corps de la réponse (str). Toujours fixé à ``text/html``.
   * - ``content``
     - Corps HTML en cache (str). Lorsque ``hq`` est spécifié, les termes correspondants sont mis en évidence.
   * - ``url``
     - URL du document (str). Retourne la valeur du champ ``url_link`` si elle est présente, sinon la valeur du champ ``url`` de l'index. Omis si aucune des deux n'est disponible.
   * - ``created``
     - Horodatage de création du document (str, format ISO 8601, ex. ``2024-05-31T12:00:00.000Z``). Omis si l'index ne contient pas de valeur.
   * - ``charset``
     - Jeu de caractères extrait du mimetype du document (str). ``UTF-8`` par défaut si absent.

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
     - Authentification requise (paramètre de connexion obligatoire activé avec appelant anonyme).
   * - 404 Not Found
     - Le document n'existe pas, ne possède pas de corps en cache, ou n'est pas accessible avec les permissions de l'appelant.
   * - 405 Method Not Allowed
     - La méthode HTTP n'est pas autorisée.
   * - 500 Internal Server Error
     - Une erreur interne s'est produite sur le serveur.

Tableau : Réponses d'erreur
