==================================
Configuracion de limite de tasa
==================================

Descripcion general
===================

|Fess| tiene una funcionalidad de limite de tasa para mantener la estabilidad y el rendimiento del sistema.
Esta funcionalidad protege el sistema de solicitudes excesivas y permite una distribucion justa de recursos.

El limite de tasa se aplica en los siguientes escenarios:

- Todas las solicitudes HTTP, incluyendo API de busqueda, API de modo IA y pantallas de administracion (``RateLimitFilter``)
- Solicitudes del crawler (controladas por la configuracion de crawl)

Limitacion de tasa de solicitudes HTTP
=======================================

Puede limitar el numero de solicitudes HTTP a |Fess| por direccion IP.
Esta limitacion se aplica a todas las solicitudes HTTP, incluyendo la API de busqueda, la API de modo IA, las pantallas de administracion, etc.

Configuracion
-------------

``app/WEB-INF/conf/fess_config.properties``:

::

    # Habilitar limite de tasa (predeterminado: false)
    rate.limit.enabled=true

    # Numero maximo de solicitudes por ventana (predeterminado: 100)
    rate.limit.requests.per.window=100

    # Tamano de ventana (milisegundos) (predeterminado: 60000)
    rate.limit.window.ms=60000

Comportamiento
--------------

- Las solicitudes que excedan el limite de tasa devuelven HTTP 429 (Too Many Requests)
- Las solicitudes de IPs incluidas en la lista de bloqueo devuelven HTTP 403 (Forbidden)
- El limite se aplica por direccion IP
- La ventana se inicia con la primera solicitud de cada IP y el contador se reinicia despues de que expire el periodo de ventana (metodo de ventana fija)
- Cuando se excede el limite, la IP se bloquea durante el periodo definido en ``rate.limit.block.duration.ms``

Limite de tasa del modo IA
==========================

La funcionalidad de modo IA tiene un limite de tasa para controlar los costos y el consumo de recursos de la API de LLM.
El modo IA tiene la limitacion de tasa de solicitudes HTTP descrita anteriormente, ademas de configuraciones de limite de tasa especificas del modo IA.

Para la configuracion especifica del limite de tasa del modo IA, consulte :doc:`rag-chat`.

.. note::
   El limite de tasa del modo IA se aplica por separado del limite de tasa del proveedor LLM.
   Considere ambos limites al configurar.

Limite de tasa del crawler
==========================

Puede configurar el intervalo entre solicitudes para evitar que el crawler sobrecargue los sitios objetivo.

Configuracion de crawl web
--------------------------

Configure lo siguiente en "Crawler" -> "Web" en la pantalla de administracion:

- **Intervalo de solicitudes**: Tiempo de espera entre solicitudes (milisegundos)
- **Numero de hilos**: Numero de hilos de crawl paralelos

Configuracion recomendada:

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

Todas las opciones de configuracion de limite de tasa
=====================================================

Todas las propiedades configurables en ``app/WEB-INF/conf/fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Predeterminado
   * - ``rate.limit.enabled``
     - Habilitar limite de tasa
     - ``false``
   * - ``rate.limit.requests.per.window``
     - Numero maximo de solicitudes por ventana
     - ``100``
   * - ``rate.limit.window.ms``
     - Tamano de ventana (milisegundos)
     - ``60000``
   * - ``rate.limit.block.duration.ms``
     - Periodo de bloqueo de IP cuando se excede el limite (milisegundos)
     - ``300000``
   * - ``rate.limit.retry.after.seconds``
     - Valor del encabezado Retry-After (segundos)
     - ``60``
   * - ``rate.limit.whitelist.ips``
     - Direcciones IP excluidas del limite de tasa (separadas por comas)
     - ``127.0.0.1,::1``
   * - ``rate.limit.blocked.ips``
     - Direcciones IP a bloquear (separadas por comas)
     - (vacio)
   * - ``rate.limit.trusted.proxies``
     - IPs de proxies confiables (para obtener X-Forwarded-For/X-Real-IP)
     - ``127.0.0.1,::1``
   * - ``rate.limit.cleanup.interval``
     - Intervalo de limpieza para prevenir fugas de memoria (numero de solicitudes)
     - ``1000``

Configuracion avanzada de limite de tasa
========================================

Limite de tasa personalizado
----------------------------

Para aplicar una logica de limite de tasa diferente basada en condiciones especificas,
se requiere una implementacion de componente personalizado.

::

    // Ejemplo de personalizacion de RateLimitHelper
    public class CustomRateLimitHelper extends RateLimitHelper {
        @Override
        public boolean allowRequest(String ip) {
            // Logica personalizada
        }
    }

Configuracion de exclusion
==========================

Puede excluir direcciones IP especificas del limite de tasa o bloquearlas.

::

    # IPs en lista blanca (excluidas del limite de tasa, separadas por comas)
    rate.limit.whitelist.ips=127.0.0.1,::1,192.168.1.100

    # IPs bloqueadas (siempre bloqueadas, separadas por comas)
    rate.limit.blocked.ips=203.0.113.50

    # IPs de proxies confiables (separadas por comas)
    rate.limit.trusted.proxies=127.0.0.1,::1

.. note::
   Si esta usando un proxy inverso, configure la direccion IP del proxy en ``rate.limit.trusted.proxies``.
   Solo se obtendrá la IP del cliente de los encabezados X-Forwarded-For y X-Real-IP
   cuando la solicitud provenga de un proxy confiable.

Monitoreo y alertas
===================

Configuracion para monitorear el estado del limite de tasa:

Salida de logs
--------------

Cuando se aplica el limite de tasa, se registra en el log:

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

Solucion de problemas
=====================

Solicitudes legitimas son bloqueadas
------------------------------------

**Causa**: Valor de limite demasiado estricto

**Solucion**:

1. Aumentar ``rate.limit.requests.per.window``
2. Agregar IPs especificas a la lista blanca (``rate.limit.whitelist.ips``)
3. Ajustar el tamano de la ventana (``rate.limit.window.ms``)

Limite de tasa no funciona
--------------------------

**Causa**: Configuracion no reflejada correctamente

**Verificaciones**:

1. Si ``rate.limit.enabled=true`` esta configurado
2. Si el archivo de configuracion se esta leyendo correctamente
3. Si |Fess| fue reiniciado

Impacto en el rendimiento
-------------------------

Si la verificacion del limite de tasa afecta el rendimiento:

1. Utilizar la lista blanca para omitir la verificacion de IPs confiables
2. Deshabilitar el limite de tasa (``rate.limit.enabled=false``)

Informacion de referencia
=========================

- :doc:`rag-chat` - Configuracion de la funcionalidad de modo IA
- :doc:`../admin/webconfig-guide` - Guia de configuracion de crawl web
- :doc:`../api/api-overview` - Descripcion general de API
