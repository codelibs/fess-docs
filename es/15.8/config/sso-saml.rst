=============================================
Configuración de SSO con autenticación SAML
=============================================

Descripción general
===================

|Fess| soporta autenticación Single Sign-On (SSO) utilizando SAML (Security Assertion Markup Language) 2.0.
Al utilizar autenticación SAML, la información del usuario autenticada por un IdP (Identity Provider) puede integrarse con |Fess|, permitiendo mostrar resultados de búsqueda basados en los permisos del usuario cuando se combina con la búsqueda basada en roles.

Cómo funciona la autenticación SAML
-----------------------------------

En la autenticación SAML, |Fess| opera como un SP (Service Provider) y colabora con un IdP externo para la autenticación.

1. El usuario accede al endpoint SSO de |Fess| (``/sso/``)
2. |Fess| redirige la solicitud de autenticación al IdP
3. El usuario se autentica en el IdP
4. El IdP envía la aserción SAML a |Fess|
5. |Fess| valida la aserción e inicia sesión del usuario

Para la integración con búsqueda basada en roles, consulte :doc:`security-role`.

Prerrequisitos
==============

Antes de configurar la autenticación SAML, verifique los siguientes prerrequisitos:

- |Fess| 15.8 o superior está instalado
- Un IdP (Identity Provider) compatible con SAML 2.0 está disponible
- |Fess| es accesible a través de HTTPS (requerido para entornos de producción)
- Tiene permiso para registrar |Fess| como SP en el lado del IdP

Ejemplos de IdP soportados:

- Microsoft Entra ID (Azure AD)
- Okta
- Google Workspace
- Keycloak
- OneLogin
- Otros IdP compatibles con SAML 2.0

Configuración básica
====================

Habilitar SSO
-------------

Para habilitar la autenticación SAML, agregue la siguiente configuración en ``app/WEB-INF/conf/system.properties``:

::

    sso.type=saml

.. note::
   ``sso.type`` y la configuración SAML básica (información del IdP, información del SP, mapeo de atributos de usuario) también pueden configurarse desde la página «Sistema > General» del panel de administración.
   Los cambios realizados en el panel de administración se guardan en ``system.properties`` y se conservan tras el reinicio.
   Sin embargo, los ajustes de seguridad como firma/cifrado y el certificado/clave privada del SP no pueden configurarse desde el panel de administración, por lo que deben escribirse directamente en ``system.properties``.

Configuración del SP (Service Provider)
---------------------------------------

Para configurar |Fess| como SP, especifique la URL base del SP.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``saml.sp.base.url``
     - URL base del SP
     - ``http://localhost:8080``

.. note::
   El valor por defecto de ``saml.sp.base.url`` es ``http://localhost:8080``.
   Fuera de entornos de prueba, establezca siempre la URL utilizada para acceder a |Fess| externamente (HTTPS en producción).

Esta configuración configura automáticamente los siguientes endpoints:

- **Entity ID**: ``{saml.sp.base.url}/sso/metadata``
- **ACS URL**: ``{saml.sp.base.url}/sso/``
- **SLO URL**: ``{saml.sp.base.url}/sso/logout``

Ejemplo::

    saml.sp.base.url=https://fess.example.com

Configuración de URL individual
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Normalmente, al configurar ``saml.sp.base.url`` cada URL de endpoint se configura automáticamente, pero si es necesario puede anular las URLs individuales explícitamente con las siguientes propiedades.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``saml.sp.entityid``
     - Entity ID del SP
     - ``{saml.sp.base.url}/sso/metadata``
   * - ``saml.sp.assertion_consumer_service.url``
     - URL del servicio Assertion Consumer
     - ``{saml.sp.base.url}/sso/``
   * - ``saml.sp.single_logout_service.url``
     - URL del servicio Single Logout
     - ``{saml.sp.base.url}/sso/logout``

Configuración del IdP (Identity Provider)
-----------------------------------------

Configure la información obtenida de su IdP.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``saml.idp.entityid``
     - Entity ID del IdP
     - (Requerido)
   * - ``saml.idp.single_sign_on_service.url``
     - URL del servicio SSO del IdP
     - (Requerido)
   * - ``saml.idp.x509cert``
     - Certificado X.509 de firma del IdP (codificado en Base64, sin saltos de línea)
     - (Requerido)
   * - ``saml.idp.single_logout_service.url``
     - URL del servicio SLO del IdP
     - (Opcional)

.. note::
   Para ``saml.idp.x509cert``, especifique solo el contenido codificado en Base64 del certificado en una sola línea sin saltos de línea.
   No incluya las líneas ``-----BEGIN CERTIFICATE-----`` y ``-----END CERTIFICATE-----``.

Obtener metadatos del SP
------------------------

Después de iniciar |Fess|, puede obtener los metadatos del SP en formato XML desde el endpoint ``/sso/metadata``.

::

    https://fess.example.com/sso/metadata

Importe estos metadatos en su IdP, o registre manualmente el SP en el lado del IdP usando el contenido de los metadatos.

.. note::
   Para obtener los metadatos, primero debe completar la configuración SAML básica (``sso.type=saml`` y ``saml.sp.base.url``) e iniciar |Fess|.

Configuración del lado del IdP
==============================

Al registrar |Fess| como SP en el lado del IdP, configure la siguiente información:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Configuración
     - Valor
   * - ACS URL / Reply URL
     - ``https://<Host de Fess>/sso/``
   * - Entity ID / Audience URI
     - ``https://<Host de Fess>/sso/metadata``
   * - Name ID Format
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress`` (Recomendado)

Información a obtener del IdP
-----------------------------

Obtenga la siguiente información de la pantalla de configuración o metadatos de su IdP para usar en la configuración de |Fess|:

- **Entity ID del IdP**: URI que identifica al IdP
- **URL SSO (HTTP-Redirect)**: URL del endpoint de Single Sign-On
- **Certificado X.509**: Certificado de clave pública usado para verificación de firma de la aserción SAML

Mapeo de atributos de usuario
=============================

Puede mapear los atributos de usuario obtenidos de las aserciones SAML a grupos y roles de |Fess|.

Configuración de atributos de grupo
-----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``saml.attribute.group.name``
     - Nombre del atributo que contiene información de grupo
     - ``memberOf``
   * - ``saml.default.groups``
     - Grupos por defecto (separados por comas)
     - (Ninguno)

Ejemplo::

    saml.attribute.group.name=groups
    saml.default.groups=user

Configuración de atributos de rol
---------------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``saml.attribute.role.name``
     - Nombre del atributo que contiene información de rol
     - (Ninguno)
   * - ``saml.default.roles``
     - Roles por defecto (separados por comas)
     - (Ninguno)

Ejemplo::

    saml.attribute.role.name=roles
    saml.default.roles=viewer

.. note::
   Si los atributos no pueden obtenerse del IdP, se usarán los valores por defecto.
   Al usar búsqueda basada en roles, configure los grupos o roles apropiados.

Configuración de seguridad
==========================

Para entornos de producción, se recomienda habilitar las siguientes configuraciones de seguridad.

Configuración de firma
----------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``saml.security.authnrequest_signed``
     - Firmar solicitudes de autenticación
     - ``false``
   * - ``saml.security.want_messages_signed``
     - Requerir firmas de mensajes
     - ``false``
   * - ``saml.security.want_assertions_signed``
     - Requerir firmas de aserciones
     - ``false``
   * - ``saml.security.logoutrequest_signed``
     - Firmar solicitudes de cierre de sesión
     - ``false``
   * - ``saml.security.logoutresponse_signed``
     - Firmar respuestas de cierre de sesión
     - ``false``

.. warning::
   Las funciones de seguridad están deshabilitadas por defecto.
   Para entornos de producción, se recomienda encarecidamente configurar al menos ``saml.security.want_assertions_signed=true``.

Configuración de cifrado
------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``saml.security.want_assertions_encrypted``
     - Requerir cifrado de aserciones
     - ``false``
   * - ``saml.security.want_nameid_encrypted``
     - Requerir cifrado de NameID
     - ``false``

Configuración del certificado y clave privada del SP
----------------------------------------------------

Cuando el SP firma solicitudes de autenticación o mensajes de cierre de sesión (p. ej., ``saml.security.authnrequest_signed``), o solicita el cifrado de aserciones o NameID (p. ej., ``saml.security.want_assertions_encrypted``), debe configurar la clave privada y el certificado X.509 del SP.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``saml.sp.x509cert``
     - Certificado X.509 del SP (codificado en Base64, sin saltos de línea)
     - (vacío)
   * - ``saml.sp.privatekey``
     - Clave privada del SP (codificada en Base64, sin saltos de línea)
     - (vacío)

.. note::
   Para ``saml.sp.x509cert`` y ``saml.sp.privatekey``, al igual que con ``saml.idp.x509cert``, especifique el contenido codificado en Base64 en una sola línea sin saltos de línea (no incluya las líneas ``-----BEGIN ...-----`` y ``-----END ...-----``).
   Al habilitar la firma/cifrado, registre también el certificado del SP en el lado del IdP. El certificado del SP se publica en los metadatos del SP en ``/sso/metadata``.

Otras configuraciones de seguridad
----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``saml.strict``
     - Modo estricto (realizar validación estricta)
     - ``true``
   * - ``saml.security.want_xml_validation``
     - Validar el esquema XML de los mensajes
     - ``true``
   * - ``saml.security.signature_algorithm``
     - Algoritmo de firma
     - ``http://www.w3.org/2001/04/xmldsig-more#rsa-sha256``
   * - ``saml.security.requested_authncontext``
     - Contexto de autenticación solicitado
     - ``urn:oasis:names:tc:SAML:2.0:ac:classes:Password``
   * - ``saml.sp.nameidformat``
     - Formato del NameID
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``

.. note::
   |Fess| utiliza internamente una biblioteca SAML (java-saml), y las propiedades que comienzan con ``saml.`` se mapean a los ajustes correspondientes de la biblioteca (prefijo ``onelogin.saml2.``).
   Por lo tanto, además de los listados aquí, puede especificar ajustes detallados en ``system.properties``, como bindings (p. ej., ``saml.sp.assertion_consumer_service.binding``), información de organización (``saml.organization.*``) e información de contacto (``saml.contacts.*``).

Ejemplos de configuración
=========================

Configuración mínima (para pruebas)
-----------------------------------

El siguiente es un ejemplo de configuración mínima para verificación en un entorno de pruebas.

::

    # Habilitar SSO
    sso.type=saml

    # Configuración SP
    saml.sp.base.url=https://fess.example.com

    # Configuración IdP (establecer valores obtenidos de la consola de administración del IdP)
    saml.idp.entityid=https://idp.example.com/saml/metadata
    saml.idp.single_sign_on_service.url=https://idp.example.com/saml/sso
    saml.idp.x509cert=MIIDpDCCAoygAwIBAgI...(certificado codificado en Base64)

    # Grupos por defecto
    saml.default.groups=user

Configuración recomendada (para producción)
-------------------------------------------

El siguiente es un ejemplo de configuración recomendada para entornos de producción.

::

    # Habilitar SSO
    sso.type=saml

    # Configuración SP
    saml.sp.base.url=https://fess.example.com

    # Configuración IdP
    saml.idp.entityid=https://idp.example.com/saml/metadata
    saml.idp.single_sign_on_service.url=https://idp.example.com/saml/sso
    saml.idp.single_logout_service.url=https://idp.example.com/saml/logout
    saml.idp.x509cert=MIIDpDCCAoygAwIBAgI...(certificado codificado en Base64)

    # Mapeo de atributos de usuario
    saml.attribute.group.name=groups
    saml.attribute.role.name=roles
    saml.default.groups=user

    # Configuración de seguridad (recomendado para producción)
    saml.security.want_assertions_signed=true
    saml.security.want_messages_signed=true

Solución de problemas
=====================

Problemas comunes y soluciones
------------------------------

No se puede regresar a Fess después de la autenticación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que la URL ACS esté configurada correctamente en el lado del IdP
- Asegúrese de que el valor de ``saml.sp.base.url`` coincida con la configuración del IdP

Error de verificación de firma
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que el certificado del IdP esté configurado correctamente
- Asegúrese de que el certificado no haya expirado
- El certificado debe especificarse solo como contenido codificado en Base64, sin saltos de línea

Grupos/roles de usuario no reflejados
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que los atributos estén configurados correctamente en el lado del IdP
- Asegúrese de que el valor de ``saml.attribute.group.name`` coincida con el nombre del atributo enviado por el IdP
- Habilite el modo de depuración para inspeccionar el contenido de la aserción SAML

Configuración de depuración
---------------------------

Para investigar problemas, puede habilitar el modo de depuración con la siguiente configuración:

::

    saml.debug=true

Al configurar ``saml.debug=true``, se imprime en el registro la razón detallada cuando falla la autenticación SAML.

También puede obtener registros SAML detallados agregando el siguiente logger a ``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.sso.saml" level="DEBUG"/>

Referencia
==========

- :doc:`security-role` - Configuración de búsqueda basada en roles
- :doc:`sso-oidc` - Configuración de SSO con OpenID Connect
- :doc:`sso-entraid` - Configuración de SSO exclusiva para Microsoft Entra ID
