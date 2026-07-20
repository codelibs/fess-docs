==========================
API General
==========================

Vue d'ensemble
==============

L'API General est une API permettant de gérer les paramètres généraux de |Fess|
(configuration à l'échelle du système). Vous pouvez obtenir et mettre à jour les
paramètres relatifs au crawl, aux journaux, à l'affichage des résultats de
recherche, aux suggestions, aux périodes de conservation des journaux, aux
notifications, à l'authentification (LDAP / SSO) et à l'intégration du stockage
cloud. Ces paramètres correspondent aux réglages « General » de l'interface
d'administration (:doc:`../../admin/general-guide`).

URL de base
===========

::

    /api/admin/general

L'accès à cette API requiert un jeton d'accès disposant de la permission ``Radmin-api``.
Consultez :doc:`api-admin-overview` pour les détails d'authentification.

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Méthode
     - Chemin
     - Description
   * - GET
     - /
     - Obtention des paramètres généraux
   * - PUT
     - /
     - Mise à jour des paramètres généraux

Obtention des paramètres généraux
==================================

Requête
-------

::

    GET /api/admin/general

Cet endpoint n'accepte pas de paramètres de requête.

Réponse
-------

``response.setting`` contient les paramètres généraux actuels. La réponse inclut
tous les champs de paramètres modifiables ; l'exemple ci-dessous ne présente que
les champs représentatifs. Les paramètres d'activation/désactivation sont exprimés
sous forme de chaînes ``"true"`` / ``"false"``, tandis que les valeurs telles que
les jours de conservation et les nombres de threads sont exprimées sous forme de
nombres.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
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

   Ce qui précède ne montre que les champs représentatifs à titre d'exemple. L'objet
   ``setting`` réel dans la réponse contient tous les champs des paramètres généraux
   (crawl, recherche, notification, LDAP, SSO, stockage, etc.). Consultez la page des
   réglages « General » de l'interface d'administration pour la liste complète des champs.

.. note::

   Pour des raisons de sécurité, les champs contenant des informations
   d'authentification ne sont pas retournés avec leur valeur réelle.

   - Le mot de passe de l'administrateur LDAP ``ldapAdminSecurityCredentials`` est
     toujours retourné sous la forme ``null``.
   - Les autres secrets (``storageAccessKey`` / ``storageSecretKey`` /
     ``oicClientId`` / ``oicClientSecret`` / ``spnegoPreauthPassword`` /
     ``entraidClientId`` / ``entraidClientSecret``) sont retournés masqués sous la
     forme ``"**********"`` lorsqu'ils sont définis, ou sous forme de chaîne vide
     (``""``) lorsqu'ils ne sont pas définis.

Mise à jour des paramètres généraux
=====================================

Requête
-------

::

    PUT /api/admin/general
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

La mise à jour est traitée comme une mise à jour partielle (merge). Le serveur
charge les paramètres actuels, puis écrase uniquement les champs non ``null``
inclus dans la requête. Les champs non inclus dans la requête, et les champs
définis à ``null``, conservent leur valeur existante.

.. warning::

   Les quatre champs suivants sont obligatoires et **doivent** être inclus dans
   **chaque** requête PUT, même lors d'une mise à jour partielle :

   - ``dayForCleanup``
   - ``crawlingThreadCount``
   - ``failureCountThreshold``
   - ``csvFileEncoding``

   Si l'un d'eux est absent, la requête échoue à la validation et l'API retourne
   HTTP 400 avec ``status: 1`` et un ``message`` d'erreur. La valeur envoyée écrase
   le paramètre existant ; si vous ne souhaitez pas modifier une valeur, récupérez
   d'abord la valeur actuelle avec ``GET`` et renvoyez-la telle quelle. Tous les
   autres champs sont optionnels ; les champs omis conservent leur valeur existante.

.. note::

   Les champs numériques font l'objet d'une validation de type et de plage. L'envoi
   d'une valeur qui ne peut pas être interprétée comme un entier, ou d'une valeur
   hors de la plage autorisée, provoque une erreur de validation (HTTP 400 avec
   ``status: 1``). La plage valide de chaque champ numérique est indiquée dans le
   tableau des champs ci-dessous.

.. note::

   Pour les champs d'activation/désactivation (type ``available``), seuls ``"true"``
   ou ``"on"`` (les deux sans distinction de casse) signifient l'activation. Toute
   autre valeur (comme ``"false"`` ou une chaîne vide) est traitée comme une
   désactivation (``false``). La valeur existante n'est conservée que lorsque le
   champ est omis (non envoyé). Dans la réponse GET, ces champs sont retournés sous
   forme de chaînes ``"true"`` / ``"false"``.

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

Les options de configuration sont nombreuses. Les champs représentatifs sont
indiqués ci-dessous (tous les champs correspondent aux réglages « General » de
l'interface d'administration). Les paramètres d'activation/désactivation sont
spécifiés sous forme de chaînes ``"true"`` / ``"false"``.

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Champ
     - Requis
     - Description
   * - ``incrementalCrawling``
     - Non
     - Activer/désactiver le crawl incrémental
   * - ``dayForCleanup``
     - Oui
     - Nombre de jours de conservation des documents crawlés (-1 = nettoyage désactivé ; plage : -1 à 1000)
   * - ``crawlingThreadCount``
     - Oui
     - Nombre de threads utilisés pour le crawl (plage : 0 à 100)
   * - ``failureCountThreshold``
     - Oui
     - Seuil du nombre d'échecs pour arrêter le crawl d'une URL (-1 = désactivé ; plage : -1 à 10000)
   * - ``csvFileEncoding``
     - Oui
     - Encodage de l'export CSV
   * - ``searchLog``
     - Non
     - Activer/désactiver le journal des requêtes de recherche
   * - ``userInfo``
     - Non
     - Activer/désactiver l'enregistrement des informations utilisateur
   * - ``userFavorite``
     - Non
     - Activer/désactiver la fonctionnalité de favoris
   * - ``webApiJson``
     - Non
     - Activer/désactiver l'API Web JSON
   * - ``appValue``
     - Non
     - Valeur de configuration supplémentaire spécifique à l'application
   * - ``virtualHostValue``
     - Non
     - Configuration d'hôte virtuel (pour les configurations multi-locataires)
   * - ``popularWord``
     - Non
     - Activer/désactiver l'agrégation et l'affichage des mots populaires
   * - ``defaultLabelValue``
     - Non
     - Valeur de label par défaut
   * - ``defaultSortValue``
     - Non
     - Ordre de tri par défaut
   * - ``appendQueryParameter``
     - Non
     - Ajout de paramètres de requête aux URLs des résultats de recherche
   * - ``loginRequired``
     - Non
     - Exiger une connexion pour effectuer une recherche
   * - ``loginLink``
     - Non
     - Activer/désactiver l'affichage du lien de connexion sur l'écran de recherche
   * - ``thumbnail``
     - Non
     - Activer/désactiver la génération de vignettes
   * - ``resultCollapsed``
     - Non
     - Activer/désactiver le regroupement des documents similaires dans les résultats de recherche
   * - ``ignoreFailureType``
     - Non
     - Types d'échec de crawl à ignorer
   * - ``crawlingUserAgent``
     - Non
     - Chaîne User-Agent envoyée lors du crawl
   * - ``purgeSearchLogDay``
     - Non
     - Nombre de jours de conservation des journaux de recherche (-1 = désactivé ; plage : -1 à 100000)
   * - ``purgeJobLogDay``
     - Non
     - Nombre de jours de conservation des journaux de tâches (-1 = désactivé ; plage : -1 à 100000)
   * - ``purgeUserInfoDay``
     - Non
     - Nombre de jours de conservation des informations utilisateur (-1 = désactivé ; plage : -1 à 100000)
   * - ``purgeSuggestSearchLogDay``
     - Non
     - Nombre de jours de conservation des journaux de recherche de suggestion (0 = désactivé ; plage : 0 à 100000)
   * - ``purgeByBots``
     - Non
     - User-Agents de bots dont les journaux de recherche doivent être supprimés
   * - ``notificationTo``
     - Non
     - Adresse e-mail de destination des notifications système
   * - ``notificationLogin``
     - Non
     - Message de notification affiché sur la page de connexion
   * - ``notificationSearchTop``
     - Non
     - Message de notification affiché sur la page d'accueil de recherche
   * - ``notificationAdvanceSearch``
     - Non
     - Message de notification affiché sur la page de recherche avancée
   * - ``suggestSearchLog``
     - Non
     - Activer/désactiver les suggestions basées sur les journaux de recherche
   * - ``suggestDocuments``
     - Non
     - Activer/désactiver les suggestions basées sur les documents
   * - ``logLevel``
     - Non
     - Niveau de journalisation du journal système
   * - ``logNotificationEnabled``
     - Non
     - Activer/désactiver les notifications de journaux ERROR/WARN
   * - ``logNotificationLevel``
     - Non
     - Niveau de notification des journaux
   * - ``slackWebhookUrls``
     - Non
     - URL de webhook Slack pour les notifications
   * - ``googleChatWebhookUrls``
     - Non
     - URL de webhook Google Chat pour les notifications
   * - ``searchUseBrowserLocale``
     - Non
     - Utiliser ou non la locale du navigateur pour la recherche
   * - ``ragLlmName``
     - Non
     - Nom du fournisseur LLM utilisé pour le RAG
   * - ``llmLogLevel``
     - Non
     - Niveau de journalisation des paquets liés au LLM

Champs relatifs à l'authentification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les paramètres relatifs à LDAP et au SSO (OpenID Connect, SAML, SPNEGO, Entra ID)
sont également gérés par cette API. Les champs représentatifs sont indiqués
ci-dessous (tous les champs correspondent aux réglages « General » de l'interface
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
     - Principal de sécurité pour le bind LDAP
   * - ``ldapAdminSecurityPrincipal``
     - Principal de sécurité pour les opérations d'administration LDAP
   * - ``ldapAdminSecurityCredentials``
     - Mot de passe de l'administrateur LDAP (remplacé par ``null`` dans la réponse)
   * - ``ldapAccountFilter`` / ``ldapGroupFilter``
     - Filtres de recherche d'utilisateurs/groupes
   * - ``ldapMemberofAttribute``
     - Nom de l'attribut LDAP indiquant l'appartenance à un groupe
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

Les paramètres d'intégration du stockage cloud (S3 / GCS) peuvent également être gérés.

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
     - Clé d'accès / clé secrète pour l'authentification
   * - ``storageBucket``
     - Nom du bucket
   * - ``storageRegion``
     - Région S3
   * - ``storageProjectId`` / ``storageCredentialsPath``
     - ID de projet GCS / chemin du fichier d'informations d'authentification

.. note::

   Les champs secrets tels que ``ldapAdminSecurityCredentials``,
   ``storageAccessKey`` / ``storageSecretKey``, ``oicClientId`` /
   ``oicClientSecret``, ``entraidClientId`` / ``entraidClientSecret``, et
   ``spnegoPreauthPassword`` conservent leur valeur stockée (ne sont pas mis à
   jour) lorsque la valeur masquée ``"**********"`` est envoyée telle quelle.
   N'envoyez la valeur réelle que lorsque vous souhaitez la modifier.

   Cette vérification étant basée sur le fait que la chaîne est vide après
   suppression des astérisques, l'envoi d'une chaîne vide (``""``) ou d'une valeur
   composée uniquement d'astérisques laisse également la valeur inchangée. Par
   conséquent, ces champs secrets ne peuvent pas être vides via l'API.

Réponse
-------

En cas de succès de la mise à jour, seuls ``version`` et ``status`` sont retournés
(``id`` et ``created`` ne sont pas inclus).

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

Si la mise à jour échoue (par exemple en raison d'une erreur de validation), l'API
retourne HTTP 400 et ``status`` est défini à une valeur non nulle (``1`` pour une
erreur de validation), et ``message`` contient les détails de l'erreur. Consultez
:doc:`api-admin-overview` pour la liste des valeurs de ``status``.

Exemples d'utilisation
======================

.. note::

   Les exemples ci-dessous incluent les champs obligatoires (``dayForCleanup``,
   ``crawlingThreadCount``, ``failureCountThreshold``, ``csvFileEncoding``). Étant
   donné que ceux-ci doivent toujours être envoyés quelle que soit la modification
   effectuée, récupérez les valeurs actuelles avec ``GET`` et incluez-les en
   situation réelle (les exemples ci-dessous utilisent les valeurs par défaut).

Mise à jour des paramètres de crawl
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

Mise à jour des périodes de conservation des journaux
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

Mise à jour des paramètres de suggestion
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

Informations complémentaires
=============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-systeminfo` - API des informations système
- :doc:`../../admin/general-guide` - Guide des paramètres généraux
