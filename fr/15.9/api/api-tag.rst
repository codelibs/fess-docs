============
API des tags
============

Ce document décrit l'API des tags v2 de |Fess|, qui permet aux utilisateurs de taguer des documents.
Pour l'enveloppe de réponse commune, le modèle d'erreur et les jetons CSRF, voir :doc:`api-overview`.

L'URL de base est ``http://<Server Name>/api/v2/`` (exemple en environnement local : ``http://localhost:8080/api/v2``).

.. note::

   Les tags sont désactivés par défaut. Pour les utiliser, définissez ``user.tag.enabled=true`` dans
   ``fess_config.properties``. ``features.user_tag`` de ``/api/v2/ui/config`` indique l'état.

Un tag est une étiquette du type « Tag » (voir :doc:`../admin/labeltype-guide`) : le nom de
l'étiquette est le nom du tag, la valeur est le SHA-256 du nom en hexadécimal, les chemins inclus sont
les URL taguées et les permissions décident qui peut voir le tag. Un tag n'est visible que si son
étiquette est visible pour l'appelant.

L'API de recherche (``/api/v2/search``) renvoie dans ``tags`` les tags de chaque résultat que
l'appelant peut voir. ``fields.tag=<valeur>`` restreint les résultats aux documents portant un tag,
et ``facet.field=tag`` renvoie une facette de tags. Le champ d'index ``tag`` lui-même n'est pas
renvoyé.

Obtenir les tags
================

Requête
-------

====================  ====================================================
Méthode HTTP          GET
Point de terminaison  ``/api/v2/documents/{docId}/tags``
====================  ====================================================

Renvoie les tags du document que l'appelant peut voir. Si l'appelant ne peut pas rechercher le
document, l'endpoint répond ``not_found`` (404).

Réponse
-------

En cas de succès (200), les champs suivants sont renvoyés directement sous ``response`` de l'enveloppe commune.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "addable": true,
        "tags": [
          { "value": "9f86d081884c7d65...", "name": "a-relire", "mine": true }
        ]
      }
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Champs de réponse

   * - ``doc_id``
     - ID du document (str).
   * - ``addable``
     - ``true`` lorsque l'appelant est connecté et peut ajouter des tags (bool).
   * - ``added``
     - POST uniquement. ``false`` lorsque l'appelant avait déjà tagué le document (bool).
   * - ``removed``
     - DELETE uniquement (bool).
   * - ``tags``
     - Les tags que l'appelant peut voir. Chacun a ``value`` (la valeur de l'étiquette, utilisée avec
       ``fields.tag``), ``name`` (le nom du tag) et ``mine`` (``true`` lorsque l'appelant figure dans
       les permissions du tag).

Tableau : Champs de réponse

Ajouter un tag
==============

Requête
-------

====================  ====================================================
Méthode HTTP          POST
Point de terminaison  ``/api/v2/documents/{docId}/tags``
====================  ====================================================

Tague l'URL du document pour l'utilisateur connecté ; un jeton d'accès ne remplace pas une connexion.
Comme requête qui modifie l'état, elle exige l'en-tête ``X-Fess-CSRF-Token``.

- Si un tag de ce nom existe, l'URL est ajoutée à ses chemins inclus et l'utilisateur à ses
  permissions. Sinon, un tag visible par ce seul utilisateur est créé. Les tags de même nom
  fusionnent donc en un seul, et les utilisateurs qui ont ajouté un tag de même nom voient où se
  trouvent les tags des autres.
- Taguer à nouveau le même document renvoie ``added: false``.
- Un document peut avoir au plus ``user.tag.max.document.tags`` (par défaut : ``100``) tags.

Envoyez ``Content-Type: application/json`` avec le nom du tag dans ``name``.

::

    {
      "name": "a-relire"
    }

Le nom est normalisé en NFKC, les suites d'espaces sont réduites et il est rogné. Il doit compter de
1 à ``user.tag.name.max.length`` (par défaut : ``50``) caractères, et les noms contenant un caractère
de contrôle ou de format (comme un caractère de largeur nulle ou un forçage bidirectionnel) sont
refusés.

Retirer un tag
==============

Requête
-------

====================  ====================================================
Méthode HTTP          DELETE
Point de terminaison  ``/api/v2/documents/{docId}/tags?value=<valeur>``
====================  ====================================================

Retire l'utilisateur connecté des permissions du tag indiqué par ``value``. Lorsqu'il ne reste aucune
permission d'utilisateur, de groupe ou de rôle, le tag est supprimé et retiré des documents. Si
l'utilisateur ne figure pas dans les permissions du tag, l'endpoint répond ``forbidden`` (403).
L'en-tête ``X-Fess-CSRF-Token`` est requis.

Réponses d'erreur
=================

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur

   * - Code de statut
     - Description
   * - 400 Bad Request
     - Lorsque la requête est invalide (y compris lorsque les tags sont désactivés, que le nom est
       invalide ou qu'une limite est dépassée).
   * - 401 Unauthorized
     - POST ou DELETE sans connexion.
   * - 403 Forbidden
     - Un jeton CSRF absent ou expiré, ou un DELETE d'un tag que l'utilisateur n'a pas ajouté.
   * - 404 Not Found
     - Lorsque le document est introuvable ou que l'appelant ne peut pas le rechercher.
   * - 405 Method Not Allowed
     - Lorsque la méthode HTTP n'est pas autorisée.
   * - 413 Payload Too Large
     - Lorsque le corps de la requête dépasse la taille maximale.
   * - 415 Unsupported Media Type
     - Lorsque le ``Content-Type`` n'est pas pris en charge.
   * - 500 Internal Server Error
     - Lorsqu'une erreur interne du serveur se produit.

Tableau : Réponses d'erreur
