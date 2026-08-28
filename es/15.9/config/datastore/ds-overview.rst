==================================
Descripción General de los Conectores de Almacén de Datos
==================================

Descripción General
===================

Los conectores de almacén de datos de |Fess| proporcionan funcionalidad para obtener contenido
de fuentes de datos distintas a sitios web o sistemas de archivos y indexarlo.

Al utilizar conectores de almacén de datos, puede hacer que los datos de las siguientes fuentes sean buscables:

- Almacenamiento en la nube (Box, Dropbox, Google Drive, OneDrive)
- Herramientas de colaboración (Confluence, Jira, Slack)
- Bases de datos (MySQL, PostgreSQL, Oracle, etc.)
- Otros sistemas (Git, Salesforce, Elasticsearch, etc.)

Conectores Disponibles
======================

|Fess| proporciona conectores para diversas fuentes de datos.
Muchos conectores se proporcionan como plugins y pueden instalarse según sea necesario.

Almacenamiento en la Nube
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Conector
     - Plugin
     - Descripción
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

Herramientas de Colaboración
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Conector
     - Plugin
     - Descripción
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
     - Descripción
   * - :doc:`ds-git`
     - fess-ds-git
     - Rastrea código fuente de repositorios Git
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
     - Descripción
   * - :doc:`ds-database`
     - fess-ds-db
     - Obtiene datos de bases de datos compatibles con JDBC
   * - :doc:`ds-csv`
     - fess-ds-csv
     - Obtiene datos de archivos CSV
   * - :doc:`ds-json`
     - fess-ds-json
     - Obtiene datos de archivos JSON

Instalación de Conectores
=========================

Instalación de Plugins
----------------------

Los plugins de conectores de almacén de datos pueden instalarse desde la consola de administración.

Desde la Consola de Administración
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Inicie sesión en la consola de administración
2. Vaya a "Sistema" -> "Plugin"
3. Haga clic en el botón "Instalar"
4. Seleccione el plugin en la pestaña "Remoto" (o suba un archivo JAR desde la pestaña "Local")
5. Haga clic en "Instalar"
6. Reinicie |Fess|

Conceptos Básicos de Configuración del Almacén de Datos
=======================================================

La configuración de los conectores de almacén de datos se realiza en la consola de administración bajo "Rastreador" -> "Almacén de Datos".

Elementos de Configuración Comunes
----------------------------------

Elementos de configuración comunes a todos los conectores de almacén de datos:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Elemento
     - Descripción
   * - Nombre
     - Nombre identificador de la configuración
   * - Descripción
     - Texto descriptivo de la configuración
   * - Nombre del Manejador
     - Nombre del manejador del conector a utilizar (ej., ``CsvDataStore``)
   * - Parámetros
     - Parámetros de configuración específicos del conector (formato key=value)
   * - Script
     - Script de mapeo de campos del índice
   * - Boost
     - Prioridad en los resultados de búsqueda
   * - Permisos
     - Permisos de acceso para los documentos obtenidos de este almacén de datos
   * - Hosts virtuales
     - Host virtual al que se aplica esta configuración
   * - Orden de visualización
     - Orden de visualización en la lista de configuraciones
   * - Habilitado
     - Si esta configuración está activa o no

Configuración de Parámetros
---------------------------

Los parámetros se especifican en formato ``key=value`` separados por saltos de linea:

::

    api.key=xxxxxxxxxxxxx
    folder.id=0
    max.depth=3

Configuración de Script
-----------------------

Los scripts mapean los datos obtenidos a los campos del índice de |Fess|.
El lado izquierdo de cada línea es el campo del índice de |Fess|; el lado derecho es el campo obtenido del conector.

El siguiente es un ejemplo para el conector CSV con columnas de encabezado ``link``, ``subject`` y ``body``:

::

    url=link
    title=subject
    content=body

.. note::

   Los nombres de campo utilizables en los scripts difieren según el conector.
   Box/Dropbox/Google Drive/OneDrive referencian el objeto obtenido con el prefijo ``file.*``; Slack utiliza ``message.*``; Jira utiliza ``issue.*``.
   Los conectores CSV, JSON y de base de datos NO utilizan prefijo; los campos se referencian directamente:

   - CSV: nombres de columna del encabezado (si ``has_header_line=true``), o ``cell1``, ``cell2``, ... (índice basado en 1); además de ``csvfile`` y ``csvfilename``.
   - JSON: nombres de campo del objeto JSON.
   - Base de datos: nombres de columna (alias) del resultado del SELECT.

   Consulte la documentación individual de cada conector para más detalles.

Configuración de Autenticación
==============================

Muchos conectores de almacén de datos requieren autenticación mediante OAuth 2.0, claves API, cuentas de servicio, etc.

Los parámetros de autenticación varían según el conector.
Consulte la documentación individual de cada conector para los detalles de configuración de autenticación.

Parámetros Comunes
==================

Parámetros comunes disponibles para todos los conectores de almacén de datos:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parámetro
     - Valor por defecto
     - Descripción
   * - ``readInterval``
     - ``0``
     - Tiempo de espera entre el procesamiento de cada registro (milisegundos). Se utiliza para reducir la carga del servidor al procesar grandes cantidades de datos.
   * - ``script_type``
     - ``javascript``
     - Tipo de motor de scripts usado para el mapeo de campos del índice. JavaScript es el motor
       de scripts integrado en |Fess|, y la pantalla de creación de una nueva configuración de
       almacén de datos viene rellenada con ``script_type=javascript``. ``groovy`` sigue estando
       disponible a través del complemento ``fess-script-groovy``. Una configuración que no tiene
       registrado un ``script_type`` se trata como Groovy, por lo que una configuración creada
       antes de 15.9 sigue funcionando sin cambios. Consulte :doc:`../scripting-overview` para
       más detalles.

Solución de Problemas
=====================

El Conector No Aparece
----------------------

1. Verifique que el plugin esté instalado correctamente
2. Reinicie |Fess|
3. Revise los logs en busca de errores

Errores de Autenticación
------------------------

1. Verifique que las credenciales de autenticación sean correctas
2. Verifique la fecha de expiración del token
3. Confirme que se hayan otorgado los permisos necesarios
4. Verifique que el acceso a la API esté permitido en el servicio

No Se Pueden Obtener Datos
--------------------------

1. Verifique que el formato de los parámetros sea correcto
2. Verifique los permisos de acceso a las carpetas/archivos de destino
3. Revise la configuración de filtros
4. Revise los logs para mensajes de error detallados

Configuración de Depuración
---------------------------

Al investigar problemas, ajuste el nivel de log. El rastreo de almacenes de datos se ejecuta en el proceso del rastreador, por lo que debe editar el archivo de configuración de log del rastreador:

``app/WEB-INF/env/crawler/resources/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.ds" level="DEBUG"/>

Información de Referencia
=========================

- :doc:`../../admin/dataconfig-guide` - Guía de Configuración de Almacén de Datos
- :doc:`../../admin/plugin-guide` - Guía de Administración de Plugins
- :doc:`../../api/admin/api-admin-dataconfig` - API de Configuración de Almacén de Datos
