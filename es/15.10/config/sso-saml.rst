=============================================
Configuración de SSO con autenticación SAML
=============================================

Descripción general
===================

|Fess| soporta autenticación Single Sign-On (SSO) utilizando SAML (Security Assertion Markup Language) 2.0.
Al utilizar autenticación SAML, la información del usuario autenticada por un IdP (Identity Provider) puede integrarse con |Fess|, permitiendo mostrar resultados de búsqueda basados en los permisos del usuario cuando se combina con la búsqueda basada en roles.

.. note::
   La compatibilidad con la autenticación SAML proviene del plugin ``fess-sso-saml``, que no
   forma parte de la distribución. Instálelo desde la página **Sistema > Plugin** de la
   pantalla de administración o con ``bin/fess-setup install plugin fess-sso-saml``.
   El plugin procesa los mensajes SAML con la biblioteca SAML `saml4j <https://github.com/codelibs/saml4j>`__.
   Hasta entonces, con ``sso.type=saml`` toda petición a ``/sso/`` solo se redirige de vuelta a
   la página de inicio de sesión.

Cómo funciona la autenticación SAML
-----------------------------------

En la autenticación SAML, |Fess| opera como un SP (Service Provider) y colabora con un IdP externo para la autenticación.

1. El usuario accede al endpoint SSO de |Fess| (``/sso/``)
2. |Fess| redirige la solicitud de autenticación al IdP
3. El usuario se autentica en el IdP
4. El IdP envía la aserción SAML a |Fess|
5. |Fess| valida la aserción e inicia sesión del usuario

.. note::
   Solo se admite el inicio de sesión iniciado por el SP, que comienza en el endpoint SSO de |Fess|
   (``/sso/``) tal como se describe arriba. |Fess| vincula cada respuesta SAML al identificador de la
   AuthnRequest que envió, por lo que una respuesta iniciada por el IdP (no solicitada), por ejemplo
   desde un icono de |Fess| en el panel de Okta o en el portal «Mis aplicaciones» de Microsoft Entra
   ID, no tiene ninguna AuthnRequest con la que emparejarse y se rechaza. Si coloca un icono en el
   lado del IdP, haga que apunte al endpoint ``/sso/`` de |Fess|.

   Tenga en cuenta que en 15.7 el inicio de sesión iniciado por el IdP funcionaba de forma incidental
   cuando se establecía ``tomcat.sameSiteCookies=none``: |Fess| devolvía al IdP la respuesta que no
   podía emparejar y el IdP entregaba de inmediato una aserción solicitada. En 15.8 ya no se devuelve
   la respuesta, por lo que el inicio de sesión iniciado por el IdP no funciona.

Para la integración con búsqueda basada en roles, consulte :doc:`security-role`.

.. note::
   Si ejecuta varios nodos, defina la variable de entorno ``FESS_SESSION_STORE=opensearch`` para compartir la sesión HTTP entre ellos; un inicio de sesión iniciado en un nodo podrá entonces completarse en otro. Actualice el plugin en cada nodo a 15.10 antes de activarlo: un plugin 15.9.0 no comparte el estado del inicio de sesión, y un usuario que vuelve a otro nodo permanece como anónimo. Sin una sesión compartida, haga que el balanceador de carga fije cada sesión a un nodo. Incluso con una sesión compartida se recomiendan las sesiones persistentes (consulte :doc:`session-store`).

   Con ``FESS_SESSION_STORE=opensearch``, añadir o quitar un plugin SSO (``fess-sso-saml``, ``fess-sso-oidc`` o ``fess-sso-entraid``) cambia la versión de formato de las sesiones almacenadas. Todas las sesiones almacenadas dejan entonces de ser válidas y todos los usuarios deben iniciar sesión de nuevo. Instale o quite estos plugins en todos los nodos: un nodo cuyo conjunto de estos plugins difiere del de los demás nodos no puede leer las sesiones que estos almacenaron, y ellos no pueden leer las suyas. Los demás plugins, como los de almacenamiento, de scripts y SPNEGO, no cambian el formato.

Prerrequisitos
==============

Antes de configurar la autenticación SAML, verifique los siguientes prerrequisitos:

- |Fess| 15.10 o superior está instalado
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

.. note::
   Los ajustes que comienzan por ``saml.`` se leen únicamente de ``system.properties``.
   Las propiedades de sistema de la JVM, como ``-Dsaml.security....`` o ``-Dfess.saml.security....``, no se consultan.
   En particular, ``saml.security.*`` tampoco tiene ningún campo en el panel de administración,
   por lo que escribirlo directamente en ``system.properties`` es la única forma de configurarlo.

Configuración de la cookie de sesión
------------------------------------

El IdP devuelve la aserción a |Fess| mediante un **POST entre sitios**. Una cookie ``SameSite=Lax`` no se envía en ese tipo de petición, por lo que el inicio de sesión SAML no se completa con el valor predeterminado que incluye |Fess|.

Cambie ``tomcat.sameSiteCookies`` a ``none`` en ``tomcat_config.properties``. Este archivo se encuentra en ``lib/classes/`` en el paquete ZIP y en ``/etc/fess/`` en los paquetes DEB/RPM.

::

    tomcat.sameSiteCookies = none

.. warning::
   Los navegadores solo aceptan ``none`` en una cookie que además tenga el atributo ``Secure``, por lo que |Fess| debe servirse mediante HTTPS. Sobre HTTP simple, esta opción impide iniciar sesión en |Fess|.

.. note::
   El valor predeterminado ``lax`` está pensado para los métodos de SSO cuya respuesta vuelve como redirección (GET). El enlace HTTP-POST de SAML no lo es, por lo que este cambio solo es necesario al usar SAML. |Fess| debe reiniciarse tras cambiar la configuración.

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
   * - ``saml.idp.x509certMulti.1``, ``.2``, ...
     - Certificados de firma adicionales del IdP (por ejemplo, durante una rotación de claves)
     - (Opcional)

.. note::
   El certificado del IdP es el único ancla de confianza para las firmas; nunca se confía en un certificado incluido dentro de un mensaje.
   Los certificados del IdP y del SP deben ser claves RSA de al menos 2048 bits.
   ``saml.idp.x509cert`` puede omitirse cuando se establece ``saml.idp.x509certMulti.N``.

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

.. note::
   |Fess| comprueba lo siguiente en cada aserción. Las URL se derivan de ``saml.sp.base.url`` (o de las propiedades de URL individuales), no de la petición entrante.

   - La aserción incluye un ``AudienceRestriction`` que nombra el entity ID del SP
   - El ``Destination`` de una Response firmada y el ``Recipient`` del SubjectConfirmation son la URL del servicio Assertion Consumer

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

.. note::
   |Fess| utiliza directamente los valores de grupo de la aserción: no realiza ninguna consulta al
   directorio ni expande los grupos anidados (transitivos). Por lo tanto, que aparezcan los grupos
   padre depende únicamente de la configuración de claims del IdP, a diferencia de
   :doc:`sso-entraid`, donde |Fess| resuelve los grupos padre mediante la API de Microsoft Graph.

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

.. warning::
   Cuando se configura ``saml.attribute.role.name``, los valores de atributo enviados por el IdP se
   convierten directamente en roles de |Fess|. Como ``authentication.admin.roles`` en
   ``fess_config.properties`` tiene el valor predeterminado ``admin``, cualquier usuario cuyo
   atributo de rol contenga ``admin`` obtiene privilegios de administrador en |Fess|. Compruebe
   quién puede controlar el atributo de rol en el IdP y, si es necesario, cambie
   ``authentication.admin.roles`` por otro nombre.

IdP que repiten un nombre de atributo
-------------------------------------

Si el IdP reparte el mismo nombre de atributo entre varios elementos ``<Attribute>``, |Fess|
fusiona sus valores.

Keycloak envía aserciones con esta forma de manera predeterminada: sus mapeadores de roles y grupos
emiten un elemento ``<Attribute>`` por cada valor salvo que se active su opción ``single``, y toda
cuenta de Keycloak tiene varios roles de reino predeterminados. No se necesita ningún ajuste en |Fess| para esto.

Configuración de seguridad
==========================

Los siguientes ajustes de seguridad se leen de ``system.properties``.

.. note::
   Si permanecen ajustes que debilitan los valores predeterminados (``saml.security.want_logout_signed=false``
   con el cierre de sesión único configurado, ``saml.security.allow_deprecated_alg=true`` o
   ``saml.security.allow_rsa_1_5=true``), se escribe en el registro una advertencia
   ``Insecure SAML settings: ...`` al cargar la configuración SAML.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``saml.session.end_with_idp``
     - Finalizar el inicio de sesión de |Fess| cuando termina la sesión del IdP, en el ``SessionNotOnOrAfter`` de la aserción más ``saml.security.clock_drift``. ``false`` lo desactiva
     - ``true``

.. note::
   El ajuste no tiene efecto cuando el IdP no envía ``SessionNotOnOrAfter``. Cuando el IdP limita su sesión a un tiempo corto (el valor predeterminado en Keycloak es de 10 horas), los usuarios pueden ver cerrada su sesión antes que antes. Cerrar la sesión en el IdP no finaliza el inicio de sesión de |Fess| antes de ese momento.

Configuración de firma
----------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``saml.security.authnrequest_signed``
     - Firmar solicitudes de autenticación (requiere ``saml.sp.privatekey``)
     - ``false``
   * - ``saml.security.want_messages_signed``
     - Requerir que la Response esté firmada
     - ``false``
   * - ``saml.security.want_assertions_signed``
     - Requerir que la Assertion esté firmada
     - ``false``
   * - ``saml.security.want_logout_signed``
     - Requerir que los mensajes de cierre de sesión del IdP estén firmados
     - ``true``
   * - ``saml.security.allow_deprecated_alg``
     - Aceptar firmas SHA-1
     - ``false``
   * - ``saml.security.signature_algorithm``
     - Algoritmo de las firmas salientes: el URI de ``rsa-sha256``, ``rsa-sha384`` o ``rsa-sha512``
     - ``http://www.w3.org/2001/04/xmldsig-more#rsa-sha256``

.. note::
   Independientemente de estos ajustes, debe estar firmada la Response o la Assertion.
   Use ``saml.security.want_messages_signed`` o ``saml.security.want_assertions_signed`` para exigir la firma en el elemento que firma su IdP.
   La firma debe referenciar el elemento firmado mediante su propio ID y usar ``rsa-sha256``, ``rsa-sha384`` o ``rsa-sha512`` (o las variantes ECDSA).
   Las firmas SHA-1 se rechazan a menos que ``saml.security.allow_deprecated_alg=true``, así que confirme que su IdP firma con SHA-256 o superior.

.. note::
   Cuando se configura el cierre de sesión único (``saml.idp.single_logout_service.url``), la LogoutRequest y
   la LogoutResponse enviadas por el IdP deben estar firmadas con la clave de ``saml.idp.x509cert``
   (``saml.security.want_logout_signed=true`` es el valor predeterminado).
   Establezca ``saml.security.want_logout_signed=false`` solo para un IdP que no pueda firmarlas.
   El servicio de cierre de sesión único (``/sso/logout``) acepta el enlace de redirección (GET) y el enlace POST.
   Registre también en el IdP la URL ``/sso/logout`` para el enlace POST; una LogoutResponse
   que el IdP envía por POST al servicio Assertion Consumer no se reconoce.

Configuración de cifrado
------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``saml.security.want_assertions_encrypted``
     - Requerir cifrado de aserciones (requiere ``saml.sp.privatekey``)
     - ``false``
   * - ``saml.security.allow_rsa_1_5``
     - Aceptar el transporte de clave RSA 1.5 (requiere ``saml.sp.privatekey``). De lo contrario, solo se acepta OAEP
     - ``false``

.. note::
   Deje ``saml.security.allow_rsa_1_5`` en ``false`` a menos que su IdP solo pueda cifrar con RSA 1.5.

Configuración del certificado y clave privada del SP
----------------------------------------------------

Cuando el SP firma solicitudes de autenticación o mensajes de cierre de sesión (p. ej., ``saml.security.authnrequest_signed``), o solicita el cifrado de aserciones o NameID (p. ej., ``saml.security.want_assertions_encrypted``), debe configurar la clave privada (PKCS#8) y el certificado X.509 del SP.

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
   * - ``saml.security.requested_authncontext``
     - Contexto de autenticación solicitado (un valor vacío no solicita ninguno)
     - ``urn:oasis:names:tc:SAML:2.0:ac:classes:Password``
   * - ``saml.security.requested_authncontextcomparison``
     - Comparación para el contexto de autenticación solicitado (``exact``, ``minimum``, ``maximum`` o ``better``)
     - ``exact``
   * - ``saml.security.clock_drift``
     - Desfase de reloj tolerado al comprobar los periodos de validez (segundos, de 0 a 600)
     - ``120``
   * - ``saml.security.max_message_size``
     - Mayor tamaño de mensaje decodificado aceptado (bytes, de 1024 a 16777216)
     - ``1048576``
   * - ``saml.sp.nameidformat``
     - Formato del NameID
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``

.. note::
   La audiencia, el destinatario, el destino, el emisor y el periodo de validez de una aserción se comprueban siempre,
   y una respuesta debe corresponder a un inicio de sesión que |Fess| inició.
   Se rechaza una aserción que no tiene Audience o cuya Audience no nombra el entity ID del SP.
   La validación es siempre estricta: ``saml.strict=false`` se rechaza.

Propiedades que ya no se utilizan
---------------------------------

Las siguientes propiedades se ignoran. Se escribe en el registro una única advertencia que las nombra.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Propiedad
     - Ahora
   * - ``saml.security.reject_deprecated_alg``
     - Las firmas SHA-1 se rechazan por defecto; ``saml.security.allow_deprecated_alg=true`` las acepta
   * - ``saml.security.allowed_key_transport_algorithms``
     - Por defecto solo se acepta OAEP; ``saml.security.allow_rsa_1_5=true`` acepta también RSA 1.5
   * - ``saml.security.allow_duplicated_attribute_name``
     - Los atributos repetidos siempre se fusionan
   * - ``saml.security.reject_missing_audience``
     - Una aserción sin audiencia siempre se rechaza
   * - ``saml.idp.certfingerprint``, ``saml.idp.certfingerprint_algorithm``
     - Establezca ``saml.idp.x509cert``; una huella digital no es un ancla de confianza
   * - ``saml.security.sign_metadata``, ``saml.security.want_nameid_encrypted``, ``saml.security.want_xml_validation``, ``saml.security.logoutrequest_signed``, ``saml.security.logoutresponse_signed``, ``saml.security.digest_algorithm``, ``saml.keystore.*``, ``saml.contacts.*``, ``saml.organization.*``, ``saml.compress.*``, ``saml.parsing.*``, ``saml.unique_id_prefix``, las propiedades ``*.binding`` y ``*.response.url``
     - Ya no se utilizan

Cualquier otra propiedad ``saml.`` que la biblioteca no conozca detiene los inicios de sesión SAML con un mensaje que la nombra,
para que un ajuste de seguridad mal escrito no pase inadvertido. ``saml.debug`` se acepta y no tiene ningún efecto.

Expiración del AuthnRequest
===========================

|Fess| envía una AuthnRequest al IdP por cada acceso a ``/sso/`` y registra su identificador en la sesión.
La respuesta SAML devuelta por el IdP se valida frente al identificador registrado.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``saml.request.id.ttl``
     - Tiempo durante el que se conserva el identificador de una AuthnRequest sin respuesta (segundos)
     - ``3600``

El identificador registrado se descarta una vez transcurrido este periodo.
Si expira (por ejemplo, porque se dejó abierta la página de inicio de sesión del IdP), la aserción devuelta no puede emparejarse y el inicio de sesión falla una sola vez.

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
    # Requiera la firma en el elemento que firma su IdP
    # (saml.security.want_messages_signed=true para la Response)
    saml.security.want_assertions_signed=true

Solución de problemas
=====================

Problemas comunes y soluciones
------------------------------

No se puede regresar a Fess después de la autenticación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que la URL ACS esté configurada correctamente en el lado del IdP
- Asegúrese de que el valor de ``saml.sp.base.url`` coincida con la configuración del IdP
- La aserción SAML llega como un POST entre sitios desde el IdP. Cuando
  ``tomcat.sameSiteCookies`` en ``tomcat_config.properties`` es ``lax`` (el valor predeterminado), el
  navegador no envía la cookie de sesión con ella y el inicio de sesión falla una sola vez.
  En ese caso, configure ``tomcat.sameSiteCookies = none`` (``SameSite=None`` requiere HTTPS)
- Si el inicio de sesión tardó demasiado en el IdP, el identificador de AuthnRequest ya no está
  disponible cuando llega la aserción, por lo que el inicio de sesión falla una sola vez y hay que
  empezarlo de nuevo
- |Fess| no define ``session-timeout`` en ``app/WEB-INF/web.xml``, por lo que se aplica el valor
  predeterminado del contenedor de servlets, 30 minutos, más corto que los 3600 segundos de
  ``saml.request.id.ttl``, y la sesión se descarta antes. Aumentar solo ``saml.request.id.ttl`` no da
  a los usuarios más tiempo para completar el inicio de sesión en el IdP, así que amplíe también el
  tiempo de espera de la sesión

Falla la validación de Destination o Recipient
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El ``Destination`` de una Response firmada y el ``Recipient`` del SubjectConfirmation deben ser la
URL del servicio Assertion Consumer de |Fess|. Esa URL procede de ``saml.sp.base.url`` (o de
``saml.sp.assertion_consumer_service.url``), no de la petición que llega a |Fess|, por lo que un
proxy inverso que termina TLS no afecta a la comparación.

- Establezca ``saml.sp.base.url`` en la URL visible desde el exterior, incluidos el esquema y el puerto
- Registre la misma URL ACS (``{saml.sp.base.url}/sso/``) en el lado del IdP
- Si se anula ``saml.sp.entityid``, el IdP debe usar ese valor como Audience

Error de verificación de firma
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que el certificado del IdP esté configurado correctamente
- Asegúrese de que el certificado no haya expirado
- El certificado debe especificarse solo como contenido codificado en Base64, sin saltos de línea
- El certificado del IdP debe ser una clave RSA de al menos 2048 bits
- Debe estar firmada la Response o la Assertion, y la firma debe usar SHA-256 o superior
  (SHA-1 solo se acepta con ``saml.security.allow_deprecated_alg=true``)
- El motivo por el que se rechazó una respuesta se escribe en el registro como ``Authentication failed: <reason> - <detail>``

Grupos/roles de usuario no reflejados
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que los atributos estén configurados correctamente en el lado del IdP
- Asegúrese de que el valor de ``saml.attribute.group.name`` coincida con el nombre del atributo enviado por el IdP
- Con Microsoft Entra ID, el claim de grupos contiene los ``ObjectId`` (GUID) de los grupos salvo
  que se seleccione otro atributo de origen, por lo que los valores no coincidirán con los nombres
  de grupo
- Microsoft Entra ID omite por completo el claim de grupos cuando el usuario pertenece a más de 150
  grupos (los grupos anidados cuentan para este límite), y entonces |Fess| recurre a
  ``saml.default.groups``
- Compare los nombres de atributo con los de la aserción que el IdP envía realmente

Configuración del registro
--------------------------

Cuando falla la autenticación SAML, el motivo se escribe siempre en el registro como advertencia.
La propiedad ``saml.debug`` no tiene ningún efecto.

Para obtener registros SAML detallados, agregue el siguiente logger a ``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.sso.saml" level="DEBUG"/>

Referencia
==========

- :doc:`security-role` - Configuración de búsqueda basada en roles
- :doc:`sso-oidc` - Configuración de SSO con OpenID Connect
- :doc:`sso-entraid` - Configuración de SSO exclusiva para Microsoft Entra ID
