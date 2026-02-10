==================================
Configuracion de control de carga
==================================

Descripcion general
===================

|Fess| incluye una funcion de control de carga que controla las solicitudes en funcion del uso de CPU de OpenSearch.
Esta funcion limita automaticamente las solicitudes cuando el motor de busqueda esta bajo alta carga, protegiendo la estabilidad del sistema.

Caracteristicas del control de carga:

- Monitoreo en tiempo real del uso de CPU del cluster de OpenSearch
- Umbrales independientes para solicitudes web y solicitudes API
- Devuelve HTTP 429 (Too Many Requests) cuando se superan los umbrales
- El panel de administracion, el inicio de sesion y los recursos estaticos estan excluidos del control
- Deshabilitado por defecto (umbral=100)

Configuracion
=============

Configure las siguientes propiedades en ``fess_config.properties``:

::

    # Umbral de uso de CPU para solicitudes web (%)
    # Las solicitudes se rechazan cuando el uso de CPU alcanza o supera este valor
    # Establecer en 100 para deshabilitar (predeterminado: 100)
    web.load.control=100

    # Umbral de uso de CPU para solicitudes API (%)
    # Las solicitudes se rechazan cuando el uso de CPU alcanza o supera este valor
    # Establecer en 100 para deshabilitar (predeterminado: 100)
    api.load.control=100

    # Intervalo de monitoreo de uso de CPU (segundos)
    # Intervalo para obtener el uso de CPU del cluster de OpenSearch
    # Predeterminado: 1
    load.control.monitor.interval=1

.. note::
   Cuando tanto ``web.load.control`` como ``api.load.control`` estan establecidos en 100 (predeterminado),
   la funcion de control de carga esta completamente deshabilitada y el monitoreo no se inicia.

Como funciona
=============

Mecanismo de monitoreo
----------------------

Cuando el control de carga esta habilitado (algun umbral es inferior a 100), LoadControlMonitorTarget monitorea periodicamente el uso de CPU del cluster de OpenSearch.

- Obtiene estadisticas del SO de todos los nodos del cluster de OpenSearch
- Registra el uso de CPU mas alto entre todos los nodos
- Monitorea en el intervalo especificado por ``load.control.monitor.interval`` (predeterminado: 1 segundo)
- El monitoreo se inicia de forma diferida en la primera solicitud

.. note::
   Si falla la obtencion de informacion de monitoreo, el uso de CPU se restablece a 0.
   Despues de 3 fallos consecutivos, el nivel de log cambia de WARNING a DEBUG.

Control de solicitudes
----------------------

Cuando llega una solicitud, LoadControlFilter la procesa en el siguiente orden:

1. Verificar si la ruta esta excluida (si esta excluida, dejar pasar)
2. Determinar el tipo de solicitud (Web / API)
3. Obtener el umbral correspondiente
4. Si el umbral es 100 o superior, no controlar (dejar pasar)
5. Comparar el uso actual de CPU con el umbral
6. Si el uso de CPU >= umbral, devolver HTTP 429

**Solicitudes excluidas:**

- Rutas que comienzan con ``/admin`` (panel de administracion)
- Rutas que comienzan con ``/error`` (paginas de error)
- Rutas que comienzan con ``/login`` (paginas de inicio de sesion)
- Recursos estaticos (``.css``, ``.js``, ``.png``, ``.jpg``, ``.gif``, ``.ico``, ``.svg``, ``.woff``, ``.woff2``, ``.ttf``, ``.eot``)

**Para solicitudes web:**

- Devuelve el codigo de estado HTTP 429
- Muestra la pagina de error (``busy.jsp``)

**Para solicitudes API:**

- Devuelve el codigo de estado HTTP 429
- Devuelve una respuesta JSON:

::

    {
        "response": {
            "status": 9,
            "message": "Server is busy. Please retry after 60 seconds.",
            "retry_after": 60
        }
    }

Ejemplos de configuracion
=========================

Limitar solo solicitudes web
-----------------------------

Configuracion que limita solo las solicitudes de busqueda web sin restringir la API:

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
   Al establecer el umbral de API mas alto que el de web, puede lograr un control escalonado
   donde las solicitudes web se restringen primero durante alta carga, y las solicitudes API tambien
   se restringen cuando la carga aumenta aun mas.

Diferencia con el limite de tasa
================================

|Fess| tiene una funcion de :doc:`rate-limiting` separada del control de carga.
Estas protegen el sistema usando enfoques diferentes.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Aspecto
     - Limite de tasa
     - Control de carga
   * - Base de control
     - Numero de solicitudes (por unidad de tiempo)
     - Uso de CPU de OpenSearch
   * - Proposito
     - Prevencion de solicitudes excesivas
     - Proteccion del motor de busqueda contra alta carga
   * - Unidad de limite
     - Por direccion IP
     - Todo el sistema
   * - Respuesta
     - HTTP 429
     - HTTP 429
   * - Alcance
     - API de busqueda / API de modo IA
     - Solicitudes web / Solicitudes API

Combinar ambas funciones permite una proteccion del sistema mas robusta.

Solucion de problemas
=====================

El control de carga no se activa
---------------------------------

**Causa**: La configuracion no se refleja correctamente

**Verificaciones**:

1. Si ``web.load.control`` o ``api.load.control`` esta establecido por debajo de 100
2. Si el archivo de configuracion se esta leyendo correctamente
3. Si |Fess| fue reiniciado

Solicitudes legitimas son rechazadas
--------------------------------------

**Causa**: Los umbrales son demasiado bajos

**Solucion**:

1. Aumentar los valores de ``web.load.control`` o ``api.load.control``
2. Ajustar ``load.control.monitor.interval`` para cambiar la frecuencia de monitoreo
3. Aumentar los recursos del cluster de OpenSearch

.. warning::
   Establecer umbrales demasiado bajos puede causar que las solicitudes sean rechazadas incluso bajo carga normal.
   Verifique el uso normal de CPU de su cluster de OpenSearch antes de establecer umbrales apropiados.

Informacion de referencia
=========================

- :doc:`rate-limiting` - Configuracion de limite de tasa
