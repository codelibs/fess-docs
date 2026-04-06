============================
Arquitectura y Estructura del Código
============================

Esta página explica la arquitectura, estructura del código,
y componentes principales de |Fess|.
Al comprender la estructura interna de |Fess|, puede proceder con el desarrollo de manera eficiente.

.. contents:: Índice
   :local:
   :depth: 2

Arquitectura General
================

|Fess| se compone de los siguientes componentes principales:

.. code-block:: text

    ┌─────────────────────────────────────────────────┐
    │          Interfaz de Usuario                     │
    │  ┌──────────────┐      ┌──────────────┐        │
    │  │  Pantalla de │      │   Pantalla de │        │
    │  │  Búsqueda    │      │   Administración │    │
    │  │  (JSP/HTML)  │      │   (JSP/HTML)  │        │
    │  └──────────────┘      └──────────────┘        │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │              Capa de Aplicación Web              │
    │  ┌──────────────────────────────────────────┐  │
    │  │           LastaFlute                       │  │
    │  │  ┌────────┐  ┌─────────┐  ┌──────────┐  │  │
    │  │  │ Action │  │  Form   │  │  Service │  │  │
    │  │  └────────┘  └─────────┘  └──────────┘  │  │
    │  └──────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │              Capa de Lógica de Negocio           │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
    │  │ Crawler  │  │  Job     │  │  Helper  │    │
    │  └──────────┘  └──────────┘  └──────────┘    │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │              Capa de Acceso a Datos              │
    │  ┌──────────────────────────────────────────┐  │
    │  │          DBFlute / OpenSearch             │  │
    │  │  ┌────────┐  ┌─────────┐  ┌──────────┐  │  │
    │  │  │Behavior│  │ Entity  │  │  Query   │  │  │
    │  │  └────────┘  └─────────┘  └──────────┘  │  │
    │  └──────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │               Almacén de Datos                   │
    │              OpenSearch 3.5.0                   │
    └─────────────────────────────────────────────────┘

Descripción de Capas
------------

Capa de Interfaz de Usuario
~~~~~~~~~~~~~~~~~~~~~~~~

Esta es la pantalla que los usuarios operan directamente.
Está implementada con JSP, HTML y JavaScript.

- Pantalla de búsqueda: Interfaz de búsqueda para usuarios finales
- Pantalla de administración: Interfaz de configuración y administración para administradores del sistema

Capa de Aplicación Web
~~~~~~~~~~~~~~~~~~~~

Esta es la capa de aplicación web que usa el framework LastaFlute.

- **Action**: Procesa solicitudes HTTP y llama a lógica de negocio
- **Form**: Recepción de parámetros de solicitud y validación
- **Service**: Implementación de lógica de negocio

Capa de Lógica de Negocio
~~~~~~~~~~~~~~~~

Esta es la capa que implementa las funciones principales de |Fess|.

- **Crawler**: Recopila datos de sitios web, sistemas de archivos, etc.
- **Job**: Tareas ejecutadas según programación
- **Helper**: Clases helper usadas en toda la aplicación

Capa de Acceso a Datos
~~~~~~~~~~~~~~

Esta es la capa de acceso a OpenSearch usando DBFlute.

- **Behavior**: Interfaz de operación de datos
- **Entity**: Entidad de datos
- **Query**: Construcción de consultas de búsqueda

Capa de Almacén de Datos
~~~~~~~~~~~~

Usa OpenSearch 3.5.0 como motor de búsqueda.

Estructura del Proyecto
==============

Estructura de Directorios
--------------

.. code-block:: text

    fess/
    ├── src/
    │   ├── main/
    │   │   ├── java/org/codelibs/fess/
    │   │   │   ├── app/              # Aplicación web
    │   │   │   │   ├── web/          # Pantalla de búsqueda
    │   │   │   │   │   ├── admin/    # Pantalla de administración
    │   │   │   │   │   │   ├── ...Action.java
    │   │   │   │   │   │   └── ...Form.java
    │   │   │   │   │   └── ...Action.java
    │   │   │   │   └── service/      # Capa de servicio
    │   │   │   ├── crawler/          # Crawler
    │   │   │   │   ├── helper/       # Crawler helper
    │   │   │   │   ├── processor/    # Crawl processing
    │   │   │   │   ├── service/      # Crawler service
    │   │   │   │   └── transformer/  # Data transformation
    │   │   │   ├── opensearch/       # OpenSearch related
    │   │   │   │   ├── client/       # OpenSearch client
    │   │   │   │   ├── config/       # Configuration management
    │   │   │   │   ├── log/          # Log management
    │   │   │   │   ├── query/        # Query builder
    │   │   │   │   └── user/         # User management
    │   │   │   ├── helper/           # Clases helper
    │   │   │   │   ├── ...Helper.java
    │   │   │   ├── job/              # Jobs
    │   │   │   │   ├── ...Job.java
    │   │   │   ├── util/             # Utilidades
    │   │   │   ├── entity/           # Entidades (generadas automáticamente)
    │   │   │   ├── mylasta/          # Configuración de LastaFlute
    │   │   │   │   ├── action/       # Clase base de Action
    │   │   │   │   ├── direction/    # Configuración de aplicación
    │   │   │   │   └── mail/         # Configuración de correo
    │   │   │   ├── Constants.java    # Definición de constantes
    │   │   │   └── FessBoot.java     # Clase de inicio
    │   │   ├── resources/
    │   │   │   ├── fess_config.properties  # Archivo de configuración
    │   │   │   ├── fess_config.xml         # LastaDi component configuration
    │   │   │   ├── fess_message_ja.properties  # Mensajes (japonés)
    │   │   │   ├── fess_message_en.properties  # Mensajes (inglés)
    │   │   │   └── ...
    │   │   └── webapp/
    │   │       ├── WEB-INF/
    │   │       │   ├── view/          # Archivos JSP
    │   │       │   │   ├── admin/     # JSP de pantalla de administración
    │   │       │   │   └── ...
    │   │       │   └── web.xml
    │   │       ├── css/               # Archivos CSS
    │   │       ├── js/                # Archivos JavaScript
    │   │       └── images/            # Archivos de imagen
    │   └── test/
    │       └── java/org/codelibs/fess/
    │           ├── ...Test.java       # Clases de prueba
    │           └── it/                # Pruebas de integración
    ├── pom.xml                        # Configuración de Maven
    ├── dbflute_fess/                  # Configuración de DBFlute
    │   ├── dfprop/                    # Propiedades de DBFlute
    │   └── freegen/                   # Configuración de FreeGen
    └── README.md

Detalles de Paquetes Principales
==================

Paquete app
------------

Este es el código de la capa de aplicación web.

Paquete app.web
~~~~~~~~~~~~~~~~

Implementa la pantalla de búsqueda y funciones para usuarios finales.

**Clases principales:**

- ``SearchAction.java``: Procesamiento de búsqueda
- ``LoginAction.java``: Procesamiento de inicio de sesión

**Ejemplo:**

.. code-block:: java

    @Execute
    public HtmlResponse index(SearchForm form) {
        // Implementación de procesamiento de búsqueda
        return asHtml(path_IndexJsp);
    }

Paquete app.web.admin
~~~~~~~~~~~~~~~~~~~~~~~

Implementa funciones de la pantalla de administración.

**Clases principales:**

- ``AdminWebconfigAction.java``: Configuración de rastreo web
- ``AdminSchedulerAction.java``: Gestión de programador
- ``AdminUserAction.java``: Gestión de usuarios

**Convenciones de nomenclatura:**

- Prefijo ``Admin``: Action para administración
- Sufijo ``Action``: Clase Action
- Sufijo ``Form``: Clase Form

Paquete app.service
~~~~~~~~~~~~~~~~~~~~

Esta es la capa de servicio que implementa la lógica de negocio.

**Clases principales:**

- ``SearchLogService.java``: Servicio de registro de búsqueda
- ``UserService.java``: Servicio de gestión de usuarios
- ``ScheduledJobService.java``: Servicio de gestión de jobs

**Ejemplo:**

.. code-block:: java

    public class ScheduledJobService {
        @Resource
        private ScheduledJobBhv scheduledJobBhv;

        // Job CRUD operations implementation
    }

Paquete crawler (biblioteca fess-crawler)
-------------------------------------------

Implementa funcionalidad de recopilación de datos.

**Clases principales:**

- ``CrawlerClient.java``: Clase base de cliente de crawler
- ``HcHttpClient.java``: Cliente de rastreo HTTP
- ``FileSystemClient.java``: Rastreo de sistema de archivos
- ``ExtractorFactory.java``: Fábrica de extractores
- ``TikaExtractor.java``: Extracción usando Apache Tika
- ``Transformer.java``: Interfaz de procesamiento de transformación

Paquete crawler (fess main)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integración del crawler en la aplicación principal de Fess.

**Clases principales:**

- ``FessStandardTransformer.java``: Procesamiento de transformación estándar
- ``FessXpathTransformer.java``: Procesamiento de transformación basado en XPath

Paquete opensearch
-------------------

Implementa integración con OpenSearch.

Paquete opensearch.client
~~~~~~~~~~~~~~~~~~~~~~~~~~

Esta es la implementación del cliente de OpenSearch.

**Clases principales:**

- ``SearchEngineClient.java``: Cliente de OpenSearch

Paquete opensearch.query
~~~~~~~~~~~~~~~~~~~~~~~~~

Implementa construcción de consultas de búsqueda.

**Clases principales:**

- ``QueryCommand.java``: Comando de consulta
- ``QueryProcessor.java``: Procesamiento de consultas

Paquete helper
---------------

Estas son clases helper usadas en toda la aplicación.

**Clases principales:**

- ``SystemHelper.java``: Helper de todo el sistema
- ``CrawlingConfigHelper.java``: Helper de configuración de rastreo
- ``SearchLogHelper.java``: Helper de registro de búsqueda
- ``UserInfoHelper.java``: Helper de información de usuario
- ``ViewHelper.java``: Helper relacionado con vista
- ``QueryHelper.java``: Helper de construcción de consultas

**Ejemplo:**

.. code-block:: java

    public class SystemHelper {
        @PostConstruct
        public void init() {
            // Procesamiento de inicialización del sistema
        }
    }

Paquete job
------------

Implementa jobs ejecutados según programación.

**Clases principales:**

- ``CrawlJob.java``: Job de rastreo
- ``SuggestJob.java``: Job de sugerencias
- ``ScriptExecutorJob.java``: Job de ejecución de scripts

**Ejemplo:**

.. code-block:: java

    public class CrawlJob extends ExecJob {
        @Override
        public void execute() {
            // Implementación de procesamiento de rastreo
        }
    }

Paquete entity
---------------

Estas son clases entity correspondientes a documentos de OpenSearch.
Este paquete es generado automáticamente por DBFlute.

**Clases principales:**

- ``SearchLog.java``: Registro de búsqueda
- ``ClickLog.java``: Registro de clics
- ``FavoriteLog.java``: Registro de favoritos
- ``User.java``: Información de usuario
- ``Role.java``: Información de rol

.. note::

   No edite directamente el código del paquete entity.
   Se actualiza regenerándolo después de cambiar el esquema.

Paquete mylasta
----------------

Realiza configuración y personalización de LastaFlute.

Paquete mylasta.action
~~~~~~~~~~~~~~~~~~~~~~~

Define clases base de Action.

- ``FessUserBean.java``: Información de usuario
- ``FessHtmlPath.java``: Definición de ruta HTML

Paquete mylasta.direction
~~~~~~~~~~~~~~~~~~~~~~~~~~

Realiza configuración de toda la aplicación.

- ``FessConfig.java``: Lectura de configuración
- ``FessFwAssistantDirector.java``: Configuración de framework

Patrones de Diseño y Patrones de Implementación
============================

En |Fess|, se usan los siguientes patrones de diseño.

Patrón MVC
----------

Está implementado con patrón MVC de LastaFlute.

- **Model**: Service, Entity
- **View**: JSP
- **Controller**: Action

Ejemplo:

.. code-block:: java

    // Controller (Action)
    public class SearchAction extends FessSearchAction {
        @Resource
        private SearchHelper searchHelper;  // Model (Service)

        @Execute
        public HtmlResponse index(SearchForm form) {
            return search(form);
        }
    }

Patrón DI
---------

Usa el contenedor DI de LastaFlute.

.. code-block:: java

    public class SearchService {
        @Resource
        private SearchEngineClient searchEngineClient;

        @Resource
        private UserInfoHelper userInfoHelper;
    }

Patrón Factory
--------------

Se usa para generar diversos componentes.

.. code-block:: java

    public class ExtractorFactory {
        public Extractor getExtractor(String key) {
            // Generar Extractor según tipo MIME
        }
    }

Patrón Strategy
---------------

Se usa en crawlers y transformers.

.. code-block:: java

    public interface Transformer {
        ResultData transform(ResponseData responseData);
    }

    public class HtmlTransformer implements Transformer {
        // Procesamiento de transformación para HTML
    }

Gestión de Configuración
======

La configuración de |Fess| se gestiona en múltiples archivos.

fess_config.properties
--------------------

Define la configuración principal de la aplicación.

.. code-block:: properties

    # Configuración de conexión a OpenSearch
    search_engine.http.url=http://localhost:9201

    # Configuración de rastreo
    crawler.document.max.site.length=100
    crawler.document.cache.enabled=true

fess_config.xml
--------------

Archivo de configuración de componentes LastaDi.

.. code-block:: xml

    <component name="systemProperties" class="org.codelibs.core.misc.DynamicProperties">
        <arg>
            org.codelibs.fess.util.ResourceUtil.getConfPath("system.properties")
        </arg>
    </component>

fess_message_*.properties
------------------------

Estos son archivos de mensajes para soporte multilingüe.

- ``fess_message_ja.properties``: Japonés
- ``fess_message_en.properties``: Inglés

Flujo de Datos
==========

Flujo de Búsqueda
--------

.. code-block:: text

    1. Usuario busca en pantalla de búsqueda
       ↓
    2. SearchAction recibe solicitud de búsqueda
       ↓
    3. SearchService ejecuta lógica de negocio
       ↓
    4. SearchEngineClient envía consulta de búsqueda a OpenSearch
       ↓
    5. OpenSearch devuelve resultados de búsqueda
       ↓
    6. SearchService formatea resultados
       ↓
    7. SearchAction pasa resultados a JSP y los muestra

Flujo de Rastreo
------------

.. code-block:: text

    1. CrawlJob se ejecuta según programación
       ↓
    2. CrawlingConfigHelper obtiene configuración de rastreo
       ↓
    3. CrawlerClient accede al sitio objetivo
       ↓
    4. Extractor extrae texto del contenido
       ↓
    5. Transformer transforma datos a formato de búsqueda
       ↓
    6. SearchEngineClient registra documento en OpenSearch

Puntos de Extensión
==========

|Fess| se puede extender en los siguientes puntos.

Agregar Crawler Personalizado
--------------------

Puede soportar fuentes de datos propias implementando la ``CrawlerClient interface``.

Agregar Transformer Personalizado
----------------------------

Puede agregar procesamiento de transformación de datos propio implementando ``Transformer``.

Agregar Extractor Personalizado
--------------------------

Puede agregar procesamiento de extracción de contenido propio implementando ``Extractor``.

Agregar Plugin Personalizado
--------------------

Los plugins se pueden gestionar a través de la pantalla de gestión de plugins en la UI de administración.

Materiales de Referencia
======

Frameworks
------------

- `Referencia de LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `Documentación de DBFlute <https://dbflute.seasar.org/>`__

Documentación Técnica
--------------

- `Referencia de API de OpenSearch <https://opensearch.org/docs/latest/api-reference/>`__
- `Apache Tika <https://tika.apache.org/>`__

Próximos Pasos
==========

Una vez que comprenda la arquitectura, consulte los siguientes documentos:

- :doc:`workflow` - Flujo de desarrollo real
- :doc:`building` - Construcción y pruebas
- :doc:`contributing` - Crear pull requests
