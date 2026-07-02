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

Lorsque vous démarrez |Fess| avec Docker Compose, les deux conteneurs suivants fonctionnent :

- **Fess** (``fess01``) : système de recherche plein texte principal
- **OpenSearch** (``search01``) : moteur de recherche

Les images Docker officielles sont publiées sur `GitHub Container Registry <https://github.com/codelibs/docker-fess/pkgs/container/fess>`__.
Les fichiers Compose et la procédure de démarrage sont gérés dans le dépôt `docker-fess <https://github.com/codelibs/docker-fess>`__.

Étape 1 : Obtention des fichiers Docker Compose
================================================

Pour le démarrage avec Docker Compose, les fichiers suivants sont nécessaires.

Méthode 1 : Téléchargement individuel des fichiers
---------------------------------------------------

Téléchargez les fichiers suivants :

::

    $ mkdir fess-docker
    $ cd fess-docker
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.7.0/compose/compose.yaml
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.7.0/compose/compose-opensearch3.yaml

Méthode 2 : Clonage du dépôt avec Git
--------------------------------------

Si Git est installé, vous pouvez également cloner l'ensemble du dépôt :

::

    $ git clone --depth 1 --branch v15.7.0 https://github.com/codelibs/docker-fess.git
    $ cd docker-fess/compose

Étape 2 : Vérification des fichiers Docker Compose
===================================================

Contenu de ``compose.yaml``
----------------------------

``compose.yaml`` contient la configuration de Fess lui-même (service ``fess01``).

Principaux paramètres :

- **Numéro de port** : port de l'interface Web de Fess (par défaut : 8080)
- **Variables d'environnement** : destination de connexion à OpenSearch (``SEARCH_ENGINE_HTTP_URL``), chemin du fichier de dictionnaire (``FESS_DICTIONARY_PATH``), etc.
- **Ordre de démarrage** : ``depends_on`` est configuré pour que le démarrage n'ait lieu qu'une fois qu'OpenSearch (``search01``) est dans un état sain

Contenu de ``compose-opensearch3.yaml``
----------------------------------------

``compose-opensearch3.yaml`` contient la configuration du moteur de recherche (service ``search01``, OpenSearch).

Principaux paramètres :

- **Image OpenSearch** : image OpenSearch utilisée (``ghcr.io/codelibs/fess-opensearch``)
- **Configuration mémoire** : taille du tas JVM
- **Volumes** : volumes de persistance des données (``search01_data`` : données d'index, ``search01_dictionary`` : fichiers de dictionnaire)

Personnalisation de la configuration (optionnel)
-------------------------------------------------

Pour modifier la configuration par défaut, éditez ``compose.yaml``.

Exemple : pour modifier le numéro de port ::

    services:
      fess01:
        ports:
          - "9080:8080"  # Mappage sur le port 9080 de l'hôte

Exemple : pour modifier la configuration mémoire ::

    services:
      fess01:
        environment:
          - "FESS_HEAP_SIZE=2g"  # Définir la taille du tas de Fess à 2 Go

Étape 3 : Démarrage des conteneurs Docker
==========================================

Démarrage de base
------------------

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
---------------------------

Vérifiez l'état des conteneurs ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

Vérifiez que les conteneurs suivants sont en cours d'exécution :

- ``fess01``
- ``search01``

.. tip::

   Le démarrage peut prendre quelques minutes. OpenSearch (``search01``) doit d'abord atteindre un état sain avant que Fess (``fess01``) ne démarre.
   Vérifiez l'état de chaque conteneur avec ``docker compose ... ps`` ; une fois que ``fess01`` a démarré, vous pouvez accéder à http://localhost:8080/ dans votre navigateur.

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

Activation du mode de recherche IA (plugins LLM)
=================================================

Depuis |Fess| 15.7, la fonctionnalité de mode de recherche IA (RAG Chat) a été séparée sous forme de plugins ``fess-llm-*``.
Le dépôt officiel `docker-fess <https://github.com/codelibs/docker-fess>`__ inclut des fichiers overlay pour les principaux fournisseurs de LLM.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Overlay
     - Usage
   * - ``compose-ollama.yaml``
     - Ollama (LLM local, démarre un service ``ollama01`` supplémentaire)
   * - ``compose-gemini.yaml``
     - Google Gemini (API cloud)
   * - ``compose-openai.yaml``
     - OpenAI (API cloud)

Chaque overlay récupère automatiquement le plugin correspondant via ``FESS_PLUGINS`` et active RAG Chat en définissant
``-Dfess.config.rag.chat.enabled=true`` dans ``FESS_JAVA_OPTS``.
Pour Gemini et OpenAI, qui font appel à une API cloud, le fournisseur à utiliser est en outre spécifié via ``-Dfess.system.rag.llm.name``,
et la clé API (``rag.llm.<provider>.api.key``) ainsi que le modèle (``rag.llm.<provider>.model``) sont configurés.
Pour Ollama, la valeur par défaut de ``rag.llm.name`` (``ollama``) est utilisée telle quelle, sans spécification explicite,
et la destination de connexion (``rag.llm.ollama.api.url``) est configurée.

Exemple d'utilisation de Gemini ::

    $ export GEMINI_API_KEY="AIzaSy..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-gemini.yaml up -d

Exemple d'utilisation d'OpenAI ::

    $ export OPENAI_API_KEY="sk-..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

.. note::

   Le modèle utilisé peut être modifié via les variables d'environnement ``GEMINI_MODEL`` et ``OPENAI_MODEL``
   (les valeurs par défaut sont respectivement ``gemini-2.5-flash`` et ``gpt-5-mini``).

Exemple d'utilisation d'Ollama ::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    $ docker exec -it ollama01 ollama pull gpt-oss:20b

.. warning::

   Le service ``ollama01`` de ``compose-ollama.yaml`` est configuré par défaut pour utiliser un GPU NVIDIA
   (le `NVIDIA Container Toolkit <https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html>`__ est requis).
   Si vous exécutez ce service dans un environnement sans GPU, supprimez ou commentez le bloc ``deploy:`` de ``compose-ollama.yaml`` (la spécification du GPU sous ``reservations``).

.. tip::

   Après le démarrage, l'écran de configuration « Système > Général » de l'écran d'administration permet de modifier
   le fournisseur LLM utilisé (``rag.llm.name``) ainsi que les paramètres spécifiques à chaque fournisseur. Cependant, ces
   modifications sont enregistrées dans le fichier de configuration à l'intérieur du conteneur et seront perdues si le
   conteneur est recréé (``docker compose down`` suivi de ``up``).
   Pour rendre la configuration persistante, spécifiez-la via ``FESS_JAVA_OPTS`` dans le fichier Compose, comme dans les exemples ci-dessus.

Persistance des données
========================

Toutes les données de |Fess| (index, documents explorés, informations utilisateur, configuration, etc.) sont stockées dans OpenSearch.
Ces données sont persistées dans les volumes d'OpenSearch, de sorte qu'elles sont conservées même après la suppression des conteneurs.
Le conteneur de Fess lui-même (``fess01``) est sans état et ne dispose d'aucun volume dédié.

Vérification des volumes ::

    $ docker volume ls

Principaux volumes définis dans ``compose-opensearch3.yaml`` :

- ``search01_data`` : données d'index d'OpenSearch (contenant l'ensemble des données de Fess)
- ``search01_dictionary`` : fichiers de dictionnaire

.. note::

   Les noms de volumes de Docker Compose sont préfixés par le nom du projet (par défaut, le nom du répertoire contenant le fichier Compose).
   Par exemple, si le démarrage a été effectué dans le répertoire ``compose``, le nom réel du volume sera de la forme ``compose_search01_data``.

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

   La commande ``down`` supprime les conteneurs, mais pas les volumes.
   Si vous souhaitez également supprimer les volumes (tels que ``search01_data``), ajoutez l'option ``-v`` ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

   **Attention** : l'exécution de cette commande supprime toutes les données stockées dans OpenSearch.

Configuration avancée
======================

Personnalisation des variables d'environnement
-------------------------------------------------

En ajoutant ou en modifiant des variables d'environnement dans ``compose.yaml``, vous pouvez effectuer une configuration détaillée.

Principales variables d'environnement :

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Variable d'environnement
     - Description
   * - ``FESS_HEAP_SIZE``
     - Taille du tas JVM de Fess (valeur par défaut de l'image Docker : 512m)
   * - ``FESS_JAVA_OPTS``
     - Spécification d'options JVM supplémentaires (par exemple pour remplacer des paramètres via ``-Dfess.config.*``)
   * - ``FESS_PLUGINS``
     - Plugins installés automatiquement au démarrage (format ``name:version`` séparés par des espaces. Exemple : ``fess-ds-wikipedia:15.7.0``)
   * - ``SEARCH_ENGINE_HTTP_URL``
     - Point de terminaison HTTP d'OpenSearch (valeur par défaut dans ``compose.yaml`` : ``http://search01:9200``)
   * - ``SEARCH_ENGINE_USERNAME`` / ``SEARCH_ENGINE_PASSWORD``
     - Informations d'identification pour se connecter à un OpenSearch avec authentification activée
   * - ``FESS_DICTIONARY_PATH``
     - Chemin du fichier de dictionnaire (répertoire partagé avec OpenSearch)
   * - ``FESS_PORT``
     - Port sur lequel Fess écoute à l'intérieur du conteneur (valeur par défaut : 8080)

Exemple ::

    services:
      fess01:
        environment:
          - "FESS_HEAP_SIZE=4g"

.. note::

   Pour changer le fuseau horaire, spécifiez-le dans ``FESS_JAVA_OPTS``, par exemple ``-Duser.timezone=Asia/Tokyo``.

Comment appliquer les fichiers de configuration
-------------------------------------------------

Les paramètres détaillés de |Fess| sont décrits dans le fichier ``fess_config.properties``.
Dans l'image Docker, ``fess_config.properties`` se trouve dans ``/etc/fess`` à l'intérieur du conteneur.
Voici les méthodes disponibles pour appliquer la configuration dans un environnement Docker.

Méthode 1 : Monter le fichier de configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``/etc/fess`` contient également d'autres fichiers de configuration nécessaires au fonctionnement de Fess ; remplacer directement ce répertoire par un montage entraîne un échec du démarrage.
Utilisez à la place le répertoire de substitution ``/opt/fess``, qui est ajouté en tête du classpath (il est vide au départ).

1. Créez, côté hôte, un répertoire destiné à contenir le fichier de configuration ::

       $ mkdir -p /path/to/fess-config

2. Récupérez le modèle du fichier de configuration (uniquement la première fois) ::

       $ curl -o /path/to/fess-config/fess_config.properties https://raw.githubusercontent.com/codelibs/fess/refs/tags/fess-15.7.0/src/main/resources/fess_config.properties

3. Modifiez ``/path/to/fess-config/fess_config.properties`` pour y décrire les paramètres nécessaires ::

       # Exemple
       crawler.document.cache.enabled=false
       adaptive.load.control=20
       query.facet.fields=label,host

4. Ajoutez un montage de volume au service ``fess01`` dans ``compose.yaml`` ::

       services:
         fess01:
           volumes:
             - /path/to/fess-config/fess_config.properties:/opt/fess/fess_config.properties

5. Démarrez le conteneur ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   ``/opt/fess`` étant ajouté en tête du classpath, le fichier ``fess_config.properties`` placé ici est prioritaire
   par rapport à celui fourni avec l'image, ``/etc/fess/fess_config.properties``.
   Les fichiers de propriétés sont chargés fichier par fichier et ne sont pas fusionnés élément par élément.
   Il est donc nécessaire de placer un **fichier complet contenant tous les paramètres de configuration**, et pas seulement ceux que vous souhaitez remplacer.
   Si vous souhaitez ne modifier que certains éléments, utilisez la « Méthode 2 » ci-dessous.

Méthode 2 : Configuration via propriétés système
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Vous pouvez remplacer les paramètres de ``fess_config.properties`` sous forme de propriétés système, via des variables d'environnement.

Les paramètres décrits dans ``fess_config.properties`` (par exemple ``crawler.document.cache.enabled=false``) sont spécifiés
au format ``-Dfess.config.nom_du_paramètre=valeur``.

Ajoutez ``FESS_JAVA_OPTS`` aux variables d'environnement du service ``fess01`` dans ``compose.yaml`` ::

    services:
      fess01:
        environment:
          - "FESS_JAVA_OPTS=-Dfess.config.crawler.document.cache.enabled=false -Dfess.config.adaptive.load.control=20 -Dfess.config.query.facet.fields=label,host"

.. note::

   La partie qui suit ``-Dfess.config.`` correspond au nom du paramètre dans ``fess_config.properties``.
   Cette méthode est plus simple si vous souhaitez ne remplacer que certains éléments.

Connexion à un OpenSearch externe
------------------------------------

Si vous souhaitez utiliser un cluster OpenSearch existant, démarrez uniquement avec ``compose.yaml`` sans utiliser ``compose-opensearch3.yaml``, et modifiez la destination de connexion.

1. Démarrez sans spécifier ``compose-opensearch3.yaml`` ::

       $ docker compose -f compose.yaml up -d

2. Configurez la destination de connexion dans le service ``fess01`` de ``compose.yaml`` ::

       environment:
         - "SEARCH_ENGINE_HTTP_URL=http://your-opensearch-host:9200"

.. note::

   Si vous vous connectez à un OpenSearch avec authentification activée, spécifiez également ``SEARCH_ENGINE_USERNAME`` et ``SEARCH_ENGINE_PASSWORD``.

Autres overlays et configurations
------------------------------------

Le dépôt ``docker-fess`` contient également, en plus de ceux mentionnés ci-dessus, d'autres fichiers Compose et répertoires spécifiques à certains usages.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Fichier / Répertoire
     - Usage
   * - ``compose-dashboards3.yaml``
     - Ajoute OpenSearch Dashboards (port 5601, pour la visualisation des données)
   * - ``compose-minio.yaml``
     - Ajoute MinIO (stockage objet) et l'utilise comme destination de stockage pour la fonctionnalité de stockage de Fess
   * - ``vanilla/``
     - Configuration combinée avec un OpenSearch standard ne comportant pas les plugins pour Fess (certaines fonctionnalités, comme la gestion du dictionnaire, ne sont pas disponibles)
   * - ``snapshot/``
     - Configuration utilisant des images de développement (snapshot) (inclut une configuration en cluster et une combinaison avec Elasticsearch 8)
   * - ``multi-instance/``
     - Configuration démarrant plusieurs instances de Fess partageant un seul OpenSearch

Configuration du réseau Docker
---------------------------------

Si vous devez intégrer plusieurs services, vous pouvez utiliser un réseau personnalisé.

Exemple ::

    networks:
      fess-network:
        driver: bridge

    services:
      fess01:
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

Q : Quel espace disque est nécessaire pour le téléchargement des images ?
---------------------------------------------------------------------------

R : Les images de Fess et d'OpenSearch sont téléchargées lors du premier démarrage et nécessitent au total quelques Go d'espace disque.
Le téléchargement peut prendre du temps selon l'environnement réseau.

Q : Est-il possible d'exploiter Fess sur Kubernetes ?
--------------------------------------------------------

R : Oui, c'est possible. Vous pouvez convertir les fichiers Docker Compose en manifestes Kubernetes à l'aide d'un outil tel que ``kompose``,
ou créer vos propres manifestes pour l'exploitation (aucun chart Helm officiel n'est fourni).

Q : Comment effectuer les mises à jour des conteneurs ?
-----------------------------------------------------------

R : Suivez la procédure suivante pour les mises à jour :

1. Obtenir les derniers fichiers Compose
2. Arrêter les conteneurs ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

3. Obtenir les nouvelles images ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

4. Démarrer les conteneurs ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Q : Une configuration multi-nœuds est-elle possible ?
--------------------------------------------------------

R : Oui, c'est possible. Vous pouvez vous appuyer sur ``snapshot/compose-cluster.yaml`` du dépôt ``docker-fess`` pour configurer OpenSearch avec plusieurs nœuds,
ou sur ``multi-instance/`` pour configurer plusieurs instances de Fess partageant un seul OpenSearch.
Cependant, pour les environnements de production, nous recommandons l'utilisation d'outils d'orchestration tels que Kubernetes.
