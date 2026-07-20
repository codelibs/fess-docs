==================================
Conector Salesforce
==================================

Descripción general
===================

El conector Salesforce proporciona la funcionalidad para obtener datos de objetos de Salesforce
(objetos estándar, objetos personalizados) y registrarlos en el índice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-salesforce``.

Objetos compatibles
===================

- **Objetos estándar**: objetos estándar predefinidos (Account, Contact, Lead, Opportunity, Case, Solution, etc.). El conjunto de objetos estándar es fijo y todos ellos se recuperan en cada crawl.
- **Objetos personalizados**: objetos definidos por el usuario y especificados mediante el parámetro ``custom`` (objetos cuyos nombres de API terminan en ``__c``).

.. note::

   Los objetos estándar se crawlean siempre en su totalidad (no es posible seleccionar individualmente cuáles se crawlean). Para excluir objetos no deseados, utilice el filtrado por URL mediante ``include_pattern`` / ``exclude_pattern``.

Lista de objetos estándar
-------------------------

Los siguientes objetos estándar son crawleados. El "Nombre de objeto" es el identificador que se usa en el mapeo de campos (p. ej. ``<NombreObjeto>.title``); ``object.type`` es el valor del tipo de objeto al que puede hacer referencia en los scripts.

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Nombre de objeto
     - ``object.type``
     - Descripción
   * - ``ACCOUNT``
     - ``Account``
     - Account
   * - ``CONTACT``
     - ``Contact``
     - Contact
   * - ``LEAD``
     - ``Lead``
     - Lead
   * - ``OPPORTUNITY``
     - ``Opportunity``
     - Opportunity
   * - ``CASE``
     - ``Case``
     - Case
   * - ``SOLUTION``
     - ``Solution``
     - Solution
   * - ``CONTRACT``
     - ``Contract``
     - Contract
   * - ``ORDER``
     - ``Order``
     - Order
   * - ``CAMPAIGN``
     - ``Campaign``
     - Campaign
   * - ``PRODUCT2``
     - ``Product2``
     - Product
   * - ``PRICEBOOK2``
     - ``Pricebook2``
     - Price Book
   * - ``ASSET``
     - ``Asset``
     - Asset
   * - ``ASSET_RELATIONSHIP``
     - ``AssetRelationship``
     - Asset Relationship
   * - ``TASK``
     - ``Task``
     - Task
   * - ``USER``
     - ``User``
     - User
   * - ``COLLABORATION_GROUP``
     - ``CollaborationGroup``
     - Chatter Group
   * - ``IDEA``
     - ``Idea``
     - Idea
   * - ``RECOMMENDATION``
     - ``Recommendation``
     - Recommendation
   * - ``QUICK_TEXT``
     - ``QuickText``
     - Quick Text
   * - ``MACRO``
     - ``Macro``
     - Macro
   * - ``LIST_EMAIL``
     - ``ListEmail``
     - List Email
   * - ``IMAGE``
     - ``Image``
     - Image
   * - ``DAND_B_COMPANY``
     - ``DandBCompany``
     - D&B Company

Requisitos previos
==================

1. Es necesario instalar el plugin
2. Es necesario crear una aplicación conectada (Connected App) en Salesforce
3. Es necesario configurar la autenticación OAuth
4. Se requiere acceso de lectura a los objetos

Instalación del plugin
----------------------

Instale desde la pantalla de administración en "Sistema" -> "Plugins".

O consulte :doc:`../../admin/plugin-guide` para más detalles.

Configuración
=============

Configure desde la pantalla de administración en "Crawler" -> "Data Store" -> "Crear nuevo".

Configuración básica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Campo
     - Ejemplo
   * - Nombre
     - Salesforce CRM
   * - Handler
     - SalesforceDataStore
   * - Habilitado
     - Activado

Configuración de parámetros
---------------------------

Autenticación OAuth Token (recomendada):

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=1
    ignore_error=true
    custom=FessObj,CustomProduct
    FessObj.title=Name
    FessObj.contents=Name,Description__c
    CustomProduct.title=Product_Name__c
    CustomProduct.contents=Product_Name__c,Product_Description__c

Autenticación OAuth Password:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_password
    username=admin@example.com
    password=YourPassword
    client_id=3MVG9...
    client_secret=1234567890ABCDEF
    security_token=AbCdEfGhIjKlMnOpQrSt
    number_of_threads=1
    ignore_error=true

Lista de parámetros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parámetro
     - Requerido
     - Descripción
   * - ``base_url``
     - No
     - URL de Salesforce (predeterminado: ``https://login.salesforce.com``; Sandbox: ``https://test.salesforce.com``)
   * - ``auth_type``
     - Sí
     - Tipo de autenticación (``oauth_token`` o ``oauth_password``)
   * - ``username``
     - Sí
     - Nombre de usuario de Salesforce
   * - ``client_id``
     - Sí
     - Consumer Key de la aplicación conectada
   * - ``password``
     - Para oauth_password
     - Contraseña de Salesforce
   * - ``private_key``
     - Para oauth_token
     - Clave privada (formato PEM, saltos de línea como ``\n``)
   * - ``client_secret``
     - Para oauth_password
     - Consumer Secret de la aplicación conectada
   * - ``security_token``
     - Para oauth_password
     - Token de seguridad del usuario
   * - ``number_of_threads``
     - No
     - Número de hilos de procesamiento paralelo (predeterminado: 1)
   * - ``ignore_error``
     - No
     - Continuar procesando en caso de error (predeterminado: true)
   * - ``custom``
     - No
     - Nombres de objetos personalizados (separados por comas)
   * - ``<objeto>.title``
     - No
     - Nombre del campo a usar para el título
   * - ``<objeto>.contents``
     - No
     - Nombres de campos a usar para el contenido (separados por comas)
   * - ``<objeto>.descriptions``
     - No
     - Nombres de campos para descripción (separados por comas)
   * - ``<objeto>.thumbnail``
     - No
     - Nombre del campo para miniatura
   * - ``include_pattern``
     - No
     - Patrón de inclusión del filtro URL (regex)
   * - ``exclude_pattern``
     - No
     - Patrón de exclusión del filtro URL (regex)
   * - ``refresh_token_interval``
     - No
     - Intervalo de actualización del token en segundos (predeterminado: 3540)
   * - ``proxy_host``
     - No
     - Nombre del host del proxy HTTP
   * - ``proxy_port``
     - Si proxy_host está configurado
     - Número de puerto del proxy HTTP

Configuración de scripts
------------------------

::

    title="[" + object.type + "] " + object.title
    digest=object.description
    content=object.content
    created=object.created
    timestamp=object.last_modified
    url=object.url

Campos disponibles
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripción
   * - ``object.type``
     - Tipo del objeto (ej: Case, User, Solution)
   * - ``object.title``
     - Nombre del objeto
   * - ``object.description``
     - Descripción del objeto
   * - ``object.content``
     - Contenido de texto del objeto
   * - ``object.id``
     - ID del objeto
   * - ``object.content_length``
     - Longitud del contenido
   * - ``object.created``
     - Fecha y hora de creación
   * - ``object.last_modified``
     - Fecha y hora de última modificación
   * - ``object.url``
     - URL del objeto
   * - ``object.thumbnail``
     - URL del thumbnail

Configuración de aplicación conectada de Salesforce
===================================================

1. Crear aplicación conectada
-----------------------------

En Salesforce Setup:

1. Abrir "Application Manager"
2. Hacer clic en "New Connected App"
3. Ingresar información básica:

   - Nombre de aplicación conectada: Fess Crawler
   - Nombre de API: Fess_Crawler
   - Email de contacto: your-email@example.com

4. Marcar "Enable OAuth Settings"

2. Configuración de autenticación OAuth Token (recomendada)
-----------------------------------------------------------

En configuración OAuth:

1. Marcar "Use digital signatures"
2. Subir el certificado (crear según los pasos a continuación)
3. OAuth Scopes seleccionados:

   - Full access (full)
   - Perform requests on your behalf at any time (refresh_token, offline_access)

4. Hacer clic en "Save"
5. Copiar el Consumer Key

Creación del certificado:

::

    # Generar clave privada
    openssl genrsa -out private_key.pem 2048

    # Generar certificado
    openssl req -new -x509 -key private_key.pem -out certificate.crt -days 365

    # Verificar clave privada
    cat private_key.pem

Suba el certificado (certificate.crt) a Salesforce y
configure el contenido de la clave privada (private_key.pem) en los parámetros.

3. Configuración de autenticación OAuth Password
------------------------------------------------

En configuración OAuth:

1. URL de callback: ``https://localhost`` (no se usa pero es requerido)
2. OAuth Scopes seleccionados:

   - Full access (full)
   - Perform requests on your behalf at any time (refresh_token, offline_access)

3. Hacer clic en "Save"
4. Copiar Consumer Key y Consumer Secret

Obtener el token de seguridad:

1. Abrir configuración personal en Salesforce
2. Hacer clic en "Reset My Security Token"
3. Copiar el token enviado por email

4. Aprobación de aplicación conectada
-------------------------------------

En "Manage" -> "Manage Connected Apps":

1. Seleccionar la aplicación conectada creada
2. Hacer clic en "Edit"
3. Cambiar "Permitted Users" a "Admin approved users are pre-authorized"
4. Asignar perfiles o conjuntos de permisos

Configuración de objetos personalizados
=======================================

Crawl de objetos personalizados
-------------------------------

Especifique los nombres de objetos personalizados en el parámetro ``custom``:

::

    custom=FessObj,CustomProduct,ProjectTask

Mapeo de campos para cada objeto:

::

    FessObj.title=Name
    FessObj.contents=Name,Description__c,Notes__c

    CustomProduct.title=Product_Name__c
    CustomProduct.contents=Product_Name__c,Product_Description__c,Specifications__c

    ProjectTask.title=Task_Name__c
    ProjectTask.contents=Task_Name__c,Task_Description__c

Reglas de mapeo de campos
~~~~~~~~~~~~~~~~~~~~~~~~~

- ``<nombre_objeto>.title`` - Campo a usar para el título (campo único)
- ``<nombre_objeto>.contents`` - Campos a usar para el contenido (múltiples separados por comas)
- ``<nombre_objeto>.descriptions`` - Campos a usar para la descripción (múltiples separados por comas)
- ``<nombre_objeto>.thumbnail`` - Campo a usar para la miniatura (campo único)

.. note::

   En el mapeo de campos de objetos estándar, el nombre de objeto usa UPPER_SNAKE_CASE
   (el valor de la columna "Nombre de objeto" de la sección `Lista de objetos estándar`_)
   (p. ej. ``ACCOUNT.title=Name``, ``DAND_B_COMPANY.title=Name``).
   Para objetos personalizados, se usa el nombre de referencia de la API tal cual (p. ej. ``Product__c.title=Name``).

Ejemplos de uso
===============

Crawl de objetos estándar
-------------------------

Parámetros:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=1
    ignore_error=true

Script:

::

    title="[" + object.type + "] " + object.title
    content=object.content
    digest=object.description
    created=object.created
    timestamp=object.last_modified
    url=object.url

Crawl de objetos personalizados
-------------------------------

Parámetros:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=2
    ignore_error=true
    custom=Product__c,Contract__c
    Product__c.title=Name
    Product__c.contents=Name,Description__c,Category__c
    Contract__c.title=Contract_Name__c
    Contract__c.contents=Contract_Name__c,Terms__c,Notes__c

Script:

::

    title="[" + object.type + "] " + object.title
    content=object.content
    created=object.created
    timestamp=object.last_modified
    url=object.url

Crawl de entorno Sandbox
------------------------

Parámetros:

::

    base_url=https://test.salesforce.com
    auth_type=oauth_password
    username=admin@example.com.sandbox
    password=YourPassword
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    client_secret=1234567890ABCDEF1234567890ABCDEF
    security_token=AbCdEfGhIjKlMnOpQrStUvWxYz
    number_of_threads=1
    ignore_error=true

Script:

::

    title="[SANDBOX] [" + object.type + "] " + object.title
    content=object.content
    timestamp=object.last_modified
    url=object.url

Solución de problemas
=====================

Error de autenticación
----------------------

**Síntoma**: ``Authentication failed`` o ``invalid_grant``

**Verificaciones**:

1. Para autenticación OAuth Token:

   - Verificar que el Consumer Key sea correcto
   - Verificar que la clave privada esté copiada correctamente (saltos de línea como ``\n``)
   - Confirmar que el certificado esté subido a Salesforce
   - Verificar que el nombre de usuario sea correcto

2. Para autenticación OAuth Password:

   - Verificar que Consumer Key y Consumer Secret sean correctos
   - Verificar que el token de seguridad sea correcto
   - Confirmar que la contraseña y el token de seguridad no estén concatenados (configurar por separado)

3. Común:

   - Verificar que base_url sea correcta (entorno de producción o Sandbox)
   - Confirmar que la aplicación conectada esté aprobada

No se obtienen objetos
----------------------

**Síntoma**: El crawl tiene éxito pero hay 0 objetos

**Verificaciones**:

1. Confirmar que el usuario tiene permisos de lectura en los objetos
2. Para objetos personalizados, verificar que el nombre del objeto sea correcto (API Name)
3. Verificar que el mapeo de campos sea correcto
4. Revisar los mensajes de error en el log

Nombre de objeto personalizado
------------------------------

Verificar el API Name del objeto personalizado:

1. Abrir "Object Manager" en Salesforce Setup
2. Seleccionar el objeto personalizado
3. Copiar el "API Name" (generalmente termina en ``__c``)

Ejemplo:

- Label: Product
- API Name: Product__c (usar este)

Verificación de nombres de campo
--------------------------------

Verificar el API Name del campo personalizado:

1. Abrir "Fields & Relationships" del objeto
2. Seleccionar el campo personalizado
3. Copiar el "Field Name" (generalmente termina en ``__c``)

Ejemplo:

- Field Label: Product Description
- Field Name: Product_Description__c (usar este)

Límite de tasa de API
---------------------

**Síntoma**: ``REQUEST_LIMIT_EXCEEDED``

**Solución**:

1. Reducir ``number_of_threads`` (configurar a 1)
2. Aumentar el intervalo de crawl
3. Verificar el uso de la API de Salesforce
4. Comprar límite de API adicional si es necesario

Gran volumen de datos
---------------------

**Síntoma**: El crawl toma mucho tiempo o tiene timeout

**Solución**:

1. Dividir objetos en múltiples data stores
2. Ajustar ``number_of_threads`` (aproximadamente 2-4)
3. Distribuir el horario de crawl
4. Mapear solo los campos necesarios

Error de formato de clave privada
---------------------------------

**Síntoma**: ``Invalid private key format``

**Solución**:

Verificar que los saltos de línea en la clave privada sean correctamente ``\n``:

::

    # Formato correcto
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n

    # Formato incorrecto (contiene saltos de linea reales)
    private_key=-----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQE...
    -----END PRIVATE KEY-----

Información de referencia
=========================

- :doc:`ds-overview` - Descripción general de conectores de Data Store
- :doc:`ds-database` - Conector de base de datos
- :doc:`../../admin/dataconfig-guide` - Guía de configuración de Data Store
- `Salesforce REST API <https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/>`_
- `Salesforce OAuth 2.0 JWT Bearer Flow <https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_jwt_flow.htm>`_
- `Salesforce Connected Apps <https://help.salesforce.com/s/articleView?id=sf.connected_app_overview.htm>`_
