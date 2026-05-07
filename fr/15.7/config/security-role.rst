=================================
Configuration de la recherche basée sur les rôles
=================================

À propos de la recherche basée sur les rôles
==================

|Fess| permet de différencier les résultats de recherche en fonction des informations d'authentification des utilisateurs authentifiés par un système d'authentification arbitraire.
Par exemple, l'utilisateur A avec le rôle a verra les informations du rôle a dans les résultats de recherche, mais l'utilisateur B sans le rôle a ne les verra pas même en effectuant une recherche.
En utilisant cette fonctionnalité, il est possible de réaliser des recherches par département ou par poste pour les utilisateurs connectés dans un portail ou un environnement d'authentification unique.

La recherche basée sur les rôles de |Fess| peut obtenir les informations de rôle à partir de :

-  Paramètres de requête

-  En-têtes de requête

-  Cookies

-  Informations d'authentification de |Fess|

Dans les portails et les systèmes d'authentification unique de type agent, les informations de rôle peuvent être obtenues en stockant les informations d'authentification dans les cookies pour le domaine et le chemin où |Fess| fonctionne lors de l'authentification.
De plus, dans les systèmes d'authentification unique de type proxy inverse, les informations de rôle peuvent être obtenues en ajoutant les informations d'authentification aux paramètres de requête ou aux en-têtes de requête lors de l'accès à |Fess|.

Configuration de la recherche basée sur les rôles
=================

Cette section explique comment configurer la recherche basée sur les rôles en utilisant les informations d'authentification de |Fess|.

Configuration dans l'interface d'administration de |Fess|
---------------------

Démarrez |Fess| et connectez-vous en tant qu'administrateur.
Créez des rôles et des utilisateurs.
Par exemple, créez Role1 dans l'écran de gestion des rôles et créez un utilisateur appartenant à Role1 dans l'écran de gestion des utilisateurs.
Ensuite, dans la configuration de l'exploration, saisissez {role}Role1 dans le champ de permission et enregistrez.
Pour spécifier par utilisateur, vous pouvez écrire {user}nom_utilisateur, et pour spécifier par groupe, vous pouvez écrire {group}nom_groupe.
Ensuite, en effectuant une exploration avec cette configuration, un index consultable uniquement par les utilisateurs créés sera créé.

Connexion
------

Déconnectez-vous de l'interface d'administration.
Connectez-vous avec un utilisateur appartenant à Role1.
En cas de succès de la connexion, vous serez redirigé vers la page d'accueil de recherche.

En effectuant une recherche normale, seuls les éléments configurés avec le rôle Role1 dans la configuration de l'exploration seront affichés.

De plus, une recherche sans être connecté sera effectuée en tant qu'utilisateur invité.

Déconnexion
--------

En sélectionnant la déconnexion sur l'écran de recherche alors que vous êtes connecté avec un utilisateur autre que l'administrateur, vous serez déconnecté.
