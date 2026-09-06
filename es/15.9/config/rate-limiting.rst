==================================
Configuración de límite de tasa
==================================

Descripción general
===================

|Fess| tiene una funcionalidad de límite de tasa para mantener la estabilidad y el rendimiento del sistema.
Esta funcionalidad protege el sistema de solicitudes excesivas y permite una distribución justa de recursos.

El límite de tasa se aplica en los siguientes escenarios:

- Todas las solicitudes HTTP, incluyendo API de búsqueda, API de modo de búsqueda IA y pantallas de administración (``RateLimitFilter``)
- Solicitudes del crawler (controladas por la configuración de crawl)

Limitación de tasa de solicitudes HTTP
=======================================

Puede limitar el número de solicitudes HTTP a |Fess| por dirección IP.
Esta limitación se aplica a todas las solicitudes HTTP, incluyendo la API de búsqueda, la API de modo de búsqueda IA, las pantallas de administración, etc.

Configuración
-------------

``app/WEB-INF/classes/fess_config.properties``:

::

    # Habilitar limite de tasa (predeterminado: false)
    rate.limit.enabled=true

    # Numero maximo de solicitudes por ventana (predeterminado: 100)
    rate.limit.requests.per.window=100

    # Tamano de ventana (milisegundos) (predeterminado: 60000)
    rate.limit.window.ms=60000

Comportamiento
--------------

- Las solicitudes que excedan el límite de tasa devuelven HTTP 429 (Too Many Requests)
- Las solicitudes de IPs incluidas en la lista de bloqueo devuelven HTTP 403 (Forbidden)
- El límite se aplica por dirección IP
- La ventana se inicia con la primera solicitud de cada IP y el contador se reinicia después de que expire el período de ventana (método de ventana fija)
- Cuando se excede el límite, la IP se bloquea durante el período definido en ``rate.limit.block.duration.ms``

Límite de tasa del modo de búsqueda IA
==========================

La funcionalidad de modo de búsqueda IA tiene un límite de tasa para controlar los costos y el consumo de recursos de la API de LLM.
El modo de búsqueda IA tiene la limitación de tasa de solicitudes HTTP descrita anteriormente, además de configuraciones de límite de tasa específicas del modo de búsqueda IA.

Para la configuración específica del límite de tasa del modo de búsqueda IA, consulte :doc:`rag-chat`.

.. note::
   El límite de tasa del modo de búsqueda IA se aplica por separado del límite de tasa del proveedor LLM.
   Considere ambos límites al configurar.

Límite de tasa del crawler
==========================

Puede configurar el intervalo entre solicitudes para evitar que el crawler sobrecargue los sitios objetivo.

Configuración de crawl web
--------------------------

Configure lo siguiente en "Crawler" -> "Web" en la pantalla de administración:

- **Intervalo de solicitudes**: Tiempo de espera entre solicitudes (milisegundos)
- **Número de hilos**: Número de hilos de crawl paralelos

Configuración recomendada:

::

    # Sitios generales
    intervalTime=1000
    numOfThread=1

    # Sitios grandes (cuando se tiene permiso)
    intervalTime=500
    numOfThread=3

Respeto de robots.txt
---------------------

|Fess| respeta por defecto la directiva Crawl-delay de robots.txt.

::

    # Ejemplo de robots.txt
    User-agent: *
    Crawl-delay: 10

El manejo de robots.txt se controla mediante ``crawler.ignore.robots.txt`` en
``app/WEB-INF/classes/fess_config.properties`` (predeterminado: ``false``).
Al establecerlo en ``true``, se deshabilita el manejo de robots.txt, incluyendo Crawl-delay.

::

    # Ignorar robots.txt (predeterminado: false)
    crawler.ignore.robots.txt=false

Todas las opciones de configuración de límite de tasa
=====================================================

Todas las propiedades configurables en ``app/WEB-INF/classes/fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Predeterminado
   * - ``rate.limit.enabled``
     - Habilitar límite de tasa
     - ``false``
   * - ``rate.limit.requests.per.window``
     - Número máximo de solicitudes por ventana
     - ``100``
   * - ``rate.limit.window.ms``
     - Tamaño de ventana (milisegundos)
     - ``60000``
   * - ``rate.limit.block.duration.ms``
     - Período de bloqueo de IP cuando se excede el límite (milisegundos)
     - ``300000``
   * - ``rate.limit.retry.after.seconds``
     - Valor del encabezado Retry-After (segundos)
     - ``60``
   * - ``rate.limit.whitelist.ips``
     - Direcciones IP excluidas del límite de tasa (separadas por comas)
     - ``127.0.0.1,::1``
   * - ``rate.limit.blocked.ips``
     - Direcciones IP a bloquear (separadas por comas)
     - (vacío)
   * - ``rate.limit.trusted.proxies``
     - IPs de proxies confiables (para obtener X-Forwarded-For/X-Real-IP)
     - ``127.0.0.1,::1``
   * - ``rate.limit.cleanup.interval``
     - Intervalo de limpieza (número de solicitudes, reservado)
     - ``1000``

.. note::
   ``rate.limit.cleanup.interval`` es una configuración reservada para uso futuro.
   En la implementación actual, los contadores de solicitudes y la información de IPs bloqueadas
   se limpian automáticamente en función de la expiración de la caché interna
   (``rate.limit.window.ms`` y ``rate.limit.block.duration.ms``),
   por lo que este valor no se utiliza.

Configuración avanzada de límite de tasa
========================================

Límite de tasa personalizado
----------------------------

Para aplicar una lógica de límite de tasa diferente basada en condiciones específicas,
se requiere una implementación de componente personalizado.

::

    // Ejemplo de personalizacion de RateLimitHelper
    public class CustomRateLimitHelper extends RateLimitHelper {
        @Override
        public boolean allowRequest(String ip) {
            // Logica personalizada
        }
    }

Configuración de exclusión
==========================

Puede excluir direcciones IP específicas del límite de tasa o bloquearlas.

::

    # IPs en lista blanca (excluidas del limite de tasa, separadas por comas)
    rate.limit.whitelist.ips=127.0.0.1,::1,192.168.1.100

    # IPs bloqueadas (siempre bloqueadas, separadas por comas)
    rate.limit.blocked.ips=203.0.113.50

    # IPs de proxies confiables (separadas por comas)
    rate.limit.trusted.proxies=127.0.0.1,::1

.. note::
   Si está usando un proxy inverso, configure la dirección IP del proxy en ``rate.limit.trusted.proxies``.
   Solo se obtendrá la IP del cliente de los encabezados X-Forwarded-For y X-Real-IP
   cuando la solicitud provenga de un proxy confiable.

Monitoreo y alertas
===================

Configuración para monitorear el estado del límite de tasa:

Salida de logs
--------------

Cuando se aplica el límite de tasa, se registra en el log:

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

Solución de problemas
=====================

Solicitudes legítimas son bloqueadas
------------------------------------

**Causa**: Valor de límite demasiado estricto

**Solución**:

1. Aumentar ``rate.limit.requests.per.window``
2. Agregar IPs específicas a la lista blanca (``rate.limit.whitelist.ips``)
3. Ajustar el tamaño de la ventana (``rate.limit.window.ms``)

Límite de tasa no funciona
--------------------------

**Causa**: Configuración no reflejada correctamente

**Verificaciones**:

1. Si ``rate.limit.enabled=true`` está configurado
2. Si el archivo de configuración se está leyendo correctamente
3. Si |Fess| fue reiniciado

Impacto en el rendimiento
-------------------------

Si la verificación del límite de tasa afecta el rendimiento:

1. Utilizar la lista blanca para omitir la verificación de IPs confiables
2. Deshabilitar el límite de tasa (``rate.limit.enabled=false``)

Información de referencia
=========================

- :doc:`rag-chat` - Configuración de la funcionalidad de modo de búsqueda IA
- :doc:`../admin/webconfig-guide` - Guía de configuración de crawl web
- :doc:`../api/api-overview` - Descripción general de API
