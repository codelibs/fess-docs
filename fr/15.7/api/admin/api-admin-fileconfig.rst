==========================
API FileConfig
==========================

Vue d'ensemble
==============

L'API FileConfig permet de gerer les configurations de crawl de fichiers de |Fess|.
Vous pouvez manipuler les configurations de crawl pour les systemes de fichiers et les dossiers partages SMB/CIFS.

URL de base
===========

::

    /api/admin/fileconfig

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
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
     - Creation d'une configuration de crawl de fichiers
   * - PUT
     - /setting
     - Mise a jour d'une configuration de crawl de fichiers
   * - DELETE
     - /setting/{id}
     - Suppression d'une configuration de crawl de fichiers

Obtention de la liste des configurations de crawl de fichiers
=============================================================

Requete
-------

::

    GET /api/admin/fileconfig/settings

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15.70

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``size``
     - Integer
     - Non
     - Nombre d'elements par page (par defaut : 20)
   * - ``page``
     - Integer
     - Non
     - Numero de page (commence a 0)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "fileconfig_id_1",
            "name": "Shared Documents",
            "description": "共有ドキュメント",
            "paths": "file://///server/share/documents",
            "includedPaths": ".*\\.pdf$",
            "excludedPaths": ".*/(temp|cache)/.*",
            "includedDocPaths": "",
            "excludedDocPaths": "",
            "configParameter": "",
            "depth": 10,
            "maxAccessCount": 1000,
            "numOfThread": 1,
            "intervalTime": 1000,
            "boost": 1.0,
            "available": "true",
            "permissions": "{role}admin",
            "virtualHosts": "",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

Obtention d'une configuration de crawl de fichiers
==================================================

Requete
-------

::

    GET /api/admin/fileconfig/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "fileconfig_id_1",
          "name": "Shared Documents",
          "description": "共有ドキュメント",
          "paths": "file://///server/share/documents",
          "includedPaths": ".*\\.pdf$",
          "excludedPaths": ".*/(temp|cache)/.*",
          "includedDocPaths": "",
          "excludedDocPaths": "",
          "configParameter": "",
          "depth": 10,
          "maxAccessCount": 1000,
          "numOfThread": 1,
          "intervalTime": 1000,
          "boost": 1.0,
          "available": "true",
          "sortOrder": 0,
          "permissions": "{role}admin",
          "virtualHosts": "",
          "labelTypeIds": []
        }
      }
    }

Creation d'une configuration de crawl de fichiers
=================================================

Requete
-------

::

    POST /api/admin/fileconfig/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Local Files",
      "paths": "file:///data/documents",
      "includedPaths": ".*\\.(pdf|doc|docx|xls|xlsx)$",
      "excludedPaths": ".*/(temp|backup)/.*",
      "numOfThread": 2,
      "intervalTime": 500,
      "boost": 1.0,
      "available": "true",
      "sortOrder": 0,
      "permissions": "{role}admin\n{role}user",
      "labelTypeIds": ["label_id_1"]
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - Champ
     - Requis
     - Description
   * - ``name``
     - Oui
     - Nom de la configuration
   * - ``description``
     - Non
     - Description de la configuration
   * - ``paths``
     - Oui
     - Chemins de depart du crawl (separes par des sauts de ligne si multiples)
   * - ``includedPaths``
     - Non
     - Pattern regex des chemins a crawler
   * - ``excludedPaths``
     - Non
     - Pattern regex des chemins a exclure
   * - ``includedDocPaths``
     - Non
     - Pattern regex des chemins a indexer
   * - ``excludedDocPaths``
     - Non
     - Pattern regex des chemins a exclure de l'indexation
   * - ``configParameter``
     - Non
     - Parametres de configuration supplementaires
   * - ``depth``
     - Non
     - Profondeur du crawl
   * - ``maxAccessCount``
     - Non
     - Nombre maximum d'acces
   * - ``numOfThread``
     - Oui
     - Nombre de threads paralleles
   * - ``intervalTime``
     - Oui
     - Intervalle entre les acces (millisecondes)
   * - ``boost``
     - Oui
     - Valeur de boost des resultats de recherche
   * - ``available``
     - Oui
     - Active/Desactive (chaine ``"true"`` / ``"false"``)
   * - ``sortOrder``
     - Oui
     - Ordre d'affichage
   * - ``permissions``
     - Non
     - Roles autorises (separes par des sauts de ligne si plusieurs)
   * - ``virtualHosts``
     - Non
     - Hotes virtuels (separes par des sauts de ligne si plusieurs)
   * - ``labelTypeIds``
     - Non
     - IDs des types de labels (tableau)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_fileconfig_id",
        "created": true
      }
    }

Mise a jour d'une configuration de crawl de fichiers
====================================================

Requete
-------

::

    PUT /api/admin/fileconfig/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_fileconfig_id",
      "name": "Updated Local Files",
      "paths": "file:///data/documents",
      "includedPaths": ".*\\.(pdf|doc|docx|xls|xlsx|ppt|pptx)$",
      "excludedPaths": ".*/(temp|backup|archive)/.*",
      "depth": 10,
      "maxAccessCount": 10000,
      "numOfThread": 3,
      "intervalTime": 300,
      "boost": 1.2,
      "available": "true",
      "sortOrder": 0,
      "versionNo": 1
    }

Reponse
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

Requete
-------

::

    DELETE /api/admin/fileconfig/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Format des chemins
==================

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Protocole
     - Format du chemin
   * - Fichiers locaux
     - ``file:///path/to/directory``
   * - Partage Windows (SMB)
     - ``file://///server/share/path``
   * - SMB avec authentification
     - ``smb://username:password@server/share/path``
   * - NFS
     - ``file://///nfs-server/export/path``

Exemples d'utilisation
======================

Configuration de crawl pour un partage SMB
------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/fileconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "SMB Share",
           "paths": "smb://user:pass@server/documents",
           "includedPaths": ".*\\.(pdf|doc|docx)$",
           "excludedPaths": ".*/(temp|private)/.*",
           "maxAccessCount": 50000,
           "numOfThread": 3,
           "intervalTime": 200,
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-webconfig` - API de configuration de crawl Web
- :doc:`api-admin-dataconfig` - API de configuration datastore
- :doc:`../../admin/fileconfig-guide` - Guide de configuration du crawl de fichiers
