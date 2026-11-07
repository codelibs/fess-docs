=================================================
Partie 12 : Rendre les données SaaS recherchables
=================================================

Introduction
=============

Les données importantes d'une entreprise ne sont pas uniquement stockées sur des serveurs de fichiers et dans le stockage cloud, mais également dans des applications SaaS et des bases de données.
Les informations clients dans Salesforce, les données de référence produit dans les bases de données internes, les données de listes gérées dans des fichiers CSV -- ces données ne sont généralement recherchables que dans leurs systèmes respectifs.

Cet article traite des scénarios d'importation des données SaaS et de bases de données dans l'index Fess, permettant une recherche transversale avec les autres documents.

Public cible
=============

- Ceux qui souhaitent inclure les informations SaaS et de bases de données dans les résultats de recherche
- Ceux qui souhaitent apprendre à utiliser les plugins de data store
- Ceux qui souhaitent construire une plateforme de recherche couvrant plusieurs sources de données

Scénario
========

Une organisation commerciale a ses données réparties dans les systèmes suivants.

.. list-table:: Situation des sources de données
   :header-rows: 1
   :widths: 20 35 45

   * - Système
     - Données stockées
     - Défi actuel
   * - Salesforce
     - Informations clients, enregistrements d'affaires, historique d'activités
     - Recherche possible uniquement dans Salesforce
   * - BD interne
     - Référentiel produits, grilles tarifaires, informations de stock
     - Accessible uniquement via une interface d'administration dédiée
   * - Fichiers CSV
     - Listes de clients, listes de participants aux événements
     - Recherche uniquement possible en ouvrant dans Excel et en parcourant visuellement
   * - Serveur de fichiers
     - Propositions, devis, contrats
     - Déjà explorés par Fess

L'objectif est de permettre la recherche transversale de toutes ces données avec Fess, afin que les informations nécessaires aux activités commerciales puissent être trouvées depuis un seul champ de recherche.

Intégration des données Salesforce
====================================

Pour rendre les données Salesforce recherchables dans Fess, utilisez le plugin de data store Salesforce.

Installation du plugin
-----------------------

1. Accédez à [Système] > [Plugins] dans le panneau d'administration
2. Installez ``fess-ds-salesforce``

Paramètres de connexion
------------------------

L'intégration avec Salesforce nécessite la configuration d'une Connected App.

**Préparation côté Salesforce**

1. Créez une Connected App dans les paramètres Salesforce
2. Activez les paramètres OAuth
3. Obtenez la clé et le secret du consommateur

**Configuration côté Fess**

1. Accédez à [Crawler] > [Data Store] > [Créer nouveau]
2. Nom du handler : Sélectionnez SalesforceDataStore
3. Configurez les paramètres et les scripts
4. Label : Définissez ``salesforce``

**Exemple de configuration des paramètres**

.. code-block:: properties

    base_url=https://login.salesforce.com
    auth_type=oauth_password
    username=user@example.com
    password=your-password
    security_token=your-security-token
    client_id=your-consumer-key
    client_secret=your-consumer-secret

**Exemple de configuration du script**

.. code-block:: properties

    url=url
    title=title
    content=content
    last_modified=last_modified

Pour ``auth_type``, spécifiez ``oauth_password`` (authentification par nom d'utilisateur/mot de passe) ou ``oauth_token`` (authentification par jeton JWT Bearer). Lors de l'utilisation de l'authentification JWT, définissez la clé privée RSA dans ``private_key``.

Sélection des données cibles
------------------------------

Salesforce contient de nombreux objets, mais il n'est pas nécessaire de tous les rendre recherchables.
Concentrez-vous sur les objets que l'équipe commerciale recherche fréquemment.

.. list-table:: Exemple d'objets cibles
   :header-rows: 1
   :widths: 25 35 40

   * - Objet
     - Champs recherchables
     - Utilisation
   * - Account
     - Nom, secteur d'activité, adresse, description
     - Rechercher les informations de base des comptes
   * - Opportunity
     - Nom, étape, description, montant
     - Rechercher les affaires en cours
   * - Case
     - Objet, description, statut
     - Rechercher l'historique des demandes

Intégration des bases de données
=================================

Pour rendre les données de bases de données internes recherchables, utilisez le plugin de data store de base de données.

Installation du plugin
-----------------------

Installez le plugin ``fess-ds-db``.
Ce plugin peut se connecter à diverses bases de données (MySQL, PostgreSQL, Oracle, SQL Server, etc.) via JDBC.

Configuration
--------------

1. Accédez à [Crawler] > [Data Store] > [Créer nouveau]
2. Nom du handler : Sélectionnez DatabaseDataStore
3. Configurez les paramètres et les scripts
4. Label : Définissez ``database``

**Exemple de configuration des paramètres**

.. code-block:: properties

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://db-server:3306/mydb?useSSL=true
    username=fess_reader
    password=your-password
    sql=SELECT product_id, product_name, description, price, CONCAT('https://internal-app/products/', product_id) AS url FROM products WHERE status = 'active'

**Exemple de configuration du script**

.. code-block:: properties

    url=url
    title=product_name
    content=description

Les résultats de la requête SQL spécifiée dans ``sql`` sont explorés. Dans les scripts, utilisez les noms de colonnes SQL (ou les libellés de colonnes) pour les mapper aux champs de l'index Fess.

Conception des requêtes SQL
-----------------------------

Points clés lors de la conception de la requête SQL pour le paramètre ``sql`` :

- Incluez une colonne ``url`` servant de destination du lien dans les résultats de recherche (par ex., ``CONCAT('https://.../', id) AS url``)
- Incluez les colonnes servant de corps de texte recherchable
- Utilisez une clause ``WHERE`` pour exclure les données inutiles (par ex., ``status = 'active'``)

Dans les scripts, utilisez directement les noms de colonnes SQL pour les mapper aux champs de l'index Fess.

Intégration des fichiers CSV
==============================

Les données des fichiers CSV peuvent également être rendues recherchables.

Configuration
--------------

Utilisez le plugin ``fess-ds-csv`` ou la fonctionnalité du data store CSV.

1. Accédez à [Crawler] > [Data Store] > [Créer nouveau]
2. Nom du handler : Sélectionnez CsvDataStore
3. Configurez les paramètres et les scripts
4. Label : Définissez ``csv-data``

**Exemple de configuration des paramètres**

.. code-block:: properties

    directories=/opt/fess/csv-data
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

**Exemple de configuration du script** (utiliser les noms de colonnes lorsqu'une ligne d'en-tête est présente)

.. code-block:: properties

    url="https://internal-app/contacts/" + id
    title=company_name
    content=company_name + " " + contact_name + " " + email

Lorsque ``has_header_line=true``, les noms de colonnes de la ligne d'en-tête peuvent être utilisés dans les scripts. En l'absence de ligne d'en-tête, les colonnes sont référencées par numéro, comme ``cell1``, ``cell2``, ``cell3``. Les scripts peuvent contenir des expressions Groovy, y compris la concaténation de chaînes.

Si les fichiers CSV sont mis à jour régulièrement, fixez l'emplacement des fichiers et configurez un calendrier d'exploration pour que les données les plus récentes soient automatiquement reflétées dans l'index.

Recherche transversale
========================

Une fois toutes les configurations de sources de données terminées, vous pouvez expérimenter la recherche transversale.

Exemple de recherche
---------------------

En recherchant "ABC Corporation", des résultats tels que les suivants sont retournés :

1. Informations de compte Salesforce (Account)
2. Propositions du serveur de fichiers (PDF)
3. Historique d'achats de produits de la base de données
4. Liste de participants au salon professionnel du CSV

Les utilisateurs peuvent trouver les informations dont ils ont besoin sans avoir à savoir où elles sont stockées.

Filtrage par label
-------------------

Lorsqu'il y a de nombreux résultats de recherche, utilisez les labels pour les affiner.

- ``salesforce`` : Données Salesforce uniquement
- ``database`` : Données de base de données uniquement
- ``csv-data`` : Données CSV uniquement
- ``shared-files`` : Documents du serveur de fichiers uniquement

Considérations opérationnelles
================================

Fraîcheur des données
----------------------

Les données SaaS et de bases de données peuvent être mises à jour fréquemment.
Configurez la fréquence d'exploration de manière appropriée pour maintenir la fraîcheur des résultats de recherche.

.. list-table:: Fréquence d'exploration recommandée
   :header-rows: 1
   :widths: 25 25 50

   * - Source de données
     - Fréquence recommandée
     - Raison
   * - Salesforce
     - Toutes les 4 à 6 heures
     - Les informations d'affaires et de clients sont mises à jour pendant les heures ouvrables
   * - Base de données
     - Toutes les 2 à 4 heures
     - Données à forte volatilité, comme les informations de stock
   * - CSV
     - Quotidiennement
     - Généralement mis à jour par traitement par lots

Sécurité de la connexion à la base de données
-------------------------------------------------

Lorsque vous vous connectez directement à une base de données, portez une attention particulière à la sécurité.

- Utilisez un utilisateur de base de données en lecture seule
- Restreignez les connexions à l'adresse IP du serveur Fess
- N'accordez pas de permissions d'accès aux tables inutiles
- Soyez vigilant quant à la gestion des mots de passe

Synthèse
=========

Cet article a couvert les scénarios pour rendre les données de Salesforce, des bases de données et des fichiers CSV recherchables avec Fess.

- Intégration des données CRM via le plugin de data store Salesforce
- Intégration de la BD interne via le plugin de data store de base de données
- Intégration des données de listes via le data store CSV
- Mappage des champs et conception des requêtes SQL
- Exploitation des labels dans la recherche transversale

En éliminant les silos de données, vous pouvez réaliser un environnement où toutes les sources d'information sont recherchables depuis une seule plateforme.
Ceci conclut la section Solutions Pratiques. À partir de la prochaine partie, nous aborderons la section Architecture et Mise à l'échelle, en commençant par la conception multi-tenant.

Références
==========

- `Fess Data Store Configuration <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Fess Plugin Management <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
