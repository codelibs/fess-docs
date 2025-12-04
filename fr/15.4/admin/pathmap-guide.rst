=================
Mappage de chemin
=================

Présentation
============

Cette section explique la configuration du mappage de chemin.
Le mappage de chemin est une fonction qui utilise des expressions régulières pour transformer les URLs des documents explorés par |Fess|.
Par exemple, il peut être utilisé lorsque vous souhaitez explorer des documents d'un serveur de fichiers (chemins commençant par ``file://``) et les rendre accessibles via un serveur web (``http://``) depuis les résultats de recherche.

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

Spécifie le moment du remplacement. Sélectionnez le type approprié selon votre objectif.

Crawl
  Remplace l'URL après l'obtention du document lors du crawl et avant l'indexation.
  L'URL convertie est enregistrée dans l'index.
  Utilisez ceci lorsque vous souhaitez convertir les chemins du serveur de fichiers en URLs de serveur web et les enregistrer dans l'index.

Affichage
  Remplace l'URL avant l'affichage des résultats de recherche et lors du clic sur les liens des résultats de recherche.
  Les URLs stockées dans l'index ne sont pas modifiées.
  Utilisez ceci lorsque vous souhaitez conserver l'URL originale dans l'index mais la convertir en une URL différente uniquement lors de l'affichage des résultats de recherche.

Crawl/Affichage
  Remplace l'URL lors du crawl et de l'affichage.
  Utilisez ceci lorsque vous souhaitez appliquer la même conversion aux deux moments.

Conversion d'URL extraite
  Remplace les URLs de liens lors de l'extraction de liens à partir de documents HTML.
  Efficace uniquement avec le crawler web (non efficace avec le crawler de fichiers).
  Les URLs enregistrées dans l'index ne sont pas modifiées.
  Utilisez ceci lorsque vous souhaitez convertir les URLs de liens extraites du HTML et les ajouter à la file d'attente de crawl.

Ordre d'affichage
:::::::::::::::::

Vous pouvez spécifier l'ordre de traitement du mappage de chemin.
Le traitement s'effectue dans l'ordre croissant.

Agent utilisateur
:::::::::::::::::

Spécifiez ceci lorsque vous souhaitez appliquer le mappage de chemin uniquement à des agents utilisateurs spécifiques.
La correspondance est effectuée à l'aide d'expressions régulières.
Si non défini, il s'applique à toutes les requêtes.

Suppression de configuration
----------------------------

Cliquez sur le nom de la configuration dans la page de liste, puis cliquez sur le bouton Supprimer pour afficher l'écran de confirmation.
Appuyer sur le bouton Supprimer supprimera la configuration.

Exemples
========

Accéder au serveur de fichiers via le serveur web
-------------------------------------------------

Ceci est un exemple de configuration pour explorer des documents d'un serveur de fichiers et les rendre accessibles via un serveur web depuis les résultats de recherche.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Élément de configuration
     - Valeur
   * - Expression régulière
     - ``file:/srv/documents/``
   * - Remplacement
     - ``http://fileserver.example.com/documents/``
   * - Type de traitement
     - Crawl

Avec cette configuration, les URLs sont enregistrées dans l'index comme ``http://fileserver.example.com/documents/...``.

Convertir l'URL uniquement à l'affichage
----------------------------------------

Ceci est un exemple de configuration pour conserver le chemin de fichier original dans l'index et convertir en URL de serveur web uniquement lors de l'affichage des résultats de recherche.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Élément de configuration
     - Valeur
   * - Expression régulière
     - ``file:/srv/documents/``
   * - Remplacement
     - ``http://fileserver.example.com/documents/``
   * - Type de traitement
     - Affichage

Avec cette configuration, les URLs sont enregistrées dans l'index comme ``file:/srv/documents/...`` et converties en ``http://...`` lors du clic sur les résultats de recherche.

Conversion de liens lors de la migration de serveur
---------------------------------------------------

Ceci est un exemple de configuration pour convertir les liens dans le HTML d'un ancien serveur vers un nouveau serveur lors de l'exploration d'un site web.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Élément de configuration
     - Valeur
   * - Expression régulière
     - ``http://old-server\\.example\\.com/``
   * - Remplacement
     - ``http://new-server.example.com/``
   * - Type de traitement
     - Conversion d'URL extraite

Avec cette configuration, les liens extraits du HTML sont convertis et ajoutés à la file d'attente de crawl.

Notes
=====

À propos de la conversion d'URL extraite
----------------------------------------

La conversion d'URL extraite est efficace uniquement avec le crawler web.
Elle n'est pas appliquée lors de l'exploration des systèmes de fichiers.
De plus, les URLs enregistrées dans l'index ne sont pas modifiées ; seules les URLs ajoutées à la file d'attente de crawl sont converties.

À propos des expressions régulières
-----------------------------------

Les expressions régulières sont écrites au format d'expressions régulières Java.

* Les références arrière (``$1``, ``$2``, etc.) peuvent être utilisées
* Les caractères spéciaux doivent être échappés (par exemple, ``.`` → ``\\.``)

À propos de l'ordre de tri
--------------------------

Les mappages de chemin sont appliqués séquentiellement dans l'ordre de tri configuré (croissant).
Lorsque plusieurs mappages de chemin correspondent, ils sont appliqués en commençant par la première correspondance.

.. |image0| image:: ../../../resources/images/en/15.4/admin/pathmap-1.png
.. |image1| image:: ../../../resources/images/en/15.4/admin/pathmap-2.png
