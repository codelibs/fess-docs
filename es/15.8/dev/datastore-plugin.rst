=========================================
Desarrollo de Plugins de Almacén de Datos
=========================================

Visión General
==============

Al desarrollar un plugin de almacén de datos, puede agregar a |Fess| la
funcionalidad de obtener contenido desde nuevas fuentes de datos. El almacén
de datos obtiene registros de sistemas externos, como bases de datos, API o
archivos, los convierte en campos de índice de acuerdo con el script de
mapeo configurado en la consola de administración, y los registra en el
índice de |Fess|.

Todos los conectores públicos (``fess-ds-*``), como CSV, JSON, bases de
datos, Git y diversos servicios en la nube, están implementados con este
mecanismo. Como plantilla de implementación se publica
`fess-ds-example <https://github.com/codelibs/fess-ds-example>`__, por lo
que, al crear un nuevo conector, resulta sencillo comenzar copiando este
proyecto.

Estructura Básica
==================

El plugin de almacén de datos se compone de los siguientes tres elementos:

- Crear una clase que herede de ``AbstractDataStore``
- Implementar los dos métodos ``getName()`` y ``storeData()``
- Registrarla como componente en ``fess_ds++.xml``

Implementación Mínima
---------------------

.. code-block:: java

    package org.codelibs.fess.ds.example;

    import java.util.Map;

    import org.codelibs.fess.ds.AbstractDataStore;
    import org.codelibs.fess.ds.callback.IndexUpdateCallback;
    import org.codelibs.fess.entity.DataStoreParams;
    import org.codelibs.fess.opensearch.config.exentity.DataConfig;

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

            // Implementar aquí la obtención y el procesamiento de los datos
        }
    }

.. note::

   Tanto ``getName()`` como ``storeData()`` son métodos abstractos
   ``protected``. Tenga en cuenta que, en |Fess| 15.x, el paquete de
   ``DataConfig`` es ``org.codelibs.fess.opensearch.config.exentity`` (el
   anterior ``org.codelibs.fess.es.config.exentity`` ha quedado obsoleto).

Registro del Componente
-----------------------

Para que |Fess| reconozca el almacén de datos creado, registre el
componente en ``src/main/resources/fess_ds++.xml``.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

Mediante ``<postConstruct name="register">``, tras la creación del
componente se invoca automáticamente el método ``register()`` que posee
``AbstractDataStore``, y este se registra a sí mismo en
``DataStoreFactory``. El nombre registrado en este momento es el valor
devuelto por ``getName()`` (``ExampleDataStore`` en el ejemplo anterior), y
es el que se selecciona como «nombre del manejador» en la configuración del
almacén de datos de la consola de administración.

AbstractDataStore
=================

Métodos Principales
--------------------

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - Método
     - Categoría
     - Descripción
   * - ``getName()``
     - Implementación (obligatoria)
     - Método abstracto que devuelve el nombre del manejador del almacén de
       datos. La convención es devolver ``getClass().getSimpleName()``
   * - ``storeData()``
     - Implementación (obligatoria)
     - Método abstracto que obtiene, convierte y registra los datos en el
       índice
   * - ``register()``
     - Heredado (normalmente no requiere cambios)
     - Se invoca automáticamente desde el ``postConstruct`` de
       ``fess_ds++.xml`` y se registra en ``DataStoreFactory``
   * - ``store()``
     - Heredado (invocado por el framework)
     - Punto de entrada invocado por el framework. Prepara
       ``defaultDataMap`` y otros datos, y llama a ``storeData()``
   * - ``convertValue()``
     - Heredado (auxiliar)
     - Evalúa con el motor de scripts el valor (plantilla) de ``scriptMap``
   * - ``getScriptType()``
     - Heredado (auxiliar)
     - Obtiene el parámetro ``script_type`` (el valor predeterminado es
       Groovy)
   * - ``getReadInterval()``
     - Heredado (auxiliar)
     - Obtiene el parámetro ``readInterval`` (en milisegundos)
   * - ``sleep()``
     - Heredado (auxiliar)
     - Duerme durante los milisegundos indicados (se utiliza para esperar
       entre registros)

Parámetros de storeData
-----------------------

Parámetros que se pasan al método ``storeData()``:

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Parámetro
     - Tipo
     - Descripción
   * - ``dataConfig``
     - ``DataConfig``
     - Configuración del almacén de datos (ID, nombre del manejador,
       parámetros, scripts, etc.)
   * - ``callback``
     - ``IndexUpdateCallback``
     - Callback para registrar en el índice los documentos generados
   * - ``paramMap``
     - ``DataStoreParams``
     - Valores configurados en el campo «Parámetros» de la consola de
       administración. Se accede a ellos mediante ``getAsString(key)``,
       ``getAsString(key, default)``, ``get(key)``, ``asMap()`` y
       ``containsKey(key)``
   * - ``scriptMap``
     - ``Map<String, String>``
     - Configuración del campo «Script» de la consola de administración.
       La clave es el nombre del campo de índice, y el valor es la
       plantilla de script que se evalúa
   * - ``defaultDataMap``
     - ``Map<String, Object>``
     - Valores predeterminados de campo para cada documento (ID de
       configuración, boost, role, mimetype, host virtual, etc.). El
       framework los prepara

.. warning::

   El tipo de ``paramMap`` no es ``Map<String, String>``, sino
   ``DataStoreParams``. Dado que ``DataStoreParams`` no implementa
   ``Map``, utilice ``getAsString()``, que devuelve una cadena, en lugar
   de ``get()`` para obtener los valores.

Flujo de Procesamiento de Datos
--------------------------------

La implementación de ``storeData()`` procesa los datos siguiendo este
flujo.

#. Obtener los registros de origen desde el sistema externo.
#. Combinar los campos del registro de origen con ``paramMap.asMap()``
   para construir ``resultMap`` (el script se evalúa sobre este
   ``resultMap``).
#. Evaluar cada entrada de ``scriptMap`` con
   ``convertValue(scriptType, template, resultMap)`` y almacenar el
   resultado en ``dataMap``. Es importante que el mapeo no se codifique de
   forma fija en el código, sino que lo defina el administrador en el
   campo «Script».
#. Invocar ``callback.store(paramMap, dataMap)`` para registrar el
   documento en el índice.

Ejemplo de Implementación
==========================

Almacén de Datos Simple
-----------------------

Ejemplo que obtiene registros desde una API externa y los registra en el
índice.

.. code-block:: java

    @Override
    protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback,
            final DataStoreParams paramMap, final Map<String, String> scriptMap,
            final Map<String, Object> defaultDataMap) {

        // Obtener los parámetros (en DataStoreParams se usa getAsString)
        final String apiUrl = paramMap.getAsString("api.url");
        final String apiKey = paramMap.getAsString("api.key");

        // Tipo de evaluación del script (el valor predeterminado es Groovy)
        final String scriptType = getScriptType(paramMap);
        // Tiempo de espera entre registros (milisegundos)
        final long readInterval = getReadInterval(paramMap);

        try {
            // Obtener los datos del sistema externo
            final List<Map<String, Object>> records = fetchRecords(apiUrl, apiKey);

            for (final Map<String, Object> record : records) {
                // Copiar los campos predeterminados para inicializar dataMap
                final Map<String, Object> dataMap = new HashMap<>(defaultDataMap);

                // Construir resultMap combinando los parámetros y el registro de origen
                // (el script se evalúa sobre este resultMap)
                final Map<String, Object> resultMap = new LinkedHashMap<>(paramMap.asMap());
                resultMap.putAll(record);

                // Evaluar cada entrada de scriptMap para generar los campos de índice
                for (final Map.Entry<String, String> entry : scriptMap.entrySet()) {
                    final Object value = convertValue(scriptType, entry.getValue(), resultMap);
                    if (value != null) {
                        dataMap.put(entry.getKey(), value);
                    }
                }

                // Registrar en el índice
                callback.store(paramMap, dataMap);

                if (readInterval > 0) {
                    sleep(readInterval);
                }
            }
        } catch (final Exception e) {
            throw new DataStoreException("Failed to crawl data from " + apiUrl, e);
        }
    }

``fetchRecords()`` es un método propio que obtiene la lista de registros
del sistema externo. Los nombres de los campos de cada registro obtenido
(``Map<String, Object>``) son los nombres que se pueden referenciar desde
los scripts de ``scriptMap``. ``DataStoreException`` es una clase del
paquete ``org.codelibs.fess.exception``.

Soporte de Paginación
----------------------

Cuando se manejan grandes volúmenes de datos, el procesamiento se realiza
obteniendo los registros página por página. Si se extrae el procesamiento
por registro (la construcción de ``resultMap``, la evaluación de
``scriptMap`` y la llamada a ``callback.store()``) a un método como
``processRecord()``, es posible separarlo de la lógica de obtención.

.. code-block:: java

    int offset = 0;
    final int pageSize = 100;

    while (true) {
        final List<Map<String, Object>> records = fetchRecords(apiUrl, apiKey, offset, pageSize);

        if (records.isEmpty()) {
            break;
        }

        for (final Map<String, Object> record : records) {
            processRecord(record, callback, paramMap, scriptMap, defaultDataMap);
        }

        offset += pageSize;
    }

Implementación de Autenticación
================================

La autenticación con el sistema externo se implementa en el lado del
conector. A continuación se muestra un ejemplo de implementación con una
biblioteca cliente HTTP habitual; no se trata de una API proporcionada por
|Fess|. Incluya la biblioteca que utilice como dependencia del plugin.

OAuth 2.0
---------

.. code-block:: java

    protected String getAccessToken(final String clientId, final String clientSecret, final String refreshToken) {
        // Ejemplo de obtención de un token de acceso mediante el token de actualización
        final OkHttpClient client = new OkHttpClient();

        final RequestBody body = new FormBody.Builder()
            .add("grant_type", "refresh_token")
            .add("client_id", clientId)
            .add("client_secret", clientSecret)
            .add("refresh_token", refreshToken)
            .build();

        final Request request = new Request.Builder()
            .url("https://oauth.example.com/token")
            .post(body)
            .build();

        try (Response response = client.newCall(request).execute()) {
            final JsonNode json = objectMapper.readTree(response.body().string());
            return json.get("access_token").asText();
        }
    }

Autenticación con Clave API
----------------------------

.. code-block:: java

    protected Response callApi(final String url, final String apiKey) {
        final Request request = new Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer " + apiKey)
            .build();

        return httpClient.newCall(request).execute();
    }

Manejo de Errores
=================

Para errores fatales que deben interrumpir el procesamiento, lance
``DataStoreException``.

.. code-block:: java

    @Override
    protected void storeData(...) {
        try {
            // Procesamiento
        } catch (final AuthenticationException e) {
            logger.error("Authentication failed. Check your credentials.", e);
            throw new DataStoreException("Authentication failed", e);
        } catch (final RateLimitException e) {
            logger.warn("Rate limit exceeded. Waiting...");
            sleep(60000L);
            // Lógica de reintento
        } catch (final Exception e) {
            logger.error("Unexpected error occurred", e);
            throw new DataStoreException("Failed to crawl data", e);
        }
    }

.. note::

   En conectores reales, como ``fess-ds-example``, para evitar que el
   error de un solo registro detenga todo el rastreo, se captura
   ``CrawlingAccessException`` a nivel de registro y se registra la URL
   con error en ``FailureUrlService``. Además, se controla si se debe
   interrumpir todo el rastreo mediante el indicador de interrupción de
   ``DataStoreCrawlingException``. Si desea implementar un conector
   robusto, consulte la implementación de ``ExampleDataStore``.

Pruebas
=======

Pruebas Unitarias
------------------

Los plugins de |Fess| se prueban utilizando ``LastaDiTestCase`` de
UTFlute. Las pruebas se escriben con JUnit 5 (Jupiter). Al sustituir
``IndexUpdateCallback`` por una implementación que recopila los
``dataMap`` registrados, es posible verificar el resultado del mapeo sin
utilizar bibliotecas de mocks.

.. code-block:: java

    public class ExampleDataStoreTest extends LastaDiTestCase {

        public ExampleDataStore dataStore;

        @Override
        protected String prepareConfigFile() {
            return "test_app.xml";
        }

        @Override
        public void setUp(final TestInfo testInfo) throws Exception {
            super.setUp(testInfo);
            dataStore = new ExampleDataStore();
        }

        @Test
        public void test_getName() {
            assertEquals("ExampleDataStore", dataStore.getName());
        }

        @Test
        public void test_storeData() {
            final TestIndexUpdateCallback callback = new TestIndexUpdateCallback();
            final DataStoreParams paramMap = new DataStoreParams();

            final Map<String, String> scriptMap = new HashMap<>();
            scriptMap.put("title", "title");

            dataStore.storeData(new DataConfig(), callback, paramMap, scriptMap, new HashMap<>());

            assertFalse(callback.getDataMapList().isEmpty());
        }

        // Callback de prueba que recopila los dataMap registrados
        private static class TestIndexUpdateCallback implements IndexUpdateCallback {
            private final List<Map<String, Object>> dataMapList = new ArrayList<>();

            @Override
            public void store(final DataStoreParams paramMap, final Map<String, Object> dataMap) {
                dataMapList.add(new HashMap<>(dataMap));
            }

            @Override
            public long getExecuteTime() {
                return 0;
            }

            @Override
            public long getDocumentSize() {
                return dataMapList.size();
            }

            @Override
            public void commit() {
                // No hace nada
            }

            public List<Map<String, Object>> getDataMapList() {
                return dataMapList;
            }
        }
    }

.. note::

   ``setUp`` ya tiene la anotación ``@BeforeEach`` en la clase base, por
   lo que no es necesario volver a añadir anotaciones de ciclo de vida al
   sobrescribirlo. Cada método de prueba debe llevar la anotación
   ``@Test`` (``org.junit.jupiter.api.Test``).

Construcción e Instalación
===========================

pom.xml
-------

El plugin se construye como un jar que utiliza ``fess-parent`` como POM
padre. Las dependencias de ``fess`` y ``opensearch`` se marcan como
``provided``, ya que en tiempo de ejecución las proporciona el propio
|Fess|.

.. code-block:: xml

    <project xmlns="http://maven.apache.org/POM/4.0.0" ...>
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

Para las pruebas se utilizan JUnit 5 y
``org.dbflute.utflute:utflute-lastaflute``.

Construcción
------------

.. code-block:: bash

    mvn clean package

Se generará ``fess-ds-example-15.8.0.jar`` en el directorio ``target/``.

Instalación
-----------

Instale el JAR generado en |Fess| y reinicie |Fess|. Para más detalles
sobre el procedimiento de instalación, consulte
:doc:`../admin/plugin-guide`. Después de la instalación, cree una nueva
configuración desde «Rastreador > Almacén de Datos» en la consola de
administración y especifique en «Nombre del manejador» el nombre que
devuelve ``getName()`` (``ExampleDataStore`` en este ejemplo).

Ejemplo de Configuración
========================

Ejemplo de configuración en la consola de administración:

Parámetros
----------

En el campo «Parámetros» se describen las claves y los valores que el
conector lee desde ``paramMap``.

::

    api.url=https://api.example.com/v1
    api.key=your_api_key

Script
------

En el campo «Script» se describe el mapeo con el formato
``lado izquierdo=lado derecho``. El lado izquierdo es el nombre del campo
de índice, y el lado derecho es un script (Groovy de forma predeterminada)
que referencia un campo del registro de origen. A continuación se muestra
un ejemplo para el caso en que el registro de origen tiene los campos
``url``, ``title``, ``content``, ``updated_at`` y ``content_type``.

::

    url=url
    title=title
    content=content
    last_modified=updated_at
    mimetype=content_type

.. note::

   Los nombres de campo que se pueden referenciar en el lado derecho
   dependen de los valores que el conector almacena en ``resultMap`` (los
   valores de ``paramMap`` y los campos del registro de origen). En
   conectores existentes, como CSV o JSON, puede añadirse un prefijo
   propio como ``data.*``, por lo que debe consultar la documentación de
   cada conector.

Información de Referencia
==========================

- :doc:`plugin-architecture` - Arquitectura de plugins
- :doc:`../admin/plugin-guide` - Instalación de plugins
- :doc:`../config/datastore/ds-overview` - Descripción general de los
  conectores de almacén de datos
- `fess-ds-example <https://github.com/codelibs/fess-ds-example>`__ -
  Plantilla de implementación de plugins de almacén de datos
- `GitHub: fess-ds-* <https://github.com/codelibs?q=fess-ds>`__ - Ejemplos
  de conectores públicos
