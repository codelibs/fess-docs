==========================
API General
==========================

Vue d'ensemble
==============

L'API General est une API permettant de gerer les parametres generaux de |Fess|
(configuration a l'echelle du systeme). Vous pouvez obtenir et mettre a jour les
parametres relatifs au crawl, aux journaux, a l'affichage des resultats de
recherche, aux suggestions, aux periodes de conservation des journaux, aux
notifications, a l'authentification (LDAP / SSO) et a l'integration du stockage
cloud. Ces parametres correspondent aux reglages « General » de l'interface
d'administration (:doc:`../../admin/general-guide`).

URL de base
===========

::

    /api/admin/general

L'acces a cette API requiert un jeton d'acces disposant de la permission ``Radmin-api``.
Consultez :doc:`api-admin-overview` pour les details d'authentification.

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Chemin
     - Description
   * - GET
     - /
     - Obtention des parametres generaux
   * - PUT
     - /
     - Mise a jour des parametres generaux

Obtention des parametres generaux
==================================

Requete
-------

::

    GET /api/admin/general

Cet endpoint n'accepte pas de parametres de requete.

Reponse
-------

``response.setting`` contient les parametres generaux actuels. La reponse inclut
tous les champs de parametres modifiables ; l'exemple ci-dessous ne presente que
les champs representatifs. Les parametres d'activation/desactivation sont exprimes
sous forme de chaines ``"true"`` / ``"false"``, tandis que les valeurs telles que
les jours de conservation et les nombres de threads sont exprimes sous forme de
nombres.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "incrementalCrawling": "true",
          "dayForCleanup": -1,
          "crawlingThreadCount": 5,
          "searchLog": "true",
          "userInfo": "true",
          "userFavorite": "false",
          "webApiJson": "true",
          "defaultLabelValue": "",
          "defaultSortValue": "",
          "appendQueryParameter": "false",
          "loginRequired": "false",
          "thumbnail": "true",
          "failureCountThreshold": -1,
          "popularWord": "true",
          "csvFileEncoding": "UTF-8",
          "purgeSearchLogDay": 30,
          "purgeJobLogDay": 30,
          "purgeUserInfoDay": 30,
          "purgeSuggestSearchLogDay": 30,
          "notificationTo": "",
          "suggestSearchLog": "true",
          "suggestDocuments": "true",
          "ldapProviderUrl": "ldap://localhost:389/",
          "ldapBaseDn": "dc=example,dc=com",
          "ldapAdminSecurityPrincipal": "cn=admin,dc=example,dc=com",
          "ldapAdminSecurityCredentials": null,
          "storageAccessKey": "**********",
          "logLevel": "",
          "ssoType": "none",
          "storageType": "",
          "notificationLogin": "",
          "notificationSearchTop": ""
        }
      }
    }

.. note::

   Pour des raisons de securite, les mots de passe et valeurs secretes ne sont
   pas retournes tels quels. Le mot de passe de l'administrateur LDAP
   ``ldapAdminSecurityCredentials`` est toujours retourne sous la forme ``null``.
   Les autres champs secrets (``storageAccessKey``, ``storageSecretKey``,
   ``oicClientId``, ``oicClientSecret``, ``spnegoPreauthPassword``,
   ``entraidClientId``, ``entraidClientSecret``) sont retournes avec la valeur
   masquee ``"**********"`` lorsqu'ils sont definis, ou sous forme de chaine vide
   lorsqu'ils ne sont pas definis.

Mise a jour des parametres generaux
=====================================

Requete
-------

::

    PUT /api/admin/general
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

La mise a jour est traitee comme une mise a jour partielle (merge). Le serveur
charge les parametres actuels, puis ecrase uniquement les champs non ``null``
inclus dans la requete. Les champs non inclus dans la requete, et les champs
definis a ``null``, conservent leur valeur existante.

.. important::

   Le corps de la requete est valide avant l'application de l'ecrasement. Par
   consequent, les champs obligatoires (``dayForCleanup``, ``crawlingThreadCount``,
   ``failureCountThreshold``, ``csvFileEncoding``) **doivent toujours etre inclus
   dans la requete**, quelle que soit la modification effectuee. Si l'un d'eux est
   absent, la requete echoue a la validation et ``status: 1`` est retourne. Pour
   modifier uniquement certains champs, recuperez d'abord les parametres actuels
   via ``GET``, puis effectuez la requete ``PUT`` en incluant les valeurs actuelles
   des champs obligatoires.

.. note::

   Les champs de type mot de passe et secret (``ldapAdminSecurityCredentials``,
   ``storageAccessKey``, ``storageSecretKey``, ``oicClientId``, ``oicClientSecret``,
   ``spnegoPreauthPassword``, ``entraidClientId``, ``entraidClientSecret``) sont
   ignores lorsqu'une chaine vide ou la valeur masquee (``**********``) est envoyee,
   et la valeur existante est conservee. Ces champs ne sont mis a jour que lorsqu'une
   valeur reelle est envoyee.

.. code-block:: json

    {
      "incrementalCrawling": "true",
      "dayForCleanup": -1,
      "crawlingThreadCount": 10,
      "failureCountThreshold": 100,
      "csvFileEncoding": "UTF-8",
      "popularWord": "true"
    }

Principaux champs
~~~~~~~~~~~~~~~~~

Les options de configuration sont nombreuses. Les champs representatifs sont
indiques ci-dessous (tous les champs correspondent aux reglages « General » de
l'interface d'administration). Les parametres d'activation/desactivation sont
specifies sous forme de chaines ``"true"`` / ``"false"``.

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Champ
     - Requis
     - Description
   * - ``incrementalCrawling``
     - Non
     - Activer/desactiver le crawl incremental
   * - ``dayForCleanup``
     - Oui
     - Nombre de jours de conservation des documents crawles (-1 = nettoyage desactive ; plage : -1 a 1000)
   * - ``crawlingThreadCount``
     - Oui
     - Nombre de threads utilises pour le crawl (plage : 0 a 100)
   * - ``failureCountThreshold``
     - Oui
     - Seuil du nombre d'echecs pour arreter le crawl d'une URL (-1 = desactive ; plage : -1 a 10000)
   * - ``csvFileEncoding``
     - Oui
     - Encodage de l'export CSV
   * - ``searchLog``
     - Non
     - Activer/desactiver le journal des requetes de recherche
   * - ``userInfo``
     - Non
     - Activer/desactiver l'enregistrement des informations utilisateur
   * - ``userFavorite``
     - Non
     - Activer/desactiver la fonctionnalite de favoris
   * - ``webApiJson``
     - Non
     - Activer/desactiver l'API Web JSON
   * - ``popularWord``
     - Non
     - Activer/desactiver l'agregation et l'affichage des mots populaires
   * - ``defaultLabelValue``
     - Non
     - Valeur de label par defaut
   * - ``defaultSortValue``
     - Non
     - Ordre de tri par defaut
   * - ``appendQueryParameter``
     - Non
     - Ajout de parametres de requete aux URLs des resultats de recherche
   * - ``loginRequired``
     - Non
     - Exiger une connexion pour effectuer une recherche
   * - ``thumbnail``
     - Non
     - Activer/desactiver la generation de vignettes
   * - ``ignoreFailureType``
     - Non
     - Types d'echec de crawl a ignorer
   * - ``purgeSearchLogDay``
     - Non
     - Nombre de jours de conservation des journaux de recherche (-1 = desactive ; plage : -1 a 100000)
   * - ``purgeJobLogDay``
     - Non
     - Nombre de jours de conservation des journaux de taches (-1 = desactive ; plage : -1 a 100000)
   * - ``purgeUserInfoDay``
     - Non
     - Nombre de jours de conservation des informations utilisateur (-1 = desactive ; plage : -1 a 100000)
   * - ``purgeSuggestSearchLogDay``
     - Non
     - Nombre de jours de conservation des journaux de recherche de suggestion (0 = desactive ; plage : 0 a 100000)
   * - ``purgeByBots``
     - Non
     - User-Agents de bots dont les journaux de recherche doivent etre supprimes
   * - ``notificationTo``
     - Non
     - Adresse e-mail de destination des notifications systeme
   * - ``notificationLogin``
     - Non
     - Message de notification affiche sur la page de connexion
   * - ``notificationSearchTop``
     - Non
     - Message de notification affiche sur la page d'accueil de recherche
   * - ``notificationAdvanceSearch``
     - Non
     - Message de notification affiche sur la page de recherche avancee
   * - ``suggestSearchLog``
     - Non
     - Activer/desactiver les suggestions basees sur les journaux de recherche
   * - ``suggestDocuments``
     - Non
     - Activer/desactiver les suggestions basees sur les documents
   * - ``logLevel``
     - Non
     - Niveau de journalisation du journal systeme
   * - ``logNotificationEnabled``
     - Non
     - Activer/desactiver les notifications de journaux ERROR/WARN
   * - ``logNotificationLevel``
     - Non
     - Niveau de notification des journaux
   * - ``slackWebhookUrls``
     - Non
     - URL de webhook Slack pour les notifications
   * - ``googleChatWebhookUrls``
     - Non
     - URL de webhook Google Chat pour les notifications

Champs relatifs a l'authentification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les parametres relatifs a LDAP et au SSO (OpenID Connect, SAML, SPNEGO, Entra ID)
sont egalement geres par cette API. Les champs representatifs sont indiques
ci-dessous (tous les champs correspondent aux reglages « General » de l'interface
d'administration).

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Champ
     - Description
   * - ``ldapProviderUrl``
     - URL de connexion LDAP
   * - ``ldapBaseDn``
     - DN de base LDAP
   * - ``ldapSecurityPrincipal``
     - Principal de securite pour le bind LDAP
   * - ``ldapAdminSecurityPrincipal``
     - Principal de securite pour les operations d'administration LDAP
   * - ``ldapAdminSecurityCredentials``
     - Mot de passe de l'administrateur LDAP (remplace par ``null`` dans la reponse)
   * - ``ldapAccountFilter`` / ``ldapGroupFilter``
     - Filtres de recherche d'utilisateurs/groupes
   * - ``ssoType``
     - Type de SSO (``none`` / ``oic`` / ``saml`` / ``spnego`` / ``entraid``)
   * - ``oicClientId`` / ``oicClientSecret`` / ``oicAuthServerUrl`` etc.
     - Configuration OpenID Connect
   * - ``samlIdpEntityid`` / ``samlSpEntityid`` etc.
     - Configuration SAML
   * - ``spnegoKrb5Conf`` / ``spnegoLoginConf`` etc.
     - Configuration SPNEGO
   * - ``entraidClientId`` / ``entraidTenant`` etc.
     - Configuration Microsoft Entra ID

Champs relatifs au stockage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les parametres d'integration du stockage cloud (S3 / GCS) peuvent egalement etre geres.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Champ
     - Description
   * - ``storageType``
     - Type de stockage (``auto`` / ``s3`` / ``gcs``)
   * - ``storageEndpoint``
     - URL du point de terminaison du stockage
   * - ``storageAccessKey`` / ``storageSecretKey``
     - Cle d'acces / cle secrete pour l'authentification
   * - ``storageBucket``
     - Nom du bucket
   * - ``storageRegion``
     - Region S3
   * - ``storageProjectId`` / ``storageCredentialsPath``
     - ID de projet GCS / chemin du fichier d'informations d'authentification

Reponse
-------

En cas de succes de la mise a jour, seuls ``version`` et ``status`` sont retournes
(``id`` et ``created`` ne sont pas inclus).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Si la mise a jour echoue (par exemple en raison d'une erreur de validation),
``status`` est defini a une valeur non nulle (``1`` pour une erreur de validation),
et ``message`` contient les details de l'erreur. Consultez :doc:`api-admin-overview`
pour la liste des valeurs de ``status``.

Exemples d'utilisation
======================

.. note::

   Les exemples ci-dessous incluent les champs obligatoires (``dayForCleanup``,
   ``crawlingThreadCount``, ``failureCountThreshold``, ``csvFileEncoding``). Etant
   donne que ceux-ci doivent toujours etre specifies quelle que soit la modification
   effectuee, utilisez les valeurs actuelles recuperees via ``GET`` en situation reelle.

Mise a jour des parametres de crawl
-------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "incrementalCrawling": "true",
           "crawlingThreadCount": 10,
           "failureCountThreshold": 100,
           "dayForCleanup": -1,
           "csvFileEncoding": "UTF-8"
         }'

Mise a jour des periodes de conservation des journaux
-------------------------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "dayForCleanup": -1,
           "crawlingThreadCount": 5,
           "failureCountThreshold": -1,
           "csvFileEncoding": "UTF-8",
           "purgeSearchLogDay": 90,
           "purgeJobLogDay": 90,
           "purgeUserInfoDay": 90
         }'

Mise a jour des parametres de suggestion
------------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "dayForCleanup": -1,
           "crawlingThreadCount": 5,
           "failureCountThreshold": -1,
           "csvFileEncoding": "UTF-8",
           "suggestSearchLog": "true",
           "suggestDocuments": "true"
         }'

Informations complementaires
=============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-systeminfo` - API des informations systeme
- :doc:`../../admin/general-guide` - Guide des parametres generaux
