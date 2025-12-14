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

- |Fess| 14.0 o superior está instalado
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
     - (Requerido)

Esta configuración configura automáticamente los siguientes endpoints:

- **Entity ID**: ``{base_url}/sso/metadata``
- **ACS URL**: ``{base_url}/sso/``
- **SLO URL**: ``{base_url}/sso/logout``

Ejemplo::

    saml.sp.base.url=https://fess.example.com

Configuración de URL individual
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

También puede especificar las URLs individualmente en lugar de usar la URL base.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``saml.sp.entityid``
     - Entity ID del SP
     - (Requerido para config individual)
   * - ``saml.sp.assertion_consumer_service.url``
     - URL del servicio Assertion Consumer
     - (Requerido para config individual)
   * - ``saml.sp.single_logout_service.url``
     - URL del servicio Single Logout
     - (Opcional)

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

Otras configuraciones de seguridad
----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``saml.security.strict``
     - Modo estricto (realizar validación estricta)
     - ``true``
   * - ``saml.security.signature_algorithm``
     - Algoritmo de firma
     - ``http://www.w3.org/2000/09/xmldsig#rsa-sha1``
   * - ``saml.sp.nameidformat``
     - Formato del NameID
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``

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

    saml.security.debug=true

También puede ajustar los niveles de registro de |Fess| para mostrar registros SAML detallados.

Referencia
==========

- :doc:`security-role` - Configuración de búsqueda basada en roles
