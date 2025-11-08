====================
Configuration requise
====================

Cette page décrit la configuration matérielle et logicielle requise pour exécuter |Fess|.

Configuration matérielle
========================

Configuration minimale
----------------------

Voici la configuration minimale pour les environnements d'évaluation et de développement :

- Processeur : 2 cœurs ou plus
- Mémoire : 4 Go ou plus
- Espace disque : 10 Go d'espace libre ou plus

Configuration recommandée
-------------------------

Pour les environnements de production, nous recommandons les spécifications suivantes :

- Processeur : 4 cœurs ou plus
- Mémoire : 8 Go ou plus (à augmenter en fonction de la taille de l'index)
- Espace disque :

  - Zone système : 20 Go ou plus
  - Zone de données : 3 fois la taille de l'index ou plus (réplicas inclus)

- Réseau : 1 Gbit/s ou plus

.. note::

   Si la taille de l'index devient importante ou si vous effectuez des explorations à haute fréquence,
   veuillez augmenter la mémoire et l'espace disque de manière appropriée.

Configuration logicielle
========================

Système d'exploitation
----------------------

|Fess| fonctionne sur les systèmes d'exploitation suivants :

**Linux**

- Red Hat Enterprise Linux 8 ou ultérieur
- CentOS 8 ou ultérieur
- Ubuntu 20.04 LTS ou ultérieur
- Debian 11 ou ultérieur
- Autres distributions Linux (environnement capable d'exécuter Java 21)

**Windows**

- Windows Server 2019 ou ultérieur
- Windows 10 ou ultérieur

**Autres**

- macOS 11 (Big Sur) ou ultérieur (recommandé pour les environnements de développement uniquement)
- Environnement capable d'exécuter Docker

Logiciels requis
----------------

Selon la méthode d'installation, les logiciels suivants sont nécessaires :

Version TAR.GZ/ZIP/RPM/DEB
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Java 21** : `Eclipse Temurin <https://adoptium.net/temurin>`__ recommandé

  - OpenJDK 21 ou ultérieur
  - Eclipse Temurin 21 ou ultérieur

- **OpenSearch 3.3.0** : Obligatoire pour les environnements de production (la version intégrée est déconseillée)

  - Version compatible : OpenSearch 3.3.0
  - Attention à la compatibilité des plugins avec les autres versions

Version Docker
~~~~~~~~~~~~~~

- **Docker** : 20.10 ou ultérieur
- **Docker Compose** : 2.0 ou ultérieur

Configuration réseau
====================

Ports requis
------------

Les ports principaux utilisés par |Fess| sont les suivants :

.. list-table::
   :header-rows: 1
   :widths: 15 15 50

   * - Port
     - Protocole
     - Utilisation
   * - 8080
     - HTTP
     - Interface Web |Fess| (écran de recherche/écran d'administration)
   * - 9200
     - HTTP
     - API HTTP OpenSearch (communication de |Fess| vers OpenSearch)
   * - 9300
     - TCP
     - Communication de transport OpenSearch (lors de la configuration en cluster)

.. warning::

   En environnement de production, il est fortement recommandé de restreindre l'accès direct depuis l'extérieur aux ports 9200 et 9300.
   Ces ports ne doivent être utilisés que pour la communication interne entre |Fess| et OpenSearch.

Configuration du pare-feu
-------------------------

Si vous souhaitez rendre |Fess| accessible depuis l'extérieur, vous devez ouvrir le port 8080.

**Linux (avec firewalld)**

::

    $ sudo firewall-cmd --permanent --add-port=8080/tcp
    $ sudo firewall-cmd --reload

**Linux (avec iptables)**

::

    $ sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
    $ sudo iptables-save

Navigateurs Web compatibles
============================

Nous recommandons les navigateurs suivants pour l'écran d'administration et l'écran de recherche de |Fess| :

- Google Chrome (dernière version)
- Mozilla Firefox (dernière version)
- Microsoft Edge (dernière version)
- Safari (dernière version)

.. note::

   Internet Explorer n'est pas pris en charge.

Liste de vérification des prérequis
====================================

Avant l'installation, veuillez vérifier les éléments suivants :

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Élément de vérification
     - État
   * - La configuration matérielle est-elle satisfaite ?
     - □
   * - Java 21 est-il installé ? (sauf version Docker)
     - □
   * - Docker est-il installé ? (version Docker)
     - □
   * - Les ports nécessaires sont-ils disponibles ?
     - □
   * - La configuration du pare-feu est-elle appropriée ?
     - □
   * - Y a-t-il suffisamment d'espace disque disponible ?
     - □
   * - La connexion réseau est-elle normale ? (si vous effectuez une exploration de sites externes)
     - □

Étapes suivantes
================

Après avoir vérifié la configuration requise, passez à la procédure d'installation adaptée à votre environnement :

- :doc:`install-linux` - Installation pour Linux (TAR.GZ/RPM/DEB)
- :doc:`install-windows` - Installation pour Windows (ZIP)
- :doc:`install-docker` - Installation pour Docker
- :doc:`install` - Vue d'ensemble des méthodes d'installation
