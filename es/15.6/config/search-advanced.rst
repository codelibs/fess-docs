====================================
Configuración de Búsqueda Avanzada
====================================

Las configuraciones descritas a continuación se especifican en fess_config.properties.
Es necesario reiniciar |Fess| después de realizar los cambios.

Búsqueda Difusa
===============

La búsqueda difusa se aplica a términos de 4 caracteres o más, encontrando coincidencias con una diferencia de 1 carácter.
Para desactivar esta configuración, especifique `-1`.
::

    query.boost.fuzzy.min.length=-1

Tiempo de Espera en Búsqueda
=============================

Puede especificar el valor de tiempo de espera para las búsquedas.
El valor predeterminado es 10 segundos.
::

    query.timeout=10000

Longitud Máxima de Consulta
============================

Puede especificar la longitud máxima de caracteres para las búsquedas.
El valor predeterminado es 1000 caracteres.
::

    query.max.length=1000

Registro de Tiempos de Espera en Búsqueda
==========================================

Esta es la configuración de registro para cuando se excede el tiempo de espera durante las búsquedas.
El valor predeterminado es `true (activado)`.
::

    query.timeout.logging=true

Visualización del Número de Resultados
=======================================

Especifique esta configuración cuando necesite mostrar más de 10,000 resultados.
De forma predeterminada, cuando hay más de 10,000 resultados, se muestra de la siguiente manera:

`Resultados de búsqueda de xxxxx: aproximadamente 10,000 o más resultados, mostrando 1 - 10 (4.94 segundos)`

::

    query.track.total.hits=10000

Nombre del Índice para Búsqueda Geoespacial
============================================

Especifica el nombre del índice para búsquedas geoespaciales.
El valor predeterminado es `location`.
::

    query.geo.fields=location

Especificación de Idioma en Parámetros de Solicitud
====================================================

Especifica el nombre del parámetro para especificar el idioma en los parámetros de solicitud.
Por ejemplo, si pasa `browser_lang=en` como parámetro de solicitud en la URL, el idioma de visualización de la interfaz cambiará a inglés.
::

    query.browser.lang.parameter.name=browser_lang

Especificación de Búsqueda por Prefijo
=======================================

Cuando se especifica `~\*` en una búsqueda de coincidencia exacta, se realiza como una búsqueda por prefijo.
El valor predeterminado es `true (activado)`.
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

Nombres de Campo Adicionales en Respuesta
==========================================

Especifica los nombres de campo adicionales en la respuesta para búsquedas normales o búsquedas API.
::

    query.additional.response.fields=
    query.additional.api.response.fields=

Adición de Nombres de Campo
============================

Especifique al agregar nombres de campo de búsqueda o nombres de campo de facetas.
::

    query.additional.search.fields=
    query.additional.facet.fields=

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
