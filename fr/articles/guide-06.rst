==============================================
Rechercher dans Git, Confluence, Jira et Slack
==============================================

Introduction
============

Les informations d'une équipe de développement sont réparties entre plusieurs outils : le code et les README dans Git, les documents de conception dans Confluence, les tickets dans Jira et les discussions dans Slack.
Chercher successivement dans les quatre outils chaque fois que l'on veut savoir « où cette spécification a-t-elle été décidée ? » est fastidieux.
Avec les plugins de magasin de données de Fess, vous pouvez rechercher les informations des quatre outils depuis une seule page de recherche.

Une configuration erronée conduit toutefois à des situations comme celles-ci :

- Tous les fichiers Git sont enregistrés avec une URL vide, si bien que le fichier d'origine ne peut pas être ouvert depuis les résultats de recherche
- Tous les messages Slack s'affichent sans titre
- Les messages des canaux privés apparaissent aussi dans les résultats de recherche des utilisateurs non connectés
- Les fichiers Git disparaissent de l'index au bout de quelques jours

Pour chaque outil, cet article présente une configuration minimale qui fonctionne telle quelle, et explique comment chaque réglage évite les pièges ci-dessus.
Les étapes communes à tous les magasins de données, comme l'installation des plugins, la saisie du nom du gestionnaire, des paramètres et du script, ou la création des tâches, sont regroupées dans :doc:`datastore-basics`.
Lisez d'abord cet article avant de poursuivre.
Les réglages de cet article correspondent à Fess 15.9 et à la version 15.9.0 de chaque plugin.

Ce que nous allons construire
=============================

.. list-table::
   :header-rows: 1
   :widths: 14 20 26 40

   * - Outil
     - Plugin
     - Nom du gestionnaire
     - À préparer côté outil
   * - Git
     - ``fess-ds-git``
     - ``GitDataStore``
     - Un jeton d'accès avec droit de lecture (le clonage en HTTPS doit être possible)
   * - Confluence / Jira
     - ``fess-ds-atlassian``
     - ``ConfluenceDataStore`` / ``JiraDataStore``
     - Un jeton d'API du compte d'exploration
   * - Slack
     - ``fess-ds-slack``
     - ``SlackDataStore``
     - Le Bot User OAuth Token (``xoxb-``) d'une application Slack

Si Fess tourne sous Docker, vous pouvez installer tous les plugins au démarrage en listant leurs noms et versions, séparés par des espaces, dans la variable d'environnement ``FESS_PLUGINS``.

.. code-block:: yaml

    environment:
      - FESS_PLUGINS=fess-ds-git:15.9.0 fess-ds-atlassian:15.9.0 fess-ds-slack:15.9.0

Si vous les installez depuis la console d'administration ou avec ``fess-setup``, redémarrez Fess après l'installation.

À décider d'abord : qui peut voir les résultats
===============================================

Lorsque vous créez une nouvelle configuration de magasin de données, le champ « Autorisations » contient déjà ``{role}guest``.
Si vous le laissez ainsi, les informations importées sont trouvées aussi par les utilisateurs non connectés.

Les plugins Git, Confluence et Jira ne transposent pas dans Fess les droits d'accès de l'outil d'origine.
Tout ce que le compte d'exploration peut lire est importé, et devient visible pour quiconque possède un rôle ou un groupe inscrit dans le champ « Autorisations ».
Vous définissez donc la portée en combinant les deux points suivants :

- Remplacer ``{role}guest`` dans le champ « Autorisations » par les personnes qui doivent voir le contenu (par ex. ``{group}developers``)
- Limiter ce qui est importé à ce que ces personnes peuvent voir, au moyen des droits du compte d'exploration ainsi que de ``jira.jql`` et ``include_pattern`` décrits plus loin

Seul le plugin Slack peut importer les membres des canaux privés en tant qu'autorisations (voir plus loin).
Pour le fonctionnement des groupes et des rôles, consultez :doc:`guide-05`.

Dépôts Git
==========

Préparation
-----------

``fess-ds-git`` clone en HTTPS.
Les URI SSH (de la forme ``git@...``) ne sont pas prises en charge.
Pour les dépôts privés, créez un jeton d'accès en lecture.
Pour un jeton classique GitHub, il s'agit du scope ``repo`` ; pour GitLab, du scope ``read_repository``.

Paramètres et script
--------------------

Dans [Robot d'exploration] > [Magasin de données] > [Créer nouveau], sélectionnez ``GitDataStore`` comme « Nom du gestionnaire ».

.. code-block:: properties

    script_type=javascript
    uri=https://github.com/example/dev-platform.git
    username=fess-crawler
    password=ghp_xxxxxxxxxxxxxxxxxxxx
    base_url=https://github.com/example/dev-platform/blob/main/
    include_pattern=.*\.(md|rst|txt|java|py|ts|yml|yaml)$
    time_to_live=5256000

.. code-block:: properties

    url=url
    title=path
    content=content
    mimetype=mimetype
    content_length=contentLength
    last_modified=timestamp
    label="code"

Chaque ligne a la signification suivante :

- ``base_url`` : l'``url`` du script est ``base_url`` concaténée telle quelle avec le chemin dans le dépôt. Si vous l'omettez, ``url`` devient une chaîne vide ; tous les fichiers reçoivent alors le même ID de document et s'écrasent mutuellement. Terminez la valeur par ``/`` et faites correspondre le nom de branche à la branche explorée (par défaut la branche par défaut du dépôt distant ; pour la changer, utilisez ``commit_id``).
- ``username`` / ``password`` : utilisés pour l'authentification uniquement lorsque les deux sont renseignés. N'intégrez pas le jeton dans ``uri`` ; écrivez-le dans ``password`` (``password`` est chiffré à l'enregistrement, ``uri`` ne l'est pas).
- ``include_pattern`` : une expression régulière qui doit correspondre au chemin complet dans le dépôt (par ex. ``docs/setup.md``). Ce n'est pas une URL.
- ``title=path`` : avec ``name``, qui ne contient que le nom du fichier, les fichiers de même nom comme ``README.md`` ne se distinguent pas dans les résultats de recherche ; on utilise donc le chemin.

Exploration différentielle et expiration
----------------------------------------

Lorsqu'une exploration réussit, ``fess-ds-git`` réécrit son ID de commit dans ``prev_commit_id`` du champ « Paramètres ».
À partir de la deuxième exploration, il n'enregistre que les fichiers figurant dans le diff par rapport au commit précédent, et supprime les documents des fichiers supprimés ou renommés (la prise en compte des suppressions nécessite ``base_url``).

Cette exploration différentielle s'accorde mal avec l'expiration des documents de Fess ; c'est pourquoi l'exemple ci-dessus précise ``time_to_live``.
Les documents d'un magasin de données reçoivent une date d'expiration lors de leur enregistrement.
Par défaut, elle est déterminée par « Supprimer les anciens documents » dans [Système] > [Général] (3 jours par défaut), et les documents expirés sont supprimés par la tâche « Doc Purger », exécutée chaque minute.
En exploration différentielle, les fichiers inchangés ne sont pas réenregistrés ; leur expiration n'est donc pas prolongée et ils disparaissent quelques jours après la première exploration.
``time_to_live`` est un paramètre qui indique en minutes l'expiration des documents de cette configuration ; ``5256000`` correspond à environ 10 ans.

Pour la même raison, les modifications du script, de ``base_url``, d'``include_pattern`` ou du champ « Autorisations » ne s'appliquent pas aux fichiers inchangés.
Pour réenregistrer tous les fichiers, procédez comme suit :

1. Dans [Informations système] > [Rechercher], recherchez ``label:code`` et supprimez les anciens documents avec [Tout supprimer par cette requête]
2. Effacez la valeur de ``prev_commit_id=`` dans le champ « Paramètres » et enregistrez
3. Exécutez la tâche

Si vous avez modifié le champ « Autorisations » ou ``base_url``, les ID de document changent ; si vous sautez l'étape 1, les anciens documents restent.
De même, avant de supprimer cette configuration de magasin de données, supprimez d'abord ses documents avec l'étape 1.

Confluence
==========

Sur Atlassian Cloud, créez un jeton d'API avec le compte d'exploration et utilisez-le comme mot de passe de l'authentification Basic.
Sont importés les pages et les billets de blog des espaces que ce compte peut consulter.
Sélectionnez ``ConfluenceDataStore`` comme « Nom du gestionnaire ».

.. code-block:: properties

    script_type=javascript
    home=https://example.atlassian.net
    deployment=cloud
    auth_type=basic
    basic.username=fess-crawler@example.com
    basic.password=your-api-token
    include_pattern=https://example\.atlassian\.net/wiki/spaces/(DEV|OPS)/.*

.. code-block:: properties

    url=content.view_url
    title=content.title
    content=content.body + content.comments
    last_modified=content.last_modified
    label="docs"

- ``home`` fonctionne avec ou sans ``/wiki``. Sur Cloud, ``/wiki`` est ajouté pour Confluence.
- Si ``deployment`` est omis, il est considéré comme ``cloud`` lorsque le nom d'hôte se termine par ``.atlassian.net``, et comme ``datacenter`` sinon.
- Avec ``content.comments``, les commentaires de la page deviennent eux aussi interrogeables comme partie du corps. Les commentaires sont concaténés, séparés par des lignes vides.
- ``include_pattern`` est comparé à l'URL complète du document. Sur Cloud, les URL des pages ont la forme ``https://<site>/wiki/spaces/<clé-d-espace>/pages/<id-de-page>`` ; vous pouvez donc filtrer par clé d'espace. Les URL de Data Center (``/pages/viewpage.action?pageId=...``) ne contiennent pas la clé d'espace ; cette méthode n'y est donc pas utilisable.

Sur Data Center, indiquez ``deployment=datacenter`` ; pour utiliser un jeton d'accès personnel, spécifiez ``auth_type=pat`` et ``pat.token``.

Jira
====

L'authentification est la même que pour Confluence.
Sélectionnez ``JiraDataStore`` comme « Nom du gestionnaire » et limitez les tickets à importer avec JQL.

.. code-block:: properties

    script_type=javascript
    home=https://example.atlassian.net
    deployment=cloud
    auth_type=basic
    basic.username=fess-crawler@example.com
    basic.password=your-api-token
    jira.jql=project in (DEV, OPS)

.. code-block:: properties

    url=issue.view_url
    title=issue.summary
    content=issue.description + issue.comments
    last_modified=issue.last_modified
    label="tickets"

Le paramètre JQL s'appelle ``jira.jql``.
L'ancien nom ``issue.jql`` fonctionne encore, mais le journal affiche alors l'avertissement ``Parameter "issue.jql" is deprecated``.
L'ancien nom doit être supprimé en 16.0.
Si ``jira.jql`` est omis, ``created is not empty`` s'applique, c'est-à-dire tous les tickets que le compte peut consulter.

Avec ``issue.comments``, les commentaires du ticket sont aussi ajoutés au corps, séparés par des lignes vides, et deviennent interrogeables.
Les commentaires sont récupérés par l'API pour chaque ticket, ce qui augmente le nombre d'appels (voir les limites de débit plus loin).

Slack
=====

Préparer l'application Slack
----------------------------

Créez une application sur https://api.slack.com/apps et ajoutez les scopes suivants dans Bot Token Scopes sous [OAuth & Permissions] ; installez-la ensuite dans l'espace de travail.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Scope
     - Quand il est nécessaire
   * - ``channels:read``, ``channels:history``, ``users:read``, ``team:read``
     - Toujours
   * - ``groups:read``, ``groups:history``
     - Importer les canaux privés (``include_private=true``)
   * - ``users:read.email``
     - Utiliser les membres des canaux privés comme autorisations (``permission_sync=true``)
   * - ``files:read``
     - Importer aussi les fichiers (``file_crawl=true``)

Sans ``team:read``, le plugin appelle ``chat.getPermalink`` pour chaque message, ce qui augmente fortement le nombre d'appels d'API.
Après l'installation, ajoutez l'application à chaque canal à importer.
Les canaux que l'application n'a pas rejoints sont ignorés avec un avertissement.

Créez deux configurations de magasin de données distinctes, l'une pour les canaux publics et l'autre pour les canaux privés.
La raison en est expliquée dans la section « Canaux privés ».

Canaux publics
--------------

Sélectionnez ``SlackDataStore`` comme « Nom du gestionnaire » et indiquez dans le champ « Autorisations » les personnes qui doivent voir les canaux publics.

.. code-block:: properties

    script_type=javascript
    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=*all
    include_private=false

.. code-block:: properties

    url=message.permalink
    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    last_modified=message.timestamp
    label="slack"

``message.title`` est toujours une chaîne vide pour les messages ; si vous écrivez ``title=message.title``, aucun résultat n'a de titre.
Comme dans l'exemple ci-dessus, construisez le titre à partir de l'auteur et du nom du canal.
Les réponses dans les fils sont elles aussi enregistrées comme documents individuels.
Les messages système tels que ``channel_join`` sont exclus par défaut (``ignore_system_events=true``).

Canaux privés
-------------

Avec ``permission_sync=true``, le plugin crée, à partir des adresses e-mail des membres d'un canal privé, un rôle utilisateur par membre et les place dans ``message.roles``.
Toutefois, les valeurs de ``default_permissions`` et du champ « Autorisations » sont aussi ajoutées à cette valeur.
Les canaux publics n'ont pas de rôles propres ; si ces deux réglages sont vides, les documents des canaux publics ne sont visibles par personne.
À l'inverse, si vous indiquez dans l'un des deux le public des canaux publics, ce public voit aussi les documents des canaux privés.
Comme une seule configuration ne peut pas traiter correctement les deux cas, les canaux privés font l'objet d'une configuration distincte.

Dans la deuxième configuration de magasin de données, supprimez ``{role}guest`` du champ « Autorisations » pour le laisser vide, et listez dans ``channels`` les noms des canaux privés à importer.

.. code-block:: properties

    script_type=javascript
    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=dev-security,dev-incident
    include_private=true
    permission_sync=true

.. code-block:: properties

    url=message.permalink
    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    last_modified=message.timestamp
    role=message.roles
    label="slack"

- Sans ``role=message.roles``, les rôles calculés ne sont pas utilisés. Dans ce cas, l'avertissement ``no script value references message.roles`` s'affiche au démarrage de l'exploration.
- Si vous mélangez des canaux publics dans ``channels``, leurs documents ont des rôles vides et ne sont visibles par personne.
- Avec cette configuration, l'avertissement ``default_permissions is not set and this crawl's DataConfig permission field is empty`` s'affiche au démarrage de l'exploration. Tant qu'aucun canal public n'est inclus, ce n'est pas un problème.
- Les canaux dont les membres n'ont pas pu être récupérés, ou pour lesquels aucune adresse e-mail n'a pu être résolue (par exemple parce que ``users:read.email`` a été oublié), ne sont pas importés lors de cette exploration. Ils sont enregistrés dans [Informations système] > [URL d'échec] avec l'ID et le nom du canal.

Lors de la recherche, le nom de l'utilisateur connecté à Fess est comparé à ces adresses e-mail.
Le nom d'utilisateur Fess doit donc correspondre à l'adresse e-mail Slack.
Slack traite les adresses e-mail en minuscules ; les noms d'utilisateur Fess doivent donc aussi être en minuscules.
Les utilisateurs sans correspondance ne voient simplement pas les documents des canaux privés ; ils ne voient jamais les documents d'autres personnes.
Pour savoir quelle valeur devient le nom d'utilisateur lors d'une connexion par SSO, consultez :doc:`guide-15`.

Si vous aviez déjà importé des canaux privés sans ``permission_sync``, ces documents restent sans autorisations jusqu'à leur expiration.
Supprimez ces documents dans [Informations système] > [Rechercher] avant d'explorer avec cette configuration.

Étiquettes, boost et planification
==================================

Les étiquettes sont attribuées par la ligne ``label="..."`` de chacun des scripts ci-dessus.
Pour les afficher comme filtres sur la page de recherche, créez dans [Robot d'exploration] > [Étiquette] des étiquettes ayant les mêmes valeurs (``code``, ``docs``, ``tickets``, ``slack``).
Attention : si une étiquette possède des « Chemins inclus » qui correspondent à l'URL du document, l'étiquette du script est perdue (:doc:`datastore-basics`).

Les règles de [Robot d'exploration] > [Boost de document] ne s'appliquent pas aux documents des magasins de données.
Pour faire remonter les documents de conception de Confluence au-dessus des messages Slack, augmentez le « Boost » (valeur initiale ``1.0``) de la configuration de magasin de données de Confluence.
La valeur est multipliée par le score de recherche ; modifiez-la donc progressivement en comparant les résultats.

Pour explorer chaque outil à une fréquence différente, utilisez [Créer une nouvelle tâche] sur la page de détails de chaque configuration de magasin de données (:doc:`datastore-basics`).

Limites de débit des API
========================

Les plugins Slack et Atlassian renvoient automatiquement la requête en cas de réponse ``429`` ou ``5xx`` et, en présence d'un en-tête ``Retry-After``, attendent le nombre de secondes indiqué (60 secondes au maximum pour Slack).

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Plugin
     - Paramètres réglables
   * - Slack
     - ``read_interval`` (attente par message, en millisecondes, ``0`` par défaut), ``max_retry_count`` (``3`` par défaut), ``retry_interval`` (attente avant la première nouvelle tentative, en millisecondes, ``3000`` par défaut ; doublée à chaque tentative, 60 secondes au maximum)
   * - Atlassian
     - ``read_interval`` (intervalle minimal entre appels d'API, en millisecondes, ``0`` par défaut ; partagé entre les threads). Le nombre et l'intervalle des nouvelles tentatives sont fixes

Lorsque Slack épuise ses nouvelles tentatives, l'exploration est interrompue.
L'état dans le journal des tâches reste « OK » ; vérifiez donc avec les étapes de la section suivante.

Vérifier le fonctionnement
==========================

La lecture des résultats de tâche et des journaux est expliquée dans :doc:`datastore-basics`.
Une exploration de magasin de données peut échouer alors que la tâche s'affiche « OK » ; jugez donc d'après le nombre de documents et les journaux.
Pour la configuration de cet article, vérifiez en outre les points suivants :

1. Dans [Informations système] > [Rechercher], recherchez successivement ``label:code``, ``label:docs``, ``label:tickets`` et ``label:slack``, et vérifiez que le nombre n'est pas 0
2. Ouvrez l'URL d'un document Git et vérifiez que le fichier du dépôt s'affiche. Si ``fess-crawler.log`` contient l'avertissement ``base_url is blank``, revoyez ``base_url``
3. Ouvrez la page de détails de la configuration Git et vérifiez que ``prev_commit_id`` a été réécrit dans les paramètres
4. Déconnecté, recherchez un mot qui n'apparaît que dans un canal privé et vérifiez qu'aucun résultat ne s'affiche
5. Connectez-vous en tant que membre de ce canal et vérifiez que le même mot est trouvé

S'il n'est pas trouvé à l'étape 5, vérifiez que le nom d'utilisateur Fess correspond à l'adresse e-mail Slack, et que ``fess-crawler.log`` ne contient pas l'avertissement ``private channel(s) skipped``.
Si une configuration échoue dans son ensemble, par exemple à cause d'une erreur d'authentification, l'échec est enregistré par configuration dans [Informations système] > [URL d'échec].

Résumé
======

- Pour Git, indiquez toujours ``base_url`` et ajoutez ``time_to_live`` pour que les documents n'expirent pas en exploration différentielle.
- Pour Confluence et Jira, importez aussi les commentaires avec ``content.comments`` / ``issue.comments``, et écrivez le JQL dans ``jira.jql``.
- Pour Slack, construisez le titre à partir de ``message.user`` et ``message.channel``.
- Git, Confluence et Jira ne transposent pas les droits d'origine ; définissez donc la portée avec le champ « Autorisations » et le périmètre d'import.
- Placez les canaux privés Slack dans une configuration distincte, et importez-les avec ``permission_sync=true``, ``role=message.roles`` et un champ « Autorisations » vide.
- Ajustez la priorité de chaque source d'information avec le « Boost » de sa configuration de magasin de données.

Références
==========

- `Connecteur Git <https://fess.codelibs.org/fr/stable/config/datastore/ds-git.html>`__
- `Connecteur Atlassian <https://fess.codelibs.org/fr/stable/config/datastore/ds-atlassian.html>`__
- `Connecteur Slack <https://fess.codelibs.org/fr/stable/config/datastore/ds-slack.html>`__
- `Crawl de magasin de données <https://fess.codelibs.org/fr/stable/admin/dataconfig-guide.html>`__
- `Général <https://fess.codelibs.org/fr/stable/admin/general-guide.html>`__
- `README de fess-ds-slack 15.9.0 (scopes et synchronisation des autorisations) <https://github.com/codelibs/fess-ds-slack/blob/fess-ds-slack-15.9.0/README.md>`__
