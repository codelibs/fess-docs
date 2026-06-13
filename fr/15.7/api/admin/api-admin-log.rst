==========================
API Log
==========================

Vue d'ensemble
==============

L'API Log permet de consulter et de telecharger les fichiers journaux de |Fess|.
Vous pouvez obtenir la liste des fichiers journaux generes sur le serveur et telecharger individuellement chaque fichier journal.

URL de base
===========

::

    /api/admin/log

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
     - Obtention de la liste des fichiers journaux
   * - GET
     - /file/{id}
     - Telechargement d'un fichier journal

Obtention de la liste des fichiers journaux
===========================================

Renvoie la liste des fichiers journaux (``.log`` et ``.log.gz``) presents dans le repertoire de sortie des journaux du serveur.

Requete
-------

::

    GET /api/admin/log/files

Reponse
-------

``files`` contient un tableau d'objets representant les informations de chaque fichier journal, et ``total`` contient le nombre d'elements.
Chaque objet possede les champs suivants.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``id``
     - Valeur du nom de fichier encode en Base64 URL (utilisee comme ``{id}`` lors du telechargement)
   * - ``name``
     - Nom du fichier journal
   * - ``lastModified``
     - Date et heure de derniere modification

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "files": [
          {
            "id": "ZmVzcy5sb2c=",
            "name": "fess.log",
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          },
          {
            "id": "ZmVzcy1jcmF3bGVyLmxvZw==",
            "name": "fess-crawler.log",
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          }
        ],
        "total": 2
      }
    }

Telechargement d'un fichier journal
===================================

Telecharge le contenu du fichier journal specifie.
Pour ``{id}``, indiquez l'``id`` obtenu lors de l'obtention de la liste (la valeur du nom de fichier encode en Base64).
La reponse est renvoyee sous forme de flux ``application/octet-stream``.
Si vous specifiez un nom de fichier inexistant ou un nom non autorise en tant que fichier journal, une reponse vide est renvoyee.

Requete
-------

::

    GET /api/admin/log/file/{id}

Reponse
-------

Flux binaire du fichier journal (``Content-Type: application/octet-stream``).

Exemples d'utilisation
======================

Obtention de la liste des fichiers journaux
-------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/files" \
         -H "Authorization: Bearer YOUR_TOKEN"

Telechargement d'un fichier journal
-----------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/file/ZmVzcy5sb2c=" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess.log

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-backup` - API de sauvegarde
