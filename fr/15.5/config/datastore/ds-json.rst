==================================
Connecteur JSON
==================================

Apercu
====

Le connecteur JSON fournit la fonctionnalite permettant de recuperer des donnees
a partir de fichiers JSON ou d'API JSON et de les enregistrer dans l'index |Fess|.

Cette fonctionnalite necessite le plugin ``fess-ds-json``.

Prerequis
========

1. L'installation du plugin est requise
2. L'acces au fichier JSON ou a l'API est necessaire
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

    file_path=/path/to/data.json
    encoding=UTF-8
    json_path=$

Fichier HTTP :

::

    file_path=https://api.example.com/products.json
    encoding=UTF-8
    json_path=$.data

API REST (avec authentification) :

::

    file_path=https://api.example.com/v1/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    auth_type=bearer
    auth_token=your_api_token_here

Fichiers multiples :

::

    file_path=/path/to/data1.json,https://api.example.com/data2.json
    encoding=UTF-8
    json_path=$

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
     - Chemin du fichier JSON ou URL de l'API (plusieurs separes par des virgules)
   * - ``encoding``
     - Non
     - Encodage des caracteres (par defaut : UTF-8)
   * - ``json_path``
     - Non
     - Chemin d'extraction JSONPath (par defaut : ``$``)
   * - ``http_method``
     - Non
     - Methode HTTP (GET, POST, etc., par defaut : GET)
   * - ``auth_type``
     - Non
     - Type d'authentification (bearer, basic)
   * - ``auth_token``
     - Non
     - Token d'authentification (pour authentification bearer)
   * - ``auth_username``
     - Non
     - Nom d'utilisateur (pour authentification basic)
   * - ``auth_password``
     - Non
     - Mot de passe (pour authentification basic)
   * - ``http_headers``
     - Non
     - En-tetes HTTP personnalises (format JSON)

Configuration du script
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
- ``data.<tableau>[<index>]`` - Element de tableau
- ``data.<tableau>.<methode>`` - Methodes de tableau (join, length, etc.)

Details du format JSON
==============

Tableau simple
----------

::

    [
      {
        "id": 1,
        "name": "Product A",
        "description": "Description A",
        "price": 1000
      },
      {
        "id": 2,
        "name": "Product B",
        "description": "Description B",
        "price": 2000
      }
    ]

Parametres :

::

    json_path=$

Structure imbriquee
--------------

::

    {
      "data": {
        "products": [
          {
            "id": 1,
            "name": "Product A",
            "details": {
              "description": "Description A",
              "price": 1000,
              "category": {
                "id": 10,
                "name": "Electronics"
              }
            }
          }
        ]
      }
    }

Parametres :

::

    json_path=$.data.products

Script :

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.details.description
    price=data.details.price
    category=data.details.category.name

Tableau complexe
----------

::

    {
      "articles": [
        {
          "id": 1,
          "title": "Article 1",
          "content": "Content 1",
          "tags": ["tag1", "tag2", "tag3"],
          "author": {
            "name": "John Doe",
            "email": "john@example.com"
          }
        }
      ]
    }

Parametres :

::

    json_path=$.articles

Script :

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    author=data.author.name
    tags=data.tags.join(", ")

Utilisation de JSONPath
===============

Qu'est-ce que JSONPath
------------

JSONPath est un langage de requete pour specifier des elements dans du JSON.
C'est l'equivalent de XPath pour XML.

Syntaxe de base
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Syntaxe
     - Description
   * - ``$``
     - Element racine
   * - ``$.field``
     - Champ de niveau superieur
   * - ``$.parent.child``
     - Champ imbrique
   * - ``$.array[0]``
     - Premier element du tableau
   * - ``$.array[*]``
     - Tous les elements du tableau
   * - ``$..field``
     - Recherche recursive

Exemples JSONPath
-------------

Tous les elements (racine) :

::

    json_path=$

Tableau specifique :

::

    json_path=$.data.items

Tableau imbrique :

::

    json_path=$.response.results.products

Recherche recursive :

::

    json_path=$..products

Exemples d'utilisation
======

API de catalogue de produits
---------------

Reponse API :

::

    {
      "status": "success",
      "data": {
        "products": [
          {
            "product_id": "P001",
            "name": "Laptop",
            "description": "High-performance laptop",
            "price": 120000,
            "category": "Computer",
            "in_stock": true
          }
        ]
      }
    }

Parametres :

::

    file_path=https://api.example.com/products
    encoding=UTF-8
    json_path=$.data.products

Script :

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " Prix: " + data.price + " EUR"
    digest=data.category
    price=data.price

API d'articles de blog
-------------

Reponse API :

::

    {
      "posts": [
        {
          "id": 1,
          "title": "Titre de l'article",
          "body": "Corps de l'article...",
          "author": {
            "name": "Jean Dupont",
            "email": "dupont@example.com"
          },
          "tags": ["technologie", "programmation"],
          "published_at": "2024-01-15T10:00:00Z"
        }
      ]
    }

Parametres :

::

    file_path=https://blog.example.com/api/posts
    encoding=UTF-8
    json_path=$.posts

Script :

::

    url="https://blog.example.com/post/" + data.id
    title=data.title
    content=data.body
    author=data.author.name
    tags=data.tags.join(", ")
    created=data.published_at

API avec authentification Bearer
---------------

Parametres :

::

    file_path=https://api.example.com/v1/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    auth_type=bearer
    auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Script :

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.description

API avec authentification Basic
--------------

Parametres :

::

    file_path=https://api.example.com/data
    encoding=UTF-8
    json_path=$.data
    http_method=GET
    auth_type=basic
    auth_username=apiuser
    auth_password=password123

Script :

::

    url="https://example.com/data/" + data.id
    title=data.name
    content=data.content

Utilisation d'en-tetes personnalises
----------------------

Parametres :

::

    file_path=https://api.example.com/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    http_headers={"X-API-Key":"your-api-key","Accept":"application/json"}

Script :

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

Integration de plusieurs fichiers JSON
---------------------

Parametres :

::

    file_path=/var/data/data1.json,/var/data/data2.json,https://api.example.com/data3.json
    encoding=UTF-8
    json_path=$.items

Script :

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

Requete POST
--------------

Parametres :

::

    file_path=https://api.example.com/search
    encoding=UTF-8
    json_path=$.results
    http_method=POST
    http_headers={"Content-Type":"application/json"}
    post_body={"query":"search term","limit":100}

Script :

::

    url="https://example.com/result/" + data.id
    title=data.title
    content=data.content

Depannage
======================

Fichier introuvable
----------------------

**Symptome** : ``FileNotFoundException`` ou ``404 Not Found``

**Points a verifier** :

1. Verifier si le chemin du fichier ou l'URL est correct
2. Verifier si le fichier existe
3. Pour les URL, verifier si l'API fonctionne
4. Verifier la connexion reseau

Erreur d'analyse JSON
--------------

**Symptome** : ``JsonParseException`` ou ``Unexpected character``

**Points a verifier** :

1. Verifier si le fichier JSON est au bon format :

   ::

       # Validation JSON
       cat data.json | jq .

2. Verifier si l'encodage des caracteres est correct
3. Verifier s'il y a des caracteres ou sauts de ligne invalides
4. Verifier s'il y a des commentaires (non autorises dans le standard JSON)

Erreur JSONPath
--------------

**Symptome** : Impossible de recuperer les donnees ou resultat vide

**Points a verifier** :

1. Verifier si la syntaxe JSONPath est correcte
2. Verifier si l'element cible existe
3. Valider le JSONPath avec un outil de test :

   ::

       # Verification avec jq
       cat data.json | jq '$.data.products'

4. Verifier si le chemin pointe vers la bonne hierarchie

Erreur d'authentification
----------

**Symptome** : ``401 Unauthorized`` ou ``403 Forbidden``

**Points a verifier** :

1. Verifier si le type d'authentification est correct (bearer, basic)
2. Verifier si le token ou le nom d'utilisateur/mot de passe est correct
3. Verifier la date d'expiration du token
4. Verifier les parametres de permission de l'API

Impossible de recuperer les donnees
--------------------

**Symptome** : Le crawl reussit mais le nombre d'elements est 0

**Points a verifier** :

1. Verifier si le JSONPath pointe vers le bon element
2. Verifier la structure JSON
3. Verifier si la configuration du script est correcte
4. Verifier si les noms de champs sont corrects (incluant la casse)
5. Verifier les messages d'erreur dans les logs

Traitement des tableaux
----------

Si le JSON est un tableau :

::

    [
      {"id": 1, "name": "Item 1"},
      {"id": 2, "name": "Item 2"}
    ]

Parametres :

::

    json_path=$

Si le JSON est un objet contenant un tableau :

::

    {
      "items": [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"}
      ]
    }

Parametres :

::

    json_path=$.items

Fichiers JSON volumineux
------------------

**Symptome** : Memoire insuffisante ou timeout

**Solution** :

1. Diviser le fichier JSON en plusieurs parties
2. Extraire uniquement les parties necessaires avec JSONPath
3. Pour les API, utiliser la pagination
4. Augmenter la taille du tas de |Fess|

Limitation de debit API
-------------

**Symptome** : ``429 Too Many Requests``

**Solution** :

1. Augmenter l'intervalle de crawl
2. Verifier la limitation de debit de l'API
3. Repartir la charge avec plusieurs cles API

Exemples d'utilisation avancee des scripts
========================

Traitement conditionnel
------------

::

    if (data.status == "published" && data.price > 1000) {
        url="https://example.com/product/" + data.id
        title=data.name
        content=data.description
        price=data.price
    }

Concatenation de tableaux
----------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    tags=data.tags ? data.tags.join(", ") : ""
    categories=data.categories.map(function(c) { return c.name; }).join(", ")

Definition de valeurs par defaut
------------------

::

    url="https://example.com/item/" + data.id
    title=data.title || "Sans titre"
    content=data.description || data.summary || "Pas de description"
    price=data.price || 0

Format de date
------------------

::

    url="https://example.com/post/" + data.id
    title=data.title
    content=data.body
    created=data.created_at
    last_modified=data.updated_at

Traitement numerique
----------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=parseFloat(data.price)
    stock=parseInt(data.stock_quantity)

Informations de reference
========

- :doc:`ds-overview` - Apercu des connecteurs Data Store
- :doc:`ds-csv` - Connecteur CSV
- :doc:`ds-database` - Connecteur de base de donnees
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSONPath <https://goessner.net/articles/JsonPath/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
