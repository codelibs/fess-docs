=======================
Recherche par plage
=======================

Lorsque des données permettant une spécification de plage, telles que des valeurs numériques, sont stockées dans un champ, il est possible d'effectuer une recherche par plage sur ce champ.

Utilisation
-----------

Pour effectuer une recherche par plage, saisissez « nom_champ:[valeur TO valeur] » dans le formulaire de recherche.

Par exemple, pour rechercher des documents dont le champ content_length se situe entre 1 ko et 10 ko, saisissez ce qui suit dans le formulaire de recherche :

::

    content_length:[1000 TO 10000]

Pour effectuer une recherche par plage de temps, saisissez « last_modified:[datetime1 TO datetime2] » (datetime1 < datetime2) dans le formulaire de recherche.

La notation des dates/heures est basée sur la norme ISO 8601.

.. list-table::

   * - Année, mois, jour et heures, minutes, secondes et fractions
     - En utilisant la date/heure actuelle comme référence
   * - AAAA-MM-JJThh:mm:sssZ (exemple : 2012-12-02T10:45:235Z)
     - now (date/heure actuelle), y (année), M (mois), w (semaine), d (jour), h (heure), m (minute), s (seconde)

Lors de l'utilisation de now ou d'une heure comme référence, vous pouvez utiliser les symboles +, - (addition, soustraction) et / (arrondi). Cependant, lors de l'utilisation d'une heure comme référence, il est nécessaire d'insérer || entre le symbole.

Le symbole / arrondit à l'unité qui suit /. now-1d/d représente 00:00 de la veille, quelle que soit l'heure d'exécution du jour même, en soustrayant -1 jour à partir de 00:00 du jour actuel.

Par exemple, pour rechercher des documents mis à jour dans les 30 derniers jours à partir du 21 février 2016 à 20h (heure actuelle), saisissez ce qui suit dans le formulaire de recherche :

::

    last_modified:[now-30d TO now](=[2016-01-23T00:00:000Z+TO+2016-02-21T20:00:000Z(datetime actuelle)])
