============================================================
Parte 22: Dibujando un mapa de conocimiento organizacional a partir de datos de busqueda -- Comprendiendo el uso de la informacion a traves del panel de analisis
============================================================

Introduccion
=============

Un sistema de busqueda es una herramienta para "encontrar" informacion, pero los propios registros de busqueda tambien son una valiosa fuente de informacion.
"Que se busca?", "Que no se puede encontrar?", "Que informacion se consulta con frecuencia?" -- estos datos sirven como un espejo que refleja las necesidades de informacion y las brechas de conocimiento de la organizacion.

En este articulo, combinamos los registros de busqueda de Fess con OpenSearch Dashboards para construir un panel de analisis que visualiza el estado de utilizacion del conocimiento en la organizacion.

Publico objetivo
=================

- Personas que desean comprender cuantitativamente como se utiliza su sistema de busqueda
- Personas que desean recopilar datos para estrategias de utilizacion de la informacion
- Personas que desean aprender las operaciones basicas de OpenSearch Dashboards

El valor de los datos de busqueda
==================================

Lo que los registros de busqueda pueden revelar
-------------------------------------------------

Los registros de busqueda son un tipo de datos poco comun que permite comprender cuantitativamente las necesidades de informacion de una organizacion.

.. list-table:: Informacion obtenida de los datos de busqueda
   :header-rows: 1
   :widths: 30 70

   * - Datos
     - Informacion
   * - Palabras clave de busqueda
     - Que buscan los empleados (necesidades de informacion)
   * - Consultas sin resultados
     - Informacion que falta en la organizacion (brechas de conocimiento)
   * - Registros de clics
     - Que resultados de busqueda fueron utiles (valor del contenido)
   * - Frecuencia de busqueda en el tiempo
     - Cambios en las necesidades de informacion (tendencias)
   * - Palabras populares
     - Temas de interes en toda la organizacion

Datos recopilados por Fess
============================

Fess recopila y almacena automaticamente los siguientes datos.

Registros de busqueda (``fess_log.search_log``)
-------------------------------------------------

Se pueden consultar en la consola de administracion en [Informacion del sistema] > [Registro de busqueda].
Se almacenan en el indice de OpenSearch ``fess_log.search_log``.

Campos principales:

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Nombre del campo
     - Tipo
     - Descripcion
   * - ``searchWord``
     - keyword
     - Palabra clave de busqueda
   * - ``requestedAt``
     - date
     - Fecha y hora de la busqueda
   * - ``hitCount``
     - long
     - Numero de resultados de busqueda (0 indica una consulta sin resultados)
   * - ``queryTime``
     - long
     - Tiempo de ejecucion de la consulta (milisegundos)
   * - ``responseTime``
     - long
     - Tiempo total de respuesta (milisegundos)
   * - ``userAgent``
     - keyword
     - Agente de usuario
   * - ``clientIp``
     - keyword
     - Direccion IP del cliente
   * - ``accessType``
     - keyword
     - Tipo de acceso (web, json, gsa, admin, etc.)
   * - ``queryId``
     - keyword
     - ID de consulta (utilizado para vincular con registros de clics)

Registros de clics (``fess_log.click_log``)
---------------------------------------------

Son registros de cuando se hace clic en los enlaces de los resultados de busqueda.
Se almacenan en el indice de OpenSearch ``fess_log.click_log``.

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Nombre del campo
     - Tipo
     - Descripcion
   * - ``url``
     - keyword
     - URL clicada
   * - ``queryId``
     - keyword
     - queryId del registro de busqueda (identifica que busqueda llevo al clic)
   * - ``order``
     - integer
     - Posicion de visualizacion en los resultados de busqueda
   * - ``requestedAt``
     - date
     - Fecha y hora del clic
   * - ``docId``
     - keyword
     - ID del documento

Palabras populares
-------------------

Las palabras populares que se muestran en la pantalla de busqueda se agregan a partir de los registros de busqueda en el indice suggest de Fess.
Las consultas que superan un cierto numero de resultados de busqueda se clasifican segun el numero de busquedas.

Visualizacion con OpenSearch Dashboards
=========================================

Dado que los registros de busqueda de Fess se almacenan en OpenSearch, es posible realizar una visualizacion avanzada utilizando OpenSearch Dashboards.

Configuracion de OpenSearch Dashboards
----------------------------------------

Agregue OpenSearch Dashboards a su configuracion de Docker Compose.

.. code-block:: yaml

    services:
      opensearch-dashboards:
        image: opensearchproject/opensearch-dashboards:3.6.0
        ports:
          - "5601:5601"
        environment:
          OPENSEARCH_HOSTS: '["http://opensearch:9200"]'
          DISABLE_SECURITY_DASHBOARDS_PLUGIN: "true"

Acceda a ``http://localhost:5601`` para utilizar la interfaz de Dashboards.

Creacion de patrones de indice
--------------------------------

Para visualizar los datos de registro de Fess en OpenSearch Dashboards, primero debe crear patrones de indice.

1. Acceda a Dashboards y seleccione [Stack Management] > [Index Patterns] en el menu izquierdo
2. Haga clic en [Create index pattern]
3. Cree los siguientes patrones de indice

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - Patron de indice
     - Campo de tiempo
     - Proposito
   * - ``fess_log.search_log``
     - ``requestedAt``
     - Analisis de registros de busqueda
   * - ``fess_log.click_log``
     - ``requestedAt``
     - Analisis de registros de clics

Diseno del panel
==================

Disene el panel con las siguientes perspectivas analiticas.
Cree cada visualizacion desde [Visualize] en el menu izquierdo y combinelas en un [Dashboard].

Resumen del uso de busqueda
-----------------------------

**Tendencia diaria de busquedas**

Comprenda como cambia el uso de la busqueda a lo largo del tiempo.

- Patron de indice: ``fess_log.search_log``
- Visualizacion: Line (grafico de lineas)
- Eje X: Date Histogram (campo: ``requestedAt``, intervalo: 1d)
- Eje Y: Count

Si el uso aumenta, es evidencia de que el sistema de busqueda se ha consolidado; si disminuye, se necesitan mejoras.

**Busquedas por hora del dia**

Comprenda en que momentos del dia se realizan mas busquedas.

- Visualizacion: Vertical Bar (grafico de barras)
- Eje X: Date Histogram (campo: ``requestedAt``, intervalo: 1h)
- Eje Y: Count

Si las busquedas son frecuentes al inicio de la jornada laboral o despues del almuerzo, indica que la recopilacion de informacion se ha convertido en una parte establecida del trabajo diario.

Analisis de la calidad de busqueda
------------------------------------

**Tendencia de la tasa de consultas sin resultados**

La tasa de consultas sin resultados es un indicador importante de la calidad de busqueda.
Los registros donde el campo ``hitCount`` en el registro de busqueda es ``0`` corresponden a consultas sin resultados.

- Patron de indice: ``fess_log.search_log``
- Filtro: Agregar ``hitCount: 0`` para extraer consultas sin resultados
- Visualizacion: Line (grafico de lineas)
- Eje X: Date Histogram (campo: ``requestedAt``, intervalo: 1d)
- Eje Y: Count

Si la tasa de consultas sin resultados es alta, es necesario agregar sinonimos o ampliar el alcance del rastreo (vease la Parte 8).

Tenga en cuenta que tambien puede ver una lista de consultas sin resultados en la consola de administracion en [Informacion del sistema] > [Registro de busqueda].

**Nube de palabras de consultas sin resultados**

Mostrar las consultas sin resultados como una nube de palabras proporciona una vision rapida de que informacion falta.

- Filtro: ``hitCount: 0``
- Visualizacion: Tag Cloud
- Campo: Terms Aggregation (campo: ``searchWord``, tamano: 50)

Analisis del valor del contenido
----------------------------------

**Resultados de busqueda mas clicados**

Los resultados de busqueda que reciben clics con frecuencia representan contenido de alto valor para la organizacion.

- Patron de indice: ``fess_log.click_log``
- Visualizacion: Data Table
- Campo: Terms Aggregation (campo: ``url``, tamano: 20, orden: Count descendente)

Priorice el mantenimiento y la actualizacion de estos contenidos.

**Distribucion de posiciones de clic**

Revise la distribucion de en que posicion de los resultados de busqueda se hace clic.

- Patron de indice: ``fess_log.click_log``
- Visualizacion: Vertical Bar (grafico de barras)
- Eje X: Histogram (campo: ``order``, intervalo: 1)
- Eje Y: Count

Si las posiciones 1-3 reciben la mayoria de los clics, la calidad de busqueda es buena; si las posiciones 10 en adelante reciben muchos clics, se necesitan mejoras en el ranking.

Analisis de tendencias en las necesidades de informacion
----------------------------------------------------------

**Ranking de palabras clave populares**

Comprenda en que esta interesada la organizacion en su conjunto.

- Patron de indice: ``fess_log.search_log``
- Visualizacion: Data Table
- Campo: Terms Aggregation (campo: ``searchWord``, tamano: 20, orden: Count descendente)

Los cambios en las palabras clave populares reflejan los cambios en los desafios e intereses de la organizacion.

Aprovechamiento de los resultados del analisis
=================================================

Los resultados del analisis de datos de busqueda pueden aplicarse a las siguientes iniciativas.

Estrategia de contenido
-------------------------

- **Consultas sin resultados**: Identificar contenido faltante y solicitar su creacion
- **Palabras clave populares**: Enriquecer la informacion sobre temas buscados con frecuencia
- **Resultados con baja tasa de clics**: Considerar la mejora o eliminacion del contenido

Mejora de la calidad de busqueda
----------------------------------

- **Agregar sinonimos**: Descubrir candidatos a sinonimos a partir de consultas sin resultados
- **Configuracion de Key Match**: Establecer resultados optimos para consultas populares
- **Ajuste de Boost**: Mejorar los rankings basandose en las tasas de clics

Decisiones de inversion en TI
-------------------------------

- **Aumento del uso**: Planificar la ampliacion de recursos del servidor
- **Nuevas necesidades de informacion**: Considerar la conexion de fuentes de datos adicionales
- **Necesidades de funciones de IA**: Decidir sobre la introduccion del modo de busqueda con IA (vease la Parte 19)

Creacion de informes periodicos
=================================

Resuma los resultados del analisis en informes periodicos y compartalos con las partes interesadas.

Ejemplo de elementos del informe mensual
-------------------------------------------

1. Resumen del uso de busqueda (total de busquedas, comparacion con el mes anterior)
2. Tendencia de la tasa de consultas sin resultados y estado de mejora
3. Top 10 de palabras clave populares
4. Brechas de conocimiento recien descubiertas
5. Medidas de mejora implementadas y sus efectos
6. Planes de mejora para el proximo mes

Conclusion
===========

En este articulo, explicamos como visualizar la utilizacion del conocimiento organizacional mediante registros de busqueda.

- Informacion obtenida de los registros de busqueda (necesidades de informacion, brechas de conocimiento, valor del contenido)
- Construccion de paneles de visualizacion con OpenSearch Dashboards
- Aplicacion de los resultados del analisis a la estrategia de contenido, mejora de la calidad de busqueda e inversiones en TI
- Mejora continua a traves de informes periodicos

Los datos de busqueda son un activo valioso para dibujar un "mapa de conocimiento organizacional."
Con esto concluye la seccion de IA y busqueda de proxima generacion. En la proxima y ultima entrega, presentaremos un resumen general de la serie.

Referencias
============

- `Registro de busqueda de Fess <https://fess.codelibs.org/ja/15.5/admin/searchlog.html>`__

- `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/>`__
