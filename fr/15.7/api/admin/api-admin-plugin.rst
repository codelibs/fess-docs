==========================
API Plugin
==========================

Vue d'ensemble
==============

L'API Plugin permet de gerer les plugins (artefacts) de |Fess|.
Vous pouvez obtenir la liste des plugins installes et des plugins installables, et effectuer l'installation et la suppression de plugins.

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
     - /installed
     - Obtention de la liste des plugins installes
   * - GET
     - /available
     - Obtention de la liste des plugins installables
   * - POST
     - /
     - Installation d'un plugin
   * - DELETE
     - /
     - Suppression d'un plugin

Obtention de la liste des plugins installes
===========================================

Renvoie la liste des plugins installes.

Requete
-------

::

    GET /api/admin/plugin/installed

Reponse
-------

``plugins`` contient un tableau d'objets representant les informations des plugins.
Chaque objet est une map de cles et valeurs de type chaine, comprenant notamment ``name`` (nom du plugin) et ``version`` (version).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "name": "fess-ds-slack",
            "version": "15.7.0"
          }
        ]
      }
    }

Obtention de la liste des plugins installables
==============================================

Renvoie la liste des plugins installables.

Requete
-------

::

    GET /api/admin/plugin/available

Reponse
-------

``plugins`` contient un tableau d'objets representant les informations des plugins installables.
Chaque objet est, comme pour ``installed``, une map de cles et valeurs de type chaine.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "name": "fess-ds-slack",
            "version": "15.7.0"
          }
        ]
      }
    }

Installation d'un plugin
========================

Installe le plugin du nom et de la version specifies.

Requete
-------

::

    POST /api/admin/plugin
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "fess-ds-slack",
      "version": "15.7.0"
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Champ
     - Requis
     - Description
   * - ``name``
     - Oui
     - Nom du plugin (100 caracteres maximum)
   * - ``version``
     - Oui
     - Version du plugin (100 caracteres maximum)

Reponse
-------

En cas de succes, seul ``status`` est renvoye.
Si aucun artefact ne correspond a ``name`` ou ``version``, ``status`` vaut ``1`` (BAD_REQUEST) et ``message`` contient ``invalid name or version``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Suppression d'un plugin
=======================

Supprime le plugin du nom et de la version specifies.

Requete
-------

::

    DELETE /api/admin/plugin
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "fess-ds-slack",
      "version": "15.7.0"
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Champ
     - Requis
     - Description
   * - ``name``
     - Oui
     - Nom du plugin (100 caracteres maximum)
   * - ``version``
     - Non
     - Version du plugin (100 caracteres maximum)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Exemples d'utilisation
======================

Obtention de la liste des plugins installes
-------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/plugin/installed" \
         -H "Authorization: Bearer YOUR_TOKEN"

Installation d'un plugin
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.7.0"
         }'

Suppression d'un plugin
-----------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.7.0"
         }'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
