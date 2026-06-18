==============================
Connecteur JSON
==============================

Apercu
======

Le connecteur JSON fournit la fonctionnalite permettant de recuperer des donnees
a partir de fichiers JSONL locaux (format JSON Lines) et de les enregistrer dans
l'index |Fess|.

Cette fonctionnalite necessite le plugin ``fess-ds-json``.

Prerequis
=========

1. L'installation du plugin est requise
2. L'acces aux fichiers JSON est necessaire
3. La structure du JSON doit etre comprise

Installation du plugin
----------------------

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
=============

Configurez depuis l'interface d'administration via "Crawler" -> "Data Store" -> "Nouveau".

Configuration de base
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Element
     - Exemple de configuration
   * - Nom
     - Products JSON
   * - Nom du gestionnaire
     - JsonDataStore
   * - Actif
     - Oui

Configuration des parametres
-----------------------------

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
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Parametre
     - Requis
     - Description
   * - ``files``
     - Non
     - Chemin des fichiers JSON a traiter (plusieurs valeurs possibles, separees par des virgules). Seuls les fichiers avec l'extension ``.json`` ou ``.jsonl`` sont traites.
   * - ``directories``
     - Non
     - Chemin des repertoires contenant les fichiers JSON (plusieurs valeurs possibles, separees par des virgules)
   * - ``fileEncoding``
     - Non
     - Encodage des caracteres (par defaut : UTF-8)

.. warning::
   Il est necessaire de specifier ``files`` ou ``directories``.
   Si aucun des deux n'est specifie (vide), une ``DataStoreException`` sera levee.
   Si les deux sont specifies, ``files`` a la priorite et ``directories`` est ignore.

.. note::
   Le nom du parametre est en camelCase : ``fileEncoding`` (et non en snake_case : ``file_encoding``).

Comportement lors de la specification d'un repertoire
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lorsque ``directories`` est specifie, les fichiers directement dans chaque repertoire sont traites selon les regles suivantes.

- **Les sous-repertoires ne sont pas parcourus** (pas d'exploration recursive).
- Seuls les fichiers avec l'extension ``.json`` ou ``.jsonl`` sont concernes (sans distinction de casse).
- Les fichiers sont traites dans l'ordre croissant de leur date de modification (date de derniere modification).

.. note::
   Ce connecteur traite uniquement les fichiers JSON sur le systeme de fichiers local. L'acces HTTP et les fonctions d'authentification API ne sont pas pris en charge.

Configuration des scripts
--------------------------

La valeur de chaque champ est construite en referençant les valeurs des champs de l'objet JSON.
Les champs de niveau superieur de l'objet JSON sont directement accessibles dans les scripts
sous forme de **variables sans prefixe** (sans prefixe tel que ``data.``).

Objet JSON simple :

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=price
    category=category

Objet JSON imbrique (les objets imbriques sont references comme des maps) :

::

    url="https://example.com/product/" + id
    title=product.name
    content=product.description
    price=product.pricing.amount
    author=product.author.name

Traitement des elements de tableau :

::

    url="https://example.com/article/" + id
    title=title
    content=body
    tags=tags.join(", ")
    categories=categories[0].name

Champs disponibles
~~~~~~~~~~~~~~~~~~

- ``<nom_champ>`` - Reference directe par nom d'un champ de niveau superieur de l'objet JSON
- ``<parent>.<enfant>`` - Champ d'un objet imbrique
- ``<tableau>[<indice>]`` - Element de tableau
- ``<tableau>.<methode>`` - Methodes de tableau (``join``, ``collect``, ``size``, etc.)

.. note::

   Si un nom de champ contient des caracteres invalides comme identificateur Groovy
   (espaces, tirets, etc.), ce champ ne peut pas etre reference directement comme variable.

Details du format JSON
=======================

Format de fichier JSON
-----------------------

Le connecteur JSON lit les fichiers au format JSONL (JSON Lines).
C'est un format ou un objet JSON est ecrit par ligne. Le fichier est lu ligne par ligne,
et chaque ligne est analysee comme un objet JSON independant.

.. note::
   Les fichiers avec l'extension ``.json`` sont egalement traites, mais leur contenu
   doit etre au format JSONL (un objet par ligne).
   Les fichiers JSON au format tableau ( ``[{...}, {...}]`` ) ou mis en forme sur plusieurs
   lignes (pretty-print) ne peuvent pas etre lus directement. Veuillez les convertir
   au format JSONL.

Fichier au format JSONL :

::

    {"id": 1, "name": "Product A", "description": "Description A"}
    {"id": 2, "name": "Product B", "description": "Description B"}

Exemples d'utilisation
=======================

Catalogue de produits
----------------------

Parametres :

::

    files=/var/data/products.json
    fileEncoding=UTF-8

Scripts :

::

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description + " Prix : " + price + " yens"
    digest=category
    price=price

Integration de plusieurs fichiers JSON
---------------------------------------

Parametres :

::

    files=/var/data/data1.json,/var/data/data2.json
    fileEncoding=UTF-8

Scripts :

::

    url="https://example.com/item/" + id
    title=title
    content=content

Depannage
==========

Fichier introuvable
--------------------

**Symptome** : ``... is not found.`` ou ``Source file ... does not exist.`` apparait dans les journaux

**Verifications** :

1. Verifier que le chemin du fichier est correct
2. Verifier que le fichier existe
3. Verifier que l'extension du fichier est ``.json`` ou ``.jsonl``
4. Verifier les permissions de lecture du fichier

Erreur d'analyse JSON
----------------------

**Symptome** : ``Crawling Access Exception`` et ``JsonParseException`` apparaissent dans les journaux

Si une ligne invalide est rencontree, seule cette ligne est ignoree et enregistree comme URL
en echec ; le crawl continue a partir de la ligne suivante.

**Verifications** :

1. Verifier que le fichier JSON est au bon format (JSONL : un objet par ligne) :

   ::

       # Valider que chaque ligne est un objet JSON valide
       cat data.json | jq -c .

2. Verifier l'encodage des caracteres
3. Verifier qu'un seul objet ne s'etend pas sur plusieurs lignes
4. Verifier l'absence de commentaires (non autorises dans la norme JSON)

Aucune donnee recuperee
------------------------

**Symptome** : Le crawl reussit mais le nombre de resultats est 0

**Verifications** :

1. Verifier la structure JSON
2. Verifier la configuration des scripts (les references de champs ne doivent pas avoir de prefixe ``data.``)
3. Verifier les noms de champs (y compris la casse)
4. Verifier les messages d'erreur dans les journaux

Fichiers JSON volumineux
-------------------------

**Symptome** : Memoire insuffisante ou delai d'attente depasse

Les fichiers etant lus ligne par ligne, la taille totale du fichier n'affecte pas directement
la consommation memoire. Des problemes peuvent toutefois survenir si une seule ligne
(un objet) est extremement grande ou si la charge d'indexation est elevee.

**Solutions** :

1. Diviser le fichier JSON en plusieurs fichiers
2. Augmenter la taille du tas (heap) de |Fess|

Utilisation avancee des scripts
================================

Traitement conditionnel
------------------------

Chaque champ est evalue comme une expression independante. Pour les valeurs conditionnelles,
utilisez l'operateur ternaire :

::

    url=status == "published" ? "https://example.com/product/" + id : null
    title=status == "published" ? name : null
    content=status == "published" ? description : null
    price=status == "published" ? price : null

Jointure de tableaux
---------------------

::

    url="https://example.com/article/" + id
    title=title
    content=content
    tags=tags ? tags.join(", ") : ""
    categories=categories.collect { it.name }.join(", ")

Configuration des valeurs par defaut
--------------------------------------

::

    url="https://example.com/item/" + id
    title=title ?: "Sans titre"
    content=description ?: (summary ?: "Sans description")
    price=price ?: 0

Formatage des dates
--------------------

::

    url="https://example.com/post/" + id
    title=title
    content=body
    created=created_at
    last_modified=updated_at

Traitement des nombres
-----------------------

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=price as Float
    stock=stock_quantity as Integer

Informations de reference
==========================

- :doc:`ds-overview` - Apercu des connecteurs Data Store
- :doc:`ds-csv` - Connecteur CSV
- :doc:`ds-database` - Connecteur de base de donnees
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSON Lines <https://jsonlines.org/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
