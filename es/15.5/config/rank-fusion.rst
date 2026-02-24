==================================
Configuracion de Rank Fusion
==================================

Descripcion general
====================

La funcion de Rank Fusion de |Fess| integra multiples resultados de busqueda
para proporcionar resultados de busqueda mas precisos.

Que es Rank Fusion
===================

Rank Fusion es una tecnica que combina resultados de multiples algoritmos de busqueda
o metodos de puntuacion para generar un unico ranking optimizado.

Principales beneficios:

- Combina las fortalezas de diferentes algoritmos
- Mejora la precision de busqueda
- Proporciona resultados de busqueda diversos

Algoritmos compatibles
=======================

|Fess| soporta los siguientes algoritmos de Rank Fusion:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Algoritmo
     - Descripcion
   * - RRF (Reciprocal Rank Fusion)
     - Algoritmo de fusion que utiliza el reciproco de la posicion
   * - Score Fusion
     - Fusion mediante normalizacion de puntuacion y promedio ponderado
   * - Borda Count
     - Fusion de ranking basada en votacion

RRF (Reciprocal Rank Fusion)
----------------------------

RRF calcula las puntuaciones sumando el reciproco de la posicion de cada resultado.

Formula::

    score(d) = Σ 1 / (k + rank(d))

- ``k``: Parametro constante (predeterminado: 60)
- ``rank(d)``: Posicion del documento d en cada resultado de busqueda

Configuracion
==============

fess_config.properties
----------------------

Configuracion basica::

    # Habilitar Rank Fusion
    rank.fusion.enabled=true

    # Algoritmo a utilizar
    rank.fusion.algorithm=rrf

    # Parametro k de RRF
    rank.fusion.rrf.k=60

    # Tipos de busqueda para fusion
    rank.fusion.search.types=keyword,semantic

Configuracion por algoritmo
-----------------------------

Configuracion de RRF::

    rank.fusion.algorithm=rrf
    rank.fusion.rrf.k=60

Configuracion de Score Fusion::

    rank.fusion.algorithm=score
    rank.fusion.score.normalize=true
    rank.fusion.score.weights=0.7,0.3

Configuracion de Borda Count::

    rank.fusion.algorithm=borda
    rank.fusion.borda.top_n=100

Integracion con busqueda hibrida
==================================

Rank Fusion es particularmente efectivo en la busqueda hibrida que combina
busqueda por palabras clave y busqueda semantica.

Ejemplo de configuracion
--------------------------

::

    # Habilitar busqueda hibrida
    search.hybrid.enabled=true

    # Fusionar resultados de busqueda por palabras clave y busqueda semantica
    rank.fusion.enabled=true
    rank.fusion.algorithm=rrf
    rank.fusion.rrf.k=60

    # Peso para cada tipo de busqueda
    search.hybrid.keyword.weight=0.6
    search.hybrid.semantic.weight=0.4

Ejemplos de uso
================

Busqueda hibrida basica
-------------------------

1. Calcular puntuacion BM25 con busqueda por palabras clave
2. Calcular similitud vectorial con busqueda semantica
3. Fusionar ambos resultados con RRF
4. Generar ranking final

Flujo de busqueda::

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

Puntuacion personalizada
--------------------------

Ejemplo de combinacion de multiples factores de puntuacion::

    # Puntuacion base + Impulso por fecha + Popularidad
    rank.fusion.enabled=true
    rank.fusion.algorithm=score
    rank.fusion.score.factors=relevance,recency,popularity
    rank.fusion.score.weights=0.5,0.3,0.2

Consideraciones de rendimiento
================================

Uso de memoria
---------------

- El uso de memoria aumenta al retener multiples resultados de busqueda
- Limite el numero maximo de objetivos de fusion con ``rank.fusion.max.results``

::

    # Numero maximo de resultados para fusion
    rank.fusion.max.results=1000

Tiempo de procesamiento
------------------------

- El tiempo de respuesta aumenta al ejecutar multiples busquedas
- Considere la optimizacion mediante ejecucion paralela

::

    # Habilitar ejecucion paralela
    rank.fusion.parallel=true
    rank.fusion.thread.pool.size=4

Cache
------

- Utilice cache para consultas frecuentes

::

    # Cache para resultados de Rank Fusion
    rank.fusion.cache.enabled=true
    rank.fusion.cache.size=1000
    rank.fusion.cache.expire=300

Solucion de problemas
======================

Los resultados de busqueda difieren de lo esperado
----------------------------------------------------

**Sintoma**: Los resultados despues de Rank Fusion difieren de lo esperado

**Verificaciones**:

1. Verificar los resultados de cada tipo de busqueda individualmente
2. Verificar que la ponderacion sea apropiada
3. Ajustar el valor del parametro k

La busqueda es lenta
---------------------

**Sintoma**: La busqueda se vuelve lenta cuando Rank Fusion esta habilitado

**Soluciones**:

1. Habilitar ejecucion paralela::

       rank.fusion.parallel=true

2. Limitar el numero de resultados objetivo de fusion::

       rank.fusion.max.results=500

3. Habilitar cache::

       rank.fusion.cache.enabled=true

Memoria insuficiente
---------------------

**Sintoma**: Se produce OutOfMemoryError

**Soluciones**:

1. Reducir el numero maximo de resultados objetivo de fusion
2. Aumentar el tamano del heap de JVM
3. Deshabilitar tipos de busqueda innecesarios

Referencia
==========

- :doc:`scripting-overview` - Descripcion general de scripting
- :doc:`../admin/search-settings` - Guia de configuracion de busqueda
- :doc:`llm-overview` - Guia de integracion LLM (Busqueda semantica)
