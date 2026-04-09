============================================================
Parte 7: Estrategia de busqueda en la era del almacenamiento en la nube -- Busqueda cruzada en Google Drive, SharePoint y Box
============================================================

Introduccion
============

En muchas empresas, el uso del almacenamiento en la nube se ha convertido en algo habitual.
Sin embargo, no son pocos los casos en los que se utilizan diferentes servicios de almacenamiento en la nube segun el departamento o el proposito.
El tiempo dedicado a preguntarse "ese archivo esta en Google Drive, en SharePoint o en Box" reduce la productividad.

En este articulo, integraremos multiples servicios de almacenamiento en la nube con Fess para construir un entorno en el que se puedan buscar todos los archivos en la nube desde una unica barra de busqueda.

Publico objetivo
================

- Administradores de organizaciones que utilizan multiples servicios de almacenamiento en la nube
- Personas que enfrentan desafios en la busqueda dentro del almacenamiento en la nube
- Personas que comprenden los conceptos basicos de la autenticacion OAuth

Escenario
=========

Una empresa utiliza los siguientes servicios de almacenamiento en la nube.

.. list-table:: Uso de los servicios de almacenamiento en la nube
   :header-rows: 1
   :widths: 25 35 40

   * - Servicio
     - Departamento
     - Uso principal
   * - Google Drive
     - Ventas y Marketing
     - Propuestas, informes, hojas de calculo
   * - SharePoint Online
     - Toda la empresa
     - Portal interno, documentos compartidos
   * - Box
     - Legal y Contabilidad
     - Contratos, facturas, documentos confidenciales

Preparacion para la integracion con almacenamiento en la nube
=============================================================

Instalacion de los plugins de Data Store
----------------------------------------

Para el rastreo del almacenamiento en la nube se utilizan los siguientes plugins.

- ``fess-ds-gsuite``: Rastreo de Google Drive / Google Workspace
- ``fess-ds-microsoft365``: Rastreo de SharePoint Online / OneDrive
- ``fess-ds-box``: Rastreo de Box

Se instalan desde [Sistema] > [Plugins] en la pantalla de administracion.

Configuracion de la autenticacion OAuth
----------------------------------------

Para acceder a las API de los servicios de almacenamiento en la nube, es necesario configurar la autenticacion OAuth.
En la consola de administracion de cada servicio, se registra una aplicacion y se obtienen el ID de cliente y el secreto.

**Procedimiento comun**

1. Registrar una aplicacion en la consola de administracion de cada servicio
2. Configurar los scopes (permisos) de API necesarios (solo lectura es suficiente)
3. Obtener el ID de cliente y el secreto de cliente
4. Configurar esta informacion en los ajustes de Data Store de Fess

Configuracion de cada servicio
===============================

Configuracion de Google Drive
------------------------------

Se configura Google Drive como objetivo de busqueda.

**Preparacion en Google Cloud Console**

1. Crear un proyecto en Google Cloud Console
2. Habilitar la API de Google Drive
3. Crear una cuenta de servicio y descargar el archivo de clave JSON
4. Configurar el uso compartido de la cuenta de servicio en las unidades o carpetas objetivo

**Configuracion en Fess**

1. [Crawler] > [Data Store] > [Crear nuevo]
2. Nombre del handler: Seleccionar GoogleDriveDataStore
3. Configuracion de parametros y scripts
4. Etiqueta: Establecer ``google-drive``

**Ejemplo de configuracion de parametros**

.. code-block:: properties

    private_key=-----BEGIN RSA PRIVATE KEY-----\nMIIE...\n-----END RSA PRIVATE KEY-----
    private_key_id=your-private-key-id
    client_email=fess-crawler@your-project.iam.gserviceaccount.com
    supported_mimetypes=.*
    include_pattern=
    exclude_pattern=

**Ejemplo de configuracion de scripts**

.. code-block:: properties

    url=url
    title=name
    content=contents
    mimetype=mimetype
    content_length=size
    last_modified=modified_time

Se configuran los valores de ``private_key``, ``private_key_id`` y ``client_email`` a partir del archivo de clave JSON de la cuenta de servicio. Los formatos propios de Google, como Google Docs, Hojas de calculo y Presentaciones, tambien se pueden extraer como texto y buscar.

Configuracion de SharePoint Online
------------------------------------

Se configura la biblioteca de documentos de SharePoint Online como objetivo de busqueda.

**Preparacion en Entra ID (Azure AD)**

1. Registrar una aplicacion en Entra ID
2. Configurar los permisos de Microsoft Graph API (como Sites.Read.All)
3. Crear un secreto de cliente o un certificado

**Configuracion en Fess**

1. [Crawler] > [Data Store] > [Crear nuevo]
2. Nombre del handler: Seleccionar SharePointDocLibDataStore (para bibliotecas de documentos. Segun el caso de uso, tambien se pueden utilizar SharePointListDataStore, SharePointPageDataStore, OneDriveDataStore, entre otros)
3. Configuracion de parametros y scripts
4. Etiqueta: Establecer ``sharepoint``

**Ejemplo de configuracion de parametros**

.. code-block:: properties

    tenant=your-tenant-id
    client_id=your-client-id
    client_secret=your-client-secret
    site_id=your-site-id

**Ejemplo de configuracion de scripts**

.. code-block:: properties

    url=url
    title=name
    content=content
    last_modified=modified

Se configuran los valores de ``tenant``, ``client_id`` y ``client_secret`` obtenidos del registro de aplicacion en Entra ID. Si se especifica ``site_id``, solo se rastrea el sitio indicado. Si se omite, se incluyen todos los sitios accesibles.

Configuracion de Box
---------------------

Se configura Box como objetivo de busqueda.

**Preparacion en Box Developer Console**

1. Crear una aplicacion personalizada en Box Developer Console
2. Seleccionar "Autenticacion de servidor (con credenciales de cliente)" como metodo de autenticacion
3. Solicitar al administrador la aprobacion de la aplicacion

**Configuracion en Fess**

1. [Crawler] > [Data Store] > [Crear nuevo]
2. Nombre del handler: Seleccionar BoxDataStore
3. Configuracion de parametros y scripts
4. Etiqueta: Establecer ``box``

**Ejemplo de configuracion de parametros**

.. code-block:: properties

    client_id=your-client-id
    client_secret=your-client-secret
    enterprise_id=your-enterprise-id
    public_key_id=your-public-key-id
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIE...\n-----END ENCRYPTED PRIVATE KEY-----
    passphrase=your-passphrase
    supported_mimetypes=.*

**Ejemplo de configuracion de scripts**

.. code-block:: properties

    url=url
    title=name
    content=contents
    mimetype=mimetype
    content_length=size
    last_modified=modified_at

Se configuran las credenciales de autenticacion de la aplicacion personalizada creada en Box Developer Console. Con ``supported_mimetypes`` se pueden filtrar los tipos de archivo a rastrear mediante expresiones regulares.

Optimizacion de la busqueda cruzada
=====================================

Uso del rastreo diferencial
----------------------------

En el rastreo de almacenamiento en la nube, en lugar de obtener todos los archivos cada vez, es mas eficiente utilizar el rastreo diferencial, que obtiene solo los archivos actualizados desde el ultimo rastreo.

Verifique si las opciones de rastreo diferencial estan disponibles en la configuracion de cada plugin.
El rastreo diferencial reduce el numero de llamadas a la API y acorta el tiempo de rastreo.

URL de los resultados de busqueda
----------------------------------

En el caso de documentos rastreados desde el almacenamiento en la nube, al hacer clic en el enlace de los resultados de busqueda, el archivo se abre en la interfaz web de cada servicio.
Este es un comportamiento natural para el usuario y normalmente no requiere configuracion especial.

Consideraciones operativas
===========================

Renovacion de tokens OAuth
----------------------------

En la integracion con almacenamiento en la nube, es importante prestar atencion a la fecha de expiracion de los tokens OAuth.

- **Google Drive**: En el caso de cuentas de servicio, los tokens se renuevan automaticamente
- **SharePoint Online**: Los secretos de cliente tienen fecha de expiracion, por lo que es necesario renovarlos periodicamente
- **Box**: Puede ser necesario volver a aprobar la aplicacion

Registre las fechas de expiracion de los tokens en un calendario para evitar la interrupcion del rastreo por expiracion.

Monitoreo del uso de la API
-----------------------------

Las API de almacenamiento en la nube tienen limites de uso.
Especialmente al rastrear una gran cantidad de archivos, monitoree el uso de la API y ajuste la configuracion del rastreo para no exceder los limites.

Permisos y seguridad
---------------------

Configure permisos de solo lectura para la cuenta de servicio de Fess en el almacenamiento en la nube.
Los permisos de escritura no son necesarios, siguiendo el principio de minimizar los riesgos de seguridad.

Ademas, combinando con la busqueda basada en roles tratada en la Parte 5, es posible controlar los resultados de busqueda de acuerdo con el sistema de permisos del almacenamiento en la nube.

Resumen
========

En este articulo, integramos tres servicios de almacenamiento en la nube (Google Drive, SharePoint Online y Box) con Fess y construimos un entorno de busqueda cruzada.

- Configuracion de los plugins de Data Store y autenticacion OAuth para cada almacenamiento en la nube
- Distincion y filtrado de fuentes de informacion mediante etiquetas
- Optimizacion de la experiencia de busqueda mediante rastreo diferencial
- Gestion de tokens OAuth y monitoreo del uso de la API

Se logra un entorno en el que se pueden encontrar los archivos necesarios de inmediato sin pensar en "en que nube estan".

En la proxima entrega, abordaremos el ciclo de ajuste para mejorar continuamente la calidad de la busqueda.

Referencias
============

- `Configuracion de Data Store de Fess <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Lista de plugins de Fess <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
