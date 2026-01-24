====================================================
Configuración de SSO con Auth Integrada de Windows
====================================================

Descripción general
===================

|Fess| soporta autenticación Single Sign-On (SSO) utilizando Autenticación Integrada de Windows (SPNEGO/Kerberos).
Al utilizar la Autenticación Integrada de Windows, los usuarios que han iniciado sesión en una computadora unida al dominio Windows pueden acceder a |Fess| sin operaciones de inicio de sesión adicionales.

Cómo funciona la Autenticación Integrada de Windows
---------------------------------------------------

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

- |Fess| 15.5 o superior está instalado
- Un servidor Active Directory (AD) está disponible
- El servidor |Fess| es accesible desde el dominio AD
- Tiene permiso para configurar Nombres de Principal de Servicio (SPN) en AD
- Una cuenta para recuperar información de usuario vía LDAP está disponible

Configuración del lado de Active Directory
===========================================

Registro del Nombre de Principal de Servicio (SPN)
--------------------------------------------------

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
------------------------------------

Cree ``app/WEB-INF/classes/krb5.conf`` con la configuración de Kerberos.

::

    [libdefaults]
        default_realm = EXAMPLE.LOCAL
        default_tkt_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        default_tgs_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        permitted_enctypes   = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc

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

Archivo de configuración de inicio de sesión
--------------------------------------------

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
     - (Requerido)
   * - ``spnego.preauth.password``
     - Contraseña de conexión AD
     - (Requerido)
   * - ``spnego.krb5.conf``
     - Ruta del archivo de configuración de Kerberos
     - ``krb5.conf``
   * - ``spnego.login.conf``
     - Ruta del archivo de configuración de inicio de sesión
     - ``auth_login.conf``

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
     - ``true``
   * - ``spnego.prompt.ntlm``
     - Mostrar solicitud NTLM
     - ``true``
   * - ``spnego.allow.localhost``
     - Permitir acceso localhost
     - ``true``
   * - ``spnego.allow.delegation``
     - Permitir delegación
     - ``false``
   * - ``spnego.exclude.dirs``
     - Directorios excluidos de autenticación (separados por comas)
     - (Ninguno)
   * - ``spnego.logger.level``
     - Nivel de log (0-7)
     - (Auto)

.. warning::
   ``spnego.allow.unsecure.basic=true`` puede enviar credenciales codificadas en Base64 sobre conexiones no cifradas.
   Para entornos de producción, se recomienda encarecidamente establecer esto en ``false`` y usar HTTPS.

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

Configuración del navegador
===========================

Se requieren configuraciones del navegador del cliente para usar la Autenticación Integrada de Windows.

Internet Explorer / Microsoft Edge
----------------------------------

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
=========================

Configuración mínima (para pruebas)
-----------------------------------

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
        default_tkt_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        default_tgs_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        permitted_enctypes   = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc

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
-------------------------------------------

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
    spnego.allow.localhost=false

Solución de problemas
=====================

Problemas comunes y soluciones
------------------------------

Aparece el diálogo de autenticación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que el servidor Fess está agregado a la zona Intranet local en la configuración del navegador
- Verifique que "Habilitar autenticación integrada de Windows" está habilitado
- Verifique que el SPN está correctamente registrado (``setspn -L <nombre de usuario>``)

Ocurren errores de autenticación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que el nombre de dominio (mayúsculas) y el nombre del servidor AD en ``krb5.conf`` son correctos
- Verifique que ``spnego.preauth.username`` y ``spnego.preauth.password`` son correctos
- Verifique la conectividad de red al servidor AD

No se puede recuperar la información de grupo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que la configuración LDAP es correcta
- Verifique que el Bind DN y la contraseña son correctos
- Verifique que el usuario pertenece a grupos en AD

Configuración de depuración
---------------------------

Para investigar problemas, puede mostrar logs detallados relacionados con SPNEGO ajustando el nivel de log de |Fess|.

Agregue lo siguiente a ``app/WEB-INF/conf/system.properties``:

::

    spnego.logger.level=1

O agregue los siguientes loggers a ``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.sso.spnego" level="DEBUG"/>
    <Logger name="org.codelibs.spnego" level="DEBUG"/>

Referencia
==========

- :doc:`security-role` - Configuración de búsqueda basada en roles
- :doc:`sso-saml` - Configuración de SSO con autenticación SAML
- :doc:`sso-oidc` - Configuración de SSO con autenticación OpenID Connect
- :doc:`sso-entraid` - Configuración de SSO con Microsoft Entra ID

