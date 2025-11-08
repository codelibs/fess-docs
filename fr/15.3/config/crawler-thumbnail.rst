===============
Configuration des vignettes
===============

Affichage des vignettes
===============

|Fess| peut afficher des vignettes dans les résultats de recherche.
Les vignettes sont générées en fonction du type MIME des résultats de recherche.
Pour les types MIME pris en charge, les vignettes sont générées lors de l'affichage des résultats de recherche.
Le traitement de génération de vignettes peut être configuré et ajouté pour chaque type MIME.

Pour afficher les vignettes, connectez-vous en tant qu'administrateur et activez l'affichage des vignettes dans les paramètres généraux, puis enregistrez.

Vignettes des fichiers HTML
======================

Les vignettes HTML utilisent les images spécifiées ou contenues dans le HTML.
Les vignettes sont recherchées dans l'ordre suivant et affichées si elles sont spécifiées.

- Valeur de l'attribut content d'une balise meta avec l'attribut name défini sur thumbnail
- Valeur de l'attribut content d'une balise meta avec l'attribut property défini sur og:image
- Image de taille appropriée pour une vignette dans une balise img


Vignettes des fichiers MS Office
===========================

Les vignettes des fichiers MS Office sont générées à l'aide de LibreOffice et ImageMagick.
Si les commandes unoconv et convert sont installées, les vignettes sont générées.

Installation des paquets
------------------

Pour les systèmes d'exploitation de type Redhat, installez les paquets suivants pour créer des images.

::

    $ sudo yum install unoconv libreoffice-headless vlgothic-fonts ImageMagick

Script de génération
-----------

Lors de l'installation via le paquet RPM/Deb, le script de génération de vignettes pour MS Office est installé dans /usr/share/fess/bin/generate-thumbnail.

Vignettes des fichiers PDF
=====================

Les vignettes PDF sont générées à l'aide d'ImageMagick.
Si la commande convert est installée, les vignettes sont générées.

Désactivation du travail de vignettes
==================

Pour désactiver le travail de vignettes, configurez ce qui suit.

1. Dans l'interface d'administration, allez dans Système > Général, décochez « Affichage des vignettes », et cliquez sur le bouton « Mettre à jour ».
2. Définissez ``thumbnail.crawler.enabled`` sur ``false`` dans ``app/WEB-INF/classes/fess_config.properties`` ou ``/etc/fess/fess_config.properties``.

::

    thumbnail.crawler.enabled=false

3. Redémarrez le service Fess.
