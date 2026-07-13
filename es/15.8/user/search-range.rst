=============================
Búsqueda por rango de valores
=============================

Si un campo almacena datos que permiten especificar un rango, como valores numéricos o fechas y horas, es posible realizar una búsqueda por rango en dicho campo.

Cómo utilizar
-------------

Para realizar una búsqueda por rango, introduzca «nombre_de_campo:[valor TO valor]» en el formulario de búsqueda. Para separar el rango se utiliza ``TO`` en mayúsculas.

Por ejemplo, para buscar documentos cuyo campo content_length esté en el rango de 1 kilobyte a 10 kilobytes, introduzca lo siguiente en el formulario de búsqueda:

::

    content_length:[1000 TO 10000]

Los corchetes ``[ ]`` incluyen los límites del rango (mayor o igual / menor o igual), mientras que las llaves ``{ }`` no incluyen los límites del rango (mayor que / menor que). También se pueden combinar ambos. Por ejemplo, ``content_length:{1000 TO 10000]`` representa los documentos con un valor mayor que 1000 y menor o igual que 10000.

Si se establece ``*`` en un lado, se representa un rango abierto especificando solo el límite superior o inferior. ``content_length:[1000 TO *]`` representa 1000 o más, y ``content_length:[* TO 10000]`` representa 10000 o menos.

La búsqueda por rango solo está disponible para los campos registrados como objeto de búsqueda. De forma predeterminada, se puede realizar una búsqueda por rango en campos como content_length, last_modified, timestamp, click_count y favorite_count.

Búsqueda por rango de tiempo
----------------------------

Para realizar una búsqueda por rango de tiempo (fecha y hora), introduzca «last_modified:[fecha_hora1 TO fecha_hora2]» (fecha_hora1 < fecha_hora2) en el formulario de búsqueda. Tenga en cuenta que, si fecha_hora1 es posterior a fecha_hora2, no se produce un error; simplemente el resultado de la búsqueda será de 0 documentos.

La fecha y hora se especifican en formato ISO 8601. El formato es ``YYYY-MM-DDThh:mm:ss.SSSZ``, y todo lo que va después de la hora se puede omitir.

.. list-table::
   :header-rows: 1

   * - Especificación
     - Ejemplo
   * - Solo año, mes y día
     - 2012-12-02
   * - Año, mes, día, hora, minuto y segundo
     - 2012-12-02T10:45:23Z
   * - Año, mes, día, hora, minuto y segundo (hasta milisegundos)
     - 2012-12-02T10:45:23.235Z

Para especificar la fecha y hora, se puede utilizar el cálculo de fecha y hora basado en la fecha y hora actuales. Los símbolos disponibles son los siguientes.

.. list-table::
   :header-rows: 1

   * - Símbolo
     - Significado
   * - ``now``
     - Fecha y hora actuales
   * - ``y`` / ``M`` / ``w`` / ``d`` / ``h`` / ``m`` / ``s``
     - Año / Mes / Semana / Día / Hora / Minuto / Segundo
   * - ``+`` / ``-``
     - Suma / Resta
   * - ``/``
     - Redondeo (redondea a la unidad que sigue a ``/``)

Cuando se toma como referencia now o una fecha y hora, se pueden añadir símbolos como +, - (suma, resta) o / (redondeo). Sin embargo, cuando se toma como referencia una fecha y hora específica en lugar de now, es necesario insertar ``||`` entre la fecha y hora y el símbolo (ejemplo: ``2016-01-01||+1M/d``).

``/`` es un símbolo que redondea a la unidad que sigue a ``/``. ``now-1d/d`` representa las 00:00 del día anterior, es decir, un día menos que las 00:00 de hoy, sin importar a qué hora del día se ejecute.

Tenga en cuenta que estos cálculos de fecha y hora se evalúan en el motor de búsqueda (OpenSearch) y solo son válidos para campos de tipo fecha y hora.

Por ejemplo, para buscar en el campo last_modified los documentos actualizados hasta 30 días antes de la fecha y hora actuales (suponiendo que son las 20:00 del 21 de febrero de 2016), introduzca lo siguiente en el formulario de búsqueda:

::

    last_modified:[now-30d TO now]

Si la fecha y hora actuales son las 20:00 del 21 de febrero de 2016 (UTC), lo anterior corresponde aproximadamente al rango ``[2016-01-22T20:00:00Z TO 2016-02-21T20:00:00Z]``.
