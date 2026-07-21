==========================
API SystemInfo
==========================

Vue d'ensemble
==============

L'API SystemInfo permet d'obtenir les informations système de |Fess|.
Vous pouvez consulter les variables d'environnement, les propriétés système Java, les propriétés de configuration de |Fess| et les informations destinées aux rapports de bogues.

URL de base
===========

::

    /api/admin/systeminfo

L'accès à cette API nécessite un jeton d'accès disposant de la permission ``Radmin-api``.
Pour les détails sur l'authentification, consultez :doc:`api-admin-overview`.

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
     - Obtention des informations système

Obtention des informations système
==================================

Requête
-------

::

    GET /api/admin/systeminfo

Cet endpoint n'accepte aucun paramètre de requête.

Réponse
-------

La réponse contient ``version`` indiquant la version du produit, ``status`` indiquant le résultat du traitement, ainsi que les quatre groupes de propriétés suivants. Chaque groupe de propriétés est un tableau d'objets possédant ``label`` et ``value``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "envProps": [
          {"label": "JAVA_HOME", "value": "/usr/lib/jvm/java-21"},
          {"label": "FESS_DICTIONARY_PATH", "value": "/var/lib/fess/dict"}
        ],
        "systemProps": [
          {"label": "java.version", "value": "21.0.1"},
          {"label": "java.vendor", "value": "Oracle Corporation"},
          {"label": "os.name", "value": "Linux"},
          {"label": "user.dir", "value": "/opt/fess"}
        ],
        "fessProps": [
          {"label": "crawler.document.max.site.length", "value": "100"},
          {"label": "indexer.thread.dump.enabled", "value": "true"},
          {"label": "app.cipher.key", "value": "XXXXXXXX"}
        ],
        "bugReportProps": [
          {"label": "os.name", "value": "Linux"},
          {"label": "java.vm.version", "value": "21.0.1+12"}
        ]
      }
    }

Champs de la réponse
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``version``
     - Version du produit |Fess| (ex. : ``15.7.0``).
   * - ``status``
     - Code indiquant le résultat du traitement. ``0`` signifie une terminaison normale.
   * - ``envProps``
     - Liste des variables d'environnement (tableau de ``label`` / ``value``). Les valeurs retournées sont celles obtenues via ``System.getenv()``, sans modification.
   * - ``systemProps``
     - Liste des propriétés système Java (tableau de ``label`` / ``value``). Les valeurs retournées sont celles obtenues via ``System.getProperties()``, sans modification.
   * - ``fessProps``
     - Liste des propriétés de configuration de |Fess| (tableau de ``label`` / ``value``). Inclut les valeurs de ``fess_config.properties`` ainsi que les propriétés système définies via l'interface d'administration. Les éléments sensibles sont masqués (voir la note ci-dessous).
   * - ``bugReportProps``
     - Liste des informations collectées pour les rapports de bogues (tableau de ``label`` / ``value``). Inclut les principales propriétés système relatives au système d'exploitation et à l'environnement d'exécution Java (``os.name``, ``os.version``, ``java.vm.version``, etc.) ainsi que les valeurs des propriétés système de |Fess|.

.. note::

   Dans ``fessProps``, les valeurs de configuration suivantes, jugées sensibles, sont masquées et retournées sous la forme ``XXXXXXXX`` :
   ``http.proxy.password``, ``ldap.admin.security.credentials``, ``spnego.preauth.password``,
   ``app.cipher.key``, ``oic.client.id``, ``oic.client.secret``.

.. warning::

   ``envProps`` (variables d'environnement) et ``systemProps`` (propriétés système Java) ne sont pas masquées :
   les valeurs configurées sont retournées telles quelles. Si des informations confidentielles (identifiants,
   mots de passe, etc.) sont stockées dans des variables d'environnement ou des propriétés système, elles
   apparaîtront dans la réponse.

Exemples d'utilisation
======================

Obtention des informations système
----------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN"

Extraction d'une propriété système spécifique
---------------------------------------------

.. code-block:: bash

    # Extraire uniquement la valeur de java.version
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.systemProps[] | select(.label == "java.version") | .value'

Affichage de la liste des variables d'environnement
---------------------------------------------------

.. code-block:: bash

    # Afficher les variables d'environnement au format label=value
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.envProps[] | "\(.label)=\(.value)"'

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-stats` - API de statistiques
- :doc:`api-admin-general` - API de configuration générale
- :doc:`../../admin/systeminfo-guide` - Guide des informations système
