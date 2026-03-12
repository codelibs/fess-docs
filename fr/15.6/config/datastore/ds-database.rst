==================================
Connecteur base de donnees
==================================

Apercu
======

Le connecteur de base de donnees fournit une fonctionnalite pour recuperer des donnees depuis
des bases de donnees relationnelles compatibles JDBC et les enregistrer dans l'index de |Fess|.

Cette fonctionnalite est integree a |Fess| et ne necessite pas de plugin supplementaire.

Bases de donnees prises en charge
=================================

Toutes les bases de donnees compatibles JDBC sont prises en charge. Exemples principaux :

- MySQL / MariaDB
- PostgreSQL
- Oracle Database
- Microsoft SQL Server
- SQLite
- H2 Database

Prerequis
=========

1. Un pilote JDBC est necessaire
2. Un acces en lecture a la base de donnees est requis
3. Pour les grands volumes de donnees, une conception de requete appropriee est importante

Installation du pilote JDBC
---------------------------

Placez le pilote JDBC dans le repertoire ``lib/`` :

::

    # Exemple : pilote MySQL
    cp mysql-connector-java-8.0.33.jar /path/to/fess/lib/

Redemarrez |Fess| pour charger le pilote.

Methode de configuration
========================

Configurez depuis l'interface d'administration : "Crawler" -> "DataStore" -> "Nouveau".

Configuration de base
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Element
     - Exemple de configuration
   * - Nom
     - Products Database
   * - Nom du handler
     - DatabaseDataStore
   * - Actif
     - Oui

Configuration des parametres
----------------------------

Exemple MySQL/MariaDB :

::

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://localhost:3306/mydb?useSSL=false&serverTimezone=UTC
    username=fess_user
    password=your_password
    sql=SELECT id, title, content, url, updated_at FROM articles WHERE deleted = 0

Exemple PostgreSQL :

::

    driver=org.postgresql.Driver
    url=jdbc:postgresql://localhost:5432/mydb
    username=fess_user
    password=your_password
    sql=SELECT id, title, content, url, updated_at FROM articles WHERE deleted = false

Liste des parametres
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametre
     - Requis
     - Description
   * - ``driver``
     - Oui
     - Nom de classe du pilote JDBC
   * - ``url``
     - Oui
     - URL de connexion JDBC
   * - ``username``
     - Oui
     - Nom d'utilisateur de la base de donnees
   * - ``password``
     - Oui
     - Mot de passe de la base de donnees
   * - ``sql``
     - Oui
     - Requete SQL pour la recuperation des donnees
   * - ``fetch.size``
     - Non
     - Taille de fetch (defaut : 100)

Configuration du script
-----------------------

Mappez les noms de colonnes SQL vers les champs d'index :

::

    url="https://example.com/articles/" + data.id
    title=data.title
    content=data.content
    lastModified=data.updated_at

Champs disponibles :

- ``data.<column_name>`` - Colonnes du resultat de la requete SQL

Conception des requetes SQL
===========================

Requetes efficaces
------------------

Pour les grands volumes de donnees, les performances de requete sont importantes :

::

    # Requete efficace utilisant un index
    SELECT id, title, content, url, updated_at
    FROM articles
    WHERE updated_at >= :last_crawl_date
    ORDER BY id

Exploration incrementale
------------------------

Methode pour recuperer uniquement les enregistrements mis a jour :

::

    # Filtrage par date de mise a jour
    sql=SELECT * FROM articles WHERE updated_at >= '2024-01-01 00:00:00'

    # Specification de plage par ID
    sql=SELECT * FROM articles WHERE id > 10000

Generation d'URL
----------------

L'URL du document est generee par le script :

::

    # Motif fixe
    url="https://example.com/article/" + data.id

    # Combinaison de plusieurs champs
    url="https://example.com/" + data.category + "/" + data.slug

    # Utilisation de l'URL stockee dans la base de donnees
    url=data.url

Prise en charge des caracteres multi-octets
===========================================

Pour traiter des donnees contenant des caracteres multi-octets comme le francais :

MySQL
-----

::

    url=jdbc:mysql://localhost:3306/mydb?useUnicode=true&characterEncoding=UTF-8

PostgreSQL
----------

PostgreSQL utilise generalement UTF-8 par defaut. Si necessaire :

::

    url=jdbc:postgresql://localhost:5432/mydb?charSet=UTF-8

Pooling de connexions
=====================

Pour le traitement de grands volumes de donnees, envisagez le pooling de connexions :

::

    # Configuration avec HikariCP
    datasource.class=com.zaxxer.hikari.HikariDataSource
    pool.size=5

Securite
========

Protection des identifiants de base de donnees
----------------------------------------------

.. warning::
   Ecrire les mots de passe directement dans les fichiers de configuration presente un risque de securite.

Methodes recommandees :

1. Utiliser des variables d'environnement
2. Utiliser la fonctionnalite de chiffrement de |Fess|
3. Utiliser un utilisateur en lecture seule

Principe du moindre privilege
-----------------------------

Accordez uniquement les privileges minimum necessaires a l'utilisateur de la base de donnees :

::

    -- Exemple MySQL
    CREATE USER 'fess_user'@'localhost' IDENTIFIED BY 'password';
    GRANT SELECT ON mydb.articles TO 'fess_user'@'localhost';

Exemples d'utilisation
======================

Recherche de catalogue de produits
----------------------------------

Parametres :

::

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://localhost:3306/shop
    username=fess_user
    password=password
    sql=SELECT p.id, p.name, p.description, p.price, c.name as category, p.updated_at FROM products p JOIN categories c ON p.category_id = c.id WHERE p.active = 1

Script :

::

    url="https://shop.example.com/product/" + data.id
    title=data.name
    content=data.description + " Categorie: " + data.category + " Prix: " + data.price + " EUR"
    lastModified=data.updated_at

Articles de base de connaissances
---------------------------------

Parametres :

::

    driver=org.postgresql.Driver
    url=jdbc:postgresql://localhost:5432/knowledge
    username=fess_user
    password=password
    sql=SELECT id, title, body, tags, author, created_at, updated_at FROM articles WHERE published = true ORDER BY id

Script :

::

    url="https://kb.example.com/article/" + data.id
    title=data.title
    content=data.body
    digest=data.tags
    author=data.author
    created=data.created_at
    lastModified=data.updated_at

Depannage
=========

Pilote JDBC introuvable
-----------------------

**Symptome** : ``ClassNotFoundException`` ou ``No suitable driver``

**Solution** :

1. Verifiez que le pilote JDBC est place dans ``lib/``
2. Verifiez que le nom de classe du pilote est correct
3. Redemarrez |Fess|

Erreur de connexion
-------------------

**Symptome** : ``Connection refused`` ou erreur d'authentification

**Points a verifier** :

1. La base de donnees est-elle demarree ?
2. Le nom d'hote et le numero de port sont-ils corrects ?
3. Le nom d'utilisateur et le mot de passe sont-ils corrects ?
4. Configuration du pare-feu

Erreur de requete
-----------------

**Symptome** : ``SQLException`` ou erreur de syntaxe SQL

**Points a verifier** :

1. Testez la requete SQL directement sur la base de donnees
2. Verifiez que les noms de colonnes sont corrects
3. Verifiez que les noms de tables sont corrects

Informations de reference
=========================

- :doc:`ds-overview` - Apercu des connecteurs DataStore
- :doc:`ds-csv` - Connecteur CSV
- :doc:`ds-json` - Connecteur JSON
- :doc:`../../admin/dataconfig-guide` - Guide de configuration DataStore
