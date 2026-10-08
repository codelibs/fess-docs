=========================
Tipo de motor de búsqueda
=========================

Descripción general
===================

|Fess| guarda sus datos en OpenSearch. El parámetro ``search_engine.type`` indica a |Fess| con qué tipo de OpenSearch está conectado. De ello dependen las definiciones de índice que |Fess| crea y las funciones que ofrece.

Con el valor predeterminado, ``default``, |Fess| espera un OpenSearch que tenga instalados los cuatro plugins de CodeLibs (``opensearch-analysis-fess``, ``opensearch-analysis-extension``, ``opensearch-minhash`` y ``opensearch-configsync``; consulte :doc:`../install/install`). Para conectarse a un OpenSearch puro sin estos plugins, por ejemplo un servicio gestionado en el que no puede instalar plugins propios, establezca el valor ``vanilla``.

Tipos
=====

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Valor
     - Descripción
   * - ``default``
     - OpenSearch con los plugins de CodeLibs. Es el valor predeterminado.
   * - ``vanilla``
     - Un OpenSearch puro sin los plugins de CodeLibs. Novedad de la versión 15.9. Las definiciones de índice se leen de ``fess_indices/_vanilla/``. |Fess| 15.8 y anteriores no reconocen este valor; con ellas utilice ``cloud``.
   * - ``aws``
     - Igual que ``vanilla``, pensado para Amazon OpenSearch Service. Consulte :ref:`search-engine-type-aws`.
   * - ``cloud``
     - Un alias obsoleto de ``vanilla``. |Fess| registra una advertencia al iniciarse. Cámbielo a ``vanilla``.
   * - Cualquier otro valor
     - Se trata como ``default``, con la diferencia de que los archivos de definición de ``fess_indices/_<tipo>/`` tienen prioridad sobre los archivos del mismo nombre de ``fess_indices/``.

|Fess| no detecta los plugins automáticamente; usted establece el tipo. Establézcalo antes del primer inicio. Las definiciones de índice se aplican al crear un índice, por lo que cambiar el valor más adelante no modifica los índices que ya existen.

Funciones no disponibles sin los plugins
========================================

Con ``vanilla`` y ``aws`` (incluido el obsoleto ``cloud``) no están disponibles las siguientes funciones. Los elementos de la pantalla de administración que dependen de ellas se ocultan.

* **Gestión de diccionarios**: [Sistema > Diccionario] se oculta. Las páginas de diccionarios y la API de administración de diccionarios (``/api/admin/dict/``) no se pueden utilizar. También se ocultan «Restablecer diccionarios» y «Recargar índice de documentos» de la página Mantenimiento. Los analizadores utilizan las reglas incluidas en la definición del índice, no archivos de diccionario.
* **Contracción de resultados**: «Contraer resultados duplicados» de General se oculta y la contracción está siempre desactivada.
* **Detección de duplicados**: no se calcula la firma de contenido que sirve para encontrar documentos con el mismo contenido. La pestaña «Duplicados» del Informe de documentos se oculta (el informe de documentos inactivos sigue disponible) y el parámetro de búsqueda ``sdh`` (documentos similares) se ignora.
* **Analizadores**: el japonés, el coreano y el chino simplificado se segmentan con los analizadores Kuromoji, Nori y SmartCN de OpenSearch en lugar de con los tokenizadores de CodeLibs, por lo que los tokens difieren de los de ``default``. El vietnamita (campos ``*_vi``) y el chino tradicional (campos ``*_zh-tw``) usan un analizador vacío que no registra ningún término. Los documentos en estos idiomas siguen indexándose en los campos independientes del idioma ``content`` y ``title``.

Plugins de OpenSearch necesarios
================================

Las definiciones de índice de ``vanilla`` y ``aws`` utilizan analizadores y un tipo de campo vectorial que proporcionan plugins oficiales de OpenSearch. El OpenSearch al que se conecte debe tener estos plugins:

* ``analysis-kuromoji``
* ``analysis-nori``
* ``analysis-smartcn``
* ``opensearch-knn`` (k-NN)

Los plugins de CodeLibs no son necesarios. En un OpenSearch que usted mismo administra, instale un plugin con ``opensearch-plugin install``, por ejemplo ``bin/opensearch-plugin install analysis-nori``. Para Amazon OpenSearch Service, consulte :ref:`search-engine-type-aws`.

Cuando el tipo es ``vanilla`` o ``aws``, |Fess| enumera los plugins instalados (``GET /_cat/plugins``) al iniciarse. Si falta alguno de los plugins anteriores, registra una advertencia que nombra los plugins que faltan y continúa con el inicio. Si la solicitud falla, por ejemplo porque el servicio no la permite, se omite la comprobación.

Cómo establecer el tipo
=======================

Docker
------

Establezca la variable de entorno ``SEARCH_ENGINE_TYPE`` en el servicio ``fess01`` de ``compose.yaml``::

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "SEARCH_ENGINE_TYPE=vanilla"

``vanilla`` se puede usar con imágenes de |Fess| 15.9 o posteriores. Con una imagen anterior, establezca ``SEARCH_ENGINE_TYPE=cloud``. Para el resto de la configuración de Docker, consulte :doc:`../install/install-docker`.

Instalaciones sin Docker
------------------------

``bin/fess.in.sh`` no lee ``SEARCH_ENGINE_TYPE``. Utilice en su lugar una de las siguientes opciones.

* Escriba ``search_engine.type`` en ``fess_config.properties`` (``app/WEB-INF/classes/fess_config.properties`` en la edición ZIP, ``/etc/fess/fess_config.properties`` en las ediciones RPM y DEB).
* Añada una opción de JVM a ``FESS_JAVA_OPTS`` en ``bin/fess.in.sh`` de la edición ZIP (``bin\fess.in.bat`` en Windows).

::

    # fess_config.properties
    search_engine.type=vanilla

    # bin/fess.in.sh
    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.config.search_engine.type=vanilla"

    REM bin\fess.in.bat
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.config.search_engine.type=vanilla

Reinicie |Fess| después del cambio. El rastreador y los demás procesos de trabajos reciben el ajuste de |Fess|, por lo que no hace falta establecerlo por separado para ellos.

Configuración de la conexión
============================

La conexión con OpenSearch se configura igual que con cualquier otro tipo.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Parámetro
     - Descripción
   * - ``search_engine.http.url``
     - El punto de conexión HTTP de OpenSearch. Si está definida la variable de entorno ``SEARCH_ENGINE_HTTP_URL``, tiene prioridad.
   * - ``search_engine.username`` / ``search_engine.password``
     - El nombre de usuario y la contraseña para la autenticación HTTP Basic. Solo se utilizan si se establecen ambos. En Docker, utilice las variables de entorno ``SEARCH_ENGINE_USERNAME`` y ``SEARCH_ENGINE_PASSWORD``.
   * - ``search_engine.http.ssl.certificate_authorities``
     - La ruta de un archivo de certificado de CA (X.509) que se utiliza para verificar el certificado del servidor de un punto de conexión HTTPS. No hace falta si el certificado lo emitió una CA en la que Java ya confía.

Un elemento de ``fess_config.properties`` también se puede indicar como ``-Dfess.config.<nombre del elemento>`` en ``FESS_JAVA_OPTS`` (consulte :doc:`../install/install-docker`).

.. _search-engine-type-aws:

Amazon OpenSearch Service
=========================

Para usar un dominio de Amazon OpenSearch Service, establezca ``search_engine.type`` en ``aws`` (``vanilla`` se comporta igual).

Requisitos
----------

* El dominio ejecuta OpenSearch 3.x. |Fess| comprueba el motor al iniciarse y no arranca con nada que no sea OpenSearch 3.
* Los plugins indicados en «Plugins de OpenSearch necesarios» están disponibles en el dominio. En Amazon OpenSearch Service, Nori es un paquete opcional: asócielo al dominio antes de iniciar |Fess|.
* El punto de conexión utiliza HTTPS.
* El control de acceso detallado (fine-grained access control) está habilitado y dispone de un usuario interno con el que |Fess| inicia sesión (autenticación HTTP Basic). Todavía no se admite firmar las solicitudes con credenciales de AWS IAM (SigV4), por lo que no se puede usar un dominio que solo acepte solicitudes firmadas con IAM.

Ejemplo de configuración
------------------------

::

    search_engine.type=aws
    search_engine.http.url=https://<domain-endpoint>:443
    search_engine.username=<internal-user-name>
    search_engine.password=<password>

Comprobaciones al iniciar
-------------------------

* La comprobación de plugins descrita en «Plugins de OpenSearch necesarios» también se ejecuta con ``aws``. Si olvidó asociar Nori, aparece una advertencia en ``fess.log``.
* Si el dominio rechaza una solicitud con HTTP 401 o 403, |Fess| registra una advertencia. Cuando esto provoca que el inicio falle, el mensaje de error remite al nombre de usuario, la contraseña y la política de acceso del dominio.

TTL de la caché DNS
-------------------

El punto de conexión de un servicio gestionado puede resolverse a direcciones IP distintas con el tiempo, y la JVM guarda en caché el resultado de una consulta DNS. Un tiempo de caché corto permite que |Fess| siga ese cambio. Establezca ``-Dsun.net.inetaddr.ttl=5`` (segundos) en los dos lugares siguientes.

1. El proceso de |Fess|: añádalo a ``FESS_JAVA_OPTS``.

   ::

       FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dsun.net.inetaddr.ttl=5"

2. Los procesos de trabajos: los procesos del rastreador, de sugerencias, de chunk y de miniaturas los inicia |Fess| como JVM independientes y no heredan ``FESS_JAVA_OPTS``. Añada la misma opción al final de ``jvm.crawler.options``, ``jvm.suggest.options``, ``jvm.chunk.options`` y ``jvm.thumbnail.options`` en ``fess_config.properties``. Cada uno de estos valores tiene una opción por línea, y cada línea termina en ``\n\``.

   ::

       jvm.crawler.options=\
       -Djava.awt.headless=true\n\
       ...
       -Dsun.net.inetaddr.ttl=5\n\

   Añada la línea después de las existentes y haga lo mismo con los otros tres elementos.

En Docker, indique ``FESS_JAVA_OPTS`` en las variables de entorno del archivo Compose. Para cambiar los elementos ``jvm.*.options``, monte un ``fess_config.properties`` modificado (consulte :doc:`../install/install-docker`).
