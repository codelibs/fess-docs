==================================
Conector de Wikipedia
==================================

Visión General
==============

El conector de Wikipedia proporciona funcionalidad para leer un archivo de volcado de Wikipedia
y registrar sus páginas en el índice de |Fess|.
Funciona con los volcados de Wikipedia, de otros proyectos de Wikimedia y de cualquier sitio MediaWiki.

Esta funcionalidad requiere el plugin ``fess-ds-wikipedia``.

Volcados Soportados
===================

El parámetro ``source`` selecciona el formato del volcado.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - ``source``
     - Descripción
   * - ``cirrus``
     - Un volcado del índice de CirrusSearch, que Wikimedia publica para sus wikis en
       ``https://dumps.wikimedia.org/other/cirrus_search_index/``. Contiene el texto que el propio MediaWiki renderizó, con las plantillas expandidas,
       de modo que ningún marcado de wikitexto llega al índice. Es el formato recomendado para Wikipedia y otros wikis de Wikimedia
   * - ``xml``
     - Una exportación XML de MediaWiki (``*-pages-articles.xml.bz2``, o la salida de ``Special:Export`` o ``dumpBackup.php`` de cualquier MediaWiki).
       Contiene wikitexto, que el conector convierte a texto plano (consulte «Texto Plano de los Volcados XML»)
   * - ``auto``
     - El valor predeterminado. Una ubicación que contiene ``cirrus_search_index`` o termina en ``.json.bz2`` o ``.json`` se lee como ``cirrus``; cualquier otra se lee como ``xml``

La compresión de un volcado (como bzip2 o gzip) se detecta a partir de su contenido, y también se puede leer un archivo sin comprimir.

Requisitos Previos
==================

1. Se requiere la instalación del plugin
2. El archivo de volcado debe ser accesible, ya sea como URL HTTP(S) o como ruta en el servidor de |Fess|
3. Tiempo para el rastreo: el volcado de una Wikipedia grande ocupa varios gigabytes. Pruebe primero una configuración con ``limit``

Instalación del Plugin
----------------------

Instale desde "Sistema" -> "Plugins" en la pantalla de administración, o ejecute ``bin/fess-setup install plugin fess-ds-wikipedia``
y reinicie |Fess|.
Consulte :doc:`../../admin/plugin-guide` para más detalles.

Método de Configuración
=======================

Configure desde la pantalla de administración en "Rastreador" -> "Almacén de datos" -> "Nuevo".

Configuración Básica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Elemento
     - Ejemplo
   * - Nombre
     - Japanese Wikipedia
   * - Nombre del manejador
     - WikipediaDataStore
   * - Habilitado
     - Activado

Configuración de Parámetros
---------------------------

::

    url=https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2
    limit=10000

Lista de Parámetros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parámetro
     - Requerido
     - Descripción
   * - ``url``
     - No
     - Ubicación del volcado: una URL HTTP(S), una URL ``file:`` o una ruta local. El valor predeterminado es el volcado de la Wikipedia en inglés
       (``http://download.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2``), por lo que debe especificar este parámetro de forma explícita.
       Para las formas admitidas con ``source=cirrus``, consulte «Volcados de CirrusSearch»
   * - ``source``
     - No
     - ``auto``, ``cirrus`` o ``xml`` (predeterminado: ``auto``)
   * - ``limit``
     - No
     - Detenerse tras este número de páginas. ``0`` significa sin límite (predeterminado: ``0``). Sirve para probar una configuración con pocas páginas
   * - ``user_agent``
     - No
     - Encabezado User-Agent que se envía al descargar el volcado. Si no se especifica, se usa el nombre de User-Agent del rastreador de |Fess|
   * - ``max_digest_length``
     - No
     - Longitud máxima de ``digest``, en caracteres (predeterminado: ``100``)
   * - ``total_entity_size_limit``
     - No
     - Límite superior, en bytes, del tamaño total de las entidades que procesa el analizador XML (predeterminado: ``100000000``). Se aplica solo a ``source=xml``
   * - ``text_extractor``
     - No
     - Cómo se convierte a texto plano el wikitexto de un volcado XML: ``sweble`` (predeterminado) o ``regex``. Consulte «Texto Plano de los Volcados XML»
   * - ``drop_templates``
     - No
     - Nombres de plantillas, separados por comas, cuyo texto se descarta del contenido de un volcado XML, o ``*`` para todas las plantillas
   * - ``keep_templates``
     - No
     - Nombres de plantillas, separados por comas, cuyo texto se conserva aunque ``drop_templates`` las incluya
   * - ``drop_captions``
     - No
     - Descartar los pies de imagen y de galería del contenido de un volcado XML (predeterminado: ``false``)

Volcados de CirrusSearch
~~~~~~~~~~~~~~~~~~~~~~~~

Un volcado de CirrusSearch se publica en fragmentos numerados, como ``jawiki_content-20261004-00000.json.bz2``.
Con ``source=cirrus``, ``url`` admite una lista separada por comas cuyas entradas pueden ser cada una de las siguientes:

- un único archivo (una URL HTTP(S) o una ruta local)
- un directorio local: se leen, en orden de nombre, todos los archivos que contiene cuyo nombre termina en ``.json.bz2`` o ``.json``
- una URL HTTP(S) que termina en ``/``: se obtiene el listado del directorio y se leen, en orden de nombre, todos los archivos cuyo nombre termina en ``.json.bz2`` o ``.json``

Por ejemplo, para leer todos los fragmentos del índice de contenido de la Wikipedia en japonés:

::

    url=https://dumps.wikimedia.org/other/cirrus_search_index/20261004/index_name=jawiki_content/
    source=cirrus

.. note::

   Wikimedia elimina del servidor las fechas antiguas. Busque una fecha existente en el listado de
   ``https://dumps.wikimedia.org/other/cirrus_search_index/`` antes de configurar el rastreo.

Configuración de Script
-----------------------

::

    lang="ja"
    filetype=format
    filename=title
    url="https://ja.wikipedia.org/wiki/" + encodedTitle
    host="ja.wikipedia.org"
    site="ja.wikipedia.org"
    title=title
    content=content
    digest=digest
    anchor=
    content_length=content.length()
    last_modified=timestamp
    timestamp=timestamp

Campos Disponibles
~~~~~~~~~~~~~~~~~~

Desde el script se pueden referenciar los siguientes valores.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripción
   * - ``id``
     - ID de la página
   * - ``title``
     - Título de la página
   * - ``encodedTitle``
     - El título en la forma que se usa en la URL de una página de MediaWiki (los espacios pasan a ser ``_`` y los demás caracteres se codifican con porcentaje)
   * - ``content``
     - Texto plano de la página
   * - ``digest``
     - ``content`` abreviado a ``max_digest_length`` caracteres
   * - ``contentLength``
     - Longitud de ``content``
   * - ``wikitext``
     - Wikitexto de la página, si el volcado lo incluye
   * - ``format``, ``model``
     - Formato y modelo de contenido de la página
   * - ``timestamp``
     - Marca de tiempo de la página
   * - ``ns``
     - Número del espacio de nombres
   * - ``categories``, ``links``
     - Categorías de la página y las páginas a las que enlaza
   * - ``redirect``, ``redirectTitle``
     - Si la página es una redirección, y su destino
   * - ``stub``, ``disambiguation``
     - Si la página es un esbozo, y si es una página de desambiguación
   * - ``lang``, ``host``, ``site``, ``url``
     - Derivados de la ubicación del volcado. Consulte «Valores Derivados de la Ubicación del Volcado»

Con ``source=cirrus``, están disponibles además los siguientes valores:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripción
   * - ``openingText``
     - El texto inicial de la página
   * - ``headings``
     - Encabezados
   * - ``externalLinks``
     - Enlaces externos
   * - ``templates``
     - Plantillas que usa la página
   * - ``redirects``
     - Títulos que redirigen a la página
   * - ``auxiliaryText``
     - Texto auxiliar, como los pies de imagen
   * - ``weightedTags``
     - Etiquetas ponderadas
   * - ``wikibaseItem``
     - ID del elemento de Wikidata
   * - ``incomingLinks``
     - Número de enlaces entrantes
   * - ``popularityScore``
     - Puntuación de popularidad
   * - ``revisionId``
     - ID de la revisión

Valores Derivados de la Ubicación del Volcado
---------------------------------------------

``lang``, ``host``, ``site`` y ``url`` se derivan del nombre del volcado: un nombre como ``jawiki-latest-pages-articles.xml.bz2``
o ``index_name=jawiki_content`` da ``lang`` ``ja``, ``host`` y ``site`` ``ja.wikipedia.org`` y ``url`` ``https://ja.wikipedia.org/wiki/<título codificado>``.
El nombre debe contener el código de idioma seguido inmediatamente de ``wiki`` y después de ``-``, ``_`` o ``.``.
Los proyectos hermanos como Wikiquote (``jawikiquote-...``) no se derivan a propósito, porque un host incorrecto produciría enlaces rotos.

.. warning::

   Cuando el nombre del volcado no coincide, no se establecen ``host``, ``site`` ni ``url``, y ``url`` conserva el valor del parámetro ``url``,
   que es la ubicación del volcado. Si el script usa ``url`` tal cual, todas las páginas obtienen la misma URL y todo el rastreo acaba como un único documento en el índice,
   sin ningún error.
   Con un volcado renombrado u otro proyecto de Wikimedia, construya la URL en el script, como hace el ejemplo anterior, por ejemplo
   ``url="https://ja.wikiquote.org/wiki/" + encodedTitle``.

Texto Plano de los Volcados XML
-------------------------------

Con ``source=xml``, el wikitexto se convierte a texto plano con el analizador de wikitexto Sweble. Los nombres de los espacios de nombres se leen del ``<siteinfo>`` de la exportación,
por lo que las imágenes y las declaraciones de categoría se reconocen en cualquier idioma (``[[ファイル:...]]``, ``[[Kategorie:...]]``) y en wikis con nombres de espacios de nombres propios.
Una página en la que Sweble falla se convierte con expresiones regulares.

``text_extractor=regex`` usa expresiones regulares para todas las páginas. Es varias veces más rápido, pero las plantillas anidadas, las tablas y el marcado de varias líneas permanecen en el texto.

De forma predeterminada, el texto de cada argumento de plantilla (sin los nombres de parámetro) y cada pie de imagen y de galería se conserva en ``content``, para que ese texto pueda encontrarse.
Use ``drop_templates``, ``keep_templates`` y ``drop_captions`` para filtrarlo:

::

    # Descartar el texto de estas plantillas, también cuando están anidadas ("*" descarta todas las plantillas)
    drop_templates=Cite web,Cite news,Use dmy dates
    # Conservar estas plantillas aunque drop_templates las incluya
    # (drop_templates=* con keep_templates=Note,Warning conserva solo esas dos)
    keep_templates=
    # Descartar los pies de imagen y de galería
    drop_captions=false

Los nombres de plantilla se comparan como los resuelve MediaWiki: la primera letra no distingue mayúsculas de minúsculas, ``_`` equivale a un espacio y el prefijo ``Template:`` es opcional.
Las plantillas no se expanden, por lo que una plantilla conservada aporta el texto de sus argumentos, no lo que MediaWiki renderizaría.
Un volcado de CirrusSearch ya contiene el texto renderizado por MediaWiki, por lo que estos parámetros no se aplican a ``source=cirrus``.

Ejemplos de Uso
===============

Wikipedia en japonés desde un volcado de CirrusSearch
-----------------------------------------------------

Parámetros:

::

    url=https://dumps.wikimedia.org/other/cirrus_search_index/20261004/index_name=jawiki_content/
    source=cirrus

Script:

::

    lang="ja"
    filetype=format
    filename=title
    url="https://ja.wikipedia.org/wiki/" + encodedTitle
    host="ja.wikipedia.org"
    site="ja.wikipedia.org"
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=timestamp
    timestamp=timestamp

Wikipedia en japonés desde un volcado XML, sin plantillas de citas
------------------------------------------------------------------

Parámetros:

::

    url=https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2
    source=xml
    drop_templates=Cite web,Cite news
    limit=10000

El script es el mismo que en «Configuración de Script».

Otro proyecto de Wikimedia (Wikiquote)
--------------------------------------

El nombre de volcado ``jawikiquote-...`` no permite derivar ``host`` ni ``url``, así que constrúyalos en el script.

Script:

::

    lang="ja"
    url="https://ja.wikiquote.org/wiki/" + encodedTitle
    host="ja.wikiquote.org"
    site="ja.wikiquote.org"
    title=title
    content=content
    digest=digest
    last_modified=timestamp
    timestamp=timestamp

Solución de Problemas
=====================

Solo se indexa un documento
---------------------------

Consulte «Valores Derivados de la Ubicación del Volcado». Compruebe que el script establece ``url`` para cada página.

El rastreo tarda demasiado
--------------------------

1. Empiece con ``limit`` para confirmar la configuración
2. Use ``source=cirrus``, o ``text_extractor=regex`` con un volcado XML
3. Coloque el volcado en el servidor de |Fess| y especifique una ruta local

El marcado de wikitexto permanece en el contenido
-------------------------------------------------

Use un volcado de CirrusSearch (``source=cirrus``). Con ``source=xml``, ``text_extractor=regex`` deja en el texto las plantillas anidadas, las tablas y el marcado de varias líneas, así que use ``sweble`` (el valor predeterminado).

No se puede leer el volcado
---------------------------

1. Compruebe que la URL o la ruta son correctas (la fecha de un volcado de CirrusSearch puede haberse eliminado del servidor)
2. En una URL de directorio, compruebe que termina en ``/`` y que los archivos que contiene terminan en ``.json.bz2`` o ``.json``
3. Revise el log para ver el error exacto

Información de Referencia
=========================

- :doc:`ds-overview` - Visión general de conectores de almacén de datos
- :doc:`../../admin/dataconfig-guide` - Guía de configuración de almacén de datos
- :doc:`../../admin/plugin-guide` - Guía de gestión de plugins
- `Wikimedia Downloads <https://dumps.wikimedia.org/>`_
- `CirrusSearch index dumps <https://dumps.wikimedia.org/other/cirrus_search_index/>`_
