==========================
API SystemInfo
==========================

Vue d'ensemble
==============

L'API SystemInfo permet d'obtenir les informations systeme de |Fess|.
Vous pouvez consulter les variables d'environnement, les proprietes systeme Java, les proprietes de configuration de |Fess| et les informations destinees aux rapports de bogues.

URL de base
===========

::

    /api/admin/systeminfo

L'acces a cette API necessite un jeton d'acces disposant de la permission ``Radmin-api``.
Pour les details sur l'authentification, consultez :doc:`api-admin-overview`.

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
     - Obtention des informations systeme

Obtention des informations systeme
==================================

Requete
-------

::

    GET /api/admin/systeminfo

Cet endpoint n'accepte aucun parametre de requete.

Reponse
-------

La reponse contient ``version`` indiquant la version du produit, ``status`` indiquant le resultat du traitement, ainsi que les quatre groupes de proprietes suivants. Chaque groupe de proprietes est un tableau d'objets possedant ``label`` et ``value``.

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

Champs de la reponse
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``version``
     - Version du produit |Fess| (ex. : ``15.7.0``).
   * - ``status``
     - Code indiquant le resultat du traitement. ``0`` signifie une terminaison normale.
   * - ``envProps``
     - Liste des variables d'environnement (tableau de ``label`` / ``value``). Les valeurs retournees sont celles obtenues via ``System.getenv()``, sans modification.
   * - ``systemProps``
     - Liste des proprietes systeme Java (tableau de ``label`` / ``value``). Les valeurs retournees sont celles obtenues via ``System.getProperties()``, sans modification.
   * - ``fessProps``
     - Liste des proprietes de configuration de |Fess| (tableau de ``label`` / ``value``). Inclut les valeurs de ``fess_config.properties`` ainsi que les proprietes systeme definies via l'interface d'administration. Les elements sensibles sont masques (voir la note ci-dessous).
   * - ``bugReportProps``
     - Liste des informations collectees pour les rapports de bogues (tableau de ``label`` / ``value``). Inclut les principales proprietes systeme relatives au systeme d'exploitation et a l'environnement d'execution Java (``os.name``, ``os.version``, ``java.vm.version``, etc.) ainsi que les valeurs des proprietes systeme de |Fess|.

.. note::

   Dans ``fessProps``, les valeurs de configuration suivantes, jugees sensibles, sont masquees et retournees sous la forme ``XXXXXXXX`` :
   ``http.proxy.password``, ``ldap.admin.security.credentials``, ``spnego.preauth.password``,
   ``app.cipher.key``, ``oic.client.id``, ``oic.client.secret``.

.. warning::

   ``envProps`` (variables d'environnement) et ``systemProps`` (proprietes systeme Java) ne sont pas masquees :
   les valeurs configurees sont retournees telles quelles. Si des informations confidentielles (identifiants,
   mots de passe, etc.) sont stockees dans des variables d'environnement ou des proprietes systeme, elles
   apparaitront dans la reponse.

Exemples d'utilisation
======================

Obtention des informations systeme
----------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN"

Extraction d'une propriete systeme specifique
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

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-stats` - API de statistiques
- :doc:`api-admin-general` - API de configuration generale
- :doc:`../../admin/systeminfo-guide` - Guide des informations systeme
