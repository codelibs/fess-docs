================================================
Déploiement en entreprise : check-list par étape
================================================

Introduction
============

Lorsque l'essai de Fess est concluant et que l'on décide de l'étendre à toute l'entreprise, la difficulté tient moins aux fonctionnalités elles-mêmes qu'à l'ordre dans lequel les mettre en place.
Certains réglages coûtent cher à reprendre s'ils sont repoussés à une étape ultérieure.
Par exemple, changer la clé de chiffrement après avoir enregistré des identifiants rend les valeurs stockées impossibles à déchiffrer, et modifier après coup les autorisations des documents impose une nouvelle exploration.

Cet article présente, étape par étape, l'ordre de déploiement de Fess 15.9 dans toute l'entreprise.
Pour chaque étape, il indique ce qu'il faut configurer, ce qu'il faut vérifier et les indicateurs qui permettent de décider si l'on peut passer à l'étape suivante.
Comme indicateurs, nous utilisons les rapports d'analyse de [Informations système] > [Journal de recherche] dans la console d'administration.
Les procédures propres à chaque fonctionnalité ne sont pas détaillées ici ; nous renvoyons aux articles qui les traitent.

Composants et articles de référence
===================================

Les composants concernés par un déploiement à l'échelle de l'entreprise, et les articles qui traitent chacun d'eux en détail, sont les suivants.

- Fess lui-même : fournit la page de recherche, la console d'administration, l'API et le planificateur. Vue d'ensemble dans :doc:`guide-01`, mémoire et montée en charge dans :doc:`guide-14`
- OpenSearch : stocke non seulement l'index des documents, mais aussi les configurations d'exploration, les utilisateurs, les journaux des tâches et les journaux de recherche. Séparation et mise en cluster dans :doc:`guide-14`, instantanés dans :doc:`guide-10`
- Processus enfants comme le robot d'exploration : l'exploration, la génération des suggestions, la génération des vignettes et le traitement des fragments s'exécutent, pour chaque tâche, dans une JVM distincte de celle de Fess. Réglages du tas dans :doc:`guide-14`
- Plugins : magasins de données (``fess-ds-*``), SSO (``fess-sso-*``), LLM et embeddings (``fess-llm-*``), MCP et recherche multimodale (``fess-webapp-*``), etc. Installez la même version mineure que Fess (15.9.x) et redémarrez Fess après chaque installation ou suppression. Pour en écrire un : :doc:`guide-17`
- LLM et modèles d'embedding (facultatif) : services externes, ou serveurs comme Ollama, utilisés par le mode de recherche IA et la recherche sémantique. Configuration dans :doc:`guide-18` et :doc:`guide-19`

Ce qui n'est pas stocké dans OpenSearch se gère séparément sur chaque serveur Fess.
Il s'agit de trois éléments : les paramètres de [Système] > [Général] (``system.properties``), ``fess_config.properties`` (y compris la clé de chiffrement ``app.cipher.key``) et les plugins installés.
Pour en conserver une copie, voir :doc:`guide-10` ; pour les gérer sous forme de code, voir :doc:`guide-16`.

Vue d'ensemble des étapes
=========================

.. list-table::
   :header-rows: 1
   :widths: 22 40 38

   * - Étape
     - Objectif
     - Passer à la suite lorsque
   * - 1. Essai
     - Faire chercher un petit nombre d'utilisateurs et savoir ce qu'ils cherchent
     - Les requêtes les plus fréquentes et les requêtes sans résultat sont consignées
   * - 2. Publier la première source
     - Publier une première source avec autorisations et poser les bases de l'exploitation
     - Les valeurs de référence du nombre d'utilisateurs et du taux de clics sont consignées
   * - 3. SSO et connexion
     - Faire se connecter avec l'identifiant de l'entreprise et adapter les résultats selon le groupe
     - Les groupes de l'IdP apparaissent dans « Recherches par rôle et par groupe »
   * - 4. Ajouter des sources
     - Ajouter des SaaS, du stockage cloud et des bases de données
     - Les requêtes sans résultat dues à des documents manquants disparaissent
   * - 5. Cycle d'amélioration de la qualité
     - Repérer les requêtes problématiques dans le journal de recherche et les corriger
     - Les indicateurs corrigés ne sont pas moins bons que sur la période précédente
   * - 6. Montée en charge et automatisation
     - Se préparer à l'augmentation des documents et des utilisateurs, et rendre l'environnement reproductible
     - Les temps de réponse de l'onglet [Performances] ne sont pas pires qu'avant la montée en charge, même avec plus d'utilisateurs
   * - 7. Fonctions d'IA
     - Ajouter le mode de recherche IA, la recherche sémantique et MCP
     - Les requêtes sont enregistrées dans l'onglet [Chat IA], et le taux d'erreur n'est pas plus élevé que juste après la mise en place

Chaque étape suppose les réglages des étapes précédentes.
En particulier, les étapes 2 et 3 comportent des réglages qui imposent une nouvelle exploration s'ils sont modifiés plus tard ; n'inversez donc pas leur ordre.

Étape 1 : essai
===============

Mettez en place un Fess d'évaluation et faites-le utiliser par quelques services.
L'objectif de cette étape est de recueillir, sous forme de journaux de recherche, ce que les utilisateurs cherchent.

**À configurer**

- En suivant :doc:`guide-02`, démarrez Fess avec les fichiers Compose du tag ``v15.9.0`` de docker-fess, et changez le mot de passe lors de la première connexion
- Créez une configuration d'exploration limitée à un seul site ou à un seul dossier
- Vérifiez que « Journal de recherche » et « Journal utilisateur » sont activés dans [Système] > [Général] (tous deux le sont par défaut). Si « Journal utilisateur » est désactivé, le nombre d'utilisateurs n'est pas comptabilisé

**À vérifier**

- Dans [Informations système] > [Journal des tâches], la tâche d'exploration se termine par « OK », et dans [Informations système] > [Informations sur l'exploration], le nombre de documents enregistrés n'est pas 0
- S'il y a peu de documents, consultez [Informations système] > [URL d'échec] (:doc:`guide-02`)

**Passer à la suite lorsque**

- L'onglet [Aperçu] de [Journal de recherche] affiche, pour la période d'essai, le nombre de recherches, le nombre d'utilisateurs, les requêtes les plus fréquentes et les requêtes sans résultat
- Cliquez sur les requêtes sans résultat, vérifiez les recherches réelles dans l'onglet [Journaux], puis, d'après le tableau de :doc:`guide-08`, classez les causes en « formulation différente », « orienter vers le terme officiel » et « aucun document »
- Les termes classés en « aucun document » sont des candidats pour les sources à ajouter aux étapes 2 et 4. Téléchargez le tableau en CSV et conservez-le

Étape 2 : publier la première source
====================================

Choisissez une source utilisée par l'ensemble des collaborateurs et publiez-la avec des autorisations.
En parallèle, mettez en place la supervision et les sauvegardes nécessaires à l'exploitation en production.

**À configurer**

- Fixez la clé de chiffrement ``app.cipher.key`` avant d'enregistrer des identifiants dans l'authentification Web, l'authentification de fichier ou les paramètres des magasins de données. Si vous la changez après, les valeurs stockées ne peuvent plus être déchiffrées (:doc:`guide-16`, :doc:`guide-10`)
- Créez les configurations d'exploration des sites Web et des dossiers partagés, l'authentification de fichier et les étiquettes (:doc:`guide-04`). Pour refléter les ACL d'un serveur de fichiers dans les résultats de recherche, voir :doc:`file-server-search`
- Définissez la conception des autorisations (:doc:`guide-05`). Les nouvelles configurations d'exploration et étiquettes contiennent l'autorisation ``{role}guest`` et sont donc, en l'état, visibles aussi des utilisateurs non connectés. Pour les documents réservés à certains services, supprimez cette valeur puis indiquez ``{group}`` ou équivalent
- Faites correspondre les noms de groupes saisis dans ``{group}`` aux noms qui arriveront de l'IdP à l'étape 3. Les renommer plus tard impose de réécrire les autorisations et de relancer l'exploration
- Si certaines configurations d'exploration sont exécutées par une tâche, par exemple une fois par semaine, réglez « Supprimer les anciens documents » de [Général] (3 jours par défaut) sur une durée plus longue que l'intervalle d'exploration (:doc:`guide-04`)
- Mettez en place la supervision, les notifications et les sauvegardes (:doc:`guide-10`). Appelez ``/api/v2/health`` depuis un outil de supervision externe, renseignez « E-mail de notification » ou « Slack Webhook URLs » dans [Général], et récupérez chaque jour le fichier de [Informations système] > [Sauvegarde] via l'API d'administration
- Avec Docker, les paramètres de [Général] sont enregistrés dans ``system.properties`` à l'intérieur du conteneur ``fess01`` et sont perdus lorsque ``down`` recrée le conteneur. Incluez-les dans vos sauvegardes ou passez-les via ``FESS_JAVA_OPTS`` (:doc:`guide-02`, :doc:`guide-16`)
- Si nécessaire, placez une zone de recherche sur le portail de l'entreprise (:doc:`guide-03`)

**À vérifier**

- Connectez-vous avec des utilisateurs de services différents : les documents visibles changent. Les autorisations enregistrées sur les documents réservés à un service ne contiennent plus le rôle guest initial (méthode de vérification dans :doc:`guide-05`)
- ``/api/v2/health`` renvoie 200, et [Envoyer un e-mail de test] dans [Général] fait bien arriver un e-mail
- Exécutez une fois le script de sauvegarde à la main et vérifiez que le fichier récupéré n'est pas vide (:doc:`guide-10`)

**Passer à la suite lorsque**

[Journal de recherche] ne renseigne pas sur l'état de la supervision et des sauvegardes de cette étape.
Jugez-en à l'aide de la rubrique « À vérifier » ci-dessus.
Dans le journal de recherche, relevez les valeurs de référence de l'utilisation après la publication.

- Dans l'onglet [Aperçu], relevez le nombre de recherches, le nombre d'utilisateurs, le taux de zéro résultat et le taux de clics pour la période postérieure à la publication, et conservez-les en CSV. Aux étapes suivantes, comparez-vous à ces valeurs avec « Comparer à la période précédente »
- Les URL de la source publiée figurent dans « URL les plus cliquées » de l'onglet [Clics]
- Si un nombre de jours est indiqué dans « Supprimer les anciens journaux de recherche » de [Général], les journaux plus anciens ne peuvent pas servir à la comparaison (la valeur par défaut ``-1`` ne supprime rien). Fixez une durée de conservation

Étape 3 : SSO et connexion
==========================

Faites se connecter les utilisateurs via le fournisseur d'identité (IdP) de l'entreprise, et adaptez les résultats de recherche selon les groupes de l'IdP.

Le SSO désigne ici les quatre méthodes fournies sous forme de plugins dans Fess 15.9.
Entra ID utilise ``fess-sso-entraid``, OpenID Connect ``fess-sso-oidc`` (« SSO Type » vaut ``oic``), SAML ``fess-sso-saml`` et SPNEGO ``fess-sso-spnego``.
Les images Docker contiennent les quatre, mais pas les images ``-slim``.
Avec les paquets ZIP, RPM et DEB, installez-les depuis [Système] > [Plugin] ou avec ``bin/fess-setup``.

LDAP n'est pas du SSO.
Les paramètres LDAP de [Général] vérifient l'identifiant et le mot de passe saisis sur la page de connexion de Fess auprès d'Active Directory ou d'un annuaire similaire, et récupèrent les groupes d'appartenance (:doc:`guide-05`).
SPNEGO s'appuie sur ces paramètres LDAP pour récupérer les groupes.

**À configurer**

- Installez le plugin, redémarrez Fess, puis renseignez « SSO Type » et les informations de l'IdP dans [Général]. L'URL de retour à enregistrer auprès de l'IdP est ``https://<hôte Fess>/sso/`` (:doc:`guide-15`)
- Si Fess est placé derrière un proxy inverse qui termine TLS, indiquez à Fess le schéma et le port externes (:doc:`guide-15`)
- Si les utilisateurs non connectés ne doivent pas pouvoir chercher, activez « Connexion requise » dans [Général]

« Connexion requise » ne s'applique pas qu'à la page de recherche.

- L'API de recherche ``/api/v2/`` renvoie 401 aux appels qui n'ont ni session de connexion ni jeton d'accès valide. Préparez des jetons pour les appels provenant des applications métier (:doc:`guide-11`)
- Avec la valeur par défaut ``mcp.auth.mode=none``, ``/mcp`` rejette les appels des agents IA avec HTTP 403. Si vous l'utilisez, passez à une authentification par jeton d'accès (:doc:`guide-20`)

**À vérifier**

- En ouvrant ``/sso/``, on peut se connecter via l'IdP, et les documents visibles par chaque service changent conformément à la conception de l'étape 2 (:doc:`guide-15`)
- Si Fess tourne sur plusieurs serveurs, les sessions persistantes (sticky sessions) sont activées sur le répartiteur de charge. En 15.9, les sessions de connexion sont conservées dans la mémoire de chaque Fess

**Passer à la suite lorsque**

- Dans « Recherches par rôle et par groupe » de l'onglet [Audience] de [Journal de recherche], les lignes des groupes transmis par l'IdP apparaissent sous la forme ``{group}<nom du groupe>``
- Si aucune ligne de groupe n'apparaît, soit les utilisateurs cherchent sans se connecter (ils sont comptés dans la ligne ``{role}guest``), soit les groupes ne parviennent pas à Fess
- Le nombre d'utilisateurs de l'onglet [Aperçu] n'a pas fortement baissé par rapport à la valeur de référence de l'étape 2. Vérifiez avec la colonne « Utilisateurs » de « Recherches par rôle et par groupe » qu'aucun service n'a cessé d'utiliser la recherche à cause de l'introduction de la connexion

Étape 4 : ajouter des sources
=============================

Ajoutez, au moyen de plugins de magasin de données, des sources autres que les sites Web et les serveurs de fichiers.
Les étapes communes à toutes les sources (installation du plugin, paramètres et scripts, autorisations, tâches, vérification des résultats) sont réunies dans :doc:`datastore-basics`.
Lisez-le en premier.

**À configurer**

- Installez le plugin de chaque source et redémarrez

  - Git, Confluence/Jira, Slack : ``fess-ds-git``, ``fess-ds-atlassian``, ``fess-ds-slack`` (:doc:`guide-06`)
  - Google Drive, SharePoint/OneDrive, Box : ``fess-ds-gsuite``, ``fess-ds-microsoft365``, ``fess-ds-box`` (:doc:`guide-07`)
  - Bases de données, CSV, Salesforce : ``fess-ds-db``, ``fess-ds-csv``, ``fess-ds-salesforce`` (:doc:`guide-12`)
  - Pour une source sans plugin adapté, écrivez votre propre plugin (:doc:`guide-17`)

- Les configurations de magasin de données contiennent elles aussi ``{role}guest``. Pour chaque configuration, décidez s'il faut reprendre les autorisations de la source ou les écrire avec les entrées ``{group}`` de l'étape 2
- Avec [Créer une nouvelle tâche], donnez à chaque configuration sa propre tâche, afin de gérer source par source les limites de débit des API et l'expiration des identifiants
- Attribuez une étiquette à chaque source pour pouvoir filtrer sur la page de recherche. Les configurations de magasin de données n'ont pas de champ d'étiquette : attribuez-les par script ou via « Chemins inclus » de l'étiquette (:doc:`datastore-basics`)

**À vérifier**

- Une tâche de magasin de données peut se terminer par « OK » même si une erreur survient dans le connecteur. Vérifiez ensemble « Taille de l'index (Magasin de données) » dans [Informations sur l'exploration], [URL d'échec] et ``fess-crawler.log`` (:doc:`datastore-basics`)
- Pour les sources dont les autorisations sont reprises, cherchez avec des utilisateurs aux droits différents : les documents visibles changent

**Passer à la suite lorsque**

- Les requêtes sans résultat classées en « aucun document » aux étapes 1 et 2 disparaissent des requêtes sans résultat de l'onglet [Requêtes] pour la période qui suit l'ajout de la source
- Des documents des sources ajoutées apparaissent dans « URL les plus cliquées » de l'onglet [Clics]. Une source qui n'apparaît pas n'est soit pas recherchée, soit pas classée en haut des résultats. Le second cas est traité à l'étape 5

Étape 5 : cycle d'amélioration de la qualité
============================================

Une fois les sources en place, consultez régulièrement le journal de recherche et corrigez les requêtes problématiques.
Le choix de la correction et la procédure pour l'appliquer sont traités dans :doc:`guide-08`.

**À configurer**

- Utilisez des synonymes ou des requêtes associées pour les requêtes sans résultat, et la correspondance de clé ou le boost de document pour les documents enfouis en bas des résultats (:doc:`guide-08`). Après avoir modifié le dictionnaire de synonymes, rechargez l'index des documents dans [Informations système] > [Maintenance]
- Si des documents mêlant japonais, anglais et chinois sont mal trouvés, vérifiez les champs et dictionnaires propres à chaque langue (:doc:`guide-09`)
- Si vous avez besoin d'agrégations absentes des rapports intégrés (URL ouvertes par requête, requêtes sans résultat par rôle, évolution mensuelle sur une longue période, etc.), utilisez OpenSearch Dashboards (:doc:`guide-22`)
- Pour gérer les dictionnaires et les réglages de correspondance de clé sous forme de code, voir :doc:`guide-16`

**À vérifier**

- Recherchez les termes corrigés depuis la page de recherche : les documents visés sont trouvés ou apparaissent en haut
- Pour la correspondance de clé, le document ciblé s'affiche dans le champ « URL » de la page de détails (:doc:`guide-08`)

**Passer à la suite lorsque**

Cette étape n'a pas de fin : elle se répète.
Vérifiez l'effet de chaque amélioration de la façon suivante.

- Réglez la période sur « Personnalisée » à partir du lendemain de la modification, et activez « Comparer à la période précédente »
- Si vous avez corrigé des requêtes sans résultat, regardez le taux de zéro résultat de l'onglet [Aperçu] et les requêtes sans résultat de l'onglet [Requêtes] ; si vous avez corrigé un classement, regardez la position moyenne des clics de l'onglet [Requêtes] et la répartition des positions de clic de l'onglet [Clics]
- Si les termes corrigés ont disparu de la liste et que les indicateurs globaux ne sont pas moins bons que sur la période précédente, conservez la modification

Étape 6 : montée en charge et automatisation
============================================

Lorsque les documents et les utilisateurs augmentent, identifiez ce qui manque avant d'agrandir.
Faites aussi en sorte de pouvoir reconstruire le même environnement.

**À configurer**

- Identifiez ce qui manque à partir des symptômes (:doc:`guide-14`). Un OutOfMemoryError dans ``fess-crawler.log`` traduit un manque de mémoire de la JVM du robot d'exploration (``jvm.crawler.options``) ; augmenter le tas de Fess lui-même (``FESS_HEAP_SIZE``) n'y change rien
- Envisagez, dans cet ordre : placer OpenSearch sur un serveur séparé, en faire un cluster de trois nœuds, puis faire tourner Fess sur plusieurs serveurs (:doc:`guide-14`)
- Avec plusieurs serveurs Fess, confiez l'exploration à un seul. Réglez à la fois ``scheduler.target.name`` et « Cible » dans [Système] > [Planificateur] (:doc:`guide-14`)
- Avec plusieurs serveurs, gardez ``app.cipher.key``, ``fess_config.properties``, les paramètres de [Général] et les plugins identiques sur tous les serveurs
- Figez le tag de l'image Docker et les versions des plugins, et rendez les paramètres applicables avec fessctl et l'API d'administration (:doc:`guide-16`)
- Pour partager un même Fess entre plusieurs organisations, combinez hôtes virtuels et rôles. Les hôtes virtuels seuls ne constituent pas un contrôle d'accès (:doc:`guide-13`)

**À vérifier**

- Avant et après la montée en charge, comparez le taux d'utilisation du tas fourni par ``/api/admin/stats`` et la durée d'exploration dans [Informations système] > [Journal des tâches] (:doc:`guide-10`)
- Avec plusieurs serveurs, les résultats de recherche sont identiques quel que soit le serveur ouvert, et l'exploration ne s'exécute que sur le serveur désigné. Cliquer sur [Démarrer maintenant] sur un autre serveur ne lance pas l'exploration (:doc:`guide-14`)
- Les paramètres peuvent être restaurés depuis une sauvegarde dans un environnement reconstruit (:doc:`guide-10`)

**Passer à la suite lorsque**

- Dans l'onglet [Performances] de [Journal de recherche], la médiane, le p95 et le p99 du temps de réponse sont plus bas qu'avant la montée en charge, ou n'ont pas augmenté malgré la hausse du nombre d'utilisateurs
- Recherchez les termes listés dans « Requêtes les plus lentes » pour distinguer si seuls certains termes sont lents ou si tout est lent

Notez que la possibilité d'enregistrer les sessions de connexion dans OpenSearch et de les partager entre plusieurs serveurs est disponible à partir de 15.10.
En 15.9, fonctionnez avec les sessions persistantes mentionnées plus haut.

Étape 7 : fonctions d'IA
========================

Chaque fonction d'IA demande une préparation différente.
Ajoutez d'abord celles qui correspondent à vos objectifs.

**Mode de recherche IA (RAG)**

- Un LLM répond aux questions des utilisateurs en s'appuyant sur les documents internes (:doc:`guide-19`)
- La recherche vectorielle n'est pas nécessaire. Les documents justificatifs sont rassemblés par une recherche ordinaire : les autorisations des étapes 2 et 3 s'appliquent telles quelles, et les documents qu'un utilisateur ne peut pas voir ne servent pas à la réponse
- Trois éléments sont nécessaires : ``rag.chat.enabled=true`` dans ``fess_config.properties`` (la valeur par défaut est ``false``, et la console d'administration n'a pas d'option correspondante), un plugin ``fess-llm-*``, et « Fournisseur LLM » dans [Général]
- Vous pouvez restreindre les utilisateurs autorisés avec « Autorisations du chat » dans [Général]

**Recherche sémantique et recherche multimodale**

- La recherche sémantique trouve des documents de sens proche même quand les mots-clés ne correspondent pas (:doc:`guide-18`). Le fournisseur d'embeddings se choisit avec ``content_chunker.embedding.name``. La valeur par défaut ``opensearch`` utilise un modèle de ML Commons d'OpenSearch, tandis que ``ollama``, ``openai``, ``gemini`` et ``bedrock`` nécessitent le plugin ``fess-llm-*`` correspondant
- Pour l'activer sur un environnement existant, recréez l'index puis générez les vecteurs de tous les documents. Avec des modèles facturés à l'usage comme OpenAI, le premier traitement entraîne des frais pour l'ensemble des documents
- La recherche multimodale utilise le plugin ``fess-webapp-multimodal`` et un serveur CLIP pour trouver des images à partir de texte (:doc:`guide-21`)
- Ces deux fonctions ne peuvent pas être utilisées en même temps sur un même Fess. Si vous avez besoin des deux, construisez des Fess distincts

**MCP**

- Permet à des agents IA de faire des recherches dans Fess (:doc:`guide-20`). L'installation du plugin ``fess-webapp-mcp`` rend ``/mcp`` disponible
- Avec la valeur par défaut ``mcp.auth.mode=none``, toute personne qui peut atteindre ``/mcp`` peut chercher en tant qu'invité. Avant de l'ouvrir dans l'entreprise, passez à une authentification par jeton d'accès ou équivalent

**À vérifier**

- Mode de recherche IA : posez une question avec [Recherche IA] sur la page de recherche ; la réponse et ses sources s'affichent. Pour des utilisateurs aux droits différents, les documents qu'ils ne peuvent pas voir n'apparaissent pas parmi les sources (:doc:`guide-19`)
- Recherche sémantique et recherche multimodale : des vecteurs sont écrits dans les documents, et la réponse de l'API de recherche montre que la recherche vectorielle est utilisée (:doc:`guide-18`, :doc:`guide-21`)
- MCP : après la modification du réglage d'authentification, les appels sans jeton sont rejetés (:doc:`guide-20`)

**Passer à la suite lorsque**

- Pour le mode de recherche IA, regardez dans l'onglet [Chat IA] de [Journal de recherche] le nombre de requêtes, le nombre d'utilisateurs, le taux d'erreur et le temps de réponse moyen. Le nombre de jetons n'est enregistré que si le plugin LLM le communique, et le contenu des questions et des réponses n'est pas enregistré
- Pour la recherche sémantique, activez « Comparer à la période précédente » sur une période commençant le lendemain de la mise en place, et comparez le taux de zéro résultat, le taux de clics et les temps de réponse de l'onglet [Performances]
- MCP et la recherche multimodale n'ont pas d'indicateur dédié dans [Journal de recherche]. Jugez-en à l'aide de la rubrique « À vérifier » ci-dessus et des retours des services utilisateurs

Pour aller plus loin
====================

- Commencer l'essai : :doc:`guide-02`
- Publier la première source avec autorisations : :doc:`guide-04`, :doc:`guide-05`, :doc:`file-server-search`
- Supervision et sauvegardes : :doc:`guide-10`
- SSO : :doc:`guide-15`
- Ajouter des sources : :doc:`datastore-basics`
- Améliorer la qualité avec le journal de recherche : :doc:`guide-08`
- Montée en charge et configuration sous forme de code : :doc:`guide-14`, :doc:`guide-16`
- Fonctions d'IA : :doc:`guide-19`, :doc:`guide-18`, :doc:`guide-20`

Références
==========

- `Journal de recherche <https://fess.codelibs.org/fr/stable/admin/searchlog-guide.html>`__
- `Général <https://fess.codelibs.org/fr/stable/admin/general-guide.html>`__
- `Plugins <https://fess.codelibs.org/fr/stable/admin/plugin-guide.html>`__
- `Configuration requise <https://fess.codelibs.org/fr/stable/install/prerequisites.html>`__
- `Forum de discussion Fess <https://discuss.codelibs.org/c/FessEN/>`__
