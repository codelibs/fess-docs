================================
Configuración de Puerto y Red
================================

Descripción General
===================

Esta sección describe la configuración relacionada con la red en |Fess|.
Abarca configuraciones de conexión de red como cambios de números de puerto, configuración de proxy y configuración de comunicación HTTP.

Configuración de Puertos Utilizados
====================================

Puertos Predeterminados
-----------------------

|Fess| utiliza los siguientes puertos por defecto.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Servicio
     - Número de Puerto
   * - Aplicación Web Fess
     - 8080
   * - OpenSearch (HTTP)
     - 9201
   * - OpenSearch (Transport)
     - 9301

Cambio de Puerto de la Aplicación Web Fess
-------------------------------------------

Configuración en Entorno Linux
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para cambiar el número de puerto en entorno Linux, edite ``bin/fess.in.sh``.

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.port=8080"

Por ejemplo, para usar el puerto 80:

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.port=80"

.. note::
   Para usar números de puerto inferiores a 1024, se requieren privilegios de root o la configuración de permisos apropiada (CAP_NET_BIND_SERVICE).

Configuración mediante Variables de Entorno
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

También puede especificar el número de puerto mediante una variable de entorno.

::

    export FESS_PORT=8080

Para Paquetes RPM/DEB
~~~~~~~~~~~~~~~~~~~~~~

Para paquetes RPM edite ``/etc/sysconfig/fess``, para paquetes DEB edite ``/etc/default/fess``.

::

    FESS_PORT=8080

Configuración en Entorno Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

En entornos Windows, edite ``bin\fess.in.bat``.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=8080

Al Registrar como Servicio de Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Si utiliza el registro como servicio en entorno Windows, cambie también la configuración de puerto en ``bin\service.bat``.
Consulte :doc:`setup-windows-service` para más detalles.

Configuración de Ruta de Contexto
----------------------------------

Si publica |Fess| en un subdirectorio, puede configurar la ruta de contexto.

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.context.path=/search"

Con esta configuración, podrá acceder mediante ``http://localhost:8080/search/``.

.. warning::
   Si cambia la ruta de contexto, también debe configurar apropiadamente las rutas de los archivos estáticos.

Configuración de Proxy
======================

Descripción General
-------------------

Al rastrear sitios externos desde dentro de una intranet o al acceder a APIs externas,
las comunicaciones pueden ser bloqueadas por un firewall.
En tales entornos, es necesario configurar la comunicación a través de un servidor proxy.

Configuración de Proxy para el Rastreador
------------------------------------------

Configuración Básica
~~~~~~~~~~~~~~~~~~~~

En la configuración de rastreo de la pantalla de administración, especifique los parámetros de configuración de la siguiente manera.

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080

Configuración de Proxy con Autenticación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Si el servidor proxy requiere autenticación, agregue lo siguiente.

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080
    client.proxyUsername=proxyuser
    client.proxyPassword=proxypass

Exclusión de Hosts Específicos del Proxy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para conectar sin pasar por el proxy a hosts específicos (como servidores dentro de la intranet):

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080
    client.nonProxyHosts=localhost|*.local|192.168.*

Configuración de Proxy HTTP para Todo el Sistema
-------------------------------------------------

Para usar el proxy HTTP en toda la aplicación |Fess|, configure en ``fess_config.properties``.

::

    http.proxy.host=proxy.example.com
    http.proxy.port=8080
    http.proxy.username=proxyuser
    http.proxy.password=proxypass

.. warning::
   Las contraseñas se almacenan sin cifrar. Configure los permisos de archivo apropiados.

Configuración de Proxy mediante Variables de Entorno
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cuando las bibliotecas Java como la autenticación SSO necesitan usar un proxy, debe configurarlo mediante variables de entorno.
Estas variables de entorno se convierten en propiedades del sistema Java (``http.proxyHost``, ``https.proxyHost``, etc.).

::

    FESS_PROXY_HOST=proxy.example.com
    FESS_PROXY_PORT=8080
    FESS_NON_PROXY_HOSTS=localhost|*.local|192.168.*

Para paquetes RPM, configure en ``/etc/sysconfig/fess``. Para paquetes DEB, configure en ``/etc/default/fess``.

.. note::
   La configuración ``http.proxy.*`` en ``fess_config.properties`` se usa para las comunicaciones HTTP dentro de Fess.
   Si las bibliotecas Java externas como la autenticación SSO necesitan usar un proxy, también configure las variables de entorno anteriores.

Configuración de Comunicación HTTP
===================================

Límites de Carga de Archivos
-----------------------------

Puede limitar el tamaño de carga de archivos desde la pantalla de administración.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Elemento de Configuración
     - Descripción
   * - ``http.fileupload.max.size``
     - Tamaño máximo de carga de archivo (predeterminado: 262144000 bytes = 250MB)
   * - ``http.fileupload.threshold.size``
     - Tamaño umbral para mantener en memoria (predeterminado: 262144 bytes = 256KB)
   * - ``http.fileupload.max.file.count``
     - Número de archivos que se pueden cargar a la vez (predeterminado: 10)

Ejemplo de configuración en ``fess_config.properties``:

::

    http.fileupload.max.size=524288000
    http.fileupload.threshold.size=524288
    http.fileupload.max.file.count=20

Configuración de Tiempo de Espera de Conexión
----------------------------------------------

Puede configurar el tiempo de espera de conexión a OpenSearch.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Elemento de Configuración
     - Descripción
   * - ``search_engine.http.url``
     - URL de OpenSearch (predeterminado: http://localhost:9201)
   * - ``search_engine.heartbeat_interval``
     - Intervalo de verificación de estado (milisegundos, predeterminado: 10000)

Cambio de Destino de Conexión de OpenSearch
--------------------------------------------

Para conectarse a un clúster externo de OpenSearch:

::

    search_engine.http.url=http://opensearch-cluster.example.com:9200

Conexión a Múltiples Nodos
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para conectarse a múltiples nodos de OpenSearch, especifique separados por comas.

::

    search_engine.http.url=http://node1:9200,http://node2:9200,http://node3:9200

Configuración de Conexión SSL/TLS
----------------------------------

Para conectarse a OpenSearch mediante HTTPS:

::

    search_engine.http.url=https://opensearch.example.com:9200
    search_engine.http.ssl.certificate_authorities=/path/to/ca.crt
    search_engine.username=admin
    search_engine.password=admin_password

.. note::
   Para verificar certificados, especifique la ruta al certificado CA en ``certificate_authorities``.

Configuración de Host Virtual
==============================

Descripción General
-------------------

Puede diferenciar los resultados de búsqueda según el nombre de host con el que se accede a |Fess|.
Consulte :doc:`security-virtual-host` para más detalles.

Configuración Básica
--------------------

Configure el encabezado de host virtual en ``fess_config.properties``.

::

    virtual.host.headers=X-Forwarded-Host,Host

Integración con Proxy Inverso
==============================

Ejemplo de Configuración de Nginx
----------------------------------

::

    server {
        listen 80;
        server_name search.example.com;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Host $host;
        }
    }

Ejemplo de Configuración de Apache
-----------------------------------

::

    <VirtualHost *:80>
        ServerName search.example.com

        ProxyPreserveHost On
        ProxyPass / http://localhost:8080/
        ProxyPassReverse / http://localhost:8080/

        RequestHeader set X-Forwarded-Proto "http"
        RequestHeader set X-Forwarded-Host "search.example.com"
    </VirtualHost>

Terminación SSL/TLS
-------------------

Ejemplo de configuración para terminación SSL/TLS en el proxy inverso (Nginx):

::

    server {
        listen 443 ssl http2;
        server_name search.example.com;

        ssl_certificate /path/to/cert.pem;
        ssl_certificate_key /path/to/key.pem;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;
            proxy_set_header X-Forwarded-Host $host;
        }
    }

Configuración de Firewall
==========================

Apertura de Puertos Necesarios
-------------------------------

Para hacer |Fess| accesible desde el exterior, abra los siguientes puertos.

**Ejemplo de configuración de iptables:**

::

    # Aplicación Web Fess
    iptables -A INPUT -p tcp --dport 8080 -j ACCEPT

    # Para acceso HTTPS (vía proxy inverso)
    iptables -A INPUT -p tcp --dport 443 -j ACCEPT

**Ejemplo de configuración de firewalld:**

::

    # Aplicación Web Fess
    firewall-cmd --permanent --add-port=8080/tcp
    firewall-cmd --reload

Configuración de Grupo de Seguridad (Entornos en la Nube)
----------------------------------------------------------

En entornos de nube como AWS, GCP, Azure, abra los puertos apropiados
con grupos de seguridad o ACLs de red.

Configuración recomendada:
- Entrada: Puertos 80/443 (vía proxy inverso HTTP)
- Puerto 8080 restringido solo para acceso interno
- Puertos 9201/9301 de OpenSearch restringidos solo para acceso interno

Solución de Problemas
======================

No se Puede Acceder Después de Cambiar el Puerto
-------------------------------------------------

1. Verifique que haya reiniciado |Fess|.
2. Verifique que el puerto correspondiente esté abierto en el firewall.
3. Verifique errores en el archivo de log (``fess.log``).

No se Puede Rastrear a Través del Proxy
----------------------------------------

1. Verifique que el nombre de host y puerto del servidor proxy sean correctos.
2. Si el servidor proxy requiere autenticación, configure el nombre de usuario y contraseña.
3. Verifique que los intentos de conexión se registren en los logs del servidor proxy.
4. Verifique que la configuración de ``nonProxyHosts`` sea apropiada.

No se Puede Conectar a OpenSearch
----------------------------------

1. Verifique que OpenSearch esté en ejecución.
2. Verifique que la configuración de ``search_engine.http.url`` sea correcta.
3. Verifique la conexión de red: ``curl http://localhost:9201``
4. Verifique errores en los logs de OpenSearch.

No Funciona Correctamente al Acceder Vía Proxy Inverso
-------------------------------------------------------

1. Verifique que el encabezado ``X-Forwarded-Host`` esté configurado correctamente.
2. Verifique que el encabezado ``X-Forwarded-Proto`` esté configurado correctamente.
3. Verifique que la ruta de contexto esté configurada correctamente.
4. Verifique errores en los logs del proxy inverso.

Información de Referencia
==========================

- :doc:`setup-memory` - Configuración de Memoria
- :doc:`setup-windows-service` - Configuración de Servicio de Windows
- :doc:`security-virtual-host` - Configuración de Host Virtual
- :doc:`crawler-advanced` - Configuración Avanzada del Rastreador
- `OpenSearch Configuration <https://opensearch.org/docs/latest/install-and-configure/configuration/>`_
