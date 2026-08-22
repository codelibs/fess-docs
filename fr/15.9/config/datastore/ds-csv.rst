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
    quote_disabled=false

Fichiers multiples :

::

    files=/path/to/data1.csv,/path/to/data2.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="
    quote_disabled=false

.. note::

   Le traitement des guillemets (quotes) et le traitement des échappements sont **désactivés** par
   défaut. Pour traiter des CSV conformes à la RFC 4180 (champs entre guillemets pouvant contenir des
   délimiteurs ou des sauts de ligne), spécifiez explicitement ``quote_disabled=false`` pour activer
   le traitement des guillemets. Reportez-vous à la section « Activation du traitement des guillemets
   et des échappements » ci-dessous pour plus de détails.

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
     - Caractère de guillemet (par défaut : guillemet double ``"``). Notez que le traitement des guillemets est désactivé par défaut (voir ``quote_disabled``).
   * - ``escape_character``
     - Non
     - Caractère d'échappement (par défaut : barre oblique inverse ``\``). Notez que le traitement des échappements est désactivé par défaut (voir ``escape_disabled``).

.. note::

   Si ``files`` et ``directories`` sont tous les deux vides, une erreur (``DataStoreException``) est
   générée. L'un ou l'autre doit obligatoirement être spécifié.

Paramètres avancés
~~~~~~~~~~~~~~~~~~

Les paramètres suivants permettent de contrôler finement le comportement d'analyse du CSV :

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Paramètre
     - Description
   * - ``quote_disabled``
     - Désactive le traitement des guillemets (par défaut : true). Spécifiez ``false`` pour traiter des champs entre guillemets conformes à la RFC 4180.
   * - ``escape_disabled``
     - Désactive le traitement des échappements (par défaut : true). Spécifiez ``false`` pour activer l'échappement via ``escape_character``.
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

   Si un nom de colonne contient des caractères non valides comme identifiant Groovy (espaces,
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
   ci-dessus), il est nécessaire de spécifier ``quote_disabled=false`` afin d'activer le traitement
   des guillemets. Lorsque le traitement des guillemets est désactivé (comportement par défaut), les
   guillemets sont traités comme des caractères ordinaires et les champs sont découpés au niveau du
   délimiteur.

Activation du traitement des guillemets et des échappements
------------------------------------------------------------

Le traitement des guillemets et des échappements est désactivé par défaut. Activez-les explicitement
comme suit.

Activer le traitement des guillemets :

::

    # Paramètre
    quote_disabled=false
    quote_character="

Activer le traitement des échappements :

::

    # Paramètre
    escape_disabled=false
    escape_character=\

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

Guillemet simple (l'activation du traitement des guillemets est requise) :

::

    # Paramètre
    quote_disabled=false
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

2. Pour traiter des champs entre guillemets (champs contenant le délimiteur), activer le traitement
   des guillemets :

   ::

       quote_disabled=false

3. Vérifier le format du fichier CSV (conformité RFC 4180)

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
guillemets. Le traitement des guillemets étant désactivé par défaut, il est nécessaire de spécifier
``quote_disabled=false`` :

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
    quote_disabled=false
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

.. note::

   ``CsvListDataStore`` supprime automatiquement les fichiers CSV après leur traitement. En cas
   d'erreur pendant le traitement, le fichier est renommé avec l'extension ``.txt`` (s'il est
   impossible de le renommer, il est supprimé).

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
