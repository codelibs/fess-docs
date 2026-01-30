==================================
Connecteur CSV
==================================

Apercu
====

Le connecteur CSV fournit la fonctionnalite permettant de recuperer des donnees
a partir de fichiers CSV et de les enregistrer dans l'index |Fess|.

Cette fonctionnalite necessite le plugin ``fess-ds-csv``.

Prerequis
========

1. L'installation du plugin est requise
2. L'acces au fichier CSV est necessaire
3. L'encodage des caracteres du fichier CSV doit etre connu

Installation du plugin
------------------------

Methode 1 : Placement direct du fichier JAR

::

    # Telecharger depuis Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-csv/X.X.X/fess-ds-csv-X.X.X.jar

    # Placement
    cp fess-ds-csv-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # ou
    cp fess-ds-csv-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Methode 2 : Installation depuis l'interface d'administration

1. Ouvrir "Systeme" -> "Plugins"
2. Telecharger le fichier JAR
3. Redemarrer |Fess|

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
     - Products CSV
   * - Nom du gestionnaire
     - CsvDataStore
   * - Active
     - Oui

Configuration des parametres
----------------

Fichier local :

::

    file_path=/path/to/data.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Fichier HTTP :

::

    file_path=https://example.com/data/products.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Fichiers multiples :

::

    file_path=/path/to/data1.csv,/path/to/data2.csv,https://example.com/data3.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Liste des parametres
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametre
     - Requis
     - Description
   * - ``file_path``
     - Oui
     - Chemin du fichier CSV (local, HTTP, plusieurs fichiers separes par des virgules)
   * - ``encoding``
     - Non
     - Encodage des caracteres (par defaut : UTF-8)
   * - ``has_header``
     - Non
     - Presence d'une ligne d'en-tete (par defaut : true)
   * - ``separator``
     - Non
     - Caractere de separation (par defaut : virgule ``,``)
   * - ``quote``
     - Non
     - Caractere de citation (par defaut : guillemet double ``"``)

Configuration du script
--------------

Avec en-tete :

::

    url="https://example.com/product/" + data.product_id
    title=data.product_name
    content=data.description
    digest=data.category
    price=data.price

Sans en-tete (index de colonne) :

::

    url="https://example.com/product/" + data.col0
    title=data.col1
    content=data.col2
    price=data.col3

Champs disponibles
~~~~~~~~~~~~~~~~~~~~

- ``data.<nom_colonne>`` - Nom de colonne de la ligne d'en-tete (si has_header=true)
- ``data.col<N>`` - Index de colonne (si has_header=false, commence a 0)

Details du format CSV
=============

CSV standard (conforme RFC 4180)
-----------------------

::

    product_id,product_name,description,price,category
    1,Laptop,High-performance laptop,150000,Electronics
    2,Mouse,Wireless mouse,3000,Electronics
    3,"Book, Programming","Learn to code",2800,Books

Modification du separateur
------------------

Tabulation (TSV) :

::

    # Parametre
    separator=\t

Point-virgule :

::

    # Parametre
    separator=;

Caractere de citation personnalise
--------------

Guillemet simple :

::

    # Parametre
    quote='

Encodage
----------------

Fichier japonais (Shift_JIS) :

::

    encoding=Shift_JIS

Fichier japonais (EUC-JP) :

::

    encoding=EUC-JP

Exemples d'utilisation
======

Catalogue de produits CSV
-----------------

Fichier CSV (products.csv) :

::

    product_id,name,description,price,category,in_stock
    1001,Laptop,High-performance laptop,120000,Computer,true
    1002,Mouse,Wireless mouse,2500,Peripherals,true
    1003,Keyboard,Mechanical keyboard,8500,Peripherals,false

Parametres :

::

    file_path=/var/data/products.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Script :

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " Categorie: " + data.category + " Prix: " + data.price + " EUR"
    digest=data.category
    price=data.price

Filtrage des informations de stock :

::

    if (data.in_stock == "true") {
        url="https://shop.example.com/product/" + data.product_id
        title=data.name
        content=data.description
        price=data.price
    }

Annuaire des employes CSV
-------------

Fichier CSV (employees.csv) :

::

    emp_id,name,department,email,phone,position
    E001,Jean Dupont,Ventes,dupont@example.com,01-23-45-67-89,Directeur
    E002,Marie Martin,Developpement,martin@example.com,01-34-56-78-90,Manager
    E003,Pierre Durand,Administration,durand@example.com,01-45-67-89-01,Responsable

Parametres :

::

    file_path=/var/data/employees.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Script :

::

    url="https://intranet.example.com/employee/" + data.emp_id
    title=data.name + " (" + data.department + ")"
    content="Departement: " + data.department + "\nPoste: " + data.position + "\nEmail: " + data.email + "\nTelephone: " + data.phone
    digest=data.department

CSV sans en-tete
-----------------

Fichier CSV (data.csv) :

::

    1,Produit A,Ceci est le produit A,1000
    2,Produit B,Ceci est le produit B,2000
    3,Produit C,Ceci est le produit C,3000

Parametres :

::

    file_path=/var/data/data.csv
    encoding=UTF-8
    has_header=false
    separator=,
    quote="

Script :

::

    url="https://example.com/item/" + data.col0
    title=data.col1
    content=data.col2
    price=data.col3

Integration de plusieurs fichiers CSV
---------------------

Parametres :

::

    file_path=/var/data/2024-01.csv,/var/data/2024-02.csv,/var/data/2024-03.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Script :

::

    url="https://example.com/report/" + data.id
    title=data.title
    content=data.content
    timestamp=data.date

Recuperation de CSV depuis HTTP
-----------------

Parametres :

::

    file_path=https://example.com/data/products.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Script :

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description

Fichier separe par tabulation (TSV)
-------------------------

Fichier TSV (data.tsv) :

::

    id	title	content	category
    1	Article1	Contenu de l'article 1	Actualites
    2	Article2	Contenu de l'article 2	Blog

Parametres :

::

    file_path=/var/data/data.tsv
    encoding=UTF-8
    has_header=true
    separator=\t
    quote="

Script :

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    digest=data.category

Depannage
======================

Fichier introuvable
----------------------

**Symptome** : ``FileNotFoundException`` ou ``No such file``

**Points a verifier** :

1. Verifier si le chemin du fichier est correct (chemin absolu recommande)
2. Verifier si le fichier existe
3. Verifier si les droits de lecture sont accordes
4. Verifier si l'utilisateur executant |Fess| peut y acceder

Caracteres illisibles
------------------

**Symptome** : Les caracteres speciaux ne s'affichent pas correctement

**Solution** :

Specifier le bon encodage :

::

    # UTF-8
    encoding=UTF-8

    # Windows (CP1252)
    encoding=Windows-1252

    # ISO-8859-1
    encoding=ISO-8859-1

Verifier l'encodage du fichier :

::

    file -i data.csv

Les colonnes ne sont pas reconnues correctement
----------------------

**Symptome** : Les delimiteurs de colonnes ne sont pas reconnus correctement

**Points a verifier** :

1. Verifier si le caractere de separation est correct :

   ::

       # Virgule
       separator=,

       # Tabulation
       separator=\t

       # Point-virgule
       separator=;

2. Verifier le parametre de citation
3. Verifier le format du fichier CSV (conformite RFC 4180)

Gestion de la ligne d'en-tete
----------------

**Symptome** : La premiere ligne est reconnue comme donnees

**Solution** :

Si une ligne d'en-tete existe :

::

    has_header=true

Si aucune ligne d'en-tete n'existe :

::

    has_header=false

Impossible de recuperer les donnees
--------------------

**Symptome** : Le crawl reussit mais le nombre d'elements est 0

**Points a verifier** :

1. Verifier si le fichier CSV n'est pas vide
2. Verifier si la configuration du script est correcte
3. Verifier si les noms de colonnes sont corrects (si has_header=true)
4. Verifier les messages d'erreur dans les logs

Fichiers CSV volumineux
-----------------

**Symptome** : Memoire insuffisante ou timeout

**Solution** :

1. Diviser le fichier CSV en plusieurs parties
2. Utiliser uniquement les colonnes necessaires dans le script
3. Augmenter la taille du tas de |Fess|
4. Filtrer les lignes inutiles

Champs contenant des sauts de ligne
--------------------

Le format RFC 4180 permet de gerer les champs contenant des sauts de ligne en les entourant de guillemets :

::

    id,title,description
    1,"Product A","This is
    a multi-line
    description"
    2,"Product B","Single line"

Parametres :

::

    file_path=/var/data/data.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Exemples d'utilisation avancee des scripts
========================

Traitement des donnees
------------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=parseInt(data.price)
    category=data.category.toLowerCase()

Indexation conditionnelle
--------------------

::

    # Uniquement les produits dont le prix est superieur ou egal a 10000
    if (parseInt(data.price) >= 10000) {
        url="https://example.com/product/" + data.id
        title=data.name
        content=data.description
        price=data.price
    }

Concatenation de plusieurs colonnes
------------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description + "\n\nSpecifications:\n" + data.specs + "\n\nRemarques:\n" + data.notes
    category=data.category

Format de date
------------------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    created=data.created_date
    # Si une conversion de format de date est necessaire, un traitement supplementaire est requis

Informations de reference
========

- :doc:`ds-overview` - Apercu des connecteurs Data Store
- :doc:`ds-json` - Connecteur JSON
- :doc:`ds-database` - Connecteur de base de donnees
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- `RFC 4180 - Format CSV <https://datatracker.ietf.org/doc/html/rfc4180>`_
