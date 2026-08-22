============================
Búsqueda por Geolocalización
============================

Descripción General
===================

|Fess| puede ejecutar búsquedas especificando rangos geográficos en documentos que contienen información de ubicación de latitud y longitud.
Con esta funcionalidad, puede buscar documentos dentro de una cierta distancia desde un punto específico,
o construir un sistema de búsqueda integrado con servicios de mapas como Google Maps.

Internamente, se utiliza la consulta geo-distance de OpenSearch para filtrar los documentos
que se encuentran dentro de la distancia especificada desde el punto central indicado.

Casos de Uso
============

La búsqueda por geolocalización se puede utilizar para los siguientes propósitos:

- Búsqueda de tiendas: Buscar tiendas cercanas a la ubicación actual del usuario
- Búsqueda de propiedades: Buscar propiedades dentro de una cierta distancia de una estación o instalación específica
- Búsqueda de eventos: Buscar información de eventos alrededor de una ubicación especificada
- Búsqueda de instalaciones: Búsqueda de proximidad de atracciones turísticas e instalaciones públicas

Métodos de Configuración
========================

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

Si la latitud y la longitud se almacenan en columnas separadas, combínelas en una cadena separada por comas mediante SQL.

::

    SELECT
        id,
        name,
        address,
        CONCAT(latitude, ',', longitude) AS location
    FROM stores

En el script de configuración del almacén de datos, mapee el valor obtenido al campo ``location``.

::

    location=data.location

Adición de Información de Ubicación mediante Script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

También puede agregar dinámicamente información de ubicación a documentos utilizando la funcionalidad de script (Groovy) en la configuración de rastreo.
Asigne el valor directamente al nombre del campo.

::

    // Configurar latitud y longitud en el campo location
    location="35.681236,139.767125"

Para más detalles sobre los scripts, consulte :doc:`scripting-groovy`.

Configuración Durante la Búsqueda
----------------------------------

Para ejecutar una búsqueda por geolocalización, especifique el punto central y el rango de búsqueda mediante parámetros de solicitud.

Parámetros de Solicitud
~~~~~~~~~~~~~~~~~~~~~~~~

El nombre de los parámetros de búsqueda por geolocalización sigue el formato ``geo.<nombre_campo>.point``
y ``geo.<nombre_campo>.distance``. En ``<nombre_campo>`` se utiliza el nombre del campo configurado en
``query.geo.fields`` (por defecto, ``location``).

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Nombre del Parámetro
     - Descripción
   * - ``geo.location.point``
     - Latitud y longitud del punto central de búsqueda (separadas por comas; ejemplo: ``35.681236,139.767125``)
   * - ``geo.location.distance``
     - Radio de búsqueda desde el punto central (con unidad; ejemplo: ``10km``)

.. note::
   ``point`` y ``distance`` deben especificarse juntos. Un ``point`` sin ``distance`` será ignorado.
   Además, el valor de ``point`` debe estar compuesto por dos valores numéricos en formato "latitud,longitud";
   si el formato es incorrecto, se producirá un error.

.. note::
   Si se especifican varios ``point`` para el mismo campo, se tratarán como condición OR (dentro de cualquiera de los rangos).
   Si se especifican para campos distintos, se tratarán como condición AND (dentro de todos los rangos).

Unidades de Distancia
~~~~~~~~~~~~~~~~~~~~~~

Puede utilizar las siguientes unidades para la distancia:

- ``km``: Kilómetros
- ``m``: Metros
- ``mi``: Millas
- ``yd``: Yardas

.. note::
   El valor de la distancia se pasa directamente a OpenSearch, por lo que también pueden utilizarse otras unidades
   compatibles con OpenSearch (como ``cm``, ``mm``, ``ft``, ``in``, ``nmi``, entre otras).

Orden de los Resultados de Búsqueda
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La búsqueda por geolocalización actúa como un **filtro** que restringe los resultados a los documentos
dentro del rango especificado. No afecta la puntuación de búsqueda (relevancia) ni ordena los resultados
por proximidad al punto central. Los resultados se devuelven en el orden habitual por relevancia
(o según el orden especificado con el parámetro ``sort``).

.. note::
   |Fess| no admite la ordenación por distancia (ordenar por proximidad).
   Si desea mostrar los resultados ordenados por distancia, utilice las coordenadas incluidas en la respuesta
   para ordenarlos en el lado del cliente.

Ejemplos de Búsqueda
====================

Búsqueda Básica
---------------

Para buscar documentos dentro de un radio de 10km desde la Estación de Tokio (35.681236, 139.767125):

::

    http://localhost:8080/search?q=palabra_clave&geo.location.point=35.681236,139.767125&geo.location.distance=10km

Búsqueda Alrededor de la Ubicación Actual
------------------------------------------

Para buscar dentro de 1km desde la ubicación actual del usuario:

::

    http://localhost:8080/search?q=restaurante&geo.location.point=35.681236,139.767125&geo.location.distance=1km

Uso con API
-----------

La búsqueda por geolocalización también se puede utilizar con la API de búsqueda JSON v2 (``/api/v2/search``).
Especifique ``geo.location.point`` y ``geo.location.distance`` como parámetros de solicitud.

::

    curl "http://localhost:8080/api/v2/search?q=hotel&geo.location.point=35.681236,139.767125&geo.location.distance=5km"

Los resultados de búsqueda se devuelven en el arreglo ``response.data`` del envelope común. Para más detalles sobre la API,
consulte :doc:`../api/api-search` y :doc:`../api/api-overview`.

.. note::
   El campo ``location`` no se incluye en la respuesta de la API de forma predeterminada. Si desea incluir
   las coordenadas en los resultados de búsqueda, agregue la siguiente configuración a ``fess_config.properties``:

   ::

       query.additional.api.response.fields=location

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

.. note::
   - El nombre del parámetro de solicitud está vinculado al nombre del campo configurado. Por ejemplo,
     si configura ``query.geo.fields=coordinates``, deberá especificar ``geo.coordinates.point`` y
     ``geo.coordinates.distance``.
   - Cada campo especificado aquí debe estar definido como tipo ``geo_point`` en el mapeo del índice.

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
-----------------------------

Ejemplo de visualización de resultados de búsqueda con marcadores en Google Maps:

.. note::
   Este ejemplo hace referencia al campo ``location`` de los resultados de búsqueda. Es necesario configurar
   previamente ``query.additional.api.response.fields=location`` para incluir las coordenadas en la respuesta.

.. code-block:: javascript

    // Inicializar el mapa
    const map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 35.681236, lng: 139.767125},
        zoom: 13
    });

    // Ejecutar búsqueda por geolocalización con la API de búsqueda v2 de Fess
    fetch('/api/v2/search?q=tienda&geo.location.point=35.681236,139.767125&geo.location.distance=5km')
        .then(response => response.json())
        .then(json => {
            // Mostrar los resultados (arreglo response.data) como marcadores
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

Optimización del Rendimiento
=============================

Verificación de la Configuración del Índice
--------------------------------------------

El campo de información de ubicación está definido como tipo ``geo_point`` en
``app/WEB-INF/classes/fess_indices/fess/doc.json`` de la instalación.

::

    "location": {
        "type": "geo_point"
    }

Los campos de tipo ``geo_point`` se indexan mediante un árbol BKD, por lo que las consultas
geo-distance se ejecutan de forma eficiente.

Optimización del Rango de Búsqueda y Respuesta
-----------------------------------------------

Al aumentar el radio de búsqueda, aumenta el número de documentos dentro del rango,
lo que puede incrementar el tiempo de recuperación y representación de los resultados.

- Configure un radio de búsqueda apropiado según el propósito de uso.
- Si maneja muchos resultados, como en la visualización de mapas, ajuste el tamaño de página
  (parámetro ``num``) para limitar la cantidad de resultados obtenidos.

Solución de Problemas
======================

La Búsqueda por Geolocalización No Funciona
--------------------------------------------

1. Verifique que los datos estén correctamente almacenados en el campo ``location``.
2. Verifique que el formato de latitud y longitud sea correcto (separado por comas con ``latitud,longitud``; si no hay exactamente dos valores, se producirá un error).
3. Verifique que ``location`` esté definido como tipo ``geo_point`` en el mapeo del índice de OpenSearch.
4. Verifique que se estén especificando tanto ``point`` como ``distance`` (un ``point`` sin ``distance`` será ignorado).

No Se Devuelven Resultados de Búsqueda
---------------------------------------

1. Verifique que existan documentos dentro del rango de distancia especificado.
2. Verifique que los valores de latitud y longitud estén dentro del rango correcto (latitud: -90 a 90, longitud: -180 a 180).
3. Verifique que la unidad de distancia esté especificada correctamente.

La Información de Ubicación No Aparece en la Respuesta de la API
-----------------------------------------------------------------

El campo ``location`` no se incluye en la respuesta de la API de forma predeterminada.
Para incluir las coordenadas en los resultados de búsqueda, configure
``query.additional.api.response.fields=location`` en ``fess_config.properties``.

La Información de Ubicación No Se Registra Correctamente
---------------------------------------------------------

1. Verifique que el campo ``location`` esté configurado correctamente durante el rastreo.
2. Verifique que la latitud y la longitud de la fuente de datos se obtengan correctamente.
3. Al configurar la información de ubicación mediante script, verifique que el formato de cadena sea ``latitud,longitud``.

Información de Referencia
==========================

Para obtener detalles sobre la búsqueda por geolocalización, consulte los siguientes recursos:

- `OpenSearch Geo Queries <https://opensearch.org/docs/latest/query-dsl/geo-and-xy/index/>`_
- `OpenSearch Geo Point <https://opensearch.org/docs/latest/field-types/supported-field-types/geo-point/>`_
- `Geolocation API (MDN) <https://developer.mozilla.org/es/docs/Web/API/Geolocation_API>`_
