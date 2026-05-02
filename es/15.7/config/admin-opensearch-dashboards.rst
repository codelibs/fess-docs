===================================
Configuración de Visualización de Registros de Búsqueda
===================================

Acerca de la Visualización de Registros de Búsqueda
====================================================

|Fess| captura los registros de búsqueda y los registros de clics de los usuarios.
Los registros de búsqueda capturados se pueden analizar y visualizar utilizando `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/index/>`__.

Información que se Puede Visualizar
------------------------------------

Con la configuración predeterminada, se puede visualizar la siguiente información:

-  Tiempo promedio para mostrar resultados de búsqueda
-  Número de búsquedas por segundo
-  Clasificación de User Agent de usuarios que acceden
-  Clasificación de palabras clave de búsqueda
-  Clasificación de palabras clave de búsqueda con 0 resultados
-  Número total de resultados de búsqueda
-  Tendencias de búsqueda en series temporales

Puede construir su propio panel de monitoreo personalizado creando nuevos gráficos usando la función Visualize y añadiéndolos al Dashboard.

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
-----------------------------------

1. Seleccione el menú «Management» desde la pantalla de inicio de OpenSearch Dashboards.
2. Seleccione «Index Patterns».
3. Haga clic en el botón «Create index pattern».
4. Introduzca ``fess_log*`` en Index pattern name.
5. Haga clic en el botón «Next step».
6. Seleccione ``requestedAt`` en Time field.
7. Haga clic en el botón «Create index pattern».

Con esto, se completa la preparación para visualizar los registros de búsqueda de |Fess|.

Creación de Visualizaciones y Paneles
--------------------------------------

Creación de Visualizaciones Básicas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Seleccione «Visualize» del menú lateral.
2. Haga clic en el botón «Create visualization».
3. Seleccione el tipo de visualización (gráfico de líneas, gráfico circular, gráfico de barras, etc.).
4. Seleccione el patrón de índice creado ``fess_log*``.
5. Configure las métricas y buckets (unidades de agregación) necesarios.
6. Haga clic en el botón «Save» para guardar la visualización.

Creación de Paneles
~~~~~~~~~~~~~~~~~~~~

1. Seleccione «Dashboard» del menú lateral.
2. Haga clic en el botón «Create dashboard».
3. Haga clic en el botón «Add» para añadir las visualizaciones creadas.
4. Ajuste el diseño y haga clic en el botón «Save» para guardar.

Configuración de Zona Horaria
------------------------------

Si la visualización de la hora no es correcta, configure la zona horaria.

1. Seleccione «Management» del menú lateral.
2. Seleccione «Advanced Settings».
3. Busque ``dateFormat:tz``.
4. Configure la zona horaria con un valor apropiado (por ejemplo: ``Asia/Tokyo`` o ``UTC``).
5. Haga clic en el botón «Save».

Verificación de Datos de Registro
----------------------------------

1. Seleccione «Discover» del menú lateral.
2. Seleccione el patrón de índice ``fess_log*``.
3. Se mostrarán los datos de registro de búsqueda.
4. Puede especificar el período a mostrar en la selección de rango de tiempo en la parte superior derecha.

Principales Campos de Registro de Búsqueda
-------------------------------------------

Los registros de búsqueda de |Fess| contienen la siguiente información.

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
     - Tiempo de respuesta de los resultados de búsqueda (milisegundos)
   * - ``queryTime``
     - Tiempo de ejecución de la consulta (milisegundos)
   * - ``hitCount``
     - Número de coincidencias en los resultados de búsqueda
   * - ``userAgent``
     - Información del navegador del usuario
   * - ``clientIp``
     - Dirección IP del cliente
   * - ``languages``
     - Idioma utilizado
   * - ``roles``
     - Información del rol del usuario
   * - ``user``
     - Nombre de usuario (al iniciar sesión)

Puede analizar los registros de búsqueda desde diversas perspectivas utilizando estos campos.

Solución de Problemas
----------------------

Si no se Muestran Datos
~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que OpenSearch se esté ejecutando correctamente.
- Verifique que la configuración de ``opensearch.hosts`` en ``opensearch_dashboards.yml`` sea correcta.
- Verifique que se estén ejecutando búsquedas en |Fess| y que se estén registrando los logs.
- Verifique que el rango de tiempo del patrón de índice esté configurado apropiadamente.

Si se Producen Errores de Conexión
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que el número de puerto de OpenSearch sea correcto.
- Verifique la configuración del firewall o grupos de seguridad.
- Verifique si hay errores en los archivos de registro de OpenSearch.
