==================================
Connecteur Git
==================================

Apercu
====

Le connecteur Git fournit la fonctionnalite permettant de recuperer les fichiers
d'un depot Git et de les enregistrer dans l'index |Fess|.

Cette fonctionnalite necessite le plugin ``fess-ds-git``.

Depots pris en charge
==============

- GitHub (public/prive)
- GitLab (public/prive)
- Bitbucket (public/prive)
- Depot Git local
- Autres services d'hebergement Git

Prerequis
========

1. L'installation du plugin est requise
2. Pour les depots prives, les informations d'authentification sont necessaires
3. L'acces en lecture au depot est requis

Installation du plugin
------------------------

Installez depuis l'interface d'administration via "Systeme" -> "Plugins".

Ou consultez :doc:`../../admin/plugin-guide` pour plus de details.

Configuration
========

Configurez depuis l'interface d'administration via "Crawler" -> "Data Store" -> "Nouveau".

Configuration de base
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Element
     - Exemple
   * - Nom
     - Project Git Repository
   * - Nom du gestionnaire
     - GitDataStore
   * - Active
     - Oui

Configuration des parametres
----------------

Exemple de depot public :

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,
    prev_commit_id=
    delete_old_docs=false

Exemple de depot prive (avec authentification) :

::

    uri=https://username:personal_access_token@github.com/company/private-repo.git
    base_url=https://github.com/company/private-repo/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,
    prev_commit_id=
    delete_old_docs=false

Liste des parametres
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametre
     - Requis
     - Description
   * - ``uri``
     - Oui
     - URI du depot Git (pour le clone)
   * - ``base_url``
     - Oui
     - URL de base pour l'affichage des fichiers
   * - ``extractors``
     - Non
     - Configuration des extracteurs par type MIME
   * - ``prev_commit_id``
     - Non
     - ID du commit precedent (pour le crawl differentiel)
   * - ``delete_old_docs``
     - Non
     - Supprimer les fichiers supprimes de l'index (par defaut : ``false``)

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
     - Chemin du fichier dans le depot
   * - ``name``
     - Nom du fichier
   * - ``content``
     - Contenu textuel du fichier
   * - ``contentLength``
     - Longueur du contenu
   * - ``timestamp``
     - Date de derniere modification
   * - ``mimetype``
     - Type MIME du fichier
   * - ``author``
     - Informations sur le dernier commiteur

Authentification Git
===================

GitHub Personal Access Token
-----------------------------

1. Generer un Personal Access Token sur GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Accedez a https://github.com/settings/tokens :

1. Cliquez sur "Generate new token" -> "Generate new token (classic)"
2. Entrez un nom de token (ex: Fess Crawler)
3. Cochez "repo" dans les scopes
4. Cliquez sur "Generate token"
5. Copiez le token genere

2. Inclure les informations d'authentification dans l'URI
~~~~~~~~~~~~~~~~~~~~~~~~

::

    uri=https://username:ghp_abc123def456ghi789jkl012@github.com/company/repo.git

GitLab Private Token
--------------------

1. Generer un Access Token sur GitLab
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dans GitLab User Settings -> Access Tokens :

1. Entrez un nom de token
2. Cochez "read_repository" dans les scopes
3. Cliquez sur "Create personal access token"
4. Copiez le token genere

2. Inclure les informations d'authentification dans l'URI
~~~~~~~~~~~~~~~~~~~~~~~~

::

    uri=https://username:glpat-abc123def456@gitlab.com/company/repo.git

Authentification SSH
-------

Pour utiliser une cle SSH :

::

    uri=git@github.com:company/repo.git

.. note::
   Lors de l'utilisation de l'authentification SSH, vous devez configurer la cle SSH de l'utilisateur executant |Fess|.

Configuration des extracteurs
============

Extracteurs par type MIME
--------------------

Specifiez les extracteurs par type de fichier avec le parametre ``extractors`` :

::

    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,application/json:textExtractor,

Format : ``<regex_type_MIME>:<nom_extracteur>,``

Extracteurs par defaut
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

Types de fichiers specifiques uniquement
~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Uniquement Markdown, YAML, JSON
    extractors=text/markdown:textExtractor,text/yaml:textExtractor,application/json:textExtractor,

Crawl differentiel
============

Crawler uniquement les modifications depuis le dernier commit
------------------------------------

Apres le premier crawl, definissez l'ID du commit precedent dans ``prev_commit_id`` :

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    prev_commit_id=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
    delete_old_docs=true

.. note::
   L'ID de commit est celui du dernier crawl.
   Seules les modifications apres ce commit seront crawlees.

Traitement des fichiers supprimes
------------------------

Si ``delete_old_docs=true`` est defini, les fichiers supprimes du depot Git
seront egalement supprimes de l'index.

Exemples d'utilisation
======

Depot public GitHub
--------------------------

Parametres :

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,
    delete_old_docs=false

Script :

::

    url=url
    host="github.com"
    site="github.com/codelibs/fess/" + path
    title=name
    content=content
    last_modified=timestamp
    mimetype=mimetype

Depot prive GitHub
----------------------------

Parametres :

::

    uri=https://username:ghp_abc123def456ghi789jkl012@github.com/company/repo.git
    base_url=https://github.com/company/repo/blob/main/
    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,
    delete_old_docs=false

Script :

::

    url=url
    title=name
    content=content
    digest=author.toExternalString()
    content_length=contentLength
    last_modified=timestamp
    mimetype=mimetype

GitLab (auto-heberge)
----------------------

Parametres :

::

    uri=https://username:glpat-abc123@gitlab.company.com/team/project.git
    base_url=https://gitlab.company.com/team/project/-/blob/main/
    extractors=text/.*:textExtractor,
    prev_commit_id=
    delete_old_docs=false

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

Parametres :

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/markdown:textExtractor,text/plain:textExtractor,
    delete_old_docs=false

Script :

::

    if (mimetype.startsWith("text/")) {
        url=url
        title=name
        content=content
        last_modified=timestamp
    }

Crawler uniquement des repertoires specifiques
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

Depannage
======================

Erreur d'authentification
----------

**Symptome** : ``Authentication failed`` ou ``Not authorized``

**Points a verifier** :

1. Verifier si le Personal Access Token est correct
2. Verifier si le token a les droits appropries (scope ``repo``)
3. Verifier si le format de l'URI est correct :

   ::

       # Correct
       uri=https://username:token@github.com/company/repo.git

       # Incorrect
       uri=https://github.com/company/repo.git?token=...

4. Verifier la date d'expiration du token

Depot introuvable
------------------------

**Symptome** : ``Repository not found``

**Points a verifier** :

1. Verifier si l'URL du depot est correcte
2. Verifier si le depot existe et n'a pas ete supprime
3. Verifier si les informations d'authentification sont correctes
4. Verifier si vous avez acces au depot

Impossible de recuperer les fichiers
----------------------

**Symptome** : Le crawl reussit mais 0 fichiers

**Points a verifier** :

1. Verifier si la configuration ``extractors`` est appropriee
2. Verifier si des fichiers existent dans le depot
3. Verifier si la configuration du script est correcte
4. Verifier si des fichiers existent dans la branche cible

Erreur de type MIME
----------------

**Symptome** : Certains fichiers ne sont pas crawles

**Solution** :

Ajuster la configuration des extracteurs :

::

    # Tous les fichiers
    extractors=.*:tikaExtractor,

    # Ajouter des types MIME specifiques
    extractors=text/.*:textExtractor,application/json:textExtractor,application/xml:textExtractor,

Depots volumineux
----------------

**Symptome** : Le crawl prend du temps ou memoire insuffisante

**Solution** :

1. Limiter les fichiers cibles avec ``extractors``
2. Filtrer des repertoires specifiques avec le script
3. Utiliser le crawl differentiel (parametre ``prev_commit_id``)
4. Ajuster l'intervalle de crawl

Specification de branche
--------------

Pour crawler une branche autre que la branche par defaut :

::

    uri=https://github.com/company/repo.git#develop
    base_url=https://github.com/company/repo/blob/develop/

Specifiez le nom de la branche apres ``#``.

Generation d'URL
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

L'URL est generee en concatenant ``base_url`` et le chemin du fichier.

Generation d'URL dans le script
---------------------

::

    url=base_url + path
    title=name
    content=content

Ou URL personnalisee :

::

    url="https://github.com/mycompany/repo/blob/main/" + path
    title=name
    content=content

Informations de reference
========

- :doc:`ds-overview` - Apercu des connecteurs Data Store
- :doc:`ds-database` - Connecteur de base de donnees
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- `GitHub Personal Access Tokens <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token>`_
- `GitLab Personal Access Tokens <https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`_
