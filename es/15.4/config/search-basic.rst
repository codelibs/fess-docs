========================
Funcionalidad de búsqueda
========================

Resumen
========

|Fess| proporciona una potente funcionalidad de búsqueda de texto completo.
Esta sección explica la configuración detallada y los métodos de uso de la funcionalidad de búsqueda.

Visualización del número de resultados de búsqueda
===================================================

Comportamiento predeterminado
------------------------------

Cuando los resultados de búsqueda superan los 10,000 elementos, la pantalla de resultados de búsqueda muestra "Aproximadamente 10,000 o más resultados".
Esta es la configuración predeterminada que considera el rendimiento de OpenSearch.

Ejemplo de búsqueda

|image0|

.. |image0| image:: ../../../resources/images/en/15.4/config/search-result.png

Visualización del número exacto de coincidencias
-------------------------------------------------

Para mostrar el número exacto de coincidencias superior a 10,000, cambie la siguiente configuración en ``fess_config.properties``.

::

    query.track.total.hits=100000

Esta configuración permite obtener el número exacto de coincidencias hasta un máximo de 100,000.
Sin embargo, configurar un valor grande puede afectar al rendimiento.

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
De forma predeterminada, la búsqueda difusa se aplica automáticamente a palabras clave de 4 o más caracteres.

::

    motor de búsqueda~

Puede especificar la distancia de edición agregando un número después de ``~``.

Ordenamiento de resultados de búsqueda
=======================================

Por defecto, los resultados de búsqueda se ordenan por relevancia.
Puede especificar los siguientes criterios de ordenamiento en la configuración de la pantalla de administración o mediante parámetros de API.

- Por relevancia (predeterminado)
- Por fecha de actualización
- Por fecha de creación
- Por tamaño de archivo

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

Los registros de búsqueda se almacenan en el índice ``fess_log`` de OpenSearch y
se pueden visualizar y analizar con OpenSearch Dashboards.
Para más detalles, consulte :doc:`admin-opensearch-dashboards`.

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

Al habilitar el caché de resultados de búsqueda, puede reducir el tiempo de respuesta para las mismas consultas de búsqueda.
La configuración de caché debe ajustarse según los requisitos de su sistema.

Solución de problemas
======================

No se muestran resultados de búsqueda
--------------------------------------

1. Verifique que el índice se haya creado correctamente.
2. Verifique que el rastreo se haya completado correctamente.
3. Verifique que no se hayan configurado permisos de acceso en los documentos objetivo de búsqueda.
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
