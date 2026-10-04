============
API des tags
============

Ce document décrit l'API des tags v2 de |Fess|, avec laquelle les utilisateurs connectés gèrent leurs
propres tags et les posent sur des documents.
Pour l'enveloppe de réponse commune, le modèle d'erreur et les jetons CSRF, voir :doc:`api-overview`.

L'URL de base est ``http://<Server Name>/api/v2/`` (exemple en environnement local : ``http://localhost:8080/api/v2``).

.. note::

   Les tags sont désactivés par défaut. Pour les utiliser, définissez ``user.tag.enabled=true`` dans
   ``fess_config.properties``. ``features.user_tag`` de ``/api/v2/ui/config`` indique l'état. Tant
   que les tags sont désactivés, les endpoints des tags répondent ``invalid_request`` (400) à une
   requête qui passe les contrôles CSRF et Origin et utilise une méthode prise en charge.

Fonctionnement des tags
=======================

- Les tags sont gérés par utilisateur. L'utilisateur qui crée un tag en est le propriétaire, et le
  propriétaire est l'identifiant de connexion. Deux utilisateurs peuvent employer le même nom et avoir
  malgré tout deux tags distincts.
- Seuls les utilisateurs connectés peuvent utiliser les tags. Chaque endpoint agit en tant
  qu'utilisateur de la session de connexion ; un jeton d'accès ne remplace pas une connexion. Un
  appelant non connecté reçoit ``auth_required`` (401).
- Un nouveau tag est privé : seul son propriétaire le voit. Quand le propriétaire partage le tag,
  tout utilisateur connecté peut le voir et filtrer avec. Un utilisateur non connecté ne voit aucun
  tag, partagé ou non.
- Seul le propriétaire peut modifier ou supprimer un tag, ou le poser sur des documents et l'en
  retirer. Un tag partagé d'un autre utilisateur sert uniquement à l'affichage et au filtrage. Les
  administrateurs gèrent tous les tags dans l'écran d'administration (voir
  :doc:`../admin/tagtype-guide`).
- Un tag est posé sur l'URL d'un document : tous les documents indexés ayant cette URL le reçoivent.

Chaque tag a deux identifiants.

``value``
    La valeur du tag, ``base64url(nom):base64url(propriétaire)`` (UTF-8, sans remplissage), stockée
    dans le champ ``tag`` de l'index. Traitez-la comme une valeur opaque servant à filtrer les
    résultats de recherche.

``id``
    L'identifiant du tag, le SHA-256 de ``value`` en hexadécimal minuscule (64 caractères). Il
    s'indique dans des chemins comme ``/api/v2/tags/{tagId}``. Renommer un tag change à la fois
    ``value`` et ``id``.

Le nom d'un tag est normalisé en NFKC, les suites d'espaces sont réduites à une seule et les
extrémités sont rognées. Le résultat doit compter de 1 à ``user.tag.name.max.length`` (par défaut :
``50``) caractères, et les noms contenant un caractère de contrôle ou de format (comme un caractère
de largeur nulle ou un forçage bidirectionnel) sont refusés.

Les tags dans la recherche
==========================

Tant que ``user.tag.enabled`` vaut ``true``, l'API de recherche (``/api/v2/search``) traite les tags
comme suit.

- Chaque résultat porte dans ``tags`` les tags que l'appelant peut voir. Chaque entrée a ``value``,
  ``name``, ``owner``, ``mine`` (``true`` lorsque l'appelant est le propriétaire) et ``shared``
  (``true`` pour un tag partagé). ``tags`` est absent s'il n'y en a aucun. Le champ d'index ``tag``
  lui-même n'est jamais renvoyé.
- ``facet.field=tag`` renvoie dans ``facet_field`` une facette des tags que l'appelant peut voir.
  Outre ``value`` et ``count``, chaque compartiment a ``label`` (le nom du tag), ``owner``, ``mine``
  et ``shared``.
- ``fields.tag=<valeur>`` restreint les résultats aux documents portant un tag. Passez tel quel le
  ``value`` des ``tags`` d'un résultat ou d'un compartiment de la facette.

Une condition sur les tags (``fields.tag``, ``tag:``, ``ex_q``, ``facet.query``) ne correspond qu'à
la valeur exacte d'un tag que l'appelant peut voir. La valeur d'un tag qu'il ne peut pas voir, ainsi
que les conditions avec joker, par préfixe, approximatives et par plage, ne correspondent à rien. Un
appelant non connecté ne reçoit ni tags ni facette de tags, et une condition sur les tags ne
correspond à rien.

Un utilisateur voit au plus ``user.tag.visible.max.size`` (par défaut : ``1000``) tags, les siens en
premier. Au-delà, les tags n'apparaissent ni dans ``tags`` des résultats ni dans la facette, mais
peuvent toujours servir au filtrage.

Quand les documents reflètent les modifications
===============================================

La création, la modification et la suppression des tags, ainsi que leur pose et leur retrait sur
les documents, apparaissent immédiatement dans les endpoints des tags. Le champ ``tag`` des documents
indexés, en revanche, est mis à jour via une file d'attente en mémoire que la tâche « Log Aggregator »
(``log_aggregator``) applique en bloc chaque minute. Les résultats, la facette et les filtres
reflètent donc une modification au bout d'une minute environ au plus. Après un renommage, les
documents gardent l'ancienne valeur jusqu'au prochain traitement de la file, et le tag n'y est pas
affiché entre-temps.

Pour la file d'attente et les tâches, voir :doc:`../admin/tagtype-guide`.

Lister les tags
===============

Requête
-------

====================  ====================================================
Méthode HTTP          GET
Point de terminaison  ``/api/v2/tags``
====================  ====================================================

Renvoie les tags de l'appelant, par ordre de tri et par nom. Les tags partagés des autres utilisateurs
ne sont pas inclus.

Réponse
-------

En cas de succès (200), les champs suivants sont renvoyés directement sous ``response`` de l'enveloppe commune.

::

    {
      "response": {
        "status": 0,
        "tags": [
          {
            "id": "54788d242d35bdc53a2573eb7485b1d79c6c82a024c716ef6e27fc22064fb084",
            "value": "YS1yZWxpcmU:Y2xhaXJl",
            "name": "a-relire",
            "shared": false,
            "sort_order": 0,
            "path_count": 3
          }
        ]
      }
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Champs de réponse

   * - ``tags``
     - Les tags de l'appelant. Chacun a ``id``, ``value``, ``name``, ``shared`` (``true`` pour un
       tag partagé), ``sort_order`` et ``path_count`` (le nombre d'URL portant le tag).

Tableau : Champs de réponse

Créer un tag
============

Requête
-------

====================  ====================================================
Méthode HTTP          POST
Point de terminaison  ``/api/v2/tags``
====================  ====================================================

Crée un tag de l'appelant. Comme requête qui modifie l'état, elle exige l'en-tête
``X-Fess-CSRF-Token`` (voir :doc:`api-overview`).

- Un utilisateur peut avoir au plus ``user.tag.max.tags`` (par défaut : ``1000``) tags. Au-delà,
  l'endpoint répond ``invalid_request`` (400).
- Si l'appelant a déjà un tag de ce nom, l'endpoint répond ``conflict`` (409). Qu'un autre
  utilisateur ait un tag de même nom n'a pas d'importance.

Envoyez ``Content-Type: application/json`` ; le corps fait au plus 1 Kio (1024 octets).

::

    {
      "name": "a-relire",
      "shared": false
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Corps de la requête

   * - ``name``
     - Nom du tag (str, obligatoire).
   * - ``shared``
     - ``true`` rend le tag visible par tout utilisateur connecté (bool, par défaut : ``false``).

Tableau : Corps de la requête

Réponse
-------

En cas de succès (200), ``tag`` directement sous ``response`` contient le nouveau tag, sous la forme
d'une entrée de ``GET /api/v2/tags`` avec un ``path_count`` de ``0``.

Modifier un tag
===============

Requête
-------

====================  ====================================================
Méthode HTTP          PUT
Point de terminaison  ``/api/v2/tags/{tagId}``
====================  ====================================================

Renomme un tag de l'appelant ou change son partage. L'en-tête ``X-Fess-CSRF-Token`` est requis.

- Le corps contient ``name``, ``shared`` ou les deux.
- Un nouveau ``name`` renomme le tag, ce qui lui donne un nouvel ``id`` et une nouvelle ``value``.
  Les documents portant l'ancienne valeur reçoivent la nouvelle au prochain traitement de la file.
  Renommer vers un nom que l'appelant utilise déjà répond ``conflict`` (409) et laisse le tag
  inchangé.
- ``shared`` change seulement qui voit le tag ; aucun document n'est mis à jour. Passer ``shared`` à
  ``false`` conserve les rôles et groupes qu'un administrateur a ajoutés aux permissions.
- Un tag partagé d'un autre utilisateur répond ``forbidden`` (403), et un tag que l'appelant ne peut
  pas voir ``not_found`` (404).
- Une écriture qui perd plusieurs fois face à une autre mise à jour répond aussi ``conflict`` (409).

::

    {
      "name": "relu",
      "shared": true
    }

En cas de succès (200), ``response`` contient ``tag`` (le tag modifié) et ``renamed`` (``true`` si le
tag a été renommé, auquel cas ``tag.id`` et ``tag.value`` sont nouveaux).

Supprimer un tag
================

Requête
-------

====================  ====================================================
Méthode HTTP          DELETE
Point de terminaison  ``/api/v2/tags/{tagId}``
====================  ====================================================

Supprime un tag de l'appelant. Les documents perdent sa valeur au prochain traitement de la file.
L'en-tête ``X-Fess-CSRF-Token`` est requis. Un tag partagé d'un autre utilisateur répond
``forbidden`` (403), et un tag que l'appelant ne peut pas voir ``not_found`` (404).

En cas de succès (200), ``response`` contient ``id`` (l'identifiant du tag supprimé) et ``deleted``
(toujours ``true``).

Obtenir les tags d'un document
==============================

Requête
-------

====================  ====================================================
Méthode HTTP          GET
Point de terminaison  ``/api/v2/documents/{docId}/tags``
====================  ====================================================

Renvoie les tags posés sur l'URL du document que l'appelant peut voir, ainsi que les tags de
l'appelant qui n'y sont pas encore posés. Le document est recherché avec les rôles de l'appelant :
un document qu'il ne peut pas rechercher répond ``not_found`` (404).

Réponse
-------

En cas de succès (200), les champs suivants sont renvoyés directement sous ``response`` de l'enveloppe commune.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "tags": [
          {
            "id": "54788d242d35bdc53a2573eb7485b1d79c6c82a024c716ef6e27fc22064fb084",
            "value": "YS1yZWxpcmU:Y2xhaXJl",
            "name": "a-relire",
            "owner": "claire",
            "mine": true,
            "shared": false
          },
          {
            "id": "41e429a7d0081e25390c3840268d736dca00250167bab94250389aee9e08e2ed",
            "value": "c3BlY3M:Ym9i",
            "name": "specs",
            "owner": "bob",
            "mine": false,
            "shared": true
          }
        ],
        "addable": []
      }
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Champs de réponse

   * - ``doc_id``
     - ID du document (str).
   * - ``tags``
     - Les tags posés sur l'URL du document que l'appelant peut voir. Chacun a ``id``, ``value``,
       ``name``, ``owner``, ``mine`` (``true`` lorsque l'appelant est le propriétaire) et ``shared``
       (``true`` pour un tag partagé).
   * - ``addable``
     - Les tags de l'appelant qui ne sont pas posés sur l'URL du document, sous la même forme que
       ``tags``.
   * - ``added``
     - POST uniquement. ``false`` lorsque le tag était déjà posé sur le document (bool).
   * - ``tag``
     - POST uniquement. Le tag posé sur le document, sous la même forme que ``tags``.
   * - ``removed``
     - DELETE uniquement. ``false`` lorsque le tag n'était pas posé sur le document (bool).

Tableau : Champs de réponse

Poser un tag sur un document
============================

Requête
-------

====================  ====================================================
Méthode HTTP          POST
Point de terminaison  ``/api/v2/documents/{docId}/tags``
====================  ====================================================

Ajoute l'URL du document à un tag de l'appelant. L'en-tête ``X-Fess-CSRF-Token`` est requis.

Le corps (``Content-Type: application/json``, 1 Kio au plus) indique soit ``id``, un tag existant,
soit ``name``, un nom de tag. Si les deux sont indiqués, ``id`` l'emporte.

::

    {
      "name": "a-relire"
    }

- Avec ``name``, si l'appelant n'a aucun tag de ce nom, un tag privé est créé et posé. Le nouveau tag
  compte dans ``user.tag.max.tags``.
- Un tag peut être posé sur au plus ``user.tag.max.paths`` (par défaut : ``10000``) URL. Au-delà,
  l'endpoint répond ``invalid_request`` (400).
- L'``id`` d'un tag d'un autre utilisateur répond ``forbidden`` (403) si l'appelant peut voir le tag,
  et ``not_found`` (404) sinon.
- En cas de succès, la réponse contient les champs de « Obtenir les tags d'un document » plus
  ``added`` et ``tag``. Les endpoints des tags montrent le tag immédiatement ; les résultats de
  recherche des documents ayant cette URL le reflètent au prochain traitement de la file (environ une
  minute plus tard).

Retirer un tag d'un document
============================

Requête
-------

====================  ====================================================
Méthode HTTP          DELETE
Point de terminaison  ``/api/v2/documents/{docId}/tags/{tagId}``
====================  ====================================================

Retire l'URL du document du tag de l'appelant indiqué par ``tagId``. L'en-tête ``X-Fess-CSRF-Token``
est requis. Un tag d'un autre utilisateur répond ``forbidden`` (403) si l'appelant peut le voir, et
``not_found`` (404) sinon. En cas de succès, la réponse contient les champs de « Obtenir les tags
d'un document » plus ``removed``.

Réponses d'erreur
=================

Pour le détail du modèle d'erreur, voir :doc:`api-overview`. Les endpoints des tags renvoient les
statuts HTTP suivants.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur

   * - Code de statut
     - Description
   * - 400 Bad Request
     - Lorsque la requête est invalide, y compris lorsque les tags sont désactivés, que le nom est
       invalide, qu'un champ obligatoire manque ou que ``user.tag.max.tags`` ou
       ``user.tag.max.paths`` serait dépassé.
   * - 401 Unauthorized
     - Sans connexion (un jeton d'accès ne la remplace pas).
   * - 403 Forbidden
     - Un jeton CSRF absent ou expiré, ou une modification du tag d'un autre utilisateur. Le contrôle
       CSRF précède celui de la connexion : une requête qui modifie l'état sans session reçoit 403 et
       non 401.
   * - 404 Not Found
     - Lorsque le tag n'existe pas ou que l'appelant ne peut pas le voir, ou que le document est
       introuvable ou que l'appelant ne peut pas le rechercher.
   * - 405 Method Not Allowed
     - Lorsque la méthode HTTP n'est pas autorisée.
   * - 409 Conflict
     - Lorsqu'un tag de ce nom existe déjà, ou qu'une écriture a perdu face à une autre mise à jour.
   * - 413 Payload Too Large
     - Lorsque le corps de la requête dépasse la taille maximale (1 Kio).
   * - 415 Unsupported Media Type
     - Lorsque le ``Content-Type`` n'est pas pris en charge.
   * - 500 Internal Server Error
     - Lorsqu'une erreur interne du serveur se produit.

Tableau : Réponses d'erreur

Paramètres
==========

Les paramètres suivants de ``fess_config.properties`` règlent les tags.

.. list-table::
   :header-rows: 1
   :widths: 35 50 15

   * - Propriété
     - Description
     - Par défaut
   * - ``user.tag.enabled``
     - Indique si les utilisateurs connectés peuvent utiliser les tags.
     - ``false``
   * - ``user.tag.name.max.length``
     - Longueur maximale d'un nom de tag, en points de code.
     - ``50``
   * - ``user.tag.max.tags``
     - Nombre maximal de tags qu'un utilisateur peut posséder.
     - ``1000``
   * - ``user.tag.max.paths``
     - Nombre maximal d'URL sur lesquelles un tag peut être posé.
     - ``10000``
   * - ``user.tag.queue.max.size``
     - Nombre maximal de modifications gardées en mémoire jusqu'à ce qu'elles atteignent les
       documents. Une modification au-delà est abandonnée avec un journal WARN.
     - ``10000``
   * - ``user.tag.process.batch.size``
     - Nombre d'URL mises à jour par requête en bloc lors de l'application des modifications aux
       documents.
     - ``100``
   * - ``user.tag.visible.max.size``
     - Nombre maximal de tags visibles par un utilisateur dans une recherche.
     - ``1000``
