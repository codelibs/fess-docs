==================================
Connecteur Git
==================================

Aperçu
====

Le connecteur Git fournit la fonctionnalité permettant de récupérer les fichiers
d'un dépôt Git et de les enregistrer dans l'index |Fess|.

Cette fonctionnalité nécessite le plugin ``fess-ds-git``.

Dépôts pris en charge
==============

- GitHub (public/privé)
- GitLab (public/privé)
- Bitbucket (public/privé)
- Dépôt Git local
- Autres services d'hébergement Git

Prérequis
========

1. L'installation du plugin est requise
2. Pour les dépôts privés, les informations d'authentification sont nécessaires
3. L'accès en lecture au dépôt est requis

Installation du plugin
------------------------

Installez depuis l'interface d'administration via "Système" -> "Plugins".

Ou consultez :doc:`../../admin/plugin-guide` pour plus de détails.

Configuration
========

Configurez depuis l'interface d'administration via "Crawler" -> "Data Store" -> "Nouveau".

Configuration de base
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Élément
     - Exemple
   * - Nom
     - Project Git Repository
   * - Nom du gestionnaire
     - GitDataStore
   * - Activé
     - Oui

Configuration des paramètres
----------------

Exemple de dépôt public :

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/main/
    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,
    prev_commit_id=

Exemple de dépôt privé (avec authentification) :

::

    uri=https://github.com/company/private-repo.git
    username=your_username
    password=YOUR_PERSONAL_ACCESS_TOKEN
    base_url=https://github.com/company/private-repo/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,
    prev_commit_id=

Liste des paramètres
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``uri``
     - Oui
     - URI du dépôt Git (pour le clone). N'incluez pas d'identifiants (nom d'utilisateur, mot de passe, token) dans l'URI ; indiquez-les avec ``username`` et ``password``. ``uri`` n'est pas chiffré
   * - ``base_url``
     - Non
     - URL de base pour l'affichage des fichiers. Si non défini, les URLs seront vides et la suppression automatique des fichiers supprimés sera désactivée
   * - ``username``
     - Non
     - Nom d'utilisateur pour l'authentification Git. Utilisé avec ``password``
   * - ``password``
     - Non
     - Mot de passe ou token pour l'authentification Git. Utilisé avec ``username``. Stocké chiffré
   * - ``extractors``
     - Non
     - Configuration des extracteurs par type MIME
   * - ``default_extractor``
     - Non
     - Extracteur de repli quand aucun motif MIME ne correspond (par défaut : ``tikaExtractor``)
   * - ``prev_commit_id``
     - Non
     - ID du commit précédent (pour le crawl différentiel). Mis à jour automatiquement après un crawl réussi
   * - ``commit_id``
     - Non
     - ID de commit cible (par défaut : HEAD). Une branche ou un tag peut être spécifié (pour un tag, voir aussi « Spécifier une branche » ci-dessous)
   * - ``ref_specs``
     - Non
     - Git ref specs (par défaut : ``+refs/heads/*:refs/heads/*``). Pour récupérer les tags, spécifiez ``+refs/tags/*:refs/tags/*`` (voir « Spécifier une branche » ci-dessous)
   * - ``repository_path``
     - Non
     - Chemin du dépôt local. Si non défini, un répertoire temporaire est créé et supprimé après le crawl
   * - ``include_pattern``
     - Non
     - Filtre d'inclusion des chemins de fichier (regex)
   * - ``exclude_pattern``
     - Non
     - Filtre d'exclusion des chemins de fichier (regex)
   * - ``max_size``
     - Non
     - Taille maximale de fichier à indexer en octets (par défaut : ``10000000``)
   * - ``cache_threshold``
     - Non
     - Seuil en octets pour le basculement entre la mise en mémoire tampon et le disque (par défaut : ``1000000``)
   * - ``readInterval``
     - Non
     - Intervalle de traitement entre chaque fichier (en millisecondes, par défaut : ``0``)

Configuration du script
--------------

::

    url=url
    host="github.com"
    site="github.com/codelibs/fess/" + path
    title=name
    content=content
    cache=""
    digest=author.toExternalString()
    anchor=
    content_length=contentLength
    last_modified=timestamp
    mimetype=mimetype

Champs disponibles
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``url``
     - URL du fichier
   * - ``path``
     - Chemin du fichier dans le dépôt
   * - ``name``
     - Nom du fichier
   * - ``content``
     - Contenu textuel du fichier
   * - ``contentLength``
     - Longueur du contenu
   * - ``timestamp``
     - Date de dernière modification
   * - ``mimetype``
     - Type MIME du fichier
   * - ``author``
     - Informations sur le dernier auteur du commit (PersonIdent)
   * - ``committer``
     - Informations sur le commiteur (PersonIdent). Peut différer de l'auteur
   * - ``uri``
     - URI du dépôt Git

Authentification Git
===================

GitHub Personal Access Token
-----------------------------

1. Générer un Personal Access Token sur GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Accédez à https://github.com/settings/tokens :

1. Cliquez sur "Generate new token" -> "Generate new token (classic)"
2. Entrez un nom de token (ex: Fess Crawler)
3. Cochez "repo" dans les scopes
4. Cliquez sur "Generate token"
5. Copiez le token généré

2. Indiquer le token comme mot de passe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    uri=https://github.com/company/repo.git
    username=your_username
    password=YOUR_GITHUB_TOKEN

GitLab Private Token
--------------------

1. Générer un Access Token sur GitLab
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dans GitLab User Settings -> Access Tokens :

1. Entrez un nom de token
2. Cochez "read_repository" dans les scopes
3. Cliquez sur "Create personal access token"
4. Copiez le token généré

2. Indiquer le token comme mot de passe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    uri=https://gitlab.com/company/repo.git
    username=your_username
    password=YOUR_GITLAB_TOKEN

Authentification avec nom d'utilisateur et mot de passe
-------------------------------------------------------

Indiquez les identifiants avec les paramètres ``username`` et ``password`` au lieu de les incorporer dans ``uri`` :

::

    uri=https://github.com/company/repo.git
    username=your_username
    password=YOUR_PERSONAL_ACCESS_TOKEN

Les identifiants sont utilisés uniquement lorsque ``username`` et ``password`` sont tous les deux spécifiés.

.. warning::
   N'incluez pas d'identifiants dans ``uri`` (par exemple ``https://<token>@github.com/...``). ``uri`` n'est pas chiffré et s'affiche tel quel dans les paramètres du magasin de données de la console d'administration et dans l'API d'administration. ``password`` est chiffré lors de l'enregistrement. Une configuration avec des identifiants incorporés dans l'URI fonctionne toujours, mais séparez-les en ``username`` et ``password``.

.. note::
   Le connecteur Git prend en charge uniquement l'authentification HTTP/HTTPS (nom d'utilisateur et mot de passe, ou un token d'accès). L'authentification par clé SSH (URI de style ``git@...``) n'est pas prise en charge. Utilisez une URI de style HTTPS.

Configuration des extracteurs
============

Extracteurs par type MIME
--------------------

Spécifiez les extracteurs par type de fichier avec le paramètre ``extractors`` :

::

    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,application/json:textExtractor,

Format : ``<regex_type_MIME>:<nom_extracteur>,``

Extracteurs par défaut
~~~~~~~~~~~~~~~~~~

- ``textExtractor`` - Pour les fichiers texte
- ``tikaExtractor`` - Pour les fichiers binaires (PDF, Word, etc.)

Crawler uniquement les fichiers texte
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    extractors=text/.*:textExtractor,

Crawler tous les fichiers
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    extractors=.*:tikaExtractor,

Types de fichiers spécifiques uniquement
~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Uniquement Markdown, YAML, JSON
    extractors=text/markdown:textExtractor,text/yaml:textExtractor,application/json:textExtractor,

Crawl différentiel
============

Crawler uniquement les modifications depuis le dernier commit
------------------------------------

Après le premier crawl, définissez l'ID du commit précédent dans ``prev_commit_id`` :

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/main/
    prev_commit_id=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0

.. note::
   ``prev_commit_id`` est automatiquement mis à jour avec le dernier ID de commit après un crawl réussi.
   Laissez-le vide pour le premier crawl afin de traiter tous les fichiers ; les crawls suivants ne traiteront que les modifications.

Traitement des fichiers supprimés
------------------------

Lorsque ``base_url`` est défini, les fichiers détectés comme supprimés via Git DiffEntry (``ChangeType.DELETE``) sont automatiquement supprimés de l'index.

Lorsqu'un fichier est renommé (``ChangeType.RENAME``), le document à l'ancien chemin est supprimé et le fichier au nouveau chemin est réindexé.

.. note::
   La suppression automatique des fichiers supprimés n'est effective que lorsque ``base_url`` est défini. Si ``base_url`` n'est pas défini, l'URL du document est vide et la suppression n'est pas effectuée.

Exemples d'utilisation
======

Dépôt public GitHub
--------------------------

Paramètres :

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/main/
    extractors=text/.*:textExtractor,application/xml:textExtractor,

Script :

::

    url=url
    host="github.com"
    site="github.com/codelibs/fess/" + path
    title=name
    content=content
    last_modified=timestamp
    mimetype=mimetype

Dépôt privé GitHub
----------------------------

Paramètres :

::

    uri=https://github.com/company/repo.git
    username=your_username
    password=YOUR_GITHUB_TOKEN
    base_url=https://github.com/company/repo/blob/main/
    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,

Script :

::

    url=url
    title=name
    content=content
    digest=author.toExternalString()
    content_length=contentLength
    last_modified=timestamp
    mimetype=mimetype

GitLab (auto-hébergé)
----------------------

Paramètres :

::

    uri=https://gitlab.company.com/team/project.git
    username=your_username
    password=glpat-abc123
    base_url=https://gitlab.company.com/team/project/-/blob/main/
    extractors=text/.*:textExtractor,
    prev_commit_id=

Script :

::

    url=url
    host="gitlab.company.com"
    site="gitlab.company.com/team/project/" + path
    title=name
    content=content
    last_modified=timestamp

Crawler uniquement la documentation (fichiers Markdown)
--------------------------------------------

Paramètres :

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/main/
    extractors=text/markdown:textExtractor,text/plain:textExtractor,

Script :

::

    if (mimetype.startsWith("text/")) {
        url=url
        title=name
        content=content
        last_modified=timestamp
    }

Crawler uniquement des répertoires spécifiques
------------------------------

Filtrage par script :

::

    if (path.startsWith("docs/") || path.startsWith("README")) {
        url=url
        title=name
        content=content
        last_modified=timestamp
        mimetype=mimetype
    }

Dépannage
======================

Erreur d'authentification
----------

**Symptôme** : ``Authentication failed`` ou ``Not authorized``

**Points à vérifier** :

1. Vérifier si le Personal Access Token est correct
2. Vérifier si le token a les droits appropriés (scope ``repo``)
3. Vérifier si le format de l'URI est correct :

   ::

       # Correct
       uri=https://github.com/company/repo.git
       username=your_username
       password=YOUR_TOKEN

       # Incorrect
       uri=https://github.com/company/repo.git?token=...

4. Vérifier la date d'expiration du token

Dépôt introuvable
------------------------

**Symptôme** : ``Repository not found``

**Points à vérifier** :

1. Vérifier si l'URL du dépôt est correcte
2. Vérifier si le dépôt existe et n'a pas été supprimé
3. Vérifier si les informations d'authentification sont correctes
4. Vérifier si vous avez accès au dépôt

Impossible de récupérer les fichiers
----------------------

**Symptôme** : Le crawl réussit mais 0 fichiers

**Points à vérifier** :

1. Vérifier si la configuration ``extractors`` est appropriée
2. Vérifier si des fichiers existent dans le dépôt
3. Vérifier si la configuration du script est correcte
4. Vérifier si des fichiers existent dans la branche cible

Erreur de type MIME
----------------

**Symptôme** : Certains fichiers ne sont pas crawlés

**Solution** :

Ajuster la configuration des extracteurs :

::

    # Tous les fichiers
    extractors=.*:tikaExtractor,

    # Ajouter des types MIME specifiques
    extractors=text/.*:textExtractor,application/json:textExtractor,application/xml:textExtractor,

Dépôts volumineux
----------------

**Symptôme** : Le crawl prend du temps ou mémoire insuffisante

**Solution** :

1. Limiter les fichiers cibles avec ``extractors``
2. Filtrer des répertoires spécifiques avec le script
3. Utiliser le crawl différentiel (paramètre ``prev_commit_id``)
4. Ajuster l'intervalle de crawl

Spécification de branche
--------------

Pour crawler une branche autre que celle par défaut, spécifiez le nom de la branche ou du tag avec le paramètre ``commit_id`` :

::

    uri=https://github.com/company/repo.git
    base_url=https://github.com/company/repo/blob/develop/
    commit_id=develop

Pour crawler un tag, celui-ci doit avoir été récupéré. Si la valeur par défaut de ``ref_specs`` ne récupère pas les tags, spécifiez ``ref_specs=+refs/tags/*:refs/tags/*`` (seuls les tags sont récupérés, pas les branches) :

::

    uri=https://github.com/company/repo.git
    base_url=https://github.com/company/repo/blob/v1.0/
    commit_id=v1.0
    ref_specs=+refs/tags/*:refs/tags/*

Génération d'URL
=========

Patterns de configuration base_url
----------------------

**GitHub** :

::

    base_url=https://github.com/user/repo/blob/master/

**GitLab** :

::

    base_url=https://gitlab.com/user/repo/-/blob/main/

**Bitbucket** :

::

    base_url=https://bitbucket.org/user/repo/src/master/

L'URL est générée en concaténant simplement ``base_url`` et le chemin du fichier (aucun séparateur n'est inséré). Par conséquent, ``base_url`` doit se terminer par un ``/`` final.

Génération d'URL dans le script
---------------------

::

    url=url
    title=name
    content=content

Ou URL personnalisée :

::

    url="https://github.com/mycompany/repo/blob/main/" + path
    title=name
    content=content

Informations de référence
========

- :doc:`ds-overview` - Aperçu des connecteurs Data Store
- :doc:`ds-database` - Connecteur de base de données
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- `GitHub Personal Access Tokens <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token>`_
- `GitLab Personal Access Tokens <https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`_
