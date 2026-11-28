===============================================
Rechercher dans Google Drive, SharePoint et Box
===============================================

Introduction
============

Lorsque les services utilisent tour à tour Google Drive, SharePoint Online et Box, on passe de plus en plus de temps à se demander où un document a été rangé.
Avec les plugins de magasin de données de Fess, les fichiers des trois services deviennent consultables depuis une seule page de recherche.

Le stockage cloud mélange toutefois des fichiers dont les droits d'accès diffèrent.
Une erreur de configuration peut faire apparaître des fichiers confidentiels, comme des contrats, dans les résultats de recherche d'utilisateurs qui ne sont même pas connectés.
Cet article présente, pour chaque service, une configuration minimale qui fonctionne telle quelle, ainsi que la façon de reporter les autorisations d'origine dans Fess.

Les étapes communes à tous les magasins de données — installation des plugins, noms de gestionnaire, paramètres, écriture des scripts et création des tâches — sont regroupées dans :doc:`datastore-basics`.
Lisez d'abord cet article avant de continuer.
Les valeurs de configuration de cet article correspondent à Fess 15.9 et à la version 15.9.0 de chaque plugin.

Ce que nous allons construire
=============================

.. list-table::
   :header-rows: 1
   :widths: 18 22 22 38

   * - Service
     - Plugin
     - Nom du gestionnaire
     - À préparer côté service
   * - Google Drive
     - ``fess-ds-gsuite``
     - ``GoogleDriveDataStore``
     - Une clé JSON de compte de service et la délégation au niveau du domaine
   * - SharePoint Online
     - ``fess-ds-microsoft365``
     - ``OneDriveDataStore``
     - Une inscription d'application dans Entra ID (secret client) et des autorisations d'application Microsoft Graph
   * - Box
     - ``fess-ds-box``
     - ``BoxDataStore``
     - Une application personnalisée Box avec authentification JWT

Si Fess tourne sous Docker, indiquez les noms et versions des plugins, séparés par des espaces, dans la variable d'environnement ``FESS_PLUGINS`` pour les installer tous au démarrage.

.. code-block:: yaml

    environment:
      - FESS_PLUGINS=fess-ds-gsuite:15.9.0 fess-ds-microsoft365:15.9.0 fess-ds-box:15.9.0

Si vous les installez depuis l'interface d'administration ou avec ``fess-setup``, redémarrez Fess après l'installation (``FESS_PLUGINS`` installe les plugins avant le démarrage de Fess, aucun redémarrage n'est donc nécessaire).

À décider d'abord : qui peut voir les résultats
===============================================

Lorsque vous créez une nouvelle configuration de magasin de données, le champ « Autorisations » contient déjà ``{role}guest``.
Si cette valeur reste en place, les fichiers importés sont trouvables par les utilisateurs non connectés.
Les trois plugins placent dans ``file.roles`` les rôles construits à partir des paramètres de partage d'origine.
La configuration est donc identique pour les trois sur ces deux points :

- Supprimer ``{role}guest`` du champ « Autorisations » et le laisser vide
- Écrire ``role=file.roles`` dans le script

Ces deux points sont nécessaires parce que les plugins traitent le champ « Autorisations » différemment.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Plugin
     - Valeur du champ « Autorisations »
     - Paramètre ``default_permissions``
   * - Google Drive
     - Non utilisée si vous écrivez ``role=file.roles``. Sinon, la valeur du champ (initialement ``{role}guest``) est attachée telle quelle à tous les fichiers
     - Utilisé uniquement pour les fichiers dont l'ACL Drive n'a rien fourni. S'il n'est pas défini non plus, ces fichiers ne sont pas importés
   * - SharePoint (OneDriveDataStore)
     - Fusionnée dans ``file.roles``. Laisser ``{role}guest`` rend tous les fichiers publics
     - Ajouté à tous les fichiers
   * - Box
     - Fusionnée dans ``file.roles``. Laisser ``{role}guest`` rend tous les fichiers publics
     - Ajouté à tous les fichiers

``file.roles`` contient des chaînes qui représentent les utilisateurs et les groupes de chaque service.

- Google Drive : les utilisateurs et les groupes sont des adresses e-mail, et les propriétaires de fichiers ont le même format. Le partage au niveau du domaine devient ``{group}<nom-de-domaine>`` (modifiable avec ``domain_permission_format``), et le partage public trouvable par la recherche (``anyone``) devient le rôle ``guest``. Un partage limité aux personnes disposant du lien ne devient pas un rôle.
- SharePoint : les utilisateurs sont leur ID d'objet et leur UPN, les groupes leur ID et leur nom d'affichage. Un lien de partage destiné aux « personnes de votre organisation » devient le groupe ``EVERYONE_IN_TENANT``.
- Box : les utilisateurs sont leur ID utilisateur Box et leur identifiant de connexion (adresse e-mail), les groupes leur ID de groupe Box. Outre les collaborations du fichier lui-même, les collaborations et les propriétaires des dossiers parents sont inclus.

Lors de la recherche, ces valeurs sont comparées au nom d'utilisateur et aux noms de groupe de l'utilisateur connecté à Fess.
Par exemple, pour que les autorisations utilisateur de Google Drive s'appliquent, le nom d'utilisateur Fess doit correspondre à l'adresse e-mail.
Pour le fonctionnement des rôles, voir :doc:`guide-05` ; pour la connexion par SSO, voir :doc:`guide-15`.

La configuration de magasin de données n'a pas de champ dédié aux étiquettes qui permettent de filtrer les résultats par service.
Ajoutez au script une ligne comme ``label="box"``, ou créez une étiquette qui correspond aux URL (pour plus de détails, voir :doc:`datastore-basics`).
Les valeurs d'étiquette ne peuvent contenir que des caractères alphanumériques et ``_`` ; une valeur avec un trait d'union comme ``google-drive`` ne peut pas être créée.

Google Drive : importer les Drive partagés
==========================================

Préparation côté Google
-----------------------

Dans la version 15.9, ``fess-ds-gsuite`` fonctionne par défaut avec ``crawl_target=shared_drives``.
Il lit tous les Drive partagés du domaine en se faisant passer pour un administrateur du domaine.

1. Créez un projet dans la console Google Cloud et activez l'API Google Drive
2. Créez un compte de service, puis créez et téléchargez une clé au format JSON dans l'onglet [Keys]
3. Activez la délégation au niveau du domaine pour le compte de service et notez son ID client OAuth 2
4. Dans la console d'administration Google Workspace, sous [Security] > [Access and data control] > [API controls] > [Domain-wide delegation], autorisez cet ID client pour le champ d'application ``https://www.googleapis.com/auth/drive.readonly``

Le compte indiqué dans ``impersonate_user`` doit être un administrateur du domaine Google Workspace.
Si ``crawl_target`` vaut autre chose que ``legacy`` et que ``impersonate_user`` est absent, l'exploration s'arrête sur une erreur dès son démarrage.

Paramètres et script
--------------------

Dans [Robot d'exploration] > [Magasin de données] > [Créer nouveau], sélectionnez ``GoogleDriveDataStore`` comme « Nom du gestionnaire » et videz le champ « Autorisations ».
Recopiez dans ``private_key``, ``private_key_id`` et ``client_email`` les valeurs de même nom de la clé JSON.
Écrivez ``private_key`` sur une seule ligne en conservant les sauts de ligne sous la forme ``\n``.

.. code-block:: properties

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBg...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com
    impersonate_user=admin@example.com
    crawl_target=shared_drives
    script_type=javascript

.. code-block:: properties

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created_time
    last_modified=file.modified_time
    role=file.roles

``file.url`` est le ``webViewLink`` du fichier.
La prise en compte des suppressions suppose que l'URL indexée contienne l'ID de fichier Drive.
Utilisez donc ``url`` tel quel, sans le réécrire.

Les autres périmètres d'importation sont les suivants.

- ``crawl_target=users`` : lit le « Mon Drive » de tous les utilisateurs. Il faut activer l'API Admin SDK et ajouter le champ d'application ``https://www.googleapis.com/auth/admin.directory.user.readonly`` (à la fois dans la délégation et dans le paramètre ``scopes``).
- ``crawl_target=legacy`` : lit uniquement les fichiers partagés directement avec l'adresse du compte de service. Ni la délégation ni ``impersonate_user`` ne sont nécessaires.

Exploration incrémentale
------------------------

Si vous ajoutez ``incremental=true``, les explorations suivantes ne lisent plus que le flux de modifications de Drive.
Dans ce mode, ``delete_old_docs`` est forcé à ``false``, et des fichiers supprimés de Drive peuvent rester dans l'index.
De plus, les fichiers inchangés ne sont pas réenregistrés : sans autre mesure, ils disparaissent des résultats de recherche une fois écoulé le nombre de jours de « Supprimer les anciens documents » (3 jours par défaut) (voir la section sur l'expiration des documents dans :doc:`datastore-basics`).

Si vous utilisez l'exploration incrémentale, combinez-la comme suit.

- Créez aussi une configuration d'exploration complète sans ``incremental`` et exécutez-la régulièrement, par exemple une fois par semaine
- Indiquez dans les deux configurations un ``time_to_live`` un peu plus long que l'intervalle de l'exploration complète (pour une exploration complète hebdomadaire, ``time_to_live=11520``, soit 8 jours)

Les fichiers supprimés de Drive disparaissent des résultats de recherche à l'expiration de ce délai.
Le plugin réécrit la position du flux de modifications dans le champ « Paramètres » ; ne modifiez pas la valeur ainsi réécrite.

SharePoint Online : importer les fichiers des bibliothèques de documents
========================================================================

Quel gestionnaire utiliser
--------------------------

Pour rechercher dans le contenu des fichiers des bibliothèques de documents SharePoint, utilisez ``OneDriveDataStore`` de ``fess-ds-microsoft365``.

- ``SharePointDocLibDataStore`` enregistre seulement chaque bibliothèque comme un document unique et n'importe pas les fichiers qu'elle contient.
- ``fess-ds-sharepoint`` (``SharePointDataStore``) est destiné à SharePoint Server sur site. Il ne prend pas en charge Microsoft Graph et sa documentation renvoie vers ``fess-ds-microsoft365`` pour SharePoint Online.

Préparation côté Entra ID
-------------------------

1. Créez une nouvelle inscription sous [App registrations] dans le portail Azure
2. Sous [Certificates & secrets], créez un nouveau secret client et notez sa valeur (c'est ici que vous choisissez sa date d'expiration)
3. Sous [API permissions] > [Microsoft Graph] > [Application permissions], ajoutez les quatre autorisations ci-dessous
4. Exécutez [Grant admin consent]

Ajoutez les autorisations d'application suivantes.

- ``Files.Read.All``
- ``User.Read.All``, ``Group.Read.All`` : nécessaires quel que soit le périmètre d'importation pour résoudre les noms d'utilisateur et de groupe des ACL
- ``Sites.Read.All`` : nécessaire pour énumérer les sites avec ``shared_documents_drive_crawler=true``

Paramètres et script
--------------------

Sans paramètre particulier, ``OneDriveDataStore`` lit tous les sites SharePoint, ainsi que le OneDrive de tous les utilisateurs et les drives de tous les groupes Microsoft 365.
Pour ne cibler que SharePoint, définissez explicitement les trois indicateurs.

.. code-block:: properties

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your-client-secret
    shared_documents_drive_crawler=true
    user_drive_crawler=false
    group_drive_crawler=false
    script_type=javascript

.. code-block:: properties

    url=file.web_url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created
    last_modified=file.last_modified
    role=file.roles

Pour vous limiter à certaines bibliothèques, mettez les trois indicateurs à ``false`` et indiquez l'ID du drive dans ``drive_id``.
Vous trouverez l'ID du drive avec ``GET /sites/{site-id}/drives`` dans Microsoft Graph.
Si vous indiquez seulement ``drive_id`` en conservant les indicateurs, ce drive est simplement « ajouté » à l'importation globale.

Autorisations manquantes et nouvelles tentatives
------------------------------------------------

L'ACL d'un fichier est obtenue par un appel Graph distinct pour chaque fichier.
Le comportement en cas d'échec de cet appel est déterminé par ``permission_failure_policy``.
Avec la valeur par défaut ``skip``, le fichier n'est pas enregistré et il est consigné dans [Informations système] > [URL d'échec] ainsi que dans un journal WARN.
Avec ``index_without_acl``, les fichiers sont enregistrés avec une ACL incomplète ; pour des bibliothèques très confidentielles, il est donc plus sûr de garder la valeur par défaut.

Les nouvelles tentatives d'appels Graph se règlent avec ``max_retry_count`` (3 par défaut, 10 au maximum) et ``retry_interval`` (en secondes, 3 par défaut, 180 au maximum).
``OneDriveDataStore`` n'a pas d'option d'exploration incrémentale et lit tout à chaque fois.

Box : importer un dossier de contrats avec ses autorisations
============================================================

Préparation côté Box
--------------------

``fess-ds-box`` ne prend en charge que l'authentification serveur par JWT.

1. Dans la Box Developer Console, créez une « Custom App » et choisissez « Server Authentication (with JWT) » comme méthode d'authentification
2. Dans l'onglet [Configuration], activez « Read all files and folders stored in Box » sous Application Scopes
3. Choisissez « App + Enterprise Access » comme App Access Level
4. Générez une paire de clés avec [Generate a Public/Private Keypair] et enregistrez le fichier JSON
5. Autorisez l'application dans la console d'administration Box

Les valeurs ``clientID``, ``clientSecret``, ``publicKeyID``, ``privateKey``, ``passphrase`` et ``enterpriseID`` du fichier JSON correspondent respectivement à ``client_id``, ``client_secret``, ``public_key_id``, ``private_key``, ``passphrase`` et ``enterprise_id``.
Les six sont obligatoires.

Limiter l'importation à un seul dossier
---------------------------------------

Lorsque la cible est déterminée, comme les contrats du service juridique, lisez un seul dossier avec ``root_folder_id``.
Dans ce mode, le plugin ne se fait pas passer pour les utilisateurs : il lit le dossier en tant que compte de service de l'application.
Vous devez donc ajouter le compte de service comme collaborateur du dossier cible.
L'ID de dossier est le nombre situé à la fin de l'URL lorsque vous ouvrez le dossier dans l'interface web de Box.

.. code-block:: properties

    client_id=hdf8a7sd9f8a7sdf9a87sdf98a7sd
    client_secret=kMN7sd8f7a9sd8f7a9sd8f7a9sd8f
    public_key_id=4tg5h6j7
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDj...\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=7ba8sd9f7a9sd8f7a9sd8f7a9sd8f
    enterprise_id=1923456
    root_folder_id=123456789
    default_permissions={group}legal
    script_type=javascript

.. code-block:: properties

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at
    role=file.roles

Supprimez impérativement ``{role}guest`` du champ « Autorisations ».
Dans Box, la valeur du champ est fusionnée dans ``file.roles`` ; si vous la laissez, les contrats sont trouvables par les utilisateurs non connectés.

Les groupes Box deviennent des rôles sous forme d'ID de groupe et ne correspondent donc pas tels quels aux noms de groupe de Fess.
Dans cet exemple, ``default_permissions={group}legal`` rend tous les fichiers visibles au groupe Fess ``legal``.
Les utilisateurs avec qui un fichier est partagé individuellement dans Box peuvent en plus le trouver, à condition que leur identifiant de connexion (adresse e-mail) corresponde à leur nom d'utilisateur Fess.
Pour ajouter un rôle aux fichiers dotés d'un lien partagé à l'échelle de l'entreprise, utilisez ``company_shared_link_role``.

Lire les fichiers de tous les utilisateurs
------------------------------------------

Si vous omettez ``root_folder_id``, le plugin énumère tous les utilisateurs de l'entreprise et lit leurs fichiers en se faisant passer pour chacun d'eux tour à tour.
Vous pouvez restreindre les utilisateurs ciblés avec ``filter_term``.
Les appels d'API en se faisant passer pour un utilisateur doivent être autorisés dans les paramètres de l'application côté Box ; vérifiez ces paramètres dans la documentation développeur de Box.

Gérer les limites de débit
--------------------------

Le nombre de nouvelles tentatives pour les réponses ``429`` et ``5xx`` est ``max_retry_attempts`` (5 par défaut).
``max_retry_count`` (10 par défaut) est le nombre de fois où la connexion est recréée sur une réponse ``401`` ; il n'a rien à voir avec les limites de débit.
Pour espacer les appels d'API, définissez une attente par élément avec ``readInterval`` (en millisecondes).
``fess-ds-box`` n'a pas d'option d'exploration incrémentale.

Points d'exploitation
=====================

Expiration des identifiants
---------------------------

- Un secret client Entra ID a la date d'expiration choisie à sa création. Une fois expiré, l'authentification échoue et plus rien n'est importé ; créez donc un nouveau secret avant l'expiration et remplacez ``client_secret`` dans les paramètres.
- Les jetons d'accès Google sont renouvelés automatiquement par la bibliothèque qu'utilise le plugin. Dans la version 15.9, ``refresh_token_interval`` est ignoré et un avertissement est journalisé.
- Les jetons d'accès Box sont renouvelés automatiquement toutes les ``refresh_token_interval`` secondes (3540 par défaut).

Quand tout n'est pas importé
----------------------------

À la fin d'une exploration, les trois plugins attendent par défaut 60 secondes la fin de leurs threads de travail, et ce qui n'est pas terminé n'est pas importé.
Si des documents manquent sur un grand locataire, allongez ce délai d'attente.
Le paramètre s'appelle ``thread_pool_timeout_seconds`` pour Google Drive, ``executor_shutdown_timeout`` pour SharePoint et ``thread_pool_await_timeout`` pour Box (tous en secondes).

Dans Google Drive, les réponses 429, 500, 502, 503 et 504 ainsi que les réponses 403 dues aux limites de débit sont relancées avec un délai exponentiel.
Les nouvelles tentatives se règlent avec ``max_retries`` (5 par défaut), ``retry_initial_interval_ms`` (1000 par défaut) et ``max_backoff_ms`` (32000 par défaut).

Vérifier le fonctionnement
==========================

La lecture des résultats de tâche et des journaux est expliquée dans :doc:`datastore-basics`.
Lors de l'exploration d'un magasin de données, une tâche peut s'afficher « OK » même si la récupération de fichiers a échoué ; jugez donc d'après le nombre de documents et les journaux.
Pour la configuration de cet article, vérifiez en plus les trois points suivants.

1. Déconnecté, recherchez un mot contenu dans un fichier importé et vérifiez qu'aucun résultat n'apparaît (pour vous assurer que le champ « Autorisations » a bien été vidé)
2. Connectez-vous avec un utilisateur avec qui le fichier est partagé et vérifiez que le même fichier apparaît
3. Pour la configuration Google Drive, vérifiez que ``fess-crawler.log`` ne contient pas ``Skipped ... because no permission could be resolved`` (ce sont des fichiers non importés parce que leur ACL était vide)

Si le fichier n'apparaît pas à l'étape 2, vérifiez que le nom d'utilisateur et les noms de groupe de l'utilisateur correspondent aux valeurs de ``file.roles``.

Résumé
======

- Importez le contenu des fichiers SharePoint avec ``OneDriveDataStore`` et mettez OneDrive et les drives de groupe à ``false`` si vous n'en avez pas besoin.
- Pour les trois services, supprimez ``{role}guest`` du champ « Autorisations » et écrivez ``role=file.roles`` dans le script.
- ``default_permissions`` remplace une ACL vide dans Google Drive et s'ajoute à tous les fichiers dans SharePoint et Box.
- Seul Google Drive propose l'exploration incrémentale (``incremental=true``). Si vous l'utilisez, combinez-la avec une configuration d'exploration complète et indiquez ``time_to_live`` dans les deux.

Références
==========

- `Connecteur Google Workspace <https://fess.codelibs.org/fr/stable/config/datastore/ds-gsuite.html>`__
- `Connecteur Microsoft 365 <https://fess.codelibs.org/fr/stable/config/datastore/ds-microsoft365.html>`__
- `Connecteur Box <https://fess.codelibs.org/fr/stable/config/datastore/ds-box.html>`__
- `Configuration du magasin de données <https://fess.codelibs.org/fr/stable/admin/dataconfig-guide.html>`__
- `README de fess-ds-microsoft365 15.9.0 (liste des autorisations Graph) <https://github.com/codelibs/fess-ds-microsoft365/blob/fess-ds-microsoft365-15.9.0/README.md>`__
- `README de fess-ds-box 15.9.0 (file.roles et root_folder_id) <https://github.com/codelibs/fess-ds-box/blob/fess-ds-box-15.9.0/README.md>`__
