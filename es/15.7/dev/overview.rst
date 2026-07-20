==================================
Visión General de Documentación para Desarrolladores
==================================

Visión General
==============

Esta sección explica el desarrollo de extensiones de |Fess|.
Proporciona información para extender |Fess|, incluyendo desarrollo de plugins,
creación de conectores personalizados y personalización de temas.

Audiencia Objetivo
==================

- Desarrolladores que desean crear funciones personalizadas para |Fess|
- Desarrolladores que desean crear plugins
- Desarrolladores que desean entender el código fuente de |Fess|

Conocimientos Previos
---------------------

- Conocimientos básicos de Java 21
- Conceptos básicos de Maven (sistema de construcción)
- Experiencia en desarrollo de aplicaciones web

Entorno de Desarrollo
=====================

Entorno Recomendado
-------------------

- **JDK**: OpenJDK 21 o superior
- **IDE**: IntelliJ IDEA / Eclipse / VS Code
- **Herramienta de construcción**: Maven 3.9 o superior
- **Git**: Control de versiones

Configuración
-------------

1. Obtener el código fuente:

::

    git clone https://github.com/codelibs/fess.git
    cd fess

2. Construir:

::

    mvn package -DskipTests

3. Iniciar el servidor de desarrollo:

::

    ./bin/fess

Visión General de la Arquitectura
=================================

|Fess| está compuesto por los siguientes componentes principales:

Estructura de Componentes
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Componente
     - Descripción
   * - Capa Web
     - Implementación MVC con el framework LastaFlute
   * - Capa de Servicios
     - Lógica de negocio
   * - Capa de Acceso a Datos
     - Integración con OpenSearch mediante DBFlute
   * - Rastreador
     - Recolección de contenido con la biblioteca fess-crawler
   * - Motor de Búsqueda
     - Búsqueda de texto completo con OpenSearch

Frameworks Principales
----------------------

- **LastaFlute**: Framework web (Acciones, Formularios, Validación)
- **DBFlute**: Framework de acceso a datos (integración con OpenSearch)
- **Lasta Di**: Contenedor de inyección de dependencias

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

Puntos de Extensión
===================

|Fess| proporciona los siguientes puntos de extensión:

Plugins
-------

Puede agregar funcionalidad utilizando plugins.

- **Plugin de almacén de datos**: Rastreo desde nuevas fuentes de datos
- **Plugin de motor de scripts**: Soporte para nuevos lenguajes de script
- **Plugin de aplicación web**: Extensión de la interfaz web
- **Plugin Ingest**: Procesamiento de datos durante la indexación

Detalles: :doc:`plugin-architecture`

Temas
-----

Puede personalizar el diseño de la pantalla de búsqueda.

Detalles: :doc:`theme-development`

Configuración
-------------

Puede personalizar muchos comportamientos en ``fess_config.properties``.

Detalles: :doc:`../config/intro`

Desarrollo de Plugins
=====================

Para detalles sobre el desarrollo de plugins, consulte lo siguiente:

- :doc:`plugin-architecture` - Arquitectura de plugins
- :doc:`datastore-plugin` - Desarrollo de plugins de almacén de datos
- :doc:`script-engine-plugin` - Plugins de motor de scripts
- :doc:`webapp-plugin` - Plugins de aplicación web
- :doc:`ingest-plugin` - Plugins Ingest

Desarrollo de Temas
===================

- :doc:`theme-development` - Personalización de temas

Mejores Prácticas
=================

Convenciones de Codificación
----------------------------

- Seguir el estilo de código existente de |Fess|
- Formatear código con ``mvn formatter:format``
- Agregar encabezados de licencia con ``mvn license:format``

Pruebas
-------

- Escribir pruebas unitarias (``*Test.java``)
- Las pruebas de integración son ``*Tests.java``

Registro
--------

- Usar Log4j2
- ``logger.debug()`` / ``logger.info()`` / ``logger.warn()`` / ``logger.error()``
- No registrar información sensible

Recursos
========

- `Repositorio GitHub <https://github.com/codelibs/fess>`__
- `Rastreador de Problemas <https://github.com/codelibs/fess/issues>`__
- `Discusiones <https://github.com/codelibs/fess/discussions>`__
