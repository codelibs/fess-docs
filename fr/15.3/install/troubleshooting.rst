==============
Dépannage
==============

Cette page décrit les problèmes courants lors de l'installation, du démarrage et de l'exploitation de |Fess|, ainsi que leurs solutions.

Problèmes lors de l'installation
=================================

Java n'est pas reconnu
-----------------------

**Symptôme :**

::

    -bash: java: command not found

Ou ::

    'java' is not recognized as an internal or external command

**Cause :**

Java n'est pas installé, ou la variable d'environnement PATH n'est pas correctement configurée.

**Solution :**

1. Vérifiez si Java est installé ::

       $ which java
       $ java -version

2. Si non installé, installez Java 21 ::

       # Ubuntu/Debian
       $ sudo apt-get update
       $ sudo apt-get install openjdk-21-jdk

       # RHEL/CentOS
       $ sudo yum install java-21-openjdk

3. Configurez la variable d'environnement JAVA_HOME ::

       $ export JAVA_HOME=/path/to/java
       $ export PATH=$JAVA_HOME/bin:$PATH

   Pour une configuration permanente, ajoutez à ``~/.bashrc`` ou ``/etc/profile``.

Échec de l'installation des plugins
------------------------------------

**Symptôme :**

::

    ERROR: Plugin installation failed

**Cause :**

- Problème de connexion réseau
- La version du plugin ne correspond pas à la version d'OpenSearch
- Problème de permissions

**Solution :**

1. Vérifiez la version d'OpenSearch ::

       $ /path/to/opensearch/bin/opensearch --version

2. Adaptez la version du plugin à celle d'OpenSearch ::

       $ /path/to/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.0

3. Vérifiez les permissions ::

       $ sudo /path/to/opensearch/bin/opensearch-plugin install ...

4. Pour une installation via proxy ::

       $ export ES_JAVA_OPTS="-Dhttp.proxyHost=proxy.example.com -Dhttp.proxyPort=8080"
       $ /path/to/opensearch/bin/opensearch-plugin install ...

Problèmes lors du démarrage
============================

Fess ne démarre pas
-------------------

**Symptôme :**

Une erreur se produit lors de l'exécution de la commande de démarrage de Fess, ou le processus se termine immédiatement.

**Points de vérification :**

1. **Vérifiez qu'OpenSearch est démarré** ::

       $ curl http://localhost:9200/

   Si le démarrage est normal, une réponse JSON est retournée.

2. **Vérifiez les conflits de ports** ::

       $ sudo netstat -tuln | grep 8080

   Si le port 8080 est déjà utilisé, modifiez le numéro de port dans le fichier de configuration.

3. **Vérifiez les fichiers journaux** ::

       $ tail -f /path/to/fess/logs/fess.log

   Identifiez la cause à partir des messages d'erreur.

4. **Vérifiez la version de Java** ::

       $ java -version

   Vérifiez que Java 21 ou ultérieur est installé.

5. **Vérifiez la mémoire insuffisante** ::

       $ free -h

   Si la mémoire est insuffisante, ajustez la taille du tas ou augmentez la mémoire système.

OpenSearch ne démarre pas
--------------------------

**Symptôme :**

::

    ERROR: bootstrap checks failed

**Cause :**

La configuration du système ne satisfait pas aux exigences d'OpenSearch.

**Solution :**

1. **Configuration de vm.max_map_count** ::

       $ sudo sysctl -w vm.max_map_count=262144

   Pour une configuration permanente ::

       $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
       $ sudo sysctl -p

2. **Augmentation de la limite des descripteurs de fichiers** ::

       $ sudo vi /etc/security/limits.conf

   Ajoutez ::

       opensearch  -  nofile  65535
       opensearch  -  nproc   4096

3. **Configuration du verrouillage mémoire** ::

       $ sudo vi /etc/security/limits.conf

   Ajoutez ::

       opensearch  -  memlock  unlimited

4. Redémarrez OpenSearch ::

       $ sudo systemctl restart opensearch

Conflit de numéros de port
---------------------------

**Symptôme :**

::

    Address already in use

**Solution :**

1. Vérifiez les ports utilisés ::

       $ sudo netstat -tuln | grep 8080
       $ sudo lsof -i :8080

2. Arrêtez le processus utilisé, ou modifiez le numéro de port de Fess

   Modifiez le numéro de port dans le fichier de configuration (``system.properties``) ::

       server.port=9080

Problèmes de connexion
=======================

Fess ne peut pas se connecter à OpenSearch
-------------------------------------------

**Symptôme :**

Les journaux affichent des erreurs telles que ::

    Connection refused
    ou
    No route to host

**Solution :**

1. **Vérifiez qu'OpenSearch est démarré** ::

       $ curl http://localhost:9200/

2. **Vérifiez l'URL de connexion**

   Vérifiez que l'URL configurée dans ``fess.in.sh`` ou ``fess.in.bat`` est correcte ::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200

3. **Vérifiez le pare-feu** ::

       $ sudo firewall-cmd --list-all

   Vérifiez que le port 9200 est ouvert.

4. **Vérifiez la connexion réseau**

   Si vous exécutez OpenSearch sur un autre hôte ::

       $ ping opensearch-host
       $ telnet opensearch-host 9200

Impossible d'accéder à Fess depuis le navigateur
-------------------------------------------------

**Symptôme :**

Impossible d'accéder à http://localhost:8080/ via le navigateur.

**Solution :**

1. **Vérifiez que Fess est démarré** ::

       $ ps aux | grep fess

2. **Essayez d'accéder depuis localhost** ::

       $ curl http://localhost:8080/

3. **Vérifiez le pare-feu** ::

       $ sudo firewall-cmd --list-all

   Vérifiez que le port 8080 est ouvert.

4. **Si vous accédez depuis un autre hôte**

   Vérifiez que Fess écoute sur autre chose que localhost ::

       $ netstat -tuln | grep 8080

   Si c'est ``127.0.0.1:8080``, modifiez la configuration pour écouter sur ``0.0.0.0:8080`` ou une adresse IP spécifique.

Problèmes de performances
==========================

La recherche est lente
-----------------------

**Cause :**

- Taille de l'index importante
- Mémoire insuffisante
- E/S disque lentes
- Requête complexe

**Solution :**

1. **Augmentez la taille du tas**

   Modifiez ``fess.in.sh`` ::

       FESS_HEAP_SIZE=4g

   Ajustez également la taille du tas d'OpenSearch ::

       export OPENSEARCH_JAVA_OPTS="-Xms4g -Xmx4g"

2. **Optimisation de l'index**

   Exécutez régulièrement l'optimisation depuis « Système » → « Planificateur » dans l'écran d'administration.

3. **Utilisez un SSD**

   Si les E/S disque sont le goulot d'étranglement, migrez vers un SSD.

4. **Activez le cache**

   Activez le cache de requêtes dans le fichier de configuration.

L'exploration est lente
------------------------

**Cause :**

- Intervalle d'exploration long
- Réponse lente du site cible
- Nombre de threads faible

**Solution :**

1. **Ajustez l'intervalle d'exploration**

   Raccourcissez l'« Intervalle » de la configuration d'exploration dans l'écran d'administration (en millisecondes).

   .. warning::

      Un intervalle trop court peut surcharger le site cible. Configurez une valeur appropriée.

2. **Augmentez le nombre de threads**

   Augmentez le nombre de threads d'exploration dans le fichier de configuration ::

       crawler.thread.count=10

3. **Ajustez la valeur de timeout**

   Pour les sites à réponse lente, augmentez la valeur de timeout.

Problèmes de données
=====================

Les résultats de recherche ne s'affichent pas
----------------------------------------------

**Cause :**

- L'index n'a pas été créé
- L'exploration a échoué
- La requête de recherche est incorrecte

**Solution :**

1. **Vérifiez l'index** ::

       $ curl http://localhost:9200/_cat/indices?v

   Vérifiez que l'index de |Fess| existe.

2. **Vérifiez les journaux d'exploration**

   Vérifiez les journaux d'exploration depuis « Système » → « Journal » dans l'écran d'administration pour rechercher les erreurs.

3. **Réexécutez l'exploration**

   Exécutez « Default Crawler » depuis « Système » → « Planificateur » dans l'écran d'administration.

4. **Simplifiez la requête de recherche**

   Effectuez d'abord une recherche avec un mot-clé simple pour vérifier que des résultats sont retournés.

L'index est corrompu
--------------------

**Symptôme :**

Des erreurs se produisent lors de la recherche, ou des résultats inattendus sont retournés.

**Solution :**

1. **Supprimez et recréez l'index**

   .. warning::

      La suppression de l'index entraînera la perte de toutes les données de recherche. Veuillez obligatoirement effectuer une sauvegarde.

   ::

       $ curl -X DELETE http://localhost:9200/fess*

2. **Réexécutez l'exploration**

   Exécutez « Default Crawler » depuis l'écran d'administration pour recréer l'index.

Problèmes spécifiques à Docker
===============================

Le conteneur ne démarre pas
----------------------------

**Symptôme :**

Le conteneur ne démarre pas avec ``docker compose up``.

**Solution :**

1. **Vérifiez les journaux** ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs

2. **Vérifiez la mémoire insuffisante**

   Augmentez la mémoire allouée à Docker (depuis les paramètres de Docker Desktop).

3. **Vérifiez les conflits de ports** ::

       $ docker ps

   Vérifiez qu'aucun autre conteneur n'utilise les ports 8080 ou 9200.

4. **Vérifiez le fichier Docker Compose**

   Vérifiez qu'il n'y a pas d'erreur de syntaxe dans le fichier YAML ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml config

Le conteneur démarre mais impossible d'accéder à Fess
------------------------------------------------------

**Solution :**

1. **Vérifiez l'état du conteneur** ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

2. **Vérifiez les journaux** ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs fess

3. **Vérifiez la configuration réseau** ::

       $ docker network ls
       $ docker network inspect <network_name>

Problèmes spécifiques à Windows
================================

Problème de chemin
------------------

**Symptôme :**

Des erreurs se produisent si le chemin contient des espaces ou des caractères japonais.

**Solution :**

Veuillez installer dans un répertoire dont le chemin ne contient pas d'espaces ou de caractères japonais.

Exemple ::

    C:\opensearch  (recommandé)
    C:\Program Files\opensearch  (non recommandé)

Impossible d'enregistrer en tant que service
---------------------------------------------

**Solution :**

Utilisez un outil tiers (tel que NSSM) pour l'enregistrer en tant que service Windows.

Pour les procédures détaillées, consultez :doc:`install-windows`.

Autres problèmes
================

Modification du niveau de journal
----------------------------------

Pour vérifier des journaux détaillés, modifiez le niveau de journal en DEBUG.

Modifiez ``log4j2.xml`` ::

    <Logger name="org.codelibs.fess" level="debug"/>

Réinitialisation de la base de données
---------------------------------------

Pour réinitialiser la configuration, supprimez l'index d'OpenSearch ::

    $ curl -X DELETE http://localhost:9200/.fess_config*

.. warning::

   L'exécution de cette commande supprimera toutes les données de configuration.

Informations de support
========================

Si le problème n'est pas résolu, veuillez utiliser les ressources de support suivantes :

Support communautaire
---------------------

- **Issues** : https://github.com/codelibs/fess/issues

  Lors du signalement d'un problème, veuillez inclure les informations suivantes :

  - Version de Fess
  - Version d'OpenSearch
  - Système d'exploitation et version
  - Messages d'erreur (extraits des journaux)
  - Procédure de reproduction

- **Forum** : https://discuss.codelibs.org/

Support commercial
------------------

Si vous avez besoin d'un support commercial, veuillez contacter N2SM, Inc. :

- **Web** : https://www.n2sm.net/

Collecte d'informations de débogage
====================================

Lors du signalement d'un problème, il est utile de collecter les informations suivantes :

1. **Informations de version** ::

       $ cat /path/to/fess/VERSION
       $ /path/to/opensearch/bin/opensearch --version
       $ java -version

2. **Informations système** ::

       $ uname -a
       $ cat /etc/os-release
       $ free -h
       $ df -h

3. **Fichiers journaux** ::

       $ tar czf fess-logs.tar.gz /path/to/fess/logs/

4. **Fichiers de configuration** (après suppression des informations confidentielles) ::

       $ tar czf fess-config.tar.gz /path/to/fess/app/WEB-INF/conf/

5. **État d'OpenSearch** ::

       $ curl http://localhost:9200/_cluster/health?pretty
       $ curl http://localhost:9200/_cat/indices?v
