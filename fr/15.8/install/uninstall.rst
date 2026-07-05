============================
Procédure de désinstallation
============================

Cette page décrit la procédure de désinstallation complète de |Fess|.

.. warning::

   **Notes importantes avant la désinstallation**

   - La désinstallation supprimera toutes les données
   - Si vous avez des données importantes, veuillez obligatoirement effectuer une sauvegarde
   - Pour les procédures de sauvegarde, consultez :doc:`upgrade`

Préparation avant la désinstallation
====================================

Récupération de la sauvegarde
-----------------------------

Veuillez sauvegarder les données nécessaires :

1. **Données de configuration**

   Téléchargez depuis « Système » → « Sauvegarde » dans l'écran d'administration.
   Cette opération permet d'exporter en bloc les différents paramètres (y compris la configuration d'exploration), les journaux de recherche, etc.

2. **Fichiers de configuration personnalisés**

   Version TAR.GZ/ZIP ::

       $ cp -r /path/to/fess/app/WEB-INF/conf /backup/
       $ cp -r /path/to/fess/app/WEB-INF/classes /backup/

   Version RPM/DEB ::

       $ sudo cp -r /etc/fess /backup/

.. note::

   La majeure partie des index et de la configuration de |Fess| est stockée dans OpenSearch.
   Pour sauvegarder les données d'index, utilisez la fonction de snapshot d'OpenSearch.
   Pour la procédure détaillée, consultez :doc:`upgrade`.

Arrêt des services
------------------

Avant la désinstallation, arrêtez tous les services.

Version TAR.GZ/ZIP ::

    $ ps aux | grep -E 'fess|opensearch'
    $ kill <fess_pid>
    $ kill <opensearch_pid>

Version RPM/DEB ::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Version Docker ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Désinstallation de la version TAR.GZ/ZIP
========================================

Étape 1 : Suppression de Fess
-----------------------------

Supprimez le répertoire d'installation ::

    $ rm -rf /path/to/fess-15.8.0

Étape 2 : Suppression d'OpenSearch
----------------------------------

Supprimez le répertoire d'installation d'OpenSearch ::

    $ rm -rf /path/to/opensearch-3.7.0

Étape 3 : Suppression du répertoire de données (optionnel)
----------------------------------------------------------

Les données d'index de |Fess| sont stockées dans OpenSearch.
Par défaut, elles sont stockées dans le répertoire d'installation d'OpenSearch (``opensearch-3.7.0/data``, etc.),
mais si vous avez spécifié un autre emplacement avec ``path.data``, supprimez également ce répertoire ::

    $ rm -rf /path/to/data

Étape 4 : Suppression du répertoire de journaux (optionnel)
-----------------------------------------------------------

Supprimez les fichiers journaux ::

    $ rm -rf /path/to/fess-15.8.0/logs
    $ rm -rf /path/to/opensearch-3.7.0/logs

Désinstallation de la version RPM
=================================

Étape 1 : Désinstallation de Fess
---------------------------------

Désinstallez le package RPM ::

    $ sudo rpm -e fess

.. note::

   Lors de la désinstallation du package |Fess|, le script de suppression du package exécute
   automatiquement l'arrêt et la désactivation du service ``fess``, ainsi que la suppression de
   l'utilisateur et du groupe ``fess``.
   Les étapes suivantes servent à vérifier que ces éléments ont bien été supprimés, ou à
   supprimer manuellement les données et les fichiers de configuration.

Étape 2 : Désinstallation d'OpenSearch
--------------------------------------

::

    $ sudo rpm -e opensearch

Étape 3 : Vérification de la désactivation des services
-------------------------------------------------------

Normalement, le service est désactivé lors de la suppression du package, mais pour vérifier ou désactiver par précaution, exécutez ce qui suit.

Avec systemd ::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

Dans un ancien environnement SysV init (chkconfig) ::

    $ sudo /sbin/chkconfig --del fess
    $ sudo /sbin/chkconfig --del opensearch

Étape 4 : Suppression du répertoire de données
----------------------------------------------

.. warning::

   L'exécution de cette opération supprimera complètement toutes les données d'index.

Le répertoire de données n'étant pas supprimé lors de la désinstallation du package, supprimez-le manuellement ::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

Étape 5 : Suppression des fichiers de configuration
---------------------------------------------------

Supprimez les fichiers de configuration et les fichiers de configuration d'environnement ::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/sysconfig/fess
    $ sudo rm -rf /etc/opensearch

.. note::

   Avec RPM, les fichiers de configuration dans ``/etc/fess`` peuvent subsister sous le nom ``.rpmsave``.
   Pour les supprimer complètement, supprimez-les manuellement comme indiqué ci-dessus.

Étape 6 : Suppression des fichiers journaux
-------------------------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

Étape 7 : Suppression du répertoire temporaire (optionnel)
----------------------------------------------------------

::

    $ sudo rm -rf /var/tmp/fess

Étape 8 : Suppression des utilisateurs et groupes (optionnel)
-------------------------------------------------------------

Normalement, l'utilisateur et le groupe ``fess`` sont supprimés lors de la suppression du package.
S'ils subsistent, ou pour supprimer l'utilisateur et le groupe d'OpenSearch, exécutez ce qui suit ::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Désinstallation de la version DEB
=================================

Étape 1 : Désinstallation de Fess
---------------------------------

Désinstallez le package DEB ::

    $ sudo dpkg -r fess

Pour supprimer complètement, y compris les fichiers de configuration et les fichiers de configuration d'environnement, utilisez purge ::

    $ sudo dpkg -P fess

.. note::

   Avec ``dpkg -r`` (remove), les fichiers de configuration (conffile) tels que ``/etc/default/fess`` subsistent.
   Avec ``dpkg -P`` (purge), ces fichiers de configuration ainsi que l'utilisateur et le groupe ``fess`` sont également supprimés.

Étape 2 : Désinstallation d'OpenSearch
--------------------------------------

::

    $ sudo dpkg -r opensearch

Ou, pour supprimer y compris les fichiers de configuration ::

    $ sudo dpkg -P opensearch

Étape 3 : Vérification de la désactivation des services
-------------------------------------------------------

Normalement, le service est désactivé lors de la suppression du package. Pour vérifier ou désactiver par précaution, exécutez ce qui suit ::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

Étape 4 : Suppression du répertoire de données
----------------------------------------------

.. warning::

   L'exécution de cette opération supprimera complètement toutes les données d'index.

::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

Étape 5 : Suppression des fichiers de configuration (si dpkg -P n'a pas été utilisé)
------------------------------------------------------------------------------------

::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/default/fess
    $ sudo rm -rf /etc/opensearch

Étape 6 : Suppression des fichiers journaux
-------------------------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

Étape 7 : Suppression des utilisateurs et groupes (optionnel)
-------------------------------------------------------------

Si vous n'avez pas utilisé ``dpkg -P``, l'utilisateur et le groupe ``fess`` subsistent.
Pour les supprimer, exécutez ce qui suit ::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Désinstallation de la version Docker
====================================

Étape 1 : Suppression des conteneurs et réseaux
-----------------------------------------------

Supprimez les conteneurs ainsi que le réseau créé par Docker Compose (``search_net``) ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Étape 2 : Suppression des volumes
---------------------------------

.. warning::

   L'exécution de cette opération supprimera complètement toutes les données.

Les données de |Fess| (index, dictionnaires, etc.) sont stockées dans les volumes d'OpenSearch.
Vérifiez d'abord la liste des volumes ::

    $ docker volume ls

Supprimez les volumes liés à OpenSearch ::

    $ docker volume rm <project>_search01_data
    $ docker volume rm <project>_search01_dictionary

.. note::

   Les noms de volumes sont préfixés par le nom du projet Docker Compose (généralement le nom du
   répertoire dans lequel se trouve le fichier Compose). Vérifiez les noms réels avec ``docker volume ls``.

Pour supprimer en bloc les conteneurs et les volumes, ajoutez l'option ``-v`` à ``down`` ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

Étape 3 : Suppression des images (optionnel)
--------------------------------------------

Pour supprimer les images Docker et libérer de l'espace disque ::

    $ docker images | grep fess
    $ docker rmi ghcr.io/codelibs/fess:15.8.0
    $ docker rmi ghcr.io/codelibs/fess-opensearch:3.7.0

Étape 4 : Suppression des fichiers Compose
------------------------------------------

::

    $ rm compose.yaml compose-opensearch3.yaml

Vérification de la désinstallation
==================================

Vérifiez que tous les composants ont été supprimés.

Vérification des processus
--------------------------

::

    $ ps aux | grep fess
    $ ps aux | grep opensearch

Si rien ne s'affiche, les processus sont arrêtés.

Vérification des ports
----------------------

::

    $ sudo netstat -tuln | grep 8080
    $ sudo netstat -tuln | grep 9200

Vérifiez que les ports ne sont pas utilisés.

Vérification des fichiers
-------------------------

Version TAR.GZ/ZIP ::

    $ ls /path/to/fess-15.8.0  # Vérifiez que le répertoire n'existe pas

Version RPM/DEB ::

    $ ls /var/lib/fess  # Vérifiez que le répertoire n'existe pas
    $ ls /etc/fess      # Vérifiez que le répertoire n'existe pas

Version Docker ::

    $ docker ps -a | grep -E 'fess01|search01'  # Vérifiez que le conteneur n'existe pas
    $ docker volume ls | grep search01           # Vérifiez que le volume n'existe pas

Vérification des packages
-------------------------

Version RPM ::

    $ rpm -qa | grep fess
    $ rpm -qa | grep opensearch

Version DEB ::

    $ dpkg -l | grep fess
    $ dpkg -l | grep opensearch

Si rien ne s'affiche, les packages ont été supprimés.

Désinstallation partielle
=========================

Supprimer uniquement Fess en conservant OpenSearch
--------------------------------------------------

Si vous utilisez également OpenSearch pour d'autres applications, vous pouvez supprimer uniquement Fess.

1. Arrêter Fess
2. Supprimer le package ou le répertoire de Fess
3. Supprimer le répertoire de données de Fess (``/var/lib/fess``, etc.)
4. Supprimer les index de |Fess| créés dans OpenSearch (``fess.*``, ``.fess_*``, etc.)
5. Ne pas supprimer OpenSearch

Supprimer uniquement OpenSearch en conservant Fess
--------------------------------------------------

.. warning::

   Si vous supprimez OpenSearch, Fess ne fonctionnera plus.
   Veuillez modifier la configuration pour vous connecter à un autre cluster OpenSearch.

1. Arrêter OpenSearch
2. Supprimer le package ou le répertoire d'OpenSearch
3. Supprimer le répertoire de données d'OpenSearch (``/var/lib/opensearch``, etc.)
4. Mettre à jour la configuration de Fess pour spécifier un autre cluster OpenSearch

Dépannage
=========

Impossible de supprimer le package
----------------------------------

**Symptôme :**

Erreur avec ``rpm -e`` ou ``dpkg -r``.

**Solution :**

1. Vérifiez que le service est arrêté ::

       $ sudo systemctl stop fess.service

2. Vérifiez les dépendances ::

       $ rpm -qa | grep fess
       $ dpkg -l | grep fess

3. Suppression forcée (dernier recours) ::

       $ sudo rpm -e --nodeps fess
       $ sudo dpkg -r --force-all fess

Impossible de supprimer le répertoire
-------------------------------------

**Symptôme :**

Impossible de supprimer le répertoire avec ``rm -rf``.

**Solution :**

1. Vérifiez les permissions ::

       $ ls -ld /path/to/directory

2. Suppression avec sudo ::

       $ sudo rm -rf /path/to/directory

3. Vérifiez qu'aucun processus n'utilise le fichier ::

       $ sudo lsof | grep /path/to/directory

Préparation pour la réinstallation
==================================

Si vous réinstallez après la désinstallation, vérifiez les points suivants :

1. Tous les processus sont arrêtés
2. Tous les fichiers et répertoires ont été supprimés
3. Les ports 8080 et 9200 ne sont pas utilisés
4. Il ne reste aucun fichier de configuration antérieur

Pour les procédures de réinstallation, consultez :doc:`install`.

Étapes suivantes
================

Une fois la désinstallation terminée :

- Pour installer une nouvelle version, consultez :doc:`install`
- Pour migrer des données, consultez :doc:`upgrade`
- Pour envisager une solution de recherche alternative, consultez le site officiel de Fess
