==================================
Arquitectura de Plugins
==================================

Vision General
==============

El sistema de plugins de |Fess| permite extender la funcionalidad principal.
Los plugins se distribuyen como archivos JAR y se cargan dinamicamente.

Tipos de Plugins
================

|Fess| soporta los siguientes tipos de plugins:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Tipo
     - Descripcion
   * - Almacen de datos
     - Obtencion de contenido desde nuevas fuentes de datos (Box, Slack, etc.)
   * - Motor de scripts
     - Soporte para nuevos lenguajes de script
   * - Aplicacion web
     - Extension de la interfaz web
   * - Ingest
     - Procesamiento de datos durante la indexacion

Estructura de un Plugin
=======================

Estructura Basica
-----------------

::

    fess-ds-example/
    ├── pom.xml
    └── src/main/java/org/codelibs/fess/ds/example/
        ├── ExampleDataStore.java      # Implementacion del almacen de datos
        └── ExampleDataStoreHandler.java # Manejador (opcional)

Ejemplo de pom.xml
------------------

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                                 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-ds-example</artifactId>
        <version>15.5.0</version>
        <packaging>jar</packaging>

        <name>fess-ds-example</name>
        <description>Example DataStore for Fess</description>

        <properties>
            <fess.version>15.5.0</fess.version>
            <java.version>21</java.version>
        </properties>

        <dependencies>
            <dependency>
                <groupId>org.codelibs.fess</groupId>
                <artifactId>fess</artifactId>
                <version>${fess.version}</version>
                <scope>provided</scope>
            </dependency>
        </dependencies>
    </project>

Registro de Plugins
===================

Registro en el Contenedor DI
----------------------------

Los plugins se registran en archivos de configuracion como ``fess_ds.xml``:

.. code-block:: xml

    <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
        <postConstruct name="register"/>
    </component>

Registro Automatico
-------------------

Muchos plugins se registran automaticamente con la anotacion ``@PostConstruct``:

.. code-block:: java

    @PostConstruct
    public void register() {
        ComponentUtil.getDataStoreManager().add(this);
    }

Ciclo de Vida del Plugin
========================

Inicializacion
--------------

1. Se carga el archivo JAR
2. El contenedor DI inicializa los componentes
3. Se llama al metodo ``@PostConstruct``
4. El plugin se registra en el gestor

Finalizacion
------------

1. Se llama al metodo ``@PreDestroy`` (si esta definido)
2. Limpieza de recursos

Dependencias
============

Dependencia con Fess Principal
------------------------------

.. code-block:: xml

    <dependency>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess</artifactId>
        <version>${fess.version}</version>
        <scope>provided</scope>
    </dependency>

Bibliotecas Externas
--------------------

Los plugins pueden incluir sus propias bibliotecas de dependencia:

.. code-block:: xml

    <dependency>
        <groupId>com.example</groupId>
        <artifactId>example-sdk</artifactId>
        <version>1.0.0</version>
    </dependency>

Las bibliotecas de dependencia se distribuyen junto con el JAR del plugin o
se crea un fat JAR usando Maven Shade Plugin.

Obtencion de Configuracion
==========================

Obtener desde FessConfig
------------------------

.. code-block:: java

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        public String getName() {
            return "Example";
        }

        @Override
        protected void storeData(DataConfig dataConfig, IndexUpdateCallback callback,
                Map<String, String> paramMap, Map<String, String> scriptMap,
                Map<String, Object> defaultDataMap) {

            // Obtener parametros
            String apiKey = paramMap.get("api.key");
            String baseUrl = paramMap.get("base.url");

            // Obtener FessConfig
            FessConfig fessConfig = ComponentUtil.getFessConfig();
        }
    }

Construccion e Instalacion
==========================

Construccion
------------

::

    mvn clean package

Instalacion
-----------

1. **Desde la pantalla de administracion**:

   - "Sistema" -> "Plugins" -> "Instalar"
   - Ingrese el nombre del plugin e instale

2. **Linea de comandos**:

   ::

       ./bin/fess-plugin install fess-ds-example

3. **Manual**:

   - Copie el archivo JAR al directorio ``plugins/``
   - Reinicie |Fess|

Depuracion
==========

Salida de Registros
-------------------

.. code-block:: java

    private static final Logger logger = LogManager.getLogger(ExampleDataStore.class);

    public void someMethod() {
        logger.debug("Debug message");
        logger.info("Info message");
    }

Modo de Desarrollo
------------------

Durante el desarrollo, puede depurar iniciando |Fess| desde el IDE:

1. Ejecute la clase ``FessBoot`` en modo de depuracion
2. Incluya el codigo fuente del plugin en el proyecto
3. Establezca puntos de interrupcion

Lista de Plugins Publicos
=========================

Principales plugins publicados por el proyecto |Fess|:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Plugin
     - Descripcion
   * - fess-ds-box
     - Conector de Box.com
   * - fess-ds-dropbox
     - Conector de Dropbox
   * - fess-ds-slack
     - Conector de Slack
   * - fess-ds-atlassian
     - Conector de Confluence/Jira
   * - fess-ds-git
     - Conector de repositorio Git
   * - fess-theme-*
     - Temas personalizados

Estos plugins estan disponibles como referencia de desarrollo en
`GitHub <https://github.com/codelibs>`__.

Informacion de Referencia
=========================

- :doc:`datastore-plugin` - Desarrollo de plugins de almacen de datos
- :doc:`script-engine-plugin` - Plugins de motor de scripts
- :doc:`webapp-plugin` - Plugins de aplicacion web
- :doc:`ingest-plugin` - Plugins Ingest
