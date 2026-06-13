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

Reponse
-------

La reponse contient ``version`` indiquant la version du produit, ``status`` indiquant le resultat du traitement, ainsi que les quatre groupes de proprietes suivants. Chaque groupe de proprietes est un tableau d'objets possedant ``key`` et ``value``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "envProps": [
          {"key": "JAVA_HOME", "value": "/usr/lib/jvm/java-21"},
          {"key": "FESS_DICTIONARY_PATH", "value": "/var/lib/fess/dict"}
        ],
        "systemProps": [
          {"key": "java.version", "value": "21.0.1"},
          {"key": "java.vendor", "value": "Oracle Corporation"},
          {"key": "os.name", "value": "Linux"},
          {"key": "user.dir", "value": "/opt/fess"}
        ],
        "fessProps": [
          {"key": "crawler.document.max.site.length", "value": "50"},
          {"key": "indexer.thread.dump.enabled", "value": "true"}
        ],
        "bugReportProps": [
          {"key": "os.name", "value": "Linux"},
          {"key": "java.vm.version", "value": "21.0.1+12"}
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
   * - ``envProps``
     - Liste des variables d'environnement (tableau de ``key`` / ``value``)
   * - ``systemProps``
     - Liste des proprietes systeme Java (tableau de ``key`` / ``value``)
   * - ``fessProps``
     - Liste des proprietes de configuration de |Fess| (tableau de ``key`` / ``value``)
   * - ``bugReportProps``
     - Liste des informations collectees pour les rapports de bogues (tableau de ``key`` / ``value``)

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
         | jq -r '.response.systemProps[] | select(.key == "java.version") | .value'

Affichage de la liste des variables d'environnement
---------------------------------------------------

.. code-block:: bash

    # Afficher les variables d'environnement au format key=value
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.envProps[] | "\(.key)=\(.value)"'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-stats` - API de statistiques
- :doc:`api-admin-general` - API de configuration generale
- :doc:`../../admin/systeminfo-guide` - Guide des informations systeme
