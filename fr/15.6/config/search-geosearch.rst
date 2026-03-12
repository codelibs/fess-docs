============
Recherche par géolocalisation
============

Aperçu
====

|Fess| peut effectuer des recherches avec une zone géographique spécifiée sur des documents contenant des informations de géolocalisation (latitude et longitude).
En utilisant cette fonction, vous pouvez rechercher des documents situés dans une certaine distance d'un point spécifique,
ou créer un système de recherche intégré avec des services de cartographie comme Google Maps.

Cas d'utilisation
============

La recherche par géolocalisation peut être utilisée pour les applications suivantes :

- Recherche de magasins : Rechercher les magasins proches de la position actuelle de l'utilisateur
- Recherche immobilière : Rechercher des propriétés dans une certaine distance d'une gare ou d'une installation spécifique
- Recherche d'événements : Rechercher des informations sur des événements autour d'un lieu spécifié
- Recherche d'installations : Recherche à proximité de sites touristiques ou d'installations publiques

Méthode de configuration
========

Configuration lors de la génération de l'index
------------------------

Définition du champ de géolocalisation
~~~~~~~~~~~~~~~~~~~~~~~~

Dans |Fess|, le champ ``location`` est défini par défaut pour stocker les informations de géolocalisation.
Ce champ est configuré comme un type ``geo_point`` d'OpenSearch.

Format d'enregistrement des informations de géolocalisation
~~~~~~~~~~~~~~~~~~

Lors de la génération de l'index, définissez la latitude et la longitude séparées par une virgule dans le champ ``location``.

**Format :**

::

    latitude,longitude

**Exemple :**

::

    45.17614,-93.87341

.. note::
   La latitude doit être spécifiée dans la plage de -90 à 90, et la longitude dans la plage de -180 à 180.

Exemple de configuration pour l'exploration de base de données
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lors de l'utilisation de l'exploration de base de données, définissez la latitude et la longitude dans le champ ``location``
à partir d'une source de données contenant des informations de géolocalisation.

**Exemple : Récupération depuis une base de données**

::

    SELECT
        id,
        name,
        address,
        CONCAT(latitude, ',', longitude) as location
    FROM stores

Ajout d'informations de géolocalisation via script
~~~~~~~~~~~~~~~~~~~~~~~~~~

Vous pouvez également ajouter dynamiquement des informations de géolocalisation à un document en utilisant la fonction de script de configuration d'exploration.

::

    // Définir la latitude et la longitude dans le champ location
    doc.location = "35.681236,139.767125";

Configuration lors de la recherche
------------

Pour effectuer une recherche par géolocalisation, spécifiez le point central et la plage de recherche dans les paramètres de requête.

Paramètres de requête
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Nom du paramètre
     - Description
   * - ``geo.location.point``
     - Latitude et longitude du point central de recherche (séparées par une virgule)
   * - ``geo.location.distance``
     - Rayon de recherche à partir du point central (avec unité)

Unités de distance
~~~~~~~~~~

Les unités suivantes peuvent être utilisées pour la distance :

- ``km`` : Kilomètres
- ``m`` : Mètres
- ``mi`` : Miles
- ``yd`` : Yards

Exemples de recherche
======

Recherche de base
------------

Pour rechercher des documents dans un rayon de 10 km autour de la gare de Tokyo (35.681236, 139.767125) :

::

    http://localhost:8080/search?q=mot-clé&geo.location.point=35.681236,139.767125&geo.location.distance=10km

Recherche autour de la position actuelle
----------------

Pour rechercher dans un rayon de 1 km autour de la position actuelle de l'utilisateur :

::

    http://localhost:8080/search?q=ramen&geo.location.point=35.681236,139.767125&geo.location.distance=1km

Tri par distance
----------------

Pour trier les résultats de recherche par ordre de distance, utilisez le paramètre ``sort``.

::

    http://localhost:8080/search?q=magasin&geo.location.point=35.681236,139.767125&geo.location.distance=5km&sort=location.distance

Utilisation avec l'API
-----------

La recherche par géolocalisation peut également être utilisée avec l'API JSON.

::

    curl -X POST "http://localhost:8080/json/?q=hôtel" \
      -H "Content-Type: application/json" \
      -d '{
        "geo.location.point": "35.681236,139.767125",
        "geo.location.distance": "5km"
      }'

Personnalisation du nom de champ
==========================

Modification du nom de champ par défaut
----------------------------

Pour modifier le nom de champ utilisé pour la recherche par géolocalisation,
modifiez le paramètre suivant dans ``fess_config.properties``.

::

    query.geo.fields=location

Pour spécifier plusieurs noms de champs, séparez-les par des virgules.

::

    query.geo.fields=location,geo_point,coordinates

Exemples d'implémentation
======

Implémentation dans une application web
---------------------------

Exemple d'obtention de la position actuelle avec JavaScript pour effectuer une recherche :

.. code-block:: javascript

    // Obtenir la position actuelle avec l'API Geolocation du navigateur
    navigator.geolocation.getCurrentPosition(function(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        const distance = "5km";

        // Construction de l'URL de recherche
        const searchUrl = `/search?q=&geo.location.point=${latitude},${longitude}&geo.location.distance=${distance}`;

        // Exécution de la recherche
        window.location.href = searchUrl;
    });

Intégration avec Google Maps
--------------------

Exemple d'affichage des résultats de recherche sous forme de marqueurs sur Google Maps :

.. code-block:: javascript

    // Initialisation de la carte
    const map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 35.681236, lng: 139.767125},
        zoom: 13
    });

    // Exécution de la recherche par géolocalisation avec l'API Fess
    fetch('/json/?q=magasin&geo.location.point=35.681236,139.767125&geo.location.distance=5km')
        .then(response => response.json())
        .then(data => {
            // Affichage des résultats de recherche sous forme de marqueurs
            data.response.result.forEach(doc => {
                if (doc.location) {
                    const [lat, lng] = doc.location.split(',').map(Number);
                    new google.maps.Marker({
                        position: {lat: lat, lng: lng},
                        map: map,
                        title: doc.title
                    });
                }
            });
        });

Optimisation des performances
====================

Optimisation de la configuration de l'index
------------------------

Lors du traitement de grandes quantités de données de géolocalisation, optimisez la configuration de l'index.

Vérifiez la configuration du champ de géolocalisation dans ``app/WEB-INF/classes/fess_indices/fess.json``.

::

    "location": {
        "type": "geo_point"
    }

Limitation de la zone de recherche
--------------

En tenant compte des performances, il est recommandé de définir la zone de recherche au minimum nécessaire.

- Les recherches sur une large zone (plus de 50 km) peuvent prendre du temps
- Définissez une zone appropriée en fonction de votre utilisation

Dépannage
======================

La recherche par géolocalisation ne fonctionne pas
------------------------

1. Vérifiez que les données sont correctement stockées dans le champ ``location``.
2. Vérifiez que le format de latitude et longitude est correct (séparé par une virgule).
3. Vérifiez que ``location`` est défini comme type ``geo_point`` dans le mappage de l'index OpenSearch.

Aucun résultat de recherche n'est renvoyé
----------------------

1. Vérifiez s'il existe des documents dans la plage de distance spécifiée.
2. Vérifiez que les valeurs de latitude et longitude sont dans les plages correctes (latitude : -90 à 90, longitude : -180 à 180).
3. Vérifiez que l'unité de distance est correctement spécifiée.

Les informations de géolocalisation ne s'affichent pas correctement
----------------------------

1. Vérifiez que le champ ``location`` est correctement défini lors de l'exploration.
2. Vérifiez que le type de données de latitude et longitude dans la source de données est numérique.
3. Si vous définissez des informations de géolocalisation via un script, vérifiez que le format de concaténation de chaînes est correct.

Informations de référence
========

Pour plus de détails sur la recherche par géolocalisation, consultez les ressources suivantes :

- `OpenSearch Geo Queries <https://opensearch.org/docs/latest/query-dsl/geo-and-xy/index/>`_
- `OpenSearch Geo Point <https://opensearch.org/docs/latest/field-types/supported-field-types/geo-point/>`_
- `API de géolocalisation (MDN) <https://developer.mozilla.org/ja/docs/Web/API/Geolocation_API>`_
