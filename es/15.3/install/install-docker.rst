===================================
Instalación con Docker (Detalles)
===================================

Esta página describe los procedimientos de instalación de |Fess| utilizando Docker y Docker Compose.
Usar Docker permite construir un entorno |Fess| de manera fácil y rápida.

Requisitos Previos
==================

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

La imagen Docker de |Fess| está compuesta por los siguientes componentes:

- **Fess**: Cuerpo del sistema de búsqueda de texto completo
- **OpenSearch**: Motor de búsqueda

La imagen Docker oficial está publicada en `Docker Hub <https://hub.docker.com/r/codelibs/fess>`__.

Paso 1: Obtención del Archivo Docker Compose
=============================================

Se requieren los siguientes archivos para iniciar con Docker Compose.

Método 1: Descargar Archivos Individualmente
---------------------------------------------

Descargue los siguientes archivos:

::

    $ mkdir fess-docker
    $ cd fess-docker
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.3.0/compose/compose.yaml
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.3.0/compose/compose-opensearch3.yaml

Método 2: Clonar el Repositorio con Git
----------------------------------------

Si Git está instalado, también puede clonar todo el repositorio:

::

    $ git clone --depth 1 --branch v15.3.0 https://github.com/codelibs/docker-fess.git
    $ cd docker-fess/compose

Paso 2: Verificación del Archivo Docker Compose
================================================

Contenido de ``compose.yaml``
------------------------------

``compose.yaml`` contiene la configuración básica de Fess.

Elementos de configuración principales:

- **Número de puerto**: Puerto de la interfaz Web de Fess (predeterminado: 8080)
- **Variables de entorno**: Configuración como el tamaño del heap de Java
- **Volumen**: Configuración de persistencia de datos

Contenido de ``compose-opensearch3.yaml``
------------------------------------------

``compose-opensearch3.yaml`` contiene la configuración de OpenSearch.

Elementos de configuración principales:

- **Versión de OpenSearch**: Versión de OpenSearch a utilizar
- **Configuración de memoria**: Tamaño del heap de JVM
- **Volumen**: Configuración de persistencia de datos de índice

Personalización de la Configuración (Opcional)
-----------------------------------------------

Si desea cambiar la configuración predeterminada, edite ``compose.yaml``.

Ejemplo: Cambiar el número de puerto::

    services:
      fess:
        ports:
          - "9080:8080"  # Mapear al puerto 9080 del host

Ejemplo: Cambiar la configuración de memoria::

    services:
      fess:
        environment:
          - "FESS_HEAP_SIZE=2g"  # Establecer el tamaño del heap de Fess en 2GB

Paso 3: Inicio del Contenedor Docker
=====================================

Inicio Básico
-------------

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
------------------------

Verifique el estado de los contenedores::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

Verifique que los siguientes contenedores estén en ejecución:

- ``fess``
- ``opensearch``

.. tip::

   El inicio puede tardar varios minutos.
   Espere hasta que aparezca un mensaje como "Fess is ready" o similar en el registro.

Paso 4: Acceso desde el Navegador
==================================

Una vez completado el inicio, acceda a la siguiente URL:

- **Pantalla de búsqueda**: http://localhost:8080/
- **Pantalla de administración**: http://localhost:8080/admin

Cuenta de administrador predeterminada:

- Nombre de usuario: ``admin``
- Contraseña: ``admin``

.. warning::

   **Nota Importante sobre Seguridad**

   Asegúrese de cambiar la contraseña de administrador en entornos de producción.
   Para más detalles, consulte :doc:`security`.

Persistencia de Datos
======================

Los volúmenes se crean automáticamente para conservar los datos incluso si se eliminan los contenedores Docker.

Verificación de volúmenes::

    $ docker volume ls

Volúmenes relacionados con |Fess|:

- ``fess-es-data``: Datos de índice de OpenSearch
- ``fess-data``: Datos de configuración de Fess

.. important::

   Los volúmenes no se eliminan incluso si se eliminan los contenedores.
   Para eliminar volúmenes, debe ejecutar explícitamente el comando ``docker volume rm``.

Detención del Contenedor Docker
================================

Para detener contenedores::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop

Para detener y eliminar contenedores::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   El comando ``down`` elimina contenedores pero no volúmenes.
   Agregue la opción ``-v`` si también desea eliminar volúmenes::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

   **Precaución**: Ejecutar este comando eliminará todos los datos.

Configuración Avanzada
======================

Personalización de Variables de Entorno
----------------------------------------

Es posible realizar configuraciones detalladas agregando o modificando variables de entorno en ``compose.yaml``.

Variables de entorno principales:

.. list-table::
   :header-rows: 1
   :widths: 30 50

   * - Variable de Entorno
     - Descripción
   * - ``FESS_HEAP_SIZE``
     - Tamaño del heap de JVM de Fess (predeterminado: 1g)
   * - ``SEARCH_ENGINE_HTTP_URL``
     - Punto final HTTP de OpenSearch
   * - ``TZ``
     - Zona horaria (ejemplo: Asia/Tokyo)

Ejemplo::

    environment:
      - "FESS_HEAP_SIZE=4g"
      - "TZ=Asia/Tokyo"

Conexión a OpenSearch Externo
------------------------------

Si desea usar un clúster de OpenSearch existente, edite ``compose.yaml`` para cambiar el destino de conexión.

1. No use ``compose-opensearch3.yaml``::

       $ docker compose -f compose.yaml up -d

2. Configure ``SEARCH_ENGINE_HTTP_URL``::

       environment:
         - "SEARCH_ENGINE_HTTP_URL=http://your-opensearch-host:9200"

Configuración de Red Docker
----------------------------

Si se integra con múltiples servicios, puede usar una red personalizada.

Ejemplo::

    networks:
      fess-network:
        driver: bridge

    services:
      fess:
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
==============

Después de completar la instalación, consulte la siguiente documentación:

- :doc:`run` - Inicio de |Fess| y configuración inicial
- :doc:`security` - Configuración de seguridad para entornos de producción
- :doc:`troubleshooting` - Solución de problemas

Preguntas Frecuentes
=====================

P: ¿Cuál es el tamaño de las imágenes Docker?
----------------------------------------------

R: La imagen de Fess es de aproximadamente 1GB, y la imagen de OpenSearch es de aproximadamente 800MB.
La primera vez que se inicia, puede tardar tiempo en descargar.

P: ¿Es posible operar en Kubernetes?
-------------------------------------

R: Sí, es posible. Convirtiendo el archivo Docker Compose en manifiestos de Kubernetes o
usando Helm charts, es posible operar en Kubernetes.
Para más detalles, consulte la documentación oficial de Fess.

P: ¿Cómo se actualizan los contenedores?
-----------------------------------------

R: Actualice siguiendo estos pasos:

1. Obtenga los archivos Compose más recientes
2. Detenga los contenedores::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

3. Obtenga nuevas imágenes::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

4. Inicie los contenedores::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

P: ¿Es posible una configuración de múltiples nodos?
-----------------------------------------------------

R: Sí, es posible. Editando ``compose-opensearch3.yaml`` y definiendo múltiples nodos de OpenSearch,
puede configurar un clúster. Sin embargo, para entornos de producción se recomienda usar herramientas de orquestación como Kubernetes.
