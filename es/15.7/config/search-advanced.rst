====================================
Configuración de Búsqueda Avanzada
====================================

Las configuraciones descritas a continuación se especifican en fess_config.properties.
Es necesario reiniciar |Fess| después de realizar los cambios.

Búsqueda Difusa
===============

La búsqueda difusa se aplica a términos de 4 caracteres o más, encontrando coincidencias con una diferencia de 1 carácter.
Para desactivar esta configuración, especifique ``-1``.
::

    query.boost.fuzzy.min.length=-1

El valor predeterminado es ``4``. Para la configuración detallada de la búsqueda difusa, consulte la sección "Configuración de Relevancia (Boost)" que se describe más adelante.

Tiempo de Espera en Búsqueda
=============================

Puede especificar el valor de tiempo de espera para las búsquedas en milisegundos.
El valor predeterminado es 10 segundos (10000 milisegundos).
::

    query.timeout=10000

Longitud Máxima de Consulta
============================

Puede especificar la longitud máxima de caracteres para las consultas de búsqueda.
Las consultas que superen esta longitud no serán aceptadas.
El valor predeterminado es 1000 caracteres.
::

    query.max.length=1000

Registro de Tiempos de Espera en Búsqueda
==========================================

Esta es la configuración de registro para cuando se excede el tiempo de espera durante las búsquedas.
El valor predeterminado es ``true`` (activado).
::

    query.timeout.logging=true

Visualización del Número de Resultados
=======================================

Especifica el límite superior del número de resultados que se contabilizan con exactitud.
Con el valor predeterminado, cuando hay más de 10.000 resultados, se muestra de la siguiente manera:

``xxxxx の検索結果 約 10,000 件以上 1 - 10 件目 (4.94 秒)``

Especifique un valor mayor cuando sea necesario mostrar el número exacto de resultados que supere los 10.000.
::

    query.track.total.hits=10000

.. note::
   Configurar un valor demasiado grande puede afectar el rendimiento de las búsquedas. Establezca un valor apropiado según el uso previsto.

Desplazamiento Máximo de Resultados de Búsqueda
=================================================

Especifica el límite superior del desplazamiento (posición de inicio de búsqueda) que se puede obtener en los resultados de búsqueda.
Si se especifica un desplazamiento que supere este valor, la búsqueda devolverá un error.
Funciona como valor límite al navegar hasta páginas profundas en la paginación.
El valor predeterminado es 100000.
::

    query.max.search.result.offset=100000

Umbral de Repetición de Búsqueda con OR
=========================================

Cuando el número de resultados de una búsqueda normal es menor o igual al valor aquí especificado, se realiza una nueva búsqueda cambiando el operador a OR.
Esto permite complementar los resultados cuando la búsqueda AND devuelve muy pocos resultados.
El valor predeterminado es ``-1``, lo que significa que esta función está desactivada.
::

    query.orsearch.min.hit.count=-1

Nombre del Campo para Búsqueda Geoespacial
============================================

Especifica el nombre del campo para búsquedas geoespaciales.
Para especificar varios campos, utilice comas como separador.
El valor predeterminado es ``location``.
::

    query.geo.fields=location

Para obtener información sobre cómo usar la búsqueda geoespacial, consulte :doc:`search-geosearch`.

Especificación de Idioma en Parámetros de Solicitud
====================================================

Especifica el nombre del parámetro para especificar el idioma en los parámetros de solicitud.
Por ejemplo, si pasa ``browser_lang=en`` como parámetro de solicitud en la URL, el idioma de visualización de la interfaz cambiará a inglés.
::

    query.browser.lang.parameter.name=browser_lang

Idioma Predeterminado para la Búsqueda
=======================================

Especifica el idioma predeterminado para las búsquedas, separado por comas.
Si se establece un valor, tiene prioridad sobre el idioma indicado en los parámetros de solicitud o en el navegador.
El valor predeterminado está vacío (sin especificar), en cuyo caso se utiliza el idioma del parámetro de solicitud o del navegador.
::

    query.default.languages=

Mapeo de Códigos de Idioma
============================

Especifica el mapeo de normalización de los códigos de idioma utilizados durante las búsquedas.
Convierte los códigos de idioma recibidos del navegador o de la solicitud a los códigos de idioma utilizados internamente por |Fess|.
Normalmente no es necesario modificar esta configuración. El valor predeterminado incluye mapeos para los principales idiomas.
::

    query.language.mapping=\
    ar=ar\n\
    bg=bg\n\
    ...

Especificación de Búsqueda por Prefijo
=======================================

Cuando se añade ``*`` al final de un término de búsqueda (por ejemplo: ``búsqueda*``), ese término se busca como una consulta de prefijo.
El valor predeterminado es ``true`` (activado). Si se especifica ``false``, los términos con ``*`` al final también se buscan tal como están.
::

    query.replace.term.with.prefix.query=true

Caracteres de Resaltado
========================

Las oraciones se dividen utilizando las cadenas de caracteres especificadas aquí para lograr una visualización de resaltado natural.
Las cadenas especificadas se convierten en caracteres Unicode utilizando u como delimitador inicial.
::

    query.highlight.terminal.chars=u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61

El valor predeterminado se establece de la siguiente manera (en formato decodificado):

``! , . ? ։ ؟ ۔ ܀ ܁ ܂ । ၊ ။ ። ፧ ፨ ᙮ ᠃ ᠉ ‼ ‽ ⁇ ⁈ ⁉ 。 ﹒ ﹗ ！ ． ？ ｡``

Fragmentos de Resaltado
========================

Especifica el número de caracteres y el número de fragmentos de resaltado obtenidos de OpenSearch.
::

    query.highlight.fragment.size=60
    query.highlight.number.of.fragments=2

Método de Generación de Resaltado
==================================

Especifica el método de generación de resaltado de OpenSearch.
::

    query.highlight.type=fvh

Etiquetas de Resaltado
======================

Especifica las etiquetas de inicio y fin para el resaltado.
::

    query.highlight.tag.pre=<strong>
    query.highlight.tag.post=</strong>

Valores Pasados al Resaltador de OpenSearch
============================================

Especifica los valores que se pasan al resaltador de OpenSearch.
::

    query.highlight.boundary.chars=u0009u000Au0013u0020
    query.highlight.boundary.max.scan=20
    query.highlight.boundary.scanner=chars
    query.highlight.encoder=default

Configuración Avanzada de Resaltado
=====================================

Configuración para controlar el comportamiento detallado del resaltado.
::

    query.highlight.force.source=false
    query.highlight.fragmenter=span
    query.highlight.fragment.offset=-1
    query.highlight.no.match.size=0
    query.highlight.order=score
    query.highlight.phrase.limit=256
    query.highlight.content.description.fields=hl_content,digest
    query.highlight.boundary.position.detect=true
    query.highlight.text.fragment.type=query
    query.highlight.text.fragment.size=3
    query.highlight.text.fragment.prefix.length=5
    query.highlight.text.fragment.suffix.length=5

Nombres de Campo Adicionales en Respuesta
==========================================

Especifica los nombres de campo adicionales en la respuesta para búsquedas normales o búsquedas API.
Corresponden respectivamente a los resultados de búsqueda normal, búsqueda API (JSON/GSA), búsqueda scroll y visualización de caché.
::

    query.additional.response.fields=
    query.additional.api.response.fields=
    query.additional.scroll.response.fields=
    query.additional.cache.response.fields=

Para obtener más detalles sobre los campos de respuesta de la búsqueda scroll, consulte :doc:`search-scroll`.

Adición de Nombres de Campo
============================

Especifique al agregar nombres de campo de búsqueda, nombres de campo de facetas, nombres de campo de ordenación, entre otros.
::

    query.additional.default.fields=
    query.additional.search.fields=
    query.additional.facet.fields=
    query.additional.sort.fields=
    query.additional.highlighted.fields=
    query.additional.analyzed.fields=
    query.additional.not.analyzed.fields=

El significado de cada configuración es el siguiente:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Configuración
     - Descripción
   * - ``query.additional.default.fields``
     - Agrega campos al conjunto de campos predeterminados en los que se busca cuando la consulta no especifica campo.
   * - ``query.additional.search.fields``
     - Agrega campos a los que se pueden buscar especificando el nombre del campo.
   * - ``query.additional.facet.fields``
     - Agrega campos que se pueden utilizar como facetas.
   * - ``query.additional.sort.fields``
     - Agrega campos que se pueden utilizar como criterio de ordenación.
   * - ``query.additional.highlighted.fields``
     - Agrega campos que serán objeto de resaltado.
   * - ``query.additional.analyzed.fields``
     - Agrega campos que serán tratados como objeto de análisis por el Analyzer.
   * - ``query.additional.not.analyzed.fields``
     - Agrega campos que no serán analizados por el Analyzer.

Agrupación de Documentos Similares (collapse)
==============================================

Configuración de la función collapse que agrupa (colapsa) documentos similares (casi duplicados) mediante el campo ``content_minhash_bits``.
``query.collapse.inner.hits.name`` es el nombre del campo donde se almacenan los documentos similares en los resultados de búsqueda,
``query.collapse.inner.hits.size`` es el número de documentos similares a obtener por grupo (``0`` significa no obtener ninguno),
``query.collapse.inner.hits.sorts`` es el criterio de ordenación al obtener documentos similares,
``query.collapse.max.concurrent.group.results`` es el número máximo de solicitudes simultáneas al obtener grupos.
::

    query.collapse.max.concurrent.group.results=4
    query.collapse.inner.hits.name=similar_docs
    query.collapse.inner.hits.size=0
    query.collapse.inner.hits.sorts=

Preferencia de Búsqueda
=========================

Especifica la preferencia (valor que determina los shards de búsqueda) que se pasa a OpenSearch en las búsquedas API en formato JSON.
Al especificar ``_query``, el valor hash de la consulta de búsqueda se utiliza como preferencia, de modo que la misma consulta se enruta al mismo shard.
El valor predeterminado es ``_query``.
::

    query.json.default.preference=_query

Configuración de Relevancia (Boost)
=====================================

Especifica los valores de boost utilizados para el cálculo de relevancia (puntuación) durante las búsquedas.
Las configuraciones con ``.lang`` son valores de boost para campos específicos de idioma (por ejemplo: ``content_ja``).
::

    query.boost.title=0.5
    query.boost.title.lang=1.0
    query.boost.content=0.05
    query.boost.content.lang=0.1
    query.boost.important_content=-1.0
    query.boost.important_content.lang=-1.0

Los valores de boost y el comportamiento de la búsqueda difusa se especifican a continuación.
``query.boost.fuzzy.min.length`` es el número mínimo de caracteres para aplicar la búsqueda difusa (``-1`` para desactivar).
::

    query.boost.fuzzy.min.length=4
    query.boost.fuzzy.title=0.01
    query.boost.fuzzy.title.fuzziness=AUTO
    query.boost.fuzzy.title.expansions=10
    query.boost.fuzzy.title.prefix_length=0
    query.boost.fuzzy.title.transpositions=true
    query.boost.fuzzy.content=0.005
    query.boost.fuzzy.content.fuzziness=AUTO
    query.boost.fuzzy.content.expansions=10
    query.boost.fuzzy.content.prefix_length=0
    query.boost.fuzzy.content.transpositions=true

Configuración del Tipo de Consulta
====================================

Especifica el tipo de consulta a utilizar durante las búsquedas y su comportamiento detallado.
``query.default.query_type`` es el tipo de consulta estándar a utilizar,
``query.dismax.tie_breaker`` es el valor tie breaker de la consulta dismax,
``query.bool.minimum_should_match`` es el valor minimum_should_match de la consulta bool (sin especificar si está vacío).
::

    query.default.query_type=bool
    query.dismax.tie_breaker=0.1
    query.bool.minimum_should_match=

Configuración Detallada de Búsqueda por Prefijo y Difusa
==========================================================

Especifica el comportamiento detallado de las consultas de prefijo y de las consultas difusas.
::

    query.prefix.expansions=50
    query.prefix.slop=0
    query.fuzzy.prefix_length=0
    query.fuzzy.expansions=50
    query.fuzzy.transpositions=true

Configuración de Facetas
=========================

Especifica el comportamiento predeterminado de la búsqueda por facetas.
``query.facet.fields`` es el campo sobre el que se aplica la faceta,
``query.facet.fields.size`` es el límite superior del número de facetas a obtener,
``query.facet.fields.min_doc_count`` es el número mínimo de documentos para mostrar en la faceta,
``query.facet.fields.sort`` es el orden de clasificación de la faceta,
``query.facet.fields.missing`` es el valor que se asigna a los documentos que no tienen valor.
::

    query.facet.fields=label
    query.facet.fields.size=100
    query.facet.fields.min_doc_count=1
    query.facet.fields.sort=count.desc
    query.facet.fields.missing=

Configuración para Obtener Resultados en Formato XML Compatible con GSA
========================================================================

Se utiliza al obtener resultados de búsqueda en formato XML compatible con GSA.

Especifica los nombres de campo adicionales en la respuesta al usar el formato XML compatible con GSA.
    ::

        query.gsa.response.fields=UE,U,T,RK,S,LANG

Especifica el idioma predeterminado al usar el formato XML compatible con GSA.
    ::

        query.gsa.default.lang=en

Especifica la ordenación predeterminada al usar el formato XML compatible con GSA.
    ::

        query.gsa.default.sort=

Especifica el prefijo de metadatos al usar el formato XML compatible con GSA.
    ::

        query.gsa.meta.prefix=MT_

Especifica el campo charset al usar el formato XML compatible con GSA.
    ::

        query.gsa.index.field.charset=charset

Especifica el campo content_type al usar el formato XML compatible con GSA.
    ::

        query.gsa.index.field.content_type.=content_type

Especifica la preferencia predeterminada al usar el formato XML compatible con GSA.
    ::

        query.gsa.default.preference=_query
