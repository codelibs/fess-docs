==========================
API Backup
==========================

Vue d'ensemble
==============

L'API Backup permet de consulter et de telecharger les donnees cibles de sauvegarde de |Fess|.
Vous pouvez obtenir la liste des cibles de sauvegarde et telecharger individuellement chaque fichier de sauvegarde (proprietes systeme, donnees en masse de chaque index, donnees NDJSON des journaux).

URL de base
===========

::

    /api/admin/backup

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Chemin
     - Description
   * - GET
     - /files
     - Obtention de la liste des cibles de sauvegarde
   * - GET
     - /file/{id}
     - Telechargement d'un fichier de sauvegarde

Obtention de la liste des cibles de sauvegarde
==============================================

Renvoie la liste des cibles de sauvegarde. Les cibles reposent sur les parametres ``index.backup.targets`` et ``index.backup.log.targets``.

Requete
-------

::

    GET /api/admin/backup/files

Reponse
-------

``files`` contient un tableau d'objets representant les cibles de sauvegarde, et ``total`` contient le nombre d'elements.
Chaque objet possede ``id`` et ``name``, tous deux renseignes avec le nom de la cible (``fess_config.bulk``, ``system.properties``, ``search_log.ndjson``, etc.).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "files": [
          {
            "id": "fess_config.bulk",
            "name": "fess_config.bulk"
          },
          {
            "id": "system.properties",
            "name": "system.properties"
          },
          {
            "id": "search_log.ndjson",
            "name": "search_log.ndjson"
          }
        ],
        "total": 3
      }
    }

Telechargement d'un fichier de sauvegarde
=========================================

Telecharge le contenu du fichier de sauvegarde specifie. Pour ``{id}``, indiquez l'``id`` (nom de la cible) obtenu lors de l'obtention de la liste.
Selon le type de ``{id}``, le contenu de la reponse change comme suit.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ID
     - Contenu
   * - ``system.properties``
     - Contenu des proprietes systeme
   * - Nom d'index ``*.bulk`` ou sans extension ``.bulk``
     - Donnees en masse generees en parcourant (scroll) l'index cible
   * - ``*.ndjson`` (``search_log`` / ``user_info`` / ``click_log`` / ``favorite_log``)
     - Donnees NDJSON du journal correspondant

Si vous specifiez un ``{id}`` inexistant parmi les cibles de sauvegarde, une erreur est renvoyee.

Requete
-------

::

    GET /api/admin/backup/file/{id}

Reponse
-------

Flux du fichier de sauvegarde. Au format NDJSON, il est renvoye avec ``Content-Type: application/x-ndjson``, sinon avec ``application/octet-stream``.

Exemples d'utilisation
======================

Obtention de la liste des cibles de sauvegarde
----------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/files" \
         -H "Authorization: Bearer YOUR_TOKEN"

Telechargement de l'index de configuration
------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/file/fess_config.bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess_config.bulk

Telechargement des journaux de recherche
----------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/file/search_log.ndjson" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o search_log.ndjson

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-log` - API de journaux
