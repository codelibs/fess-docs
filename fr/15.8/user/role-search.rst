==================
Recherche par rôle
==================

|Fess| propose une fonctionnalité de gestion des utilisateurs : les utilisateurs connectés peuvent effectuer des recherches en fonction des rôles auxquels ils appartiennent. Les utilisateurs gérés par |Fess| peuvent, après connexion, utiliser la recherche par rôle et modifier leur mot de passe.

La recherche par rôle compare les permissions définies sur le contenu (rôle, groupe, utilisateur) avec les permissions détenues par l'utilisateur qui effectue la recherche, et n'affiche dans les résultats que le contenu dont l'accès est autorisé. Pour la configuration de la recherche basée sur les rôles, notamment la création de rôles et d'utilisateurs, ainsi que l'attribution de permissions au contenu, reportez-vous à :doc:`../config/security-role`.


Méthode de recherche
--------------------

Si des rôles sont configurés et que le contenu a été exploré et indexé dans cet état, les résultats de recherche peuvent être affichés uniquement aux utilisateurs possédant ce rôle.
Si l'utilisateur est connecté, la recherche est effectuée en fonction des rôles et des groupes auxquels il appartient.
S'il n'est pas connecté, la recherche est effectuée en tant qu'utilisateur guest, et seul le contenu publié pour guest est affiché.

Connexion
---------

En cliquant sur le lien Connexion affiché en haut de l'écran de recherche, l'écran de connexion s'affiche. Après avoir saisi le nom d'utilisateur et le mot de passe puis vous être connecté, vous revenez à l'écran de recherche, et les recherches suivantes sont effectuées en fonction des rôles auxquels appartient cet utilisateur.

.. note::
    En cas d'intégration avec l'authentification unique ou LDAP, la connexion s'effectue selon la méthode d'authentification correspondante. De plus, l'affichage ou non du lien de connexion peut être modifié via la configuration.

Modification du mot de passe
-----------------------------

Après la connexion, cliquez sur le nom d'utilisateur affiché en haut de l'écran de recherche pour afficher le menu.

|image0|

En cliquant sur « Changer le mot de passe » dans le menu, l'écran de modification du mot de passe s'affiche.

|image1|

Saisissez le mot de passe actuel dans le champ « Mot de passe actuel », le nouveau mot de passe dans le champ « Nouveau mot de passe », confirmez-le dans le champ « Confirmer le nouveau mot de passe », puis cliquez sur le bouton « Mettre à jour » pour mettre à jour le mot de passe.
Après avoir modifié le mot de passe, vous pouvez revenir à l'écran de recherche en cliquant sur le bouton « Retour ».

.. note::
    Le menu « Changer le mot de passe » ne s'affiche que pour les utilisateurs gérés par |Fess| (ainsi que pour les utilisateurs LDAP autorisés à modifier leur mot de passe). Il ne s'affiche pas pour les utilisateurs authentifiés via l'authentification unique.
    Une politique de mot de passe (longueur, types de caractères autorisés, etc.) peut s'appliquer au nouveau mot de passe.

Déconnexion
-----------

Lorsque vous êtes connecté, cliquez sur le nom d'utilisateur affiché en haut de l'écran de recherche, puis sélectionnez « Déconnexion » dans le menu pour vous déconnecter.
Pour les utilisateurs disposant des droits d'administrateur, il est également possible de sélectionner « Administration » dans le même menu pour accéder à l'écran d'administration.



.. |image0| image:: ../../../resources/images/en/15.8/user/role-search-1.png
.. pdf   :width: 200 px
.. |image1| image:: ../../../resources/images/en/15.8/user/role-search-2.png
.. pdf   :width: 300 px
