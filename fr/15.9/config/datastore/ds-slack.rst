==================================
Connecteur Slack
==================================

Aperçu
======

Le connecteur Slack fournit la fonctionnalité permettant de récupérer les messages
des canaux d'un espace de travail Slack et de les enregistrer dans l'index |Fess|.

Cette fonctionnalité nécessite le plugin ``fess-ds-slack``.

Contenu pris en charge
======================

- Messages des canaux publics
- Messages des canaux privés
- Messages de réponse dans les fils de discussion (récupérés via ``conversations.replies``)
- Fichiers joints (optionnel)

Les éléments suivants ne sont pas pris en charge :

- Les messages d'événements système (``channel_join``, ``channel_topic``, ``pinned_item``,
  etc.) sont exclus de l'indexation par défaut (``ignore_system_events``)
- Les messages directs (DM) et les DM de groupe
- Les transcriptions Huddle et les Clips (Slack ne propose pas d'API publique pour ceux-ci,
  ils ne peuvent donc pas être crawlés)

Prérequis
=========

1. L'installation du plugin est requise
2. La création et la configuration des permissions de l'application Slack sont nécessaires
3. L'obtention du OAuth Access Token est requise

Installation du plugin
----------------------

Installez depuis l'interface d'administration via "Système" -> "Plugins" :

1. Téléchargez ``fess-ds-slack-X.X.X.jar`` depuis Maven Central
2. Téléchargez et installez depuis l'interface de gestion des plugins
3. Redémarrez |Fess|

Ou consultez :doc:`../../admin/plugin-guide` pour plus de détails.

Configuration
=============

Configurez depuis l'interface d'administration via "Crawler" -> "Data Store" -> "Nouveau".

Configuration de base
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Élément
     - Exemple
   * - Nom
     - Company Slack
   * - Nom du gestionnaire
     - SlackDataStore
   * - Activé
     - Oui

Configuration des paramètres
----------------------------

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random
    file_crawl=false
    include_private=false

Liste des paramètres
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``token``
     - Oui
     - OAuth Access Token de l'application Slack
   * - ``channels``
     - Non
     - Canaux cibles du crawl (séparés par des virgules, ou ``*all``). Si non spécifié, tous les canaux sont récupérés (même comportement que ``*all``)
   * - ``file_crawl``
     - Non
     - Crawler également les fichiers (par défaut : ``false``)
   * - ``include_private``
     - Non
     - Inclure les canaux privés (par défaut : ``false``)
   * - ``number_of_threads``
     - Non
     - Nombre de threads de traitement parallèle (par défaut : ``1``)
   * - ``max_filesize``
     - Non
     - Taille maximale des fichiers en octets (par défaut : ``10000000``)
   * - ``ignore_error``
     - Non
     - Continuer le traitement en cas d'erreur (par défaut : ``true``)
   * - ``supported_mimetypes``
     - Non
     - Regex pour les types MIME autorisés (par défaut : ``.*``)
   * - ``include_pattern``
     - Non
     - Modèle regex pour les URLs à inclure
   * - ``exclude_pattern``
     - Non
     - Modèle regex pour les URLs à exclure
   * - ``proxy_host``
     - Non
     - Hôte du proxy HTTP
   * - ``proxy_port``
     - Non
     - Port du proxy HTTP (requis lorsque ``proxy_host`` est spécifié)
   * - ``file_types``
     - Non
     - Filtre de type de fichier pour l'API Slack (par défaut : ``all``)
   * - ``channel_count``
     - Non
     - Nombre de canaux par page API (par défaut : ``100``)
   * - ``message_count``
     - Non
     - Nombre de messages par page API (par défaut : ``100``)
   * - ``file_count``
     - Non
     - Nombre de fichiers par page API (par défaut : ``20``)
   * - ``user_count``
     - Non
     - Nombre d'utilisateurs par page API (par défaut : ``100``)
   * - ``user_cache_size``
     - Non
     - Nombre maximum d'entrées dans le cache des informations utilisateur (par défaut : ``10000``)
   * - ``bot_cache_size``
     - Non
     - Nombre maximum d'entrées dans le cache des informations bot (par défaut : ``10000``)
   * - ``channel_cache_size``
     - Non
     - Nombre maximum d'entrées dans le cache des informations de canal (par défaut : ``10000``)

Paramètres avancés
~~~~~~~~~~~~~~~~~~

Les paramètres suivants contrôlent le comportement de connexion et de nouvelle tentative, le
périmètre fin du crawl, ainsi que la synchronisation des permissions :

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Paramètre
     - Description
   * - ``connection_timeout``
     - Délai de connexion pour chaque requête à l'API Slack (millisecondes, par défaut : ``20000``)
   * - ``read_timeout``
     - Délai de lecture pour chaque requête à l'API Slack (millisecondes, par défaut : ``20000``)
   * - ``max_retry_count``
     - Nombre maximal de nouvelles tentatives après une réponse ``429`` (limite de débit) ou ``5xx`` (par défaut : ``3``)
   * - ``retry_interval``
     - Temps d'attente en millisecondes avant la première nouvelle tentative lorsque la réponse ne comporte pas d'en-tête ``Retry-After`` (par défaut : ``3000``). Double à chaque nouvelle tentative, plafonné à ``60000`` millisecondes. Si la réponse comporte un en-tête ``Retry-After``, cette valeur (en secondes) est utilisée à la place
   * - ``executor_timeout``
     - Secondes d'attente, à la fin d'un crawl, pour que les tâches restant en file d'attente se terminent avant de forcer l'arrêt (par défaut : ``60``)
   * - ``exclude_archived``
     - Détermine si les canaux archivés doivent être exclus des résultats de ``conversations.list`` (par défaut : ``false``). Avec ``true``, un canal archivé spécifié par son nom dans ``channels`` ne peut plus être résolu (voir Dépannage pour plus de détails)
   * - ``ignore_system_events``
     - Détermine si les messages d'administration de canal générés automatiquement par Slack (``channel_join``, ``channel_topic``, ``pinned_item``, etc.) doivent être exclus de l'indexation (par défaut : ``true``)
   * - ``read_interval``
     - Temps d'attente en millisecondes après le traitement de chaque message ou fichier (par défaut : ``0`` = pas d'attente). À utiliser pour ralentir le crawl face à un espace de travail fortement limité en débit
   * - ``max_content_length``
     - Nombre maximal de caractères que l'extracteur de contenu (Tika) peut extraire d'un fichier (par défaut : non défini, la limite par type MIME propre à |Fess| s'applique alors). ``max_filesize`` est la limite côté transfert qui rejette les fichiers selon leur taille avant le téléchargement, tandis que ``max_content_length`` est la limite côté extraction sur la quantité de texte extraite après le téléchargement ; les deux agissent indépendamment. Réduire ``max_filesize`` ne remplace pas ``max_content_length`` (par exemple, une archive de 1 Mo peut se développer en un texte bien plus volumineux une fois extraite)
   * - ``permission_sync``
     - Détermine si l'appartenance à un canal privé doit être convertie en permissions de recherche (rôles) (par défaut : ``false``). Voir « Synchronisation des permissions (ACL) » ci-dessous pour plus de détails
   * - ``default_permissions``
     - Permissions supplémentaires appliquées à tous les documents indexés, indépendamment de l'appartenance au canal (format ``{user}``/``{group}``/``{role}``, séparés par des virgules, par défaut : vide). Appliqué uniquement lorsque ``permission_sync`` est activé

.. note::

   ``ignore_system_events`` vaut ``true`` par défaut. Même une configuration de crawl existante
   qui ne définit pas ce paramètre cessera, après une mise à niveau de |Fess|, d'indexer les
   messages d'événements système tels que ``channel_join`` -- le nombre de documents indexés
   diminuera sans aucune erreur ni avertissement. Spécifiez explicitement
   ``ignore_system_events=false`` pour continuer à indexer ces messages comme auparavant.

Configuration du script
-----------------------

::

    title=message.user + " #" + message.channel
    digest=message.text + "\n" + message.attachments
    content=message.text
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

Champs disponibles
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``message.title``
     - Titre (chaîne vide pour les messages, nom et titre du fichier pour les entrées de fichier)
   * - ``message.text``
     - Contenu textuel du message (pour les entrées de fichier, le nom du fichier et le corps du fichier extrait)
   * - ``message.user``
     - Nom d'affichage de l'expéditeur du message (si non défini, résolu dans l'ordre du nom réel, du nom d'utilisateur, puis de l'identifiant utilisateur)
   * - ``message.channel``
     - Nom du canal où le message a été envoyé
   * - ``message.timestamp``
     - Date et heure d'envoi du message
   * - ``message.permalink``
     - Lien permanent du message
   * - ``message.attachments``
     - Informations de repli des fichiers joints
   * - ``message.roles``
     - Liste des permissions de recherche (rôles) autorisées à voir ce message ou ce fichier. Présent uniquement lorsque ``permission_sync=true``. Sauf si le script assigne ``role=message.roles``, les rôles calculés ne sont jamais répercutés dans le document indexé

Configuration de l'application Slack
====================================

1. Création de l'application Slack
----------------------------------

Accédez à https://api.slack.com/apps :

1. Cliquez sur "Create New App"
2. Sélectionnez "From scratch"
3. Entrez le nom de l'application (ex: Fess Crawler)
4. Sélectionnez l'espace de travail
5. Cliquez sur "Create App"

2. Configuration OAuth & Permissions
------------------------------------

Dans le menu "OAuth & Permissions" :

**Ajoutez les Bot Token Scopes suivants** :

Scopes de base (toujours requis) :

- ``channels:history`` - Lecture des messages des canaux publics
- ``channels:read`` - Lecture des informations des canaux publics
- ``users:read`` - Lecture des informations utilisateur (requis pour la résolution des noms d'affichage)
- ``team:read`` - Lecture des informations de l'espace de travail. ``team.info`` est appelé à
  chaque crawl, ce scope est donc requis ; sans lui, ce connecteur se rabat sur un appel
  supplémentaire à ``chat.getPermalink`` pour chaque message, ce qui augmente fortement le
  nombre d'appels à l'API

Pour inclure également les canaux privés (``include_private=true``) :

- ``groups:history`` - Lecture des messages des canaux privés
- ``groups:read`` - Lecture des informations des canaux privés

Pour crawler également les fichiers (``file_crawl=true``) :

- ``files:read`` - Lecture du contenu des fichiers

Pour synchroniser également les permissions des canaux privés (``permission_sync=true``) :

- ``users:read.email`` - Lecture des adresses e-mail des membres (requis pour la
  synchronisation des permissions)

3. Installation de l'application
--------------------------------

Dans le menu "Install App" :

1. Cliquez sur "Install to Workspace"
2. Vérifiez les permissions et cliquez sur "Autoriser"
3. Copiez le "Bot User OAuth Token" (commence par ``xoxb-``)

.. note::
   Normalement, utilisez le Bot User OAuth Token qui commence par ``xoxb-``,
   mais le User OAuth Token qui commence par ``xoxp-`` peut également être utilisé dans les paramètres.

4. Ajout aux canaux
-------------------

Ajoutez l'application aux canaux à crawler :

1. Ouvrez le canal dans Slack
2. Cliquez sur le nom du canal
3. Sélectionnez l'onglet "Intégrations"
4. Cliquez sur "Ajouter des applications"
5. Ajoutez l'application créée

Synchronisation des permissions (ACL)
=====================================

Le connecteur Slack peut convertir l'appartenance à un canal privé en permissions de recherche
(rôles) |Fess|, de sorte que seuls les membres de ce canal puissent en rechercher le contenu.
Cette fonctionnalité est désactivée par défaut.

.. note::

   ``permission_sync`` se contente de calculer les rôles ; il ne les applique pas
   automatiquement. Ce n'est qu'après avoir ajouté ``role=message.roles`` au script que les
   rôles calculés sont répercutés dans les documents indexés. Oublier ce mappage entraîne tout
   de même les appels API supplémentaires et les canaux privés ignorés que provoque
   ``permission_sync=true``, sans fournir le moindre contrôle d'accès.

Activation
----------

1. Ajoutez le scope ``users:read.email`` à l'application Slack (requis pour résoudre les
   adresses e-mail des membres)
2. Définissez ``permission_sync=true`` dans les paramètres
3. Ajoutez ``role=message.roles`` au script

Paramètres :

::

    include_private=true
    permission_sync=true

Script :

::

    role=message.roles

Comportement Fail-Closed
------------------------

Un canal privé n'est pas indexé du tout lors d'un crawl donné si l'un des cas suivants se
présente (il s'agit d'un comportement « fail-closed » : le risque est une sous-indexation,
jamais une exposition accidentelle du contenu à tout le monde) :

- La récupération de la liste des membres du canal a échoué
- La liste des membres est revenue vide (cela se produit lorsque l'utilisateur bot du token de
  crawl n'est lui-même pas membre de ce canal privé)
- Le canal a des membres, mais aucune de leurs adresses e-mail n'a pu être résolue (le plus
  souvent parce que le scope ``users:read.email`` est manquant)

Les canaux publics n'appellent jamais ``conversations.members`` et sont toujours considérés
comme visibles par tous.

Correspondance du nom de principal
----------------------------------

Les vérifications de permission au moment de la recherche utilisent le nom de connexion |Fess|
(le nom de principal). Étant donné que les rôles calculés par cette fonctionnalité sont dérivés
des adresses e-mail Slack, le nom de connexion |Fess| doit correspondre à l'adresse e-mail
Slack. Slack normalise les adresses e-mail en minuscules ; conservez donc également les noms de
connexion |Fess| en minuscules. Une incohérence n'expose pas le contenu d'un autre utilisateur
-- elle a simplement pour effet que les recherches de l'utilisateur concerné renvoient toujours
zéro résultat, ce qui peut facilement être confondu avec un bug sans rapport.

Autres remarques
----------------

- Les groupes d'utilisateurs (User Group) Slack ne sont pas utilisés ; les permissions sont
  calculées directement à partir de l'adresse e-mail de chaque membre
- ``default_permissions`` permet d'accorder des permissions supplémentaires à tous les
  documents, indépendamment de l'appartenance au canal (appliqué uniquement lorsque
  ``permission_sync=true``)
- Laisser ``permission_sync=false`` tout en définissant ``include_private=true`` indexe le
  contenu des canaux privés en utilisant uniquement les permissions configurées dans le champ
  « Permission » du Data Store ; si ce champ est laissé vide, le contenu devient de fait
  public pour tous
- Activer ``permission_sync`` ultérieurement ne sécurise pas rétroactivement le contenu déjà
  indexé par un crawl antérieur sans restriction. Pour appliquer des rôles à ce contenu,
  définissez ``permission_sync=true`` et ``role=message.roles``, puis relancez un crawl. De
  même, désactiver ``permission_sync`` par la suite ne supprime pas les rôles déjà appliqués
  aux documents indexés précédemment

Exemples d'utilisation
======================

Crawler des canaux spécifiques
------------------------------

Paramètres :

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random,tech-discussion
    file_crawl=false
    include_private=false

Script :

::

    title=message.user + " #" + message.channel
    digest=message.text + "\n" + message.attachments
    content=message.text
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

Crawler tous les canaux
-----------------------

Paramètres :

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    file_crawl=false
    include_private=false

Script :

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink

Crawler en incluant les canaux privés
-------------------------------------

Paramètres :

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    file_crawl=false
    include_private=true

Script :

::

    title=message.user + " #" + message.channel
    digest=message.text
    content=message.text + "\nPièce jointe : " + message.attachments
    created=message.timestamp
    url=message.permalink

Crawler en incluant les fichiers
--------------------------------

Paramètres :

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random
    file_crawl=true
    include_private=false

Script :

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink

Inclure des informations détaillées sur les messages
----------------------------------------------------

Script :

::

    title="[" + message.channel + "] " + message.user
    content=message.text
    digest=message.text.substring(0, Math.min(200, message.text.length()))
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

Crawler avec synchronisation des permissions
--------------------------------------------

Restreint le contenu des canaux privés de sorte que seuls les membres de ce canal puissent le
rechercher. Ajoutez au préalable le scope ``users:read.email`` à l'application Slack.

Paramètres :

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    include_private=true
    permission_sync=true

Script :

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink
    role=message.roles

.. note::
   Si vous oubliez ``role=message.roles``, les rôles calculés ne seront jamais répercutés dans
   les documents indexés. Voir « Synchronisation des permissions (ACL) » pour plus de détails.

Dépannage
=========

Fonctionnement de la gestion des erreurs
----------------------------------------

Le connecteur Slack classe les erreurs de l'API Slack en trois catégories :

- **Erreurs fatales**\ (``invalid_auth``, ``token_revoked``, ``account_inactive``,
  ``missing_scope``, ``not_authed``, ``token_expired``) : le token lui-même est inutilisable,
  ce qui fait échouer l'ensemble du job de crawl
- **Erreurs transitoires**\ (``ratelimited``, ``internal_error``, ``fatal_error``,
  ``service_unavailable``, ``request_timeout``) : si les nouvelles tentatives ne résolvent pas
  l'erreur, l'ensemble du job de crawl échoue (voir « Limitation de débit API » ci-dessous pour
  le comportement de nouvelle tentative)
- **Erreurs propres à un canal**\ (``channel_not_found``, ``not_in_channel``, etc.) : seul ce
  canal est ignoré avec un avertissement, et le crawl se poursuit avec le canal suivant

Dans les versions précédentes, une erreur fatale pouvait tout de même être rapportée comme un
crawl « réussi » qui indexait silencieusement zéro document, ou seulement une partie d'entre
eux. Cette répartition en trois catégories garantit désormais que les erreurs fatales et
transitoires sont toujours rapportées comme un échec du job.

Erreur d'authentification
-------------------------

**Symptôme** : ``invalid_auth`` ou ``not_authed``

**Points à vérifier** :

1. Vérifier si le token a été correctement copié
2. Vérifier le format du token :

   - Bot User OAuth Token : commence par ``xoxb-``
   - User OAuth Token : commence par ``xoxp-``

3. Vérifier si l'application est installée dans l'espace de travail
4. Vérifier si les permissions nécessaires sont accordées

Canal introuvable
-----------------

**Symptôme** : ``channel_not_found``

**Points à vérifier** :

1. Vérifier si le nom du canal est correct (# n'est pas nécessaire)
2. Vérifier si l'application a été ajoutée au canal
3. Pour les canaux privés, définir ``include_private=true``
4. Vérifiez si ``exclude_archived=true`` est défini. Par défaut (``exclude_archived=false``),
   les canaux archivés sont toujours listés et crawlés ; ce n'est que lorsqu'il est défini sur
   ``true`` qu'un canal archivé spécifié par son nom dans ``channels`` ne peut plus être résolu

Impossible de récupérer les messages
------------------------------------

**Symptôme** : Le crawl réussit, mais peu ou aucun document n'est indexé

**Points à vérifier** :

1. ``ignore_system_events`` vaut ``true`` par défaut. Si les messages d'un canal sont
   uniquement des événements système tels que ``channel_join``, aucun document n'est indexé
   pour ce canal (voir « Paramètres avancés »)
2. Vérifier si des messages existent réellement dans le canal
3. Vérifier si l'application a été ajoutée au canal
4. Avec ``permission_sync=true``, un canal privé dont l'appartenance ne peut pas être résolue
   n'est pas indexé lors de ce crawl (fail-closed ; voir « Synchronisation des permissions
   (ACL) »)

.. note::

   Dans les versions précédentes, un scope manquant (``missing_scope``) pouvait encore laisser
   le crawl « réussir » avec zéro message. Les erreurs fatales, y compris ``missing_scope``,
   font désormais échouer l'ensemble du job de crawl. Si votre job échoue, consultez plutôt
   « Erreur de permission insuffisante » ci-dessous.

Erreur de permission insuffisante
---------------------------------

**Symptôme** : ``missing_scope`` (fait échouer l'ensemble du job de crawl)

**Solution** :

1. Ajouter les scopes nécessaires dans les paramètres de l'application Slack :

   **Base**\ (toujours requis) :

   - ``channels:history``
   - ``channels:read``
   - ``users:read``
   - ``team:read``

   **Canaux privés** :

   - ``groups:history``
   - ``groups:read``

   **Fichiers** :

   - ``files:read``

   **Synchronisation des permissions**\ (``permission_sync=true``) :

   - ``users:read.email``

2. Réinstaller l'application
3. Redémarrer |Fess|

Impossible de crawler les fichiers
----------------------------------

**Symptôme** : Les fichiers ne sont pas récupérés même avec ``file_crawl=true``

**Points à vérifier** :

1. Vérifier si le scope ``files:read`` est accordé
2. Vérifier si des fichiers sont effectivement postés dans le canal
3. Vérifier les permissions d'accès aux fichiers
4. Un fichier dépassant ``max_filesize`` n'est pas téléchargé (vérifiez le log pour un
   avertissement)

Limitation de débit API
-----------------------

**Symptôme** : ``ratelimited`` (fait échouer l'ensemble du job de crawl)

**Solution** :

1. Si les valeurs par défaut de ``max_retry_count`` et ``retry_interval`` ne résolvent pas le
   problème, augmentez-les
2. Définissez ``read_interval`` pour ralentir le crawl
3. Réduisez le nombre de canaux, ou répartissez en plusieurs Data Store avec des
   planifications différentes

Une erreur ``ratelimited`` de l'API Slack est automatiquement réessayée : en utilisant la
valeur de l'en-tête ``Retry-After``, en secondes, lorsqu'elle est présente, ou sinon selon un
recul exponentiel à partir de ``retry_interval`` (jusqu'à ``max_retry_count`` tentatives,
plafonné à 60 secondes). Si la limitation de débit persiste après épuisement de toutes les
tentatives, l'ensemble du job de crawl échoue.

Niveaux (tiers) de l'API Slack (limites de fréquence d'appel) :

- Niveau 1 : 1+ requêtes/minute
- Niveau 2 : 20+ requêtes/minute -- ``conversations.list``, ``users.list`` (récupérées
  intégralement et inconditionnellement au début de chaque crawl, ce qui rend ce niveau le
  plus susceptible d'être épuisé)
- Niveau 3 : 50+ requêtes/minute -- ``conversations.history``, ``conversations.replies``,
  ``files.list``
- Niveau 4 : 100+ requêtes/minute -- ``conversations.members`` (uniquement lorsque
  ``permission_sync=true``), ``files.info`` (non appelé actuellement par le crawl de ce
  connecteur)

.. note::

   Le durcissement de la limitation de débit Slack du 29 mai 2025 (limitant
   ``conversations.history`` et ``conversations.replies`` à 50+ requêtes/minute) ne s'applique
   qu'aux applications distribuées en dehors de l'espace de travail qui les a créées, par
   exemple via le Slack Marketplace. Il ne s'applique pas à une application interne créée pour
   |Fess| et installée uniquement dans l'espace de travail qui l'a créée.

Cas de nombreux messages
------------------------

**Symptôme** : Le crawl prend du temps ou expire

**Solution** :

1. Diviser les canaux et configurer plusieurs Data Store
2. Répartir le calendrier de crawl

Exemples d'utilisation avancée des scripts
==========================================

Traitement des messages
-----------------------

Résumé des messages longs :

::

    title=message.user + " #" + message.channel
    content=message.text
    digest=message.text.length() > 100 ? message.text.substring(0, 100) + "..." : message.text
    created=message.timestamp
    url=message.permalink

Formatage du nom du canal :

::

    title="[Slack: " + message.channel + "] " + message.user
    content=message.text
    created=message.timestamp
    url=message.permalink

Informations de référence
=========================

- :doc:`ds-overview` - Aperçu des connecteurs Data Store
- :doc:`ds-atlassian` - Connecteur Atlassian
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- :doc:`../security-role` - Guide de configuration de la recherche basée sur les rôles
- `Slack API Documentation <https://api.slack.com/>`_
- `Slack Bot Token Scopes <https://api.slack.com/scopes>`_
- `Slack API Rate Limits <https://docs.slack.dev/apis/web-api/rate-limits>`_
