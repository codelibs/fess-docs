===================================================
Intégrer l'API de recherche aux applications métier
===================================================

Introduction
============

Afficher les documents liés sur la fiche client de votre CRM, proposer d'abord des FAQ similaires sur l'écran de saisie d'une demande, rendre consultables les rapports produits par votre propre système : autant de besoins courants.
Vous pouvez y répondre en appelant l'API de recherche de Fess (``/api/v2``) depuis le serveur de votre application métier.

Dans cet article, nous suivons les étapes ci-dessous avec Fess 15.9.

- Appeler avec curl les API de recherche, d'étiquettes, de suggestions et de mots populaires, et examiner la forme des réponses
- Créer un jeton d'accès et contrôler les documents renvoyés grâce aux rôles du jeton
- Écrire une fonction qui appelle l'API de recherche côté serveur de l'application métier
- Enregistrer avec ``PUT /api/admin/documents/bulk`` des données impossibles à explorer
- Se préparer aux erreurs et aux limitations de débit

L'intégration d'une zone ou d'une page de recherche dans un site web existant (intégration côté navigateur, thèmes, Fess Site Search) est traitée dans :doc:`guide-03`.
Si vous n'avez pas encore démarré Fess ni lancé d'exploration, commencez par :doc:`guide-02`.

L'architecture mise en place
============================

::

    [Navigateur de l'utilisateur] --> [Serveur de l'application métier] --(avec jeton)--> [Fess /api/v2]
                                            Le jeton reste ici uniquement

Le navigateur n'accède qu'à l'application métier ; c'est le serveur de l'application métier qui appelle Fess.
Conservez le jeton d'accès dans une variable d'environnement du serveur ou à un endroit similaire, et ne le transmettez jamais au navigateur.
Les raisons sont expliquées dans « Créer un jeton d'accès ».

Vue d'ensemble des API
======================

Les API de recherche fournies par Fess 15.9 lui-même se trouvent sous ``/api/v2``.
Celles que nous utilisons dans cet article sont les suivantes.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Point de terminaison
     - Usage
   * - ``GET /api/v2/search``
     - Recherche plein texte. Les résultats se trouvent dans ``response.data``
   * - ``GET /api/v2/labels``
     - Liste des étiquettes utilisables par l'appelant
   * - ``GET /api/v2/suggest-words``
     - Suggestions pour un mot en cours de saisie
   * - ``GET /api/v2/popular-words``
     - Mots populaires
   * - ``GET /api/v2/health``
     - État du moteur de recherche (pour la supervision, voir :doc:`guide-10`)
   * - ``PUT /api/admin/documents/bulk``
     - Enregistrement de documents en masse (API Admin)

Toutes les réponses de ``/api/v2`` sont enveloppées dans ``{"response": {...}}`` ; l'appel a réussi si ``response.status`` vaut 0.
Les clés JSON sont en ``snake_case``.

.. note::

   Fess 15.9 lui-même ne fournit pas ``/api/v1``.
   Pour continuer à faire fonctionner des clients existants qui appellent ``/api/v1``, le plugin ``fess-webapp-v1-api`` est nécessaire (il n'est pas inclus dans l'image Docker).
   Utilisez ``/api/v2`` pour toute nouvelle intégration.

Premiers essais avec curl
=========================

Si la recherche anonyme est autorisée (« Connexion requise » est désactivé dans [Système] > [Général], ce qui est le réglage par défaut), vous pouvez appeler l'API sans jeton.
Les termes de recherche contenant des espaces ou des caractères non ASCII sont encodés pour l'URL et envoyés avec ``-G --data-urlencode``.
Nous utilisons ``jq`` pour rendre la sortie plus lisible.

::

    $ curl -s -G "http://localhost:8080/api/v2/search" \
        --data-urlencode "q=guide recherche" \
        --data-urlencode "num=3" \
      | jq '.response | {status, record_count, page_size, data: [.data[] | {doc_id, title, url_link, content_description}]}'

La réponse a la forme suivante (seul le premier élément de ``data`` est montré ; les valeurs dépendent de votre environnement).

.. code-block:: json

    {
      "status": 0,
      "record_count": 12,
      "page_size": 3,
      "data": [
        {
          "doc_id": "5d4c0e0e5a7b4b5c9d2f6a1b3c8e7f90",
          "title": "Guide de recherche",
          "url_link": "https://fess.codelibs.org/fr/stable/user/index.html",
          "content_description": "Le <strong>guide</strong> de <strong>recherche</strong> de Fess. ..."
        }
      ]
    }

``response`` contient également ``page_count``, ``next_page``, ``exec_time``, ``query_id``, etc.
Chaque élément de ``data`` ne contient que les champs autorisés pour les réponses de l'API, comme ``title``, ``url``, ``url_link``, ``content_description``, ``last_modified``, ``filetype`` et ``score``.
Le texte complet (``content``) et les étiquettes (``label``) ne sont pas renvoyés par défaut.
Pour renvoyer davantage de champs, ajoutez-les à ``query.additional.api.response.fields`` dans ``fess_config.properties``.
``content_description`` est un extrait dans lequel les termes de recherche sont entourés de balises ``<strong>`` : à l'affichage, traitez-le comme du HTML ou supprimez les balises.

Les paramètres les plus utilisés sont les suivants.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Paramètre
     - Signification
   * - ``q``
     - Termes de recherche. La syntaxe est la même que sur la page de recherche (AND, OR, exclusion, recherche par champ, etc.)
   * - ``num`` / ``start``
     - Nombre de résultats par page (10 par défaut ; une valeur supérieure à la limite est ramenée à la limite) et position de départ (à partir de 0)
   * - ``sort``
     - Ordre de tri. Exemple : ``last_modified.desc`` (les plus récemment mis à jour d'abord)
   * - ``fields.label``
     - Filtre sur la valeur d'étiquette. Peut être indiqué plusieurs fois

Pour les autres paramètres (facettes, langue, recherche géographique, etc.), consultez `API de recherche <https://fess.codelibs.org/fr/stable/api/api-search.html>`__.

Les étiquettes, les suggestions et les mots populaires s'appellent de la même manière.

::

    $ curl -s "http://localhost:8080/api/v2/labels" | jq .response
    $ curl -s -G "http://localhost:8080/api/v2/suggest-words" --data-urlencode "q=fe" | jq .response
    $ curl -s "http://localhost:8080/api/v2/popular-words" | jq .response

Les résultats se trouvent respectivement dans ``response.labels[]`` (``label`` et ``value``), ``response.suggest_words[]`` (``text`` et ``types``) et ``response.popular_words`` (un tableau de chaînes).
La raison pour laquelle les suggestions et les mots populaires peuvent être vides est expliquée dans « Utiliser les étiquettes, les suggestions et les mots populaires ».

Créer un jeton d'accès
======================

Les appels depuis une application métier utilisent un jeton d'accès.
On attribue au jeton des « autorisations », et les résultats de recherche sont filtrés selon ces autorisations.

Procédure
---------

1. Dans la console d'administration, ouvrez [Système] > [Jeton d'accès] et cliquez sur [Créer nouveau].
2. Dans « Nom », saisissez un nom qui indique l'usage du jeton (par exemple ``crm-search``).
3. Dans « Autorisations », indiquez les rôles des documents que ce jeton peut montrer, un par ligne. Les formats sont ``{role}nom_rôle``, ``{group}nom_groupe`` et ``{user}nom_utilisateur``.
4. Saisissez « Expire » au format ``2027-03-31T23:59:59``. Si le champ est vide, le jeton n'expire pas.
5. Laissez « Nom du paramètre » vide.
6. Cliquez sur [Créer]. De retour dans la liste, cliquez sur le nom et notez la valeur affichée dans « Jeton » sur l'écran de détails (60 caractères alphanumériques).

Si vous renseignez « Nom du paramètre », l'appelant peut ajouter des autorisations au moyen de ce paramètre de requête.
Ne l'utilisez que si vous maîtrisez entièrement les appelants.

Envoyer le jeton
----------------

Envoyez le jeton dans l'en-tête ``Authorization``.
``Authorization: <jeton>`` sans ``Bearer`` est également accepté.

::

    $ export FESS_SEARCH_TOKEN=<jeton noté>
    $ curl -s -G "http://localhost:8080/api/v2/search" \
        -H "Authorization: Bearer $FESS_SEARCH_TOKEN" \
        --data-urlencode "q=proposition" | jq '.response.record_count'

La transmission du jeton dans un paramètre de requête est désactivée, car ``api.access.token.request.parameter`` est vide par défaut.
Les URL sont enregistrées dans les journaux d'accès : utilisez l'en-tête.

Les rôles du jeton déterminent les résultats
--------------------------------------------

Pour une requête avec jeton, seules les autorisations du jeton sont utilisées comme rôles.
Le rôle invité (``{role}guest``), attribué aux appels anonymes sans jeton, n'est pas ajouté tant que les autorisations du jeton ne sont pas vides.

Or, lorsque vous créez une nouvelle configuration d'exploration, le champ des autorisations contient ``{role}guest`` ; les documents publics ordinaires portent donc ``{role}guest``.
Par conséquent, avec un jeton dont la seule autorisation est ``{group}sales``, les documents publics disparaissent des résultats de recherche.
Pour renvoyer à la fois les documents publics et ceux destinés au service commercial, donnez au jeton les deux lignes d'autorisations suivantes.

::

    {role}guest
    {group}sales

Une fois le réglage fait, comparez ``record_count`` pour les mêmes termes de recherche sans jeton et avec jeton, et vérifiez qu'il augmente ou diminue comme prévu.
La conception des autorisations côté documents est traitée dans :doc:`guide-05`.

Pourquoi ne pas transmettre le jeton au navigateur
--------------------------------------------------

- Un jeton écrit dans le JavaScript du navigateur peut être lu par n'importe qui avec les outils de développement. Celui qui le lit peut rechercher tous les documents visibles avec les autorisations du jeton, sans passer par l'application métier.
- Un jeton n'appartient pas à un utilisateur ; il regroupe les autorisations indiquées lors de sa création. Si vous le distribuez aux navigateurs, les différences de droits entre utilisateurs disparaissent.
- Même avec « Connexion requise » activé, ``/search``, ``/documents/all``, ``/documents/export``, ``/suggest-words``, ``/labels`` et ``/popular-words`` répondent sans connexion dès qu'un jeton valide est présenté. Un jeton divulgué peut donc remplacer une connexion.

Pour faire varier ce qui est visible selon l'utilisateur de l'application métier, créez un jeton par périmètre et choisissez côté serveur celui qui correspond à l'utilisateur.

Appeler l'API de recherche côté serveur
=======================================

Voici un exemple de fonction Python à placer dans le backend de l'application métier.
Elle n'utilise que la bibliothèque standard et renvoie les résultats de recherche réduits aux éléments dont l'écran a besoin.

.. code-block:: python

    import json
    import os
    import urllib.error
    import urllib.parse
    import urllib.request

    FESS_URL = os.environ.get("FESS_URL", "http://localhost:8080")
    FESS_SEARCH_TOKEN = os.environ["FESS_SEARCH_TOKEN"]


    class FessApiError(Exception):
        def __init__(self, http_status, code, retry_after=None):
            super().__init__(f"Fess API error: {http_status} {code}")
            self.http_status = http_status
            self.code = code
            self.retry_after = retry_after


    def search_documents(query, label=None, num=5):
        params = [("q", query), ("num", str(num))]
        if label:
            params.append(("fields.label", label))
        url = FESS_URL + "/api/v2/search?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"Authorization": "Bearer " + FESS_SEARCH_TOKEN})
        try:
            with urllib.request.urlopen(req, timeout=15) as res:
                body = json.load(res)
        except urllib.error.HTTPError as e:
            try:
                code = json.load(e)["response"]["error"]["code"]
            except (ValueError, KeyError, TypeError):
                code = "unknown"
            raise FessApiError(e.code, code, e.headers.get("Retry-After")) from e
        response = body["response"]
        return {
            "total": response["record_count"],
            "items": [
                {
                    "title": doc.get("title"),
                    "url": doc.get("url_link"),
                    "snippet": doc.get("content_description"),
                    "last_modified": doc.get("last_modified"),
                }
                for doc in response["data"]
            ],
        }

Sur la fiche client d'un CRM, passez le nom du client et une étiquette, comme dans ``search_documents("Exemple SA", label="sales_docs")``, puis affichez directement la valeur renvoyée à l'écran.

- Le délai d'attente est un peu plus long que le délai de recherche côté Fess (``query.timeout``, 10000 millisecondes par défaut).
- Examinez ``code`` et ``retry_after`` de ``FessApiError`` pour décider du message affiché à l'utilisateur et des nouvelles tentatives (voir « Gérer les erreurs »).
- ``content_description`` contient des balises ``<strong>`` ; si votre modèle l'affiche en HTML, n'autorisez que la balise ``<strong>``.

Enregistrer les données de systèmes externes
============================================

Les données impossibles à explorer (rapports générés par une application métier, résumés de tickets, etc.) peuvent être enregistrées directement dans l'index avec ``PUT /api/admin/documents/bulk`` de l'API Admin.

Utiliser un jeton distinct pour l'API Admin
-------------------------------------------

L'API Admin exige un jeton dont les autorisations comprennent ``{role}admin-api`` (``api.admin.access.permissions=Radmin-api``).
Cette autorisation donne accès à tous les points de terminaison de l'API Admin.
Il n'existe pas d'autorisation limitée à l'enregistrement de documents.
Un tel jeton permet aussi de modifier les configurations d'exploration, les utilisateurs et même les jetons d'accès ; conservez-le donc avec autant de soin que le mot de passe administrateur.

De plus, une recherche avec un jeton qui ne possède que ``{role}admin-api`` n'a que le rôle ``admin-api`` et ne renvoie presque aucun document.
Utilisez des jetons distincts pour la recherche et pour l'enregistrement.
Dans [Système] > [Jeton d'accès], créez un deuxième jeton dont les autorisations se limitent à la seule ligne ``{role}admin-api`` (par exemple nommé ``crm-indexer``) et notez sa valeur.

::

    $ export FESS_ADMIN_TOKEN=<jeton API Admin noté>

Enregistrer des documents
-------------------------

``url`` et ``title`` sont obligatoires.
``content`` est le texte du document et ``label`` un tableau de valeurs d'étiquettes.

::

    $ curl -s -X PUT "http://localhost:8080/api/admin/documents/bulk" \
        -H "Authorization: Bearer $FESS_ADMIN_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "documents": [
            {
              "url": "https://crm.example.com/reports/2026-11",
              "title": "Rapport mensuel des ventes novembre 2026",
              "content": "Les nouvelles opportunités commerciales ont augmenté en novembre par rapport au mois précédent.",
              "label": ["sales_docs"]
            }
          ]
        }' | jq .response

En cas de succès, le résultat de chaque document est renvoyé dans ``items``.
Une création donne ``CREATED`` et la mise à jour d'un document existant ``OK``.

.. code-block:: json

    {
      "version": "15.9",
      "status": 0,
      "items": [
        { "result": "CREATED", "id": "9c1e47b2...e04b" }
      ]
    }

``id`` est une valeur de hachage calculée notamment à partir de ``url`` (128 chiffres hexadécimaux) ; la partie centrale est omise dans l'exemple ci-dessus.
L'enregistrement est terminé lorsqu'une recherche ``q=rapport mensuel des ventes`` avec le jeton de recherche trouve le document.

Points d'attention lors de l'enregistrement
-------------------------------------------

- Si vous omettez ``role``, le rôle invité est attribué et tout le monde peut trouver le document. Pour restreindre sa visibilité, placez dans ``role`` un tableau de valeurs au format interne. Dans le format interne, ``{role}x`` devient ``Rx``, ``{group}x`` devient ``2x`` et ``{user}x`` devient ``1x`` (par exemple ``"role": ["2sales"]``).
- L'ID du document est construit à partir de ``url`` et de ``role`` (et de l'hôte virtuel). Renvoyer le même ``url`` met le document à jour, mais le renvoyer avec un ``role`` différent l'ajoute comme document distinct et laisse l'ancien en place.
- ``items[].id`` dans la réponse est l'ID dans l'index, différent du ``doc_id`` du document. Pour supprimer un document à la fois avec ``DELETE /api/admin/searchlist/doc/{id}``, passez le ``doc_id`` issu des résultats de recherche. Pour supprimer en masse selon une condition, utilisez ``DELETE /api/admin/searchlist/query`` (`SearchList API <https://fess.codelibs.org/fr/stable/api/admin/api-admin-searchlist.html>`__).
- Si seuls certains documents échouent, ``status`` vaut 9 et les éléments en échec contiennent ``message``. Si la requête elle-même est invalide, par exemple ``url`` ou ``title`` manquant ou valeur d'un type incorrect, ``status`` vaut 1 et rien n'est enregistré.

Utiliser les étiquettes, les suggestions et les mots populaires
===============================================================

Créer des catégories avec les étiquettes
----------------------------------------

Les étiquettes utilisées pour filtrer avec ``fields.label`` se créent dans [Robot d'exploration] > [Étiquette].
« Valeur » n'accepte que des caractères alphanumériques et des traits de soulignement (``sales-docs`` et les caractères non ASCII ne sont pas acceptés).
Un document exploré reçoit une étiquette lorsque son URL correspond aux « Chemins inclus » de l'étiquette (:doc:`guide-04`).
Pour les documents enregistrés en masse, envoyez ``label`` comme dans la section précédente.

``/api/v2/labels`` ne renvoie que les étiquettes utilisables par les rôles de l'appelant.
Les étiquettes ont elles aussi des autorisations : celles qui ne correspondent pas aux autorisations du jeton n'apparaissent pas dans la liste.
Construisez la liste des catégories d'un portail à partir des champs ``label`` (nom affiché) et ``value`` (valeur à passer à ``fields.label``) de cette réponse.

Suggestions
-----------

``/api/v2/suggest-words`` renvoie les candidats qui commencent par ``q``.
Le nombre de candidats se règle avec ``num`` (10 par défaut), et les champs ciblés s'indiquent en répétant ``fn``.
Les candidats proviennent des mots des documents explorés (« Suggérer à partir des documents » dans [Système] > [Général]), des termes de recherche (« Suggérer à partir des termes de recherche » sur le même écran) et des mots de suggestion enregistrés par l'administrateur.
Les mots des documents n'apparaissent comme candidats qu'après l'exécution de la tâche « Suggest Indexer » du planificateur (une fois par jour par défaut).
Les candidats sont eux aussi filtrés selon les rôles de l'appelant.

Mots populaires
---------------

``/api/v2/popular-words`` renvoie, parmi les termes collectés dans le journal de recherche, ceux qui ont été le plus souvent recherchés.
Si un tableau vide est renvoyé, vérifiez les points suivants.

- Si « Réponse de mot populaire » dans [Système] > [Général] (``web.api.popularword``, activé par défaut) est désactivé, l'appel échoue avec ``invalid_request`` (HTTP 400).
- « Suggérer à partir des termes de recherche » doit être activé. Les termes de recherche ne sont collectés que lorsque ce réglage est activé.
- Le même terme doit avoir été recherché au moins 10 fois (``suggest.popular.word.query.freq=10``). Les recherches répétées depuis la même session dans un délai d'une minute comptent pour une seule. Juste après l'installation, un résultat vide est normal.
- Seules les recherches effectuées avec le rôle invité seul sont comptabilisées (``suggest.search.log.permissions={user}guest,{role}guest``). Les recherches faites avec un jeton possédant par exemple ``{group}sales`` ou par des utilisateurs connectés ne sont pas comptées.
- Les mots populaires sont eux aussi filtrés selon les rôles de l'appelant. Les termes comptabilisés ne portent que le rôle invité ; un jeton dont les autorisations n'incluent pas ``{role}guest`` obtient donc toujours un résultat vide.
- Les résultats sont mis en cache et ne changent donc pas immédiatement lorsque les recherches augmentent.

En changeant ``seed``, vous obtenez une autre combinaison parmi les candidats.

Gérer les erreurs
=================

En cas d'erreur, ``/api/v2`` renvoie un statut HTTP et ``response.error.code``.

::

    {"response": {"status": 1, "error": {"code": "invalid_request", "message": "..."}}}

Le système appelant doit prévoir à l'avance le traitement des cas suivants.

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - HTTP
     - ``error.code``
     - Cause et action
   * - 400
     - ``invalid_request``
     - ``num`` vaut 0 ou moins, erreur de syntaxe dans les termes de recherche, ``q`` dépasse ``api.param.max.length`` (1000 caractères par défaut), etc. Ne réessayez pas ; vérifiez la saisie
   * - 401
     - ``auth_required``
     - Jeton non enregistré ou expiré, ou absence de jeton alors que « Connexion requise » est activé. Un jeton invalide ne ramène pas à un accès anonyme mais produit un 401. Recréez le jeton
   * - 503
     - ``service_unavailable``
     - Le moteur de recherche, surchargé, a refusé la recherche. ``Retry-After: 5`` est fourni : vous pouvez réessayer après 5 secondes
   * - 500
     - ``internal_error``
     - Erreur interne de Fess. Consultez ``fess.log`` dans [Informations système] > [Fichier journal]

Pour la limitation de débit, les points de terminaison de connexion, de changement de mot de passe, de chat et d'export ont chacun leur propre limite ; en cas de dépassement, 429 ``rate_limited`` et ``Retry-After`` sont renvoyés.
La limitation du nombre de requêtes à l'échelle du serveur (``rate.limit.enabled``) est désactivée par défaut.
Si vous l'activez, le corps de la réponse 429 en cas de dépassement est ``{"error":"rate_limit_exceeded", ...}`` et n'a pas la forme ``response`` présentée plus haut.
Lors d'appels depuis le serveur d'une application métier, gardez à l'esprit que toutes les recherches arrivent depuis la même adresse IP.
Pour plus de détails, consultez `Configuration de la limitation de débit <https://fess.codelibs.org/fr/stable/config/rate-limiting.html>`__.

L'API Admin (``/api/admin/*``) utilise une autre forme d'erreur.
Sans jeton, ou avec un jeton qui ne possède pas ``{role}admin-api``, la réponse est HTTP 401 avec ``response.status`` à 3, et la raison figure dans ``response.message``.

Appel direct depuis le navigateur (CORS)
========================================

CORS ne concerne pas les appels de serveur à serveur.
Ce n'est que lorsque le JavaScript du navigateur appelle directement Fess sur une autre origine que ``api.cors.allow.origin`` (par défaut ``*``), ``api.cors.allow.methods``, ``api.cors.allow.headers`` (inclut ``Authorization`` par défaut), ``api.cors.allow.credentials`` (par défaut ``true``) et ``api.cors.max.age`` (par défaut ``3600`` secondes) de ``fess_config.properties`` s'appliquent.

Lorsque ``api.cors.allow.origin`` vaut ``*``, les requêtes avec des informations d'authentification comme les cookies ne sont pas autorisées.
Pour faire rechercher le navigateur avec les droits de l'utilisateur connecté, énumérez les origines, par exemple ``https://portal.example.com`` (séparées par des virgules).
Avec Docker, vous pouvez aussi indiquer ``-Dfess.config.api.cors.allow.origin=https://portal.example.com`` dans ``FESS_JAVA_OPTS``.
Redémarrez Fess après la modification.
Pour l'intégration côté navigateur, consultez :doc:`guide-03`.

Pour aller plus loin
====================

- Intégrer une zone ou une page de recherche dans un site existant : :doc:`guide-03`
- Concevoir les documents visibles pour chaque jeton ou utilisateur : :doc:`guide-05`
- Utiliser l'API pour les contrôles d'état et la supervision : :doc:`guide-10`
- Gérer les paramètres comme du code avec l'API Admin et fessctl : :doc:`guide-16`
- Protéger la plateforme de recherche, y compris l'exploitation du SSO et des jetons d'accès : :doc:`guide-15`

Références
==========

- `Vue d'ensemble de l'API <https://fess.codelibs.org/fr/stable/api/api-overview.html>`__
- `API de recherche <https://fess.codelibs.org/fr/stable/api/api-search.html>`__
- `API des étiquettes <https://fess.codelibs.org/fr/stable/api/api-label.html>`__
- `API de suggestions <https://fess.codelibs.org/fr/stable/api/api-suggest.html>`__
- `API des mots populaires <https://fess.codelibs.org/fr/stable/api/api-popularword.html>`__
- `Documents API <https://fess.codelibs.org/fr/stable/api/admin/api-admin-documents.html>`__
- `Vue d'ensemble de l'API Admin <https://fess.codelibs.org/fr/stable/api/admin/api-admin-overview.html>`__
- `Jeton d'accès <https://fess.codelibs.org/fr/stable/admin/accesstoken-guide.html>`__
