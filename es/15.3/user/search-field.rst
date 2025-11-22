======================================
Búsqueda con especificación de campos
======================================

Búsqueda con especificación de campos
======================================

Los resultados rastreados por |Fess| se almacenan en campos individuales como título y contenido. Puede buscar especificando estos campos. Al especificar campos, puede definir condiciones de búsqueda detalladas, como por tipo de documento o por tamaño.

Campos disponibles
------------------

Por defecto, puede buscar especificando los siguientes campos:

.. list-table::
   :header-rows: 1

   * - Nombre del campo
     - Descripción
   * - url
     - URL rastreada
   * - host
     - Nombre de host incluido en la URL rastreada
   * - title
     - Título
   * - content
     - Contenido
   * - content_length
     - Tamaño del documento rastreado
   * - last_modified
     - Fecha y hora de última modificación del documento rastreado
   * - mimetype
     - Tipo MIME del documento

Tabla: Lista de campos disponibles


Si no se especifica un campo, la búsqueda se realizará en los campos title y content.
También es posible agregar campos y utilizarlos como objetivo de búsqueda.

Cuando los archivos HTML son el objetivo de búsqueda, la etiqueta title se registra en el campo title, y el texto debajo de la etiqueta body se registra en el campo content.

Cómo utilizar
-------------

Para realizar una búsqueda con especificación de campos, ingrese en el formulario de búsqueda "nombre_del_campo:término_de_búsqueda", separando el nombre del campo y el término de búsqueda con dos puntos (:).

Para buscar fess como término de búsqueda en el campo title, ingrese lo siguiente:

::

    title:fess

La búsqueda anterior mostrará documentos que contengan fess en el campo title como resultados de búsqueda.

Para buscar en el campo url, ingrese lo siguiente:

::

   url:https\:\/\/fess.codelibs.org\/ja\/15.3\/*
   url:"https://fess.codelibs.org/ja/15.3/*"

El primero permite usar consultas con comodines, por lo que también se puede escribir como ``url:*\/\/fess.codelibs.org\/*``. Dado que ":" y "/" en la url son palabras reservadas, deben escaparse. El segundo no permite consultas con comodines, pero permite consultas de prefijo.
