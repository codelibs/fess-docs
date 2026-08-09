===========================================================
Búsqueda Híbrida y Rank Fusion (Semántica + Palabras Clave)
===========================================================

Descripción general
===================

La **búsqueda híbrida** en |Fess| combina la búsqueda tradicional por palabras clave (BM25) con la **búsqueda semántica (vectorial)** y fusiona ambos conjuntos de resultados mediante **Rank Fusion** para producir clasificaciones más precisas y relevantes. Rank Fusion integra los resultados de múltiples buscadores en un único ranking optimizado.

En |Fess| 15.8, la búsqueda semántica (chunking de contenido + búsqueda vectorial) se proporciona
como una función del núcleo. Una vez que la habilita, el buscador semántico se registra
automáticamente con Rank Fusion. Consulte :doc:`search-semantic` para su configuración.

La función de Rank Fusion de |Fess| integra múltiples resultados de búsqueda para
proporcionar resultados de búsqueda más precisos.

Qué es Rank Fusion
==================

Rank Fusion es una técnica que combina resultados de múltiples algoritmos de búsqueda
o métodos de puntuación (por ejemplo, palabras clave/BM25 y búsqueda semántica/vectorial) para generar un único ranking optimizado.

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

.. note::

   El algoritmo de fusión es siempre RRF; no existe ningún ajuste para cambiar a otro algoritmo.
   Tampoco se admite la ponderación por buscador: la contribución de cada buscador se suma con
   el mismo peso. El único ajuste que permite modificar la tendencia del ranking es
   ``rank.fusion.rank_constant``.

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
    # (si es 0 o menos, se usa availableProcessors × 3 ÷ 2 + 1)
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
     - Número máximo de resultados recuperados de cada buscador para la fusión. Debe ser >= ``paging.search.page.max.size × 2`` (``200`` de forma predeterminada); si se establece un valor menor, se eleva automáticamente a este mínimo (se registra una advertencia WARN al iniciar).
   * - ``rank.fusion.rank_constant``
     - ``20``
     - La constante ``k`` en la fórmula RRF. Un valor mayor reduce la diferencia de puntuación entre los resultados con mayor y menor rango.
   * - ``rank.fusion.threads``
     - ``-1``
     - Número de hilos del grupo de hilos fijo que ejecuta múltiples buscadores en paralelo. Si se especifica ``0`` o menos, se usa ``availableProcessors × 3 ÷ 2 + 1`` automáticamente (al tratarse de aritmética entera, la parte decimal se trunca; por ejemplo: 4 núcleos → 7, 5 núcleos → 8).
   * - ``rank.fusion.score_field``
     - ``rf_score``
     - Nombre del campo del documento de resultados utilizado para almacenar la puntuación fusionada.

.. note::

   **Cuándo se aplican los cambios de configuración**

   Los cuatro ajustes anteriores requieren reiniciar |Fess| para que un cambio se aplique. Los
   valores leídos de ``fess_config.properties`` se almacenan en caché en la JVM, por lo que
   modificar el archivo mientras |Fess| está en ejecución no tiene ningún efecto.

   A modo de referencia, ``rank.fusion.window_size`` se lee una sola vez al iniciar y
   ``rank.fusion.threads`` se lee en el momento en que se crea el grupo de hilos. El grupo de
   hilos se crea cuando se registra un buscador distinto de ``default`` (por ejemplo, el buscador
   semántico), de modo que si la búsqueda semántica está deshabilitada no se crea ningún grupo
   de hilos.

Propiedades del sistema JVM
---------------------------

Los buscadores a utilizar se especifican como una propiedad del sistema JVM. Añada lo
siguiente a ``fess.in.sh``::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Drank.fusion.searchers=default,semantic_chunk"

En el caso de ``fess.in.bat``, escriba lo siguiente::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Drank.fusion.searchers=default,semantic_chunk

Esta propiedad se comporta de la siguiente manera:

- Se establece como opción JVM, no en ``fess_config.properties``. Especifique el nombre de la
  clave tal cual: ``rank.fusion.searchers``. Las formas con los prefijos ``-Dfess.config.`` o
  ``-Dfess.system.``, habituales en otros ajustes (por ejemplo,
  ``-Dfess.config.rank.fusion.searchers``), no se reconocen.
- En lugar de una opción JVM, también puede escribirlo en una sola línea, como
  ``rank.fusion.searchers=default,semantic_chunk``, en el campo "Propiedades del sistema" de
  "Sistema > General" de la pantalla de administración. Tenga en cuenta que el valor de ese campo
  solo se aplica cuando todavía no existe una propiedad del sistema con el mismo nombre. Por ello,
  si se ha indicado con ``-D``, la opción JVM tiene prioridad, y para modificar un valor que ya se
  ha aplicado es necesario reiniciar |Fess|.
- ``default`` es el buscador que realiza la búsqueda estándar por palabras clave y siempre está disponible.
- El nombre de un buscador se deriva del nombre de su clase de implementación eliminando el
  sufijo ``Searcher`` y convirtiendo el resto a snake_case en minúsculas
  (``SemanticChunkSearcher`` → ``semantic_chunk``). El buscador semántico integrado en el núcleo
  (:doc:`search-semantic`) se registra con el nombre ``semantic_chunk``.
- Si esta propiedad no se especifica, se utilizan todos los buscadores registrados. Si ninguno de los nombres especificados coincide con un buscador registrado, solo se utiliza el buscador ``default``. Si utiliza el buscador semántico integrado en el núcleo (:doc:`search-semantic`), normalmente no necesita establecer esta propiedad en absoluto.
- La fusión de resultados se realiza únicamente cuando hay dos o más buscadores disponibles. Cuando solo hay un buscador disponible, no se realiza la fusión y se devuelven los resultados de búsqueda normales.

.. warning::

   Si anteriormente utilizaba el plugin ``fess-webapp-semantic-search`` de |Fess| 15.7 o
   anterior, es posible que se le haya indicado que estableciera esta propiedad como
   ``-Drank.fusion.searchers=default,semantic``. Ese plugin registraba su buscador con el nombre
   ``semantic``, que es un **buscador diferente** del nombre del buscador integrado en el núcleo,
   ``semantic_chunk``, introducido en la 15.8. Si traslada esa configuración de la era 15.7 a la
   15.8 sin cambios, la lista de permitidos nunca incluye ``semantic_chunk``, por lo que la
   búsqueda semántica integrada en el núcleo (chunking de contenido + búsqueda vectorial) **no
   funciona en absoluto** — |Fess| sigue devolviendo silenciosamente resultados de búsqueda por
   palabras clave normales (se registra una advertencia al iniciar, pero la exclusión por
   solicitud en sí solo se registra en el nivel DEBUG). Si su configuración especifica
   ``default,semantic``, elimine este ajuste o añada ``semantic_chunk``. Consulte "Migración
   desde la versión 15.7 o anterior" en :doc:`search-semantic` para más detalles.

Integración con la búsqueda híbrida
=====================================

Rank Fusion es particularmente eficaz para la búsqueda híbrida, que combina la búsqueda
por palabras clave y la búsqueda semántica. Para usar la búsqueda semántica, configure la función
de chunking de contenido y establezca ``content_chunker.search.enabled=true``.

.. warning::

   Los ajustes ``content_chunker.*``, como ``content_chunker.enabled`` y
   ``content_chunker.search.enabled``, no pertenecen a ``fess_config.properties``, sino que son
   **propiedades del sistema**. Escríbalos en ``conf/system.properties`` o especifíquelos como
   opción JVM, por ejemplo ``-Dfess.system.content_chunker.search.enabled=true``. Si los escribe
   en ``fess_config.properties``, no tendrán ningún efecto. Además,
   ``content_chunker.search.enabled`` solo se evalúa al iniciar, por lo que tras habilitarlo es
   necesario reiniciar |Fess|.

Consulte :doc:`search-semantic` para más detalles.

Verificación de los resultados de la fusión
===========================================

Puede comprobar si Rank Fusion está funcionando realmente mediante los dos campos siguientes,
que se añaden a los resultados de búsqueda.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Campo
     - Contenido
   * - ``searcher``
     - Array con los nombres de los buscadores que recuperaron el documento (por ejemplo, ``["default", "semantic_chunk"]``). Si contiene ambos, significa que el documento coincidió tanto en la búsqueda por palabras clave como en la búsqueda semántica.
   * - ``rf_score``
     - Puntuación fusionada calculada mediante RRF. El nombre del campo se puede cambiar con ``rank.fusion.score_field``.

Ambos son valores que se añaden dinámicamente en el momento de la búsqueda y no se almacenan en
el índice. Además, de forma predeterminada no se incluyen en la respuesta de ``/api/v2/search``,
por lo que, para consultarlos, establezca lo siguiente en ``fess_config.properties`` y reinicie
|Fess|::

    query.additional.api.response.fields=rf_score,searcher

.. note::

   ``query.additional.api.response.fields`` es un ajuste que añade elementos a la lista de
   permitidos de los campos que pueden incluirse en la respuesta de la API de búsqueda v2. No
   añada campos de control de acceso como ``role`` o ``virtual_host``, ya que la información de
   control de acceso quedaría expuesta en la respuesta de la API de búsqueda.

Impacto en el número de resultados
==================================

Cuando se ejecuta Rank Fusion, el número total de resultados devuelto no es sin más el del
buscador principal (el buscador ``default`` registrado en primer lugar), sino que se corrige de
la siguiente manera::

    Número total de resultados = número total del buscador principal + valor de corrección

El valor de corrección es el número de documentos que, estando entre los ``window_size ÷ 2``
primeros resultados tras la fusión, no estaban entre los ``window_size ÷ 2`` primeros resultados
del buscador principal. Es decir, el número aumenta en la cantidad de documentos que solo
encontró la búsqueda semántica.
Por ello, para una misma consulta el número de resultados puede variar según si la búsqueda
híbrida está habilitada o no.

Tenga en cuenta que, si el número total de resultados del buscador principal se devuelve como un
valor aproximado (un límite inferior), esta corrección no se aplica.

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
- Use ``rank.fusion.window_size`` para limitar el número máximo de resultados a fusionar. El buscador principal (el buscador ``default`` en primer lugar) recupera hasta ``window_size`` resultados, mientras que cada uno de los demás buscadores recupera ``window_size ÷ número de buscadores`` resultados (``número de buscadores`` es el total incluyendo el buscador principal, y la división se trunca).
- Por ejemplo, con dos buscadores (``default`` y ``semantic_chunk``) y ``window_size=200``, el buscador principal recupera 200 resultados y el buscador semántico 100, por lo que se retienen como máximo 300 documentos.

::

    # Tamaño de ventana para la fusión
    rank.fusion.window_size=200

.. warning::

   ``rank.fusion.window_size`` no puede ser inferior a ``paging.search.page.max.size × 2``. Si
   ``paging.search.page.max.size`` tiene su valor predeterminado ``100``, el límite inferior es
   ``200``, que coincide con el valor predeterminado de ``rank.fusion.window_size``. Es decir,
   **en la configuración predeterminada no es posible establecer window_size por debajo de su
   valor predeterminado**. Si establece un valor menor, se registra una advertencia WARN al
   iniciar y el valor se eleva a ``200``. Para reducirlo realmente es necesario reducir antes
   ``paging.search.page.max.size``, pero esto también reduce el número máximo de resultados que
   se pueden solicitar por página desde la pantalla de búsqueda y la API.

Tiempo de procesamiento
-----------------------

- El tiempo de respuesta aumenta porque se ejecutan múltiples búsquedas.
- Use ``rank.fusion.threads`` para establecer el número de hilos para la ejecución paralela.

::

    # Número de hilos para ejecución paralela
    # (si es 0 o menos, availableProcessors × 3 ÷ 2 + 1)
    rank.fusion.threads=-1

.. note::

   La ejecución de los buscadores no tiene ningún tiempo de espera configurado. Si algún buscador
   no devuelve respuesta, la solicitud de búsqueda espera hasta que este finalice.

Comportamiento cuando falla un buscador
=======================================

Si alguno de los buscadores falla con una excepción, sus resultados se tratan como vacíos: se
registra una advertencia WARN y la fusión continúa únicamente con los resultados de los
buscadores restantes. La propia solicitud de búsqueda no produce ningún error.

Sin embargo, los errores de sintaxis de consulta (``InvalidQueryException``) y la superación del
límite de paginación (``ResultOffsetExceededException``) son excepciones a esta regla: estos se
devuelven como errores tal cual. Además, en las páginas profundas en las que no se realiza la
fusión (donde ``posición de inicio × 2`` es mayor o igual que ``rank.fusion.window_size``), una
excepción producida en el buscador principal se devuelve tal cual como error de la solicitud de
búsqueda.

El buscador semántico devuelve resultados vacíos cuando no puede conectarse al proveedor de
embeddings o cuando falla el procesamiento de los embeddings. También en este caso no se produce
ningún error, y solo se obtienen los resultados de la búsqueda por palabras clave.

Solución de problemas
=====================

Los resultados de búsqueda difieren de lo esperado
---------------------------------------------------

**Síntoma**: Los resultados tras Rank Fusion difieren de lo esperado

**Verificaciones**:

1. Verificar el campo ``searcher`` (consulte "Verificación de los resultados de la fusión"). Si
   todos los documentos muestran únicamente ``["default"]``, el buscador semántico no está
   devolviendo resultados.
2. Comprobar si la búsqueda semántica se está omitiendo. Además de las consultas que contienen
   sintaxis de búsqueda (``"``, ``:``, ``AND``, etc.), en los filtrados por etiqueta, orden o
   faceta, en la búsqueda por ubicación y en la búsqueda de documentos similares, el buscador
   semántico no devuelve resultados y solo se obtienen los de la búsqueda por palabras clave.
   Consulte :doc:`search-semantic` para más detalles sobre las condiciones de omisión.
3. Verificar los resultados de cada tipo de búsqueda individualmente
4. Ajustar el valor de ``rank.fusion.rank_constant``
5. En páginas profundas (donde ``posición de inicio × 2`` es mayor o igual que
   ``rank.fusion.window_size``; de forma predeterminada, a partir del resultado 101), la fusión
   no se realiza y solo se utiliza el buscador principal. Si desea resultados fusionados en más
   páginas, aumente ``rank.fusion.window_size``.

La búsqueda es lenta
--------------------

**Síntoma**: La búsqueda se vuelve lenta cuando Rank Fusion está habilitado

**Soluciones**:

1. Ajustar ``rank.fusion.threads``::

       rank.fusion.threads=4

2. Reducir ``rank.fusion.window_size``. Sin embargo, no puede quedar por debajo de su límite
   inferior (``paging.search.page.max.size × 2``), por lo que en la configuración predeterminada
   se deben establecer los dos ajustes siguientes conjuntamente::

       paging.search.page.max.size=50
       rank.fusion.window_size=100

   Tenga en cuenta que el número máximo de resultados que se pueden solicitar por página también
   se reduce. Tras aplicar la configuración es necesario reiniciar.

Memoria insuficiente
--------------------

**Síntoma**: Se produce OutOfMemoryError

**Soluciones**:

1. Reducir ``rank.fusion.window_size`` siguiendo el mismo procedimiento que en "La búsqueda es lenta"
2. Aumentar el tamaño del heap de JVM

Referencia
==========

- :doc:`search-semantic` - Configuración de la búsqueda semántica (chunking de contenido)
- :doc:`scripting-overview` - Descripción general de scripting
- :doc:`search-advanced` - Configuración avanzada de búsqueda
- :doc:`llm-overview` - Guía de integración LLM (Búsqueda semántica)
