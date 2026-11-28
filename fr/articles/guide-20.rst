============================================
Interroger Fess depuis des agents IA via MCP
============================================

Introduction
============

Lorsque vous voulez qu'un agent IA tel que Claude Code fasse des recherches dans vos documents internes, lui permettre d'appeler directement la recherche de Fess lui donne accès aux documents indexés comme sources.
Le mécanisme qui le permet est MCP (Model Context Protocol).
Dans Fess, l'installation du plugin ``fess-webapp-mcp`` ajoute un point de terminaison de serveur MCP sur ``/mcp``.

Cet article explique comment installer ce plugin sur Fess 15.9, rendre l'authentification obligatoire, s'y connecter depuis un agent IA et vérifier son fonctionnement.

À l'issue des étapes de cet article, vous obtiendrez la situation suivante :

- Vous pouvez vérifier avec ``curl`` que ``/mcp`` fonctionne
- Les appels sans jeton d'accès sont refusés
- L'étendue des documents que l'agent peut rechercher est déterminée par les autorisations du jeton
- Claude Code peut appeler l'outil ``search`` de Fess

.. note::

   Le sens des appels est l'inverse de celui du mode de recherche IA de :doc:`guide-19`.
   En mode de recherche IA, Fess appelle un LLM (Ollama, OpenAI, etc.) pour produire les réponses. Ollama y sert d'environnement d'exécution du LLM ; ce n'est pas un client MCP.
   Avec MCP, un agent IA externe appelle Fess comme outil de recherche, et c'est le LLM côté agent qui produit la réponse.

Ce que fournit ``/mcp``
=======================

``/mcp`` n'accepte que ``POST`` et renvoie un seul JSON par requête (aucune session n'est conservée).
Les recherches passent par le même traitement que la page de recherche ; le filtrage des résultats par rôle s'applique donc tel quel.

Le plugin 15.9.0 expose les éléments suivants.
Tous sont en lecture seule ; aucun ne modifie les données de Fess.

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * - Nom
     - Description
     - Disponibilité
   * - ``search`` (outil)
     - Recherche plein texte. Chaque résultat comporte un ``doc_id``
     - Toujours disponible
   * - ``suggest`` (outil)
     - Suggestions pour un terme en cours de saisie
     - Toujours disponible
   * - ``get_document`` (outil)
     - Récupère le contenu d'un document à partir de son ``doc_id``
     - Toujours disponible
   * - ``get_index_stats`` (outil)
     - Nom de l'index, nombre de documents et utilisation mémoire de la JVM
     - Non disponible par défaut (voir plus loin)
   * - ``fess://document/{doc_id}`` (ressource)
     - Effectue la même récupération que ``get_document``, sous forme de ressource
     - Toujours disponible
   * - ``fess://index/stats`` (ressource)
     - Même contenu que ``get_index_stats``
     - Comme ``get_index_stats``
   * - ``basic_search`` / ``advanced_search`` (prompt)
     - Modèles de prompt pour la recherche. ``advanced_search`` accepte aussi ``sort`` et ``num``
     - Toujours disponible

Si vous omettez ``num`` dans ``search``, seuls 3 résultats sont renvoyés (valeur par défaut de ``mcp.default.page.size``).
Les extraits de ``search`` comme le contenu de ``get_document`` sont tronqués à 10000 caractères au maximum, et ``get_document`` met alors ``truncated`` à ``true`` (``mcp.content.max.length``).

Installer le plugin
===================

La version du plugin doit correspondre à la version mineure de Fess.
Pour Fess 15.9, utilisez ``fess-webapp-mcp`` 15.9.x.
Installez-le par l'une des méthodes suivantes, puis redémarrez Fess.

- Console d'administration : dans [Système] > [Plugin], cliquez sur [Installer], sélectionnez ``fess-webapp-mcp`` dans l'onglet [Distant] et installez-le
- Ligne de commande : ``bin/fess-setup install plugin fess-webapp-mcp:15.9.0``
- Docker : ajoutez ``FESS_PLUGINS`` à ``environment`` de ``fess01`` dans ``compose.yaml``. L'image Docker n'inclut pas ce plugin

::

    environment:
      - "FESS_PLUGINS=fess-webapp-mcp:15.9.0"

Avec la version Docker, si le nom ou la version est erroné, le plugin est ignoré et le conteneur démarre quand même.
Après l'ajout, vérifiez dans le journal de démarrage que le plugin a bien été téléchargé.

.. warning::

   Lors d'une mise à niveau de Fess, remplacez aussi ce plugin par la nouvelle version avant de démarrer Fess.
   Si le jar d'une ancienne version du plugin (par exemple celle pour 15.8) reste dans ``WEB-INF/plugin``, Fess 15.9 échoue à l'initialisation au démarrage, et non seulement ``/mcp`` mais toutes les pages et toutes les API renvoient 404.
   En ligne de commande, vous pouvez le remplacer avec ``bin/fess-setup upgrade plugins``.

Après le redémarrage, si l'avertissement WARN suivant apparaît dans le fichier journal ``fess.log``, le point de terminaison est actif.

::

    [MCP] mcp.auth.mode=none - every /mcp caller is treated as anonymous. Set mcp.auth.mode=fess_token, ...

Ce message indique que le point de terminaison fonctionne sans authentification, comme décrit dans la section suivante.

Vérifier d'abord sans authentification
======================================

.. warning::

   Juste après l'installation, ``/mcp`` fonctionne sans authentification (``mcp.auth.mode=none``).
   Toute personne qui peut atteindre ``/mcp`` peut effectuer des recherches avec les mêmes droits qu'un utilisateur non connecté (invité), et même récupérer le contenu des documents avec ``get_document``.
   Tous les documents des configurations d'exploration dont les autorisations sont restées à la valeur par défaut ``{role}guest`` sont concernés.
   Limitez les essais dans cet état à votre environnement local, et rendez l'authentification obligatoire comme indiqué dans la section suivante.
   Si « Connexion requise » est activé dans [Système] > [Général], ``/mcp`` dans cet état refuse tous les appels avec HTTP 403. Dans ce cas, passez à la section suivante.

En supposant que Fess fonctionne sur ``http://localhost:8080``, appelez ``server/discover``.

::

    $ curl -sS -X POST http://localhost:8080/mcp \
        -H 'Content-Type: application/json' \
        -H 'Accept: application/json, text/event-stream' \
        -H 'MCP-Protocol-Version: 2026-07-28' \
        -H 'Mcp-Method: server/discover' \
        -d '{"jsonrpc":"2.0","id":1,"method":"server/discover","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'

L'appel a réussi si ``result.supportedVersions`` contient ``2026-07-28`` et ``result.capabilities`` contient notamment ``tools`` dans la réponse.

Appelez ensuite l'outil ``search``.
Indiquez dans ``q`` un mot présent dans vos documents explorés.

::

    $ curl -sS -X POST http://localhost:8080/mcp \
        -H 'Content-Type: application/json' \
        -H 'MCP-Protocol-Version: 2026-07-28' \
        -H 'Mcp-Method: tools/call' \
        -H 'Mcp-Name: search' \
        -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search","arguments":{"q":"Fess","num":5},"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'

Les résultats figurent dans ``result.structuredContent.hits`` et le nombre de résultats dans ``total``.
Les valeurs des en-têtes doivent correspondre au corps de la requête.
``MCP-Protocol-Version`` doit être identique à la version de ``params._meta``, ``Mcp-Method`` à ``method``, et ``Mcp-Name`` au nom de l'outil.
En cas de divergence, le résultat est HTTP 400 (code d'erreur ``-32020``).

Rendre l'authentification obligatoire
=====================================

Passez au mode ``fess_token``, qui authentifie au moyen des jetons d'accès de Fess.
Il existe aussi un mode ``oauth``, qui authentifie au moyen de JWT émis par un serveur d'autorisation externe.
Pour sa configuration, consultez la section « OAuth 2.1 reference » du README.

Créer un jeton d'accès
----------------------

1. Dans la console d'administration, ouvrez [Système] > [Jeton d'accès] et cliquez sur [Créer nouveau]
2. Dans « Nom », saisissez un nom qui indique l'usage, par exemple ``mcp-agent``
3. Dans « Autorisations », saisissez les rôles des documents que l'agent peut voir, un par ligne. Si les documents destinés aux invités suffisent, saisissez ``{role}guest`` (le choix est expliqué dans « Autorisations du jeton et résultats de recherche »)
4. Si nécessaire, indiquez « Expire », puis cliquez sur [Créer]
5. Dans la liste, cliquez sur le nom du jeton créé ; sa valeur s'affiche dans « Jeton » sur la page de détails

Configurer mcp.auth.mode
------------------------

Tous les paramètres ``mcp.*`` sont lus depuis les propriétés système de Fess (``system.properties``).
Les écrire dans ``fess_config.properties`` ou sous la forme ``-Dfess.config.*`` est sans effet, sans erreur ni message dans les journaux.

Pour la version ZIP, ajoutez la ligne suivante à ``app/WEB-INF/conf/system.properties`` ; pour les versions RPM/DEB, à ``/etc/fess/system.properties``.

::

    mcp.auth.mode=fess_token

La valeur est relue en cours d'exécution ; elle prend effet en quelques secondes, sans redémarrage.

Le conteneur ``fess01`` de la version Docker n'a pas de volume : les paramètres écrits dans des fichiers du conteneur sont perdus lorsque le conteneur est recréé.
Indiquez le paramètre dans ``FESS_JAVA_OPTS`` de ``compose.yaml`` avec le préfixe ``-Dfess.system.`` (et non ``fess.config.``).

::

    environment:
      - "FESS_PLUGINS=fess-webapp-mcp:15.9.0"
      - "FESS_JAVA_OPTS=-Dfess.system.mcp.auth.mode=fess_token"

``FESS_PLUGINS`` et ``FESS_JAVA_OPTS`` prennent effet lorsque le conteneur est recréé.
Après avoir modifié ``compose.yaml``, exécutez la commande suivante.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Si la même clé existe dans ``system.properties``, c'est cette valeur qui prévaut.

Vérifier que l'authentification est appliquée
---------------------------------------------

Relancez tel quel l'appel ``server/discover`` de la section précédente.
Comme aucun jeton n'est joint, HTTP 401 est renvoyé avec l'en-tête ``WWW-Authenticate: Bearer realm="fess-mcp"`` (``curl -i`` affiche les en-têtes).
En mode ``fess_token``, ``server/discover`` exige lui aussi une authentification.

Exécutez ensuite la commande ``curl`` de ``search`` de la section précédente en ajoutant ``-H 'Authorization: Bearer <jeton>'``.
Remplacez ``<jeton>`` par la valeur affichée sur la page de détails.
Si des résultats de recherche sont renvoyés, la configuration est terminée.
Un jeton inexistant ou expiré entraîne HTTP 401.

Autorisations du jeton et résultats de recherche
================================================

En mode ``fess_token``, les autorisations du jeton deviennent directement les rôles utilisés pour la recherche.
Non seulement ``search`` mais aussi ``get_document`` est filtré avec les mêmes rôles ; un document sur lequel le jeton n'a pas de droits ne peut donc pas être récupéré, même si l'on connaît son ``doc_id``.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Autorisations du jeton
     - Documents consultables
   * - Vide
     - Comme un invité (documents avec ``{role}guest``)
   * - ``{role}guest``
     - Comme un invité
   * - ``{role}sales``
     - Uniquement les documents avec ``{role}sales``. Les documents destinés aux invités ne sont pas inclus
   * - ``{role}sales`` et ``{role}guest``
     - Les documents des deux

Le rôle invité n'est ajouté automatiquement que pour les jetons dont les autorisations sont vides.
Pour que l'agent recherche à la fois les documents du service et ceux destinés à tous, indiquez aussi ``{role}guest``.
Pour le fonctionnement des rôles et des autorisations, consultez :doc:`guide-05`.

Pour le vérifier, lancez ``search`` sur le même mot avec deux jetons ayant des autorisations différentes, et comparez ``total``.

.. warning::

   N'attribuez pas ``{role}admin-api`` à un jeton destiné à un agent.
   Un jeton doté de ``{role}admin-api`` peut appeler l'ensemble de l'Admin API de Fess.
   De plus, un ``search`` avec un jeton qui ne possède que ``{role}admin-api`` renvoie 0 résultat, car aucun document n'a ce rôle.

Rendre ``get_index_stats`` disponible
-------------------------------------

``get_index_stats`` et ``fess://index/stats`` ne sont présentés qu'aux appelants qui possèdent l'une des autorisations listées dans ``mcp.tools.index_stats.permissions``.
La valeur par défaut est ``Radmin-api`` (notation interne de ``{role}admin-api``) ; en mode ``none``, aucun appelant ne possède d'autorisation, ils ne sont donc présentés à personne.
Un appelant sans l'autorisation reçoit la même erreur que pour un outil inexistant.

Cet outil n'est pas nécessaire pour la seule recherche.
Si vous l'utilisez, définissez un rôle dédié au lieu de donner ``{role}admin-api``, et ajoutez ce rôle aux autorisations du jeton.
Dans ``system.properties``, utilisez la notation interne (``R`` pour ``{role}``).

::

    mcp.tools.index_stats.permissions=Rmcp-stats

Dans cet exemple, ajoutez ``{role}mcp-stats`` aux autorisations du jeton.

Autres paramètres
=================

Tous se définissent dans ``system.properties`` (pour la version Docker, ``-Dfess.system.<clé>``).
Pour les valeurs booléennes, seul ``true`` est considéré comme vrai ; ``1`` ou ``yes`` sont considérés comme faux.

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - Clé
     - Valeur par défaut
     - Description
   * - ``mcp.allowed.origins``
     - (vide)
     - Pour les appels depuis un navigateur, les valeurs ``Origin`` autorisées, de la forme ``https://app.example.com``, séparées par des virgules. Si la valeur est vide, toute requête comportant un en-tête ``Origin`` est refusée avec HTTP 403. ``curl`` et les agents en ligne de commande n'envoient pas ``Origin`` et ne sont donc pas concernés
   * - ``mcp.rate.limit.per.minute``
     - ``60``
     - Limite par minute des appels ``tools/call`` et similaires pour chaque appelant (le jeton, ou à défaut l'adresse IP). En cas de dépassement, HTTP 429 et ``Retry-After`` sont renvoyés. ``0`` désactive la limite
   * - ``mcp.content.max.length``
     - ``10000``
     - Nombre maximal de caractères du contenu renvoyé par ``search`` et ``get_document``
   * - ``mcp.default.page.size``
     - ``3``
     - Nombre de résultats lorsque ``num`` est omis dans ``search``
   * - ``mcp.enabled``
     - ``true``
     - Avec ``false``, ``/mcp`` renvoie toujours HTTP 503
   * - ``mcp.legacy.protocol.enabled``
     - ``true``
     - Accepte aussi les anciens clients (``2025-11-25`` / ``2025-06-18``) qui se connectent avec ``initialize``

Contrairement à ``mcp.*``, les deux paramètres suivants relèvent du ``fess_config.properties`` de Fess (pour la version Docker, ``-Dfess.config.<clé>``).

- Si les appels passent par un proxy inverse sur un autre hôte, ajoutez l'adresse IP du proxy à ``rate.limit.trusted.proxies`` (valeur par défaut ``127.0.0.1,::1``). Sinon, tous les appelants passant par le proxy partagent la même limite
- Pour des appels depuis un navigateur sur une autre origine, ajoutez, en plus de ``mcp.allowed.origins``, ``MCP-Protocol-Version``, ``Mcp-Method`` et ``Mcp-Name`` à ``api.cors.allow.headers``. Pour plus de détails, consultez la section « Browser clients » du README

Se connecter depuis un agent IA
===============================

Claude Code
-----------

Claude Code peut se connecter directement en ``2026-07-28``.
Enregistrez Fess comme serveur MCP HTTP avec ``claude mcp add`` et transmettez le jeton avec ``--header``.

::

    $ claude mcp add --transport http fess http://localhost:8080/mcp \
        --header "Authorization: Bearer <jeton>"

``claude mcp list`` affiche l'entrée ``fess`` enregistrée et permet aussi de vérifier l'état de la connexion.
Si vous demandez à Claude Code par exemple « Cherche dans Fess la procédure de remboursement des frais de déplacement », l'agent appelle l'outil ``search`` avec des arguments comme les suivants, puis appelle ``get_document`` avec le ``doc_id`` des résultats pour lire le contenu.

.. code-block:: json

    {
      "name": "search",
      "arguments": {
        "q": "frais de déplacement",
        "num": 5,
        "fields": { "label": ["manual"] }
      }
    }

Dans ``label`` de ``fields``, indiquez la valeur d'une étiquette Fess (omettez-le si vous ne filtrez pas par étiquette).
Les autres arguments de ``search`` comprennent notamment ``start`` (pagination), ``sort`` (par exemple ``last_modified.desc``) et ``lang``.

Autres clients
--------------

Les clients qui se connectent avec l'ancien protocole (``initialize``), comme OpenCode, Codex CLI ou Gemini CLI, fonctionnent aussi tant que ``mcp.legacy.protocol.enabled`` conserve sa valeur par défaut ``true``.
Les clients qui ne connaissent que ``2025-03-26`` ou une version antérieure ne peuvent pas se connecter.
Les clients de bureau qui ne peuvent lancer des serveurs MCP qu'en stdio passent par ``mcp-remote``, qui fait le relais entre stdio et HTTP.
La compatibilité de chaque client est résumée dans la section « Client compatibility » du README.

Attention à l'envoi des résultats de recherche à l'extérieur
------------------------------------------------------------

Si le LLM utilisé par l'agent est un service cloud, les extraits de ``search`` et le contenu de ``get_document`` sont envoyés à ce service.
Pour restreindre ce qui est envoyé, ne sélectionnez par les autorisations du jeton que les documents qui peuvent l'être et, si nécessaire, réduisez ``mcp.content.max.length``.

Dépannage
=========

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Symptôme
     - Cause et solution
   * - HTTP 400, code d'erreur ``-32020``
     - ``MCP-Protocol-Version``, ``Mcp-Method`` ou ``Mcp-Name`` est absent ou ne correspond pas au corps de la requête
   * - HTTP 401
     - En mode ``fess_token``, le jeton est absent, inexistant ou expiré
   * - Toutes les requêtes renvoient HTTP 403
     - L'en-tête ``Origin`` ne figure pas dans ``mcp.allowed.origins``. Ou bien, en mode ``none``, « Connexion requise » est activé
   * - Le premier appel échoue avec ``-32601`` en mentionnant ``initialize``
     - Il s'agit d'un ancien client, et ``mcp.legacy.protocol.enabled`` n'est pas ``true``
   * - ``search`` renvoie 0 résultat
     - Les autorisations du jeton ne contiennent pas les rôles des documents. Si ``partial`` vaut ``true`` dans le résultat, la recherche ne s'est pas terminée (délai dépassé ou panne d'OpenSearch) ; cela ne signifie pas forcément qu'il n'y a aucune correspondance
   * - ``Tool execution failed (error_code:...)``
     - La cause est consignée en WARN dans ``fess.log``. Recherchez la valeur de ``error_code`` dans le journal

Pour aller plus loin
====================

- Séparer par rôle les documents exposés via MCP : :doc:`guide-05`
- Faire répondre Fess lui-même avec un LLM : :doc:`guide-19`
- Trouver des documents de sens proche même sans correspondance de mots-clés : :doc:`guide-18`
- Utiliser l'API de recherche depuis des applications métier ou répartir les jetons d'accès selon l'usage : :doc:`guide-11`
- Configurer ensemble le SSO et la protection d'accès : :doc:`guide-15`

Références
==========

- `fess-webapp-mcp README (15.9.0) <https://github.com/codelibs/fess-webapp-mcp/blob/fess-webapp-mcp-15.9.0/README.md>`__
- `Plugins <https://fess.codelibs.org/fr/stable/admin/plugin-guide.html>`__
- `Jeton d'accès <https://fess.codelibs.org/fr/stable/admin/accesstoken-guide.html>`__
- `Installation avec Docker (Détails) <https://fess.codelibs.org/fr/stable/install/install-docker.html>`__
- `Model Context Protocol <https://modelcontextprotocol.io/>`__
