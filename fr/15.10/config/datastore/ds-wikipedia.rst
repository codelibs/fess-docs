==================================
Connecteur Wikipedia
==================================

Aperçu
======

Le connecteur Wikipedia fournit la fonctionnalité permettant de lire un fichier de dump Wikipedia
et d'enregistrer ses pages dans l'index |Fess|.
Il fonctionne avec les dumps de Wikipedia, d'autres projets Wikimedia et de tout site MediaWiki.

Cette fonctionnalité nécessite le plugin ``fess-ds-wikipedia``.

Dumps pris en charge
====================

Le paramètre ``source`` sélectionne le format du dump.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - ``source``
     - Description
   * - ``cirrus``
     - Un dump d'index CirrusSearch, que Wikimedia publie pour ses wikis sous
       ``https://dumps.wikimedia.org/other/cirrus_search_index/``. Il contient le texte que MediaWiki a lui-même rendu, avec les modèles développés,
       de sorte qu'aucun balisage wikitext n'atteint l'index. C'est le format recommandé pour Wikipedia et les autres wikis Wikimedia
   * - ``xml``
     - Un export XML MediaWiki (``*-pages-articles.xml.bz2``, ou la sortie de ``Special:Export`` ou de ``dumpBackup.php`` de n'importe quel MediaWiki).
       Il contient du wikitext, que le connecteur convertit en texte brut (voir « Texte brut des dumps XML »)
   * - ``auto``
     - La valeur par défaut. Un emplacement qui contient ``cirrus_search_index`` ou se termine par ``.json.bz2`` ou ``.json`` est lu comme ``cirrus`` ; tout autre emplacement est lu comme ``xml``

La compression d'un dump (bzip2 ou gzip, par exemple) est détectée à partir de son contenu, et un fichier non compressé peut également être lu.

Prérequis
=========

1. L'installation du plugin est requise
2. Le fichier de dump doit être accessible, sous forme d'URL HTTP(S) ou de chemin sur le serveur |Fess|
3. Du temps pour le crawl : le dump d'une grande Wikipedia représente plusieurs gigaoctets. Essayez d'abord une configuration avec ``limit``

Installation du plugin
----------------------

Installez depuis l'interface d'administration via "Système" -> "Plugins", ou exécutez ``bin/fess-setup install plugin fess-ds-wikipedia``
puis redémarrez |Fess|.
Consultez :doc:`../../admin/plugin-guide` pour plus de détails.

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
     - Japanese Wikipedia
   * - Nom du gestionnaire
     - WikipediaDataStore
   * - Activé
     - Oui

Configuration des paramètres
----------------------------

::

    url=https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2
    limit=10000

Liste des paramètres
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``url``
     - Non
     - Emplacement du dump : une URL HTTP(S), une URL ``file:`` ou un chemin local. La valeur par défaut est le dump de Wikipedia en anglais
       (``http://download.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2``) ; indiquez donc ce paramètre explicitement.
       Pour les formes acceptées avec ``source=cirrus``, voir « Dumps CirrusSearch »
   * - ``source``
     - Non
     - ``auto``, ``cirrus`` ou ``xml`` (par défaut : ``auto``)
   * - ``limit``
     - Non
     - S'arrêter après ce nombre de pages. ``0`` signifie aucune limite (par défaut : ``0``). Utile pour essayer une configuration sur un petit nombre de pages
   * - ``user_agent``
     - Non
     - En-tête User-Agent envoyé lors du téléchargement du dump. S'il n'est pas indiqué, le nom de User-Agent du crawler |Fess| est utilisé
   * - ``max_digest_length``
     - Non
     - Longueur maximale de ``digest``, en caractères (par défaut : ``100``)
   * - ``total_entity_size_limit``
     - Non
     - Limite supérieure, en octets, de la taille totale des entités traitées par l'analyseur XML (par défaut : ``100000000``). S'applique uniquement à ``source=xml``
   * - ``text_extractor``
     - Non
     - Comment le wikitext d'un dump XML est converti en texte brut : ``sweble`` (par défaut) ou ``regex``. Voir « Texte brut des dumps XML »
   * - ``drop_templates``
     - Non
     - Noms de modèles, séparés par des virgules, dont le texte est supprimé du contenu d'un dump XML, ou ``*`` pour tous les modèles
   * - ``keep_templates``
     - Non
     - Noms de modèles, séparés par des virgules, dont le texte est conservé bien que ``drop_templates`` les désigne
   * - ``drop_captions``
     - Non
     - Supprimer les légendes d'images et de galeries du contenu d'un dump XML (par défaut : ``false``)

Dumps CirrusSearch
~~~~~~~~~~~~~~~~~~

Un dump CirrusSearch est publié en fragments numérotés, comme ``jawiki_content-20261004-00000.json.bz2``.
Avec ``source=cirrus``, ``url`` accepte une liste séparée par des virgules dont chaque entrée peut être :

- un fichier unique (une URL HTTP(S) ou un chemin local)
- un répertoire local : tous les fichiers qu'il contient dont le nom se termine par ``.json.bz2`` ou ``.json`` sont lus, dans l'ordre des noms
- une URL HTTP(S) qui se termine par ``/`` : le listing du répertoire est récupéré et tous les fichiers dont le nom se termine par ``.json.bz2`` ou ``.json`` sont lus, dans l'ordre des noms

Par exemple, pour lire tous les fragments de l'index de contenu de Wikipedia en japonais :

::

    url=https://dumps.wikimedia.org/other/cirrus_search_index/20261004/index_name=jawiki_content/
    source=cirrus

.. note::

   Wikimedia supprime les anciennes dates du serveur. Cherchez une date existante dans le listing de
   ``https://dumps.wikimedia.org/other/cirrus_search_index/`` avant de configurer le crawl.

Configuration du script
-----------------------

::

    lang="ja"
    filetype=format
    filename=title
    url="https://ja.wikipedia.org/wiki/" + encodedTitle
    host="ja.wikipedia.org"
    site="ja.wikipedia.org"
    title=title
    content=content
    digest=digest
    anchor=
    content_length=content.length()
    last_modified=timestamp
    timestamp=timestamp

Champs disponibles
~~~~~~~~~~~~~~~~~~

Les valeurs suivantes peuvent être référencées depuis le script.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``id``
     - ID de la page
   * - ``title``
     - Titre de la page
   * - ``encodedTitle``
     - Le titre sous la forme utilisée dans l'URL d'une page MediaWiki (les espaces deviennent ``_`` et les autres caractères sont encodés en pourcentage)
   * - ``content``
     - Texte brut de la page
   * - ``digest``
     - ``content`` abrégé à ``max_digest_length`` caractères
   * - ``contentLength``
     - Longueur de ``content``
   * - ``wikitext``
     - Wikitext de la page, si le dump le contient
   * - ``format``, ``model``
     - Format et modèle de contenu de la page
   * - ``timestamp``
     - Horodatage de la page
   * - ``ns``
     - Numéro de l'espace de noms
   * - ``categories``, ``links``
     - Catégories de la page et pages vers lesquelles elle pointe
   * - ``redirect``, ``redirectTitle``
     - Si la page est une redirection, et sa cible
   * - ``stub``, ``disambiguation``
     - Si la page est une ébauche, et si c'est une page d'homonymie
   * - ``lang``, ``host``, ``site``, ``url``
     - Déduits de l'emplacement du dump. Voir « Valeurs déduites de l'emplacement du dump »

Avec ``source=cirrus``, les valeurs suivantes sont également disponibles :

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``openingText``
     - Le texte d'ouverture de la page
   * - ``headings``
     - Titres de section
   * - ``externalLinks``
     - Liens externes
   * - ``templates``
     - Modèles utilisés par la page
   * - ``redirects``
     - Titres qui redirigent vers la page
   * - ``auxiliaryText``
     - Texte auxiliaire, comme les légendes d'images
   * - ``weightedTags``
     - Tags pondérés
   * - ``wikibaseItem``
     - ID de l'élément Wikidata
   * - ``incomingLinks``
     - Nombre de liens entrants
   * - ``popularityScore``
     - Score de popularité
   * - ``revisionId``
     - ID de la révision

Valeurs déduites de l'emplacement du dump
-----------------------------------------

``lang``, ``host``, ``site`` et ``url`` sont déduits du nom du dump : un nom comme ``jawiki-latest-pages-articles.xml.bz2``
ou ``index_name=jawiki_content`` donne ``lang`` ``ja``, ``host`` et ``site`` ``ja.wikipedia.org`` et ``url`` ``https://ja.wikipedia.org/wiki/<titre encodé>``.
Le nom doit contenir le code de langue immédiatement suivi de ``wiki`` puis de ``-``, ``_`` ou ``.``.
Les projets frères comme Wikiquote (``jawikiquote-...``) ne sont volontairement pas déduits, car un mauvais hôte produirait des liens morts.

.. warning::

   Lorsque le nom du dump ne correspond pas, ``host``, ``site`` et ``url`` ne sont pas définis, et ``url`` conserve la valeur du paramètre ``url``,
   c'est-à-dire l'emplacement du dump. Si le script utilise ``url`` tel quel, toutes les pages obtiennent la même URL et l'ensemble du crawl se retrouve en un seul document dans l'index,
   sans aucune erreur.
   Pour un dump renommé ou un autre projet Wikimedia, construisez l'URL dans le script, comme le fait l'exemple ci-dessus, par exemple
   ``url="https://ja.wikiquote.org/wiki/" + encodedTitle``.

Texte brut des dumps XML
------------------------

Avec ``source=xml``, le wikitext est converti en texte brut avec l'analyseur de wikitext Sweble. Les noms des espaces de noms sont lus dans le ``<siteinfo>`` de l'export,
de sorte que les images et les déclarations de catégorie sont reconnues dans n'importe quelle langue (``[[ファイル:...]]``, ``[[Kategorie:...]]``) et dans les wikis ayant leurs propres noms d'espaces de noms.
Une page sur laquelle Sweble échoue est convertie avec des expressions régulières.

``text_extractor=regex`` utilise des expressions régulières pour toutes les pages. C'est plusieurs fois plus rapide, mais les modèles imbriqués, les tableaux et le balisage multiligne restent dans le texte.

Par défaut, le texte de chaque argument de modèle (sans les noms de paramètres) et chaque légende d'image et de galerie sont conservés dans ``content``, afin que ce texte puisse être retrouvé.
Utilisez ``drop_templates``, ``keep_templates`` et ``drop_captions`` pour le filtrer :

::

    # Supprimer le texte de ces modèles, y compris lorsqu'ils sont imbriqués ("*" supprime tous les modèles)
    drop_templates=Cite web,Cite news,Use dmy dates
    # Conserver ces modèles bien que drop_templates les désigne
    # (drop_templates=* avec keep_templates=Note,Warning ne conserve que ces deux-là)
    keep_templates=
    # Supprimer les légendes d'images et de galeries
    drop_captions=false

Les noms de modèles sont comparés comme MediaWiki les résout : la première lettre est insensible à la casse, ``_`` équivaut à une espace, et le préfixe ``Template:`` est facultatif.
Les modèles ne sont pas développés ; un modèle conservé apporte donc le texte de ses arguments, et non ce que MediaWiki rendrait.
Un dump CirrusSearch contient déjà le texte rendu par MediaWiki ; ces paramètres ne s'appliquent donc pas à ``source=cirrus``.

Exemples d'utilisation
======================

Wikipedia en japonais à partir d'un dump CirrusSearch
-----------------------------------------------------

Paramètres :

::

    url=https://dumps.wikimedia.org/other/cirrus_search_index/20261004/index_name=jawiki_content/
    source=cirrus

Script :

::

    lang="ja"
    filetype=format
    filename=title
    url="https://ja.wikipedia.org/wiki/" + encodedTitle
    host="ja.wikipedia.org"
    site="ja.wikipedia.org"
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=timestamp
    timestamp=timestamp

Wikipedia en japonais à partir d'un dump XML, sans les modèles de citation
--------------------------------------------------------------------------

Paramètres :

::

    url=https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2
    source=xml
    drop_templates=Cite web,Cite news
    limit=10000

Le script est le même que dans « Configuration du script ».

Un autre projet Wikimedia (Wikiquote)
-------------------------------------

Le nom de dump ``jawikiquote-...`` ne permet pas de déduire ``host`` et ``url`` ; construisez-les donc dans le script.

Script :

::

    lang="ja"
    url="https://ja.wikiquote.org/wiki/" + encodedTitle
    host="ja.wikiquote.org"
    site="ja.wikiquote.org"
    title=title
    content=content
    digest=digest
    last_modified=timestamp
    timestamp=timestamp

Dépannage
=========

Un seul document est indexé
---------------------------

Voir « Valeurs déduites de l'emplacement du dump ». Vérifiez que le script définit ``url`` pour chaque page.

Le crawl est trop long
----------------------

1. Commencez avec ``limit`` pour confirmer la configuration
2. Utilisez ``source=cirrus``, ou ``text_extractor=regex`` pour un dump XML
3. Placez le dump sur le serveur |Fess| et indiquez un chemin local

Du balisage wikitext reste dans le contenu
------------------------------------------

Utilisez un dump CirrusSearch (``source=cirrus``). Avec ``source=xml``, ``text_extractor=regex`` laisse dans le texte les modèles imbriqués, les tableaux et le balisage multiligne ; utilisez donc ``sweble`` (la valeur par défaut).

Le dump ne peut pas être lu
---------------------------

1. Vérifiez que l'URL ou le chemin est correct (la date d'un dump CirrusSearch a peut-être été supprimée du serveur)
2. Pour une URL de répertoire, vérifiez qu'elle se termine par ``/`` et que les fichiers qu'elle contient se terminent par ``.json.bz2`` ou ``.json``
3. Consultez le journal pour connaître l'erreur exacte

Informations de référence
=========================

- :doc:`ds-overview` - Aperçu des connecteurs Data Store
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- :doc:`../../admin/plugin-guide` - Guide de gestion des plugins
- `Wikimedia Downloads <https://dumps.wikimedia.org/>`_
- `CirrusSearch index dumps <https://dumps.wikimedia.org/other/cirrus_search_index/>`_
