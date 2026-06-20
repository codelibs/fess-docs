==========================
BoostDoc API
==========================

Vue d'ensemble
==============

L'API BoostDoc est une API permettant de gerer les configurations de boost de documents dans |Fess|.
En configurant le boost de documents, vous pouvez augmenter le score des documents correspondant a certaines conditions
et les faire apparaitre plus haut dans les resultats de recherche.

Le boost est applique a chaque document lors de la creation de l'index (au moment du crawl).
La condition (``urlExpr``) et la valeur de boost (``boostExpr``) sont toutes deux evaluees comme des expressions Groovy.
Les regles multiples sont evaluees dans l'ordre croissant de ``sortOrder``, et seule la valeur de boost de la premiere regle
dont la condition correspond est appliquee (une fois qu'une regle correspondante est trouvee, les regles suivantes ne sont pas evaluees).

.. note::

   Dans l'interface d'administration, ``urlExpr`` est affiche sous le nom « Condition » et ``boostExpr`` sous le nom « Expression de valeur de boost ».
   Pour plus de details sur les elements de configuration, consultez :doc:`../../admin/boostdoc-guide`.

URL de base
===========

::

    /api/admin/boostdoc

Authentification
================

Pour utiliser cette API, un jeton d'acces avec la permission ``Radmin-api`` est requis.
Pour savoir comment obtenir et specifier un jeton d'acces, consultez :doc:`api-admin-overview`.

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
     - Obtention de la liste des boosts de documents
   * - GET
     - /setting/{id}
     - Obtention d'un boost de document
   * - POST
     - /setting
     - Creation d'un boost de document
   * - PUT
     - /setting
     - Mise a jour d'un boost de document
   * - DELETE
     - /setting/{id}
     - Suppression d'un boost de document

Obtention de la liste des boosts de documents
=============================================

Requete
-------

::

    GET /api/admin/boostdoc/settings

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
     - Nombre d'elements par page (par defaut : 25)
   * - ``page``
     - Integer
     - Non
     - Numero de page (commence a 1. Par defaut : 1)
   * - ``urlExpr``
     - String
     - Non
     - Filtrage par expression de condition (correspondance partielle)
   * - ``boostExpr``
     - String
     - Non
     - Filtrage par expression de valeur de boost (correspondance partielle)

Reponse
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

   En plus des champs presentes ci-dessus, chaque objet de configuration dans la reponse inclut egalement des metadonnees de creation/mise a jour (``createdBy``, ``createdTime``, ``updatedBy``, ``updatedTime``).
   ``versionNo`` est obligatoire lors d'une mise a jour (PUT) ; recuperez sa valeur actuelle via l'API d'obtention ou de liste avant de proceder a la mise a jour.

Obtention d'un boost de document
==================================

Requete
-------

::

    GET /api/admin/boostdoc/setting/{id}

Reponse
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

Creation d'un boost de document
=================================

Requete
-------

::

    POST /api/admin/boostdoc/setting
    Content-Type: application/json

Corps de la requete
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
   :widths: 25 15.70

   * - Champ
     - Requis
     - Description
   * - ``urlExpr``
     - Oui
     - Expression de condition. Expression Groovy retournant un ``Boolean`` permettant de determiner les documents a booster. Correspond au champ « Condition » de l'interface d'administration (maximum 10000 caracteres).
   * - ``boostExpr``
     - Oui
     - Expression de valeur de boost. Expression Groovy retournant la valeur de boost (numerique). Une valeur fixe telle que ``3.0`` peut egalement etre specifiee. Correspond au champ « Expression de valeur de boost » de l'interface d'administration (maximum 10000 caracteres).
   * - ``sortOrder``
     - Oui
     - Ordre d'application. Les regles sont evaluees dans l'ordre croissant et la valeur de boost de la premiere regle correspondante est appliquee (valeur initiale du formulaire : 0, entier superieur ou egal a 0).

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_boostdoc_id",
        "created": true
      }
    }

Mise a jour d'un boost de document
====================================

Requete
-------

::

    PUT /api/admin/boostdoc/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_boostdoc_id",
      "urlExpr": "url.startsWith(\"https://important.example.com/\")",
      "boostExpr": "10.0",
      "sortOrder": 0,
      "versionNo": 1
    }

Lors de la mise a jour, en plus des champs utilises lors de la creation, ``id`` (l'identifiant de la regle cible, 1000 caracteres maximum) et ``versionNo`` (le numero de version pour le verrouillage optimiste) sont obligatoires. Specifiez pour ``versionNo`` la valeur actuelle obtenue depuis la reponse de l'API d'obtention ou de liste. La mise a jour echoue si le numero de version ne correspond pas.

Reponse
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

Requete
-------

::

    DELETE /api/admin/boostdoc/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Expressions de condition et de valeur de boost
===============================================

``urlExpr`` (condition) et ``boostExpr`` (expression de valeur de boost) sont toutes deux evaluees comme des expressions Groovy.
Dans les expressions, les valeurs des champs du document cible de l'indexation peuvent etre referenciees comme des variables portant le nom du champ.

- ``urlExpr`` doit retourner un ``Boolean`` (exemple : ``url.startsWith("https://docs.example.com/")``). Une simple chaine d'expression reguliere (exemple : ``.*docs\.example\.com.*``) ne retourne pas un ``Boolean`` en tant qu'expression Groovy et ne fonctionne donc pas comme condition. Pour utiliser des expressions regulieres, utilisez ``String#matches`` de Groovy.
- ``boostExpr`` doit retourner une valeur numerique. Le resultat est converti en ``float`` et le boost n'est applique que si la valeur est superieure a 0.

.. note::

   Principales variables de champs referenciables dans les expressions : ``url``, ``title``, ``content``, ``content_length``, ``last_modified``, etc.
   ``click_count`` et ``favorite_count`` sont disponibles respectivement lorsque ``indexer.click.count.enabled`` /
   ``indexer.favorite.count.enabled`` sont actives (toutes deux activees par defaut).
   La syntaxe de calcul de date OpenSearch telle que ``now - 7d`` ne peut pas etre utilisee en Groovy.

Exemples d'expressions de condition (``urlExpr``)
--------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Expression de condition
     - Description
   * - ``url.startsWith("https://docs.example.com/")``
     - Cible les documents dont l'URL commence par la valeur specifiee
   * - ``url.matches("https://www\\.example\\.com/.*")``
     - Evalue l'URL avec une expression reguliere (``String#matches`` de Groovy)
   * - ``title.contains("Notes de version")``
     - Cible les documents dont le titre contient un mot specifique

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
     - Boost sur une echelle logarithmique basee sur le nombre de clics

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

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-elevateword` - API ElevateWord
- :doc:`../../admin/boostdoc-guide` - Guide de gestion des boosts de documents
