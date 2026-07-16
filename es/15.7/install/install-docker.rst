==================================
Instalación con Docker (Detalles)
==================================

Esta página describe los procedimientos de instalación de |Fess| utilizando Docker y Docker Compose.
Usar Docker permite construir un entorno |Fess| de manera fácil y rápida.

Requisitos Previos
===================

- Cumplir con los requisitos del sistema descritos en :doc:`prerequisites`
- Docker 20.10 o posterior instalado
- Docker Compose 2.0 o posterior instalado

Verificación de la Instalación de Docker
=========================================

Verifique las versiones de Docker y Docker Compose con los siguientes comandos.

::

    $ docker --version
    $ docker compose version

.. note::

   Si está usando una versión antigua de Docker Compose, use el comando ``docker-compose``.
   Este documento utiliza el nuevo formato de comando ``docker compose``.

Acerca de las Imágenes Docker
==============================

Al iniciar |Fess| con Docker Compose, se ejecutan los siguientes dos contenedores:

- **Fess** (``fess01``): El sistema de búsqueda de texto completo en sí
- **OpenSearch** (``search01``): El motor de búsqueda

La imagen Docker oficial está publicada en `GitHub Container Registry <https://github.com/codelibs/docker-fess/pkgs/container/fess>`__.
Los archivos Compose y los procedimientos de inicio se gestionan en el repositorio `docker-fess <https://github.com/codelibs/docker-fess>`__.

Paso 1: Obtención del Archivo Docker Compose
=============================================

Se requieren los siguientes archivos para iniciar con Docker Compose.

Método 1: Descargar Archivos Individualmente
----------------------------------------------

Descargue los siguientes archivos:

::

    $ mkdir fess-docker
    $ cd fess-docker
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.7.0/compose/compose.yaml
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.7.0/compose/compose-opensearch3.yaml

Método 2: Clonar el Repositorio con Git
------------------------------------------

Si Git está instalado, también puede clonar todo el repositorio:

::

    $ git clone --depth 1 --branch v15.7.0 https://github.com/codelibs/docker-fess.git
    $ cd docker-fess/compose

Paso 2: Verificación del Archivo Docker Compose
================================================

Contenido de ``compose.yaml``
-------------------------------

``compose.yaml`` contiene la configuración de Fess en sí (servicio ``fess01``).

Elementos de configuración principales:

- **Número de puerto**: Puerto de la interfaz web de Fess (predeterminado: 8080)
- **Variables de entorno**: El destino de conexión de OpenSearch (``SEARCH_ENGINE_HTTP_URL``), la ruta del archivo de diccionario (``FESS_DICTIONARY_PATH``), entre otras
- **Orden de inicio**: Se configura ``depends_on`` para que el inicio ocurra una vez que OpenSearch (``search01``) esté en un estado saludable

Contenido de ``compose-opensearch3.yaml``
---------------------------------------------

``compose-opensearch3.yaml`` contiene la configuración del motor de búsqueda (servicio ``search01``, OpenSearch).

Elementos de configuración principales:

- **Imagen de OpenSearch**: La imagen de OpenSearch que se utiliza (``ghcr.io/codelibs/fess-opensearch``)
- **Configuración de memoria**: Tamaño del heap de JVM
- **Volumen**: Volúmenes para la persistencia de datos (``search01_data``: datos de índice, ``search01_dictionary``: archivos de diccionario)

Personalización de la Configuración (Opcional)
-------------------------------------------------

Si desea cambiar la configuración predeterminada, edite ``compose.yaml``.

Ejemplo: para cambiar el número de puerto::

    services:
      fess01:
        ports:
          - "9080:8080"  # Mapear al puerto 9080 del host

Ejemplo: para cambiar la configuración de memoria::

    services:
      fess01:
        environment:
          - "FESS_HEAP_SIZE=2g"  # Establecer el tamaño del heap de Fess en 2GB

Paso 3: Inicio del Contenedor Docker
=====================================

Inicio Básico
--------------

Inicie Fess y OpenSearch con el siguiente comando:

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   - Especifique múltiples archivos Compose con la opción ``-f``
   - Ejecute en segundo plano con la opción ``-d``

Verificación de registros de inicio::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f

Puede salir de la visualización de registros con ``Ctrl+C``.

Verificación del Inicio
-------------------------

Verifique el estado de los contenedores::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

Verifique que los siguientes contenedores estén en ejecución:

- ``fess01``
- ``search01``

.. tip::

   El inicio puede tardar varios minutos. Primero OpenSearch (``search01``) debe alcanzar un estado saludable,
   y luego se inicia Fess (``fess01``).
   Verifique el estado de cada contenedor con ``docker compose ... ps``; una vez que ``fess01`` esté en
   ejecución, podrá acceder a http://localhost:8080/ desde el navegador.

Paso 4: Acceso desde el Navegador
==================================

Una vez completado el inicio, acceda a las siguientes URL:

- **Pantalla de búsqueda**: http://localhost:8080/
- **Pantalla de administración**: http://localhost:8080/admin

Cuenta de administrador predeterminada:

- Nombre de usuario: ``admin``
- Contraseña: ``admin``

.. warning::

   **Nota Importante sobre Seguridad**

   Asegúrese de cambiar la contraseña de administrador en entornos de producción.
   Para más detalles, consulte :doc:`security`.

Habilitación del Modo de Búsqueda con IA (Plugins LLM)
========================================================

A partir de |Fess| 15.7, la función de modo de búsqueda con IA (RAG Chat) se separó en los plugins
``fess-llm-*``. El repositorio oficial `docker-fess <https://github.com/codelibs/docker-fess>`__ incluye
archivos overlay para los principales proveedores de LLM.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Overlay
     - Uso
   * - ``compose-ollama.yaml``
     - Ollama (LLM local, inicia un servicio ``ollama01`` adicional)
   * - ``compose-gemini.yaml``
     - Google Gemini (API en la nube)
   * - ``compose-openai.yaml``
     - OpenAI (API en la nube)

Cada overlay obtiene automáticamente el plugin correspondiente mediante ``FESS_PLUGINS`` y habilita RAG Chat
configurando ``-Dfess.config.rag.chat.enabled=true`` en ``FESS_JAVA_OPTS``.
En el caso de Gemini y OpenAI, que utilizan API en la nube, además se especifica el proveedor a usar mediante
``-Dfess.system.rag.llm.name``, y se configuran la clave de API (``rag.llm.<provider>.api.key``) y el modelo
(``rag.llm.<provider>.model``).
En Ollama se utiliza tal cual el valor predeterminado de ``rag.llm.name`` (``ollama``), por lo que no se
especifica explícitamente, y se configura el destino de conexión (``rag.llm.ollama.api.url``).

Ejemplo de uso de Gemini::

    $ export GEMINI_API_KEY="AIzaSy..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-gemini.yaml up -d

Ejemplo de uso de OpenAI::

    $ export OPENAI_API_KEY="sk-..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

.. note::

   El modelo utilizado se puede cambiar mediante las variables de entorno ``GEMINI_MODEL`` y ``OPENAI_MODEL``
   (los valores predeterminados son ``gemini-2.5-flash`` y ``gpt-5-mini``, respectivamente).

Ejemplo de uso de Ollama::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    $ docker exec -it ollama01 ollama pull gpt-oss:20b

.. warning::

   El servicio ``ollama01`` de ``compose-ollama.yaml`` está definido para usar una GPU NVIDIA de forma
   predeterminada (se requiere `NVIDIA Container Toolkit <https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html>`__).
   Si va a ejecutarlo en un entorno sin GPU, elimine o comente el bloque ``deploy:`` de
   ``compose-ollama.yaml`` (la especificación de GPU bajo ``reservations``).

.. tip::

   Después del inicio, en la pantalla de configuración "Sistema > General" del panel de administración,
   puede cambiar el proveedor de LLM a utilizar (``rag.llm.name``) y la configuración específica de cada
   proveedor. Sin embargo, estos cambios se guardan en el archivo de configuración dentro del contenedor,
   por lo que se perderán si se recrea el contenedor (``docker compose down`` seguido de ``up``).
   Para hacer persistente la configuración, especifíquela mediante ``FESS_JAVA_OPTS`` en el archivo Compose,
   como en los ejemplos anteriores.

Persistencia de Datos
======================

Todos los datos de |Fess| (índices, documentos rastreados, información de usuarios, configuración, etc.) se
almacenan en OpenSearch.
Dado que estos datos se persisten en los volúmenes de OpenSearch, se conservan aunque se eliminen los
contenedores.
El propio contenedor de Fess (``fess01``) no mantiene estado y no tiene un volumen dedicado.

Verificación de volúmenes::

    $ docker volume ls

Volúmenes principales definidos en ``compose-opensearch3.yaml``:

- ``search01_data``: Datos de índice de OpenSearch (incluye todos los datos de Fess)
- ``search01_dictionary``: Archivos de diccionario

.. note::

   Los nombres de los volúmenes de Docker Compose llevan como prefijo el nombre del proyecto (de forma
   predeterminada, el nombre del directorio donde se encuentra el archivo Compose).
   Por ejemplo, si se inicia desde el directorio ``compose``, el nombre real del volumen sería algo como
   ``compose_search01_data``.

.. important::

   Los volúmenes no se eliminan aunque se eliminen los contenedores.
   Para eliminar los volúmenes, es necesario ejecutar explícitamente el comando ``docker volume rm``.

Detención del Contenedor Docker
================================

Para detener contenedores::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop

Para detener y eliminar contenedores::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   El comando ``down`` elimina los contenedores, pero no los volúmenes.
   Si también desea eliminar los volúmenes (como ``search01_data``), agregue la opción ``-v``::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

   **Precaución**: Ejecutar este comando eliminará todos los datos almacenados en OpenSearch.

Configuración Avanzada
=======================

Personalización de Variables de Entorno
----------------------------------------

Es posible realizar configuraciones detalladas agregando o modificando variables de entorno en ``compose.yaml``.

Variables de entorno principales:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Variable de Entorno
     - Descripción
   * - ``FESS_HEAP_SIZE``
     - Tamaño del heap de JVM de Fess (valor predeterminado de la imagen Docker: 512m)
   * - ``FESS_JAVA_OPTS``
     - Especificación de opciones JVM adicionales (por ejemplo, sobrescribir configuraciones mediante ``-Dfess.config.*``)
   * - ``FESS_PLUGINS``
     - Plugins que se instalan automáticamente al iniciar (formato ``name:version`` separado por espacios; ejemplo: ``fess-ds-wikipedia:15.7.0``)
   * - ``SEARCH_ENGINE_HTTP_URL``
     - Punto de conexión HTTP de OpenSearch (valor predeterminado en ``compose.yaml``: ``http://search01:9200``)
   * - ``SEARCH_ENGINE_USERNAME`` / ``SEARCH_ENGINE_PASSWORD``
     - Credenciales para conectarse a un OpenSearch con autenticación habilitada
   * - ``FESS_DICTIONARY_PATH``
     - Ruta del archivo de diccionario (directorio compartido con OpenSearch)
   * - ``FESS_PORT``
     - Puerto en el que Fess escucha dentro del contenedor (valor predeterminado: 8080)

Ejemplo::

    services:
      fess01:
        environment:
          - "FESS_HEAP_SIZE=4g"

.. note::

   Si desea cambiar la zona horaria, especifíquela en ``FESS_JAVA_OPTS`` como ``-Duser.timezone=Asia/Tokyo``.

Cómo Aplicar Archivos de Configuración
----------------------------------------

La configuración detallada de |Fess| se describe en el archivo ``fess_config.properties``.
En la imagen Docker, ``fess_config.properties`` se encuentra ubicado en ``/etc/fess`` dentro del contenedor.
Para reflejar la configuración en un entorno Docker, existen los siguientes métodos.

Método 1: Montar Archivos de Configuración
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``/etc/fess`` también contiene otros archivos de configuración necesarios para el funcionamiento de Fess, por
lo que si se reemplaza este directorio directamente mediante un montaje, el inicio fallará.
En su lugar, se utiliza el directorio de anulación ``/opt/fess``, que se añade al principio del classpath
(está vacío de forma predeterminada).

1. Cree en el host un directorio para preparar el archivo de configuración::

       $ mkdir -p /path/to/fess-config

2. Obtenga la plantilla del archivo de configuración (solo la primera vez)::

       $ curl -o /path/to/fess-config/fess_config.properties https://raw.githubusercontent.com/codelibs/fess/refs/tags/fess-15.7.0/src/main/resources/fess_config.properties

3. Edite ``/path/to/fess-config/fess_config.properties`` y escriba la configuración necesaria::

       # Ejemplo
       crawler.document.cache.enabled=false
       adaptive.load.control=20
       query.facet.fields=label,host

4. Agregue el montaje de volumen al servicio ``fess01`` en ``compose.yaml``::

       services:
         fess01:
           volumes:
             - /path/to/fess-config/fess_config.properties:/opt/fess/fess_config.properties

5. Inicie el contenedor::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   ``/opt/fess`` se añade al principio del classpath, por lo que el archivo ``fess_config.properties``
   colocado aquí tiene prioridad sobre el ``/etc/fess/fess_config.properties`` incluido en la imagen.
   Los archivos de propiedades se cargan como un todo y no se combinan elemento por elemento.
   Por lo tanto, es necesario colocar no solo los elementos que se desean sobrescribir, sino \*\*un archivo
   completo que contenga todos los elementos de configuración\*\*.
   Si solo desea cambiar algunos elementos, utilice el "Método 2" a continuación.

Método 2: Configuración mediante Propiedades del Sistema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Los elementos de configuración de ``fess_config.properties`` se pueden sobrescribir como propiedades del
sistema mediante variables de entorno.

Los elementos de configuración descritos en ``fess_config.properties`` (por ejemplo,
``crawler.document.cache.enabled=false``) se especifican en el formato
``-Dfess.config.nombre_del_elemento=valor``.

Agregue ``FESS_JAVA_OPTS`` a las variables de entorno del servicio ``fess01`` en ``compose.yaml``::

    services:
      fess01:
        environment:
          - "FESS_JAVA_OPTS=-Dfess.config.crawler.document.cache.enabled=false -Dfess.config.adaptive.load.control=20 -Dfess.config.query.facet.fields=label,host"

.. note::

   La parte que sigue a ``-Dfess.config.`` corresponde al nombre del elemento de configuración en
   ``fess_config.properties``.
   Si solo desea sobrescribir algunos elementos, este método es más sencillo.

Conexión a OpenSearch Externo
------------------------------

Si desea utilizar un clúster de OpenSearch existente, inicie solo con ``compose.yaml`` sin usar
``compose-opensearch3.yaml``, y cambie el destino de conexión.

1. Inicie sin especificar ``compose-opensearch3.yaml``::

       $ docker compose -f compose.yaml up -d

2. Configure el destino de conexión en el servicio ``fess01`` de ``compose.yaml``::

       environment:
         - "SEARCH_ENGINE_HTTP_URL=http://your-opensearch-host:9200"

.. note::

   Si se conecta a un OpenSearch con autenticación habilitada, especifique también
   ``SEARCH_ENGINE_USERNAME`` y ``SEARCH_ENGINE_PASSWORD``.

Otros Overlays y Configuraciones
=================================

El repositorio ``docker-fess`` incluye, además de lo anterior, archivos Compose y directorios para otros usos.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Archivo / Directorio
     - Uso
   * - ``compose-dashboards3.yaml``
     - Agrega OpenSearch Dashboards (puerto 5601, para visualización de datos)
   * - ``compose-minio.yaml``
     - Agrega MinIO (almacenamiento de objetos) y lo utiliza como destino de almacenamiento para la función de almacenamiento de Fess
   * - ``vanilla/``
     - Configuración que combina con un OpenSearch puro sin los plugins para Fess (algunas funciones, como la gestión de diccionarios, no están disponibles)
   * - ``snapshot/``
     - Configuración que utiliza imágenes de desarrollo (snapshot) (incluye configuraciones de clúster y combinaciones con Elasticsearch 8)
   * - ``multi-instance/``
     - Configuración que inicia múltiples instancias de Fess compartiendo un solo OpenSearch

Configuración de Red Docker
-----------------------------

Si se integra con múltiples servicios, puede usar una red personalizada.

Ejemplo::

    networks:
      fess-network:
        driver: bridge

    services:
      fess01:
        networks:
          - fess-network

Operación en Producción con Docker Compose
===========================================

Configuraciones recomendadas al usar Docker Compose en entornos de producción:

1. **Configuración de límites de recursos**::

       deploy:
         resources:
           limits:
             cpus: '2.0'
             memory: 4G
           reservations:
             cpus: '1.0'
             memory: 2G

2. **Configuración de política de reinicio**::

       restart: unless-stopped

3. **Configuración de registros**::

       logging:
         driver: "json-file"
         options:
           max-size: "10m"
           max-file: "3"

4. **Habilitación de configuración de seguridad**

   Habilite el plugin de seguridad de OpenSearch y configure la autenticación apropiada.
   Para más detalles, consulte :doc:`security`.

Solución de Problemas
======================

Los Contenedores no Inician
----------------------------

1. Verificar registros::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs

2. Verificar conflictos de puertos::

       $ sudo netstat -tuln | grep 8080
       $ sudo netstat -tuln | grep 9200

3. Verificar espacio en disco::

       $ df -h

Errores de Memoria Insuficiente
--------------------------------

Si OpenSearch no inicia por falta de memoria, es necesario aumentar ``vm.max_map_count``.

En Linux::

    $ sudo sysctl -w vm.max_map_count=262144

Para configurar permanentemente::

    $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
    $ sudo sysctl -p

Inicialización de Datos
------------------------

Para eliminar todos los datos y volver al estado inicial::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v
    $ docker volume prune

.. warning::

   Ejecutar este comando eliminará todos los datos completamente.

Próximos Pasos
===============

Después de completar la instalación, consulte la siguiente documentación:

- :doc:`run` - Inicio de |Fess| y configuración inicial
- :doc:`security` - Configuración de seguridad para entornos de producción
- :doc:`troubleshooting` - Solución de problemas

Preguntas Frecuentes
=====================

P: ¿Cuánto espacio en disco se necesita para descargar las imágenes?
------------------------------------------------------------------------

R: Las imágenes de Fess y OpenSearch se descargan la primera vez que se inician, y en conjunto requieren
aproximadamente varios GB de espacio en disco.
Dependiendo del entorno de red, la descarga puede tardar cierto tiempo.

P: ¿Es posible operar en Kubernetes?
--------------------------------------

R: Sí, es posible. Puede convertir el archivo Docker Compose en manifiestos de Kubernetes usando herramientas
como ``kompose``, o crear sus propios manifiestos para operar (no se ofrece un chart oficial de Helm).

P: ¿Cómo se actualizan los contenedores?
------------------------------------------

R: Actualice siguiendo estos pasos:

1. Obtenga los archivos Compose más recientes
2. Detenga los contenedores::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

3. Obtenga nuevas imágenes::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

4. Inicie los contenedores::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

P: ¿Es posible una configuración de múltiples nodos?
-------------------------------------------------------

R: Sí, es posible. Puede configurar OpenSearch con múltiples nodos tomando como referencia
``snapshot/compose-cluster.yaml`` del repositorio ``docker-fess``, o configurar múltiples instancias de Fess
que comparten un solo OpenSearch tomando como referencia ``multi-instance/``.
Sin embargo, para entornos de producción se recomienda usar herramientas de orquestación como Kubernetes.
