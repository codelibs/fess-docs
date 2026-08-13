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

.. note::
   Los ajustes que comienzan por ``saml.`` se leen únicamente de ``system.properties``.
   Las propiedades de sistema de la JVM, como ``-Dsaml.security....`` o ``-Dfess.saml.security....``, no se consultan.
   En particular, ``saml.security.*``, ``saml.strict`` y ``saml.debug`` tampoco tienen ningún campo en el panel de administración,
   por lo que escribirlos directamente en ``system.properties`` es la única forma de configurarlos.

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
rechaza la aserción y el inicio de sesión falla. La validación de la aserción -- firma, InResponseTo
y repetición -- ya se ha completado correctamente en ese punto; el rechazo ocurre al leer los
atributos, por lo que una configuración que no establece ``saml.attribute.role.name`` falla
exactamente igual.

Keycloak envía aserciones con esta forma de manera predeterminada: sus mapeadores de roles y grupos
emiten un elemento ``<Attribute>`` por cada valor salvo que se active su opción ``single``, y toda
cuenta de Keycloak tiene varios roles de reino predeterminados.

Hay dos soluciones:

- Agrupar los valores en un solo elemento en el IdP (en Keycloak, active la opción ``single`` de los
  mapeadores)
- Aceptar las repeticiones en |Fess| y fusionar sus valores

.. list-table::
   :header-rows: 1
   :widths: 45 40 15

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``saml.security.allow_duplicated_attribute_name``
     - Permite el mismo nombre de atributo en varios elementos y fusiona sus valores
     - ``false``

Ejemplo::

    saml.security.allow_duplicated_attribute_name=true

Configuración de seguridad
==========================

Para entornos de producción, se recomienda habilitar las siguientes configuraciones de seguridad.

.. note::
   Si permanecen configuraciones no recomendadas, se escribe en el registro una advertencia
   ``Insecure SAML settings: ...`` al cargar la configuración SAML.

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
   * - ``saml.security.reject_deprecated_alg``
     - Rechazar algoritmos de firma obsoletos como SHA-1
     - ``false``

.. warning::
   Las funciones de seguridad están deshabilitadas por defecto.
   Para entornos de producción, se recomienda encarecidamente configurar al menos ``saml.security.want_assertions_signed=true``.

.. note::
   Mientras ``saml.security.reject_deprecated_alg`` sea ``false``, también se aceptan aserciones y
   mensajes firmados con SHA-1 (``rsa-sha1`` y ``dsa-sha1``). No está habilitado por defecto porque
   activarlo hace que se rechacen los IdP que siguen firmando con SHA-1.
   Confirme que su IdP firma con SHA-256 o superior y, a continuación, configure
   ``saml.security.reject_deprecated_alg=true``.

.. warning::
   Cuando se configura el cierre de sesión único (``saml.idp.single_logout_service.url``), establezca
   siempre también ``saml.security.want_messages_signed=true``.
   Mientras sea ``false``, no se exige ninguna firma en una LogoutRequest recibida en ``/sso/logout``.
   Las únicas comprobaciones que se realizan son el esquema XML, ``NotOnOrAfter`` (si está presente),
   ``Destination`` (si está presente) y que el Issuer coincida con ``saml.idp.entityid`` (si está
   presente); el NameID de la LogoutRequest nunca se compara con el usuario que ha iniciado sesión.
   El elemento Issuer es opcional en el esquema SAML, por lo que una LogoutRequest que lo omita nunca
   se compara con el identificador de entidad del IdP. Por tanto, un atacante, sin necesidad de conocer
   el identificador de entidad del IdP, puede crear una LogoutRequest sin firmar y terminar la sesión
   de un usuario autenticado atrayéndolo a esa URL.
   El impacto es un cierre de sesión forzado (denegación de servicio), no una apropiación de la cuenta.

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
Si no se establece ningún valor, se usan 3600 segundos.
Si se establece un valor que no puede interpretarse como un número, también se usan 3600 segundos y se registra una advertencia que comienza por ``Invalid saml.request.id.ttl``.
Un valor igual o menor que cero descartaría el identificador de la AuthnRequest antes de que el inicio de sesión pudiera regresar del IdP, por lo que también en ese caso se usan 3600 segundos y se registra una advertencia.

.. note::
   Como máximo se conservan 10 AuthnRequest sin respuesta por sesión; al superar ese límite, se descartan las más antiguas.
   Esto existe para permitir iniciar sesiones desde varias pestañas a la vez, y no se puede cambiar con ningún ajuste ``saml.``.
   Si el límite se sobrescribe con un valor de cero o menos, se usan 10 en su lugar y se registra una advertencia.

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

    # Habilitar tras confirmar que el IdP firma con SHA-256 o superior
    saml.security.reject_deprecated_alg=true

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
  navegador no envía la cookie de sesión con ella, por lo que |Fess| no encuentra ninguna AuthnRequest
  con la que emparejar y el inicio de sesión falla una sola vez, en ese momento. El navegador vuelve a
  la página de inicio de sesión mostrando «Error en el proceso de inicio de sesión SSO.» y en el
  registro se escribe una advertencia que empieza por
  ``Received a SAML response with no matching AuthnRequest ID in the session``.
  En ese caso, configure ``tomcat.sameSiteCookies = none`` (``SameSite=None`` requiere HTTPS)
- Si el inicio de sesión tardó demasiado en el IdP, el identificador de AuthnRequest ya no está
  disponible cuando llega la aserción, por lo que el inicio de sesión falla una sola vez y hay que
  empezarlo de nuevo. La advertencia que aparece indica qué caducó: una que empieza por
  ``Received a SAML response after the session it belongs to had expired`` significa que el
  contenedor de servlets descartó la sesión entera, mientras que una que contiene
  ``pending AuthnRequest ID(s) of the session had expired`` significa que la sesión sigue activa y
  que solo expiró ``saml.request.id.ttl``. Ambas se registran únicamente cuando el navegador sí
  envió su cookie de sesión, que es lo que las distingue del caso SameSite anterior
- |Fess| no define ``session-timeout`` en ``app/WEB-INF/web.xml``, por lo que se aplica el valor
  predeterminado del contenedor de servlets, 30 minutos, más corto que los 3600 segundos de
  ``saml.request.id.ttl``. La sesión, y con ella el identificador de AuthnRequest que guarda, se
  descarta antes: aumentar solo ``saml.request.id.ttl`` no da a los usuarios más tiempo para
  completar el inicio de sesión en el IdP, así que amplíe también el tiempo de espera de la sesión.
  Por eso la advertencia de ``saml.request.id.ttl`` solo aparece donde el TTL se ha configurado por
  debajo del tiempo de espera de la sesión

.. note::
   En 15.7, la misma situación hacía que |Fess| redirigiera una y otra vez al IdP, dejando el inicio de
   sesión en un bucle. En 15.8 falla una sola vez en lugar de entrar en bucle. La solución de
   configuración no cambia.

La validación de Destination falla detrás de un proxy inverso
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cuando |Fess| se ejecuta detrás de un proxy inverso o balanceador de carga que termina TLS, la
validación de la aserción puede fallar aunque ``saml.sp.base.url`` esté configurado correctamente.

La causa es que la biblioteca SAML compara el atributo ``Destination`` de la aserción con la URL de la
solicitud reconstruida por el contenedor de servlets, y no con la URL ACS configurada. Cuando el proxy
termina HTTPS, la URL de solicitud que ve |Fess| es interna, como
``http://<host-interno>:<puerto-interno>/sso/``, y no coincide con la
``https://fess.example.com/sso/`` enviada por el IdP. ``saml.sp.base.url`` no se utiliza para esta
comparación, por lo que configurarlo por sí solo no resuelve el problema.

Configure ``saml.debug=true`` para que el motivo se escriba en el registro:

::

    The response was received at http://... instead of https://fess.example.com/sso/

Ajuste la configuración del conector en ``tomcat_config.properties`` al esquema y puerto visibles desde
el exterior. Estos ajustes se distribuyen comentados:

::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.proxyPort=443

Configure además el proxy inverso para que transmita a |Fess| la cabecera ``Host`` original, ya que la
parte del nombre de host de la URL de solicitud se construye a partir de esa cabecera. Es necesario
reiniciar |Fess| después de modificar ``tomcat_config.properties``.

La misma validación se aplica a los mensajes de cierre de sesión único, así que configúrelo también si
utiliza SLO.

Error de verificación de firma
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que el certificado del IdP esté configurado correctamente
- Asegúrese de que el certificado no haya expirado
- El certificado debe especificarse solo como contenido codificado en Base64, sin saltos de línea

El inicio de sesión falla por un nombre de atributo repetido
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Si el registro contiene una advertencia que comienza por ``The IdP repeated an attribute name in
  the SAML assertion``, el IdP está repartiendo el mismo nombre de atributo entre varios elementos
  ``<Attribute>``
- La aserción en sí superó la validación, por lo que el certificado y el desfase horario no son la causa
- Agrupe los atributos en el IdP o establezca ``saml.security.allow_duplicated_attribute_name=true``

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
