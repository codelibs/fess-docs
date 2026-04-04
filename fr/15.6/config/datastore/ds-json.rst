==================================
Connecteur JSON
==================================

Apercu
====

Le connecteur JSON fournit la fonctionnalite permettant de recuperer des donnees
a partir de fichiers JSON ou JSONL locaux et de les enregistrer dans l'index |Fess|.

Cette fonctionnalite necessite le plugin ``fess-ds-json``.

Prerequis
========

1. L'installation du plugin est requise
2. L'acces aux fichiers JSON est necessaire
3. La structure du JSON doit etre comprise

Installation du plugin
------------------------

Methode 1 : Placement direct du fichier JAR

::

    # Telecharger depuis Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-json/X.X.X/fess-ds-json-X.X.X.jar

    # Placement
    cp fess-ds-json-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # ou
    cp fess-ds-json-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

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
     - Products JSON
   * - Nom du gestionnaire
     - JsonDataStore
   * - Active
     - Oui

Configuration des parametres
----------------

Fichier local :

::

    files=/path/to/data.json
    fileEncoding=UTF-8

Fichiers multiples :

::

    files=/path/to/data1.json,/path/to/data2.json
    fileEncoding=UTF-8

Specification de repertoire :

::

    directories=/path/to/json_dir/
    fileEncoding=UTF-8

Liste des parametres
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametre
     - Requis
     - Description
   * - ``files``
     - Non
     - Chemin du fichier JSON (plusieurs separes par des virgules)
   * - ``directories``
     - Non
     - Chemin du repertoire contenant les fichiers JSON
   * - ``fileEncoding``
     - Non
     - Encodage des caracteres (par defaut : UTF-8)

.. warning::
   Il est necessaire de specifier ``files`` ou ``directories``.
   Si aucun n'est specifie, une ``DataStoreException`` sera levee.
   Si les deux sont specifies, ``files`` a la priorite et ``directories`` est ignore.

.. note::
   Ce connecteur ne prend en charge que les fichiers JSON sur le systeme de fichiers local. L'acces HTTP et les fonctions d'authentification API ne sont pas pris en charge.

Configuration des scripts
--------------

Objet JSON simple :

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=data.price
    category=data.category

Objet JSON imbrique :

::

    url="https://example.com/product/" + data.id
    title=data.product.name
    content=data.product.description
    price=data.product.pricing.amount
    author=data.product.author.name

Traitement des elements de tableau :

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.body
    tags=data.tags.join(", ")
    categories=data.categories[0].name

Champs disponibles
~~~~~~~~~~~~~~~~~~~~

- ``data.<nom_champ>`` - Champ de l'objet JSON
- ``data.<parent>.<enfant>`` - Objet imbrique
- ``data.<tableau>[<indice>]`` - Element de tableau
- ``data.<tableau>.<methode>`` - Methodes de tableau (join, length, etc.)

Details du format JSON
==============

Format de fichier JSON
----------------

Le connecteur JSON lit les fichiers au format JSONL (JSON Lines).
C'est un format ou un objet JSON est ecrit par ligne.

.. note::
   Les fichiers JSON au format tableau ( ``[{...}, {...}]`` ) ne peuvent pas etre lus directement.
   Veuillez convertir au format JSONL.

Fichier au format JSONL :

::

    {"id": 1, "name": "Product A", "description": "Description A"}
    {"id": 2, "name": "Product B", "description": "Description B"}

Exemples d'utilisation
======

Catalogue de produits
--------------

Parametres :

::

    files=/var/data/products.json
    fileEncoding=UTF-8

Scripts :

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " Prix : " + data.price + " EUR"
    digest=data.category
    price=data.price

Integration de plusieurs fichiers JSON
---------------------

Parametres :

::

    files=/var/data/data1.json,/var/data/data2.json
    fileEncoding=UTF-8

Scripts :

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

Depannage
======================

Fichier introuvable
----------------------

**Symptome** : ``FileNotFoundException``

**Verifications** :

1. Verifier que le chemin du fichier est correct
2. Verifier que le fichier existe
3. Verifier les permissions de lecture du fichier

Erreur d'analyse JSON
--------------

**Symptome** : ``JsonParseException`` ou ``Unexpected character``

**Verifications** :

1. Verifier que le fichier JSON est au bon format :

   ::

       # Validation du JSON
       cat data.json | jq .

2. Verifier l'encodage des caracteres
3. Verifier l'absence de caracteres ou de sauts de ligne non valides
4. Verifier l'absence de commentaires (non autorises dans la norme JSON)

Aucune donnee recuperee
--------------------

**Symptome** : Le crawl reussit mais le nombre de resultats est 0

**Verifications** :

1. Verifier la structure JSON
2. Verifier la configuration des scripts
3. Verifier les noms de champs (y compris les majuscules et minuscules)
4. Verifier les messages d'erreur dans les journaux

Fichiers JSON volumineux
------------------

**Symptome** : Memoire insuffisante ou delai d'attente depasse

**Solution** :

1. Diviser le fichier JSON en plusieurs fichiers
2. Augmenter la taille du heap de |Fess|

Utilisation avancee des scripts
========================

Traitement conditionnel
------------

Chaque champ est evalue comme une expression independante. Pour les valeurs conditionnelles, utilisez l'operateur ternaire :

::

    url=data.status == "published" ? "https://example.com/product/" + data.id : null
    title=data.status == "published" ? data.name : null
    content=data.status == "published" ? data.description : null
    price=data.status == "published" ? data.price : null

Jointure de tableaux
----------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    tags=data.tags ? data.tags.join(", ") : ""
    categories=data.categories.collect { it.name }.join(", ")

Configuration des valeurs par defaut
------------------

::

    url="https://example.com/item/" + data.id
    title=data.title ?: "Sans titre"
    content=data.description ?: (data.summary ?: "Pas de description")
    price=data.price ?: 0

Formatage des dates
------------------

::

    url="https://example.com/post/" + data.id
    title=data.title
    content=data.body
    created=data.created_at
    last_modified=data.updated_at

Traitement des nombres
----------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=data.price as Float
    stock=data.stock_quantity as Integer

Informations de reference
========

- :doc:`ds-overview` - Apercu des connecteurs Data Store
- :doc:`ds-csv` - Connecteur CSV
- :doc:`ds-database` - Connecteur de base de donnees
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSONPath <https://goessner.net/articles/JsonPath/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
