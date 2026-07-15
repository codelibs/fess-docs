========================
Búsqueda con ordenamiento
========================

Puede ordenar los resultados de búsqueda especificando campos como la fecha de búsqueda.

Campos de ordenamiento
----------------------

Por defecto, puede ordenar especificando los siguientes campos:

.. list-table::
   :header-rows: 1

   * - Nombre del campo
     - Descripción
   * - created
     - Fecha y hora de rastreo
   * - content_length
     - Tamaño del documento rastreado
   * - last_modified
     - Fecha y hora de última modificación del documento rastreado
   * - filename
     - Nombre del archivo
   * - score
     - Valor de puntuación
   * - timestamp
     - Fecha y hora de indexación del documento
   * - click_count
     - Número de clics en el documento
   * - favorite_count
     - Número de veces que el documento se agregó a favoritos

Tabla: Lista de campos de ordenamiento


También puede agregar sus propios campos como objetivos de ordenamiento. Para hacerlo, especifique en ``query.additional.sort.fields`` de ``fess_config.properties`` los nombres de los campos que desea usar como objetivos de ordenamiento, separados por comas (el valor inicial está vacío). Los campos especificados aquí se agregan a los campos estándar mencionados anteriormente y quedan disponibles para el ordenamiento. Tenga en cuenta que el campo que se utilice como objetivo de ordenamiento debe estar registrado previamente en el índice.

Cómo utilizar
-------------

Puede seleccionar condiciones de ordenamiento en el momento de la búsqueda. Las condiciones de ordenamiento se pueden seleccionar en el diálogo de opciones de búsqueda que se muestra al presionar el botón de opciones.

|image0|

Además, para ordenar en el campo de búsqueda, ingrese "sort:nombre_del_campo" separando sort y el nombre del campo con dos puntos (:) en el formulario de búsqueda.

Lo siguiente busca fess como término de búsqueda y ordena el tamaño del documento en orden ascendente:

::

    fess sort:content_length

Para ordenar en orden descendente, agregue ``.desc`` después del nombre del campo.

::

    fess sort:content_length.desc

El sufijo que se puede especificar después del nombre del campo es ``.asc`` (ascendente) o ``.desc`` (descendente); si se omite, se utilizará el orden ascendente.

Para ordenar por múltiples campos, especifíquelos separados por comas como se muestra a continuación. El campo especificado primero tiene prioridad, y los documentos que tengan el mismo valor en ese campo se ordenan a continuación según el siguiente campo.

::

    fess sort:content_length.desc,last_modified

.. note::
   Si especifica un nombre de campo que no está en la lista de campos de ordenamiento, o un orden de ordenamiento distinto de ``asc`` o ``desc``, la búsqueda producirá un error.

.. |image0| image:: ../../../resources/images/en/15.8/user/search-sort-1.png
.. pdf            :width: 300 px
