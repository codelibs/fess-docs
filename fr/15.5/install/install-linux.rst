=======================================
Installation sur Linux (Procédure détaillée)
=======================================

Cette page décrit la procédure d'installation de |Fess| sur un environnement Linux.
Elle couvre les formats de packages TAR.GZ, RPM et DEB.

.. warning::

   Pour les environnements de production, nous ne recommandons pas l'utilisation d'OpenSearch intégré.
   Veuillez obligatoirement configurer un serveur OpenSearch externe.

Prérequis
=========

- La configuration requise décrite dans :doc:`prerequisites` doit être satisfaite
- Java 21 doit être installé
- OpenSearch 3.3.2 doit être disponible (ou nouvelle installation)

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

Installation avec la version TAR.GZ
===================================

Étape 1 : Installation d'OpenSearch
------------------------------------

1. Téléchargement d'OpenSearch

   Téléchargez la version TAR.GZ depuis `Download OpenSearch <https://opensearch.org/downloads.html>`__.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.3.2/opensearch-3.3.2-linux-x64.tar.gz
       $ tar -xzf opensearch-3.3.2-linux-x64.tar.gz
       $ cd opensearch-3.3.2

   .. note::

      Cet exemple utilise OpenSearch 3.3.2.
      Veuillez vérifier la version compatible avec |Fess|.

2. Installation des plugins OpenSearch

   Installez les plugins requis par |Fess|.

   ::

       $ cd /path/to/opensearch-3.3.2
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.1
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.1
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.1
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.1

   .. important::

      Les versions des plugins doivent correspondre à la version d'OpenSearch.
      Dans l'exemple ci-dessus, toutes sont spécifiées en 3.3.2.

3. Configuration d'OpenSearch

   Ajoutez les paramètres suivants dans ``config/opensearch.yml``.

   ::

       # Chemin pour la synchronisation de configuration (spécifier en chemin absolu)
       configsync.config_path: /path/to/opensearch-3.3.2/data/config/

       # Désactivation du plugin de sécurité (environnement de développement uniquement)
       plugins.security.disabled: true

   .. warning::

      **Note importante sur la sécurité**

      ``plugins.security.disabled: true`` ne doit être utilisé que dans les environnements de développement ou de test.
      Pour les environnements de production, veuillez activer le plugin de sécurité d'OpenSearch et configurer une authentification et une autorisation appropriées.
      Pour plus de détails, consultez :doc:`security`.

   .. tip::

      Vous pouvez ajuster d'autres paramètres tels que le nom du cluster et la configuration réseau en fonction de votre environnement.
      Exemple de configuration ::

          cluster.name: fess-cluster
          node.name: fess-node-1
          network.host: 0.0.0.0
          discovery.type: single-node

Étape 2 : Installation de Fess
-------------------------------

1. Téléchargement et décompression de Fess

   Téléchargez la version TAR.GZ depuis le `site de téléchargement <https://fess.codelibs.org/ja/downloads.html>`__.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.5.0/fess-15.5.0.tar.gz
       $ tar -xzf fess-15.5.0.tar.gz
       $ cd fess-15.5.0

2. Configuration de Fess

   Modifiez ``bin/fess.in.sh`` pour configurer les informations de connexion à OpenSearch.

   ::

       $ vi bin/fess.in.sh

   Ajoutez ou modifiez les paramètres suivants ::

       # Point de terminaison HTTP d'OpenSearch
       SEARCH_ENGINE_HTTP_URL=http://localhost:9200

       # Chemin de placement des fichiers de dictionnaire (identique à configsync.config_path d'OpenSearch)
       FESS_DICTIONARY_PATH=/path/to/opensearch-3.3.2/data/config/

   .. note::

      Si vous exécutez OpenSearch sur un autre hôte,
      modifiez ``SEARCH_ENGINE_HTTP_URL`` avec le nom d'hôte ou l'adresse IP appropriés.
      Exemple : ``SEARCH_ENGINE_HTTP_URL=http://192.168.1.100:9200``

3. Vérification de l'installation

   Vérifiez que les fichiers de configuration ont été correctement modifiés ::

       $ grep "SEARCH_ENGINE_HTTP_URL" bin/fess.in.sh
       $ grep "FESS_DICTIONARY_PATH" bin/fess.in.sh

Étape 3 : Démarrage
-------------------

Pour la procédure de démarrage, consultez :doc:`run`.

Installation avec la version RPM
=================================

La version RPM est utilisée sur les distributions Linux basées sur RPM telles que Red Hat Enterprise Linux, CentOS, Fedora, etc.

Étape 1 : Installation d'OpenSearch
------------------------------------

1. Téléchargement et installation du RPM OpenSearch

   Téléchargez et installez le package RPM depuis `Download OpenSearch <https://opensearch.org/downloads.html>`__.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.3.2/opensearch-3.3.2-linux-x64.rpm
       $ sudo rpm -ivh opensearch-3.3.2-linux-x64.rpm

   Vous pouvez également ajouter un dépôt pour l'installation.
   Pour plus de détails, consultez `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/rpm/>`__.

2. Installation des plugins OpenSearch

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.1

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
-------------------------------

1. Installation du RPM Fess

   Téléchargez et installez le package RPM depuis le `site de téléchargement <https://fess.codelibs.org/ja/downloads.html>`__.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.5.0/fess-15.5.0.rpm
       $ sudo rpm -ivh fess-15.5.0.rpm

2. Configuration de Fess

   Modifiez ``/usr/share/fess/bin/fess.in.sh``.

   ::

       $ sudo vi /usr/share/fess/bin/fess.in.sh

   Ajoutez ou modifiez les paramètres suivants ::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

3. Enregistrement du service

   **Si vous utilisez chkconfig** ::

       $ sudo /sbin/chkconfig --add opensearch
       $ sudo /sbin/chkconfig --add fess

   **Si vous utilisez systemd** (recommandé) ::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

Étape 3 : Démarrage
-------------------

Pour la procédure de démarrage, consultez :doc:`run`.

Installation avec la version DEB
=================================

La version DEB est utilisée sur les distributions Linux basées sur DEB telles que Debian, Ubuntu, etc.

Étape 1 : Installation d'OpenSearch
------------------------------------

1. Téléchargement et installation du DEB OpenSearch

   Téléchargez et installez le package DEB depuis `Download OpenSearch <https://opensearch.org/downloads.html>`__.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.3.2/opensearch-3.3.2-linux-x64.deb
       $ sudo dpkg -i opensearch-3.3.2-linux-x64.deb

   Vous pouvez également ajouter un dépôt pour l'installation.
   Pour plus de détails, consultez `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/debian/>`__.

2. Installation des plugins OpenSearch

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.1

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
-------------------------------

1. Installation du DEB Fess

   Téléchargez et installez le package DEB depuis le `site de téléchargement <https://fess.codelibs.org/ja/downloads.html>`__.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.5.0/fess-15.5.0.deb
       $ sudo dpkg -i fess-15.5.0.deb

2. Configuration de Fess

   Modifiez ``/usr/share/fess/bin/fess.in.sh``.

   ::

       $ sudo vi /usr/share/fess/bin/fess.in.sh

   Ajoutez ou modifiez les paramètres suivants ::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

3. Enregistrement du service

   Activez le service avec systemd ::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

Étape 3 : Démarrage
-------------------

Pour la procédure de démarrage, consultez :doc:`run`.

Vérification après l'installation
==================================

Une fois l'installation terminée, veuillez vérifier les éléments suivants :

1. **Vérification des fichiers de configuration**

   - Fichier de configuration d'OpenSearch (opensearch.yml)
   - Fichier de configuration de Fess (fess.in.sh)

2. **Permissions des répertoires**

   Vérifiez que les répertoires spécifiés dans la configuration existent et ont les permissions appropriées.

   Pour la version TAR.GZ ::

       $ ls -ld /path/to/opensearch-3.3.2/data/config/

   Pour les versions RPM/DEB ::

       $ sudo ls -ld /var/lib/opensearch/data/config/

3. **Vérification de la version de Java**

   ::

       $ java -version

   Vérifiez que Java 21 ou ultérieur est installé.

Étapes suivantes
================

Une fois l'installation terminée, consultez les documents suivants :

- :doc:`run` - Démarrage de |Fess| et configuration initiale
- :doc:`security` - Configuration de la sécurité pour les environnements de production
- :doc:`troubleshooting` - Dépannage

Questions fréquemment posées
=============================

Q : D'autres versions d'OpenSearch fonctionnent-elles ?
--------------------------------------------------------

R : |Fess| dépend d'une version spécifique d'OpenSearch.
Pour garantir la compatibilité des plugins, il est fortement recommandé d'utiliser la version recommandée (3.3.2).
Si vous utilisez une autre version, vous devrez également ajuster les versions des plugins de manière appropriée.

Q : Peut-on partager le même OpenSearch avec plusieurs instances Fess ?
------------------------------------------------------------------------

R : C'est possible, mais ce n'est pas recommandé. Nous recommandons de prévoir un cluster OpenSearch dédié pour chaque instance Fess.
Si vous partagez OpenSearch avec plusieurs instances Fess, faites attention aux collisions de noms d'index.

Q : Comment configurer OpenSearch en cluster ?
-----------------------------------------------

R : Consultez la documentation officielle d'OpenSearch `Cluster formation <https://opensearch.org/docs/latest/tuning-your-cluster/cluster/>`__.
Pour une configuration en cluster, vous devez supprimer le paramètre ``discovery.type: single-node`` et ajouter une configuration de cluster appropriée.
