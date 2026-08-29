==================================
Connecteur Google Workspace
==================================

Aperçu
======

Le connecteur Google Workspace fournit la fonctionnalité permettant de récupérer les fichiers
depuis Google Drive (anciennement G Suite) et de les enregistrer dans l'index |Fess|.

Cette fonctionnalité nécessite le plugin ``fess-ds-gsuite``.

Modifications dans la version 15.9
==================================

Le connecteur a été profondément remanié dans |Fess| 15.9. Lisez cette section avant de
mettre à niveau une configuration de data store existante.

.. warning::

   ``crawl_target`` vaut désormais ``shared_drives`` par défaut, et toute valeur autre que
   ``legacy`` exige ``impersonate_user``. Une configuration existante mise à niveau sans
   modification **échoue donc au démarrage** avec une ``DataStoreException`` au lieu de
   s'exécuter.

   C'est délibéré : le comportement précédent n'atteignait que les fichiers explicitement
   partagés avec le compte de service, si bien que l'alternative serait un crawl qui
   n'indexe silencieusement rien. Définissez ``impersonate_user`` sur un compte
   d'administrateur de domaine, ou définissez ``crawl_target=legacy`` pour conserver le
   comportement précédent.

Changements de comportement
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Changement
     - Action requise
   * - ``crawl_target`` vaut ``shared_drives`` par défaut et exige ``impersonate_user``
     - Définissez ``impersonate_user``, ou définissez ``crawl_target=legacy``. Sinon, le crawl échoue au démarrage.
   * - Le scope OAuth par défaut est passé de ``https://www.googleapis.com/auth/drive`` à ``https://www.googleapis.com/auth/drive.readonly``
     - Mettez à jour l'entrée de délégation à l'échelle du domaine dans la console d'administration Google Workspace, qui énumère explicitement les scopes.
   * - ``crawl_target=users`` et ``crawl_target=both`` exigent en plus ``https://www.googleapis.com/auth/admin.directory.user.readonly``
     - Ajoutez le scope à la fois au paramètre ``scopes`` et à l'entrée de délégation. Ceci est vérifié au démarrage.
   * - L'URL indexée est désormais ``webViewLink`` (le lien ouvrable dans le navigateur) au lieu du lien de téléchargement
     - Effectuez un crawl complet pour prendre en compte les nouvelles URL.
   * - ``default_permissions`` est désormais une valeur de repli, et non un ajout
     - Un document dont l'ACL peut être résolue reçoit uniquement cette ACL, et non plus l'union avec ``default_permissions``. Le résultat est strictement plus restrictif.
   * - Le partage par lien seul n'accorde plus de rôle de recherche
     - Une permission ``domain`` ou ``anyone`` avec ``allowFileDiscovery=false`` signifie « toute personne disposant du lien », ce que Drive lui-même ne rend pas non plus détectable par la recherche.
   * - Un document dont l'ACL ne donne rien est ignoré au lieu d'être indexé sans rôle
     - Définissez ``default_permissions`` pour continuer à indexer ces documents. Auparavant, ils étaient visibles par tous les utilisateurs, car une liste de rôles vide désactive le filtre de permissions.
   * - ``fields`` ne vaut plus ``*`` par défaut, mais une liste de champs explicite
     - Un script de crawl qui référence un champ inhabituel lit désormais null. Définissez ``fields=*`` pour rétablir la projection précédente.
   * - Les Google Docs sont exportés en Markdown au lieu de texte brut, et les Google Sheets en TSV au lieu de CSV
     - Le texte indexé de chaque Google Doc contient désormais des caractères de syntaxe Markdown. Effectuez un crawl complet.
   * - ``refresh_token_interval`` est ignoré
     - Le renouvellement des jetons est assuré par la bibliothèque d'authentification. Une configuration existante continue de fonctionner, et un avertissement est journalisé.
   * - Google Forms et Google Sites ne sont indexés que par leurs métadonnées
     - Ils n'ont pas de format d'export dans l'API Drive. Auparavant, chacun d'eux produisait une erreur de crawl.

Nouvelles fonctionnalités
-------------------------

- ``crawl_target`` sélectionne ce qui est crawlé : la vue propre du compte de service
  (``legacy``), tous les Drive partagés du domaine (``shared_drives``), le Mon Drive de
  chaque utilisateur de l'annuaire (``users``), ou les deux (``both``). Voir
  `Cible du crawl`_.
- Les éléments des Drive partagés reçoivent désormais l'ACL correcte. Voir
  `Permissions et contrôle d'accès`_.
- Crawl incrémentiel via le flux de modifications de Drive. Voir `Crawl incrémentiel`_.
- Limitation de débit avec un back-off exponentiel qui honore ``Retry-After``, et un Drive
  partagé ou un utilisateur en échec qui n'interrompt plus l'ensemble du crawl. Voir
  `Limitation de débit et nouvelles tentatives`_.
- ``proxy_username`` et ``proxy_password`` pour un proxy avec authentification.

Services pris en charge
=======================

- Google Drive (Mon Drive, Drive partagés)
- Google Docs, Sheets, Slides, Drawings, Apps Script
- Google Forms et Google Sites (métadonnées uniquement ; ils n'ont pas de format d'export)

Prérequis
=========

1. L'installation du plugin est requise
2. La création d'un projet Google Cloud Platform est nécessaire
3. La création d'un compte de service et l'obtention des identifiants sont nécessaires
4. La configuration de la délégation à l'échelle du domaine Google Workspace est nécessaire
5. Sauf si ``crawl_target=legacy`` est utilisé, un compte d'administrateur Google Workspace
   à emprunter est nécessaire

Installation du plugin
----------------------

Méthode 1 : Placement direct du fichier JAR

::

    # Telecharger depuis Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-gsuite/X.X.X/fess-ds-gsuite-X.X.X.jar

    # Placement
    cp fess-ds-gsuite-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # ou
    cp fess-ds-gsuite-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Méthode 2 : Installation depuis l'interface d'administration

1. Ouvrir "Système" -> "Plugins"
2. Télécharger le fichier JAR
3. Redémarrer |Fess|

Configuration
=============

Configurez depuis l'interface d'administration via "Crawler" -> "Data Store" -> "Nouveau".

Configuration de base
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Élément
     - Exemple
   * - Nom
     - Company Google Drive
   * - Nom du gestionnaire
     - GoogleDriveDataStore
   * - Active
     - Oui

Configuration des paramètres
----------------------------

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com
    impersonate_user=admin@example.com

Liste des paramètres
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``private_key``
     - Oui
     - Clé privée du compte de service (format PEM, sauts de ligne en ``\n``)
   * - ``private_key_id``
     - Oui
     - ID de la clé privée
   * - ``client_email``
     - Oui
     - Adresse email du compte de service
   * - ``impersonate_user``
     - Conditionnel
     - Le compte Google Workspace emprunté via la délégation à l'échelle du domaine. Requis sauf si ``crawl_target=legacy`` ; sans lui, le crawl échoue au démarrage. ``shared_drives`` et ``both`` énumèrent les Drive partagés avec un accès d'administrateur de domaine, ce compte doit donc être administrateur du domaine.
   * - ``crawl_target``
     - Non
     - Ce qui est crawlé : ``legacy``, ``shared_drives``, ``users`` ou ``both``. Par défaut : ``shared_drives``. Voir `Cible du crawl`_.
   * - ``scopes``
     - Non
     - Scopes OAuth, séparés par des virgules. Par défaut : ``https://www.googleapis.com/auth/drive.readonly``. ``crawl_target=users`` et ``crawl_target=both`` exigent en plus ``https://www.googleapis.com/auth/admin.directory.user.readonly``.
   * - ``user_query``
     - Non
     - ``query`` de l'Admin SDK utilisée pour restreindre les utilisateurs énumérés par ``crawl_target=users`` et ``crawl_target=both``. Par défaut : non défini (tous les utilisateurs du client).
   * - ``query``
     - Non
     - Chaîne de requête de recherche de l'API Google Drive. N'est pas appliquée au flux de modifications utilisé par le crawl incrémentiel.
   * - ``corpora``
     - Non
     - Corpus à rechercher. Par défaut : ``allDrives``. Utilisé uniquement par ``crawl_target=legacy``, il n'a donc aucun effet avec la cible par défaut : ``shared_drives`` liste chaque Drive avec ``drive`` et ``users`` liste chaque Mon Drive avec ``user``, les deux étant fixés.
   * - ``spaces``
     - Non
     - Espaces à rechercher (paramètre ``spaces`` de l'API Google Drive, par ex. ``drive``, ``appDataFolder``). Par défaut : non défini (valeur par défaut de l'API). Utilisé par ``crawl_target=legacy`` et ``users`` ; ignoré pour ``shared_drives``.
   * - ``fields``
     - Non
     - Champs de fichier à demander à l'API Google Drive. La valeur par défaut n'est **pas** ``*``, mais une liste de champs explicite. Elle couvre tous les champs nécessaires au contexte de script, à la résolution des ACL, à l'URL d'index et au crawl incrémentiel ; un champ absent de cette liste vaut null dans le script de crawl. Définissez ``fields=*`` pour demander tous les champs, comme dans les versions précédentes.
   * - ``default_permissions``
     - Non
     - Permissions utilisées lorsque l'ACL Drive d'un document ne donne rien (séparées par des virgules, ex : ``{role}drive-users``). C'est une valeur de repli, et non un ajout : un document dont l'ACL peut être résolue reçoit uniquement cette ACL.
   * - ``max_size``
     - Non
     - Taille maximale des fichiers à indexer (en octets). Par défaut : ``10000000`` (environ 10 Mo)
   * - ``number_of_threads``
     - Non
     - Nombre de threads de traitement parallèle. Par défaut : ``1``
   * - ``incremental``
     - Non
     - Indique s'il faut crawler via le flux de modifications de Drive au lieu de tout lister. Par défaut : ``false``. La valeur est lue directement dans le champ de paramètres de la configuration du data store, avant le démarrage du crawl. Voir `Crawl incrémentiel`_.

Paramètres avancés
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Paramètre
     - Description
   * - ``domain_permission_format``
     - Format de rôle appliqué à une permission Drive de type ``domain``. ``{domain}`` est remplacé par le nom de domaine. Par défaut : ``{group}{domain}``
   * - ``thread_pool_timeout_seconds``
     - Durée d'attente de la fin des threads de traitement à l'issue d'un crawl (secondes). Par défaut : ``60``
   * - ``page_size``
     - Taille de page pour ``files.list`` et ``changes.list``. Par défaut : ``1000`` ; les valeurs supérieures à ``1000`` sont ramenées à cette limite.
   * - ``permission_page_size``
     - Taille de page pour ``permissions.list`` et ``drives.list``. Par défaut : ``100`` ; les valeurs supérieures à ``100`` sont ramenées à cette limite.
   * - ``max_cached_content_size``
     - Taille maximale (en octets) du contenu conservé en mémoire ; un contenu plus volumineux est déchargé dans un fichier temporaire. Par défaut : ``1048576`` (1 Mo).
   * - ``max_retries``
     - Nombre maximal de nouvelles tentatives pour un appel de l'API Drive limité ou temporairement en échec. Par défaut : ``5``
   * - ``retry_initial_interval_ms``
     - Intervalle de back-off initial avant la première nouvelle tentative (millisecondes). Par défaut : ``1000``
   * - ``max_backoff_ms``
     - Limite supérieure d'une attente unique (millisecondes). Par défaut : ``32000``
   * - ``read_timeout``
     - Délai de lecture HTTP (en millisecondes). Par défaut : ``20000``
   * - ``connect_timeout``
     - Délai de connexion HTTP (en millisecondes). Par défaut : ``20000``
   * - ``proxy_host``
     - Nom d'hôte du serveur proxy. Le proxy n'est utilisé que si ``proxy_host`` et ``proxy_port`` sont tous deux définis ; l'un sans l'autre n'a aucun effet.
   * - ``proxy_port``
     - Numéro de port du serveur proxy. Voir ``proxy_host``.
   * - ``proxy_username``
     - Nom d'utilisateur pour un proxy avec authentification. S'il est défini, un en-tête ``Proxy-Authorization`` est ajouté à chaque requête. Voir `Limitations`_ pour ce que cela authentifie ou non.
   * - ``proxy_password``
     - Mot de passe pour un proxy avec authentification
   * - ``ignore_folder``
     - Ignorer les dossiers ou non. Par défaut : ``true``
   * - ``ignore_error``
     - Continuer le traitement en cas d'erreur. Par défaut : ``true``
   * - ``supported_mimetypes``
     - Types MIME à indexer (expression régulière, séparés par des virgules). Par défaut : ``.*`` (tous les types)
   * - ``include_pattern``
     - Expression régulière des URL à inclure dans l'indexation
   * - ``exclude_pattern``
     - Expression régulière des URL à exclure de l'indexation
   * - ``refresh_token_interval``
     - Ignoré depuis la version 15.9. Les jetons d'accès sont renouvelés par la bibliothèque d'authentification. Un réglage existant continue de fonctionner et un avertissement est journalisé.

.. note::

   ``private_key``, ``private_key_id``, ``client_email``, ``proxy_username`` et
   ``proxy_password`` sont retirés du contexte d'évaluation du script : un script de crawl
   ne peut donc pas les indexer et aucun résultat de recherche ne peut les divulguer.

.. note::

   Lorsque le crawl incrémentiel est activé, le connecteur réécrit ``start_page_tokens`` et
   ``crawl_signature`` dans le champ de paramètres de la configuration du data store. Ces
   valeurs sont gérées par le connecteur et apparaissent à côté des paramètres que vous
   définissez ; ne les modifiez pas. Les modifier ou les supprimer amène l'exécution
   suivante à crawler intégralement chaque portée.

Cible du crawl
--------------

Un compte de service ne possède pas de Drive propre et n'appartient à aucun groupe Google :
un crawl qui s'authentifie en tant que compte de service n'atteint donc que les fichiers
explicitement partagés avec l'adresse du compte de service. ``crawl_target`` sélectionne
par conséquent la vue de Drive qui est crawlée.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Valeur
     - Description
   * - ``legacy``
     - La vue propre du compte de service, comme dans les versions précédentes. ``impersonate_user`` n'est pas requis. Seuls les fichiers explicitement partagés avec le compte de service sont trouvés.
   * - ``shared_drives``
     - Valeur par défaut. Tous les Drive partagés du domaine sont énumérés, et chacun est parcouru séparément.
   * - ``users``
     - Tous les utilisateurs de l'annuaire sont énumérés via l'Admin SDK, et le Mon Drive de chacun est parcouru en empruntant son identité.
   * - ``both``
     - ``shared_drives`` puis ``users``. Un fichier présent dans plusieurs portées n'est indexé qu'une seule fois.

Les points suivants sont vérifiés au démarrage du crawl ; une combinaison invalide lève une
``DataStoreException`` au lieu de s'exécuter :

1. ``crawl_target`` doit valoir ``legacy``, ``shared_drives``, ``users`` ou ``both``.
2. ``impersonate_user`` doit être défini sauf si ``crawl_target=legacy``.
3. ``scopes`` doit contenir ``https://www.googleapis.com/auth/admin.directory.user.readonly``
   lorsque ``crawl_target`` vaut ``users`` ou ``both``.

.. note::

   ``shared_drives`` et ``both`` énumèrent les Drive partagés avec un accès d'administrateur
   de domaine : le compte désigné par ``impersonate_user`` doit donc être administrateur du
   domaine Google Workspace. Cette énumération détermine toute la portée du crawl, si bien
   qu'un échec permanent interrompt le crawl au lieu d'être signalé et ignoré : un crawl qui
   n'a énuméré aucun Drive n'a pas réussi partiellement et ne doit pas pouvoir se déclarer
   réussi alors qu'il n'indexe rien.

Crawl incrémentiel
------------------

Définir ``incremental=true`` amène chaque portée -- un Drive partagé, ou la vue d'un
utilisateur dont l'identité est empruntée -- à lire le flux de modifications de Drive au
lieu de tout lister. Une portée sans jeton enregistré est listée intégralement et son flux
de modifications est ancré pour l'exécution suivante.

::

    crawl_target=shared_drives
    impersonate_user=admin@example.com
    incremental=true

.. warning::

   ``delete_old_docs`` est forcé à ``false`` pour toute exécution incrémentielle, et un
   ``delete_old_docs=true`` explicite est écrasé plutôt qu'honoré (un avertissement est
   journalisé). La suppression des documents obsolètes efface tous les documents de la
   configuration que le crawl courant n'a pas touchés, ce qui suppose un crawl complet ; une
   exécution incrémentielle ne touche que les documents modifiés, si bien que cette
   suppression effacerait le reste de l'index.

   Pour supprimer les documents disparus de Drive, planifiez une configuration de data store
   distincte avec ``incremental=false``.

Les jetons ne sont enregistrés que si le crawl s'est terminé et que les threads de
traitement se sont achevés. Un crawl interrompu laisse les jetons intacts, et l'exécution
suivante relit les mêmes modifications.

Les jetons sont également abandonnés, et chaque portée crawlée intégralement, lorsque la
configuration qui détermine ce que produit une portée a changé, c'est-à-dire l'un de
``crawl_target``, ``impersonate_user``, ``user_query``, ``query``, ``corpora`` ou
``spaces``. Un jeton enregistré ne décrit que la population sur laquelle il a été pris ;
le reprendre après un tel changement laisserait un trou permanent dans l'index.

Limitation de débit et nouvelles tentatives
-------------------------------------------

Un appel de l'API Drive limité ou temporairement en échec est retenté avec un back-off
exponentiel, borné par ``max_retries``, ``retry_initial_interval_ms`` et ``max_backoff_ms``.
Un en-tête ``Retry-After`` prime sur l'attente exponentielle, mais il est plafonné par
``max_backoff_ms`` afin qu'un en-tête erroné ne puisse pas bloquer le crawl pendant des
heures. Seule la forme en secondes de ``Retry-After`` est honorée ; une date HTTP retombe
sur l'attente exponentielle.

``429``, ``500``, ``502``, ``503`` et ``504`` sont toujours retentés. Un ``403`` n'est
retenté que s'il s'agit d'une erreur de limitation de débit ; tout autre ``403`` est un
échec d'autorisation qu'une nouvelle tentative ne peut pas résoudre, et il est signalé
immédiatement.

Un listage de fichiers qui n'a pas pu aboutir n'interrompt plus l'ensemble du crawl : les
Drive partagés et les utilisateurs restants sont toujours crawlés, et l'échec est inscrit
dans le journal du crawler ainsi que dans la liste des URL en échec de l'interface
d'administration.

Configuration du script
-----------------------

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.url
    thumbnail=file.thumbnail_link
    content_length=file.size
    filetype=file.filetype
    role=file.roles
    filename=file.name

Champs disponibles
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``file.name``
     - Nom du fichier
   * - ``file.description``
     - Description du fichier
   * - ``file.contents``
     - Contenu textuel du fichier
   * - ``file.mimetype``
     - Type MIME du fichier
   * - ``file.filetype``
     - Type de fichier
   * - ``file.created_time``
     - Date de création
   * - ``file.modified_time``
     - Date de dernière modification
   * - ``file.web_view_link``
     - Lien pour ouvrir dans le navigateur
   * - ``file.url``
     - URL du fichier. Il s'agit de ``webViewLink`` ; lorsqu'un fichier n'en a pas, ``https://drive.google.com/open?id=<ID du fichier>`` est utilisé à la place.
   * - ``file.thumbnail_link``
     - Lien vers la miniature (valide temporairement)
   * - ``file.size``
     - Taille du fichier (octets)
   * - ``file.roles``
     - Permissions d'accès

.. note::

   Seuls les champs listés dans le paramètre ``fields`` sont renseignés. Un champ non
   demandé vaut null dans le script. Définissez ``fields=*`` pour demander tous les champs,
   comme dans les versions précédentes.

Pour plus de détails, consultez `Google Drive Files API <https://developers.google.com/drive/api/v3/reference/files>`_.

Extraction de texte des types Google natifs
-------------------------------------------

Un type Google natif ne peut pas être téléchargé et doit être exporté. La cible d'export est
choisie parmi les formats d'export que l'API Drive signale réellement, et non dans une table
figée, et un export est limité à 10 Mo.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Type
     - Exporté en
   * - Google Docs
     - Markdown (``text/markdown``), à défaut texte brut puis HTML
   * - Google Sheets
     - TSV (``text/tab-separated-values``), à défaut CSV
   * - Google Slides
     - Texte brut
   * - Google Drawings
     - PNG. Il n'y a pas de texte à indexer, seules les métadonnées sont donc indexées.
   * - Apps Script
     - Le paquet JSON exporté, dont les sources des scripts sont indexées
   * - Google Forms, Google Sites
     - Non exportables. Les métadonnées sont indexées et aucune erreur n'est signalée.

.. note::

   Comme les Google Docs sont désormais exportés en Markdown, le texte indexé de chaque
   Google Doc contient des caractères de syntaxe Markdown. Un crawl complet est nécessaire
   pour que le changement atteigne les documents déjà indexés.

.. note::

   Les cibles d'export sont lues une fois par crawl depuis l'API Drive. Si cet appel échoue,
   le connecteur retombe sur les conversions que Drive a toujours prises en charge -- texte
   brut pour les Google Docs et CSV pour les Google Sheets -- et journalise un avertissement.

Configuration Google Cloud Platform
===================================

1. Création du projet
---------------------

Accédez à https://console.cloud.google.com/ :

1. Créez un nouveau projet
2. Entrez le nom du projet
3. Sélectionnez l'organisation et l'emplacement

2. Activation de l'API Google Drive
-----------------------------------

Dans "APIs et services" -> "Bibliothèque" :

1. Recherchez "Google Drive API"
2. Cliquez sur "Activer"
3. Activez également "Admin SDK API" si ``crawl_target`` vaut ``users`` ou ``both``

3. Création du compte de service
--------------------------------

Dans "APIs et services" -> "Identifiants" :

1. Sélectionnez "Créer des identifiants" -> "Compte de service"
2. Entrez le nom du compte de service (ex: fess-crawler)
3. Cliquez sur "Créer et continuer"
4. Les rôles ne sont pas nécessaires (ignorez)
5. Cliquez sur "Terminer"

4. Création de la clé du compte de service
------------------------------------------

Pour le compte de service créé :

1. Cliquez sur le compte de service
2. Ouvrez l'onglet "Clés"
3. "Ajouter une clé" -> "Créer une nouvelle clé"
4. Sélectionnez le format JSON
5. Enregistrez le fichier JSON téléchargé

5. Activation de la délégation à l'échelle du domaine
-----------------------------------------------------

Dans les paramètres du compte de service :

1. Cochez "Activer la délégation à l'échelle du domaine"
2. Cliquez sur "Enregistrer"
3. Copiez "l'ID client OAuth 2"

6. Autorisation dans la console d'administration Google Workspace
-----------------------------------------------------------------

Accédez à https://admin.google.com/ :

1. Ouvrez "Sécurité" -> "Accès et contrôle des données" -> "Contrôles d'API"
2. Sélectionnez "Délégation à l'échelle du domaine"
3. Cliquez sur "Ajouter nouveau"
4. Entrez l'ID client
5. Entrez les scopes OAuth :

   ::

       https://www.googleapis.com/auth/drive.readonly

   Lorsque ``crawl_target`` vaut ``users`` ou ``both``, entrez les deux scopes :

   ::

       https://www.googleapis.com/auth/drive.readonly,https://www.googleapis.com/auth/admin.directory.user.readonly

6. Cliquez sur "Autoriser"

.. warning::

   L'entrée de délégation énumère explicitement les scopes : une mise à niveau depuis une
   version antérieure impose donc de la mettre à jour. Le scope par défaut est passé de
   ``https://www.googleapis.com/auth/drive`` à
   ``https://www.googleapis.com/auth/drive.readonly`` en 15.9, et les scopes accordés ici
   doivent correspondre au paramètre ``scopes`` de la configuration du data store.

Configuration des identifiants
==============================

Obtention des informations depuis le fichier JSON
-------------------------------------------------

Fichier JSON téléchargé :

::

    {
      "type": "service_account",
      "project_id": "your-project-id",
      "private_key_id": "46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgk...\n-----END PRIVATE KEY-----\n",
      "client_email": "fess-crawler@your-project.iam.gserviceaccount.com",
      "client_id": "123456789012345678901",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
    }

Configurez les informations suivantes dans les paramètres :

- ``private_key_id`` -> ``private_key_id``
- ``private_key`` -> ``private_key`` (conservez les sauts de ligne en ``\n``)
- ``client_email`` -> ``client_email``

Format de la clé privée
~~~~~~~~~~~~~~~~~~~~~~~

``private_key`` conserve les sauts de ligne en ``\n`` :

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG...\n-----END PRIVATE KEY-----\n

Exemples d'utilisation
======================

Crawl de tous les Drive partagés
--------------------------------

Paramètres :

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=shared_drives
    impersonate_user=admin@example.com

Script :

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link
    thumbnail=file.thumbnail_link
    content_length=file.size
    filetype=file.filetype
    role=file.roles
    filename=file.name

Crawl du Mon Drive de chaque utilisateur
----------------------------------------

Paramètres :

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=users
    impersonate_user=admin@example.com
    scopes=https://www.googleapis.com/auth/drive.readonly,https://www.googleapis.com/auth/admin.directory.user.readonly

Pour restreindre les utilisateurs, ajoutez une requête Admin SDK :

::

    user_query=orgUnitPath=/Sales

Conserver le comportement précédent
-----------------------------------

``crawl_target=legacy`` conserve le parcours antérieur à la version 15.9, dans lequel seuls
les fichiers explicitement partagés avec le compte de service sont trouvés.
``impersonate_user`` n'est pas requis.

Paramètres :

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=legacy

Crawl avec permissions
----------------------

Paramètres :

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=shared_drives
    impersonate_user=admin@example.com
    default_permissions={role}drive-users

Script :

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link
    role=file.roles
    filename=file.name

``default_permissions`` n'est utilisé que pour un document dont l'ACL Drive ne donne rien.

Crawler uniquement certains types de fichiers
---------------------------------------------

Google Docs uniquement :

::

    if (file.mimetype == "application/vnd.google-apps.document") {
        title=file.name
        content=file.description + "\n" + file.contents
        mimetype=file.mimetype
        created=file.created_time
        last_modified=file.modified_time
        url=file.web_view_link
    }

Dépannage
=========

Le crawl ne démarre pas
-----------------------

**Symptôme** : Le crawl se termine immédiatement avec une ``DataStoreException``

**Solution** :

1. ``parameter 'crawl_target' must be one of ...`` : la valeur de ``crawl_target`` n'est ni
   ``legacy``, ni ``shared_drives``, ni ``users``, ni ``both``.
2. ``parameter 'impersonate_user' is required when 'crawl_target' is not 'legacy'`` :
   définissez ``impersonate_user`` sur un compte d'administrateur de domaine, ou définissez
   ``crawl_target=legacy``.
3. ``parameter 'scopes' must include 'https://www.googleapis.com/auth/admin.directory.user.readonly'`` :
   ajoutez ce scope à ``scopes`` et à l'entrée de délégation à l'échelle du domaine.

C'est le résultat attendu lorsqu'une configuration existante est mise à niveau sans
modification. Voir `Modifications dans la version 15.9`_.

Erreur d'authentification
-------------------------

**Symptôme** : ``401 Unauthorized`` ou ``403 Forbidden``

**Points à vérifier** :

1. Vérifier si les identifiants du compte de service sont corrects :

   - Les sauts de ligne de ``private_key`` sont-ils en ``\n`` ?
   - ``private_key_id`` est-il correct ?
   - ``client_email`` est-il correct ?

2. Vérifier si l'API Google Drive est activée
3. Vérifier si la délégation à l'échelle du domaine est configurée
4. Vérifier si l'autorisation a été accordée dans la console d'administration Google Workspace
5. Vérifier si le scope OAuth est correct (``https://www.googleapis.com/auth/drive.readonly``,
   plus ``https://www.googleapis.com/auth/admin.directory.user.readonly`` pour
   ``crawl_target=users`` ou ``both``)

Erreur de délégation à l'échelle du domaine
-------------------------------------------

**Symptôme** : ``Not Authorized to access this resource/api``

**Solution** :

1. Vérifier l'autorisation dans la console d'administration Google Workspace :

   - L'ID client est-il correctement enregistré ?
   - Les scopes OAuth sont-ils corrects ? L'entrée de délégation les énumère explicitement,
     la restriction introduite en 15.9 impose donc de la mettre à jour.

2. Vérifier si la délégation à l'échelle du domaine est activée sur le compte de service
3. Vérifier que le compte désigné par ``impersonate_user`` est administrateur du domaine
   lorsque ``crawl_target`` vaut ``shared_drives`` ou ``both``

Impossible de récupérer les fichiers
------------------------------------

**Symptôme** : Le crawl réussit mais 0 fichiers

**Points à vérifier** :

1. Vérifier que ``crawl_target`` correspond à votre intention. Avec ``legacy``, seuls les
   fichiers explicitement partagés avec le compte de service sont trouvés, car un compte de
   service ne possède pas de Drive propre et n'appartient à aucun groupe.
2. Vérifier si des fichiers existent dans Google Drive
3. Vérifier si le compte de service a les droits de lecture
4. Vérifier si la délégation à l'échelle du domaine est correctement configurée
5. Vérifier si le Drive de l'utilisateur cible est accessible

Des documents sont ignorés
--------------------------

**Symptôme** : ``Skipped ... because no permission could be resolved`` dans le journal du crawler

**Solution** :

L'ACL Drive du document n'a donné aucun rôle de recherche, le document a donc été ignoré au
lieu d'être indexé. Indexer un document sans rôle désactive le filtre de permissions de
|Fess| pour ce document et le rend visible par tous les utilisateurs : c'est pourquoi il est
ignoré. Un document ignoré n'est pas un échec de crawl ; il n'apparaît donc que dans le
journal du crawler, et non dans la liste des URL en échec.

1. Définissez ``default_permissions`` pour indexer ces documents avec une permission de repli
2. Vérifiez que le compte désigné par ``impersonate_user`` est administrateur du domaine,
   afin que les ACL des Drive partagés puissent être lues
3. Vérifiez si le document est partagé par lien seul. Une permission ``domain`` ou
   ``anyone`` avec ``allowFileDiscovery=false`` n'accorde aucun rôle de recherche, car Drive
   lui-même ne rend pas un tel document détectable par la recherche.

Erreur de quota API
-------------------

**Symptôme** : ``403 Rate Limit Exceeded`` ou ``429 Too Many Requests``

**Solution** :

1. Ce type d'échec est retenté automatiquement avec un back-off exponentiel. Augmentez
   ``max_retries`` ou ``max_backoff_ms`` si le crawl échoue toujours.
2. Diminuez ``number_of_threads`` pour réduire le débit de requêtes
3. Vérifier le quota dans Google Cloud Platform
4. Augmenter l'intervalle de crawl
5. Demander une augmentation de quota si nécessaire

Erreur de format de clé privée
------------------------------

**Symptôme** : ``Invalid private key format``

**Solution** :

Vérifier si les sauts de ligne sont correctement en ``\n`` :

::

    # Correct
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n

    # Incorrect (contient des sauts de ligne reels)
    private_key=-----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQE...
    -----END PRIVATE KEY-----

Crawl des Drive partagés
------------------------

.. note::
   Avec ``crawl_target=shared_drives`` (la valeur par défaut), les Drive partagés sont
   énumérés avec un accès d'administrateur de domaine : le compte de service n'a donc pas
   besoin d'être membre de chaque Drive partagé. En revanche, ``impersonate_user`` doit
   désigner un administrateur du domaine.

Avec ``crawl_target=legacy``, le compte de service doit être ajouté à chaque Drive partagé :

1. Ouvrez le Drive partagé dans Google Drive
2. Cliquez sur "Gérer les membres"
3. Ajoutez l'adresse email du compte de service
4. Définissez le niveau de permission sur "Lecteur"

Cas de nombreux fichiers
------------------------

**Symptôme** : Le crawl prend du temps ou expire

**Solution** :

1. Activez ``incremental=true`` afin que seules les modifications depuis l'exécution
   précédente soient crawlées
2. Répartissez les Drive partagés et les utilisateurs dans des configurations de data store
   distinctes plutôt que d'utiliser ``crawl_target=both``
3. Restreignez la portée avec ``query``, ``user_query`` ou ``supported_mimetypes``
4. Répartir la charge avec les paramètres de planification
5. Ajuster l'intervalle de crawl

Permissions et contrôle d'accès
===============================

Conversion des permissions Drive en rôles Fess
----------------------------------------------

L'ACL d'un document est résolue en trois étapes, afin que le nombre d'appels d'API
supplémentaires reste proportionnel au nombre de Drive partagés plutôt qu'au nombre de
fichiers :

1. les permissions incluses dans le listage des fichiers, qui ne coûtent rien de plus ;
2. pour un élément d'un Drive partagé, dont l'API Drive ne renseigne pas ces permissions,
   l'ACL du Drive partagé lui-même. Elle est récupérée une fois par Drive avec un accès
   d'administrateur de domaine, puis mise en cache ;
3. pour un élément portant ses propres permissions supplémentaires, ces permissions.

Chaque permission Drive devient un rôle de recherche |Fess| :

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Permission Drive
     - Rôle de recherche
   * - ``user``
     - Le rôle de recherche de l'adresse email de cet utilisateur. Les propriétaires du fichier sont toujours ajoutés de cette façon.
   * - ``group``
     - Le rôle de recherche de l'adresse email de ce groupe. L'appartenance aux groupes Google n'est jamais développée ; |Fess| est censé la résoudre côté utilisateur via SSO ou LDAP.
   * - ``domain``
     - ``domain_permission_format`` avec ``{domain}`` remplacé par le nom de domaine. Par défaut : ``{group}{domain}``
   * - ``anyone``
     - Le rôle ``guest``
   * - L'une des précédentes avec ``allowFileDiscovery=false``, ainsi qu'une permission supprimée
     - Aucun rôle. Le partage par lien seul n'est pas non plus détectable par la recherche dans Drive.

Lorsque le résultat est vide, ``default_permissions`` est utilisé à la place -- comme valeur
de repli, et non comme ajout. Lorsque ``default_permissions`` n'est pas défini non plus, le
document est ignoré.

Reflet des permissions de partage Google Drive
----------------------------------------------

Reflet des paramètres de partage Google Drive dans les permissions Fess :

Paramètres :

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=shared_drives
    impersonate_user=admin@example.com
    default_permissions={role}drive-users

Script :

::

    title=file.name
    content=file.description + "\n" + file.contents
    role=file.roles
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link

``file.roles`` contient les informations de partage Google Drive.

Limitations
===========

- Le signal « supprimé » de Drive couvre aussi bien la perte d'accès que la suppression.
  Avec ``crawl_target=users`` ou ``both``, révoquer l'accès d'un utilisateur retire le
  document de l'index alors même qu'un autre utilisateur peut encore le lire. Il revient à
  la modification suivante de ce fichier, ou au prochain crawl complet.
- Lorsqu'une portée retombe sur un crawl complet pendant une exécution incrémentielle, la
  suppression des documents obsolètes reste désactivée : les documents supprimés de Drive
  pendant qu'une portée n'était pas ancrée restent donc dans l'index. Le remède est une
  configuration distincte avec ``incremental=false``, dont le crawl complet les élimine.
- La propagation d'une suppression suppose que l'URL indexée contient l'ID du fichier Drive,
  ce qui est le cas de ``webViewLink`` et de l'URL de repli. Un script de crawl qui réécrit
  ``url`` en une valeur ne contenant pas l'ID du fichier empêche la propagation des
  suppressions.
- Le flux de modifications n'est pas filtré par ``query``. Avec ``query`` défini et
  ``incremental=true``, un fichier modifié qui ne correspond pas à la requête est tout de
  même indexé.
- ``crawl_target=both`` sur un grand domaine déclenche environ
  ``2 + (nombre de Drive partagés) + (nombre d'utilisateurs)`` séquences de listage. La
  parade pratique consiste à répartir les Drive partagés et les utilisateurs dans des
  configurations de data store distinctes.
- ``proxy_username`` et ``proxy_password`` sont envoyés dans un en-tête de requête
  ``Proxy-Authorization``, qui n'authentifie qu'une requête HTTP en clair. Tout le trafic
  des API Google est en HTTPS, et une connexion HTTPS via un proxy avec authentification est
  établie par un échange ``CONNECT`` que le JDK pilote au moyen de
  ``java.net.Authenticator`` et non d'un en-tête de requête. Un tel environnement nécessite
  plutôt l'option JVM ``-Djdk.http.auth.tunneling.disabledSchemes=`` et un ``Authenticator``.

Informations de référence
=========================

- :doc:`ds-overview` - Aperçu des connecteurs Data Store
- :doc:`ds-microsoft365` - Connecteur Microsoft 365
- :doc:`ds-box` - Connecteur Box
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- `Google Drive API <https://developers.google.com/drive/api>`_
- `Google Cloud Platform <https://console.cloud.google.com/>`_
- `Google Workspace Admin <https://admin.google.com/>`_
