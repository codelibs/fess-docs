============================================================
Parte 6: Hub de conocimiento para equipos de desarrollo -- Entorno de busqueda integrada de codigo, Wiki y tickets
============================================================

Introduccion
============

Los equipos de desarrollo de software utilizan diversas herramientas en su trabajo diario.
El codigo se almacena en repositorios Git, las especificaciones en Confluence, las tareas en Jira y la comunicacion cotidiana en Slack.
Cada herramienta dispone de su propia funcion de busqueda, pero ante la pregunta "donde fue aquella discusion?", buscar individualmente en cada herramienta resulta ineficiente.

En este articulo, construiremos un hub de conocimiento que centraliza en Fess la informacion de las herramientas que el equipo de desarrollo utiliza a diario, permitiendo realizar busquedas integradas.

Lectores objetivo
=================

- Lideres de equipos de desarrollo de software y responsables de infraestructura
- Personas que desean realizar busquedas transversales en herramientas de desarrollo
- Personas que desean conocer el uso basico de los plugins de data store

Escenario
=========

Habilitaremos la busqueda integrada de la informacion de un equipo de desarrollo (20 personas).

.. list-table:: Fuentes de datos objetivo
   :header-rows: 1
   :widths: 20 30 50

   * - Herramienta
     - Uso
     - Informacion a buscar
   * - Repositorio Git
     - Gestion de codigo fuente
     - Codigo, README, archivos de configuracion
   * - Confluence
     - Gestion de documentos
     - Documentos de diseno, actas de reuniones, manuales de procedimientos
   * - Jira
     - Gestion de tickets
     - Reportes de errores, tareas, historias de usuario
   * - Slack
     - Comunicacion
     - Discusiones tecnicas, registros de decisiones

Que es el rastreo de data store
================================

El rastreo web y el rastreo de archivos recopilan documentos siguiendo URLs o rutas de archivos.
Por otro lado, para recopilar informacion de herramientas SaaS se utiliza el "rastreo de data store".

El rastreo de data store obtiene datos a traves de la API de cada herramienta y los registra en el indice de Fess.
En Fess, se proporcionan plugins de data store para cada herramienta.

Instalacion de plugins
========================

Los plugins de data store se pueden instalar desde el panel de administracion de Fess.

1. Seleccionar [Sistema] > [Plugins] en el panel de administracion
2. Verificar la lista de plugins instalados
3. Ir a la pantalla de instalacion desde el boton [Instalar] e instalar los plugins necesarios desde la pestana [Remoto]

Para el escenario de este articulo, utilizaremos los siguientes plugins.

- ``fess-ds-git``: Rastreo de repositorios Git
- ``fess-ds-atlassian``: Rastreo de Confluence / Jira
- ``fess-ds-slack``: Rastreo de mensajes de Slack

Configuracion de cada fuente de datos
======================================

Configuracion de repositorio Git
----------------------------------

Rastrearemos repositorios Git para incluir codigo y documentos como objetivos de busqueda.

1. [Rastreador] > [Data Store] > [Crear nuevo]
2. Nombre del handler: Seleccionar GitDataStore
3. Configuracion de parametros

**Ejemplo de configuracion de parametros**

.. code-block:: properties

    uri=https://github.com/example/my-repo.git
    username=git-user
    password=ghp_xxxxxxxxxxxxxxxxxxxx
    include_pattern=.*\.(java|py|js|ts|md|rst|txt)$
    max_size=10000000

**Ejemplo de configuracion de scripts**

.. code-block:: properties

    url=url
    title=name
    content=content
    mimetype=mimetype
    content_length=contentLength
    last_modified=timestamp

En ``uri`` se especifica la URL del repositorio, y en ``username`` / ``password`` las credenciales de autenticacion. Para repositorios privados, se establece un token de acceso en ``password``. Con ``include_pattern`` se pueden filtrar las extensiones de archivo objetivo del rastreo mediante expresiones regulares.

Configuracion de Confluence
-----------------------------

Incluiremos las paginas y articulos de blog de Confluence como objetivos de busqueda.

1. [Rastreador] > [Data Store] > [Crear nuevo]
2. Nombre del handler: Seleccionar ConfluenceDataStore
3. Configuracion de parametros

**Ejemplo de configuracion de parametros**

.. code-block:: properties

    home=https://your-domain.atlassian.net/wiki
    auth_type=basic
    basic.username=user@example.com
    basic.password=your-api-token

**Ejemplo de configuracion de scripts**

.. code-block:: properties

    url=content.view_url
    title=content.title
    content=content.body
    last_modified=content.last_modified

En ``home`` se especifica la URL de Confluence y en ``auth_type`` se selecciona el metodo de autenticacion. Para Confluence Cloud se utiliza autenticacion ``basic``, configurando el token de API en ``basic.password``.

Configuracion de Jira
----------------------

Incluiremos los tickets (Issues) de Jira como objetivos de busqueda.

Se utiliza el handler JiraDataStore incluido en el mismo plugin ``fess-ds-atlassian``.
Con JQL (Jira Query Language) se pueden filtrar los tickets objetivo del rastreo.
Por ejemplo, es posible limitar el rastreo unicamente a los tickets de un proyecto especifico o solo a aquellos con un estado determinado (excluyendo los cerrados).

1. [Rastreador] > [Data Store] > [Crear nuevo]
2. Nombre del handler: Seleccionar JiraDataStore
3. Configuracion de parametros

**Ejemplo de configuracion de parametros**

.. code-block:: properties

    home=https://your-domain.atlassian.net
    auth_type=basic
    basic.username=user@example.com
    basic.password=your-api-token
    issue.jql=project = MYPROJ AND status != Closed

**Ejemplo de configuracion de scripts**

.. code-block:: properties

    url=issue.view_url
    title=issue.summary
    content=issue.description
    last_modified=issue.last_modified

En ``issue.jql`` se especifica la consulta JQL para filtrar los tickets objetivo del rastreo.

Configuracion de Slack
-----------------------

Incluiremos los mensajes de Slack como objetivos de busqueda.

1. [Rastreador] > [Data Store] > [Crear nuevo]
2. Nombre del handler: Seleccionar SlackDataStore
3. Configuracion de parametros

**Ejemplo de configuracion de parametros**

.. code-block:: properties

    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=general,engineering,design
    include_private=false

**Ejemplo de configuracion de scripts**

.. code-block:: properties

    url=message.permalink
    title=message.title
    content=message.text
    last_modified=message.timestamp

En ``token`` se especifica el token OAuth del Bot de Slack. Con ``channels`` se pueden especificar los canales objetivo del rastreo; para incluir todos los canales se establece ``*all``. Para incluir canales privados se establece ``include_private=true``, y es necesario que el Bot haya sido invitado a dichos canales.

Uso de etiquetas
=================

Distinguir fuentes de informacion con etiquetas
-------------------------------------------------

Al configurar etiquetas en cada fuente de datos, se permite alternar entre las fuentes de informacion durante la busqueda.

- ``code``: Codigo de repositorios Git
- ``docs``: Documentos de Confluence
- ``tickets``: Tickets de Jira
- ``discussions``: Mensajes de Slack

Los usuarios pueden realizar busquedas transversales con "Todos" y filtrar por etiqueta segun sea necesario.

Mejora de la calidad de busqueda
=================================

Uso del impulso de documentos
-------------------------------

En un hub de conocimiento para equipos de desarrollo, no todos los documentos tienen la misma importancia.
Por ejemplo, se pueden considerar las siguientes prioridades.

1. Documentos de Confluence (especificaciones formales y manuales de procedimientos)
2. Tickets de Jira (problemas actuales y tareas en curso)
3. Repositorios Git (codigo y README)
4. Mensajes de Slack (registros de discusiones)

Con el impulso de documentos, se puede aumentar la puntuacion de busqueda de los documentos que coincidan con condiciones especificas.
Desde [Rastreador] > [Impulso de documentos] en el panel de administracion, se pueden configurar valores de impulso basados en patrones de URL o etiquetas.

Uso de contenido relacionado
------------------------------

Al mostrar "contenido relacionado" en los resultados de busqueda, se ayuda a los usuarios a encontrar la informacion que necesitan.
Por ejemplo, al buscar un documento de diseno en Confluence, resulta util que los tickets de Jira relacionados se muestren como "contenido relacionado".

Consideraciones operativas
===========================

Programacion del rastreo
--------------------------

Se configura una frecuencia de rastreo apropiada para cada fuente de datos.

.. list-table:: Ejemplo de programacion
   :header-rows: 1
   :widths: 25 25 50

   * - Fuente de datos
     - Frecuencia recomendada
     - Motivo
   * - Confluence
     - Cada 4 horas
     - La frecuencia de actualizacion de documentos es moderada
   * - Jira
     - Cada 2 horas
     - Las actualizaciones de tickets son frecuentes
   * - Git
     - Diariamente
     - Alineado con el ciclo de lanzamiento
   * - Slack
     - Cada 4 horas
     - No se requiere tiempo real, pero la frescura es importante

Manejo de limites de tasa de API
----------------------------------

Las API de herramientas SaaS tienen limites de tasa.
Se deben configurar intervalos de rastreo apropiados para no exceder los limites de tasa de la API.
En particular, la API de Slack tiene limites de tasa estrictos, por lo que es importante dejar un margen en los intervalos de rastreo.

Gestion de tokens de acceso
-----------------------------

La configuracion de los plugins de data store requiere tokens de acceso a la API de cada herramienta.
Desde el punto de vista de la seguridad, tenga en cuenta los siguientes aspectos.

- Principio de minimo privilegio: Utilizar tokens de acceso de solo lectura
- Rotacion periodica: Actualizar los tokens regularmente
- Uso de cuentas dedicadas: Utilizar cuentas de servicio en lugar de cuentas personales

Resumen
========

En este articulo, construimos un hub de conocimiento que centraliza en Fess la informacion de las herramientas que el equipo de desarrollo utiliza a diario, permitiendo realizar busquedas integradas.

- Recopilacion de datos de Git, Confluence, Jira y Slack mediante plugins de data store
- Experiencia de busqueda amigable para desarrolladores mediante etiquetas
- Control de la prioridad de la informacion con impulso de documentos
- Consideraciones operativas como limites de tasa de API y gestion de tokens

Con el hub de conocimiento del equipo de desarrollo, se logra un entorno donde es posible responder rapidamente a preguntas como "donde fue aquella discusion?" o "donde esta esa especificacion?".

En el proximo articulo, abordaremos la busqueda transversal en almacenamiento en la nube.

Referencias
============

- `Configuracion de data store de Fess <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Gestion de plugins de Fess <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
