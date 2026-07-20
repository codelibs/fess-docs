==========================================
Démarrage, arrêt et configuration initiale
==========================================

Cette page décrit les procédures de démarrage, d'arrêt et de configuration initiale du serveur |Fess|.

.. important::

   Avant de démarrer |Fess|, veuillez obligatoirement démarrer OpenSearch.
   Si OpenSearch n'est pas démarré, |Fess| ne fonctionnera pas correctement.

Méthodes de démarrage
=====================

Les procédures de démarrage diffèrent selon la méthode d'installation.

Version TAR.GZ
--------------

Démarrage d'OpenSearch
~~~~~~~~~~~~~~~~~~~~~~

::

    $ cd /path/to/opensearch-3.7.0
    $ ./bin/opensearch

Pour un démarrage en arrière-plan ::

    $ ./bin/opensearch -d

Démarrage de Fess
~~~~~~~~~~~~~~~~~

::

    $ cd /path/to/fess-15.8.0
    $ ./bin/fess

Pour un démarrage en arrière-plan ::

    $ ./bin/fess -d

.. note::

   Le démarrage peut prendre quelques minutes.
   Vous pouvez vérifier l'état du démarrage dans le fichier de log (``logs/fess.log``).

Version ZIP (Windows)
---------------------

Démarrage d'OpenSearch
~~~~~~~~~~~~~~~~~~~~~~

1. Ouvrez le répertoire d'installation d'OpenSearch
2. Double-cliquez sur ``opensearch.bat`` dans le dossier ``bin``

Ou depuis l'invite de commandes ::

    C:\> cd C:\opensearch-3.7.0
    C:\opensearch-3.7.0> bin\opensearch.bat

Démarrage de Fess
~~~~~~~~~~~~~~~~~

1. Ouvrez le répertoire d'installation de Fess
2. Double-cliquez sur ``fess.bat`` dans le dossier ``bin``

Ou depuis l'invite de commandes ::

    C:\> cd C:\fess-15.8.0
    C:\fess-15.8.0> bin\fess.bat

Version RPM/DEB (chkconfig)
---------------------------

Démarrage d'OpenSearch ::

    $ sudo service opensearch start

Démarrage de Fess ::

    $ sudo service fess start

Vérification de l'état de démarrage ::

    $ sudo service fess status

Version RPM/DEB (systemd)
-------------------------

Démarrage d'OpenSearch ::

    $ sudo systemctl start opensearch.service

Démarrage de Fess ::

    $ sudo systemctl start fess.service

Vérification de l'état de démarrage ::

    $ sudo systemctl status fess.service

Activation du démarrage automatique du service ::

    $ sudo systemctl enable opensearch.service
    $ sudo systemctl enable fess.service

Version Docker
--------------

.. note::

   ``compose.yaml`` et ``compose-opensearch3.yaml`` ne sont pas inclus dans |Fess| lui-même. Ils sont fournis par le projet docker-fess (https://github.com/codelibs/docker-fess) ; récupérez le dépôt et exécutez les commandes suivantes dans le répertoire ``compose``.

Démarrage avec Docker Compose ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Vérification de l'état de démarrage ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

Vérification des logs ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

Vérification du démarrage
==========================

Vérifiez que |Fess| a démarré normalement.

Vérification de l'état de santé
--------------------------------

Accédez à l'URL suivante via un navigateur ou la commande curl ::

    http://localhost:8080/

Si le démarrage est normal, l'écran de recherche de Fess s'affiche.

Vérification en ligne de commande ::

    $ curl -I http://localhost:8080/

Si ``HTTP/1.1 200 OK`` est retourné, le démarrage est normal.

Vérification des logs
----------------------

Vérifiez les logs de démarrage pour confirmer qu'il n'y a pas d'erreurs.

Version TAR.GZ/ZIP ::

    $ tail -f /path/to/fess-15.8.0/logs/fess.log

Version RPM/DEB ::

    $ sudo tail -f /var/log/fess/fess.log

Ou en utilisant journalctl ::

    $ sudo journalctl -u fess.service -f

Version Docker ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

.. tip::

   Lorsque le démarrage se termine avec succès, un message de fin de démarrage comme celui-ci s'affiche sur la console et dans les logs :

   ::

       ...Booting the Tomcat: port=8080 contextPath=/
       ...
       Boot successful: url -> http://localhost:8080

Accès via un navigateur
========================

Accédez aux URL suivantes pour vérifier l'interface Web.

Écran de recherche
------------------

**URL** : http://localhost:8080/

L'écran de recherche de Fess s'affiche. Dans l'état initial, aucun résultat de recherche ne s'affiche car aucune configuration d'exploration n'a été effectuée.

Écran d'administration
-----------------------

**URL** : http://localhost:8080/admin

Compte administrateur par défaut :

- **Nom d'utilisateur** : ``admin``
- **Mot de passe** : ``admin``

.. warning::

   **Note importante sur la sécurité**

   Veuillez obligatoirement changer le mot de passe par défaut.
   En particulier dans les environnements de production, il est fortement recommandé de changer le mot de passe immédiatement après la première connexion.

Configuration initiale
======================

Après vous être connecté à l'écran d'administration, effectuez les configurations initiales suivantes.

Étape 1 : Modification du mot de passe administrateur
------------------------------------------------------

1. Connexion à l'écran d'administration (http://localhost:8080/admin)
2. Cliquez sur « Système » → « Utilisateur » dans le menu de gauche
3. Cliquez sur l'utilisateur ``admin``
4. Saisissez un nouveau mot de passe dans le champ [Mot de passe]
5. Saisissez à nouveau le même mot de passe dans le champ [Mot de passe (confirmer)]
6. Cliquez sur le bouton [Mettre à jour]

.. important::

   Nous recommandons que le mot de passe satisfasse les conditions suivantes :

   - 8 caractères ou plus (longueur minimale requise définie par ``password.min.length``)
   - Combinaison de majuscules, minuscules, chiffres et symboles
   - Difficile à deviner

   Par défaut, seule la longueur minimale (8 caractères) est requise ; aucune combinaison de types de caractères n'est imposée. Les exigences relatives aux types de caractères peuvent être activées avec des paramètres tels que ``password.require.uppercase``.

Étape 2 : Création de la configuration d'exploration
-----------------------------------------------------

Créez une configuration pour explorer les sites ou systèmes de fichiers à rechercher.

1. Cliquez sur « Explorateur » → « Web » dans le menu de gauche
2. Cliquez sur le bouton « Nouveau »
3. Saisissez les informations nécessaires :

   - **Nom** : Nom de la configuration d'exploration (exemple : Site Web de l'entreprise)
   - **URL** : URL cible de l'exploration (exemple : https://www.example.com/). Pour spécifier plusieurs URL, saisissez une URL par ligne
   - **Nombre d'accès maximum** : Nombre maximum de documents à explorer (facultatif)
   - **Intervalle** : Temps d'attente entre les accès (en millisecondes ; valeur par défaut : ``10000``)

   .. note::

      Les autres éléments (tels que l'agent utilisateur, le nombre de threads et la profondeur) utilisent leurs valeurs par défaut lorsqu'ils sont laissés vides.

4. Cliquez sur le bouton « Créer »

Étape 3 : Exécution de l'exploration
-------------------------------------

1. Cliquez sur [Système] → [Planificateur] dans le menu de gauche
2. Ouvrez le job [Default Crawler] et cliquez sur le bouton « Démarrer maintenant »
3. Attendez la fin de l'exploration (la progression peut être vérifiée sur le tableau de bord)

Étape 4 : Vérification de la recherche
---------------------------------------

1. Accédez à l'écran de recherche (http://localhost:8080/)
2. Saisissez un mot-clé de recherche
3. Vérifiez que les résultats de recherche s'affichent

.. note::

   L'exploration peut prendre du temps.
   Pour les sites de grande envergure, cela peut prendre de plusieurs heures à plusieurs jours.

Autres configurations recommandées
===================================

Pour une exploitation en environnement de production, veuillez également envisager les configurations suivantes.

Principaux paramètres via les variables d'environnement
--------------------------------------------------------

Les paramètres tels que le numéro de port, la taille du tas JVM et l'URL de connexion à OpenSearch peuvent être modifiés via des variables d'environnement. Modifiez ``bin/fess.in.sh`` pour l'édition TAR.GZ, ``/etc/sysconfig/fess`` pour l'édition RPM, et ``/etc/default/fess`` pour l'édition DEB. Un redémarrage de |Fess| est requis après toute modification.

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Variable d'environnement
     - Valeur par défaut
     - Description
   * - ``FESS_PORT``
     - ``8080``
     - Port HTTP sur lequel |Fess| écoute.
   * - ``FESS_HEAP_SIZE``
     - (non défini)
     - Taille du tas JVM. Définit la même valeur pour le minimum et le maximum. Lorsqu'elle n'est pas définie, un minimum de ``256m`` et un maximum de ``2g`` sont utilisés (l'édition ZIP Windows utilise un maximum de ``1g``) ; l'édition RPM/DEB utilise ``512m``.
   * - ``SEARCH_ENGINE_HTTP_URL``
     - (non défini)
     - URL de l'OpenSearch auquel se connecter. Lorsqu'elle n'est pas définie, la valeur par défaut intégrée ``http://localhost:9201`` est utilisée. À modifier lorsqu'OpenSearch s'exécute sur un port ou un hôte différent (la procédure :doc:`install-linux` la définit à ``http://localhost:9200`` pour correspondre au port d'écoute d'OpenSearch). L'édition RPM/DEB définit ``http://localhost:9200`` par défaut via le fichier d'environnement du paquet.
   * - ``FESS_LOG_LEVEL``
     - ``warn``
     - Niveau de log de |Fess|.

.. note::

   L'édition ZIP Windows (``bin\fess.in.bat``) ne lit pas ces variables d'environnement (à l'exception de celles liées au proxy). Les valeurs sont écrites directement dans le fichier ; modifiez ``bin\fess.in.bat`` directement pour les changer.

Configuration du serveur de messagerie
---------------------------------------

Pour recevoir des notifications d'échec et autres messages par e-mail, configurez le serveur SMTP et l'adresse du destinataire des notifications.

1. Dans le fichier de configuration ``app/WEB-INF/classes/fess_env.properties``, spécifiez l'hôte et le port du serveur SMTP dans ``mail.smtp.server.main.host.and.port`` (valeur par défaut : ``localhost:25``). Un redémarrage de |Fess| est requis après la modification.
2. Dans l'interface d'administration, cliquez sur [Système] → [Général] dans le menu de gauche.
3. Saisissez l'adresse e-mail du destinataire dans le champ [E-mail de notification].
4. Cliquez sur le bouton [Mettre à jour].
5. Vous pouvez vérifier que l'envoi d'e-mail fonctionne correctement avec le bouton [Envoyer un e-mail de test].

Configuration du fuseau horaire
--------------------------------

|Fess| utilise le fuseau horaire du serveur (OS / JVM). Il n'existe pas de paramètre permettant de modifier le fuseau horaire dans l'interface d'administration. Pour le modifier, changez le paramètre de fuseau horaire de l'OS, ou ajoutez l'option JVM ``-Duser.timezone=Asia/Tokyo`` à ``FESS_JAVA_OPTS`` dans ``bin/fess.in.sh`` (sous Windows, ``bin\fess.in.bat``).

Ajustement du niveau de log
----------------------------

En production, vous pouvez ajuster le niveau de log pour réduire l'utilisation du disque.

Le niveau de log global de |Fess| peut être modifié avec la variable d'environnement ``FESS_LOG_LEVEL`` (valeur par défaut : ``warn``). Pour contrôler les journaliseurs individuels en détail, modifiez le fichier de configuration ``app/WEB-INF/classes/log4j2.xml``. L'exploration, les suggestions et la génération de miniatures s'exécutent comme des processus séparés ; configurez donc leurs niveaux de log individuellement dans ``app/WEB-INF/env/{crawler,suggest,thumbnail}/resources/log4j2.xml``.

Pour plus de détails, consultez :doc:`../admin/index`.

Méthodes d'arrêt
================

Version TAR.GZ/ZIP
------------------

Arrêt de Fess
~~~~~~~~~~~~~

Tuez le processus ::

    $ ps aux | grep fess
    $ kill <PID>

Ou arrêtez depuis la console avec ``Ctrl+C`` (si vous l'exécutez au premier plan).

Arrêt d'OpenSearch ::

    $ ps aux | grep opensearch
    $ kill <PID>

Version RPM/DEB (chkconfig)
---------------------------

Arrêt de Fess ::

    $ sudo service fess stop

Arrêt d'OpenSearch ::

    $ sudo service opensearch stop

Version RPM/DEB (systemd)
-------------------------

Arrêt de Fess ::

    $ sudo systemctl stop fess.service

Arrêt d'OpenSearch ::

    $ sudo systemctl stop opensearch.service

Version Docker
--------------

Arrêt des conteneurs ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop

Arrêt et suppression des conteneurs ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   Pour supprimer également les volumes avec la commande ``down``, ajoutez l'option ``-v``.
   Dans ce cas, toutes les données seront supprimées, soyez vigilant.

Méthodes de redémarrage
========================

Version TAR.GZ/ZIP
------------------

Arrêtez puis démarrez.

Version RPM/DEB
---------------

chkconfig ::

    $ sudo service fess restart

systemd ::

    $ sudo systemctl restart fess.service

Version Docker
--------------

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml restart

Dépannage
=========

En cas de non-démarrage
-----------------------

1. **Vérifiez qu'OpenSearch est démarré**

   ::

       $ curl http://localhost:9200/

   Si OpenSearch n'est pas démarré, démarrez d'abord OpenSearch.

2. **Vérifiez les conflits de ports**

   ::

       $ sudo netstat -tuln | grep 8080

   Si le port 8080 est déjà utilisé, modifiez le numéro de port.

   - Édition TAR.GZ : modifiez ``FESS_PORT`` dans ``bin/fess.in.sh``
   - Édition ZIP (Windows) : modifiez ``-Dfess.port=8080`` directement dans ``bin\fess.in.bat``
   - Édition RPM : modifiez ``FESS_PORT`` dans ``/etc/sysconfig/fess``
   - Édition DEB : modifiez ``FESS_PORT`` dans ``/etc/default/fess``

3. **Vérifiez les logs**

   Vérifiez les messages d'erreur pour identifier le problème.

4. **Vérifiez la version de Java**

   ::

       $ java -version

   Vérifiez que Java 21 ou ultérieur est installé.

Pour un dépannage détaillé, consultez :doc:`troubleshooting`.

Étapes suivantes
================

Une fois |Fess| démarré normalement, consultez les documents suivants pour commencer l'exploitation :

- :doc:`../admin/index` - Détails sur la configuration de l'exploration, la configuration de la recherche et la configuration du système
- :doc:`security` - Configuration de la sécurité pour les environnements de production
- :doc:`troubleshooting` - Problèmes courants et solutions
- :doc:`upgrade` - Procédure de mise à niveau de version
- :doc:`uninstall` - Procédure de désinstallation
