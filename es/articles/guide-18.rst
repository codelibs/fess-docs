===================================================
Búsqueda semántica para encontrar documentos afines
===================================================

Introducción
============

Si un usuario busca "quiero cobrar el sueldo en otro banco" pero la normativa interna se titula "Trámite para cambiar la cuenta de nómina", la búsqueda por palabras clave no la encontrará.
En Fess 15.9, la "búsqueda semántica", que convierte el texto en vectores que representan su significado y busca con ellos, está integrada en el núcleo y funciona sin plugins (según dónde se ejecute el modelo de embedding, se añade un plugin).

Siguiendo los pasos de este artículo, podrá:

- Distinguir cuándo ayuda la búsqueda semántica y cuándo basta con la búsqueda por palabras clave
- Poner en marcha de inmediato con Docker un entorno con la búsqueda semántica ya configurada
- Configurar ``content_chunker.*`` en un Fess existente y generar los vectores con el trabajo del indexador
- Comprobar con el campo ``searcher`` si un resultado de búsqueda se encontró mediante la búsqueda vectorial

La configuración del modo de búsqueda IA (RAG) se trata en :doc:`guide-19`.

Cuándo ayuda la búsqueda semántica
==================================

La búsqueda semántica de Fess no sustituye a la búsqueda por palabras clave (BM25).
Funciona como una "búsqueda híbrida": ejecuta tanto la búsqueda por palabras clave como la búsqueda vectorial y combina los resultados en una única clasificación mediante Rank Fusion (RRF).

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - La búsqueda semántica ayuda
     - Basta con la búsqueda por palabras clave
   * - Los usuarios y los documentos usan palabras distintas ("banco donde cobro" y "cuenta de nómina", "trabajar desde casa" y "teletrabajo")
     - Buscar la misma cadena que aparece en el documento: referencias de productos, códigos de error, nombres de personas, etc.
   * - Preguntar con una frase ("cómo solicito un PC nuevo")
     - Hay pocas combinaciones de paráfrasis y caben todas en un diccionario de sinónimos
   * - Buscar en español para encontrar documentos en inglés (requiere un modelo de embedding multilingüe)
     - Usar sintaxis de búsqueda como frases o comodines (en este caso, la búsqueda vectorial ni siquiera se ejecuta)

Si las combinaciones de paráfrasis son limitadas, es más sencillo probar primero con un diccionario de sinónimos.
Para registrar sinónimos a partir de los términos sin resultados del registro de búsqueda, consulte :doc:`guide-08`.

Flujo de procesamiento dentro de Fess
=====================================

#. El rastreador registra los documentos en el índice como de costumbre. En este momento todavía no hay vectores.
#. El trabajo del programador ``Content Chunk Vector Indexer`` localiza los documentos sin procesar, divide el texto en chunks (fragmentos), crea un vector de embedding para cada chunk y lo guarda en el campo ``content_chunk_vector``. El resultado se registra en el campo ``content_chunk_status``.
#. Con ``content_chunker.search.enabled=true``, en cada búsqueda se ejecutan la búsqueda por palabras clave (searcher ``default``) y la búsqueda vectorial (searcher ``semantic_chunk``), y se fusionan con RRF.

Este trabajo está deshabilitado de forma predeterminada y no está vinculado al rastreo.
Tenga en cuenta que añadir la configuración por sí solo no crea vectores y que los resultados siguen siendo solo de búsqueda por palabras clave.

Requisitos previos
==================

**OpenSearch con el plugin k-NN**

El índice de búsqueda que crea Fess 15.9 contiene un campo de tipo ``knn_vector``, se use o no la búsqueda semántica.
La imagen de Docker ``ghcr.io/codelibs/fess-opensearch`` y la distribución estándar de OpenSearch incluyen el plugin k-NN.
Con la distribución minimal, que no incluye el plugin k-NN, no se puede crear el índice y Fess no arranca.

**Proveedor de embeddings**

Con ``content_chunker.embedding.name`` se elige dónde se ejecuta el modelo que convierte el texto en vectores.

.. list-table::
   :header-rows: 1
   :widths: 18 32 50

   * - Valor
     - Requisito
     - Descripción
   * - ``opensearch`` (predeterminado)
     - No requiere plugins adicionales
     - Usa un modelo desplegado en OpenSearch ML Commons
   * - ``ollama``
     - Plugin ``fess-llm-ollama``
     - Usa un modelo de embedding de Ollama (modelo predeterminado: ``embeddinggemma``)
   * - ``openai``
     - Plugin ``fess-llm-openai``
     - Usa la API de embeddings de OpenAI (modelo predeterminado: ``text-embedding-3-small``)
   * - ``gemini``
     - Plugin ``fess-llm-gemini``
     - Usa la API de embeddings de Google Gemini
   * - ``bedrock``
     - Plugin ``fess-llm-bedrock``
     - Usa un modelo de embedding de Amazon Bedrock

Instale el plugin en la misma versión menor que Fess (15.9.x) y reinicie Fess después de instalarlo.
OpenAI, Gemini y Bedrock se facturan por uso, por lo que la primera ejecución del trabajo genera de una sola vez el coste de todos los documentos existentes.

El camino más corto: probar con docker-semanticsearch
=====================================================

El repositorio docker-semanticsearch inicia con Docker Compose un Fess 15.9 con la búsqueda semántica ya configurada.
Despliega automáticamente un modelo de embedding multilingüe (``paraphrase-multilingual-MiniLM-L12-v2``, 384 dimensiones) en OpenSearch ML Commons e incluso habilita el trabajo del indexador.

::

    $ git clone --branch v15.9.0 https://github.com/codelibs/docker-semanticsearch.git
    $ cd docker-semanticsearch
    $ FESS_THEMES_REF=15.9.x bash ./bin/setup.sh
    $ docker compose up -d
    $ docker compose logs -f init-semantic init-fess-chunk

``setup.sh`` obtiene el tema ``semanticlens`` de la página de búsqueda del repositorio ``fess-themes``.
El tema de ``main``, el origen predeterminado en ``v15.9.0``, es para Fess 15.10 y posteriores (``minFessVersion: 15.10``), por lo que con ``FESS_THEMES_REF`` se indica la rama ``15.9.x``, que contiene el tema para 15.9.

La primera vez, la descarga del modelo (unos 490MB) tarda varios minutos.
Todo está listo cuando ``docker compose ps -a`` muestra ``fess01`` como healthy e ``init-semantic`` e ``init-fess-chunk`` como ``Exited (0)``.

A continuación, igual que en un Fess normal, cree una configuración de rastreo en la consola de administración (``http://localhost:8080/admin``) y ejecute el rastreo.
En este entorno, el trabajo del indexador se ejecuta cada hora.
Si quiere crear los vectores de inmediato, abra ``Content Chunk Vector Indexer`` en [Sistema] > [Programador] y haga clic en [Iniciar ahora].

Además de la configuración que se explica más adelante en este artículo, este entorno usa los siguientes valores:

- La fusión se realiza en el lado de OpenSearch (``rank.fusion.engine.enabled=true``)
- La longitud de los chunks es de 250 caracteres (porque el límite de entrada del modelo es de 128 tokens)
- Umbral mínimo de similitud ``content_chunker.search.min_score=0.5``
- El tema ``semanticlens``, que muestra en cada resultado si se encontró por palabras clave, por búsqueda semántica o por ambas

Para cambiar estos valores, consulte la sección Configuration del README del repositorio.

Habilitar la búsqueda semántica en un Fess existente
====================================================

Aquí se muestran los pasos con el ejemplo de ``embeddinggemma`` de Ollama (768 dimensiones, multilingüe).
Si usa el proveedor integrado ``opensearch``, en lugar de los pasos 1 y 2, despliegue un modelo en ML Commons y configure ``content_chunker.embedding.name=opensearch`` y ``content_chunker.embedding.opensearch.model.id``.
El procedimiento está en "Procedimiento de configuración (ejemplo con el proveedor opensearch)" de `Búsqueda semántica <https://fess.codelibs.org/es/stable/config/search-semantic.html>`__.

Paso 1: instalar el plugin
--------------------------

En [Sistema] > [Plugin] > [Instalar], seleccione ``fess-llm-ollama`` en la versión 15.9.x, instálelo y reinicie Fess.
Con Docker, indique ``FESS_PLUGINS=fess-llm-ollama:15.9.0`` para ``fess01`` en ``compose.yaml``.

Paso 2: preparar el modelo de embedding
---------------------------------------

Descargue el modelo en el servidor donde se ejecuta Ollama.

::

    $ ollama pull embeddinggemma

Paso 3: escribir la configuración en system.properties
------------------------------------------------------

La configuración ``content_chunker.*`` se lee únicamente desde ``system.properties``.
Se ignora si se escribe en ``fess_config.properties`` o con ``-Dfess.config.``.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Tipo de instalación
     - Dónde escribirla
   * - Versión ZIP
     - ``app/WEB-INF/conf/system.properties``
   * - Versión RPM/DEB
     - ``/etc/fess/system.properties``
   * - Docker (docker-fess)
     - Indicarla como ``-Dfess.system.<clave>=<valor>`` en ``FESS_JAVA_OPTS`` de ``compose.yaml``

También se lee ``/opt/fess/system.properties`` dentro del contenedor Docker, pero ``fess01`` de docker-fess no tiene volumen, así que el archivo desaparece con ``docker compose down``.

Escriba lo siguiente:

::

    content_chunker.enabled=true
    content_chunker.embedding.name=ollama
    content_chunker.embedding.dimension=768
    content_chunker.embedding.ollama.api.url=http://localhost:11434
    content_chunker.embedding.ollama.model=embeddinggemma
    content_chunker.search.enabled=true

``api.url`` es la dirección de Ollama vista desde Fess.
Si Fess se ejecuta en Docker, ``localhost`` apunta al propio contenedor, así que cámbiela por una dirección accesible desde el contenedor.

``content_chunker.embedding.dimension`` debe coincidir siempre con la dimensión de salida del modelo.
Este valor se escribe en el mapeo al crear el índice y no se puede cambiar después.

Paso 4: reiniciar Fess
----------------------

El cambio de ``content_chunker.search.enabled`` a ``true`` no se aplica hasta reiniciar (el resto de ``content_chunker.*`` se vuelve a leer durante la ejecución).

Paso 5: reconstruir el índice existente
---------------------------------------

En un entorno en el que Fess se haya iniciado aunque sea una vez, el mapeo con la nueva dimensión no está aplicado al índice.
En [Información del sistema] > [Mantenimiento], active "Actualizar alias" en "Reindexación" y haga clic en [Iniciar].
No es necesario en un entorno nuevo en el que haya completado el paso 3 antes del primer arranque.

La reindexación avanza de forma asíncrona en segundo plano y la pantalla no muestra cuándo termina.
Antes de pasar al siguiente paso, compruebe que los alias ``fess.search`` y ``fess.update`` apuntan ambos al nuevo índice (``fess.<marca de tiempo>``).

::

    $ curl -s "http://localhost:9200/_cat/aliases/fess.search,fess.update?v"

El índice antiguo no se elimina automáticamente, así que elimínelo manualmente una vez hecha la comprobación.
No es necesario volver a rastrear.
El trabajo del indexador crea los vectores a partir del texto ya guardado.

Paso 6: habilitar y ejecutar el trabajo del indexador
-----------------------------------------------------

#. En [Sistema] > [Programador], abra ``Content Chunk Vector Indexer`` y haga clic en [Editar].
#. Marque "Habilitado" en "Estado", cambie la programación si es necesario y haga clic en [Actualizar]. La programación predeterminada es ``0 13 * * *`` (todos los días a las 13:00).
#. Al volver a la pantalla de detalles aparece [Iniciar ahora]; haga clic para ejecutarlo una vez.

Como el trabajo no está vinculado al rastreo, los documentos rastreados se pueden buscar por palabras clave de inmediato, pero solo entran en la búsqueda vectorial después de la siguiente ejecución de este trabajo.
Programe el trabajo para una hora posterior a la finalización de sus trabajos de rastreo.

Comprobar el funcionamiento
===========================

Comprobar que se crearon los vectores
-------------------------------------

Haga que OpenSearch agregue el resultado del procesamiento de cada documento.

::

    $ curl -s -XPOST "http://localhost:9200/fess.search/_search" \
        -H "Content-Type: application/json" -d '
    {"size": 0, "aggs": {"status": {"terms": {"field": "content_chunk_status", "missing": "pending"}}}}'

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Valor
     - Significado
   * - ``pending``
     - Sin procesar (se procesará en la siguiente ejecución del trabajo). Los documentos que se vuelven a rastrear también regresan a este estado
   * - ``done``
     - División en chunks y generación de vectores completadas
   * - ``chunked``
     - Solo división en chunks. Los documentos también quedan en este estado cuando no está instalado el plugin del proveedor
   * - ``skipped``
     - El texto está vacío o el número de chunks superó el límite (1000 de forma predeterminada)
   * - ``fail``
     - Error. Revise la causa en el archivo de registro ``fess-chunk.log``

Si con cada ejecución del trabajo ``pending`` disminuye y ``done`` aumenta, todo va bien.

Comprobar si un resultado se encontró mediante la búsqueda vectorial
--------------------------------------------------------------------

El campo ``searcher`` de un resultado de búsqueda contiene los nombres de los searchers que encontraron el documento.
De forma predeterminada no se incluye en la respuesta de la API de búsqueda, así que añada la siguiente línea a ``fess_config.properties`` y reinicie (en Docker, ``-Dfess.config.query.additional.api.response.fields=searcher``).

::

    query.additional.api.response.fields=searcher

Busque con una paráfrasis cuyas palabras clave no coincidan con el documento.
Si tiene un documento que explica el "Trámite para cambiar la cuenta de nómina", busque así:

::

    $ curl -s -G "http://localhost:8080/api/v2/search" \
        --data-urlencode "q=quiero cobrar el sueldo en otro banco" \
      | jq '.response.data[] | {title, searcher}'

Un resultado cuyo ``searcher`` es ``["semantic_chunk"]`` se encontró solo mediante la búsqueda vectorial, y ``["default", "semantic_chunk"]`` indica que se encontró con ambas.
Si todos los resultados tienen solo ``["default"]``, la búsqueda vectorial no está devolviendo resultados.
Revise la sección siguiente.

Problemas frecuentes
====================

**Sigue configurado rank.fusion.searchers de la época del plugin antiguo**

Con el plugin ``fess-webapp-semantic-search`` de la versión 15.7 y anteriores se indicaba ``-Drank.fusion.searchers=default,semantic``.
En 15.9 el searcher se llama ``semantic_chunk``, así que, si este ajuste permanece, la búsqueda semántica no se ejecuta y solo se devuelven resultados de la búsqueda por palabras clave.
Al arrancar aparece el registro WARN ``rank.fusion.searchers allows 'semantic' but not 'semantic_chunk'``.
Revise tanto las opciones de la JVM como el campo "Propiedad del sistema" de [Sistema] > [General], y elimine este ajuste (si no se indica, se usan todos los searchers).
Para migrar desde el plugin antiguo, consulte "Migración desde la versión 15.7 o anterior" en `Búsqueda semántica <https://fess.codelibs.org/es/stable/config/search-semantic.html>`__.

**La búsqueda vectorial no se ejecuta en consultas con sintaxis de búsqueda**

Las siguientes consultas se procesan solo con la búsqueda por palabras clave:

- Frases (``"..."``), comodines, búsqueda difusa y rangos
- Oraciones que terminan en un ``?`` ASCII (por ejemplo, "¿qué es ...?"). El "？" de ancho completo que se usa en japonés y chino no cuenta
- Exclusiones (``-palabra``, ``NOT palabra``) y ponderaciones (``palabra^2``)
- Búsquedas que especifican un orden

El filtrado con ``label:``, ``site:`` o facetas no supone ningún problema, porque también se aplica como filtro a la búsqueda vectorial.

**La dimensión no coincide, o el índice se creó sin configurarla**

Si el índice se crea sin configurar ``content_chunker.embedding.dimension``, el mapeo queda con 768 dimensiones y el trabajo marca los documentos como ``fail``.
Si la dimensión del modelo no es 768, configure el valor correcto y repita la reindexación del paso 5.
Los documentos ``fail`` y ``skipped`` no se vuelven a procesar aunque se ejecute de nuevo el trabajo.
Después de corregir la causa, configure temporalmente ``content_chunker.job.retry_failed=true`` y ejecute el trabajo.

**Se cambió el modelo de embedding**

Los vectores guardados se crearon con el modelo antiguo, por lo que cambiar solo el modelo degrada la precisión de la búsqueda (no aparece ningún error aunque la dimensión sea la misma).
El procedimiento para eliminar ``content_chunk_vector`` y ``content_chunk_status`` y volver a ejecutar el trabajo está en "Notas" de la referencia.

**Aparecen arriba documentos poco relacionados**

La búsqueda vectorial devuelve los documentos por orden de cercanía, incluso los de baja similitud.
Si configura en ``content_chunker.search.min_score`` un umbral mínimo de similitud de coseno (de 0 a 1), se excluyen los documentos que no lo alcanzan.
El valor adecuado depende del modelo y de los documentos, así que ajústelo buscando tanto con términos que antes no tenían resultados como con términos sin relación.

**Los resultados cambian de carácter a partir de la segunda mitad de la página 2**

En la configuración predeterminada, en la que la fusión se hace en el lado de Fess, solo se fusionan los 200 primeros resultados de cada searcher (``rank.fusion.window_size``), y a partir del resultado 101 solo quedan resultados de la búsqueda por palabras clave.
El número de resultados también aumenta en la cantidad de documentos que solo encontró la búsqueda vectorial.
Para el funcionamiento de la fusión y las opciones de ajuste (``rank.fusion.rank_constant``, fusión en el lado de OpenSearch), consulte `Búsqueda híbrida y Rank Fusion <https://fess.codelibs.org/es/stable/config/rank-fusion.html>`__.

Relación con el modo de búsqueda IA y la búsqueda multimodal
============================================================

El modo de búsqueda IA (RAG) se puede usar sin habilitar la búsqueda semántica.
En los documentos cuyos vectores se han creado con ``content_chunker.enabled=true``, el texto que se usa para la respuesta se limita a los chunks más cercanos a la pregunta, de modo que incluso en documentos largos se pueden pasar al LLM las partes relevantes.
Para configurar el modo de búsqueda IA, consulte :doc:`guide-19`.

La búsqueda multimodal (``fess-webapp-multimodal``), que busca en imágenes y texto a la vez, no se puede usar en el mismo Fess al mismo tiempo que la búsqueda semántica de texto de este artículo.
Para más detalles, consulte :doc:`guide-21`.

Artículos siguientes
====================

- Mejorar los términos sin resultados del registro de búsqueda con sinónimos y Coincidencia de clave: :doc:`guide-08`
- Hacer que la IA generativa responda a partir de documentos internos: :doc:`guide-19`
- Buscar también en imágenes: :doc:`guide-21`
- Buscar desde sistemas de negocio mediante la API de búsqueda: :doc:`guide-11`

Referencias
===========

- `Búsqueda semántica (chunking de contenido + búsqueda vectorial) <https://fess.codelibs.org/es/stable/config/search-semantic.html>`__
- `Búsqueda híbrida y Rank Fusion (semántica + palabras clave) <https://fess.codelibs.org/es/stable/config/rank-fusion.html>`__
- `Configuración de Ollama (LLM local / RAG) <https://fess.codelibs.org/es/stable/config/llm-ollama.html>`__
- `Programador de tareas <https://fess.codelibs.org/es/stable/admin/scheduler-guide.html>`__
- `Mantenimiento <https://fess.codelibs.org/es/stable/admin/maintenance-guide.html>`__
- `Complemento <https://fess.codelibs.org/es/stable/admin/plugin-guide.html>`__
- `docker-semanticsearch (GitHub) <https://github.com/codelibs/docker-semanticsearch>`__
