============================
Architecture et structure du code
============================

Cette page explique l'architecture de |Fess|, la structure du code,
et les principaux composants.
En comprenant la structure interne de |Fess|, vous pouvez développer efficacement.

.. contents:: Table des matières
   :local:
   :depth: 2

Architecture globale
================

|Fess| est composé des principaux composants suivants :

.. code-block:: text

    ┌─────────────────────────────────────────────────┐
    │          Interface utilisateur                   │
    │  ┌──────────────┐      ┌──────────────┐        │
    │  │  Écran de    │      │   Écran      │        │
    │  │  recherche   │      │   d'admin    │        │
    │  │  (JSP/HTML)  │      │   (JSP/HTML) │        │
    │  └──────────────┘      └──────────────┘        │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │              Couche application Web              │
    │  ┌──────────────────────────────────────────┐  │
    │  │           LastaFlute                       │  │
    │  │  ┌────────┐  ┌─────────┐  ┌──────────┐  │  │
    │  │  │ Action │  │  Form   │  │  Service │  │  │
    │  │  └────────┘  └─────────┘  └──────────┘  │  │
    │  └──────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │              Couche logique métier               │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
    │  │ Crawler  │  │  Job     │  │  Helper  │    │
    │  └──────────┘  └──────────┘  └──────────┘    │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │              Couche d'accès aux données          │
    │  ┌──────────────────────────────────────────┐  │
    │  │          DBFlute / OpenSearch             │  │
    │  │  ┌────────┐  ┌─────────┐  ┌──────────┐  │  │
    │  │  │Behavior│  │ Entity  │  │  Query   │  │  │
    │  │  └────────┘  └─────────┘  └──────────┘  │  │
    │  └──────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │               Stockage de données                │
    │              OpenSearch 3.3.0                   │
    └─────────────────────────────────────────────────┘

Description des couches
------------

Couche interface utilisateur
~~~~~~~~~~~~~~~~~~~~~~~~

C'est l'écran que les utilisateurs manipulent directement.
Implémenté en JSP, HTML et JavaScript.

- Écran de recherche : Interface de recherche pour les utilisateurs finaux
- Écran d'administration : Interface de configuration et de gestion pour les administrateurs système

Couche application Web
~~~~~~~~~~~~~~~~~~~~

Couche d'application Web utilisant le framework LastaFlute.

- **Action** : Traite les requêtes HTTP et appelle la logique métier
- **Form** : Réception et validation des paramètres de requête
- **Service** : Implémentation de la logique métier

Couche logique métier
~~~~~~~~~~~~~~~~

Couche qui implémente les fonctionnalités principales de |Fess|.

- **Crawler** : Collecte de données depuis des sites Web et des systèmes de fichiers
- **Job** : Tâches exécutées selon un calendrier
- **Helper** : Classes d'aide utilisées dans toute l'application

Couche d'accès aux données
~~~~~~~~~~~~~~

Couche d'accès à OpenSearch utilisant DBFlute.

- **Behavior** : Interface de manipulation de données
- **Entity** : Entité de données
- **Query** : Construction de requêtes de recherche

Couche stockage de données
~~~~~~~~~~~~

Utilise OpenSearch 3.3.0 comme moteur de recherche.

Structure du projet
==============

Structure des répertoires
--------------

.. code-block:: text

    fess/
    ├── src/
    │   ├── main/
    │   │   ├── java/org/codelibs/fess/
    │   │   │   ├── app/              # Application Web
    │   │   │   │   ├── web/          # Écran de recherche
    │   │   │   │   │   ├── admin/    # Écran d'administration
    │   │   │   │   │   │   ├── ...Action.java
    │   │   │   │   │   │   └── ...Form.java
    │   │   │   │   │   └── ...Action.java
    │   │   │   │   └── service/      # Couche service
    │   │   │   ├── crawler/          # Crawler
    │   │   │   │   ├── client/       # Client crawler
    │   │   │   │   ├── extractor/    # Extraction de contenu
    │   │   │   │   ├── filter/       # Filtres
    │   │   │   │   └── transformer/  # Transformation de données
    │   │   │   ├── es/               # Relatif à OpenSearch
    │   │   │   │   ├── client/       # Client OpenSearch
    │   │   │   │   ├── query/        # Constructeur de requêtes
    │   │   │   │   └── config/       # Gestion de configuration
    │   │   │   ├── helper/           # Classes d'aide
    │   │   │   │   ├── ...Helper.java
    │   │   │   ├── job/              # Jobs
    │   │   │   │   ├── ...Job.java
    │   │   │   ├── util/             # Utilitaires
    │   │   │   ├── entity/           # Entités (auto-généré)
    │   │   │   ├── mylasta/          # Configuration LastaFlute
    │   │   │   │   ├── action/       # Classe de base Action
    │   │   │   │   ├── direction/    # Configuration application
    │   │   │   │   └── mail/         # Configuration mail
    │   │   │   ├── Constants.java    # Définition de constantes
    │   │   │   └── FessBoot.java     # Classe de démarrage
    │   │   ├── resources/
    │   │   │   ├── fess_config.properties  # Fichier de configuration
    │   │   │   ├── fess_config.xml         # Configuration additionnelle
    │   │   │   ├── fess_message_ja.properties  # Messages (japonais)
    │   │   │   ├── fess_message_en.properties  # Messages (anglais)
    │   │   │   ├── log4j2.xml              # Configuration logs
    │   │   │   └── ...
    │   │   └── webapp/
    │   │       ├── WEB-INF/
    │   │       │   ├── view/          # Fichiers JSP
    │   │       │   │   ├── admin/     # JSP écran d'administration
    │   │       │   │   └── ...
    │   │       │   └── web.xml
    │   │       ├── css/               # Fichiers CSS
    │   │       ├── js/                # Fichiers JavaScript
    │   │       └── images/            # Fichiers images
    │   └── test/
    │       └── java/org/codelibs/fess/
    │           ├── ...Test.java       # Classes de test
    │           └── it/                # Tests d'intégration
    ├── pom.xml                        # Configuration Maven
    ├── dbflute_fess/                  # Configuration DBFlute
    │   ├── dfprop/                    # Propriétés DBFlute
    │   └── freegen/                   # Configuration FreeGen
    └── README.md

Détails des principaux packages
==================

Package app
------------

Code de la couche application Web.

Package app.web
~~~~~~~~~~~~~~~~

Implémente l'écran de recherche et les fonctionnalités pour les utilisateurs finaux.

**Classes principales :**

- ``SearchAction.java`` : Traitement de recherche
- ``LoginAction.java`` : Traitement de connexion

**Exemple :**

.. code-block:: java

    @Execute
    public HtmlResponse index(SearchForm form) {
        // Implémentation du traitement de recherche
        return asHtml(path_IndexJsp);
    }

Package app.web.admin
~~~~~~~~~~~~~~~~~~~~~~~

Implémente les fonctionnalités de l'écran d'administration.

**Classes principales :**

- ``BwCrawlingConfigAction.java`` : Configuration du crawl Web
- ``BwSchedulerAction.java`` : Gestion du planificateur
- ``BwUserAction.java`` : Gestion des utilisateurs

**Convention de nommage :**

- Préfixe ``Bw`` : Action pour l'administration
- Suffixe ``Action`` : Classe Action
- Suffixe ``Form`` : Classe Form

Package app.service
~~~~~~~~~~~~~~~~~~~~

Couche service qui implémente la logique métier.

**Classes principales :**

- ``SearchService.java`` : Service de recherche
- ``UserService.java`` : Service de gestion des utilisateurs
- ``ScheduledJobService.java`` : Service de gestion des jobs

**Exemple :**

.. code-block:: java

    public class SearchService {
        public SearchResponse search(SearchRequestParams params) {
            // Implémentation de la logique de recherche
        }
    }

Package crawler
----------------

Implémente la fonctionnalité de collecte de données.

Package crawler.client
~~~~~~~~~~~~~~~~~~~~~~~

Implémente l'accès aux différentes sources de données.

**Classes principales :**

- ``FessClient.java`` : Classe de base du client crawler
- ``WebClient.java`` : Crawl de sites Web
- ``FileSystemClient.java`` : Crawl de systèmes de fichiers
- ``DataStoreClient.java`` : Crawl de bases de données, etc.

Package crawler.extractor
~~~~~~~~~~~~~~~~~~~~~~~~~~

Extrait le texte des documents.

**Classes principales :**

- ``ExtractorFactory.java`` : Fabrique d'extracteurs
- ``TikaExtractor.java`` : Extraction utilisant Apache Tika

Package crawler.transformer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Transforme les données crawlées en format de recherche.

**Classes principales :**

- ``Transformer.java`` : Interface de traitement de transformation
- ``BasicTransformer.java`` : Traitement de transformation de base

Package es
-----------

Implémente l'intégration avec OpenSearch.

Package es.client
~~~~~~~~~~~~~~~~~~

Implémentation du client OpenSearch.

**Classes principales :**

- ``FessEsClient.java`` : Client OpenSearch
- ``SearchEngineClient.java`` : Interface du client de moteur de recherche

Package es.query
~~~~~~~~~~~~~~~~~

Implémente la construction de requêtes de recherche.

**Classes principales :**

- ``QueryHelper.java`` : Aide à la construction de requêtes
- ``FunctionScoreQueryBuilder.java`` : Ajustement du score

Package helper
---------------

Classes d'aide utilisées dans toute l'application.

**Classes principales :**

- ``SystemHelper.java`` : Aide système globale
- ``CrawlingConfigHelper.java`` : Aide à la configuration du crawl
- ``SearchLogHelper.java`` : Aide aux journaux de recherche
- ``UserInfoHelper.java`` : Aide aux informations utilisateur
- ``ViewHelper.java`` : Aide relative à la vue

**Exemple :**

.. code-block:: java

    public class SystemHelper {
        public void initializeSystem() {
            // Traitement d'initialisation du système
        }
    }

Package job
------------

Implémente les jobs exécutés selon un calendrier.

**Classes principales :**

- ``CrawlJob.java`` : Job de crawl
- ``SuggestJob.java`` : Job de suggestion
- ``ScriptExecutorJob.java`` : Job d'exécution de script

**Exemple :**

.. code-block:: java

    public class CrawlJob extends LaJob {
        @Override
        public void run() {
            // Implémentation du traitement de crawl
        }
    }

Package entity
---------------

Classes d'entités correspondant aux documents OpenSearch.
Ce package est auto-généré par DBFlute.

**Classes principales :**

- ``SearchLog.java`` : Journal de recherche
- ``ClickLog.java`` : Journal de clics
- ``FavoriteLog.java`` : Journal de favoris
- ``User.java`` : Informations utilisateur
- ``Role.java`` : Informations de rôle

.. note::

   Le code du package entity est auto-généré,
   ne le modifiez pas directement.
   Mettez à jour en modifiant le schéma et en régénérant.

Package mylasta
----------------

Configuration et personnalisation de LastaFlute.

Package mylasta.action
~~~~~~~~~~~~~~~~~~~~~~~

Définit les classes de base Action.

- ``FessUserBean.java`` : Informations utilisateur
- ``FessHtmlPath.java`` : Définition des chemins HTML

Package mylasta.direction
~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure l'application globale.

- ``FessConfig.java`` : Chargement de la configuration
- ``FessFwAssistantDirector.java`` : Configuration du framework

Modèles de conception et modèles d'implémentation
============================

|Fess| utilise les modèles de conception suivants.

Modèle MVC
----------

Implémenté selon le modèle MVC par LastaFlute.

- **Model** : Service, Entity
- **View** : JSP
- **Controller** : Action

Exemple :

.. code-block:: java

    // Controller (Action)
    public class SearchAction extends FessBaseAction {
        @Resource
        private SearchService searchService;  // Model (Service)

        @Execute
        public HtmlResponse index(SearchForm form) {
            SearchResponse response = searchService.search(form);
            return asHtml(path_IndexJsp).renderWith(data -> {
                data.register("response", response);  // Passage de données à View (JSP)
            });
        }
    }

Modèle DI
---------

Utilise le conteneur DI de LastaFlute.

.. code-block:: java

    public class SearchService {
        @Resource
        private SearchEngineClient searchEngineClient;

        @Resource
        private UserInfoHelper userInfoHelper;
    }

Modèle Factory
--------------

Utilisé pour la génération de divers composants.

.. code-block:: java

    public class ExtractorFactory {
        public Extractor createExtractor(String mimeType) {
            // Génère un Extractor selon le type MIME
        }
    }

Modèle Strategy
---------------

Utilisé dans le crawler et le transformer.

.. code-block:: java

    public interface Transformer {
        Map<String, Object> transform(Map<String, Object> data);
    }

    public class HtmlTransformer implements Transformer {
        // Traitement de transformation pour HTML
    }

Gestion de la configuration
======

La configuration de |Fess| est gérée dans plusieurs fichiers.

fess_config.properties
--------------------

Définit la configuration principale de l'application.

.. code-block:: properties

    # Numéro de port
    server.port=8080

    # Configuration de connexion OpenSearch
    opensearch.http.url=http://localhost:9201

    # Configuration du crawl
    crawler.document.max.size=10000000

fess_config.xml
--------------

Configuration additionnelle au format XML.

.. code-block:: xml

    <component name="searchService" class="...SearchService">
        <property name="maxSearchResults">1000</property>
    </component>

fess_message_*.properties
------------------------

Fichiers de messages pour le support multilingue.

- ``fess_message_ja.properties`` : Japonais
- ``fess_message_en.properties`` : Anglais

Flux de données
==========

Flux de recherche
--------

.. code-block:: text

    1. L'utilisateur effectue une recherche sur l'écran de recherche
       ↓
    2. SearchAction reçoit la requête de recherche
       ↓
    3. SearchService exécute la logique métier
       ↓
    4. SearchEngineClient envoie une requête de recherche à OpenSearch
       ↓
    5. OpenSearch retourne les résultats de recherche
       ↓
    6. SearchService formate les résultats
       ↓
    7. SearchAction passe les résultats à JSP pour l'affichage

Flux de crawl
------------

.. code-block:: text

    1. CrawlJob est exécuté selon le calendrier
       ↓
    2. CrawlingConfigHelper obtient la configuration du crawl
       ↓
    3. FessClient accède au site cible
       ↓
    4. Extractor extrait le texte du contenu
       ↓
    5. Transformer transforme les données en format de recherche
       ↓
    6. SearchEngineClient enregistre les documents dans OpenSearch

Points d'extension
==========

|Fess| peut être étendu aux points suivants.

Ajout d'un crawler personnalisé
--------------------

Vous pouvez prendre en charge vos propres sources de données en héritant de ``FessClient``.

Ajout d'un transformer personnalisé
----------------------------

Vous pouvez ajouter votre propre traitement de transformation de données en implémentant ``Transformer``.

Ajout d'un extracteur personnalisé
--------------------------

Vous pouvez ajouter votre propre traitement d'extraction de contenu en implémentant ``Extractor``.

Ajout d'un plugin personnalisé
--------------------

Vous pouvez créer vos propres plugins en implémentant l'interface ``Plugin``.

Ressources de référence
======

Frameworks
------------

- `Référence LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `Documentation DBFlute <https://dbflute.seasar.org/>`__

Documentation technique
--------------

- `Référence API OpenSearch <https://opensearch.org/docs/latest/api-reference/>`__
- `Apache Tika <https://tika.apache.org/>`__

Étapes suivantes
==========

Après avoir compris l'architecture, consultez la documentation suivante :

- :doc:`workflow` - Flux de développement réel
- :doc:`building` - Compilation et tests
- :doc:`contributing` - Création de pull requests
