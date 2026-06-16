====================================
Configuración de Rank Fusion
====================================

Descripción general
===================

La función de Rank Fusion de |Fess| integra múltiples resultados de búsqueda para
proporcionar resultados de búsqueda más precisos.

Qué es Rank Fusion
==================

Rank Fusion es una técnica que combina resultados de múltiples algoritmos de búsqueda
o métodos de puntuación para generar un único ranking optimizado.

Principales beneficios:

- Combina las fortalezas de diferentes algoritmos
- Mejora la precisión de búsqueda
- Proporciona resultados de búsqueda diversos

Algoritmos compatibles
======================

|Fess| soporta el algoritmo RRF (Reciprocal Rank Fusion) para Rank Fusion.

RRF (Reciprocal Rank Fusion)
----------------------------

RRF calcula una puntuación sumando el recíproco de la posición de cada documento en cada
resultado de búsqueda. Cuando un documento es recuperado por múltiples buscadores, sus
puntuaciones se suman.

Fórmula::

    score(d) = Σ 1 / (k + rank(d))

- ``k``: Parámetro constante que controla la influencia del rango (valor predeterminado: 20)
- ``rank(d)``: Posición del documento d en cada resultado de búsqueda (base 0)
- ``Σ``: Suma sobre todos los buscadores en los que aparece el documento d

Configuración
=============

fess_config.properties
----------------------

Configuración básica::

    # Tamaño de ventana (número de resultados a fusionar)
    # Nota: Debe ser >= paging.search.page.max.size × 2.
    # Si el valor es inferior a este mínimo, se utiliza automáticamente el mínimo.
    rank.fusion.window_size=200

    # Constante de rango (parámetro k para RRF)
    rank.fusion.rank_constant=20

    # Número de hilos para procesamiento paralelo
    # (si es 0 o menos, se usa availableProcessors × 1.5 + 1)
    rank.fusion.threads=-1

    # Nombre del campo de puntuación (campo que almacena la puntuación fusionada)
    rank.fusion.score_field=rf_score

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Propiedad
     - Predeterminado
     - Descripción
   * - ``rank.fusion.window_size``
     - ``200``
     - Número máximo de resultados recuperados de cada buscador para la fusión. Debe ser >= ``paging.search.page.max.size × 2`` (``200`` de forma predeterminada); si se establece un valor menor, se eleva automáticamente a este mínimo.
   * - ``rank.fusion.rank_constant``
     - ``20``
     - La constante ``k`` en la fórmula RRF. Un valor mayor reduce la diferencia de puntuación entre los resultados con mayor y menor rango.
   * - ``rank.fusion.threads``
     - ``-1``
     - Número de hilos utilizados al ejecutar múltiples buscadores en paralelo. Si se especifica ``0`` o menos, se usa ``availableProcessors × 1.5 + 1`` automáticamente.
   * - ``rank.fusion.score_field``
     - ``rf_score``
     - Nombre del campo del documento de resultados utilizado para almacenar la puntuación fusionada.

Propiedades del sistema JVM
---------------------------

Los buscadores a utilizar se especifican como una propiedad del sistema JVM. Añada lo
siguiente a ``fess.in.sh`` (o ``fess.in.bat``)::

    # Especificar buscadores (separados por comas)
    -Drank.fusion.searchers=default,semantic

Esta propiedad se comporta de la siguiente manera:

- Se establece como opción JVM, no en ``fess_config.properties``.
- ``default`` es el buscador que realiza la búsqueda estándar por palabras clave y siempre está disponible.
- ``semantic`` es el buscador que realiza la búsqueda semántica (vectorial) y está disponible cuando el plugin de Búsqueda Semántica (``fess-webapp-semantic-search``) está instalado.
- Si esta propiedad no se especifica, se utilizan todos los buscadores registrados. Si ninguno de los nombres especificados coincide con un buscador registrado, solo se utiliza el buscador ``default``.
- La fusión de resultados se realiza únicamente cuando hay dos o más buscadores disponibles. Cuando solo hay un buscador disponible, no se realiza la fusión y se devuelven los resultados de búsqueda normales.

Integración con la búsqueda híbrida
=====================================

Rank Fusion es particularmente eficaz para la búsqueda híbrida, que combina la búsqueda
por palabras clave y la búsqueda semántica. Para usar la búsqueda semántica, instale el
plugin de Búsqueda Semántica (``fess-webapp-semantic-search``) y añada ``semantic`` a
``-Drank.fusion.searchers``.

Ejemplos de uso
===============

Búsqueda híbrida básica
-----------------------

1. Calcular la puntuación BM25 con la búsqueda por palabras clave
2. Calcular la similitud vectorial con la búsqueda semántica
3. Fusionar ambos resultados con RRF
4. Generar el ranking final

Flujo de búsqueda::

    User Query
        ↓
    ┌──────────────────┬──────────────────┐
    │  Keyword Search  │ Semantic Search  │
    │    (BM25)        │  (Vector)        │
    └────────┬─────────┴────────┬─────────┘
             ↓                  ↓
         Rank List 1        Rank List 2
             └────────┬─────────┘
                      ↓
              Rank Fusion (RRF)
                      ↓
              Final Ranking

Consideraciones de rendimiento
================================

Uso de memoria
--------------

- El uso de memoria aumenta porque se retienen múltiples resultados de búsqueda.
- Use ``rank.fusion.window_size`` para limitar el número máximo de resultados a fusionar. El buscador principal (el buscador ``default`` en primer lugar) recupera hasta ``window_size`` resultados, mientras que cada uno de los demás buscadores recupera ``window_size ÷ número de buscadores`` resultados.

::

    # Tamaño de ventana para la fusión
    rank.fusion.window_size=200

Tiempo de procesamiento
-----------------------

- El tiempo de respuesta aumenta porque se ejecutan múltiples búsquedas.
- Use ``rank.fusion.threads`` para establecer el número de hilos para la ejecución paralela.

::

    # Número de hilos para ejecución paralela
    # (si es 0 o menos, availableProcessors × 1.5 + 1)
    rank.fusion.threads=-1

Solución de problemas
=====================

Los resultados de búsqueda difieren de lo esperado
---------------------------------------------------

**Síntoma**: Los resultados tras Rank Fusion difieren de lo esperado

**Verificaciones**:

1. Verificar los resultados de cada tipo de búsqueda individualmente
2. Ajustar el valor de ``rank.fusion.rank_constant``
3. Ajustar el valor de ``rank.fusion.window_size``
4. En páginas profundas (donde ``posición de inicio × 2`` es mayor o igual que ``rank.fusion.window_size``), la fusión no se realiza y solo se utiliza el buscador principal. Si desea resultados fusionados en más páginas, aumente ``rank.fusion.window_size``.

La búsqueda es lenta
--------------------

**Síntoma**: La búsqueda se vuelve lenta cuando Rank Fusion está habilitado

**Soluciones**:

1. Reducir ``rank.fusion.window_size``::

       rank.fusion.window_size=100

2. Ajustar ``rank.fusion.threads``::

       rank.fusion.threads=4

Memoria insuficiente
--------------------

**Síntoma**: Se produce OutOfMemoryError

**Soluciones**:

1. Reducir ``rank.fusion.window_size``
2. Aumentar el tamaño del heap de JVM

Referencia
==========

- :doc:`scripting-overview` - Descripción general de scripting
- :doc:`search-advanced` - Configuración avanzada de búsqueda
- :doc:`llm-overview` - Guía de integración LLM (Búsqueda semántica)
