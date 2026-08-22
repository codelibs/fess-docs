=================================================================
Búsqueda Semántica (Chunking de Contenido + Búsqueda Vectorial)
=================================================================

Descripción general
====================

En |Fess| 15.9, la **función de chunking de contenido** — que divide el cuerpo de los documentos
en chunks y genera y almacena un vector de embedding para cada chunk — se ha integrado en el
núcleo. Los vectores generados se utilizan para dos propósitos:

- **Búsqueda semántica**: una búsqueda híbrida que combina la búsqueda por palabras clave (BM25)
  y la búsqueda vectorial mediante Rank Fusion. Los documentos que son semánticamente cercanos a
  la consulta pueden coincidir incluso sin una superposición exacta de palabras clave.
- **Modo de búsqueda IA (RAG)**: al generar una respuesta, solo se seleccionan como contexto del
  LLM los chunks semánticamente más cercanos a la pregunta, lo que mejora la calidad de la
  respuesta y la eficiencia de tokens.

Todo esto está deshabilitado de forma predeterminada. A menos que lo habilite, |Fess| continúa
funcionando exactamente igual que antes, utilizando únicamente la búsqueda por palabras clave. Si
está actualizando |Fess| desde la versión 15.7 o anterior, o si utilizaba el plugin
``fess-webapp-semantic-search``, consulte :ref:`semantic-search-migration`.

Flujo de procesamiento
------------------------

1. El rastreador indexa los documentos como de costumbre (en este momento no existen chunks).
2. El trabajo del programador **Content Chunk Vector Indexer** busca documentos no procesados,
   divide su contenido (el campo ``content``) en chunks, genera vectores de embedding y los
   almacena en el campo ``content_chunk_vector``. En ese momento, el propio campo ``content``
   también se reescribe como el array de chunks (``content_length`` conserva su valor original).
3. El resultado de ese procesamiento se registra en el campo ``content_chunk_status``
   (descrito más abajo).
4. Cuando ``content_chunker.search.enabled=true``, el buscador semántico participa en Rank
   Fusion en el momento de la búsqueda.

Requisitos previos
====================

- **OpenSearch con el plugin k-NN**: En |Fess| 15.9, el mapeo del índice de búsqueda
  (``fess.search``) siempre incluye el campo ``content_chunk_vector`` (de tipo ``nested``, cuyo
  subcampo ``vector`` es el tipo ``knn_vector`` para ANN), y la configuración del índice siempre
  incluye ``index.knn: true``, independientemente de si la función de chunking de contenido está
  habilitada. Como resultado, si OpenSearch no tiene instalado el plugin k-NN, la creación de un
  nuevo índice falla directamente y |Fess| no puede arrancar.

  .. list-table::
     :header-rows: 1
     :widths: 35 65

     * - Configuración
       - Compatibilidad con el plugin k-NN
     * - OpenSearch integrado (``bin/fess``, o los paquetes TAR.GZ/ZIP con
         ``SEARCH_ENGINE_HTTP_URL`` sin definir — el valor predeterminado)
       - Se distribuye con el plugin k-NN. Sin embargo, no incluye las bibliotecas nativas JNI,
         por lo que el único motor ANN compatible es ``lucene``. ``content_chunker.search.knn.engine``
         también acepta ``faiss`` como valor, y establecerlo aquí igualmente crea el mapeo
         correctamente — pero **los documentos se pierden silenciosamente en cada escritura y las
         búsquedas no devuelven ningún resultado** (al arrancar con esta combinación, |Fess|
         registra una advertencia en el inicio).
     * - Docker (``ghcr.io/codelibs/fess-opensearch``), los paquetes RPM/DEB (que siempre se
         conectan a un OpenSearch externo instalado por separado) u otro OpenSearch externo
         (distribución estándar)
       - Totalmente compatible, incluyendo ``faiss``.
     * - La **distribución mínima** de un OpenSearch externo
       - **No compatible.** No incluye el plugin k-NN, por lo que la creación de un nuevo índice
         falla.

  ``nmslib`` nunca es un valor aceptado para ``content_chunker.search.knn.engine`` en ninguna de
  las configuraciones anteriores: ``content_chunk_vector`` es un campo ``nested``, y el plugin
  k-NN solo admite campos nested con los motores ``lucene``/``faiss`` (``nmslib`` también está
  obsoleto y restringido a partir de OpenSearch 3.0). Si se establece, se aplica el valor
  predeterminado ``lucene`` con una advertencia; consulte la Referencia de configuración más abajo
  para conocer los valores aceptados del resto de ajustes ANN.

- **Versión de OpenSearch de un clúster externo**: la configuración del índice ``fess.search``
  incluida siempre envía ``index.knn`` y ``knn.derived_source.enabled`` (en
  ``fess_indices/fess.json`` y sus variantes de AWS/nube). Este último es un ajuste
  relativamente reciente del plugin k-NN, y en un OpenSearch antiguo que no lo reconoce la
  creación del índice falla, esté o no instalado el plugin k-NN. Consulte
  :doc:`../install/prerequisites` para conocer las versiones de OpenSearch compatibles con
  |Fess| 15.9.

- **Proveedor de embedding**: use uno de los siguientes.

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - Valor de configuración
     - Proporcionado por
     - Descripción
   * - ``opensearch``
     - Núcleo de |Fess| (integrado)
     - Utiliza un modelo de embedding desplegado en OpenSearch ML Commons. No requiere plugin
       adicional. Configuración predeterminada.
   * - ``ollama``
     - Plugin ``fess-llm-ollama``
     - Utiliza un modelo de embedding de Ollama (p. ej., ``nomic-embed-text``).
   * - ``openai``
     - Plugin ``fess-llm-openai``
     - Utiliza la API de embeddings de OpenAI.
   * - ``gemini``
     - Plugin ``fess-llm-gemini``
     - Utiliza la API de embeddings de Google Gemini.
   * - ``none``
     - Núcleo de |Fess| (integrado)
     - Solo divide los documentos en chunks; no se genera ningún vector (modo solo chunking).

Referencia de configuración
==============================

Todas las configuraciones ``content_chunker.*`` residen en un único canal: las **propiedades del
sistema** (``system.properties``). Configúrelas en ``app/WEB-INF/conf/system.properties`` (en
RPM/DEB, ``/etc/fess/system.properties``; en Docker, ``/opt/fess/system.properties``), o
proporcione un valor inicial con la opción de inicio ``-Dfess.system.<key>``. Los valores se
recargan en tiempo de ejecución, por lo que la mayoría de las configuraciones surten efecto
inmediatamente después de cambiarlas. La única excepción es habilitar
``content_chunker.search.enabled`` (``false`` → ``true``): dado que el buscador semántico solo se
registra al iniciar, **este cambio requiere un reinicio para surtir efecto**.

.. note::

   Las claves ``content_chunker.*`` solo se leen desde el canal ``system.properties``. Escribirlas
   en ``fess_config.properties`` o en ``-Dfess.config.<key>`` no surte ningún efecto, así que
   configúrelas siempre en ``system.properties``. Tenga además en cuenta que la pantalla de
   administración **Información del sistema > Información de configuración** es una vista de
   **solo lectura** de los valores actuales: desde ella no se pueden establecer las claves
   ``content_chunker.*``.

Configuraciones en system.properties
---------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 15 45

   * - Propiedad
     - Predeterminado
     - Descripción
   * - ``content_chunker.enabled``
     - ``false``
     - Interruptor principal de toda la función de chunking de contenido
   * - ``content_chunker.chunker.name``
     - ``length``
     - Método de chunking
   * - ``content_chunker.length.chunk_size``
     - ``800``
     - Número objetivo de caracteres por chunk. Con la división consciente de límites activada
       (valor predeterminado) se trata de un objetivo y no de un máximo estricto: un chunk puede
       ser hasta ``boundary.lookback_percent`` más corto y hasta ``max(lookahead, 32)`` caracteres
       más largo (de 640 a 840 caracteres con los valores predeterminados). Reserve ese margen
       frente al límite de tokens del modelo de embeddings
   * - ``content_chunker.length.overlap``
     - ``0``
     - Número de caracteres que se superponen entre chunks. El punto de reinicio también se
       ajusta a un límite, y ese ajuste solo puede adelantarlo, por lo que la superposición
       efectiva queda entre este valor y el doble de este valor
   * - ``content_chunker.length.boundary.enabled``
     - ``true``
     - Desplaza cada corte a un límite de texto razonable en lugar de cortar exactamente a
       los ``chunk_size`` caracteres. Los candidatos se agrupan en niveles y gana el más cercano
       del nivel más alto presente: salto de línea o fin de frase; si no, separador de cláusula o
       espacio; si no, cambio de sistema de escritura. Con ``false`` se recupera el
       comportamiento anterior de longitud fija
   * - ``content_chunker.length.boundary.lookback_percent``
     - ``20``
     - Hasta dónde se puede buscar un límite antes del corte ideal, como porcentaje de
       ``chunk_size`` (0-50)
   * - ``content_chunker.length.boundary.lookahead_percent``
     - ``5``
     - Hasta dónde se puede buscar un fin de frase o un salto de línea después del corte
       ideal, como porcentaje de ``chunk_size`` (0-25). Solo se usa si no se encontró nada
       antes del corte
   * - ``content_chunker.max_chunks_per_document``
     - ``1000``
     - Número máximo de chunks por documento. Los documentos que superan este valor se marcan
       como ``skipped`` y no reciben embeddings. Como la división consciente de
       límites acorta los chunks, un documento genera entre un 3 % y un 25 % más de chunks que
       con longitud fija, por lo que un corpus de documentos muy grandes puede necesitar un valor
       mayor aquí
   * - ``content_chunker.embedding.name``
     - ``opensearch``
     - Proveedor de embedding (``opensearch`` / ``ollama`` / ``openai`` / ``gemini`` / ``none``)
   * - ``content_chunker.embedding.dimension``
     - ``768``
     - Dimensión del vector de embedding. Este valor se utiliza al crear el mapeo, por lo que
       **debe** coincidir con la dimensión del modelo de embedding que utilice. Este valor tiene
       dos rutas de lectura, con comportamientos distintos. Al crear el mapeo del índice, si el
       valor no está establecido, no es numérico, es 0 o negativo, o supera ``16000`` (el máximo
       propio del plugin k-NN), se aplica ``768`` con una advertencia. En cambio, al ejecutar el
       proceso de embedding no hay ningún valor de respaldo: un valor sin establecer, no numérico
       o 0 o negativo produce un error. Un valor superior a ``16000`` no se rechaza en tiempo de
       ejecución, por lo que solo el mapeo acaba creado con ``768`` y se produce un desajuste de
       dimensión
   * - ``content_chunker.job.concurrency``
     - ``2``
     - Número de workers paralelos para el trabajo del indexador
   * - ``content_chunker.job.bulk_size``
     - ``20``
     - Número de documentos obtenidos y escritos por lote
   * - ``content_chunker.job.max_documents_per_run``
     - ``-1``\ (ilimitado)
     - Número máximo de documentos procesados por ejecución del trabajo. Cualquier valor de
       ``0`` o menor se trata como ilimitado
   * - ``content_chunker.job.retry_failed``
     - ``false``
     - Cuando se establece en ``true``, los documentos que finalizaron la ejecución anterior con
       ``content_chunk_status=fail`` también se incluyen en el objetivo de procesamiento de la
       siguiente ejecución. No existe reintento automático ni seguimiento del número de
       intentos; el flujo de trabajo previsto es corregir la causa subyacente y luego habilitar
       esto temporalmente para reintentar
   * - ``content_chunker.chat.top_k``
     - ``3``
     - Número de chunks seleccionados cuando el modo de búsqueda IA genera una respuesta
   * - ``content_chunker.search.enabled``
     - ``false``
     - Integración con Rank Fusion para la búsqueda semántica (**habilitarlo requiere un
       reinicio**)
   * - ``content_chunker.search.min_score``
     - (sin establecer)
     - Similitud de coseno mínima (0-1) requerida para incluir un resultado. Sin este valor no
       hay corte. En el modo ``ann``, si ``search.knn.space_type`` no es ``cosinesimil`` no se
       puede definir un corte basado en el coseno, por lo que se omite con una advertencia
   * - ``content_chunker.search.knn.method``
     - ``hnsw``
     - Método de índice ANN. Actualmente ``hnsw`` es el único valor aceptado; cualquier otro valor
       aplica el valor predeterminado ``hnsw`` con una advertencia (se refleja en el mapeo;
       cambiarlo requiere recrear el índice)
   * - ``content_chunker.search.knn.engine``
     - ``lucene``
     - Motor ANN. Solo se aceptan ``lucene`` o ``faiss`` (véase Requisitos previos más arriba);
       cualquier otro valor aplica el valor predeterminado ``lucene`` con una advertencia (se
       refleja en el mapeo; cambiarlo requiere recrear el índice)
   * - ``content_chunker.search.knn.space_type``
     - ``cosinesimil``
     - Espacio de distancia. Solo se aceptan ``cosinesimil``, ``innerproduct`` o ``l2``; cualquier
       otro valor aplica el valor predeterminado ``cosinesimil`` con una advertencia (se refleja
       en el mapeo; cambiarlo requiere recrear el índice)
   * - ``content_chunker.search.knn.k``
     - ``100``
     - Número de vecinos recuperados por consulta ANN (se amplía automáticamente para paginación
       profunda)
   * - ``content_chunker.search.knn.param.ef_search``
     - (sin establecer)
     - El parámetro ``ef_search`` para las consultas ANN

.. note::

   Con ``content_chunker.length.boundary.enabled=true`` (valor predeterminado),
   ``content_chunker.length.chunk_size`` pasa a ser un objetivo en lugar de un límite estricto:
   cada corte se desplaza hasta el candidato más cercano del nivel más alto presente en la
   ventana de búsqueda. Un salto de línea o un fin de frase gana a cualquier separador de
   cláusula o espacio por muy atrás que quede este, y esos ganan a un cambio de sistema de
   escritura. Solo se desplaza el punto de corte; no se pierde ningún carácter, por lo que
   concatenar los chunks de un documento sigue reproduciendo exactamente su contenido. La
   búsqueda hacia adelante puede superar ``chunk_size`` en hasta
   ``content_chunker.length.boundary.lookahead_percent``. Puede producirse un segundo exceso,
   independiente, de hasta 32 caracteres cuando un corte caería en medio de un clúster de
   grafemas (una marca combinante, un selector de variación o una secuencia de emojis unida por
   un conector de ancho cero; ZWJ); este ignora ``lookahead_percent`` y puede ocurrir incluso con
   ``0``. Los dos tipos de exceso nunca se producen en el mismo corte, de modo que con los
   valores predeterminados un chunk va de 640 a 840 caracteres. Como los chunks resultan más
   cortos en promedio, un documento genera entre un 3 % y un 25 % más de chunks que con longitud
   fija (véase ``content_chunker.max_chunks_per_document``). Establecer
   ``content_chunker.length.boundary.enabled`` en ``false``, o ambos porcentajes en ``0``,
   reproduce exactamente el comportamiento anterior de longitud fija. Cambiar cualquiera de estos
   ajustes solo afecta a los documentos divididos a partir de ese momento: un documento ya
   almacenado como array de chunks conserva sus límites hasta que se vuelve a rastrear.

.. note::

   Los parámetros HNSW ``m`` y ``ef_construction`` están codificados de forma fija en
   ``doc.json`` (``m=16`` / ``ef_construction=100``) y no se pueden cambiar mediante
   configuración.

Configuración de conexión para el proveedor opensearch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configuración de conexión para el proveedor integrado ``opensearch`` (OpenSearch ML Commons).
Estos se establecen en el mismo archivo ``system.properties`` que se indicó anteriormente.

.. list-table::
   :header-rows: 1
   :widths: 50 20 30

   * - Propiedad
     - Predeterminado
     - Descripción
   * - ``content_chunker.embedding.opensearch.model.id``
     - (requerido)
     - ID del modelo ya desplegado en ML Commons
   * - ``content_chunker.embedding.opensearch.api.url``
     - Dirección del motor de búsqueda
     - Endpoint de la API de ML Commons. Sin establecer, se usa de forma predeterminada el motor
       de búsqueda que |Fess| ya está utilizando (p. ej., ``http://localhost:9200``)
   * - ``content_chunker.embedding.opensearch.username`` / ``password``
     - Credenciales del motor de búsqueda
     - Sin establecer, recurre a las credenciales utilizadas para la conexión al motor de
       búsqueda — pero solo mientras ``api.url`` no esté configurado (es decir, el destino es el
       mismo clúster que |Fess| ya utiliza). Una vez configurado ``api.url``, este mecanismo de
       respaldo no se aplica.
   * - ``content_chunker.embedding.opensearch.timeout``
     - ``60000``
     - Tiempo de espera de la solicitud (ms)
   * - ``content_chunker.embedding.opensearch.connect.timeout``
     - ``5000``
     - Tiempo de espera de conexión (ms)
   * - ``content_chunker.embedding.opensearch.retry.max``
     - ``3``
     - Número de reintentos para errores transitorios (429, 5xx, etc.)
   * - ``content_chunker.embedding.opensearch.retry.base.delay.ms``
     - ``2000``
     - Retraso base de reintento (ms)
   * - ``content_chunker.embedding.opensearch.availability.check.interval``
     - ``60``
     - Intervalo entre verificaciones de disponibilidad del proveedor (segundos)
   * - ``content_chunker.embedding.opensearch.document.prefix`` / ``query.prefix``
     - (vacío)
     - Prefijo antepuesto al texto del documento/consulta antes del embedding

.. warning::

   El contenido de ``system.properties`` se puede consultar en la pantalla de administración
   **Información del sistema > Información de configuración**, en el panel **Propiedades de la
   aplicación**. Allí, ``content_chunker.embedding.opensearch.password`` aparece enmascarado como
   ``XXXXXXXX``, pero ``username`` se muestra tal cual. Además, los valores indicados con
   ``-Dfess.system.<key>`` se muestran **sin enmascarar** en el panel **Propiedades del sistema**
   de esa misma pantalla, así que escriba las credenciales en ``system.properties`` y no en las
   opciones de inicio.

Otros proveedores (ollama / openai / gemini)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El proveedor ``ollama`` (plugin ``fess-llm-ollama``) utiliza el mismo estilo de configuración
bajo el prefijo ``content_chunker.embedding.ollama.`` (``api.url`` es ``http://localhost:11434``
de forma predeterminada, ``model`` es ``embeddinggemma`` de forma predeterminada, y
``document.prefix`` / ``query.prefix`` son ``title: none | text:`` /
``task: search result | query:`` de forma predeterminada respectivamente). Si utiliza un modelo
del estilo de ``nomic-embed-text``, establezca explícitamente ``search_document:`` /
``search_query:`` en ``document.prefix`` / ``query.prefix``. Estos prefijos se concatenan con el
texto que se va a incrustar tal cual (los espacios circundantes no se recortan), por lo que tanto
los valores predeterminados anteriores como ``search_document:`` / ``search_query:``
**incluyen un espacio final**. Recuerde el espacio separador si define un prefijo usted mismo.
Los proveedores ``openai`` y
``gemini`` se configuran de la misma manera, bajo los prefijos
``content_chunker.embedding.openai.`` y ``content_chunker.embedding.gemini.`` respectivamente.
Consulte la documentación de cada plugin para obtener la lista completa de configuraciones.

Procedimiento de configuración (ejemplo con el proveedor opensearch)
========================================================================

Esta sección recorre un ejemplo de configuración utilizando el proveedor integrado ``opensearch``
(ML Commons).

1. Desplegar el modelo de embedding
--------------------------------------

Registre y despliegue un modelo de embedding en OpenSearch ML Commons. En un clúster de un solo
nodo, primero debe aplicar la siguiente configuración.

.. code-block:: bash

    curl -XPUT "http://localhost:9200/_cluster/settings" \
         -H "Content-Type: application/json" -d '
    {"persistent": {"plugins.ml_commons.only_run_on_ml_node": false}}'

Registre y despliegue el modelo (ejemplo: un modelo de embedding de oraciones de 384
dimensiones):

.. code-block:: bash

    # Registrar el modelo (obtenga model_id del task_id de la respuesta)
    curl -XPOST "http://localhost:9200/_plugins/_ml/models/_register" \
         -H "Content-Type: application/json" -d '
    {
      "name": "huggingface/sentence-transformers/all-MiniLM-L6-v2",
      "version": "1.0.2",
      "model_format": "TORCH_SCRIPT"
    }'

    # Comprobar que la tarea ha terminado y obtener el model_id
    # (cuando state pasa a COMPLETED, la respuesta incluye model_id)
    curl "http://localhost:9200/_plugins/_ml/tasks/<task_id>"

    # Desplegar
    curl -XPOST "http://localhost:9200/_plugins/_ml/models/<model_id>/_deploy"

    # Verificar estado: model_state debería ser DEPLOYED
    curl "http://localhost:9200/_plugins/_ml/models/<model_id>"

.. note::

   Un modelo que aún esté en estado ``REGISTERED`` no se puede usar. Asegúrese de desplegarlo y
   confirmar que ``model_state`` pase a ``DEPLOYED``.

2. Configurar |Fess|
-----------------------

``app/WEB-INF/conf/system.properties`` (en RPM/DEB, ``/etc/fess/system.properties``; en Docker,
``/opt/fess/system.properties``. Todo lo siguiente va en ese mismo archivo)::

    content_chunker.enabled=true
    content_chunker.embedding.name=opensearch
    content_chunker.embedding.dimension=384
    content_chunker.embedding.opensearch.model.id=<model_id>

Si además desea utilizar la búsqueda semántica, añada también lo siguiente::

    content_chunker.search.enabled=true

Reinicie |Fess| después de realizar estos cambios.

3. Recrear el índice (al habilitar en una instalación existente)
----------------------------------------------------------------------

El mapeo del campo ``content_chunk_vector`` — incluyendo la dimensión y la configuración del
método ANN que configuró — se aplica **en el momento en que se crea de nuevo el índice**
``fess.search``.

- **Instalaciones nuevas**: si aplica la configuración anterior a ``system.properties`` antes de
  iniciar |Fess| por primera vez, el mapeo correcto se aplica automáticamente cuando se crea el
  índice por primera vez, por lo que este paso no es necesario.
- **Si ya existe un índice** (es decir, si ya ha iniciado |Fess| al menos una vez): el índice en
  ejecución no adopta el nuevo mapeo automáticamente, y un mapeo existente no se puede modificar
  posteriormente. Recree el índice de la siguiente manera:

  Abra **Información del sistema > Mantenimiento**, y en **Reindexación** ejecútela con la
  opción **Actualizar alias** habilitada.

  A continuación, puede confirmar que el índice recreado incluye ``index.knn: true`` en la
  configuración del índice y un mapeo de ``content_chunk_vector`` con la dimensión y la
  configuración del método ANN que estableció (``index.knn`` se aplica a la configuración del
  índice y la configuración del método ANN al mapeo: son destinos distintos).

.. warning::

   La reindexación se ejecuta como una operación en segundo plano asíncrona, y la interfaz de
   administración no muestra ninguna notificación de finalización. ``_cat/indices`` solo muestra
   que el nuevo índice existe (estado, número de documentos, etc.) — no muestra a qué índice
   apuntan los alias. Antes de continuar con el trabajo del indexador que se describe a
   continuación, compruebe en su lugar ``_cat/aliases`` y confirme que tanto ``fess.search`` como
   ``fess.update`` apuntan al nuevo índice; el registro de |Fess| solo registra una advertencia en
   caso de fallo, por lo que un registro silencioso no es prueba de éxito, solo la ausencia de un
   fallo conocido. El índice antiguo (el índice físico al que apuntaba anteriormente el alias
   ``fess.search``, con el nombre ``fess.<timestamp>``) no se elimina automáticamente; elimínelo
   manualmente cuando ya no lo necesite. Mientras existan ambos índices, espere que el uso de
   disco del índice sea aproximadamente el doble de lo habitual.

4. Habilitar el trabajo del indexador
------------------------------------------

El chunking y la generación de embeddings se realizan mediante el trabajo del programador
**Content Chunk Vector Indexer** (ID: ``content-chunk-vector-indexer``; deshabilitado de forma
predeterminada; programado como ``0 13 * * *``).

Habilite este trabajo en **Sistema > Programador**, y luego ejecútelo una vez con **Iniciar
ahora**. A partir de ahí, los documentos no procesados se procesan según la programación
configurada (de forma predeterminada, todos los días a las 13:00), con independencia de que un
rastreo haya terminado o no. Este trabajo no está encadenado al trabajo de rastreo, así que si
desea procesarlos justo después de un rastreo, programe este trabajo a una hora posterior a la
hora prevista de finalización del rastreo.

.. note::

   En una implementación multinodo, recomendamos anclar este trabajo para que se ejecute
   exactamente en un nodo. Ejecutarlo en todos los nodos a la vez no rompe la corrección, pero
   cada nodo procesa y embebe los mismos documentos de forma redundante, multiplicando la carga
   y el coste en su proveedor de embedding por el número de nodos.

   Anclarlo requiere **ambas** de las siguientes configuraciones — una sola de ellas no ancla el
   trabajo.

   1. **En el nodo donde desea ejecutar el trabajo**: establezca
      ``scheduler.target.name=<algún identificador>`` en
      ``app/WEB-INF/classes/fess_config.properties`` (en RPM/DEB,
      ``/etc/fess/fess_config.properties``; o mediante
      ``-Dfess.config.scheduler.target.name=<algún identificador>``), y luego reinicie ese nodo.
      (El valor predeterminado está vacío; deje todos los demás nodos con el valor
      predeterminado.)
   2. En la interfaz de administración, en **Sistema > Programador**, abra el trabajo Content
      Chunk Vector Indexer y cambie su campo **Objetivo** de ``all`` al mismo identificador que
      estableció en el paso 1, y luego guarde.

   Consulte :doc:`../admin/scheduler-guide` para saber qué significa el campo **Objetivo**.
   Establecer ``scheduler.target.name`` por sí solo no ancla el trabajo si el campo
   **Objetivo** se deja en ``all``: **no quedará anclado**. ``all`` se trata como un valor
   especial que siempre coincide, por lo que solo el paso 1 o solo el paso 2 no son suficientes —
   debe realizar ambos.

.. warning::

   Una vez anclado el trabajo, pulse **Iniciar ahora** también **desde la interfaz de
   administración del nodo en el que estableció el identificador en el paso 1**. Si lo pulsa en
   un nodo que no es el destino, la pantalla muestra igualmente el mensaje de éxito ("Se ha
   iniciado el trabajo …"), pero el trabajo **no se ejecuta**, porque el campo **Objetivo** no
   coincide (en el registro de ese nodo solo aparece una línea ``Ignoring job`` de nivel INFO).

5. Verificar el estado de procesamiento
--------------------------------------------

Puede verificar el resultado de cada documento en su campo ``content_chunk_status``.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Valor
     - Significado
   * - (campo ausente)
     - Aún no procesado (se recogerá en la próxima ejecución del trabajo). Los documentos
       también vuelven a este estado después de ser rastreados nuevamente
   * - ``done``
     - Chunking y generación de vectores completados
   * - ``chunked``
     - Solo chunking completado (modo solo chunking). Además del caso
       ``embedding.name=none``, este estado también se produce cuando el plugin del proveedor
       indicado en ``embedding.name`` no está instalado
   * - ``skipped``
     - Procesamiento omitido (p. ej., se superó ``max_chunks_per_document``)
   * - ``fail``
     - Procesamiento fallido (revise los registros)

Puede verificar la distribución de estados consultando directamente el motor de búsqueda::

    curl -XPOST "http://localhost:9200/fess.search/_search" \
         -H "Content-Type: application/json" -d '
    {"size": 0, "aggs": {"status": {"terms": {"field": "content_chunk_status", "missing": "pending"}}}}'

Gracias a la opción ``missing``, los documentos que no tienen ``content_chunk_status`` (es decir,
los que aún no se han procesado) se agrupan en un bucket con la clave ``pending``.

Comportamiento de la búsqueda semántica
==========================================

Establecer ``content_chunker.search.enabled=true`` registra el buscador semántico con Rank
Fusion, que luego fusiona los resultados de la búsqueda por palabras clave con los resultados de
la búsqueda vectorial. (Consulte :doc:`rank-fusion` para saber cómo funciona Rank Fusion.)
En el momento de la búsqueda también se consulta ``content_chunker.enabled``: si
``content_chunker.enabled=false`` o ``content_chunker.embedding.name=none``, la búsqueda
semántica no se ejecuta aunque el buscador ya esté registrado (esta comprobación se realiza en
cada solicitud, por lo que no hace falta reiniciar).

.. warning::

   Dado que el buscador semántico se registra al iniciar, **habilitarlo requiere un reinicio**.
   Deshabilitarlo (volver a establecer el valor en ``false``) se evalúa por solicitud, por lo que
   surte efecto de inmediato.

Modo exact y modo ann
------------------------

El método de búsqueda se elige automáticamente según el estado del índice.

.. list-table::
   :header-rows: 1
   :widths: 12 44 44

   * - Modo
     - Condición
     - Características
   * - ``ann``
     - Un índice que tiene configuración de ``index.knn`` y método ANN
     - Búsqueda aproximada del vecino más cercano usando HNSW. Adecuado para índices grandes
   * - ``exact``
     - Cualquier otro caso (un índice al que le falta ``index.knn`` o la configuración del método
       ANN, incluido el caso en que falla la comprobación del estado del índice)
     - Cálculo exacto de similitud de coseno contra cada vector. Adecuado para índices pequeños
       a medianos

Cualquier índice ``fess.search`` creado nuevo bajo |Fess| 15.9 siempre tiene configuración de
``index.knn`` y de método ANN, independientemente del valor de
``content_chunker.search.enabled`` — por lo que normalmente siempre se usa el modo ``ann``. El
modo ``exact`` es un mecanismo de respaldo para índices más antiguos creados antes de que
existiera este mecanismo. Dado que la configuración k-NN no se puede añadir a un índice existente
posteriormente, cambiar un índice en modo ``exact`` al modo ``ann`` requiere recrear el índice
(consulte :ref:`semantic-search-migration`). Tenga en cuenta que el resultado de esta
comprobación se almacena en caché durante 60 segundos, por lo que justo después de recrear el
índice el cambio puede tardar hasta 60 segundos en reflejarse.

Corte de puntuación
----------------------

Establecer ``content_chunker.search.min_score`` en una similitud de coseno (0-1) excluye de los
resultados de la búsqueda semántica los documentos cuyo mejor chunk no alcanza ese valor (la
puntuación de un documento es la de su mejor chunk, de modo que el corte actúa a nivel de
documento, no de chunk individual). Úselo para controlar el número de resultados cuando las
consultas sin superposición de vocabulario coinciden de forma demasiado amplia::

    content_chunker.search.min_score=0.4

El valor configurado se interpreta como similitud de coseno tanto en el modo ``exact`` como en el
modo ``ann`` (internamente se convierte a la escala de puntuación de cada modo).

.. note::

   Este corte solo se aplica cuando ``content_chunker.search.knn.space_type`` es
   ``cosinesimil`` (el valor predeterminado). En un índice en modo ``ann`` configurado con
   ``innerproduct`` o ``l2`` no se puede definir la similitud de coseno, por lo que el corte se
   omite después de registrar una advertencia una sola vez.

Limitaciones
--------------

- **La búsqueda semántica se omite para las consultas que contienen sintaxis de búsqueda** y
  solo se ejecuta la búsqueda por palabras clave. La comprobación se realiza sobre la cadena de
  consulta ya **ensamblada**, y se activa cuando esta contiene alguno de estos elementos: ``"``
  ``(`` ``)`` ``:`` ``[`` ``]`` ``{`` ``}`` ``^`` ``~`` ``*`` ``?`` ``\``, ``&&``, ``||``, un
  ``+`` o un ``-`` al principio o justo después de un espacio, o las palabras en mayúsculas
  ``AND`` / ``OR`` / ``NOT`` / ``TO``. Por eso, aunque el usuario no escriba ninguna sintaxis de
  búsqueda, las siguientes operaciones también se omiten:

  - Seleccionar una etiqueta (internamente se añade ``label:"..."``)
  - Especificar un criterio de ordenación (internamente se añade ``sort:...``)
  - Filtrar mediante facetas (internamente se añade ``filetype:...``, etc.)
  - En la búsqueda avanzada: búsqueda de frase, términos excluidos, tipo de archivo, sitio y
    rango de fechas
  - Un término de búsqueda que tiene consultas relacionadas configuradas (internamente se
    expande a ``("A" OR "B")``)

  El ``?`` de medio ancho (ASCII) también está incluido, por lo que una frase en lenguaje
  natural terminada en signo de interrogación, como «¿Qué es …?», se omite (el ``？`` de ancho
  completo no cuenta).
- También se omite cuando se combina con la búsqueda por geolocalización (un filtro geo) o la
  búsqueda de documentos similares.
- En las páginas profundas se desactiva el propio Rank Fusion y los resultados provienen solo de
  la búsqueda por palabras clave. El límite lo determina ``rank.fusion.window_size``
  (predeterminado ``200``), lo que con los valores predeterminados corresponde a los resultados a
  partir del número 101.
- Si el proveedor de embedding no está disponible o se produce un error de búsqueda, |Fess|
  vuelve automáticamente a los resultados basados solo en palabras clave (la búsqueda en sí nunca
  falla como resultado).
- El control de acceso basado en roles y en el host virtual también se aplica a los resultados de
  la búsqueda semántica.

Integración con el modo de búsqueda IA
==========================================

Cuando el modo de búsqueda IA (:doc:`rag-chat`, ``rag.chat.enabled=true``) está habilitado, para
los documentos cuyo ``content_chunk_status`` es ``done``, la generación de respuestas calcula la
similitud con cada chunk y usa solo los ``content_chunker.chat.top_k`` chunks más relevantes
(predeterminado: ``3``) como contexto del LLM.

Lo que se convierte en embedding en ese momento no es la frase del usuario tal cual, sino **la
consulta de búsqueda que genera el LLM en la fase de detección de la intención** (si se produce
una nueva búsqueda, se utiliza la consulta regenerada). Cuando no se genera ninguna consulta de
búsqueda —por ejemplo, si se pide el resumen de un documento— no se realiza ninguna selección de
chunks.

Como resultado, incluso para documentos largos solo se pasan al LLM las partes relevantes, lo
que puede mejorar la precisión de la respuesta y reducir el uso de tokens. En los documentos
cuyo ``content_chunk_status`` es ``chunked`` (tienen chunks pero no vectores), la selección de
chunks se realiza por coincidencia de palabras clave (resaltado) en lugar de por cálculo de
similitud. Los documentos con ``skipped`` / ``fail`` y los que aún no se han procesado siguen
usando el cuerpo completo (o un fragmento resaltado) como antes.

Este comportamiento es independiente de ``content_chunker.search.enabled``, pero requiere que
``content_chunker.enabled`` esté habilitado. Tenga en cuenta además que el texto resultante de
concatenar los chunks seleccionados también se trunca según
``rag.chat.content.fulltext.max.length`` (predeterminado ``3000``), por lo que aumentar
``content_chunker.chat.top_k`` o ``content_chunker.length.chunk_size`` no hace que el número de
caracteres entregado al LLM supere ese límite.

.. _semantic-search-migration:

Migración desde la versión 15.7 o anterior
==============================================

Si está actualizando |Fess| desde la versión 15.7 o anterior, su situación corresponde a uno de
los cuatro patrones siguientes, según cómo utilice actualmente estas funciones. Siga las
instrucciones del patrón que se aplique a su caso.

Instalaciones nuevas
-----------------------

No se necesita trabajo adicional. Si desea usar la búsqueda vectorial, simplemente configure
``system.properties`` según la sección *Referencia de configuración* de esta página antes de
iniciar |Fess| por primera vez; el mapeo correcto se aplica automáticamente cuando se crea el
índice por primera vez. (Consulte *Procedimiento de configuración* más arriba para los pasos
concretos.)

.. note::

   Si ya ha iniciado |Fess| al menos una vez (es decir, el índice ya existe), siga en su lugar
   uno de los patrones para *usuarios existentes* que se indican más abajo.

Usuarios existentes que no desean la búsqueda vectorial
-----------------------------------------------------------

No se necesita ningún trabajo. ``content_chunker.enabled`` y
``content_chunker.search.enabled`` son ambos ``false`` de forma predeterminada, por lo que sus
resultados de búsqueda y el comportamiento del índice existente no cambian después de la
actualización. El nuevo trabajo del programador **Content Chunk Vector Indexer** se registra
automáticamente al iniciar, pero como está deshabilitado de forma predeterminada nunca se
ejecuta, y el buscador semántico nunca se registra con Rank Fusion (este trabajo se registra en
cada arranque, así que si lo elimina desde la interfaz de administración se vuelve a crear
—deshabilitado— en el siguiente arranque).

.. note::

   Aunque no utilice la búsqueda vectorial, cualquier **creación de un índice nuevo** (incluida
   la reindexación) a partir de |Fess| 15.9 aplica el mapeo que contiene
   ``content_chunk_vector`` (de tipo ``knn_vector``) y ``index.knn: true``. En una configuración
   en la que OpenSearch no tiene instalado el plugin k-NN, la creación del índice falla en ese
   momento. Consulte *Requisitos previos* en esta misma página para más detalles.

Usuarios existentes que desean habilitar la búsqueda vectorial
--------------------------------------------------------------------

El índice en ejecución no adopta el nuevo mapeo automáticamente, por lo que se requieren los
siguientes pasos.

1. Aplique la configuración a ``system.properties`` como se describe en *Referencia de
   configuración* en esta página (consulte *Procedimiento de configuración* más arriba para los
   pasos concretos al usar el proveedor opensearch).
2. Reinicie |Fess|.
3. En la interfaz de administración, ejecute la **Reindexación** en **Información del sistema >
   Mantenimiento** con la opción **Actualizar alias** habilitada. Esto se ejecuta en segundo plano
   sin notificación de finalización. ``_cat/indices`` solo muestra que el nuevo índice existe, no
   si los alias ya cambiaron — compruebe en su lugar ``_cat/aliases`` y confirme que
   ``fess.search``/``fess.update`` apuntan al nuevo índice (el registro de |Fess| solo advierte en
   caso de fallo, así que el silencio no es prueba de éxito). El índice antiguo no se elimina
   automáticamente (elimínelo manualmente cuando ya no lo necesite), y el uso de disco del índice
   se duplica aproximadamente hasta entonces.
4. Solo después de confirmar que el cambio de alias anterior ha finalizado, habilite y ejecute el
   trabajo Content Chunk Vector Indexer en **Sistema > Programador** (no necesita volver a
   rastrear: el trabajo lee ``content`` desde el ``_source`` del índice existente para dividirlo
   en chunks y generar los embeddings).

.. note::

   Si en el paso 1 aplica también ``content_chunker.search.enabled=true``, entre el reinicio del
   paso 2 y la finalización del paso 4 cada búsqueda generará únicamente el embedding de la
   consulta, sin que ese trabajo se refleje en los resultados. Si utiliza un proveedor facturado
   por uso, como ``openai`` o ``gemini``, aplique ``content_chunker.search.enabled=true`` y
   reinicie una vez completado el paso 4.

Si estaba utilizando el plugin fess-webapp-semantic-search
------------------------------------------------------------------

El plugin ``fess-webapp-semantic-search``, que proporcionaba la búsqueda semántica en |Fess|
15.7 y versiones anteriores, se ha incorporado al núcleo en la versión 15.9 y ahora es
**innecesario (obsoleto)**. Además de los pasos descritos en *Usuarios existentes que desean
habilitar la búsqueda vectorial* anteriores, también debe hacer lo siguiente.

1. **Eliminar el plugin**: elimine ``fess-webapp-semantic-search-*.jar`` de
   ``app/WEB-INF/plugin/`` (en Docker, excúyalo de ``FESS_PLUGINS``).

2. **Eliminar la configuración antigua**: elimine todas las opciones de inicio
   ``-Dfess.semantic_search.*``. Además, si había especificado
   ``-Drank.fusion.searchers=default,semantic`` para el plugin antiguo, elimínelo también.
   Dejarlo excluye al nuevo buscador semántico (``semantic_chunk``) de Rank Fusion y registra
   una advertencia al iniciar.

3. **Desvincular la pipeline de ingesta antigua**: si había configurado
   ``-Dfess.semantic_search.pipeline``, el plugin antiguo incrusta ``default_pipeline`` (una
   pipeline de ingesta para la búsqueda neuronal) en la configuración del índice al crearlo.
   **Eliminar el plugin no elimina la pipeline** — permanece adjunta al índice y sigue
   ejecutándose —, por lo que debe desvincularla **antes** de ejecutar la reindexación descrita
   en *Usuarios existentes que desean habilitar la búsqueda vectorial*. El índice nuevo que
   resulta de la reindexación ya no lleva ese ajuste, así que hacerlo después no sirve de nada.
   Compruebe con ``_cat/aliases`` a qué ``fess.<timestamp>`` apunta ``fess.search`` e indique el
   nombre del índice real, no el del alias::

       curl -XPUT "http://localhost:9200/fess.<timestamp>/_settings" \
            -H "Content-Type: application/json" -d '
       {"index": {"default_pipeline": "_none"}}'

   Aunque la desvincule de la configuración del índice, la propia pipeline de ingesta permanece
   en el motor de búsqueda. Si no va a volver a utilizarla, elimínela::

       curl -XDELETE "http://localhost:9200/_ingest/pipeline/<nombre_de_pipeline>"

4. **Añadir la nueva configuración**: configure ``content_chunker.*`` en
   ``system.properties`` como se describe en *Referencia de configuración* en esta página. Si
   continúa utilizando su modelo de ML Commons existente, establezca
   ``content_chunker.embedding.name=opensearch`` y coloque su ``model_id`` existente en
   ``content_chunker.embedding.opensearch.model.id``.

5. **Recrear el índice y ejecutar el trabajo**: el campo vectorial que almacenaba el plugin
   antiguo (``content_vector`` en la configuración predeterminada) y el campo
   ``content_chunk_vector`` que utiliza la nueva función del núcleo son campos distintos, por lo
   que los vectores antiguos no se pueden aprovechar con la nueva función. En cambio, la
   reindexación copia ``_source`` tal cual, así que esos vectores antiguos sí se duplican en el
   índice nuevo y siguen consumiendo disco a través del mapeo dinámico. Se recomienda eliminarlos
   **antes** de la reindexación (si cambió el nombre del campo, adapte el ejemplo)::

       curl -XPOST "http://localhost:9200/fess.search/_update_by_query" \
            -H "Content-Type: application/json" -d '
       {
         "query": {"exists": {"field": "content_vector"}},
         "script": {"source": "ctx._source.remove(\"content_vector\")"}
       }'

   A continuación, ejecute la **Reindexación** en **Información del sistema > Mantenimiento**, y
   luego habilite y ejecute el trabajo Content Chunk Vector Indexer para regenerar los vectores.

Notas
=======

Cambiar el modelo de embedding (dimensión)
----------------------------------------------

Para cambiar a un modelo de embedding con una dimensión diferente, siga este orden.

1. Elimine los vectores antiguos existentes. Si reindexa con vectores de la dimensión antigua
   todavía presentes, el nuevo mapeo no los acepta y esos documentos no se copian al índice
   nuevo, mientras el proceso sigue adelante. Como |Fess| solo comprueba el estado HTTP de la
   reindexación, la interfaz de administración no muestra ningún error y aun así se pierden
   documentos::

       curl -XPOST "http://localhost:9200/fess.search/_update_by_query" \
            -H "Content-Type: application/json" -d '
       {
         "query": {"exists": {"field": "content_chunk_status"}},
         "script": {"source": "ctx._source.remove(\"content_chunk_vector\"); ctx._source.remove(\"content_chunk_status\")"}
       }'

   .. note::

      También puede indicar como destino ``fess.update`` (el alias de actualización desde el que
      la reindexación lee los documentos). Además, esta operación deja el campo ``content`` como
      un array de chunks: en la siguiente ejecución del trabajo se vuelve a concatenar y a
      dividir, por lo que si ha establecido ``content_chunker.length.overlap`` en un valor
      distinto de 0, las partes solapadas quedarán duplicadas en la nueva división. Si eso le
      preocupa, vuelva a rastrear los documentos afectados.

2. Cambie ``content_chunker.embedding.dimension`` y la configuración del modelo de su proveedor.
3. Recree el índice siguiendo *3. Recrear el índice (al habilitar en una instalación existente)*
   del *Procedimiento de configuración*, y vuelva a ejecutar el trabajo del indexador.

Uso de disco
--------------

Los vectores de chunks se conservan en ``_source`` además de las estructuras del índice de
búsqueda, por lo que cada documento consume espacio de disco adicional proporcional a su número
de chunks multiplicado por la dimensión del vector. Si el espacio en disco se convierte en un
problema, ajuste ``content_chunker.length.chunk_size`` o
``content_chunker.max_chunks_per_document``.

Modo solo chunking
---------------------

Establecer ``content_chunker.embedding.name=none`` realiza solo el chunking, sin generar
vectores de embedding (``content_chunk_status`` pasa a ``chunked``). Esto le permite ejecutar el
chunking con antelación, antes de que su proveedor de embedding esté listo; una vez que configure
un proveedor más adelante y vuelva a ejecutar el trabajo, se generan vectores para los chunks ya
almacenados, sin volver a dividirlos.

Configuración de memoria para corpus grandes
-------------------------------------------------

La JVM hija del trabajo del indexador se inicia con ``jvm.chunk.options`` en
``fess_config.properties`` (opciones de JVM que por defecto incluyen ``-Xms128m -Xmx1g``). Dado
que ``content_chunker.job.max_documents_per_run`` es ilimitado de forma predeterminada, una sola
ejecución mantiene en memoria todos los ID de documentos pendientes. Cada ID de documento es un
resumen SHA-512 (128 caracteres) y ocupa unos 200 bytes en el heap; el propio procesamiento de
chunks consume además entre 200 y 250 MB. Por eso, a partir de **un corpus de entre 1 y 2
millones de documentos**, aumente el valor de ``-Xmx`` en ``jvm.chunk.options`` o establezca un
valor finito en ``content_chunker.job.max_documents_per_run`` para repartir el trabajo en varias
ejecuciones. ``jvm.chunk.options`` se sobrescribe en
``app/WEB-INF/classes/fess_config.properties`` (en RPM/DEB,
``/etc/fess/fess_config.properties``); consulte :doc:`setup-memory` para entender cómo funcionan
las opciones de JVM.

El mismo valor predeterminado ilimitado tiene una consecuencia de costo con un proveedor de
embedding facturado por uso (``openai``, ``gemini``): la primera ejecución del indexador genera
los embeddings de todo el corpus existente de una sola vez y factura todo eso de golpe. Establezca
un valor finito para ``content_chunker.job.max_documents_per_run`` para repartir ese costo entre
varias ejecuciones.

Referencias
=============

- :doc:`rank-fusion` - Configuración de Rank Fusion (búsqueda híbrida)
- :doc:`rag-chat` - Configuración del modo de búsqueda IA
- :doc:`llm-overview` - Descripción general de la integración LLM
- :doc:`llm-ollama` - Configuración de Ollama
- :doc:`setup-memory` - Configuración de memoria de la JVM
- :doc:`../install/upgrade` - Procedimiento de actualización
