===================================================
Rechercher dans bases de données, CSV et Salesforce
===================================================

Introduction
============

Le référentiel produits se trouve dans une base de données interne, la liste des clients dans un fichier CSV que le système de gestion exporte chaque nuit, et l'historique des opportunités et des demandes dans Salesforce.
Ce type de données métier n'est souvent consultable que depuis les écrans de chaque système.
Avec les plugins de magasin de données de Fess, vous pouvez importer ces données enregistrement par enregistrement et les retrouver depuis la même page de recherche que les documents des serveurs de fichiers et des sites internes.

Cet article explique comment configurer l'import de chacune des trois sources, puis comment filtrer par source, planifier les exécutions et vérifier les résultats.
Les étapes communes à tous les magasins de données, comme l'installation des plugins, l'écriture du nom du gestionnaire, des paramètres et du script, ou la création des tâches, sont regroupées dans :doc:`datastore-basics`.
Lisez d'abord cet article avant de continuer.
Les valeurs de configuration de cet article correspondent à Fess 15.9 et à la version 15.9.0 de chaque plugin.

L'architecture mise en place dans cet article
=============================================

.. list-table::
   :header-rows: 1
   :widths: 18 22 22 38

   * - Source
     - Plugin
     - Nom du gestionnaire
     - À préparer au préalable
   * - Base de données (référentiel produits)
     - ``fess-ds-db``
     - ``DatabaseDataStore``
     - Le fichier jar du pilote JDBC et un utilisateur de base de données limité à SELECT
   * - CSV (liste des clients)
     - ``fess-ds-csv``
     - ``CsvDataStore``
     - Un répertoire où les fichiers CSV sont exportés (un emplacement lisible par le robot d'exploration)
   * - Salesforce (comptes, opportunités, requêtes)
     - ``fess-ds-salesforce``
     - ``SalesforceDataStore``
     - Une application connectée et une paire de clés pour signer le JWT

Si vous utilisez Fess avec Docker, indiquez les trois plugins, séparés par des espaces, dans ``environment`` de ``fess01`` dans ``compose.yaml``.

.. code-block:: yaml

    environment:
      - "FESS_PLUGINS=fess-ds-db:15.9.0 fess-ds-csv:15.9.0 fess-ds-salesforce:15.9.0"

Si vous les installez depuis l'interface d'administration ou avec ``fess-setup``, vous devez redémarrer Fess.

À décider d'abord : qui peut voir les résultats
===============================================

Aucun des trois plugins ne transfère vers Fess les droits d'accès (ACL) du système d'origine.
Les rôles des documents importés sont déterminés uniquement par la valeur du champ « Autorisations » de la configuration du magasin de données.
Ce champ contient ``{role}guest`` dès le départ ; en l'état, même les utilisateurs non connectés peuvent donc effectuer des recherches.

Pour des données contenant des prix ou des informations clients, remplacez cette valeur par les groupes qui doivent les voir (par exemple ``{group}sales``).
Tous les documents enregistrés à partir d'une même configuration reçoivent les mêmes autorisations.
Répartissez les données destinées à des publics différents dans des configurations de magasin de données distinctes.
Pour la conception des groupes, voir :doc:`guide-05`.

Base de données : importer le référentiel produits
==================================================

Placer le pilote JDBC
---------------------

``fess-ds-db`` ne contient aucun pilote JDBC.
Procurez-vous le fichier jar du pilote adapté à votre base de données (``postgresql-<version>.jar`` pour PostgreSQL, ``mysql-connector-j-<version>.jar`` pour MySQL) et placez-le dans le classpath du robot d'exploration.
L'exploration des magasins de données s'exécute dans un processus de robot distinct de Fess lui-même, et son classpath inclut les fichiers jar des deux répertoires suivants.

- ``app/WEB-INF/lib/``
- ``app/WEB-INF/env/crawler/lib/``

Avec le paquet ZIP, ils se trouvent sous le répertoire où Fess a été décompressé ; avec RPM / DEB, sous ``/usr/share/fess/``.
Après avoir placé le fichier, redémarrez Fess.

Dans l'image Docker aussi, Fess se trouve dans ``/usr/share/fess/``.
Un fichier jar copié dans le conteneur disparaît lorsque le conteneur est recréé ; montez donc uniquement ce fichier jar dans ``fess01`` de ``compose.yaml``.

.. code-block:: yaml

    volumes:
      - ./postgresql-42.7.4.jar:/usr/share/fess/app/WEB-INF/env/crawler/lib/postgresql.jar:ro

Si vous montez le répertoire entier, les fichiers jar que l'image y place deviennent invisibles et le robot d'exploration ne peut plus démarrer.
Montez toujours des fichiers individuels.
Après la modification, recréez les conteneurs avec ``docker compose -f compose.yaml -f compose-opensearch3.yaml up -d``.

Paramètres et SQL
-----------------

Nous prenons ici comme exemple la table PostgreSQL ``products``.
Comme destination des liens des résultats de recherche, nous utilisons l'écran de consultation du référentiel produits (par exemple ``https://erp.example.com/products/<ID produit>``).
Dans [Robot d'exploration] > [Magasin de données] > [Créer nouveau], choisissez ``DatabaseDataStore`` comme nom du gestionnaire et définissez les paramètres comme suit.

.. code-block:: properties

    script_type=javascript
    driver=org.postgresql.Driver
    url=jdbc:postgresql://db.example.com:5432/erp
    username=fess_reader
    password=your-password
    query_timeout=600
    sql=SELECT p.product_id, concat('https://erp.example.com/products/', p.product_id) AS page_url, p.product_name AS title, concat_ws(' ', p.product_name, p.model_number, c.category_name, p.description) AS body, p.updated_at FROM products p JOIN categories c ON c.category_id = p.category_id WHERE p.discontinued = false

Le script est le suivant.

.. code-block:: properties

    url=page_url
    title=title
    content=body
    last_modified=updated_at
    label="products"

Écrivez ``sql`` sur une seule ligne.
Le SQL est envoyé tel quel à la base de données, et chaque ligne du résultat devient un document.
Si vous construisez l'URL de destination et le corps du texte dans le SQL, le script n'a plus qu'à indiquer des noms de colonnes.
``concat_ws`` ignore les colonnes NULL lors de la concaténation ; le corps ne devient donc pas NULL, même pour un produit sans description.
Dans MySQL, ``CONCAT_WS`` se comporte de la même façon, mais ``CONCAT`` renvoie NULL pour tout le résultat dès qu'un argument est NULL.

Si vous utilisez Fess avec Docker, ``localhost`` dans ``url`` désigne le conteneur Fess lui-même, et non le serveur de base de données.
Indiquez le nom d'hôte ou l'adresse IP de la base de données.

Correspondance entre noms de colonnes et script
-----------------------------------------------

Dans la partie droite du script, indiquez tels quels les libellés de colonnes du résultat du SELECT (les alias définis avec ``AS``).
Tenez compte des trois points suivants.

- La casse des libellés de colonnes dépend de la base de données. Les alias sans guillemets sont convertis en minuscules par PostgreSQL et en majuscules par Oracle et H2, tandis que MySQL les renvoie tels qu'ils ont été écrits. Dans le script, respectez exactement la casse renvoyée par la base de données. En cas de différence, le champ ne reçoit aucune valeur
- Les valeurs du champ des paramètres sont aussi visibles dans le script sous forme de variables portant le même nom. Si vous écrivez ``url=url`` alors que le résultat ne comporte pas de colonne ``url``, l'URL de connexion JDBC devient l'URL du document. Donnez à la colonne de destination des liens un nom qui n'entre pas en conflit avec un paramètre, par exemple ``page_url``
- Une requête bloquée ne s'arrête pas lorsque vous arrêtez la tâche. Définissez toujours ``query_timeout`` (en secondes)

``fess-ds-db`` n'offre aucune option d'exploration incrémentale.
Chaque exécution lance l'intégralité de ``sql`` et réenregistre toutes les lignes.
Pour les tables volumineuses, exécutez la tâche à un moment où la charge de la base de données est faible (voir « Créer une tâche par source » plus bas).

CSV : importer la liste des clients exportée par le système de gestion
======================================================================

L'utilisation de base du connecteur CSV est expliquée dans la section d'exemple sur les fichiers CSV de :doc:`datastore-basics`.
Nous ne complétons ici que les points nécessaires pour importer des fichiers CSV exportés régulièrement par le système de gestion.

Supposons, à titre d'exemple, qu'un système de gestion japonais exporte chaque nuit à 2 h 00 un fichier ``customers_20261128.csv`` comme celui-ci.
Son encodage est MS932 (la variante Windows de Shift_JIS), et la première ligne contient des en-têtes en japonais (code client, nom du client, adresse, service responsable, statut commercial).

.. code-block:: text

    取引先コード,取引先名,所在地,担当部署,取引状況
    C0001,株式会社サンプル商事,東京都千代田区,第一営業部,取引中
    C0002,サンプル工業株式会社,大阪府大阪市,第二営業部,取引終了

Emplacement des fichiers
------------------------

Exportez les fichiers CSV vers un chemin lisible depuis le serveur où s'exécute le robot d'exploration de Fess.
Avec Docker, montez le répertoire d'export dans ``fess01`` en lecture seule.

.. code-block:: yaml

    volumes:
      - ./export/customers:/data/customers:ro

Paramètres et script
--------------------

.. code-block:: properties

    script_type=javascript
    directories=/data/customers
    file_encoding=MS932
    has_header_line=true

.. code-block:: javascript

    url=cell5 == "取引中" ? "https://crm.example.com/customers/" + cell1 : null
    title=cell2
    content=cell2 + " " + cell3 + " " + cell4
    label="customers"

- Si vous indiquez ``directories``, tous les fichiers d'extension ``.csv`` / ``.tsv`` de ce répertoire sont lus, du plus ancien au plus récent selon la date de modification. Lorsqu'un fichier dont le nom contient la date est exporté chaque jour, vous n'avez pas à modifier les paramètres. Si vous laissez les anciens fichiers en place, leurs lignes sont aussi lues à chaque fois
- Les fichiers CSV exportés par l'Excel japonais ou par des systèmes destinés au Windows japonais sont le plus souvent en MS932. Si vous indiquez ``Shift_JIS``, des caractères comme ``①`` ou ``㈱`` deviennent des caractères de remplacement ; indiquez donc ``MS932``
- Même si les en-têtes contiennent des caractères non ASCII, comme ici en japonais, ``has_header_line=true`` permet d'ignorer la première ligne. Dans le script, le plus sûr est de référencer les colonnes par leur numéro (``cell1``, ``cell2`` …). Les colonnes dont l'en-tête contient des espaces ou des symboles ne peuvent pas être référencées par le nom de l'en-tête
- Pour les fichiers séparés par des tabulations, ajoutez ``separator_character=\t``
- Les lignes pour lesquelles ``url`` vaut ``null`` ne sont pas enregistrées. Dans cet exemple, les clients au statut 取引終了 (relation terminée) sont exclus ; seuls ceux au statut 取引中 (actif) sont enregistrés. Le nombre de lignes exclues apparaît dans ``fess-crawler.log`` sous la forme d'un WARN : ``Skipped 1 row(s) in ... because the script did not set the url field.``

Si un fichier est lu pendant son export, seules les lignes déjà écrites sont enregistrées.
Exécutez la tâche après l'heure à laquelle l'export du CSV se termine.

Salesforce : importer les comptes, opportunités et requêtes
===========================================================

Préparation côté Salesforce
---------------------------

``fess-ds-salesforce`` prend en charge deux méthodes d'authentification : ``auth_type=oauth_token`` (flux JWT bearer) et ``auth_type=oauth_password`` (nom d'utilisateur et mot de passe).
Nous utilisons ici ``oauth_token``, qui évite de stocker un mot de passe.
Le flux OAuth par nom d'utilisateur et mot de passe utilisé par ``oauth_password`` peut être désactivé selon les paramètres de l'organisation Salesforce.

1. Créez une paire de clés et un certificat

   .. code-block:: bash

       openssl genrsa -out private_key.pem 2048
       openssl req -new -x509 -key private_key.pem -out certificate.crt -days 365

2. Dans Salesforce Setup, créez une application connectée, activez les paramètres OAuth et téléversez ``certificate.crt`` sous « Utiliser les signatures numériques ». Choisissez les scopes OAuth comme indiqué dans la référence
3. Dans les stratégies de l'application connectée, réglez « Utilisateurs autorisés » sur « Les utilisateurs approuvés par l'administrateur sont préautorisés », puis attribuez le profil ou l'ensemble d'autorisations de l'utilisateur servant à l'exploration
4. Notez la Consumer Key de l'application connectée

Les écrans et les libellés de Salesforce peuvent changer ; pour plus de détails, consultez aussi la description du flux JWT bearer dans l'aide de Salesforce.

Fess ne peut importer que les enregistrements et les champs que l'utilisateur servant à l'exploration peut lire.
Si vous indiquez dans ``contents`` (décrit plus bas) un champ que cet utilisateur ne peut pas lire, la récupération de l'objet concerné échoue.

Paramètres et script
--------------------

Pour ``private_key``, écrivez le contenu de ``private_key.pem`` sur une seule ligne en remplaçant les sauts de ligne par ``\n``.
Le plugin ne sait lire que le format PKCS#8 (le format qui commence par ``-----BEGIN PRIVATE KEY-----``).
Une clé commençant par ``-----BEGIN RSA PRIVATE KEY-----``, créée avec une ancienne version d'OpenSSL, doit d'abord être convertie avec ``openssl pkcs8 -topk8 -nocrypt -in private_key.pem -out private_key_pkcs8.pem``.

.. code-block:: properties

    script_type=javascript
    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=fess-crawler@example.com
    client_id=3MVG9...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBg...\n-----END PRIVATE KEY-----\n
    include_pattern=.*/(001|006|500)[A-Za-z0-9]+
    OPPORTUNITY.contents=Name,StageName,NextStep,Description

.. code-block:: javascript

    url=object.url
    title="[" + object.type + "] " + object.title
    content=object.content
    digest=object.description
    created=object.created
    last_modified=object.last_modified
    label="salesforce"

Pour cibler une sandbox, indiquez ``base_url=https://test.salesforce.com``.

Tous les éléments de la partie droite commencent par ``object.``.
Si vous les écrivez sans ce préfixe, comme ``url=url``, l'évaluation de l'expression échoue : l'enregistrement n'est pas indexé, mais consigné comme URL d'échec.
``object.url`` a la forme ``<URL de l'instance>/<ID de l'enregistrement>`` ; un clic ouvre la page de l'enregistrement dans Salesforce.

Limiter le périmètre de l'import
--------------------------------

``fess-ds-salesforce`` lit toujours la totalité des 23 types d'objets standard, dont Account, Contact, Lead, Opportunity, Case, Task et User.
Aucun paramètre ne permet de choisir les objets à lire.
Pour limiter le périmètre, combinez les trois moyens suivants.

- ``include_pattern`` / ``exclude_pattern`` : expressions régulières devant correspondre à l'intégralité de ``object.url``, qui sélectionnent les enregistrements à indexer. Les trois premiers caractères d'un ID d'enregistrement Salesforce sont fixés pour chaque objet (Account ``001``, Opportunity ``006``, Case ``500``, etc.). L'exemple ci-dessus n'enregistre que ces trois types. La récupération porte malgré tout sur tous les objets ; les autres enregistrements sont simplement écartés avant l'indexation
- ``<nom de l'objet>.title`` / ``<nom de l'objet>.contents`` : indiquent, par leur nom d'API, les champs utilisés pour le titre et le corps. Les noms des objets standard sont en majuscules avec des traits de soulignement, comme ``ACCOUNT``, ``OPPORTUNITY`` ou ``CASE``. Sans indication, les champs par défaut du plugin sont utilisés
- ``custom`` : indiquez les noms d'API des objets personnalisés, séparés par des virgules, pour les lire en plus des objets standard

Les objets personnalisés n'ont pas de champs par défaut ; indiquez donc toujours ``.title`` et ``.contents``.
Incluez aussi le champ du titre dans les champs du corps.
Le plugin ne récupère que les champs indiqués dans ``.contents`` et assimilés : un champ indiqué uniquement dans ``.title`` n'est pas récupéré, et le titre reste vide.

.. code-block:: properties

    custom=Project__c
    Project__c.title=Name
    Project__c.contents=Name,Customer_Name__c,Summary__c

Filtrer par source avec les étiquettes
======================================

Dans les exemples précédents, le ``label`` du script attribue ``products``, ``customers`` et ``salesforce``.
Pour les afficher parmi les choix d'étiquettes de la page de recherche, créez dans [Robot d'exploration] > [Étiquette] des étiquettes ayant la même « Valeur » (« Chemins inclus » peut rester vide).
Les valeurs d'étiquette ne peuvent contenir que des caractères alphanumériques et ``_``.

Pour séparer les données Salesforce par objet, créez, au lieu d'utiliser le ``label`` du script, des étiquettes dont les « Chemins inclus » examinent les trois premiers caractères de l'ID d'enregistrement.
Par exemple, une étiquette de valeur ``sf_case`` avec le chemin inclus ``https://example\.my\.salesforce\.com/500.*`` n'est attribuée qu'aux requêtes (Case).
Si une étiquette correspond à l'URL, l'étiquette attribuée par le script est perdue.
Dans une même configuration de magasin de données, n'utilisez qu'une seule des deux méthodes (pour plus de détails, voir la section sur les étiquettes dans :doc:`datastore-basics`).

Créer une tâche par source
==========================

Dans l'état initial, « Default Crawler » explore toutes les configurations ensemble chaque jour à 0 h 00.
Chaque source a son horaire le plus pratique ; créez donc une tâche par configuration de magasin de données.
Sur l'écran de détails de chaque configuration, cliquez sur [Créer une nouvelle tâche] et saisissez l'heure au format cron dans « Planification » (pour la procédure, voir la section sur la planification dans :doc:`datastore-basics`).

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Source
     - Exemple de planification
     - Points à considérer
   * - Base de données
     - ``0 3 * * *``
     - Toutes les lignes sont lues à chaque fois : choisir un moment où la charge de la base de données est faible
   * - CSV
     - ``30 2 * * *``
     - Planifier après l'heure de fin de l'export
   * - Salesforce
     - ``0 7,12,18 * * *``
     - Chaque exécution crée autant de tâches Bulk API qu'il y a d'objets standard et personnalisés. Fixer la fréquence selon le quota d'API restant de l'organisation

Default Crawler continue lui aussi d'explorer ces configurations.
Si vous ne voulez pas d'exécution en double, réglez le « Statut » de la configuration du magasin de données sur « Désactivé » (une tâche qui indique un ID de configuration explore cette configuration même si elle est désactivée).

Lignes disparues des données d'origine
======================================

Même si vous supprimez une ligne de la base de données ou si une ligne disparaît du CSV, le document correspondant n'est pas supprimé lors de l'exploration suivante.
Les documents enregistrés par un magasin de données reçoivent une date d'expiration, prolongée à chaque enregistrement.
Un document qui n'est plus enregistré est supprimé automatiquement une fois écoulé, depuis son dernier enregistrement, le nombre de jours indiqué dans « Supprimer les anciens documents » de [Système] > [Général] (3 jours par défaut).

Ce mécanisme comporte aussi un aspect qui demande de la vigilance.
Si la base de données reste inaccessible plusieurs jours d'affilée au-delà de ce nombre de jours, tous les documents de cette configuration disparaissent des résultats de recherche.
Détectez rapidement les échecs d'import grâce aux méthodes de la section suivante.

Vérifier le fonctionnement
==========================

La lecture du journal des tâches, de [Informations système] > [Informations sur l'exploration], des URL d'échec et de ``fess-crawler.log`` est expliquée dans la section sur la vérification des résultats de :doc:`datastore-basics`.
Avec l'exploration des magasins de données, la tâche peut afficher « OK » même si l'import a échoué ; jugez donc d'après le nombre de documents et les journaux.

1. Dans [Informations système] > [Rechercher], recherchez ``label:products``, ``label:customers`` et ``label:salesforce``, puis comparez le nombre de résultats avec les données d'origine (pour une base de données, un ``SELECT count(*)`` avec les mêmes conditions que ``sql``)
2. Vérifiez les entrées WARN et ERROR de ``fess-crawler.log``. Avec l'architecture de cet article, les messages suivants sont les plus fréquents

   - ``The JDBC driver ... is not on the crawler classpath.`` : l'emplacement du pilote ou le nom de classe dans ``driver`` est incorrect
   - ``Failed to connect to ...`` : vérifiez le nom d'hôte, le port, le nom d'utilisateur et le mot de passe de la base de données
   - ``is not a directory.`` ou ``No CSV file.`` : aucun fichier CSV lisible par le robot d'exploration ne se trouve dans le chemin de ``directories``
   - ``Batch:... Failed caused by ...`` : certains objets Salesforce n'ont pas pu être récupérés. Vérifiez les noms de champs dans ``.contents`` et les autorisations sur les champs de l'utilisateur servant à l'exploration
   - ``Failed to process a data crawling: <nom de la configuration>`` : la configuration entière a échoué. Pour Salesforce, c'est le cas des échecs d'authentification. Vérifiez la cause dans la trace de pile qui suit

3. Pour les configurations dont vous avez modifié le champ « Autorisations », connectez-vous avec un utilisateur du groupe cible et vérifiez que les documents apparaissent dans les résultats de recherche, puis qu'ils n'apparaissent pas une fois déconnecté

Résumé
======

- Aucun des trois plugins ne reprend les droits du système d'origine ; remplacez donc ``{role}guest`` dans le champ « Autorisations » par les groupes qui doivent voir les données
- Pour une base de données, placez le pilote JDBC dans le classpath du robot d'exploration et construisez l'URL de destination et le corps dans le SQL. Toutes les lignes sont lues à chaque fois
- Lisez les CSV du système de gestion avec ``directories`` et ``file_encoding=MS932``, et référencez les colonnes avec ``cellN``. Les lignes dont ``url`` vaut ``null`` ne sont pas enregistrées
- Écrivez le script Salesforce avec ``object.*``. Les objets standard ne peuvent pas être choisis ; limitez donc le périmètre avec ``include_pattern`` et ``<nom de l'objet>.contents``
- Créez une tâche par source, et exploitez le système en partant du principe que les lignes supprimées des données d'origine disparaissent après le nombre de jours de « Supprimer les anciens documents »

Articles à lire ensuite
=======================

- Les mécanismes communs des magasins de données (scripts, autorisations, étiquettes, vérification des résultats) : :doc:`datastore-basics`
- Importer Git, Confluence, Jira et Slack : :doc:`guide-06`
- Importer Google Drive, SharePoint et Box : :doc:`guide-07`
- Afficher des résultats de recherche différents selon le service : :doc:`guide-05`
- Surveiller les échecs d'import : :doc:`guide-10`

Références
==========

- `Connecteur de base de données <https://fess.codelibs.org/fr/stable/config/datastore/ds-database.html>`__
- `Connecteur CSV <https://fess.codelibs.org/fr/stable/config/datastore/ds-csv.html>`__
- `Connecteur Salesforce <https://fess.codelibs.org/fr/stable/config/datastore/ds-salesforce.html>`__
- `Configuration du magasin de données <https://fess.codelibs.org/fr/stable/admin/dataconfig-guide.html>`__
- `Planificateur <https://fess.codelibs.org/fr/stable/admin/scheduler-guide.html>`__
- `Étiquette <https://fess.codelibs.org/fr/stable/admin/labeltype-guide.html>`__
- `Général <https://fess.codelibs.org/fr/stable/admin/general-guide.html>`__
