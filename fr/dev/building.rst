==============
Compilation et tests
==============

Cette page explique les méthodes de compilation, de test,
et de création de packages de distribution de |Fess|.

.. contents:: Table des matières
   :local:
   :depth: 2

Aperçu du système de compilation
==================

|Fess| utilise Maven comme outil de compilation.
Maven automatise la gestion des dépendances, la compilation, les tests et le packaging.

pom.xml
-------

C'est le fichier de configuration de Maven. Il est placé dans le répertoire racine du projet.

Principaux contenus de configuration :

- Informations du projet (groupId, artifactId, version)
- Bibliothèques dépendantes
- Plugins de compilation
- Profils

Commandes de compilation de base
==================

Compilation propre
------------

Supprimez les artefacts de compilation, puis recompilez :

.. code-block:: bash

    mvn clean compile

Création de package
--------------

Créez un fichier WAR et un package zip de distribution :

.. code-block:: bash

    mvn package

Les artefacts sont générés dans le répertoire ``target/`` :

.. code-block:: text

    target/
    ├── fess.war
    └── releases/
        └── fess-{version}.zip

Compilation complète
--------

Exécutez clean, compilation, tests et packaging :

.. code-block:: bash

    mvn clean package

Téléchargement des dépendances
--------------------

Téléchargez les bibliothèques dépendantes :

.. code-block:: bash

    mvn dependency:resolve

Téléchargement des plugins OpenSearch
---------------------------------

Téléchargez OpenSearch et les plugins requis :

.. code-block:: bash

    mvn antrun:run

.. note::

   Cette commande est exécutée lors de la configuration de l'environnement de développement ou
   lors de la mise à jour des plugins.

Tests
====

|Fess| implémente les tests en utilisant JUnit.

Exécution des tests unitaires
--------------

Exécuter tous les tests unitaires
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test

Exécuter une classe de test spécifique
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest

Exécuter une méthode de test spécifique
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest#testSearch

Exécuter plusieurs classes de tests
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest,CrawlerTest

Ignorer les tests
--------------

Pour compiler en ignorant les tests :

.. code-block:: bash

    mvn package -DskipTests

.. warning::

   Pendant le développement, n'ignorez pas les tests et exécutez-les toujours.
   Avant de créer une PR, vérifiez que tous les tests passent.

Exécution des tests d'intégration
--------------

Les tests d'intégration nécessitent le profil ``integrationTests``.
Un serveur |Fess| et OpenSearch en cours d'exécution sont requis :

.. code-block:: bash

    mvn test -P integrationTests \
        -Dtest.fess.url="http://localhost:8080" \
        -Dtest.search_engine.url="http://localhost:9201"

.. note::

   Les classes de tests d'intégration utilisent le modèle ``*Tests.java`` (les tests unitaires utilisent ``*Test.java``).

Rédaction de tests
============

Création de tests unitaires
--------------

Placement des classes de tests
~~~~~~~~~~~~~~~~

Placez les classes de tests sous ``src/test/java/``.
La structure des packages doit être la même que le code principal.

.. code-block:: text

    src/
    ├── main/java/org/codelibs/fess/app/service/SearchService.java
    └── test/java/org/codelibs/fess/app/service/SearchServiceTest.java

Structure de base de la classe de test
~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

    package org.codelibs.fess.app.service;

    import org.junit.jupiter.api.Test;
    import static org.junit.jupiter.api.Assertions.*;

    public class SearchServiceTest {

        @Test
        public void testSearch() {
            // Given: Conditions préalables du test
            SearchService service = new SearchService();
            String query = "test";

            // When: Exécution du sujet du test
            SearchResponse response = service.search(query);

            // Then: Vérification des résultats
            assertNotNull(response);
            assertTrue(response.getResultCount() > 0);
        }
    }

Cycle de vie des tests
~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

    import org.junit.jupiter.api.*;

    public class MyServiceTest {

        @BeforeAll
        static void setUpClass() {
            // Exécuté une fois avant tous les tests
        }

        @BeforeEach
        void setUp() {
            // Exécuté avant chaque test
        }

        @Test
        void testSomething() {
            // Test
        }

        @AfterEach
        void tearDown() {
            // Exécuté après chaque test
        }

        @AfterAll
        static void tearDownClass() {
            // Exécuté une fois après tous les tests
        }
    }

Assertions
~~~~~~~~~~

Utilisez les assertions de JUnit 5 :

.. code-block:: java

    import static org.junit.jupiter.api.Assertions.*;

    // Égalité
    assertEquals(expected, actual);
    assertNotEquals(unexpected, actual);

    // Vérification null
    assertNull(obj);
    assertNotNull(obj);

    // Valeur booléenne
    assertTrue(condition);
    assertFalse(condition);

    // Exceptions
    assertThrows(IllegalArgumentException.class, () -> {
        service.doSomething();
    });

    // Collections
    assertIterableEquals(expectedList, actualList);

Couverture des tests
--------------

Mesurez la couverture des tests avec JaCoCo :

.. code-block:: bash

    mvn clean test jacoco:report

Le rapport est généré dans ``target/site/jacoco/index.html``.

Formatage du code
================

|Fess| utilise les outils suivants pour maintenir la qualité du code.

Formateur de code
------------------

Uniformiser le style de codage :

.. code-block:: bash

    mvn formatter:format

En-têtes de licence
----------------

Ajouter les en-têtes de licence aux fichiers sources :

.. code-block:: bash

    mvn license:format

Vérifications avant le commit
------------------

Exécutez les deux avant de commiter :

.. code-block:: bash

    mvn formatter:format
    mvn license:format

Création de packages de distribution
==================

Création de packages zip
------------------

Créez un package zip pour la distribution :

.. code-block:: bash

    mvn clean package

Artefacts générés :

.. code-block:: text

    target/releases/
    └── fess-{version}.zip

Création de packages RPM
------------------

.. code-block:: bash

    mvn rpm:rpm

Création de packages DEB
------------------

.. code-block:: bash

    mvn jdeb:jdeb

Profils
==========

Les profils Maven permettent de basculer entre les types de tests.

build (par défaut)
-----------------

Le profil par défaut. Exécute les tests unitaires (``*Test.java``) :

.. code-block:: bash

    mvn package

integrationTests
----------------

Profil pour exécuter les tests d'intégration (``*Tests.java``) :

.. code-block:: bash

    mvn test -P integrationTests \
        -Dtest.fess.url="http://localhost:8080" \
        -Dtest.search_engine.url="http://localhost:9201"

CI/CD
=====

|Fess| utilise GitHub Actions pour exécuter CI/CD.

GitHub Actions
-------------

Les fichiers de configuration se trouvent dans le répertoire ``.github/workflows/``.

Vérifications automatiquement exécutées :

- Compilation
- Tests unitaires
- Création de packages

Vérification CI en local
-----------------------

Avant de créer une PR, vous pouvez exécuter les mêmes vérifications que CI en local :

.. code-block:: bash

    mvn clean package

Dépannage
====================

Erreurs de compilation
----------

**Erreur : Échec du téléchargement des dépendances**

.. code-block:: bash

    # Nettoyer le dépôt local Maven
    rm -rf ~/.m2/repository
    mvn clean compile

**Erreur : Mémoire insuffisante**

.. code-block:: bash

    # Augmenter la mémoire Maven
    export MAVEN_OPTS="-Xmx2g"
    mvn clean package

**Erreur : Version Java obsolète**

Utilisez Java 21 ou supérieur :

.. code-block:: bash

    java -version

Erreurs de test
----------

**Les tests expirent**

Prolongez le délai d'expiration des tests :

.. code-block:: bash

    mvn test -Dmaven.test.timeout=600

**OpenSearch ne démarre pas**

Vérifiez les ports et changez-les s'ils sont utilisés :

.. code-block:: bash

    lsof -i :9201

Problèmes de dépendances
------------

**Conflits de dépendances**

Vérifiez l'arbre des dépendances :

.. code-block:: bash

    mvn dependency:tree

Exclure une dépendance spécifique :

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

Meilleures pratiques de compilation
========================

Compilation propre régulière
--------------------

Exécutez régulièrement une compilation propre pour éviter les problèmes de cache de compilation :

.. code-block:: bash

    mvn clean package

Exécution des tests
----------

Exécutez toujours les tests avant de commiter :

.. code-block:: bash

    mvn test

Formatage du code
------------------

Exécutez le formatage du code avant de créer une PR :

.. code-block:: bash

    mvn formatter:format
    mvn license:format

Mise à jour des dépendances
------------

Mettez à jour régulièrement les dépendances :

.. code-block:: bash

    mvn versions:display-dependency-updates

Utilisation du cache de compilation
--------------------

Utilisez le cache Maven pour réduire le temps de compilation :

.. code-block:: bash

    # Ignorer si déjà compilé
    mvn compile

Référence des commandes Maven
========================

Commandes couramment utilisées
--------------

.. code-block:: bash

    # Clean
    mvn clean

    # Compilation
    mvn compile

    # Tests
    mvn test

    # Package
    mvn package

    # Installation (enregistrement dans le dépôt local)
    mvn install

    # Vérification (y compris les tests d'intégration)
    mvn verify

    # Résolution des dépendances
    mvn dependency:resolve

    # Affichage de l'arbre des dépendances
    mvn dependency:tree

    # Affichage des informations du projet
    mvn help:effective-pom

    # Formatage du code
    mvn formatter:format

    # Ajout des en-têtes de licence
    mvn license:format

Étapes suivantes
==========

Après avoir compris les méthodes de compilation et de test, consultez la documentation suivante :

- :doc:`workflow` - Flux de travail de développement
- :doc:`contributing` - Directives de contribution
- :doc:`architecture` - Compréhension du code source

Ressources de référence
======

- `Documentation officielle Maven <https://maven.apache.org/guides/>`__
- `Guide utilisateur JUnit 5 <https://junit.org/junit5/docs/current/user-guide/>`__
- `Documentation JaCoCo <https://www.jacoco.org/jacoco/trunk/doc/>`__
