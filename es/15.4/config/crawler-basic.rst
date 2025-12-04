===============================
Configuración Básica del Rastreador
===============================

Descripción General
===================

El rastreador de |Fess| es una función que recopila automáticamente contenido de sitios web, sistemas de archivos y otros, y lo registra en el índice de búsqueda.
Esta guía describe los conceptos básicos del rastreador y los métodos de configuración.

Conceptos Básicos del Rastreador
=================================

Qué es un Rastreador
--------------------

Un rastreador (Crawler) es un programa que recopila automáticamente contenido siguiendo enlaces, comenzando desde URLs o rutas de archivo especificadas.

El rastreador de |Fess| tiene las siguientes características:

- **Soporte multi-protocolo**: HTTP/HTTPS, sistemas de archivos, SMB, FTP, etc.
- **Ejecución programada**: Rastreo automático periódico
- **Rastreo incremental**: Actualiza solo el contenido modificado
- **Procesamiento paralelo**: Rastreo simultáneo de múltiples URLs
- **Cumplimiento de robots**: Respeta robots.txt

Tipos de Rastreador
-------------------

En |Fess|, existen los siguientes tipos de rastreador según el objetivo.

.. list-table:: Tipos de Rastreador
   :header-rows: 1
   :widths: 20 40 40

   * - Tipo
     - Objetivo
     - Uso
   * - **Rastreador Web**
     - Sitios web (HTTP/HTTPS)
     - Sitios web públicos, sitios web dentro de intranet
   * - **Rastreador de Archivos**
     - Sistema de archivos, SMB, FTP
     - Servidores de archivos, carpetas compartidas
   * - **Rastreador de Almacén de Datos**
     - Bases de datos
     - Fuentes de datos como RDB, CSV, JSON

Creación de Configuración de Rastreo
=====================================

Agregar Configuración Básica de Rastreo
----------------------------------------

1. **Acceder a la Pantalla de Administración**

   Acceda a ``http://localhost:8080/admin`` en su navegador e inicie sesión como administrador.

2. **Abrir Pantalla de Configuración del Rastreador**

   Seleccione "Rastreador" → "Web" o "Sistema de archivos" del menú izquierdo.

3. **Crear Nueva Configuración**

   Haga clic en el botón "Nuevo".

4. **Ingresar Información Básica**

   - **Nombre**: Nombre de identificación de la configuración de rastreo (ej: Wiki Corporativo)
   - **URL**: URL de inicio del rastreo (ej: ``https://wiki.example.com/``)
   - **Intervalo de Rastreo**: Frecuencia de ejecución del rastreo (ej: cada 1 hora)
   - **Número de Hilos**: Número de rastreos paralelos (ej: 5)
   - **Profundidad**: Profundidad de niveles de enlaces a seguir (ej: 3)

5. **Guardar**

   Haga clic en el botón "Crear" para guardar la configuración.

Ejemplos de Configuración del Rastreador Web
---------------------------------------------

Rastreo de Sitio de Intranet Corporativa
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    Nombre: Portal Corporativo
    URL: http://intranet.example.com/
    Intervalo de Rastreo: 1 vez al día
    Número de Hilos: 10
    Profundidad: Ilimitada (-1)
    Máximo Número de Accesos: 10000

Rastreo de Sitio Web Público
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    Nombre: Sitio de Productos
    URL: https://www.example.com/products/
    Intervalo de Rastreo: 1 vez por semana
    Número de Hilos: 5
    Profundidad: 5
    Máximo Número de Accesos: 1000

Ejemplos de Configuración del Rastreador de Archivos
-----------------------------------------------------

Sistema de Archivos Local
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    Nombre: Carpeta de Documentos
    URL: file:///home/share/documents/
    Intervalo de Rastreo: 1 vez al día
    Número de Hilos: 3
    Profundidad: Ilimitada (-1)

SMB/CIFS (Compartición de Archivos Windows)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    Nombre: Servidor de Archivos
    URL: smb://fileserver.example.com/share/
    Intervalo de Rastreo: 1 vez al día
    Número de Hilos: 5
    Profundidad: Ilimitada (-1)

Configuración de Información de Autenticación
----------------------------------------------

Para acceder a sitios o servidores de archivos que requieren autenticación, configure la información de autenticación.

1. Seleccione "Rastreador" → "Autenticación" en la pantalla de administración
2. Haga clic en "Nuevo"
3. Ingrese la información de autenticación:

   ::

       Nombre de Host: wiki.example.com
       Puerto: 443
       Método de Autenticación: Autenticación Basic
       Nombre de Usuario: crawler_user
       Contraseña: ********

4. Haga clic en "Crear"

Ejecución del Rastreo
======================

Ejecución Manual
----------------

Para ejecutar inmediatamente el rastreo configurado:

1. Seleccione la configuración objetivo en la lista de configuraciones de rastreo
2. Haga clic en el botón "Iniciar"
3. Verifique el estado de ejecución del trabajo en el menú "Programador"

Ejecución Programada
--------------------

Para ejecutar el rastreo periódicamente:

1. Abra el menú "Programador"
2. Seleccione el trabajo "Default Crawler"
3. Configure la expresión de programación (formato Cron)

   ::

       # Ejecutar todos los días a las 2 AM
       0 0 2 * * ?

       # Ejecutar cada hora a los 0 minutos
       0 0 * * * ?

       # Ejecutar de lunes a viernes a las 6 PM
       0 0 18 ? * MON-FRI

4. Haga clic en "Actualizar"

Verificación del Estado del Rastreo
------------------------------------

Para verificar el estado del rastreo en ejecución:

1. Abra el menú "Programador"
2. Verifique los trabajos en ejecución
3. Verifique los detalles en los logs:

   ::

       tail -f /var/log/fess/fess_crawler.log

Elementos Básicos de Configuración
===================================

Limitación de Objetivos de Rastreo
-----------------------------------

Limitación por Patrón de URL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Puede incluir solo patrones de URL específicos como objetivos de rastreo, o excluirlos.

**Patrón de URL a Incluir (expresión regular):**

::

    # Rastrear solo bajo /docs/
    https://example\.com/docs/.*

**Patrón de URL a Excluir (expresión regular):**

::

    # Excluir directorios específicos
    .*/admin/.*
    .*/private/.*

    # Excluir extensiones de archivo específicas
    .*\.(jpg|png|gif|css|js)$

Limitación de Profundidad
~~~~~~~~~~~~~~~~~~~~~~~~~~

Limitar la profundidad de niveles de enlaces a seguir:

- **0**: Solo la URL de inicio
- **1**: URL de inicio y páginas enlazadas desde ella
- **-1**: Ilimitada (seguir todos los enlaces)

Máximo Número de Accesos
~~~~~~~~~~~~~~~~~~~~~~~~~

Límite superior del número de páginas a rastrear:

::

    Máximo Número de Accesos: 1000

Detenerse después de rastrear hasta 1000 páginas.

Número de Rastreos Paralelos (Número de Hilos)
-----------------------------------------------

Especifique el número de URLs a rastrear simultáneamente.

.. list-table:: Número de Hilos Recomendado
   :header-rows: 1
   :widths: 40 30 30

   * - Entorno
     - Valor Recomendado
     - Descripción
   * - Sitio Pequeño (〜10,000 páginas)
     - 3〜5
     - Reducir la carga en el servidor objetivo
   * - Sitio Mediano (10,000〜100,000 páginas)
     - 5〜10
     - Configuración equilibrada
   * - Sitio Grande (más de 100,000 páginas)
     - 10〜20
     - Rastreo de alta velocidad requerido
   * - Servidor de Archivos
     - 3〜5
     - Considerar la carga de I/O de archivos

.. warning::
   Aumentar demasiado el número de hilos causará carga excesiva en el servidor objetivo.
   Configure un valor apropiado.

Intervalo de Rastreo
--------------------

Especifique la frecuencia de ejecución del rastreo.

::

    # Especificación de tiempo
    Intervalo de Rastreo: 3600000  # milisegundos (1 hora)

    # O configure en el programador
    0 0 2 * * ?  # Todos los días a las 2 AM

Configuración de Tamaño de Archivo
===================================

Puede configurar el límite superior del tamaño de archivo a rastrear.

Límite Superior del Tamaño de Archivo a Obtener
------------------------------------------------

Agregue lo siguiente a "Parámetros de Configuración" en la configuración del rastreador:

::

    client.maxContentLength=10485760

Obtiene archivos de hasta 10MB. Por defecto no hay límite.

.. note::
   Si rastrea archivos grandes, también ajuste la configuración de memoria.
   Consulte :doc:`setup-memory` para más detalles.

Límite Superior del Tamaño de Archivo a Indexar
------------------------------------------------

Puede configurar el límite superior del tamaño a indexar para cada tipo de archivo.

**Valores predeterminados:**

- Archivos HTML: 2.5MB
- Otros archivos: 10MB

**Archivo de configuración:** ``app/WEB-INF/classes/crawler/contentlength.xml``

::

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
            "http://dbflute.org/meta/lastadi10.dtd">
    <components namespace="fessCrawler">
            <include path="crawler/container.xml" />

            <component name="contentLengthHelper"
                    class="org.codelibs.fess.crawler.helper.ContentLengthHelper" instance="singleton">
                    <property name="defaultMaxLength">10485760</property><!-- 10M -->
                    <postConstruct name="addMaxLength">
                            <arg>"text/html"</arg>
                            <arg>2621440</arg><!-- 2.5M -->
                    </postConstruct>
                    <postConstruct name="addMaxLength">
                            <arg>"application/pdf"</arg>
                            <arg>5242880</arg><!-- 5M -->
                    </postConstruct>
            </component>
    </components>

Se ha agregado una configuración para procesar archivos PDF hasta 5MB.

.. warning::
   Si aumenta el tamaño de archivo a manejar, también aumente la configuración de memoria del rastreador.

Limitación de Longitud de Palabras
===================================

Descripción General
-------------------

Las cadenas largas de solo caracteres alfanuméricos o símbolos continuos causan aumento del tamaño del índice y degradación del rendimiento.
Por lo tanto, |Fess| impone las siguientes limitaciones por defecto:

- **Caracteres alfanuméricos continuos**: hasta 20 caracteres
- **Símbolos continuos**: hasta 10 caracteres

Método de Configuración
------------------------

Edite ``fess_config.properties``.

**Configuración predeterminada:**

::

    crawler.document.max.alphanum.term.size=20
    crawler.document.max.symbol.term.size=10

**Ejemplo: Relajar la limitación**

::

    crawler.document.max.alphanum.term.size=50
    crawler.document.max.symbol.term.size=20

.. note::
   Si necesita buscar cadenas alfanuméricas largas (ej: números de serie, tokens, etc.),
   aumente este valor. Sin embargo, el tamaño del índice aumentará.

Configuración de Proxy
======================

Descripción General
-------------------

Al rastrear sitios externos desde dentro de una intranet, puede ser bloqueado por el firewall.
En ese caso, rastree a través de un servidor proxy.

Método de Configuración
------------------------

Agregue lo siguiente a "Parámetros de Configuración" en la configuración de rastreo de la pantalla de administración.

**Configuración básica de proxy:**

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080

**Proxy con autenticación:**

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080
    client.proxyUsername=proxyuser
    client.proxyPassword=proxypass

**Excluir hosts específicos del proxy:**

::

    client.nonProxyHosts=localhost|127.0.0.1|*.example.com

Configuración de Proxy para Todo el Sistema
--------------------------------------------

Si usa el mismo proxy para todas las configuraciones de rastreo, puede configurar mediante variables de entorno.

::

    export http_proxy=http://proxy.example.com:8080
    export https_proxy=http://proxy.example.com:8080
    export no_proxy=localhost,127.0.0.1,.example.com

Configuración de robots.txt
============================

Descripción General
-------------------

robots.txt es un archivo que instruye a los rastreadores sobre si permitir o no el rastreo.
|Fess| respeta robots.txt por defecto.

Método de Configuración
------------------------

Para ignorar robots.txt, edite ``fess_config.properties``.

::

    crawler.ignore.robots.txt=true

.. warning::
   Al rastrear sitios externos, respete robots.txt.
   Ignorarlo puede causar carga excesiva en el servidor o violar términos de uso.

Configuración de User-Agent
============================

Puede cambiar el User-Agent del rastreador.

Configuración en la Pantalla de Administración
-----------------------------------------------

Agregue a "Parámetros de Configuración" en la configuración de rastreo:

::

    client.userAgent=MyCompanyCrawler/1.0

Configuración para Todo el Sistema
-----------------------------------

Configure en ``fess_config.properties``:

::

    crawler.user.agent=MyCompanyCrawler/1.0

Configuración de Codificación
==============================

Codificación de Datos de Rastreo
---------------------------------

Configure en ``fess_config.properties``:

::

    crawler.crawling.data.encoding=UTF-8

Codificación de Nombres de Archivo
-----------------------------------

Codificación de nombres de archivo del sistema de archivos:

::

    crawler.document.file.name.encoding=UTF-8

Solución de Problemas de Rastreo
=================================

El Rastreo No Inicia
--------------------

**Elementos a verificar:**

1. Verificar si el programador está habilitado

   - Verificar si el trabajo "Default Crawler" está habilitado en el menú "Programador"

2. Verificar si la configuración de rastreo está habilitada

   - Verificar si la configuración objetivo está habilitada en la lista de configuraciones de rastreo

3. Verificar logs

   ::

       tail -f /var/log/fess/fess.log
       tail -f /var/log/fess/fess_crawler.log

El Rastreo se Detiene a Mitad
------------------------------

**Causas posibles:**

1. **Falta de memoria**

   - Verificar si hay ``OutOfMemoryError`` en ``fess_crawler.log``
   - Aumentar la memoria del rastreador (ver :doc:`setup-memory`)

2. **Error de red**

   - Ajustar configuración de timeout
   - Verificar configuración de reintento

3. **Error en objetivo de rastreo**

   - Verificar si hay muchos errores 404
   - Verificar detalles de error en logs

Páginas Específicas No se Rastrean
-----------------------------------

**Elementos a verificar:**

1. **Verificar patrón de URL**

   - Verificar si corresponde al patrón de URL excluido

2. **Verificar robots.txt**

   - Verificar ``/robots.txt`` del sitio objetivo

3. **Verificar autenticación**

   - Si es una página que requiere autenticación, verificar configuración de autenticación

4. **Limitación de profundidad**

   - Verificar si la jerarquía de enlaces excede la limitación de profundidad

5. **Máximo número de accesos**

   - Verificar si se ha alcanzado el máximo número de accesos

El Rastreo es Lento
-------------------

**Contramedidas:**

1. **Aumentar número de hilos**

   - Aumentar número de rastreos paralelos (pero tenga cuidado con la carga del servidor objetivo)

2. **Excluir URLs innecesarias**

   - Agregar imágenes y archivos CSS al patrón de URL excluido

3. **Ajustar configuración de timeout**

   - Para sitios con respuesta lenta, acortar el timeout

4. **Aumentar memoria del rastreador**

   - Ver :doc:`setup-memory`

Mejores Prácticas
==================

Recomendaciones para Configuración de Rastreo
----------------------------------------------

1. **Configurar número apropiado de hilos**

   Configure un número apropiado de hilos para no causar carga excesiva en el servidor objetivo.

2. **Optimización de patrones de URL**

   Al excluir archivos innecesarios (imágenes, CSS, JavaScript, etc.),
   reduce el tiempo de rastreo y mejora la calidad del índice.

3. **Configuración de limitación de profundidad**

   Configure una profundidad apropiada según la estructura del sitio.
   Use ilimitada (-1) solo al rastrear todo el sitio.

4. **Configuración de máximo número de accesos**

   Configure un límite superior para no rastrear inesperadamente una gran cantidad de páginas.

5. **Ajuste del intervalo de rastreo**

   Configure un intervalo apropiado según la frecuencia de actualización.
   - Sitios actualizados frecuentemente: cada 1 hora〜varias horas
   - Sitios que no se actualizan mucho: cada 1 día〜1 semana

Recomendaciones para Configuración de Programación
---------------------------------------------------

1. **Ejecución nocturna**

   Ejecute en horas de baja carga del servidor (ej: 2 AM).

2. **Evitar ejecución duplicada**

   Configure para iniciar el siguiente rastreo después de que se complete el rastreo anterior.

3. **Notificación en caso de error**

   Configure notificación por correo electrónico en caso de falla del rastreo.

Información de Referencia
==========================

- :doc:`crawler-advanced` - Configuración Avanzada del Rastreador
- :doc:`crawler-thumbnail` - Configuración de Miniaturas
- :doc:`setup-memory` - Configuración de Memoria
- :doc:`admin-logging` - Configuración de Logs
