===========================
Configuration des vignettes
===========================

Présentation
============

|Fess| peut afficher des vignettes dans les résultats de recherche.
Les vignettes sont générées en fonction du type MIME des résultats de recherche.
Pour les types MIME pris en charge, les vignettes sont générées lors de l'affichage des résultats de recherche.
Le traitement de génération de vignettes peut être configuré et ajouté pour chaque type MIME.

Pour afficher les vignettes, connectez-vous en tant qu'administrateur et activez l'affichage des vignettes dans les paramètres généraux, puis enregistrez.

Formats de fichiers pris en charge
==================================

Fichiers image
--------------

.. list-table::
   :widths: 15 40 20
   :header-rows: 1

   * - Format
     - Type MIME
     - Description
   * - JPEG
     - ``image/jpeg``
     - Photos, etc.
   * - PNG
     - ``image/png``
     - Images transparentes, etc.
   * - GIF
     - ``image/gif``
     - Y compris les GIF animés
   * - BMP
     - ``image/bmp``, ``image/x-windows-bmp``, ``image/x-ms-bmp``
     - Images bitmap
   * - TIFF
     - ``image/tiff``
     - Images haute qualité
   * - SVG
     - ``image/svg+xml``
     - Images vectorielles
   * - Photoshop
     - ``image/vnd.adobe.photoshop``, ``image/photoshop``, ``application/x-photoshop``, ``application/photoshop``
     - Fichiers PSD

Fichiers document
-----------------

.. list-table::
   :widths: 15 50 20
   :header-rows: 1

   * - Format
     - Type MIME
     - Description
   * - PDF
     - ``application/pdf``
     - Documents PDF
   * - Word
     - ``application/msword``, ``application/vnd.openxmlformats-officedocument.wordprocessingml.document``
     - Documents Word
   * - Excel
     - ``application/vnd.ms-excel``, ``application/vnd.openxmlformats-officedocument.spreadsheetml.sheet``
     - Feuilles de calcul Excel
   * - PowerPoint
     - ``application/vnd.ms-powerpoint``, ``application/vnd.openxmlformats-officedocument.presentationml.presentation``
     - Présentations PowerPoint
   * - RTF
     - ``application/rtf``
     - Texte enrichi
   * - PostScript
     - ``application/postscript``
     - Fichiers PostScript

Contenu HTML
------------

.. list-table::
   :widths: 15 30 40
   :header-rows: 1

   * - Format
     - Type MIME
     - Description
   * - HTML
     - ``text/html``
     - Génère des vignettes à partir des images intégrées dans les pages HTML

Outils externes requis
======================

La génération de vignettes nécessite les outils externes suivants. Installez-les en fonction des formats de fichiers que vous devez prendre en charge.

Outils de base (requis)
-----------------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Outil
     - Utilisation
     - Linux (apt)
     - Mac (Homebrew)
   * - ImageMagick
     - Conversion et redimensionnement d'images
     - ``apt install imagemagick``
     - ``brew install imagemagick``

.. note::

   ImageMagick 6 (commande ``convert``) et ImageMagick 7 (commande ``magick``) sont tous deux pris en charge.

Support SVG
-----------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Outil
     - Utilisation
     - Linux (apt)
     - Mac (Homebrew)
   * - rsvg-convert
     - Conversion SVG vers PNG
     - ``apt install librsvg2-bin``
     - ``brew install librsvg``

Support PDF
-----------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Outil
     - Utilisation
     - Linux (apt)
     - Mac (Homebrew)
   * - pdftoppm
     - Conversion PDF vers PNG
     - ``apt install poppler-utils``
     - ``brew install poppler``

Support MS Office
-----------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Outil
     - Utilisation
     - Linux (apt)
     - Mac (Homebrew)
   * - unoconv
     - Conversion Office vers PDF
     - ``apt install unoconv``
     - ``brew install unoconv``
   * - pdftoppm
     - Conversion PDF vers PNG
     - ``apt install poppler-utils``
     - ``brew install poppler``

Pour les systèmes d'exploitation de type Redhat, installez les paquets suivants :

::

    $ sudo yum install unoconv libreoffice-headless vlgothic-fonts ImageMagick poppler-utils

Support PostScript
------------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Outil
     - Utilisation
     - Linux (apt)
     - Mac (Homebrew)
   * - ps2pdf
     - Conversion PS vers PDF
     - ``apt install ghostscript``
     - ``brew install ghostscript``
   * - pdftoppm
     - Conversion PDF vers PNG
     - ``apt install poppler-utils``
     - ``brew install poppler``

Vignettes des fichiers HTML
===========================

Les vignettes HTML utilisent les images spécifiées ou contenues dans le HTML.
Les vignettes sont recherchées dans l'ordre suivant et affichées si elles sont spécifiées :

1. Valeur de l'attribut content d'une balise meta avec l'attribut name défini sur "thumbnail"
2. Valeur de l'attribut content d'une balise meta avec l'attribut property défini sur "og:image"
3. Image de taille appropriée pour une vignette dans une balise img

Configuration
=============

Fichier de configuration
------------------------

Le générateur de vignettes est configuré dans ``fess_thumbnail.xml``.

::

    src/main/resources/fess_thumbnail.xml

Principales options de configuration (fess_config.properties)
-------------------------------------------------------------

Les options suivantes peuvent être configurées dans ``app/WEB-INF/classes/fess_config.properties`` ou ``/etc/fess/fess_config.properties``.

::

    # Largeur minimale pour les vignettes (pixels)
    thumbnail.html.image.min.width=100

    # Hauteur minimale pour les vignettes (pixels)
    thumbnail.html.image.min.height=100

    # Rapport d'aspect maximum (largeur:hauteur ou hauteur:largeur)
    thumbnail.html.image.max.aspect.ratio=3.0

    # Largeur des vignettes générées
    thumbnail.html.image.thumbnail.width=100

    # Hauteur des vignettes générées
    thumbnail.html.image.thumbnail.height=100

    # Format de sortie
    thumbnail.html.image.format=png

    # XPath pour extraire les images du HTML
    thumbnail.html.image.xpath=//IMG

    # Extensions exclues
    thumbnail.html.image.exclude.extensions=svg,html,css,js

    # Intervalle de génération des vignettes (millisecondes)
    thumbnail.generator.interval=0

    # Délai d'expiration de l'exécution de commande (millisecondes)
    thumbnail.command.timeout=30000

    # Délai de destruction du processus (millisecondes)
    thumbnail.command.destroy.timeout=5000

Script generate-thumbnail
=========================

Présentation
------------

``generate-thumbnail`` est un script shell qui effectue la génération réelle des vignettes.
Lors de l'installation via le paquet RPM/Deb, il est installé dans ``/usr/share/fess/bin/generate-thumbnail``.

Utilisation
-----------

::

    generate-thumbnail <type> <url> <output_file> [mimetype]

Arguments
---------

.. list-table::
   :widths: 15 40 30
   :header-rows: 1

   * - Argument
     - Description
     - Exemple
   * - ``type``
     - Type de fichier
     - ``image``, ``svg``, ``pdf``, ``msoffice``, ``ps``
   * - ``url``
     - URL du fichier d'entrée
     - ``file:/path/to/file.jpg``
   * - ``output_file``
     - Chemin du fichier de sortie
     - ``/var/lib/fess/thumbnails/_0/_1/abc.png``
   * - ``mimetype``
     - Type MIME (optionnel)
     - ``image/gif``

Types pris en charge
--------------------

.. list-table::
   :widths: 15 30 40
   :header-rows: 1

   * - Type
     - Description
     - Outils utilisés
   * - ``image``
     - Fichiers image
     - ImageMagick (convert/magick)
   * - ``svg``
     - Fichiers SVG
     - rsvg-convert
   * - ``pdf``
     - Fichiers PDF
     - pdftoppm + ImageMagick
   * - ``msoffice``
     - Fichiers MS Office
     - unoconv + pdftoppm + ImageMagick
   * - ``ps``
     - Fichiers PostScript
     - ps2pdf + pdftoppm + ImageMagick

Exemples
--------

::

    # Générer une vignette pour un fichier image
    ./generate-thumbnail image file:/path/to/image.jpg /tmp/thumbnail.png image/jpeg

    # Générer une vignette pour un fichier SVG
    ./generate-thumbnail svg file:/path/to/image.svg /tmp/thumbnail.png

    # Générer une vignette pour un fichier PDF
    ./generate-thumbnail pdf file:/path/to/document.pdf /tmp/thumbnail.png

    # Fichier GIF (spécifier le type MIME pour activer l'indication de format)
    ./generate-thumbnail image file:/path/to/image.gif /tmp/thumbnail.png image/gif

Emplacement de stockage des vignettes
=====================================

Chemin par défaut
-----------------

::

    ${FESS_VAR_PATH}/thumbnails/

ou

::

    /var/lib/fess/thumbnails/

Structure des répertoires
-------------------------

Les vignettes sont stockées dans une structure de répertoires basée sur le hachage.

::

    thumbnails/
    ├── _0/
    │   ├── _1/
    │   │   ├── _2/
    │   │   │   └── _3/
    │   │   │       └── abcdef123456.png
    │   │   └── ...
    │   └── ...
    └── ...

Désactivation du travail de vignettes
=====================================

Pour désactiver le travail de vignettes, configurez ce qui suit :

1. Dans l'interface d'administration, allez dans Système > Général, décochez "Affichage des vignettes", et cliquez sur le bouton "Mettre à jour".
2. Définissez ``thumbnail.crawler.enabled`` sur ``false`` dans ``app/WEB-INF/classes/fess_config.properties`` ou ``/etc/fess/fess_config.properties``.

::

    thumbnail.crawler.enabled=false

3. Redémarrez le service Fess.

Dépannage
=========

Les vignettes ne sont pas générées
----------------------------------

1. **Vérifier les outils externes**

::

    # Vérifier ImageMagick
    which convert || which magick

    # Vérifier rsvg-convert (pour SVG)
    which rsvg-convert

    # Vérifier pdftoppm (pour PDF)
    which pdftoppm

2. **Vérifier les logs**

::

    ${FESS_LOG_PATH}/fess-thumbnail.log

3. **Exécuter le script manuellement**

::

    /usr/share/fess/bin/generate-thumbnail image file:/path/to/test.jpg /tmp/test_thumbnail.png image/jpeg

Erreurs avec les fichiers GIF/TIFF
----------------------------------

Lors de l'utilisation d'ImageMagick 6, spécifiez le type MIME pour activer les indications de format. Cela se fait automatiquement si Fess est correctement configuré.

Exemple d'erreur::

    convert-im6.q16: corrupt image `/tmp/thumbnail_xxx' @ error/gif.c/DecodeImage/512

Solutions :

- Mettre à niveau vers ImageMagick 7
- Ou vérifier que le type MIME est correctement transmis

Les vignettes SVG ne sont pas générées
--------------------------------------

1. Vérifier si ``rsvg-convert`` est installé

::

    which rsvg-convert

2. Tester la conversion manuellement

::

    rsvg-convert -w 100 -h 100 --keep-aspect-ratio input.svg -o output.png

Erreurs de permission
---------------------

Vérifiez les permissions du répertoire de stockage des vignettes.

::

    ls -la /var/lib/fess/thumbnails/

Corrigez les permissions si nécessaire.

::

    chown -R fess:fess /var/lib/fess/thumbnails/
    chmod -R 755 /var/lib/fess/thumbnails/

Support des plateformes
=======================

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Plateforme
     - Statut de support
     - Remarques
   * - Linux
     - Entièrement pris en charge
     - \-
   * - macOS
     - Entièrement pris en charge
     - Installer les outils externes via Homebrew
   * - Windows
     - Non pris en charge
     - En raison de la dépendance au script bash
