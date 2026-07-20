====================================
Configuración de control de carga
====================================

Descripción general
===================

|Fess| incluye dos tipos de funciones de control de carga que protegen la estabilidad del sistema en función del uso de CPU.

**Control de carga de solicitudes HTTP** (``web.load.control`` / ``api.load.control``):

- Monitoreo en tiempo real del uso de CPU del cluster de OpenSearch
- Umbrales independientes para solicitudes web y solicitudes API
- Devuelve HTTP 429 (Too Many Requests) cuando se superan los umbrales
- El panel de administración, el inicio de sesión y los recursos estáticos están excluidos del control
- Deshabilitado por defecto (umbral=100)

**Control de carga adaptativo** (``adaptive.load.control``):

- Monitorea el uso de CPU del sistema del propio servidor Fess
- Regula automáticamente las tareas en segundo plano como rastreo, indexación, actualizaciones de sugerencias y generación de miniaturas
- Cuando el uso de CPU alcanza o supera el umbral, los hilos de procesamiento se pausan y se reanudan cuando desciende por debajo del umbral
- Habilitado por defecto (umbral=50)

Configuración del control de carga de solicitudes HTTP
======================================================

Configure las siguientes propiedades en ``fess_config.properties``:

::

    # Umbral de uso de CPU para solicitudes web (%)
    # Las solicitudes se rechazan cuando el uso de CPU de OpenSearch alcanza o supera este valor
    # Establecer en 100 para deshabilitar (predeterminado: 100)
    web.load.control=100

    # Umbral de uso de CPU para solicitudes API (%)
    # Las solicitudes se rechazan cuando el uso de CPU de OpenSearch alcanza o supera este valor
    # Establecer en 100 para deshabilitar (predeterminado: 100)
    api.load.control=100

    # Intervalo de monitoreo de uso de CPU (segundos)
    # Intervalo para obtener el uso de CPU del cluster de OpenSearch
    # Predeterminado: 1
    load.control.monitor.interval=1

.. note::
   Cuando tanto ``web.load.control`` como ``api.load.control`` están establecidos en 100 (predeterminado),
   el monitoreo de CPU de OpenSearch no se inicia.

Cómo funciona
=============

Mecanismo de monitoreo
----------------------

Cuando el control de carga está habilitado (algún umbral es inferior a 100), LoadControlMonitorTarget monitorea periódicamente el uso de CPU del cluster de OpenSearch.

- Obtiene estadísticas del SO de todos los nodos del cluster de OpenSearch
- Registra el uso de CPU más alto entre todos los nodos
- Monitorea en el intervalo especificado por ``load.control.monitor.interval`` (predeterminado: 1 segundo)
- El monitoreo se inicia de forma diferida en la primera solicitud

.. note::
   Si falla la obtención de información de monitoreo, el uso de CPU se restablece a 0.
   Hasta el tercer fallo consecutivo, el nivel de log es WARNING; a partir del cuarto fallo, cambia a DEBUG
   (para evitar que los fallos continuos hinchen los logs). El contador de fallos se reinicia cuando el monitoreo tiene éxito al menos una vez.

Control de solicitudes
----------------------

Cuando llega una solicitud, LoadControlFilter la procesa en el siguiente orden:

1. Verificar si la ruta está excluida (si está excluida, dejar pasar)
2. Determinar el tipo de solicitud (Web / API)
3. Obtener el umbral correspondiente
4. Si el umbral es 100 o superior, no controlar (dejar pasar)
5. Comparar el uso actual de CPU con el umbral
6. Si el uso de CPU >= umbral, devolver HTTP 429

**Solicitudes excluidas:**

- Rutas que comienzan con ``/admin`` (panel de administración)
- Rutas que comienzan con ``/error`` (páginas de error)
- Rutas que comienzan con ``/login`` (páginas de inicio de sesión)
- Recursos estáticos (``.css``, ``.js``, ``.png``, ``.jpg``, ``.gif``, ``.ico``, ``.svg``, ``.woff``, ``.woff2``, ``.ttf``, ``.eot``)

**Para solicitudes web:**

- Devuelve el código de estado HTTP 429
- Muestra la página de error (``busy.jsp``)

**Para solicitudes API:**

- Devuelve el código de estado HTTP 429
- Adjunta el encabezado de respuesta HTTP ``Retry-After: 60``
- Devuelve una respuesta JSON:

::

    {
        "response": {
            "status": 9,
            "message": "Server is busy. Please retry after 60 seconds.",
            "retry_after": 60
        }
    }

.. note::
   Cuando una solicitud es rechazada, el servidor registra a nivel INFO el mensaje
   ``Rejecting request due to high CPU load: path=..., cpu=...%, threshold=...%``.
   Esto permite verificar qué rutas fueron rechazadas y con qué umbral.

Ejemplos de configuración
=========================

Limitar solo solicitudes web
-----------------------------

Configuración que limita solo las solicitudes de búsqueda web sin restringir la API:

::

    # Web: Rechazar solicitudes cuando el uso de CPU es 80% o superior
    web.load.control=80

    # API: Sin restriccion
    api.load.control=100

    # Intervalo de monitoreo: 1 segundo
    load.control.monitor.interval=1

Limitar tanto web como API
--------------------------

Ejemplo con diferentes umbrales para web y API:

::

    # Web: Rechazar solicitudes cuando el uso de CPU es 70% o superior
    web.load.control=70

    # API: Rechazar solicitudes cuando el uso de CPU es 80% o superior
    api.load.control=80

    # Intervalo de monitoreo: 2 segundos
    load.control.monitor.interval=2

.. note::
   Al establecer el umbral de API más alto que el de web, puede lograr un control escalonado
   donde las solicitudes web se restringen primero durante alta carga, y las solicitudes API tambien
   se restringen cuando la carga aumenta aún más.

Diferencia con el límite de tasa
=================================

|Fess| tiene una función de :doc:`rate-limiting` separada del control de carga.
Estas protegen el sistema usando enfoques diferentes.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Aspecto
     - Límite de tasa
     - Control de carga
   * - Base de control
     - Número de solicitudes (por unidad de tiempo)
     - Uso de CPU de OpenSearch
   * - Propósito
     - Prevención de solicitudes excesivas
     - Protección del motor de búsqueda contra alta carga
   * - Unidad de límite
     - Por dirección IP
     - Todo el sistema
   * - Respuesta
     - HTTP 429
     - HTTP 429
   * - Alcance
     - Todas las solicitudes HTTP
     - Solicitudes web / Solicitudes API (panel de administración etc. excluido)

Combinar ambas funciones permite una protección del sistema más robusta.

Control de carga adaptativo
===========================

El control de carga adaptativo ajusta automáticamente la velocidad de procesamiento de las tareas
en segundo plano en función del uso de CPU del sistema del servidor Fess.

Configuración
-------------

``fess_config.properties``:

::

    # Umbral de uso de CPU del control de carga adaptativo (%)
    # Pausa las tareas en segundo plano cuando el uso de CPU del sistema alcanza o supera este valor
    # Establecer en 0 o menos para deshabilitar (predeterminado: 50)
    adaptive.load.control=50

Comportamiento
--------------

- Monitorea el uso de CPU del sistema del servidor donde se ejecuta Fess
- Cuando el uso de CPU alcanza o supera el umbral, los hilos de procesamiento afectados esperan hasta que el uso de CPU descienda por debajo del umbral
- Cuando el uso de CPU desciende por debajo del umbral, el procesamiento se reanuda automáticamente

**Tareas en segundo plano afectadas:**

- Rastreo (Web / Sistema de archivos)
- Indexación (registro de documentos)
- Procesamiento de almacén de datos
- Actualizaciones de sugerencias
- Generación de miniaturas
- Respaldo y restauración

.. note::
   El control de carga adaptativo está habilitado por defecto (umbral=50).
   Opera de forma independiente del control de carga de solicitudes HTTP (``web.load.control`` / ``api.load.control``).

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Aspecto
     - Control de carga de solicitudes HTTP
     - Control de carga adaptativo
   * - Objetivo de monitoreo
     - Uso de CPU de OpenSearch
     - Uso de CPU del sistema del servidor Fess
   * - Objetivo de control
     - Solicitudes HTTP (Web / API)
     - Tareas en segundo plano
   * - Método de control
     - Rechaza solicitudes devolviendo HTTP 429
     - Pausa temporalmente los hilos de procesamiento
   * - Predeterminado
     - Deshabilitado (umbral=100)
     - Habilitado (umbral=50)

Solución de problemas
=====================

El control de carga no se activa
---------------------------------

**Causa**: La configuración no se refleja correctamente

**Verificaciones**:

1. Si ``web.load.control`` o ``api.load.control`` está establecido por debajo de 100
2. Si el archivo de configuración se está leyendo correctamente
3. Si |Fess| fue reiniciado

Solicitudes legítimas son rechazadas
--------------------------------------

**Causa**: Los umbrales son demasiado bajos

**Solución**:

1. Aumentar los valores de ``web.load.control`` o ``api.load.control``
2. Ajustar ``load.control.monitor.interval`` para cambiar la frecuencia de monitoreo
3. Aumentar los recursos del cluster de OpenSearch

.. warning::
   Establecer umbrales demasiado bajos puede causar que las solicitudes sean rechazadas incluso bajo carga normal.
   Verifique el uso normal de CPU de su cluster de OpenSearch antes de establecer umbrales apropiados.

El rastreo es lento
-------------------

**Causa**: Los hilos están en estado de espera debido al control de carga adaptativo

**Verificaciones**:

1. Si ``Cpu Load XX% is greater than YY%`` aparece en los logs
2. Si el umbral de ``adaptive.load.control`` es demasiado bajo

**Solución**:

1. Aumentar el valor de ``adaptive.load.control`` (ej: 70)
2. Aumentar los recursos de CPU del servidor Fess
3. Establecer en 0 para deshabilitar el control de carga adaptativo (no recomendado)

Información de referencia
=========================

- :doc:`rate-limiting` - Configuración de límite de tasa
