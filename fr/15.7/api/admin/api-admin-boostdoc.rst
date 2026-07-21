==========================
BoostDoc API
==========================

Vue d'ensemble
==============

L'API BoostDoc est une API permettant de gérer les configurations de boost de documents dans |Fess|.
En configurant le boost de documents, vous pouvez augmenter le score des documents correspondant à certaines conditions
et les faire apparaître plus haut dans les résultats de recherche.

Le boost est appliqué à chaque document lors de la création de l'index (au moment du crawl).
La condition (``urlExpr``) et la valeur de boost (``boostExpr``) sont toutes deux évaluées comme des expressions Groovy.
Les règles multiples sont évaluées dans l'ordre croissant de ``sortOrder``, et seule la valeur de boost de la première règle
dont la condition correspond est appliquée (une fois qu'une règle correspondante est trouvée, les règles suivantes ne sont pas évaluées).

.. note::

   Dans l'interface d'administration, ``urlExpr`` est affiché sous le nom « Condition » et ``boostExpr`` sous le nom « Expression de valeur de boost ».
   Pour plus de détails sur les éléments de configuration, consultez :doc:`../../admin/boostdoc-guide`.

URL de base
===========

::

    /api/admin/boostdoc

Authentification
================

Pour utiliser cette API, un jeton d'accès avec la permission ``Radmin-api`` est requis.
Pour savoir comment obtenir et spécifier un jeton d'accès, consultez :doc:`api-admin-overview`.

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
     - Obtention de la liste des boosts de documents
   * - GET
     - /setting/{id}
     - Obtention d'un boost de document
   * - POST
     - /setting
     - Création d'un boost de document
   * - PUT
     - /setting
     - Mise à jour d'un boost de document
   * - DELETE
     - /setting/{id}
     - Suppression d'un boost de document

Obtention de la liste des boosts de documents
=============================================

Requête
-------

::

    GET /api/admin/boostdoc/settings

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
     - Numéro de page (commence à 1. Par défaut : 1)
   * - ``urlExpr``
     - String
     - Non
     - Filtrage par expression de condition (correspondance partielle)
   * - ``boostExpr``
     - String
     - Non
     - Filtrage par expression de valeur de boost (correspondance partielle)

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "boostdoc_id_1",
            "urlExpr": "url.startsWith(\"https://docs.example.com/\")",
            "boostExpr": "3.0",
            "sortOrder": 1,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   En plus des champs présentés ci-dessus, chaque objet de configuration dans la réponse inclut également des métadonnées de création/mise à jour (``createdBy``, ``createdTime``, ``updatedBy``, ``updatedTime``).
   ``versionNo`` est obligatoire lors d'une mise à jour (PUT) ; récupérez sa valeur actuelle via l'API d'obtention ou de liste avant de procéder à la mise à jour.

Obtention d'un boost de document
==================================

Requête
-------

::

    GET /api/admin/boostdoc/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "boostdoc_id_1",
          "urlExpr": "url.startsWith(\"https://docs.example.com/\")",
          "boostExpr": "3.0",
          "sortOrder": 1,
          "versionNo": 1
        }
      }
    }

Création d'un boost de document
=================================

Requête
-------

::

    POST /api/admin/boostdoc/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "urlExpr": "url.startsWith(\"https://important.example.com/\")",
      "boostExpr": "5.0",
      "sortOrder": 0
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``urlExpr``
     - Oui
     - Expression de condition. Expression Groovy retournant un ``Boolean`` permettant de déterminer les documents à booster. Correspond au champ « Condition » de l'interface d'administration (maximum 10000 caractères).
   * - ``boostExpr``
     - Oui
     - Expression de valeur de boost. Expression Groovy retournant la valeur de boost (numérique). Une valeur fixe telle que ``3.0`` peut également être spécifiée. Correspond au champ « Expression de valeur de boost » de l'interface d'administration (maximum 10000 caractères).
   * - ``sortOrder``
     - Oui
     - Ordre d'application. Les règles sont évaluées dans l'ordre croissant et la valeur de boost de la première règle correspondante est appliquée (valeur initiale du formulaire : 0, entier supérieur ou égal à 0).

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_boostdoc_id",
        "created": true
      }
    }

Mise à jour d'un boost de document
====================================

Requête
-------

::

    PUT /api/admin/boostdoc/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_boostdoc_id",
      "urlExpr": "url.startsWith(\"https://important.example.com/\")",
      "boostExpr": "10.0",
      "sortOrder": 0,
      "versionNo": 1
    }

Lors de la mise à jour, en plus des champs utilisés lors de la création, ``id`` (l'identifiant de la règle cible, 1000 caractères maximum) et ``versionNo`` (le numéro de version pour le verrouillage optimiste) sont obligatoires. Spécifiez pour ``versionNo`` la valeur actuelle obtenue depuis la réponse de l'API d'obtention ou de liste. La mise à jour échoue si le numéro de version ne correspond pas.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_boostdoc_id",
        "created": false
      }
    }

Suppression d'un boost de document
====================================

Requête
-------

::

    DELETE /api/admin/boostdoc/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Expressions de condition et de valeur de boost
===============================================

``urlExpr`` (condition) et ``boostExpr`` (expression de valeur de boost) sont toutes deux évaluées comme des expressions Groovy.
Dans les expressions, les valeurs des champs du document cible de l'indexation peuvent être référenciées comme des variables portant le nom du champ.

- ``urlExpr`` doit retourner un ``Boolean`` (exemple : ``url.startsWith("https://docs.example.com/")``). Une simple chaîne d'expression régulière (exemple : ``.*docs\.example\.com.*``) ne retourne pas un ``Boolean`` en tant qu'expression Groovy et ne fonctionne donc pas comme condition. Pour utiliser des expressions régulières, utilisez ``String#matches`` de Groovy.
- ``boostExpr`` doit retourner une valeur numérique. Le résultat est converti en ``float`` et le boost n'est appliqué que si la valeur est supérieure à 0.

.. note::

   Principales variables de champs référenciables dans les expressions : ``url``, ``title``, ``content``, ``content_length``, ``last_modified``, etc.
   ``click_count`` et ``favorite_count`` sont disponibles respectivement lorsque ``indexer.click.count.enabled`` /
   ``indexer.favorite.count.enabled`` sont actives (toutes deux activées par défaut).
   La syntaxe de calcul de date OpenSearch telle que ``now - 7d`` ne peut pas être utilisée en Groovy.

Exemples d'expressions de condition (``urlExpr``)
--------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Expression de condition
     - Description
   * - ``url.startsWith("https://docs.example.com/")``
     - Cible les documents dont l'URL commence par la valeur spécifiée
   * - ``url.matches("https://www\\.example\\.com/.*")``
     - Évalue l'URL avec une expression régulière (``String#matches`` de Groovy)
   * - ``title.contains("Notes de version")``
     - Cible les documents dont le titre contient un mot spécifique

Exemples d'expressions de valeur de boost (``boostExpr``)
----------------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Expression de valeur de boost
     - Description
   * - ``3.0``
     - Boost avec une valeur fixe
   * - ``click_count * 0.1 + 1``
     - Boost proportionnel au nombre de clics
   * - ``Math.log(click_count + 1)``
     - Boost sur une échelle logarithmique basée sur le nombre de clics

Exemples d'utilisation
======================

Boost d'un site de documentation
----------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": "url.startsWith(\"https://docs.example.com/\")",
           "boostExpr": "5.0",
           "sortOrder": 0
         }'

Boost de contenu populaire
---------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": "url.startsWith(\"https://www.example.com/\")",
           "boostExpr": "click_count * 0.1 + 1",
           "sortOrder": 10
         }'

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-elevateword` - API ElevateWord
- :doc:`../../admin/boostdoc-guide` - Guide de gestion des boosts de documents
