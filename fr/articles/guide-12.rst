============================================================
Partie 12 : Rendre les donnees SaaS recherchables -- Scenarios d'integration avec Salesforce et les bases de donnees
============================================================

Introduction
=============

Les donnees importantes d'une entreprise ne sont pas uniquement stockees sur des serveurs de fichiers et dans le stockage cloud, mais egalement dans des applications SaaS et des bases de donnees.
Les informations clients dans Salesforce, les donnees de reference produit dans les bases de donnees internes, les donnees de listes gerees dans des fichiers CSV -- ces donnees ne sont generalement recherchables que dans leurs systemes respectifs.

Cet article traite des scenarios d'importation des donnees SaaS et de bases de donnees dans l'index Fess, permettant une recherche transversale avec les autres documents.

Public cible
=============

- Ceux qui souhaitent inclure les informations SaaS et de bases de donnees dans les resultats de recherche
- Ceux qui souhaitent apprendre a utiliser les plugins de data store
- Ceux qui souhaitent construire une plateforme de recherche couvrant plusieurs sources de donnees

Scenario
========

Une organisation commerciale a ses donnees reparties dans les systemes suivants.

.. list-table:: Situation des sources de donnees
   :header-rows: 1
   :widths: 20 35 45

   * - Systeme
     - Donnees stockees
     - Defi actuel
   * - Salesforce
     - Informations clients, enregistrements d'affaires, historique d'activites
     - Recherche possible uniquement dans Salesforce
   * - BD interne
     - Referentiel produits, grilles tarifaires, informations de stock
     - Accessible uniquement via une interface d'administration dediee
   * - Fichiers CSV
     - Listes de clients, listes de participants aux evenements
     - Recherche uniquement possible en ouvrant dans Excel et en parcourant visuellement
   * - Serveur de fichiers
     - Propositions, devis, contrats
     - Deja explores par Fess

L'objectif est de permettre la recherche transversale de toutes ces donnees avec Fess, afin que les informations necessaires aux activites commerciales puissent etre trouvees depuis un seul champ de recherche.

Integration des donnees Salesforce
====================================

Pour rendre les donnees Salesforce recherchables dans Fess, utilisez le plugin de data store Salesforce.

Installation du plugin
-----------------------

1. Accedez a [Systeme] > [Plugins] dans le panneau d'administration
2. Installez ``fess-ds-salesforce``

Parametres de connexion
------------------------

L'integration avec Salesforce necessite la configuration d'une Connected App.

**Preparation cote Salesforce**

1. Creez une Connected App dans les parametres Salesforce
2. Activez les parametres OAuth
3. Obtenez la cle et le secret du consommateur

**Configuration cote Fess**

1. Accedez a [Crawler] > [Data Store] > [Creer nouveau]
2. Nom du handler : Selectionnez SalesforceDataStore
3. Configurez les parametres et les scripts
4. Label : Definissez ``salesforce``

**Exemple de configuration des parametres**

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

Pour ``auth_type``, specifiez ``oauth_password`` (authentification par nom d'utilisateur/mot de passe) ou ``oauth_token`` (authentification par jeton JWT Bearer). Lors de l'utilisation de l'authentification JWT, definissez la cle privee RSA dans ``private_key``.

Selection des donnees cibles
------------------------------

Salesforce contient de nombreux objets, mais il n'est pas necessaire de tous les rendre recherchables.
Concentrez-vous sur les objets que l'equipe commerciale recherche frequemment.

.. list-table:: Exemple d'objets cibles
   :header-rows: 1
   :widths: 25 35 40

   * - Objet
     - Champs recherchables
     - Utilisation
   * - Account
     - Nom, secteur d'activite, adresse, description
     - Rechercher les informations de base des comptes
   * - Opportunity
     - Nom, etape, description, montant
     - Rechercher les affaires en cours
   * - Case
     - Objet, description, statut
     - Rechercher l'historique des demandes

Integration des bases de donnees
=================================

Pour rendre les donnees de bases de donnees internes recherchables, utilisez le plugin de data store de base de donnees.

Installation du plugin
-----------------------

Installez le plugin ``fess-ds-db``.
Ce plugin peut se connecter a diverses bases de donnees (MySQL, PostgreSQL, Oracle, SQL Server, etc.) via JDBC.

Configuration
--------------

1. Accedez a [Crawler] > [Data Store] > [Creer nouveau]
2. Nom du handler : Selectionnez DatabaseDataStore
3. Configurez les parametres et les scripts
4. Label : Definissez ``database``

**Exemple de configuration des parametres**

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

Les resultats de la requete SQL specifiee dans ``sql`` sont explores. Dans les scripts, utilisez les noms de colonnes SQL (ou les libelles de colonnes) pour les mapper aux champs de l'index Fess.

Conception des requetes SQL
-----------------------------

Points cles lors de la conception de la requete SQL pour le parametre ``sql`` :

- Incluez une colonne ``url`` servant de destination du lien dans les resultats de recherche (par ex., ``CONCAT('https://.../', id) AS url``)
- Incluez les colonnes servant de corps de texte recherchable
- Utilisez une clause ``WHERE`` pour exclure les donnees inutiles (par ex., ``status = 'active'``)

Dans les scripts, utilisez directement les noms de colonnes SQL pour les mapper aux champs de l'index Fess.

Integration des fichiers CSV
==============================

Les donnees des fichiers CSV peuvent egalement etre rendues recherchables.

Configuration
--------------

Utilisez le plugin ``fess-ds-csv`` ou la fonctionnalite du data store CSV.

1. Accedez a [Crawler] > [Data Store] > [Creer nouveau]
2. Nom du handler : Selectionnez CsvDataStore
3. Configurez les parametres et les scripts
4. Label : Definissez ``csv-data``

**Exemple de configuration des parametres**

.. code-block:: properties

    directories=/opt/fess/csv-data
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

**Exemple de configuration du script** (utiliser les noms de colonnes lorsqu'une ligne d'en-tete est presente)

.. code-block:: properties

    url="https://internal-app/contacts/" + id
    title=company_name
    content=company_name + " " + contact_name + " " + email

Lorsque ``has_header_line=true``, les noms de colonnes de la ligne d'en-tete peuvent etre utilises dans les scripts. En l'absence de ligne d'en-tete, les colonnes sont referencees par numero, comme ``cell1``, ``cell2``, ``cell3``. Les scripts peuvent contenir des expressions Groovy, y compris la concatenation de chaines.

Si les fichiers CSV sont mis a jour regulierement, fixez l'emplacement des fichiers et configurez un calendrier d'exploration pour que les donnees les plus recentes soient automatiquement refletees dans l'index.

Recherche transversale
========================

Une fois toutes les configurations de sources de donnees terminees, vous pouvez experimenter la recherche transversale.

Exemple de recherche
---------------------

En recherchant "ABC Corporation", des resultats tels que les suivants sont retournes :

1. Informations de compte Salesforce (Account)
2. Propositions du serveur de fichiers (PDF)
3. Historique d'achats de produits de la base de donnees
4. Liste de participants au salon professionnel du CSV

Les utilisateurs peuvent trouver les informations dont ils ont besoin sans avoir a savoir ou elles sont stockees.

Filtrage par label
-------------------

Lorsqu'il y a de nombreux resultats de recherche, utilisez les labels pour les affiner.

- ``salesforce`` : Donnees Salesforce uniquement
- ``database`` : Donnees de base de donnees uniquement
- ``csv-data`` : Donnees CSV uniquement
- ``shared-files`` : Documents du serveur de fichiers uniquement

Considerations operationnelles
================================

Fraicheur des donnees
----------------------

Les donnees SaaS et de bases de donnees peuvent etre mises a jour frequemment.
Configurez la frequence d'exploration de maniere appropriee pour maintenir la fraicheur des resultats de recherche.

.. list-table:: Frequence d'exploration recommandee
   :header-rows: 1
   :widths: 25 25 50

   * - Source de donnees
     - Frequence recommandee
     - Raison
   * - Salesforce
     - Toutes les 4 a 6 heures
     - Les informations d'affaires et de clients sont mises a jour pendant les heures ouvrables
   * - Base de donnees
     - Toutes les 2 a 4 heures
     - Donnees a forte volatilite, comme les informations de stock
   * - CSV
     - Quotidiennement
     - Generalement mis a jour par traitement par lots

Securite de la connexion a la base de donnees
-------------------------------------------------

Lorsque vous vous connectez directement a une base de donnees, portez une attention particuliere a la securite.

- Utilisez un utilisateur de base de donnees en lecture seule
- Restreignez les connexions a l'adresse IP du serveur Fess
- N'accordez pas de permissions d'acces aux tables inutiles
- Soyez vigilant quant a la gestion des mots de passe

Synthese
=========

Cet article a couvert les scenarios pour rendre les donnees de Salesforce, des bases de donnees et des fichiers CSV recherchables avec Fess.

- Integration des donnees CRM via le plugin de data store Salesforce
- Integration de la BD interne via le plugin de data store de base de donnees
- Integration des donnees de listes via le data store CSV
- Mappage des champs et conception des requetes SQL
- Exploitation des labels dans la recherche transversale

En eliminant les silos de donnees, vous pouvez realiser un environnement ou toutes les sources d'information sont recherchables depuis une seule plateforme.
Ceci conclut la section Solutions Pratiques. A partir de la prochaine partie, nous aborderons la section Architecture et Mise a l'echelle, en commencant par la conception multi-tenant.

References
==========

- `Fess Data Store Configuration <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Fess Plugin Management <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
