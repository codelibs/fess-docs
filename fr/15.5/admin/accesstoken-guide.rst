==================
Jeton d'accès
=============

Présentation
============

La page de configuration des jetons d'accès gère les jetons d'accès.

Gestion
=======

Affichage
---------

Pour ouvrir la page de liste de configuration des jetons d'accès illustrée ci-dessous, cliquez sur [Système > Jeton d'accès] dans le menu de gauche.

|image0|

Cliquez sur le nom de la configuration pour la modifier.

Création de configuration
-------------------------

Cliquez sur le bouton Nouvelle création pour ouvrir la page de configuration des jetons d'accès.

|image1|

Paramètres de configuration
---------------------------

Nom
::::

Spécifiez un nom pour décrire ce jeton d'accès.

Permission
::::::::::

Configure la permission du jeton d'accès.
Décrivez au format « {user|group|role}nom ».
Par exemple, pour qu'un utilisateur appartenant au groupe developer affiche les résultats de recherche, configurez la permission « {group}developer ».

Nom du paramètre
::::::::::::::::

Spécifiez le nom du paramètre de requête pour spécifier la permission comme requête de recherche.

.. warning::

   La fonctionnalité de nom de paramètre est conçue uniquement pour une utilisation dans des environnements internes de confiance.
   Lorsque cette fonctionnalité est activée, des permissions supplémentaires peuvent être spécifiées via des paramètres d'URL.
   Cependant, dans des environnements accessibles de l'extérieur ou exposés comme API publique,
   des utilisateurs malveillants peuvent manipuler les paramètres d'URL pour obtenir des privilèges qu'ils ne devraient pas avoir.

   Veuillez noter les points suivants :

   * Utilisez cette fonctionnalité uniquement lorsque Fess est intégré dans une autre application ou service qui contrôle entièrement les requêtes entrantes.
   * Ne configurez pas de nom de paramètre lorsque Fess est exposé à des réseaux non fiables.
   * Assurez-vous que les paramètres d'URL ne peuvent pas être manipulés par des utilisateurs externes lors de l'utilisation de jetons d'accès.

Date d'expiration
:::::::::::::::::

Spécifie la date d'expiration du jeton d'accès.

Suppression de configuration
----------------------------

Cliquez sur le nom de la configuration dans la page de liste, puis cliquez sur le bouton Supprimer pour afficher l'écran de confirmation.
Appuyer sur le bouton Supprimer supprimera la configuration.



.. |image0| image:: ../../../resources/images/en/15.5/admin/accesstoken-1.png
.. |image1| image:: ../../../resources/images/en/15.5/admin/accesstoken-2.png
