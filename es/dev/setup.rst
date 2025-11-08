====================
Configuración del Entorno de Desarrollo
====================

Esta página explica en detalle el procedimiento para construir el entorno de desarrollo de |Fess|.
Desde la selección del IDE hasta la obtención del código fuente, ejecución y depuración,
se explica paso a paso.

.. contents:: Índice
   :local:
   :depth: 2

Requisitos del Sistema
==========

Se recomiendan los siguientes requisitos de hardware para el entorno de desarrollo.

Requisitos de Hardware
--------------

- **CPU**: 4 núcleos o más
- **Memoria**: 8GB o más (se recomienda 16GB)
- **Disco**: 20GB o más de espacio libre

.. note::

   Durante el desarrollo, |Fess| y OpenSearch integrado se ejecutan simultáneamente,
   por lo que asegure suficiente memoria y espacio en disco.

Requisitos de Software
--------------

- **OS**: Windows 10/11, macOS 11 o posterior, Linux (Ubuntu 20.04 o posterior, etc.)
- **Java**: JDK 21 o posterior
- **Maven**: 3.x o posterior
- **Git**: 2.x o posterior
- **IDE**: Eclipse, IntelliJ IDEA, VS Code, etc.

Instalación de Software Obligatorio
==========================

Instalación de Java
-----------------

Se requiere Java 21 o posterior para el desarrollo de |Fess|.

Instalación de Eclipse Temurin (Recomendado)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Se recomienda Eclipse Temurin (anteriormente AdoptOpenJDK).

1. Acceda a `Adoptium <https://adoptium.net/temurin/releases/>`__
2. Descargue la versión LTS de Java 21
3. Instale siguiendo las instrucciones del instalador

Verificación de Instalación
~~~~~~~~~~~~~~

Ejecute lo siguiente en la terminal o símbolo del sistema:

.. code-block:: bash

    java -version

Si ve una salida como la siguiente, es exitoso:

.. code-block:: text

    openjdk version "21.0.x" 2024-xx-xx LTS
    OpenJDK Runtime Environment Temurin-21.0.x+x (build 21.0.x+x-LTS)
    OpenJDK 64-Bit Server VM Temurin-21.0.x+x (build 21.0.x+x-LTS, mixed mode, sharing)

Configuración de Variables de Entorno
~~~~~~~~~~~~

**Linux/macOS:**

Agregue lo siguiente a ``~/.bashrc`` o ``~/.zshrc``:

.. code-block:: bash

    export JAVA_HOME=/path/to/java21
    export PATH=$JAVA_HOME/bin:$PATH

**Windows:**

1. Abra "Editar las variables de entorno del sistema"
2. Haga clic en "Variables de entorno"
3. Agregue ``JAVA_HOME``: ``C:\Program Files\Eclipse Adoptium\jdk-21.x.x.x-hotspot``
4. Agregue ``%JAVA_HOME%\bin`` a ``PATH``

Instalación de Maven
------------------

Instale Maven 3.x o posterior.

Descarga e Instalación
~~~~~~~~~~~~~~~~~~~~~~~~

1. Acceda a la `página de descarga de Maven <https://maven.apache.org/download.cgi>`__
2. Descargue Binary zip/tar.gz archive
3. Extraiga y coloque en una ubicación apropiada

**Linux/macOS:**

.. code-block:: bash

    tar xzvf apache-maven-3.x.x-bin.tar.gz
    sudo mv apache-maven-3.x.x /opt/
    sudo ln -s /opt/apache-maven-3.x.x /opt/maven

**Windows:**

1. Extraiga el archivo ZIP
2. Colóquelo en ``C:\Program Files\Apache\maven`` o similar

Configuración de Variables de Entorno
~~~~~~~~~~~~

**Linux/macOS:**

Agregue lo siguiente a ``~/.bashrc`` o ``~/.zshrc``:

.. code-block:: bash

    export MAVEN_HOME=/opt/maven
    export PATH=$MAVEN_HOME/bin:$PATH

**Windows:**

1. Agregue ``MAVEN_HOME``: ``C:\Program Files\Apache\maven``
2. Agregue ``%MAVEN_HOME%\bin`` a ``PATH``

Verificación de Instalación
~~~~~~~~~~~~~~

.. code-block:: bash

    mvn -version

Si ve una salida como la siguiente, es exitoso:

.. code-block:: text

    Apache Maven 3.x.x
    Maven home: /opt/maven
    Java version: 21.0.x, vendor: Eclipse Adoptium

Instalación de Git
----------------

Si Git no está instalado, instálelo desde lo siguiente.

- **Windows**: `Git para Windows <https://git-scm.com/download/win>`__
- **macOS**: ``brew install git`` o `página de descarga de Git <https://git-scm.com/download/mac>`__
- **Linux**: ``sudo apt install git`` (Ubuntu/Debian) o ``sudo yum install git`` (RHEL/CentOS)

Verificación de instalación:

.. code-block:: bash

    git --version

Configuración del IDE
===============

En caso de Eclipse
------------

Eclipse es el IDE recomendado en la documentación oficial de |Fess|.

Instalación de Eclipse
~~~~~~~~~~~~~~~~~~~~

1. Acceda a la `página de descarga de Eclipse <https://www.eclipse.org/downloads/>`__
2. Descargue "Eclipse IDE for Enterprise Java and Web Developers"
3. Ejecute el instalador y siga las instrucciones para instalar

Plugins Recomendados
~~~~~~~~~~~~

Eclipse incluye los siguientes plugins por defecto:

- Maven Integration for Eclipse (m2e)
- Eclipse Java Development Tools

Importación del Proyecto
~~~~~~~~~~~~~~~~~~~~

1. Inicie Eclipse
2. Seleccione ``File`` > ``Import``
3. Seleccione ``Maven`` > ``Existing Maven Projects``
4. Especifique el directorio del código fuente de Fess
5. Haga clic en ``Finish``

Configuración de Ejecución
~~~~~~~~~~~~

1. Seleccione ``Run`` > ``Run Configurations...``
2. Haga clic derecho en ``Java Application`` y seleccione ``New Configuration``
3. Configure lo siguiente:

   - **Name**: Fess Boot
   - **Project**: fess
   - **Main class**: ``org.codelibs.fess.FessBoot``

4. Haga clic en ``Apply``

En caso de IntelliJ IDEA
-------------------

IntelliJ IDEA también es un IDE ampliamente utilizado.

Instalación de IntelliJ IDEA
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Acceda a la `página de descarga de IntelliJ IDEA <https://www.jetbrains.com/idea/download/>`__
2. Descargue Community Edition (gratis) o Ultimate Edition
3. Ejecute el instalador y siga las instrucciones para instalar

Importación del Proyecto
~~~~~~~~~~~~~~~~~~~~

1. Inicie IntelliJ IDEA
2. Seleccione ``Open``
3. Seleccione ``pom.xml`` del directorio del código fuente de Fess
4. Haga clic en ``Open as Project``
5. Se importa automáticamente como proyecto Maven

Configuración de Ejecución
~~~~~~~~~~~~

1. Seleccione ``Run`` > ``Edit Configurations...``
2. Haga clic en el botón ``+`` y seleccione ``Application``
3. Configure lo siguiente:

   - **Name**: Fess Boot
   - **Module**: fess
   - **Main class**: ``org.codelibs.fess.FessBoot``
   - **JRE**: Java 21

4. Haga clic en ``OK``

En caso de VS Code
------------

VS Code también es una opción si prefiere un entorno de desarrollo ligero.

Instalación de VS Code
~~~~~~~~~~~~~~~~~~~~

1. Acceda a la `página de descarga de VS Code <https://code.visualstudio.com/>`__
2. Descargue y ejecute el instalador

Instalación de Extensiones Necesarias
~~~~~~~~~~~~~~~~~~~~~~~~

Instale las siguientes extensiones:

- **Extension Pack for Java**: Conjunto de extensiones necesarias para desarrollo Java
- **Maven for Java**: Soporte de Maven

Abrir Proyecto
~~~~~~~~~~~~~~~~

1. Inicie VS Code
2. Seleccione ``File`` > ``Open Folder``
3. Seleccione el directorio del código fuente de Fess

Obtención del Código Fuente
==============

Clonar desde GitHub
-------------------

Clone el código fuente de |Fess| desde GitHub.

.. code-block:: bash

    git clone https://github.com/codelibs/fess.git
    cd fess

Si usa SSH:

.. code-block:: bash

    git clone git@github.com:codelibs/fess.git
    cd fess

.. tip::

   Si desarrolla bifurcando, primero bifurque el repositorio de Fess en GitHub,
   luego clone su repositorio bifurcado:

   .. code-block:: bash

       git clone https://github.com/YOUR_USERNAME/fess.git
       cd fess
       git remote add upstream https://github.com/codelibs/fess.git

Construcción del Proyecto
==================

Descarga de Plugins de OpenSearch
---------------------------------

Se necesitan plugins para OpenSearch para ejecutar Fess.
Descárguelos con el siguiente comando:

.. code-block:: bash

    mvn antrun:run

Este comando ejecuta lo siguiente:

- Descarga de OpenSearch
- Descarga e instalación de plugins obligatorios
- Configuración de OpenSearch

.. note::

   Ejecute este comando solo la primera vez o al actualizar plugins.
   No necesita ejecutarlo cada vez.

Construcción Inicial
--------

Construya el proyecto:

.. code-block:: bash

    mvn clean compile

La construcción inicial puede llevar tiempo (descarga de bibliotecas de dependencias, etc.).

Si la construcción es exitosa, aparecerá el siguiente mensaje:

.. code-block:: text

    [INFO] BUILD SUCCESS
    [INFO] Total time: xx:xx min
    [INFO] Finished at: 2024-xx-xxTxx:xx:xx+09:00

Ejecución de Fess
==========

Ejecución desde Línea de Comandos
--------------------

Ejecute usando Maven:

.. code-block:: bash

    mvn compile exec:java

O empaquete y luego ejecute:

.. code-block:: bash

    mvn package
    java -jar target/fess-15.3.x.jar

Ejecución desde IDE
------------

En caso de Eclipse
~~~~~~~~~~~~

1. Haga clic derecho en la clase ``org.codelibs.fess.FessBoot``
2. Seleccione ``Run As`` > ``Java Application``

O use la configuración de ejecución creada:

1. Haga clic en el menú desplegable del botón de ejecución en la barra de herramientas
2. Seleccione ``Fess Boot``

En caso de IntelliJ IDEA
~~~~~~~~~~~~~~~~~~

1. Haga clic derecho en la clase ``org.codelibs.fess.FessBoot``
2. Seleccione ``Run 'FessBoot.main()'``

O use la configuración de ejecución creada:

1. Haga clic en el menú desplegable del botón de ejecución en la barra de herramientas
2. Seleccione ``Fess Boot``

En caso de VS Code
~~~~~~~~~~~~

1. Abra ``src/main/java/org/codelibs/fess/FessBoot.java``
2. Seleccione ``Run Without Debugging`` desde el menú ``Run``

Confirmación de Inicio
--------

Fess tarda 1-2 minutos en iniciarse.
Si aparecen los siguientes registros en la consola, el inicio está completo:

.. code-block:: text

    [INFO] Boot Thread: Boot process completed successfully.

Verifique el funcionamiento accediendo a lo siguiente en el navegador:

- **Pantalla de búsqueda**: http://localhost:8080/
- **Pantalla de administración**: http://localhost:8080/admin/

  - Usuario predeterminado: ``admin``
  - Contraseña predeterminada: ``admin``

Cambiar Número de Puerto
--------------

Si el puerto predeterminado 8080 está en uso, puede cambiarlo en el siguiente archivo:

``src/main/resources/fess_config.properties``

.. code-block:: properties

    # Cambiar número de puerto
    server.port=8080

Ejecución de Depuración
==========

Depuración en IDE
------------------

En caso de Eclipse
~~~~~~~~~~~~

1. Haga clic derecho en la clase ``org.codelibs.fess.FessBoot``
2. Seleccione ``Debug As`` > ``Java Application``
3. Establezca puntos de interrupción y rastree el comportamiento del código

En caso de IntelliJ IDEA
~~~~~~~~~~~~~~~~~~

1. Haga clic derecho en la clase ``org.codelibs.fess.FessBoot``
2. Seleccione ``Debug 'FessBoot.main()'``
3. Establezca puntos de interrupción y rastree el comportamiento del código

En caso de VS Code
~~~~~~~~~~~~

1. Abra ``src/main/java/org/codelibs/fess/FessBoot.java``
2. Seleccione ``Start Debugging`` desde el menú ``Run``

Depuración Remota
--------------

También puede conectar un depurador a Fess iniciado desde la línea de comandos.

Inicie Fess en modo de depuración:

.. code-block:: bash

    mvn compile exec:java -Dexec.args="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005"

Conecte depuración remota desde IDE:

**Eclipse:**

1. Seleccione ``Run`` > ``Debug Configurations...``
2. Haga clic derecho en ``Remote Java Application`` y seleccione ``New Configuration``
3. Configure ``Port: 5005``
4. Haga clic en ``Debug``

**IntelliJ IDEA:**

1. Seleccione ``Run`` > ``Edit Configurations...``
2. Seleccione ``+`` > ``Remote JVM Debug``
3. Configure ``Port: 5005``
4. Haga clic en ``OK`` y ejecute ``Debug``

Configuraciones Útiles para el Desarrollo
==============

Cambiar Nivel de Registro
--------------

Cambiar el nivel de registro al depurar permite verificar información detallada.

Edite ``src/main/resources/log4j2.xml``:

.. code-block:: xml

    <Configuration status="INFO">
        <Loggers>
            <Logger name="org.codelibs.fess" level="DEBUG"/>
            <Root level="INFO">
                <AppenderRef ref="console"/>
            </Root>
        </Loggers>
    </Configuration>

Habilitar Hot Deploy
-------------------

LastaFlute puede reflejar algunos cambios sin reiniciar.

Configure lo siguiente en ``src/main/resources/fess_config.properties``:

.. code-block:: properties

    # Habilitar hot deploy
    development.here=true

Sin embargo, se requiere reiniciar para los siguientes cambios:

- Cambios en la estructura de clases (agregar/eliminar métodos, etc.)
- Cambios en archivos de configuración
- Cambios en bibliotecas de dependencias

Operación de OpenSearch Integrado
------------------------

En el entorno de desarrollo, se usa OpenSearch integrado.

Ubicación de OpenSearch:

.. code-block:: text

    target/fess/es/

Acceso directo a la API de OpenSearch:

.. code-block:: bash

    # Lista de índices
    curl -X GET http://localhost:9201/_cat/indices?v

    # Búsqueda de documentos
    curl -X GET http://localhost:9201/fess.search/_search?pretty

    # Verificar mapeo
    curl -X GET http://localhost:9201/fess.search/_mapping?pretty

Usar OpenSearch Externo
--------------------

Si usa un servidor OpenSearch externo,
edite ``src/main/resources/fess_config.properties``:

.. code-block:: properties

    # Deshabilitar OpenSearch integrado
    opensearch.cluster.name=fess
    opensearch.http.url=http://localhost:9200

Generación de Código con DBFlute
======================

|Fess| usa DBFlute para generar automáticamente
código Java desde el esquema de OpenSearch.

Regeneración cuando el Esquema Cambia
----------------------------

Si cambia el mapeo de OpenSearch, regenere
el código Java correspondiente con el siguiente comando:

.. code-block:: bash

    rm -rf mydbflute
    mvn antrun:run
    mvn dbflute:freegen
    mvn license:format

Explicación de cada comando:

- ``rm -rf mydbflute``: Eliminar directorio de trabajo de DBFlute existente
- ``mvn antrun:run``: Descargar plugins de OpenSearch
- ``mvn dbflute:freegen``: Generar código Java desde esquema
- ``mvn license:format``: Agregar encabezado de licencia

Solución de Problemas
==================

Errores de Construcción
----------

**Error: Versión antigua de Java**

.. code-block:: text

    [ERROR] Failed to execute goal ... requires at least Java 21

Solución: Instale Java 21 o posterior y configure ``JAVA_HOME`` apropiadamente.

**Error: Falla en descarga de bibliotecas de dependencias**

.. code-block:: text

    [ERROR] Failed to collect dependencies

Solución: Verifique la conexión de red, limpie el repositorio local de Maven y vuelva a intentar:

.. code-block:: bash

    rm -rf ~/.m2/repository
    mvn clean compile

Errores de Ejecución
--------

**Error: El puerto 8080 ya está en uso**

.. code-block:: text

    Address already in use

Solución:

1. Terminar proceso que usa el puerto 8080
2. O cambiar número de puerto en ``fess_config.properties``

**Error: OpenSearch no se inicia**

Verifique archivos de registro ``target/fess/es/logs/``.

Causas comunes:

- Memoria insuficiente: Aumentar tamaño del heap de JVM
- Puerto 9201 en uso: Cambiar número de puerto
- Espacio en disco insuficiente: Asegurar espacio en disco

IDE no Reconoce el Proyecto
----------------------------

**Actualizar Proyecto Maven**

- **Eclipse**: Clic derecho en proyecto > ``Maven`` > ``Update Project``
- **IntelliJ IDEA**: Haga clic en ``Reload All Maven Projects`` en ventana de herramientas ``Maven``
- **VS Code**: Ejecute ``Java: Clean Java Language Server Workspace`` desde paleta de comandos

Próximos Pasos
==========

Una vez completada la configuración del entorno de desarrollo, consulte los siguientes documentos:

- :doc:`architecture` - Comprender estructura del código
- :doc:`workflow` - Aprender flujo de trabajo de desarrollo
- :doc:`building` - Métodos de construcción y prueba
- :doc:`contributing` - Crear pull requests

Recursos
========

- `Descarga de Eclipse <https://www.eclipse.org/downloads/>`__
- `Descarga de IntelliJ IDEA <https://www.jetbrains.com/idea/download/>`__
- `Descarga de VS Code <https://code.visualstudio.com/>`__
- `Documentación de Maven <https://maven.apache.org/guides/>`__
- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
