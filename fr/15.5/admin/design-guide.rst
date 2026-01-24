==================
Conception de page
==================

Présentation
============

Cette section explique les paramètres de configuration concernant la conception de l'écran de recherche.

Méthode de configuration
========================

Affichage
---------

Pour ouvrir la page de liste pour configurer la conception de page illustrée ci-dessous, cliquez sur [Système > Conception de page] dans le menu de gauche.

|image0|


Gestionnaire de fichiers
------------------------

Vous pouvez télécharger ou supprimer des fichiers disponibles sur l'écran de recherche.

Affichage des fichiers de page
------------------------------

Vous pouvez modifier les fichiers JSP de l'écran de recherche.
Vous pouvez modifier le fichier JSP cible en appuyant sur le bouton Modifier.
De plus, en appuyant sur le bouton Utiliser par défaut, vous pouvez modifier comme le fichier JSP lors de l'installation.
La sauvegarde avec le bouton Mettre à jour sur l'écran de modification appliquera les modifications.

Voici un résumé des pages modifiables.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - /index.jsp
     - Fichier JSP de la page d'accueil de recherche. Ce fichier JSP inclut les fichiers JSP de chaque partie.
   * - /header.jsp
     - Fichier JSP de l'en-tête.
   * - /footer.jsp
     - Fichier JSP du pied de page.
   * - /search.jsp
     - Fichier JSP de la page de liste des résultats de recherche. Ce fichier JSP inclut les fichiers JSP de chaque partie.
   * - /searchResults.jsp
     - Fichier JSP qui représente la partie des résultats de recherche de la page de liste des résultats. C'est le fichier JSP utilisé lorsqu'il y a des résultats de recherche. Modifiez-le si vous souhaitez personnaliser la présentation des résultats.
   * - /searchNoResult.jsp
     - Fichier JSP qui représente la partie des résultats de recherche de la page de liste des résultats. C'est le fichier JSP utilisé lorsqu'il n'y a pas de résultats de recherche.
   * - /searchOptions.jsp
     - Fichier JSP de l'écran des options de recherche.
   * - /advance.jsp
     - Fichier JSP de l'écran de recherche avancée.
   * - /help.jsp
     - Fichier JSP de la page d'aide.
   * - /error/error.jsp
     - Fichier JSP de la page d'erreur de recherche. Modifiez-le si vous souhaitez personnaliser la présentation des erreurs de recherche.
   * - /error/notFound.jsp
     - Fichier JSP de la page d'erreur affiché lorsque la page n'est pas trouvée.
   * - /error/system.jsp
     - Fichier JSP de la page d'erreur affiché en cas d'erreur système.
   * - /error/redirect.jsp
     - Fichier JSP de la page d'erreur affiché lors d'une redirection HTTP.
   * - /error/badRequest.jsp
     - Fichier JSP de la page d'erreur affiché en cas de requête incorrecte.
   * - /cache.hbs
     - Fichier pour afficher le cache des résultats de recherche.
   * - /login/index.jsp
     - Fichier JSP de l'écran de connexion.
   * - /profile/index.jsp
     - JSP de l'écran de modification du mot de passe utilisateur.
   * - /profile/newpassword.jsp
     - JSP de l'écran de mise à jour du mot de passe administrateur. Si le nom d'utilisateur et le mot de passe sont la même chaîne lors de la connexion, un changement de mot de passe est requis.


Tableau : Fichiers JSP modifiables

|image1|

Fichiers à téléverser
---------------------

Vous pouvez téléverser des fichiers à utiliser sur l'écran de recherche.
Les noms de fichiers image pris en charge sont jpg, gif, png, css, js.

Téléversement de fichier
:::::::::::::::::::::::::

Spécifiez le fichier à téléverser.

Nom de fichier (optionnel)
:::::::::::::::::::::::::::

Utilisez-le si vous souhaitez spécifier un nom de fichier pour le fichier à téléverser.
Si omis, le nom du fichier téléversé sera utilisé.
Par exemple, si vous spécifiez logo.png, l'image de la page d'accueil de recherche sera modifiée.


.. |image0| image:: ../../../resources/images/en/15.5/admin/design-1.png
.. |image1| image:: ../../../resources/images/en/15.5/admin/design-2.png
