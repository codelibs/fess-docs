==================================
Conector Salesforce
==================================

Descripcion general
===================

El conector Salesforce proporciona la funcionalidad para obtener datos de objetos de Salesforce
(objetos estandar, objetos personalizados) y registrarlos en el indice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-salesforce``.

Objetos compatibles
===================

- **Objetos estandar**: Account, Contact, Lead, Opportunity, Case, Solution, etc.
- **Objetos personalizados**: Objetos creados por el usuario
- **Articulos de Knowledge**: Salesforce Knowledge

Requisitos previos
==================

1. Es necesario instalar el plugin
2. Es necesario crear una aplicacion conectada (Connected App) en Salesforce
3. Es necesario configurar la autenticacion OAuth
4. Se requiere acceso de lectura a los objetos

Instalacion del plugin
----------------------

Instale desde la pantalla de administracion en "Sistema" -> "Plugins".

O consulte :doc:`../../admin/plugin-guide` para mas detalles.

Configuracion
=============

Configure desde la pantalla de administracion en "Crawler" -> "Data Store" -> "Crear nuevo".

Configuracion basica
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

Configuracion de parametros
---------------------------

Autenticacion OAuth Token (recomendada):

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=1
    ignoreError=true
    custom=FessObj,CustomProduct
    FessObj.title=Name
    FessObj.contents=Name,Description__c
    CustomProduct.title=Product_Name__c
    CustomProduct.contents=Product_Name__c,Product_Description__c

Autenticacion OAuth Password:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_password
    username=admin@example.com
    client_id=3MVG9...
    client_secret=1234567890ABCDEF
    security_token=AbCdEfGhIjKlMnOpQrSt
    number_of_threads=1
    ignoreError=true

Lista de parametros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametro
     - Requerido
     - Descripcion
   * - ``base_url``
     - Si
     - URL de Salesforce (Produccion: ``https://login.salesforce.com``, Sandbox: ``https://test.salesforce.com``)
   * - ``auth_type``
     - Si
     - Tipo de autenticacion (``oauth_token`` o ``oauth_password``)
   * - ``username``
     - Si
     - Nombre de usuario de Salesforce
   * - ``client_id``
     - Si
     - Consumer Key de la aplicacion conectada
   * - ``private_key``
     - Para oauth_token
     - Clave privada (formato PEM, saltos de linea como ``\n``)
   * - ``client_secret``
     - Para oauth_password
     - Consumer Secret de la aplicacion conectada
   * - ``security_token``
     - Para oauth_password
     - Token de seguridad del usuario
   * - ``number_of_threads``
     - No
     - Numero de hilos de procesamiento paralelo (predeterminado: 1)
   * - ``ignoreError``
     - No
     - Continuar procesando en caso de error (predeterminado: true)
   * - ``custom``
     - No
     - Nombres de objetos personalizados (separados por comas)
   * - ``<objeto>.title``
     - No
     - Nombre del campo a usar para el titulo
   * - ``<objeto>.contents``
     - No
     - Nombres de campos a usar para el contenido (separados por comas)

Configuracion de scripts
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
     - Descripcion
   * - ``object.type``
     - Tipo del objeto (ej: Case, User, Solution)
   * - ``object.title``
     - Nombre del objeto
   * - ``object.description``
     - Descripcion del objeto
   * - ``object.content``
     - Contenido de texto del objeto
   * - ``object.id``
     - ID del objeto
   * - ``object.content_length``
     - Longitud del contenido
   * - ``object.created``
     - Fecha y hora de creacion
   * - ``object.last_modified``
     - Fecha y hora de ultima modificacion
   * - ``object.url``
     - URL del objeto
   * - ``object.thumbnail``
     - URL del thumbnail

Configuracion de aplicacion conectada de Salesforce
===================================================

1. Crear aplicacion conectada
-----------------------------

En Salesforce Setup:

1. Abrir "Application Manager"
2. Hacer clic en "New Connected App"
3. Ingresar informacion basica:

   - Nombre de aplicacion conectada: Fess Crawler
   - Nombre de API: Fess_Crawler
   - Email de contacto: your-email@example.com

4. Marcar "Enable OAuth Settings"

2. Configuracion de autenticacion OAuth Token (recomendada)
-----------------------------------------------------------

En configuracion OAuth:

1. Marcar "Use digital signatures"
2. Subir el certificado (crear segun los pasos a continuacion)
3. OAuth Scopes seleccionados:

   - Full access (full)
   - Perform requests on your behalf at any time (refresh_token, offline_access)

4. Hacer clic en "Save"
5. Copiar el Consumer Key

Creacion del certificado:

::

    # Generar clave privada
    openssl genrsa -out private_key.pem 2048

    # Generar certificado
    openssl req -new -x509 -key private_key.pem -out certificate.crt -days 365

    # Verificar clave privada
    cat private_key.pem

Suba el certificado (certificate.crt) a Salesforce y
configure el contenido de la clave privada (private_key.pem) en los parametros.

3. Configuracion de autenticacion OAuth Password
------------------------------------------------

En configuracion OAuth:

1. URL de callback: ``https://localhost`` (no se usa pero es requerido)
2. OAuth Scopes seleccionados:

   - Full access (full)
   - Perform requests on your behalf at any time (refresh_token, offline_access)

3. Hacer clic en "Save"
4. Copiar Consumer Key y Consumer Secret

Obtener el token de seguridad:

1. Abrir configuracion personal en Salesforce
2. Hacer clic en "Reset My Security Token"
3. Copiar el token enviado por email

4. Aprobacion de aplicacion conectada
-------------------------------------

En "Manage" -> "Manage Connected Apps":

1. Seleccionar la aplicacion conectada creada
2. Hacer clic en "Edit"
3. Cambiar "Permitted Users" a "Admin approved users are pre-authorized"
4. Asignar perfiles o conjuntos de permisos

Configuracion de objetos personalizados
=======================================

Crawl de objetos personalizados
-------------------------------

Especifique los nombres de objetos personalizados en el parametro ``custom``:

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

- ``<nombre_objeto>.title`` - Campo a usar para el titulo (campo unico)
- ``<nombre_objeto>.contents`` - Campos a usar para el contenido (multiples separados por comas)

Ejemplos de uso
===============

Crawl de objetos estandar
-------------------------

Parametros:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=1
    ignoreError=true

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

Parametros:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=2
    ignoreError=true
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

Parametros:

::

    base_url=https://test.salesforce.com
    auth_type=oauth_password
    username=admin@example.com.sandbox
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    client_secret=1234567890ABCDEF1234567890ABCDEF
    security_token=AbCdEfGhIjKlMnOpQrStUvWxYz
    number_of_threads=1
    ignoreError=true

Script:

::

    title="[SANDBOX] [" + object.type + "] " + object.title
    content=object.content
    timestamp=object.last_modified
    url=object.url

Solucion de problemas
=====================

Error de autenticacion
----------------------

**Sintoma**: ``Authentication failed`` o ``invalid_grant``

**Verificaciones**:

1. Para autenticacion OAuth Token:

   - Verificar que el Consumer Key sea correcto
   - Verificar que la clave privada este copiada correctamente (saltos de linea como ``\n``)
   - Confirmar que el certificado este subido a Salesforce
   - Verificar que el nombre de usuario sea correcto

2. Para autenticacion OAuth Password:

   - Verificar que Consumer Key y Consumer Secret sean correctos
   - Verificar que el token de seguridad sea correcto
   - Confirmar que la contrasena y el token de seguridad no esten concatenados (configurar por separado)

3. Comun:

   - Verificar que base_url sea correcta (entorno de produccion o Sandbox)
   - Confirmar que la aplicacion conectada este aprobada

No se obtienen objetos
----------------------

**Sintoma**: El crawl tiene exito pero hay 0 objetos

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

Verificacion de nombres de campo
--------------------------------

Verificar el API Name del campo personalizado:

1. Abrir "Fields & Relationships" del objeto
2. Seleccionar el campo personalizado
3. Copiar el "Field Name" (generalmente termina en ``__c``)

Ejemplo:

- Field Label: Product Description
- Field Name: Product_Description__c (usar este)

Limite de tasa de API
---------------------

**Sintoma**: ``REQUEST_LIMIT_EXCEEDED``

**Solucion**:

1. Reducir ``number_of_threads`` (configurar a 1)
2. Aumentar el intervalo de crawl
3. Verificar el uso de la API de Salesforce
4. Comprar limite de API adicional si es necesario

Gran volumen de datos
---------------------

**Sintoma**: El crawl toma mucho tiempo o tiene timeout

**Solucion**:

1. Dividir objetos en multiples data stores
2. Ajustar ``number_of_threads`` (aproximadamente 2-4)
3. Distribuir el horario de crawl
4. Mapear solo los campos necesarios

Error de formato de clave privada
---------------------------------

**Sintoma**: ``Invalid private key format``

**Solucion**:

Verificar que los saltos de linea en la clave privada sean correctamente ``\n``:

::

    # Formato correcto
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n

    # Formato incorrecto (contiene saltos de linea reales)
    private_key=-----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQE...
    -----END PRIVATE KEY-----

Informacion de referencia
=========================

- :doc:`ds-overview` - Descripcion general de conectores de Data Store
- :doc:`ds-database` - Conector de base de datos
- :doc:`../../admin/dataconfig-guide` - Guia de configuracion de Data Store
- `Salesforce REST API <https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/>`_
- `Salesforce OAuth 2.0 JWT Bearer Flow <https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_jwt_flow.htm>`_
- `Salesforce Connected Apps <https://help.salesforce.com/s/articleView?id=sf.connected_app_overview.htm>`_
