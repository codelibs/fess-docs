===========
Storage API
===========

Vue d'ensemble
==============

L'API Storage est une API permettant de gerer le stockage d'objets de |Fess|.
Elle permet de lister les fichiers et repertoires dans le stockage, ainsi que de telecharger, supprimer et envoyer des fichiers.

URL de base
===========

::

    /api/admin/storage

Authentification
================

Tous les endpoints de l'API Admin, y compris l'API Storage, necessitent une authentification par jeton d'acces.
Indiquez le jeton d'acces dans l'en-tete ``Authorization`` de la requete.

::

    Authorization: Bearer <jeton d'acces>

Pour plus d'informations sur l'obtention d'un jeton d'acces et sur les permissions requises (par defaut, le role ``admin-api``), consultez :doc:`api-admin-overview`.

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
     - /upload
     - Envoi d'un fichier

Obtention de la liste des fichiers et repertoires
=================================================

Retourne la liste des fichiers et repertoires situes sous le repertoire specifie.
Indiquez dans ``{id}`` l'``id`` du repertoire obtenu lors d'un appel de listage. Si ``{id}`` est omis, la liste du repertoire racine est retournee.

Requete
-------

::

    GET /api/admin/storage/list/{id}

Reponse
-------

Le champ ``items`` contient un tableau d'objets representant les fichiers et repertoires (les repertoires apparaissent avant les fichiers).
Chaque objet possede les champs suivants.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``id``
     - Identifiant encode. Chaine de caracteres representant le chemin de l'objet encode en Base64 URL-safe, utilisee comme ``{id}`` lors du telechargement ou de la suppression.
   * - ``path``
     - Chemin du repertoire parent
   * - ``name``
     - Nom du fichier ou du repertoire
   * - ``hashCode``
     - Valeur de hachage utilisee en interne (il ne s'agit pas d'une valeur stable representant le contenu de l'objet)
   * - ``size``
     - Taille (en octets)
   * - ``directory``
     - Indique s'il s'agit d'un repertoire (boolean)
   * - ``lastModified``
     - Date et heure de la derniere modification (format ISO 8601 ; presente uniquement pour les fichiers)

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
============================

Telecharge un fichier depuis le stockage. Indiquez dans ``{id}`` l'``id`` obtenu lors du listage.
La reponse est retournee sous forme de flux ``application/octet-stream``.

Requete
-------

::

    GET /api/admin/storage/download/{id}

Reponse
-------

Flux binaire du fichier (``Content-Type: application/octet-stream``).

.. note::

   La reponse de cette API ne contient pas d'en-tete ``Content-Disposition``.
   Le nom du fichier a enregistrer doit etre specifie cote client (avec l'option ``-o`` pour cURL).

Suppression d'un fichier
=========================

Supprime un fichier du stockage. Indiquez dans ``{id}`` l'``id`` obtenu lors du listage.

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

Envoie un fichier vers le stockage au format ``multipart/form-data``.
Le repertoire de destination est specifie via le champ de formulaire ``path``, et non dans le chemin de l'URL.

Requete
-------

::

    PUT /api/admin/storage/upload
    Content-Type: multipart/form-data

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Champ
     - Obligatoire
     - Description
   * - ``path``
     - Non
     - Chemin du repertoire de destination (sans slash initial ni final). Si non specifie, le fichier est enregistre a la racine (directement sous le bucket).
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

Erreurs
=======

En cas d'echec du traitement, chaque endpoint retourne une reponse avec un ``status`` different de 0 (``1`` en cas d'erreur de validation).
Le champ ``message`` du corps de la reponse contient le detail de l'erreur. Pour plus de details sur les valeurs de status et les codes de statut HTTP, consultez :doc:`api-admin-overview`.

Les principaux cas d'erreur sont les suivants.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Principaux cas d'erreur
   * - Obtention de la liste des fichiers et repertoires
     - Lorsque le nombre d'elements recuperes depasse la limite maximale
   * - Telechargement d'un fichier
     - Lorsque l'``id`` est invalide ou que le telechargement echoue
   * - Suppression d'un fichier
     - Lorsque l'``id`` est invalide ou que la suppression echoue
   * - Envoi d'un fichier
     - Lorsque ``file`` n'est pas specifie ou que l'envoi echoue

Exemples d'utilisation
======================

Obtention de la liste du repertoire racine
------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/list/" \
         -H "Authorization: Bearer YOUR_TOKEN"

Telechargement d'un fichier
----------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/download/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o sample.txt

Suppression d'un fichier
-------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/storage/delete/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN"

Envoi d'un fichier
-------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/storage/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "path=subdir" \
         -F "file=@sample.txt"

Informations complementaires
=============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
