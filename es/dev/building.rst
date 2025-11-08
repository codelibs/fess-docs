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

Crea un archivo JAR ejecutable:

.. code-block:: bash

    mvn package

Los artefactos se generan en el directorio ``target/``:

.. code-block:: text

    target/
    ├── fess-15.3.x.jar
    └── fess-15.3.x/

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

Ejecuta todas las pruebas incluyendo pruebas de integración:

.. code-block:: bash

    mvn verify

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

Uso de Mocks
~~~~~~~~~~

Cree mocks usando Mockito:

.. code-block:: java

    import static org.mockito.Mockito.*;
    import org.mockito.Mock;
    import org.mockito.junit.jupiter.MockitoExtension;
    import org.junit.jupiter.api.extension.ExtendWith;

    @ExtendWith(MockitoExtension.class)
    public class SearchServiceTest {

        @Mock
        private SearchEngineClient searchEngineClient;

        @Test
        public void testSearch() {
            // Configurar mock
            when(searchEngineClient.search(anyString()))
                .thenReturn(new SearchResponse());

            // Ejecutar prueba
            SearchService service = new SearchService();
            service.setSearchEngineClient(searchEngineClient);
            SearchResponse response = service.search("test");

            // Verificación
            assertNotNull(response);
            verify(searchEngineClient, times(1)).search("test");
        }
    }

Cobertura de Pruebas
--------------

Mida la cobertura de pruebas con JaCoCo:

.. code-block:: bash

    mvn clean test jacoco:report

El informe se genera en ``target/site/jacoco/index.html``.

Verificación de Calidad del Código
================

Checkstyle
----------

Verifica el estilo de codificación:

.. code-block:: bash

    mvn checkstyle:check

El archivo de configuración está en ``checkstyle.xml``.

SpotBugs
--------

Detecta errores potenciales:

.. code-block:: bash

    mvn spotbugs:check

PMD
---

Detecta problemas de calidad del código:

.. code-block:: bash

    mvn pmd:check

Ejecutar Todas las Verificaciones
--------------------

.. code-block:: bash

    mvn clean verify checkstyle:check spotbugs:check pmd:check

Creación de Paquetes de Distribución
==================

Creación de Paquetes de Lanzamiento
--------------------

Cree paquetes para distribución:

.. code-block:: bash

    mvn clean package

Artefactos generados:

.. code-block:: text

    target/releases/
    ├── fess-15.3.x.tar.gz      # Para Linux/macOS
    ├── fess-15.3.x.zip         # Para Windows
    ├── fess-15.3.x.rpm         # Paquete RPM
    └── fess-15.3.x.deb         # Paquete DEB

Creación de Imagen Docker
-------------------

Cree imagen Docker:

.. code-block:: bash

    mvn package docker:build

Imagen generada:

.. code-block:: bash

    docker images | grep fess

Perfiles
==========

Puede aplicar configuraciones diferentes para cada entorno usando perfiles de Maven.

Perfil de Desarrollo
--------------

Construya con configuración de desarrollo:

.. code-block:: bash

    mvn package -Pdev

Perfil de Producción
--------------

Construya con configuración de producción:

.. code-block:: bash

    mvn package -Pprod

Construcción Rápida
--------

Construya rápidamente omitiendo pruebas y verificaciones:

.. code-block:: bash

    mvn package -Pfast

.. warning::

   La construcción rápida es para verificación durante el desarrollo.
   Antes de crear un PR, ejecute siempre una construcción completa.

CI/CD
=====

|Fess| usa GitHub Actions para ejecutar CI/CD.

GitHub Actions
-------------

Los archivos de configuración están en el directorio ``.github/workflows/``.

Verificaciones ejecutadas automáticamente:

- Construcción
- Pruebas unitarias
- Pruebas de integración
- Verificación de estilo de código
- Verificación de calidad de código

Verificación de CI Local
-----------------------

Antes de crear un PR, puede ejecutar las mismas verificaciones que CI localmente:

.. code-block:: bash

    mvn clean verify checkstyle:check

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
    export MAVEN_OPTS="-Xmx2g -XX:MaxPermSize=512m"
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

Verificación de Calidad del Código
------------------

Verifique la calidad del código antes de crear un PR:

.. code-block:: bash

    mvn checkstyle:check spotbugs:check

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
- `Documentación de Mockito <https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html>`__
- `Documentación de JaCoCo <https://www.jacoco.org/jacoco/trunk/doc/>`__
