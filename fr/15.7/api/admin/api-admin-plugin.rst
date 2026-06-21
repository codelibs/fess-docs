==========================
API Plugin
==========================

Vue d'ensemble
==============

L'API Plugin permet de gérer les plugins (artefacts) de |Fess|.
Vous pouvez obtenir la liste des plugins installés et des plugins installables, et effectuer l'installation et la suppression de plugins.

URL de base
===========

::

    /api/admin/plugin

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Méthode
     - Chemin
     - Description
   * - GET
     - /installed
     - Obtention de la liste des plugins installés
   * - GET
     - /available
     - Obtention de la liste des plugins installables
   * - POST
     - /
     - Installation d'un plugin
   * - DELETE
     - /
     - Suppression d'un plugin

Champs des informations de plugin
==================================

Chaque élément du tableau ``plugins`` renvoyé par les endpoints de liste
(``/installed`` et ``/available``) est un objet possédant les champs suivants.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Champ
     - Description
   * - ``type``
     - Identifiant de catégorie de l'artefact. L'une des valeurs suivantes :
       ``fess-ds`` (data store), ``fess-theme`` (thème),
       ``fess-ingest`` (Ingest), ``fess-script`` (script), ``fess-webapp`` (application web),
       ``fess-thumbnail`` (miniature), ``fess-crawler`` (crawler), ``fess-llm`` (LLM),
       ``jar`` (JAR générique pour tout autre cas).
   * - ``id``
     - Identifiant au format ``{name}:{version}``.
   * - ``name``
     - Nom du plugin.
   * - ``version``
     - Version du plugin.
   * - ``url``
     - URL de téléchargement. Présent uniquement dans la réponse de ``/available``.
       Ce champ est omis dans la réponse de ``/installed`` car la valeur est absente.

.. note::

   Dans les réponses de l'API |Fess|, les champs dont la valeur est ``null`` ne sont pas inclus dans la sortie.
   Par conséquent, le champ ``url`` n'est pas présent dans chaque élément des plugins installés.

Obtention de la liste des plugins installés
===========================================

Renvoie la liste des plugins installés. Les artefacts présents dans le répertoire des plugins
sont parcourus par catégorie et renvoyés triés par ordre alphabétique.

Requête
-------

::

    GET /api/admin/plugin/installed

Réponse
-------

``plugins`` contient un tableau d'objets représentant les informations des plugins.
Pour les champs de chaque objet, reportez-vous à `Champs des informations de plugin`_.
Le champ ``url`` n'est pas inclus dans la réponse pour les plugins installés.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "type": "fess-ds",
            "id": "fess-ds-slack:15.7.0",
            "name": "fess-ds-slack",
            "version": "15.7.0"
          }
        ]
      }
    }

Obtention de la liste des plugins installables
==============================================

Renvoie la liste des plugins installables. Les artefacts de toutes les catégories sont récupérés
depuis les dépôts configurés dans ``plugin.repositories`` de ``fess_config.properties``.
Les résultats sont mis en cache pendant une durée déterminée (5 minutes par défaut).

Requête
-------

::

    GET /api/admin/plugin/available

Réponse
-------

``plugins`` contient un tableau d'objets représentant les informations des plugins installables.
Pour les champs de chaque objet, reportez-vous à `Champs des informations de plugin`_.
Pour les plugins installables, le champ ``url`` de téléchargement est inclus.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "type": "fess-ds",
            "id": "fess-ds-slack:15.7.0",
            "name": "fess-ds-slack",
            "version": "15.7.0",
            "url": "https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-slack/15.7.0/fess-ds-slack-15.7.0.jar"
          }
        ]
      }
    }

Installation d'un plugin
========================

Installe le plugin du nom et de la version spécifiés.

Requête
-------

::

    POST /api/admin/plugin
    Content-Type: application/json

Corps de la requête
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
     - Nom du plugin (100 caractères maximum)
   * - ``version``
     - Oui
     - Version du plugin (100 caractères maximum)

.. note::

   ``name`` et ``version`` doivent correspondre à l'un des plugins installables
   récupérables via ``/available``. Si aucun artefact correspondant n'existe,
   une erreur est renvoyée.

Réponse
-------

Lorsque la requête est acceptée, une réponse avec ``status`` à ``0`` (OK) est renvoyée.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Si aucun artefact correspondant à ``name`` ou ``version`` n'existe, ``status`` vaut
``1`` (BAD_REQUEST) et ``message`` contient ``invalid name or version``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 1,
        "message": "invalid name or version"
      }
    }

.. note::

   L'installation s'exécute de manière asynchrone en arrière-plan. Une réponse ``status: 0``
   indique que la requête a été acceptée, mais ne garantit pas que l'installation est terminée.
   Une fois l'installation terminée, si des plugins portant le même nom mais une version
   différente sont déjà installés, ils sont automatiquement supprimés. En cas d'échec du
   téléchargement ou de l'installation, l'erreur est consignée dans les journaux du serveur
   mais n'est pas reflétée dans la réponse de l'API.

Suppression d'un plugin
=======================

Supprime le plugin du nom et de la version spécifiés.

Requête
-------

::

    DELETE /api/admin/plugin
    Content-Type: application/json

Corps de la requête
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
     - Nom du plugin (100 caractères maximum)
   * - ``version``
     - Non
     - Version du plugin (100 caractères maximum). Il est recommandé de la spécifier pour identifier
       de manière unique le plugin à supprimer.

Réponse
-------

Lorsque la requête est acceptée, une réponse avec ``status`` à ``0`` (OK) est renvoyée.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

.. note::

   La suppression s'exécute de manière asynchrone en arrière-plan. Une réponse ``status: 0``
   indique que la requête a été acceptée ; elle ne vérifie pas si le plugin concerné existe
   ni si la suppression a réussi. En cas d'échec de la suppression (par exemple si le fichier
   cible n'existe pas), l'erreur est consignée dans les journaux du serveur mais n'est pas
   reflétée dans la réponse de l'API.

Exemples d'utilisation
======================

Obtention de la liste des plugins installés
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

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
