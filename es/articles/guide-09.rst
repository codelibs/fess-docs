===============================================
Buscar en documentos en japonés, inglés y chino
===============================================

Introducción
============

Cuando actas de reuniones en japonés, especificaciones técnicas en inglés e informes de mercado en chino conviven en el mismo servidor de archivos o en el mismo sitio de la intranet, pronto surgen comentarios como "los documentos en inglés se encuentran, pero las formas conjugadas del japonés no coinciden", "quiero buscar solo en los documentos en chino" o "quiero encontrar material escrito en inglés usando palabras en japonés".

Fess puede buscar documentos en cualquier idioma sin una configuración especial.
Sin embargo, si añade entradas a los diccionarios sin saber dónde se aplica el análisis de cada idioma, los resultados no cambiarán.
En este artículo se explica, a partir de los valores reales de los archivos de configuración, cómo Fess 15.9 indexa y busca documentos multilingües.
Con esa base, podrá hacer lo siguiente:

- Comprobar el idioma detectado en cada documento y acotar la búsqueda por idioma con ``lang:``
- Decidir, con ``query.default.languages`` y ajustes relacionados, qué análisis de idioma se usa al buscar
- Editar los diccionarios (sinónimos, Kuromoji, palabras vacías, etc.) según los campos en los que actúan, y aplicar los cambios
- Confirmar que un cambio surtió efecto mediante los resultados de búsqueda y la API ``_analyze``

La forma de impulsar mejoras a partir de los registros de búsqueda se trata en :doc:`guide-08`.

Cómo funciona la indexación: campos comunes y campos por idioma
===============================================================

En el índice de Fess, el cuerpo del texto y el título se guardan de dos formas.
Están definidos en ``fess_indices/fess.json`` (analizadores) y ``fess_indices/fess/doc.json`` (mapeo), ambos incluidos con Fess.

.. list-table::
   :header-rows: 1
   :widths: 28 32 40

   * - Campo
     - Analizador
     - Qué hace el análisis
   * - ``content``, ``title``, ``important_content``
     - ``standard_analyzer`` (``standard_search_analyzer`` al buscar)
     - Común a todos los documentos. Los kanji, hiragana, katakana y hangul se dividen en unidades de dos caracteres (bigramas), y se aplican la eliminación de palabras vacías en inglés y la lematización (stemming). Los sinónimos solo se expanden al buscar
   * - ``content_ja``, ``title_ja``, etc.
     - ``japanese_analyzer``
     - Análisis morfológico con Kuromoji. Los verbos y otras palabras se reducen a su forma base, y se eliminan partículas, verbos auxiliares y símbolos
   * - ``content_en``, ``title_en``, etc.
     - ``english_analyzer``
     - Eliminación de palabras vacías en inglés y lematización
   * - ``content_zh-cn``, ``title_zh-cn``, etc.
     - ``simplified_chinese_analyzer``
     - Divide el texto en palabras con un tokenizador para chino
   * - ``content_zh-tw``, ``title_zh-tw``, etc.
     - ``traditional_chinese_analyzer``
     - Convierte el chino tradicional a simplificado y luego lo divide con el mismo tokenizador que el chino simplificado

Todos los documentos tienen los campos comunes.
Los campos por idioma solo se crean cuando se ha determinado el idioma del documento.
Durante la indexación, el código de idioma se guarda en el campo ``lang``, y los valores de ``content``, ``important_content`` y ``title`` (``indexer.language.fields``) se copian en campos ``<campo>_<idioma>`` como ``content_ja``.
Cada documento recibe un único idioma.

Cómo se determina el idioma de un documento
-------------------------------------------

``lang`` se determina en el siguiente orden.

1. Para el HTML de un rastreo web, se usa el valor de ``<html lang="...">`` (``crawler.document.html.lang.xpath=//HTML/@lang``). Si escribe ``field.xpath.default.lang=<XPath>`` en el "Parámetro de configuración" de una configuración de rastreo, cambia el lugar del que se lee el valor solo para esa configuración
2. En los documentos cuyo idioma no se determina en el paso 1, se detecta automáticamente a partir del texto. Se examinan los primeros 1000 caracteres (``indexer.language.detect.length``) de ``content``, ``important_content`` y ``title``, en ese orden. En los rastreos de archivos, la detección se hace solo con el cuerpo de texto extraído
3. Si el idioma detectado no figura en ``supported.languages``, o si no se puede detectar, no se asigna ``lang`` y no se crean campos por idioma

Los valores como ``ja-JP`` o ``zh_CN`` se normalizan a minúsculas con guion (``ja``, ``zh-cn``) al guardarse.

Los documentos de los almacenes de datos también pasan por la misma detección automática al indexarse.
Si un script asigna a ``lang`` un idioma incluido en ``supported.languages`` (por ejemplo, ``ja``), ese valor tiene prioridad sobre la detección automática.

Cómo funciona la búsqueda: qué campos de idioma se consultan
============================================================

Los términos de búsqueda siempre se buscan en los campos comunes.
Además, por cada "idioma de búsqueda" que se determina en cada búsqueda, se añaden a la consulta los campos de ese idioma.
Las condiciones de cada campo se combinan con OR (``should`` de una consulta ``bool``), de modo que un documento aparece en los resultados si coincide en cualquiera de los campos.

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - Campo
     - Clave de configuración
     - Valor predeterminado
   * - ``title``
     - ``query.boost.title``
     - ``0.5``
   * - ``content``
     - ``query.boost.content``
     - ``0.05``
   * - ``title_<idioma de búsqueda>``
     - ``query.boost.title.lang``
     - ``1.0``
   * - ``content_<idioma de búsqueda>``
     - ``query.boost.content.lang``
     - ``0.1``

Los idiomas de búsqueda se toman de la primera de las siguientes fuentes que tenga un valor.

1. ``query.default.languages`` en ``fess_config.properties`` (vacío de forma predeterminada). Si tiene un valor, se ignoran todas las demás indicaciones
2. El parámetro ``lang`` de la solicitud: el idioma elegido en [Opciones] > "Idioma preferido" de la página de búsqueda o en "Idioma preferido" de la búsqueda avanzada, o ``lang`` de ``/api/v2/search``
3. El idioma de la cabecera ``Accept-Language`` que envía el navegador

Por ejemplo, si busca "会議" ("reunión") en un navegador configurado en japonés, el idioma de búsqueda es ``ja`` y, además de ``content``, se consulta ``content_ja``.
Los documentos en inglés no tienen ``content_ja``, por lo que solo coinciden mediante los bigramas de los campos comunes.
A la inversa, cuando un documento en japonés también coincide en ``title_ja`` o ``content_ja``, su puntuación aumenta en esa medida y tiende a aparecer más arriba.
Como Kuromoji reduce las formas conjugadas a su forma base, una búsqueda de "走った" ("corrió") también encuentra, a través de ``content_ja``, documentos en japonés en los que aparece "走る" ("correr").

Por eso, "Idioma preferido" hace subir los documentos de ese idioma; no es un filtro que excluya los documentos de otros idiomas.

Acotar por idioma: la búsqueda ``lang:``
========================================

Para acotar por idioma, indique el campo ``lang`` en la búsqueda.
``lang`` es un campo de tipo keyword en el que se puede buscar, así que no es necesario crear una etiqueta para cada idioma.

::

    lang:en meeting
    lang:ja 会議
    lang:zh-cn 会议
    会議 -lang:ja

El último ejemplo busca "会議" excluyendo los documentos detectados como japonés.
Desde la API, escriba la misma expresión en ``q`` o añada ``fields.lang=en`` (que agrega una condición ``lang:"en"``).

::

    $ curl -s "http://localhost:8080/api/v2/search?q=meeting&fields.lang=en"

Los documentos sin ``lang`` (aquellos cuyo idioma no se pudo detectar) no coinciden con ninguna condición ``lang:``.

Comprobar el idioma detectado
-----------------------------

Antes de cambiar diccionarios o ajustes, compruebe qué idioma se ha asignado a sus documentos.

1. En la página de búsqueda, busque ``lang:ja``, ``lang:en``, ``lang:zh-cn`` y ``lang:zh-tw`` uno por uno y compare el número de resultados. Con la API, el número está en ``response.record_count``

   ::

       $ curl -s "http://localhost:8080/api/v2/search?q=lang:zh-cn&num=1"

2. Para un documento concreto, búsquelo por su URL u otro dato en [Información del sistema] > [Búsqueda] de la consola de administración y ábralo; el valor aparece en el campo ``lang``

Si la detección no es la esperada, compruebe los siguientes puntos.

- El ``<html lang>`` del HTML tiene prioridad sobre la detección automática. Si la plantilla del sitio genera ``lang="en"`` incluso en las páginas en japonés, esas páginas se tratan como inglés
- El chino sin región, como ``<html lang="zh">``, queda como ``zh``. Para ``zh`` no existe un campo por idioma con un analizador de chino, de modo que el análisis del chino se limita a los bigramas de los campos comunes
- Los documentos cortos en japonés con muchos kanji y pocos kana pueden detectarse como ``zh-cn`` o similar

También hay ajustes que tratan todo el HTML, o todos los archivos, como un único idioma.
Si asigna un valor a ``crawler.document.html.default.lang`` y ``crawler.document.file.default.lang``, no se usan ni ``<html lang>`` ni la detección automática, y el idioma queda fijado en ese valor para todos los rastreos de Fess.
En un entorno con documentos en varios idiomas, déjelos vacíos.

Definir los idiomas de búsqueda: ``query.default.languages``
============================================================

De forma predeterminada, el idioma de búsqueda cambia según el idioma del navegador de cada usuario.
Por ejemplo, cuando un empleado con un navegador en inglés busca documentos en japonés, no se usa ``content_ja``, y el orden de los resultados varía de un usuario a otro.
Para evitarlo, fije los idiomas de búsqueda con ``query.default.languages``.

::

    query.default.languages=ja,en,zh-cn,zh-tw

En este ejemplo, los cuatro campos por idioma se añaden a la consulta, sin importar quién busque ni en qué idioma.
Cada documento tiene un solo campo para su propio idioma, de modo que los documentos de todos los idiomas se benefician del análisis por idioma en las mismas condiciones.
A cambio, subir un idioma concreto con "Idioma preferido" deja de tener efecto.
Si la mayoría de sus documentos están en japonés, también puede indicar un solo idioma, como ``query.default.languages=ja``.

Escriba el ajuste en ``fess_config.properties`` y reinicie Fess.
El archivo se encuentra en ``app/WEB-INF/classes/fess_config.properties`` en la versión ZIP y en ``/etc/fess/fess_config.properties`` en las versiones RPM/DEB.
Con Docker, añádalo como opción de la JVM en ``environment`` de ``fess01`` en ``compose.yaml`` y vuelva a crear el contenedor.

::

    - "FESS_JAVA_OPTS=-Dfess.config.query.default.languages=ja,en,zh-cn,zh-tw"

``FESS_JAVA_OPTS`` se divide por espacios, así que no incluya espacios en el valor.
Al volver a crear el contenedor, los ajustes cambiados en [Sistema] > [General] se pierden junto con el ``system.properties`` del contenedor (:doc:`guide-02`).

El peso que se da a las coincidencias en los campos por idioma se ajusta con ``query.boost.title.lang`` y ``query.boost.content.lang``.
Después de cambiarlos, compare el orden de los resultados de búsqueda siguiendo los pasos de "Comprobación" más abajo.

Usar los diccionarios según el idioma
=====================================

Los diccionarios se editan en [Sistema] > [Diccionario].
Cada diccionario actúa sobre campos concretos; si no elige el diccionario que actúa sobre el campo que le interesa, los resultados de búsqueda no cambiarán.

.. list-table::
   :header-rows: 1
   :widths: 24 36 40

   * - Diccionario (archivo)
     - Campos en los que actúa
     - Uso en un entorno multilingüe
   * - Sinónimos (``synonym.txt``)
     - ``content``, ``title`` (solo al buscar)
     - Equivalencias entre idiomas ("会議" y "meeting") y variantes de escritura. No actúa sobre los campos por idioma
   * - Kuromoji (``ja/kuromoji.txt``)
     - Solo campos ``_ja``
     - Hacer que términos internos y nombres de productos se traten como una sola palabra japonesa
   * - Palabras vacías (``ja/stopwords.txt``)
     - Solo campos ``_ja``
     - Palabras que no deben usarse para buscar en documentos en japonés
   * - Palabras vacías (``en/stopwords.txt``)
     - ``content``, ``title`` y campos ``_en``
     - Palabras innecesarias en inglés. Como actúa sobre los campos comunes, afecta a los documentos de todos los idiomas
   * - Protwords (``en/protwords.txt``)
     - ``content``, ``title`` y campos ``_en``
     - Palabras en inglés que no deben lematizarse (nombres de productos, por ejemplo)
   * - Anulación de Stemmer (``en/stemmer_override.txt``)
     - ``content``, ``title`` y campos ``_en``
     - Indicar el resultado de la lematización en inglés
   * - Mapeo (``mapping.txt``)
     - ``content``, ``title``
     - Sustitución de caracteres. ``ja/mapping.txt`` es un archivo aparte para los campos ``_ja``

No existe un diccionario de palabras protegidas (Protwords) para el japonés.
Esto se debe a que ``japanese_analyzer`` no tiene un filtro que lea palabras protegidas.
Los campos de chino simplificado y tradicional no tienen un diccionario de usuario que se pueda editar desde la consola de administración (sus palabras vacías están en ``zh-cn/stopwords.txt`` y ``zh-tw/stopwords.txt``).

Sinónimos entre idiomas
-----------------------

Para encontrar documentos en inglés con palabras en japonés, registre las traducciones como sinónimos.
En el formato del archivo que se sube, se escriben en una línea las palabras de igual significado, separadas por comas.

::

    会議,ミーティング,meeting
    見積,quotation

Los sinónimos se expanden en los campos comunes al buscar, así que no es necesario volver a rastrear.
Para conocer las reglas de registro, como escribir los hiragana en katakana y los caracteres alfanuméricos de ancho completo en ancho medio, consulte `Diccionario de Sinónimos <https://fess.codelibs.org/es/stable/admin/synonym-guide.html>`__.

Diccionario de usuario de Kuromoji
----------------------------------

En el diccionario de Kuromoji se registran un token, sus tokens segmentados, su lectura (en katakana) y su categoría gramatical.
Para que un término interno o un nombre de producto que Kuromoji divide demasiado se trate como una sola palabra, escriba la misma palabra como token y como tokens segmentados.

::

    東京スカイツリー,東京スカイツリー,トウキョウスカイツリー,カスタム名詞

Este diccionario solo actúa sobre los campos ``_ja``.
El campo común ``content`` se divide en bigramas, por lo que cambiar el diccionario de Kuromoji no altera las coincidencias en ``content``.
El efecto solo aparece en las búsquedas cuyos idiomas de búsqueda incluyen ``ja``, y solo sobre los documentos detectados como japonés.

Aplicar los cambios de diccionario
----------------------------------

Guardar un diccionario no basta para cambiar los resultados de búsqueda.

1. Abra [Información del sistema] > [Mantenimiento] y haga clic en [Recargar] en "Recargar índice de documentos". El índice se cierra y se vuelve a abrir, así que mientras tanto las búsquedas devuelven un error o 0 resultados. Hágalo en un horario de poco uso
2. Los sinónimos solo se usan al buscar, de modo que con la recarga ya quedan aplicados
3. Los demás diccionarios (Kuromoji, Mapeo, Palabras vacías, Protwords y Anulación de Stemmer) también cambian el análisis que se hace al construir el índice. Los documentos que ya están en el índice siguen analizados con el diccionario anterior, así que vuelva a rastrear el contenido afectado

Al volver a rastrear, si "Comprobar fecha de última modificación" de [Sistema] > [General] está activado (valor predeterminado), los archivos y páginas que no se han actualizado no se vuelven a obtener.
Desactívelo temporalmente, ejecute el rastreo y vuelva a activarlo cuando termine.

Comprobación
============

Ver la división en tokens con la API ``_analyze``
-------------------------------------------------

La forma más fiable de comprobar si un cambio de diccionario se aplicó es usar la API ``_analyze`` de OpenSearch para pasar la misma cadena por los analizadores del campo común y del campo japonés, y comparar los resultados.
En el entorno Docker de :doc:`guide-02`, se puede acceder a OpenSearch por el puerto 9200 del host.

::

    $ curl -s -X POST "http://localhost:9200/fess.search/_analyze" \
        -H "Content-Type: application/json" \
        -d '{"analyzer":"japanese_analyzer","text":"全文検索エンジンを導入した"}'

    $ curl -s -X POST "http://localhost:9200/fess.search/_analyze" \
        -H "Content-Type: application/json" \
        -d '{"analyzer":"standard_analyzer","text":"全文検索エンジンを導入した"}'

Con ``japanese_analyzer``, el texto se divide en palabras y se eliminan "を" y "た".
Con ``standard_analyzer``, se divide en unidades de dos caracteres como "全文", "文検" y "検索".
Después de registrar "東京スカイツリー" en el diccionario de Kuromoji y recargar, al analizar esta palabra con ``japanese_analyzer`` se devuelve un único token.
Un sinónimo registrado se comprueba analizando "会議" con ``"analyzer":"standard_search_analyzer"`` y verificando que aparece un token generado a partir de "meeting" (lematizado como ``meet``).

Comprobar en los resultados de búsqueda
---------------------------------------

1. En la página de búsqueda, busque una palabra que aparezca tanto en documentos en japonés como en inglés
2. En [Opciones], cambie "Idioma preferido" entre "Japonés" e "Inglés" y compruebe que cambia el idioma de los primeros documentos. Si configuró ``query.default.languages``, compruebe que el orden no cambia al alternar
3. Tras registrar sinónimos de traducción y recargar, compruebe que ``lang:en 会議`` encuentra documentos en inglés
4. Tras cambiar el diccionario de Kuromoji y volver a rastrear, busque la palabra registrada y compruebe que se encuentran los documentos en japonés que la contienen. Que la división en sí ha cambiado se comprueba con ``_analyze``, como se explicó antes

Si los resultados no cambian, compare la columna "Campos en los que actúa" de la tabla de diccionarios con el ``lang`` del documento.
Por ejemplo, añadir a ``en/stopwords.txt`` una palabra japonesa de tres o más caracteres no tiene efecto, porque en los campos comunes el texto se convierte en tokens de dos caracteres y nunca coincide con ella.

Resumen
=======

- Todos los documentos se pueden buscar a través de los campos comunes (``content``, ``title``), que aplican bigramas y lematización en inglés
- El idioma detectado en ``lang`` y los campos por idioma (como ``content_ja``) añaden un análisis adecuado al idioma
- Los idiomas de búsqueda se determinan en el orden ``query.default.languages``, ``lang`` de la solicitud e idioma del navegador, y hacen subir los documentos en lugar de filtrarlos
- Para acotar por idioma, indique el campo ``lang``, como en ``lang:en``
- Edite el diccionario que actúa sobre el campo que le interesa y aplíquelo recargando el índice de documentos y, si es necesario, volviendo a rastrear

Artículos recomendados
======================

- Encontrar puntos de mejora en los registros de búsqueda y corregirlos con sinónimos y coincidencias de clave: :doc:`guide-08`
- Rastrear juntos los sitios web internos y los servidores de archivos: :doc:`guide-04`
- Encontrar documentos de significado similar aunque las palabras clave no coincidan: :doc:`guide-18`
- Llamar a la API de búsqueda desde sistemas empresariales: :doc:`guide-11`

Referencias
===========

- `Diccionario <https://fess.codelibs.org/es/stable/admin/dict-guide.html>`__
- `Diccionario Kuromoji <https://fess.codelibs.org/es/stable/admin/kuromoji-guide.html>`__
- `Diccionario de Sinónimos <https://fess.codelibs.org/es/stable/admin/synonym-guide.html>`__
- `Diccionario de Palabras Vacías <https://fess.codelibs.org/es/stable/admin/stopwords-guide.html>`__
- `Mantenimiento <https://fess.codelibs.org/es/stable/admin/maintenance-guide.html>`__
- `Configuración de Búsqueda Avanzada (Idioma Predeterminado para la Búsqueda) <https://fess.codelibs.org/es/stable/config/search-advanced.html>`__
- `Configuración Avanzada del Rastreador <https://fess.codelibs.org/es/stable/config/crawler-advanced.html>`__
- `Búsqueda por campo <https://fess.codelibs.org/es/stable/user/search-field.html>`__
- `API de búsqueda <https://fess.codelibs.org/es/stable/api/api-search.html>`__
