==========================
API General
==========================

Vue d'ensemble
==============

L'API General permet de gerer les parametres generaux de |Fess|.
Vous pouvez obtenir et mettre a jour les parametres relatifs a l'ensemble du systeme.

URL de base
===========

::

    /api/admin/general

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
=================================

Requete
-------

::

    GET /api/admin/general

Reponse
-------

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
          "logLevel": "",
          "ssoType": "none",
          "storageType": "",
          "notificationLogin": "",
          "notificationSearchTop": ""
        }
      }
    }

.. note::

   Pour des raisons de securite, le mot de passe de l'administrateur LDAP
   ``ldapAdminSecurityCredentials`` est toujours remplace par ``null`` dans la
   reponse (source : ``ApiAdminGeneralAction.java:71``).

Mise a jour des parametres generaux
===================================

Requete
-------

::

    PUT /api/admin/general
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

La mise a jour est traitee comme une mise a jour partielle (merge). Les champs non
inclus dans la requete conservent leur valeur existante, et les champs ``null``
sont ignores (source : ``ApiAdminGeneralAction.java:84-90``).

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
indiques ci-dessous (pour tous les champs, voir ``EditForm.java``). Les options
d'activation/desactivation de type ``available`` sont exprimees sous forme de
chaines ``"true"`` / ``"false"``.

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
     - Nombre de jours de conservation des documents crawles (-1=nettoyage desactive)
   * - ``crawlingThreadCount``
     - Oui
     - Nombre de threads utilises pour le crawl
   * - ``failureCountThreshold``
     - Oui
     - Seuil du nombre d'echecs pour arreter le crawl d'une URL (-1=desactive)
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
     - Nombre de jours de conservation des journaux de recherche (-1=desactive)
   * - ``purgeJobLogDay``
     - Non
     - Nombre de jours de conservation des journaux de taches (-1=desactive)
   * - ``purgeUserInfoDay``
     - Non
     - Nombre de jours de conservation des informations utilisateur (-1=desactive)
   * - ``purgeSuggestSearchLogDay``
     - Non
     - Nombre de jours de conservation des journaux de recherche de suggestion (0=desactive)
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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les parametres relatifs a LDAP et au SSO (OpenID Connect, SAML, SPNEGO, Entra ID)
sont egalement geres par cette API. Les champs representatifs sont indiques
ci-dessous (pour tous les champs, voir ``EditForm.java``).

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les parametres d'integration du stockage cloud (S3 / GCS) peuvent egalement etre geres.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Champ
     - Description
   * - ``storageType``
     - Type de stockage (``s3`` / ``gcs`` / ``auto``)
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

En cas de succes de la mise a jour, seul ``status`` est retourne (``id`` et
``created`` ne sont pas inclus).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Exemples d'utilisation
======================

Mise a jour des parametres de crawl
-----------------------------------

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
-----------------------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "purgeSearchLogDay": 90,
           "purgeJobLogDay": 90,
           "purgeUserInfoDay": 90
         }'

Mise a jour des parametres de suggestion
----------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestSearchLog": "true",
           "suggestDocuments": "true"
         }'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-systeminfo` - API des informations systeme
- :doc:`../../admin/general-guide` - Guide des parametres generaux
