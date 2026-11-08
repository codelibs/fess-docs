========================================================================================
Parte 22: Dibujando un mapa de conocimiento organizacional a partir de datos de búsqueda
========================================================================================

Introducción
=============

Un sistema de búsqueda es una herramienta para "encontrar" información, pero los propios registros de búsqueda también son una valiosa fuente de información.
"¿Qué se busca?", "¿Qué no se puede encontrar?", "¿Qué información se consulta con frecuencia?" -- estos datos sirven como un espejo que refleja las necesidades de información y las brechas de conocimiento de la organización.

En este artículo, combinamos los registros de búsqueda de Fess con OpenSearch Dashboards para construir un panel de análisis que visualiza el estado de utilización del conocimiento en la organización.

Público objetivo
=================

- Personas que desean comprender cuantitativamente cómo se utiliza su sistema de búsqueda
- Personas que desean recopilar datos para estrategias de utilización de la información
- Personas que desean aprender las operaciones básicas de OpenSearch Dashboards

El valor de los datos de búsqueda
==================================

Lo que los registros de búsqueda pueden revelar
-------------------------------------------------

Los registros de búsqueda son un tipo de datos poco común que permite comprender cuantitativamente las necesidades de información de una organización.

.. list-table:: Información obtenida de los datos de búsqueda
   :header-rows: 1
   :widths: 30 70

   * - Datos
     - Información
   * - Palabras clave de búsqueda
     - Que buscan los empleados (necesidades de información)
   * - Consultas sin resultados
     - Información que falta en la organización (brechas de conocimiento)
   * - Registros de clics
     - Que resultados de búsqueda fueron útiles (valor del contenido)
   * - Frecuencia de búsqueda en el tiempo
     - Cambios en las necesidades de información (tendencias)
   * - Palabras populares
     - Temas de interés en toda la organización

Datos recopilados por Fess
============================

Fess recopila y almacena automáticamente los siguientes datos.

Registros de búsqueda (``fess_log.search_log``)
-------------------------------------------------

Se pueden consultar en la consola de administración en [Información del sistema] > [Registro de búsqueda].
Se almacenan en el índice de OpenSearch ``fess_log.search_log``.

Campos principales:

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Nombre del campo
     - Tipo
     - Descripción
   * - ``searchWord``
     - keyword
     - Palabra clave de búsqueda
   * - ``requestedAt``
     - date
     - Fecha y hora de la búsqueda
   * - ``hitCount``
     - long
     - Número de resultados de búsqueda (0 indica una consulta sin resultados)
   * - ``queryTime``
     - long
     - Tiempo de ejecución de la consulta (milisegundos)
   * - ``responseTime``
     - long
     - Tiempo total de respuesta (milisegundos)
   * - ``userAgent``
     - keyword
     - Agente de usuario
   * - ``clientIp``
     - keyword
     - Dirección IP del cliente
   * - ``accessType``
     - keyword
     - Tipo de acceso (web, json, gsa, admin, etc.)
   * - ``queryId``
     - keyword
     - ID de consulta (utilizado para vincular con registros de clics)

Registros de clics (``fess_log.click_log``)
---------------------------------------------

Son registros de cuando se hace clic en los enlaces de los resultados de búsqueda.
Se almacenan en el índice de OpenSearch ``fess_log.click_log``.

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Nombre del campo
     - Tipo
     - Descripción
   * - ``url``
     - keyword
     - URL clicada
   * - ``queryId``
     - keyword
     - queryId del registro de búsqueda (identifica que búsqueda llevo al clic)
   * - ``order``
     - integer
     - Posición de visualización en los resultados de búsqueda
   * - ``requestedAt``
     - date
     - Fecha y hora del clic
   * - ``docId``
     - keyword
     - ID del documento

Palabras populares
-------------------

Las palabras populares que se muestran en la pantalla de búsqueda se agregan a partir de los registros de búsqueda en el índice suggest de Fess.
Las consultas que superan un cierto número de resultados de búsqueda se clasifican según el número de búsquedas.

Visualización con OpenSearch Dashboards
=========================================

Dado que los registros de búsqueda de Fess se almacenan en OpenSearch, es posible realizar una visualización avanzada utilizando OpenSearch Dashboards.

Configuración de OpenSearch Dashboards
----------------------------------------

Agregue OpenSearch Dashboards a su configuración de Docker Compose.

.. code-block:: yaml

    services:
      opensearch-dashboards:
        image: public.ecr.aws/opensearchproject/opensearch-dashboards:3.6.0
        ports:
          - "5601:5601"
        environment:
          OPENSEARCH_HOSTS: '["http://opensearch:9200"]'
          DISABLE_SECURITY_DASHBOARDS_PLUGIN: "true"

Acceda a ``http://localhost:5601`` para utilizar la interfaz de Dashboards.

Creación de patrones de índice
--------------------------------

Para visualizar los datos de registro de Fess en OpenSearch Dashboards, primero debe crear patrones de índice.

1. Acceda a Dashboards y seleccione [Stack Management] > [Index Patterns] en el menú izquierdo
2. Haga clic en [Create index pattern]
3. Cree los siguientes patrones de índice

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - Patrón de índice
     - Campo de tiempo
     - Propósito
   * - ``fess_log.search_log``
     - ``requestedAt``
     - Análisis de registros de búsqueda
   * - ``fess_log.click_log``
     - ``requestedAt``
     - Análisis de registros de clics

Diseño del panel
==================

Diseñe el panel con las siguientes perspectivas analíticas.
Cree cada visualización desde [Visualize] en el menú izquierdo y combínelas en un [Dashboard].

Resumen del uso de búsqueda
-----------------------------

**Tendencia diaria de búsquedas**

Comprenda como cambia el uso de la búsqueda a lo largo del tiempo.

- Patrón de índice: ``fess_log.search_log``
- Visualización: Line (gráfico de líneas)
- Eje X: Date Histogram (campo: ``requestedAt``, intervalo: 1d)
- Eje Y: Count

Si el uso aumenta, es evidencia de que el sistema de búsqueda se ha consolidado; si disminuye, se necesitan mejoras.

**Búsquedas por hora del día**

Comprenda en que momentos del día se realizan más búsquedas.

- Visualización: Vertical Bar (gráfico de barras)
- Eje X: Date Histogram (campo: ``requestedAt``, intervalo: 1h)
- Eje Y: Count

Si las búsquedas son frecuentes al inicio de la jornada laboral o después del almuerzo, indica que la recopilación de información se ha convertido en una parte establecida del trabajo diario.

Análisis de la calidad de búsqueda
------------------------------------

**Tendencia de la tasa de consultas sin resultados**

La tasa de consultas sin resultados es un indicador importante de la calidad de búsqueda.
Los registros donde el campo ``hitCount`` en el registro de búsqueda es ``0`` corresponden a consultas sin resultados.

- Patrón de índice: ``fess_log.search_log``
- Filtro: Agregar ``hitCount: 0`` para extraer consultas sin resultados
- Visualización: Line (gráfico de líneas)
- Eje X: Date Histogram (campo: ``requestedAt``, intervalo: 1d)
- Eje Y: Count

Si la tasa de consultas sin resultados es alta, es necesario agregar sinónimos o ampliar el alcance del rastreo (véase la Parte 8).

Tenga en cuenta que también puede ver una lista de consultas sin resultados en la consola de administración en [Información del sistema] > [Registro de búsqueda].

**Nube de palabras de consultas sin resultados**

Mostrar las consultas sin resultados como una nube de palabras proporciona una visión rápida de que información falta.

- Filtro: ``hitCount: 0``
- Visualización: Tag Cloud
- Campo: Terms Aggregation (campo: ``searchWord``, tamaño: 50)

Análisis del valor del contenido
----------------------------------

**Resultados de búsqueda más clicados**

Los resultados de búsqueda que reciben clics con frecuencia representan contenido de alto valor para la organización.

- Patrón de índice: ``fess_log.click_log``
- Visualización: Data Table
- Campo: Terms Aggregation (campo: ``url``, tamaño: 20, orden: Count descendente)

Priorice el mantenimiento y la actualización de estos contenidos.

**Distribución de posiciones de clic**

Revise la distribución de en que posición de los resultados de búsqueda se hace clic.

- Patrón de índice: ``fess_log.click_log``
- Visualización: Vertical Bar (gráfico de barras)
- Eje X: Histogram (campo: ``order``, intervalo: 1)
- Eje Y: Count

Si las posiciones 1-3 reciben la mayoría de los clics, la calidad de búsqueda es buena; si las posiciones 10 en adelante reciben muchos clics, se necesitan mejoras en el ranking.

Análisis de tendencias en las necesidades de información
----------------------------------------------------------

**Ranking de palabras clave populares**

Comprenda en qué está interesada la organización en su conjunto.

- Patrón de índice: ``fess_log.search_log``
- Visualización: Data Table
- Campo: Terms Aggregation (campo: ``searchWord``, tamaño: 20, orden: Count descendente)

Los cambios en las palabras clave populares reflejan los cambios en los desafíos e intereses de la organización.

Aprovechamiento de los resultados del análisis
=================================================

Los resultados del análisis de datos de búsqueda pueden aplicarse a las siguientes iniciativas.

Estrategia de contenido
-------------------------

- **Consultas sin resultados**: Identificar contenido faltante y solicitar su creación
- **Palabras clave populares**: Enriquecer la información sobre temas buscados con frecuencia
- **Resultados con baja tasa de clics**: Considerar la mejora o eliminación del contenido

Mejora de la calidad de búsqueda
----------------------------------

- **Agregar sinónimos**: Descubrir candidatos a sinónimos a partir de consultas sin resultados
- **Configuración de Key Match**: Establecer resultados óptimos para consultas populares
- **Ajuste de Boost**: Mejorar los rankings basándose en las tasas de clics

Decisiones de inversión en TI
-------------------------------

- **Aumento del uso**: Planificar la ampliación de recursos del servidor
- **Nuevas necesidades de información**: Considerar la conexión de fuentes de datos adicionales
- **Necesidades de funciones de IA**: Decidir sobre la introducción del modo de búsqueda con IA (véase la Parte 19)

Creación de informes periódicos
=================================

Resuma los resultados del análisis en informes periódicos y compártalos con las partes interesadas.

Ejemplo de elementos del informe mensual
-------------------------------------------

1. Resumen del uso de búsqueda (total de búsquedas, comparación con el mes anterior)
2. Tendencia de la tasa de consultas sin resultados y estado de mejora
3. Top 10 de palabras clave populares
4. Brechas de conocimiento recién descubiertas
5. Medidas de mejora implementadas y sus efectos
6. Planes de mejora para el próximo mes

Conclusión
===========

En este artículo, explicamos cómo visualizar la utilización del conocimiento organizacional mediante registros de búsqueda.

- Información obtenida de los registros de búsqueda (necesidades de información, brechas de conocimiento, valor del contenido)
- Construcción de paneles de visualización con OpenSearch Dashboards
- Aplicación de los resultados del análisis a la estrategia de contenido, mejora de la calidad de búsqueda e inversiones en TI
- Mejora continua a través de informes periódicos

Los datos de búsqueda son un activo valioso para dibujar un "mapa de conocimiento organizacional."
Con esto concluye la sección de IA y búsqueda de próxima generación. En la próxima y última entrega, presentaremos un resumen general de la serie.

Referencias
============

- `Registro de búsqueda de Fess <https://fess.codelibs.org/ja/15.5/admin/searchlog.html>`__

- `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/>`__
