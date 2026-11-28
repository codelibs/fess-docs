=========================================
Ce que permet Fess et comment le déployer
=========================================

Introduction
============

Les documents internes sont répartis entre les sites web, les serveurs de fichiers, le stockage cloud, des services SaaS comme la messagerie instantanée ou la gestion de tickets, et les bases de données.
Même si chacun de ces outils dispose de sa propre recherche, il est impossible de chercher dans tous ces emplacements à la fois.
Fess est un serveur de recherche qui rassemble les documents de ces emplacements dans un index unique, afin de pouvoir les rechercher depuis une seule page de recherche ou une seule API.

Cet article s'adresse aux responsables informatiques et aux développeurs qui envisagent de déployer Fess, et explique les points suivants :

- De quoi Fess est constitué et comment il fonctionne
- Quelles fonctionnalités sont disponibles en standard et lesquelles nécessitent des plugins supplémentaires
- Quels articles lire ensuite selon votre objectif

Les procédures de configuration de chaque fonctionnalité sont traitées dans les articles correspondants.

Version couverte par ce guide pratique
======================================

Tous les articles de ce guide pratique portent sur Fess 15.9.
Les noms des champs à l'écran, les clés de configuration et les valeurs par défaut ont été vérifiés avec la version 15.9.
Lorsqu'un article présente une fonctionnalité disponible uniquement à partir de la version 15.10, il le précise explicitement.

Les liens vers la documentation de référence commencent par ``https://fess.codelibs.org/fr/stable/`` et pointent vers la documentation de la version stable actuelle.
Si vous utilisez une autre version, remplacez ``stable`` dans l'URL par le numéro de version (par exemple ``15.9``) et vérifiez les noms de champs et les valeurs par défaut sur cette page.

Qu'est-ce que Fess ?
====================

Fess est un serveur de recherche plein texte open source écrit en Java.
Il est distribué sous licence Apache 2.0 et peut être utilisé gratuitement, y compris dans un environnement commercial.

Fess utilise OpenSearch pour stocker et rechercher les documents.
Au démarrage, Fess 15.9 vérifie le serveur auquel il se connecte et interrompt le démarrage s'il ne s'agit pas d'OpenSearch 3 ou d'une version ultérieure.
Il ne peut pas se connecter à OpenSearch 2 ou antérieur, ni à Elasticsearch.
Dans la version 15.9, le moteur de recherche autrefois intégré à Fess a été supprimé : vous devez donc toujours fournir OpenSearch séparément (dans la configuration Docker, un conteneur OpenSearch est démarré en même temps que Fess).

Une seule instance de Fess comprend tous les éléments suivants :

- Des robots d'exploration qui collectent les documents (web, serveurs de fichiers et divers services via des plugins)
- Une interface d'administration pour configurer l'exploration, les utilisateurs, les autorisations, les dictionnaires, les planifications, etc.
- Une page de recherche pour les utilisateurs
- Des API (``/api/v2/``) permettant d'appeler la recherche et les suggestions depuis des systèmes externes

La page de recherche est affichée par un thème statique qui regroupe HTML, CSS et JavaScript.
Fess est livré avec le thème ``bootstrap`` ; vous pouvez ajouter d'autres thèmes sous forme de fichiers ZIP dans [Système] > [Thème].

Architecture de Fess
====================

Les composants qui interviennent dans le fonctionnement de Fess sont les suivants.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Composant
     - Rôle
   * - Fess lui-même (application web)
     - Fournit la page de recherche, l'interface d'administration et les API. Le planificateur s'exécute également ici et lance aux heures configurées des tâches comme l'exploration
   * - Robot d'exploration (processus séparé)
     - Les tâches d'exploration sont lancées sous forme de processus Java distincts de Fess. Elles récupèrent les pages web et les fichiers, en extraient le texte et l'enregistrent dans OpenSearch. Les tâches de création des suggestions, de génération des miniatures et de création des vecteurs pour la recherche sémantique s'exécutent elles aussi de la même façon, dans des processus séparés
   * - OpenSearch
     - Contient l'index des documents à rechercher et exécute les recherches. Une grande partie des informations enregistrées dans l'interface d'administration, comme les paramètres d'exploration, les utilisateurs, les journaux des tâches et les journaux de recherche, y est également stockée

Comme le robot d'exploration est un processus Java distinct, sa mémoire se configure séparément de celle de Fess (voir :doc:`guide-14`).

Voici les étapes qui mènent à des documents consultables :

1. Enregistrez une configuration d'exploration dans l'interface d'administration (URL ou chemins cibles, autorisations qui déterminent qui peut voir les résultats, etc.)
2. Le planificateur lance la tâche d'exploration. Vous pouvez aussi la lancer manuellement depuis l'interface d'administration avec [Démarrer maintenant]
3. Le robot d'exploration récupère les documents, en extrait le texte et les enregistre dans OpenSearch avec leurs autorisations
4. Lorsqu'un utilisateur effectue une recherche, Fess filtre les résultats selon les rôles et les groupes de cet utilisateur avant de les renvoyer

Vous pouvez essayer l'ensemble de la séquence, du démarrage avec Docker à la recherche en passant par l'exploration, dans :doc:`guide-02`.

Fonctionnalités de base et plugins
==================================

Dans Fess 15.9, de nombreuses fonctionnalités sont fournies sous forme de plugins séparés de Fess.
La présence des plugins nécessaires dépend de la méthode d'installation.

- Un Fess installé à partir du ZIP, du RPM ou du DEB ne contient aucun plugin
- L'image Docker standard (par exemple ``ghcr.io/codelibs/fess:15.9.0``) contient les sept plugins suivants préinstallés : ``fess-script-groovy``, ``fess-storage-s3``, ``fess-storage-gcs``, ``fess-sso-saml``, ``fess-sso-spnego``, ``fess-sso-entraid``, ``fess-sso-oidc``
- L'image Docker slim (par exemple ``15.9.0-slim``) ne contient aucun plugin

Le tableau suivant résume les principales fonctionnalités et les plugins qu'elles nécessitent.

.. list-table::
   :header-rows: 1
   :widths: 22 39 39

   * - Fonctionnalité
     - Disponible avec Fess seul
     - Nécessite un plugin
   * - Exploration
     - Web (http et https), systèmes de fichiers, serveurs de fichiers (SMB), FTP
     - Amazon S3 (``fess-storage-s3``), Google Cloud Storage (``fess-storage-gcs``), exploration web qui exécute le JavaScript dans un navigateur pour récupérer les pages (``fess-crawler-playwright``)
   * - SaaS, bases de données, etc.
     - L'écran de configuration des magasins de données et le mécanisme qui les exécute
     - Un plugin de magasin de données (``fess-ds-*``) pour chaque source à importer. Slack, Confluence et Jira, Google Drive, Microsoft 365, Box, bases de données, CSV, Git, etc.
   * - Connexion et autorisations
     - Utilisateurs, rôles et groupes enregistrés dans Fess, et intégration avec LDAP / Active Directory
     - SSO (``fess-sso-oidc`` pour OpenID Connect, ``fess-sso-saml`` pour SAML, ``fess-sso-entraid`` pour Entra ID, ``fess-sso-spnego`` pour SPNEGO)
   * - Scripts
     - JavaScript
     - Groovy (``fess-script-groovy``), OGNL (``fess-script-ognl``)
   * - Page de recherche
     - Le thème fourni ``bootstrap``
     - On ajoute un fichier ZIP de thème, et non un plugin
   * - API
     - ``/api/v2/`` (recherche, étiquettes, suggestions, mots populaires, contrôle d'état, etc.) et l'API d'administration
     - ``/api/v1/`` (``fess-webapp-v1-api``), ``/json`` et ``/suggest`` (``fess-webapp-classic-api``). Fess Site Search utilise ``/api/v1/`` et nécessite donc ``fess-webapp-v1-api``
   * - IA
     - Les mécanismes de recherche sémantique et du mode de recherche IA (RAG). Si vous utilisez un modèle d'embedding déployé dans OpenSearch, la recherche sémantique ne nécessite aucun plugin
     - Connexion aux LLM et aux modèles d'embedding externes (``fess-llm-ollama``, ``fess-llm-openai``, ``fess-llm-gemini``, ``fess-llm-bedrock``), serveur MCP (``fess-webapp-mcp``), recherche d'images (``fess-webapp-multimodal``)

Parmi les éléments de la colonne « Nécessite un plugin », seuls S3 et GCS, les quatre types de SSO et Groovy sont inclus dans l'image Docker standard.
Tout le reste doit être installé en plus, quelle que soit la méthode d'installation.

Les configurations dont le type de script est Groovy, ainsi que les configurations reprises de versions antérieures dont le type de script n'est pas enregistré, sont exécutées en Groovy.
Pour les utiliser, ``fess-script-groovy`` est nécessaire.
Pour les nouvelles configurations de magasin de données, le type de script par défaut est JavaScript.

Installez les plugins de l'une des façons suivantes.
Après avoir installé ou supprimé un plugin, redémarrez Fess.
Alignez la version du plugin sur celle de Fess (15.9.x pour Fess 15.9).

- Dans l'interface d'administration, ouvrez [Système] > [Plugin], cliquez sur [Installer] et choisissez dans la liste
- En ligne de commande, exécutez ``bin/fess-setup install plugin <nom-du-plugin>:<version>``
- Avec Docker, définissez la variable d'environnement ``FESS_PLUGINS`` avec une liste séparée par des espaces, par exemple ``fess-ds-slack:15.9.0 fess-webapp-mcp:15.9.0``

L'utilisation des plugins de magasin de données est expliquée dans :doc:`datastore-basics`, et l'écriture de vos propres plugins dans :doc:`guide-17`.

Formats de fichiers consultables
================================

Le texte est extrait des fichiers par des traitements d'extraction comme Apache Tika.
Vous pouvez rechercher dans le HTML, le PDF, les documents Microsoft Office, le texte, le contenu des fichiers d'archive, etc.
Pour la liste des formats vérifiés, consultez `Fichiers recherchables <https://fess.codelibs.org/fr/supported-files.html>`__.

Le texte contenu dans les images et dans les PDF numérisés n'est pas consultable par défaut.
Il le devient si vous installez ``tesseract`` sur l'hôte où s'exécute le robot d'exploration et que vous activez l'OCR.
Pour la procédure, consultez `Configuration de l'OCR <https://fess.codelibs.org/fr/stable/config/crawler-ocr.html>`__.

Choisir une méthode d'installation
==================================

Fess est distribué sous forme d'image Docker et de paquets ZIP, RPM et DEB.
Pour un premier essai, Docker est le plus rapide, car il démarre Fess et OpenSearch ensemble.
La procédure est décrite dans :doc:`guide-02`.

En production, vous pouvez aussi fournir OpenSearch sous la forme d'un serveur ou d'un cluster séparé.
Pour les versions de Java et d'OpenSearch requises ainsi que les recommandations en matière de CPU, de mémoire et de disque, consultez `Configuration requise <https://fess.codelibs.org/fr/stable/install/prerequisites.html>`__.

Parcours de lecture par objectif
================================

Les articles sont organisés pour être lus selon votre objectif.
Choisissez la ligne la plus proche de votre objectif et lisez les articles de gauche à droite.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Objectif
     - Articles à lire
   * - Je veux d'abord essayer Fess
     - :doc:`guide-02`
   * - Je veux rechercher dans des serveurs de fichiers
     - :doc:`file-server-search` → :doc:`guide-04` → :doc:`guide-05`
   * - Je veux rechercher des données du cloud et de services SaaS
     - :doc:`datastore-basics` → :doc:`guide-07` / :doc:`guide-06` / :doc:`guide-12`
   * - Je veux intégrer la recherche à un site ou un système existant
     - :doc:`guide-03` → :doc:`guide-11`
   * - Je veux afficher des informations différentes selon le service ou l'utilisateur
     - :doc:`guide-05` → :doc:`guide-15` → :doc:`guide-13`
   * - Je veux améliorer la recherche avec l'IA
     - :doc:`guide-18` → :doc:`guide-19` → :doc:`guide-20`
   * - Je commence l'exploitation en production
     - :doc:`guide-10` → :doc:`guide-16` → :doc:`guide-14`

Les articles suivants sont également disponibles :

- Améliorer la qualité de la recherche : :doc:`guide-08`, :doc:`guide-09`, :doc:`guide-22`
- Rechercher des images et du texte ensemble : :doc:`guide-21`
- Écrire vos propres plugins : :doc:`guide-17`
- Planifier un déploiement à l'échelle de l'entreprise : :doc:`guide-23`
- Cas d'utilisation et comparaisons avec d'autres produits : :doc:`use-cases`, :doc:`comparison`

La liste des articles est également disponible sur la page :doc:`../guide`.

Références
==========

- `Documentation de Fess (version stable) <https://fess.codelibs.org/fr/stable/>`__
- `Configuration requise <https://fess.codelibs.org/fr/stable/install/prerequisites.html>`__
- `Plugins <https://fess.codelibs.org/fr/stable/admin/plugin-guide.html>`__
- `Architecture des plugins <https://fess.codelibs.org/fr/stable/dev/plugin-architecture.html>`__
- `Thème <https://fess.codelibs.org/fr/stable/admin/theme-guide.html>`__
- `Fichiers recherchables <https://fess.codelibs.org/fr/supported-files.html>`__
- `docker-fess (GitHub) <https://github.com/codelibs/docker-fess>`__
- `codelibs/fess (GitHub) <https://github.com/codelibs/fess>`__
