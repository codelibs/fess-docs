==============================================
Cas d'usage et scénarios d'utilisation de Fess
==============================================

Introduction
============

Cette page présente les situations dans lesquelles Fess est couramment utilisé, classées par secteur d'activité, par taille et par objectif technique.
Pour chaque scénario, elle indique le problème à résoudre, les fonctionnalités et plugins de Fess utilisés, ainsi que les articles qui expliquent la marche à suivre.
Les étapes de configuration elles-mêmes se trouvent dans chaque article : partez du scénario le plus proche de votre situation pour choisir les articles à lire.

Les noms des fonctionnalités et des plugins de cette page correspondent à Fess 15.9.
Dans la version 15.9, l'import depuis les bases de données et les services SaaS, le SSO ainsi que l'exploration de S3 et GCS sont fournis par des plugins.
Utilisez pour les plugins la même version 15.9.x que Fess, et redémarrez Fess après leur installation.
Pour la procédure d'installation, consultez `Plugins <https://fess.codelibs.org/fr/stable/admin/plugin-guide.html>`__.

.. note::

   Les sections suivantes décrivent des modèles d'utilisation généraux. Pour des cas de déploiement concrets, veuillez contacter le `support commercial <../support-services.html>`__.

Trouver les fonctionnalités selon l'objectif
============================================

.. list-table::
   :header-rows: 1
   :widths: 34 38 28

   * - Ce que vous voulez faire
     - Fonctionnalités et plugins
     - Articles à lire
   * - L'essayer d'abord en local
     - Docker Compose (docker-fess)
     - :doc:`guide-02`
   * - Rechercher ensemble dans le site intranet et les serveurs de fichiers
     - Exploration Web, exploration du système de fichiers, Authentification de fichier, étiquettes
     - :doc:`guide-04`, :doc:`file-server-search`
   * - Afficher des documents différents selon le service ou le poste
     - Autorisations, rôles et groupes, LDAP (Active Directory)
     - :doc:`guide-05`
   * - Ajouter une zone de recherche à un site existant
     - Formulaire de recherche, Fess Site Search (``fess-webapp-v1-api``), thèmes
     - :doc:`guide-03`
   * - Rechercher dans Git, Confluence, Jira et Slack
     - ``fess-ds-git``, ``fess-ds-atlassian``, ``fess-ds-slack``
     - :doc:`datastore-basics`, :doc:`guide-06`
   * - Rechercher dans Google Drive, SharePoint Online et Box
     - ``fess-ds-gsuite``, ``fess-ds-microsoft365``, ``fess-ds-box``
     - :doc:`datastore-basics`, :doc:`guide-07`
   * - Rechercher dans des bases de données, des CSV et Salesforce
     - ``fess-ds-db``, ``fess-ds-csv``, ``fess-ds-salesforce``
     - :doc:`datastore-basics`, :doc:`guide-12`
   * - Rechercher depuis les applications métier
     - API de recherche (``/api/v2``), jetons d'accès
     - :doc:`guide-11`
   * - Faire rechercher avec la connexion de l'entreprise
     - ``fess-sso-entraid``, ``fess-sso-oidc``, ``fess-sso-saml``, ``fess-sso-spnego``
     - :doc:`guide-15`
   * - Partager un seul Fess entre plusieurs organisations
     - Hôtes virtuels, rôles, étiquettes
     - :doc:`guide-13`
   * - Analyser les termes sans résultat et les usages pour améliorer la recherche
     - [Informations système] > [Journal de recherche]
     - :doc:`guide-08`
   * - Trouver des documents de sens proche, faire répondre une IA
     - Recherche sémantique, mode de recherche IA, ``fess-webapp-mcp``
     - :doc:`guide-18`, :doc:`guide-19`, :doc:`guide-20`
   * - Se préparer à l'augmentation des documents et des utilisateurs
     - Séparation et mise en cluster d'OpenSearch, plusieurs serveurs Fess
     - :doc:`guide-14`
   * - Fonctionner de manière stable en production
     - ``/api/v2/health``, sauvegardes, journaux
     - :doc:`guide-10`

Cas d'usage par secteur
=======================

Industrie : retrouver des documents techniques dispersés
--------------------------------------------------------

**Problème** : les documents de conception, les spécifications et les enregistrements qualité sont répartis sur les serveurs de fichiers de chaque service, et retrouver les documents liés à partir d'un numéro de plan ou de modèle prend du temps.

**Fonctionnalités utilisées** :

- Explorez les serveurs de fichiers avec ``smb://`` pour rendre le texte des PDF et des documents Office consultable par la recherche. Les droits d'accès Windows (ACL) sont importés par défaut comme autorisations des documents
- Créez des étiquettes dont le nom d'affichage est par exemple « Conception » ou « Qualité », classez les documents selon les chemins qu'elles couvrent et permettez de filtrer sur la page de recherche
- Les archives papier numérisées deviennent consultables par leur texte une fois l'OCR activé. L'OCR est désactivé par défaut et nécessite ``tesseract`` sur l'hôte où s'exécute le robot d'exploration (`Configuration de l'OCR <https://fess.codelibs.org/fr/stable/config/crawler-ocr.html>`__)

Les fichiers dont Fess ne peut pas extraire le texte ne sont trouvés que par leur nom ou leur chemin.
Vérifiez les formats pris en charge dans `Fichiers pris en charge <../supported-files.html>`__.

**Articles à lire** : construisez la configuration avec :doc:`guide-04`, vérifiez les prérequis des ACL dans :doc:`file-server-search`, puis configurez l'affichage par service avec :doc:`guide-05`.

Finance et assurance : retrouver règlements et contrats avec des autorisations
------------------------------------------------------------------------------

**Problème** : les règlements internes, manuels et contrats sont très nombreux, et les retrouver à chaque demande ou audit demande des efforts. Dans le même temps, il faut séparer strictement, par service, qui peut les consulter.

**Fonctionnalités utilisées** :

- Les autorisations par document limitent à qui un document est présenté dans les résultats de recherche. Les autorisations d'une nouvelle configuration d'exploration contiennent ``{role}guest`` dès le départ ; supprimez-le pour les documents non publics
- Pour empêcher les utilisateurs non connectés de rechercher, activez « Connexion requise » dans [Général]
- Pour la connexion via la plateforme d'identité de l'entreprise, utilisez le SSO : ``fess-sso-saml`` pour SAML, ``fess-sso-entraid`` pour Entra ID (l'image Docker inclut les quatre plugins SSO)
- Pour rechercher depuis les applications métier, conservez un jeton d'accès côté serveur et appelez l'API de recherche

**Articles à lire** : concevez les autorisations avec :doc:`guide-05`, et configurez le SSO et le HTTPS avec :doc:`guide-15`. L'intégration aux applications métier est traitée dans :doc:`guide-11`.

Enseignement : rechercher dans les sites et les lecteurs partagés du campus
---------------------------------------------------------------------------

**Problème** : les sites Web de chaque faculté, les supports de cours et les documents internes de l'établissement se trouvent à des endroits différents, et ni les étudiants ni le personnel ne parviennent à l'information recherchée.

**Fonctionnalités utilisées** :

- Importez les sites Web du campus par exploration Web. Les archives institutionnelles (comme DSpace) n'ont pas de connecteur dédié ; explorez donc leurs pages publiques
- Importez les lecteurs partagés de Google Drive avec ``fess-ds-gsuite`` et SharePoint Online avec ``fess-ds-microsoft365``
- Pour montrer des périmètres différents aux étudiants et au personnel, séparez-les avec les rôles et les autorisations. Pour séparer le site lui-même, utilisez les hôtes virtuels

**Articles à lire** : :doc:`guide-04`, :doc:`guide-07`, :doc:`guide-05`. Pour séparer le site, consultez :doc:`guide-13`.

Informatique et logiciel : retrouver les informations de développement en un seul endroit
-----------------------------------------------------------------------------------------

**Problème** : le code est dans Git, la conception dans Confluence, les tickets dans Jira et les discussions dans Slack ou Teams, ce qui rend difficile de retrouver l'historique des décisions.

**Fonctionnalités utilisées** :

- Importez les fichiers des dépôts avec ``fess-ds-git``, Confluence et Jira avec ``fess-ds-atlassian``, et les messages Slack avec ``fess-ds-slack``
- Les canaux et conversations Teams peuvent être importés avec le ``TeamsDataStore`` de ``fess-ds-microsoft365`` (`Connecteur Microsoft 365 <https://fess.codelibs.org/fr/stable/config/datastore/ds-microsoft365.html>`__)
- Une configuration spécialisée dans la recherche de code source, `docker-codesearch <https://github.com/codelibs/docker-codesearch>`__, est publiée
- Pour intégrer la recherche dans des outils internes, utilisez l'API de recherche ; pour faire rechercher des agents IA, utilisez ``fess-webapp-mcp``

**Articles à lire** : :doc:`datastore-basics`, puis :doc:`guide-06`. L'intégration avec les agents IA est traitée dans :doc:`guide-20`.

Cas d'usage par taille
======================

Le nombre de serveurs et la mémoire nécessaires ne se déduisent pas du seul nombre d'utilisateurs ou de documents.
La charge varie selon la longueur des textes, la part des pièces jointes et le fait que les utilisateurs se connectent ou non : commencez petit, mesurez, puis ajoutez ce qui manque.
La démarche de décision est résumée dans la section sur les ordres de grandeur de :doc:`guide-14`.
Pour la configuration serveur recommandée en production (au moins 4 cœurs CPU, au moins 8 Go de mémoire, etc.), consultez `Configuration requise <https://fess.codelibs.org/fr/stable/install/prerequisites.html>`__.

Commencer avec un seul serveur
------------------------------

Pour un déploiement à l'échelle d'un service ou un essai, exécutez Fess et OpenSearch sur un seul serveur.
Avec Docker Compose, démarrez-les avec deux fichiers : ``compose.yaml`` et ``compose-opensearch3.yaml``.
La marche à suivre se trouve dans :doc:`guide-02`.

Même avec un seul serveur, décidez dès le départ des deux points suivants.

- La manière de faire les sauvegardes. Les paramètres peuvent être téléchargés depuis [Informations système] > [Sauvegarde], mais les dictionnaires n'y sont pas inclus (:doc:`guide-10`)
- Avec Docker, les paramètres modifiés dans [Système] > [Général] sont enregistrés dans ``system.properties`` à l'intérieur du conteneur et reviennent à leur état initial lorsque le conteneur est recréé (voir la section sur l'arrêt et le redémarrage dans :doc:`guide-02`)

Quand d'autres services l'adoptent
----------------------------------

Lorsque la recherche ou l'exploration ralentit, déterminez d'abord si la cause se trouve dans Fess lui-même, dans le robot d'exploration ou dans OpenSearch.
Dans la plupart des cas, on étend le système dans l'ordre suivant.

1. Sur le serveur unique, ajuster le tas (heap) de Fess, du robot d'exploration et d'OpenSearch, ainsi que le parallélisme de l'exploration
2. Déplacer OpenSearch sur un serveur distinct
3. Passer OpenSearch en cluster de trois nœuds
4. Exécuter plusieurs serveurs Fess et répartir les requêtes avec un répartiteur de charge

Avec plusieurs serveurs Fess, gardez identiques sur tous les serveurs les paramètres de [Général], ``app.cipher.key`` dans ``fess_config.properties`` et les plugins installés.
Dans Fess 15.9, les sessions de connexion sont conservées dans la mémoire de chaque serveur ; lorsque vous répartissez des pages utilisées en étant connecté, activez donc les sessions persistantes (sticky sessions) sur le répartiteur de charge.
Enregistrer les sessions dans OpenSearch pour les partager entre serveurs est possible à partir de la version 15.10.

**Articles à lire** : :doc:`guide-14`, :doc:`guide-10`.

Utilisation à l'échelle de l'entreprise
---------------------------------------

À l'échelle de l'entreprise, envisagez les points suivants en plus de la configuration ci-dessus.

- Confiez l'exploration à un seul serveur Fess (``scheduler.target.name`` et la « Cible » de la tâche). Cela évite de faire peser la charge de l'exploration sur les serveurs qui traitent les recherches
- Utilisez ``/api/v2/health`` pour le répartiteur de charge et la supervision. Il renvoie 503 lorsque le cluster OpenSearch est ``RED`` ou injoignable
- Pour séparer la page de recherche ou les cibles par organisation, utilisez les hôtes virtuels ou des instances Fess distinctes (:doc:`guide-13`)
- Vérifiez régulièrement dans le journal de recherche les termes sans résultat et ceux dont les résultats ne sont pas cliqués (:doc:`guide-08`)

Fess peut aussi fonctionner sur Kubernetes, mais aucun chart Helm officiel n'est fourni.
Convertissez les fichiers Docker Compose ou écrivez vous-même les manifestes (voir la FAQ de `Installation Docker (détails) <https://fess.codelibs.org/fr/stable/install/install-docker.html>`__).

Pour un déploiement dans un environnement de grande taille, envisagez aussi le `support commercial <../support-services.html>`__.

Cas d'usage techniques
======================

Recherche transversale dans les wikis internes et les bases de connaissances
----------------------------------------------------------------------------

La façon d'importer le contenu dépend du type de wiki.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Cible
     - Mode d'import
     - Référence
   * - Confluence
     - ``fess-ds-atlassian`` (``ConfluenceDataStore``)
     - :doc:`guide-06`
   * - Notion
     - ``fess-ds-notion``
     - `Connecteur Notion <https://fess.codelibs.org/fr/stable/config/datastore/ds-notion.html>`__
   * - Backlog
     - ``fess-ds-backlog``
     - `Connecteur Backlog <https://fess.codelibs.org/fr/stable/config/datastore/ds-backlog.html>`__
   * - Wikis consultables sur le Web, comme MediaWiki
     - Exploration Web (configurez aussi l'Authentification Web si une connexion est requise)
     - :doc:`guide-04`

Les documents importés via un magasin de données contiennent eux aussi ``{role}guest`` dans leurs autorisations dès le départ.
Si vous importez des espaces que seul un groupe restreint peut lire, lisez d'abord la section de :doc:`guide-06` consacrée au choix des personnes à qui montrer les résultats de recherche.

Recherche unifiée sur les serveurs de fichiers
----------------------------------------------

L'exploration de fichiers de Fess 15.9 prend en charge les protocoles suivants.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Format du chemin
     - Cible
   * - ``smb://``
     - Dossiers partagés Windows, ou NAS partagés via SMB
   * - ``smb1://``
     - Anciens serveurs qui ne prennent en charge que SMB1
   * - ``file:``
     - Répertoires visibles depuis le serveur Fess. Montez d'abord les partages NFS dans le système d'exploitation, puis indiquez-les dans ce format
   * - ``ftp://``
     - Serveurs FTP
   * - ``s3://`` / ``gcs://``
     - Stockage compatible Amazon S3 / Google Cloud Storage. Nécessite ``fess-storage-s3`` / ``fess-storage-gcs`` (inclus dans l'image Docker)

Les protocoles activés par défaut sont ``file``, ``smb``, ``smb1`` et ``ftp`` (``crawler.file.protocols``).
Pour que les ACL SMB soient prises en compte dans les résultats de recherche, vous devez supprimer ``{role}guest`` des autorisations de la configuration d'exploration.
La raison et la méthode de vérification se trouvent dans :doc:`file-server-search`, et les réglages concrets dans :doc:`guide-04`.

Recherche dans un site Web
--------------------------

Il existe trois façons d'ajouter une recherche à un site public, et elles peuvent être combinées.

- Placer un formulaire de recherche qui renvoie vers la page de recherche de Fess. Aucun réglage supplémentaire n'est nécessaire côté Fess
- Afficher les résultats de recherche à l'intérieur d'une page existante avec Fess Site Search (FSS). FSS appelle ``/api/v1`` et nécessite donc, en 15.9, le plugin ``fess-webapp-v1-api``. Le JavaScript de FSS n'est pas servi par Fess : générez-le avec FSS JS Generator et hébergez-le sur votre propre site
- Adapter la page de recherche de Fess à l'apparence du site existant avec un thème

La marche à suivre se trouve dans :doc:`guide-03`.
Pour créer votre propre page de recherche, utilisez ``/api/v2/search`` (:doc:`guide-11`).

Recherche dans les bases de données
-----------------------------------

Les informations stockées dans des bases de données, comme les référentiels produits ou les FAQ, sont importées avec ``fess-ds-db``.
Les bases compatibles JDBC (MySQL, PostgreSQL, Oracle, SQL Server, etc.) sont prises en charge ; fournissez séparément un pilote JDBC adapté à la base cible.
Un script associe les colonnes obtenues par une requête SELECT à des champs tels que ``title`` et ``content``.

Si vous construisez l'URL de l'écran métier d'origine et la placez dans ``url``, les utilisateurs peuvent ouvrir directement les données d'origine depuis le lien du résultat de recherche.
La marche à suivre se trouve dans :doc:`guide-12`.

Combiner avec l'IA générative
-----------------------------

- Trouver des documents de sens proche même lorsque les mots-clés ne correspondent pas : recherche sémantique (:doc:`guide-18`)
- Faire répondre une IA en s'appuyant sur les documents internes : mode de recherche IA. Il fonctionne aussi sans recherche vectorielle (:doc:`guide-19`)
- Faire rechercher dans Fess des agents IA comme Claude Code : ``fess-webapp-mcp`` (:doc:`guide-20`)

Quelle que soit la méthode, les documents recherchés sont filtrés par les mêmes autorisations que pour une recherche normale (pour le mode de recherche IA, celles de l'utilisateur connecté ; pour MCP, celles du jeton d'accès, ou les autorisations d'invité lorsque MCP est utilisé sans authentification).
Ces autorisations déterminent aussi les documents transmis à l'IA : terminez donc d'abord la conception des autorisations de :doc:`guide-05`.

Démarche de déploiement
=======================

1. Démarrer Fess avec :doc:`guide-02`, explorer une partie des cibles et essayer la recherche
2. Dans le tableau ci-dessus, choisir les articles qui correspondent à votre problème et effectuer la configuration
3. Définir les autorisations (:doc:`guide-05`) et l'exploitation (:doc:`guide-10`) avant d'ouvrir le service aux utilisateurs

Références
==========

- `Démarrage rapide <../quick-start.html>`__
- `Documentation <../documentation.html>`__
- `Plugins <https://fess.codelibs.org/fr/stable/admin/plugin-guide.html>`__
- `Guide des connecteurs de magasin de données <https://fess.codelibs.org/fr/stable/config/datastore/index.html>`__
- `Forum de discussion <https://discuss.codelibs.org/c/FessEN/>`__
- `GitHub <https://github.com/codelibs/fess>`__
