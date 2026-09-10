=======
Plugins
=======

Présentation
============

La page de configuration des plugins gère les plugins.

Gestion
=======

Affichage
---------

Pour ouvrir la page de liste des plugins installés illustrée ci-dessous, cliquez sur [Système > Plugin] dans le menu de gauche.

|image0|

Pour désinstaller, cliquez sur le bouton Supprimer.

Installation
------------

Pour installer un nouveau plugin, cliquez sur le bouton Installer.

|image1|

Sélectionnez le plugin que vous souhaitez installer dans le menu déroulant et cliquez sur le bouton Installer pour démarrer l'installation.

Installation en ligne de commande
=================================

``bin/fess-setup`` installe des plugins en ligne de commande.

::

    $ bin/fess-setup install plugin fess-script-groovy

Sans version, la plus récente compilée pour ce |Fess| est choisie dans le dépôt, si bien que chaque exécution peut installer une version différente. Pour la figer, indiquez la version après le nom du plugin, séparée par deux-points.

::

    $ bin/fess-setup install plugin fess-script-groovy:15.9.0 fess-ds-git:15.9.0

Les plugins sont publiés séparément : ceux installés ensemble ne sont donc pas nécessairement dans la même version. Indiquez la version pour chacun. Un plugin indiqué sans version utilise la valeur de ``--version``.

::

    $ bin/fess-setup install plugin fess-script-groovy fess-ds-git:15.9.1 --version 15.9.0

La version précédemment installée d'un plugin est supprimée une fois la nouvelle installée. Une version inexistante se termine avec le code de sortie 1 : une étape de build telle qu'un Dockerfile échoue au lieu de continuer sans le plugin.

.. |image0| image:: ../../../resources/images/en/15.9/admin/plugin-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/plugin-2.png
