==========================
API DataConfig
==========================

Vue d'ensemble
==============

L'API DataConfig permet de gérer les configurations de datastore de |Fess|.
Vous pouvez manipuler les configurations de crawl pour les bases de données, les fichiers CSV, JSON et autres sources de données.

URL de base
===========

::

    /api/admin/dataconfig

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
     - Obtention de la liste des configurations datastore
   * - GET
     - /setting/{id}
     - Obtention d'une configuration datastore
   * - POST
     - /setting
     - Création d'une configuration datastore
   * - PUT
     - /setting
     - Mise à jour d'une configuration datastore
   * - DELETE
     - /setting/{id}
     - Suppression d'une configuration datastore

Obtention de la liste des configurations datastore
==================================================

Requête
-------

::

    GET /api/admin/dataconfig/settings

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Paramètre
     - Type
     - Requis
     - Description
   * - ``size``
     - Integer
     - Non
     - Nombre d'éléments par page (par défaut : 25)
   * - ``page``
     - Integer
     - Non
     - Numéro de page (commence à 1, par défaut : 1)
   * - ``name``
     - String
     - Non
     - Filtrer par nom de configuration
   * - ``handlerName``
     - String
     - Non
     - Filtrer par nom de gestionnaire
   * - ``description``
     - String
     - Non
     - Filtrer par description

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "dataconfig_id_1",
            "name": "Database Crawler",
            "description": "Crawler de base de données",
            "handlerName": "DatabaseDataStore",
            "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb",
            "handlerScript": "...",
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

Obtention d'une configuration datastore
=======================================

Requête
-------

::

    GET /api/admin/dataconfig/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "dataconfig_id_1",
          "name": "Database Crawler",
          "description": "Crawler de base de données",
          "handlerName": "DatabaseDataStore",
          "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb\nusername=dbuser\npassword=dbpass",
          "handlerScript": "...",
          "boost": 1.0,
          "available": "true",
          "sortOrder": 0,
          "permissions": "{role}admin",
          "virtualHosts": ""
        }
      }
    }

Création d'une configuration datastore
======================================

Requête
-------

::

    POST /api/admin/dataconfig/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Product Database",
      "handlerName": "DatabaseDataStore",
      "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/products\nusername=user\npassword=pass",
      "handlerScript": "url=\"https://example.com/product/\" + product_id\ntitle=product_name\ncontent=description",
      "boost": 1.0,
      "available": "true",
      "sortOrder": 0,
      "permissions": "{role}admin\n{role}user"
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``name``
     - Oui
     - Nom de la configuration
   * - ``description``
     - Non
     - Description de la configuration
   * - ``handlerName``
     - Oui
     - Nom du gestionnaire de datastore
   * - ``handlerParameter``
     - Non
     - Paramètres du gestionnaire (informations de connexion, etc.)
   * - ``handlerScript``
     - Non
     - Script de transformation des données
   * - ``boost``
     - Oui
     - Valeur de boost des résultats de recherche
   * - ``available``
     - Oui
     - Activé/Désactivé (chaîne ``"true"`` / ``"false"``)
   * - ``sortOrder``
     - Oui
     - Ordre d'affichage
   * - ``permissions``
     - Non
     - Rôles autorisés (séparés par des sauts de ligne si plusieurs)
   * - ``virtualHosts``
     - Non
     - Hôtes virtuels (séparés par des sauts de ligne si plusieurs)

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_dataconfig_id",
        "created": true
      }
    }

Mise à jour d'une configuration datastore
=========================================

Requête
-------

::

    PUT /api/admin/dataconfig/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_dataconfig_id",
      "name": "Updated Product Database",
      "handlerName": "DatabaseDataStore",
      "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/products\nusername=user\npassword=newpass",
      "handlerScript": "url=\"https://example.com/product/\" + product_id\ntitle=product_name\ncontent=description + \" \" + features",
      "boost": 1.5,
      "available": "true",
      "sortOrder": 0,
      "versionNo": 1
    }

Les requêtes de mise a jour nécessitent les mêmes champs obligatoires que la création (``name``, ``handlerName``, ``boost``, ``available``, ``sortOrder``), ainsi que les champs suivants :

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``id``
     - Oui
     - ID de la configuration à mettre à jour
   * - ``versionNo``
     - Oui
     - Numéro de version pour le verrouillage optimiste (indiquer la valeur obtenue lors de la récupération du paramètre)

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_dataconfig_id",
        "created": false
      }
    }

Suppression d'une configuration datastore
=========================================

Requête
-------

::

    DELETE /api/admin/dataconfig/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Types de gestionnaires
======================

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Nom du gestionnaire
     - Description
   * - ``DatabaseDataStore``
     - Connexion à une base de données via JDBC
   * - ``CsvDataStore``
     - Lecture des données depuis un fichier CSV (traitement de chaque ligne comme un document)
   * - ``CsvListDataStore``
     - Lecture des fichiers CSV avec suppression automatique des fichiers traités (extension de ``CsvDataStore`` avec filtrage par horodatage)
   * - ``JsonDataStore``
     - Lecture des données depuis un fichier JSON ou une API JSON

.. note::

   Les types de gestionnaires disponibles dépendent des plugins de datastore installés.
   Les gestionnaires ci-dessus sont inclus par défaut. L'installation de plugins de datastore
   tels que SharePoint, Slack ou Salesforce rend disponibles leurs noms de gestionnaire respectifs.

Exemples d'utilisation
======================

Configuration de crawl de base de données
-----------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dataconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "User Database",
           "handlerName": "DatabaseDataStore",
           "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/userdb\nusername=dbuser\npassword=dbpass\nsql=SELECT * FROM users WHERE active=true",
           "handlerScript": "url=\"https://example.com/user/\" + user_id\ntitle=username\ncontent=profile",
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0
         }'

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-webconfig` - API de configuration de crawl Web
- :doc:`api-admin-fileconfig` - API de configuration de crawl de fichiers
- :doc:`../../admin/dataconfig-guide` - Guide de configuration datastore
