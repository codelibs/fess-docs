=======================================================
Configuración de Visualización de Registros de Búsqueda
=======================================================

Acerca de la Visualización de Registros de Búsqueda
====================================================

|Fess| captura los registros de búsqueda y los registros de clics de los usuarios.
Los registros de búsqueda capturados se pueden analizar y visualizar utilizando `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/index/>`__.

|Fess| incluye el archivo de definición de dashboard ``extension/kibana/fess_log.ndjson`` para visualizar los registros de búsqueda.
Al importar este archivo en OpenSearch Dashboards, podrá utilizar de inmediato los dashboards predefinidos.

Información que se Puede Visualizar
------------------------------------

Al importar la definición de dashboard incluida (``fess_log.ndjson``), se registran el dashboard ``fess_log`` y las siguientes 6 visualizaciones:

-  Tiempo de respuesta promedio para mostrar resultados de búsqueda (``average-response-time``)
-  Número de solicitudes de búsqueda por unidad de tiempo (``search-query-counts-per-sec``)
-  Clasificación de User Agent de usuarios que acceden (``rank-of-UserAgent``)
-  Clasificación de palabras clave de búsqueda (``search-term-rank``)
-  Clasificación de palabras clave de búsqueda con 0 resultados (``search-term-rank-of-no-results``)
-  Número promedio de resultados de búsqueda (``hit-counts``)

Además de estos, también puede construir su propio panel de monitoreo personalizado creando nuevos gráficos usando la función Visualize y añadiéndolos al dashboard.

Configuración de Visualización de Datos mediante OpenSearch Dashboards
=======================================================================

Instalación de OpenSearch Dashboards
-------------------------------------

OpenSearch Dashboards es una herramienta para visualizar datos de OpenSearch utilizada por |Fess|.
Instale OpenSearch Dashboards siguiendo la `documentación oficial de OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-dashboards/index/>`__.

Edición del Archivo de Configuración
-------------------------------------

Para que OpenSearch Dashboards reconozca el OpenSearch utilizado por |Fess|, edite el archivo de configuración ``config/opensearch_dashboards.yml``.

::

    opensearch.hosts: ["http://localhost:9201"]

Cambie ``localhost`` al nombre de host o dirección IP apropiado para su entorno.
Con la configuración predeterminada de |Fess|, OpenSearch se inicia en el puerto 9201.

.. note::
   Si el número de puerto de OpenSearch es diferente, cámbielo al número de puerto apropiado.

Inicio de OpenSearch Dashboards
--------------------------------

Después de editar el archivo de configuración, inicie OpenSearch Dashboards.

::

    $ cd /path/to/opensearch-dashboards
    $ ./bin/opensearch-dashboards

Después del inicio, acceda a ``http://localhost:5601`` en su navegador.

Configuración del Patrón de Índice
------------------------------------

Cree un patrón de índice para visualizar los registros de búsqueda.

1. Seleccione «Management» (o «Dashboards Management» según la versión de OpenSearch Dashboards) del menú lateral izquierdo.
2. Seleccione «Index Patterns».
3. Haga clic en el botón «Create index pattern».
4. Introduzca ``fess_log*`` en Index pattern name.
5. Haga clic en el botón «Next step».
6. Seleccione ``requestedAt`` en Time field.
7. Haga clic en el botón «Create index pattern».

.. note::
   Los registros de búsqueda de |Fess| se almacenan en múltiples índices que comienzan con ``fess_log``, como ``fess_log.search_log`` para los registros de búsqueda y ``fess_log.click_log`` para los registros de clics.
   Al especificar el patrón de índice ``fess_log*``, puede incluirlos todos a la vez.

Importación de la Definición de Dashboard
------------------------------------------

Al importar la definición de dashboard incluida con |Fess|, podrá utilizar las visualizaciones y dashboards predefinidos.

1. Seleccione «Management» (o «Dashboards Management» según la versión de OpenSearch Dashboards) del menú lateral izquierdo.
2. Seleccione «Saved Objects».
3. Haga clic en «Import».
4. Seleccione ``extension/kibana/fess_log.ndjson`` ubicado en el directorio de instalación de |Fess|.
5. Haga clic en «Import» para ejecutar la importación.

Una vez completada la importación, se registrarán 6 visualizaciones y el dashboard ``fess_log``.

Visualización del Dashboard
-----------------------------

1. Seleccione «Dashboard» del menú lateral izquierdo.
2. Seleccione el dashboard ``fess_log``.
3. Se mostrarán los resultados de la visualización de los registros de búsqueda.
4. Puede especificar el período a mostrar en la selección de rango de tiempo en la parte superior derecha.

Creación de Visualizaciones Personalizadas
-------------------------------------------

Además del dashboard incluido, también puede crear sus propias visualizaciones y dashboards.

Creación de Visualizaciones
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Seleccione «Visualize» del menú lateral izquierdo.
2. Haga clic en el botón «Create visualization».
3. Seleccione el tipo de visualización (gráfico de líneas, gráfico circular, gráfico de barras, etc.).
4. Seleccione el patrón de índice creado ``fess_log*``.
5. Configure las métricas y buckets (unidades de agregación) necesarios.
6. Haga clic en el botón «Save» para guardar la visualización.

Creación de Dashboards
~~~~~~~~~~~~~~~~~~~~~~~

1. Seleccione «Dashboard» del menú lateral izquierdo.
2. Haga clic en el botón «Create dashboard».
3. Haga clic en el botón «Add» para añadir las visualizaciones creadas.
4. Ajuste el diseño y haga clic en el botón «Save» para guardar.

Configuración de Zona Horaria
-------------------------------

Si la visualización de la hora no es correcta, configure la zona horaria.

1. Seleccione «Management» (o «Dashboards Management» según la versión de OpenSearch Dashboards) del menú lateral izquierdo.
2. Seleccione «Advanced Settings».
3. Busque ``dateFormat:tz``.
4. Configure la zona horaria con un valor apropiado (por ejemplo: ``Asia/Tokyo`` o ``UTC``).
5. Haga clic en el botón «Save».

Verificación de Datos de Registro
------------------------------------

1. Seleccione «Discover» del menú lateral izquierdo.
2. Seleccione el patrón de índice ``fess_log*``.
3. Se mostrarán los datos de registro de búsqueda.
4. Puede especificar el período a mostrar en la selección de rango de tiempo en la parte superior derecha.

Principales Campos de Registro de Búsqueda
--------------------------------------------

Los registros de búsqueda de |Fess| (``fess_log.search_log``) contienen la siguiente información.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Nombre del Campo
     - Descripción
   * - ``queryId``
     - Identificador único de la consulta de búsqueda
   * - ``searchWord``
     - Palabra clave de búsqueda
   * - ``requestedAt``
     - Fecha y hora en que se ejecutó la búsqueda
   * - ``responseTime``
     - Tiempo de respuesta total del proceso de búsqueda (milisegundos)
   * - ``queryTime``
     - Tiempo de ejecución de la consulta al motor de búsqueda (milisegundos)
   * - ``hitCount``
     - Número de coincidencias en los resultados de búsqueda
   * - ``hitCountRelation``
     - Relación que indica si el número de coincidencias es un valor exacto o un límite inferior (``eq``: número exacto, ``gte``: mayor o igual al valor indicado)
   * - ``queryOffset``
     - Posición de inicio para obtener los resultados de búsqueda
   * - ``queryPageSize``
     - Número de resultados mostrados por página
   * - ``userAgent``
     - Información del navegador del usuario
   * - ``referer``
     - URL de referencia de la página desde la que se ejecutó la búsqueda
   * - ``clientIp``
     - Dirección IP del cliente
   * - ``languages``
     - Idioma utilizado en la solicitud
   * - ``accessType``
     - Tipo de acceso (``web``, ``json``, ``gsa``, ``admin``, ``other``)
   * - ``roles``
     - Información del rol del usuario
   * - ``user``
     - Nombre de usuario (al iniciar sesión)
   * - ``virtualHost``
     - Nombre del host virtual (si está configurado)

Puede analizar los registros de búsqueda desde diversas perspectivas utilizando estos campos.

Solución de Problemas
----------------------

Si no se Muestran Datos
~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que OpenSearch se esté ejecutando correctamente.
- Verifique que la configuración de ``opensearch.hosts`` en ``opensearch_dashboards.yml`` sea correcta.
- Verifique que se estén ejecutando búsquedas en |Fess| y que se estén registrando los logs.
- Verifique que el rango de tiempo en la parte superior derecha esté configurado para incluir el período en que se registraron los logs.
- Si la visualización de la hora está desfasada, verifique la configuración de ``dateFormat:tz``.

Si se Producen Errores de Conexión
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que el número de puerto de OpenSearch sea correcto.
- Verifique la configuración del firewall o grupos de seguridad.
- Verifique si hay errores en los archivos de registro de OpenSearch.
