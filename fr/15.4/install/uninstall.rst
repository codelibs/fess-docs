==========================
Procédure de désinstallation
==========================

Cette page décrit la procédure de désinstallation complète de |Fess|.

.. warning::

   **Notes importantes avant la désinstallation**

   - La désinstallation supprimera toutes les données
   - Si vous avez des données importantes, veuillez obligatoirement effectuer une sauvegarde
   - Pour les procédures de sauvegarde, consultez :doc:`upgrade`

Préparation avant la désinstallation
=====================================

Récupération de la sauvegarde
------------------------------

Veuillez sauvegarder les données nécessaires :

1. **Données de configuration**

   Téléchargez depuis « Système » → « Sauvegarde » dans l'écran d'administration

2. **Configuration d'exploration**

   Si nécessaire, exportez la configuration d'exploration

3. **Fichiers de configuration personnalisés**

   Version TAR.GZ/ZIP ::

       $ cp -r /path/to/fess/app/WEB-INF/conf /backup/
       $ cp -r /path/to/fess/app/WEB-INF/classes /backup/

   Version RPM/DEB ::

       $ sudo cp -r /etc/fess /backup/

Arrêt des services
-------------------

Avant la désinstallation, arrêtez tous les services.

Version TAR.GZ/ZIP ::

    $ ps aux | grep fess
    $ kill <fess_pid>
    $ kill <opensearch_pid>

Version RPM/DEB ::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Version Docker ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Désinstallation de la version TAR.GZ/ZIP
=========================================

Étape 1 : Suppression de Fess
------------------------------

Supprimez le répertoire d'installation ::

    $ rm -rf /path/to/fess-15.4.0

Étape 2 : Suppression d'OpenSearch
-----------------------------------

Supprimez le répertoire d'installation d'OpenSearch ::

    $ rm -rf /path/to/opensearch-3.3.2

Étape 3 : Suppression du répertoire de données (optionnel)
-----------------------------------------------------------

Par défaut, le répertoire de données se trouve dans le répertoire d'installation de Fess,
mais si vous avez spécifié un emplacement différent, supprimez également ce répertoire ::

    $ rm -rf /path/to/data

Étape 4 : Suppression du répertoire de journaux (optionnel)
------------------------------------------------------------

Supprimez les fichiers journaux ::

    $ rm -rf /path/to/fess/logs
    $ rm -rf /path/to/opensearch/logs

Désinstallation de la version RPM
==================================

Étape 1 : Désinstallation de Fess
----------------------------------

Désinstallez le package RPM ::

    $ sudo rpm -e fess

Étape 2 : Désinstallation d'OpenSearch
---------------------------------------

::

    $ sudo rpm -e opensearch

Étape 3 : Désactivation et suppression des services
----------------------------------------------------

Avec chkconfig ::

    $ sudo /sbin/chkconfig --del fess
    $ sudo /sbin/chkconfig --del opensearch

Avec systemd ::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

Étape 4 : Suppression du répertoire de données
-----------------------------------------------

.. warning::

   L'exécution de cette opération supprimera complètement toutes les données d'index et la configuration.

::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

Étape 5 : Suppression des fichiers de configuration
----------------------------------------------------

::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/opensearch

Étape 6 : Suppression des fichiers journaux
--------------------------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

Étape 7 : Suppression des utilisateurs et groupes (optionnel)
--------------------------------------------------------------

Pour supprimer les utilisateurs et groupes système ::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Désinstallation de la version DEB
==================================

Étape 1 : Désinstallation de Fess
----------------------------------

Désinstallez le package DEB ::

    $ sudo dpkg -r fess

Pour supprimer complètement y compris les fichiers de configuration ::

    $ sudo dpkg -P fess

Étape 2 : Désinstallation d'OpenSearch
---------------------------------------

::

    $ sudo dpkg -r opensearch

Ou pour supprimer y compris les fichiers de configuration ::

    $ sudo dpkg -P opensearch

Étape 3 : Désactivation des services
-------------------------------------

::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

Étape 4 : Suppression du répertoire de données
-----------------------------------------------

.. warning::

   L'exécution de cette opération supprimera complètement toutes les données d'index et la configuration.

::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

Étape 5 : Suppression des fichiers de configuration (si dpkg -P n'a pas été utilisé)
-------------------------------------------------------------------------------------

::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/opensearch

Étape 6 : Suppression des fichiers journaux
--------------------------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

Étape 7 : Suppression des utilisateurs et groupes (optionnel)
--------------------------------------------------------------

Pour supprimer les utilisateurs et groupes système ::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Désinstallation de la version Docker
=====================================

Étape 1 : Suppression des conteneurs et réseaux
------------------------------------------------

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Étape 2 : Suppression des volumes
----------------------------------

.. warning::

   L'exécution de cette opération supprimera complètement toutes les données.

Vérification de la liste des volumes ::

    $ docker volume ls

Suppression des volumes liés à Fess ::

    $ docker volume rm fess-es-data
    $ docker volume rm fess-data

Ou suppression groupée de tous les volumes ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

Étape 3 : Suppression des images (optionnel)
---------------------------------------------

Pour supprimer les images Docker et libérer de l'espace disque ::

    $ docker images | grep fess
    $ docker rmi codelibs/fess:15.4.0

    $ docker images | grep opensearch
    $ docker rmi opensearchproject/opensearch:3.3.2

Étape 4 : Suppression du réseau (optionnel)
--------------------------------------------

Suppression du réseau créé par Docker Compose ::

    $ docker network ls
    $ docker network rm <network_name>

Étape 5 : Suppression des fichiers Compose
-------------------------------------------

::

    $ rm compose.yaml compose-opensearch3.yaml

Vérification de la désinstallation
===================================

Vérifiez que tous les composants ont été supprimés.

Vérification des processus
---------------------------

::

    $ ps aux | grep fess
    $ ps aux | grep opensearch

Si rien ne s'affiche, les processus sont arrêtés.

Vérification des ports
-----------------------

::

    $ sudo netstat -tuln | grep 8080
    $ sudo netstat -tuln | grep 9200

Vérifiez que les ports ne sont pas utilisés.

Vérification des fichiers
--------------------------

Version TAR.GZ/ZIP ::

    $ ls /path/to/fess-15.4.0  # Vérifiez que le répertoire n'existe pas

Version RPM/DEB ::

    $ ls /var/lib/fess  # Vérifiez que le répertoire n'existe pas
    $ ls /etc/fess      # Vérifiez que le répertoire n'existe pas

Version Docker ::

    $ docker ps -a | grep fess  # Vérifiez que le conteneur n'existe pas
    $ docker volume ls | grep fess  # Vérifiez que le volume n'existe pas

Vérification des packages
--------------------------

Version RPM ::

    $ rpm -qa | grep fess
    $ rpm -qa | grep opensearch

Version DEB ::

    $ dpkg -l | grep fess
    $ dpkg -l | grep opensearch

Si rien ne s'affiche, les packages ont été supprimés.

Désinstallation partielle
==========================

Supprimer uniquement Fess en conservant OpenSearch
---------------------------------------------------

Si vous utilisez également OpenSearch pour d'autres applications, vous pouvez supprimer uniquement Fess.

1. Arrêt de Fess
2. Suppression du package ou du répertoire de Fess
3. Suppression du répertoire de données de Fess (``/var/lib/fess``, etc.)
4. Ne pas supprimer OpenSearch

Supprimer uniquement OpenSearch en conservant Fess
---------------------------------------------------

.. warning::

   Si vous supprimez OpenSearch, Fess ne fonctionnera plus.
   Veuillez modifier la configuration pour vous connecter à un autre cluster OpenSearch.

1. Arrêt d'OpenSearch
2. Suppression du package ou du répertoire d'OpenSearch
3. Suppression du répertoire de données d'OpenSearch (``/var/lib/opensearch``, etc.)
4. Mise à jour de la configuration de Fess pour spécifier un autre cluster OpenSearch

Dépannage
=========

Impossible de supprimer le package
-----------------------------------

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
--------------------------------------

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
===================================

Si vous réinstallez après la désinstallation, vérifiez les points suivants :

1. Tous les processus sont arrêtés
2. Tous les fichiers et répertoires ont été supprimés
3. Les ports 8080 et 9200 ne sont pas utilisés
4. Il ne reste aucun fichier de configuration antérieur

Pour les procédures de réinstallation, consultez :doc:`install`.

Étapes suivantes
================

Après la désinstallation :

- Pour installer une nouvelle version, consultez :doc:`install`
- Pour migrer des données, consultez :doc:`upgrade`
- Pour envisager une solution de recherche alternative, consultez le site officiel de Fess
