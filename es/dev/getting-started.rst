================================================
Servidor de Búsqueda de Texto Completo de Código Abierto - Visión General del Desarrollo de |Fess|
================================================

Esta página proporciona una visión general del desarrollo de |Fess| e información básica para comenzar el desarrollo.

.. contents:: Índice
   :local:
   :depth: 2

Visión General
====

|Fess| es un servidor de búsqueda de texto completo de código abierto desarrollado en Java.
Con el objetivo de facilitar la construcción de búsqueda empresarial,
proporciona potentes funciones de búsqueda y una pantalla de administración fácil de usar.

Características de |Fess|
-------------

- **Configuración sencilla**: Se puede iniciar inmediatamente con un entorno Java
- **Crawler potente**: Compatible con diversas fuentes de datos como sitios web, sistemas de archivos, bases de datos, etc.
- **Soporte de japonés**: Optimizado para búsqueda de texto completo en japonés
- **Extensibilidad**: Se pueden extender funciones mediante plugins
- **REST API**: Las funciones de búsqueda se pueden usar desde otras aplicaciones

Pila de Tecnología
==========

|Fess| se desarrolla usando las siguientes tecnologías.

Versión Objetivo
------------

Esta documentación está dirigida a las siguientes versiones:

- **Fess**: 15.3.0
- **Java**: 21 o posterior
- **OpenSearch**: 3.3.0
- **Maven**: 3.x

Tecnologías y Frameworks Principales
----------------------

Java 21
~~~~~~~

|Fess| es una aplicación que funciona con Java 21 o posterior.
Aprovecha las últimas características de Java, mejorando el rendimiento y la mantenibilidad.

- **Recomendado**: Eclipse Temurin 21 (anteriormente AdoptOpenJDK)
- **Versión mínima**: Java 21

LastaFlute
~~~~~~~~~~

`LastaFlute <https://github.com/lastaflute/lastaflute>`__ es
el framework usado en la capa de aplicación web de |Fess|.

**Funciones principales:**

- Contenedor DI (Inyección de dependencias)
- Framework web basado en acciones
- Validación
- Gestión de mensajes
- Gestión de configuración

**Recursos de aprendizaje:**

- `Documentación oficial de LastaFlute <https://github.com/lastaflute/lastaflute>`__
- Puede aprender el uso práctico leyendo el código de Fess

DBFlute
~~~~~~~

`DBFlute <https://dbflute.seasar.org/>`__ es
una herramienta de mapeo O/R para acceso a bases de datos.
En |Fess|, se usa para generar automáticamente código Java desde el esquema de OpenSearch.

**Funciones principales:**

- Constructor SQL con seguridad de tipos
- Generación automática de código desde esquema
- Generación automática de documentación de base de datos

**Recursos de aprendizaje:**

- `Sitio oficial de DBFlute <https://dbflute.seasar.org/>`__

OpenSearch
~~~~~~~~~~

`OpenSearch <https://opensearch.org/>`__ es
un motor de búsqueda y análisis distribuido usado como motor de búsqueda de |Fess|.

**Versión soportada**: OpenSearch 3.3.0

**Plugins obligatorios:**

- opensearch-analysis-fess: Plugin de análisis morfológico dedicado a Fess
- opensearch-analysis-extension: Funcionalidad de análisis de idiomas adicionales
- opensearch-minhash: Detección de documentos similares
- opensearch-configsync: Sincronización de configuración

**Recursos de aprendizaje:**

- `Documentación de OpenSearch <https://opensearch.org/docs/latest/>`__

Maven
~~~~~

Maven se usa como herramienta de construcción de |Fess|.

**Usos principales:**

- Gestión de bibliotecas de dependencias
- Ejecución de procesamiento de construcción
- Ejecución de pruebas
- Creación de paquetes

Herramientas de Desarrollo
========

Entornos de Desarrollo Recomendados
----------------

Eclipse
~~~~~~~

La documentación oficial explica métodos de desarrollo usando Eclipse.

**Versión recomendada**: Eclipse 2023-09 o posterior

**Plugins necesarios:**

- Maven Integration for Eclipse (m2e)
- Eclipse Java Development Tools

IntelliJ IDEA
~~~~~~~~~~~~~

También es posible desarrollar con IntelliJ IDEA.

**Edición recomendada**: Community Edition o Ultimate Edition

**Funciones necesarias:**

- Soporte de Maven (incluido por defecto)
- Soporte de Java

VS Code
~~~~~~~

VS Code también se puede usar para desarrollo ligero.

**Extensiones necesarias:**

- Java Extension Pack
- Maven for Java

Control de Versiones
~~~~~~~~~~~~

- **Git**: Gestión de código fuente
- **GitHub**: Alojamiento de repositorios, gestión de issues, pull requests

Conocimientos Necesarios
========

Conocimientos Básicos
--------

Para el desarrollo de |Fess|, se necesitan los siguientes conocimientos:

**Obligatorio**

- **Programación Java**: Clases, interfaces, genéricos, expresiones lambda, etc.
- **Orientación a objetos**: Herencia, polimorfismo, encapsulación
- **Maven**: Comandos básicos y comprensión de pom.xml
- **Git**: clone, commit, push, pull, branch, merge, etc.

**Recomendado**

- **LastaFlute**: Conceptos de Action, Form, Service
- **DBFlute**: Uso de Behavior, ConditionBean
- **OpenSearch/Elasticsearch**: Conceptos básicos de índice, mapeo, consultas
- **Desarrollo web**: HTML, CSS, JavaScript (especialmente para desarrollo frontend)
- **Comandos Linux**: Desarrollo/depuración en entorno de servidor

Recursos de Aprendizaje
----------

Si está abordando el desarrollo de |Fess| por primera vez, los siguientes recursos son útiles:

Documentación Oficial
~~~~~~~~~~~~~~

- `Manual de Usuario de Fess <https://fess.codelibs.org/ja/>`__
- `Guía del Administrador de Fess <https://fess.codelibs.org/ja/15.3/admin/index.html>`__

Comunidad
~~~~~~~~~~

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__: Preguntas y discusiones
- `Rastreador de Issues <https://github.com/codelibs/fess/issues>`__: Reportes de errores y solicitudes de funciones
- `Foro de Fess <https://discuss.codelibs.org/c/FessJA>`__: Foro de comunidad en japonés

Código Fuente
~~~~~~~~~~

Leer el código real es el método de aprendizaje más efectivo:

- Comenzar leyendo desde funciones pequeñas
- Rastrear el comportamiento del código usando depurador
- Consultar código de prueba existente

Flujo Básico de Desarrollo
==============

El desarrollo de |Fess| generalmente procede con el siguiente flujo:

1. **Verificar/Crear Issue**

   Verifique los issues de GitHub y decida el contenido a trabajar.
   Si es una nueva función o corrección de error, cree un issue.

2. **Crear Rama**

   Cree una rama de trabajo:

   .. code-block:: bash

       git checkout -b feature/my-new-feature

3. **Codificar**

   Implemente la función o corrija el error.

4. **Probar**

   Cree/ejecute pruebas unitarias y verifique que los cambios funcionen correctamente.

5. **Hacer Commit**

   Haga commit de los cambios:

   .. code-block:: bash

       git add .
       git commit -m "Add new feature"

6. **Pull Request**

   Haga push a GitHub y cree un pull request:

   .. code-block:: bash

       git push origin feature/my-new-feature

Consulte :doc:`workflow` para más detalles.

Visión General de la Estructura del Proyecto
==================

El código fuente de |Fess| tiene la siguiente estructura:

.. code-block:: text

    fess/
    ├── src/
    │   ├── main/
    │   │   ├── java/
    │   │   │   └── org/codelibs/fess/
    │   │   │       ├── app/           # Capa de aplicación web
    │   │   │       │   ├── web/       # Pantalla de búsqueda
    │   │   │       │   └── service/   # Capa de servicio
    │   │   │       ├── crawler/       # Funcionalidad de crawler
    │   │   │       ├── es/            # Relacionado con OpenSearch
    │   │   │       ├── helper/        # Clases helper
    │   │   │       ├── job/           # Procesamiento de jobs
    │   │   │       ├── util/          # Utilidades
    │   │   │       └── FessBoot.java  # Clase de inicio
    │   │   ├── resources/
    │   │   │   ├── fess_config.properties
    │   │   │   ├── fess_config.xml
    │   │   │   └── ...
    │   │   └── webapp/
    │   │       └── WEB-INF/
    │   │           └── view/          # Archivos JSP
    │   └── test/
    │       └── java/                  # Código de prueba
    ├── pom.xml                        # Archivo de configuración de Maven
    └── README.md

Paquetes Principales
--------------

app
~~~

Este es el código de la capa de aplicación web.
Incluye Action, Form, Service de la pantalla de administración y pantalla de búsqueda.

crawler
~~~~~~~

Este es el código de funcionalidad de recopilación de datos, como
web crawler, file crawler, data store crawler, etc.

es
~~

Este es el código de integración con OpenSearch.
Incluye operaciones de índice, construcción de consultas de búsqueda, etc.

helper
~~~~~~

Estas son clases helper usadas en toda la aplicación.

job
~~~

Este es el código de jobs ejecutados según programación.
Incluye job de rastreo, job de optimización de índice, etc.

Consulte :doc:`architecture` para más detalles.

Inicio Rápido del Entorno de Desarrollo
=======================

Explicamos cómo configurar el entorno de desarrollo y ejecutar |Fess| con pasos mínimos.

Requisitos Previos
--------

- Java 21 o posterior instalado
- Git instalado
- Maven 3.x instalado

Procedimiento
----

1. **Clonar Repositorio**

   .. code-block:: bash

       git clone https://github.com/codelibs/fess.git
       cd fess

2. **Descargar Plugins de OpenSearch**

   .. code-block:: bash

       mvn antrun:run

3. **Ejecutar**

   Ejecutar desde Maven:

   .. code-block:: bash

       mvn compile exec:java

   O ejecute la clase ``org.codelibs.fess.FessBoot`` desde un IDE (Eclipse, IntelliJ IDEA, etc.).

4. **Acceder**

   Acceda a lo siguiente en el navegador:

   - Pantalla de búsqueda: http://localhost:8080/
   - Pantalla de administración: http://localhost:8080/admin/
     - Usuario predeterminado: admin / admin

Consulte :doc:`setup` para procedimientos de configuración detallados.

Consejos de Desarrollo
==========

Ejecución de Depuración
----------

Al ejecutar depuración en IDE, ejecute la clase ``FessBoot``.
Al establecer puntos de interrupción, puede rastrear el comportamiento del código en detalle.

Hot Deploy
------------

LastaFlute puede reflejar algunos cambios sin reiniciar.
Sin embargo, se requiere reiniciar para cambios en la estructura de clases, etc.

Verificación de Registros
--------

Los registros se emiten en el directorio ``target/fess/logs/``.
Si ocurre un problema, verifique los archivos de registro.

Operación de OpenSearch
----------------

OpenSearch integrado se coloca en ``target/fess/es/``.
También es posible depurar llamando directamente a la API de OpenSearch:

.. code-block:: bash

    # Verificar índices
    curl -X GET http://localhost:9201/_cat/indices?v

    # Buscar documentos
    curl -X GET http://localhost:9201/fess.search/_search?pretty

Comunidad y Soporte
==================

Preguntas y Consultas
--------

Si tiene preguntas o consultas durante el desarrollo, use lo siguiente:

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__: Preguntas y discusiones generales
- `GitHub Issues <https://github.com/codelibs/fess/issues>`__: Reportes de errores y solicitudes de funciones
- `Foro de Fess <https://discuss.codelibs.org/c/FessJA>`__: Foro en japonés

Métodos de Contribución
--------

Consulte :doc:`contributing` para métodos de contribución a |Fess|.

Próximos Pasos
==========

Cuando esté listo para configurar el entorno de desarrollo, proceda a :doc:`setup`.

Consulte también los siguientes documentos para información detallada:

- :doc:`architecture` - Arquitectura y estructura del código
- :doc:`workflow` - Flujo de trabajo de desarrollo
- :doc:`building` - Construcción y pruebas
- :doc:`contributing` - Guía de contribución

Materiales de Referencia
========

Recursos Oficiales
----------

- `Sitio Oficial de Fess <https://fess.codelibs.org/ja/>`__
- `Repositorio de GitHub <https://github.com/codelibs/fess>`__
- `Página de Descargas <https://fess.codelibs.org/ja/downloads.html>`__

Documentación Técnica
--------------

- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
- `OpenSearch <https://opensearch.org/docs/latest/>`__

Comunidad
----------

- `Foro de Fess <https://discuss.codelibs.org/c/FessJA>`__
- `Twitter: @codelibs <https://twitter.com/codelibs>`__
