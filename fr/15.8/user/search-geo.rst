==========================
Recherche géolocalisée
==========================

En ajoutant des informations de géolocalisation (latitude et longitude) à chaque document lors de la génération de l'index, il devient possible de filtrer les résultats de recherche en fonction de la distance par rapport à un point spécifié au moment de la recherche.

Aperçu
----------

La recherche géolocalisée n'inclut dans les résultats de recherche que les documents situés dans un rayon autour d'un point spécifié (latitude et longitude). Ce filtrage est appliqué sous forme de filtre utilisant la requête geo_distance d'OpenSearch, et n'a donc aucun impact sur le score (pertinence). Par ailleurs, le tri par distance n'est pas pris en charge.

Le champ dans lequel sont stockées les informations de géolocalisation doit être défini comme étant de type ``geo_point`` dans le mapping d'OpenSearch. Par défaut, le champ ``location`` est fourni en tant que type ``geo_point``. Cependant, comme aucun traitement n'est fourni par défaut pour stocker une valeur dans le champ ``location``, l'utilisateur doit lui-même y stocker les informations de géolocalisation, par exemple via le mapping de champs du crawl de source de données, un script, ou une API d'enregistrement de documents dans le moteur de recherche.

Utilisation
--------------

La recherche géolocalisée se spécifie en ajoutant les paramètres suivants à la requête de recherche. Par défaut, elle est disponible pour le champ ``location``.

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Description
   * - ``geo.<fieldname>.point``
     - Spécifie la latitude et la longitude du point central au format ``latitude,longitude``. La valeur est exprimée en degrés décimaux (type ``Double``), sous forme de deux nombres séparés par une virgule. Exemple : ``35.681236,139.767125``
   * - ``geo.<fieldname>.distance``
     - Spécifie la distance (rayon) à partir du point central. Exemple : ``10km``

Table : Paramètres de requête

``<fieldname>`` désigne le nom du champ dans lequel sont stockées les informations de géolocalisation. Seuls les champs enregistrés dans ``query.geo.fields`` peuvent être spécifiés ; par défaut, il s'agit de ``location``. Pour utiliser un autre champ, mappez-le en tant que type ``geo_point``, puis ajoutez-le à ``query.geo.fields`` dans ``fess_config.properties``, en séparant les valeurs par des virgules.

Par exemple, pour rechercher les documents situés dans un rayon de 10 km autour du point de latitude 35.681236 et de longitude 139.767125 (à proximité de la gare de Tokyo), ajoutez les paramètres suivants à la requête de recherche.

::

    geo.location.point=35.681236,139.767125&geo.location.distance=10km

Unités de distance
----------------------

La valeur de ``geo.<fieldname>.distance`` est interprétée comme une unité de distance d'OpenSearch. Outre ``km`` (kilomètres), les unités ``mm``, ``cm``, ``m``, ``in``, ``ft``, ``yd``, ``mi`` (miles) et ``nmi`` (milles nautiques), entre autres, peuvent être utilisées. Si l'unité est omise et que seule une valeur numérique est indiquée, elle est traitée comme des mètres (exemple : ``500`` correspond à 500 mètres).

Spécification multiple
---------------------------

* Si plusieurs valeurs de ``geo.<fieldname>.point`` sont spécifiées pour le même champ, les documents situés dans le rayon de l'un des points sont recherchés (condition OR).
* Si des informations de géolocalisation sont spécifiées pour des champs différents, seuls les documents satisfaisant à toutes les conditions sont recherchés (condition AND).

.. note::

   ``geo.<fieldname>.point`` et ``geo.<fieldname>.distance`` doivent tous deux être spécifiés. Si ``distance`` n'est pas spécifié, la condition du ``point`` correspondant est ignorée. Par ailleurs, une erreur se produit si la valeur de ``point`` n'est pas au format ``latitude,longitude`` (deux nombres séparés par une virgule) ou si elle ne peut pas être interprétée comme des nombres.
