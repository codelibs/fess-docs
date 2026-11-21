===========
Utilisateur
===========

Présentation
============

Vous pouvez gérer les utilisateurs qui se connectent à |Fess|.

Gestion
=======

Affichage
---------

Pour ouvrir la page de liste de configuration des utilisateurs illustrée ci-dessous, cliquez sur [Utilisateur > Utilisateur] dans le menu de gauche.

|image0|

Cliquez sur le nom de la configuration pour la modifier.

Création de configuration
-------------------------

Cliquez sur le bouton Créer nouveau pour ouvrir la page de configuration des utilisateurs.

|image1|

Paramètres de configuration
---------------------------

Nom d'utilisateur
:::::::::::::::::

Nom d'utilisateur. Il ne peut pas être modifié après la création de l'utilisateur.

Mot de passe, Mot de passe (confirmer)
::::::::::::::::::::::::::::::::::::::

Spécifie le mot de passe de l'utilisateur, puis saisissez-le à nouveau dans Mot de passe (confirmer). Le mot de passe est obligatoire lors de la création d'un utilisateur. Lors de la modification d'un utilisateur, laissez les deux champs vides pour conserver le mot de passe actuel.

Nom de famille, Prénom, E-mail
::::::::::::::::::::::::::::::

Spécifie le nom de famille, le prénom et l'adresse e-mail de l'utilisateur. Ces champs sont facultatifs.

Rôle
::::

Spécifie les rôles auxquels l'utilisateur appartient.

.. note::

   Un utilisateur disposant du rôle ``admin-user`` peut attribuer n'importe quel rôle existant, y compris le rôle administrateur, à n'importe quel utilisateur. Traitez les rôles ``admin-*`` comme équivalents au rôle administrateur ; voir :doc:`../install/security`.

Groupe
::::::

Spécifie les groupes auxquels l'utilisateur appartient.

Suppression de configuration
----------------------------

Cliquez sur le nom de la configuration dans la page de liste, puis cliquez sur le bouton Supprimer pour afficher la boîte de dialogue de confirmation.
Cliquez sur le bouton Supprimer dans la boîte de dialogue pour supprimer la configuration.

.. |image0| image:: ../../../resources/images/fr/15.10/admin/user-1.png
.. |image1| image:: ../../../resources/images/fr/15.10/admin/user-2.png
