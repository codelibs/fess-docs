==========================
API Plugin
==========================

Vue d'ensemble
==============

L'API Plugin permet de gerer les plugins de |Fess|.
Vous pouvez installer, activer, desactiver et supprimer des plugins.

URL de base
===========

::

    /api/admin/plugin

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
     - Obtention de la liste des plugins
   * - POST
     - /install
     - Installation d'un plugin
   * - DELETE
     - /{id}
     - Suppression d'un plugin

Obtention de la liste des plugins
=================================

Requete
-------

::

    GET /api/admin/plugin

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "plugins": [
          {
            "id": "analysis-kuromoji",
            "name": "Japanese (kuromoji) Analysis Plugin",
            "version": "2.11.0",
            "description": "Japanese language analysis plugin",
            "enabled": true,
            "installed": true
          },
          {
            "id": "analysis-icu",
            "name": "ICU Analysis Plugin",
            "version": "2.11.0",
            "description": "Unicode normalization and collation",
            "enabled": true,
            "installed": true
          }
        ],
        "total": 2
      }
    }

Champs de la reponse
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``id``
     - ID du plugin
   * - ``name``
     - Nom du plugin
   * - ``version``
     - Version du plugin
   * - ``description``
     - Description du plugin
   * - ``enabled``
     - Etat d'activation
   * - ``installed``
     - Etat d'installation

Installation d'un plugin
========================

Requete
-------

::

    POST /api/admin/plugin/install
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "url": "https://example.com/plugins/my-plugin-1.0.0.zip"
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``url``
     - Oui
     - URL de telechargement du plugin

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Plugin installed successfully. Restart required.",
        "pluginId": "my-plugin"
      }
    }

Suppression d'un plugin
=======================

Requete
-------

::

    DELETE /api/admin/plugin/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Plugin deleted successfully. Restart required."
      }
    }

Exemples d'utilisation
======================

Obtention de la liste des plugins
---------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN"

Installation d'un plugin
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/plugin/install" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "url": "https://artifacts.opensearch.org/releases/plugins/analysis-icu/2.11.0/analysis-icu-2.11.0.zip"
         }'

Suppression d'un plugin
-----------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/plugin/analysis-icu" \
         -H "Authorization: Bearer YOUR_TOKEN"

Notes importantes
=================

- Un redemarrage de Fess est necessaire apres l'installation ou la suppression d'un plugin
- L'installation d'un plugin incompatible peut empecher le demarrage de Fess
- Soyez prudent lors de la suppression de plugins. Les dependances peuvent affecter le systeme

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-systeminfo` - API des informations systeme
- :doc:`../../admin/plugin-guide` - Guide de gestion des plugins
