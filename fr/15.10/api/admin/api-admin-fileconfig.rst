==========================
FileConfig API
==========================

Vue d'ensemble
==============

L'API FileConfig permet de gérer les configurations de crawl de fichiers de |Fess|.
Vous pouvez manipuler les configurations de crawl pour les systèmes de fichiers locaux, les dossiers partagés SMB/CIFS, FTP et divers stockages objets.

URL de base
===========

::

    /api/admin/fileconfig

.. note::

   Tous les endpoints nécessitent des droits d'administration et un jeton d'accès valide.
   Consultez :doc:`api-admin-overview` pour les modalités d'authentification.

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Méthode
     - Chemin
     - Description
   * - GET
     - /settings
     - Obtention de la liste des configurations de crawl de fichiers
   * - GET
     - /setting/{id}
     - Obtention d'une configuration de crawl de fichiers
   * - POST
     - /setting
     - Création d'une configuration de crawl de fichiers
   * - PUT
     - /setting
     - Mise à jour d'une configuration de crawl de fichiers
   * - DELETE
     - /setting/{id}
     - Suppression d'une configuration de crawl de fichiers

Obtention de la liste des configurations de crawl de fichiers
=============================================================

Requête
-------

::

    GET /api/admin/fileconfig/settings

.. note::

   L'endpoint de liste est accessible à la fois via ``GET`` et via ``PUT``.

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 10 55

   * - Paramètre
     - Type
     - Requis
     - Description
   * - ``page``
     - Integer
     - Non
     - Numéro de page (commence à 1, par défaut : 1)
   * - ``size``
     - Integer
     - Non
     - Nombre d'éléments par page (par défaut : 25, selon le paramètre ``paging.page.size``)
   * - ``name``
     - String
     - Non
     - Filtrage par nom de configuration
   * - ``paths``
     - String
     - Non
     - Filtrage par chemin de crawl
   * - ``description``
     - String
     - Non
     - Filtrage par description

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "fileconfig_id_1",
            "name": "Shared Documents",
            "description": "Documents partagés",
            "paths": "smb://server/share/documents",
            "included_paths": ".*\\.pdf$",
            "excluded_paths": ".*/(temp|cache)/.*",
            "included_doc_paths": "",
            "excluded_doc_paths": "",
            "config_parameter": "",
            "depth": 10,
            "max_access_count": 1000,
            "num_of_thread": 1,
            "interval_time": 1000,
            "boost": 1.0,
            "available": "true",
            "permissions": "{role}admin",
            "virtual_hosts": "",
            "sort_order": 0
          }
        ],
        "total": 5
      }
    }

``total`` représente le nombre total de configurations correspondant aux critères de recherche.

Obtention d'une configuration de crawl de fichiers
==================================================

Requête
-------

::

    GET /api/admin/fileconfig/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "fileconfig_id_1",
          "name": "Shared Documents",
          "description": "Documents partagés",
          "paths": "smb://server/share/documents",
          "included_paths": ".*\\.pdf$",
          "excluded_paths": ".*/(temp|cache)/.*",
          "included_doc_paths": "",
          "excluded_doc_paths": "",
          "config_parameter": "",
          "depth": 10,
          "max_access_count": 1000,
          "num_of_thread": 1,
          "interval_time": 1000,
          "boost": 1.0,
          "available": "true",
          "sort_order": 0,
          "permissions": "{role}admin",
          "virtual_hosts": "",
          "created_by": "admin",
          "created_time": 1700000000000,
          "updated_by": "admin",
          "updated_time": 1700000000000,
          "version_no": 1
        }
      }
    }

.. note::

   La réponse inclut les champs d'audit ``created_by``, ``created_time``,
   ``updated_by``, ``updated_time`` et ``version_no``, qui sont définis automatiquement
   lors de la création ou de la mise à jour.
   ``version_no`` est requis lors de la mise à jour (voir la section « Mise à jour d'une configuration de crawl de fichiers » ci-dessous).

Création d'une configuration de crawl de fichiers
=================================================

Requête
-------

::

    POST /api/admin/fileconfig/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Local Files",
      "paths": "file:///data/documents",
      "included_paths": ".*\\.(pdf|doc|docx|xls|xlsx)$",
      "excluded_paths": ".*/(temp|backup)/.*",
      "num_of_thread": 2,
      "interval_time": 500,
      "boost": 1.0,
      "available": "true",
      "sort_order": 0,
      "permissions": "{role}admin\n{role}user"
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Champ
     - Requis
     - Description
   * - ``name``
     - Oui
     - Nom de la configuration (200 caractères maximum)
   * - ``description``
     - Non
     - Description de la configuration (1 000 caractères maximum)
   * - ``paths``
     - Oui
     - Chemins de départ du crawl (séparés par des sauts de ligne si multiples). Indiquez l'un des protocoles suivants : ``file:``, ``smb:``, ``smb1:``, ``ftp:``, ``s3:``, ``gcs:``
   * - ``included_paths``
     - Non
     - Expression régulière des chemins à crawler
   * - ``excluded_paths``
     - Non
     - Expression régulière des chemins à exclure du crawl
   * - ``included_doc_paths``
     - Non
     - Expression régulière des chemins à indexer
   * - ``excluded_doc_paths``
     - Non
     - Expression régulière des chemins à exclure de l'indexation
   * - ``config_parameter``
     - Non
     - Paramètres de configuration supplémentaires (format ``key=value``, un par ligne)
   * - ``depth``
     - Non
     - Profondeur du crawl (0 ou plus)
   * - ``max_access_count``
     - Non
     - Nombre maximum d'accès (0 ou plus)
   * - ``num_of_thread``
     - Oui
     - Nombre de threads parallèles (1 ou plus)
   * - ``interval_time``
     - Oui
     - Intervalle entre les accès (en millisecondes, 0 ou plus)
   * - ``boost``
     - Oui
     - Valeur de boost des résultats de recherche
   * - ``available``
     - Oui
     - Activé/Désactivé (chaîne ``"true"`` / ``"false"``)
   * - ``sort_order``
     - Oui
     - Ordre d'affichage (0 ou plus)
   * - ``permissions``
     - Non
     - Rôles autorisés (séparés par des sauts de ligne si plusieurs)
   * - ``virtual_hosts``
     - Non
     - Hôtes virtuels (séparés par des sauts de ligne si plusieurs)

.. note::

   Les champs d'audit tels que ``created_by``, ``created_time``, ``updated_by`` et ``updated_time``
   sont définis automatiquement côté serveur et n'ont pas besoin d'être fournis dans le corps de la requête.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_fileconfig_id",
        "created": true
      }
    }

Mise à jour d'une configuration de crawl de fichiers
====================================================

Requête
-------

::

    PUT /api/admin/fileconfig/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

Lors d'une mise à jour, les champs de création sont complétés par ``id``, qui identifie la configuration à mettre à jour, et ``version_no``, le numéro de version actuel.
Indiquez pour ``version_no`` la valeur renvoyée par l'API de récupération (GET).

.. code-block:: json

    {
      "id": "existing_fileconfig_id",
      "name": "Updated Local Files",
      "paths": "file:///data/documents",
      "included_paths": ".*\\.(pdf|doc|docx|xls|xlsx|ppt|pptx)$",
      "excluded_paths": ".*/(temp|backup|archive)/.*",
      "depth": 10,
      "max_access_count": 10000,
      "num_of_thread": 3,
      "interval_time": 300,
      "boost": 1.2,
      "available": "true",
      "sort_order": 0,
      "version_no": 1
    }

Champs supplémentaires pour la mise à jour
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Champ
     - Requis
     - Description
   * - ``id``
     - Oui
     - Identifiant de la configuration à mettre à jour (1 000 caractères maximum)
   * - ``version_no``
     - Oui
     - Numéro de version actuel de la configuration à mettre à jour. Indiquez la valeur ``version_no`` contenue dans la réponse de l'API de récupération (GET)

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_fileconfig_id",
        "created": false
      }
    }

Suppression d'une configuration de crawl de fichiers
====================================================

Requête
-------

::

    DELETE /api/admin/fileconfig/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Format des chemins
==================

Le champ ``paths`` accepte les protocoles suivants (la liste des protocoles pris en charge peut être modifiée via le paramètre ``crawler.file.protocols``).

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Protocole
     - Format du chemin
   * - Fichiers locaux
     - ``file:///path/to/directory``
   * - Partage SMB/CIFS
     - ``smb://server/share/path``
   * - Partage SMB/CIFS (SMB1)
     - ``smb1://server/share/path``
   * - FTP
     - ``ftp://server/path``
   * - Amazon S3 / Stockage objet compatible S3 (MinIO, etc.)
     - ``s3://bucket/path``
   * - Google Cloud Storage
     - ``gcs://bucket/path``

.. note::

   Les informations d'authentification (nom d'utilisateur et mot de passe) pour SMB/CIFS ou FTP
   ne doivent pas être intégrées dans le chemin. Configurez-les via la fonctionnalité
   « Authentification de fichier ». Pour plus de détails, consultez :doc:`../../admin/fileauth-guide`.

Exemples d'utilisation
======================

Configuration de crawl pour des fichiers locaux
------------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/fileconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Local Files",
           "paths": "file:///data/documents",
           "included_paths": ".*\\.(pdf|doc|docx)$",
           "excluded_paths": ".*/(temp|backup)/.*",
           "num_of_thread": 2,
           "interval_time": 500,
           "boost": 1.0,
           "available": "true",
           "sort_order": 0,
           "permissions": "{role}guest"
         }'

Configuration de crawl pour un partage SMB
------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/fileconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "SMB Share",
           "paths": "smb://server/documents",
           "included_paths": ".*\\.(pdf|doc|docx)$",
           "excluded_paths": ".*/(temp|private)/.*",
           "max_access_count": 50000,
           "num_of_thread": 3,
           "interval_time": 200,
           "boost": 1.0,
           "available": "true",
           "sort_order": 0,
           "permissions": "{role}guest"
         }'

.. note::

   Si l'accès au partage SMB nécessite une authentification, enregistrez préalablement
   les informations d'identification de l'hôte cible via la configuration « Authentification de fichier ».

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-webconfig` - API de configuration de crawl Web
- :doc:`api-admin-dataconfig` - API de configuration datastore
- :doc:`../../admin/fileconfig-guide` - Guide de configuration du crawl de fichiers
- :doc:`../../admin/fileauth-guide` - Guide de configuration de l'authentification de fichier
