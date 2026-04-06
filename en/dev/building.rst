==============
Build and Test
==============

This page explains how to build |Fess|, run tests,
and create distribution packages.

.. contents:: Table of Contents
   :local:
   :depth: 2

Build System Overview
==================

|Fess| uses Maven as its build tool.
Maven automates dependency management, compilation, testing, and packaging.

pom.xml
-------

This is Maven's configuration file, located in the project root directory.

Main configuration contents:

- Project information (groupId, artifactId, version)
- Dependency libraries
- Build plugins
- Profiles

Basic Build Commands
==================

Clean Build
------------

Remove build artifacts and rebuild:

.. code-block:: bash

    mvn clean compile

Creating Packages
--------------

Create a WAR file and distribution zip package:

.. code-block:: bash

    mvn package

Artifacts are generated in the ``target/`` directory:

.. code-block:: text

    target/
    ├── fess.war
    └── releases/
        └── fess-{version}.zip

Full Build
--------

Execute all: clean, compile, test, and package:

.. code-block:: bash

    mvn clean package

Downloading Dependencies
--------------------

Download dependency libraries:

.. code-block:: bash

    mvn dependency:resolve

Downloading OpenSearch Plugins
---------------------------------

Download OpenSearch and required plugins:

.. code-block:: bash

    mvn antrun:run

.. note::

   Execute this command when setting up the development environment or
   when updating plugins.

Testing
====

|Fess| uses JUnit for implementing tests.

Running Unit Tests
--------------

Running All Unit Tests
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test

Running Specific Test Classes
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest

Running Specific Test Methods
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest#testSearch

Running Multiple Test Classes
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest,CrawlerTest

Skipping Tests
--------------

To build without running tests:

.. code-block:: bash

    mvn package -DskipTests

.. warning::

   Do not skip tests during development.
   Before creating a PR, ensure all tests pass.

Running Integration Tests
--------------

Integration tests require the ``integrationTests`` profile.
A running |Fess| server and OpenSearch are required:

.. code-block:: bash

    mvn test -P integrationTests \
        -Dtest.fess.url="http://localhost:8080" \
        -Dtest.search_engine.url="http://localhost:9201"

.. note::

   Integration test classes use the ``*Tests.java`` naming pattern (unit tests use ``*Test.java``).

Writing Tests
============

Creating Unit Tests
--------------

Test Class Placement
~~~~~~~~~~~~~~~~

Place test classes under ``src/test/java/``.
Use the same package structure as the main code.

.. code-block:: text

    src/
    ├── main/java/org/codelibs/fess/app/service/SearchService.java
    └── test/java/org/codelibs/fess/app/service/SearchServiceTest.java

Basic Test Class Structure
~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

    package org.codelibs.fess.app.service;

    import org.junit.jupiter.api.Test;
    import static org.junit.jupiter.api.Assertions.*;

    public class SearchServiceTest {

        @Test
        public void testSearch() {
            // Given: Test preconditions
            SearchService service = new SearchService();
            String query = "test";

            // When: Execute test target
            SearchResponse response = service.search(query);

            // Then: Verify results
            assertNotNull(response);
            assertTrue(response.getResultCount() > 0);
        }
    }

Test Lifecycle
~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

    import org.junit.jupiter.api.*;

    public class MyServiceTest {

        @BeforeAll
        static void setUpClass() {
            // Execute once before all tests
        }

        @BeforeEach
        void setUp() {
            // Execute before each test
        }

        @Test
        void testSomething() {
            // Test
        }

        @AfterEach
        void tearDown() {
            // Execute after each test
        }

        @AfterAll
        static void tearDownClass() {
            // Execute once after all tests
        }
    }

Assertions
~~~~~~~~~~

Use JUnit 5 assertions:

.. code-block:: java

    import static org.junit.jupiter.api.Assertions.*;

    // Equality
    assertEquals(expected, actual);
    assertNotEquals(unexpected, actual);

    // null check
    assertNull(obj);
    assertNotNull(obj);

    // Boolean
    assertTrue(condition);
    assertFalse(condition);

    // Exception
    assertThrows(IllegalArgumentException.class, () -> {
        service.doSomething();
    });

    // Collection
    assertIterableEquals(expectedList, actualList);

Test Coverage
--------------

Measure test coverage with JaCoCo:

.. code-block:: bash

    mvn clean test jacoco:report

The report is generated at ``target/site/jacoco/index.html``.

Code Formatting
================

|Fess| uses the following tools to maintain code quality.

Code Formatter
------------------

Unify coding style:

.. code-block:: bash

    mvn formatter:format

License Headers
----------------

Add license headers to source files:

.. code-block:: bash

    mvn license:format

Pre-commit Checks
------------------

Run both before committing:

.. code-block:: bash

    mvn formatter:format
    mvn license:format

Creating Distribution Packages
==================

Creating zip Packages
------------------

Create a zip package for distribution:

.. code-block:: bash

    mvn clean package

Generated artifacts:

.. code-block:: text

    target/releases/
    └── fess-{version}.zip

Creating RPM Packages
------------------

.. code-block:: bash

    mvn rpm:rpm

Creating DEB Packages
------------------

.. code-block:: bash

    mvn jdeb:jdeb

Profiles
==========

Maven profiles allow you to switch between test types.

build (default)
-----------------

The default profile. Runs unit tests (``*Test.java``):

.. code-block:: bash

    mvn package

integrationTests
----------------

Profile for running integration tests (``*Tests.java``):

.. code-block:: bash

    mvn test -P integrationTests \
        -Dtest.fess.url="http://localhost:8080" \
        -Dtest.search_engine.url="http://localhost:9201"

CI/CD
=====

|Fess| uses GitHub Actions for CI/CD.

GitHub Actions
-------------

Configuration files are in the ``.github/workflows/`` directory.

Automatically executed checks:

- Build
- Unit tests
- Package creation

Local CI Checks
-----------------------

Before creating a PR, you can run checks similar to CI locally:

.. code-block:: bash

    mvn clean package

Troubleshooting
====================

Build Errors
----------

**Error: Failed to download dependencies**

.. code-block:: bash

    # Clear Maven local repository
    rm -rf ~/.m2/repository
    mvn clean compile

**Error: Out of memory**

.. code-block:: bash

    # Increase Maven memory
    export MAVEN_OPTS="-Xmx2g"
    mvn clean package

**Error: Java version is old**

Use Java 21 or later:

.. code-block:: bash

    java -version

Test Errors
----------

**Tests timeout**

Extend test timeout:

.. code-block:: bash

    mvn test -Dmaven.test.timeout=600

**OpenSearch won't start**

Check ports and change if in use:

.. code-block:: bash

    lsof -i :9201

Dependency Issues
------------

**Dependency conflicts**

Check dependency tree:

.. code-block:: bash

    mvn dependency:tree

Exclude specific dependencies:

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

Build Best Practices
========================

Regular Clean Builds
--------------------

Regularly perform clean builds to avoid build cache issues:

.. code-block:: bash

    mvn clean package

Running Tests
----------

Always run tests before committing:

.. code-block:: bash

    mvn test

Running Code Formatting
----------------------

Run code formatting before creating a PR:

.. code-block:: bash

    mvn formatter:format
    mvn license:format

Updating Dependencies
------------

Regularly update dependencies:

.. code-block:: bash

    mvn versions:display-dependency-updates

Leveraging Build Cache
--------------------

Leverage Maven cache to reduce build time:

.. code-block:: bash

    # Skip if already compiled
    mvn compile

Maven Command Reference
========================

Frequently Used Commands
--------------

.. code-block:: bash

    # Clean
    mvn clean

    # Compile
    mvn compile

    # Test
    mvn test

    # Package
    mvn package

    # Install (register to local repository)
    mvn install

    # Verify (including integration tests)
    mvn verify

    # Resolve dependencies
    mvn dependency:resolve

    # Display dependency tree
    mvn dependency:tree

    # Display project information
    mvn help:effective-pom

    # Code formatting
    mvn formatter:format

    # Add license headers
    mvn license:format

Next Steps
==========

After understanding build and test methods, refer to the following documents:

- :doc:`workflow` - Development workflow
- :doc:`contributing` - Contribution guidelines
- :doc:`architecture` - Understanding the codebase

References
======

- `Maven Official Documentation <https://maven.apache.org/guides/>`__
- `JUnit 5 User Guide <https://junit.org/junit5/docs/current/user-guide/>`__
- `JaCoCo Documentation <https://www.jacoco.org/jacoco/trunk/doc/>`__
