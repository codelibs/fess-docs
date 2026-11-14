========================================================
Configuration de la connexion par clé d'accès (WebAuthn)
========================================================

Aperçu
======

|Fess| permet à un utilisateur local (un utilisateur créé sous « Utilisateur » dans l'écran d'administration) de se connecter avec une clé d'accès (passkey, WebAuthn) au lieu d'un mot de passe. La fonctionnalité est nouvelle dans la 15.10 et est désactivée par défaut.

- Un utilisateur peut se connecter avec le mot de passe ou avec une clé d'accès. Il ne s'agit pas d'une authentification multifacteur qui exigerait les deux.
- Seul un utilisateur local de l'index ``fess_user`` est concerné. Un utilisateur LDAP ou SSO ne peut pas enregistrer de clé d'accès, et une connexion par clé d'accès n'interroge jamais LDAP.
- |Fess| stocke la clé publique, le nom de la clé d'accès, etc. La clé privée reste dans l'authentificateur de l'utilisateur (un navigateur, un système d'exploitation, une clé de sécurité, etc.) et n'atteint jamais |Fess|.

Paramètres
==========

Les paramètres des clés d'accès se placent dans ``fess_config.properties`` (``app/WEB-INF/classes/fess_config.properties`` pour le package ZIP, ``/etc/fess/fess_config.properties`` pour les packages RPM/DEB). Ils n'ont pas d'élément dans « Système » > « Général » de l'écran d'administration et ne peuvent pas être définis dans ``system.properties``. Un redémarrage de |Fess| est nécessaire pour appliquer une modification. Avec Docker, vous pouvez les transmettre sous la forme ``-Dfess.config.passkey.enabled=true`` dans ``FESS_JAVA_OPTS`` (voir :doc:`../install/install-docker`).

.. list-table::
   :header-rows: 1
   :widths: 22 18 60

   * - Clé
     - Valeur par défaut
     - Description
   * - ``passkey.enabled``
     - ``false``
     - Active la connexion par clé d'accès. Même avec ``true``, la fonctionnalité reste désactivée tant que ``passkey.rp.id`` et ``passkey.origins`` ci-dessous ne contiennent pas de valeurs utilisables.
   * - ``passkey.rp.id``
     - (vide)
     - ID de la partie de confiance (relying party) : le domaine auquel les clés d'accès sont liées (par exemple ``example.com``). Une clé d'accès ne fonctionne que sur cet hôte et ses sous-domaines.
   * - ``passkey.rp.name``
     - ``Fess``
     - Le nom de la partie de confiance que le navigateur affiche lors de la création d'une clé d'accès.
   * - ``passkey.origins``
     - (vide)
     - Les origines (séparées par des virgules) dont une cérémonie de clé d'accès est acceptée (par exemple ``https://fess.example.com``). Chaque entrée doit être une origine ``http`` ou ``https`` avec un nom d'hôte.

Exemple d'activation de la fonctionnalité :
::

    passkey.enabled=true
    passkey.rp.id=example.com
    passkey.rp.name=Fess
    passkey.origins=https://fess.example.com

- ``passkey.rp.id`` est le domaine auquel toutes les clés d'accès sont liées. Le modifier alors que des utilisateurs ont enregistré des clés d'accès les rend toutes inutilisables, et les utilisateurs doivent se réenregistrer sous le nouvel ID ; choisissez-le donc une fois pour toutes. L'hôte de chaque origine de ``passkey.origins`` doit être ``passkey.rp.id`` ou l'un de ses sous-domaines.
- ``passkey.origins`` énumère telles quelles les origines (schéma, hôte et port) auxquelles les utilisateurs ouvrent |Fess| dans le navigateur, et non les adresses situées derrière un reverse proxy. Une cérémonie provenant de toute autre origine est rejetée.

Cas où la fonctionnalité reste désactivée
-----------------------------------------

Même avec ``passkey.enabled=true``, les clés d'accès **restent désactivées sans aucune erreur à l'écran** dans les cas ci-dessous. Les écrans de connexion n'affichent aucun bouton de clé d'accès, toutes les API sous ``/api/v2/auth/passkey`` répondent ``404`` et ``features.passkey_enabled`` de ``/api/v2/ui/config`` vaut ``false``. La raison figure dans un avertissement de ``fess.log`` ; chaque avertissement n'est écrit qu'une seule fois après le démarrage.

- ``passkey.rp.id`` ou ``passkey.origins`` est vide : ``passkey.enabled is true but passkey.rp.id or passkey.origins is empty, so passkeys are disabled.``
- ``passkey.origins`` ne contient aucune entrée : ``passkey.enabled is true but passkey.origins holds no origin, so passkeys are disabled.``
- ``passkey.origins`` contient une entrée qui n'est pas une origine ``http`` ou ``https`` (une valeur sans nom d'hôte, un autre schéma, etc.) : ``passkey.origins holds an entry that is not an http or https origin, so passkeys are disabled: entry=...``

Lorsque ``passkey.origins`` est utilisable mais que l'origine à laquelle l'utilisateur ouvre |Fess| n'y figure pas, tous les enregistrements et toutes les connexions sont rejetés. L'écran de l'utilisateur n'indique aucune raison ; consultez donc ``fess.log`` : ``A passkey response came from an origin that is not in passkey.origins: origin=...`` indique l'origine rejetée et le paramètre (seule la première est écrite). Ajoutez cette origine à ``passkey.origins``.

Utilisation
===========

Connexion
---------

Lorsque les clés d'accès sont activées et que le navigateur prend en charge WebAuthn, un bouton « Se connecter avec une clé d'accès » apparaît dans la connexion de l'écran de recherche et sur la page de connexion de l'écran d'administration. Le navigateur demande l'authentificateur, et l'utilisateur se connecte sans saisir de nom d'utilisateur.

Une connexion par clé d'accès utilise la même limite de débit par adresse IP (``theme.api.login.*``) qu'une connexion par mot de passe. Un échec s'y compte, et un succès restitue le décompte (voir :doc:`rate-limiting`). L'écran n'indique pas la raison d'un échec ; il affiche le même message que pour un mot de passe erroné.

Enregistrement et suppression des clés d'accès
----------------------------------------------

Un utilisateur local enregistre et supprime ses propres clés d'accès sous « Clés d'accès » dans « Changer le mot de passe » (``/profile``) du menu utilisateur de l'écran de recherche.

1. Saisissez un nom pour la clé d'accès (64 caractères au maximum) et le mot de passe actuel, puis appuyez sur « Enregistrer une clé d'accès ».
2. Suivez les invites du navigateur pour créer la clé d'accès sur un authentificateur.

- Le mot de passe actuel est exigé à chaque enregistrement. Un utilisateur local dont le nom et le mot de passe sont aussi acceptés par l'annuaire (LDAP) ne peut pas enregistrer de clé d'accès, car la vérification du mot de passe ne peut pas dire quel compte elle a vérifié.
- Un utilisateur peut avoir jusqu'à 20 clés d'accès.
- La section « Clés d'accès » n'est pas affichée à un utilisateur qui n'a aucune clé d'accès et ne peut pas en enregistrer (un utilisateur LDAP ou SSO, ou un navigateur sans WebAuthn).
- La suppression d'une clé d'accès **met fin aux autres sessions de connexion** de l'utilisateur, afin qu'une session ouverte avec un authentificateur perdu ne survive pas. Le fonctionnement est le même que pour un changement de mot de passe (voir « Relation avec le mot de passe » ci-dessous). La session qui a effectué la suppression est conservée.

Actions de l'administrateur
---------------------------

La page de détails d'un utilisateur sous « Utilisateur » dans l'écran d'administration liste les clés d'accès de l'utilisateur (libellé, date de création, date de dernière utilisation). Un administrateur ne peut pas enregistrer de clé d'accès, mais un administrateur disposant de la permission d'édition peut en supprimer une avec « Réinitialiser », par exemple lorsque l'utilisateur a perdu l'authentificateur. L'utilisateur peut alors enregistrer une nouvelle clé d'accès. Une réinitialisation met aussi fin aux sessions de connexion de cet utilisateur (voir « Relation avec le mot de passe » ci-dessous).

Une fois ``passkey.enabled`` remis à ``false``, la page de détails liste encore les clés d'accès d'un utilisateur qui en a, et elles peuvent être supprimées. La désactivation de la fonctionnalité ne supprime pas les données des clés d'accès.

Relation avec le mot de passe
=============================

- Une clé d'accès et un mot de passe sont des identifiants distincts. Modifier le mot de passe d'un utilisateur, ou qu'un administrateur en définisse un nouveau, ne supprime pas les clés d'accès enregistrées, et elles peuvent toujours servir à se connecter.
- Lorsqu'un mot de passe est modifié, les autres sessions de connexion de l'utilisateur prennent fin (voir :doc:`../install/security`). Cela inclut une session ouverte avec une clé d'accès. Chaque session vérifie au plus une fois toutes les ``password.changed.check.interval`` secondes (``60`` par défaut), de sorte que les sessions prennent fin dans ce délai.
- La suppression d'une clé d'accès met fin aux autres sessions de la même façon (voir ci-dessus).

Suppression et renommage des utilisateurs
=========================================

Une clé d'accès est liée à un utilisateur par le seul nom d'utilisateur. Pour qu'un autre utilisateur portant le même nom ne l'hérite pas, les clés d'accès sont aussi supprimées dans les cas suivants :

- Lorsqu'un utilisateur est supprimé.
- Lorsqu'un utilisateur est créé (toute clé d'accès restée sous ce nom est supprimée).
- Lorsqu'un utilisateur est renommé (les clés d'accès de l'ancien nom et du nouveau nom sont supprimées). Une clé d'accès ne suit pas un renommage ; l'utilisateur se réenregistre donc. Un renommage vers un nom qu'un autre utilisateur porte déjà est refusé avant toute suppression de clé d'accès.

Stockage et sauvegarde
======================

Les clés d'accès sont stockées dans l'index ``fess_user.passkey`` (le préfixe est ``index.user.index``, ``fess_user`` par défaut). L'index est créé au démarrage de |Fess| même si les clés d'accès sont désactivées, et il est utilisé lors de la suppression ou du renommage d'un utilisateur et sur la page de détails de l'utilisateur. Si |Fess| n'est pas autorisé à créer des index, créez-le avant la mise à niveau (voir :ref:`upgrade-1510-passkey`).

L'index ne rejoint pas l'alias ``fess_user``, de sorte que ``fess_user.bulk`` de « Sauvegarde » dans l'écran d'administration ne contient pas les clés d'accès. Après une restauration à partir d'une sauvegarde, les utilisateurs réenregistrent leurs clés d'accès.

Prérequis
=========

- **HTTPS** : les navigateurs n'autorisent WebAuthn que dans un contexte sécurisé (HTTPS, ou ``localhost``). |Fess| accepte aussi une origine ``http`` dans ``passkey.origins``, mais en production, servez |Fess| en HTTPS et indiquez des origines ``https://`` (voir « Activation de HTTPS » dans :doc:`../install/security`).
- **Navigateur** : un navigateur qui fournit l'API WebAuthn (``PublicKeyCredential``) est nécessaire. Dans un navigateur qui ne la fournit pas, ni le bouton de connexion ni la section d'enregistrement ne sont affichés.
- **Authentificateur** : il doit prendre en charge les identifiants découvrables (discoverable credentials) et la vérification de l'utilisateur (un code PIN, la biométrie, etc.). |Fess| exige les deux, prend en charge les algorithmes de signature ES256 et RS256, et n'utilise pas l'attestation.
- **Plusieurs nœuds** : le défi (challenge) d'une cérémonie de clé d'accès est conservé dans la session HTTP pendant 5 minutes. Lorsque vous exécutez plusieurs nœuds derrière un répartiteur de charge, partagez les sessions entre les nœuds (variable d'environnement ``FESS_SESSION_STORE=opensearch``) ou configurez le répartiteur de charge pour qu'il rattache chaque session à un seul nœud.

API
===

Les API de clés d'accès se trouvent sous ``/api/v2/auth/passkey``. Toutes répondent ``404`` tant que les clés d'accès sont désactivées. ``features.passkey_enabled`` de ``/api/v2/ui/config`` indique si la fonctionnalité est disponible (voir :doc:`../api/api-uiconfig`).

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Point d'accès
     - Description
   * - ``POST /api/v2/auth/passkey/login/options``
     - Obtient les options de connexion (le défi).
   * - ``POST /api/v2/auth/passkey/login/verify``
     - Vérifie la réponse de l'authentificateur et connecte l'utilisateur.
   * - ``GET /api/v2/auth/passkey``
     - Liste les clés d'accès de l'utilisateur connecté et indique s'il peut en enregistrer une (``can_register``).
   * - ``POST /api/v2/auth/passkey/register/options``
     - Vérifie le mot de passe actuel (``current_password``) et obtient les options d'enregistrement.
   * - ``POST /api/v2/auth/passkey/register/verify``
     - Vérifie le nom (``label``) et la réponse de l'authentificateur, puis enregistre la clé d'accès.
   * - ``DELETE /api/v2/auth/passkey/{credentialId}``
     - Supprime une clé d'accès de l'utilisateur connecté.

Les appels ``register`` et la suppression exigent l'en-tête ``X-Fess-CSRF-Token``. Les deux appels de connexion n'exigent aucun jeton CSRF, comme ``/api/v2/auth/login``.

Dépannage
=========

Le bouton de clé d'accès n'est pas affiché
------------------------------------------

- Vérifiez ``features.passkey_enabled`` de ``/api/v2/ui/config``. S'il vaut ``false``, cherchez un avertissement dans ``fess.log`` pour savoir si les paramètres sont utilisables (voir « Cas où la fonctionnalité reste désactivée » ci-dessus).
- Vérifiez que |Fess| a été redémarré après la modification.
- Vérifiez que le navigateur prend en charge WebAuthn et que la page est ouverte en HTTPS (ou sur ``localhost``).
- Si vous utilisez un thème autre que celui fourni, le thème doit prendre en charge le bouton de clé d'accès.

L'enregistrement ou la connexion échoue
---------------------------------------

- Si ``fess.log`` contient un avertissement comportant ``is not in passkey.origins``, ajoutez à ``passkey.origins`` l'origine ouverte dans le navigateur.
- Après la modification de ``passkey.rp.id``, les clés d'accès enregistrées avant la modification ne peuvent plus être utilisées. Supprimez les anciennes clés d'accès et enregistrez-les de nouveau.
