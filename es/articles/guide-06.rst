=======================================================
Parte 6: Hub de conocimiento para equipos de desarrollo
=======================================================

Introducción
============

Los equipos de desarrollo de software utilizan diversas herramientas en su trabajo diario.
El código se almacena en repositorios Git, las especificaciones en Confluence, las tareas en Jira y la comunicación cotidiana en Slack.
Cada herramienta dispone de su propia función de búsqueda, pero ante la pregunta "¿dónde fue aquella discusión?", buscar individualmente en cada herramienta resulta ineficiente.

En este artículo, construiremos un hub de conocimiento que centraliza en Fess la información de las herramientas que el equipo de desarrollo utiliza a diario, permitiendo realizar búsquedas integradas.

Lectores objetivo
=================

- Líderes de equipos de desarrollo de software y responsables de infraestructura
- Personas que desean realizar búsquedas transversales en herramientas de desarrollo
- Personas que desean conocer el uso básico de los plugins de data store

Escenario
=========

Habilitaremos la búsqueda integrada de la información de un equipo de desarrollo (20 personas).

.. list-table:: Fuentes de datos objetivo
   :header-rows: 1
   :widths: 20 30 50

   * - Herramienta
     - Uso
     - Información a buscar
   * - Repositorio Git
     - Gestión de código fuente
     - Código, README, archivos de configuración
   * - Confluence
     - Gestión de documentos
     - Documentos de diseño, actas de reuniones, manuales de procedimientos
   * - Jira
     - Gestión de tickets
     - Reportes de errores, tareas, historias de usuario
   * - Slack
     - Comunicación
     - Discusiones técnicas, registros de decisiones

Qué es el rastreo de data store
================================

El rastreo web y el rastreo de archivos recopilan documentos siguiendo URLs o rutas de archivos.
Por otro lado, para recopilar información de herramientas SaaS se utiliza el "rastreo de data store".

El rastreo de data store obtiene datos a través de la API de cada herramienta y los registra en el índice de Fess.
En Fess, se proporcionan plugins de data store para cada herramienta.

Instalación de plugins
========================

Los plugins de data store se pueden instalar desde el panel de administración de Fess.

1. Seleccionar [Sistema] > [Plugins] en el panel de administración
2. Verificar la lista de plugins instalados
3. Ir a la pantalla de instalación desde el botón [Instalar] e instalar los plugins necesarios desde la pestaña [Remoto]

Para el escenario de este artículo, utilizaremos los siguientes plugins.

- ``fess-ds-git``: Rastreo de repositorios Git
- ``fess-ds-atlassian``: Rastreo de Confluence / Jira
- ``fess-ds-slack``: Rastreo de mensajes de Slack

Configuración de cada fuente de datos
======================================

Configuración de repositorio Git
----------------------------------

Rastrearemos repositorios Git para incluir código y documentos como objetivos de búsqueda.

1. [Rastreador] > [Data Store] > [Crear nuevo]
2. Nombre del handler: Seleccionar GitDataStore
3. Configuración de parámetros

**Ejemplo de configuración de parámetros**

.. code-block:: properties

    uri=https://github.com/example/my-repo.git
    username=git-user
    password=ghp_xxxxxxxxxxxxxxxxxxxx
    include_pattern=.*\.(java|py|js|ts|md|rst|txt)$
    max_size=10000000

**Ejemplo de configuración de scripts**

.. code-block:: properties

    url=url
    title=name
    content=content
    mimetype=mimetype
    content_length=contentLength
    last_modified=timestamp

En ``uri`` se especifica la URL del repositorio, y en ``username`` / ``password`` las credenciales de autenticación. Para repositorios privados, se establece un token de acceso en ``password``. Con ``include_pattern`` se pueden filtrar las extensiones de archivo objetivo del rastreo mediante expresiones regulares.

Configuración de Confluence
-----------------------------

Incluiremos las páginas y artículos de blog de Confluence como objetivos de búsqueda.

1. [Rastreador] > [Data Store] > [Crear nuevo]
2. Nombre del handler: Seleccionar ConfluenceDataStore
3. Configuración de parámetros

**Ejemplo de configuración de parámetros**

.. code-block:: properties

    home=https://your-domain.atlassian.net/wiki
    auth_type=basic
    basic.username=user@example.com
    basic.password=your-api-token

**Ejemplo de configuración de scripts**

.. code-block:: properties

    url=content.view_url
    title=content.title
    content=content.body
    last_modified=content.last_modified

En ``home`` se especifica la URL de Confluence y en ``auth_type`` se selecciona el método de autenticación. Para Confluence Cloud se utiliza autenticación ``basic``, configurando el token de API en ``basic.password``.

Configuración de Jira
----------------------

Incluiremos los tickets (Issues) de Jira como objetivos de búsqueda.

Se utiliza el handler JiraDataStore incluido en el mismo plugin ``fess-ds-atlassian``.
Con JQL (Jira Query Language) se pueden filtrar los tickets objetivo del rastreo.
Por ejemplo, es posible limitar el rastreo únicamente a los tickets de un proyecto específico o solo a aquellos con un estado determinado (excluyendo los cerrados).

1. [Rastreador] > [Data Store] > [Crear nuevo]
2. Nombre del handler: Seleccionar JiraDataStore
3. Configuración de parámetros

**Ejemplo de configuración de parámetros**

.. code-block:: properties

    home=https://your-domain.atlassian.net
    auth_type=basic
    basic.username=user@example.com
    basic.password=your-api-token
    issue.jql=project = MYPROJ AND status != Closed

**Ejemplo de configuración de scripts**

.. code-block:: properties

    url=issue.view_url
    title=issue.summary
    content=issue.description
    last_modified=issue.last_modified

En ``issue.jql`` se especifica la consulta JQL para filtrar los tickets objetivo del rastreo.

Configuración de Slack
-----------------------

Incluiremos los mensajes de Slack como objetivos de búsqueda.

1. [Rastreador] > [Data Store] > [Crear nuevo]
2. Nombre del handler: Seleccionar SlackDataStore
3. Configuración de parámetros

**Ejemplo de configuración de parámetros**

.. code-block:: properties

    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=general,engineering,design
    include_private=false

**Ejemplo de configuración de scripts**

.. code-block:: properties

    url=message.permalink
    title=message.title
    content=message.text
    last_modified=message.timestamp

En ``token`` se especifica el token OAuth del Bot de Slack. Con ``channels`` se pueden especificar los canales objetivo del rastreo; para incluir todos los canales se establece ``*all``. Para incluir canales privados se establece ``include_private=true``, y es necesario que el Bot haya sido invitado a dichos canales.

Uso de etiquetas
=================

Distinguir fuentes de información con etiquetas
-------------------------------------------------

Al configurar etiquetas en cada fuente de datos, se permite alternar entre las fuentes de información durante la búsqueda.

- ``code``: Código de repositorios Git
- ``docs``: Documentos de Confluence
- ``tickets``: Tickets de Jira
- ``discussions``: Mensajes de Slack

Los usuarios pueden realizar búsquedas transversales con "Todos" y filtrar por etiqueta según sea necesario.

Mejora de la calidad de búsqueda
=================================

Uso del impulso de documentos
-------------------------------

En un hub de conocimiento para equipos de desarrollo, no todos los documentos tienen la misma importancia.
Por ejemplo, se pueden considerar las siguientes prioridades.

1. Documentos de Confluence (especificaciones formales y manuales de procedimientos)
2. Tickets de Jira (problemas actuales y tareas en curso)
3. Repositorios Git (código y README)
4. Mensajes de Slack (registros de discusiones)

Con el impulso de documentos, se puede aumentar la puntuación de búsqueda de los documentos que coincidan con condiciones específicas.
Desde [Rastreador] > [Impulso de documentos] en el panel de administración, se pueden configurar valores de impulso basados en patrones de URL o etiquetas.

Uso de contenido relacionado
------------------------------

Al mostrar "contenido relacionado" en los resultados de búsqueda, se ayuda a los usuarios a encontrar la información que necesitan.
Por ejemplo, al buscar un documento de diseño en Confluence, resulta útil que los tickets de Jira relacionados se muestren como "contenido relacionado".

Consideraciones operativas
===========================

Programación del rastreo
--------------------------

Se configura una frecuencia de rastreo apropiada para cada fuente de datos.

.. list-table:: Ejemplo de programación
   :header-rows: 1
   :widths: 25 25 50

   * - Fuente de datos
     - Frecuencia recomendada
     - Motivo
   * - Confluence
     - Cada 4 horas
     - La frecuencia de actualización de documentos es moderada
   * - Jira
     - Cada 2 horas
     - Las actualizaciones de tickets son frecuentes
   * - Git
     - Diariamente
     - Alineado con el ciclo de lanzamiento
   * - Slack
     - Cada 4 horas
     - No se requiere tiempo real, pero la frescura es importante

Manejo de límites de tasa de API
----------------------------------

Las API de herramientas SaaS tienen límites de tasa.
Se deben configurar intervalos de rastreo apropiados para no exceder los límites de tasa de la API.
En particular, la API de Slack tiene límites de tasa estrictos, por lo que es importante dejar un margen en los intervalos de rastreo.

Gestión de tokens de acceso
-----------------------------

La configuración de los plugins de data store requiere tokens de acceso a la API de cada herramienta.
Desde el punto de vista de la seguridad, tenga en cuenta los siguientes aspectos.

- Principio de mínimo privilegio: Utilizar tokens de acceso de solo lectura
- Rotación periódica: Actualizar los tokens regularmente
- Uso de cuentas dedicadas: Utilizar cuentas de servicio en lugar de cuentas personales

Resumen
========

En este artículo, construimos un hub de conocimiento que centraliza en Fess la información de las herramientas que el equipo de desarrollo utiliza a diario, permitiendo realizar búsquedas integradas.

- Recopilación de datos de Git, Confluence, Jira y Slack mediante plugins de data store
- Experiencia de búsqueda amigable para desarrolladores mediante etiquetas
- Control de la prioridad de la información con impulso de documentos
- Consideraciones operativas como límites de tasa de API y gestión de tokens

Con el hub de conocimiento del equipo de desarrollo, se logra un entorno donde es posible responder rápidamente a preguntas como "¿dónde fue aquella discusión?" o "donde esta esa especificación?".

En el próximo artículo, abordaremos la búsqueda transversal en almacenamiento en la nube.

Referencias
============

- `Configuración de data store de Fess <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Gestión de plugins de Fess <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
