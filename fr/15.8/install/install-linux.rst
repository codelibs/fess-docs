================================================
Installation sur Linux (Procédure détaillée)
================================================

Cette page décrit la procédure d'installation de |Fess| sur un environnement Linux.
Elle prend en charge les formats de packages TAR.GZ, RPM et DEB.

.. warning::

   Pour les environnements de production, l'utilisation d'OpenSearch intégré n'est pas recommandée.
   Veillez impérativement à mettre en place un serveur OpenSearch externe.

Prérequis
=========

- La configuration requise décrite dans :doc:`prerequisites` doit être satisfaite
- Java 21 doit être installé
- OpenSearch 3.7.0 doit être disponible (ou nouvelle installation)

Choix de la méthode d'installation
===================================

Pour les environnements Linux, vous pouvez choisir parmi les méthodes d'installation suivantes :

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Méthode
     - Environnement recommandé
     - Caractéristiques
   * - TAR.GZ
     - Environnement de développement, environnement nécessitant une personnalisation
     - Peut être déployé dans un répertoire arbitraire
   * - RPM
     - Systèmes RHEL, CentOS, Fedora
     - Gestion des services possible avec systemd
   * - DEB
     - Systèmes Debian, Ubuntu
     - Gestion des services possible avec systemd

Configuration système pour l'exécution d'OpenSearch
=====================================================

Pour qu'OpenSearch fonctionne de manière stable sous Linux, configurez les paramètres du noyau et les limites de ressources suivants.
Ces réglages sont principalement nécessaires pour la version TAR.GZ (lorsque OpenSearch est installé manuellement).
Avec les versions RPM / DEB, les packages OpenSearch et |Fess| configurent notamment le nombre de descripteurs de fichiers via systemd, mais comme ``vm.max_map_count`` est un paramètre du noyau côté hôte, vérifiez-le quelle que soit la méthode utilisée.

Nombre maximal de mappages de mémoire virtuelle
------------------------------------------------

OpenSearch utilise un grand nombre de mappages mémoire ; définissez donc ``vm.max_map_count`` à ``262144`` ou plus.

Pour une configuration temporaire ::

    $ sudo sysctl -w vm.max_map_count=262144

Pour une configuration permanente ::

    $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
    $ sudo sysctl -p

Nombre de descripteurs de fichiers
------------------------------------

Lorsque vous exécutez OpenSearch manuellement (version TAR.GZ), définissez la limite du nombre de descripteurs de fichiers de l'utilisateur exécutant OpenSearch à ``65535`` ou plus.

Ajoutez ce qui suit dans ``/etc/security/limits.conf`` (remplacez ``opensearch`` par le nom de l'utilisateur exécutant OpenSearch) ::

    opensearch  -  nofile  65535

.. note::

   Avec les versions RPM / DEB, cette configuration n'est pas nécessaire, car la limite du nombre de descripteurs de fichiers est définie dans la définition du service systemd.

Installation avec la version TAR.GZ
=====================================

Étape 1 : Installation d'OpenSearch
--------------------------------------

1. Téléchargement d'OpenSearch

   Téléchargez la version TAR.GZ depuis `Download OpenSearch <https://opensearch.org/downloads.html>`__.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.7.0/opensearch-3.7.0-linux-x64.tar.gz
       $ tar -xzf opensearch-3.7.0-linux-x64.tar.gz
       $ cd opensearch-3.7.0

   .. note::

      Cet exemple utilise OpenSearch 3.7.0.
      |Fess| 15.8 est compatible avec OpenSearch 3.7.0.

2. Installation des plugins OpenSearch

   Installez les plugins requis par |Fess|.

   ::

       $ cd /path/to/opensearch-3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

   .. important::

      Les versions des plugins doivent correspondre à la version d'OpenSearch.
      Dans l'exemple ci-dessus, toutes sont spécifiées en 3.7.0.

3. Configuration d'OpenSearch

   Ajoutez les paramètres suivants dans ``config/opensearch.yml``.

   ::

       # Chemin pour la synchronisation de configuration (spécifier en chemin absolu)
       configsync.config_path: /path/to/opensearch-3.7.0/data/config/

       # Désactivation du plugin de sécurité (environnement de développement uniquement)
       plugins.security.disabled: true

   .. warning::

      **Remarque importante concernant la sécurité**

      ``plugins.security.disabled: true`` ne doit être utilisé que dans les environnements de développement ou de test.
      Pour les environnements de production, activez le plugin de sécurité d'OpenSearch et configurez une authentification et une autorisation appropriées.
      Si vous activez le plugin de sécurité avec OpenSearch 2.12 ou une version ultérieure, vous devez définir un mot de passe administrateur (variable d'environnement ``OPENSEARCH_INITIAL_ADMIN_PASSWORD``) lors du premier démarrage.
      Pour plus de détails, consultez :doc:`security`.

   .. tip::

      Vous pouvez ajuster d'autres paramètres tels que le nom du cluster et la configuration réseau en fonction de votre environnement.
      Exemple de configuration ::

          cluster.name: fess-cluster
          node.name: fess-node-1
          network.host: 0.0.0.0
          discovery.type: single-node

   .. tip::

      La taille du tas (heap) d'OpenSearch se configure via ``-Xms`` / ``-Xmx`` dans ``config/jvm.options``.
      Il est recommandé d'utiliser une valeur inférieure ou égale à la moitié de la mémoire physique disponible, et inférieure à 32 Go, en indiquant la même valeur pour ``-Xms`` et ``-Xmx``.

Étape 2 : Installation de Fess
---------------------------------

1. Téléchargement et décompression de Fess

   Téléchargez la version TAR.GZ depuis le `site de téléchargement <https://fess.codelibs.org/fr/downloads.html>`__.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.8.0/fess-15.8.0.tar.gz
       $ tar -xzf fess-15.8.0.tar.gz
       $ cd fess-15.8.0

2. Configuration de Fess

   Modifiez ``bin/fess.in.sh`` pour configurer les informations de connexion à OpenSearch.
   Ce fichier contient, à l'état commenté, les paramètres permettant de se connecter à un cluster OpenSearch externe.

   ::

       $ vi bin/fess.in.sh

   Décommentez (supprimez le ``#`` en début de ligne) les deux lignes suivantes, situées près du début du fichier.

   Avant modification (état par défaut) ::

       # External opensearch cluster
       #SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       #FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

   Après modification ::

       # External opensearch cluster
       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/path/to/opensearch-3.7.0/data/config/

   .. note::

      - Définissez pour ``FESS_DICTIONARY_PATH`` le même chemin que celui indiqué dans ``configsync.config_path`` du fichier ``opensearch.yml`` d'OpenSearch.
      - Si OpenSearch s'exécute sur un autre hôte, remplacez ``SEARCH_ENGINE_HTTP_URL`` par le nom d'hôte ou l'adresse IP appropriés. Exemple : ``SEARCH_ENGINE_HTTP_URL=http://192.168.1.100:9200``
      - N'ajoutez pas une nouvelle ligne ``SEARCH_ENGINE_HTTP_URL=...`` ; décommentez et modifiez plutôt la ligne existante.

   .. tip::

      Pour modifier la taille du tas (heap) de |Fess|, modifiez ``FESS_MIN_MEM`` (par défaut : ``256m``) et ``FESS_MAX_MEM`` (par défaut : ``2g``) dans ``bin/fess.in.sh``, ou définissez la variable d'environnement ``FESS_HEAP_SIZE``.

3. Vérification de l'installation

   Vérifiez que le fichier de configuration a été correctement modifié ::

       $ grep "SEARCH_ENGINE_HTTP_URL" bin/fess.in.sh
       $ grep "FESS_DICTIONARY_PATH" bin/fess.in.sh

Étape 3 : Démarrage
----------------------

Pour la procédure de démarrage, consultez :doc:`run`.

Installation avec la version RPM
===================================

La version RPM est utilisée sur les distributions Linux basées sur RPM telles que Red Hat Enterprise Linux, CentOS, Fedora, etc.

Étape 1 : Installation d'OpenSearch
--------------------------------------

1. Téléchargement et installation du RPM OpenSearch

   Téléchargez et installez le package RPM depuis `Download OpenSearch <https://opensearch.org/downloads.html>`__.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.7.0/opensearch-3.7.0-linux-x64.rpm
       $ sudo rpm -ivh opensearch-3.7.0-linux-x64.rpm

   Vous pouvez également ajouter un dépôt pour l'installation.
   Pour plus de détails, consultez `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/rpm/>`__.

2. Installation des plugins OpenSearch

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

3. Configuration d'OpenSearch

   Ajoutez les paramètres suivants dans ``/etc/opensearch/opensearch.yml``.

   ::

       $ sudo vi /etc/opensearch/opensearch.yml

   Paramètres à ajouter ::

       configsync.config_path: /var/lib/opensearch/data/config/
       plugins.security.disabled: true

   .. warning::

      N'utilisez pas ``plugins.security.disabled: true`` en environnement de production.
      Consultez :doc:`security` pour configurer une sécurité appropriée.

Étape 2 : Installation de Fess
---------------------------------

1. Installation du RPM Fess

   Téléchargez et installez le package RPM depuis le `site de téléchargement <https://fess.codelibs.org/fr/downloads.html>`__.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.8.0/fess-15.8.0.rpm
       $ sudo rpm -ivh fess-15.8.0.rpm

2. Configuration de Fess

   Pour la version RPM, modifiez le fichier de configuration des variables d'environnement ``/etc/sysconfig/fess``.
   Ce fichier est conservé lors des mises à niveau du package (ne modifiez pas directement ``/usr/share/fess/bin/fess.in.sh``, car il est écrasé lors des mises à niveau).

   ::

       $ sudo vi /etc/sysconfig/fess

   Configurez les informations de connexion à OpenSearch. Les valeurs par défaut sont les suivantes. Modifiez-les si nécessaire ::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

   .. note::

      Indiquez pour ``FESS_DICTIONARY_PATH`` le même chemin que celui défini dans ``configsync.config_path`` du fichier ``opensearch.yml``.

3. Enregistrement et activation du service

   Activez les services à l'aide de systemd (systemd est standard à partir de RHEL 8 et CentOS 8) ::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

   .. note::

      Le service |Fess| dépend du service OpenSearch ; OpenSearch doit donc être démarré en premier.

   .. note::

      Dans les environnements traditionnels n'utilisant pas systemd, vous pouvez enregistrer |Fess| avec ``chkconfig`` ::

          $ sudo /sbin/chkconfig --add fess

Étape 3 : Démarrage
----------------------

Pour la procédure de démarrage, consultez :doc:`run`.

Installation avec la version DEB
===================================

La version DEB est utilisée sur les distributions Linux basées sur DEB telles que Debian, Ubuntu, etc.

Étape 1 : Installation d'OpenSearch
--------------------------------------

1. Téléchargement et installation du DEB OpenSearch

   Téléchargez et installez le package DEB depuis `Download OpenSearch <https://opensearch.org/downloads.html>`__.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.7.0/opensearch-3.7.0-linux-x64.deb
       $ sudo dpkg -i opensearch-3.7.0-linux-x64.deb

   Vous pouvez également ajouter un dépôt pour l'installation.
   Pour plus de détails, consultez `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/debian/>`__.

2. Installation des plugins OpenSearch

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

3. Configuration d'OpenSearch

   Ajoutez les paramètres suivants dans ``/etc/opensearch/opensearch.yml``.

   ::

       $ sudo vi /etc/opensearch/opensearch.yml

   Paramètres à ajouter ::

       configsync.config_path: /var/lib/opensearch/data/config/
       plugins.security.disabled: true

   .. warning::

      N'utilisez pas ``plugins.security.disabled: true`` en environnement de production.
      Consultez :doc:`security` pour configurer une sécurité appropriée.

Étape 2 : Installation de Fess
---------------------------------

1. Installation du DEB Fess

   Téléchargez et installez le package DEB depuis le `site de téléchargement <https://fess.codelibs.org/fr/downloads.html>`__.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.8.0/fess-15.8.0.deb
       $ sudo dpkg -i fess-15.8.0.deb

2. Configuration de Fess

   Pour la version DEB, modifiez le fichier de configuration des variables d'environnement ``/etc/default/fess``.
   Ce fichier est conservé lors des mises à niveau du package (ne modifiez pas directement ``/usr/share/fess/bin/fess.in.sh``, car il est écrasé lors des mises à niveau).

   ::

       $ sudo vi /etc/default/fess

   Configurez les informations de connexion à OpenSearch. Les valeurs par défaut sont les suivantes. Modifiez-les si nécessaire ::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

   .. note::

      Indiquez pour ``FESS_DICTIONARY_PATH`` le même chemin que celui défini dans ``configsync.config_path`` du fichier ``opensearch.yml``.

3. Enregistrement et activation du service

   Activez le service à l'aide de systemd ::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

   .. note::

      Le service |Fess| dépend du service OpenSearch ; OpenSearch doit donc être démarré en premier.

Étape 3 : Démarrage
----------------------

Pour la procédure de démarrage, consultez :doc:`run`.

Vérification après l'installation
====================================

Une fois l'installation terminée, veuillez vérifier les éléments suivants :

1. **Vérification des fichiers de configuration**

   - Fichier de configuration d'OpenSearch (opensearch.yml)
   - Fichier de configuration de |Fess|

     - Version TAR.GZ : ``bin/fess.in.sh``
     - Version RPM : ``/etc/sysconfig/fess``
     - Version DEB : ``/etc/default/fess``

2. **Permissions des répertoires**

   Vérifiez que le répertoire spécifié dans la configuration (``configsync.config_path`` / ``FESS_DICTIONARY_PATH``) existe et dispose des permissions appropriées.

   Pour la version TAR.GZ ::

       $ ls -ld /path/to/opensearch-3.7.0/data/config/

   Pour les versions RPM/DEB ::

       $ sudo ls -ld /var/lib/opensearch/data/config/

3. **Vérification des paramètres du noyau**

   ::

       $ sysctl vm.max_map_count

   Vérifiez que la valeur est ``262144`` ou plus.

4. **Vérification de la version de Java**

   ::

       $ java -version

   Vérifiez que Java 21 ou une version ultérieure est installé.

Étapes suivantes
================

Une fois l'installation terminée, consultez les documents suivants :

- :doc:`run` - Démarrage de |Fess| et configuration initiale
- :doc:`security` - Configuration de la sécurité pour les environnements de production
- :doc:`troubleshooting` - Dépannage

Questions fréquemment posées
=============================

Q : D'autres versions d'OpenSearch fonctionnent-elles ?
------------------------------------------------------------------

R : |Fess| dépend d'une version spécifique d'OpenSearch.
Pour garantir la compatibilité des plugins, il est fortement recommandé d'utiliser la version recommandée (3.7.0).
Si vous utilisez une autre version, vous devrez également ajuster les versions des plugins de manière appropriée.

Q : Peut-on partager le même OpenSearch avec plusieurs instances Fess ?
------------------------------------------------------------------------

R : C'est possible, mais ce n'est pas recommandé. Nous recommandons de prévoir un cluster OpenSearch dédié pour chaque instance Fess.
Si vous partagez OpenSearch avec plusieurs instances Fess, faites attention aux collisions de noms d'index.

Q : Comment configurer OpenSearch en cluster ?
-----------------------------------------------

R : Consultez la documentation officielle d'OpenSearch `Cluster formation <https://opensearch.org/docs/latest/tuning-your-cluster/cluster/>`__.
Pour une configuration en cluster, vous devez supprimer le paramètre ``discovery.type: single-node`` et ajouter une configuration de cluster appropriée.
