============================================================
Connecteur de base de données (recherche de base de données)
============================================================

Aperçu
======

Le connecteur de base de données permet d'enregistrer dans l'index de |Fess| les enregistrements de bases de données relationnelles compatibles JDBC (MySQL, PostgreSQL, Oracle, SQL Server, etc.), afin de réaliser une recherche de base de données (recherche en texte intégral sur une base de données). Chaque colonne récupérée par une instruction SELECT est mappée à un champ de recherche lors de l'enregistrement.

Le connecteur de base de données fournit une fonctionnalité pour récupérer des données depuis
des bases de données relationnelles compatibles JDBC et les enregistrer dans l'index de |Fess|.

Cette fonctionnalité nécessite le plugin ``fess-ds-db``.

Bases de données prises en charge
==================================

Toutes les bases de données compatibles JDBC sont prises en charge. Exemples principaux :

- MySQL / MariaDB
- PostgreSQL
- Oracle Database
- Microsoft SQL Server
- SQLite
- H2 Database

Prérequis
=========

1. L'installation du plugin ``fess-ds-db`` est nécessaire
2. Un pilote JDBC adapté à la base de données cible est requis
3. Un accès en lecture à la base de données est requis
4. Pour les grands volumes de données, une conception de requête appropriée est importante

Installation du plugin
----------------------

Méthode 1 : Déposer le fichier JAR directement

::

    # Téléchargement depuis Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-db/X.X.X/fess-ds-db-X.X.X.jar

    # Déploiement
    cp fess-ds-db-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # ou
    cp fess-ds-db-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Méthode 2 : Installer depuis l'interface d'administration

1. Ouvrir « Système » → « Plugins »
2. Téléverser le fichier JAR
3. Redémarrer |Fess|

Installation du pilote JDBC
----------------------------

Placez le pilote JDBC adapté à la base de données cible dans le répertoire ``app/WEB-INF/lib/`` du classpath de |Fess| :

::

    # Exemple : pilote MySQL
    cp mysql-connector-j-8.x.x.jar $FESS_HOME/app/WEB-INF/lib/
    # ou
    cp mysql-connector-j-8.x.x.jar /usr/share/fess/app/WEB-INF/lib/

Une fois le pilote JDBC déposé, redémarrez |Fess| pour le charger.

Méthode de configuration
========================

Configurez depuis l'interface d'administration : « Crawler » → « DataStore » → « Nouveau ».

Configuration de base
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Élément
     - Exemple de configuration
   * - Nom
     - Products Database
   * - Nom du handler
     - DatabaseDataStore
   * - Actif
     - Oui

Configuration des paramètres
-----------------------------

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

Liste des paramètres
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Paramètre
     - Requis
     - Description
   * - ``driver``
     - Oui
     - Nom de classe du pilote JDBC (si absent, une ``DataStoreException`` est levée)
   * - ``url``
     - Oui
     - URL de connexion JDBC (obligatoire pour la connexion)
   * - ``sql``
     - Oui
     - Requête SQL pour la récupération des données (si absente, une ``DataStoreException`` est levée)
   * - ``username``
     - Non
     - Nom d'utilisateur de la base de données
   * - ``password``
     - Non
     - Mot de passe de la base de données
   * - ``fetch_size``
     - Non
     - Taille de fetch JDBC. Pour le streaming de résultats MySQL, spécifiez ``MIN_VALUE``
   * - ``default_mimetype``
     - Non
     - Type MIME par défaut utilisé lors de l'extraction du contenu des colonnes BLOB/binaires
   * - ``column_label.mimetype``
     - Non
     - Nom de la colonne contenant le type MIME à utiliser pour l'extraction d'une colonne BLOB/binaire (ex. : ``column_label.mimetype=content_type``)
   * - ``column_label.filename``
     - Non
     - Nom de la colonne contenant le nom de fichier à utiliser pour l'extraction d'une colonne BLOB/binaire (le type MIME est déduit de l'extension)
   * - ``info.*``
     - Non
     - Propriétés de connexion JDBC supplémentaires (ex. : ``info.ssl=true``). La clé sans le préfixe ``info.`` est transmise au pilote JDBC
   * - ``readInterval``
     - Non
     - Délai en millisecondes entre le traitement de chaque ligne. Par défaut : 0
   * - ``script_type``
     - Non
     - Type du moteur de script. Par défaut : groovy

Configuration du script
-----------------------

Mappez les noms de colonnes SQL vers les champs d'index :

::

    url="https://example.com/articles/" + id
    title=title
    content=content
    lastModified=updated_at

Champs disponibles :

- ``<column_name>`` - Colonnes du résultat de la requête SQL (accès direct par le nom de colonne. Aucun préfixe tel que ``data.`` n'est ajouté)

.. note::
   Le nom de colonne doit correspondre au libellé de colonne (alias) de la clause ``SELECT``.
   Pour les fonctions d'agrégation ou les expressions, utilisez explicitement ``AS`` pour définir un alias
   (ex. : ``COUNT(*) AS total``).

Chargement de données BLOB/binaires
=====================================

Les colonnes de type BLOB, CLOB, NCLOB, tableau d'octets ou flux binaire sont automatiquement
soumises au traitement d'extraction de contenu (le même extracteur que pour le crawl de fichiers)
et intégrées sous forme de texte. Les colonnes de type tableau sont converties en chaîne séparée
par des espaces. Les valeurs NULL deviennent des chaînes vides.

Pour extraire correctement du texte depuis des BLOB ou des flux binaires, il est nécessaire de
déterminer le type de données (type MIME). La priorité de détermination est la suivante :

1. ``column_label.mimetype=<nom_de_colonne>`` - Utilise la valeur de la colonne spécifiée comme type MIME
2. ``column_label.filename=<nom_de_colonne>`` - Traite la valeur de la colonne spécifiée comme un nom de fichier et déduit le type MIME à partir de l'extension
3. ``default_mimetype`` - Type MIME par défaut utilisé si aucune des méthodes ci-dessus ne permet de déterminer le type

Exemple (extraction du BLOB de la colonne ``file_data`` en utilisant le type MIME de la colonne ``content_type``) :

::

    sql=SELECT id, title, file_data, content_type FROM documents
    column_label.mimetype=content_type

Conception des requêtes SQL
============================

Requêtes efficaces
------------------

Pour les grands volumes de données, les performances de requête sont importantes.
La requête SQL est envoyée telle quelle à la base de données (aucune liaison de paramètres n'est effectuée) :

::

    SELECT id, title, content, url, updated_at
    FROM articles
    WHERE updated_at >= '2024-01-01 00:00:00'
    ORDER BY id

Exploration incrémentale
------------------------

Méthode pour récupérer uniquement les enregistrements mis à jour :

::

    # Filtrage par date de mise à jour
    sql=SELECT * FROM articles WHERE updated_at >= '2024-01-01 00:00:00'

    # Spécification de plage par ID
    sql=SELECT * FROM articles WHERE id > 10000

Génération d'URL
----------------

L'URL du document est générée par le script :

::

    # Modèle fixe
    url="https://example.com/article/" + id

    # Combinaison de plusieurs champs
    url="https://example.com/" + category + "/" + slug

    # Utilisation de l'URL stockée dans la base de données
    url=url

Prise en charge des caractères multi-octets
============================================

Pour traiter des données contenant des caractères multi-octets tels que le japonais :

MySQL
-----

::

    url=jdbc:mysql://localhost:3306/mydb?useUnicode=true&characterEncoding=UTF-8

PostgreSQL
----------

PostgreSQL utilise généralement UTF-8 par défaut. Si nécessaire :

::

    url=jdbc:postgresql://localhost:5432/mydb?charSet=UTF-8

Sécurité
========

Protection des identifiants de base de données
-----------------------------------------------

.. warning::
   Écrire les mots de passe directement dans les fichiers de configuration présente un risque de sécurité.

Méthodes recommandées :

1. Utiliser des variables d'environnement
2. Utiliser la fonctionnalité de chiffrement de |Fess|
3. Utiliser un utilisateur en lecture seule

Principe du moindre privilège
------------------------------

Accordez uniquement les privilèges minimum nécessaires à l'utilisateur de la base de données :

::

    -- Exemple MySQL
    CREATE USER 'fess_user'@'localhost' IDENTIFIED BY 'password';
    GRANT SELECT ON mydb.articles TO 'fess_user'@'localhost';

Exemples d'utilisation
=======================

Recherche de catalogue de produits
------------------------------------

Paramètres :

::

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://localhost:3306/shop
    username=fess_user
    password=password
    sql=SELECT p.id, p.name, p.description, p.price, c.name as category, p.updated_at FROM products p JOIN categories c ON p.category_id = c.id WHERE p.active = 1

Script :

::

    url="https://shop.example.com/product/" + id
    title=name
    content=description + " Catégorie: " + category + " Prix: " + price + " EUR"
    lastModified=updated_at

Articles de base de connaissances
-----------------------------------

Paramètres :

::

    driver=org.postgresql.Driver
    url=jdbc:postgresql://localhost:5432/knowledge
    username=fess_user
    password=password
    sql=SELECT id, title, body, tags, author, created_at, updated_at FROM articles WHERE published = true ORDER BY id

Script :

::

    url="https://kb.example.com/article/" + id
    title=title
    content=body
    digest=tags
    author=author
    created=created_at
    lastModified=updated_at

Dépannage
=========

Pilote JDBC introuvable
-----------------------

**Symptôme** : ``ClassNotFoundException`` ou ``No suitable driver``

**Solution** :

1. Vérifiez que le pilote JDBC est placé dans ``lib/``
2. Vérifiez que le nom de classe du pilote est correct
3. Redémarrez |Fess|

Erreur de connexion
--------------------

**Symptôme** : ``Connection refused`` ou erreur d'authentification

**Points à vérifier** :

1. La base de données est-elle démarrée ?
2. Le nom d'hôte et le numéro de port sont-ils corrects ?
3. Le nom d'utilisateur et le mot de passe sont-ils corrects ?
4. Configuration du pare-feu

Erreur de requête
-----------------

**Symptôme** : ``SQLException`` ou erreur de syntaxe SQL

**Points à vérifier** :

1. Testez la requête SQL directement sur la base de données
2. Vérifiez que les noms de colonnes sont corrects
3. Vérifiez que les noms de tables sont corrects

Informations de référence
==========================

- :doc:`ds-overview` - Aperçu des connecteurs DataStore
- :doc:`ds-csv` - Connecteur CSV
- :doc:`ds-json` - Connecteur JSON
- :doc:`../../admin/dataconfig-guide` - Guide de configuration DataStore
- :doc:`../crawler-basic` - Configuration de base du robot d'indexation
- :doc:`../search-basic` - Fonction de recherche
