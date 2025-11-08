=========================================
Installation sur Windows (Procédure détaillée)
=========================================

Cette page décrit la procédure d'installation de |Fess| sur un environnement Windows.
Elle documente la méthode d'installation à l'aide du package ZIP.

.. warning::

   Pour les environnements de production, nous ne recommandons pas l'utilisation d'OpenSearch intégré.
   Veuillez obligatoirement configurer un serveur OpenSearch externe.

Prérequis
=========

- La configuration requise décrite dans :doc:`prerequisites` doit être satisfaite
- Java 21 doit être installé
- OpenSearch 3.3.0 doit être disponible (ou nouvelle installation)
- La variable d'environnement Windows ``JAVA_HOME`` doit être configurée de manière appropriée

Vérification de l'installation de Java
=======================================

Ouvrez l'invite de commandes ou PowerShell et vérifiez la version de Java avec la commande suivante.

Invite de commandes ::

    C:\> java -version

PowerShell ::

    PS C:\> java -version

Vérifiez que Java 21 ou ultérieur est affiché.

Configuration des variables d'environnement
============================================

1. Configuration de la variable d'environnement ``JAVA_HOME``

   Configurez le répertoire d'installation de Java comme ``JAVA_HOME``.

   Exemple ::

       JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-21.0.1.12-hotspot

2. Ajout à la variable d'environnement ``PATH``

   Ajoutez ``%JAVA_HOME%\bin`` à la variable d'environnement ``PATH``.

.. tip::

   Méthode de configuration des variables d'environnement :

   1. Ouvrir les « Paramètres » depuis le menu « Démarrer »
   2. Cliquer sur « Système » → « Informations système » → « Paramètres système avancés »
   3. Cliquer sur le bouton « Variables d'environnement »
   4. Configurer dans « Variables système » ou « Variables utilisateur »

Étape 1 : Installation d'OpenSearch
====================================

Téléchargement d'OpenSearch
----------------------------

1. Téléchargez le package ZIP pour Windows depuis `Download OpenSearch <https://opensearch.org/downloads.html>`__.

2. Décompressez le fichier ZIP téléchargé dans un répertoire arbitraire.

   Exemple ::

       C:\opensearch-3.3.0

   .. note::

      Nous recommandons de choisir un répertoire dont le chemin ne contient pas de caractères japonais ou d'espaces.

Installation des plugins OpenSearch
------------------------------------

Ouvrez l'invite de commandes **avec des privilèges d'administrateur** et exécutez les commandes suivantes.

::

    C:\> cd C:\opensearch-3.3.0
    C:\opensearch-3.3.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.0
    C:\opensearch-3.3.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.0
    C:\opensearch-3.3.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.0
    C:\opensearch-3.3.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.0

.. important::

   Les versions des plugins doivent correspondre à la version d'OpenSearch.
   Dans l'exemple ci-dessus, toutes sont spécifiées en 3.3.0.

Configuration d'OpenSearch
---------------------------

Ouvrez ``config\opensearch.yml`` avec un éditeur de texte et ajoutez les paramètres suivants.

::

    # Chemin pour la synchronisation de configuration (spécifier en chemin absolu)
    configsync.config_path: C:/opensearch-3.3.0/data/config/

    # Désactivation du plugin de sécurité (environnement de développement uniquement)
    plugins.security.disabled: true

.. warning::

   **Note importante sur la sécurité**

   ``plugins.security.disabled: true`` ne doit être utilisé que dans les environnements de développement ou de test.
   Pour les environnements de production, veuillez activer le plugin de sécurité d'OpenSearch et configurer une authentification et une autorisation appropriées.
   Pour plus de détails, consultez :doc:`security`.

.. note::

   Sous Windows, utilisez ``/`` plutôt que ``\`` comme séparateur de chemin.
   Écrivez ``C:/opensearch-3.3.0/data/config/`` plutôt que ``C:\opensearch-3.3.0\data\config\``.

.. tip::

   Autres paramètres recommandés ::

       cluster.name: fess-cluster
       node.name: fess-node-1
       network.host: 0.0.0.0
       discovery.type: single-node

Étape 2 : Installation de Fess
===============================

Téléchargement de Fess
-----------------------

1. Téléchargez le package ZIP pour Windows depuis le `site de téléchargement <https://fess.codelibs.org/ja/downloads.html>`__.

2. Décompressez le fichier ZIP téléchargé dans un répertoire arbitraire.

   Exemple ::

       C:\fess-15.3.0

   .. note::

      Nous recommandons de choisir un répertoire dont le chemin ne contient pas de caractères japonais ou d'espaces.

Configuration de Fess
----------------------

Ouvrez ``bin\fess.in.bat`` avec un éditeur de texte et ajoutez ou modifiez les paramètres suivants.

::

    set SEARCH_ENGINE_HTTP_URL=http://localhost:9200
    set FESS_DICTIONARY_PATH=C:/opensearch-3.3.0/data/config/

.. note::

   - Si vous exécutez OpenSearch sur un autre hôte, modifiez ``SEARCH_ENGINE_HTTP_URL`` avec le nom d'hôte ou l'adresse IP appropriés.
   - Utilisez ``/`` comme séparateur de chemin.

Vérification de l'installation
-------------------------------

Vérifiez que les fichiers de configuration ont été correctement modifiés.

Invite de commandes ::

    C:\> findstr "SEARCH_ENGINE_HTTP_URL" C:\fess-15.3.0\bin\fess.in.bat
    C:\> findstr "FESS_DICTIONARY_PATH" C:\fess-15.3.0\bin\fess.in.bat

Étape 3 : Démarrage
====================

Pour la procédure de démarrage, consultez :doc:`run`.

Enregistrement en tant que service Windows (optionnel)
=======================================================

En enregistrant |Fess| et OpenSearch en tant que services Windows, vous pouvez les configurer pour qu'ils démarrent automatiquement au démarrage du système.

.. note::

   Pour l'enregistrement en tant que service Windows, vous devez utiliser un outil tiers (tel que NSSM).
   Pour les procédures détaillées, consultez la documentation de chaque outil.

Exemple d'utilisation de NSSM
------------------------------

1. Téléchargez et décompressez `NSSM (Non-Sucking Service Manager) <https://nssm.cc/download>`__.

2. Enregistrement d'OpenSearch en tant que service ::

       C:\> nssm install OpenSearch C:\opensearch-3.3.0\bin\opensearch.bat

3. Enregistrement de Fess en tant que service ::

       C:\> nssm install Fess C:\fess-15.3.0\bin\fess.bat

4. Configuration des dépendances de service (Fess dépend d'OpenSearch) ::

       C:\> sc config Fess depend= OpenSearch

5. Démarrage des services ::

       C:\> net start OpenSearch
       C:\> net start Fess

Configuration du pare-feu
==========================

Ouvrez les ports nécessaires dans le Pare-feu Windows Defender.

1. Ouvrez « Panneau de configuration » → « Pare-feu Windows Defender » → « Paramètres avancés »

2. Créez une nouvelle règle dans « Règles de trafic entrant »

   - Type de règle : Port
   - Protocole et port : TCP, 8080
   - Action : Autoriser la connexion
   - Nom : Fess Web Interface

Ou exécutez dans PowerShell ::

    PS C:\> New-NetFirewallRule -DisplayName "Fess Web Interface" -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow

Dépannage
=========

Conflit de numéros de port
---------------------------

Si les ports 8080 ou 9200 sont déjà utilisés, vous pouvez le vérifier avec la commande suivante ::

    C:\> netstat -ano | findstr :8080
    C:\> netstat -ano | findstr :9200

Modifiez le numéro de port utilisé ou arrêtez le processus en conflit.

Limitation de la longueur des chemins
--------------------------------------

Sous Windows, il existe une limitation de la longueur des chemins. Nous recommandons d'installer dans un chemin aussi court que possible.

Exemple ::

    C:\opensearch  (recommandé)
    C:\Program Files\opensearch-3.3.0  (non recommandé - chemin trop long)

Java n'est pas reconnu
-----------------------

Si une erreur s'affiche avec la commande ``java -version`` :

1. Vérifiez que la variable d'environnement ``JAVA_HOME`` est correctement configurée
2. Vérifiez que ``%JAVA_HOME%\bin`` est inclus dans la variable d'environnement ``PATH``
3. Redémarrez l'invite de commandes pour appliquer les paramètres

Étapes suivantes
================

Une fois l'installation terminée, consultez les documents suivants :

- :doc:`run` - Démarrage de |Fess| et configuration initiale
- :doc:`security` - Configuration de la sécurité pour les environnements de production
- :doc:`troubleshooting` - Dépannage

Questions fréquemment posées
=============================

Q : L'exploitation sur Windows Server est-elle recommandée ?
-------------------------------------------------------------

R : Oui, l'exploitation sur Windows Server est possible.
Lors de l'exploitation sur Windows Server, enregistrez-le en tant que service Windows et configurez une surveillance appropriée.

Q : Quelle est la différence entre les versions 64 bits et 32 bits ?
---------------------------------------------------------------------

R : |Fess| et OpenSearch ne prennent en charge que la version 64 bits.
Ils ne fonctionnent pas sur Windows 32 bits.

Q : Comment gérer les chemins contenant des caractères japonais ?
------------------------------------------------------------------

R : Dans la mesure du possible, veuillez installer dans un chemin ne contenant pas de caractères japonais ou d'espaces.
Si vous devez absolument utiliser un chemin japonais, vous devez échapper correctement le chemin dans les fichiers de configuration.
