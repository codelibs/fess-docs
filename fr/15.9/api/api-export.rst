============================================
API d'exportation des résultats de recherche
============================================

Ce document décrit l'API d'exportation v2 de |Fess|, qui télécharge les résultats de recherche sous
forme de fichier CSV ou JSON. Pour l'enveloppe de réponse commune et le modèle d'erreur, voir
:doc:`api-overview`.

L'URL de base est ``http://<Server Name>/api/v2/`` (exemple en environnement local : ``http://localhost:8080/api/v2``).

.. note::

   L'exportation est désactivée par défaut. Pour l'utiliser, définissez ``api.search.export=true``
   dans ``fess_config.properties``. Lorsqu'elle est activée, le thème fourni ``bootstrap`` affiche un
   menu d'exportation (CSV / JSON) à côté du nombre de résultats. ``features.search_export`` de
   ``/api/v2/ui/config`` indique l'état.

Télécharger les résultats de recherche
======================================

Requête
-------

====================  ====================================================
Méthode HTTP          GET
Point de terminaison  ``/api/v2/documents/export``
====================  ====================================================

Renvoie les documents correspondant à la recherche sous forme de téléchargement de fichier
(``Content-Disposition: attachment``, nom ``search_results.csv`` ou ``search_results.json``).

- Le même filtre de rôles que pour ``/api/v2/search`` s'applique. Avec ``login.required=true``, un
  jeton d'accès s'utilise comme avec ``/api/v2/search``.
- Au plus ``api.search.export.max.size`` (par défaut : ``1000``) documents sont exportés. Les
  paramètres de pagination (``start``, ``num``) ne sont pas utilisés.
- Les champs exportés sont ceux de ``api.search.export.fields`` (par défaut :
  ``title,url_link,last_modified,content_length,filetype``) qui peuvent aussi figurer dans les
  réponses de l'API.
- Les requêtes sont limitées à ``api.search.export.rate.limit.per.minute`` (par défaut : ``10`` ;
  ``0`` signifie illimité) par minute, comptées par utilisateur connecté ou, pour un invité, par IP
  cliente. Au-delà, l'endpoint répond ``429`` avec un en-tête ``Retry-After``.
- Une exportation n'est pas enregistrée dans le journal de recherche.

Paramètres de requête
---------------------

Les mêmes paramètres de condition de recherche que pour ``/api/v2/documents/all`` peuvent être
indiqués, comme ``q``, ``ex_q``, ``fields.*``, ``sort`` et ``lang`` (voir :doc:`api-search`). En
plus :

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Paramètres de requête

   * - ``format``
     - Format du fichier : ``csv`` (par défaut) ou ``json``. Toute autre valeur produit ``invalid_request`` (400).

Tableau : Paramètres de requête

Réponse
-------

Le fichier CSV a une ligne d'en-tête avec les noms des champs et est écrit dans l'encodage de
``csv.file.encoding`` (un fichier UTF-8 commence par une marque d'ordre des octets). Une valeur qui
commence par ``=``, ``+``, ``-``, ``@``, une tabulation ou un retour chariot reçoit un ``'`` initial
afin qu'un tableur ne l'exécute pas comme une formule. Un champ à plusieurs valeurs est joint par un
espace.

::

    "title","url_link","last_modified","content_length","filetype"
    "Example","https://example.com/","2025-01-01T00:00:00.000Z","1234","html"

Le fichier JSON a la forme ``{"data":[{...},...]}`` et les champs à plusieurs valeurs restent des
tableaux.

Un échec avant le début du fichier renvoie l'enveloppe d'erreur habituelle. Un échec ultérieur ne
peut pas être signalé dans le fichier : le téléchargement s'arrête prématurément, avec un CSV tronqué
ou un JSON non analysable.

Réponses d'erreur
-----------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur

   * - Code de statut
     - Description
   * - 400 Bad Request
     - Une requête mal formée, un ``format`` autre que ``csv`` / ``json``, ou l'exportation
       désactivée par ``api.search.export=false``.
   * - 401 Unauthorized
     - Lorsqu'une authentification est requise (par exemple, un appelant anonyme avec ``login.required=true``).
   * - 405 Method Not Allowed
     - Lorsque la méthode HTTP n'est pas autorisée.
   * - 429 Too Many Requests
     - Lorsque la limite de requêtes par minute est dépassée.
   * - 500 Internal Server Error
     - Lorsqu'une erreur interne du serveur se produit.

Tableau : Réponses d'erreur
