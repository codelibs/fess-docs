==========================
Arquitectura de Plugins
==========================

Visión General
==============

El sistema de plugins de |Fess| permite ampliar la funcionalidad
principal. Los plugins se distribuyen como archivos JAR y, al añadirse
al classpath, el contenedor DI (Lasta Di) carga los componentes y los
registra en la fábrica o el gestor correspondiente.

Tipos de Plugins
================

|Fess| determina el tipo de plugin según el prefijo del nombre del
artefacto (``PluginHelper.ArtifactType``). Los tipos principales son los
siguientes:

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - Tipo
     - Prefijo
     - Descripción
   * - Almacén de datos
     - ``fess-ds-*``
     - Obtención de contenido desde nuevas fuentes de datos (Box, Slack,
       Git, etc.)
   * - Aplicación web
     - ``fess-webapp-*``
     - Ampliación de la interfaz web o de las funciones de búsqueda
   * - Motor de scripts
     - ``fess-script-*``
     - Soporte para nuevos lenguajes de script
   * - Ingest
     - ``fess-ingest-*``
     - Procesamiento de documentos durante el registro en el índice
   * - Tema
     - ``fess-theme-*``
     - Personalización del diseño de la pantalla de búsqueda
   * - Miniatura
     - ``fess-thumbnail-*``
     - Adición de métodos de generación de miniaturas
   * - LLM
     - ``fess-llm-*``
     - Adición de proveedores de LLM utilizados en RAG/chat
   * - Rastreador
     - ``fess-crawler-*``
     - Ampliación de clientes de rastreador

Estructura del Plugin
======================

Estructura Básica
-----------------

Tomando como ejemplo `fess-ds-example
<https://github.com/codelibs/fess-ds-example>`__, la plantilla de
implementación de un plugin de almacén de datos, un plugin se compone de
una «clase de implementación» y un «archivo de registro DI»:

::

    fess-ds-example/
    ├── pom.xml
    └── src/main/
        ├── java/org/codelibs/fess/ds/example/
        │   └── ExampleDataStore.java     # Implementación del almacén de datos
        └── resources/
            └── fess_ds++.xml             # Registro de componentes DI

Ejemplo de pom.xml
------------------

Los plugins se construyen como jar con ``fess-parent`` como POM padre.
Las bibliotecas que se proporcionan en tiempo de ejecución desde el
propio |Fess|, como ``fess`` u ``opensearch``, se declaran con el ámbito
``provided``. El número de versión y la configuración de compilación
(formateador, cabeceras de licencia, etc.) se heredan del POM padre.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                                 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-ds-example</artifactId>
        <version>15.8.0</version>
        <packaging>jar</packaging>

        <parent>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess-parent</artifactId>
            <version>15.8.0</version>
            <relativePath />
        </parent>

        <dependencies>
            <dependency>
                <groupId>org.codelibs.fess</groupId>
                <artifactId>fess</artifactId>
                <scope>provided</scope>
            </dependency>
            <dependency>
                <groupId>org.opensearch</groupId>
                <artifactId>opensearch</artifactId>
                <scope>provided</scope>
            </dependency>
        </dependencies>
    </project>

.. note::

   En las ramas en desarrollo, la versión llevará el sufijo
   ``-SNAPSHOT``, como en ``15.8.0-SNAPSHOT``. Las bibliotecas de
   dependencia propias del plugin se declaran como dependencias Maven
   normales. Puesto que no están incluidas en el propio |Fess|, deben
   distribuirse junto con el plugin.

Registro del Plugin
====================

Registro en el Contenedor DI
-----------------------------

Los plugins registran sus componentes mediante un archivo de
configuración DI cuyo nombre termina en ``++``, como ``fess_ds++.xml``.
Lasta Di combina automáticamente los archivos con el sufijo ``++``
encontrados en el classpath con el archivo de configuración
correspondiente del propio |Fess| (en este ejemplo, ``fess_ds.xml``).
Gracias a este mecanismo, el plugin puede añadir sus propios componentes
sin modificar los archivos del propio |Fess|.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

Según el tipo de plugin, el archivo de destino de la fusión varía. Por
ejemplo, el motor de scripts utiliza ``fess_se++.xml``, Ingest utiliza
``fess_ingest++.xml``, los proveedores de LLM utilizan
``fess_llm++.xml``, y las aplicaciones web utilizan ``app++.xml``.

Inicialización del Componente
-------------------------------

``<postConstruct name="register">`` es una configuración del ciclo de
vida de Lasta Di que especifica el método que se invoca tras la creación
del componente. En el caso de un almacén de datos, se invoca el método
``register()`` que posee ``AbstractDataStore``, y este se registra a sí
mismo en ``DataStoreFactory``:

.. code-block:: java

    // Implementación de AbstractDataStore (normalmente no requiere sobrescritura)
    public void register() {
        ComponentUtil.getDataStoreFactory().add(getName(), this);
    }

.. note::

   Esto no es la anotación ``@PostConstruct`` de Java, sino una
   inicialización mediante el elemento ``<postConstruct>`` del archivo
   de configuración DI. El nombre que se registra es el valor devuelto
   por ``getName()``, y es el nombre que se selecciona al elegir el
   plugin en la consola de administración.

Ciclo de Vida del Plugin
==========================

Inicialización
---------------

1. El JAR del plugin se añade al classpath.
2. El contenedor DI combina ``fess_*++.xml`` y crea los componentes.
3. Se invoca el método especificado en ``<postConstruct>`` (por ejemplo,
   ``register``).
4. El plugin se registra en la fábrica o el gestor correspondiente.

Finalización
-------------

1. Al finalizar el contenedor DI, se invoca el método especificado en
   ``<preDestroy>`` (si está definido).
2. Limpieza de recursos.

.. note::

   En el caso de un almacén de datos, ``AbstractDataStore.stop()``
   activa un indicador de detención en el rastreo en curso, y el bucle
   de procesamiento de registros finaliza de forma segura.

Dependencias
============

Dependencia con el Núcleo de Fess
-----------------------------------

Puesto que las clases del propio |Fess| están presentes en el classpath
del servidor en tiempo de ejecución, se declaran como dependencia con el
ámbito ``provided`` (no se incluyen en el JAR del plugin).

.. code-block:: xml

    <dependency>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess</artifactId>
        <scope>provided</scope>
    </dependency>

Bibliotecas Externas
----------------------

Los plugins pueden incluir sus propias bibliotecas de dependencia:

.. code-block:: xml

    <dependency>
        <groupId>com.example</groupId>
        <artifactId>example-sdk</artifactId>
        <version>1.0.0</version>
    </dependency>

Puesto que estas no están incluidas en el propio |Fess|, deben
distribuirse junto con el plugin.

Obtención de la Configuración
================================

Obtención de Parámetros y de FessConfig
------------------------------------------

En el método ``storeData()`` del almacén de datos, los parámetros
configurados en la consola de administración se obtienen desde
``DataStoreParams``. Para obtener los valores, utilice
``getAsString()`` (dado que ``DataStoreParams`` no implementa ``Map``,
``get()`` no devuelve una cadena). Además, los valores de configuración
de |Fess| se pueden obtener desde ``ComponentUtil.getFessConfig()``:

.. code-block:: java

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        protected String getName() {
            // Se utiliza como nombre del manejador. La convención es devolver el nombre simple de la clase
            return this.getClass().getSimpleName();
        }

        @Override
        protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback,
                final DataStoreParams paramMap, final Map<String, String> scriptMap,
                final Map<String, Object> defaultDataMap) {

            // Obtención de los parámetros
            final String apiKey = paramMap.getAsString("api.key");
            final String baseUrl = paramMap.getAsString("base.url");

            // Obtención de FessConfig
            final FessConfig fessConfig = ComponentUtil.getFessConfig();
        }
    }

Para más detalles sobre la implementación de ``storeData()`` (el flujo
de obtención de datos, evaluación de scripts y registro en el índice),
consulte :doc:`datastore-plugin`.

Construcción e Instalación
=============================

Construcción
-------------

::

    mvn clean package

En el directorio ``target/`` se generará un archivo JAR (por ejemplo,
``fess-ds-example-15.8.0.jar``).

Instalación
------------

1. **Desde la consola de administración**:

   - Abra «Sistema» → «Plugin» → «Instalar»
   - Seleccione de la lista del repositorio de plugins, o suba el
     archivo JAR compilado para instalarlo

2. **Manual**:

   - Copie el archivo JAR al directorio ``app/WEB-INF/plugin/``
   - Reinicie |Fess|

Para más detalles sobre el procedimiento de instalación, consulte
:doc:`../admin/plugin-guide`.

Depuración
==========

Salida de Logs
---------------

|Fess| utiliza Log4j2. El logger se obtiene mediante
``LogManager.getLogger()``:

.. code-block:: java

    private static final Logger logger = LogManager.getLogger(ExampleDataStore.class);

    public void someMethod() {
        logger.debug("Debug message");
        logger.info("Info message");
    }

.. note::

   No registre en los logs información sensible, como contraseñas o
   tokens.

Modo de Desarrollo
--------------------

Durante el desarrollo, puede depurar |Fess| iniciándolo desde el IDE:

1. Ejecute en modo depuración la clase ``org.codelibs.fess.FessBoot``.
2. Incluya el código fuente del plugin en el proyecto.
3. Establezca puntos de interrupción.

Lista de Plugins Públicos
============================

En el proyecto |Fess| se publican numerosos plugins. A continuación se
muestran algunos ejemplos representativos (esta lista no es exhaustiva):

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Plugin
     - Descripción
   * - ``fess-ds-box``
     - Conector de Box
   * - ``fess-ds-dropbox``
     - Conector de Dropbox
   * - ``fess-ds-slack``
     - Conector de Slack
   * - ``fess-ds-atlassian``
     - Conector de JIRA / Confluence
   * - ``fess-ds-git``
     - Conector de repositorios Git
   * - ``fess-llm-openai``
     - Proveedor de LLM OpenAI
   * - ``fess-theme-*``
     - Tema personalizado

Además de estos, también se publican conectores de almacén de datos como
``fess-ds-csv`` / ``fess-ds-db`` / ``fess-ds-json`` /
``fess-ds-microsoft365`` / ``fess-ds-sharepoint``, y proveedores de LLM
como ``fess-llm-ollama`` / ``fess-llm-gemini``. Estos plugins se
publican en `GitHub <https://github.com/codelibs>`__ como referencia
para el desarrollo.

Información de Referencia
============================

- :doc:`datastore-plugin` - Desarrollo de plugins de almacén de datos
- :doc:`script-engine-plugin` - Plugin de motor de scripts
- :doc:`webapp-plugin` - Plugin de aplicación web
- :doc:`ingest-plugin` - Plugin de Ingest
- :doc:`theme-development` - Personalización de temas
- :doc:`../admin/plugin-guide` - Instalación de plugins
