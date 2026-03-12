==========================
Búsqueda por Geolocalización
==========================

Descripción General
===================

|Fess| puede ejecutar búsquedas especificando rangos geográficos en documentos que contienen información de ubicación de latitud y longitud.
Con esta funcionalidad, puede buscar documentos dentro de una cierta distancia desde un punto específico,
o construir un sistema de búsqueda integrado con servicios de mapas como Google Maps.

Casos de Uso
============

La búsqueda por geolocalización se puede utilizar para los siguientes propósitos:

- Búsqueda de tiendas: Buscar tiendas cercanas a la ubicación actual del usuario
- Búsqueda de propiedades: Buscar propiedades dentro de una cierta distancia de una estación o instalación específica
- Búsqueda de eventos: Buscar información de eventos alrededor de una ubicación especificada
- Búsqueda de instalaciones: Búsqueda de proximidad de atracciones turísticas e instalaciones públicas

Métodos de Configuración
=========================

Configuración Durante la Generación del Índice
-----------------------------------------------

Definición del Campo de Ubicación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

En |Fess|, el campo ``location`` está definido por defecto para almacenar información de ubicación.
Este campo está configurado como tipo ``geo_point`` de OpenSearch.

Formato de Registro de Información de Ubicación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Durante la generación del índice, configure la latitud y longitud separadas por comas en el campo ``location``.

**Formato:**

::

    latitud,longitud

**Ejemplo:**

::

    45.17614,-93.87341

.. note::
   La latitud se especifica en el rango de -90 a 90, y la longitud en el rango de -180 a 180.

Ejemplo de Configuración en Rastreo de Almacén de Datos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Al utilizar el rastreo de almacén de datos, configure la latitud y longitud en el campo ``location``
desde una fuente de datos que contiene información de ubicación.

**Ejemplo: Obtención desde Base de Datos**

::

    SELECT
        id,
        name,
        address,
        CONCAT(latitude, ',', longitude) as location
    FROM stores

Adición de Información de Ubicación mediante Script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

También puede agregar dinámicamente información de ubicación a documentos utilizando la funcionalidad de script en la configuración de rastreo.

::

    // Configurar latitud y longitud en el campo location
    doc.location = "35.681236,139.767125";

Configuración Durante la Búsqueda
----------------------------------

Para ejecutar una búsqueda por geolocalización, especifique el punto central y el rango de búsqueda mediante parámetros de solicitud.

Parámetros de Solicitud
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Nombre del Parámetro
     - Descripción
   * - ``geo.location.point``
     - Latitud y longitud del punto central de búsqueda (separadas por comas)
   * - ``geo.location.distance``
     - Radio de búsqueda desde el punto central (con unidad)

Unidades de Distancia
~~~~~~~~~~~~~~~~~~~~~~

Puede utilizar las siguientes unidades para la distancia:

- ``km``: Kilómetros
- ``m``: Metros
- ``mi``: Millas
- ``yd``: Yardas

Ejemplos de Búsqueda
=====================

Búsqueda Básica
---------------

Para buscar documentos dentro de un radio de 10km desde la Estación de Tokio (35.681236, 139.767125):

::

    http://localhost:8080/search?q=palabra_clave&geo.location.point=35.681236,139.767125&geo.location.distance=10km

Búsqueda Alrededor de la Ubicación Actual
------------------------------------------

Para buscar dentro de 1km desde la ubicación actual del usuario:

::

    http://localhost:8080/search?q=ramen&geo.location.point=35.681236,139.767125&geo.location.distance=1km

Ordenamiento por Distancia
---------------------------

Para ordenar los resultados de búsqueda por distancia, utilice el parámetro ``sort``.

::

    http://localhost:8080/search?q=tienda&geo.location.point=35.681236,139.767125&geo.location.distance=5km&sort=location.distance

Uso con API
-----------

La búsqueda por geolocalización también se puede utilizar con la API JSON.

::

    curl -X POST "http://localhost:8080/json/?q=hotel" \
      -H "Content-Type: application/json" \
      -d '{
        "geo.location.point": "35.681236,139.767125",
        "geo.location.distance": "5km"
      }'

Personalización del Nombre del Campo
=====================================

Cambio del Nombre de Campo Predeterminado
------------------------------------------

Para cambiar el nombre del campo utilizado en la búsqueda por geolocalización,
modifique la siguiente configuración en ``fess_config.properties``.

::

    query.geo.fields=location

Para especificar múltiples nombres de campo, sepárelos con comas.

::

    query.geo.fields=location,geo_point,coordinates

Ejemplos de Implementación
===========================

Implementación en Aplicación Web
---------------------------------

Ejemplo de búsqueda obteniendo la ubicación actual con JavaScript:

.. code-block:: javascript

    // Obtener la ubicación actual con la API de Geolocation del navegador
    navigator.geolocation.getCurrentPosition(function(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        const distance = "5km";

        // Construir la URL de búsqueda
        const searchUrl = `/search?q=&geo.location.point=${latitude},${longitude}&geo.location.distance=${distance}`;

        // Ejecutar búsqueda
        window.location.href = searchUrl;
    });

Integración con Google Maps
----------------------------

Ejemplo de visualización de resultados de búsqueda con marcadores en Google Maps:

.. code-block:: javascript

    // Inicializar el mapa
    const map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 35.681236, lng: 139.767125},
        zoom: 13
    });

    // Ejecutar búsqueda por geolocalización con API de Fess
    fetch('/json/?q=tienda&geo.location.point=35.681236,139.767125&geo.location.distance=5km')
        .then(response => response.json())
        .then(data => {
            // Mostrar resultados de búsqueda como marcadores
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

Optimización del Rendimiento
=============================

Optimización de la Configuración del Índice
--------------------------------------------

Al manejar grandes cantidades de datos de ubicación, optimice la configuración del índice.

Verifique la configuración del campo de información de ubicación en ``app/WEB-INF/classes/fess_indices/fess.json``.

::

    "location": {
        "type": "geo_point"
    }

Limitación del Rango de Búsqueda
---------------------------------

Considerando el rendimiento, se recomienda establecer el rango de búsqueda al mínimo necesario.

- Las búsquedas de amplio rango (más de 50km) pueden tomar tiempo de procesamiento
- Configure el rango apropiado según el propósito de uso

Solución de Problemas
======================

La Búsqueda por Geolocalización No Funciona
--------------------------------------------

1. Verifique que los datos estén correctamente almacenados en el campo ``location``.
2. Verifique que el formato de latitud y longitud sea correcto (separado por comas).
3. Verifique que ``location`` esté definido como tipo ``geo_point`` en el mapeo del índice de OpenSearch.

No Se Devuelven Resultados de Búsqueda
---------------------------------------

1. Verifique que existan documentos dentro del rango de distancia especificado.
2. Verifique que los valores de latitud y longitud estén dentro del rango correcto (latitud: -90 a 90, longitud: -180 a 180).
3. Verifique que la unidad de distancia esté especificada correctamente.

La Información de Ubicación No Se Muestra Correctamente
--------------------------------------------------------

1. Verifique que el campo ``location`` esté configurado correctamente durante el rastreo.
2. Verifique que el tipo de dato de latitud y longitud de la fuente de datos sea numérico.
3. Al configurar la información de ubicación mediante script, verifique que el formato de concatenación de cadenas sea correcto.

Información de Referencia
==========================

Para obtener detalles sobre la búsqueda por geolocalización, consulte los siguientes recursos:

- `OpenSearch Geo Queries <https://opensearch.org/docs/latest/query-dsl/geo-and-xy/index/>`_
- `OpenSearch Geo Point <https://opensearch.org/docs/latest/field-types/supported-field-types/geo-point/>`_
- `Geolocation API (MDN) <https://developer.mozilla.org/ja/docs/Web/API/Geolocation_API>`_
