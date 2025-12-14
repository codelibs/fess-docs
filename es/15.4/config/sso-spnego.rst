====================================================
Configuracion de SSO con Auth Integrada de Windows
====================================================

Descripcion general
===================

|Fess| soporta autenticacion Single Sign-On (SSO) utilizando Autenticacion Integrada de Windows (SPNEGO/Kerberos).
Al utilizar la Autenticacion Integrada de Windows, los usuarios que han iniciado sesion en una computadora unida al dominio Windows pueden acceder a |Fess| sin operaciones de inicio de sesion adicionales.

Como funciona la Autenticacion Integrada de Windows
---------------------------------------------------

En la Autenticacion Integrada de Windows, |Fess| utiliza el protocolo SPNEGO (Simple and Protected GSSAPI Negotiation Mechanism) para la autenticacion Kerberos.

1. El usuario inicia sesion en el dominio Windows
2. El usuario accede a |Fess|
3. |Fess| envia un desafio SPNEGO
4. El navegador obtiene un ticket Kerberos y lo envia al servidor
5. |Fess| valida el ticket y recupera el nombre de usuario
6. La informacion de grupo del usuario se recupera via LDAP
7. El usuario inicia sesion y la informacion de grupo se aplica a la busqueda basada en roles

Para la integracion con la busqueda basada en roles, consulte :doc:`security-role`.

Prerrequisitos
==============

Antes de configurar la Autenticacion Integrada de Windows, verifique los siguientes prerrequisitos:

- |Fess| 15.4 o superior esta instalado
- Un servidor Active Directory (AD) esta disponible
- El servidor |Fess| es accesible desde el dominio AD
- Tiene permiso para configurar Nombres de Principal de Servicio (SPN) en AD
- Una cuenta para recuperar informacion de usuario via LDAP esta disponible

Configuracion del lado de Active Directory
===========================================

Registro del Nombre de Principal de Servicio (SPN)
--------------------------------------------------

Necesita registrar un SPN para |Fess| en Active Directory.
Abra un simbolo del sistema en una computadora Windows unida al dominio AD y ejecute el comando ``setspn``.

::

    setspn -S HTTP/<nombre de host del servidor Fess> <usuario de acceso AD>

Ejemplo:

::

    setspn -S HTTP/fess-server.example.local svc_fess

Para verificar el registro:

::

    setspn -L <usuario de acceso AD>

.. note::
   Despues de registrar el SPN, si ejecuto el comando en el servidor Fess, cierre sesion en Windows y vuelva a iniciar sesion.

Configuracion basica
====================

Habilitar SSO
-------------

Para habilitar la Autenticacion Integrada de Windows, agregue la siguiente configuracion en ``app/WEB-INF/conf/system.properties``:

::

    sso.type=spnego

Archivo de configuracion de Kerberos
------------------------------------

Cree ``app/WEB-INF/classes/krb5.conf`` con la configuracion de Kerberos.

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
   Reemplace ``EXAMPLE.LOCAL`` con su nombre de dominio AD (en mayusculas) y ``AD-SERVER.EXAMPLE.LOCAL`` con el nombre de host de su servidor AD.

Archivo de configuracion de inicio de sesion
--------------------------------------------

Cree ``app/WEB-INF/classes/auth_login.conf`` con la configuracion de inicio de sesion JAAS.

::

    spnego-client {
        com.sun.security.auth.module.Krb5LoginModule required;
    };

    spnego-server {
        com.sun.security.auth.module.Krb5LoginModule required
        storeKey=true
        isInitiator=false;
    };

Configuracion requerida
-----------------------

Agregue la siguiente configuracion a ``app/WEB-INF/conf/system.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Por defecto
   * - ``spnego.preauth.username``
     - Nombre de usuario de conexion AD
     - (Requerido)
   * - ``spnego.preauth.password``
     - Contrasena de conexion AD
     - (Requerido)
   * - ``spnego.krb5.conf``
     - Ruta del archivo de configuracion de Kerberos
     - ``krb5.conf``
   * - ``spnego.login.conf``
     - Ruta del archivo de configuracion de inicio de sesion
     - ``auth_login.conf``

Configuracion opcional
----------------------

Las siguientes configuraciones pueden agregarse segun sea necesario.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Por defecto
   * - ``spnego.login.client.module``
     - Nombre del modulo cliente
     - ``spnego-client``
   * - ``spnego.login.server.module``
     - Nombre del modulo servidor
     - ``spnego-server``
   * - ``spnego.allow.basic``
     - Permitir autenticacion Basic
     - ``true``
   * - ``spnego.allow.unsecure.basic``
     - Permitir autenticacion Basic no segura
     - ``true``
   * - ``spnego.prompt.ntlm``
     - Mostrar solicitud NTLM
     - ``true``
   * - ``spnego.allow.localhost``
     - Permitir acceso localhost
     - ``true``
   * - ``spnego.allow.delegation``
     - Permitir delegacion
     - ``false``
   * - ``spnego.exclude.dirs``
     - Directorios excluidos de autenticacion (separados por comas)
     - (Ninguno)
   * - ``spnego.logger.level``
     - Nivel de log (0-7)
     - (Auto)

.. warning::
   ``spnego.allow.unsecure.basic=true`` puede enviar credenciales codificadas en Base64 sobre conexiones no cifradas.
   Para entornos de produccion, se recomienda encarecidamente establecer esto en ``false`` y usar HTTPS.

Configuracion LDAP
==================

La configuracion LDAP es requerida para recuperar informacion de grupo de usuarios autenticados via Autenticacion Integrada de Windows.
Configure los ajustes LDAP en el panel de administracion de |Fess| bajo "Sistema" -> "General".

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
   * - Contrasena
     - Contrasena del usuario de acceso AD
   * - User DN
     - ``%s@example.local``
   * - Filtro de cuenta
     - ``(&(objectClass=user)(sAMAccountName=%s))``
   * - Atributo memberOf
     - ``memberOf``

Configuracion del navegador
===========================

Se requieren configuraciones del navegador del cliente para usar la Autenticacion Integrada de Windows.

Internet Explorer / Microsoft Edge
----------------------------------

1. Abrir Opciones de Internet
2. Seleccionar la pestana "Seguridad"
3. Hacer clic en "Sitios" para la zona "Intranet local"
4. Hacer clic en "Opciones avanzadas" y agregar la URL de Fess
5. Hacer clic en "Nivel personalizado" para la zona "Intranet local"
6. Bajo "Autenticacion de usuario" -> "Inicio de sesion", seleccionar "Inicio de sesion automatico solo en la zona Intranet"
7. En la pestana "Opciones avanzadas", marcar "Habilitar autenticacion integrada de Windows"

Google Chrome
-------------

Chrome normalmente usa la configuracion de Opciones de Internet de Windows.
Si se necesita configuracion adicional, configure ``AuthServerAllowlist`` via Politica de Grupo o registro.

Mozilla Firefox
---------------

1. Ingresar ``about:config`` en la barra de direcciones
2. Buscar ``network.negotiate-auth.trusted-uris``
3. Establecer la URL o dominio del servidor Fess (ej: ``https://fess-server.example.local``)

Ejemplos de configuracion
=========================

Configuracion minima (para pruebas)
-----------------------------------

El siguiente es un ejemplo de configuracion minima para un entorno de pruebas.

``app/WEB-INF/conf/system.properties``:

::

    # Habilitar SSO
    sso.type=spnego

    # Configuracion SPNEGO
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

Configuracion recomendada (para produccion)
-------------------------------------------

El siguiente es un ejemplo de configuracion recomendada para entornos de produccion.

``app/WEB-INF/conf/system.properties``:

::

    # Habilitar SSO
    sso.type=spnego

    # Configuracion SPNEGO
    spnego.preauth.username=svc_fess
    spnego.preauth.password=your-secure-password
    spnego.krb5.conf=krb5.conf
    spnego.login.conf=auth_login.conf

    # Configuracion de seguridad (produccion)
    spnego.allow.basic=false
    spnego.allow.unsecure.basic=false
    spnego.allow.localhost=false

Solucion de problemas
=====================

Problemas comunes y soluciones
------------------------------

Aparece el dialogo de autenticacion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que el servidor Fess esta agregado a la zona Intranet local en la configuracion del navegador
- Verifique que "Habilitar autenticacion integrada de Windows" esta habilitado
- Verifique que el SPN esta correctamente registrado (``setspn -L <nombre de usuario>``)

Ocurren errores de autenticacion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que el nombre de dominio (mayusculas) y el nombre del servidor AD en ``krb5.conf`` son correctos
- Verifique que ``spnego.preauth.username`` y ``spnego.preauth.password`` son correctos
- Verifique la conectividad de red al servidor AD

No se puede recuperar la informacion de grupo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que la configuracion LDAP es correcta
- Verifique que el Bind DN y la contrasena son correctos
- Verifique que el usuario pertenece a grupos en AD

Configuracion de depuracion
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

- :doc:`security-role` - Configuracion de busqueda basada en roles
- :doc:`sso-saml` - Configuracion de SSO con autenticacion SAML
- :doc:`sso-oidc` - Configuracion de SSO con autenticacion OpenID Connect
- :doc:`sso-entraid` - Configuracion de SSO con Microsoft Entra ID

