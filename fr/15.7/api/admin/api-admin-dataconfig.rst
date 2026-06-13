==========================
API DataConfig
==========================

Vue d'ensemble
==============

L'API DataConfig permet de gerer les configurations de datastore de |Fess|.
Vous pouvez manipuler les configurations de crawl pour les bases de donnees, les fichiers CSV, JSON et autres sources de donnees.

URL de base
===========

::

    /api/admin/dataconfig

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
     - Obtention de la liste des configurations datastore
   * - GET
     - /setting/{id}
     - Obtention d'une configuration datastore
   * - POST
     - /setting
     - Creation d'une configuration datastore
   * - PUT
     - /setting
     - Mise a jour d'une configuration datastore
   * - DELETE
     - /setting/{id}
     - Suppression d'une configuration datastore

Obtention de la liste des configurations datastore
==================================================

Requete
-------

::

    GET /api/admin/dataconfig/settings

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
            "id": "dataconfig_id_1",
            "name": "Database Crawler",
            "description": "データベースクローラー",
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

Requete
-------

::

    GET /api/admin/dataconfig/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "dataconfig_id_1",
          "name": "Database Crawler",
          "description": "データベースクローラー",
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

Creation d'une configuration datastore
======================================

Requete
-------

::

    POST /api/admin/dataconfig/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Product Database",
      "handlerName": "DatabaseDataStore",
      "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/products\nusername=user\npassword=pass",
      "handlerScript": "url=\"https://example.com/product/\" + data.product_id\ntitle=data.product_name\ncontent=data.description",
      "boost": 1.0,
      "available": "true",
      "sortOrder": 0,
      "permissions": "{role}admin\n{role}user"
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
   * - ``handlerName``
     - Oui
     - Nom du gestionnaire de datastore
   * - ``handlerParameter``
     - Non
     - Parametres du gestionnaire (informations de connexion, etc.)
   * - ``handlerScript``
     - Non
     - Script de transformation des donnees
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

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_dataconfig_id",
        "created": true
      }
    }

Mise a jour d'une configuration datastore
=========================================

Requete
-------

::

    PUT /api/admin/dataconfig/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_dataconfig_id",
      "name": "Updated Product Database",
      "handlerName": "DatabaseDataStore",
      "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/products\nusername=user\npassword=newpass",
      "handlerScript": "url=\"https://example.com/product/\" + data.product_id\ntitle=data.product_name\ncontent=data.description + \" \" + data.features",
      "boost": 1.5,
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
        "id": "existing_dataconfig_id",
        "created": false
      }
    }

Suppression d'une configuration datastore
=========================================

Requete
-------

::

    DELETE /api/admin/dataconfig/setting/{id}

Reponse
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
     - Connexion a une base de donnees via JDBC
   * - ``CsvDataStore``
     - Lecture des donnees depuis un fichier CSV
   * - ``JsonDataStore``
     - Lecture des donnees depuis un fichier JSON ou une API JSON

Exemples d'utilisation
======================

Configuration de crawl de base de donnees
-----------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dataconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "User Database",
           "handlerName": "DatabaseDataStore",
           "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/userdb\nusername=dbuser\npassword=dbpass\nsql=SELECT * FROM users WHERE active=true",
           "handlerScript": "url=\"https://example.com/user/\" + data.user_id\ntitle=data.username\ncontent=data.profile",
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0
         }'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-webconfig` - API de configuration de crawl Web
- :doc:`api-admin-fileconfig` - API de configuration de crawl de fichiers
- :doc:`../../admin/dataconfig-guide` - Guide de configuration datastore
