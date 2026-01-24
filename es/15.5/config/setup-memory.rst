=====================
Configuración de Memoria
=====================

Descripción General
===================

En aplicaciones Java, es necesario configurar la memoria heap máxima utilizada por cada proceso.
En |Fess|, la configuración de memoria se realiza para cada uno de los siguientes tres componentes:

- Aplicación Web Fess
- Proceso del Rastreador
- OpenSearch

Una configuración de memoria apropiada permite mejorar el rendimiento y lograr una operación estable.

Configuración de Memoria de la Aplicación Web Fess
===================================================

Cuándo es Necesaria la Configuración
-------------------------------------

Considere ajustar el tamaño de memoria en los siguientes casos:

- Se registran errores OutOfMemory en ``fess.log``
- Es necesario procesar un gran número de accesos simultáneos
- Las operaciones de la pantalla de administración son lentas o se produce timeout

El tamaño de memoria predeterminado es suficiente para uso general, pero se requiere incremento en entornos de alta carga.

Configuración mediante Variables de Entorno
--------------------------------------------

Configure la variable de entorno ``FESS_HEAP_SIZE``.

::

    export FESS_HEAP_SIZE=2g

Unidades:

- ``m``: megabytes
- ``g``: gigabytes

Para Paquetes RPM/DEB
----------------------

Para instalación con paquete RPM, edite ``/etc/sysconfig/fess``.

::

    FESS_HEAP_SIZE=2g

Para paquetes DEB, edite ``/etc/default/fess``.

::

    FESS_HEAP_SIZE=2g

.. warning::
   Después de cambiar el tamaño de memoria, es necesario reiniciar el servicio |Fess|.

Tamaños de Memoria Recomendados
--------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Entorno
     - Tamaño Heap Recomendado
     - Observaciones
   * - Entorno de Desarrollo/Prueba
     - 512m〜1g
     - Índice de pequeña escala
   * - Entorno de Producción Pequeño
     - 1g〜2g
     - Decenas a cientos de miles de documentos
   * - Entorno de Producción Mediano
     - 2g〜4g
     - Cientos de miles a millones de documentos
   * - Entorno de Producción Grande
     - 4g〜8g
     - Millones o más documentos

Configuración de Memoria del Rastreador
========================================

Cuándo es Necesaria la Configuración
-------------------------------------

Es necesario aumentar el tamaño de memoria del rastreador en los siguientes casos:

- Al aumentar el número de rastreos paralelos
- Al rastrear archivos grandes
- Cuando ocurren errores OutOfMemory durante la ejecución del rastreo

Método de Configuración
------------------------

Edite ``app/WEB-INF/classes/fess_config.properties`` o ``/etc/fess/fess_config.properties``.

::

    jvm.crawler.options=-Xmx512m

Por ejemplo, para cambiar a 1GB:

::

    jvm.crawler.options=-Xmx1g

.. note::
   Esta configuración se aplica por unidad de proceso del rastreador (por unidad de trabajo del programador).
   Si ejecuta múltiples trabajos de rastreo simultáneamente, cada trabajo utilizará la memoria especificada.

Configuración Recomendada
--------------------------

- **Rastreo Web normal**: 512m〜1g
- **Rastreo paralelo masivo**: 1g〜2g
- **Rastreo de archivos grandes**: 2g〜4g

Opciones Detalladas de JVM
---------------------------

Las opciones detalladas de JVM para el rastreador se pueden configurar en ``jvm.crawler.options``.
La configuración predeterminada incluye las siguientes optimizaciones.

**Opciones principales:**

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Opción
     - Descripción
   * - ``-Xms128m -Xmx512m``
     - Tamaño heap inicial y máximo
   * - ``-XX:MaxMetaspaceSize=128m``
     - Tamaño máximo de Metaspace
   * - ``-XX:+UseG1GC``
     - Uso del recolector de basura G1
   * - ``-XX:MaxGCPauseMillis=60000``
     - Tiempo objetivo de pausa de GC (60 segundos)
   * - ``-XX:-HeapDumpOnOutOfMemoryError``
     - Desactivar heap dump en OutOfMemory

Configuración de Memoria de OpenSearch
=======================================

Consideraciones Importantes
----------------------------

Para OpenSearch, es necesario considerar los siguientes dos puntos al configurar la memoria:

1. **Memoria Heap Java**: Utilizada por el proceso de OpenSearch
2. **Caché del Sistema de Archivos del SO**: Importante para el rendimiento de búsqueda

.. warning::
   Si hace la memoria heap Java demasiado grande, disminuirá la memoria disponible
   para la caché del sistema de archivos del SO, reduciendo el rendimiento de búsqueda.

Método de Configuración
------------------------

Entorno Linux
~~~~~~~~~~~~~

La memoria heap de OpenSearch se especifica mediante variables de entorno o el archivo de configuración de OpenSearch.

Configuración mediante variable de entorno:

::

    export OPENSEARCH_HEAP_SIZE=2g

O edite ``config/jvm.options``:

::

    -Xms2g
    -Xmx2g

.. note::
   Se recomienda configurar el tamaño heap mínimo (``-Xms``) y el tamaño heap máximo (``-Xmx``) al mismo valor.

Entorno Windows
~~~~~~~~~~~~~~~

Edite el archivo ``config\jvm.options``.

::

    -Xms2g
    -Xmx2g

Tamaños de Memoria Recomendados
--------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Tamaño del Índice
     - Tamaño Heap Recomendado
     - Memoria Total Recomendada
   * - 〜10GB
     - 2g
     - 4GB o más
   * - 10GB〜50GB
     - 4g
     - 8GB o más
   * - 50GB〜100GB
     - 8g
     - 16GB o más
   * - 100GB o más
     - 16g〜31g
     - 32GB o más

.. warning::
   No configure la memoria heap de OpenSearch por encima de 32GB.
   Superar 32GB desactiva Compressed OOP y reduce la eficiencia de memoria.

Mejores Prácticas
-----------------

1. **Asignar el 50% de la memoria física al heap**

   Asigne aproximadamente el 50% de la memoria física del servidor al heap de OpenSearch.
   El resto se utiliza para el SO y la caché del sistema de archivos.

2. **Máximo de 31GB**

   El tamaño heap debe ser hasta 31GB como máximo; si se necesita más, aumente el número de nodos.

3. **Verificación en Entorno de Producción**

   Consulte la documentación oficial de OpenSearch y realice la configuración óptima según su entorno.

Configuración de Memoria para Procesamiento de Sugerencias y Miniaturas
========================================================================

Proceso de Generación de Sugerencias
-------------------------------------

La configuración de memoria para el proceso de generación de sugerencias se configura en ``jvm.suggest.options``.

::

    jvm.suggest.options=-Xmx256m

Por defecto se utiliza la siguiente configuración:

- Heap inicial: 128MB
- Heap máximo: 256MB
- Metaspace máximo: 128MB

Proceso de Generación de Miniaturas
------------------------------------

La configuración de memoria para el proceso de generación de miniaturas se configura en ``jvm.thumbnail.options``.

::

    jvm.thumbnail.options=-Xmx256m

Por defecto se utiliza la siguiente configuración:

- Heap inicial: 128MB
- Heap máximo: 256MB
- Metaspace máximo: 128MB

.. note::
   Si procesa imágenes grandes en la generación de miniaturas, es necesario aumentar la memoria.

Monitoreo y Ajuste de Memoria
==============================

Verificación del Uso de Memoria
--------------------------------

Uso de Memoria de Fess
~~~~~~~~~~~~~~~~~~~~~~~

Puede verificar en "Información del Sistema" en la pantalla de administración.

O utilice herramientas de monitoreo de JVM:

::

    jps -l  # Verificar proceso de Fess
    jstat -gcutil <PID> 1000  # Mostrar estadísticas de GC cada segundo

Uso de Memoria de OpenSearch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    curl -X GET "localhost:9201/_nodes/stats/jvm?pretty"
    curl -X GET "localhost:9201/_cat/nodes?v&h=heap.percent,ram.percent"

Síntomas de Falta de Memoria
-----------------------------

Si aparecen los siguientes síntomas, es posible que haya falta de memoria.

**Aplicación Web Fess:**

- Respuesta lenta
- ``OutOfMemoryError`` registrado en logs
- El proceso termina inesperadamente

**Rastreador:**

- El rastreo se detiene a mitad
- ``OutOfMemoryError`` registrado en ``fess_crawler.log``
- Falla el rastreo de archivos grandes

**OpenSearch:**

- Búsqueda lenta
- Creación de índice lenta
- Ocurre error ``circuit_breaker_exception``

Procedimiento de Ajuste
------------------------

1. **Verificar el uso actual de memoria**

   Monitoree el uso de memoria de cada componente.

2. **Identificar el cuello de botella**

   Identifique qué componente tiene falta de memoria.

3. **Aumentar gradualmente**

   En lugar de aumentar mucho de una vez, aumente en incrementos del 25-50% y verifique el efecto.

4. **Considerar el equilibrio del sistema completo**

   Asegúrese de que el total de memoria de cada componente no exceda la memoria física.

5. **Monitoreo continuo**

   Monitoree continuamente el uso de memoria y ajuste según sea necesario.

Contramedidas para Fugas de Memoria
------------------------------------

Si se sospecha una fuga de memoria:

1. **Obtener heap dump**

::

    jmap -dump:format=b,file=heap.bin <PID>

2. **Análisis del heap dump**

   Analice con herramientas como Eclipse Memory Analyzer (MAT).

3. **Reportar el problema**

   Si descubre una fuga de memoria, repórtela en GitHub Issues.

Solución de Problemas
======================

Ocurre OutOfMemoryError
------------------------

**Aplicación Web Fess:**

1. Aumente ``FESS_HEAP_SIZE``.
2. Limite el número de accesos simultáneos.
3. Reduzca el nivel de log para disminuir el uso de memoria por salida de logs.

**Rastreador:**

1. Aumente ``-Xmx`` en ``jvm.crawler.options``.
2. Reduzca el número de rastreos paralelos.
3. Ajuste la configuración de rastreo para excluir archivos grandes.

**OpenSearch:**

1. Aumente el tamaño heap (hasta 31GB como máximo).
2. Revise el número de shards del índice.
3. Verifique la complejidad de las consultas.

Tiempo de Pausa Largo por GC
-----------------------------

1. Ajuste la configuración de G1GC.
2. Configure el tamaño heap apropiadamente (GC frecuente si es demasiado grande o demasiado pequeño).
3. Considere actualizar a una versión más reciente de Java.

El Rendimiento No Mejora Después de Configurar la Memoria
----------------------------------------------------------

1. Verifique otros recursos como CPU, I/O de disco, red.
2. Realice optimización del índice.
3. Revise las consultas y la configuración de rastreo.

Información de Referencia
==========================

- :doc:`setup-port-network` - Configuración de Puerto y Red
- :doc:`crawler-advanced` - Configuración Avanzada del Rastreador
- :doc:`admin-logging` - Configuración de Logs
- `OpenSearch Memory Settings <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/index/#important-settings>`_
- `Java GC Tuning <https://docs.oracle.com/en/java/javase/11/gctuning/>`_
