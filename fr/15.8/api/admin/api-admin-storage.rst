===========
Storage API
===========

Vue d'ensemble
==============

L'API Storage est une API permettant de gérer le stockage d'objets de |Fess|.
Elle permet de lister les fichiers et répertoires dans le stockage, ainsi que de télécharger, supprimer et envoyer des fichiers.

URL de base
===========

::

    /api/admin/storage

Authentification
=================

Tous les endpoints de l'API Admin, y compris l'API Storage, nécessitent une authentification par jeton d'accès.
Indiquez le jeton d'accès dans l'en-tête ``Authorization`` de la requête.

::

    Authorization: Bearer <jeton d'accès>

Pour plus d'informations sur l'obtention d'un jeton d'accès et sur les permissions requises (par défaut, le rôle ``admin-api``), consultez :doc:`api-admin-overview`.

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Méthode
     - Chemin
     - Description
   * - GET
     - /list/{id}
     - Obtention de la liste des fichiers et répertoires
   * - GET
     - /download/{id}
     - Téléchargement d'un fichier
   * - DELETE
     - /delete/{id}
     - Suppression d'un fichier
   * - PUT
     - /upload
     - Envoi d'un fichier

Obtention de la liste des fichiers et répertoires
====================================================

Retourne la liste des fichiers et répertoires situés sous le répertoire spécifié.
Indiquez dans ``{id}`` l'``id`` du répertoire obtenu lors d'un appel de listage. Si ``{id}`` est omis, la liste du répertoire racine est retournée.

Requête
-------

::

    GET /api/admin/storage/list/{id}

Réponse
-------

Le champ ``items`` contient un tableau d'objets représentant les fichiers et répertoires (les répertoires apparaissent avant les fichiers).
Chaque objet possède les champs suivants.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``id``
     - Identifiant encodé. Chaîne de caractères représentant le chemin de l'objet encodé en Base64 URL-safe, utilisée comme ``{id}`` lors du téléchargement ou de la suppression.
   * - ``path``
     - Chemin du répertoire parent
   * - ``name``
     - Nom du fichier ou du répertoire
   * - ``hashCode``
     - Valeur de hachage utilisée en interne (il ne s'agit pas d'une valeur stable représentant le contenu de l'objet)
   * - ``size``
     - Taille (en octets)
   * - ``directory``
     - Indique s'il s'agit d'un répertoire (boolean)
   * - ``lastModified``
     - Date et heure de la dernière modification (format ISO 8601 ; présente uniquement pour les fichiers)

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
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

Téléchargement d'un fichier
==============================

Télécharge un fichier depuis le stockage. Indiquez dans ``{id}`` l'``id`` obtenu lors du listage.
La réponse est retournée sous forme de flux ``application/octet-stream``.

Requête
-------

::

    GET /api/admin/storage/download/{id}

Réponse
-------

Flux binaire du fichier (``Content-Type: application/octet-stream``).

.. note::

   La réponse de cette API ne contient pas d'en-tête ``Content-Disposition``.
   Le nom du fichier à enregistrer doit être spécifié côté client (avec l'option ``-o`` pour cURL).

Suppression d'un fichier
===========================

Supprime un fichier du stockage. Indiquez dans ``{id}`` l'``id`` obtenu lors du listage.

Requête
-------

::

    DELETE /api/admin/storage/delete/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

Envoi d'un fichier
====================

Envoie un fichier vers le stockage au format ``multipart/form-data``.
Le répertoire de destination est spécifié via le champ de formulaire ``path``, et non dans le chemin de l'URL.

Requête
-------

::

    PUT /api/admin/storage/upload
    Content-Type: multipart/form-data

Description des champs
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Champ
     - Obligatoire
     - Description
   * - ``path``
     - Non
     - Chemin du répertoire de destination (sans slash initial ni final). Si non spécifié, le fichier est enregistré à la racine (directement sous le bucket).
   * - ``file``
     - Oui
     - Fichier à envoyer

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

Erreurs
=======

En cas d'échec du traitement, chaque endpoint retourne une réponse avec un ``status`` différent de 0 (``1`` en cas d'erreur de validation).
Le champ ``message`` du corps de la réponse contient le détail de l'erreur. Pour plus de détails sur les valeurs de status et les codes de statut HTTP, consultez :doc:`api-admin-overview`.

Les principaux cas d'erreur sont les suivants.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Principaux cas d'erreur
   * - Obtention de la liste des fichiers et répertoires
     - Lorsque le nombre d'éléments récupérés dépasse la limite maximale
   * - Téléchargement d'un fichier
     - Lorsque l'``id`` est invalide ou que le téléchargement échoue
   * - Suppression d'un fichier
     - Lorsque l'``id`` est invalide ou que la suppression échoue
   * - Envoi d'un fichier
     - Lorsque ``file`` n'est pas spécifié ou que l'envoi échoue

Exemples d'utilisation
======================

Obtention de la liste du répertoire racine
-------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/list/" \
         -H "Authorization: Bearer YOUR_TOKEN"

Téléchargement d'un fichier
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/download/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o sample.txt

Suppression d'un fichier
---------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/storage/delete/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN"

Envoi d'un fichier
---------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/storage/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "path=subdir" \
         -F "file=@sample.txt"

Informations complémentaires
=============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
