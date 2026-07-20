==========================
Funcionalidad de búsqueda
==========================

Resumen
=======

|Fess| proporciona una potente funcionalidad de búsqueda de texto completo.
Esta sección explica la configuración detallada y los métodos de uso de la funcionalidad de búsqueda.

Visualización del número de resultados de búsqueda
===================================================

Comportamiento predeterminado
------------------------------

El valor predeterminado de ``query.track.total.hits`` es ``10000``.
Por ello, cuando los resultados de búsqueda superan los 10,000 elementos, la pantalla de resultados muestra "Aproximadamente 10,000 o más resultados".
Esta es la configuración predeterminada que limita a ``query.track.total.hits`` el umbral hasta el que OpenSearch cuenta el total exacto de coincidencias, con el fin de reducir el impacto en el rendimiento en búsquedas de gran escala.

Ejemplo de búsqueda

|image0|

.. |image0| image:: ../../../resources/images/es/15.8/config/search-result.png

Visualización del número exacto de coincidencias
-------------------------------------------------

Para mostrar el número exacto de coincidencias hasta un valor superior, cambie el valor de ``query.track.total.hits`` en ``fess_config.properties``.

::

    query.track.total.hits=100000

Con el ejemplo anterior se pueden obtener hasta 100,000 coincidencias exactas.
El umbral a partir del cual la visualización pasa a mostrar "Aproximadamente N o más" también cambia de forma acorde al valor configurado.
Sin embargo, configurar un valor demasiado grande puede afectar al rendimiento.

.. warning::
   Si el valor es demasiado grande, el rendimiento de búsqueda puede verse afectado.
   Configure un valor apropiado según su situación de uso real.

Opciones de búsqueda
=====================

Búsqueda básica
---------------

En |Fess|, simplemente ingrese palabras clave en el cuadro de búsqueda para ejecutar una búsqueda de texto completo.
Si ingresa múltiples palabras clave, se ejecutará una búsqueda AND.

::

    búsqueda motor

En el ejemplo anterior, se buscan documentos que contienen tanto "búsqueda" como "motor".

Búsqueda OR
-----------

Para ejecutar una búsqueda OR, inserte ``OR`` entre las palabras clave.

::

    búsqueda OR motor

Búsqueda NOT
------------

Para excluir una palabra clave específica, agregue un signo ``-`` (menos) antes de la palabra clave.

::

    búsqueda -motor

Búsqueda de frases
------------------

Para buscar una frase de coincidencia exacta, enciérrela entre comillas dobles.

::

    "motor de búsqueda"

Búsqueda con especificación de campos
--------------------------------------

Puede realizar búsquedas especificando campos específicos.

::

    title:motor de búsqueda
    url:https://fess.codelibs.org/

Campos principales:

- ``title``: Título del documento
- ``content``: Cuerpo del documento
- ``url``: URL del documento
- ``filetype``: Tipo de archivo (ejemplo: pdf, html, doc)
- ``label``: Etiqueta (clasificación)
- ``mimetype``: Tipo MIME (ejemplo: text/html, application/pdf)
- ``filename``: Nombre de archivo
- ``host``: Nombre de host
- ``site``: Sitio (combinación de nombre de host y ruta)
- ``lang``: Idioma

Los campos de búsqueda adicionales se pueden añadir mediante ``query.additional.search.fields`` en ``fess_config.properties``.

Búsqueda con comodines
----------------------

Es posible realizar búsquedas utilizando comodines.

- ``*``: Cualquier cadena de 0 o más caracteres
- ``?``: Cualquier carácter único

::

    búsqueda*
    b?squeda

Búsqueda difusa
---------------

Puede utilizar la búsqueda difusa que admite errores ortográficos y variaciones de notación.
De forma predeterminada, para palabras clave de 4 o más caracteres, se ejecuta una consulta de búsqueda difusa adicional junto con la búsqueda normal.

::

    motor de búsqueda~

Puede especificar la distancia de edición agregando un número después de ``~``.

Ordenamiento de resultados de búsqueda
=======================================

Por defecto, los resultados de búsqueda se ordenan por relevancia.
Puede especificar los siguientes criterios de ordenamiento en la configuración de la pantalla de administración o mediante parámetros de API.

- Por relevancia (``score``, predeterminado)
- Por fecha de actualización (``last_modified``)
- Por fecha de creación (``created``)
- Por tamaño de archivo (``content_length``)
- Por nombre de archivo (``filename``)
- Por número de clics (``click_count``)
- Por número de favoritos (``favorite_count``)

Los campos de ordenamiento adicionales se pueden añadir mediante ``query.additional.sort.fields`` en ``fess_config.properties``.

Búsqueda por facetas
====================

La búsqueda por facetas le permite refinar los resultados de búsqueda por categoría.
De forma predeterminada, el campo de etiqueta (label) está configurado como faceta.

Puede refinar los resultados de búsqueda haciendo clic en las facetas mostradas en el lado izquierdo de la pantalla de búsqueda.

Resaltado de resultados de búsqueda
====================================

Las palabras clave de búsqueda se resaltan en el título y la sección de resumen de los resultados de búsqueda.
La configuración de resaltado se puede personalizar en ``fess_config.properties``.

::

    query.highlight.tag.pre=<strong>
    query.highlight.tag.post=</strong>
    query.highlight.fragment.size=60
    query.highlight.number.of.fragments=2

- ``query.highlight.tag.pre`` / ``query.highlight.tag.post``: Etiquetas que rodean las secciones resaltadas (predeterminado: ``<strong>`` / ``</strong>``)
- ``query.highlight.fragment.size``: Número de caracteres de cada fragmento resaltado (predeterminado: ``60``)
- ``query.highlight.number.of.fragments``: Número máximo de fragmentos a mostrar (predeterminado: ``2``)

Los campos que se utilizan como objetivo del resaltado en el resumen (snippet) se especifican mediante ``query.highlight.content.description.fields`` (predeterminado: ``hl_content,digest``).

Función de sugerencias
=======================

Cuando ingresa texto en el cuadro de búsqueda, se muestran sugerencias (autocompletado).
Las sugerencias se generan en base a palabras clave de búsquedas anteriores y palabras clave de búsqueda populares.

La función de sugerencias se puede habilitar/deshabilitar en la configuración "General" de la pantalla de administración.

Registros de búsqueda
======================

|Fess| registra todas las consultas de búsqueda y los registros de clics.
Estos registros se pueden utilizar para los siguientes propósitos:

- Análisis y mejora de la calidad de búsqueda
- Análisis del comportamiento del usuario
- Identificación de palabras clave de búsqueda populares
- Identificación de palabras clave con cero resultados de búsqueda

Los registros de búsqueda y de clics se almacenan en los índices de OpenSearch con el prefijo ``fess_log``
(las consultas de búsqueda en el índice ``fess_log.search_log`` y los registros de clics en ``fess_log.click_log``).
Estos registros se pueden visualizar y analizar con OpenSearch Dashboards.
|Fess| incluye un archivo de definición de dashboard para su visualización. Para más detalles, consulte :doc:`admin-opensearch-dashboards`.

Ajuste de rendimiento
======================

Configuración del tiempo de espera de búsqueda
-----------------------------------------------

Puede configurar el tiempo de espera para las búsquedas. El valor predeterminado es 10 segundos.

::

    query.timeout=10000

Número máximo de caracteres de consulta de búsqueda
----------------------------------------------------

Por razones de seguridad y rendimiento, puede limitar el número máximo de caracteres de la consulta de búsqueda.

::

    query.max.length=1000

Uso de caché
------------

|Fess| en sí no dispone de funcionalidad para almacenar en caché los resultados de búsqueda (respuestas de búsqueda).
No obstante, el backend OpenSearch proporciona a nivel de motor una caché de solicitudes de shard y una caché de consultas, lo que contribuye a reducir el tiempo de respuesta para búsquedas con las mismas condiciones.
Dado que estas son funciones propias de OpenSearch, ajústelas en la configuración de OpenSearch según sea necesario.

Solución de problemas
======================

No se muestran resultados de búsqueda
--------------------------------------

1. Verifique que el índice se haya creado correctamente.
2. Verifique que el rastreo se haya completado correctamente.
3. Verifique que el filtrado de búsqueda basado en roles y permisos no esté excluyendo los documentos objetivo para el usuario actual (incluidos los usuarios invitados).
4. Verifique que OpenSearch esté funcionando correctamente.

La búsqueda es lenta
--------------------

1. Verifique el tamaño de la memoria heap de OpenSearch.
2. Optimice el número de fragmentos (shards) y réplicas del índice.
3. Verifique la complejidad de la consulta de búsqueda.
4. Verifique los recursos de hardware (CPU, memoria, E/S de disco).

Se muestran resultados de baja relevancia
------------------------------------------

1. Ajuste la configuración de impulso (boost) (``query.boost.title``, ``query.boost.content``, etc.).
2. Revise la configuración de búsqueda difusa.
3. Verifique la configuración del analizador (Analyzer).
4. Si es necesario, consulte con el soporte comercial.
5. También puede mejorar la precisión de búsqueda utilizando Rank Fusion. Consulte :doc:`rank-fusion` para más detalles.
