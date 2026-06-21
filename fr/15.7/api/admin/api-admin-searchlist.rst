==========================
SearchList API
==========================

Vue d'ensemble
==============

L'API SearchList est une API d'administration de |Fess| permettant de rechercher et de gerer les documents dans l'index.
Elle permet de rechercher, obtenir, creer, mettre a jour et supprimer des documents.

Tous les noms de champs dans la reponse sont en ``snake_case``. Les champs dont la valeur est ``null`` sont omis de la reponse.

URL de base
===========

::

    /api/admin/searchlist

Authentification
================

Pour appeler cette API, une authentification par jeton d'acces est requise, comme explique dans :doc:`api-admin-overview`.
Le jeton doit disposer des permissions d'acces a l'API d'administration (par defaut ``Radmin-api``).
Cette permission peut etre modifiee via la cle de configuration ``api.admin.access.permissions``.

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Chemin
     - Description
   * - GET / PUT
     - /docs
     - Recherche de documents
   * - GET
     - /doc/{id}
     - Obtention d'un document
   * - POST
     - /doc
     - Creation d'un document
   * - PUT
     - /doc
     - Mise a jour d'un document
   * - DELETE
     - /doc/{id}
     - Suppression d'un document (par ID)
   * - DELETE
     - /query
     - Suppression de documents (par requete)

Recherche de documents
======================

Recherche les documents correspondant aux criteres de recherche.

Requete
-------

::

    GET /api/admin/searchlist/docs
    PUT /api/admin/searchlist/docs

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``q``
     - String
     - Non
     - Requete de recherche (1000 caracteres maximum). Si elle n'est pas specifiee, tous les documents sont concernes.
   * - ``sort``
     - String
     - Non
     - Champ et direction de tri (ex. ``last_modified.desc``).
   * - ``start``
     - Integer
     - Non
     - Position de depart a base zero (par defaut ``0``).
   * - ``offset``
     - Integer
     - Non
     - Decalage depuis ``start`` (par defaut ``0``).
   * - ``pn``
     - Integer
     - Non
     - Numero de page.
   * - ``num``
     - Integer
     - Non
     - Nombre d'elements a obtenir (par defaut ``10``). Les valeurs depassant le maximum configure (par defaut ``100``) ou les valeurs inferieures ou egales a ``0`` sont ramenees au maximum.
   * - ``size``
     - Integer
     - Non
     - Nombre d'elements a obtenir (alias de ``num``, fourni pour compatibilite avec les autres API d'administration).
   * - ``lang``
     - String[]
     - Non
     - Langue de recherche. Peut etre specifie plusieurs fois (tableau). Ex. ``en``.
   * - ``ex_q``
     - String[]
     - Non
     - Expressions de requete supplementaires. Peut etre specifie plusieurs fois (tableau).
   * - ``fields.<name>``
     - String[]
     - Non
     - Filtre par valeur de champ. Le cas le plus courant est ``fields.label`` (filtre par nom d'etiquette) ; tout ``fields.<name>`` restreint les resultats aux documents dont le champ ``<name>`` correspond a la valeur donnee. Peut etre specifie plusieurs fois.
   * - ``as.<name>``
     - String[]
     - Non
     - Conditions de recherche avancee. Tout ``as.<name>`` (ex. ``as.q``) est transmis au generateur de conditions de recherche avancee. Peut etre specifie plusieurs fois par nom.
   * - ``sdh``
     - String
     - Non
     - Hachage de document similaire (similar-document hash).

.. note::

   Cet endpoint ne prend pas en charge les facettes, la mise en evidence ou la recherche geographique. Ces parametres sont ignores s'ils sont specifies.

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "query_id": "f8b1c2d3e4a5",
        "exec_time": "0.05",
        "query_time": 8,
        "page_size": 20,
        "page_number": 1,
        "record_count": 234,
        "record_count_relation": "eq",
        "page_count": 12,
        "next_page": true,
        "prev_page": false,
        "start_record_number": 1,
        "end_record_number": 20,
        "page_numbers": ["1", "2", "3", "4", "5"],
        "partial": false,
        "search_query": "title:Fess OR content:Fess",
        "requested_time": 1717142400000,
        "docs": [
          {
            "doc_id": "abcdef0123456789",
            "url": "https://example.com/page1",
            "title": "Sample Page 1",
            "content_description": "..."
          }
        ]
      }
    }

Champs de la reponse
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``version``
     - Version de |Fess| en cours d'execution (la valeur d'exemple est indicative).
   * - ``status``
     - Code de statut (``0`` en cas de succes ; voir "Codes de statut").
   * - ``query_id``
     - ID de la requete de recherche.
   * - ``docs``
     - Tableau des documents resultats de la recherche. Chaque document est une carte de noms de champs et de valeurs, utilisant les noms de champs de l'index tels quels (``doc_id``, ``url``, ``title``, ``content_description``, etc.).
   * - ``exec_time``
     - Temps d'execution de la recherche (secondes, chaine de caracteres).
   * - ``query_time``
     - Temps de requete du moteur de recherche (millisecondes).
   * - ``page_size``
     - Nombre d'elements par page.
   * - ``page_number``
     - Numero de la page courante.
   * - ``record_count``
     - Nombre d'elements correspondants.
   * - ``record_count_relation``
     - Relation du nombre d'elements correspondants. ``eq`` indique un comptage exact, ``gte`` indique que seule la borne inferieure est connue.
   * - ``page_count``
     - Nombre total de pages.
   * - ``next_page``
     - Indique s'il existe une page suivante (bool).
   * - ``prev_page``
     - Indique s'il existe une page precedente (bool).
   * - ``start_record_number``
     - Numero du premier enregistrement de cette page.
   * - ``end_record_number``
     - Numero du dernier enregistrement de cette page.
   * - ``page_numbers``
     - Tableau des numeros de page a afficher dans le paginateur (chaines de caracteres).
   * - ``partial``
     - Indique si les resultats sont partiels (bool).
   * - ``search_query``
     - Requete de recherche reellement executee.
   * - ``requested_time``
     - Horodatage de la requete (epoch en millisecondes).
   * - ``highlight_params``
     - Chaine de parametres de requete pour la mise en evidence (generalement vide pour cette API d'administration).

Obtention d'un document
=======================

Obtient un seul document en specifiant son ID de document.

Requete
-------

::

    GET /api/admin/searchlist/doc/{id}

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``id``
     - String
     - Oui
     - ID du document (valeur de ``doc_id``, parametre de chemin).

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "doc": {
          "doc_id": "abcdef0123456789",
          "url": "https://example.com/page1",
          "title": "Sample Page 1"
        }
      }
    }

Si aucun document n'existe pour l'ID specifie, une reponse d'erreur (``status`` = ``1``) est retournee.

Creation d'un document
======================

Cree un nouveau document dans l'index.

Requete
-------

::

    POST /api/admin/searchlist/doc
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "doc": {
        "url": "https://example.com/page1",
        "title": "Sample Page 1",
        "content": "This is the body text.",
        "role": ["{role}guest"],
        "boost": 1.0
      }
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``doc``
     - Oui
     - Document a enregistrer. Specifie sous forme de carte de noms de champs d'index et de valeurs.

Parmi les champs specifies dans ``doc``, tous les champs obligatoires configures dans ``index.admin.required.fields`` (par defaut ``url,title,role,boost``) doivent etre fournis.
Contrairement a l'API :doc:`Documents API <api-admin-documents>` par lot, cet endpoint ne complete pas automatiquement les valeurs par defaut telles que ``role`` ou ``boost``, de sorte que les champs obligatoires doivent etre specifies explicitement dans la requete.
``doc_id`` est genere automatiquement cote serveur et n'est pas specifie lors de la creation.

La valeur de chaque champ est validee en fonction de la configuration du type de champ. Si le type ne correspond pas, une erreur (``status`` = ``1``) est retournee.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Cle de configuration
     - Valeur par defaut
   * - ``index.admin.array.fields``
     - ``lang,role,label,anchor,virtual_host``
   * - ``index.admin.date.fields``
     - ``expires,created,timestamp,last_modified``
   * - ``index.admin.integer.fields``
     - (vide)
   * - ``index.admin.long.fields``
     - ``content_length,favorite_count,click_count``
   * - ``index.admin.float.fields``
     - ``boost``
   * - ``index.admin.double.fields``
     - (vide)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": true
      }
    }

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``id``
     - Le ``doc_id`` du document enregistre.
   * - ``created``
     - ``true`` lors de la creation.

Mise a jour d'un document
=========================

Met a jour un document existant.

Requete
-------

::

    PUT /api/admin/searchlist/doc
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "doc": {
        "doc_id": "abcdef0123456789",
        "url": "https://example.com/page1",
        "title": "Updated Title",
        "content": "This is the updated body text.",
        "role": ["{role}guest"],
        "boost": 1.0
      }
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``doc``
     - Oui
     - Document a mettre a jour. Specifie sous forme de carte de noms de champs d'index et de valeurs.

Le document a mettre a jour est identifie par ``doc_id`` dans ``doc``. Si ``doc_id`` n'est pas specifie, ou si aucun document correspondant n'existe, une erreur (``status`` = ``1``) est retournee.
Comme pour la creation, tous les champs obligatoires configures dans ``index.admin.required.fields`` (par defaut ``url,title,role,boost``) doivent etre fournis, et la valeur de chaque champ est validee en fonction de la configuration du type.

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": false
      }
    }

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``id``
     - Le ``doc_id`` du document mis a jour.
   * - ``created``
     - ``false`` lors de la mise a jour.

Suppression d'un document (par ID)
===================================

Supprime un document en specifiant son ID de document.

Requete
-------

::

    DELETE /api/admin/searchlist/doc/{id}

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``id``
     - String
     - Oui
     - ID du document (valeur de ``doc_id``, parametre de chemin).

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Suppression de documents (par requete)
=======================================

Supprime en masse les documents correspondant a une requete de recherche.

Requete
-------

::

    DELETE /api/admin/searchlist/query

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``q``
     - String
     - Oui
     - Requete de recherche des documents a supprimer.

La cible de suppression est construite avec la meme requete que "Recherche de documents", de sorte que les parametres de filtrage tels que ``fields.<name>`` et ``ex_q`` peuvent etre utilises conjointement. Si ``q`` n'est pas specifie, une erreur (``status`` = ``1``) est retournee.

Reponse
-------

Retourne le nombre de documents supprimes dans ``count``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "count": 150
      }
    }

Codes de statut
===============

Le champ ``status`` dans la reponse prend l'une des valeurs suivantes.

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - Valeur
     - Nom
     - Description
   * - ``0``
     - OK
     - Succes.
   * - ``1``
     - BAD_REQUEST
     - La requete est invalide (champ obligatoire manquant, type incorrect, document cible introuvable, requete invalide, etc.).
   * - ``2``
     - SYSTEM_ERROR
     - Erreur systeme.
   * - ``3``
     - UNAUTHORIZED
     - Erreur d'authentification.
   * - ``9``
     - FAILED
     - Le traitement a echoue.

Exemples d'utilisation
======================

Recherche de documents
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/docs?q=Fess&size=20" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtention d'un document
-----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/doc/abcdef0123456789" \
         -H "Authorization: Bearer YOUR_TOKEN"

Creation d'un document
----------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/searchlist/doc" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "doc": {
             "url": "https://example.com/page1",
             "title": "Sample Page 1",
             "content": "This is the body text.",
             "role": ["{role}guest"],
             "boost": 1.0
           }
         }'

Suppression de documents par requete
-------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/searchlist/query?q=url:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informations complementaires
=============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-documents` - API d'enregistrement en masse de documents
- :doc:`api-admin-crawlinginfo` - API des informations de crawl
- :doc:`../../admin/searchlist-guide` - Guide de gestion de la liste de recherche
