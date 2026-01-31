==================================
Configuracion de limite de tasa
==================================

Descripcion general
===================

|Fess| tiene una funcionalidad de limite de tasa para mantener la estabilidad y el rendimiento del sistema.
Esta funcionalidad protege el sistema de solicitudes excesivas y permite una distribucion justa de recursos.

El limite de tasa se aplica en los siguientes escenarios:

- API de busqueda
- API de modo IA
- Solicitudes del crawler

Limite de tasa de la API de busqueda
====================================

Puede limitar el numero de solicitudes a la API de busqueda.

Configuracion
-------------

``app/WEB-INF/conf/system.properties``:

::

    # Habilitar limite de tasa
    api.rate.limit.enabled=true

    # Numero maximo de solicitudes por minuto por direccion IP
    api.rate.limit.requests.per.minute=60

    # Tamano de ventana del limite de tasa (segundos)
    api.rate.limit.window.seconds=60

Comportamiento
--------------

- Las solicitudes que excedan el limite de tasa devuelven HTTP 429 (Too Many Requests)
- El limite se aplica por direccion IP
- Los valores de limite se cuentan usando el metodo de ventana deslizante

Limite de tasa del modo IA
==========================

La funcionalidad de modo IA tiene un limite de tasa para controlar los costos y el consumo de recursos de la API de LLM.

Configuracion
-------------

``app/WEB-INF/conf/system.properties``:

::

    # Habilitar limite de tasa para chat
    rag.chat.rate.limit.enabled=true

    # Numero maximo de solicitudes por minuto
    rag.chat.rate.limit.requests.per.minute=10

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

Configuracion avanzada de limite de tasa
========================================

Limite de tasa personalizado
----------------------------

Para aplicar limites diferentes a usuarios o roles especificos,
se requiere una implementacion de componente personalizado.

::

    // Ejemplo de personalizacion de RateLimitHelper
    public class CustomRateLimitHelper extends RateLimitHelper {
        @Override
        public boolean isAllowed(String key) {
            // Logica personalizada
        }
    }

Limite de rafaga
----------------

Configuracion que permite rafagas breves de solicitudes mientras previene alta carga continua:

::

    # Cantidad de rafaga permitida
    api.rate.limit.burst.size=20

    # Limite sostenido
    api.rate.limit.sustained.requests.per.second=1

Configuracion de exclusion
==========================

Puede excluir direcciones IP o usuarios especificos del limite de tasa.

::

    # Direcciones IP excluidas (separadas por comas)
    api.rate.limit.excluded.ips=192.168.1.100,10.0.0.0/8

    # Roles excluidos
    api.rate.limit.excluded.roles=admin

Monitoreo y alertas
===================

Configuracion para monitorear el estado del limite de tasa:

Salida de logs
--------------

Cuando se aplica el limite de tasa, se registra en el log:

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

Metricas
--------

Las metricas relacionadas con el limite de tasa se pueden obtener a traves de la API de estadisticas del sistema:

::

    GET /api/admin/stats

Solucion de problemas
=====================

Solicitudes legitimas son bloqueadas
------------------------------------

**Causa**: Valor de limite demasiado estricto

**Solucion**:

1. Aumentar ``requests.per.minute``
2. Agregar IPs especificas a la lista de exclusion
3. Ajustar el tamano de la ventana

Limite de tasa no funciona
--------------------------

**Causa**: Configuracion no reflejada correctamente

**Verificaciones**:

1. Si ``api.rate.limit.enabled=true`` esta configurado
2. Si el archivo de configuracion se esta leyendo correctamente
3. Si |Fess| fue reiniciado

Impacto en el rendimiento
-------------------------

Si la verificacion del limite de tasa afecta el rendimiento:

1. Cambiar el almacenamiento del limite de tasa a Redis u otro
2. Ajustar la frecuencia de verificacion

Informacion de referencia
=========================

- :doc:`rag-chat` - Configuracion de la funcionalidad de modo IA
- :doc:`../admin/webconfig-guide` - Guia de configuracion de crawl web
- :doc:`../api/api-overview` - Descripcion general de API
