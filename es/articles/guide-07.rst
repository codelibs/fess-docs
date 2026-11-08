=======================================================================
Parte 7: Estrategia de búsqueda en la era del almacenamiento en la nube
=======================================================================

Introducción
============

En muchas empresas, el uso del almacenamiento en la nube se ha convertido en algo habitual.
Sin embargo, no son pocos los casos en los que se utilizan diferentes servicios de almacenamiento en la nube según el departamento o el propósito.
El tiempo dedicado a preguntarse "ese archivo está en Google Drive, en SharePoint o en Box" reduce la productividad.

En este artículo, integraremos múltiples servicios de almacenamiento en la nube con Fess para construir un entorno en el que se puedan buscar todos los archivos en la nube desde una única barra de búsqueda.

Público objetivo
================

- Administradores de organizaciones que utilizan múltiples servicios de almacenamiento en la nube
- Personas que enfrentan desafíos en la búsqueda dentro del almacenamiento en la nube
- Personas que comprenden los conceptos básicos de la autenticación OAuth

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
     - Propuestas, informes, hojas de cálculo
   * - SharePoint Online
     - Toda la empresa
     - Portal interno, documentos compartidos
   * - Box
     - Legal y Contabilidad
     - Contratos, facturas, documentos confidenciales

Preparación para la integración con almacenamiento en la nube
=============================================================

Instalación de los plugins de Data Store
----------------------------------------

Para el rastreo del almacenamiento en la nube se utilizan los siguientes plugins.

- ``fess-ds-gsuite``: Rastreo de Google Drive / Google Workspace
- ``fess-ds-microsoft365``: Rastreo de SharePoint Online / OneDrive
- ``fess-ds-box``: Rastreo de Box

Se instalan desde [Sistema] > [Plugins] en la pantalla de administración.

Configuración de la autenticación OAuth
----------------------------------------

Para acceder a las API de los servicios de almacenamiento en la nube, es necesario configurar la autenticación OAuth.
En la consola de administración de cada servicio, se registra una aplicación y se obtienen el ID de cliente y el secreto.

**Procedimiento común**

1. Registrar una aplicación en la consola de administración de cada servicio
2. Configurar los scopes (permisos) de API necesarios (solo lectura es suficiente)
3. Obtener el ID de cliente y el secreto de cliente
4. Configurar esta información en los ajustes de Data Store de Fess

Configuración de cada servicio
===============================

Configuración de Google Drive
------------------------------

Se configura Google Drive como objetivo de búsqueda.

**Preparación en Google Cloud Console**

1. Crear un proyecto en Google Cloud Console
2. Habilitar la API de Google Drive
3. Crear una cuenta de servicio y descargar el archivo de clave JSON
4. Configurar el uso compartido de la cuenta de servicio en las unidades o carpetas objetivo

**Configuración en Fess**

1. [Crawler] > [Data Store] > [Crear nuevo]
2. Nombre del handler: Seleccionar GoogleDriveDataStore
3. Configuración de parámetros y scripts
4. Etiqueta: Establecer ``google-drive``

**Ejemplo de configuración de parámetros**

.. code-block:: properties

    private_key=-----BEGIN RSA PRIVATE KEY-----\nMIIE...\n-----END RSA PRIVATE KEY-----
    private_key_id=your-private-key-id
    client_email=fess-crawler@your-project.iam.gserviceaccount.com
    supported_mimetypes=.*
    include_pattern=
    exclude_pattern=

**Ejemplo de configuración de scripts**

.. code-block:: properties

    url=url
    title=name
    content=contents
    mimetype=mimetype
    content_length=size
    last_modified=modified_time

Se configuran los valores de ``private_key``, ``private_key_id`` y ``client_email`` a partir del archivo de clave JSON de la cuenta de servicio. Los formatos propios de Google, como Google Docs, Hojas de cálculo y Presentaciones, también se pueden extraer como texto y buscar.

Configuración de SharePoint Online
------------------------------------

Se configura la biblioteca de documentos de SharePoint Online como objetivo de búsqueda.

**Preparación en Entra ID (Azure AD)**

1. Registrar una aplicación en Entra ID
2. Configurar los permisos de Microsoft Graph API (como Sites.Read.All)
3. Crear un secreto de cliente o un certificado

**Configuración en Fess**

1. [Crawler] > [Data Store] > [Crear nuevo]
2. Nombre del handler: Seleccionar SharePointDocLibDataStore (para bibliotecas de documentos. Según el caso de uso, también se pueden utilizar SharePointListDataStore, SharePointPageDataStore, OneDriveDataStore, entre otros)
3. Configuración de parámetros y scripts
4. Etiqueta: Establecer ``sharepoint``

**Ejemplo de configuración de parámetros**

.. code-block:: properties

    tenant=your-tenant-id
    client_id=your-client-id
    client_secret=your-client-secret
    site_id=your-site-id

**Ejemplo de configuración de scripts**

.. code-block:: properties

    url=url
    title=name
    content=content
    last_modified=modified

Se configuran los valores de ``tenant``, ``client_id`` y ``client_secret`` obtenidos del registro de aplicación en Entra ID. Si se especifica ``site_id``, solo se rastrea el sitio indicado. Si se omite, se incluyen todos los sitios accesibles.

Configuración de Box
---------------------

Se configura Box como objetivo de búsqueda.

**Preparación en Box Developer Console**

1. Crear una aplicación personalizada en Box Developer Console
2. Seleccionar "Autenticación de servidor (con credenciales de cliente)" como método de autenticación
3. Solicitar al administrador la aprobación de la aplicación

**Configuración en Fess**

1. [Crawler] > [Data Store] > [Crear nuevo]
2. Nombre del handler: Seleccionar BoxDataStore
3. Configuración de parámetros y scripts
4. Etiqueta: Establecer ``box``

**Ejemplo de configuración de parámetros**

.. code-block:: properties

    client_id=your-client-id
    client_secret=your-client-secret
    enterprise_id=your-enterprise-id
    public_key_id=your-public-key-id
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIE...\n-----END ENCRYPTED PRIVATE KEY-----
    passphrase=your-passphrase
    supported_mimetypes=.*

**Ejemplo de configuración de scripts**

.. code-block:: properties

    url=url
    title=name
    content=contents
    mimetype=mimetype
    content_length=size
    last_modified=modified_at

Se configuran las credenciales de autenticación de la aplicación personalizada creada en Box Developer Console. Con ``supported_mimetypes`` se pueden filtrar los tipos de archivo a rastrear mediante expresiones regulares.

Optimización de la búsqueda cruzada
=====================================

Uso del rastreo diferencial
----------------------------

En el rastreo de almacenamiento en la nube, en lugar de obtener todos los archivos cada vez, es más eficiente utilizar el rastreo diferencial, que obtiene solo los archivos actualizados desde el último rastreo.

Verifique si las opciones de rastreo diferencial están disponibles en la configuración de cada plugin.
El rastreo diferencial reduce el número de llamadas a la API y acorta el tiempo de rastreo.

URL de los resultados de búsqueda
----------------------------------

En el caso de documentos rastreados desde el almacenamiento en la nube, al hacer clic en el enlace de los resultados de búsqueda, el archivo se abre en la interfaz web de cada servicio.
Este es un comportamiento natural para el usuario y normalmente no requiere configuración especial.

Consideraciones operativas
===========================

Renovación de tokens OAuth
----------------------------

En la integración con almacenamiento en la nube, es importante prestar atención a la fecha de expiración de los tokens OAuth.

- **Google Drive**: En el caso de cuentas de servicio, los tokens se renuevan automáticamente
- **SharePoint Online**: Los secretos de cliente tienen fecha de expiración, por lo que es necesario renovarlos periódicamente
- **Box**: Puede ser necesario volver a aprobar la aplicación

Registre las fechas de expiración de los tokens en un calendario para evitar la interrupción del rastreo por expiración.

Monitoreo del uso de la API
-----------------------------

Las API de almacenamiento en la nube tienen límites de uso.
Especialmente al rastrear una gran cantidad de archivos, monitoree el uso de la API y ajuste la configuración del rastreo para no exceder los límites.

Permisos y seguridad
---------------------

Configure permisos de solo lectura para la cuenta de servicio de Fess en el almacenamiento en la nube.
Los permisos de escritura no son necesarios, siguiendo el principio de minimizar los riesgos de seguridad.

Además, combinando con la búsqueda basada en roles tratada en la Parte 5, es posible controlar los resultados de búsqueda de acuerdo con el sistema de permisos del almacenamiento en la nube.

Resumen
========

En este artículo, integramos tres servicios de almacenamiento en la nube (Google Drive, SharePoint Online y Box) con Fess y construimos un entorno de búsqueda cruzada.

- Configuración de los plugins de Data Store y autenticación OAuth para cada almacenamiento en la nube
- Distinción y filtrado de fuentes de información mediante etiquetas
- Optimización de la experiencia de búsqueda mediante rastreo diferencial
- Gestión de tokens OAuth y monitoreo del uso de la API

Se logra un entorno en el que se pueden encontrar los archivos necesarios de inmediato sin pensar en "en qué nube están".

En la próxima entrega, abordaremos el ciclo de ajuste para mejorar continuamente la calidad de la búsqueda.

Referencias
============

- `Configuración de Data Store de Fess <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Lista de plugins de Fess <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
