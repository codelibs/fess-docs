=========================
Extender Fess con plugins
=========================

Introducción
============

Cuando no existe un plugin ``fess-ds-*`` adecuado para su sistema interno, o cuando quiere procesar todos los documentos antes de indexarlos, debe escribir su propio plugin.
Este artículo está dirigido a desarrolladores Java. Explica cómo crear, a partir de una plantilla oficial, un plugin que funcione en Fess 15.9, instalarlo y comprobar su funcionamiento.

Si sigue los pasos de este artículo, podrá:

- Entender los tipos de plugins y cómo los distingue Fess
- Compilar un plugin de almacén de datos a partir de ``fess-ds-example``, incorporarlo a Fess e indexar documentos con él
- Crear, a partir de ``fess-ingest-example``, un Ingester que procese los documentos antes de indexarlos

Se da por supuesto que dispone de Java 21 o posterior y Maven 3, y que Fess 15.9 está en ejecución (:doc:`guide-02`).
El uso de la pantalla de configuración de almacenes de datos se explica en :doc:`datastore-basics`; si lo lee primero, le resultará más fácil seguir los pasos.

Tipos de plugins
================

Un plugin es un archivo jar que se coloca en ``app/WEB-INF/plugin/`` dentro del directorio de instalación de Fess.
Fess determina el tipo de plugin a partir del comienzo (prefijo) del nombre del archivo jar (``PluginHelper.ArtifactType``).
Los tipos de la versión 15.9 son los siguientes.

.. list-table::
   :header-rows: 1
   :widths: 22 43 35

   * - Prefijo
     - Función
     - Repositorio de referencia
   * - ``fess-ds``
     - Almacén de datos. Obtiene registros de un sistema externo y los indexa
     - ``fess-ds-example``
   * - ``fess-ingest``
     - Ingester. Procesa los documentos antes de indexarlos
     - ``fess-ingest-example``
   * - ``fess-script``
     - Motor de scripts
     - ``fess-script-groovy``
   * - ``fess-webapp``
     - Extensión de la aplicación web (añadir API o endpoints)
     - ``fess-webapp-mcp``
   * - ``fess-thumbnail``
     - Generación de miniaturas
     - ``fess-thumbnail-playwright``
   * - ``fess-crawler``
     - Cliente del rastreador
     - ``fess-crawler-playwright``
   * - ``fess-llm``
     - Proveedor de LLM que usa el modo de búsqueda con IA
     - ``fess-llm-openai``
   * - ``fess-storage``
     - Almacenamiento de objetos (S3 / GCS)
     - ``fess-storage-s3``
   * - ``fess-sso``
     - Método de autenticación de inicio de sesión único (SSO)
     - ``fess-sso-oidc``

Todos estos repositorios están publicados en https://github.com/codelibs.

El diseño de la página de búsqueda no se cambia con plugins.
Los plugins de tema JAR ``fess-theme-*``, que reemplazaban las JSP, se eliminaron en la versión 15.9; la página de búsqueda es ahora un tema ZIP compuesto por ``theme.yml``, ``index.html`` y ``assets/``.
Los temas se suben desde [Sistema] > [Tema].
Para saber cómo crear uno, consulte la `Guía de Desarrollo de Temas <https://fess.codelibs.org/es/stable/dev/theme-development.html>`__; para integrar la búsqueda en un sitio existente, consulte :doc:`guide-03`.

Crear un plugin de almacén de datos
===================================

Obtener la plantilla
--------------------

``fess-ds-example`` es un repositorio publicado como esqueleto para plugins de almacén de datos.
Su rama predeterminada sigue la versión en desarrollo (15.10.0-SNAPSHOT), así que, para compilar para 15.9, use el commit adaptado a 15.9.0.

::

    $ git clone https://github.com/codelibs/fess-ds-example.git
    $ cd fess-ds-example
    $ git checkout 0252a8b08d7de4eeea7a88c52aa884094ef099be

La única diferencia entre este commit y la rama predeterminada son dos líneas de ``pom.xml`` (la versión del proyecto y la del POM padre).
Obtendrá el mismo resultado si se queda en la rama predeterminada y cambia para 15.9 los dos puntos que se describen en la sección siguiente.

pom.xml
-------

Las partes esenciales de ``pom.xml`` son las siguientes.

.. code-block:: xml

    <artifactId>fess-ds-example</artifactId>
    <packaging>jar</packaging>
    <version>15.9.0-SNAPSHOT</version>

    <parent>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-parent</artifactId>
        <version>15.9.0</version>
        <relativePath />
    </parent>

    <dependencies>
        <dependency>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess</artifactId>
            <version>${fess.version}</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.opensearch</groupId>
            <artifactId>opensearch</artifactId>
            <version>${opensearch.version}</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

La versión de ``fess-parent`` debe coincidir con la versión de Fess en la que se instalará el plugin.
En ``fess-parent`` 15.9.0, ``fess.version`` es ``15.9.0``, por lo que el plugin se compila contra la API de Fess 15.9.0.
El propio Fess y las clases de OpenSearch los proporciona Fess en tiempo de ejecución, por eso se declaran como ``provided``.
El ``pom.xml`` real contiene además otras dependencias y ajustes de compilación; para empezar, úselo tal cual.
El jar de ``fess`` no se descarga de Maven Central, sino del repositorio de CodeLibs que declara ``fess-parent`` (``https://maven.codelibs.org/release/``).
En entornos que usan un proxy o un mirror, asegúrese de que este repositorio sea accesible.

Cuando lo convierta en su propio plugin, haga que el ``artifactId`` empiece siempre por ``fess-ds-``.
Como se explica más adelante, las opciones de «Nombre del manejador» de la consola de administración solo se obtienen de los jar cuyo nombre de archivo empieza por ``fess-ds``.

Clase del almacén de datos
--------------------------

Un almacén de datos hereda de ``org.codelibs.fess.ds.AbstractDataStore`` e implementa ``getName()`` y ``storeData(...)``.
A continuación se muestra ``ExampleDataStore`` reducido al esqueleto de su procesamiento.
Sirve para entender el funcionamiento; para compilar, use tal cual el ``ExampleDataStore`` del repositorio (las pruebas usan métodos que no están en el esqueleto, así que, si sustituye la clase, la compilación de las pruebas falla).

.. code-block:: java

    package org.codelibs.fess.ds.example;

    import java.util.HashMap;
    import java.util.LinkedHashMap;
    import java.util.Map;

    import org.codelibs.fess.ds.AbstractDataStore;
    import org.codelibs.fess.ds.callback.IndexUpdateCallback;
    import org.codelibs.fess.entity.DataStoreParams;
    import org.codelibs.fess.opensearch.config.exentity.DataConfig;

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        protected String getName() {
            return this.getClass().getSimpleName();
        }

        @Override
        protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback, final DataStoreParams paramMap,
                final Map<String, String> scriptMap, final Map<String, Object> defaultDataMap) {
            final String scriptType = getScriptType(paramMap);
            final int dataSize = Integer.parseInt(paramMap.getAsString("data.size", "10"));

            for (int i = 0; i < dataSize && alive; i++) {
                // Un registro obtenido del sistema externo (aquí, valores fijos)
                final Map<String, Object> source = new HashMap<>();
                source.put("title", "Sample " + i);
                source.put("body", "Sample body text for record " + i);
                source.put("url", "http://fess.codelibs.org/?sample=" + i);

                // Los scripts se evalúan sobre «parámetros + registro»
                final Map<String, Object> resultMap = new LinkedHashMap<>(paramMap.asMap());
                resultMap.putAll(source);

                final Map<String, Object> dataMap = new HashMap<>(defaultDataMap);
                for (final Map.Entry<String, String> entry : scriptMap.entrySet()) {
                    final Object value = convertValue(scriptType, entry.getValue(), resultMap);
                    if (value != null) {
                        dataMap.put(entry.getKey(), value);
                    }
                }
                callback.store(paramMap, dataMap);
            }
        }
    }

La función de cada parte es la siguiente.

- El valor devuelto por ``getName()`` se registra en ``DataStoreFactory`` como nombre de este almacén de datos. Por convención, devuelve el nombre simple de la clase
- ``paramMap`` contiene los valores del campo «Parámetro» de la configuración del almacén de datos. Se leen con ``getAsString(clave, valorPredeterminado)``
- ``scriptMap`` contiene las líneas del campo «Script», con la forma ``nombreDeCampo=expresión``. ``convertValue()`` evalúa la expresión y el resultado se guarda en el campo correspondiente del índice
- ``defaultDataMap`` contiene valores que determina la configuración del almacén de datos, como el ID de configuración, los permisos (roles), el valor de boost y los hosts virtuales. Cópielo primero y después añada cada campo
- ``callback.store()`` indexa los registros de uno en uno. ``alive`` pasa a ser ``false`` cuando se detiene el trabajo, así que inclúyalo en la condición del bucle

Es decir, el plugin no decide qué valor de un registro va a qué campo: eso lo decide el administrador en el campo «Script».
La tarea del plugin es obtener los registros y disponerlos en ``resultMap``.

El ``ExampleDataStore`` real implementa además el manejo de excepciones por registro (registro en [URL de fallo]) y las estadísticas de rastreo (``CrawlerStatsHelper``).
Cuando cree su propio plugin, copie ``ExampleDataStore`` en lugar de este esqueleto y reescriba los puntos marcados con ``// CUSTOMIZE:`` (la parte que obtiene los registros).

Archivo de configuración de DI
------------------------------

Crear la clase no basta para que Fess la cargue.
Regístrela como componente en ``src/main/resources/fess_ds++.xml``.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

El contenedor de DI (Lasta Di) incorpora cualquier ``fess_ds++.xml`` del classpath al ``fess_ds.xml`` del propio Fess.
Gracias a ``<postConstruct name="register">``, se llama a ``AbstractDataStore.register()`` después de crear el componente, y el almacén de datos se registra con el nombre que devuelve ``getName()``.
Si cambia el nombre de la clase o el paquete, cambie también el atributo ``class``.

Compilar
--------

::

    $ mvn clean package

Se generan tres jar en ``target/``.
El que se instala en Fess es ``fess-ds-example-15.9.0-SNAPSHOT.jar``, el que no lleva ``-sources`` ni ``-javadoc``.
Puede comprobar con ``unzip -l`` que contiene ``fess_ds++.xml`` y ``ExampleDataStore.class``.

Instalar
========

Lo más sencillo es instalarlo desde la consola de administración.

1. En [Sistema] > [Plugin], haga clic en [Instalar]
2. Deje la lista desplegable de la pestaña [Remoto] en la primera opción, ``-``. Si hay otro plugin seleccionado, se instalará ese en su lugar
3. En la pestaña [Local], seleccione el jar compilado en «Archivo Jar» y haga clic en [Instalar]
4. Reinicie Fess

El jar subido se guarda en ``app/WEB-INF/plugin/`` con la forma ``<nombre>-<versión>.jar``.
El nombre y la versión se leen del nombre del archivo, así que suba el jar sin cambiar el nombre que le asignó Maven.
En lugar de usar la consola de administración, también puede copiar el jar directamente en este directorio y reiniciar (``/usr/share/fess/app/WEB-INF/plugin/`` en la imagen de Docker).

Con Docker, ``FESS_PLUGINS`` descarga plugins publicados en un repositorio, por lo que no sirve para un jar propio.
Instálelo desde la consola de administración y reinicie con ``docker compose -f compose.yaml -f compose-opensearch3.yaml restart fess01``.
El jar se guarda dentro del contenedor, así que desaparece si vuelve a crear el contenedor con ``down`` y ``up``.
En ese caso, instálelo de nuevo.

Comprobar el funcionamiento
===========================

Comprobar el nombre del manejador
---------------------------------

Tras el reinicio, abra [Rastreador] > [Almacén de datos] > [Crear nuevo] y compruebe que ``ExampleDataStore`` aparece en la lista desplegable «Nombre del manejador».
Las opciones se generan a partir de los jar de ``app/WEB-INF/plugin/`` cuyo nombre de archivo empieza por ``fess-ds``.
Fess lee el ``fess_ds++.xml`` del jar y usa como opción el nombre simple de la clase indicada en el atributo ``class`` (se guarda en caché durante 60 segundos).
Si no aparece, compruebe el nombre del archivo jar, el ``fess_ds++.xml`` del jar y que haya reiniciado.

Crear la configuración del almacén de datos
-------------------------------------------

En la misma pantalla, introduzca lo siguiente y haga clic en [Crear].

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Campo
     - Valor
   * - Nombre
     - ``Example``
   * - Nombre del manejador
     - ``ExampleDataStore``
   * - Parámetro
     - Añadir ``data.size=5`` en la línea siguiente a ``script_type=javascript``, que ya viene escrito
   * - Script
     - Tres líneas: ``title=title``, ``content=body`` y ``url=url``

Cuando el lado derecho de una línea del script coincide con una clave del registro (``title``, ``body``, ``url``), ``convertValue()`` devuelve ese valor tal cual sin usar un motor de scripts.
Si escribe una expresión como ``content=title + " " + body``, se evalúa con el motor indicado en ``script_type``.
Si elimina ``script_type``, el script se trata como ``groovy`` y la evaluación de expresiones falla en entornos sin ``fess-script-groovy``, así que no lo elimine.

``url`` es obligatorio.
``callback.store()`` no acepta documentos sin ``url`` y lanza una excepción.

Ejecutar el trabajo
-------------------

1. En la lista de [Rastreador] > [Almacén de datos], haga clic en ``Example`` y después en [Crear nuevo trabajo]
2. Se abre la pantalla de creación del programador; haga clic en [Crear] sin cambiar nada
3. En [Sistema] > [Programador], abra el trabajo creado y haga clic en [Iniciar ahora]

Comprobar los resultados
------------------------

Compruebe los cuatro puntos siguientes.

1. En [Información del sistema] > [Registro de trabajo], el estado del trabajo es «OK»
2. En [Información del sistema] > [Información de rastreo], el «Tamaño del índice (Almacén de datos)» de esa sesión es ``5``
3. No hay nada registrado en [Información del sistema] > [URL de fallo]
4. Al buscar ``Sample`` en [Información del sistema] > [Búsqueda] aparecen cinco resultados, de ``Sample 0`` a ``Sample 4``

Que el estado del trabajo sea «OK» no garantiza que el procesamiento del almacén de datos haya tenido éxito.
Por ejemplo, si elimina ``url=url`` del script y ejecuta el trabajo, ``callback.store()`` lanza una excepción en todos los registros y no se indexa nada.
``ExampleDataStore`` captura las excepciones registro por registro, de modo que en [URL de fallo] se registran de ``record:0`` a ``record:4`` y aparecen mensajes WARN en ``fess-crawler.log``, pero el registro de trabajos sigue mostrando «OK».
Con un código que no captura excepciones, como el esqueleto, falla toda la configuración y en [URL de fallo] se registra una sola entrada con la forma ``D<IDdeConfiguración>:Example``.
Los pasos de comprobación y la ubicación de los registros se resumen en la sección sobre la comprobación de resultados de :doc:`datastore-basics`.

Una vez comprobado todo esto, sustituya la parte que obtiene los registros, como ``createSourceRecord()``, por código que lea su API o sus archivos reales.
No escriba en el código el destino de conexión ni las credenciales del sistema externo; recíbalos a través de ``paramMap`` desde el campo «Parámetro».

El ``src/test`` de la plantilla contiene pruebas que usan ``LastaDiTestCase`` de UTFlute.
Una clase de prueba que implementa ``IndexUpdateCallback`` recoge los ``dataMap`` pasados a ``store()``, y las pruebas comprueban su número y los valores de los campos.
Por eso puede ejecutar ``mvn test`` sin OpenSearch.
Cuando reescriba la parte que obtiene los registros, adapte también estas pruebas.

Procesar documentos antes de indexarlos con un Ingester
=======================================================

Un Ingester se llama justo antes de enviar un documento al índice en cualquier tipo de rastreo: almacén de datos, web o sistema de archivos.
Se usa, por ejemplo, para añadir un campo común a todos los documentos o para normalizar valores.
No hay forma de activarlo o desactivarlo por configuración: una vez instalado, se aplica a todos los rastreos.

Herede de ``org.codelibs.fess.ingest.Ingester`` y sobrescriba solo los métodos ``process`` que necesite.

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Método
     - Cuándo se llama
   * - ``process(Map<String, Object> target, DataStoreParams params)``
     - En el rastreo de almacenes de datos (dentro de ``callback.store()``)
   * - ``process(Map<String, Object> target, AccessResult<String> accessResult)``
     - Al indexar en los rastreos web y de archivos
   * - ``process(ResultData target, ResponseData responseData)``
     - Al procesar la respuesta obtenida en los rastreos web y de archivos
   * - ``protected process(Map<String, Object> target)``
     - Método al que llaman por defecto las dos versiones ``Map`` anteriores. Sobrescriba solo este cuando quiera que el procesamiento se aplique tanto a los almacenes de datos como a los rastreos web y de archivos

A continuación se muestra ``ExampleIngester`` de ``fess-ingest-example``, reducido al procesamiento para almacenes de datos.

.. code-block:: java

    package org.codelibs.fess.ingest.example;

    import java.util.Map;

    import org.apache.logging.log4j.LogManager;
    import org.apache.logging.log4j.Logger;
    import org.codelibs.fess.entity.DataStoreParams;
    import org.codelibs.fess.ingest.Ingester;

    public class ExampleIngester extends Ingester {
        private static final Logger logger = LogManager.getLogger(ExampleIngester.class);

        public ExampleIngester() {
            setPriority(50);
        }

        @Override
        public Map<String, Object> process(final Map<String, Object> target, final DataStoreParams params) {
            target.put("ingested_by", ExampleIngester.class.getSimpleName());
            logger.info("DATASTORE CRAWL: {}", target);
            return target;
        }
    }

El registro se hace en ``src/main/resources/fess_ingest++.xml``.
Tiene la misma forma que ``fess_ds++.xml``: un componente llamado ``exampleIngester`` con ``<postConstruct name="register">``.
``Ingester.register()`` añade el propio Ingester a ``IngestFactory``.

La obtención de la plantilla, la compilación, la instalación y el reinicio siguen los mismos pasos que para el almacén de datos (el commit para 15.9 es ``8a1e45ddb63a118802287120effd3ce49fb60bfb`` y el jar es ``fess-ingest-example-15.9.0-SNAPSHOT.jar``).
En su propio plugin, haga que el artifactId empiece por ``fess-ingest-``.

Tenga en cuenta lo siguiente al implementarlo.

- Devuelva siempre ``target`` después de modificarlo. El valor devuelto se pasa tal cual al siguiente Ingester y al indexador, sin comprobar si es ``null``. Devolver ``null`` no excluye el documento, sino que rompe el proceso de indexación
- Si hay varios Ingesters, se ejecutan en orden ascendente de ``priority`` (valor predeterminado: 99). Cada Ingester recibe el ``target`` modificado por el anterior
- Si ``process`` lanza una excepción, Fess registra un WARN y pasa al siguiente Ingester. La indexación del documento no se detiene. Los cambios hechos en ``target`` antes de la excepción se conservan

Para comprobarlo, vuelva a ejecutar el trabajo de la configuración de almacén de datos creada en «Comprobar el funcionamiento».
Los Ingesters se ejecutan en el proceso del rastreador, así que, si ``fess-crawler.log`` contiene una línea ``DATASTORE CRAWL:`` por cada documento, el Ingester se está llamando.
El ``ExampleIngester`` del repositorio también registra uno a uno los documentos de los rastreos web y de archivos como ``WEB/FILE CRAWL:``.
Como afecta a todos los rastreos, elimínelo en [Sistema] > [Plugin] cuando termine la comprobación y reinicie Fess.

Actualizar Fess
===============

Compile el plugin con el ``fess-parent`` de la misma versión menor que el Fess en el que se instala (15.9.x para Fess 15.9).
Los plugins publicados también se lanzan en una versión correspondiente para cada versión menor de Fess.

Al actualizar Fess a 15.10, ajuste la versión de ``fess-parent`` en ``pom.xml`` y vuelva a compilar.
En la lista de [Sistema] > [Plugin], elimine el jar antiguo, instale el nuevo y reinicie.
``bin/fess-setup upgrade plugins`` descarga las versiones nuevas del repositorio de plugins, por lo que no puede actualizar plugins propios que no estén en ese repositorio.

Siguientes lecturas
===================

- Para saber más sobre parámetros, scripts, permisos y programación de almacenes de datos: :doc:`datastore-basics`
- Para ver ejemplos de configuración de plugins de almacén de datos publicados: :doc:`guide-06`, :doc:`guide-07` y :doc:`guide-12`
- Para cambiar el aspecto de la página de búsqueda: :doc:`guide-03`
- Para activar el modo de búsqueda con IA mediante un plugin de LLM: :doc:`guide-19`
- Para usar un plugin de aplicación web (servidor MCP): :doc:`guide-20`

Referencias
===========

- `Arquitectura de Plugins <https://fess.codelibs.org/es/stable/dev/plugin-architecture.html>`__
- `Desarrollo de Plugins de Almacén de Datos <https://fess.codelibs.org/es/stable/dev/datastore-plugin.html>`__
- `Plugin Ingest <https://fess.codelibs.org/es/stable/dev/ingest-plugin.html>`__
- `Guía de Desarrollo de Temas <https://fess.codelibs.org/es/stable/dev/theme-development.html>`__
- `Complemento (consola de administración) <https://fess.codelibs.org/es/stable/admin/plugin-guide.html>`__
- `fess-ds-example (GitHub) <https://github.com/codelibs/fess-ds-example>`__
- `fess-ingest-example (GitHub) <https://github.com/codelibs/fess-ingest-example>`__
