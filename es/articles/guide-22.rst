==============================================
Registros de búsqueda en OpenSearch Dashboards
==============================================

Introducción
============

En Fess 15.9, [Información del sistema] > [Registro de búsqueda] de la pantalla de administración muestra la tasa de cero resultados, la tasa de clics, la distribución de posiciones de clic, los tiempos de respuesta, el número de búsquedas por día de la semana y por hora, y el número de búsquedas por rol y por grupo.
Cada tabla se puede descargar en formato CSV.
El proceso de encontrar términos de búsqueda problemáticos y corregirlos con sinónimos o coincidencias de clave se explica en :doc:`guide-08`.

Sin embargo, esta pantalla no permite agregaciones como las siguientes:

- Tendencias en periodos de más de 366 días (el periodo "Personalizado" de la pantalla tiene un máximo de 366 días)
- Qué términos no obtienen resultados, desglosados por rol o por etiqueta
- Qué URL se abrieron realmente para cada término de búsqueda
- Un panel con gráficos según los criterios que usted elija

Los registros de búsqueda y de clics se guardan en índices de OpenSearch, por lo que puede agregarlos directamente desde OpenSearch Dashboards.
En este artículo se inicia OpenSearch Dashboards con los archivos Compose de docker-fess, se importa el panel incluido en Fess, se revisan los campos de los registros y, por último, se crean las cuatro agregaciones mencionadas.

Antes de empezar: restricción del acceso
========================================

En docker-fess, OpenSearch Dashboards funciona sin el plugin de seguridad, igual que OpenSearch.
Cualquier persona que llegue al puerto 5601 puede leer, sin iniciar sesión, todos los campos de los registros de búsqueda (ID de usuario, direcciones IP, etc.).
Además, desde Dev Tools puede modificar o eliminar cualquier índice, incluidos los índices de Fess con los usuarios y la configuración.

Por eso, haga que el puerto 5601 (y el 9200) solo sea accesible desde los equipos de los administradores.
Si quiere mostrar las estadísticas de los registros de búsqueda a personas que no son administradores, no publique OpenSearch Dashboards; en su lugar, cree en Fess un rol llamado ``admin-searchlog-view`` en [Usuario] > [Rol] y asígnelo a esas personas.
Con este rol se puede consultar [Información del sistema] > [Registro de búsqueda], pero no eliminar registros.

Inicio de OpenSearch Dashboards
===============================

Añada los archivos para Dashboards al directorio donde colocó ``compose.yaml`` y ``compose-opensearch3.yaml`` siguiendo :doc:`guide-02`.
``compose-dashboards3.yaml`` construye su imagen a partir del Dockerfile del directorio ``dashboards/``, por lo que se necesitan tres archivos.

::

    $ cd fess-docker
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-dashboards3.yaml
    $ mkdir dashboards
    $ curl -L -o dashboards/Dockerfile https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/dashboards/Dockerfile
    $ curl -L -o dashboards/opensearch_dashboards.yml https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/dashboards/opensearch_dashboards.yml

Inicie especificando los tres archivos Compose.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-dashboards3.yaml up -d

En el primer ``up`` se construye, a partir de ``opensearch-dashboards:3.9.0``, una imagen sin el plugin ``securityDashboards``.
El contenedor se conecta a ``OPENSEARCH_HOSTS='["http://search01:9200"]'`` en la red ``search_net`` y publica el puerto 5601.

Abra ``http://localhost:5601`` en el navegador; si aparece la página de inicio, ya está en marcha.
Para detenerlo o comprobar su estado, especifique también los tres archivos con ``-f``.
Los objetos guardados, como los paneles, se almacenan en el índice ``.kibana`` de OpenSearch, de modo que si elimina los volúmenes con ``down -v`` también se borran.

Importación del panel incluido
==============================

Fess incluye una definición de panel para los registros de búsqueda, ``fess_log.ndjson``.
Con Docker, cópiela desde el contenedor.
En la versión ZIP se encuentra en ``extension/kibana/fess_log.ndjson`` del directorio descomprimido.

::

    $ docker cp fess01:/usr/share/fess/extension/kibana/fess_log.ndjson .

También puede obtener el mismo archivo desde GitHub en ``https://raw.githubusercontent.com/codelibs/fess/fess-15.9.0/src/main/assemblies/extension/kibana/fess_log.ndjson``.

1. Abra [Dashboards Management] en el menú de la izquierda y seleccione [Saved objects]
2. Haga clic en [Import], seleccione ``fess_log.ndjson`` e impórtelo
3. Abra el panel ``fess_log`` desde [Dashboards] en el menú de la izquierda

La importación registra el patrón de índice ``fess_log*`` (campo de tiempo ``requestedAt``), seis visualizaciones y el panel ``fess_log``.
Como incluye el patrón de índice, no es necesario crear ``fess_log*`` manualmente antes.
Si lo crea manualmente y después importa el archivo, tendrá dos patrones con el mismo nombre.

Cuidado con cómo cuenta el panel incluido
-----------------------------------------

``fess_log*`` abarca todos los índices cuyo nombre empieza por ``fess_log``, y las visualizaciones incluidas no filtran por índice.
En 15.9, los registros de clics contienen el término de búsqueda (``searchWord``) y ``requestedAt``, así que el recuento de "search-term-rank", por ejemplo, suma búsquedas y clics.
Si utiliza el modo Búsqueda IA, los registros de chat (``fess_log.chat_log``) también se mezclan en los recuentos y los tiempos de respuesta.

Para contar solo las búsquedas, introduzca la siguiente condición en la barra de búsqueda de la parte superior del panel antes de consultarlo.

::

    _index : "fess_log.search_log"

Además, la lista de campos guardada en ``fess_log*`` corresponde a una versión antigua y no incluye campos nuevos como ``rank``.
Para crear sus propias agregaciones, use los patrones de índice de la sección siguiente.

Creación de patrones de índice para las agregaciones
====================================================

Si separa los registros de búsqueda y de clics en patrones de índice distintos, no se mezclan y puede elegir todos los campos actuales.

1. En [Dashboards Management] > [Index patterns], haga clic en [Create index pattern]
2. Escriba ``fess_log.search_log`` en "Index pattern name" y haga clic en [Next step]
3. Seleccione ``requestedAt`` en "Time field" y haga clic en [Create index pattern]
4. Cree del mismo modo ``fess_log.click_log`` (campo de tiempo ``requestedAt``)

Si más adelante aparecen campos nuevos (por ejemplo, cuando se registra la primera búsqueda filtrada por etiqueta), haga clic en [Refresh field list] en la pantalla del patrón de índice.

Tratamiento de la hora
----------------------

Fess guarda las fechas y horas en UTC.
De forma predeterminada, OpenSearch Dashboards las muestra en la zona horaria del navegador y también divide los días según ella.
Para verlas en otra zona horaria, cambie ``dateFormat:tz`` en [Dashboards Management] > [Advanced settings] a su zona horaria, por ejemplo ``Asia/Tokyo``.

La pantalla [Registro de búsqueda] de Fess divide los días según la zona horaria del servidor.
Los contenedores de docker-fess usan UTC de forma predeterminada, así que, al comparar las cifras diarias de ambos, pueden diferir por la distinta frontera entre días.

Campos de los registros
=======================

El registro de búsqueda (``fess_log.search_log``) tiene una entrada por búsqueda.
Los campos más utilizados en las agregaciones son los siguientes.

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Tipo
     - Contenido
   * - ``queryId``
     - keyword
     - ID de cada búsqueda. Corresponde al ``queryId`` del registro de clics
   * - ``searchWord``
     - keyword
     - El término de búsqueda. En una búsqueda filtrada por etiqueta incluye también la condición, como en ``solicitud label:"hr"``
   * - ``searchField.*``
     - keyword
     - El término de búsqueda dividido por campos. Los términos normales van a ``searchField._default`` y los filtros de etiqueta a ``searchField.label``
   * - ``requestedAt``
     - date
     - Fecha y hora de la búsqueda (guardadas en UTC)
   * - ``hitCount``
     - long
     - Número de resultados. ``0`` indica una búsqueda sin resultados
   * - ``responseTime`` / ``queryTime``
     - long
     - Tiempo de procesamiento de toda la búsqueda y tiempo de búsqueda en OpenSearch (milisegundos)
   * - ``queryOffset`` / ``queryPageSize``
     - integer
     - Posición inicial y número de resultados por página. A partir de la segunda página, ``queryOffset`` es mayor que 0
   * - ``accessType``
     - keyword
     - Uno de ``json``, ``gsa``, ``admin``, ``other`` y ``web``. La página de búsqueda del tema predeterminado llama a ``/api/v2/search``, por lo que es ``json``; las búsquedas desde [Información del sistema] > [Búsqueda] de la pantalla de administración son ``admin``
   * - ``user`` / ``roles``
     - keyword
     - El ID del usuario que ha iniciado sesión y la lista de roles usados en la búsqueda. El primer carácter de un valor de ``roles`` indica su tipo: ``R`` es un rol, ``2`` un grupo y ``1`` un usuario (ejemplo: ``Rguest``)
   * - ``userSessionId`` / ``clientIp`` / ``userAgent`` / ``referer`` / ``virtualHost``
     - keyword
     - El valor de la cookie que identifica al usuario, la dirección IP, el navegador, la página de referencia y el host virtual

El registro de clics (``fess_log.click_log``) se guarda cuando se abre un enlace de los resultados de búsqueda a través de ``/go/``.
Sin embargo, no se guarda en las solicitudes en las que el navegador no tiene una sesión de Fess (no envía una cookie de sesión válida).

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Tipo
     - Contenido
   * - ``queryId``
     - keyword
     - ``queryId`` de la búsqueda de la que procede el clic
   * - ``url`` / ``docId``
     - keyword
     - URL e ID del documento abierto
   * - ``rank``
     - integer
     - Posición en el conjunto de los resultados (el primer puesto es 1). El primer resultado de la segunda página es 11
   * - ``order``
     - integer
     - Posición dentro de la página (la primera es 0). Para agregar posiciones, use ``rank``
   * - ``searchWord`` / ``accessType``
     - keyword
     - Término de búsqueda y tipo de acceso copiados de la búsqueda de origen. Permiten agregar por término de búsqueda sin combinar con el registro de búsqueda
   * - ``requestedAt`` / ``queryRequestedAt``
     - date
     - Fecha y hora del clic y de la búsqueda de origen

``searchWord``, ``accessType`` y ``rank`` se incluyen en el registro de clics a partir de 15.9.
Los clics registrados antes no los tienen.

Recetas de agregación
=====================

Aquí creamos las cuatro "agregaciones que la pantalla no permite" mencionadas al principio.
La primera se crea con Visualize y las demás se ejecutan con la API de búsqueda desde [Dev Tools] en el menú de la izquierda.

URL abiertas para cada término de búsqueda
------------------------------------------

Esta tabla muestra, para cada término de búsqueda, qué documentos se abrieron y en qué posición.
Sirve para elegir candidatos para coincidencia de clave o impulso de documento.

1. En [Visualize] del menú de la izquierda, haga clic en [Create visualization] y elija "Data Table"
2. Seleccione ``fess_log.click_log`` como origen
3. En Metrics, añada una Metric con [Add] y elija "Average" en "Aggregation" y ``rank`` en "Field"
4. En Buckets, elija [Add] > [Split rows] y establezca "Aggregation" en "Terms", "Field" en ``searchWord`` y "Size" en 20
5. Añada otro [Split rows] con "Terms", "Field" en ``url`` y "Size" en 5
6. Haga clic en [Update], elija el periodo en la esquina superior derecha y guarde

Las combinaciones con una posición media alta son documentos que los usuarios abrieron tras bajar mucho en los resultados.

Términos sin resultados por rol
-------------------------------

Si asigna los roles por departamento, compruebe qué no encuentran las búsquedas de cada departamento.

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": {
        "bool": {
          "filter": [
            { "term": { "hitCount": 0 } },
            { "range": { "requestedAt": { "gte": "now-90d/d" } } }
          ]
        }
      },
      "aggs": {
        "roles": {
          "terms": { "field": "roles", "size": 20, "exclude": "1.*" },
          "aggs": {
            "words": { "terms": { "field": "searchWord", "size": 10 } }
          }
        }
      }
    }

``exclude`` descarta los valores que empiezan por ``1`` (usuarios individuales), de modo que solo se listan roles y grupos.
Una misma búsqueda se cuenta en cada uno de los roles y grupos del usuario.
Las búsquedas de usuarios sin sesión iniciada se cuentan en ``Rguest``.

Búsquedas y búsquedas sin resultados por etiqueta
-------------------------------------------------

Para cada etiqueta, cuente cuántas búsquedas se hicieron con esa etiqueta seleccionada en la página de búsqueda y cuántas de ellas no obtuvieron resultados.

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": { "range": { "requestedAt": { "gte": "now-90d/d" } } },
      "aggs": {
        "labels": {
          "terms": { "field": "searchField.label", "size": 20 },
          "aggs": {
            "zero_hit": { "filter": { "term": { "hitCount": 0 } } }
          }
        }
      }
    }

Si todavía no se ha registrado ninguna búsqueda filtrada por etiqueta, el campo ``searchField.label`` aún no existe y los buckets de ``labels`` quedan vacíos.

Tasa mensual de cero resultados (dos años)
------------------------------------------

Observe, más allá del límite de periodo de la pantalla, la evolución a largo plazo de la tasa de cero resultados (una proporción, no un recuento).

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": {
        "bool": {
          "filter": [ { "range": { "requestedAt": { "gte": "now-2y/d" } } } ],
          "must_not": [ { "term": { "accessType": "admin" } } ]
        }
      },
      "aggs": {
        "per_month": {
          "date_histogram": {
            "field": "requestedAt",
            "calendar_interval": "month",
            "time_zone": "Asia/Tokyo"
          },
          "aggs": {
            "zero_hit": { "filter": { "term": { "hitCount": 0 } } },
            "zero_hit_rate": {
              "bucket_script": {
                "buckets_path": { "zero": "zero_hit>_count", "total": "_count" },
                "script": "params.zero / params.total"
              }
            }
          }
        }
      }
    }

Cada bucket mensual devuelve el número de búsquedas (``doc_count``), el número de búsquedas sin resultados (``zero_hit.doc_count``) y la tasa de cero resultados (``zero_hit_rate.value``, entre 0 y 1).
Con ``time_zone``, los meses empiezan a medianoche en la zona horaria indicada (aquí ``Asia/Tokyo``; sustitúyala por la suya), y ``must_not`` excluye las búsquedas hechas desde la pantalla de administración.
Que haya dos años de registros disponibles depende de la configuración de conservación que se describe en la sección siguiente.

Conservación y datos personales
===============================

De forma predeterminada, los registros de búsqueda se conservan indefinidamente.
Esto se debe a que "Eliminar registros de búsqueda anteriores" en [Sistema] > [General] tiene ``-1`` (no eliminar) como valor predeterminado.
Si indica un número de días, el trabajo "Log Purger", que se ejecuta cada día a medianoche, elimina los registros de búsqueda con más antigüedad que ese número de días.
Los registros de clics, de favoritos y de chat se eliminan tras el mismo número de días.
Los datos de los usuarios dependen de otra opción, "Eliminar registros de usuarios anteriores", cuyo valor predeterminado también es ``-1``.

Decida el número de días teniendo en cuenta tanto hasta dónde quiere remontarse para ver tendencias como las normas de su organización sobre el tratamiento de datos personales.
Los registros de búsqueda contienen el ID del usuario que ha iniciado sesión (``user`` y los valores de ``roles`` que empiezan por ``1``), la dirección IP y el User-Agent.
Además, de forma predeterminada, las URL y los títulos de los documentos mostrados en los resultados de búsqueda se guardan en el campo ``documents`` (``logging.search.docs.enabled=true``).
Todo ello es visible en OpenSearch Dashboards, así que respete las restricciones de acceso descritas al principio.

Solución de problemas
=====================

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Síntoma
     - Qué comprobar
   * - No aparecen datos en Discover ni en las visualizaciones
     - Si el periodo de la esquina superior derecha incluye las fechas de los registros. Tras una búsqueda, el registro puede tardar alrededor de un minuto en escribirse (lo escribe el trabajo "Log Aggregator", que se ejecuta cada minuto)
   * - No se pueden seleccionar ``rank`` ni ``searchField.label``
     - Si está usando ``fess_log*``. Cree un patrón de índice propio o haga clic en [Refresh field list]
   * - Los recuentos son mayores que en la pantalla [Registro de búsqueda]
     - Si ``fess_log*`` también cuenta los registros de clics o de chat. Si el filtro por tipo de acceso y la zona horaria de la frontera entre días coinciden
   * - Hay pocos clics
     - Los enlaces no pasan por ``/go/``, "Registro de búsqueda" está desactivado en [General] o el navegador abre ``/go/`` sin una sesión de Fess. Compruebe también los requisitos previos de :doc:`guide-08`

Artículos relacionados
======================

- Mejorar los términos de búsqueda encontrados con sinónimos o coincidencias de clave: :doc:`guide-08`
- Revisar el diseño de roles y grupos: :doc:`guide-05`
- Organizar la operación, incluidas la supervisión y las copias de seguridad: :doc:`guide-10`
- Decidir qué medir en cada fase de una implantación en toda la empresa: :doc:`guide-23`

Referencias
===========

- `Registro de búsqueda <https://fess.codelibs.org/es/stable/admin/searchlog-guide.html>`__
- `Configuración de Visualización de Registros de Búsqueda <https://fess.codelibs.org/es/stable/config/admin-opensearch-dashboards.html>`__
- `General <https://fess.codelibs.org/es/stable/admin/general-guide.html>`__
- `Instalación con Docker (Detalles) <https://fess.codelibs.org/es/stable/install/install-docker.html>`__
- `Archivos Compose de docker-fess (GitHub) <https://github.com/codelibs/docker-fess/tree/v15.9.0/compose>`__
- `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/index/>`__
