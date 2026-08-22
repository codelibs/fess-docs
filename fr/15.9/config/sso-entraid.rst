=======================================
Configuration SSO avec Entra ID
=======================================

Aperçu
======

|Fess| prend en charge l'authentification Single Sign-On (SSO) en utilisant Microsoft Entra ID (anciennement Azure AD).
En utilisant l'authentification Entra ID, vous pouvez intégrer les informations utilisateur et les informations de groupe de votre environnement Microsoft 365 avec la recherche basée sur les rôles de |Fess|.

Fonctionnement de l'authentification Entra ID
---------------------------------------------

Dans l'authentification Entra ID, |Fess| opère en tant que client OAuth 2.0/OpenID Connect et collabore avec Microsoft Entra ID pour l'authentification.

1. L'utilisateur accède au point de terminaison SSO de |Fess| (``/sso/``)
2. |Fess| redirige vers le point de terminaison d'autorisation d'Entra ID
3. L'utilisateur s'authentifie auprès d'Entra ID (connexion Microsoft)
4. Entra ID redirige le code d'autorisation vers |Fess|
5. |Fess| utilise le code d'autorisation pour obtenir un jeton d'accès
6. L'utilisateur est connecté
7. En arrière-plan, |Fess| utilise l'API Microsoft Graph pour récupérer les informations de groupe et de rôle de l'utilisateur, et les applique à la recherche basée sur les rôles une fois la résolution terminée

.. note::
   À partir de |Fess| 15.9, la réponse d'autorisation de l'étape 4 est renvoyée via une requête
   GET, car |Fess| demande ``response_mode=query`` au point de terminaison d'autorisation.
   Jusqu'à la version 15.7, elle était renvoyée via un POST inter-sites, et la valeur par défaut
   fournie ``tomcat.sameSiteCookies = lax`` n'envoie pas le cookie de session dans ce cas ;
   ``tomcat.sameSiteCookies = none`` était donc nécessaire comme contournement. Si vous avez
   défini ``none`` uniquement pour cette raison, vous pouvez revenir à la valeur par défaut.

Pour l'intégration avec la recherche basée sur les rôles, consultez :doc:`security-role`.

Prérequis
=========

Avant de configurer l'authentification Entra ID, vérifiez les prérequis suivants :

- |Fess| 15.9 ou supérieur est installé
- Un tenant Microsoft Entra ID (Azure AD) est disponible
- |Fess| est accessible via HTTPS (requis pour les environnements de production)
- Vous avez la permission d'enregistrer des applications dans Entra ID

Configuration de base
=====================

Activation du SSO
-----------------

Pour activer l'authentification Entra ID, ajoutez le paramètre suivant dans ``app/WEB-INF/conf/system.properties`` :

::

    sso.type=entraid

Paramètres requis
-----------------

Configurez les informations obtenues d'Entra ID.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Valeur par défaut
   * - ``entraid.tenant``
     - ID du tenant (ex: ``xxx.onmicrosoft.com``)
     - (Requis)
   * - ``entraid.client.id``
     - ID d'application (Client)
     - (Requis)
   * - ``entraid.client.secret``
     - Valeur du secret client
     - (Requis)
   * - ``entraid.reply.url``
     - URI de redirection (URL de callback)
     - Utilise l'URL de la requête

.. note::
   Au lieu du préfixe ``entraid.*``, vous pouvez également utiliser le préfixe legacy ``aad.*`` pour la rétrocompatibilité.

Paramètres optionnels
---------------------

Les paramètres suivants peuvent être ajoutés si nécessaire.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Valeur par défaut
   * - ``entraid.authority``
     - URL du serveur d'authentification
     - ``https://login.microsoftonline.com/``
   * - ``entraid.state.ttl``
     - Durée de vie du state (secondes)
     - ``3600``
   * - ``entraid.response.mode``
     - Mode de renvoi de la réponse d'autorisation. Soit ``query``, soit ``form_post``.
     - ``query``
   * - ``entraid.default.groups``
     - Groupes par défaut (séparés par des virgules). Appliqués à tous les utilisateurs Entra ID.
     - (Aucun)
   * - ``entraid.default.roles``
     - Rôles par défaut (séparés par des virgules). Appliqués à tous les utilisateurs Entra ID.
     - (Aucun)
   * - ``entraid.permission.fields``
     - Champs de groupe/rôle (séparés par des virgules) à utiliser en plus comme valeurs de permission. L'ID (GUID) du groupe/rôle est toujours utilisé comme permission, et les valeurs des champs indiqués ici (ex : ``mail``) sont ajoutées. Seuls les champs dont la valeur est une chaîne de caractères peuvent être utilisés. Microsoft Graph renvoie un champ tel que ``securityEnabled`` sous forme de booléen et ``groupTypes`` sous forme de liste ; ni l'un ni l'autre ne peut devenir une valeur de permission, un tel champ est donc ignoré et un avertissement mentionnant son nom est écrit dans le journal.
     - ``mail``
   * - ``entraid.use.ds``
     - Intégration avec le service de domaine. Quand ``true``, pour les valeurs de permission au format ``name@domain``, la partie locale (``name``) sans la partie domaine est également ajoutée comme permission. Cela s'applique non seulement aux groupes et aux rôles, mais aussi à l'utilisateur connecté lui-même : la partie locale de son nom principal d'utilisateur (UPN) est ajoutée comme permission au niveau utilisateur. Le passage à ``false`` supprime donc également cette permission au niveau utilisateur, et pas seulement celles des groupes.
     - ``true``

.. note::

   L'ID (GUID) du groupe/rôle est toujours utilisé comme permission, mais seuls les groupes à
   extension messagerie possèdent une valeur ``mail``. Les groupes Microsoft 365 sont à extension
   messagerie, leur nom est donc également enregistré comme permission. **Les groupes de sécurité
   ne sont pas à extension messagerie : avec la valeur par défaut, seul leur GUID devient une
   permission.** Si les droits d'accès du système de fichiers désignent un groupe de sécurité, les
   permissions ne correspondent pas et ces documents n'apparaissent pas dans les résultats de
   recherche.

   Dans ce cas, ajoutez ``displayName``, que tous les groupes possèdent :

   .. code-block:: properties

      entraid.permission.fields=mail,displayName

   ``displayName`` n'est ni qualifié par domaine ni unique, c'est pourquoi il ne figure pas dans la
   valeur par défaut. Par exemple, si Entra ID contient un groupe nommé ``Administrators``, il
   correspondra aussi aux documents dont les droits d'accès désignent le groupe Windows intégré
   ``Administrators``. Avant de l'ajouter, vérifiez que les noms n'entrent pas en conflit avec ceux
   déjà utilisés dans vos droits d'accès.

.. note::
   Avec la valeur par défaut ``query``, le code d'autorisation figure dans la chaîne de requête de
   l'URL de callback. ``form_post`` maintient le code hors de l'URL, et donc hors de l'historique
   du navigateur et des journaux d'accès des proxys frontaux ou d'un WAF, mais il transforme le
   callback en un POST inter-sites et nécessite ``tomcat.sameSiteCookies = none``. Sans ce
   paramètre, le cookie de session n'est pas renvoyé et la connexion échoue. Les navigateurs
   n'acceptent en outre ``none`` que sur un cookie portant également l'attribut ``Secure`` :
   ``form_post`` impose donc de servir |Fess| en HTTPS. En HTTP simple, le navigateur n'enregistre
   pas du tout le cookie de session et la connexion échoue malgré tout. La plupart des
   installations doivent donc conserver la valeur par défaut. Toute autre valeur est ignorée avec
   un avertissement et ``query`` est utilisé.

.. warning::

   ``entraid.default.groups`` et ``entraid.default.roles`` sont des valeurs globales uniques, sans
   portée par utilisateur. |Fess| les applique à tous les utilisateurs Entra ID lors de la
   connexion et les réapplique à chaque résolution ultérieure, si bien que Microsoft Graph ne les
   retire jamais. En particulier, ne placez jamais le rôle d'administrateur |Fess| — ``admin`` avec
   la valeur ``authentication.admin.roles`` livrée — dans ``entraid.default.roles`` : cela
   accorderait à tous les utilisateurs du locataire un accès permanent aux écrans
   d'administration.

Configuration côté Entra ID
===========================

Enregistrement de l'application dans le portail Azure
-----------------------------------------------------

1. Connectez-vous au `Portail Azure <https://portal.azure.com/>`_

2. Sélectionnez **Microsoft Entra ID**

3. Allez dans **Gérer** → **Inscriptions d'applications** → **Nouvelle inscription**

4. Enregistrez l'application :

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - Paramètre
        - Valeur
      * - Nom
        - Tout nom (ex: Fess SSO)
      * - Types de comptes pris en charge
        - "Comptes de cet annuaire d'organisation uniquement"
      * - Plateforme
        - Web
      * - URI de redirection
        - ``https://<hôte Fess>/sso/``

5. Cliquez sur **Inscrire**

Création d'un secret client
---------------------------

1. Sur la page de détails de l'application, cliquez sur **Certificats et secrets**

2. Cliquez sur **Nouveau secret client**

3. Définissez une description et une date d'expiration, puis cliquez sur **Ajouter**

4. Copiez et sauvegardez la **Valeur** générée (cette valeur ne sera plus affichée)

.. warning::
   La valeur du secret client n'est affichée qu'immédiatement après la création.
   Assurez-vous de l'enregistrer avant de quitter la page.

Configuration des autorisations d'API
-------------------------------------

1. Cliquez sur **Autorisations d'API** dans le menu de gauche

2. Cliquez sur **Ajouter une autorisation**

3. Sélectionnez **Microsoft Graph**

4. Sélectionnez **Autorisations déléguées**

5. Ajoutez l'autorisation suivante :

   - ``User.Read`` - Requis pour récupérer les appartenances aux groupes de l'utilisateur connecté (``/me/memberOf``). Accordé par défaut lors de la création de l'inscription d'application
   - ``GroupMember.Read.All`` - Requis pour lire les attributs de groupe tels que le nom du groupe et pour résoudre les groupes imbriqués

6. Cliquez sur **Ajouter des autorisations**

7. Cliquez sur **Accorder le consentement administrateur pour <nom du tenant>**

.. note::
   Le consentement administrateur nécessite des privilèges d'administrateur de tenant.

.. note::
   ``Group.Read.All`` ou ``Directory.Read.All`` peuvent être accordés à la place de
   ``GroupMember.Read.All`` : la lecture des attributs de groupe et la résolution des groupes
   imbriqués fonctionnent également. En revanche, ``/me/memberOf`` n'est pas autorisé par
   ``Group.Read.All``, si bien que ``User.Read`` reste nécessaire dans tous les cas.

.. note::
   Les autorisations ci-dessus ne couvrent pas le ``displayName`` d'un rôle d'annuaire :
   Microsoft Graph le renvoie à null. Indiquer ``displayName`` dans
   ``entraid.permission.fields`` n'apporte donc rien pour un rôle d'annuaire, et seul
   l'identifiant (GUID) du rôle devient une autorisation. Pour utiliser les noms de rôle comme
   valeurs d'autorisation, accordez également ``RoleManagement.Read.Directory`` (ou
   ``Directory.Read.All``).

.. note::
   |Fess| demande le scope ``https://graph.microsoft.com/.default`` lors de l'acquisition d'un jeton.
   Depuis la version 15.9, ``openid profile offline_access https://graph.microsoft.com/.default`` est également envoyé au point de terminaison d'autorisation, afin que le consentement soit demandé pour le même ensemble.
   Cela signifie que toutes les autorisations d'accès configurées et consenties sur l'inscription d'application sont utilisées.
   Par conséquent, pour récupérer les informations de groupe, vous devez ajouter les autorisations ci-dessus à l'inscription d'application et accorder le consentement administrateur.

Informations à obtenir
----------------------

Les informations suivantes sont utilisées pour la configuration de Fess :

- **ID d'application (Client)** : Sur la page Vue d'ensemble, sous "ID d'application (client)"
- **ID du tenant** : Sur la page Vue d'ensemble, sous "ID de répertoire (tenant)" ou au format ``xxx.onmicrosoft.com``
- **Valeur du secret client** : La valeur créée dans Certificats et secrets

Mappage des groupes et rôles
============================

Avec l'authentification Entra ID, |Fess| récupère automatiquement les groupes et rôles auxquels un utilisateur appartient en utilisant l'API Microsoft Graph.
Les ID de groupe et noms de groupe récupérés peuvent être utilisés pour la recherche basée sur les rôles de |Fess|.

Groupes imbriqués
-----------------

|Fess| récupère non seulement les groupes auxquels les utilisateurs appartiennent directement, mais aussi les groupes parents auxquels ceux-ci appartiennent (groupes imbriqués).
La recherche de l'appartenance directe et la recherche des groupes parents s'exécutent toutes deux dans la même tâche en arrière-plan après la connexion, si bien que la connexion elle-même n'est jamais ralentie par Microsoft Graph.
La recherche des groupes parents utilise l'opération ``getMemberGroups`` de Microsoft Graph, qui résout de manière transitive : un seul appel par groupe directement attribué renvoie tous les groupes situés au-dessus de lui, quelle que soit la profondeur de l'imbrication. Les résultats récupérés sont mis en cache pendant une certaine durée. Lorsque cette tâche en arrière-plan est terminée, les permissions de l'utilisateur sont recalculées.

Paramètres de groupe par défaut
-------------------------------

Pour attribuer des groupes communs à tous les utilisateurs Entra ID :

::

    entraid.default.groups=authenticated_users,entra_users

Exemples de configuration
=========================

Configuration minimale (pour les tests)
---------------------------------------

Voici un exemple de configuration minimale pour vérification dans un environnement de test.

::

    # Activer SSO
    sso.type=entraid

    # Paramètres Entra ID
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=http://localhost:8080/sso/

Configuration recommandée (pour la production)
----------------------------------------------

Voici un exemple de configuration recommandée pour les environnements de production.

::

    # Activer SSO
    sso.type=entraid

    # Paramètres Entra ID
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=https://fess.example.com/sso/

    # Groupes par défaut (optionnel)
    entraid.default.groups=authenticated_users

Configuration legacy (rétrocompatibilité)
-----------------------------------------

Pour la compatibilité avec les versions antérieures, le préfixe ``aad.*`` peut également être utilisé.
Quand une propriété ``entraid.*`` n'est pas définie, la valeur de la propriété ``aad.*`` correspondante est utilisée. De plus, ``sso.type=aad`` est traité de la même manière que ``sso.type=entraid``.

::

    # Activer SSO (sso.type=aad peut également être utilisé)
    sso.type=entraid

    # Clés de configuration legacy
    aad.tenant=yourcompany.onmicrosoft.com
    aad.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    aad.client.secret=your-client-secret-value
    aad.reply.url=https://fess.example.com/sso/

Dépannage
=========

Problèmes courants et solutions
-------------------------------

Impossible de revenir à Fess après l'authentification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que l'URI de redirection est correctement configurée dans l'inscription de l'application du portail Azure
- Assurez-vous que la valeur de ``entraid.reply.url`` correspond exactement à la configuration du portail Azure
- Vérifiez que le protocole (HTTP/HTTPS) correspond
- Vérifiez que l'URI de redirection se termine par ``/``
- Si ``entraid.response.mode`` est défini sur ``form_post``, vérifiez à la fois que
  ``tomcat.sameSiteCookies = none`` est configuré et que |Fess| est servi en HTTPS. Avec la valeur
  par défaut ``lax``, le navigateur n'envoie pas le cookie de session avec le POST inter-sites du
  callback ; avec ``none`` en HTTP simple, le navigateur n'enregistre pas du tout ce cookie, car
  ``none`` exige l'attribut ``Secure``. Dans les deux cas, la connexion échoue une seule fois : le
  navigateur revient à la page de connexion en affichant "Le processus de connexion SSO a échoué."
  et un avertissement indiquant ``Failed to process SSO login: could not validate state`` est écrit
  dans le journal

Des erreurs d'authentification se produisent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que l'ID du tenant, l'ID client et le secret client sont correctement configurés
- Vérifiez que le secret client n'a pas expiré
- Vérifiez que le consentement administrateur a été accordé pour les autorisations d'API

Impossible de récupérer les informations de groupe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que les autorisations ``User.Read`` et ``GroupMember.Read.All`` ont été accordées
  (``GroupMember.Read.All`` peut être remplacé par ``Group.Read.All`` ou ``Directory.Read.All``,
  mais ``/me/memberOf`` exige toujours ``User.Read``)
- Vérifiez que le consentement administrateur a été accordé
- Vérifiez que l'utilisateur appartient à des groupes dans Entra ID
- Si les groupes parents imbriqués ne peuvent pas être résolus, l'avertissement
  ``Not allowed to read the parent groups of ...`` est journalisé. Accordez alors
  ``GroupMember.Read.All``
- |Fess| résout l'appartenance aux groupes et rôles de l'utilisateur en arrière-plan une fois la
  connexion terminée, si bien que la connexion elle-même n'attend jamais Microsoft Graph. Tant que
  la résolution n'est pas terminée, l'utilisateur ne dispose que de sa propre autorisation au
  niveau utilisateur et de ce qu'apportent ``entraid.default.groups`` et
  ``entraid.default.roles``. Si aucun des deux n'est défini — la valeur livrée par défaut —, une
  recherche effectuée pendant cette fenêtre ne renvoie aucun document :
  ``role.search.default.permissions`` est vide d'origine, et une configuration d'exploration créée
  avec la valeur ``role.search.default.display.permissions`` livrée accorde ``{role}guest``, rôle
  que ne possède pas un utilisateur connecté. La fenêtre dure jusqu'à environ une seconde de délai
  de planification, plus les appels à Microsoft Graph eux-mêmes — un pour les appartenances
  directes, puis un de plus pour chacun de ces groupes afin de parcourir les groupes imbriqués,
  émis les uns après les autres avec un cache froid — : elle croît donc avec le nombre de groupes
  auxquels appartient l'utilisateur. Pendant ce temps, l'écran de recherche indique à
  l'utilisateur que ses autorisations de groupe et de rôle sont en cours de chargement et l'invite
  à relancer la recherche dans un instant
- Si la résolution n'aboutit pas entièrement, l'écran de recherche indique à l'utilisateur que ses
  autorisations de groupe et de rôle n'ont pas pu être entièrement chargées, l'invite à se
  déconnecter puis à se reconnecter, et à contacter l'administrateur si le problème persiste.
  « Entièrement » est délibéré : la résolution n'est considérée comme réussie que si la requête
  des appartenances directes et le parcours des groupes imbriqués ont tous deux abouti ; un
  utilisateur qui possède ses groupes directs mais pas ses groupes parents reçoit donc aussi ce
  message. Un cas fait exception, et c'est celui que décrit le point précédent : lorsque
  Microsoft Graph refuse la recherche des groupes imbriqués avec ``Authorization_RequestDenied``
  parce que ``GroupMember.Read.All`` n'a jamais été accordé, |Fess| l'interprète non pas comme un
  échec, mais comme une réponse signifiant que le groupe n'a pas de groupe parent. La résolution
  est alors considérée comme réussie et **aucun message n'est affiché**, bien que les
  autorisations des groupes parents manquent. Le seul indice est l'avertissement
  ``Not allowed to read the parent groups of ...`` dans le journal ; vérifiez donc sa présence dès
  que des groupes imbriqués sont utilisés. La cause habituelle du cas partiel est la limitation de
  débit : un seul HTTP 429 ou 503
  de Microsoft Graph fait patienter |Fess| aussi longtemps que l'exige l'en-tête ``Retry-After``
  (60 secondes s'il n'indique rien d'exploitable, 60 minutes au maximum), et pendant ce temps
  toute recherche de groupes imbriqués est ignorée dans l'ensemble de l'instance |Fess| alors que
  les requêtes directes continuent de répondre. L'échec
  n'est pas nécessairement définitif : la résolution est relancée à chaque renouvellement du jeton
  d'accès, et une réussite ultérieure fait disparaître le message et restaure les autorisations
  manquantes. Se déconnecter puis se reconnecter relance la résolution immédiatement — ouvrir
  l'URL de connexion SSO alors qu'il est encore connecté ne fait que le rediriger vers l'écran de
  recherche

Paramètres de débogage
----------------------

Pour investiguer les problèmes, vous pouvez afficher des logs détaillés liés à Entra ID en ajustant le niveau de log de |Fess|.

Dans ``app/WEB-INF/classes/log4j2.xml``, vous pouvez ajouter le logger suivant pour changer le niveau de log :

::

    <Logger name="org.codelibs.fess.sso.entraid" level="DEBUG"/>

Référence
=========

- :doc:`security-role` - Configuration de la recherche basée sur les rôles
- :doc:`sso-saml` - Configuration SSO avec authentification SAML
- :doc:`sso-oidc` - Configuration SSO avec authentification OpenID Connect
