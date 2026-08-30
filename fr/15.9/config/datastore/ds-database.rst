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

Méthode 1 : Installer depuis l'interface d'administration

1. Ouvrir « Système » → « Plugins »
2. Téléverser le fichier JAR
3. Redémarrer |Fess|

Méthode 2 : Déposer le fichier JAR directement

::

    # Téléchargement depuis le dépôt CodeLibs
    wget https://maven.codelibs.org/release/org/codelibs/fess/fess-ds-db/X.X.X/fess-ds-db-X.X.X.jar

    # Déploiement (le même répertoire que celui utilisé par l'interface d'administration)
    cp fess-ds-db-X.X.X.jar $FESS_HOME/app/WEB-INF/plugin/
    # ou
    cp fess-ds-db-X.X.X.jar /usr/share/fess/app/WEB-INF/plugin/

Installation du pilote JDBC
----------------------------

Le pilote JDBC n'est pas fourni avec le plugin. Procurez-vous séparément le pilote adapté à votre base de données et déposez-le vous-même.

Le crawl de DataStore s'exécute dans le processus du crawler ; le pilote doit donc se trouver dans le **classpath du processus du crawler**. L'un ou l'autre de ces répertoires convient :

- ``app/WEB-INF/lib/``
- ``app/WEB-INF/env/crawler/lib/``

::

    # Exemple : pilote MySQL
    cp mysql-connector-j-9.x.x.jar $FESS_HOME/app/WEB-INF/lib/
    # ou
    cp mysql-connector-j-9.x.x.jar /usr/share/fess/app/WEB-INF/lib/

Une fois le pilote JDBC déposé, redémarrez |Fess| pour le charger.

.. note::
   Lorsque le pilote est absent, le crawl échoue avec le message
   ``The JDBC driver ... is not on the crawler classpath.``

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
     - Taille de fetch JDBC. ``MIN_VALUE`` demande à MySQL de lire le jeu de résultats ligne par ligne ; les autres pilotes rejettent une valeur négative, et le crawl se poursuit avec la valeur par défaut du pilote après un avertissement. Une valeur négative ou non numérique est signalée puis ignorée
   * - ``query_timeout``
     - Non
     - Délai d'expiration de la requête, en secondes. ``0`` signifie aucune limite (valeur par défaut de JDBC). Si le paramètre est absent, aucun délai n'est défini
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

.. note::
   Si une requête reste bloquée, arrêter le job ne libère pas le thread du crawler.
   La demande d'arrêt n'est vérifiée qu'entre deux lignes : elle ne peut donc pas interrompre
   un appel bloqué à l'intérieur du pilote. Définissez ``query_timeout`` pour les requêtes
   susceptibles d'être longues.

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
- ``crawlingConfig`` - la configuration du DataStore
- ``crawlingContext`` - le contexte du crawl ; ``crawlingContext.doc`` contient le document en cours de construction

.. note::
   Le nom de colonne doit correspondre au libellé de colonne (alias) de la clause ``SELECT``.
   Pour les fonctions d'agrégation ou les expressions, utilisez explicitement ``AS`` pour définir un alias
   (ex. : ``COUNT(*) AS total``).

.. note::
   La casse des libellés de colonne varie selon la base de données. PostgreSQL convertit les
   identifiants non entourés de guillemets en minuscules, H2 les convertit en majuscules et
   MySQL les renvoie tels qu'ils ont été déclarés. Un nom qui ne peut pas être résolu laisse
   le champ non renseigné au lieu de provoquer une erreur : définissez donc explicitement un
   alias avec ``AS`` lorsque la portabilité est importante.

.. warning::
   Les scripts peuvent référencer **l'ensemble des paramètres du DataStore**, et pas seulement
   les colonnes du résultat SQL. ``driver``, ``url``, ``username``, ``password`` et ``sql``
   sont tous visibles sous forme de variables portant le même nom : une colonne peut donc être
   masquée involontairement, ou la valeur d'un paramètre peut apparaître là où une colonne
   absente était attendue. Lorsque les deux existent, la valeur de la colonne l'emporte.

Chargement de données BLOB/binaires
=====================================

Les colonnes binaires (BLOB, ``BYTEA``, tableau d'octets, flux binaire) sont soumises au
traitement d'extraction de contenu - le même extracteur que pour le crawl de fichiers - et
intégrées sous forme de texte.

Les CLOB, NCLOB et flux de caractères ne passent **pas** par un extracteur. Ils sont lus tels
quels sous forme de texte, et les indications de type MIME décrites ci-dessous ne s'appliquent
pas à eux.

Les colonnes de type tableau deviennent leurs éléments joints par des espaces. Les valeurs NULL
deviennent des chaînes vides.

.. note::
   Le fait qu'une colonne BLOB arrive sous forme de ``java.sql.Blob`` ou de tableau d'octets
   dépend du pilote JDBC - MySQL et PostgreSQL renvoient un tableau d'octets. Les deux sont
   extraits de la même manière.

.. note::
   Les CLOB et NCLOB sont lus intégralement en mémoire, sans limite de taille. Pour des colonnes
   de texte très volumineuses, envisagez de les tronquer en SQL avec ``SUBSTRING`` ou équivalent.
   Le chemin passant par l'extracteur respecte, lui, la taille maximale de contenu du crawler.

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

.. warning::
   Restreindre la requête de cette manière ne transforme pas le crawl en crawl
   incrémental. À la fin d'un crawl, |Fess| supprime les documents de cette
   configuration du DataStore qui ne faisaient pas partie du crawl qui vient de
   s'exécuter : une requête filtrée ne laisse donc dans l'index que les lignes
   correspondantes.

   Ajoutez ``delete_old_docs=false`` aux paramètres du DataStore pour conserver les
   documents indexés par les crawls précédents. Les lignes supprimées de la base de
   données ne sont alors plus retirées de l'index non plus : exécutez donc
   périodiquement un crawl complet.

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

.. warning::
   ``url=url`` ne fait ce à quoi on s'attend que si le résultat du ``SELECT`` comporte une
   colonne portant le libellé ``url``. En l'absence d'une telle colonne, c'est le paramètre du
   DataStore de même nom - autrement dit l'**URL de connexion JDBC** - qui devient l'URL du
   document. Définissez un alias pour la colonne, comme dans ``SELECT page_url AS url``, ou
   indiquez-la dans le script, comme dans ``url=page_url``.

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

1. S'appuyer sur le chiffrement automatique

   La valeur d'un paramètre dont le nom correspond à ``app.encrypt.property.pattern``
   (par défaut ``.*password|.*key|.*token|.*secret``) est chiffrée lors de l'enregistrement
   depuis l'interface d'administration et stockée avec le préfixe ``{cipher}``. ``password``
   correspond à ce motif : il n'est donc pas stocké en clair lorsqu'il est défini depuis
   l'interface d'administration.

2. Utiliser des variables d'environnement

   Une variable d'environnement dont le nom commence par ``FESS_ENV_`` est développée à
   l'intérieur d'un paramètre du DataStore sous la forme ``${nom de la variable}`` :

   ::

       password=${FESS_ENV_DB_PASSWORD}

   Les noms développés sont déterminés par ``crawler.data.env.param.key.pattern``
   (par défaut ``^FESS_ENV_.*``).

3. Utiliser un utilisateur en lecture seule

.. note::
   Passer ``org.codelibs.fess.ds`` en DEBUG n'expose pas les identifiants : les valeurs des
   paramètres correspondant à ``app.encrypt.property.pattern``, ainsi que les identifiants
   intégrés dans l'URL JDBC, sont masqués dans le journal.

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

Lorsqu'un crawl échoue, le message du journal indique quelle étape a échoué.

Pilote JDBC introuvable
-----------------------

**Symptôme** : ``The JDBC driver ... is not on the crawler classpath.``

**Solution** :

1. Vérifiez que le pilote JDBC est placé dans ``app/WEB-INF/lib/`` ou ``app/WEB-INF/env/crawler/lib/``
2. Vérifiez que le nom de classe indiqué dans ``driver`` est correct
3. Redémarrez |Fess|

Erreur de connexion
--------------------

**Symptôme** : ``Failed to connect to <URL>.``

**Points à vérifier** :

1. La base de données est-elle démarrée ?
2. Le nom d'hôte et le numéro de port sont-ils corrects ?
3. Le nom d'utilisateur et le mot de passe sont-ils corrects ?
4. Configuration du pare-feu

Erreur de requête
-----------------

**Symptôme** : ``Failed to execute the query.``

**Points à vérifier** :

1. Testez la requête SQL directement sur la base de données
2. Vérifiez que les noms de colonnes sont corrects
3. Vérifiez que les noms de tables sont corrects

Paramètres manquants
--------------------

**Symptôme** : ``The driver parameter is required.``, ``The url parameter is required.`` ou ``The sql parameter is required.``

Un paramètre obligatoire n'est pas défini. Vérifiez le champ des paramètres.

Seules certaines lignes échouent
--------------------------------

Une ligne en échec n'interrompt pas le crawl : elle est enregistrée sous « Système » →
« URL en échec ». L'URL du document est utilisée lorsque les scripts en ont produit une, et
``datastore://<id de la configuration DataStore>/<numéro de ligne>`` dans le cas contraire.

Les documents n'apparaissent pas dans les résultats de recherche
----------------------------------------------------------------

1. Vérifiez que les scripts définissent ``url``, ``title`` et ``content``
2. Vérifiez que la casse des libellés de colonne correspond à celle utilisée par les scripts (voir « Configuration du script »)
3. Vérifiez le nombre de documents dans le journal du job de crawl

Informations de référence
==========================

- :doc:`ds-overview` - Aperçu des connecteurs DataStore
- :doc:`ds-csv` - Connecteur CSV
- :doc:`ds-json` - Connecteur JSON
- :doc:`../../admin/dataconfig-guide` - Guide de configuration DataStore
- :doc:`../crawler-basic` - Configuration de base du robot d'indexation
- :doc:`../search-basic` - Fonction de recherche
