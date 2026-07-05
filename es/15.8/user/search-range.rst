============================
Búsqueda por rango de valores
============================

Cuando se almacenan datos que permiten especificar rangos, como valores numéricos, en un campo, es posible realizar búsquedas por rango en ese campo.

Cómo utilizar
-------------

Para realizar una búsqueda por rango, ingrese "nombre_del_campo:[valor TO valor]" en el formulario de búsqueda.

Por ejemplo, para buscar documentos en el campo content_length con un tamaño entre 1 kbyte y 10 kbytes, ingrese lo siguiente en el formulario de búsqueda:

::

    content_length:[1000 TO 10000]

Para realizar una búsqueda por rango de tiempo, ingrese "last_modified:[fecha_hora1 TO fecha_hora2]" (fecha_hora1 < fecha_hora2) en el formulario de búsqueda.

Las fechas y horas se basan en el estándar ISO 8601.

.. list-table::

   * - Año-mes-día y hora-minuto-segundo y fracción decimal
     - Cuando se basa en la fecha y hora actual
   * - YYYY-MM-DDThh:mm:sssZ (ejemplo: 2012-12-02T10:45:235Z)
     - now (fecha y hora actual), y (año), M (mes), w (semana), d (día), h (hora), m (minuto), s (segundo)

Cuando se basa en now o una hora específica, se pueden agregar símbolos como +, - (suma, resta) y / (redondeo). Sin embargo, cuando se basa en una hora específica, es necesario agregar || entre el símbolo.

/ es un símbolo que redondea a la unidad después de /. now-1d/d representa las 00:00 del día anterior menos 1 día desde las 00:00 del día actual, sin importar a qué hora se ejecute hoy.

Por ejemplo, para buscar documentos actualizados desde hace 30 días hasta el 21 de febrero de 2016 a las 20:00 (asumiendo que es la fecha y hora actual) en el campo last_modified, ingrese lo siguiente en el formulario de búsqueda:

::

    last_modified:[now-30d TO now](=[2016-01-23T00:00:000Z+TO+2016-02-21T20:00:000Z(fecha y hora actual)])
