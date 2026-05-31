================
API de recherche
================

Ce document décrit l'API de recherche v2 de |Fess|.
Pour l'enveloppe de réponse commune, le modèle d'erreur et les jetons CSRF, voir :doc:`api-overview`.

L'URL de base est ``http://<Server Name>/api/v2/`` (exemple en environnement local : ``http://localhost:8080/api/v2``).

Recherche de documents
======================

Requête
-------

====================  ====================================================
Méthode HTTP          GET
Point de terminaison  ``/api/v2/search``
====================  ====================================================

Recherche les documents correspondant à la requête et retourne les résultats dans l'enveloppe commune.
Tous les noms de champs dans le corps de la réponse utilisent le format ``snake_case``.

Paramètres de requête
~~~~~~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Paramètres de requête

   * - ``q``
     - Terme de recherche (encodé en URL).
   * - ``start``
     - Position de départ à base zéro (entier, ``>=0``, valeur par défaut ``0``).
   * - ``offset``
     - Décalage depuis ``start`` (entier, ``>=0``, valeur par défaut ``0``).
   * - ``num``
     - Taille de la page (entier, ``>=1``, valeur par défaut ``20``). Une valeur ``<= 0`` provoque une erreur ``invalid_request``. Les valeurs dépassant la limite maximale configurée sont réduites silencieusement. Vous pouvez détecter ce rognage en comparant ``num`` dans la requête avec ``page_size`` dans la réponse.
   * - ``sort``
     - Critère de tri (ex. : ``score``).
   * - ``lang``
     - Langue de recherche. Peut être répété (tableau). Ex. : ``en``.
   * - ``ex_q``
     - Expression de requête supplémentaire. Peut être répété.
   * - ``sdh``
     - Hachage de document similaire (similar-document hash).
   * - ``fields.label``
     - Filtre par nom d'étiquette. Peut être répété. Il s'agit du cas le plus courant de la famille générique ``fields.<name>`` : tout paramètre de requête ``fields.<name>`` restreint les résultats aux documents dont le champ ``<name>`` correspond à la valeur spécifiée.
   * - ``as.*``
     - Conditions de recherche avancée. Tout paramètre ``as.<name>`` (ex. : ``as.q``, ``as.filetype``) est transmis au générateur de conditions de recherche avancée. Peut être répété pour chaque nom.
   * - ``track_total_hits``
     - Transmis au moteur de recherche pour contrôler le comptage précis des résultats (ex. : ``true`` ou un seuil entier). Influence la valeur de ``record_count_relation`` (``eq`` ou ``gte``).
   * - ``facet.field``
     - Champ de facette. Peut être répété (tableau).
   * - ``facet.query``
     - Requête de facette. Peut être répété (tableau).
   * - ``facet.size``
     - Nombre maximum de termes de facette à retourner (entier).
   * - ``facet.minDocCount``
     - Nombre minimum de documents contenant un terme de facette (entier).
   * - ``facet.sort``
     - Tri des facettes.
   * - ``facet.missing``
     - Traitement des facettes pour les documents sans valeur.
   * - ``geo.location.point``
     - Point central des coordonnées géographiques (ex. : ``35.0,139.0``).
   * - ``geo.location.distance``
     - Distance depuis le point central (ex. : ``10km``).

Tableau : Paramètres de requête

Réponse
-------

En cas de succès (200), les champs suivants sont retournés directement sous ``response`` dans l'enveloppe commune.

::

    {
      "response": {
        "status": 0,
        "q": "Fess",
        "query_id": "f8b1c2d3e4a5",
        "exec_time": 0.012,
        "query_time": 8,
        "page_size": 20,
        "page_number": 1,
        "record_count": 42,
        "record_count_relation": "eq",
        "page_count": 3,
        "highlight_params": "&hq=Fess",
        "next_page": true,
        "prev_page": false,
        "start_record_number": 1,
        "end_record_number": 20,
        "page_numbers": ["1", "2", "3"],
        "partial": false,
        "search_query": "title:Fess OR content:Fess",
        "requested_time": 1717142400000,
        "related_query": ["enterprise search"],
        "related_contents": [],
        "data": [
          {
            "doc_id": "a1b2c3d4e5f6",
            "url": "https://example.com/",
            "title": "Example",
            "content_description": "An example document about Fess.",
            "score": 1.2345
          }
        ],
        "facet_field": [
          {
            "name": "label",
            "result": [
              { "value": "news", "count": 12 }
            ]
          }
        ],
        "facet_query": [
          { "value": "filetype:html", "count": 30 }
        ]
      }
    }

Les détails de chaque champ sont les suivants.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Champs de réponse

   * - ``q``
     - Terme de recherche (nullable).
   * - ``query_id``
     - Identifiant de la requête.
   * - ``exec_time``
     - Temps d'exécution (double, secondes).
   * - ``query_time``
     - Temps de requête du moteur de recherche (int64, millisecondes).
   * - ``page_size``
     - Taille de la page.
   * - ``page_number``
     - Numéro de la page courante.
   * - ``record_count``
     - Nombre de résultats (int64).
   * - ``record_count_relation``
     - ``eq`` indique un comptage exact ; ``gte`` indique que seule la borne inférieure est connue.
   * - ``page_count``
     - Nombre total de pages.
   * - ``highlight_params``
     - Chaîne de paramètres de requête pour la mise en évidence.
   * - ``next_page``
     - Indique s'il existe une page suivante (bool).
   * - ``prev_page``
     - Indique s'il existe une page précédente (bool).
   * - ``start_record_number``
     - Numéro du premier enregistrement de cette page.
   * - ``end_record_number``
     - Numéro du dernier enregistrement de cette page.
   * - ``page_numbers``
     - Tableau des numéros de page à afficher dans le paginateur (chaînes de caractères).
   * - ``partial``
     - Indique si les résultats sont partiels (bool).
   * - ``search_query``
     - Requête de recherche réellement exécutée.
   * - ``requested_time``
     - Horodatage de la requête (int64, epoch en millisecondes).
   * - ``related_query``
     - Tableau des requêtes associées (chaînes de caractères).
   * - ``related_contents``
     - Tableau des contenus associés (chaînes de caractères).
   * - ``data``
     - Tableau des résultats de recherche, un élément par document. Seuls les champs autorisés par ``QueryFieldConfig#isApiResponseField`` sont inclus ; les valeurs null et les clés vides sont exclues.
   * - ``facet_field``
     - Tableau présent uniquement si des facettes de champ ont été demandées. Chaque élément est de la forme ``{name, result:[{value, count}]}``.
   * - ``facet_query``
     - Tableau présent uniquement si des requêtes de facette ont été demandées. Chaque élément est de la forme ``{value, count}``.

Tableau : Champs de réponse

Réponse d'erreur
~~~~~~~~~~~~~~~~

Pour le détail du modèle d'erreur, voir :doc:`api-overview`. Les statuts HTTP retournés par ce point de terminaison sont les suivants.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur

   * - Code de statut
     - Description
   * - 400 Bad Request
     - La requête est incorrecte.
   * - 405 Method Not Allowed
     - La méthode HTTP n'est pas autorisée.
   * - 500 Internal Server Error
     - Une erreur interne s'est produite sur le serveur.

Tableau : Réponses d'erreur

Récupération de tous les documents (recherche par défilement / NDJSON)
======================================================================

Requête
-------

====================  ====================================================
Méthode HTTP          GET
Point de terminaison  ``/api/v2/documents/all``
====================  ====================================================

Diffuse en continu tous les documents correspondant à la requête au format NDJSON (``application/x-ndjson``).
Chaque ligne est un objet ``{"data":{...}}`` contenant les champs autorisés par ``QueryFieldConfig#isApiResponseField``.

En cas d'échec en cours de stream, la ligne finale sera la suivante.

::

    {"error":{"code":"internal_error","message":"stream error"}}

Le client doit donc vérifier la première clé de la dernière ligne pour distinguer une fin normale (``data``) d'une erreur serveur (``error``).

La requête est construite avec le même ensemble de paramètres que ``GET /search`` (``q``, ``sort``, ``num``, ``lang``, ``ex_q``, ``sdh``, ``fields.*``, ``as.*``, ``track_total_hits``, ``facet.*``, ``geo.*``).
Si la recherche par défilement est désactivée (``api.search.scroll=false``), une erreur ``invalid_request`` (400) est retournée.

Paramètres de requête
~~~~~~~~~~~~~~~~~~~~~

Les paramètres explicitement définis dans la spécification sont les suivants.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Paramètres de requête

   * - ``q``
     - Terme de recherche.
   * - ``sort``
     - Critère de tri.
   * - ``num``
     - Taille de la page (lot de défilement) (entier, ``>=1``). Une valeur ``<= 0`` provoque une erreur ``invalid_request``.
   * - ``lang``
     - Langue de recherche. Peut être répété (tableau).
   * - ``ex_q``
     - Expression de requête supplémentaire. Peut être répété (tableau).
   * - ``fields.label``
     - Filtre par nom d'étiquette. Peut être répété (tableau). Fait partie de la famille générique ``fields.<name>`` (voir ``GET /search``).
   * - ``sdh``
     - Hachage de document similaire (similar-document hash).

Tableau : Paramètres de requête

Réponse
-------

En cas de succès (200), le Content-Type est ``application/x-ndjson``, et les résultats sont retournés à raison d'un document par ligne.

::

    {"data":{"url":"https://example.com/","title":"Example"}}
    {"data":{"url":"https://example.org/","title":"Example Org"}}

Réponse d'erreur
~~~~~~~~~~~~~~~~

Pour le détail du modèle d'erreur, voir :doc:`api-overview`. Les statuts HTTP retournés par ce point de terminaison sont les suivants.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur

   * - Code de statut
     - Description
   * - 400 Bad Request
     - Requête incorrecte, ``num <= 0``, ou recherche par défilement désactivée (``api.search.scroll=false``).
   * - 405 Method Not Allowed
     - La méthode HTTP n'est pas autorisée.
   * - 500 Internal Server Error
     - Une erreur interne s'est produite sur le serveur.

Tableau : Réponses d'erreur
