==========================
API Storage
==========================

Vue d'ensemble
==============

L'API Storage permet de gerer le stockage d'objets de |Fess|.
Vous pouvez obtenir la liste des fichiers et repertoires du stockage, et effectuer le telechargement, la suppression et l'envoi de fichiers.

URL de base
===========

::

    /api/admin/storage

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Chemin
     - Description
   * - GET
     - /list/{id}
     - Obtention de la liste des fichiers et repertoires
   * - GET
     - /download/{id}
     - Telechargement d'un fichier
   * - DELETE
     - /delete/{id}
     - Suppression d'un fichier
   * - PUT
     - /upload/{pathId}
     - Envoi d'un fichier

Obtention de la liste des fichiers et repertoires
=================================================

Renvoie la liste des fichiers et repertoires situes sous le repertoire specifie.
Pour ``{id}``, indiquez un chemin encode. Si ``{id}`` est omis, la liste du repertoire racine est obtenue.

Requete
-------

::

    GET /api/admin/storage/list/{id}

Reponse
-------

``items`` contient un tableau d'objets representant les informations des fichiers et repertoires (les repertoires en premier, puis les fichiers).
Chaque objet possede les champs suivants.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``id``
     - Identifiant encode (utilise comme ``{id}`` lors du telechargement et de la suppression)
   * - ``path``
     - Chemin parent
   * - ``name``
     - Nom de fichier ou de repertoire
   * - ``hashCode``
     - Code de hachage
   * - ``size``
     - Taille (octets)
   * - ``directory``
     - Indique s'il s'agit d'un repertoire (boolean)
   * - ``lastModified``
     - Date et heure de derniere modification (fichiers uniquement)

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "items": [
          {
            "id": "c3ViZGly",
            "path": "/",
            "name": "subdir",
            "hashCode": 12345,
            "size": 0,
            "directory": true
          },
          {
            "id": "c2FtcGxlLnR4dA==",
            "path": "/",
            "name": "sample.txt",
            "hashCode": 67890,
            "size": 1024,
            "directory": false,
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          }
        ]
      }
    }

Telechargement d'un fichier
===========================

Telecharge un fichier du stockage. Pour ``{id}``, indiquez l'``id`` obtenu lors de l'obtention de la liste.
La reponse est renvoyee sous forme de flux ``application/octet-stream``.

Requete
-------

::

    GET /api/admin/storage/download/{id}

Reponse
-------

Flux binaire du fichier (``Content-Type: application/octet-stream``).

Suppression d'un fichier
========================

Supprime un fichier du stockage. Pour ``{id}``, indiquez l'``id`` obtenu lors de l'obtention de la liste.

Requete
-------

::

    DELETE /api/admin/storage/delete/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Envoi d'un fichier
==================

Envoie un fichier vers le stockage. L'envoi se fait au format ``multipart/form-data``.

Requete
-------

::

    PUT /api/admin/storage/upload/{pathId}
    Content-Type: multipart/form-data

Description des champs
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Champ
     - Requis
     - Description
   * - ``path``
     - Non
     - Chemin de destination de l'envoi (emplacement par defaut si non specifie)
   * - ``file``
     - Oui
     - Fichier a envoyer

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

Obtention de la liste du repertoire racine
------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/list/" \
         -H "Authorization: Bearer YOUR_TOKEN"

Telechargement d'un fichier
---------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/download/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o sample.txt

Suppression d'un fichier
------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/storage/delete/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN"

Envoi d'un fichier
------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/storage/upload/" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "path=/" \
         -F "file=@sample.txt"

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
