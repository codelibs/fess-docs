==================================
Installation avec Docker (Détails)
==================================

Cette page décrit la procédure d'installation de |Fess| à l'aide de Docker et Docker Compose.
L'utilisation de Docker vous permet de construire un environnement |Fess| facilement et rapidement.

Prérequis
=========

- La configuration requise décrite dans :doc:`prerequisites` doit être satisfaite
- Docker 20.10 ou ultérieur doit être installé
- Docker Compose 2.0 ou ultérieur doit être installé

Vérification de l'installation de Docker
=========================================

Vérifiez les versions de Docker et Docker Compose avec les commandes suivantes.

::

    $ docker --version
    $ docker compose version

.. note::

   Si vous utilisez une ancienne version de Docker Compose, utilisez la commande ``docker-compose``.
   Ce document utilise le nouveau format de commande ``docker compose``.

À propos des images Docker
===========================

Les images Docker de |Fess| sont composées des composants suivants :

- **Fess** : Système de recherche plein texte principal
- **OpenSearch** : Moteur de recherche

Les images Docker officielles sont publiées sur `Docker Hub <https://hub.docker.com/r/codelibs/fess>`__.

Étape 1 : Obtention des fichiers Docker Compose
================================================

Pour le démarrage avec Docker Compose, les fichiers suivants sont nécessaires.

Méthode 1 : Téléchargement individuel des fichiers
---------------------------------------------------

Téléchargez les fichiers suivants :

::

    $ mkdir fess-docker
    $ cd fess-docker
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.5.0/compose/compose.yaml
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.5.0/compose/compose-opensearch3.yaml

Méthode 2 : Clonage du dépôt avec Git
--------------------------------------

Si Git est installé, vous pouvez également cloner l'ensemble du dépôt :

::

    $ git clone --depth 1 --branch v15.5.0 https://github.com/codelibs/docker-fess.git
    $ cd docker-fess/compose

Étape 2 : Vérification des fichiers Docker Compose
===================================================

Contenu de ``compose.yaml``
----------------------------

``compose.yaml`` contient la configuration de base de Fess.

Paramètres principaux :

- **Numéro de port** : Port de l'interface Web de Fess (par défaut : 8080)
- **Variables d'environnement** : Configuration de la taille du tas Java, etc.
- **Volumes** : Configuration de la persistance des données

Contenu de ``compose-opensearch3.yaml``
----------------------------------------

``compose-opensearch3.yaml`` contient la configuration d'OpenSearch.

Paramètres principaux :

- **Version d'OpenSearch** : Version d'OpenSearch à utiliser
- **Configuration mémoire** : Taille du tas JVM
- **Volumes** : Configuration de la persistance des données d'index

Personnalisation de la configuration (optionnel)
-------------------------------------------------

Si vous souhaitez modifier la configuration par défaut, modifiez ``compose.yaml``.

Exemple : Modification du numéro de port ::

    services:
      fess:
        ports:
          - "9080:8080"  # Mappage sur le port 9080 de l'hôte

Exemple : Modification de la configuration mémoire ::

    services:
      fess:
        environment:
          - "FESS_HEAP_SIZE=2g"  # Définir la taille du tas de Fess à 2 Go

Étape 3 : Démarrage des conteneurs Docker
==========================================

Démarrage de base
-----------------

Démarrez Fess et OpenSearch avec la commande suivante :

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   - L'option ``-f`` permet de spécifier plusieurs fichiers Compose
   - L'option ``-d`` permet d'exécuter en arrière-plan

Vérification des logs de démarrage ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f

Vous pouvez terminer l'affichage des logs avec ``Ctrl+C``.

Vérification du démarrage
--------------------------

Vérifiez l'état des conteneurs ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

Vérifiez que les conteneurs suivants sont en cours d'exécution :

- ``fess``
- ``opensearch``

.. tip::

   Le démarrage peut prendre quelques minutes.
   Attendez jusqu'à ce que le message « Fess is ready » ou similaire apparaisse dans les logs.

Étape 4 : Accès via un navigateur
==================================

Une fois le démarrage terminé, accédez aux URL suivantes :

- **Écran de recherche** : http://localhost:8080/
- **Écran d'administration** : http://localhost:8080/admin

Compte administrateur par défaut :

- Nom d'utilisateur : ``admin``
- Mot de passe : ``admin``

.. warning::

   **Note importante sur la sécurité**

   En environnement de production, veuillez obligatoirement changer le mot de passe administrateur.
   Pour plus de détails, consultez :doc:`security`.

Persistance des données
========================

Pour conserver les données même après la suppression des conteneurs Docker, des volumes sont automatiquement créés.

Vérification des volumes ::

    $ docker volume ls

Volumes liés à |Fess| :

- ``fess-es-data`` : Données d'index OpenSearch
- ``fess-data`` : Données de configuration de Fess

.. important::

   Les volumes ne sont pas supprimés même si les conteneurs sont supprimés.
   Pour supprimer les volumes, vous devez exécuter explicitement la commande ``docker volume rm``.

Arrêt des conteneurs Docker
============================

Arrêt des conteneurs ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop

Arrêt et suppression des conteneurs ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   La commande ``down`` supprime les conteneurs mais pas les volumes.
   Pour supprimer également les volumes, ajoutez l'option ``-v`` ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

   **Attention** : L'exécution de cette commande supprimera toutes les données.

Configuration avancée
=====================

Personnalisation des variables d'environnement
-----------------------------------------------

En ajoutant/modifiant des variables d'environnement dans ``compose.yaml``, vous pouvez effectuer des configurations détaillées.

Variables d'environnement principales :

.. list-table::
   :header-rows: 1
   :widths: 30 50

   * - Variable d'environnement
     - Description
   * - ``FESS_HEAP_SIZE``
     - Taille du tas JVM de Fess (par défaut : 1g)
   * - ``SEARCH_ENGINE_HTTP_URL``
     - Point de terminaison HTTP d'OpenSearch
   * - ``TZ``
     - Fuseau horaire (exemple : Europe/Paris)

Exemple ::

    environment:
      - "FESS_HEAP_SIZE=4g"
      - "TZ=Europe/Paris"

Comment appliquer les fichiers de configuration
------------------------------------------------

Les paramètres détaillés de |Fess| sont écrits dans le fichier ``fess_config.properties``.
Dans les environnements Docker, il existe les méthodes suivantes pour appliquer ces paramètres de fichier.

Méthode 1 : Monter le fichier de configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

En montant un répertoire contenant ``fess_config.properties`` et d'autres fichiers de configuration,
vous pouvez appliquer les paramètres modifiés côté hôte au conteneur.

1. Créez un répertoire de configuration sur l'hôte ::

       $ mkdir -p /path/to/fess-config

2. Obtenez le modèle du fichier de configuration (première fois uniquement) ::

       $ curl -o /path/to/fess-config/fess_config.properties https://raw.githubusercontent.com/codelibs/fess/refs/tags/fess-15.5.0/src/main/resources/fess_config.properties

3. Modifiez ``/path/to/fess-config/fess_config.properties`` et ajoutez les paramètres nécessaires ::

       # Exemple
       crawler.document.cache.enabled=false
       adaptive.load.control=20
       query.facet.fields=label,host

4. Ajoutez le montage de volume à ``compose.yaml`` ::

       services:
         fess:
           volumes:
             - /path/to/fess-config:/opt/fess/app/WEB-INF/conf

5. Démarrez le conteneur ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   ``fess_config.properties`` contient les paramètres de recherche, les paramètres du crawler,
   les paramètres de messagerie et d'autres configurations système.
   Même si vous supprimez les conteneurs avec ``docker compose down``, les fichiers côté hôte sont conservés.

Méthode 2 : Configuration via propriétés système
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Vous pouvez remplacer les éléments de configuration dans ``fess_config.properties`` via des variables d'environnement utilisant des propriétés système.

Les éléments de configuration écrits dans ``fess_config.properties`` (par exemple, ``crawler.document.cache.enabled=false``)
peuvent être spécifiés au format ``-Dfess.config.nom_paramètre=valeur``.

Ajoutez ``FESS_JAVA_OPTS`` aux variables d'environnement dans ``compose.yaml`` ::

    services:
      fess:
        environment:
          - "FESS_JAVA_OPTS=-Dfess.config.crawler.document.cache.enabled=false -Dfess.config.adaptive.load.control=20 -Dfess.config.query.facet.fields=label,host"

.. note::

   La partie suivant ``-Dfess.config.`` correspond au nom de l'élément de configuration dans ``fess_config.properties``.

Connexion à un OpenSearch externe
----------------------------------

Si vous utilisez un cluster OpenSearch existant, modifiez ``compose.yaml`` pour changer la destination de connexion.

1. N'utilisez pas ``compose-opensearch3.yaml`` ::

       $ docker compose -f compose.yaml up -d

2. Configurez ``SEARCH_ENGINE_HTTP_URL`` ::

       environment:
         - "SEARCH_ENGINE_HTTP_URL=http://your-opensearch-host:9200"

Configuration du réseau Docker
-------------------------------

Lors de l'intégration avec plusieurs services, vous pouvez utiliser un réseau personnalisé.

Exemple ::

    networks:
      fess-network:
        driver: bridge

    services:
      fess:
        networks:
          - fess-network

Exploitation en production avec Docker Compose
===============================================

Configuration recommandée pour l'utilisation de Docker Compose en environnement de production :

1. **Configuration des limitations de ressources** ::

       deploy:
         resources:
           limits:
             cpus: '2.0'
             memory: 4G
           reservations:
             cpus: '1.0'
             memory: 2G

2. **Configuration de la politique de redémarrage** ::

       restart: unless-stopped

3. **Configuration des logs** ::

       logging:
         driver: "json-file"
         options:
           max-size: "10m"
           max-file: "3"

4. **Activation de la configuration de sécurité**

   Activez le plugin de sécurité d'OpenSearch et configurez une authentification appropriée.
   Pour plus de détails, consultez :doc:`security`.

Dépannage
=========

Le conteneur ne démarre pas
----------------------------

1. Vérification des logs ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs

2. Vérification des conflits de ports ::

       $ sudo netstat -tuln | grep 8080
       $ sudo netstat -tuln | grep 9200

3. Vérification de l'espace disque ::

       $ df -h

Erreur de mémoire insuffisante
-------------------------------

Si OpenSearch ne démarre pas en raison d'une mémoire insuffisante, vous devez augmenter ``vm.max_map_count``.

Pour Linux ::

    $ sudo sysctl -w vm.max_map_count=262144

Pour une configuration permanente ::

    $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
    $ sudo sysctl -p

Initialisation des données
---------------------------

Pour supprimer toutes les données et revenir à l'état initial ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v
    $ docker volume prune

.. warning::

   L'exécution de cette commande supprimera complètement toutes les données.

Étapes suivantes
================

Une fois l'installation terminée, consultez les documents suivants :

- :doc:`run` - Démarrage de |Fess| et configuration initiale
- :doc:`security` - Configuration de la sécurité pour les environnements de production
- :doc:`troubleshooting` - Dépannage

Questions fréquemment posées
=============================

Q : Quelle est la taille des images Docker ?
---------------------------------------------

R : L'image Fess fait environ 1 Go, et l'image OpenSearch fait environ 800 Mo.
Le téléchargement peut prendre du temps lors du premier démarrage.

Q : Est-il possible d'exploiter sur Kubernetes ?
-------------------------------------------------

R : Oui, c'est possible. En convertissant les fichiers Docker Compose en manifestes Kubernetes,
ou en utilisant des charts Helm, vous pouvez exploiter sur Kubernetes.
Pour plus de détails, consultez la documentation officielle de Fess.

Q : Comment effectuer les mises à jour des conteneurs ?
--------------------------------------------------------

R : Suivez la procédure suivante pour les mises à jour :

1. Obtenir les derniers fichiers Compose
2. Arrêter les conteneurs ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

3. Obtenir les nouvelles images ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

4. Démarrer les conteneurs ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Q : Est-il possible d'avoir une configuration multi-nœuds ?
------------------------------------------------------------

R : Oui, c'est possible. En modifiant ``compose-opensearch3.yaml`` pour définir plusieurs nœuds OpenSearch,
vous pouvez créer une configuration en cluster. Cependant, pour les environnements de production, nous recommandons l'utilisation d'outils d'orchestration tels que Kubernetes.
