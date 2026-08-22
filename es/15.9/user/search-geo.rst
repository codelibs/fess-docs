============================
Búsqueda por geolocalización
============================

Al agregar información de latitud y longitud a cada documento durante la generación del índice, es posible filtrar los resultados de búsqueda según la distancia desde un punto especificado en el momento de la búsqueda.

Descripción general
-------------------

La búsqueda por geolocalización incluye en los resultados de búsqueda únicamente los documentos que se encuentran dentro de un radio determinado alrededor de un punto especificado (latitud y longitud). Este filtrado se aplica como un filtro que utiliza la consulta geo_distance de OpenSearch, por lo que no afecta a la puntuación (relevancia). Además, no se admite la ordenación por distancia.

El campo que almacena la información de ubicación debe estar definido como tipo ``geo_point`` en el mapeo de OpenSearch. Por defecto, el campo ``location`` está preparado como tipo ``geo_point``. Sin embargo, dado que no existe de forma estándar un proceso para almacenar valores en el campo ``location``, es necesario que el propio usuario almacene la información de ubicación mediante el mapeo de campos del rastreo de almacenes de datos, scripts, o la API de registro de documentos en el motor de búsqueda, entre otros métodos.

Cómo utilizar
-------------

La búsqueda por geolocalización se especifica agregando los siguientes parámetros a la solicitud de búsqueda. Por defecto, se puede utilizar con el campo ``location``.

.. list-table::
   :header-rows: 1

   * - Parámetro
     - Descripción
   * - ``geo.<fieldname>.point``
     - Especifica la latitud y la longitud del punto central en el formato ``latitud,longitud``. El valor se expresa en grados decimales (tipo Double), con dos números separados por una coma. Ejemplo: ``35.681236,139.767125``
   * - ``geo.<fieldname>.distance``
     - Especifica la distancia (radio) desde el punto central. Ejemplo: ``10km``

Tabla: Parámetros de solicitud

``<fieldname>`` especifica el nombre del campo que almacena la información de ubicación. Solo se pueden especificar los campos registrados en ``query.geo.fields``, que por defecto es ``location``. Para utilizar otros campos, es necesario mapearlos como tipo ``geo_point`` y agregarlos separados por comas en ``query.geo.fields`` dentro de ``fess_config.properties``.

Por ejemplo, para buscar documentos dentro de un radio de 10km desde el punto de latitud 35.681236 y longitud 139.767125 (cerca de la estación de Tokio), se agregan los siguientes parámetros a la solicitud de búsqueda.

::

    geo.location.point=35.681236,139.767125&geo.location.distance=10km

Unidades de distancia
---------------------

El valor de ``geo.<fieldname>.distance`` se interpreta como una unidad de distancia de OpenSearch. Además de ``km`` (kilómetros), se pueden utilizar ``mm``, ``cm``, ``m``, ``in``, ``ft``, ``yd``, ``mi`` (millas), ``nmi`` (millas náuticas), entre otras. Si se omite la unidad y solo se especifica un número, se interpreta como metros (por ejemplo, ``500`` equivale a 500 metros).

Especificación múltiple
-----------------------

* Si se especifican varios valores de ``geo.<fieldname>.point`` para el mismo campo, se buscan los documentos que se encuentren dentro del radio de cualquiera de los puntos (condición OR).
* Si se especifica información de ubicación para diferentes campos, se buscan los documentos que cumplan todas las condiciones (condición AND).

.. note::

   Es necesario especificar tanto ``geo.<fieldname>.point`` como ``geo.<fieldname>.distance``. Si no se especifica ``distance``, la condición de ese ``point`` se ignora. Además, se producirá un error si el valor de ``point`` no tiene el formato ``latitud,longitud`` (dos números separados por una coma) o si no se puede interpretar como números.
