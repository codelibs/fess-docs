=======================================================
Visión General de la Documentación para Desarrolladores
=======================================================

Visión General
==============

Esta sección explica el desarrollo de extensiones para |Fess|.
Proporciona información para extender |Fess|, incluyendo el desarrollo de plugins,
la creación de conectores personalizados y la personalización de temas.

Audiencia Objetivo
==================

- Desarrolladores que desean crear funciones personalizadas para |Fess|
- Desarrolladores que desean crear plugins
- Desarrolladores que desean comprender el código fuente de |Fess|

Conocimientos Previos
---------------------

- Conocimientos básicos de Java 21
- Conceptos básicos de Maven (sistema de compilación)
- Experiencia en desarrollo de aplicaciones web
- Conocimientos básicos de OpenSearch (|Fess| utiliza OpenSearch como motor de búsqueda)

Entorno de Desarrollo
=====================

Entorno Recomendado
-------------------

- **JDK**: OpenJDK 21 o superior
- **IDE**: IntelliJ IDEA / Eclipse / VS Code
- **Herramienta de compilación**: Maven (no se exige una versión mínima para la compilación, pero se recomienda una versión 3.x reciente compatible con Java 21)
- **Git**: Control de versiones
- **OpenSearch**: Backend del motor de búsqueda (si se inicia desde el IDE, los módulos y plugins necesarios se descargan durante la compilación)

Configuración Inicial
---------------------

|Fess| se compila como un proyecto Maven. Durante el desarrollo, lo más sencillo es iniciarlo desde el IDE.

1. Obtención del código fuente:

   ::

       git clone https://github.com/codelibs/fess.git

2. Importación al IDE:

   Importe el directorio obtenido al IDE como un proyecto Maven.

3. Descarga de los módulos y plugins de OpenSearch:

   Solo la primera vez, utilice el siguiente comando para obtener en el directorio ``plugins``
   los módulos y plugins del motor de búsqueda.

   ::

       mvn antrun:run

4. Inicio del servidor de desarrollo (desde el IDE):

   Ejecute o depure ``org.codelibs.fess.FessBoot`` en el IDE y abra
   http://localhost:8080/ en el navegador.
   La pantalla de administración está en http://localhost:8080/admin/ (cuenta inicial: ``admin`` / ``admin``).

5. Compilación del paquete (creación de la distribución):

   Si necesita un paquete de distribución, ejecute el objetivo ``package``.
   Los artefactos se generan en ``target/releases`` (agregue ``-DskipTests`` para omitir las pruebas unitarias).

   ::

       mvn package

   Al descomprimir la distribución generada, dispondrá del script de inicio ``bin/fess``.

   ::

       unzip target/releases/fess-*.zip
       ./fess-*/bin/fess

.. note::

    El script de inicio ``bin/fess`` se incluye en el paquete de distribución (zip/rpm/deb).
    Con solo ejecutar ``mvn package`` en el árbol del código fuente, no se genera ``bin/fess``
    directamente en la raíz del repositorio.
    Para desarrollar desde el código fuente, ejecute ``FessBoot`` en el IDE como se indicó
    anteriormente, o utilice el ``bin/fess`` de la distribución descomprimida.

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
     - Implementación MVC mediante el framework LastaFlute
   * - Capa de Servicios
     - Lógica de negocio
   * - Capa de Acceso a Datos
     - Acceso a OpenSearch con seguridad de tipos mediante DBFlute (ESFlute/FreeGen)
   * - Rastreador
     - Recopilación de contenido mediante la biblioteca fess-crawler
   * - Motor de Búsqueda
     - Búsqueda de texto completo mediante OpenSearch

Frameworks Principales
----------------------

- **LastaFlute**: Framework web (acciones, formularios, validación)
- **DBFlute**: Framework de acceso a datos. Las clases de acceso con seguridad de tipos para
  OpenSearch (``Bhv`` / ``ConditionBean``) se generan mediante la función FreeGen de DBFlute
  y las plantillas de ESFlute (para regenerarlas, ejecute ``mvn dbflute:freegen``)
- **Lasta Di**: Contenedor de inyección de dependencias

Estructura de Directorios
=========================

::

    fess/
    ├── src/main/java/org/codelibs/fess/
    │   ├── app/
    │   │   ├── web/         # Controladores (Action)
    │   │   ├── service/     # Servicios
    │   │   ├── logic/       # Lógica
    │   │   └── pager/       # Paginación
    │   ├── api/             # REST API (api/v2, etc.)
    │   ├── helper/          # Clases auxiliares
    │   ├── crawler/         # Relacionado con el rastreador
    │   ├── indexer/         # Procesamiento de indexación
    │   ├── opensearch/      # Acceso a OpenSearch (generado por ESFlute/FreeGen)
    │   ├── llm/             # Integración con LLM
    │   ├── ds/              # Conectores de almacén de datos
    │   ├── ingest/          # Ingest (procesamiento de datos durante la indexación)
    │   ├── script/          # Motor de scripts
    │   ├── entity/          # Entidades
    │   └── mylasta/         # Configuración de LastaFlute (DI, mensajes, configuración con seguridad de tipos)
    ├── src/main/resources/
    │   ├── fess_config.properties  # Configuración
    │   └── fess_*.xml              # Configuración DI (app.xml, fess_ds.xml, etc.)
    └── src/main/webapp/
        └── WEB-INF/view/    # Plantillas JSP

Puntos de Extensión
===================

|Fess| ofrece los siguientes puntos de extensión:

Plugins
-------

Puede agregar funciones utilizando plugins.

- **Plugin de almacén de datos**: Rastreo desde nuevas fuentes de datos (extiende ``AbstractDataStore``)
- **Plugin de motor de scripts**: Compatibilidad con nuevos lenguajes de script (implementa ``ScriptEngine``)
- **Plugin de aplicación web**: Extensión de la interfaz web (sobrescritura de componentes de Lasta Di y fusión de recursos)
- **Plugin Ingest**: Procesamiento de datos durante la indexación (extiende ``Ingester``)

Detalles: :doc:`plugin-architecture`

.. note::

    El propio |Fess| se empaqueta como ``war``. Al compilar plugins localmente, si no se puede
    resolver |Fess| como dependencia, cambie temporalmente ``<packaging>`` en ``pom.xml`` a ``jar``,
    ejecute ``mvn clean install -DskipTests`` y luego vuelva a cambiarlo a ``war``.

Temas
-----

Puede personalizar el diseño de la pantalla de búsqueda.

Detalles: :doc:`theme-development`

Configuración
-------------

Puede personalizar muchos comportamientos mediante ``fess_config.properties``.

Detalles: :doc:`../config/intro`

Desarrollo de Plugins
=====================

Para obtener más detalles sobre el desarrollo de plugins, consulte lo siguiente:

- :doc:`plugin-architecture` - Arquitectura de plugins
- :doc:`datastore-plugin` - Desarrollo de plugins de almacén de datos
- :doc:`script-engine-plugin` - Plugin de motor de scripts
- :doc:`webapp-plugin` - Plugin de aplicación web
- :doc:`ingest-plugin` - Plugin Ingest

Desarrollo de Temas
===================

- :doc:`theme-development` - Personalización de temas

Mejores Prácticas
=================

Convenciones de Codificación
----------------------------

- Seguir el estilo de código existente de |Fess|
- Formatear el código con ``mvn formatter:format``
- Agregar encabezados de licencia con ``mvn license:format``

Pruebas
-------

- Pruebas unitarias (``*Test.java``): se ejecutan con ``mvn test`` en el perfil ``build`` predeterminado
- Pruebas de integración (``*Tests.java``): se ejecutan con ``mvn test -P integrationTests``.
  Para ejecutar las pruebas de integración se necesita un servidor |Fess| en ejecución y OpenSearch

Registro
--------

- Utiliza Log4j2
- ``logger.debug()`` / ``logger.info()`` / ``logger.warn()`` / ``logger.error()``
- No registrar información sensible en los registros

Recursos
========

- `Repositorio de GitHub <https://github.com/codelibs/fess>`__
- `Seguimiento de problemas <https://github.com/codelibs/fess/issues>`__
- `Discusiones <https://github.com/codelibs/fess/discussions>`__
