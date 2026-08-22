===================
Recherche par plage
===================

Lorsqu'un champ contient des données pour lesquelles une plage peut être spécifiée, telles que des valeurs numériques ou des dates/heures, il est possible d'effectuer une recherche par plage sur ce champ.

Utilisation
-----------

Pour effectuer une recherche par plage, saisissez « nom_champ:[valeur TO valeur] » dans le formulaire de recherche. Le séparateur de plage est ``TO``, à saisir en majuscules (caractères alphanumériques standard).

Par exemple, pour rechercher des documents dont le champ content_length est compris entre 1 Ko et 10 Ko, saisissez ce qui suit dans le formulaire de recherche :

::

    content_length:[1000 TO 10000]

Les crochets ``[ ]`` incluent les bornes de la plage (supérieur ou égal / inférieur ou égal), tandis que les accolades ``{ }`` les excluent (strictement supérieur / strictement inférieur). Il est également possible de combiner les deux. Par exemple, ``content_length:{1000 TO 10000]`` représente les documents dont la valeur est strictement supérieure à 1000 et inférieure ou égale à 10000.

En utilisant ``*`` d'un seul côté, vous obtenez une plage ouverte ne spécifiant que la borne supérieure ou la borne inférieure. ``content_length:[1000 TO *]`` représente les valeurs supérieures ou égales à 1000, et ``content_length:[* TO 10000]`` représente les valeurs inférieures ou égales à 10000.

La recherche par plage n'est valable que pour les champs enregistrés comme cibles de recherche. Par défaut, les champs content_length, last_modified, timestamp, click_count et favorite_count peuvent être utilisés pour une recherche par plage.

Recherche par plage de temps
-----------------------------

Pour effectuer une recherche par plage de temps (date/heure), saisissez « last_modified:[datetime1 TO datetime2] » (datetime1 < datetime2) dans le formulaire de recherche. Notez que si datetime1 est postérieur à datetime2, cela ne provoque pas d'erreur : le résultat de la recherche sera simplement de 0 document.

Les dates/heures doivent être indiquées au format ISO 8601. Le format est ``YYYY-MM-DDThh:mm:ss.SSSZ``, et la partie relative à l'heure peut être omise.

.. list-table::
   :header-rows: 1

   * - Contenu spécifié
     - Exemple
   * - Année, mois, jour uniquement
     - 2012-12-02
   * - Année, mois, jour, heures, minutes, secondes
     - 2012-12-02T10:45:23Z
   * - Année, mois, jour, heures, minutes, secondes (jusqu'aux millisecondes)
     - 2012-12-02T10:45:23.235Z

Pour spécifier une date/heure, vous pouvez utiliser des calculs de date/heure basés sur la date/heure actuelle. Les symboles utilisables sont les suivants :

.. list-table::
   :header-rows: 1

   * - Symbole
     - Signification
   * - ``now``
     - Date/heure actuelle
   * - ``y`` / ``M`` / ``w`` / ``d`` / ``h`` / ``m`` / ``s``
     - Année / mois / semaine / jour / heure / minute / seconde
   * - ``+`` / ``-``
     - Addition / soustraction
   * - ``/``
     - Arrondi (arrondi à l'unité qui suit ``/``)

Lorsque vous utilisez ``now`` ou une date/heure comme référence, vous pouvez ajouter des symboles tels que ``+``, ``-`` (addition, soustraction) ou ``/`` (arrondi). Cependant, si la référence est une date/heure précise plutôt que ``now``, il est nécessaire d'insérer ``||`` entre la date/heure et le symbole (exemple : ``2016-01-01||+1M/d``).

``/`` est le symbole qui permet d'arrondir à l'unité indiquée après ``/``. ``now-1d/d`` représente 00:00 de la veille, c'est-à-dire 00:00 du jour actuel moins 1 jour, quelle que soit l'heure d'exécution de la requête aujourd'hui.

Notez que ces calculs de date/heure sont évalués côté moteur de recherche (OpenSearch) et ne sont valables que pour les champs de type date/heure.

Par exemple, pour rechercher, dans le champ last_modified, les documents mis à jour entre 30 jours avant la date/heure actuelle (supposée être le 21 février 2016 à 20h) et la date/heure actuelle, saisissez ce qui suit dans le formulaire de recherche :

::

    last_modified:[now-30d TO now]

Si la date/heure actuelle est le 21 février 2016 à 20h (UTC), cela correspond approximativement à la plage ``[2016-01-22T20:00:00Z TO 2016-02-21T20:00:00Z]``.
