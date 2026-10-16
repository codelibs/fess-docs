======
Groupe
======

Présentation
============

Vous pouvez gérer les groupes auxquels les utilisateurs appartiennent.
Cela peut être utilisé pour l'intégration LDAP, par exemple.

Gestion
=======

Affichage
---------

Pour ouvrir la page de liste pour configurer les groupes illustrée ci-dessous, cliquez sur [Utilisateur > Groupe] dans le menu de gauche.

|image0|

Cliquez sur le nom de la configuration pour la modifier.

Création de configuration
-------------------------

Cliquez sur le bouton Nouvelle création pour ouvrir la page de configuration des groupes.

|image1|

Paramètres de configuration
---------------------------

Nom
::::

Nom du groupe.

gidNumber
:::::::::

Le gidNumber (l'ID de groupe POSIX dans LDAP) du groupe, sous forme de nombre. Il est facultatif. La saisie d'une valeur qui n'est pas un nombre provoque une erreur.
Lorsque |Fess| est configuré pour gérer LDAP depuis les écrans d'administration (``ldap.admin.enabled=true``), la valeur est écrite dans l'attribut ``gidNumber`` de l'entrée du groupe dans LDAP (le nom de l'attribut peut être modifié avec ``ldap.attr.gidNumber``). Si vous n'utilisez pas LDAP, il n'est pas nécessaire de le renseigner.

Méthode de suppression
----------------------

Cliquez sur le nom de la configuration dans la page de liste, puis cliquez sur le bouton Supprimer pour afficher l'écran de confirmation.
Appuyer sur le bouton Supprimer supprimera la configuration.

.. |image0| image:: ../../../resources/images/en/15.10/admin/group-1.png
.. |image1| image:: ../../../resources/images/en/15.10/admin/group-2.png
