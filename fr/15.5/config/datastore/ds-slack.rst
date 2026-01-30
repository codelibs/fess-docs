==================================
Connecteur Slack
==================================

Apercu
====

Le connecteur Slack fournit la fonctionnalite permettant de recuperer les messages
des canaux d'un espace de travail Slack et de les enregistrer dans l'index |Fess|.

Cette fonctionnalite necessite le plugin ``fess-ds-slack``.

Contenu pris en charge
==============

- Messages des canaux publics
- Messages des canaux prives
- Fichiers joints (optionnel)

Prerequis
========

1. L'installation du plugin est requise
2. La creation et la configuration des permissions de l'application Slack sont necessaires
3. L'obtention du OAuth Access Token est requise

Installation du plugin
------------------------

Installez depuis l'interface d'administration via "Systeme" -> "Plugins" :

1. Telechargez ``fess-ds-slack-X.X.X.jar`` depuis Maven Central
2. Telechargez et installez depuis l'interface de gestion des plugins
3. Redemarrez |Fess|

Ou consultez :doc:`../../admin/plugin-guide` pour plus de details.

Configuration
========

Configurez depuis l'interface d'administration via "Crawler" -> "Data Store" -> "Nouveau".

Configuration de base
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Element
     - Exemple
   * - Nom
     - Company Slack
   * - Nom du gestionnaire
     - SlackDataStore
   * - Active
     - Oui

Configuration des parametres
----------------

::

    token=xoxp-123456789012-123456789012-123456789012-abc123def456ghi789jkl012mno345pq
    channels=general,random
    file_crawl=false
    include_private=false

Liste des parametres
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametre
     - Requis
     - Description
   * - ``token``
     - Oui
     - OAuth Access Token de l'application Slack
   * - ``channels``
     - Oui
     - Canaux cibles du crawl (separes par des virgules, ou ``*all``)
   * - ``file_crawl``
     - Non
     - Crawler egalement les fichiers (par defaut : ``false``)
   * - ``include_private``
     - Non
     - Inclure les canaux prives (par defaut : ``false``)

Configuration du script
--------------

::

    title=message.user + " #" + message.channel
    digest=message.text + "\n" + message.attachments
    content=message.text
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

Champs disponibles
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``message.text``
     - Contenu textuel du message
   * - ``message.user``
     - Nom d'affichage de l'expediteur
   * - ``message.channel``
     - Nom du canal ou le message a ete envoye
   * - ``message.timestamp``
     - Date et heure d'envoi du message
   * - ``message.permalink``
     - Lien permanent du message
   * - ``message.attachments``
     - Informations de fallback des fichiers joints

Configuration de l'application Slack
=============

1. Creation de l'application Slack
------------------

Accedez a https://api.slack.com/apps :

1. Cliquez sur "Create New App"
2. Selectionnez "From scratch"
3. Entrez le nom de l'application (ex: Fess Crawler)
4. Selectionnez l'espace de travail
5. Cliquez sur "Create App"

2. Configuration OAuth & Permissions
----------------------------

Dans le menu "OAuth & Permissions" :

**Ajoutez les Bot Token Scopes suivants** :

Pour les canaux publics uniquement :

- ``channels:history`` - Lecture des messages des canaux publics
- ``channels:read`` - Lecture des informations des canaux publics

Pour inclure les canaux prives (``include_private=true``) :

- ``channels:history``
- ``channels:read``
- ``groups:history`` - Lecture des messages des canaux prives
- ``groups:read`` - Lecture des informations des canaux prives

Pour crawler egalement les fichiers (``file_crawl=true``) :

- ``files:read`` - Lecture du contenu des fichiers

3. Installation de l'application
-----------------------

Dans le menu "Install App" :

1. Cliquez sur "Install to Workspace"
2. Verifiez les permissions et cliquez sur "Autoriser"
3. Copiez le "Bot User OAuth Token" (commence par ``xoxb-``)

.. note::
   Normalement, utilisez le Bot User OAuth Token qui commence par ``xoxb-``,
   mais le User OAuth Token qui commence par ``xoxp-`` peut egalement etre utilise dans les parametres.

4. Ajout aux canaux
---------------------

Ajoutez l'application aux canaux a crawler :

1. Ouvrez le canal dans Slack
2. Cliquez sur le nom du canal
3. Selectionnez l'onglet "Integrations"
4. Cliquez sur "Ajouter des applications"
5. Ajoutez l'application creee

Exemples d'utilisation
======

Crawler des canaux specifiques
--------------------------

Parametres :

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
----------------------------

Parametres :

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

Crawler en incluant les canaux prives
--------------------------------------

Parametres :

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    file_crawl=false
    include_private=true

Script :

::

    title=message.user + " #" + message.channel
    digest=message.text
    content=message.text + "\nPiece jointe: " + message.attachments
    created=message.timestamp
    url=message.permalink

Crawler en incluant les fichiers
------------------------

Parametres :

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

Inclure des informations detaillees sur les messages
----------------------------

Script :

::

    title="[" + message.channel + "] " + message.user
    content=message.text
    digest=message.text.substring(0, Math.min(200, message.text.length()))
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

Depannage
======================

Erreur d'authentification
----------

**Symptome** : ``invalid_auth`` ou ``not_authed``

**Points a verifier** :

1. Verifier si le token a ete correctement copie
2. Verifier le format du token :

   - Bot User OAuth Token : commence par ``xoxb-``
   - User OAuth Token : commence par ``xoxp-``

3. Verifier si l'application est installee dans l'espace de travail
4. Verifier si les permissions necessaires sont accordees

Canal introuvable
------------------------

**Symptome** : ``channel_not_found``

**Points a verifier** :

1. Verifier si le nom du canal est correct (# n'est pas necessaire)
2. Verifier si l'application a ete ajoutee au canal
3. Pour les canaux prives, definir ``include_private=true``
4. Verifier si le canal existe et n'est pas archive

Impossible de recuperer les messages
------------------------

**Symptome** : Le crawl reussit mais 0 messages

**Points a verifier** :

1. Verifier si les scopes necessaires sont accordes :

   - ``channels:history``
   - ``channels:read``
   - Pour les canaux prives : ``groups:history``, ``groups:read``

2. Verifier si des messages existent dans le canal
3. Verifier si l'application a ete ajoutee au canal
4. Verifier si l'application Slack est active

Erreur de permission insuffisante
--------------

**Symptome** : ``missing_scope``

**Solution** :

1. Ajouter les scopes necessaires dans les parametres de l'application Slack :

   **Canaux publics** :

   - ``channels:history``
   - ``channels:read``

   **Canaux prives** :

   - ``groups:history``
   - ``groups:read``

   **Fichiers** :

   - ``files:read``

2. Reinstaller l'application
3. Redemarrer |Fess|

Impossible de crawler les fichiers
--------------------------

**Symptome** : Les fichiers ne sont pas recuperes meme avec ``file_crawl=true``

**Points a verifier** :

1. Verifier si le scope ``files:read`` est accorde
2. Verifier si des fichiers sont effectivement postes dans le canal
3. Verifier les permissions d'acces aux fichiers

Limitation de debit API
-------------

**Symptome** : ``rate_limited``

**Solution** :

1. Augmenter l'intervalle de crawl
2. Reduire le nombre de canaux
3. Repartir en plusieurs data stores avec des planifications differentes

Limites de l'API Slack :

- Methodes Tier 3 : 50+ requetes/minute
- Methodes Tier 4 : 100+ requetes/minute

Cas de nombreux messages
--------------------------

**Symptome** : Le crawl prend du temps ou expire

**Solution** :

1. Diviser les canaux et configurer plusieurs data stores
2. Repartir le calendrier de crawl
3. Envisager une configuration pour exclure les anciens messages

Exemples d'utilisation avancee des scripts
========================

Filtrage des messages
--------------------------

Indexer uniquement les messages d'un utilisateur specifique :

::

    if (message.user == "Jean Dupont") {
        title=message.user + " #" + message.channel
        content=message.text
        created=message.timestamp
        url=message.permalink
    }

Uniquement les messages contenant des mots-cles :

::

    if (message.text.contains("important") || message.text.contains("incident")) {
        title="[Important] " + message.user + " #" + message.channel
        content=message.text
        created=message.timestamp
        url=message.permalink
    }

Traitement des messages
----------------

Resume des messages longs :

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

Informations de reference
========

- :doc:`ds-overview` - Apercu des connecteurs Data Store
- :doc:`ds-atlassian` - Connecteur Atlassian
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- `Slack API Documentation <https://api.slack.com/>`_
- `Slack Bot Token Scopes <https://api.slack.com/scopes>`_
