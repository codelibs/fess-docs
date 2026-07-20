==========================
API Backup
==========================

Vue d'ensemble
==============

L'API Backup permet de consulter et de télécharger les données cibles de sauvegarde de |Fess|.
Vous pouvez obtenir la liste des cibles de sauvegarde et télécharger individuellement chaque fichier de sauvegarde (propriétés système, données en masse de chaque index, données NDJSON des journaux).

Cette API est réservée à la consultation et au téléchargement (lecture seule). La fonctionnalité de restauration permettant de téléverser des fichiers de sauvegarde pour les restaurer n'est pas fournie par l'API. Si vous avez besoin d'effectuer une restauration, utilisez Informations système → Sauvegarde dans la console d'administration.

URL de base
===========

::

    /api/admin/backup

Authentification
================

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
     - Obtention de la liste des cibles de sauvegarde
   * - GET
     - /file/{id}
     - Téléchargement d'un fichier de sauvegarde

Obtention de la liste des cibles de sauvegarde
===============================================

Renvoie la liste des cibles de sauvegarde. Les cibles reposent sur les paramètres ``index.backup.targets`` et ``index.backup.log.targets`` ; la liste retournée est la concaténation des deux.

Requête
-------

::

    GET /api/admin/backup/files

Réponse
-------

``files`` contient un tableau d'objets représentant les cibles de sauvegarde, et ``total`` contient le nombre d'éléments.
Chaque objet possède ``id`` et ``name``, tous deux renseignés avec le nom de la cible (``fess_config.bulk``, ``system.properties``, ``search_log.ndjson``, etc.).

Voici un exemple avec la configuration par défaut (valeurs par défaut de ``index.backup.targets`` et ``index.backup.log.targets``).

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "files": [
          { "id": "fess_basic_config.bulk", "name": "fess_basic_config.bulk" },
          { "id": "fess_config.bulk", "name": "fess_config.bulk" },
          { "id": "fess_user.bulk", "name": "fess_user.bulk" },
          { "id": "system.properties", "name": "system.properties" },
          { "id": "fess.json", "name": "fess.json" },
          { "id": "doc.json", "name": "doc.json" },
          { "id": "click_log.ndjson", "name": "click_log.ndjson" },
          { "id": "favorite_log.ndjson", "name": "favorite_log.ndjson" },
          { "id": "search_log.ndjson", "name": "search_log.ndjson" },
          { "id": "user_info.ndjson", "name": "user_info.ndjson" }
        ],
        "total": 10
      }
    }

.. note::

   ``version`` contient la version du produit |Fess| en cours d'exécution. Le contenu de ``files``
   varie selon les paramètres ``index.backup.targets`` / ``index.backup.log.targets`` ;
   l'exemple ci-dessus correspond aux valeurs par défaut.

Téléchargement d'un fichier de sauvegarde
==========================================

Télécharge le contenu du fichier de sauvegarde spécifié. Pour ``{id}``, indiquez l'``id`` (nom de la cible) obtenu lors de l'obtention de la liste.
Selon le type de ``{id}``, le contenu de la réponse change comme suit.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ID
     - Contenu
   * - ``system.properties``
     - Contenu des propriétés système (``application/octet-stream``)
   * - ``*.bulk`` ou nom d'index sans extension
     - Données en masse générées en parcourant (scroll) l'index du même nom que la cible (``application/octet-stream``). Le nom sans ``.bulk`` est traité comme le nom de l'index.
   * - ``*.ndjson`` (``search_log`` / ``user_info`` / ``click_log`` / ``favorite_log``)
     - Données NDJSON du journal correspondant (``application/x-ndjson``)

.. note::

   ``fess.json`` et ``doc.json`` sont des fichiers de définition de mapping (schéma) d'index.
   Ils figurent dans la liste des cibles (``/files``), mais lors du téléchargement via cette API,
   ils sont traités comme un parcours (scroll) d'index, de la même manière que ``.bulk``.
   Pour la sauvegarde et la restauration incluant les définitions de mapping, utilisez
   Informations système → Sauvegarde dans la console d'administration.

Si vous spécifiez un ``{id}`` inexistant parmi les cibles de sauvegarde, une réponse d'erreur est renvoyée avec une valeur différente de 0 dans ``status`` et le message d'erreur (``Could not find any backup index.``).

Requête
-------

::

    GET /api/admin/backup/file/{id}

Réponse
-------

Flux du fichier de sauvegarde. Au format NDJSON, il est renvoyé avec ``Content-Type: application/x-ndjson``, sinon avec ``application/octet-stream``.

.. note::

   L'export des journaux (``*.ndjson``) est soumis à la contrainte ``index.backup.log.load.timeout``
   (valeur par défaut : ``60000`` millisecondes). Si la génération prend trop de temps, les données
   de journal peuvent être tronquées en cours de route.

Exemples d'utilisation
======================

Obtention de la liste des cibles de sauvegarde
----------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/files" \
         -H "Authorization: Bearer YOUR_TOKEN"

Téléchargement de l'index de configuration
------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/file/fess_config.bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess_config.bulk

Téléchargement des journaux de recherche
----------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/file/search_log.ndjson" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o search_log.ndjson

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-log` - API de journaux
