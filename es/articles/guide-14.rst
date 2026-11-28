===============================================
Escalar Fess según crecen documentos y usuarios
===============================================

Introducción
============

Cuando aumentan los documentos y los usuarios, empiezan a aparecer problemas: "el rastreo ya no termina antes de la mañana", "la búsqueda se ha vuelto lenta", "Fess se detuvo con un OutOfMemoryError".
Añadir servidores de inmediato no siempre los resuelve.
Fess se ejecuta como varios procesos JVM, y a menudo es solo uno de ellos el que se queda corto.

Este artículo se centra en Fess 15.9 y explica cómo escalar en el siguiente orden.

1. Averiguar qué le falta a qué proceso
2. Ajustar la memoria y el paralelismo del rastreo en un solo servidor
3. Separar OpenSearch en otro servidor
4. Convertir OpenSearch en un clúster de tres nodos
5. Ejecutar varios servidores Fess

La puesta en marcha de la supervisión (comprobaciones de estado, registros, notificaciones) y las copias de seguridad se tratan en :doc:`guide-10`.

Los procesos que componen Fess
==============================

Aunque Fess se ejecute en un solo servidor, su configuración de memoria se divide de la siguiente manera.

.. list-table::
   :header-rows: 1
   :widths: 20 30 25 25

   * - Proceso
     - Función
     - Heap predeterminado
     - Dónde se configura
   * - Servidor Fess
     - Página de búsqueda, consola de administración, API, programador
     - Paquete ZIP: mínimo 256m, máximo 2g; paquetes RPM/DEB e imagen Docker: 512m
     - Variable de entorno ``FESS_HEAP_SIZE``
   * - Rastreador
     - JVM independiente que se inicia para cada trabajo de rastreo
     - Máximo 512m
     - ``jvm.crawler.options`` en ``fess_config.properties``
   * - Generación de sugerencias, generación de miniaturas
     - JVM independiente que se inicia para cada trabajo
     - Máximo 256m
     - ``jvm.suggest.options``, ``jvm.thumbnail.options``
   * - OpenSearch
     - Almacena el índice y ejecuta las búsquedas
     - 1g en ``compose-opensearch3.yaml`` de docker-fess
     - ``OPENSEARCH_JAVA_OPTS`` o ``config/jvm.options``

El procesamiento de chunks que usa la búsqueda semántica también tiene su propia JVM (``jvm.chunk.options``, máximo 1g); se trata en :doc:`guide-18`.

Si ``fess-crawler.log`` muestra un OutOfMemoryError, a quien le falta memoria es a la JVM del rastreador.
En ese caso, aumentar ``FESS_HEAP_SIZE`` no tiene ningún efecto.

Averiguar qué falta
===================

Según el síntoma, compruebe los siguientes lugares.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Síntoma
     - Dónde comprobar
   * - La búsqueda es lenta
     - En la pestaña [Rendimiento] de [Información del sistema] > [Registro de búsqueda], revise los tiempos de respuesta p95 y p99 y los términos de búsqueda lentos. Distinga si solo son lentos ciertos términos o si todo es lento.
   * - El rastreo no termina
     - En [Información del sistema] > [Registro de trabajo], observe cómo evolucionan las horas de inicio y fin de los trabajos de rastreo. Si ``fess-crawler.log`` muestra continuamente ``Cpu Load XX% is greater than 50%``, el rastreo está esperando por el control de carga que se describe más adelante.
   * - El rastreador se detiene
     - Busque ``OutOfMemoryError`` en ``fess-crawler.log``.
   * - El servidor Fess se detiene o la consola de administración va lenta
     - Busque ``OutOfMemoryError`` en ``fess.log`` y revise ``response.stats.jvm.memory.heap.percent`` en ``/api/admin/stats``.
   * - OpenSearch va lento
     - Revise ``response.stats.engine.status`` en ``/api/admin/stats`` y el uso del heap en ``_cat/nodes`` de OpenSearch. Un ``circuit_breaker_exception`` es señal de que falta heap.

``/api/admin/stats`` devuelve el estado de la JVM y del sistema operativo del servidor Fess que recibió la solicitud, así como el del clúster de OpenSearch.
No incluye la JVM del rastreador ni el heap de cada nodo de OpenSearch.
Para llamarlo se necesita un token de acceso con el permiso ``admin-api``.
Consulte cómo crearlo en `Visión General de Admin API <https://fess.codelibs.org/es/stable/api/admin/api-admin-overview.html>`__ y los campos de la respuesta en `API de Stats <https://fess.codelibs.org/es/stable/api/admin/api-admin-stats.html>`__.

El heap de cada nodo de OpenSearch se consulta directamente a OpenSearch.

::

    $ curl -s 'http://localhost:9200/_cat/nodes?v&h=name,heap.max,heap.percent,ram.percent,cpu'

El número de documentos y el tamaño del índice se pueden comprobar con el siguiente comando.
``fess.search`` es el alias del índice que se usa para buscar.

::

    $ curl -s 'http://localhost:9200/_cat/indices/fess.search?v&h=index,docs.count,pri.store.size,store.size'

Ajustes en un solo servidor
===========================

Cambiar el heap del servidor Fess
---------------------------------

Con Docker, añada ``FESS_HEAP_SIZE`` a ``environment`` de ``fess01`` en ``compose.yaml``.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "FESS_DICTIONARY_PATH=${FESS_DICTIONARY_PATH:-/usr/share/opensearch/config/dictionary/}"
          - "FESS_HEAP_SIZE=2g"

Si cambia ``environment`` o ``volumes`` de ``fess01`` en ``compose.yaml`` y ejecuta ``docker compose ... up -d``, el contenedor ``fess01`` se vuelve a crear.
La configuración cambiada en [Sistema] > [General] se guarda en ``system.properties`` dentro del contenedor, por lo que se pierde al volver a crearlo.
Lo mismo ocurre cuando otros pasos de este artículo modifican ``compose.yaml``.
Haga antes una copia de seguridad siguiendo el procedimiento de :doc:`guide-10`.

En el paquete RPM, modifique ``FESS_HEAP_SIZE=512m`` en ``/etc/sysconfig/fess``; en el paquete DEB, en ``/etc/default/fess``. Después reinicie Fess.
En el paquete ZIP, exporte ``FESS_HEAP_SIZE`` en el entorno desde el que se inicia Fess.

Compruebe que el cambio se aplicó mirando los argumentos de los procesos en ejecución.
Con Docker, se hace así.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml exec -T fess01 sh -c 'cat /proc/[0-9]*/cmdline 2>/dev/null' | tr '\0' '\n' | grep -e '^-Xmx' -e 'FessBoot' -e 'exec.Crawler'
    -Xmx2g
    org.codelibs.fess.FessBoot

La línea que sigue a ``-Xmx`` indica el tipo de proceso.
``FessBoot`` es el servidor Fess y ``exec.Crawler`` es el rastreador.
En los paquetes RPM/DEB y ZIP, ejecute directamente en el servidor Fess el comando que está dentro de ``sh -c`` y todo lo que le sigue.

Cambiar el heap del rastreador
------------------------------

``jvm.crawler.options`` es un único valor que enumera opciones de la JVM separadas por ``\n``.
Como se reemplaza el valor completo, escribir solo ``-Xmx1g`` elimina todas las opciones predeterminadas, como G1GC.
Conserve el valor predeterminado y modifique solo la línea ``-Xmx512m``.

::

    -Xms128m\n\
    -Xmx1g\n\

El archivo de configuración está en ``/etc/fess/fess_config.properties`` en los paquetes RPM/DEB y en ``app/WEB-INF/classes/fess_config.properties`` en el paquete ZIP.
Con Docker, copie ``fess_config.properties`` de la imagen a su equipo, edítelo y móntelo en ``/opt/fess/fess_config.properties`` del contenedor.
``/opt/fess`` se lee con prioridad sobre ``/etc/fess``.
Como este valor ocupa varias líneas, no es adecuado definirlo con ``-Dfess.config.`` en ``FESS_JAVA_OPTS``.
Para el procedimiento, consulte "Cómo Aplicar Archivos de Configuración" en `Instalación con Docker (Detalles) <https://fess.codelibs.org/es/stable/install/install-docker.html>`__.

Después de reiniciar Fess, compruebe en "Propiedades de la aplicación" de [Información del sistema] > [Información de configuración] que ``jvm.crawler.options`` contiene ``-Xmx1g``.
El cambio se aplica a partir del siguiente rastreador que se inicie.
Si ejecuta el comando de la sección anterior durante un rastreo, ``-Xmx1g`` aparece en la línea anterior a ``org.codelibs.fess.exec.Crawler``.

Se inicia una JVM de rastreador por cada trabajo de rastreo.
El trabajo "Default Crawler" procesa todas las configuraciones de rastreo en un único rastreador.
Si crea un trabajo por configuración con [Crear nuevo trabajo] en la página de detalles de una configuración de rastreo, cada uno se inicia como un rastreador independiente y cada uno usa memoria hasta su ``-Xmx``.
Para limitar el número de rastreadores que se ejecutan a la vez, use ``job.max.crawler.processes`` en ``fess_config.properties`` (el valor predeterminado ``0`` significa sin límite).
Un trabajo de rastreo iniciado por encima de ese límite no espera su turno: termina con un error.

Para las JVM de generación de sugerencias y de miniaturas, modifique de la misma forma la línea ``-Xmx256m`` de ``jvm.suggest.options`` y ``jvm.thumbnail.options``.

Cambiar el heap de OpenSearch
-----------------------------

En docker-fess, ``search01`` en ``compose-opensearch3.yaml`` tiene la siguiente línea.

::

    - "OPENSEARCH_JAVA_OPTS=-Xms1g -Xmx1g"

Cambie estos dos valores por un mismo valor nuevo.
En un OpenSearch instalado desde ZIP o RPM, modifique ``-Xms`` y ``-Xmx`` en ``config/jvm.options`` y reinícielo.

Como referencia, el límite superior es como máximo la mitad de la memoria física y menos de 32GB.
La memoria restante sirve como caché de archivos del sistema operativo y contribuye a la velocidad de búsqueda, así que no asigne demasiada al heap.
Con 32GB o más se desactivan los Compressed OOPs de la JVM y la eficiencia incluso empeora.
Si se necesita más, añada nodos.

En `Configuración de Memoria <https://fess.codelibs.org/es/stable/config/setup-memory.html>`__ encontrará valores orientativos de heap según el tamaño del índice.
Empiece por esos valores y ajuste observando el uso del heap en ``_cat/nodes`` mencionado antes y los tiempos de respuesta de la búsqueda.

Si Fess y OpenSearch se ejecutan en el mismo servidor, asegúrese de que la suma de los heaps del servidor Fess, del rastreador y de OpenSearch quepa en la memoria física.

Cambiar el paralelismo del rastreo
----------------------------------

La velocidad del rastreo depende de los tres ajustes siguientes.

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Ajuste
     - Valor predeterminado
     - Ubicación
   * - Número de hilos
     - Web 1, sistema de archivos 5
     - Cada configuración de rastreo ([Rastreador] > [Web], [Sistema de archivos])
   * - Intervalo
     - Web 10000 ms, sistema de archivos 1000 ms
     - Igual que arriba. Tiempo que espera cada hilo cada vez que obtiene una URL
   * - Configuración de rastreadores simultáneos
     - 5
     - [Sistema] > [General]. Número de configuraciones de rastreo que un rastreador procesa a la vez

Aumentar el número de hilos acelera la obtención en esa configuración de rastreo, pero también aumenta el uso de memoria del rastreador y la carga de los servidores rastreados.
Al rastrear sitios externos o servidores que se usan en el trabajo diario, no acorte demasiado el intervalo.

Algo que se pasa por alto fácilmente en un solo servidor es ``adaptive.load.control`` en ``fess_config.properties`` (valor predeterminado ``50``).
Mientras el uso de CPU del servidor donde se ejecuta Fess sea igual o superior a este valor, los hilos de rastreo y de indexación esperan.
Si OpenSearch, en el mismo servidor, usa la CPU para escribir en el índice o para ejecutar búsquedas, el rastreo puede casi dejar de avanzar.
En ese caso, ``fess-crawler.log`` muestra ``Cpu Load XX% is greater than 50%``.
Puede subir el valor, pero si la CPU falta de forma crónica, la solución de fondo es separar OpenSearch en otro servidor, como se explica en la sección siguiente.
Para más detalles, consulte `Configuración de control de carga <https://fess.codelibs.org/es/stable/config/load-control.html>`__.

Separar OpenSearch en otro servidor
===================================

Al mover OpenSearch a otro servidor, el rastreo y la búsqueda dejan de competir por la CPU, la memoria y la E/S de disco.

Lo que necesita OpenSearch
--------------------------

El OpenSearch que usa Fess necesita las dos cosas siguientes.

- Los cuatro plugins para Fess (``opensearch-analysis-fess``, ``opensearch-analysis-extension``, ``opensearch-minhash``, ``opensearch-configsync``). Su versión debe coincidir con la de OpenSearch (Fess 15.9 usa OpenSearch 3.9.0)
- ``configsync.config_path`` en ``opensearch.yml``. Indique como ruta absoluta un directorio para los archivos de diccionario, situado bajo el directorio de configuración de OpenSearch

Los comandos de instalación están en `Instalación en Linux (Procedimientos Detallados) <https://fess.codelibs.org/es/stable/install/install-linux.html>`__.
La imagen ``ghcr.io/codelibs/fess-opensearch`` de docker-fess incluye todo esto desde el principio.

Al colocar OpenSearch en otro servidor, el puerto 9200 queda expuesto en la red.
No lo use en producción con el plugin de seguridad desactivado.
Para la configuración, consulte :doc:`guide-15` y `Configuración de Seguridad <https://fess.codelibs.org/es/stable/install/security.html>`__.

Lo que se configura en Fess
---------------------------

En Fess, el destino de conexión y la ubicación de los diccionarios se indican con dos variables de entorno.

- ``SEARCH_ENGINE_HTTP_URL`` : la URL de OpenSearch
- ``FESS_DICTIONARY_PATH`` : la misma ruta que ``configsync.config_path`` en el lado de OpenSearch

``FESS_DICTIONARY_PATH`` es una ruta del servidor de OpenSearch.
Fess escribe los archivos de diccionario a través del plugin ``configsync``, por lo que no es necesario montar ese directorio desde el servidor Fess.
Si no está definida, Fess no puede crear sus índices y no arranca.

Se definen en ``/etc/sysconfig/fess`` para el paquete RPM, en ``/etc/default/fess`` para el paquete DEB y en ``bin/fess.in.sh`` para el paquete ZIP.
Con Docker, no use ``compose-opensearch3.yaml``; indíquelas en ``environment`` de ``fess01`` en ``compose.yaml``.
En v15.9.0, ``fess01`` en ``compose.yaml`` tiene un ``depends_on`` que espera a ``search01``, por lo que una configuración que no define ``search01`` no arranca y falla con el error ``service "fess01" depends on undefined service "search01"``.
Elimine las tres líneas desde ``depends_on`` hasta ``condition: service_healthy``.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://opensearch1.example.com:9200"
          - "FESS_DICTIONARY_PATH=/etc/opensearch/dictionary/"

En este caso, ejecute todos los comandos ``docker compose`` posteriores solo con ``-f compose.yaml``.

En el paquete ZIP, antes de iniciar Fess puede comprobar con ``bin/fess-setup check`` la conexión, los cuatro plugins y la respuesta de ``configsync``.

::

    $ bin/fess-setup check --url http://opensearch1.example.com:9200

Cambiar el destino de conexión no traslada los índices existentes al nuevo OpenSearch.
Para conservar los documentos existentes, migre con instantáneas ("Migración de Datos" en `Gestión de Índices <https://fess.codelibs.org/es/stable/config/admin-index-backup.html>`__).
Si basta con volver a rastrear, es más sencillo conectarse a un OpenSearch vacío y rastrear de nuevo.

Convertir OpenSearch en un clúster de tres nodos
================================================

Mientras OpenSearch se ejecute en un solo servidor, la búsqueda se detiene en cuanto ese servidor se detiene.
Cuando necesite redundancia, convierta OpenSearch en un clúster.

Composición de los nodos
------------------------

Para elegir el nodo que gestiona el clúster (cluster manager) se necesita el acuerdo de una mayoría.
Si solo uno o dos nodos pueden ser cluster manager, basta con que se detenga uno para que la elección sea imposible.
Por eso, prepare tres nodos que puedan ser cluster manager.
La configuración mínima es aquella en la que los tres también almacenan datos.

A continuación se muestra un ejemplo de los ajustes relacionados con el clúster en ``opensearch.yml`` de cada nodo (cambie ``node.name`` en cada nodo).
Añada los ajustes de red como ``network.host`` y los de seguridad según su entorno.

.. code-block:: yaml

    cluster.name: fess-search
    node.name: search01
    node.roles: [ cluster_manager, data, ingest ]
    discovery.seed_hosts: [ "search01", "search02", "search03" ]
    cluster.initial_cluster_manager_nodes: [ "search01", "search02", "search03" ]
    configsync.config_path: /etc/opensearch/dictionary/

Instale los cuatro plugins para Fess en los tres nodos, con la misma versión.
Use también la misma ruta para ``configsync.config_path`` en los tres nodos.
Esto se debe a que Fess escribe un único valor de ``FESS_DICTIONARY_PATH`` en la configuración del índice, y todos los nodos leen los diccionarios de esa ruta.

``compose/snapshot/compose-cluster.yaml`` de docker-fess contiene un ejemplo de cómo montar varios nodos con Docker.
Este archivo está pensado para combinarse con una versión de desarrollo de la imagen de Fess, así que úselo como referencia de cómo escribir las variables de entorno de OpenSearch.

Conexión desde Fess
-------------------

En ``SEARCH_ENGINE_HTTP_URL``, enumere las URL de los nodos separadas por comas.
Aunque algunos nodos estén detenidos, Fess se conecta a los restantes.

::

    SEARCH_ENGINE_HTTP_URL=http://search01:9200,http://search02:9200,http://search03:9200

Shards y réplicas
-----------------

Fess crea el índice de documentos con ``index.number_of_shards`` de ``fess_config.properties`` (valor predeterminado ``5``, número de shards primarios) e ``index.auto_expand_replicas`` (valor predeterminado ``0-1``, que ajusta automáticamente las réplicas entre 0 y 1 según el número de nodos de datos).
Debido al valor predeterminado ``0-1``, en cuanto hay dos o más nodos de datos se crea una réplica para cada shard sin cambiar la configuración de Fess.
Cuando el estado del clúster pasa a ``green``, todas las réplicas están asignadas.

El número de shards se fija al crear el índice; cambiar después ``index.number_of_shards`` no afecta al índice existente.
Para cambiarlo, use "Reindexación" en [Información del sistema] > [Mantenimiento].
Si indica "Número de fragmentos" y "Número máximo de réplicas", activa "Actualizar alias" e inicia el proceso, Fess crea un índice nuevo, copia los documentos y traslada los alias ``fess.search`` y ``fess.update`` al índice nuevo.

La reindexación tiene las siguientes precauciones.

- Los documentos se copian desde el índice al que apunta ``fess.update`` en el momento de iniciarla. Ejecútela en un momento en que no haya ningún rastreo en marcha
- El índice antiguo no se elimina automáticamente. El disco necesita capacidad para contener a la vez el índice antiguo y el nuevo

Para los elementos de la pantalla, consulte `Mantenimiento <https://fess.codelibs.org/es/stable/admin/maintenance-guide.html>`__.

Comprobar el clúster
--------------------

::

    $ curl -s 'http://search01:9200/_cat/nodes?v&h=name,node.role,cluster_manager,heap.percent'
    $ curl -s 'http://search01:9200/_cluster/health?pretty'

Si aparecen los tres nodos y ``status`` es ``green``, el clúster está listo.
También puede comprobar lo mismo en ``/api/admin/stats`` de Fess con ``response.stats.engine.number_of_nodes`` y ``response.stats.engine.status``.

Ejecutar varios servidores Fess
===============================

Cuando aumentan los usuarios de la búsqueda y al servidor Fess le falta CPU, o cuando quiere que el propio Fess sea redundante, conecte varios servidores Fess al mismo OpenSearch.
Tenga en cuenta que ``compose/multi-instance/`` de docker-fess es una configuración que ejecuta en paralelo servicios de búsqueda independientes, en la que cada Fess usa sus propios índices; es distinta de la configuración que se describe aquí (para separar por organización, consulte :doc:`guide-13`).

Las configuraciones de rastreo, los usuarios, los trabajos y los registros de trabajo se guardan en OpenSearch, por lo que se ven igual desde cualquier Fess.
En cambio, lo siguiente existe por separado en cada servidor Fess, así que debe mantenerse igual en todos los servidores.

- La configuración de [Sistema] > [General] (``system.properties`` de cada servidor). Cambiarla en la pantalla de configuración solo cambia el valor de ese servidor
- ``fess_config.properties`` y las variables de entorno como ``FESS_HEAP_SIZE``
- Los plugins instalados
- ``app.cipher.key`` en ``fess_config.properties``. Entre los parámetros de las configuraciones de rastreo y de almacén de datos, los valores cuyo nombre termina en ``password``, ``key``, ``token``, ``secret``, etc. se cifran con esta clave y se guardan en OpenSearch. Si la clave es distinta en cada servidor, los valores guardados en otro servidor no se pueden descifrar

Decidir qué servidor rastrea
----------------------------

El "Objetivo" de todos los trabajos predeterminados es ``all``.
``all`` coincide en cualquier Fess, así que, tal como está, "Default Crawler" se ejecuta en todos los servidores a la misma hora.

Para dejar el rastreo en un solo servidor, haga las dos cosas siguientes.

1. Solo en el servidor que rastrea, escriba un identificador en ``fess_config.properties``, por ejemplo ``scheduler.target.name=crawler``, y reinicie. Con Docker, puede indicar ``-Dfess.config.scheduler.target.name=crawler`` en ``FESS_JAVA_OPTS``. En los demás servidores, déjelo vacío
2. En [Sistema] > [Programador], abra "Default Crawler", cambie el "Objetivo" de ``all`` a ``crawler`` y guarde. Cambie de la misma forma los trabajos de rastreo creados con [Crear nuevo trabajo]

En "Objetivo" se pueden escribir varios identificadores separados por comas.
Solo con el paso 1, los trabajos siguen ejecutándose en todos los servidores como hasta ahora.
Solo con el paso 2, ningún servidor tiene un identificador que coincida, así que el rastreo no se ejecuta en ninguno.
Para comprobar que el paso 1 se aplicó, mire el valor de ``scheduler.target.name`` en "Propiedades de la aplicación" de [Información del sistema] > [Información de configuración] del servidor que rastrea.

Para los trabajos que no son de rastreo (como la agregación de registros o la eliminación de documentos antiguos), deje el "Objetivo" en ``all``.

Una vez fijado, pulse también [Iniciar ahora] desde la consola de administración del servidor que rastrea.
Si lo pulsa en otro servidor, la pantalla indica que se ha iniciado, pero no se ejecuta en ese servidor; solo se registra ``Ignoring job`` en ``fess.log``.
Si los servidores están detrás de un balanceador de carga, prepare una ruta para acceder directamente al servidor que rastrea.

Configuración del balanceador de carga
--------------------------------------

En Fess 15.9, las sesiones de inicio de sesión se guardan en la memoria de cada Fess.
Si un balanceador de carga reparte la página de búsqueda o la consola de administración que se usan con inicio de sesión, active las sesiones persistentes (sticky sessions) para que el mismo usuario se envíe siempre al mismo servidor.
Guardar las sesiones en OpenSearch para compartirlas entre servidores es posible a partir de 15.10.

Para la comprobación de estado del balanceador de carga puede usar ``/api/v2/health``.
Devuelve 503 cuando el clúster de OpenSearch está en ``RED`` y cuando no puede conectarse a OpenSearch.

Exclusión mutua de las operaciones de mantenimiento
---------------------------------------------------

"Reindexación", "Recargar índice de documentos", "Eliminar índice de rastreo" y "Reconstruir índice de configuración" de [Información del sistema] > [Mantenimiento] se ejecutan en exclusión mutua para que varios servidores Fess no las ejecuten al mismo tiempo.
Si ya se está ejecutando en otro servidor, aparece el mensaje "La operación ya se está ejecutando en <nombre de host>."
Esta exclusión solo afecta a las operaciones de mantenimiento; no coordina los trabajos ni la configuración de [General] entre servidores.

Sobre los valores orientativos de dimensionamiento
==================================================

El número de documentos o de usuarios por sí solo no determina la configuración necesaria.
La memoria y la CPU necesarias varían mucho según la longitud del texto de cada documento, la proporción de archivos adjuntos, la tendencia de los términos de búsqueda y si los usuarios inician sesión o no.

Decida a partir de valores medidos, como se indica a continuación.

- A partir del ``store.size`` del índice, determine el heap de OpenSearch con la tabla orientativa de `Configuración de Memoria <https://fess.codelibs.org/es/stable/config/setup-memory.html>`__
- Si el p95 del registro de búsqueda empeora y el uso del heap o la CPU en ``_cat/nodes`` se mantienen altos, aumente el heap de OpenSearch o añada nodos
- Si los tiempos de rastreo del registro de trabajo se alargan y aparecen registros de ``Cpu Load``, separe OpenSearch en otro servidor
- Si OpenSearch tiene margen pero la CPU del servidor Fess está alta, ejecute varios servidores Fess

Artículos relacionados
======================

- Poner Fess en producción con supervisión, registros y copias de seguridad: :doc:`guide-10`
- Proteger el acceso, incluida la exposición de OpenSearch y el inicio de sesión: :doc:`guide-15`
- Gestionar como código la tarea de igualar la configuración de varios servidores: :doc:`guide-16`
- Usar un solo Fess de forma separada para cada organización: :doc:`guide-13`
- Organizar qué comprobar en cada etapa del despliegue: :doc:`guide-23`

Referencias
===========

- `Configuración de Memoria <https://fess.codelibs.org/es/stable/config/setup-memory.html>`__
- `Configuración de Puerto y Red <https://fess.codelibs.org/es/stable/config/setup-port-network.html>`__
- `Configuración de control de carga <https://fess.codelibs.org/es/stable/config/load-control.html>`__
- `Instalación en Linux (Procedimientos Detallados) <https://fess.codelibs.org/es/stable/install/install-linux.html>`__
- `Instalación con Docker (Detalles) <https://fess.codelibs.org/es/stable/install/install-docker.html>`__
- `Comando fess-setup <https://fess.codelibs.org/es/stable/install/fess-setup.html>`__
- `Mantenimiento <https://fess.codelibs.org/es/stable/admin/maintenance-guide.html>`__
- `Programador de Tareas <https://fess.codelibs.org/es/stable/admin/scheduler-guide.html>`__
- `Registro de búsqueda <https://fess.codelibs.org/es/stable/admin/searchlog-guide.html>`__
- `API de Stats <https://fess.codelibs.org/es/stable/api/admin/api-admin-stats.html>`__
- `Gestión de Índices <https://fess.codelibs.org/es/stable/config/admin-index-backup.html>`__
