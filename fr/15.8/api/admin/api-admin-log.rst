==========================
Log API
==========================

Vue d'ensemble
==============

L'API Log permet de consulter et de télécharger les fichiers journaux de |Fess|.
Vous pouvez obtenir la liste des fichiers journaux générés sur le serveur et télécharger individuellement chaque fichier journal.

URL de base
===========

::

    /api/admin/log

Authentification
=================

Comme pour les autres API Admin, une authentification par jeton d'accès est requise. Le jeton d'accès doit disposer de la permission ``Radmin-api`` (configurée via ``api.admin.access.permissions``, valeur par défaut : ``Radmin-api``).
Indiquez le jeton d'accès dans l'en-tête de la requête.

::

    Authorization: Bearer <jeton d'accès>

Pour plus de détails sur l'authentification et l'obtention d'un jeton d'accès, consultez :doc:`api-admin-overview`.

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Méthode
     - Chemin
     - Description
   * - GET
     - /files
     - Obtention de la liste des fichiers journaux
   * - GET
     - /file/{id}
     - Téléchargement d'un fichier journal

Obtention de la liste des fichiers journaux
=============================================

Renvoie la liste des fichiers journaux (``.log`` et ``.log.gz``) présents dans le répertoire de sortie des journaux du serveur.
Les fichiers sont retournés triés par ordre croissant de nom de fichier.

Requête
-------

::

    GET /api/admin/log/files

Réponse
-------

``files`` contient un tableau d'objets représentant les informations de chaque fichier journal, et ``total`` contient le nombre d'éléments.
Chaque objet possède les champs suivants.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``id``
     - Valeur du nom de fichier encodé en Base64 URL (utilisée comme ``{id}`` lors du téléchargement)
   * - ``name``
     - Nom du fichier journal
   * - ``lastModified``
     - Date et heure de dernière modification

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
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

.. note::

   ``version`` contient la version du produit |Fess| en cours d'exécution. Le contenu de ``files``
   et le nombre d'éléments varient selon les fichiers journaux présents sur le serveur ;
   l'exemple ci-dessus est fourni à titre indicatif.

Téléchargement d'un fichier journal
=====================================

Télécharge le contenu du fichier journal spécifié.
Pour ``{id}``, indiquez tel quel l'``id`` retourné lors de l'obtention de la liste (la valeur du nom de fichier encodée en Base64 URL).
La réponse est renvoyée sous forme de flux ``application/octet-stream``.
Pour des raisons de sécurité, seuls les noms se terminant par ``.log`` ou ``.log.gz`` sont acceptés ; les noms contenant des séquences de manipulation de chemin telles que ``..`` sont rejetés.
Si vous spécifiez un nom de fichier inexistant ou un nom non autorisé en tant que fichier journal, une réponse vide est renvoyée.

Requête
-------

::

    GET /api/admin/log/file/{id}

Réponse
-------

Flux binaire du fichier journal (``Content-Type: application/octet-stream``).

Exemples d'utilisation
======================

Obtention de la liste des fichiers journaux
---------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/files" \
         -H "Authorization: Bearer YOUR_TOKEN"

Téléchargement d'un fichier journal
-------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/file/ZmVzcy5sb2c=" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess.log

Informations complémentaires
=============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-backup` - API de sauvegarde
