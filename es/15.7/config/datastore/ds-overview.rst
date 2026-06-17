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
     - Rastrea Google Drive
   * - :doc:`ds-microsoft365`
     - fess-ds-microsoft365
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
     - fess-ds-db
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

Los plugins de conectores de almacen de datos pueden instalarse desde la consola de administracion.

Desde la Consola de Administracion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Inicie sesion en la consola de administracion
2. Vaya a "Sistema" -> "Plugin"
3. Haga clic en el boton "Instalar"
4. Seleccione el plugin en la pestana "Remoto" (o suba un archivo JAR desde la pestana "Local")
5. Haga clic en "Instalar"
6. Reinicie |Fess|

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
   * - Descripcion
     - Texto descriptivo de la configuracion
   * - Nombre del Manejador
     - Nombre del manejador del conector a utilizar (ej., ``CsvDataStore``)
   * - Parametros
     - Parametros de configuracion especificos del conector (formato key=value)
   * - Script
     - Script de mapeo de campos del indice
   * - Boost
     - Prioridad en los resultados de busqueda
   * - Permisos
     - Permisos de acceso para los documentos obtenidos de este almacen de datos
   * - Hosts virtuales
     - Host virtual al que se aplica esta configuracion
   * - Orden de visualizacion
     - Orden de visualizacion en la lista de configuraciones
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

Los scripts mapean los datos obtenidos a los campos del indice de |Fess|.
El lado izquierdo de cada linea es el campo del indice de |Fess|; el lado derecho es el campo obtenido del conector.

El siguiente es un ejemplo para el conector CSV con columnas de encabezado ``link``, ``subject`` y ``body``:

::

    url=link
    title=subject
    content=body

.. note::

   Los nombres de campo utilizables en los scripts difieren segun el conector.
   Box/Dropbox/Google Drive/OneDrive referencian el objeto obtenido con el prefijo ``file.*``; Slack utiliza ``message.*``; Jira utiliza ``issue.*``.
   Los conectores CSV, JSON y de base de datos NO utilizan prefijo; los campos se referencian directamente:

   - CSV: nombres de columna del encabezado (si ``has_header_line=true``), o ``cell1``, ``cell2``, ... (indice basado en 1); ademas de ``csvfile`` y ``csvfilename``.
   - JSON: nombres de campo del objeto JSON.
   - Base de datos: nombres de columna (alias) del resultado del SELECT.

   Consulte la documentacion individual de cada conector para mas detalles.

Configuracion de Autenticacion
==============================

Muchos conectores de almacen de datos requieren autenticacion mediante OAuth 2.0, claves API, cuentas de servicio, etc.

Los parametros de autenticacion varian segun el conector.
Consulte la documentacion individual de cada conector para los detalles de configuracion de autenticacion.

Parametros Comunes
==================

Parametros comunes disponibles para todos los conectores de almacen de datos:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parametro
     - Valor por defecto
     - Descripcion
   * - ``readInterval``
     - ``0``
     - Tiempo de espera entre el procesamiento de cada registro (milisegundos). Se utiliza para reducir la carga del servidor al procesar grandes cantidades de datos.
   * - ``script_type``
     - ``groovy``
     - Tipo de motor de scripts usado para el mapeo de campos del indice. De forma predeterminada solo esta disponible ``groovy``.

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

Al investigar problemas, ajuste el nivel de log. El rastreo de almacenes de datos se ejecuta en el proceso del rastreador, por lo que debe editar el archivo de configuracion de log del rastreador:

``app/WEB-INF/env/crawler/resources/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.ds" level="DEBUG"/>

Informacion de Referencia
=========================

- :doc:`../../admin/dataconfig-guide` - Guia de Configuracion de Almacen de Datos
- :doc:`../../admin/plugin-guide` - Guia de Administracion de Plugins
- :doc:`../../api/admin/api-admin-dataconfig` - API de Configuracion de Almacen de Datos
