==============================
Recherche par géolocalisation
==============================

Aperçu
======

|Fess| peut effectuer des recherches avec une zone géographique spécifiée sur des documents contenant des informations de géolocalisation (latitude et longitude).
En utilisant cette fonction, vous pouvez rechercher des documents situés dans une certaine distance d'un point spécifique,
ou créer un système de recherche intégré avec des services de cartographie comme Google Maps.

En interne, |Fess| utilise la requête geo-distance d'OpenSearch pour filtrer les documents
dont les coordonnées se trouvent dans la distance spécifiée à partir d'un point central.

Cas d'utilisation
=================

La recherche par géolocalisation peut être utilisée pour les applications suivantes :

- Recherche de magasins : Rechercher les magasins proches de la position actuelle de l'utilisateur
- Recherche immobilière : Rechercher des propriétés dans une certaine distance d'une gare ou d'une installation spécifique
- Recherche d'événements : Rechercher des informations sur des événements autour d'un lieu spécifié
- Recherche d'installations : Recherche à proximité de sites touristiques ou d'installations publiques

Méthode de configuration
========================

Configuration lors de la génération de l'index
-----------------------------------------------

Définition du champ de géolocalisation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dans |Fess|, le champ ``location`` est défini par défaut pour stocker les informations de géolocalisation.
Ce champ est configuré comme un type ``geo_point`` d'OpenSearch.

Format d'enregistrement des informations de géolocalisation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lors de la génération de l'index, définissez la latitude et la longitude séparées par une virgule dans le champ ``location``.

**Format :**

::

    latitude,longitude

**Exemple :**

::

    45.17614,-93.87341

.. note::
   La latitude doit être spécifiée dans la plage de -90 à 90, et la longitude dans la plage de -180 à 180.

Exemple de configuration pour l'exploration de source de données
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lors de l'utilisation de l'exploration de source de données, définissez la latitude et la longitude dans le champ ``location``
à partir d'une source de données contenant des informations de géolocalisation.

**Exemple : Récupération depuis une base de données**

Si la latitude et la longitude sont stockées dans des colonnes séparées, concaténez-les en une chaîne séparée par une virgule via SQL.

::

    SELECT
        id,
        name,
        address,
        CONCAT(latitude, ',', longitude) AS location
    FROM stores

Dans le script de configuration de la source de données, mappez la valeur récupérée vers le champ ``location``.

::

    location=data.location

Ajout d'informations de géolocalisation via script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Vous pouvez également ajouter dynamiquement des informations de géolocalisation à un document en utilisant la fonctionnalité de script (Groovy) dans la configuration d'exploration.
Assignez directement la valeur au nom du champ.

::

    // Définir la latitude et la longitude dans le champ location
    location="35.681236,139.767125"

Pour plus de détails sur les scripts, consultez :doc:`scripting-groovy`.

Configuration lors de la recherche
-----------------------------------

Pour effectuer une recherche par géolocalisation, spécifiez le point central et le rayon de recherche dans les paramètres de la requête.

Paramètres de requête
~~~~~~~~~~~~~~~~~~~~~

Le nom des paramètres de la recherche par géolocalisation suit le format ``geo.<nom_du_champ>.point`` et ``geo.<nom_du_champ>.distance``.
``<nom_du_champ>`` correspond au nom du champ configuré dans ``query.geo.fields``
(par défaut : ``location``).

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Nom du paramètre
     - Description
   * - ``geo.location.point``
     - Latitude et longitude du point central de recherche (séparées par une virgule. Exemple : ``35.681236,139.767125``)
   * - ``geo.location.distance``
     - Rayon de recherche à partir du point central (avec unité. Exemple : ``10km``)

.. note::
   ``point`` et ``distance`` doivent être spécifiés ensemble. Un ``point`` sans ``distance`` est ignoré.
   De plus, la valeur de ``point`` doit être composée de deux nombres (latitude,longitude) ; un format incorrect
   entraîne une erreur.

.. note::
   Si plusieurs ``point`` sont spécifiés pour le même champ, ils sont traités comme une condition OU (dans l'une des zones).
   Si des ``point`` sont spécifiés pour plusieurs champs distincts, ils sont traités comme une condition ET (dans toutes les zones).

Unités de distance
~~~~~~~~~~~~~~~~~~

Les unités suivantes peuvent être utilisées pour la distance :

- ``km`` : Kilomètres
- ``m`` : Mètres
- ``mi`` : Miles
- ``yd`` : Yards

.. note::
   La valeur de distance est transmise telle quelle à OpenSearch. Vous pouvez donc également utiliser
   toute unité prise en charge par OpenSearch (``cm``, ``mm``, ``ft``, ``in``, ``nmi``, etc.).

Ordre des résultats de recherche
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La recherche par géolocalisation fonctionne comme un **filtre** qui restreint les résultats aux documents situés dans la zone spécifiée.
Elle n'affecte pas le score de pertinence et ne trie pas les résultats par distance croissante par rapport au point central.
Les résultats sont retournés dans l'ordre de pertinence habituel (ou dans l'ordre spécifié par le paramètre ``sort``).

.. note::
   |Fess| ne prend pas en charge le tri par distance (ordre croissant de proximité).
   Si vous souhaitez afficher les résultats par ordre de distance, récupérez les coordonnées de latitude/longitude
   incluses dans la réponse et effectuez le tri côté client.

Exemples de recherche
=====================

Recherche de base
-----------------

Pour rechercher des documents dans un rayon de 10 km autour de la gare de Tokyo (35.681236, 139.767125) :

::

    http://localhost:8080/search?q=mot-clé&geo.location.point=35.681236,139.767125&geo.location.distance=10km

Recherche autour de la position actuelle
-----------------------------------------

Pour rechercher dans un rayon de 1 km autour de la position actuelle de l'utilisateur :

::

    http://localhost:8080/search?q=restaurant&geo.location.point=35.681236,139.767125&geo.location.distance=1km

Utilisation avec l'API
-----------------------

La recherche par géolocalisation peut également être utilisée avec l'API de recherche JSON v2 (``/api/v2/search``).
Spécifiez ``geo.location.point`` et ``geo.location.distance`` en tant que paramètres de requête.

::

    curl "http://localhost:8080/api/v2/search?q=hôtel&geo.location.point=35.681236,139.767125&geo.location.distance=5km"

Les résultats de recherche sont retournés dans le tableau ``response.data`` de l'enveloppe commune. Pour plus de détails sur l'API, consultez :doc:`../api/api-search`
et :doc:`../api/api-overview`.

.. note::
   Le champ ``location`` n'est pas inclus dans la réponse de l'API par défaut. Pour inclure les coordonnées de latitude/longitude
   dans les résultats de recherche, ajoutez le paramètre suivant dans ``fess_config.properties`` :

   ::

       query.additional.api.response.fields=location

Personnalisation du nom de champ
=================================

Modification du nom de champ par défaut
-----------------------------------------

Pour modifier le nom de champ utilisé pour la recherche par géolocalisation,
modifiez le paramètre suivant dans ``fess_config.properties`` :

::

    query.geo.fields=location

Pour spécifier plusieurs noms de champs, séparez-les par des virgules.

::

    query.geo.fields=location,geo_point,coordinates

.. note::
   - Le nom des paramètres de requête est lié au nom du champ configuré. Par exemple,
     si vous définissez ``query.geo.fields=coordinates``, spécifiez ``geo.coordinates.point`` et
     ``geo.coordinates.distance``.
   - Chaque champ spécifié ici doit être défini comme type ``geo_point`` dans le mappage de l'index.

Exemples d'implémentation
==========================

Implémentation dans une application web
-----------------------------------------

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
------------------------------

Exemple d'affichage des résultats de recherche sous forme de marqueurs sur Google Maps :

.. note::
   Cet exemple accède au champ ``location`` dans les résultats de recherche. Assurez-vous de configurer
   ``query.additional.api.response.fields=location`` au préalable pour inclure les coordonnées de latitude/longitude
   dans la réponse.

.. code-block:: javascript

    // Initialisation de la carte
    const map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 35.681236, lng: 139.767125},
        zoom: 13
    });

    // Exécution de la recherche par géolocalisation avec l'API de recherche v2 de Fess
    fetch('/api/v2/search?q=magasin&geo.location.point=35.681236,139.767125&geo.location.distance=5km')
        .then(response => response.json())
        .then(json => {
            // Affichage des résultats de recherche (tableau response.data) sous forme de marqueurs
            json.response.data.forEach(doc => {
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
==============================

Vérification de la configuration de l'index
--------------------------------------------

Le champ de géolocalisation est défini comme type ``geo_point`` dans
``app/WEB-INF/classes/fess_indices/fess/doc.json`` de l'installation.

::

    "location": {
        "type": "geo_point"
    }

Les champs de type ``geo_point`` sont indexés sous forme d'arbre BKD, ce qui permet d'exécuter
les requêtes geo-distance de manière efficace.

Optimisation de la zone de recherche et de la réponse
------------------------------------------------------

Plus le rayon de recherche est grand, plus le nombre de documents correspondants augmente,
ce qui peut allonger le temps de récupération et d'affichage des résultats.

- Définissez un rayon de recherche adapté à votre cas d'utilisation.
- Si vous traitez un grand nombre de résultats (par exemple pour un affichage cartographique),
  limitez le nombre de résultats récupérés en ajustant la taille de page (paramètre ``num``).

Dépannage
==========

La recherche par géolocalisation ne fonctionne pas
----------------------------------------------------

1. Vérifiez que les données sont correctement stockées dans le champ ``location``.
2. Vérifiez que le format de latitude et longitude est correct (deux valeurs séparées par une virgule sous la forme ``latitude,longitude`` ; une erreur est générée si le nombre de valeurs est différent de deux).
3. Vérifiez que ``location`` est défini comme type ``geo_point`` dans le mappage de l'index OpenSearch.
4. Vérifiez que ``point`` et ``distance`` sont tous les deux spécifiés (un ``point`` sans ``distance`` est ignoré).

Aucun résultat de recherche n'est renvoyé
------------------------------------------

1. Vérifiez s'il existe des documents dans la plage de distance spécifiée.
2. Vérifiez que les valeurs de latitude et longitude sont dans les plages correctes (latitude : -90 à 90, longitude : -180 à 180).
3. Vérifiez que l'unité de distance est correctement spécifiée.

Les informations de géolocalisation ne sont pas incluses dans la réponse de l'API
-----------------------------------------------------------------------------------

Le champ ``location`` n'est pas inclus dans la réponse de l'API par défaut.
Pour inclure les coordonnées de latitude/longitude dans les résultats de recherche, ajoutez
``query.additional.api.response.fields=location`` dans ``fess_config.properties``.

Les informations de géolocalisation ne sont pas enregistrées correctement
--------------------------------------------------------------------------

1. Vérifiez que le champ ``location`` est correctement défini lors de l'exploration.
2. Vérifiez que la latitude et la longitude sont correctement récupérées depuis la source de données.
3. Si vous définissez des informations de géolocalisation via un script, vérifiez que le format est une chaîne ``latitude,longitude``.

Informations de référence
==========================

Pour plus de détails sur la recherche par géolocalisation, consultez les ressources suivantes :

- `OpenSearch Geo Queries <https://opensearch.org/docs/latest/query-dsl/geo-and-xy/index/>`_
- `OpenSearch Geo Point <https://opensearch.org/docs/latest/field-types/supported-field-types/geo-point/>`_
- `API de géolocalisation (MDN) <https://developer.mozilla.org/fr/docs/Web/API/Geolocation_API>`_
