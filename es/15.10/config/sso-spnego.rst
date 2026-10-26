====================================================
Configuración de SSO con Auth Integrada de Windows
====================================================

Descripción general
===================

|Fess| soporta autenticación Single Sign-On (SSO) utilizando Autenticación Integrada de Windows (SPNEGO/Kerberos).
Al utilizar la Autenticación Integrada de Windows, los usuarios que han iniciado sesión en una computadora unida al dominio Windows pueden acceder a |Fess| sin operaciones de inicio de sesión adicionales.

.. note::
   La compatibilidad con la Autenticación Integrada de Windows proviene del plugin
   ``fess-sso-spnego``, que no forma parte de la distribución. Instálelo desde la página
   **Sistema > Plugin** de la pantalla de administración o con
   ``bin/fess-setup install plugin fess-sso-spnego``.
   Hasta entonces, con ``sso.type=spnego`` toda petición a ``/sso/`` solo se redirige de vuelta
   a la página de inicio de sesión.

Cómo funciona la Autenticación Integrada de Windows
----------------------------------------------------

En la Autenticación Integrada de Windows, |Fess| utiliza el protocolo SPNEGO (Simple and Protected GSSAPI Negotiation Mechanism) para la autenticación Kerberos.

1. El usuario inicia sesión en el dominio Windows
2. El usuario accede a |Fess|
3. |Fess| envía un desafío SPNEGO
4. El navegador obtiene un ticket Kerberos y lo envía al servidor
5. |Fess| valida el ticket y recupera el nombre de usuario
6. La información de grupo del usuario se recupera vía LDAP
7. El usuario inicia sesión y la información de grupo se aplica a la búsqueda basada en roles

Para la integración con la búsqueda basada en roles, consulte :doc:`security-role`.

Prerrequisitos
==============

Antes de configurar la Autenticación Integrada de Windows, verifique los siguientes prerrequisitos:

- |Fess| 15.10 o superior está instalado
- Un servidor Active Directory (AD) está disponible
- El servidor |Fess| es accesible desde el dominio AD
- Tiene permiso para configurar Nombres de Principal de Servicio (SPN) en AD
- Una cuenta para recuperar información de usuario vía LDAP está disponible

Configuración del lado de Active Directory
==========================================

Registro del Nombre de Principal de Servicio (SPN)
---------------------------------------------------

Necesita registrar un SPN para |Fess| en Active Directory.
Abra un símbolo del sistema en una computadora Windows unida al dominio AD y ejecute el comando ``setspn``.

::

    setspn -S HTTP/<nombre de host del servidor Fess> <usuario de acceso AD>

Ejemplo:

::

    setspn -S HTTP/fess-server.example.local svc_fess

Para verificar el registro:

::

    setspn -L <usuario de acceso AD>

.. note::
   Después de registrar el SPN, si ejecutó el comando en el servidor Fess, cierre sesión en Windows y vuelva a iniciar sesión.

Configuración básica
====================

Habilitar SSO
-------------

Para habilitar la Autenticación Integrada de Windows, agregue la siguiente configuración en ``app/WEB-INF/conf/system.properties``:

::

    sso.type=spnego

Archivo de configuración de Kerberos
-------------------------------------

Cree ``app/WEB-INF/classes/krb5.conf`` con la configuración de Kerberos.

::

    [libdefaults]
        default_realm = EXAMPLE.LOCAL
        default_tkt_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128
        default_tgs_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128
        permitted_enctypes   = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128

    [realms]
        EXAMPLE.LOCAL = {
            kdc = AD-SERVER.EXAMPLE.LOCAL
            default_domain = EXAMPLE.LOCAL
        }

    [domain_realm]
        example.local = EXAMPLE.LOCAL
        .example.local = EXAMPLE.LOCAL

.. note::
   Reemplace ``EXAMPLE.LOCAL`` con su nombre de dominio AD (en mayúsculas) y ``AD-SERVER.EXAMPLE.LOCAL`` con el nombre de host de su servidor AD.

.. warning::
   Un ticket de servicio cifrado con un tipo que no aparece en ``permitted_enctypes`` es rechazado por
   el aceptador de Kerberos con ``encryption type not in permitted_enctypes list``.
   Active Directory suele emitir tickets de servicio AES256, por lo que AES256 debe estar incluido.

.. note::
   RC4 (``rc4-hmac``), 3DES y DES están deshabilitados de forma predeterminada en Java 17 y posteriores,
   por lo que incluirlos no tiene efecto; el ejemplo anterior especifica solo AES.
   ``aes256-cts-hmac-sha384-192`` y ``aes128-cts-hmac-sha256-128`` son los tipos AES-SHA2 (RFC 8009)
   compatibles con Windows Server 2025.
   Una cuenta de servicio que solo tiene una clave RC4 no puede usarse para la autenticación Kerberos;
   restablezca su contraseña para que se generen claves AES.

Archivo de configuración de inicio de sesión
---------------------------------------------

Cree ``app/WEB-INF/classes/auth_login.conf`` con la configuración de inicio de sesión JAAS.

::

    spnego-client {
        com.sun.security.auth.module.Krb5LoginModule required;
    };

    spnego-server {
        com.sun.security.auth.module.Krb5LoginModule required
        storeKey=true
        isInitiator=false;
    };

.. note::
   Los nombres de archivo predeterminados para ``krb5.conf`` y ``auth_login.conf`` están definidos en ``spnego.krb5.conf`` y ``spnego.login.conf`` respectivamente, pero los archivos en sí deben crearse obligatoriamente.
   SPNEGO se inicializa en el primer inicio de sesión, por lo que |Fess| arranca aunque falten estos archivos, pero el inicio de sesión SSO falla.

Configuración requerida
-----------------------

Agregue la siguiente configuración a ``app/WEB-INF/conf/system.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``spnego.preauth.username``
     - Nombre de usuario de conexión AD
     - (Requerido salvo que se use un keytab)
   * - ``spnego.preauth.password``
     - Contraseña de conexión AD
     - (Requerido salvo que se use un keytab)
   * - ``spnego.krb5.conf``
     - Ruta del archivo de configuración de Kerberos
     - ``krb5.conf``
   * - ``spnego.login.conf``
     - Ruta del archivo de configuración de inicio de sesión
     - ``auth_login.conf``

.. note::
   Si deja vacíos tanto ``spnego.preauth.username`` como ``spnego.preauth.password``, el módulo de
   inicio de sesión del servidor utiliza un keytab.
   Si no desea almacenar la contraseña de la cuenta de servicio de AD en un archivo de configuración
   de |Fess|, cree un keytab y configure ``spnego-server`` en ``auth_login.conf`` de la siguiente manera.

   ::

       spnego-server {
           com.sun.security.auth.module.Krb5LoginModule required
           useKeyTab=true
           keyTab="/var/lib/fess/fess.keytab"
           principal="HTTP/fess-server.example.local@EXAMPLE.LOCAL"
           storeKey=true
           isInitiator=false;
       };

Configuración opcional
----------------------

Las siguientes configuraciones pueden agregarse según sea necesario.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``spnego.login.client.module``
     - Nombre del módulo cliente
     - ``spnego-client``
   * - ``spnego.login.server.module``
     - Nombre del módulo servidor
     - ``spnego-server``
   * - ``spnego.allow.basic``
     - Permitir autenticación Basic
     - ``true``
   * - ``spnego.allow.unsecure.basic``
     - Permitir autenticación Basic no segura
     - ``false``
   * - ``spnego.prompt.ntlm``
     - Retroceder a autenticación Basic cuando se recibe un token NTLM
     - ``true``
   * - ``spnego.allow.localhost``
     - Permitir acceso desde localhost
     - ``false``
   * - ``spnego.allow.delegation``
     - Permitir delegación
     - ``false``
   * - ``spnego.allowed.realms``
     - Reinos Kerberos aceptados además del reino del servidor (separados por comas)
     - (Ninguno)
   * - ``spnego.logger.level``
     - Nivel de log interno de la biblioteca SPNEGO (``1`` =FINEST, ``2`` =FINER, ``3`` =FINE, ``4`` =CONFIG, ``6`` =WARNING, ``7`` =SEVERE; cualquier otro valor, incluidos ``0`` y ``5``, se trata como INFO)
     - (Automático)

.. warning::
   ``spnego.allow.unsecure.basic=true`` puede enviar credenciales codificadas en Base64 sobre conexiones no cifradas.
   Para entornos de producción, se recomienda encarecidamente establecer esto en ``false`` y usar HTTPS.

.. note::
   Con ``spnego.allow.unsecure.basic=false`` (valor predeterminado), la autenticación básica solo
   se ofrece en las peticiones en las que ``HttpServletRequest#isSecure()`` devuelve ``true``.
   Si TLS se termina en un proxy inverso y la petición se reenvía a |Fess| por HTTP, ese valor es
   ``false``, por lo que un cliente que no puede obtener un tique de Kerberos y recurre a NTLM no
   puede iniciar sesión. Establezca ``tomcat.secure=true`` en ``tomcat_config.properties`` para
   indicar a |Fess| que la petición llegó por HTTPS. Ese archivo se encuentra en ``lib/classes/``
   en la distribución ZIP y en ``/etc/fess/`` en los paquetes DEB/RPM, y hay que reiniciar |Fess|
   después de modificarlo.

.. warning::
   En |Fess| 15.8, un inicio de sesión se rechaza de forma predeterminada cuando el reino del
   principal del cliente difiere del reino del servidor. Si los usuarios inician sesión desde un
   dominio secundario de un árbol de dominios de AD o desde un bosque de confianza, indique esos
   reinos en ``spnego.allowed.realms``, separados por comas. De lo contrario, los usuarios que
   podían iniciar sesión hasta la versión 15.7 son rechazados con
   ``Kerberos realm is not allowed``.

.. warning::
   |Fess| identifica a un usuario por la parte del principal anterior a ``@``, por lo que el reino
   no forma parte del nombre de usuario. Cuando indica reinos adicionales en
   ``spnego.allowed.realms``, los usuarios que comparten un nombre de cuenta entre reinos — por
   ejemplo, ``alice@CORP.EXAMPLE.COM`` y ``alice@PARTNER.EXAMPLE.COM`` — pasan a ser el mismo
   usuario de |Fess| y comparten sus grupos, roles y permisos sobre los documentos. Añada un reino
   solo cuando el nombre de cuenta identifique exactamente a una persona en todos los reinos que
   indique.

.. note::
   La lista de permitidos también se aplica al retroceso a la autenticación Basic. Si un usuario
   introduce un nombre con la forma ``user@REALM``, ese reino se comprueba contra
   ``spnego.allowed.realms`` y el inicio de sesión se rechaza cuando no está permitido. Un nombre
   de cuenta simple, o la forma ``DOMAIN\user``, no indica ningún reino y se autentica en el reino
   predeterminado de ``krb5.conf``. Como un inicio de sesión Basic se autentica directamente contra
   el reino que el usuario escribe, mantenga la lista de permitidos al mínimo y considere
   establecer ``spnego.allow.basic`` en ``false`` si confía en ella como límite de seguridad.

.. note::
   Cuando ``spnego.prompt.ntlm=true`` (valor predeterminado), ``spnego.allow.basic`` también debe ser ``true``.
   Si establece ``spnego.allow.basic=false``, debe establecer también ``spnego.prompt.ntlm=false``.
   Si no se cumple esta condición, se producirá un error durante la inicialización de SPNEGO.

.. note::
   ``spnego.logger.level`` controla el nivel de log del logger interno de la biblioteca SPNEGO (el logger llamado ``Spnego`` de ``java.util.logging``).
   Si no se especifica, el nivel se determina automáticamente en función del nivel de log de |Fess|.

Límite de intentos fallidos de autenticación Basic
--------------------------------------------------

La alternativa de autenticación Basic envía al directorio una contraseña escrita por el usuario desde ``/sso/``, al que cualquiera puede acceder sin iniciar sesión, por lo que la versión 15.10 de |Fess| la limita.
Se aplican los límites y el bloqueo del formulario de inicio de sesión y de ``/api/v2/auth/login`` (consulte :doc:`rate-limiting`), y el contador de la dirección IP del cliente se comparte con ellos, de modo que alternar entre los endpoints no concede más intentos desde una misma dirección.
Los ajustes están en ``fess_config.properties`` (valores predeterminados entre paréntesis):

- ``theme.api.login.rate.limit.per.ip.per.minute`` (``10``): solicitudes Basic por minuto desde una dirección IP de cliente. Cada solicitud con un encabezado ``Authorization`` Basic usa un cupo, que un inicio de sesión correcto devuelve.
- ``theme.api.login.rate.limit.per.user.per.minute`` (``5``): contraseñas rechazadas por minuto para una combinación de dirección IP de cliente y cuenta. Cuando se han rechazado tantas, se rechazan las siguientes solicitudes Basic para esa cuenta desde esa dirección IP. Un inicio de sesión correcto borra el recuento.
- ``theme.api.login.lockout.seconds`` (``900``): durante cuánto tiempo queda bloqueada la dirección IP del cliente, o la combinación de dirección IP y cuenta, una vez superado un límite.

Mientras está bloqueado, una solicitud Basic se rechaza antes de comprobar la contraseña, por lo que ni siquiera la contraseña correcta permite iniciar sesión.
El navegador es enviado a la página de inicio de sesión con el error de inicio de sesión SSO, y se escribe una advertencia en ``fess.log`` cuando comienza el bloqueo.

La cuenta se cuenta solo por su nombre, sin distinguir mayúsculas de minúsculas y sin el sufijo ``@REALM`` ni el prefijo ``DOMAIN\``: ``alice``, ``ALICE``, ``alice@EXAMPLE.COM`` y ``EXAMPLE\alice`` cuentan como una sola cuenta, por lo que escribir el nombre de otra forma no da un nuevo cupo.
Como el recuento también es por dirección IP, nadie puede bloquear a un usuario desde otra dirección.
Se rechaza un nombre de usuario de más de 100 caracteres.
Un inicio de sesión que falla porque no se puede alcanzar el KDC cuenta como una contraseña rechazada.
Las solicitudes sin encabezado Basic, como el intercambio Negotiate, no se cuentan.

Detrás de un proxy inverso cuya dirección no está en ``rate.limit.trusted.proxies``, todos los clientes cuentan como una sola dirección IP, por lo que los fallos repetidos pueden bloquear a todos los usuarios (consulte :doc:`rate-limiting`).

Configuración LDAP
==================

La configuración LDAP es requerida para recuperar información de grupo de usuarios autenticados vía Autenticación Integrada de Windows.
Configure los ajustes LDAP en el panel de administración de |Fess| bajo "Sistema" -> "General".

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Elemento
     - Ejemplo
   * - URL LDAP
     - ``ldap://AD-SERVER.example.local:389``
   * - Base DN
     - ``dc=example,dc=local``
   * - Bind DN
     - ``svc_fess@example.local``
   * - Contraseña
     - Contraseña del usuario de acceso AD
   * - User DN
     - ``%s@example.local``
   * - Filtro de cuenta
     - ``(&(objectClass=user)(sAMAccountName=%s))``
   * - Atributo memberOf
     - ``memberOf``

.. note::
   |Fess| lee el atributo ``memberOf`` del usuario con un solo nivel de profundidad, por lo que los
   grupos anidados (un grupo que es miembro de otro grupo) no se expanden de forma predeterminada.
   Para reflejar los grupos anidados de AD, establezca ``(member:1.2.840.113556.1.4.1941:=%s)`` como
   Filtro de grupo (``ldap.group.filter``) en «Sistema» → «General» de la interfaz de administración.
   La expansión se ejecuta de forma asíncrona tras el inicio de sesión, por lo que la entrada de
   inicio de sesión del registro de auditoría solo contiene los grupos resueltos hasta ese momento.

Configuración del navegador
============================

Se requieren configuraciones del navegador del cliente para usar la Autenticación Integrada de Windows.

Internet Explorer / Microsoft Edge
-----------------------------------

1. Abrir Opciones de Internet
2. Seleccionar la pestaña "Seguridad"
3. Hacer clic en "Sitios" para la zona "Intranet local"
4. Hacer clic en "Opciones avanzadas" y agregar la URL de Fess
5. Hacer clic en "Nivel personalizado" para la zona "Intranet local"
6. Bajo "Autenticación de usuario" -> "Inicio de sesión", seleccionar "Inicio de sesión automático solo en la zona Intranet"
7. En la pestaña "Opciones avanzadas", marcar "Habilitar autenticación integrada de Windows"

Google Chrome
-------------

Chrome normalmente usa la configuración de Opciones de Internet de Windows.
Si se necesita configuración adicional, configure ``AuthServerAllowlist`` vía Política de Grupo o registro.

Mozilla Firefox
---------------

1. Ingresar ``about:config`` en la barra de direcciones
2. Buscar ``network.negotiate-auth.trusted-uris``
3. Establecer la URL o dominio del servidor Fess (ej: ``https://fess-server.example.local``)

Ejemplos de configuración
==========================

Configuración mínima (para pruebas)
------------------------------------

El siguiente es un ejemplo de configuración mínima para un entorno de pruebas.

``app/WEB-INF/conf/system.properties``:

::

    # Habilitar SSO
    sso.type=spnego

    # Configuración SPNEGO
    spnego.preauth.username=svc_fess
    spnego.preauth.password=your-password

``app/WEB-INF/classes/krb5.conf``:

::

    [libdefaults]
        default_realm = EXAMPLE.LOCAL
        default_tkt_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128
        default_tgs_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128
        permitted_enctypes   = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128

    [realms]
        EXAMPLE.LOCAL = {
            kdc = AD-SERVER.EXAMPLE.LOCAL
            default_domain = EXAMPLE.LOCAL
        }

    [domain_realm]
        example.local = EXAMPLE.LOCAL
        .example.local = EXAMPLE.LOCAL

``app/WEB-INF/classes/auth_login.conf``:

::

    spnego-client {
        com.sun.security.auth.module.Krb5LoginModule required;
    };

    spnego-server {
        com.sun.security.auth.module.Krb5LoginModule required
        storeKey=true
        isInitiator=false;
    };

Configuración recomendada (para producción)
--------------------------------------------

El siguiente es un ejemplo de configuración recomendada para entornos de producción.

``app/WEB-INF/conf/system.properties``:

::

    # Habilitar SSO
    sso.type=spnego

    # Configuración SPNEGO
    spnego.preauth.username=svc_fess
    spnego.preauth.password=your-secure-password
    spnego.krb5.conf=krb5.conf
    spnego.login.conf=auth_login.conf

    # Configuración de seguridad (producción)
    spnego.allow.basic=false
    spnego.allow.unsecure.basic=false
    spnego.prompt.ntlm=false
    spnego.allow.localhost=false

.. note::
   Al establecer ``spnego.allow.basic=false``, también debe establecer ``spnego.prompt.ntlm=false``.
   Como ``spnego.prompt.ntlm`` es ``true`` de forma predeterminada, omitir esta configuración provocará un error durante la inicialización.

Solución de problemas
=====================

Problemas comunes y soluciones
-------------------------------

Aparece el diálogo de autenticación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que el servidor Fess está agregado a la zona Intranet local en la configuración del navegador
- Verifique que "Habilitar autenticación integrada de Windows" está habilitado
- Verifique que el SPN está correctamente registrado (``setspn -L <nombre de usuario>``)

Ocurren errores de autenticación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que el nombre de dominio (mayúsculas) y el nombre del servidor AD en ``krb5.conf`` son correctos
- Verifique que ``spnego.preauth.username`` y ``spnego.preauth.password`` son correctos
- Verifique la conectividad de red al servidor AD

No se puede recuperar la información de grupo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que la configuración LDAP es correcta
- Verifique que el Bind DN y la contraseña son correctos
- Verifique que el usuario pertenece a grupos en AD

El inicio de sesión devuelve HTTP 400
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para un usuario que pertenece a muchos grupos, el ticket Kerberos (PAC) crece y la cabecera
``Authorization`` puede superar el límite predeterminado de Tomcat de 8 KB, que se responde con 400.
La petición nunca llega a |Fess|, por lo que no se registra nada en el log.
Aumente el límite en ``tomcat_config.properties``.

::

    tomcat.maxHttpHeaderSize=65536

La autenticación falla tras cambiar la contraseña de la cuenta de servicio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La credencial del servidor se obtiene en el primer inicio de sesión y, mientras no cambie ningún
ajuste ``spnego.*``, se almacena en caché durante toda la vida del proceso.
Reinicie |Fess| después de cambiar la contraseña de la cuenta de servicio en AD o de sustituir el
keytab. En cambio, un cambio en un ajuste ``spnego.*`` no requiere reiniciar, ya se guarde en la pantalla de administración o se haga editando ``system.properties``.
|Fess| compara los ajustes en cada inicio de sesión y, tras un cambio, vuelve a construir SPNEGO con los nuevos valores en el siguiente inicio de sesión.
Un handshake en curso durante la reconstrucción puede fallar una vez; el navegador lo reintenta.
Solo se comparan los ajustes: si sustituye un keytab, o edita únicamente el contenido de ``krb5.conf`` o del archivo de configuración de inicio de sesión sin cambiar ningún ajuste, sigue siendo necesario reiniciar, como se describe más arriba.

Configuración de depuración
-----------------------------

Para investigar problemas, puede mostrar logs detallados relacionados con SPNEGO.

Para obtener el log detallado interno de la biblioteca SPNEGO, agregue lo siguiente a ``app/WEB-INF/conf/system.properties``.
``spnego.logger.level=1`` produce el log más detallado (FINEST).

::

    spnego.logger.level=1

Para obtener el log detallado del procesamiento de integración SPNEGO del lado de |Fess| (paquete ``org.codelibs.fess.sso.spnego``), agregue el siguiente logger a ``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.sso.spnego" level="DEBUG"/>

.. note::
   Los logs de la propia biblioteca SPNEGO se emiten mediante ``java.util.logging`` y se controlan con ``spnego.logger.level``, no a través de ``log4j2.xml``.
   Los logs del procesamiento de integración del lado de |Fess| se controlan con el logger de ``log4j2.xml``.

Referencia
==========

- :doc:`security-role` - Configuración de búsqueda basada en roles
- :doc:`sso-saml` - Configuración de SSO con autenticación SAML
- :doc:`sso-oidc` - Configuración de SSO con autenticación OpenID Connect
- :doc:`sso-entraid` - Configuración de SSO con Microsoft Entra ID
