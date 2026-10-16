==================================
Connecteur Notion
==================================

Aperçu
======

Le connecteur Notion fournit la fonctionnalité permettant de récupérer les pages et les lignes de bases de données de Notion
et de les enregistrer dans l'index |Fess|.
Il s'authentifie comme une intégration interne Notion et indexe tout ce qui a été partagé avec cette intégration.

Cette fonctionnalité nécessite le plugin ``fess-ds-notion``.

Contenu pris en charge
======================

- Pages (le texte de leurs blocs)
- Lignes de bases de données, avec les valeurs de leurs propriétés
- Pièces jointes des blocs de fichier et PDF hébergées par Notion (chacune est indexée comme un document distinct)
- Commentaires de page non résolus (intégrés au document de la page)

Les éléments suivants ne sont pas pris en charge :

- Les fichiers simplement référencés depuis Notion (fichiers externes) ; seuls les blocs ``file`` et ``pdf`` hébergés par Notion sont téléchargés
- Les pages et lignes de bases de données qui se trouvent dans la corbeille de Notion
- Le contrôle d'accès par page (voir « Permissions » ci-dessous)

Prérequis
=========

1. L'installation du plugin est requise
2. Une intégration interne Notion doit être créée
3. L'intégration doit être partagée avec les pages et bases de données à explorer

Installation du plugin
----------------------

Installez depuis l'interface d'administration via "Système" -> "Plugins", ou exécutez ``bin/fess-setup install plugin fess-ds-notion``
puis redémarrez |Fess|.
Consultez :doc:`../../admin/plugin-guide` pour plus de détails.

Configuration de l'intégration Notion
-------------------------------------

1. Créez une intégration interne dans Notion et copiez son « Internal Integration Secret ».
2. Sur la page « Configuration » de l'intégration, activez les capacités suivantes :

   .. list-table::
      :header-rows: 1
      :widths: 25 25 50

      * - Capacité
        - Requise
        - Utilisation
      * - Read content
        - Toujours
        - Lecture des pages, blocs, bases de données et lignes de bases de données. Sans elle, toutes les requêtes échouent avec ``401 unauthorized`` et le crawl est immédiatement interrompu
      * - Read comments
        - Seulement si ``include_comments=true`` (par défaut)
        - Récupération des commentaires de page. Si la capacité est absente, un avertissement est consigné une seule fois et l'exploration des commentaires est désactivée pour le reste de ce crawl ; le crawl lui-même n'échoue pas
      * - Read user information
        - Facultative
        - Résolution des ID d'utilisateur (``created_by``, ``last_edited_by`` et propriétés ``people``) en noms affichés. Sans elle, l'ID d'utilisateur est indexé à la place du nom

3. Partagez l'intégration dans Notion avec chaque page ou base de données à explorer.
   Ajouter une capacité seule ne donne accès à aucun contenu.

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
     - Company Notion
   * - Nom du gestionnaire
     - NotionDataStore
   * - Activé
     - Oui

Configuration des paramètres
----------------------------

::

    token=secret_************************************

Liste des paramètres
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``token``
     - Oui
     - L'Internal Integration Secret. Il n'est pas transmis au script et n'est pas consigné dans les journaux
   * - ``root_page_ids``
     - Non
     - ID des pages à partir desquelles explorer, séparés par des virgules. Si ce paramètre et ``database_ids`` sont tous deux vides, toutes les pages et bases de données partagées avec l'intégration sont découvertes via la recherche de Notion
   * - ``database_ids``
     - Non
     - ID des bases de données à partir desquelles explorer, séparés par des virgules. Chaque ligne de chaque base de données est indexée
   * - ``include_comments``
     - Non
     - Récupérer les commentaires non résolus de chaque page et ajouter leur texte à ``notion.content`` et ``notion.comments`` (par défaut : ``true``)
   * - ``include_files``
     - Non
     - Télécharger les pièces jointes des blocs ``file`` et ``pdf`` hébergées par Notion, en extraire le texte et indexer chacune comme un document distinct (par défaut : ``true``)
   * - ``max_file_size``
     - Non
     - Une pièce jointe plus grande que ce nombre d'octets est entièrement ignorée, sans être indexée même avec un contenu vide (par défaut : ``10485760``)
   * - ``include_pattern``
     - Non
     - Expression régulière à laquelle le ``notion.url`` d'un document doit correspondre pour être indexé (voir « Périmètre de l'exploration »)
   * - ``exclude_pattern``
     - Non
     - Expression régulière à laquelle le ``notion.url`` d'un document ne doit pas correspondre (voir « Périmètre de l'exploration »)
   * - ``request_interval``
     - Non
     - Millisecondes d'attente avant chaque requête à l'API Notion, pour rester sous la limite de débit de Notion (environ 3 requêtes par seconde) (par défaut : ``350``)
   * - ``max_retry_count``
     - Non
     - Nombre maximal de nouvelles tentatives pour une requête qui se termine par ``429``, ``5xx`` ou ``529``, ou par un échec de transport tel qu'un délai dépassé (par défaut : ``5``)
   * - ``connection_timeout``
     - Non
     - Délai de connexion de chaque requête à l'API, en millisecondes (par défaut : ``10000``)
   * - ``read_timeout``
     - Non
     - Délai de lecture de chaque requête à l'API, en millisecondes (par défaut : ``30000``)
   * - ``ignore_error``
     - Non
     - Si l'extraction du texte échoue pour une pièce jointe téléchargée, indexer la pièce jointe avec un contenu vide au lieu de faire échouer le document (par défaut : ``true``). Un échec de téléchargement fait toujours échouer le document, quel que soit ce paramètre

.. note::

   Pour un paramètre numérique, une valeur vide ou non numérique revient à sa valeur par défaut avec un avertissement dans le journal.
   Il en va de même pour un ``request_interval`` ou ``max_retry_count`` négatif (``0`` est valide pour les deux) et pour un
   paramètre ``true``/``false`` défini sur toute autre valeur.

Configuration du script
-----------------------

::

    title=notion.title
    content=notion.content
    url=notion.url
    mimetype=notion.mimetype
    last_modified=notion.last_edited_time
    created=notion.created_time

Champs disponibles
~~~~~~~~~~~~~~~~~~

Chaque document, qu'il s'agisse d'une page, d'une ligne de base de données ou d'une pièce jointe, est exposé au script sous l'objet ``notion``.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``notion.type``
     - ``page`` pour une page ou une ligne de base de données, ``file`` pour une pièce jointe
   * - ``notion.id``
     - L'ID de la page ou, pour une pièce jointe, l'ID du bloc
   * - ``notion.title``
     - Le titre de la page (la propriété de type ``title``, quel que soit son nom) ou le nom de fichier d'une pièce jointe
   * - ``notion.content``
     - Pour une page : les valeurs des propriétés autres que le titre (lignes de bases de données uniquement), le texte de ses blocs et le texte de ses commentaires, réunis. Pour une pièce jointe : le texte extrait
   * - ``notion.url``
     - L'URL Notion de la page. Pour une pièce jointe, l'URL de la page qui la contient, suivie de ``#<ID du bloc>``
   * - ``notion.mimetype``
     - ``text/html`` pour une page, le type MIME détecté pour une pièce jointe
   * - ``notion.created_time``
     - Date de création de la page. Non disponible pour une pièce jointe
   * - ``notion.last_edited_time``
     - Date de dernière modification de la page ou du bloc de la pièce jointe
   * - ``notion.created_by``
     - Créateur de la page : le nom si Notion en a renvoyé un, sinon l'ID d'utilisateur. Non disponible pour une pièce jointe
   * - ``notion.last_edited_by``
     - Dernier éditeur, au même format. Non disponible pour une pièce jointe
   * - ``notion.parent_id``
     - ID de la page, base de données, source de données ou bloc parent. Vide pour une page placée directement dans l'espace de travail. Non disponible pour une pièce jointe
   * - ``notion.properties``
     - Table associant le nom de colonne au texte formaté, pour une ligne de base de données. Vide pour une page normale. Non disponible pour une pièce jointe
   * - ``notion.comments``
     - Le texte des commentaires de la page, réunis. Vide si ``include_comments=false`` ou si la page n'a pas de commentaires. Non disponible pour une pièce jointe
   * - ``notion.page_url``
     - URL de la page qui contient la pièce jointe. Pièces jointes uniquement
   * - ``notion.page_title``
     - Titre de la page qui contient la pièce jointe. Pièces jointes uniquement
   * - ``notion.size``
     - Taille de la pièce jointe en octets, lorsque Notion l'a indiquée. Pièces jointes uniquement

Périmètre de l'exploration
==========================

- Lorsque ni ``root_page_ids`` ni ``database_ids`` n'est défini, le connecteur utilise la recherche de Notion pour découvrir toutes les pages et bases de données partagées avec l'intégration.
  Notion ne garantit pas que la recherche soit exhaustive ; si du contenu manque dans l'index, définissez explicitement ``root_page_ids`` ou ``database_ids``.
- À partir de chaque point de départ, toutes les sous-pages et sous-bases de données accessibles sont également explorées, de sorte qu'une seule page racine suffit généralement pour atteindre toute une section d'un espace de travail.
- ``include_pattern`` et ``exclude_pattern`` déterminent uniquement si le document de cette page (ou pièce jointe) est indexé.
  Ils n'empêchent jamais la découverte des descendants : les blocs d'une page sont toujours parcourus avant que le motif soit comparé à l'URL de la page elle-même,
  de sorte que les sous-pages d'une page exclue sont quand même explorées et indexées sous leurs propres URL.
  Pour exclure un sous-arbre entier, le motif doit correspondre à toutes les URL situées en dessous, et pas seulement à sa racine.
- Une page ou une ligne de base de données qui se trouve dans la corbeille de Notion est ignorée.

Permissions
===========

L'API Notion n'expose pas les paramètres de partage d'une page ; ce connecteur ne peut donc pas synchroniser le contrôle d'accès par page.
Chaque document est indexé uniquement avec les permissions définies dans le champ « Permissions » de la configuration du Data Store.

.. warning::

   Tout ce qui est partagé avec l'intégration devient consultable par les rôles accordés dans ce champ, quelles que soient les personnes pouvant le voir dans Notion.
   Ne partagez l'intégration qu'avec les pages et bases de données que ces rôles doivent pouvoir rechercher.

Gestion des erreurs
===================

- Le crawl n'est interrompu que sur un HTTP ``401`` (le jeton ne peut pas s'authentifier) ou sur une réponse ``429`` qui mentionne ``public_api_request_blocked`` (le limiteur de débit de Notion bloque l'intégration).
  Le crawl est aussi interrompu si la recherche de Notion échoue alors que ni ``root_page_ids`` ni ``database_ids`` n'est défini, faute de point de départ.
- Toute autre erreur est traitée par document : un ``404`` ou ``403`` sur une page, une base de données, un fil de commentaires ou un bloc, ou l'épuisement de ``max_retry_count`` sur une requête, est consigné et ignoré, et le crawl continue.
- Chaque échec par document est enregistré sous "Crawler" -> "URL en échec" avec l'URL de ce document (l'URL Notion d'une page, ``<URL de la page>#<ID du bloc>`` pour une pièce jointe).
  L'URL de téléchargement signée d'une pièce jointe n'est jamais enregistrée ni consignée dans les journaux.
- Avec ``keep_expires_docs=false`` dans les paramètres, les documents du Data Store qui n'ont pas été réindexés lors d'un crawl sont supprimés à la fin de celui-ci, y compris lorsque le crawl est interrompu.
  Par défaut, les documents portent une date d'expiration et restent dans l'index jusqu'à celle-ci.

Exemples d'utilisation
======================

Explorer une arborescence de pages précise
------------------------------------------

Paramètres :

::

    token=secret_************************************
    root_page_ids=0123456789abcdef0123456789abcdef
    include_comments=false

Script :

::

    title=notion.title
    content=notion.content
    url=notion.url
    mimetype=notion.mimetype
    last_modified=notion.last_edited_time

Explorer une base de données
----------------------------

Paramètres :

::

    token=secret_************************************
    database_ids=fedcba9876543210fedcba9876543210
    include_files=false

Script :

::

    title=notion.title
    content=notion.content
    url=notion.url
    created=notion.created_time
    last_modified=notion.last_edited_time

Explorer tout ce qui est partagé avec l'intégration
---------------------------------------------------

Paramètres :

::

    token=secret_************************************
    request_interval=500

Dépannage
=========

Le crawl est interrompu immédiatement avec ``401``
--------------------------------------------------

Vérifiez que le jeton est bien l'« Internal Integration Secret » de l'intégration et que la capacité « Read content » est activée.

Des pages manquent dans l'index
-------------------------------

1. Vérifiez que l'intégration a été partagée avec la page ou la base de données
2. Si vous vous appuyez sur la découverte automatique, définissez explicitement ``root_page_ids`` ou ``database_ids``, car la recherche de Notion n'est pas garantie exhaustive
3. Vérifiez ``include_pattern`` et ``exclude_pattern``
4. Consultez "Crawler" -> "URL en échec" pour repérer les documents ayant échoué individuellement

Les commentaires ne sont pas indexés
------------------------------------

Activez la capacité « Read comments » de l'intégration. Sans elle, un avertissement est consigné une seule fois et les commentaires sont ignorés pour ce crawl.
Seuls les commentaires non résolus sont indexés.

Informations de référence
=========================

- :doc:`ds-overview` - Aperçu des connecteurs Data Store
- :doc:`ds-slack` - Connecteur Slack
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- :doc:`../../admin/failureurl-guide` - URL en échec
- :doc:`../../admin/plugin-guide` - Guide de gestion des plugins
- `Notion API Documentation <https://developers.notion.com/>`_
