==================================
Connecteur CSV
==================================

Aperçu
======

Le connecteur CSV fournit la fonctionnalité permettant de récupérer des données
à partir de fichiers CSV et de les enregistrer dans l'index |Fess|.

Cette fonctionnalité nécessite le plugin ``fess-ds-csv``.

Prérequis
=========

1. L'installation du plugin est requise
2. L'accès au fichier CSV est nécessaire
3. L'encodage des caractères du fichier CSV doit être connu

Installation du plugin
----------------------

Méthode 1 : Placement direct du fichier JAR

::

    # Télécharger depuis Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-csv/X.X.X/fess-ds-csv-X.X.X.jar

    # Placement
    cp fess-ds-csv-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # ou
    cp fess-ds-csv-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Méthode 2 : Installation depuis l'interface d'administration

1. Ouvrir « Système » → « Plugins »
2. Téléverser le fichier JAR
3. Redémarrer |Fess|

Configuration
=============

Configurez depuis l'interface d'administration via « Crawler » → « Data Store » → « Nouveau ».

Configuration de base
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Élément
     - Exemple
   * - Nom
     - Products CSV
   * - Nom du gestionnaire
     - CsvDataStore
   * - Activé
     - Oui

Configuration des paramètres
-----------------------------

Fichier local :

::

    files=/path/to/data.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="

Fichiers multiples :

::

    files=/path/to/data1.csv,/path/to/data2.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="

.. note::

   Le traitement des guillemets (quotes) et le traitement des échappements sont **activés par
   défaut** dans |Fess| 15.9. Les fichiers CSV conformes à la RFC 4180 (champs entre guillemets
   pouvant contenir des délimiteurs ou des sauts de ligne) sont analysés correctement sans qu'il
   soit nécessaire de spécifier le moindre paramètre.
   Pour savoir comment revenir au comportement précédent (désactiver le traitement des guillemets)
   et connaître les précautions à prendre, reportez-vous à la section « Désactivation du
   traitement des guillemets et des échappements » ci-dessous.

Liste des paramètres
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``files``
     - Non
     - Chemin du fichier CSV (chemin local, plusieurs fichiers séparés par des virgules). ``files`` ou ``directories`` doit être spécifié. Si les deux sont indiqués, ``files`` est prioritaire. Les fichiers spécifiés doivent avoir l'extension ``.csv`` ou ``.tsv`` ; les fichiers ayant une autre extension sont ignorés.
   * - ``directories``
     - Non
     - Chemin du répertoire contenant les fichiers CSV (plusieurs répertoires séparés par des virgules). Seuls les fichiers ``.csv`` et ``.tsv`` présents dans le répertoire sont traités. Utilisé si ``files`` n'est pas spécifié.
   * - ``file_encoding``
     - Non
     - Encodage des caractères (par défaut : UTF-8)
   * - ``has_header_line``
     - Non
     - Présence d'une ligne d'en-tête (par défaut : false)
   * - ``separator_character``
     - Non
     - Caractère de séparation (par défaut : virgule ``,``). Les séquences d'échappement telles que ``\t`` peuvent être spécifiées (séparation par tabulation).
   * - ``quote_character``
     - Non
     - Caractère de guillemet (par défaut : guillemet double ``"``). Le traitement des guillemets est activé par défaut (voir ``quote_disabled``).
   * - ``escape_character``
     - Non
     - Caractère d'échappement (par défaut : le même caractère que ``quote_character`` ; conformément à la RFC 4180, les guillemets sont échappés en les doublant). L'activation du traitement des échappements suit la valeur résolue de ``quote_disabled`` (voir ``escape_disabled``).

.. note::

   Si ``files`` et ``directories`` sont tous les deux vides, une erreur (``DataStoreException``) est
   générée. L'un ou l'autre doit obligatoirement être spécifié.

Paramètres avancés
~~~~~~~~~~~~~~~~~~

Les paramètres suivants permettent de contrôler finement le comportement d'analyse du CSV et de l'indexation :

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Paramètre
     - Description
   * - ``quote_disabled``
     - Désactive le traitement des guillemets (par défaut : false). Les champs entre guillemets conformes à la RFC 4180 sont analysés correctement par défaut. Spécifiez ``true`` pour revenir au comportement précédent (traiter les guillemets comme des caractères ordinaires).
   * - ``escape_disabled``
     - Désactive le traitement des échappements (par défaut : identique à la valeur résolue de ``quote_disabled``). Une valeur spécifiée explicitement est prioritaire.
   * - ``delete_old_docs``
     - Détermine si, une fois le crawl terminé, les documents appartenant à cette configuration Data Store et n'ayant pas été réenregistrés durant la session de crawl en cours doivent être supprimés de l'index (par défaut : true). Si vous injectez plusieurs fichiers CSV dans la même configuration Data Store à des moments différents, spécifiez ``false`` — sinon les documents enregistrés par les fichiers précédents seront supprimés (voir la section de dépannage ci-dessous pour plus de détails).
   * - ``keep_expires_docs``
     - Lors de la suppression via ``delete_old_docs``, détermine si les documents dont la date d'expiration (la valeur « expires » définie par exemple via ``time_to_live``) n'est pas encore atteinte doivent être exclus de la suppression (par défaut : true). Avec ``false``, les documents non réenregistrés sont supprimés même s'ils sont encore dans leur période de validité.
   * - ``time_to_live``
     - Nombre de minutes après l'enregistrement au bout desquelles la date d'expiration d'un document doit être définie (en minutes ; par défaut : non défini, c'est-à-dire pas d'expiration).
   * - ``skip_lines``
     - Nombre de lignes à ignorer en début de fichier (par défaut : 0)
   * - ``ignore_line_patterns``
     - Expression régulière pour ignorer certaines lignes (ex. : ``^#.*`` pour ignorer les lignes de commentaire)
   * - ``ignore_empty_lines``
     - Ignorer les lignes vides (par défaut : false)
   * - ``ignore_trailing_whitespaces``
     - Ignorer les espaces en fin de champ (par défaut : false)
   * - ``ignore_leading_whitespaces``
     - Ignorer les espaces en début de champ (par défaut : false)
   * - ``null_string``
     - Chaîne de caractères traitée comme valeur nulle
   * - ``break_string``
     - Chaîne de remplacement des sauts de ligne dans les valeurs de champ
   * - ``readInterval``
     - Temps d'attente après le traitement de chaque enregistrement (en millisecondes) (par défaut : 0)

Configuration du script
------------------------

Les valeurs de chaque champ sont construites en référençant les valeurs des colonnes du CSV. Les
colonnes CSV sont accessibles directement dans le script en tant que **variables sans préfixe** (sans
préfixe ``data.`` ni autre).

Avec en-tête (référence par nom de colonne) :

::

    url="https://example.com/product/" + product_id
    title=product_name
    content=description
    digest=category
    price=price

Sans en-tête (référence par index de colonne) :

::

    url="https://example.com/product/" + cell1
    title=cell2
    content=cell3
    price=cell4

Champs disponibles
~~~~~~~~~~~~~~~~~~

- ``<nom_colonne>`` — Référence directe par le nom de la colonne de la ligne d'en-tête (uniquement si ``has_header_line=true`` et si le nom de colonne n'est pas vide)
- ``cell<N>`` — Référence par index de colonne (``cell1``, ``cell2``... en commençant à 1 ; disponible que l'en-tête soit présent ou non)
- ``csvfile`` — Chemin complet du fichier CSV en cours de traitement
- ``csvfilename`` — Nom du fichier CSV en cours de traitement

.. note::

   Si un nom de colonne contient des caractères non valides comme identifiant de script (espaces,
   tirets, etc.), la référence par nom de colonne n'est pas possible. Dans ce cas, utilisez
   ``cell<N>``.

Détails du format CSV
=====================

CSV standard (conforme RFC 4180)
---------------------------------

::

    product_id,product_name,description,price,category
    1,Laptop,High-performance laptop,150000,Electronics
    2,Mouse,Wireless mouse,3000,Electronics
    3,"Book, Programming","Learn to code",2800,Books

.. note::

   Pour inclure un délimiteur dans un champ en l'entourant de guillemets (comme ``"Book, Programming"``
   ci-dessus), le champ est déjà analysé correctement comme une seule valeur avec le comportement par
   défaut (traitement des guillemets activé).
   Pour savoir comment revenir au comportement précédent (traiter les guillemets comme des caractères
   ordinaires et découper les champs au niveau du délimiteur), reportez-vous à la section
   « Désactivation du traitement des guillemets et des échappements » ci-dessous.

Désactivation du traitement des guillemets et des échappements
-----------------------------------------------------------------

Le traitement des guillemets et des échappements est activé par défaut dans |Fess| 15.9. Le
caractère de guillemet par défaut est le guillemet double ``"``, et le caractère d'échappement par
défaut est le même que le caractère de guillemet (échappé en le doublant, conformément à la RFC
4180) ; les fichiers CSV standard conformes à la RFC 4180 peuvent ainsi être analysés tels quels,
sans aucun paramètre.

.. warning::

   Lorsque le traitement des guillemets est activé, si un fichier CSV contient ne serait-ce qu'un
   seul ``"`` sans guillemet fermant correspondant, tout le reste du fichier à partir de ce
   guillemet (y compris les lignes suivantes) est lu comme une seule valeur de champ, et aucun
   document n'est généré pour les lignes restantes. Comme les versions précédentes analysaient
   chaque ligne indépendamment, ce comportement peut n'apparaître qu'après une mise à niveau.
   ``delete_old_docs`` (décrit ci-dessus) étant activé par défaut, cela peut entraîner la
   suppression non seulement des documents qui n'ont pas pu être générés, mais aussi de documents
   déjà enregistrés lors d'un crawl précédent.
   Avant la mise à niveau, vérifiez que vos fichiers CSV ne contiennent pas de guillemets non
   fermés, ou envisagez de spécifier ``quote_disabled=true`` pour revenir à la méthode d'analyse
   précédente.

Désactiver le traitement des guillemets (revenir au comportement précédent) :

::

    # Paramètre
    quote_disabled=true

Spécifier ``quote_disabled=true`` désactive également le traitement des échappements en même
temps (sauf si vous spécifiez explicitement ``escape_disabled=false``).

Désactiver uniquement le traitement des échappements :

::

    # Paramètre
    escape_disabled=true

Modification du séparateur
---------------------------

Séparation par tabulation (TSV) :

::

    # Paramètre
    separator_character=\t

Séparation par point-virgule :

::

    # Paramètre
    separator_character=;

Guillemet personnalisé
-----------------------

Guillemet simple :

::

    # Paramètre
    quote_character='

Encodage
--------

Fichier en Shift_JIS :

::

    file_encoding=Shift_JIS

Fichier en EUC-JP :

::

    file_encoding=EUC-JP

Exemples d'utilisation
=======================

Catalogue de produits CSV
--------------------------

Fichier CSV (products.csv) :

::

    product_id,name,description,price,category,in_stock
    1001,Ordinateur portable,Ordinateur portable haute performance,120000,Informatique,true
    1002,Souris,Souris sans fil,2500,Périphériques,true
    1003,Clavier,Clavier mécanique,8500,Périphériques,false

Paramètres :

::

    files=/var/data/products.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

Script :

::

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description + " Catégorie : " + category + " Prix : " + price + " EUR"
    digest=category
    price=price

Filtrage des informations de stock :

::

    url=in_stock == "true" ? "https://shop.example.com/product/" + product_id : null
    title=in_stock == "true" ? name : null
    content=in_stock == "true" ? description : null
    price=in_stock == "true" ? price : null

Annuaire des employés CSV
--------------------------

Fichier CSV (employees.csv) :

::

    emp_id,name,department,email,phone,position
    E001,Jean Dupont,Ventes,dupont@example.com,01-23-45-67-89,Directeur
    E002,Marie Martin,Développement,martin@example.com,01-34-56-78-90,Manager
    E003,Pierre Durand,Administration,durand@example.com,01-45-67-89-01,Responsable

Paramètres :

::

    files=/var/data/employees.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

Script :

::

    url="https://intranet.example.com/employee/" + emp_id
    title=name + " (" + department + ")"
    content="Département : " + department + "\nPoste : " + position + "\nEmail : " + email + "\nTéléphone : " + phone
    digest=department

CSV sans en-tête
-----------------

Fichier CSV (data.csv) :

::

    1,Produit A,Ceci est le produit A,1000
    2,Produit B,Ceci est le produit B,2000
    3,Produit C,Ceci est le produit C,3000

Paramètres :

::

    files=/var/data/data.csv
    file_encoding=UTF-8
    has_header_line=false
    separator_character=,

Script :

::

    url="https://example.com/item/" + cell1
    title=cell2
    content=cell3
    price=cell4

Intégration de plusieurs fichiers CSV
--------------------------------------

Paramètres :

::

    files=/var/data/2024-01.csv,/var/data/2024-02.csv,/var/data/2024-03.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

Script :

::

    url="https://example.com/report/" + id
    title=title
    content=content
    timestamp=date

Fichier séparé par tabulation (TSV)
-------------------------------------

Fichier TSV (data.tsv) :

::

    id	title	content	category
    1	Article 1	Contenu de l'article 1	Actualités
    2	Article 2	Contenu de l'article 2	Blog

Paramètres :

::

    files=/var/data/data.tsv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=\t

Script :

::

    url="https://example.com/article/" + id
    title=title
    content=content
    digest=category

Dépannage
==========

Fichier introuvable
--------------------

**Symptôme** : Le crawl s'exécute mais le fichier n'est pas traité ; le log affiche ``is not found``

**Points à vérifier** :

1. Vérifier si le chemin du fichier est correct (chemin absolu recommandé)
2. Vérifier si le fichier existe
3. Vérifier si l'extension du fichier est ``.csv`` ou ``.tsv`` (les autres extensions sont ignorées)
4. Vérifier si les droits de lecture sont accordés
5. Vérifier si l'utilisateur exécutant |Fess| peut y accéder

Caractères illisibles
----------------------

**Symptôme** : Les caractères ne s'affichent pas correctement

**Solution** :

Spécifier le bon encodage :

::

    # UTF-8
    file_encoding=UTF-8

    # Shift_JIS
    file_encoding=Shift_JIS

    # EUC-JP
    file_encoding=EUC-JP

    # Windows standard (CP932)
    file_encoding=Windows-31J

Vérifier l'encodage du fichier :

::

    file -i data.csv
    # ou
    nkf -g data.csv

Les colonnes ne sont pas reconnues correctement
------------------------------------------------

**Symptôme** : Les délimiteurs de colonnes ne sont pas reconnus correctement, ou les champs entre
guillemets sont découpés

**Points à vérifier** :

1. Vérifier si le caractère de séparation est correct :

   ::

       # Virgule
       separator_character=,

       # Tabulation
       separator_character=\t

       # Point-virgule
       separator_character=;

2. Les champs entre guillemets (champs contenant le délimiteur) sont analysés correctement par
   défaut. Vérifiez que vous n'avez pas spécifié ``quote_disabled=true`` par inadvertance.
3. Vérifier le format du fichier CSV (conformité RFC 4180). S'il contient un ``"`` sans guillemet
   fermant correspondant, tout le reste du fichier à partir de ce point est lu comme une seule
   valeur de champ.

Gestion de la ligne d'en-tête
-------------------------------

**Symptôme** : La première ligne est reconnue comme données

**Solution** :

Si une ligne d'en-tête existe :

::

    has_header_line=true

Si aucune ligne d'en-tête n'existe :

::

    has_header_line=false

Impossible de récupérer les données
-------------------------------------

**Symptôme** : Le crawl réussit mais le nombre d'éléments est 0

**Points à vérifier** :

1. Vérifier si le fichier CSV n'est pas vide
2. Vérifier si la configuration du script est correcte (les noms de colonnes et ``cell<N>`` sont
   référencés sans préfixe ``data.``)
3. Vérifier si les noms de colonnes sont corrects (si has_header_line=true)
4. Vérifier les messages d'erreur dans les logs
5. Vérifier qu'aucun nom de paramètre n'est mal orthographié (un nom de paramètre non
   reconnu est ignoré sans aucun avertissement ; ``has_headerline=true`` laisse par
   exemple ``has_header_line`` à sa valeur par défaut ``false``)

Les documents d'un crawl précédent disparaissent après un second import CSV
---------------------------------------------------------------------------

**Symptôme** : Après le crawl d'un premier fichier CSV, le crawl d'un second fichier CSV avec la
même configuration Data Store un jour ultérieur fait disparaître des résultats de recherche les
documents enregistrés à partir du premier fichier CSV.

**Cause** :

Une fois un crawl terminé, |Fess| supprime de l'index les documents appartenant à cette
configuration Data Store qui n'ont pas été réenregistrés pendant la session en cours
(``delete_old_docs``, par défaut : true). Si vous injectez plusieurs fichiers CSV dans la même
configuration Data Store à des moments différents, alors au moment du crawl du fichier le plus
récent, le contenu enregistré par le fichier précédent est considéré comme « non réenregistré
pendant la session en cours » et est supprimé.

**Solution** :

Si vous injectez plusieurs fichiers CSV dans la même configuration Data Store à des moments
différents et souhaitez que leur contenu s'accumule, spécifiez ce qui suit.

::

    delete_old_docs=false

Fichiers CSV volumineux
------------------------

**Symptôme** : Mémoire insuffisante ou timeout

**Solution** :

1. Diviser le fichier CSV en plusieurs parties
2. Utiliser uniquement les colonnes nécessaires dans le script
3. Augmenter la taille du tas de |Fess|
4. Filtrer les lignes inutiles

Champs contenant des sauts de ligne
-------------------------------------

Le format RFC 4180 permet de gérer les champs contenant des sauts de ligne en les entourant de
guillemets. Le traitement des guillemets étant activé par défaut, cela est analysé correctement sans qu'il
soit nécessaire de spécifier le moindre paramètre :

::

    id,title,description
    1,"Product A","This is
    a multi-line
    description"
    2,"Product B","Single line"

Paramètres :

::

    files=/var/data/data.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="

CsvListDataStore
================

Le plugin ``fess-ds-csv`` inclut, en plus de ``CsvDataStore``, le gestionnaire ``CsvListDataStore``.

``CsvListDataStore`` étend ``CsvDataStore`` et fournit les fonctionnalités supplémentaires suivantes :

- Traitement multi-thread (contrôlé par le paramètre ``numOfThreads``)
- Suppression automatique des fichiers CSV traités
- Filtrage des fichiers par horodatage (les fichiers en cours d'écriture sont ignorés)

Tous les paramètres et configurations de script de ``CsvDataStore`` sont utilisables tels quels.

Configuration de base
----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Élément
     - Exemple
   * - Nom du gestionnaire
     - CsvListDataStore

Paramètres supplémentaires
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``timestamp_margin``
     - Non
     - Délai écoulé depuis la dernière modification du fichier (en millisecondes). Les fichiers dont ce délai n'est pas écoulé sont considérés comme en cours d'écriture et sont ignorés (par défaut : 10000)
   * - ``numOfThreads``
     - Non
     - Nombre de threads de traitement (par défaut : 1)
   * - ``delete_processed_file``
     - Non
     - Détermine si le fichier CSV doit être supprimé une fois le traitement terminé (par défaut : true)
   * - ``ignore_data_store_exception``
     - Non
     - Détermine si le crawl global doit se poursuivre même si une exception se produit pendant le traitement d'un fichier CSV (par défaut : true)

.. warning::

   ``CsvListDataStore`` **supprime** automatiquement les fichiers CSV une fois leur traitement terminé (``delete_processed_file`` vaut ``true`` par défaut). En cas d'erreur pendant le traitement, le fichier est renommé avec l'extension ``.txt`` à la place (s'il est impossible de le renommer, il est supprimé). Si vous ne souhaitez pas que les fichiers soient supprimés, spécifiez ``delete_processed_file=false``.

Format de ligne CSV (type d'événement)
----------------------------------------

Les fichiers CSV transmis à ``CsvListDataStore`` doivent comporter au moins deux colonnes par
ligne : un « type d'événement » et une « URL ». Des colonnes supplémentaires peuvent être ajoutées
et référencées sous la forme ``cell3``, ``cell4``... (par exemple pour alimenter
``timestamp.overwrite``).

::

    <type_evenement>,<URL>

Le type d'événement peut prendre l'une des trois valeurs suivantes.

- ``create`` — un fichier a été créé
- ``modify`` — un fichier a été mis à jour
- ``delete`` — un fichier a été supprimé

``create`` et ``modify`` sont traités comme la même opération (crawl et indexation de l'URL
cible). Il n'y a aucune différence de comportement entre les deux.

Le nom de colonne (si un en-tête est présent) et la valeur de chaque type d'événement peuvent être
modifiés à l'aide des paramètres suivants.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Paramètre
     - Description
   * - ``field.event_type``
     - Nom de la colonne contenant le type d'événement (par défaut : ``event_type``)
   * - ``event.create``
     - Valeur représentant « créé » (par défaut : ``create``)
   * - ``event.modify``
     - Valeur représentant « mis à jour » (par défaut : ``modify``)
   * - ``event.delete``
     - Valeur représentant « supprimé » (par défaut : ``delete``)

Exemple de fichier CSV :

::

    modify,smb://servername/data/testfile1.txt
    delete,smb://servername/data/testfile2.txt

Exemple de script (sans en-tête) :

::

    event_type=cell1
    url=cell2

Écrasement des valeurs de champ (.overwrite)
----------------------------------------------

Ajouter ``.overwrite`` à la fin du nom d'un champ d'index construit dans le script fait que la
valeur de ce champ est écrasée par la valeur définie à partir du CSV, au lieu de la valeur obtenue
par le crawl réel du fichier cible.

::

    timestamp.overwrite=cell3

.. note::

   La facette de date de l'écran de recherche filtre à l'aide du champ ``timestamp``, et non
   ``created``. Si vous souhaitez écraser l'horodatage avec une valeur du CSV, spécifiez
   ``timestamp.overwrite`` plutôt que ``created.overwrite``.

Transmission des paramètres d'authentification et de proxy
------------------------------------------------------------

``CsvListDataStore`` effectue réellement le crawl des URL écrites dans le CSV, mais les paramètres
d'authentification et de proxy configurés dans la configuration Data Store du crawl de fichiers ou
du crawl Web ne sont pas transmis. Spécifiez individuellement les paramètres nécessaires en tant
que paramètres de cette configuration Data Store.

Exemple d'authentification SMB :

::

    crawler.file.auth=example
    crawler.file.auth.example.scheme=SAMBA
    crawler.file.auth.example.username=username
    crawler.file.auth.example.password=password

Exemple de configuration de proxy :

::

    crawler.web.proxyHost=proxy.example.com
    crawler.web.proxyPort=8080

Exemples d'utilisation avancée des scripts
==========================================

Traitement des données
-----------------------

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=Integer.parseInt(price)
    category=category.toLowerCase()

Indexation conditionnelle
--------------------------

::

    // Indexer uniquement les produits dont le prix est supérieur ou égal à 10000
    url=Integer.parseInt(price) >= 10000 ? "https://example.com/product/" + id : null
    title=Integer.parseInt(price) >= 10000 ? name : null
    content=Integer.parseInt(price) >= 10000 ? description : null
    price=Integer.parseInt(price) >= 10000 ? price : null

.. note::

   Comme indiqué ci-dessus, une ligne pour laquelle ``url`` renvoie ``null`` n'est pas traitée
   comme un échec, mais est ignorée silencieusement. Le nombre de lignes ignorées est comptabilisé
   par fichier CSV et affiché sous la forme d'un seul log WARN récapitulatif à la fin de la lecture
   de chaque fichier (les URL en échec ne sont pas journalisées individuellement ligne par ligne ;
   lors du traitement de plusieurs fichiers CSV, un log WARN est émis par fichier).

Concaténation de plusieurs colonnes
-------------------------------------

::

    url="https://example.com/product/" + id
    title=name
    content=description + "\n\nSpécifications :\n" + specs + "\n\nRemarques :\n" + notes
    category=category

Format de date
---------------

::

    url="https://example.com/article/" + id
    title=title
    content=content
    created=created_date
    // Si une conversion de format de date est nécessaire, un traitement supplémentaire est requis

Informations de référence
==========================

- :doc:`ds-overview` - Aperçu des connecteurs Data Store
- :doc:`ds-json` - Connecteur JSON
- :doc:`ds-database` - Connecteur de base de données
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- `RFC 4180 - Format CSV <https://datatracker.ietf.org/doc/html/rfc4180>`_
