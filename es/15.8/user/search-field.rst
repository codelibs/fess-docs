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
     - Tipo de dato
   * - url
     - URL rastreada
     - Palabra clave
   * - host
     - Nombre de host incluido en la URL rastreada
     - Palabra clave
   * - site
     - Cadena de la URL sin el esquema ni la cadena de consulta (nombre de host y ruta). Se busca mediante coincidencia de prefijo
     - Palabra clave
   * - title
     - Título
     - Texto
   * - content
     - Contenido
     - Texto
   * - content_length
     - Tamaño del documento (en bytes)
     - Numérico
   * - last_modified
     - Fecha y hora de la última modificación del documento
     - Fecha y hora
   * - timestamp
     - Fecha y hora de registro del documento (si no se puede obtener la fecha y hora de última modificación, se utiliza la hora de ejecución del rastreo)
     - Fecha y hora
   * - mimetype
     - Tipo MIME del documento (por ejemplo, ``text/html``)
     - Palabra clave
   * - filetype
     - Tipo de archivo determinado a partir del tipo MIME (por ejemplo, ``html``, ``word``, ``pdf``; si no corresponde a ninguno, ``others``)
     - Palabra clave
   * - filename
     - Nombre de archivo al final de la ruta de la URL
     - Palabra clave
   * - label
     - Valor de la etiqueta asignada al documento
     - Palabra clave
   * - lang
     - Código de idioma del documento (por ejemplo, ``ja``, ``en``)
     - Palabra clave
   * - anchor
     - URLs de enlace extraídas de una página HTML (solo en el rastreo web)
     - Palabra clave
   * - click_count
     - Número de clics en el documento
     - Numérico
   * - favorite_count
     - Número de veces que el documento se agregó a favoritos
     - Numérico

Tabla: Lista de campos disponibles

El "tipo de dato" indica la diferencia en el método de búsqueda según cada campo.

* Palabra clave: se realiza una búsqueda de coincidencia exacta sobre el valor completo. También se puede combinar con la búsqueda con comodines o la búsqueda por prefijo.
* Texto: se realiza una búsqueda de texto completo sobre los términos divididos mediante análisis morfológico, entre otros. Corresponde a campos como title y content.
* Numérico y fecha y hora: se puede utilizar la :doc:`Búsqueda por rango de valores <search-range>`.

Si no se especifica ningún campo, la búsqueda se realiza sobre los campos title y content. Según la configuración, también es posible agregar campos adicionales como objetivo de búsqueda.

.. note::
    Según el objetivo del rastreo, hay campos en los que no se registra ningún valor. Por ejemplo, anchor solo se registra durante el rastreo web, y lang solo cuando el HTML tiene un atributo de idioma. Además, también se pueden especificar campos como segment (el ID de sesión que representa la unidad de ejecución del rastreo) o doc_id (el ID interno asignado por el sistema), aunque normalmente no se utilizan en las búsquedas habituales.

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

   url:https\:\/\/fess.codelibs.org\/ja\/15.8\/*
   url:"https://fess.codelibs.org/ja/15.8/*"

El primero permite usar la búsqueda con comodines, por lo que también se puede escribir como ``url:*\/\/fess.codelibs.org\/*``. Dado que los caracteres ":" y "/" que aparecen en la url son caracteres especiales de la consulta de búsqueda, escápelos anteponiendo ``\`` (consulte :doc:`special-char`). El segundo no permite la búsqueda con comodines, pero un término que termine en ``*`` se trata como una búsqueda de prefijo (coincidencia inicial).

.. tip::
    Si desea buscar por una parte de la URL, puede usar ``inurl:`` para realizar una búsqueda de coincidencia parcial sobre la URL. Por ejemplo, ``inurl:15.8`` busca documentos cuya URL contenga ``15.8``.

Al especificar campos cuyo valor contiene "/", como mimetype, filetype o site, enciérrelo entre comillas, como en ``mimetype:"text/html"``, o bien escápelo, como en ``mimetype:text\/html``.

Para conocer la sintaxis de búsqueda relacionada, consulte también :doc:`Búsqueda con comodines <search-wildcard>`, :doc:`Búsqueda por rango de valores <search-range>`, :doc:`Búsqueda con ordenamiento <search-sort>` y :doc:`Caracteres especiales <special-char>`.
