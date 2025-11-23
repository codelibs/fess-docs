=====================
Mappage de chemin
=================

Présentation
============

Cette section explique la configuration du mappage de chemin.
Le mappage de chemin peut être utilisé lorsque vous souhaitez remplacer les liens affichés dans les résultats de recherche.

Gestion
=======

Affichage
---------

Pour ouvrir la page de liste de configuration du mappage de chemin illustrée ci-dessous, cliquez sur [Crawler > Mappage de chemin] dans le menu de gauche.

|image0|

Cliquez sur le nom de la configuration pour la modifier.

Création de configuration
-------------------------

Cliquez sur le bouton Nouvelle création pour ouvrir la page de configuration du mappage de chemin.

|image1|

Paramètres de configuration
---------------------------

Expression régulière
::::::::::::::::::::

Spécifie la chaîne de caractères à remplacer.
La méthode de description suit les expressions régulières Java.

Remplacement
::::::::::::

Spécifie la chaîne de caractères pour remplacer l'expression régulière correspondante.

Type de traitement
::::::::::::::::::

Spécifie le moment du remplacement.

* Crawl : Lors du crawl, remplace l'URL après l'obtention du document et avant l'indexation.
* Affichage : Lors de la recherche, remplace l'URL avant l'affichage.
* Crawl/Affichage : Remplace l'URL lors du crawl et de l'affichage.
* URL enregistrée : Lors du crawl, remplace l'URL avant l'obtention du document.

Ordre d'affichage
:::::::::::::::::

Vous pouvez spécifier l'ordre de traitement du mappage de chemin.
Le traitement s'effectue dans l'ordre croissant.

Suppression de configuration
----------------------------

Cliquez sur le nom de la configuration dans la page de liste, puis cliquez sur le bouton Supprimer pour afficher l'écran de confirmation.
Appuyer sur le bouton Supprimer supprimera la configuration.

.. |image0| image:: ../../../resources/images/en/15.3/admin/pathmap-1.png
.. |image1| image:: ../../../resources/images/en/15.3/admin/pathmap-2.png
