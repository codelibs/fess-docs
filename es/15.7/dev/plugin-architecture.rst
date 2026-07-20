==================================
Arquitectura de Plugins
==================================

Visión General
==============

El sistema de plugins de |Fess| permite extender la funcionalidad principal.
Los plugins se distribuyen como archivos JAR y se cargan dinámicamente.

Tipos de Plugins
================

|Fess| soporta los siguientes tipos de plugins:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Tipo
     - Descripción
   * - Almacén de datos
     - Obtención de contenido desde nuevas fuentes de datos (Box, Slack, etc.)
   * - Motor de scripts
     - Soporte para nuevos lenguajes de script
   * - Aplicación web
     - Extensión de la interfaz web
   * - Ingest
     - Procesamiento de datos durante la indexación

Estructura de un Plugin
=======================

Estructura Básica
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
        <version>15.7.0</version>
        <packaging>jar</packaging>

        <name>fess-ds-example</name>
        <description>Example DataStore for Fess</description>

        <properties>
            <fess.version>15.7.0</fess.version>
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

Los plugins se registran en archivos de configuración como ``fess_ds.xml``:

.. code-block:: xml

    <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
        <postConstruct name="register"/>
    </component>

Registro Automático
-------------------

Muchos plugins se registran automáticamente con la anotación ``@PostConstruct``:

.. code-block:: java

    @PostConstruct
    public void register() {
        ComponentUtil.getDataStoreManager().add(this);
    }

Ciclo de Vida del Plugin
========================

Inicialización
--------------

1. Se carga el archivo JAR
2. El contenedor DI inicializa los componentes
3. Se llama al método ``@PostConstruct``
4. El plugin se registra en el gestor

Finalización
------------

1. Se llama al método ``@PreDestroy`` (si está definido)
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

Obtención de Configuración
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

Construcción e Instalación
==========================

Construcción
------------

::

    mvn clean package

Instalación
-----------

1. **Desde la pantalla de administración**:

   - "Sistema" -> "Plugins" -> "Instalar"
   - Ingrese el nombre del plugin e instale

2. **Línea de comandos**:

   ::

       ./bin/fess-plugin install fess-ds-example

3. **Manual**:

   - Copie el archivo JAR al directorio ``plugins/``
   - Reinicie |Fess|

Depuración
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

1. Ejecute la clase ``FessBoot`` en modo de depuración
2. Incluya el código fuente del plugin en el proyecto
3. Establezca puntos de interrupción

Lista de Plugins Públicos
=========================

Principales plugins publicados por el proyecto |Fess|:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Plugin
     - Descripción
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
   * - fess-theme-\*
     - Temas personalizados

Estos plugins están disponibles como referencia de desarrollo en
`GitHub <https://github.com/codelibs>`__.

Información de Referencia
=========================

- :doc:`datastore-plugin` - Desarrollo de plugins de almacén de datos
- :doc:`script-engine-plugin` - Plugins de motor de scripts
- :doc:`webapp-plugin` - Plugins de aplicación web
- :doc:`ingest-plugin` - Plugins Ingest
