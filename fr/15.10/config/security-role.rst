===================================================
Configuration de la recherche basée sur les rôles
===================================================

À propos de la recherche basée sur les rôles
=============================================

|Fess| permet de différencier les résultats de recherche en fonction des informations d'authentification des utilisateurs authentifiés par un système d'authentification arbitraire.
Par exemple, l'utilisateur A avec le rôle a verra les informations du rôle a dans les résultats de recherche, mais l'utilisateur B sans le rôle a ne les verra pas même en effectuant une recherche.
En utilisant cette fonctionnalité, il est possible de réaliser des recherches par département ou par poste pour les utilisateurs connectés dans un portail ou un environnement d'authentification unique.

La recherche basée sur les rôles de |Fess| peut obtenir les informations de rôle à partir de :

-  Paramètres de requête

-  En-têtes de requête

-  Cookies

-  Informations d'authentification de |Fess|

Dans les portails et les systèmes d'authentification unique de type agent, les informations de rôle peuvent être obtenues en stockant les informations d'authentification dans les cookies pour le domaine et le chemin où |Fess| est en cours d'exécution lors de l'authentification.
De plus, dans les systèmes d'authentification unique de type proxy inverse, les informations de rôle peuvent être obtenues en ajoutant les informations d'authentification aux paramètres de requête ou aux en-têtes de requête lors de l'accès à |Fess|.

.. note::
    L'obtention des informations de rôle à partir des paramètres de requête, des en-têtes de requête et des cookies est désactivée par défaut.
    Pour les utiliser, il est nécessaire de configurer le nom de la clé référencée (``parameterKey``, ``headerKey``, ``cookieKey``), le chiffrement des valeurs (``encryptedParameterValue``, etc.) et les séparateurs (``valueSeparator``, ``roleSeparator``) dans le composant ``roleQueryHelper`` du fichier ``app/WEB-INF/classes/fess.xml``.
    Par défaut, seule la recherche basée sur les rôles utilisant les informations d'authentification de |Fess| est activée.

Configuration de la recherche basée sur les rôles
==================================================

Cette section explique comment configurer la recherche basée sur les rôles en utilisant les informations d'authentification de |Fess|.

Configuration dans l'interface d'administration de |Fess|
---------------------------------------------------------

Démarrez |Fess| et connectez-vous en tant qu'administrateur.
Créez des rôles et des utilisateurs.
Par exemple, créez Role1 dans l'écran de gestion des rôles et créez un utilisateur appartenant à Role1 dans l'écran de gestion des utilisateurs.
Si vous souhaitez attribuer des permissions par groupe, créez un groupe dans l'écran de gestion des groupes et attribuez-le aux utilisateurs.

Ensuite, dans la configuration de l'exploration, saisissez ``{role}Role1`` dans le champ de permission et enregistrez.
Pour spécifier par utilisateur, vous pouvez écrire ``{user}username``, et pour spécifier par groupe, vous pouvez écrire ``{group}groupname``.
Pour spécifier plusieurs permissions, séparez-les par des sauts de ligne.

Ensuite, en effectuant une exploration avec cette configuration, un index consultable uniquement par les utilisateurs appartenant aux rôles, utilisateurs et groupes spécifiés sera créé.
Les utilisateurs connectés se voient automatiquement attribuer les permissions ``{user}username`` représentant leur propre identité, ``{role}`` pour les rôles auxquels ils appartiennent, et ``{group}`` pour les groupes auxquels ils appartiennent, qui sont ensuite comparées aux permissions définies sur les documents.

.. note::
    Pour refuser explicitement l'accès à un rôle, un utilisateur ou un groupe particulier, ajoutez le préfixe ``(deny)`` comme dans ``(deny){role}Role1`` (l'ajout de ``(allow)`` signifie autoriser l'accès, ce qui est équivalent à l'absence de spécification).

.. note::
    En cas d'intégration avec LDAP ou un système d'authentification unique, les informations de rôle et de groupe de l'utilisateur sont obtenues depuis la source d'authentification et traitées de la même manière comme permissions.
    Le comportement lors de l'intégration LDAP peut être contrôlé par les propriétés ``ldap.role.search.user.enabled``, ``ldap.role.search.group.enabled`` et ``ldap.role.search.role.enabled`` dans ``fess_config.properties`` (toutes initialisées à ``true`` par défaut).

Connexion
---------

Déconnectez-vous de l'interface d'administration.
Connectez-vous avec un utilisateur appartenant à Role1.
En cas de succès de la connexion, vous serez redirigé vers la page d'accueil de recherche.

En effectuant une recherche normale, seuls les éléments configurés avec le rôle Role1 dans la configuration de l'exploration seront affichés.

De plus, une recherche effectuée sans être connecté sera traitée comme une recherche par l'utilisateur invité (guest).
Pour les documents que vous souhaitez afficher aux utilisateurs non connectés, définissez ``{role}guest`` dans le champ de permission de la configuration de l'exploration (la valeur par défaut est définie par ``role.search.guest.permissions``).

Déconnexion
-----------

En sélectionnant la déconnexion sur l'écran de recherche alors que vous êtes connecté avec un utilisateur autre que l'administrateur, vous serez déconnecté.
