==========================
API Backup
==========================

Vue d'ensemble
==============

L'API Backup permet de consulter et de telecharger les donnees cibles de sauvegarde de |Fess|.
Vous pouvez obtenir la liste des cibles de sauvegarde et telecharger individuellement chaque fichier de sauvegarde (proprietes systeme, donnees en masse de chaque index, donnees NDJSON des journaux).

Cette API est reservee a la consultation et au telechargement (lecture seule). La fonctionnalite de restauration permettant de televerser des fichiers de sauvegarde pour les restaurer n'est pas fournie par l'API. Si vous avez besoin d'effectuer une restauration, utilisez Informations systeme → Sauvegarde dans la console d'administration.

URL de base
===========

::

    /api/admin/backup

Authentification
================

Comme pour les autres API Admin, une authentification par jeton d'acces est requise. Le jeton d'acces doit disposer de la permission ``Radmin-api`` (configuree via ``api.admin.access.permissions``, valeur par defaut : ``Radmin-api``).
Indiquez le jeton d'acces dans l'en-tete de la requete.

::

    Authorization: Bearer <jeton d'acces>

Pour plus de details sur l'authentification et l'obtention d'un jeton d'acces, consultez :doc:`api-admin-overview`.

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
===============================================

Renvoie la liste des cibles de sauvegarde. Les cibles reposent sur les parametres ``index.backup.targets`` et ``index.backup.log.targets`` ; la liste retournee est la concatenation des deux.

Requete
-------

::

    GET /api/admin/backup/files

Reponse
-------

``files`` contient un tableau d'objets representant les cibles de sauvegarde, et ``total`` contient le nombre d'elements.
Chaque objet possede ``id`` et ``name``, tous deux renseignes avec le nom de la cible (``fess_config.bulk``, ``system.properties``, ``search_log.ndjson``, etc.).

Voici un exemple avec la configuration par defaut (valeurs par defaut de ``index.backup.targets`` et ``index.backup.log.targets``).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
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

   ``version`` contient la version du produit |Fess| en cours d'execution. Le contenu de ``files``
   varie selon les parametres ``index.backup.targets`` / ``index.backup.log.targets`` ;
   l'exemple ci-dessus correspond aux valeurs par defaut.

Telechargement d'un fichier de sauvegarde
==========================================

Telecharge le contenu du fichier de sauvegarde specifie. Pour ``{id}``, indiquez l'``id`` (nom de la cible) obtenu lors de l'obtention de la liste.
Selon le type de ``{id}``, le contenu de la reponse change comme suit.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ID
     - Contenu
   * - ``system.properties``
     - Contenu des proprietes systeme (``application/octet-stream``)
   * - ``*.bulk`` ou nom d'index sans extension
     - Donnees en masse generees en parcourant (scroll) l'index du meme nom que la cible (``application/octet-stream``). Le nom sans ``.bulk`` est traite comme le nom de l'index.
   * - ``*.ndjson`` (``search_log`` / ``user_info`` / ``click_log`` / ``favorite_log``)
     - Donnees NDJSON du journal correspondant (``application/x-ndjson``)

.. note::

   ``fess.json`` et ``doc.json`` sont des fichiers de definition de mapping (schema) d'index.
   Ils figurent dans la liste des cibles (``/files``), mais lors du telechargement via cette API,
   ils sont traites comme un parcours (scroll) d'index, de la meme maniere que ``.bulk``.
   Pour la sauvegarde et la restauration incluant les definitions de mapping, utilisez
   Informations systeme → Sauvegarde dans la console d'administration.

Si vous specifiez un ``{id}`` inexistant parmi les cibles de sauvegarde, une reponse d'erreur est renvoyee avec une valeur differente de 0 dans ``status`` et le message d'erreur (``Could not find any backup index.``).

Requete
-------

::

    GET /api/admin/backup/file/{id}

Reponse
-------

Flux du fichier de sauvegarde. Au format NDJSON, il est renvoye avec ``Content-Type: application/x-ndjson``, sinon avec ``application/octet-stream``.

.. note::

   L'export des journaux (``*.ndjson``) est soumis a la contrainte ``index.backup.log.load.timeout``
   (valeur par defaut : ``60000`` millisecondes). Si la generation prend trop de temps, les donnees
   de journal peuvent etre tronquees en cours de route.

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
