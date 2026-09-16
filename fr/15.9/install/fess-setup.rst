====================
Commande fess-setup
====================

``bin/fess-setup`` (``bin\fess-setup.bat`` sous Windows) est fourni avec le package ZIP de |Fess|.
Il installe ce dont |Fess| a besoin sans l'intégrer : OpenSearch avec les plugins requis par
|Fess|, Node.js pour le robot Playwright, et les plugins |Fess|. Il établit également un diagnostic
d'une installation.

Exécutez-le depuis le répertoire de |Fess|. Sans argument, il affiche la liste des commandes.

::

    $ cd /path/to/fess-15.9.0
    $ bin/fess-setup <command> [options]

Codes de sortie
===============

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Code
     - Signification
   * - ``0``
     - La commande a réussi.
   * - ``1``
     - La commande a échoué : par exemple, un téléchargement a échoué, la version demandée n'existe
       pas, OpenSearch ne publie pas de version pour cette plateforme, ou ``check`` a détecté un
       problème.
   * - ``2``
     - La ligne de commande est incorrecte : commande inconnue, ou argument manquant, tel qu'un nom
       de plugin.

Installation d'OpenSearch et de Node.js
=========================================

install opensearch
------------------

::

    $ bin/fess-setup install opensearch [--dest <dir>] [--version <version>]

Télécharge la version d'OpenSearch prise en charge par ce |Fess| dans ``opensearch/`` du répertoire
de |Fess|, y installe les quatre plugins requis par |Fess| (``opensearch-analysis-fess``,
``opensearch-analysis-extension``, ``opensearch-minhash`` et ``opensearch-configsync``), puis ajoute
les paramètres suivants à son ``config/opensearch.yml`` :

- ``configsync.config_path``, défini sur le répertoire ``config/dictionary`` de cet OpenSearch
- ``plugins.security.disabled: true``

Un paramètre déjà présent dans ``opensearch.yml`` n'est pas ajouté une seconde fois, et
``plugins.security.disabled: true`` n'est pas ajouté lorsque le fichier contient un paramètre
``plugins.security.*``, quel qu'il soit. Lorsque le répertoire d'OpenSearch existe déjà, le
téléchargement est ignoré : exécuter à nouveau la commande sur une installation existante n'ajoute
donc que les paramètres manquants.

La commande affiche chaque paramètre ajouté, puis indique si ``bin/fess.in.sh`` trouve cet
OpenSearch par lui-même. C'est le cas lorsqu'il s'agit du seul OpenSearch possédant un répertoire
``config/dictionary`` sous ``opensearch/`` dans le répertoire de |Fess| : ``bin/fess.in.sh``
(``bin\fess.in.bat`` sous Windows) définit alors ``FESS_DICTIONARY_PATH`` sur ce répertoire, et rien
d'autre n'est à configurer pour un OpenSearch situé sur le même hôte. Dans le cas contraire, la
commande affiche les valeurs de ``SEARCH_ENGINE_HTTP_URL`` et de ``FESS_DICTIONARY_PATH`` à définir,
comme décrit dans :doc:`install-linux` ou :doc:`install-windows`.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Option
     - Description
   * - ``--dest <dir>``
     - Répertoire dans lequel extraire OpenSearch, au lieu de ``opensearch/`` dans le répertoire de
       |Fess|. ``bin/fess.in.sh`` ne recherche pas OpenSearch en dehors de ce répertoire.
   * - ``--version <version>``
     - Version d'OpenSearch à installer. Les plugins sont installés dans la même version.

OpenSearch ne publie de versions officielles que pour Linux et Windows. Sur les autres plateformes,
comme macOS, la commande se termine avec le code ``1`` avant tout téléchargement et suggère
d'installer OpenSearch avec Homebrew puis d'ajouter les plugins avec ``install opensearch-plugins``,
ou d'utiliser Docker.

.. warning::

   Avec ``plugins.security.disabled: true``, OpenSearch accepte les requêtes sans authentification.
   OpenSearch n'écoute que sur l'adresse de bouclage tant que ``network.host`` n'est pas défini.
   Avant qu'il n'écoute sur une autre adresse, configurez plutôt le plugin de sécurité ; consultez
   :doc:`security`.

install opensearch-plugins
--------------------------

::

    $ bin/fess-setup install opensearch-plugins --opensearch-home <dir> [--version <version>]

Installe les quatre plugins requis par |Fess| dans un OpenSearch existant, au lieu d'exécuter quatre
fois son ``bin/opensearch-plugin install``. ``--opensearch-home`` est le répertoire d'installation
d'OpenSearch et est obligatoire. ``--version`` définit la version des plugins, qui doit correspondre
à la version d'OpenSearch.

Cette commande ne modifie pas ``opensearch.yml``. Ajoutez vous-même ``configsync.config_path`` et
les autres paramètres, comme décrit dans :doc:`install-linux` ou :doc:`install-windows`.

install nodejs
--------------

::

    $ bin/fess-setup install nodejs [--dest <dir>] [--version <version>]

Télécharge Node.js, nécessaire au robot Playwright, dans ``nodejs/`` du répertoire de |Fess|.
``bin/fess.in.sh`` (``bin\fess.in.bat`` sous Windows) l'y trouve et définit
``PLAYWRIGHT_NODEJS_PATH``. Avec ``--dest`` en dehors du répertoire de |Fess|, la commande affiche à
la place la ligne ``PLAYWRIGHT_NODEJS_PATH`` à ajouter à ``bin/fess.in.sh``. ``--version`` permet de
choisir une autre version de Node.js. Consultez :doc:`../config/crawler-advanced` pour le robot
Playwright.

Gestion des plugins
===================

Ces commandes agissent sur le répertoire des plugins ``app/WEB-INF/plugin`` de l'installation de
|Fess|. Redémarrez |Fess| après avoir installé, mis à niveau ou supprimé des plugins. Les plugins
peuvent aussi être gérés depuis la page **Système > Plugin** de l'écran d'administration ; consultez
:doc:`../admin/plugin-guide`.

``install plugin``, ``list plugins`` et ``upgrade plugins`` acceptent ``--repository <url>``. Cette
option prend la liste des versions, les jars et leurs sommes de contrôle dans ce seul dépôt Maven,
par exemple un miroir interne, au lieu des dépôts release et snapshot par défaut et de GitHub.

install plugin
--------------

::

    $ bin/fess-setup install plugin <name>[:<version>]... [--version <version>] [--repository <url>]

Installe un ou plusieurs plugins |Fess|, par exemple ``fess-script-groovy`` ou ``fess-ds-git``. Un
nom sans version installe la version la plus récente compilée pour ce |Fess|.
``<name>:<version>`` fige la version de ce plugin, et ``--version`` est la version de chaque nom qui
n'en indique pas. La version précédemment installée d'un plugin est supprimée une fois la nouvelle
installée.

Un jar provient de la release GitHub du plugin, ou du dépôt Maven lorsque la release ne contient pas
ce fichier, et est vérifié avec la somme de contrôle SHA-1 publiée par le dépôt Maven. Une version
de développement de |Fess| installe aussi les builds snapshot de sa propre ligne, et les privilégie.

Consultez :doc:`../admin/plugin-guide` pour des exemples.

list plugins
------------

::

    $ bin/fess-setup list plugins [--repository <url>]

Liste les plugins publiés pour ce |Fess| et signale ceux qui sont installés par
``(installed: <version>)``. Les plugins installés mais non publiés dans le dépôt, comme un jar
compilé localement, sont listés à part. Une version de développement de |Fess| consulte aussi le
dépôt snapshot.

list installed
--------------

::

    $ bin/fess-setup list installed

Liste les plugins installés et leurs versions, sans contacter le dépôt.

upgrade plugins
---------------

::

    $ bin/fess-setup upgrade plugins [--repository <url>]

Réinstalle chaque plugin installé dans la version adaptée à ce |Fess|. Un plugin qui est déjà dans
cette version est laissé tel quel. Les plugins de ``app/WEB-INF/plugin`` sont compilés pour une
version précise de |Fess| : exécutez donc cette commande après une mise à niveau de |Fess|.

remove plugin
-------------

::

    $ bin/fess-setup remove plugin <name>...

Supprime les jars installés des plugins indiqués. Un nom qui n'est pas installé est signalé, sans
modifier le code de sortie.

Vérification d'une installation
=================================

list
----

::

    $ bin/fess-setup list

Affiche les composants que ``install`` télécharge, ``opensearch`` et ``nodejs``, avec la version de
chacun.

check
-----

::

    $ bin/fess-setup check [--url <engine url>] [--playwright]

Établit un diagnostic de l'installation, une ligne par vérification, chacune marquée ``OK``,
``WARN`` ou ``FAIL`` :

- Le moteur de recherche : s'il est joignable, sa version (un avertissement lorsque les nœuds
  indiquent des versions différentes), si les quatre plugins requis par |Fess| y sont installés, et
  si ``configsync`` répond.
- |Fess| : si le répertoire des plugins existe et est accessible en écriture, chaque plugin installé
  (un échec pour un plugin compilé pour une autre version de |Fess| et pour un plugin installé en
  deux versions), et si Node.js est installé dans ``nodejs/`` du répertoire de |Fess|.

L'URL du moteur est ``--url``, sinon la variable d'environnement ``SEARCH_ENGINE_HTTP_URL``, sinon
``http://localhost:9200``. ``bin/fess-setup`` ne lit pas ``bin/fess.in.sh`` : indiquez donc
``--url`` lorsqu'OpenSearch se trouve ailleurs. L'absence de Node.js est seulement signalée, sauf si
``--playwright`` est indiqué, auquel cas elle constitue un échec.

La commande se termine avec le code ``0`` lorsqu'aucune vérification n'a échoué, même si certaines
ont produit des avertissements, et avec le code ``1`` sinon.
