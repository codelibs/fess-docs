==========================
API SystemInfo
==========================

Vue d'ensemble
==============

L'API SystemInfo permet d'obtenir les informations systeme de |Fess|.
Vous pouvez consulter les informations de version, les variables d'environnement, les informations JVM, etc.

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

.. code-block:: json

    {
      "response": {
        "status": 0,
        "systemInfo": {
          "fessVersion": "15.5.0",
          "opensearchVersion": "2.11.0",
          "javaVersion": "21.0.1",
          "serverName": "Apache Tomcat/10.1.15",
          "osName": "Linux",
          "osVersion": "5.15.0-89-generic",
          "osArchitecture": "amd64",
          "jvmTotalMemory": "2147483648",
          "jvmFreeMemory": "1073741824",
          "jvmMaxMemory": "4294967296",
          "processorCount": "8",
          "fileEncoding": "UTF-8",
          "userLanguage": "ja",
          "userTimezone": "Asia/Tokyo"
        },
        "environmentInfo": {
          "JAVA_HOME": "/usr/lib/jvm/java-21",
          "FESS_DICTIONARY_PATH": "/var/lib/fess/dict",
          "FESS_LOG_PATH": "/var/log/fess"
        },
        "systemProperties": {
          "java.version": "21.0.1",
          "java.vendor": "Oracle Corporation",
          "os.name": "Linux",
          "os.version": "5.15.0-89-generic"
        }
      }
    }

Champs de la reponse
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``fessVersion``
     - Version de Fess
   * - ``opensearchVersion``
     - Version d'OpenSearch
   * - ``javaVersion``
     - Version de Java
   * - ``serverName``
     - Nom du serveur d'applications
   * - ``osName``
     - Nom du systeme d'exploitation
   * - ``osVersion``
     - Version du systeme d'exploitation
   * - ``osArchitecture``
     - Architecture du systeme d'exploitation
   * - ``jvmTotalMemory``
     - Memoire totale JVM (octets)
   * - ``jvmFreeMemory``
     - Memoire libre JVM (octets)
   * - ``jvmMaxMemory``
     - Memoire maximale JVM (octets)
   * - ``processorCount``
     - Nombre de processeurs
   * - ``fileEncoding``
     - Encodage des fichiers
   * - ``userLanguage``
     - Langue utilisateur
   * - ``userTimezone``
     - Fuseau horaire utilisateur

Exemples d'utilisation
======================

Obtention des informations systeme
----------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN"

Verification de la version
--------------------------

.. code-block:: bash

    # Extraire uniquement la version de Fess
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.systemInfo.fessVersion'

Verification de l'utilisation memoire
-------------------------------------

.. code-block:: bash

    # Extraire les informations memoire JVM
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.systemInfo | {total: .jvmTotalMemory, free: .jvmFreeMemory, max: .jvmMaxMemory}'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-stats` - API des statistiques
- :doc:`api-admin-general` - API des parametres generaux
- :doc:`../../admin/systeminfo-guide` - Guide des informations systeme
