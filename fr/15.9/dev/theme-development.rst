==================================
Guide de développement des thèmes
==================================

Aperçu
======

Dans |Fess| 15.9, l'écran de recherche est toujours un thème statique. Un
thème statique est une SPA (Single Page Application, application monopage)
indépendante qui utilise l'API ``/api/v2/*``. Les thèmes sont distribués sous
forme de fichiers ZIP, téléversés puis activés depuis l'écran
d'administration. Lorsqu'aucun thème n'est sélectionné, |Fess| utilise
``bootstrap``, le thème statique fourni avec lui.

Pour modifier l'apparence de l'écran de recherche, installez un autre thème
(voir :doc:`../admin/theme-guide`) ou créez le vôtre : le plus rapide est de
copier le thème fourni et de modifier la copie, comme décrit dans
`Personnalisation du thème fourni`_.

.. note::

   Les thèmes statiques sont disponibles à partir de |Fess| 15.7 et sont
   devenus l'écran de recherche par défaut en 15.9. Les plugins de thème JAR,
   qui remplacent les JSP de l'écran de recherche, ne modifient plus l'écran
   de recherche en 15.9 ; voir `Plugin de thème JAR (legacy)`_.

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
    version: "15.9.0"
    minFessVersion: "15.9"
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
     - Format de gestion sémantique des versions (exemple : ``15.9.0``,
       ``15.9.1-beta.1``). Par convention, ``major.minor`` est la ligne |Fess| que
       le thème vise, de sorte que la version seule indique pour quel |Fess| un
       thème est prévu.
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
     - Version minimale de |Fess| prise en charge par le thème. Gardez-la égale au
       ``major.minor`` de ``version``. Il n'existe pas de ``maxFessVersion`` :
       voir `Publication`_.
   * - ``supportedLocales``
     - Facultatif
     - Liste des locales prises en charge (exemple : ``[en, ja, de]``).
   * - ``entry``
     - Facultatif
     - HTML d'entrée de la SPA. Valeur par défaut : ``index.html``.
   * - ``spaFallback``
     - Facultatif
     - Obsolète. Accepté pour des raisons de compatibilité mais n'est plus
       lu : depuis la version 15.9, le HTML d'entrée est toujours servi pour
       les chemins de l'écran de recherche.

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
- Le HTML d'entrée (par défaut ``index.html``) est renvoyé pour chacun des
  chemins ``/``, ``/search``, ``/advance``, ``/help``, ``/error``,
  ``/profile``, ``/cache`` et ``/chat``, et le routage ultérieur est assuré
  par la SPA. Depuis la version 15.9, c'est le cas quelle que soit la valeur
  de ``spaFallback`` ; ce champ n'est plus lu.
- Les erreurs sont également rendues par le thème : lorsqu'une requête
  échoue, le navigateur reçoit le HTML d'entrée du thème à l'URL demandée,
  avec le véritable statut HTTP.
- L'écran d'administration (``/admin/*``), ``/api/*``, l'écran de connexion,
  etc. ne sont pas concernés par le thème statique et sont traités par le
  cœur de |Fess|.
- ``{{themePath}}`` dans le HTML d'entrée est remplacé par
  ``themes/<name>`` lorsque la page est servie. Faites référence aux
  fichiers du thème depuis ``index.html`` sous la forme
  ``{{themePath}}/assets/styles.css``, etc. Le nom du thème n'apparaît
  alors pas dans la page, et le thème charge ses propres fichiers quel que
  soit le nom sous lequel il est installé.
- Le HTML d'entrée est servi avec un en-tête ``Content-Security-Policy`` qui
  n'autorise les scripts, les styles, les images et les connexions que depuis
  |Fess| lui-même (les styles en ligne sont autorisés ; les scripts en ligne
  ne le sont pas). Les polices ou scripts provenant d'un CDN externe ne sont
  donc pas chargés ; incluez-les dans le thème.
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

Publication
-----------

Les thèmes développés par le projet |Fess| sont publiés sous
https://maven.codelibs.org/release/org/codelibs/fess/themes/ , en
``<name>/<version>/<name>-<version>.zip`` avec un ``.sha1`` à côté, et un
``maven-metadata.xml`` par thème qui liste les versions publiées.
``bin/fess-setup install theme <name>`` lit ces métadonnées pour choisir la version construite
pour le |Fess| en cours d'exécution.

Versionnez un thème sur la ligne |Fess| qu'il vise et augmentez la version dès que ce que livre
l'archive change. Une version publiée n'est jamais écrasée : une modification qui conserve sa
version n'est donc tout simplement jamais distribuée.

C'est aussi pourquoi le manifeste n'a pas de champ de borne supérieure. Une archive publiée ne
changeant jamais, une borne ne pourrait pas être ajoutée plus tard pour un thème qui cesse de
fonctionner sur un |Fess| plus récent. Ne pas publier ce thème pour la nouvelle ligne dit la même
chose, au moment où on le sait.

.. note::

   Énumérez les versions publiées à partir de ``maven-metadata.xml`` plutôt que d'un listage de
   répertoire. L'index de répertoire est généré périodiquement : un thème fraîchement publié est
   lisible via ses métadonnées avant d'apparaître dans un listage.

Installation et activation
---------------------------

1. Ouvrez « Système » → « Thème » (``/admin/theme/``) dans l'écran
   d'administration.
2. Téléversez le fichier ZIP créé. Un thème publié peut aussi être installé depuis
   la ligne de commande avec ``bin/fess-setup install theme <name>`` ; voir
   :doc:`../install/fess-setup`.
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

.. _theme-customize-bundled:

Personnalisation du thème fourni
--------------------------------

Le thème fourni ``bootstrap`` se trouve dans ``app/themes/bootstrap/`` de
l'installation de |Fess| (``/usr/share/fess/app/themes/bootstrap/`` pour les
paquets RPM/DEB). Ne le modifiez pas sur place : une mise à niveau le
remplace, et le nom ``bootstrap`` lui est réservé, de sorte qu'il ne peut être
ni supprimé ni remplacé par un téléversement. Copiez-le plutôt sous un nouveau
nom.

1. Copiez le répertoire, par exemple vers ``mytheme`` :

   ::

       $ cp -r app/themes/bootstrap /tmp/mytheme

2. Dans ``theme.yml``, remplacez ``name`` par ``mytheme`` et modifiez
   ``displayName``. ``name`` doit correspondre au nom du répertoire.

3. Laissez ``index.html`` tel quel. Le ``index.html`` fourni fait
   référence à ses propres fichiers, comme la feuille de style, les logos
   et le script, sous la forme ``{{themePath}}/assets/...``, et |Fess|
   remplace ``{{themePath}}`` par ``themes/<name>`` (le ``name`` de
   ``theme.yml``) lorsqu'il sert la page. Il suffit donc de renommer la
   copie pour qu'elle charge ses propres fichiers. Si vous ajoutez un
   fichier auquel ``index.html`` fait référence, écrivez aussi son URL sous
   la forme ``{{themePath}}/assets/...``.

4. Apportez vos modifications :

   - Couleurs et mise en page : ``assets/styles.css``.
   - Logos : ``assets/logo-head.png`` (en-tête) et ``assets/logo.png``
     (page d'accueil de la recherche).
   - Textes, comme le pied de page (``footer.copyright_org``) : les fichiers
     ``i18n/messages.<locale>.json``, un par langue.
   - Structure de la page : ``index.html``.

5. Empaquetez le répertoire dans un ZIP avec ``theme.yml`` à sa racine, puis
   téléversez-le depuis « Système » → « Thème » dans l'écran
   d'administration :

   ::

       $ cd /tmp/mytheme && zip -r ../mytheme.zip .

   Vous pouvez aussi placer le répertoire dans ``app/themes/`` et cliquer sur
   « Recharger » sur la même page.

6. Sélectionnez ``mytheme`` comme thème par défaut sur cette page.

.. note::

   Après chaque mise à niveau de |Fess|, remplacez la copie par une nouvelle
   copie du thème fourni et réappliquez vos modifications, car le thème
   fourni suit l'API ``/api/v2/*`` de sa version de |Fess|.

Plugin de thème JAR (legacy)
============================

.. warning::

   Depuis |Fess| 15.9, l'écran de recherche est toujours servi par un thème
   statique ; un plugin de thème JAR ne le modifie donc plus. Parmi les JSP
   fournies par un thème JAR, seules celles de l'écran de connexion
   (``/login/``) sont encore utilisées. Transférez le design vers un thème
   statique ; voir `Personnalisation du thème fourni`_.

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
        <version>15.9.0</version>
        <packaging>jar</packaging>

        <parent>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess-parent</artifactId>
            <version>15.9.0</version>
            <relativePath />
        </parent>
    </project>

Personnalisation du CSS et des images
---------------------------------------

Les JSP sont basées sur Bootstrap. Vous pouvez modifier les couleurs et la
mise en page en remplaçant le CSS, ou changer le logo en remplaçant
``images/logo.png``. Depuis la version 15.9, cela ne concerne que l'écran de
connexion ; l'écran de recherche est un thème statique (voir
`Personnalisation du thème fourni`_).

Build et installation
-----------------------

::

    mvn clean package

Le fichier JAR (par exemple ``fess-theme-example-15.9.0.jar``) est généré
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
- :doc:`../admin/plugin-guide` - Installation des plugins
