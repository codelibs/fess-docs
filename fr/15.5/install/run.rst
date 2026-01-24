============================
Démarrage, arrêt et configuration initiale
============================

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

    $ cd /path/to/opensearch-3.3.2
    $ ./bin/opensearch

Pour un démarrage en arrière-plan ::

    $ ./bin/opensearch -d

Démarrage de Fess
~~~~~~~~~~~~~~~~~

::

    $ cd /path/to/fess-15.5.0
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

    C:\> cd C:\opensearch-3.3.2
    C:\opensearch-3.3.2> bin\opensearch.bat

Démarrage de Fess
~~~~~~~~~~~~~~~~~

1. Ouvrez le répertoire d'installation de Fess
2. Double-cliquez sur ``fess.bat`` dans le dossier ``bin``

Ou depuis l'invite de commandes ::

    C:\> cd C:\fess-15.5.0
    C:\fess-15.5.0> bin\fess.bat

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

Démarrage avec Docker Compose ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Vérification de l'état de démarrage ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

Vérification des logs ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess

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

    $ tail -f /path/to/fess-15.5.0/logs/fess.log

Version RPM/DEB ::

    $ sudo tail -f /var/log/fess/fess.log

Ou en utilisant journalctl ::

    $ sudo journalctl -u fess.service -f

Version Docker ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess

.. tip::

   En cas de démarrage normal, un message comme celui-ci s'affiche dans les logs ::

       INFO  Boot - Fess is ready.

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
4. Saisissez un nouveau mot de passe dans le champ « Mot de passe »
5. Cliquez sur le bouton « Confirmer »
6. Cliquez sur le bouton « Mettre à jour »

.. important::

   Nous recommandons que le mot de passe satisfasse les conditions suivantes :

   - 8 caractères ou plus
   - Combinaison de majuscules, minuscules, chiffres et symboles
   - Difficile à deviner

Étape 2 : Création de la configuration d'exploration
-----------------------------------------------------

Créez une configuration pour explorer les sites ou systèmes de fichiers à rechercher.

1. Cliquez sur « Explorateur » → « Web » dans le menu de gauche
2. Cliquez sur le bouton « Nouveau »
3. Saisissez les informations nécessaires :

   - **Nom** : Nom de la configuration d'exploration (exemple : Site Web de l'entreprise)
   - **URL** : URL de la cible d'exploration (exemple : https://www.example.com/)
   - **Nombre d'accès maximum** : Limite supérieure du nombre de pages à explorer
   - **Intervalle** : Intervalle d'exploration (en millisecondes)

4. Cliquez sur le bouton « Créer »

Étape 3 : Exécution de l'exploration
-------------------------------------

1. Cliquez sur « Système » → « Planificateur » dans le menu de gauche
2. Cliquez sur le bouton « Démarrer maintenant » du job « Default Crawler »
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

Configuration du serveur de messagerie
---------------------------------------

Pour recevoir des notifications d'incidents et des rapports par e-mail, configurez le serveur de messagerie.

1. Cliquez sur « Système » → « Général » dans le menu de gauche
2. Cliquez sur l'onglet « E-mail »
3. Saisissez les informations du serveur SMTP
4. Cliquez sur le bouton « Mettre à jour »

Configuration du fuseau horaire
--------------------------------

1. Cliquez sur « Système » → « Général » dans le menu de gauche
2. Définissez le « Fuseau horaire » sur la valeur appropriée (exemple : Europe/Paris)
3. Cliquez sur le bouton « Mettre à jour »

Ajustement du niveau de log
----------------------------

Dans les environnements de production, vous pouvez ajuster le niveau de log pour réduire l'utilisation du disque.

Modifiez le fichier de configuration (``app/WEB-INF/classes/log4j2.xml``).

Pour plus de détails, consultez le guide de l'administrateur.

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

   Si le port 8080 est déjà utilisé, modifiez le numéro de port dans le fichier de configuration.

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

- **Guide de l'administrateur** : Détails sur la configuration de l'exploration, la configuration de la recherche et la configuration du système
- :doc:`security` - Configuration de la sécurité pour les environnements de production
- :doc:`troubleshooting` - Problèmes courants et solutions
- :doc:`upgrade` - Procédure de mise à niveau de version
- :doc:`uninstall` - Procédure de désinstallation
