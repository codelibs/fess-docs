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
        "version": "15.9.0",
        "status": 0,
        "setting": {
          "incremental_crawling": "true",
          "day_for_cleanup": -1,
          "crawling_thread_count": 5,
          "search_log": "true",
          "user_info": "true",
          "user_favorite": "false",
          "web_api_json": "true",
          "default_label_value": "",
          "default_sort_value": "",
          "append_query_parameter": "false",
          "login_required": "false",
          "thumbnail": "true",
          "failure_count_threshold": -1,
          "popular_word": "true",
          "csv_file_encoding": "UTF-8",
          "purge_search_log_day": 30,
          "purge_job_log_day": 30,
          "purge_user_info_day": 30,
          "purge_suggest_search_log_day": 30,
          "notification_to": "",
          "suggest_search_log": "true",
          "suggest_documents": "true",
          "ldap_provider_url": "ldap://localhost:389/",
          "ldap_base_dn": "dc=example,dc=com",
          "ldap_admin_security_principal": "cn=admin,dc=example,dc=com",
          "log_level": "",
          "sso_type": "none",
          "storage_type": "",
          "notification_login": "",
          "notification_search_top": ""
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

   - Le mot de passe de l'administrateur LDAP ``ldap_admin_security_credentials`` n'est
     jamais inclus dans la réponse.
   - Les autres secrets (``storage_access_key`` / ``storage_secret_key`` /
     ``oic_client_id`` / ``oic_client_secret`` / ``spnego_preauth_password`` /
     ``entraid_client_id`` / ``entraid_client_secret``) sont retournés masqués sous la
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

   - ``day_for_cleanup``
   - ``crawling_thread_count``
   - ``failure_count_threshold``
   - ``csv_file_encoding``

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
      "incremental_crawling": "true",
      "day_for_cleanup": -1,
      "crawling_thread_count": 10,
      "failure_count_threshold": 100,
      "csv_file_encoding": "UTF-8",
      "popular_word": "true"
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
   * - ``incremental_crawling``
     - Non
     - Activer/désactiver le crawl incrémental
   * - ``day_for_cleanup``
     - Oui
     - Nombre de jours de conservation des documents crawlés (-1 = nettoyage désactivé ; plage : -1 à 1000)
   * - ``crawling_thread_count``
     - Oui
     - Nombre de threads utilisés pour le crawl (plage : 0 à 100)
   * - ``failure_count_threshold``
     - Oui
     - Seuil du nombre d'échecs pour arrêter le crawl d'une URL (-1 = désactivé ; plage : -1 à 10000)
   * - ``csv_file_encoding``
     - Oui
     - Encodage de l'export CSV
   * - ``search_log``
     - Non
     - Activer/désactiver le journal des requêtes de recherche
   * - ``user_info``
     - Non
     - Activer/désactiver l'enregistrement des informations utilisateur
   * - ``user_favorite``
     - Non
     - Activer/désactiver la fonctionnalité de favoris
   * - ``web_api_json``
     - Non
     - Activer/désactiver l'API Web JSON
   * - ``app_value``
     - Non
     - Valeur de configuration supplémentaire spécifique à l'application
   * - ``virtual_host_value``
     - Non
     - Configuration d'hôte virtuel (pour les configurations multi-locataires)
   * - ``popular_word``
     - Non
     - Activer/désactiver l'agrégation et l'affichage des mots populaires
   * - ``default_label_value``
     - Non
     - Valeur de label par défaut
   * - ``default_sort_value``
     - Non
     - Ordre de tri par défaut
   * - ``append_query_parameter``
     - Non
     - Ajout de paramètres de requête aux URLs des résultats de recherche
   * - ``login_required``
     - Non
     - Exiger une connexion pour effectuer une recherche
   * - ``login_link``
     - Non
     - Activer/désactiver l'affichage du lien de connexion sur l'écran de recherche
   * - ``thumbnail``
     - Non
     - Activer/désactiver la génération de vignettes
   * - ``result_collapsed``
     - Non
     - Activer/désactiver le regroupement des documents similaires dans les résultats de recherche
   * - ``ignore_failure_type``
     - Non
     - Types d'échec de crawl à ignorer
   * - ``crawling_user_agent``
     - Non
     - Chaîne User-Agent envoyée lors du crawl
   * - ``purge_search_log_day``
     - Non
     - Nombre de jours de conservation des journaux de recherche (-1 = désactivé ; plage : -1 à 100000)
   * - ``purge_job_log_day``
     - Non
     - Nombre de jours de conservation des journaux de tâches (-1 = désactivé ; plage : -1 à 100000)
   * - ``purge_user_info_day``
     - Non
     - Nombre de jours de conservation des informations utilisateur (-1 = désactivé ; plage : -1 à 100000)
   * - ``purge_suggest_search_log_day``
     - Non
     - Nombre de jours de conservation des journaux de recherche de suggestion (0 = désactivé ; plage : 0 à 100000)
   * - ``purge_by_bots``
     - Non
     - User-Agents de bots dont les journaux de recherche doivent être supprimés
   * - ``notification_to``
     - Non
     - Adresse e-mail de destination des notifications système
   * - ``notification_login``
     - Non
     - Message de notification affiché sur la page de connexion
   * - ``notification_search_top``
     - Non
     - Message de notification affiché sur la page d'accueil de recherche
   * - ``notification_advance_search``
     - Non
     - Message de notification affiché sur la page de recherche avancée
   * - ``suggest_search_log``
     - Non
     - Activer/désactiver les suggestions basées sur les journaux de recherche
   * - ``suggest_documents``
     - Non
     - Activer/désactiver les suggestions basées sur les documents
   * - ``log_level``
     - Non
     - Niveau de journalisation du journal système
   * - ``log_notification_enabled``
     - Non
     - Activer/désactiver les notifications de journaux ERROR/WARN
   * - ``log_notification_level``
     - Non
     - Niveau de notification des journaux
   * - ``slack_webhook_urls``
     - Non
     - URL de webhook Slack pour les notifications
   * - ``google_chat_webhook_urls``
     - Non
     - URL de webhook Google Chat pour les notifications
   * - ``search_use_browser_locale``
     - Non
     - Utiliser ou non la locale du navigateur pour la recherche
   * - ``rag_llm_name``
     - Non
     - Nom du fournisseur LLM utilisé pour le RAG
   * - ``llm_log_level``
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
   * - ``ldap_provider_url``
     - URL de connexion LDAP
   * - ``ldap_base_dn``
     - DN de base LDAP
   * - ``ldap_security_principal``
     - Principal de sécurité pour le bind LDAP
   * - ``ldap_admin_security_principal``
     - Principal de sécurité pour les opérations d'administration LDAP
   * - ``ldap_admin_security_credentials``
     - Mot de passe de l'administrateur LDAP (jamais inclus dans la réponse)
   * - ``ldap_account_filter`` / ``ldap_group_filter``
     - Filtres de recherche d'utilisateurs/groupes
   * - ``ldap_memberof_attribute``
     - Nom de l'attribut LDAP indiquant l'appartenance à un groupe
   * - ``sso_type``
     - Type de SSO (``none`` / ``oic`` / ``saml`` / ``spnego`` / ``entraid``)
   * - ``oic_client_id`` / ``oic_client_secret`` / ``oic_auth_server_url`` etc.
     - Configuration OpenID Connect
   * - ``saml_idp_entityid`` / ``saml_sp_entityid`` etc.
     - Configuration SAML
   * - ``spnego_krb5_conf`` / ``spnego_login_conf`` etc.
     - Configuration SPNEGO
   * - ``entraid_client_id`` / ``entraid_tenant`` etc.
     - Configuration Microsoft Entra ID

Champs relatifs au stockage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les paramètres d'intégration du stockage cloud (S3 / GCS) peuvent également être gérés.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Champ
     - Description
   * - ``storage_type``
     - Type de stockage (``auto`` / ``s3`` / ``gcs``)
   * - ``storage_endpoint``
     - URL du point de terminaison du stockage
   * - ``storage_access_key`` / ``storage_secret_key``
     - Clé d'accès / clé secrète pour l'authentification
   * - ``storage_bucket``
     - Nom du bucket
   * - ``storage_region``
     - Région S3
   * - ``storage_project_id`` / ``storage_credentials_path``
     - ID de projet GCS / chemin du fichier d'informations d'authentification

.. note::

   Les champs secrets tels que ``ldap_admin_security_credentials``,
   ``storage_access_key`` / ``storage_secret_key``, ``oic_client_id`` /
   ``oic_client_secret``, ``entraid_client_id`` / ``entraid_client_secret``, et
   ``spnego_preauth_password`` conservent leur valeur stockée (ne sont pas mis à
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
        "version": "15.9.0",
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

   Les exemples ci-dessous incluent les champs obligatoires (``day_for_cleanup``,
   ``crawling_thread_count``, ``failure_count_threshold``, ``csv_file_encoding``). Étant
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
           "incremental_crawling": "true",
           "crawling_thread_count": 10,
           "failure_count_threshold": 100,
           "day_for_cleanup": -1,
           "csv_file_encoding": "UTF-8"
         }'

Mise à jour des périodes de conservation des journaux
-------------------------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "day_for_cleanup": -1,
           "crawling_thread_count": 5,
           "failure_count_threshold": -1,
           "csv_file_encoding": "UTF-8",
           "purge_search_log_day": 90,
           "purge_job_log_day": 90,
           "purge_user_info_day": 90
         }'

Mise à jour des paramètres de suggestion
------------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "day_for_cleanup": -1,
           "crawling_thread_count": 5,
           "failure_count_threshold": -1,
           "csv_file_encoding": "UTF-8",
           "suggest_search_log": "true",
           "suggest_documents": "true"
         }'

Informations complémentaires
=============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-systeminfo` - API des informations système
- :doc:`../../admin/general-guide` - Guide des paramètres généraux
