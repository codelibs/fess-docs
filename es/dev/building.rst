==============
Construcción y Pruebas
==============

Esta página explica cómo construir |Fess|, métodos de prueba,
y cómo crear paquetes de distribución.

.. contents:: Índice
   :local:
   :depth: 2

Visión General del Sistema de Construcción
==================

|Fess| usa Maven como herramienta de construcción.
Maven automatiza la gestión de dependencias, compilación, pruebas y empaquetado.

pom.xml
-------

Este es el archivo de configuración de Maven. Se encuentra en el directorio raíz del proyecto.

Contenido de configuración principal:

- Información del proyecto (groupId, artifactId, version)
- Bibliotecas de dependencias
- Plugins de construcción
- Perfiles

Comandos Básicos de Construcción
==================

Construcción Limpia
------------

Elimina artefactos de construcción y luego reconstruye:

.. code-block:: bash

    mvn clean compile

Creación de Paquetes
--------------

Crea un archivo WAR y un paquete zip de distribución:

.. code-block:: bash

    mvn package

Los artefactos se generan en el directorio ``target/``:

.. code-block:: text

    target/
    ├── fess.war
    └── releases/
        └── fess-{version}.zip

Construcción Completa
--------

Ejecuta limpieza, compilación, pruebas y empaquetado:

.. code-block:: bash

    mvn clean package

Descarga de Dependencias
--------------------

Descarga bibliotecas de dependencias:

.. code-block:: bash

    mvn dependency:resolve

Descarga de Plugins de OpenSearch
---------------------------------

Descarga OpenSearch y plugins obligatorios:

.. code-block:: bash

    mvn antrun:run

.. note::

   Ejecute este comando al configurar el entorno de desarrollo
   o al actualizar plugins.

Pruebas
====

|Fess| implementa pruebas usando JUnit.

Ejecución de Pruebas Unitarias
--------------

Ejecutar Todas las Pruebas Unitarias
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test

Ejecutar Clase de Prueba Específica
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest

Ejecutar Método de Prueba Específico
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest#testSearch

Ejecutar Múltiples Clases de Prueba
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest,CrawlerTest

Omitir Pruebas
--------------

Para construir omitiendo pruebas:

.. code-block:: bash

    mvn package -DskipTests

.. warning::

   Durante el desarrollo, no omita las pruebas, ejecútelas siempre.
   Antes de crear un PR, verifique que todas las pruebas pasen.

Ejecución de Pruebas de Integración
--------------

Las pruebas de integración requieren el perfil ``integrationTests``.
Se necesita un servidor |Fess| y OpenSearch en ejecución:

.. code-block:: bash

    mvn test -P integrationTests \
        -Dtest.fess.url="http://localhost:8080" \
        -Dtest.search_engine.url="http://localhost:9201"

.. note::

   Las clases de pruebas de integración usan el patrón ``*Tests.java`` (las unitarias usan ``*Test.java``).

Cómo Escribir Pruebas
============

Creación de Pruebas Unitarias
--------------

Ubicación de Clases de Prueba
~~~~~~~~~~~~~~~~

Coloque las clases de prueba bajo ``src/test/java/``.
La estructura de paquetes debe ser la misma que el código principal.

.. code-block:: text

    src/
    ├── main/java/org/codelibs/fess/app/service/SearchService.java
    └── test/java/org/codelibs/fess/app/service/SearchServiceTest.java

Estructura Básica de Clase de Prueba
~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

    package org.codelibs.fess.app.service;

    import org.junit.jupiter.api.Test;
    import static org.junit.jupiter.api.Assertions.*;

    public class SearchServiceTest {

        @Test
        public void testSearch() {
            // Given: Condiciones previas de la prueba
            SearchService service = new SearchService();
            String query = "test";

            // When: Ejecución del objetivo de prueba
            SearchResponse response = service.search(query);

            // Then: Verificación de resultados
            assertNotNull(response);
            assertTrue(response.getResultCount() > 0);
        }
    }

Ciclo de Vida de las Pruebas
~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

    import org.junit.jupiter.api.*;

    public class MyServiceTest {

        @BeforeAll
        static void setUpClass() {
            // Ejecutar una vez antes de todas las pruebas
        }

        @BeforeEach
        void setUp() {
            // Ejecutar antes de cada prueba
        }

        @Test
        void testSomething() {
            // Prueba
        }

        @AfterEach
        void tearDown() {
            // Ejecutar después de cada prueba
        }

        @AfterAll
        static void tearDownClass() {
            // Ejecutar una vez después de todas las pruebas
        }
    }

Aserciones
~~~~~~~~~~

Use aserciones de JUnit 5:

.. code-block:: java

    import static org.junit.jupiter.api.Assertions.*;

    // Igualdad
    assertEquals(expected, actual);
    assertNotEquals(unexpected, actual);

    // Verificación de null
    assertNull(obj);
    assertNotNull(obj);

    // Valores booleanos
    assertTrue(condition);
    assertFalse(condition);

    // Excepciones
    assertThrows(IllegalArgumentException.class, () -> {
        service.doSomething();
    });

    // Colecciones
    assertIterableEquals(expectedList, actualList);

Cobertura de Pruebas
--------------

Mida la cobertura de pruebas con JaCoCo:

.. code-block:: bash

    mvn clean test jacoco:report

El informe se genera en ``target/site/jacoco/index.html``.

Formateo de Código
================

|Fess| utiliza las siguientes herramientas para mantener la calidad del código.

Formateador de Código
------------------

Unificar el estilo de codificación:

.. code-block:: bash

    mvn formatter:format

Encabezados de Licencia
----------------

Agregar encabezados de licencia a los archivos fuente:

.. code-block:: bash

    mvn license:format

Verificaciones Previas al Commit
------------------

Ejecute ambos antes de hacer commit:

.. code-block:: bash

    mvn formatter:format
    mvn license:format

Creación de Paquetes de Distribución
==================

Creación de Paquetes Zip
------------------

Cree un paquete zip para distribución:

.. code-block:: bash

    mvn clean package

Artefactos generados:

.. code-block:: text

    target/releases/
    └── fess-{version}.zip

Creación de Paquetes RPM
------------------

.. code-block:: bash

    mvn rpm:rpm

Creación de Paquetes DEB
------------------

.. code-block:: bash

    mvn jdeb:jdeb

Perfiles
==========

Los perfiles de Maven permiten cambiar entre tipos de prueba.

build (predeterminado)
-----------------

El perfil predeterminado. Ejecuta pruebas unitarias (``*Test.java``):

.. code-block:: bash

    mvn package

integrationTests
----------------

Perfil para ejecutar pruebas de integración (``*Tests.java``):

.. code-block:: bash

    mvn test -P integrationTests \
        -Dtest.fess.url="http://localhost:8080" \
        -Dtest.search_engine.url="http://localhost:9201"

CI/CD
=====

|Fess| usa GitHub Actions para ejecutar CI/CD.

GitHub Actions
-------------

Los archivos de configuración están en el directorio ``.github/workflows/``.

Verificaciones ejecutadas automáticamente:

- Construcción
- Pruebas unitarias
- Creación de paquetes

Verificación de CI Local
-----------------------

Antes de crear un PR, puede ejecutar las mismas verificaciones que CI localmente:

.. code-block:: bash

    mvn clean package

Solución de Problemas
====================

Errores de Construcción
----------

**Error: Falla en descarga de dependencias**

.. code-block:: bash

    # Limpiar repositorio local de Maven
    rm -rf ~/.m2/repository
    mvn clean compile

**Error: Memoria insuficiente**

.. code-block:: bash

    # Aumentar memoria de Maven
    export MAVEN_OPTS="-Xmx2g"
    mvn clean package

**Error: Versión antigua de Java**

Use Java 21 o posterior:

.. code-block:: bash

    java -version

Errores de Prueba
----------

**Las pruebas agotan el tiempo de espera**

Extender tiempo de espera de pruebas:

.. code-block:: bash

    mvn test -Dmaven.test.timeout=600

**OpenSearch no se inicia**

Verifique el puerto y cámbielo si está en uso:

.. code-block:: bash

    lsof -i :9201

Problemas de Dependencias
------------

**Conflictos de dependencias**

Verifique árbol de dependencias:

.. code-block:: bash

    mvn dependency:tree

Excluir dependencia específica:

.. code-block:: xml

    <dependency>
        <groupId>org.example</groupId>
        <artifactId>example-lib</artifactId>
        <version>1.0</version>
        <exclusions>
            <exclusion>
                <groupId>conflicting-lib</groupId>
                <artifactId>conflicting-lib</artifactId>
            </exclusion>
        </exclusions>
    </dependency>

Mejores Prácticas de Construcción
========================

Construcción Limpia Regular
--------------------

Ejecute construcción limpia regularmente para evitar problemas de caché de construcción:

.. code-block:: bash

    mvn clean package

Ejecución de Pruebas
----------

Ejecute siempre las pruebas antes de hacer commit:

.. code-block:: bash

    mvn test

Formateo de Código
------------------

Ejecute el formateo de código antes de crear un PR:

.. code-block:: bash

    mvn formatter:format
    mvn license:format

Actualización de Dependencias
------------

Actualice las dependencias regularmente:

.. code-block:: bash

    mvn versions:display-dependency-updates

Uso de Caché de Construcción
--------------------

Use caché de Maven para reducir tiempo de construcción:

.. code-block:: bash

    # Omitir si ya está compilado
    mvn compile

Referencia de Comandos Maven
========================

Comandos Comúnmente Usados
--------------

.. code-block:: bash

    # Limpiar
    mvn clean

    # Compilar
    mvn compile

    # Probar
    mvn test

    # Empaquetar
    mvn package

    # Instalar (registrar en repositorio local)
    mvn install

    # Verificar (incluye pruebas de integración)
    mvn verify

    # Resolver dependencias
    mvn dependency:resolve

    # Mostrar árbol de dependencias
    mvn dependency:tree

    # Mostrar información del proyecto
    mvn help:effective-pom

    # Formateo de código
    mvn formatter:format

    # Agregar encabezados de licencia
    mvn license:format

Próximos Pasos
==========

Una vez que comprenda los métodos de construcción y prueba, consulte los siguientes documentos:

- :doc:`workflow` - Flujo de trabajo de desarrollo
- :doc:`contributing` - Directrices de contribución
- :doc:`architecture` - Comprensión del código base

Materiales de Referencia
======

- `Documentación Oficial de Maven <https://maven.apache.org/guides/>`__
- `Guía del Usuario de JUnit 5 <https://junit.org/junit5/docs/current/user-guide/>`__
- `Documentación de JaCoCo <https://www.jacoco.org/jacoco/trunk/doc/>`__
