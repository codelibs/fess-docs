==================================
Connecteur Backlog
==================================

Aperçu
======

Le connecteur Backlog fournit la fonctionnalité permettant de récupérer les tickets, pages Wiki, documents et fichiers d'un espace Backlog
et de les enregistrer dans l'index |Fess|.
Il s'authentifie auprès de l'espace avec une clé d'API.
Chaque document indexé est limité aux membres de son projet Backlog (voir « Permissions » ci-dessous).

Cette fonctionnalité nécessite le plugin ``fess-ds-backlog``.

Contenu pris en charge
======================

- Tickets (avec leurs commentaires)
- Pages Wiki
- Documents
- Pièces jointes des tickets, pages Wiki et documents
- Fichiers partagés d'un projet

Chaque crawl est un crawl complet. Par défaut, les documents qui ont disparu de Backlog ne sont pas supprimés
à la fin du crawl ; ils sont supprimés lorsqu'ils expirent (voir « Contenu supprimé et accès révoqué »).

Prérequis
=========

1. L'installation du plugin est requise
2. Un utilisateur Backlog dédié et sa clé d'API sont requis
3. L'utilisateur doit être membre de chaque projet à explorer

Installation du plugin
----------------------

Installez depuis l'interface d'administration via "Système" -> "Plugins", ou exécutez ``bin/fess-setup install plugin fess-ds-backlog``
puis redémarrez |Fess|.
Consultez :doc:`../../admin/plugin-guide` pour plus de détails.

Configuration côté Backlog
--------------------------

1. Créez un utilisateur Backlog dédié à l'exploration et émettez-lui une clé d'API (« Paramètres personnels » -> « API »).
   Le crawl voit exactement ce que voit cet utilisateur.
2. Ajoutez l'utilisateur à chaque projet à explorer. Le connecteur ne demande pas les projets que l'utilisateur n'a pas rejoints,
   même si l'utilisateur est administrateur de l'espace.
3. Attribuez à l'utilisateur un rôle sans restriction (Administrateur ou Utilisateur normal). Avec un rôle restreint,
   Backlog répond par un HTTP 403 pour certaines fonctionnalités : un utilisateur en « lecture seule » ne peut pas télécharger les pièces jointes des tickets,
   et seuls les utilisateurs sans restriction peuvent télécharger les fichiers partagés.
   Sur un tel 403, le connecteur consigne un avertissement par projet et par fonctionnalité, ignore cette fonctionnalité pour ce projet
   (pièces jointes des tickets, pièces jointes du Wiki, pièces jointes des documents ou fichiers partagés) et poursuit le reste.
4. Si l'espace exige l'authentification à deux facteurs pour l'accès à l'API, Backlog répond avec le code d'erreur 12
   (RequiredMFAError) et le crawl est interrompu.

La clé d'API n'est envoyée que dans l'en-tête de requête ``Backlog-API-Key``. Elle n'est pas transmise au script,
ce connecteur ne l'écrit pas dans les journaux, et les redirections HTTP ne sont pas suivies, de sorte que la clé ne quitte jamais l'hôte de l'espace.

.. warning::

   N'activez pas la journalisation ``FINE`` du logger ``org.codelibs.curl``. Le client HTTP consigne les en-têtes de requête à ce niveau
   et ne masque que les en-têtes de type ``Authorization`` et ``Cookie`` ; l'en-tête ``Backlog-API-Key`` serait donc écrit dans le journal.

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
     - Company Backlog
   * - Nom du gestionnaire
     - BacklogDataStore
   * - Permissions
     - (laissez vide ; voir « Permissions »)
   * - Activé
     - Oui

Configuration des paramètres
----------------------------

::

    api_key=**********************************************
    space_url=https://example.backlog.com

Liste des paramètres
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``api_key``
     - Oui
     - La clé d'API Backlog. Elle n'est pas transmise au script et n'est pas consignée dans les journaux
   * - ``space_url``
     - Oui
     - L'URL de l'espace, par exemple ``https://example.backlog.com``. Seul ``https`` est accepté, et seuls le schéma et l'hôte peuvent être indiqués (une barre oblique finale est ignorée). Une valeur absente, mal formée ou en ``http`` interrompt le crawl
   * - ``project_keys``
     - Non
     - Clés de projet à explorer, séparées par des virgules (insensible à la casse). Si vide, tous les projets visibles par l'utilisateur sont explorés. Une clé non visible par l'utilisateur est consignée comme avertissement
   * - ``include_archived``
     - Non
     - Explorer aussi les projets archivés (par défaut : ``false``)
   * - ``include_issues``
     - Non
     - Indexer les tickets (par défaut : ``true``)
   * - ``include_comments``
     - Non
     - Ajouter les commentaires des tickets au document du ticket (par défaut : ``true``)
   * - ``include_wikis``
     - Non
     - Indexer les pages Wiki, dans les projets où le Wiki est activé (par défaut : ``true``)
   * - ``include_documents``
     - Non
     - Indexer les documents, dans les projets où les documents sont activés (par défaut : ``true``)
   * - ``include_attachments``
     - Non
     - Télécharger et indexer les pièces jointes des tickets, pages Wiki et documents (par défaut : ``true``)
   * - ``include_shared_files``
     - Non
     - Télécharger et indexer les fichiers partagés, dans les projets où le partage de fichiers est activé (par défaut : ``true``)
   * - ``permission_sync``
     - Non
     - Donner à chaque document d'un projet un rôle ``{user}`` par membre du projet (par défaut : ``true``). Voir « Permissions »
   * - ``default_permissions``
     - Non
     - Permissions séparées par des virgules (``{user}name``, ``{group}name`` ou ``{role}name``) ajoutées à chaque document
   * - ``max_file_size``
     - Non
     - Les fichiers plus grands que ce nombre d'octets sont ignorés et non indexés (par défaut : ``10485760``)
   * - ``include_pattern``
     - Non
     - Expression régulière à laquelle ``backlog.url`` doit correspondre pour être indexé
   * - ``exclude_pattern``
     - Non
     - Expression régulière à laquelle ``backlog.url`` ne doit pas correspondre. Lorsqu'un ticket, une page Wiki ou un document est filtré, ses pièces jointes sont également ignorées
   * - ``request_interval``
     - Non
     - Millisecondes d'attente avant chaque requête à l'API (par défaut : ``200``)
   * - ``search_request_interval``
     - Non
     - Intervalle minimal, en millisecondes, entre deux requêtes de type recherche (liste des tickets, liste du Wiki). Backlog demande aux clients de garder au moins une seconde entre elles (par défaut : ``1000``)
   * - ``max_retry_count``
     - Non
     - Nombre de nouvelles tentatives pour HTTP 429, 5xx et échecs de connexion (par défaut : ``5``)
   * - ``connection_timeout``
     - Non
     - Délai de connexion en millisecondes (par défaut : ``10000``)
   * - ``read_timeout``
     - Non
     - Délai de lecture en millisecondes (par défaut : ``30000``)
   * - ``ignore_error``
     - Non
     - Si l'extraction du texte d'un fichier téléchargé échoue, indexer le fichier avec un contenu vide au lieu d'enregistrer un échec (par défaut : ``true``)

.. note::

   Une valeur invalide (une valeur non numérique, un intervalle ou un nombre de tentatives négatif, un délai ou ``max_file_size`` non positif,
   ou un booléen autre que ``true``/``false``) est consignée comme avertissement et la valeur par défaut est utilisée.
   ``0`` est valide pour ``request_interval``, ``search_request_interval`` et ``max_retry_count``.

Configuration du script
-----------------------

::

    title=backlog.title
    content=backlog.content
    url=backlog.url
    mimetype=backlog.mimetype
    created=backlog.created
    last_modified=backlog.updated
    role=backlog.roles

.. important::

   ``role=backlog.roles`` est nécessaire pour que la restriction aux membres du projet prenne effet.
   Sans cette ligne, seul le champ « Permissions » de la configuration du Data Store parvient à l'index.

Champs disponibles
~~~~~~~~~~~~~~~~~~

Chaque document est exposé au script sous l'objet ``backlog``.

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Champ
     - Types
     - Description
   * - ``backlog.type``
     - tous
     - ``issue``, ``wiki``, ``document``, ``attachment`` ou ``file``
   * - ``backlog.id``
     - tous
     - L'ID Backlog du ticket, de la page Wiki, du document, de la pièce jointe ou du fichier partagé
   * - ``backlog.project_key``, ``backlog.project_name``
     - tous
     - Le projet
   * - ``backlog.title``
     - tous
     - ``[KEY-1] résumé`` pour un ticket ; sinon le nom de la page, le titre du document ou le nom du fichier
   * - ``backlog.content``
     - tous
     - Ticket : description, attributs, champs personnalisés et commentaires. Page Wiki : le contenu de la page. Document : texte brut. Pièce jointe et fichier : le texte extrait
   * - ``backlog.url``
     - tous
     - Voir « URL »
   * - ``backlog.mimetype``
     - tous
     - ``text/plain`` pour les tickets, pages Wiki et documents ; le type détecté pour les fichiers
   * - ``backlog.created``, ``backlog.updated``
     - tous
     - Horodatages ISO 8601 en UTC, lorsque Backlog les renvoie
   * - ``backlog.created_by``, ``backlog.updated_by``
     - tous
     - Noms d'utilisateur, lorsque Backlog les renvoie
   * - ``backlog.roles``
     - tous
     - Les rôles de recherche (voir « Permissions »)
   * - ``backlog.issue_key``, ``backlog.issue_type``, ``backlog.status``, ``backlog.priority``, ``backlog.assignee``
     - ticket
     - Attributs du ticket (noms)
   * - ``backlog.categories``, ``backlog.milestones``, ``backlog.versions``
     - ticket
     - Listes de noms
   * - ``backlog.custom_fields``
     - ticket
     - Table associant le nom du champ personnalisé au texte de sa valeur
   * - ``backlog.comments``
     - ticket
     - Texte des commentaires sous la forme ``auteur : contenu``, séparés par des lignes vides
   * - ``backlog.tags``
     - page Wiki, document
     - Liste des noms de tags
   * - ``backlog.parent_type``, ``backlog.parent_url``, ``backlog.parent_title``
     - pièce jointe
     - Le ticket, la page Wiki ou le document auquel appartient la pièce jointe
   * - ``backlog.size``
     - pièce jointe, fichier
     - Taille téléchargée en octets
   * - ``backlog.path``
     - fichier
     - Chemin du fichier partagé, par exemple ``/docs/spec.pdf``

URL
---

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Type
     - URL
   * - ticket
     - ``{space_url}/view/{ISSUE-KEY}``
   * - page Wiki
     - ``{space_url}/alias/wiki/{ID}``
   * - document
     - ``{space_url}/document/{PROJECT}/{ID}``
   * - fichier
     - ``{space_url}/file/{PROJECT}{répertoire}{nom}`` (chaque segment du chemin est encodé en pourcentage)
   * - pièce jointe
     - ``{URL de l'élément parent}#attachment-{ID}``

.. note::

   Les formes d'URL des documents et des fichiers partagés, ainsi que le point de terminaison de téléchargement des pièces jointes de documents,
   n'ont pas été confirmés sur un véritable espace Backlog. Si un lien n'ouvre pas la page attendue,
   le document est tout de même indexé et consultable ; seule la cible du lien est erronée.

Permissions
===========

Avec ``permission_sync=true`` (par défaut), chaque document d'un projet reçoit les rôles suivants :

- un rôle ``{user}`` pour le ``mailAddress`` et un pour le ``userId`` de chaque membre du projet
  (les valeurs vides sont ignorées), de sorte qu'un membre peut se connecter à |Fess| avec l'un ou l'autre
- la valeur de ``default_permissions``
- la valeur du champ « Permissions » de la configuration du Data Store

Si les membres du projet ne peuvent pas être récupérés, ou si aucun d'eux n'a de ``mailAddress`` ou de ``userId`` utilisable,
le projet entier est ignoré et enregistré sous "Crawler" -> "URL en échec". Il n'est jamais indexé sans les rôles de ses membres.

Avec ``permission_sync=false``, seuls ``default_permissions`` et le champ « Permissions » s'appliquent.

.. warning::

   Videz le champ « Permissions » de la configuration du Data Store. L'interface d'administration le préremplit avec ``{role}guest``,
   que détiennent tous les utilisateurs, y compris les chercheurs anonymes. S'il est conservé, il est fusionné dans les rôles de chaque document
   et tout le contenu de Backlog devient consultable par tous.
   Avec ``permission_sync=true``, le connecteur consigne un avertissement par projet lorsqu'un rôle invité se retrouve parmi ses rôles.

À savoir avant de s'appuyer sur les rôles des membres :

- Un identifiant de membre est un nom de connexion |Fess|. Un ``userId`` Backlog tel que ``tanaka`` donne accès à la connexion |Fess| nommée ``tanaka``,
  qui n'est pas forcément la même personne (par exemple un nom de compte LDAP ou Active Directory). Le rôle basé sur le ``mailAddress`` n'a pas ce problème.
  N'utilisez ``permission_sync`` que lorsque les noms de connexion |Fess| sont les ID d'utilisateur ou les adresses e-mail de Backlog.
- Un membre dont l'identifiant correspondrait au rôle invité ou à une autre connexion est ignoré, avec un avertissement qui nomme le projet et l'ID du membre :
  un ``userId`` ``guest`` et tout identifiant contenant une barre oblique inverse (|Fess| supprime d'un nom d'utilisateur tout ce qui précède la barre oblique inverse).
- Chaque membre du projet peut trouver chaque élément indexé du projet, pièces jointes et fichiers partagés compris, même lorsque Backlog lui-même
  refuserait le téléchargement à ce membre (un utilisateur en « lecture seule » ne peut pas télécharger les pièces jointes des tickets). Les rôles sont par projet, pas par fonctionnalité.

Contenu supprimé et accès révoqué
=================================

Par défaut, |Fess| attribue à chaque document une date d'expiration (le paramètre « Supprimer les anciens documents » de Général, trois jours par défaut)
et ne supprime pas à la fin d'un crawl les documents qui en ont une. Les documents expirés sont supprimés par le Doc Purger. Par conséquent, par défaut :

- le contenu supprimé dans Backlog reste consultable pendant trois jours environ au maximum
- lorsqu'un membre quitte un projet, il conserve l'accès aux documents déjà indexés du projet pendant trois jours environ au maximum.
  Le crawl suivant les indexe à nouveau sous de nouveaux ID de document (l'ID inclut la liste des rôles), et les anciennes copies, avec les anciens rôles,
  restent jusqu'à leur expiration. Pendant ce temps, les autres membres voient des résultats en double

Pour supprimer ces documents à la fin du crawl, ajoutez ``keep_expires_docs=false`` aux paramètres de la configuration du Data Store.
|Fess| supprime alors tous les documents de cette configuration que le crawl n'a pas réindexés, ce qui s'applique aussi à tout ce que le crawl n'a pas atteint (voir « Gestion des erreurs »).

Exemples d'utilisation
======================

Explorer des projets précis
---------------------------

Paramètres :

::

    api_key=**********************************************
    space_url=https://example.backlog.com
    project_keys=PROJ,DOCS
    include_shared_files=false

Tickets et pages Wiki uniquement, sans pièces jointes
-----------------------------------------------------

Paramètres :

::

    api_key=**********************************************
    space_url=https://example.backlog.com
    include_documents=false
    include_attachments=false
    include_shared_files=false

Supprimer à la fin du crawl les documents supprimés dans Backlog
----------------------------------------------------------------

Paramètres :

::

    api_key=**********************************************
    space_url=https://example.backlog.com
    keep_expires_docs=false

Gestion des erreurs
===================

- Le crawl n'est interrompu que sur un HTTP ``401``, le code d'erreur Backlog 11 (AuthenticationError) ou 12 (RequiredMFAError),
  un ``api_key`` ou ``space_url`` absent ou mal formé, ou un échec de la liste des projets.
- Sur HTTP ``429``, la requête attend jusqu'à l'heure indiquée par l'en-tête ``X-RateLimit-Reset`` (120 secondes au maximum ; 60 secondes si l'en-tête est absent) puis est relancée.
  Sur HTTP ``5xx`` et les échecs de connexion, la requête est relancée avec un délai exponentiel (1 seconde, 2 secondes, 4 secondes, jusqu'à 60 secondes).
  Une fois les ``max_retry_count`` nouvelles tentatives épuisées, cet élément échoue.
- Toute autre erreur (``403``, ``404``, tentatives épuisées) est enregistrée pour cet élément seulement et le crawl continue.
- Un élément en échec ne fait pas échouer la tâche de crawl. Après un crawl, consultez "Crawler" -> "URL en échec" et le journal du crawler.
- Avec ``keep_expires_docs=false``, le contenu situé sous un échec n'est pas réindexé et est donc supprimé à la fin de ce crawl :
  tout ce qui se trouve sous un listage en échec, un projet ignoré ou une fonctionnalité ignorée sur un 403 disparaît de l'index jusqu'à ce qu'un crawl ultérieur se termine sans cet échec.
  Il en va de même pour un crawl interrompu. Par défaut, ce contenu reste consultable jusqu'à son expiration.

Dépannage
=========

Le crawl est interrompu au démarrage
------------------------------------

1. Vérifiez que ``api_key`` est correcte et a été émise pour un utilisateur de cet espace
2. Vérifiez que ``space_url`` est une URL ``https`` avec uniquement l'hôte, comme ``https://example.backlog.com``
3. Si l'espace exige l'authentification à deux facteurs pour l'accès à l'API, le crawl est interrompu avec RequiredMFAError

Un projet n'est pas indexé
--------------------------

1. Vérifiez que l'utilisateur de l'API est membre du projet
2. Avec ``permission_sync=true``, un projet dont les membres ne peuvent pas être récupérés, ou dont aucun n'a d'adresse e-mail ou d'ID d'utilisateur utilisable, est ignoré. Consultez "Crawler" -> "URL en échec"
3. Vérifiez ``project_keys`` et ``include_archived``

Des pièces jointes ou fichiers partagés manquent
------------------------------------------------

Attribuez à l'utilisateur de l'API un rôle sans restriction. Le journal contient un avertissement par projet et par fonctionnalité ignorée sur un HTTP 403.

Informations de référence
=========================

- :doc:`ds-overview` - Aperçu des connecteurs Data Store
- :doc:`ds-atlassian` - Connecteur Atlassian
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- :doc:`../../admin/failureurl-guide` - URL en échec
- :doc:`../../admin/plugin-guide` - Guide de gestion des plugins
- `Backlog API Documentation <https://developer.nulab.com/docs/backlog/>`_
