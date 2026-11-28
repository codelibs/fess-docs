===========================================
Fess face aux autres solutions de recherche
===========================================

Introduction
============

Pour mettre en place une recherche sur des documents internes ou sur un site web, les options possibles incluent des systèmes de recherche comme Fess, un développement interne reposant sur un moteur de recherche comme OpenSearch ou Apache Solr, des services de recherche web externes et des produits commerciaux de recherche d'entreprise.
Cet article présente d'abord ce que fournit Fess 15.9 sous une forme facile à vérifier, puis compare son rôle à celui des autres options.

.. note::

   Les informations sur Fess correspondent à la version 15.9.
   Pour les autres produits et services, cet article ne traite que des différences d'architecture peu susceptibles d'évoluer. Les fonctionnalités, les tarifs et la disponibilité peuvent changer ; consultez la documentation la plus récente de chaque produit.

Ce que fournit Fess
===================

Fess est un système de recherche qui utilise OpenSearch comme moteur de recherche.
Il fournit le crawler, la console d'administration, l'interface de recherche et les API sous la forme d'une seule application, et stocke l'index et les paramètres de crawl dans OpenSearch.
Elasticsearch et Solr ne peuvent pas être utilisés comme moteur de recherche.
La licence est l'Apache License 2.0.

De nombreuses fonctionnalités sont fournies sous forme de plugins, et vous n'installez que celles dont vous avez besoin.
Les éléments dont la colonne « Prérequis » est vide dans le tableau suivant fonctionnent avec Fess seul.

.. list-table::
   :header-rows: 1
   :widths: 22 48 30

   * - Élément
     - Ce que fournit 15.9
     - Prérequis
   * - Crawl web
     - Explore les sites HTTP/HTTPS. L'authentification web, les en-têtes de requête et le mappage de chemins sont configurables
     -
   * - Crawl de fichiers
     - Explore les chemins ``file``, ``smb``, ``smb1`` et ``ftp``
     -
   * - Crawl de stockage cloud
     - ``s3://`` (Amazon S3 et stockage compatible S3), ``gcs://`` (Google Cloud Storage)
     - ``fess-storage-s3``, ``fess-storage-gcs``
   * - Bases de données et SaaS
     - Importées via des connecteurs DataStore (liste dans la section suivante)
     - Plugins ``fess-ds-*``
   * - Formats de documents
     - Documents Office, PDF, HTML, texte, archives, etc. L'OCR des images et des PDF numérisés est désactivé par défaut
     - La commande ``tesseract`` pour l'OCR
   * - Contrôle d'accès
     - Affiche des résultats de recherche différents selon le rôle, le groupe et l'utilisateur. Pour le crawl SMB et de fichiers, les permissions des fichiers sont importées comme rôles. L'intégration LDAP (y compris Active Directory) est une fonctionnalité du cœur
     -
   * - Authentification unique (SSO)
     - OpenID Connect, SAML, SPNEGO (Kerberos), Microsoft Entra ID
     - ``fess-sso-oidc``, ``fess-sso-saml``, ``fess-sso-spnego``, ``fess-sso-entraid``
   * - Interface de recherche
     - Affichée par un thème statique (HTML, CSS et JavaScript regroupés dans un ZIP). Le thème fourni est ``bootstrap``
     -
   * - API
     - ``/api/v2`` pour la recherche, les étiquettes, les suggestions, les mots populaires, le contrôle de santé, le mode de recherche IA, etc. ; ``/api/admin`` pour l'administration
     -
   * - API héritées
     - ``/api/v1``, ``/json`` et ``/suggest``
     - ``fess-webapp-v1-api``, ``fess-webapp-classic-api``
   * - Recherche sémantique
     - Découpe le contenu en chunks, les vectorise et fusionne les résultats avec ceux de la recherche par mots-clés par Rank Fusion. Désactivée par défaut
     - Un modèle d'embedding (ML Commons d'OpenSearch ou un plugin ``fess-llm-*``)
   * - Mode de recherche IA (RAG)
     - Un LLM répond aux questions en s'appuyant sur les résultats de recherche. Désactivé par défaut
     - L'un de ``fess-llm-ollama``, ``fess-llm-openai``, ``fess-llm-gemini``, ``fess-llm-bedrock``
   * - Serveur MCP
     - Permet aux agents IA de rechercher dans Fess via ``/mcp``
     - ``fess-webapp-mcp``
   * - Recherche d'images
     - Recherche multimodale qui trouve des images (GIF, JPEG, PNG) à partir d'une description textuelle
     - ``fess-webapp-multimodal`` et un serveur CLIP

L'image Docker inclut les quatre plugins SSO, ``fess-storage-s3``, ``fess-storage-gcs`` et ``fess-script-groovy``.
Installez les autres plugins depuis [Système] > [Plugin], puis redémarrez Fess.
Choisissez la version du plugin correspondant à la version mineure de Fess (15.9.x pour 15.9).

Connecteurs DataStore
---------------------

Les plugins DataStore suivants sont publiés pour 15.9.
La configuration est décrite dans la référence de chaque connecteur.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Catégorie
     - Plugin (cible)
   * - Stockage cloud
     - ``fess-ds-box`` (Box), ``fess-ds-dropbox`` (Dropbox), ``fess-ds-gsuite`` (Google Drive), ``fess-ds-microsoft365`` (OneDrive, SharePoint Online, Teams, etc.)
   * - Collaboration
     - ``fess-ds-atlassian`` (Confluence, Jira), ``fess-ds-slack`` (Slack), ``fess-ds-notion`` (Notion), ``fess-ds-backlog`` (Backlog), ``fess-ds-sharepoint`` (SharePoint Server sur site)
   * - Développement et systèmes métier
     - ``fess-ds-git`` (dépôts Git), ``fess-ds-salesforce`` (Salesforce)
   * - Données
     - ``fess-ds-db`` (bases de données accessibles via JDBC), ``fess-ds-csv`` (CSV), ``fess-ds-json`` (JSON), ``fess-ds-wikipedia`` (dumps de Wikipédia)

Une source de données absente de cette liste peut être rendue consultable en écrivant votre propre plugin DataStore (:doc:`guide-17`) ou en enregistrant les documents via l'API d'administration (:doc:`guide-11`).

Par rapport à un développement interne sur un moteur de recherche (OpenSearch, Apache Solr)
===========================================================================================

OpenSearch et Apache Solr sont des moteurs de recherche.
Ils prennent en charge l'indexation et la recherche, mais n'incluent ni crawler pour collecter les données, ni interface de recherche pour les utilisateurs, ni contrôle d'accès par document.
Vous devez soit développer ces parties vous-même, soit combiner d'autres logiciels.
Pour le crawl web, par exemple, il existe des projets distincts comme Apache Nutch.

Fess est une application qui fournit ces parties au-dessus d'OpenSearch.
Les différences sont les suivantes.

.. list-table::
   :header-rows: 1
   :widths: 24 38 38

   * - Aspect
     - Fess
     - Développement interne sur un moteur de recherche
   * - Collecte des données
     - Les crawls web, de fichiers et DataStore se configurent dans la console d'administration
     - Développer des crawlers et des traitements d'import, ou combiner d'autres logiciels
   * - Interface de recherche
     - Affichée par un thème. Pour changer l'apparence, créez un thème ou construisez votre propre interface sur l'API
     - Entièrement libre, mais tout est à développer
   * - Contrôle d'accès
     - Les rôles et les permissions des fichiers sont enregistrés sur chaque document, et la recherche est filtrée selon l'utilisateur connecté
     - Concevoir et implémenter l'import des permissions des documents et le filtrage au moment de la recherche
   * - Conception de l'index
     - Utilise l'index défini par Fess. Des analyseurs pour de nombreuses langues, dont le français, sont préconfigurés
     - Peut être conçu librement selon l'usage
   * - Ce que vous exploitez
     - Fess et OpenSearch
     - Le moteur de recherche et toutes les parties développées en interne

Si vous souhaitez concevoir le mécanisme de recherche de A à Z ou rechercher dans vos propres structures de données, utiliser directement un moteur de recherche est plus adapté.
En revanche, si l'objectif est de collecter des documents et de les rendre consultables au sein de votre organisation, commencer avec Fess et combler les manques avec l'API ou des plugins réduit l'étendue du développement.

Fess peut aussi se connecter à un cluster OpenSearch existant.
Pour les services où les plugins CodeLibs ne peuvent pas être installés, comme Amazon OpenSearch Service, définissez ``search_engine.type`` sur ``aws`` ou ``vanilla``.
Dans ce cas, certaines fonctionnalités comme la gestion des dictionnaires et la détection des documents en double ne sont pas disponibles (voir `Type de moteur de recherche <https://fess.codelibs.org/fr/stable/config/search-engine-type.html>`__).

Par rapport à une recherche de site via un service de recherche web externe
===========================================================================

Une autre façon de fournir une recherche de site consiste à utiliser l'index d'un fournisseur de services de recherche.
Avec cette approche, seules les pages publiques récupérées par le crawler du fournisseur sont consultables.
Les pages nécessitant une connexion et les serveurs de fichiers internes ne peuvent pas être couverts, et le moment du crawl comme l'ordre d'affichage dépendent également du fournisseur.

Avec Fess, vous décidez de ce qui est exploré et quand, et l'index reste dans votre propre environnement.
Pour ajuster les résultats de recherche, vous pouvez utiliser notamment la Correspondance de clé (placer certains documents en tête pour certains termes), le Boost de document et la Requête associée.
Il existe deux façons d'intégrer Fess à un site existant.

- Placer un formulaire de recherche qui renvoie vers l'interface de recherche de Fess (thème)
- Intégrer le JavaScript de Fess Site Search (FSS) pour afficher les résultats de recherche dans la page

FSS appelle ``/api/v1`` ; le plugin ``fess-webapp-v1-api`` est donc requis en 15.9.
Consultez :doc:`guide-03` pour la procédure.

Par rapport aux produits commerciaux de recherche d'entreprise
==============================================================

Par rapport aux produits commerciaux, le périmètre couvert varie fortement d'un produit à l'autre ; il est donc impossible de dire de manière générale lequel est meilleur.
Nous recommandons de vérifier les produits candidats et Fess dans les mêmes conditions selon les aspects suivants.

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - Aspect
     - Pour Fess
   * - Sources de données prises en charge
     - Consultez le tableau de la section précédente et la liste des connecteurs DataStore. S'il manque quelque chose, vous pouvez écrire votre propre plugin
   * - Contrôle d'accès
     - Par rôle, groupe et utilisateur, avec prise en charge de LDAP et de quatre méthodes de SSO
   * - IA générative
     - Mode de recherche IA (RAG), recherche sémantique et serveur MCP. Le LLM se choisit parmi Ollama (auto-hébergé), OpenAI, Gemini et Amazon Bedrock
   * - Emplacement des données
     - L'index est stocké dans un OpenSearch que vous exploitez vous-même. Si vous utilisez des services externes pour le LLM ou les embeddings, les questions et le contenu des documents sont envoyés à ces services
   * - Mode d'exploitation
     - Logiciel auto-hébergé. Il s'installe avec Docker, sous Linux (ZIP, RPM, DEB) et sous Windows. Il fonctionne aussi sur Kubernetes, mais il n'existe pas de chart Helm officiel
   * - Coûts et support
     - Aucun coût de licence. Les coûts sont les serveurs et l'effort d'exploitation. Pour le support commercial, consultez `Support commercial <https://fess.codelibs.org/fr/support-services.html>`__
   * - Liberté de modification
     - Le code source est public, et Fess peut être étendu avec des thèmes, des plugins et l'API

Les produits commerciaux conviennent lorsque le produit offre déjà les connecteurs et les fonctions de gestion nécessaires et que vous souhaitez confier l'exploitation au fournisseur.
Fess convient lorsque vous souhaitez construire une plateforme de recherche en combinant les fonctionnalités nécessaires tout en gardant vos données dans votre propre environnement.

Comment choisir
===============

Répondez aux questions suivantes dans l'ordre pour déterminer si Fess est un candidat.

1. Les données que vous souhaitez rechercher sont-elles couvertes par les cibles de crawl ou les connecteurs DataStore de Fess ?

   - Sinon, estimez le développement nécessaire pour écrire votre propre plugin (:doc:`guide-17`) ou pour enregistrer les documents via l'API (:doc:`guide-11`).

2. Devez-vous afficher des documents différents selon les utilisateurs ?

   - Pour utiliser les permissions du serveur de fichiers, consultez :doc:`file-server-search` ; pour la conception des rôles, :doc:`guide-05` ; pour le SSO, :doc:`guide-15`.

3. Le thème de Fess suffit-il pour votre interface de recherche ?

   - Pour intégrer la recherche dans votre propre application, utilisez ``/api/v2`` (:doc:`guide-11`).

4. Pouvez-vous exploiter Fess et OpenSearch vous-même ?

   - Si ce n'est pas le cas, ou si vous souhaitez confier l'exploitation à un fournisseur, envisagez le support commercial de Fess ou un produit commercial.

5. Avez-vous besoin de réponses par IA générative ou d'une recherche sémantique ?

   - Choisissez le LLM à utiliser et vérifiez la configuration nécessaire dans :doc:`guide-19` et :doc:`guide-18`.

Si les réponses à 1 et 4 sont « oui », le plus sûr est d'essayer Fess et de vérifier les résultats de recherche avec vos documents réels.

Essayer pour vérifier
=====================

Un tableau comparatif seul ne permet pas de savoir dans quelle mesure vos propres documents seront bien retrouvés.
Démarrez Fess avec Docker en suivant la procédure de :doc:`guide-02`, explorez une partie des contenus à rechercher et vérifiez les points suivants.

- Les documents cibles ont-ils été indexés (vérifiez dans [Informations système] > [Journal des tâches] et [URL d'échec] qu'aucune URL n'a abouti à une erreur)
- Une recherche sur des termes fréquemment utilisés fait-elle remonter les documents attendus en tête
- Les documents qui ne doivent pas être visibles restent-ils masqués lorsque vous changez d'utilisateur connecté (si vous avez besoin du contrôle d'accès)

Articles à lire ensuite
=======================

- Comprendre l'architecture de Fess et comment parcourir les articles : :doc:`guide-01`
- Faire fonctionner Fess en local pour commencer : :doc:`guide-02`
- Ajouter une recherche à un site existant : :doc:`guide-03`
- Rechercher des données de bases de données ou de SaaS : :doc:`datastore-basics`
- Refléter les permissions du serveur de fichiers dans les résultats de recherche : :doc:`file-server-search`
- Faire répondre une IA générative à partir des documents internes : :doc:`guide-19`
- Se préparer à la montée en charge : :doc:`guide-14`
- Découvrir des exemples d'utilisation : :doc:`use-cases`

Références
==========

- `Aperçu des connecteurs DataStore <https://fess.codelibs.org/fr/stable/config/datastore/ds-overview.html>`__
- `Crawl de système de fichiers (recherche sur serveur de fichiers) <https://fess.codelibs.org/fr/stable/admin/fileconfig-guide.html>`__
- `Fichiers recherchables <https://fess.codelibs.org/fr/supported-files.html>`__
- `Configuration de l'OCR <https://fess.codelibs.org/fr/stable/config/crawler-ocr.html>`__
- `Thème <https://fess.codelibs.org/fr/stable/admin/theme-guide.html>`__
- `Vue d'ensemble de l'API <https://fess.codelibs.org/fr/stable/api/api-overview.html>`__
- `Recherche sémantique <https://fess.codelibs.org/fr/stable/config/search-semantic.html>`__
- `Vue d'ensemble du mode de recherche IA (RAG) et de l'intégration LLM <https://fess.codelibs.org/fr/stable/config/llm-overview.html>`__
- `Type de moteur de recherche <https://fess.codelibs.org/fr/stable/config/search-engine-type.html>`__
- `Plugins <https://fess.codelibs.org/fr/stable/admin/plugin-guide.html>`__
