============================
Búsqueda por geolocalización
============================

Al agregar información de latitud y longitud a cada documento durante la generación del índice, es posible realizar búsquedas utilizando información de ubicación geográfica en el momento de la búsqueda.

Cómo utilizar
-------------

Por defecto, están disponibles los siguientes parámetros:

.. list-table::

   * - geo.<fieldname>.point
     - Especifica la latitud y longitud en grados decimales como tipo Double.
   * - geo.<fieldname>.distance
     - Especifica la distancia al documento en kilómetros. Ejemplo: 10km

Tabla: Parámetros de solicitud


