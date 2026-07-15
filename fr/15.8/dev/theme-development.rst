==================================
Guide de développement des thèmes
==================================

Aperçu
======

Avec |Fess|, vous pouvez personnaliser le design de l'écran de recherche de deux façons :

Thème statique (Static Theme)
    Mécanisme introduit dans |Fess| 15.7. Le thème est distribué sous forme de
    fichier ZIP, téléversé puis activé depuis l'écran d'administration. Le
    thème lui-même est une SPA (Single Page Application, application
    monopage) indépendante qui utilise l'API ``/api/v2/*`` et ne dépend pas
    des JSP du cœur de |Fess|. Cette méthode est recommandée pour créer un
    nouveau thème.

Plugin de thème JAR (legacy)
    Plugin de type traditionnel qui remplace les répertoires ``view`` /
    ``css`` / ``js`` / ``images``. Il est construit sous forme de JAR et
    installé comme un plugin. Utilisez-le lorsque vous souhaitez remplacer
    partiellement les écrans existants basés sur JSP.

.. note::

   Les thèmes statiques sont disponibles à partir de |Fess| 15.7. Pour cibler
   les versions 15.6 et antérieures, utilisez un plugin de thème JAR. Pour
   modifier directement les JSP, CSS et images de l'écran de recherche depuis
   l'écran d'administration, reportez-vous à :doc:`../admin/design-guide`.

Thème statique
==============

Un thème statique est un ensemble de ressources statiques comprenant le
manifeste ``theme.yml`` et ``index.html``. Le thème lui-même est implémenté
comme une application front-end qui appelle l'API ``/api/v2/*`` de |Fess|.

Structure
---------

Un thème statique adopte la structure de répertoires suivante.

::

    example/
    ├── theme.yml          # Manifeste (obligatoire)
    ├── index.html         # HTML d'entrée de la SPA
    ├── assets/            # Ressources statiques telles que JavaScript, CSS
    │   └── styles.css
    ├── i18n/              # Messages multilingues (messages.<locale>.json)
    │   └── messages.en.json
    ├── help/              # Définitions d'aide (<locale>.json)
    │   └── en.json
    └── thumbnail.png      # Image d'aperçu (facultatif)

Manifeste (theme.yml)
----------------------

``theme.yml`` est le manifeste obligatoire à placer à la racine du ZIP. Voici
un exemple de configuration minimale.

.. code-block:: yaml

    apiVersion: fess.codelibs.org/v1
    kind: StaticTheme
    name: example
    displayName: "Example Theme"
    version: "1.0.0"
    minFessVersion: "15.7"
    entry: index.html
    spaFallback: true

Les champs pouvant être spécifiés sont les suivants.

.. list-table::
   :header-rows: 1
   :widths: 22 12 66

   * - Champ
     - Obligatoire
     - Description
   * - ``apiVersion``
     - Obligatoire
     - Valeur fixe ``fess.codelibs.org/v1``.
   * - ``kind``
     - Obligatoire
     - Valeur fixe ``StaticTheme``.
   * - ``name``
     - Obligatoire
     - Nom du thème. Doit correspondre à ``^[a-z0-9][a-z0-9_-]{0,63}$``. Il
       est utilisé comme nom du répertoire du thème déployé sous ``themes/``
       (déterminé automatiquement à partir de ce ``name`` lors du
       téléversement), ainsi que pour l'URL de diffusion (``/themes/<name>/``).
   * - ``displayName``
     - Obligatoire
     - Nom affiché dans l'écran d'administration.
   * - ``version``
     - Obligatoire
     - Format de gestion sémantique des versions (exemple : ``1.0.0``,
       ``1.2.3-beta.1``).
   * - ``author``
     - Facultatif
     - Nom de l'auteur.
   * - ``description``
     - Facultatif
     - Description du thème.
   * - ``license``
     - Facultatif
     - Licence.
   * - ``homepage``
     - Facultatif
     - URL de la page d'accueil.
   * - ``minFessVersion``
     - Facultatif
     - Version minimale de |Fess| prise en charge par le thème.
   * - ``supportedLocales``
     - Facultatif
     - Liste des locales prises en charge (exemple : ``[en, ja, de]``).
   * - ``entry``
     - Facultatif
     - HTML d'entrée de la SPA. Valeur par défaut : ``index.html``.
   * - ``spaFallback``
     - Facultatif
     - Active ou désactive le fallback SPA. Valeur par défaut : ``true``.

.. note::

   Lors d'un téléversement depuis un ZIP, le nom du répertoire de destination
   est déterminé automatiquement à partir de ``name``. Si vous placez
   manuellement un thème dans le répertoire ``themes/``, veillez à faire
   correspondre le nom du répertoire avec ``name``. Les thèmes dont le nom ne
   correspond pas sont ignorés lors de la nouvelle analyse.

.. note::

   La miniature d'aperçu doit être placée à la racine du thème sous le nom
   fixe ``thumbnail.png`` (elle est affichée dans la liste des thèmes de
   l'écran d'administration). Cette image n'est pas un champ du manifeste ;
   elle est reconnue par son nom de fichier. Une taille inférieure à 512 Ko
   et à 512 × 512 pixels est recommandée.

Diffusion et API
-----------------

- Un thème statique est diffusé sous ``/themes/<name>/`` (``<name>``
  correspond au ``name`` défini dans ``theme.yml``).
- Lorsque ``spaFallback`` est activé, le HTML d'entrée (par défaut
  ``index.html``) est renvoyé pour chacun des chemins ``/``, ``/search``,
  ``/help``, ``/error``, ``/profile``, ``/cache`` et ``/chat``, et le routage
  ultérieur est assuré par la SPA.
- L'écran d'administration (``/admin/*``), ``/api/*``, l'écran de connexion,
  etc. ne sont pas concernés par le thème statique et sont traités par le
  cœur de |Fess|.
- La SPA du thème récupère les données telles que les résultats de recherche
  ou le chat depuis l'API ``/api/v2/*``.

Empaquetage
-----------

Le script ``scripts/package.sh`` du dépôt `fess-themes
<https://github.com/codelibs/fess-themes>`__ permet d'empaqueter le thème
dans un fichier ZIP destiné à la distribution.

::

    ./scripts/package.sh example

``dist/example-<version>.zip`` est généré (``<version>`` correspond au
``version`` défini dans ``theme.yml``).

.. note::

   ``theme.yml`` doit être placé à la racine du ZIP. S'il se trouve dans un
   sous-répertoire, il ne sera pas reconnu lors du téléversement.

Installation et activation
---------------------------

1. Ouvrez « Système » → « Thème » (``/admin/theme/``) dans l'écran
   d'administration.
2. Téléversez le fichier ZIP créé.
3. Sur la page de liste, sélectionnez le thème souhaité dans le menu
   déroulant « Thème par défaut », puis cliquez sur le bouton « Définir »
   pour l'activer.

Le mécanisme d'activation est le suivant.

- Lorsque vous cliquez sur le bouton « Définir », le nom du thème sélectionné
  est enregistré dans la propriété système ``theme.default`` et devient le
  thème par défaut pour l'ensemble du système.
- Si le nom du thème correspond à la clé d'un hôte virtuel, le thème n'est
  appliqué que lors de l'accès à cet hôte virtuel. Cela permet de changer de
  thème pour chaque hôte virtuel.
- Si vous mettez à jour directement le répertoire ``themes/`` sur le disque,
  vous pouvez relancer une analyse avec « Recharger ».

.. note::

   Le téléversement du ZIP est soumis à des limites telles que la taille du
   fichier, la taille totale après décompression et le nombre d'entrées ; ces
   limites peuvent être ajustées via les propriétés ``theme.*`` de
   ``fess_config.properties`` (par exemple, ``theme.upload.max.size`` vaut
   50 Mo par défaut et ``theme.directory.path`` vaut ``themes`` par défaut).
   Lors de la décompression, des vérifications sont effectuées pour empêcher
   les attaques de type ZIP Slip et zip bomb.

Plugin de thème JAR (legacy)
============================

Un plugin de thème JAR est un plugin qui remplace les répertoires ``view`` /
``css`` / ``js`` / ``images`` du cœur de |Fess| pour chaque nom de thème.
Pour la structure générale des plugins et la méthode de build, reportez-vous
également à :doc:`plugin-architecture`.

Structure
---------

::

    fess-theme-example/
    ├── pom.xml
    └── src/main/resources/
        ├── view/      # Fichiers JSP (search.jsp, index.jsp, header.jsp, etc.)
        ├── css/       # Fichiers CSS (style.css, etc.)
        ├── js/        # Fichiers JavaScript
        └── images/    # Fichiers image (logo.png, etc.)

.. note::

   Les vues (templates) sont au format JSP. Seuls les quatre répertoires de
   premier niveau ``view`` / ``css`` / ``js`` / ``images`` sont reconnus
   comme ressources. Le nom de l'artefact doit commencer par
   ``fess-theme-``.

pom.xml
-------

Le plugin est construit comme un jar ayant ``fess-parent`` pour POM parent.
Comme le thème est constitué uniquement de ressources, il n'est généralement
pas nécessaire de déclarer de dépendances supplémentaires.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                                 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <artifactId>fess-theme-example</artifactId>
        <version>15.8.0</version>
        <packaging>jar</packaging>

        <parent>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess-parent</artifactId>
            <version>15.8.0</version>
            <relativePath />
        </parent>
    </project>

Personnalisation du CSS et des images
---------------------------------------

L'écran de recherche est constitué de JSP basées sur Bootstrap. Vous pouvez
modifier les couleurs et la mise en page en remplaçant le CSS, ou changer le
logo en remplaçant ``images/logo.png``. Pour connaître les noms de classes et
le balisage concernés, consultez les JSP réelles (``view/index.jsp`` /
``view/search.jsp``, etc.).

Build et installation
-----------------------

::

    mvn clean package

Le fichier JAR (par exemple ``fess-theme-example-15.8.0.jar``) est généré
dans le répertoire ``target/``. Vous pouvez l'installer depuis « Système » →
« Plugin » dans l'écran d'administration. Pour plus de détails sur la
procédure d'installation, reportez-vous à :doc:`../admin/plugin-guide`.

Après l'installation, chaque répertoire du JAR est déployé pour le nom de
thème correspondant aux emplacements suivants (le nom du thème correspond à
la partie de l'artefact restant après avoir retiré ``fess-theme-`` ; dans
l'exemple ci-dessus, il s'agit de ``example``).

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Répertoire dans le JAR
     - Emplacement de déploiement
   * - ``view/``
     - ``WEB-INF/view/<theme>/``
   * - ``css/``
     - ``css/<theme>/``
   * - ``js/``
     - ``js/<theme>/``
   * - ``images/``
     - ``images/<theme>/``

Activation
----------

Un thème JAR s'active à l'aide de la fonctionnalité d'hôte virtuel. Si la clé
de l'hôte virtuel correspond au nom du thème, le thème est appliqué lors de
l'accès à cet hôte.

1. Dans les paramètres d'hôte virtuel de « Système » → « Général », associez
   l'en-tête ``Host`` de la requête au nom du thème (clé de l'hôte virtuel),
   par exemple ``Host:localhost:8080=example``.
2. Si nécessaire, définissez également le même nom (``example``) pour
   l'hôte virtuel des paramètres Web de crawl, entre autres.

Pour plus de détails sur la configuration des hôtes virtuels, reportez-vous à
:doc:`../admin/general-guide`.

Exemples de thèmes existants
=============================

- `fess-themes <https://github.com/codelibs/fess-themes>`__ - Collection de
  thèmes statiques (regroupe plusieurs thèmes statiques tels que
  ``codesearch`` et ``docsearch``)
- `fess-theme-simple <https://github.com/codelibs/fess-theme-simple>`__ -
  Thème JAR
- `fess-theme-classic <https://github.com/codelibs/fess-theme-classic>`__ -
  Thème JAR

Informations complémentaires
=============================

- :doc:`plugin-architecture` - Architecture des plugins
- :doc:`../admin/design-guide` - Conception de la page (modification directe
  des JSP, CSS et images)
- :doc:`../admin/plugin-guide` - Installation des plugins
