==========================================
Configuración de SSO con OpenID Connect
==========================================

Descripción general
===================

|Fess| soporta autenticación Single Sign-On (SSO) utilizando OpenID Connect (OIDC).
OpenID Connect es un protocolo de autenticación basado en OAuth 2.0 que utiliza ID Tokens (JWT) para la autenticación de usuarios.
Al utilizar autenticación OpenID Connect, la información del usuario autenticada por un OpenID Provider (OP) puede integrarse con |Fess|.

Cómo funciona la autenticación OpenID Connect
----------------------------------------------

En la autenticación OpenID Connect, |Fess| opera como Relying Party (RP) y colabora con un OpenID Provider (OP) externo para la autenticación.

1. El usuario accede al endpoint SSO de |Fess| (``/sso/``)
2. |Fess| redirige al endpoint de autorización del OP
3. El usuario se autentica en el OP
4. El OP redirige el código de autorización a |Fess|
5. |Fess| utiliza el código de autorización para obtener un ID Token del endpoint de token
6. |Fess| obtiene la información del usuario del ID Token (JWT) e inicia sesión del usuario

.. note::
   |Fess| utiliza el flujo de código de autorización (Authorization Code Flow). El ID Token se obtiene directamente desde el endpoint de token a través de un canal de retaguardia (comunicación servidor a servidor) entre |Fess| y el OP, sin pasar por el navegador.
   |Fess| decodifica el ID Token y extrae los claims (como ``email`` y ``groups``) para construir la información del usuario, pero no realiza la verificación criptográfica de la firma JWT.
   Por este motivo, la comunicación con el endpoint de token debe realizarse siempre mediante HTTPS, y asegúrese de que la ruta de comunicación entre |Fess| y el OP sea de confianza.

Para la integración con búsqueda basada en roles, consulte :doc:`security-role`.

Prerrequisitos
==============

Antes de configurar la autenticación OpenID Connect, verifique los siguientes prerrequisitos:

- |Fess| 15.7 o superior está instalado
- Un proveedor compatible con OpenID Connect (OP) está disponible
- |Fess| es accesible a través de HTTPS (requerido para entornos de producción)
- Tiene permiso para registrar |Fess| como cliente (RP) en el lado del OP

Ejemplos de proveedores soportados:

- Microsoft Entra ID (Azure AD)
- Google Workspace / Google Cloud Identity
- Okta
- Keycloak
- Auth0
- Otros proveedores compatibles con OpenID Connect

Configuración básica
====================

Habilitar SSO
-------------

Para habilitar la autenticación OpenID Connect, agregue la siguiente configuración en ``app/WEB-INF/conf/system.properties``:

::

    sso.type=oic

.. note::
   Los ajustes de ``sso.type`` y los de ``oic.*`` descritos a continuación también pueden configurarse y modificarse desde la página "Sistema > General" de la pantalla de administración.
   Los cambios realizados en la pantalla de administración se guardan en ``system.properties`` y se conservan tras el reinicio.

Configuración del proveedor
---------------------------

Configure la información obtenida de su OP.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``oic.auth.server.url``
     - URL del endpoint de autorización
     - ``https://accounts.google.com/o/oauth2/auth``
   * - ``oic.token.server.url``
     - URL del endpoint de token
     - ``https://accounts.google.com/o/oauth2/token``

.. note::
   Estas URLs se pueden obtener del endpoint Discovery del OP (``/.well-known/openid-configuration``).

Configuración del cliente
-------------------------

Configure la información del cliente registrada con el OP.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``oic.client.id``
     - ID de cliente
     - (vacío)
   * - ``oic.client.secret``
     - Secreto del cliente
     - (vacío)
   * - ``oic.scope``
     - Scopes solicitados
     - (vacío)

.. note::
   El scope debe incluir al menos ``openid``.
   Para recuperar la dirección de correo electrónico del usuario, especifique ``openid email``.

Configuración de URL de redirección
------------------------------------

Configure la URL de callback después de la autenticación.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``oic.redirect.url``
     - URL de redirección (URL de callback)
     - ``{oic.base.url}/sso/``
   * - ``oic.base.url``
     - URL base de |Fess|
     - ``http://localhost:8080``

.. note::
   Si ``oic.redirect.url`` se omite, se construye automáticamente a partir de ``oic.base.url``.
   Para entornos de producción, configure ``oic.base.url`` con una URL HTTPS.

Configuración de atributos de usuario
--------------------------------------

Configure los grupos y roles por defecto que se asignarán a los usuarios autenticados con OIDC.
El ID de usuario, los grupos y los roles se determinan de la siguiente manera:

- **ID de usuario**: se obtiene del claim ``email`` del ID Token (JWT). Por este motivo, en la práctica es necesario incluir ``email`` en el scope (si no se puede obtener el claim ``email``, el inicio de sesión no funcionará correctamente).
- **Grupos**: se obtienen del claim ``groups`` del ID Token. Si el claim ``groups`` no existe, se utiliza el valor de ``oic.default.groups``.
- **Roles**: siempre se utiliza el valor de ``oic.default.roles`` (no existe mecanismo para obtener roles desde los claims del ID Token).

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``oic.default.groups``
     - Grupos por defecto (separados por comas)
     - (vacío)
   * - ``oic.default.roles``
     - Roles por defecto (separados por comas)
     - (vacío)

.. note::
   Si utiliza búsqueda basada en roles, debe asignar los grupos o roles apropiados al usuario.
   Para más detalles, consulte :doc:`security-role`.

Configuración del lado del OP
==============================

Al registrar |Fess| como cliente (RP) en el lado del OP, configure la siguiente información:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Configuración
     - Valor
   * - Tipo de aplicación
     - Aplicación web
   * - URI de redirección / URL de callback
     - ``https://<Host de Fess>/sso/``
   * - Scopes permitidos
     - ``openid`` y scopes requeridos (``email``, ``profile``, etc.)

Información a obtener del OP
-----------------------------

Obtenga la siguiente información de la pantalla de configuración o endpoint Discovery del OP para usar en la configuración de |Fess|:

- **Endpoint de autorización (Authorization Endpoint)**: URL para iniciar la autenticación del usuario
- **Endpoint de token (Token Endpoint)**: URL para obtener tokens
- **ID de cliente**: Identificador de cliente emitido por el OP
- **Secreto del cliente**: Clave secreta utilizada para la autenticación del cliente

.. note::
   La mayoría de los OP le permiten verificar las URLs de los endpoints de autorización y token desde el
   endpoint Discovery (``https://<OP>/.well-known/openid-configuration``).

Ejemplos de configuración
=========================

Configuración mínima (para pruebas)
-------------------------------------

El siguiente es un ejemplo de configuración mínima para verificación en un entorno de pruebas.

::

    # Habilitar SSO
    sso.type=oic

    # Configuración del proveedor (establecer valores obtenidos del OP)
    oic.auth.server.url=https://op.example.com/authorize
    oic.token.server.url=https://op.example.com/token

    # Configuración del cliente
    oic.client.id=your-client-id
    oic.client.secret=your-client-secret
    oic.scope=openid email

    # URL de redirección (entorno de pruebas)
    oic.redirect.url=http://localhost:8080/sso/

Configuración recomendada (para producción)
--------------------------------------------

El siguiente es un ejemplo de configuración recomendada para entornos de producción.

::

    # Habilitar SSO
    sso.type=oic

    # Configuración del proveedor
    oic.auth.server.url=https://op.example.com/authorize
    oic.token.server.url=https://op.example.com/token

    # Configuración del cliente
    oic.client.id=your-client-id
    oic.client.secret=your-client-secret
    oic.scope=openid email profile

    # URL base (usar HTTPS para producción)
    oic.base.url=https://fess.example.com

Solución de problemas
=====================

Problemas comunes y soluciones
--------------------------------

No se puede regresar a |Fess| después de la autenticación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que la URI de redirección esté configurada correctamente en el lado del OP
- Asegúrese de que el valor de ``oic.redirect.url`` o ``oic.base.url`` coincida con la configuración del OP
- Verifique que el protocolo (HTTP/HTTPS) coincida

Ocurren errores de autenticación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que el ID de cliente y el secreto del cliente estén configurados correctamente
- Asegúrese de que el scope incluya ``openid``
- Verifique que la URL del endpoint de autorización y la URL del endpoint de token sean correctas

No se puede recuperar información del usuario
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Asegúrese de que el scope incluya los permisos requeridos (``email``, ``profile``, etc.)
- Verifique que los scopes requeridos estén permitidos para el cliente en el lado del OP

Configuración de depuración
-----------------------------

Para investigar problemas, puede mostrar logs detallados relacionados con OpenID Connect ajustando el nivel de log de |Fess|.

En ``app/WEB-INF/classes/log4j2.xml``, puede agregar el siguiente logger para cambiar el nivel de log:

::

    <Logger name="org.codelibs.fess.sso.oic" level="DEBUG"/>

Referencia
==========

- :doc:`security-role` - Configuración de búsqueda basada en roles
- :doc:`sso-saml` - Configuración de SSO con autenticación SAML
- :doc:`sso-entraid` - Configuración de SSO específica para Microsoft Entra ID (si utiliza Entra ID, también puede usar la configuración dedicada en lugar de la configuración genérica de OpenID Connect)
