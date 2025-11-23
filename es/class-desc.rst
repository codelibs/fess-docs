======================================
Arquitectura y Características de Fess
======================================

Descripción General
===================

Esta página describe las principales características y la arquitectura de Fess desde la perspectiva de los componentes.
Fess emplea un diseño modularizado para facilitar la construcción de sistemas de búsqueda.

Arquitectura General
====================

Fess consta de los siguientes componentes principales:

.. figure:: ../resources/images/en/architecture-overview.png
   :scale: 100%
   :alt: Descripción general de la arquitectura de Fess
   :align: center

   Descripción general de la arquitectura de Fess

Componentes Principales
========================

1. Subsistema de Rastreo
-------------------------

El subsistema de rastreo es responsable de recopilar documentos de varias fuentes de datos.

**Clases y Características Principales:**

Crawler
~~~~~~~

- **Rol**: Clase central para el procesamiento de rastreo
- **Características Principales**:

  - Recopilación de documentos desde sitios web, sistemas de archivos y almacenes de datos
  - Selección de objetivos basada en la configuración de rastreo
  - Gestión de la ejecución de trabajos de rastreo
  - Gestión de sesiones para resultados de rastreo

- **Modos de Ejecución**:

  - Ejecución periódica programada
  - Ejecución manual desde la interfaz de administración
  - Ejecución por línea de comandos

WebCrawler
~~~~~~~~~~

- **Rol**: Rastreo de sitios web
- **Características Principales**:

  - Recuperación y análisis de páginas HTML
  - Extracción y seguimiento de enlaces
  - Soporte para sitios basados en JavaScript
  - Soporte para sitios con autenticación (BASIC/DIGEST/NTLM/FORM)
  - Cumplimiento de robots.txt

FileCrawler
~~~~~~~~~~~

- **Rol**: Rastreo de sistemas de archivos
- **Características Principales**:

  - Recorrido de sistemas de archivos locales
  - Acceso a unidades de red (SMB/CIFS)
  - Detección de formato de archivo y selección de analizador apropiado
  - Control de acceso basado en permisos

DataStoreCrawler
~~~~~~~~~~~~~~~~

- **Rol**: Rastreo de almacenes de datos externos
- **Características Principales**:

  - Recuperación de datos desde bases de datos
  - Integración con almacenamiento en la nube (Google Drive, Dropbox, Box, etc.)
  - Integración con groupware (Office 365, Slack, Confluence, etc.)
  - Extensibilidad mediante plugins

CrawlConfig
~~~~~~~~~~~

- **Rol**: Gestión de la configuración de rastreo
- **Características Principales**:

  - Definición de URLs o rutas objetivo para rastreo
  - Limitación de profundidad de rastreo
  - Configuración de intervalo de rastreo
  - Especificación de patrones de exclusión
  - Asignación de etiquetas

2. Subsistema de Indexación
----------------------------

El subsistema de indexación convierte los documentos recopilados en formato consultable.

DocumentParser
~~~~~~~~~~~~~~

- **Rol**: Análisis de documentos y extracción de texto
- **Características Principales**:

  - Soporte para varios formatos de archivo usando Apache Tika
  - Extracción de metadatos
  - Detección automática de codificación de caracteres
  - Detección automática de idioma

Indexer
~~~~~~~

- **Rol**: Registro de índices en OpenSearch/Elasticsearch
- **Características Principales**:

  - Creación de índices de documentos
  - Indexación masiva para mejorar el rendimiento
  - Optimización de índices
  - Eliminación de documentos antiguos

FieldMapper
~~~~~~~~~~~

- **Rol**: Definición de mapeo de campos
- **Características Principales**:

  - Definición de campos de documento
  - Adición de campos personalizados
  - Especificación de tipo de campo (text, keyword, date, etc.)
  - Configuración de analizadores multilingües

3. Subsistema de Búsqueda
--------------------------

El subsistema de búsqueda procesa las consultas de búsqueda de los usuarios y devuelve resultados.

SearchService
~~~~~~~~~~~~~

- **Rol**: Núcleo del procesamiento de búsqueda
- **Características Principales**:

  - Análisis y optimización de consultas
  - Ejecución de consultas en OpenSearch/Elasticsearch
  - Clasificación de resultados de búsqueda
  - Soporte para búsqueda por facetas
  - Resaltado

QueryProcessor
~~~~~~~~~~~~~~

- **Rol**: Preprocesamiento de consultas de búsqueda
- **Características Principales**:

  - Normalización de consultas
  - Expansión de sinónimos
  - Procesamiento de palabras vacías
  - Corrección de consultas

SuggestService
~~~~~~~~~~~~~~

- **Rol**: Provisión de funcionalidad de sugerencias
- **Características Principales**:

  - Generación de candidatos para autocompletado
  - Provisión de palabras clave de búsqueda populares
  - Utilización de diccionarios personalizados

RankingService
~~~~~~~~~~~~~~

- **Rol**: Ajuste de clasificación de resultados de búsqueda
- **Características Principales**:

  - Potenciación de documentos
  - Potenciación de campos
  - Puntuación personalizada
  - Ajuste de relevancia

4. Subsistema de Administración
--------------------------------

El subsistema de administración gestiona la configuración y operación de Fess.

AdminConsole
~~~~~~~~~~~~

- **Rol**: Interfaz de administración basada en web
- **Características Principales**:

  - Gestión de configuración de rastreo
  - Configuración del programador
  - Gestión de usuarios y roles
  - Configuración del sistema
  - Visualización de registros

Scheduler
~~~~~~~~~

- **Rol**: Gestión de programación de trabajos
- **Características Principales**:

  - Ejecución periódica de trabajos de rastreo
  - Ejecución periódica de optimización de índices
  - Rotación de registros
  - Configuración de programación con expresiones Cron

BackupManager
~~~~~~~~~~~~~

- **Rol**: Copia de seguridad y restauración
- **Características Principales**:

  - Copia de seguridad de datos de configuración
  - Instantáneas de índices
  - Funcionalidad de restauración
  - Programación de copias de seguridad automáticas

5. Subsistema de Autenticación y Autorización
----------------------------------------------

El subsistema de autenticación y autorización gestiona la seguridad y el control de acceso.

AuthenticationManager
~~~~~~~~~~~~~~~~~~~~~

- **Rol**: Gestión de autenticación de usuarios
- **Características Principales**:

  - Autenticación local
  - Integración LDAP/Active Directory
  - Integración SAML
  - Integración OpenID Connect
  - Control de acceso basado en roles (RBAC)

RoleManager
~~~~~~~~~~~

- **Rol**: Gestión de roles y permisos de acceso
- **Características Principales**:

  - Definición de roles
  - Asignación de roles a usuarios
  - Control de acceso a nivel de documento
  - Filtrado de resultados de búsqueda

6. Capa de API
--------------

La capa de API proporciona integración con sistemas externos.

SearchAPI
~~~~~~~~~

- **Rol**: Provisión de API de búsqueda
- **Características Principales**:

  - Búsqueda basada en API REST
  - Respuestas en formato JSON
  - Compatibilidad con OpenSearch
  - API compatible con GSA (Google Search Appliance)

AdminAPI
~~~~~~~~

- **Rol**: Provisión de API de administración
- **Características Principales**:

  - Operaciones CRUD para configuración de rastreo
  - Gestión de índices
  - Control del programador
  - Recuperación de información del sistema

7. Almacenamiento de Datos
---------------------------

El almacenamiento de datos maneja la persistencia de datos para Fess.

ConfigStore
~~~~~~~~~~~

- **Rol**: Almacenamiento de datos de configuración
- **Características Principales**:

  - Persistencia de configuración de rastreo
  - Almacenamiento de configuración del sistema
  - Gestión de información de usuarios y roles
  - Uso de base de datos H2 o BD externa

SearchEngine
~~~~~~~~~~~~

- **Rol**: Integración con motor de búsqueda
- **Características Principales**:

  - Comunicación con OpenSearch/Elasticsearch
  - Gestión de índices
  - Ejecución de consultas
  - Soporte para clustering

Arquitectura de Plugins
========================

Fess puede ampliarse mediante plugins.

Plugins DataStore
-----------------

- **Rol**: Conexión a fuentes de datos externas
- **Plugins Disponibles**:

  - Atlassian (Confluence/Jira)
  - Box
  - CSV
  - Database
  - Dropbox
  - Git/GitBucket
  - Google Drive
  - Office 365
  - S3
  - Slack
  - Otros

Plugins Theme
-------------

- **Rol**: Personalización de interfaz de búsqueda
- **Plugins Disponibles**:

  - Simple Theme
  - Classic Theme

Plugins Ingester
----------------

- **Rol**: Pre y post-procesamiento de datos de índice
- **Plugins Disponibles**:

  - Logger
  - NDJSON

Plugins Script
--------------

- **Rol**: Personalización basada en scripts
- **Plugins Disponibles**:

  - Groovy
  - OGNL

Gestión de Configuración
=========================

FessConfig
----------

- **Rol**: Gestión centralizada de configuración del sistema
- **Principales Elementos de Configuración**:

  - Configuración general del sistema
  - Configuración de rastreo
  - Configuración de búsqueda
  - Configuración de autenticación
  - Configuración de notificaciones
  - Configuración de rendimiento

DynamicProperties
-----------------

- **Rol**: Gestión de configuración dinámica
- **Características Principales**:

  - Cambios de configuración en tiempo de ejecución
  - Uso de variables de entorno
  - Configuración específica de perfil

Resumen
=======

Fess realiza un potente sistema de búsqueda de texto completo mediante la colaboración de estos componentes.
Cada componente está diseñado con acoplamiento débil y puede personalizarse o ampliarse según sea necesario.

Para información más detallada para desarrolladores, consulte:

- `JavaDoc <https://fess.codelibs.org/apidocs/index.html>`__
- `XRef <https://fess.codelibs.org/xref/index.html>`__
- `Guía del Desarrollador <dev/index.html>`__
- `Repositorio GitHub <https://github.com/codelibs/fess>`__
