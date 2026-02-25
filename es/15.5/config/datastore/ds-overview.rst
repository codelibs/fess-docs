==================================
Descripcion General de los Conectores de Almacen de Datos
==================================

Descripcion General
===================

Los conectores de almacen de datos de |Fess| proporcionan funcionalidad para obtener contenido
de fuentes de datos distintas a sitios web o sistemas de archivos y indexarlo.

Al utilizar conectores de almacen de datos, puede hacer que los datos de las siguientes fuentes sean buscables:

- Almacenamiento en la nube (Box, Dropbox, Google Drive, OneDrive)
- Herramientas de colaboracion (Confluence, Jira, Slack)
- Bases de datos (MySQL, PostgreSQL, Oracle, etc.)
- Otros sistemas (Git, Salesforce, Elasticsearch, etc.)

Conectores Disponibles
======================

|Fess| proporciona conectores para diversas fuentes de datos.
Muchos conectores se proporcionan como plugins y pueden instalarse segun sea necesario.

Almacenamiento en la Nube
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Conector
     - Plugin
     - Descripcion
   * - :doc:`ds-box`
     - fess-ds-box
     - Rastrea archivos y carpetas de Box.com
   * - :doc:`ds-dropbox`
     - fess-ds-dropbox
     - Rastrea archivos y carpetas de Dropbox
   * - :doc:`ds-gsuite`
     - fess-ds-gsuite
     - Rastrea Google Drive, Gmail, etc.
   * - :doc:`ds-microsoft365`
     - fess-ds-office365
     - Rastrea OneDrive, SharePoint, etc.

Herramientas de Colaboracion
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Conector
     - Plugin
     - Descripcion
   * - :doc:`ds-atlassian`
     - fess-ds-atlassian
     - Rastrea Confluence y Jira
   * - :doc:`ds-slack`
     - fess-ds-slack
     - Rastrea mensajes y archivos de Slack

Herramientas de Desarrollo y Operaciones
----------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Conector
     - Plugin
     - Descripcion
   * - :doc:`ds-git`
     - fess-ds-git
     - Rastrea codigo fuente de repositorios Git
   * - :doc:`ds-elasticsearch`
     - fess-ds-elasticsearch
     - Obtiene datos de Elasticsearch/OpenSearch
   * - :doc:`ds-salesforce`
     - fess-ds-salesforce
     - Rastrea objetos de Salesforce

Bases de Datos y Archivos
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Conector
     - Plugin
     - Descripcion
   * - :doc:`ds-database`
     - (incorporado)
     - Obtiene datos de bases de datos compatibles con JDBC
   * - :doc:`ds-csv`
     - fess-ds-csv
     - Obtiene datos de archivos CSV
   * - :doc:`ds-json`
     - fess-ds-json
     - Obtiene datos de archivos JSON

Instalacion de Conectores
=========================

Instalacion de Plugins
----------------------

Los plugins de conectores de almacen de datos pueden instalarse desde la consola de administracion o mediante el comando `plugin`.

Desde la Consola de Administracion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Inicie sesion en la consola de administracion
2. Navegue a "Sistema" -> "Plugins"
3. Busque el plugin deseado en la pestana "Disponible"
4. Haga clic en "Instalar"
5. Reinicie |Fess|

Linea de Comandos
~~~~~~~~~~~~~~~~~

::

    # Instalar un plugin
    ./bin/fess-plugin install fess-ds-box

    # Verificar plugins instalados
    ./bin/fess-plugin list

Entorno Docker
~~~~~~~~~~~~~~

::

    # Instalar plugins al inicio
    docker run -e FESS_PLUGINS="fess-ds-box,fess-ds-dropbox" codelibs/fess:15.5.0

Conceptos Basicos de Configuracion del Almacen de Datos
=======================================================

La configuracion de los conectores de almacen de datos se realiza en la consola de administracion bajo "Rastreador" -> "Almacen de Datos".

Elementos de Configuracion Comunes
----------------------------------

Elementos de configuracion comunes a todos los conectores de almacen de datos:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Elemento
     - Descripcion
   * - Nombre
     - Nombre identificador de la configuracion
   * - Nombre del Manejador
     - Nombre del manejador del conector a utilizar (ej., ``BoxDataStore``)
   * - Parametros
     - Parametros de configuracion especificos del conector (formato key=value)
   * - Script
     - Script de mapeo de campos del indice
   * - Boost
     - Prioridad en los resultados de busqueda
   * - Habilitado
     - Si esta configuracion esta activa o no

Configuracion de Parametros
---------------------------

Los parametros se especifican en formato ``key=value`` separados por saltos de linea:

::

    api.key=xxxxxxxxxxxxx
    folder.id=0
    max.depth=3

Configuracion de Script
-----------------------

Los scripts mapean los datos obtenidos a los campos del indice de |Fess|:

::

    url=data.url
    title=data.name
    content=data.content
    mimetype=data.mimetype
    filetype=data.filetype
    filename=data.filename
    created=data.created
    lastModified=data.lastModified
    contentLength=data.contentLength

Configuracion de Autenticacion
==============================

Muchos conectores de almacen de datos requieren autenticacion mediante OAuth 2.0 o claves API.

Autenticacion OAuth 2.0
-----------------------

Parametros tipicos de configuracion OAuth 2.0:

::

    client.id=ID del cliente
    client.secret=Secreto del cliente
    refresh.token=Token de actualizacion

O:

::

    access.token=Token de acceso

Autenticacion con Clave API
---------------------------

::

    api.key=Clave API
    api.secret=Secreto API

Autenticacion con Cuenta de Servicio
------------------------------------

::

    service.account.email=Correo de la cuenta de servicio
    service.account.key=Clave privada (formato JSON o ruta del archivo de clave)

Ajuste de Rendimiento
=====================

Configuracion para procesar grandes cantidades de datos:

::

    # Tamano del lote
    batch.size=100

    # Tiempo de espera entre solicitudes (milisegundos)
    interval=1000

    # Numero de hilos paralelos
    thread.size=1

    # Tiempo de espera (milisegundos)
    timeout=30000

Solucion de Problemas
=====================

El Conector No Aparece
----------------------

1. Verifique que el plugin este instalado correctamente
2. Reinicie |Fess|
3. Revise los logs en busca de errores

Errores de Autenticacion
------------------------

1. Verifique que las credenciales de autenticacion sean correctas
2. Verifique la fecha de expiracion del token
3. Confirme que se hayan otorgado los permisos necesarios
4. Verifique que el acceso a la API este permitido en el servicio

No Se Pueden Obtener Datos
--------------------------

1. Verifique que el formato de los parametros sea correcto
2. Verifique los permisos de acceso a las carpetas/archivos de destino
3. Revise la configuracion de filtros
4. Revise los logs para mensajes de error detallados

Configuracion de Depuracion
---------------------------

Al investigar problemas, ajuste el nivel de log:

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.ds" level="DEBUG"/>

Informacion de Referencia
=========================

- :doc:`../../admin/dataconfig-guide` - Guia de Configuracion de Almacen de Datos
- :doc:`../../admin/plugin-guide` - Guia de Administracion de Plugins
- :doc:`../../api/admin/api-admin-dataconfig` - API de Configuracion de Almacen de Datos
