==================================
Vision General de Documentacion para Desarrolladores
==================================

Vision General
==============

Esta seccion explica el desarrollo de extensiones de |Fess|.
Proporciona informacion para extender |Fess|, incluyendo desarrollo de plugins,
creacion de conectores personalizados y personalizacion de temas.

Audiencia Objetivo
==================

- Desarrolladores que desean crear funciones personalizadas para |Fess|
- Desarrolladores que desean crear plugins
- Desarrolladores que desean entender el codigo fuente de |Fess|

Conocimientos Previos
---------------------

- Conocimientos basicos de Java 21
- Conceptos basicos de Maven (sistema de construccion)
- Experiencia en desarrollo de aplicaciones web

Entorno de Desarrollo
=====================

Entorno Recomendado
-------------------

- **JDK**: OpenJDK 21 o superior
- **IDE**: IntelliJ IDEA / Eclipse / VS Code
- **Herramienta de construccion**: Maven 3.9 o superior
- **Git**: Control de versiones

Configuracion
-------------

1. Obtener el codigo fuente:

::

    git clone https://github.com/codelibs/fess.git
    cd fess

2. Construir:

::

    mvn package -DskipTests

3. Iniciar el servidor de desarrollo:

::

    ./bin/fess

Vision General de la Arquitectura
=================================

|Fess| esta compuesto por los siguientes componentes principales:

Estructura de Componentes
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Componente
     - Descripcion
   * - Capa Web
     - Implementacion MVC con el framework LastaFlute
   * - Capa de Servicios
     - Logica de negocio
   * - Capa de Acceso a Datos
     - Integracion con OpenSearch mediante DBFlute
   * - Rastreador
     - Recoleccion de contenido con la biblioteca fess-crawler
   * - Motor de Busqueda
     - Busqueda de texto completo con OpenSearch

Frameworks Principales
----------------------

- **LastaFlute**: Framework web (Acciones, Formularios, Validacion)
- **DBFlute**: Framework de acceso a datos (integracion con OpenSearch)
- **Lasta Di**: Contenedor de inyeccion de dependencias

Estructura de Directorios
=========================

::

    fess/
    ├── src/main/java/org/codelibs/fess/
    │   ├── app/
    │   │   ├── web/         # Controladores (Action)
    │   │   ├── service/     # Servicios
    │   │   └── pager/       # Paginacion
    │   ├── api/             # REST API
    │   ├── helper/          # Clases auxiliares
    │   ├── crawler/         # Relacionado con el rastreador
    │   ├── opensearch/      # Integracion con OpenSearch (generado por DBFlute)
    │   ├── llm/             # Integracion con LLM
    │   └── ds/              # Conectores de almacen de datos
    ├── src/main/resources/
    │   ├── fess_config.properties  # Configuracion
    │   └── fess_*.xml              # Configuracion DI
    └── src/main/webapp/
        └── WEB-INF/view/    # Plantillas JSP

Puntos de Extension
===================

|Fess| proporciona los siguientes puntos de extension:

Plugins
-------

Puede agregar funcionalidad utilizando plugins.

- **Plugin de almacen de datos**: Rastreo desde nuevas fuentes de datos
- **Plugin de motor de scripts**: Soporte para nuevos lenguajes de script
- **Plugin de aplicacion web**: Extension de la interfaz web
- **Plugin Ingest**: Procesamiento de datos durante la indexacion

Detalles: :doc:`plugin-architecture`

Temas
-----

Puede personalizar el diseno de la pantalla de busqueda.

Detalles: :doc:`theme-development`

Configuracion
-------------

Puede personalizar muchos comportamientos en ``fess_config.properties``.

Detalles: :doc:`../config/intro`

Desarrollo de Plugins
=====================

Para detalles sobre el desarrollo de plugins, consulte lo siguiente:

- :doc:`plugin-architecture` - Arquitectura de plugins
- :doc:`datastore-plugin` - Desarrollo de plugins de almacen de datos
- :doc:`script-engine-plugin` - Plugins de motor de scripts
- :doc:`webapp-plugin` - Plugins de aplicacion web
- :doc:`ingest-plugin` - Plugins Ingest

Desarrollo de Temas
===================

- :doc:`theme-development` - Personalizacion de temas

Mejores Practicas
=================

Convenciones de Codificacion
----------------------------

- Seguir el estilo de codigo existente de |Fess|
- Formatear codigo con ``mvn formatter:format``
- Agregar encabezados de licencia con ``mvn license:format``

Pruebas
-------

- Escribir pruebas unitarias (``*Test.java``)
- Las pruebas de integracion son ``*Tests.java``

Registro
--------

- Usar Log4j2
- ``logger.debug()`` / ``logger.info()`` / ``logger.warn()`` / ``logger.error()``
- No registrar informacion sensible

Recursos
========

- `Repositorio GitHub <https://github.com/codelibs/fess>`__
- `Rastreador de Problemas <https://github.com/codelibs/fess/issues>`__
- `Discusiones <https://github.com/codelibs/fess/discussions>`__
