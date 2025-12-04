===============
API de recherche
===============

Obtention des résultats de recherche
=====================================

Requête
-------

==================  ====================================================
Méthode HTTP        GET
Point de terminaison ``/api/v1/documents``
==================  ====================================================

En envoyant une requête à |Fess| de type
``http://<Nom du serveur>/api/v1/documents?q=mot_recherche``,
vous pouvez recevoir les résultats de recherche de |Fess| au format JSON.
Pour utiliser l'API de recherche, vous devez activer la réponse JSON dans les paramètres généraux du système dans l'interface d'administration.

Paramètres de requête
---------------------

En spécifiant des paramètres de requête comme
``http://<Nom du serveur>/api/v1/documents?q=mot_recherche&num=50&fields.label=fess``,
vous pouvez effectuer des recherches plus avancées.
Les paramètres de requête disponibles sont les suivants :

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - q
     - Mot de recherche. Doit être encodé en URL.
   * - start
     - Position de départ du nombre de résultats. Commence à 0.
   * - num
     - Nombre de résultats à afficher. Par défaut, 20 résultats. Peut afficher jusqu'à 100 résultats.
   * - sort
     - Tri. Utilisé pour trier les résultats de recherche.
   * - fields.label
     - Valeur d'étiquette. Utilisé pour spécifier une étiquette.
   * - facet.field
     - Spécification du champ de facette. (Exemple) ``facet.field=label``
   * - facet.query
     - Spécification de la requête de facette. (Exemple) ``facet.query=timestamp:[now/d-1d TO *]``
   * - facet.size
     - Spécification du nombre maximum de facettes à obtenir. Valide lorsque facet.field est spécifié.
   * - facet.minDocCount
     - Obtient les facettes dont le nombre est supérieur ou égal à cette valeur. Valide lorsque facet.field est spécifié.
   * - geo.location.point
     - Spécification de la latitude et de la longitude. (Exemple) ``geo.location.point=35.0,139.0``
   * - geo.location.distance
     - Spécification de la distance depuis le point central. (Exemple) ``geo.location.distance=10km``
   * - lang
     - Spécification de la langue de recherche. (Exemple) ``lang=en``
   * - preference
     - Chaîne de caractères spécifiant le shard lors de la recherche. (Exemple) ``preference=abc``
   * - callback
     - Nom du callback pour utiliser JSONP. Pas besoin de spécifier si JSONP n'est pas utilisé.

Tableau : Paramètres de requête


Réponse
-------

| Une réponse comme celle-ci est retournée.
| (Formatée pour plus de clarté)

::

    {
      "q": "Fess",
      "query_id": "bd60f9579a494dfd8c03db7c8aa905b0",
      "exec_time": 0.21,
      "query_time": 0,
      "page_size": 20,
      "page_number": 1,
      "record_count": 31625,
      "page_count": 1,
      "highlight_params": "&hq=n2sm&hq=Fess",
      "next_page": true,
      "prev_page": false,
      "start_record_number": 1,
      "end_record_number": 20,
      "page_numbers": [
        "1",
        "2",
        "3",
        "4",
        "5"
      ],
      "partial": false,
      "search_query": "(Fess OR n2sm)",
      "requested_time": 1507822131845,
      "related_query": [
        "aaa"
      ],
      "related_contents": [],
      "data": [
        {
          "filetype": "html",
          "title": "Open Source Enterprise Search Server: Fess — Fess 11.0 documentation",
          "content_title": "Open Source Enterprise Search Server: Fess — Fe...",
          "digest": "Docs » Open Source Enterprise Search Server: Fess Commercial Support Open Source Enterprise Search Server: Fess What is Fess ? Fess is very powerful and easily deployable Enterprise Search Server. ...",
          "host": "fess.codelibs.org",
          "last_modified": "2017-10-09T22:28:56.000Z",
          "content_length": "29624",
          "timestamp": "2017-10-09T22:28:56.000Z",
          "url_link": "https://fess.codelibs.org/",
          "created": "2017-10-10T15.40:48.609Z",
          "site_path": "fess.codelibs.org/",
          "doc_id": "e79fbfdfb09d4bffb58ec230c68f6f7e",
          "url": "https://fess.codelibs.org/",
          "content_description": "Enterprise Search Server: <strong>Fess</strong> Commercial Support Open...Search Server: <strong>Fess</strong> What is <strong>Fess</strong> ? <strong>Fess</strong> is very powerful...You can install and run <strong>Fess</strong> quickly on any platforms...Java runtime environment. <strong>Fess</strong> is provided under Apache...Apache license. Demo <strong>Fess</strong> is OpenSearch-based search",
          "site": "fess.codelibs.org/",
          "boost": "10.0",
          "mimetype": "text/html"
        }
      ]
    }

Les éléments sont les suivants :

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Informations de réponse

   * - q
     - Mot de recherche
   * - exec_time
     - Temps de réponse (en secondes)
   * - query_time
     - Temps de traitement de la requête (en millisecondes)
   * - page_size
     - Nombre de résultats affichés
   * - page_number
     - Numéro de page
   * - record_count
     - Nombre de résultats correspondant au mot de recherche
   * - page_count
     - Nombre de pages de résultats correspondant au mot de recherche
   * - highlight_params
     - Paramètres de surlignage
   * - next_page
     - true : la page suivante existe. false : la page suivante n'existe pas.
   * - prev_page
     - true : la page précédente existe. false : la page précédente n'existe pas.
   * - start_record_number
     - Position de départ du numéro d'enregistrement
   * - end_record_number
     - Position de fin du numéro d'enregistrement
   * - page_numbers
     - Tableau des numéros de page
   * - partial
     - Devient true lorsque les résultats de recherche sont tronqués, par exemple en cas de timeout.
   * - search_query
     - Requête de recherche
   * - requested_time
     - Heure de la requête (en millisecondes epoch)
   * - related_query
     - Requêtes associées
   * - related_contents
     - Requêtes de contenu associé
   * - facet_field
     - Informations sur les documents correspondant au champ de facette donné (uniquement si ``facet.field`` est fourni dans les paramètres de requête)
   * - facet_query
     - Nombre de documents correspondant à la requête de facette donnée (uniquement si ``facet.query`` est fourni dans les paramètres de requête)
   * - result
     - Élément parent des résultats de recherche
   * - filetype
     - Type de fichier
   * - created
     - Date de création du document
   * - title
     - Titre du document
   * - doc_id
     - ID du document
   * - url
     - URL du document
   * - site
     - Nom du site
   * - content_description
     - Description du contenu
   * - host
     - Nom d'hôte
   * - digest
     - Chaîne de résumé du document
   * - boost
     - Valeur de boost du document
   * - mimetype
     - Type MIME
   * - last_modified
     - Date de dernière modification
   * - content_length
     - Taille du document
   * - url_link
     - URL en tant que résultat de recherche
   * - timestamp
     - Date de mise à jour du document


Recherche de tous les documents
================================

Pour rechercher tous les documents cibles, envoyez la requête suivante :
``http://<Nom du serveur>/api/v1/documents/all?q=mot_recherche``

Pour utiliser cette fonctionnalité, vous devez définir api.search.scroll sur true dans fess_config.properties.

Paramètres de requête
---------------------

Les paramètres de requête disponibles sont les suivants :

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - q
     - Mot de recherche. Doit être encodé en URL.
   * - num
     - Nombre de résultats à afficher. Par défaut, 20 résultats. Peut afficher jusqu'à 100 résultats.
   * - sort
     - Tri. Utilisé pour trier les résultats de recherche.

Tableau : Paramètres de requête

Réponse d'erreur
================

Lorsque l'API de recherche échoue, une réponse d'erreur comme celle-ci est retournée.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponse d'erreur

   * - Code de statut
     - Description
   * - 400 Bad Request
     - Lorsque les paramètres de requête sont invalides
   * - 500 Internal Server Error
     - Lorsqu'une erreur interne du serveur s'est produite

Exemple de réponse d'erreur :

::

    {
      "message": "Invalid request parameter",
      "status": 400
    }
