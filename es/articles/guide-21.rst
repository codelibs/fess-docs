=============================================
Buscar imágenes y texto a la vez (multimodal)
=============================================

Introducción
============

Los servidores de archivos y los sitios internos contienen gran cantidad de imágenes, como fotos de productos o de obras, cuyo contenido no se describe más que por el nombre del archivo.
Con la búsqueda por palabras clave, solo se pueden encontrar imágenes a partir de las palabras que figuran en el nombre del archivo o en los metadatos.

Con el plugin de búsqueda multimodal ``fess-webapp-multimodal`` puede buscar, con palabras como "atardecer en la montaña" o "perro", imágenes cuyo contenido se aproxima a ellas.
En este artículo realizamos lo siguiente con Fess 15.9.

- Iniciar el entorno Docker de prueba ``docker-multimodalsearch`` en su versión 15.9, rastrear imágenes y buscarlas
- Comprobar en la respuesta de la API de búsqueda que las imágenes se encontraron mediante búsqueda vectorial
- Repasar la configuración necesaria para incorporarlo a un Fess existente y los puntos en los que es fácil tropezar

Qué se puede hacer y qué no
===========================

Primero, delimitamos el alcance de ``fess-webapp-multimodal`` en 15.9.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Elemento
     - Comportamiento en 15.9
   * - Dirección de la búsqueda
     - Solo la búsqueda de imágenes a partir de texto. No existe una función para subir una imagen y buscar imágenes similares
   * - Imágenes que se vectorizan
     - Solo los archivos cuyo tipo MIME es ``image/gif``, ``image/jpeg`` o ``image/png``. Los archivos BMP y TIFF no se vectorizan
   * - Imágenes dentro de PDF o documentos de Office
     - No se vectorizan. Para buscar el texto que aparece en las imágenes, use OCR (una función aparte)
   * - Documentos que no son imágenes
     - Se buscan como de costumbre mediante búsqueda por palabras clave (BM25). En los resultados aparecen mezcladas imágenes y documentos de texto
   * - Términos de búsqueda en idiomas distintos del inglés (por ejemplo, español)
     - Se necesita un modelo CLIP multilingüe. El modelo predeterminado de ``docker-multimodalsearch`` es un modelo multilingüe que, según su README, no se limita al inglés (el README pone como ejemplo el japonés)
   * - Búsqueda semántica de texto
     - No se puede usar en el mismo Fess (véase más adelante)

Para OCR, consulte `Configuración de OCR <https://fess.codelibs.org/es/stable/config/crawler-ocr.html>`__.

Funcionamiento
==============

CLIP es un modelo que convierte texto e imágenes en un mismo espacio vectorial.
El vector del texto "perro" queda cerca de los vectores de las imágenes en las que aparece un perro, por lo que es posible buscar imágenes según la cercanía entre vectores.

Desde Fess 15.8, el almacenamiento y la búsqueda de vectores los realiza el propio Fess.
El plugin solo añade la parte que se comunica con el servidor CLIP.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Momento
     - Procesamiento
   * - Durante el rastreo
     - Las imágenes GIF/JPEG/PNG se envían al servidor CLIP, se convierten en vectores y se escriben en el campo vectorial ``content_chunk_vector`` de Fess
   * - Durante la búsqueda
     - El término de búsqueda se convierte en un vector en el servidor CLIP y se buscan las imágenes cercanas. Esta búsqueda se ejecuta en paralelo con la búsqueda por palabras clave, y ambas se integran en un único resultado mediante Rank Fusion
   * - Resultados
     - Los documentos encontrados por la búsqueda vectorial llevan ``multi_modal`` en el campo ``searcher``. Los encontrados por la búsqueda por palabras clave llevan ``default``

Para el funcionamiento de Rank Fusion, consulte `Búsqueda Híbrida y Rank Fusion (Semántica + Palabras Clave) <https://fess.codelibs.org/es/stable/config/rank-fusion.html>`__.

Probarlo con docker-multimodalsearch
====================================

``docker-multimodalsearch`` es un entorno Docker Compose que reúne los contenedores y la configuración necesarios para probar la búsqueda multimodal de inmediato.
Con la etiqueta ``v15.9.0`` se inician los siguientes servicios.

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - Servicio
     - Función
   * - ``fess01``
     - El propio Fess. La imagen es ``ghcr.io/codelibs/fess:15.9.0-noble`` y, al arrancar, incorpora el plugin ``fess-webapp-multimodal:15.9.0``. La página de búsqueda usa el tema de galería de imágenes ``mosaic``
   * - ``search01``
     - OpenSearch 3.9.0. El puerto 9200 solo se publica en la interfaz de bucle invertido del host (127.0.0.1)
   * - ``clip_server``
     - El servidor CLIP. El modelo predeterminado es el multilingüe ``xlm-roberta-base-ViT-B-32::laion5b-s13b-b90k`` (512 dimensiones) y se ejecuta en la CPU
   * - ``content``
     - Un nginx que sirve las imágenes de ejemplo en ``http://content/``. Solo es accesible desde la red entre contenedores
   * - ``init-fess-verify``
     - Se ejecuta una sola vez al arrancar, comprueba que el campo vectorial del índice coincide con la configuración y termina

Requisitos previos
------------------

- Docker (el comando ``docker compose``), Git, bash
- Conexión a Internet (para descargar las imágenes y el modelo CLIP; según el README, el modelo ocupa unos 1,6 GB)
- En Linux, aumente ``vm.max_map_count`` para OpenSearch (igual que en los pasos de preparación de :doc:`guide-02`)

Obtener la versión 15.9
-----------------------

La rama predeterminada de ``docker-multimodalsearch`` sigue a la próxima versión en desarrollo, así que obtenga la etiqueta ``v15.9.0``.

::

    $ git clone --branch v15.9.0 https://github.com/codelibs/docker-multimodalsearch.git
    $ cd docker-multimodalsearch
    $ cp .env.example .env

Abra ``.env`` y cambie el origen de los temas a la rama de 15.9.

::

    FESS_THEMES_REF=15.9.x

En ``v15.9.0``, ``.env.example`` sigue indicando ``FESS_THEMES_REF=main``, pero el tema ``mosaic`` de ``main`` en ``fess-themes`` es ahora para Fess 15.10 y posteriores (``minFessVersion: 15.10``).
El tema ``mosaic`` para 15.9 está en la rama ``15.9.x``.

Deje ``FESS_VERSION=15.9.0`` y ``FESS_PLUGINS=fess-webapp-multimodal:15.9.0`` de ``.env`` tal como están.
La versión del plugin debe coincidir con la de Fess.

Configurar e iniciar
--------------------

::

    $ bash bin/setup.sh
    $ docker compose up -d

``bin/setup.sh`` crea los directorios de datos, obtiene el tema y prepara el script de generación de miniaturas.
En el primer ``docker compose up -d`` se construye la imagen de ``clip_server`` y se descarga el modelo CLIP.
``fess01`` espera a que ``clip_server`` esté listo antes de arrancar, por lo que la primera vez tarda unos minutos.

Compruebe el estado con los siguientes comandos.

::

    $ docker compose ps -a
    $ docker compose logs init-fess-verify

Si ``fess01`` pasa a ``(healthy)``, ``init-fess-verify`` termina con ``Exited (0)`` y el registro contiene la siguiente línea, el campo vectorial se ha creado según la configuración.

::

    [init-fess-verify] OK: dimension=512, engine=lucene, space_type=cosinesimil, index.knn=true

Rastrear las imágenes de ejemplo
--------------------------------

Descargue las imágenes de ejemplo (animales, vehículos, comida, naturaleza, edificios), además de archivos HTML y PDF.

::

    $ bash bin/fetch-sample-images.sh

A continuación, rastree desde la consola de administración.

1. Inicie sesión en ``http://localhost:8080/admin/`` con ``admin`` / ``admin`` y, si se le solicita, establezca una nueva contraseña
2. En [Rastreador] > [Web], haga clic en [Crear nuevo], introduzca ``content`` en "Nombre" y ``http://content/`` en "URLs", y haga clic en [Crear]
3. En [Sistema] > [Programador], abra "Default Crawler" y haga clic en [Iniciar ahora]
4. En [Información del sistema] > [Información de rastreo], espere a que termine el rastreo

Los vectores de las imágenes se escriben durante este rastreo.
Según el README, con los ejemplos incluidos se registran 43 documentos (37 imágenes, 5 HTML, 1 PDF).
La cifra es orientativa.

Buscar
------

Abra ``http://localhost:8080/`` y busque ``perro``, ``atardecer en la montaña`` o ``mountain sunset``.
El modelo predeterminado es multilingüe, por lo que se devuelven imágenes tanto en español como en inglés.

El tema ``mosaic`` muestra los resultados como una galería de miniaturas y marca cada resultado con la insignia "Palabra clave", "Visual" o "Combinada".
"Visual" indica similitud de imagen, y "Combinada", un resultado encontrado tanto por palabras clave como por la imagen.

Las miniaturas las genera un trabajo en segundo plano después del rastreo.
Si justo después del rastreo no se muestran algunas, espere un momento y vuelva a cargar la página.

Para detenerlo, ejecute ``docker compose down``.
Los datos se conservan en ``./data``.

Comprobar el funcionamiento
===========================

Ver ``searcher`` en la API de búsqueda
--------------------------------------

Si se usó la búsqueda vectorial puede comprobarse con ``searcher`` en la respuesta de la API de búsqueda.
Si dispone de ``jq``, ejecute lo siguiente.

::

    $ curl -s -G 'http://localhost:8080/api/v2/search' --data-urlencode 'q=perro' | jq -c '.response.data[] | {url, searcher}'

Los valores de ``searcher`` significan lo siguiente.

- ``["multi_modal"]``: encontrado por similitud de imagen
- ``["default"]``: encontrado por búsqueda por palabras clave
- Contiene ambos: encontrado por las dos vías

Si todos los resultados tienen solo ``["default"]``, la búsqueda vectorial no se ejecutó.
Compruebe si la búsqueda encaja en alguno de los casos de la sección "Búsquedas en las que no se ejecuta la búsqueda vectorial" que sigue.

De forma predeterminada, ``searcher`` no se incluye en la respuesta de la API.
``docker-multimodalsearch`` establece ``query.additional.api.response.fields=searcher`` de ``fess_config.properties`` mediante una opción de arranque (``-Dfess.config.query.additional.api.response.fields=searcher``), por lo que sí se incluye en la respuesta.
Para más detalles sobre la API de búsqueda, consulte `API de búsqueda <https://fess.codelibs.org/es/stable/api/api-search.html>`__.

Comprobar si se escribieron los vectores
----------------------------------------

Si la búsqueda no devuelve ninguna imagen, cuente en OpenSearch los documentos que tienen vectores (en este entorno, el puerto 9200 solo se puede usar desde el host).

::

    $ curl -s 'http://localhost:9200/fess.search/_count' -H 'Content-Type: application/json' -d '{"query":{"nested":{"path":"content_chunk_vector","query":{"exists":{"field":"content_chunk_vector.vector"}}}}}'

Si ``count`` es 0, no se crearon vectores durante el rastreo.
Compruebe en ``docker compose logs fess01`` y en los registros del rastreador si aparece la advertencia ``Failed to convert an image to a vector.``.

Búsquedas en las que no se ejecuta la búsqueda vectorial
--------------------------------------------------------

En los siguientes casos, la búsqueda vectorial no se ejecuta y los resultados proceden solo de la búsqueda por palabras clave.
No se produce ningún error y es fácil no darse cuenta, así que preste atención.

- Búsquedas que especifican un orden (el parámetro ``sort``). Si configura el "Valor de ordenación por defecto" en [Sistema] > [General], el tema ``mosaic`` envía ese valor como ``sort``, de modo que también las búsquedas normales entran en este caso
- Búsquedas que usan sintaxis de búsqueda en el término: frases (``"atardecer en la montaña"``), comodines (``dog*``), realce (``dog^2``), exclusión (``-dog``), ``allintitle:``, ``allinurl:``
- Búsquedas sin término que solo tienen condiciones de filtro, como etiquetas
- Páginas a partir del resultado 101 (cuando la posición inicial es igual o superior a la mitad de ``rank.fusion.window_size`` (valor predeterminado: 200))
- Cuando no es posible conectarse al servidor CLIP (``fess.log`` muestra un WARN como ``Embedding provider is unavailable``)

En cambio, si junto con el término de búsqueda usa una especificación de campo como ``filetype:jpg`` o un filtro por etiqueta, la búsqueda vectorial sí se ejecuta y se restringe con esa condición.

Incorporarlo a un Fess existente
================================

Para incorporarlo a un Fess 15.9 existente sin usar ``docker-multimodalsearch``, siga estos pasos.

1. Instalar el plugin
---------------------

Instale ``fess-webapp-multimodal`` 15.9.x de una de las siguientes formas y reinicie Fess.

- En la consola de administración, [Sistema] > [Plugin] > [Instalar]
- ``bin/fess-setup install plugin fess-webapp-multimodal:15.9.0``
- En Docker, añada ``fess-webapp-multimodal:15.9.0`` a la variable de entorno ``FESS_PLUGINS``

Para más detalles, consulte `Complemento <https://fess.codelibs.org/es/stable/admin/plugin-guide.html>`__.

2. Preparar un servidor CLIP
----------------------------

El plugin se conecta a una API HTTP con el mismo formato que el servidor CLIP de Jina.
Usa ``POST /post`` para la vectorización y ``GET /health`` para comprobar la conexión.
Si ``/health`` no devuelve 2xx, sigue funcionando con la búsqueda vectorial desactivada.
El destino se indica con ``content_chunker.embedding.clip.api.url``, cuyo valor predeterminado es ``http://localhost:51000``.

- El ``docker/compose.yaml`` del repositorio del plugin inicia ``jinaai/clip-server``. Su configuración ``docker/clip_config.yaml`` no especifica ningún modelo, así que se usa el modelo predeterminado (según el README, ViT-B/32 de 512 dimensiones). Además, este archivo Compose requiere una GPU
- Para usar términos de búsqueda en idiomas distintos del inglés (por ejemplo, español), prepare un servidor que ejecute un modelo multilingüe, como el ``docker/clip-server`` de ``docker-multimodalsearch``

3. Configurar system.properties
-------------------------------

La configuración de la búsqueda multimodal se escribe en ``system.properties``.
Se encuentra en ``app/WEB-INF/conf/system.properties`` en la versión ZIP, en ``/etc/fess/system.properties`` en los paquetes RPM/DEB y en ``/opt/fess/system.properties`` en Docker.

::

    content_chunker.enabled=true
    content_chunker.embedding.name=clip
    content_chunker.embedding.dimension=512
    content_chunker.embedding.clip.api.url=http://localhost:51000
    content_chunker.search.enabled=true

- Ajuste ``content_chunker.embedding.dimension`` al número de dimensiones que genera el modelo CLIP (512 en la familia ViT-B/32)
- ``content_chunker.search.enabled`` solo se lee al arrancar, así que reinicie Fess después de configurarlo
- Para pasarlo como opción de arranque, use ``-Dfess.system.<clave>``. Si se escribe en ``fess_config.properties`` o como ``-Dfess.config.<clave>``, se ignora sin ninguna advertencia
- Los valores de ``system.properties`` tienen prioridad sobre ``-Dfess.system.*``. Si escribe una clave en ambos sitios, se usa el valor del archivo
- En los archivos Compose de docker-fess, ``fess01`` no tiene volumen, y ``docker compose down`` hace que se pierda ``system.properties``. En Docker, el método fiable es enumerar ``-Dfess.system.<clave>=<valor>`` en la variable de entorno ``FESS_JAVA_OPTS`` (el ``compose.yaml`` de ``docker-multimodalsearch`` también lo hace así)

Para la lista de claves, consulte "Referencia de configuración" en `Búsqueda Semántica (Chunking de Contenido + Búsqueda Vectorial) <https://fess.codelibs.org/es/stable/config/search-semantic.html>`__.
La búsqueda multimodal usa las mismas claves ``content_chunker.*``.

4. Recrear el índice
--------------------

La asignación (mapping) del campo vectorial ``content_chunk_vector`` se crea, al crear el índice, con el número de dimensiones configurado en ese momento.
Si ya había iniciado Fess alguna vez antes de aplicar la configuración anterior, ejecute "Reindexación" en [Información del sistema] > [Mantenimiento] con "Actualizar alias" activado.
Para más detalles, consulte `Mantenimiento <https://fess.codelibs.org/es/stable/admin/maintenance-guide.html>`__.

5. Activar las miniaturas
-------------------------

En la búsqueda de imágenes, sin miniaturas no se pueden distinguir los resultados.
Las miniaturas están desactivadas de forma predeterminada.

- En [Sistema] > [General], active "Mostrar miniatura" y guarde
- Para generar miniaturas de imágenes, PDF y documentos de Office se necesitan herramientas externas como ImageMagick. No están incluidas en la imagen Docker predeterminada (Alpine), así que use una imagen ``-noble`` (por ejemplo, ``ghcr.io/codelibs/fess:15.9.0-noble``)

Para las herramientas necesarias, consulte `Configuración de Imágenes en Miniatura <https://fess.codelibs.org/es/stable/config/crawler-thumbnail.html>`__.

6. Rastrear y comprobar
-----------------------

Rastree un sitio o una carpeta que contenga imágenes GIF/JPEG/PNG.
Los vectores de las imágenes se escriben durante el rastreo.

Para comprobar ``searcher`` en la API de búsqueda, establezca ``query.additional.api.response.fields=searcher`` en ``fess_config.properties`` (o ``-Dfess.config.query.additional.api.response.fields=searcher`` como opción de arranque).

Deje desactivado el trabajo "Content Chunk Vector Indexer" del programador (está desactivado de forma predeterminada).
Los vectores de las imágenes los escribe el rastreador, así que este trabajo no es necesario.
Si lo activa, los documentos de texto también se vectorizan con la parte de texto de CLIP y el campo ``content`` se divide.

Notas de operación
==================

No se puede combinar con la búsqueda semántica de texto
-------------------------------------------------------

El plugin sustituye el procesamiento de búsqueda de la búsqueda semántica de Fess (``semanticChunkSearcher``) por uno para CLIP.
Además, ``content_chunker.embedding.name`` solo admite un valor.
Por eso, la búsqueda semántica de texto de :doc:`guide-18` y la búsqueda multimodal no se pueden usar a la vez en un mismo Fess.
Si necesita ambas, despliegue instancias de Fess separadas.

Tenga en cuenta además que, si restringe los procesamientos de búsqueda que se usan con ``rank.fusion.searchers``, la búsqueda vectorial queda excluida a menos que incluya ``multi_modal``.
Normalmente, deje este ajuste vacío.

Al cambiar de modelo, vuelva a rastrear
---------------------------------------

Cambie siempre el modelo y el número de dimensiones a la vez.
El número de dimensiones queda fijado en la asignación al crear el índice, por lo que después del cambio son necesarios los siguientes pasos.

1. En [Información del sistema] > [Mantenimiento], ejecute "Reindexación" (con "Actualizar alias" activado) para recrear el índice con el nuevo número de dimensiones
2. Vuelva a rastrear

La reindexación solo copia los documentos; no vuelve a calcular los vectores.
Aunque el número de dimensiones sea el mismo, cambiar el modelo o el servidor CLIP cambia el espacio vectorial, así que elimine los documentos y vuelva a rastrear.
En ``docker-multimodalsearch``, cambie ``CLIP_MODEL_NAME`` y ``MULTIMODAL_DIMENSION`` en ``.env``.
El procedimiento está en la sección "Model swap" del README.

CPU y GPU
---------

El modelo predeterminado de ``docker-multimodalsearch`` (512 dimensiones) está pensado para ejecutarse en la CPU, y ``CLIP_DEVICE=cpu`` es el valor predeterminado.
Si cambia al modelo más grande ``xlm-roberta-large-ViT-H-14::frozen_laion5b_s13b_b90k`` (1024 dimensiones), se recomienda una GPU; con ``CLIP_DEVICE=auto``, se usa la GPU si está disponible.

Resumen
=======

- ``fess-webapp-multimodal`` busca imágenes GIF/JPEG/PNG a partir de texto. No permite buscar por imagen ni vectorizar imágenes incrustadas en documentos
- Para probarlo, use ``v15.9.0`` de ``docker-multimodalsearch`` y especifique ``FESS_THEMES_REF=15.9.x``
- La configuración ``content_chunker.*`` se escribe en ``system.properties`` (o como ``-Dfess.system.*``)
- Si se usó la búsqueda vectorial se comprueba con ``multi_modal`` en ``searcher`` de la API de búsqueda
- Los términos de búsqueda en idiomas distintos del inglés (por ejemplo, español) requieren un modelo multilingüe, y la búsqueda multimodal no puede convivir con la búsqueda semántica de texto en el mismo Fess

Artículos relacionados
======================

- :doc:`guide-18` — Buscar documentos de texto mediante vectores (una configuración distinta de la multimodal)
- :doc:`guide-02` — Conceptos básicos para ejecutar Fess con Docker
- :doc:`guide-11` — Integrar Fess con sistemas de negocio mediante la API de búsqueda

Referencias
===========

- `docker-multimodalsearch (v15.9.0) <https://github.com/codelibs/docker-multimodalsearch/tree/v15.9.0>`__
- `fess-webapp-multimodal (15.9.0) <https://github.com/codelibs/fess-webapp-multimodal/tree/fess-webapp-multimodal-15.9.0>`__
