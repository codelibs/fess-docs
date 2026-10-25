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
- Las solicitudes de IPs bloqueadas por superar el límite y de IPs incluidas en la lista de bloqueo devuelven HTTP 403 (Forbidden)
- El cuerpo de la respuesta es JSON (429: ``{"error":"rate_limit_exceeded",...,"retry_after":60}``; 403: ``{"error":"ip_blocked",...}``). La respuesta 429 incluye la cabecera ``Retry-After``
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

Crawl-delay se aplica por origen y tiene un máximo de 60 segundos. Espacia URL, no solicitudes, por
lo que en un rastreo incremental el HEAD y el GET de una URL se envían uno tras otro. El intervalo de
una configuración de rastreo sigue actuando por separado, como espera antes de la siguiente URL.

robots.txt se interpreta según RFC 9309. Entre ``Allow:`` y ``Disallow:`` prevalece la regla
coincidente más larga, y las URL iniciales también se comprueban con robots.txt. Una URL que
robots.txt no permite se registra en INFO en ``fess-crawler.log`` y no se registra como URL fallida.

Espera tras respuestas 429/503
------------------------------

Cuando un servidor responde ``429 Too Many Requests`` o ``503 Service Unavailable``, |Fess| detiene
temporalmente las solicitudes a ese origen y reintenta la URL hasta tres veces. La espera es el valor
de la cabecera ``Retry-After`` si existe; si no, una espera exponencial que empieza en 10 segundos
(hasta 5 minutos). Si el último reintento también falla, se escribe un WARN en ``fess-crawler.log``.

Cuando no se puede obtener robots.txt
-------------------------------------

Cuando la obtención de robots.txt falla con un 5xx, un 429 o un tiempo de espera agotado, las URL de
ese origen vuelven a la cola hasta que termina la espera. Si tras el primer fallo también fallan tres
reintentos, no se rastrea ninguna URL de ese origen durante el resto del rastreo y se escribe un único
WARN en ``fess-crawler.log``. Hasta la versión 15.8, un robots.txt que no se podía obtener significaba
"permitir todo". Para recuperar ese comportamiento, indique lo siguiente en los "Parámetros de
configuración" de la configuración de rastreo web:

::

    client.robotsTxtAllowOnUnavailable=true

Para desactivar por completo el tratamiento de robots.txt, use ``client.robotsTxtEnabled=false``
(por configuración de rastreo) o ``crawler.ignore.robots.txt=true``.

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
     - IPs de proxies confiables (para obtener X-Forwarded-For/X-Real-IP; también se utilizan para la IP del cliente en el registro de auditoría y en el registro de búsqueda)
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

Límite de intentos de inicio de sesión
======================================

El inicio de sesión tiene su propio límite, independiente del anterior y configurado con ``theme.api.login.*``.
Desde 15.10, ``/api/v2/auth/login`` y el formulario de inicio de sesión de la pantalla de inicio de sesión (``/login/``) comparten el mismo límite y el mismo bloqueo.
Cada intento consume una plaza de la cuota por minuto de la IP del cliente (valor predeterminado ``10``), y la plaza se devuelve cuando el inicio de sesión tiene éxito.
Cuando los intentos desde la misma dirección IP superan el límite, esa dirección IP queda bloqueada durante ``theme.api.login.lockout.seconds`` (valor predeterminado ``900``) segundos, y durante ese tiempo no se puede iniciar sesión ni siquiera con credenciales correctas.
Por ello, si desde la misma dirección IP se hacen más intentos que el límite (por ejemplo, inicios de sesión simultáneos) antes de que alguno tenga éxito, esa dirección queda bloqueada.
Consulte :doc:`../api/api-auth` para más detalles.

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
   Si X-Forwarded-For está repartido en varias líneas de encabezado (por ejemplo, cuando un proxy añade
   una línea propia, como hace ``option forwardfor`` de HAProxy), la versión 15.10 y posteriores unen todas
   las líneas en el orden recibido, leen la cadena de derecha a izquierda y usan como IP del cliente la
   primera dirección que no es un proxy confiable. Hasta la versión 15.9 solo se leía la primera línea,
   que es la enviada por el cliente.

Monitoreo y alertas
===================

Configuración para monitorear el estado del límite de tasa:

Salida de logs
--------------

Cuando se aplica el límite de tasa, se registra en el log:

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

El mensaje se registra a nivel INFO, por lo que no se escribe con el nivel de log predeterminado (``warn``). Añada el ``Logger`` anterior a ``log4j2.xml`` (para su ubicación, consulte :doc:`admin-logging`) o establezca ``FESS_LOG_LEVEL`` en ``info``.

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
