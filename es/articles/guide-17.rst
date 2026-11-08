==========================================
Parte 17: Extender la búsqueda con plugins
==========================================

Introducción
============

Fess es compatible con muchas fuentes de datos de forma predeterminada, pero puede ser necesario extenderlo mediante plugins para adaptarlo a sistemas y formatos de datos específicos de la empresa.

En este artículo se explica la arquitectura de plugins de Fess y se presenta cómo implementar plugins de fuentes de datos personalizadas y plugins de Ingest.

Audiencia objetivo
==================

- Personas que desean conectar Fess a fuentes de datos personalizadas
- Desarrolladores Java interesados en el desarrollo de plugins
- Personas que desean comprender la arquitectura interna de Fess

Arquitectura de plugins
========================

Fess ofrece los siguientes tipos de plugins.

.. list-table:: Tipos de plugins
   :header-rows: 1
   :widths: 25 35 40

   * - Tipo
     - Función
     - Ejemplos
   * - Data Store (fess-ds-\*)
     - Obtener datos de fuentes de datos externas
     - Slack, Salesforce, DB
   * - Ingest (fess-ingest-\*)
     - Procesar y transformar datos rastreados
     - Example
   * - Theme (fess-theme-\*)
     - Diseño de la pantalla de búsqueda
     - Simple, Code Search
   * - Script (fess-script-\*)
     - Soporte de lenguajes de scripting
     - OGNL
   * - Web App (fess-webapp-\*)
     - Extensiones de aplicaciones web
     - MCP Server

Despliegue de plugins
---------------------

Los plugins se proporcionan como archivos JAR y se colocan en el directorio de plugins de Fess.
Se pueden instalar y administrar desde [Sistema] > [Plugins] en la consola de administración.

Desarrollo de un plugin de fuente de datos personalizada
=========================================================

En esta sección se explica el proceso de desarrollo de un plugin de fuente de datos, suponiendo que se dispone de un sistema de gestión documental interno propietario.

Estructura del proyecto
-----------------------

Cree un proyecto Maven tomando como referencia un plugin de Data Store existente (por ejemplo, fess-ds-git).

::

    fess-ds-custom/
    ├── pom.xml
    └── src/
        └── main/
            └── java/
                └── org/codelibs/fess/ds/custom/
                    └── CustomDataStore.java

Configuración de pom.xml
-------------------------

Especifique fess-parent como POM padre y configure las dependencias necesarias.

.. code-block:: xml

    <parent>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-parent</artifactId>
        <version>15.5.0</version>
    </parent>

    <artifactId>fess-ds-custom</artifactId>
    <packaging>jar</packaging>

    <dependencies>
        <dependency>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess</artifactId>
            <version>${fess.version}</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

Implementación de la clase Data Store
--------------------------------------

El núcleo de un plugin de Data Store es la clase que obtiene datos y registra documentos en Fess.

Los puntos clave de la implementación son los siguientes:

1. Conexión y autenticación con el sistema externo
2. Obtención de datos (llamadas a API, lectura de archivos, etc.)
3. Conversión de los datos obtenidos al formato de documento de Fess
4. Registro de documentos

**Mapeo de campos**

Mapee los datos obtenidos a los campos de Fess.
Los campos principales son los siguientes:

- ``title``: Título del documento
- ``url``: URL del documento (destino del enlace en los resultados de búsqueda)
- ``content``: Cuerpo del documento (objetivo de búsqueda)
- ``mimetype``: Tipo MIME
- ``last_modified``: Fecha y hora de la última modificación

Compilación y despliegue
-------------------------

::

    $ mvn clean package

Coloque el archivo JAR generado en el directorio de plugins de Fess y reinicie Fess.

Desarrollo de un plugin de Ingest
==================================

Un plugin de Ingest es un mecanismo para procesar y transformar documentos obtenidos mediante rastreo antes de registrarlos en el índice.

Casos de uso
-------------

- Agregar campos adicionales a los documentos rastreados
- Limpieza del texto del cuerpo (eliminación de caracteres innecesarios)
- Enriquecimiento mediante APIs externas (traducción, clasificación, etc.)
- Salida de logs (para depuración)

Puntos de implementación
-------------------------

En un plugin de Ingest, se accede a los datos del documento justo antes de registrarlo en el índice y se realiza el procesamiento de transformación.

Por ejemplo, se puede implementar un procesamiento que agregue metadatos del nombre de la organización a todos los documentos, o un procesamiento que elimine patrones específicos del texto del cuerpo.

Desarrollo de un plugin de tema
=================================

Si desea personalizar completamente el diseño de la pantalla de búsqueda, desarrolle un plugin de tema.

Estructura del tema
-------------------

Un plugin de tema se compone de archivos JSP, CSS, JavaScript y archivos de imagen.

::

    fess-theme-custom/
    ├── pom.xml
    └── src/
        └── main/
            └── resources/
                ├── css/
                ├── js/
                ├── images/
                └── view/
                    ├── index.jsp
                    ├── search.jsp
                    └── header.jsp

Personalice el diseño modificando JSP y CSS tomando como referencia los temas existentes.

Mejores prácticas de desarrollo
================================

Referencia a plugins existentes
-------------------------------

Al desarrollar un nuevo plugin, se recomienda encarecidamente consultar el código fuente de los plugins existentes.
El código fuente de todos los plugins está disponible en el repositorio de GitHub de CodeLibs.

Por ejemplo, ``fess-ds-git`` y ``fess-ds-slack`` son buenas referencias para el desarrollo de plugins de Data Store.

Pruebas
-------

Pruebe los plugins desde las siguientes perspectivas:

- Pruebas de conexión con sistemas externos
- Precisión de la transformación de datos
- Manejo de errores (fallos de conexión, datos inválidos, etc.)
- Rendimiento (tiempo de procesamiento para grandes volúmenes de datos)

Compatibilidad de versiones
----------------------------

Verifique la compatibilidad de los plugins al actualizar Fess.
Pueden producirse cambios en la API durante las actualizaciones de versión principal de Fess.

Resumen
=======

En este artículo se explicó el desarrollo de plugins para Fess.

- Visión general de la arquitectura de plugins (Data Store, Ingest, tema, script)
- Proceso de desarrollo de plugins de fuentes de datos personalizadas
- Procesamiento de documentos con plugins de Ingest
- Personalización de la interfaz con plugins de tema
- Mejores prácticas de desarrollo

Los plugins permiten extender Fess para satisfacer los requisitos específicos de la organización.
Con esto concluye la serie de Arquitectura y Escalabilidad. A partir del próximo artículo, la serie de IA y Búsqueda de Próxima Generación abordará los fundamentos de la búsqueda semántica.

Referencias
===========

- `Gestión de plugins de Fess <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__

- `CodeLibs GitHub <https://github.com/codelibs>`__
