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

|Fess| soporta el algoritmo RRF (Reciprocal Rank Fusion).

RRF (Reciprocal Rank Fusion)
----------------------------

RRF calcula las puntuaciones sumando el reciproco de la posicion de cada resultado.

Formula::

    score(d) = Σ 1 / (k + rank(d))

- ``k``: Parametro constante (predeterminado: 20)
- ``rank(d)``: Posicion del documento d en cada resultado de busqueda

Configuracion
==============

fess_config.properties
----------------------

Configuracion basica::

    # Tamano de ventana para fusion
    rank.fusion.window_size=200

    # Constante de ranking para RRF
    rank.fusion.rank_constant=20

    # Numero de hilos (-1 para automatico)
    rank.fusion.threads=-1

    # Campo de puntuacion de fusion
    rank.fusion.score_field=rf_score

Integracion con busqueda hibrida
==================================

Rank Fusion es particularmente efectivo en la busqueda hibrida que combina
busqueda por palabras clave y busqueda semantica.

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

Consideraciones de rendimiento
================================

Uso de memoria
---------------

- El uso de memoria aumenta al retener multiples resultados de busqueda
- Limite el numero maximo de objetivos de fusion con ``rank.fusion.window_size``

::

    # Tamano de ventana para fusion
    rank.fusion.window_size=200

Tiempo de procesamiento
------------------------

- El tiempo de respuesta aumenta al ejecutar multiples busquedas
- Configure el numero de hilos para ejecucion paralela con ``rank.fusion.threads``

::

    # Numero de hilos para ejecucion paralela (-1 para automatico)
    rank.fusion.threads=-1

Solucion de problemas
======================

Los resultados de busqueda difieren de lo esperado
----------------------------------------------------

**Sintoma**: Los resultados despues de Rank Fusion difieren de lo esperado

**Verificaciones**:

1. Verificar los resultados de cada tipo de busqueda individualmente
2. Ajustar el valor de ``rank.fusion.rank_constant``
3. Ajustar el valor de ``rank.fusion.window_size``

La busqueda es lenta
---------------------

**Sintoma**: La busqueda se vuelve lenta cuando Rank Fusion esta habilitado

**Soluciones**:

1. Reducir ``rank.fusion.window_size``::

       rank.fusion.window_size=100

2. Ajustar ``rank.fusion.threads``::

       rank.fusion.threads=4

Memoria insuficiente
---------------------

**Sintoma**: Se produce OutOfMemoryError

**Soluciones**:

1. Reducir ``rank.fusion.window_size``
2. Aumentar el tamano del heap de JVM

Referencia
==========

- :doc:`scripting-overview` - Descripcion general de scripting
- :doc:`search-advanced` - Configuración avanzada de búsqueda
- :doc:`llm-overview` - Guia de integracion LLM (Busqueda semantica)
