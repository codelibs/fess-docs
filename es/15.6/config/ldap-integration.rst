==================================
Guia de integracion LDAP
==================================

Descripcion general
===================

|Fess| soporta la integracion con servidores LDAP (Lightweight Directory Access Protocol),
permitiendo autenticacion y gestion de usuarios en entornos empresariales.

La integracion LDAP permite:

- Autenticacion de usuarios con Active Directory u OpenLDAP
- Control de acceso basado en grupos
- Sincronizacion automatica de informacion de usuarios

Servidores LDAP compatibles
===========================

|Fess| soporta integracion con los siguientes servidores LDAP:

- Microsoft Active Directory
- OpenLDAP
- 389 Directory Server
- Apache Directory Server
- Otros servidores compatibles con LDAP v3

Requisitos previos
==================

- Acceso de red al servidor LDAP
- Cuenta de servicio para busquedas LDAP (Bind DN)
- Comprension de la estructura LDAP (Base DN, nombres de atributos, etc.)

Configuracion basica
====================

Agregue la siguiente configuracion en ``app/WEB-INF/conf/system.properties``.

Configuracion de conexion LDAP
------------------------------

::

    # Habilitar autenticacion LDAP
    ldap.admin.enabled=true

    # URL del servidor LDAP
    ldap.provider.url=ldap://ldap.example.com:389

    # Para conexion segura (LDAPS)
    # ldap.provider.url=ldaps://ldap.example.com:636

    # Base DN
    ldap.base.dn=dc=example,dc=com

    # Plantilla de DN de enlace para autenticacion de usuario (%s se reemplaza con el nombre de usuario)
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # DN de enlace de administracion (cuenta de servicio para busquedas LDAP)
    ldap.admin.security.principal=cn=fess,ou=services,dc=example,dc=com

    # Contrasena de enlace de administracion
    ldap.admin.security.credentials=your_password

Configuracion de busqueda de usuarios
-------------------------------------

::

    # Base DN para busqueda de usuarios
    ldap.user.search.base=ou=users,dc=example,dc=com

    # Filtro de busqueda de usuarios
    ldap.account.filter=(uid=%s)

    # Atributo de nombre de usuario
    ldap.user.name.attribute=uid

    # Filtro de busqueda de usuarios del administrador para la consola de gestion LDAP
    ldap.admin.user.filter=uid=%s

.. note::

   ``ldap.account.filter`` es el filtro de busqueda para la autenticacion de usuarios,
   mientras que ``ldap.admin.user.filter`` es el filtro de busqueda de usuarios para la
   consola de gestion LDAP. Configure cada uno adecuadamente ya que tienen propositos diferentes.

Configuracion de DN base de administracion LDAP
------------------------------------------------

::

    # DN base de busqueda de usuarios
    ldap.admin.user.base.dn=ou=People,dc=example,dc=com

    # DN base de busqueda de roles
    ldap.admin.role.base.dn=ou=Roles,dc=example,dc=com

    # DN base de busqueda de grupos
    ldap.admin.group.base.dn=ou=Groups,dc=example,dc=com

Configuracion de busqueda de grupos
-----------------------------------

::

    # Base DN para busqueda de grupos
    ldap.group.search.base=ou=groups,dc=example,dc=com

    # Filtro de busqueda de grupos
    ldap.group.filter=(member=%s)

    # Atributo de nombre de grupo
    ldap.group.name.attribute=cn

Configuracion de Active Directory
=================================

Ejemplo de configuracion para Microsoft Active Directory.

Configuracion basica
--------------------

::

    ldap.admin.enabled=true
    ldap.provider.url=ldap://ad.example.com:389
    ldap.base.dn=dc=example,dc=com

    # Plantilla de DN de enlace para autenticacion de usuario (formato UPN)
    ldap.security.principal=%s@example.com

    # DN de enlace de administracion (cuenta de servicio)
    ldap.admin.security.principal=cn=fess,cn=Users,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Busqueda de usuarios
    ldap.user.search.base=ou=Users,dc=example,dc=com
    ldap.account.filter=(sAMAccountName=%s)
    ldap.user.name.attribute=sAMAccountName

    # Busqueda de grupos
    ldap.group.search.base=ou=Groups,dc=example,dc=com
    ldap.group.filter=(member=%s)
    ldap.group.name.attribute=cn

Configuracion especifica de Active Directory
--------------------------------------------

::

    # Resolucion de grupos anidados
    ldap.memberof.enabled=true

    # Usar atributo memberOf
    ldap.group.filter=(member:1.2.840.113556.1.4.1941:=%s)

Configuracion de OpenLDAP
=========================

Ejemplo de configuracion para OpenLDAP.

::

    ldap.admin.enabled=true
    ldap.provider.url=ldap://openldap.example.com:389
    ldap.base.dn=dc=example,dc=com

    # Plantilla de DN de enlace para autenticacion de usuario
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # DN de enlace de administracion (cuenta de servicio)
    ldap.admin.security.principal=cn=admin,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Busqueda de usuarios
    ldap.user.search.base=ou=people,dc=example,dc=com
    ldap.account.filter=(uid=%s)
    ldap.user.name.attribute=uid

    # Busqueda de grupos
    ldap.group.search.base=ou=groups,dc=example,dc=com
    ldap.group.filter=(memberUid=%s)
    ldap.group.name.attribute=cn

Configuracion de seguridad
==========================

LDAPS (SSL/TLS)
---------------

Usar conexion cifrada:

::

    # Usar LDAPS
    ldap.provider.url=ldaps://ldap.example.com:636

    # Usar StartTLS
    ldap.start.tls=true

Para certificados autofirmados, importe el certificado en el truststore de Java:

::

    keytool -import -alias ldap-server -keystore $JAVA_HOME/lib/security/cacerts \
            -file ldap-server.crt

Proteccion de contrasena
------------------------

Configurar contrasena con variable de entorno:

::

    ldap.admin.security.credentials=${LDAP_PASSWORD}

Mapeo de roles
==============

Puede mapear grupos LDAP a roles de |Fess|.

Mapeo automatico
----------------

Los nombres de grupo se usan directamente como nombres de rol:

::

    # Grupo LDAP "fess-users" -> Rol Fess "fess-users"
    ldap.group.role.mapping.enabled=true

Mapeo personalizado
-------------------

::

    # Mapear nombre de grupo a rol
    ldap.group.role.mapping.Administrators=admin
    ldap.group.role.mapping.PowerUsers=editor
    ldap.group.role.mapping.Users=guest

Failover
========

Failover a multiples servidores LDAP:

::

    # Especificar multiples URLs separadas por espacios
    ldap.provider.url=ldap://ldap1.example.com:389 ldap://ldap2.example.com:389

Solucion de problemas
=====================

Error de conexion
-----------------

**Sintoma**: Falla la conexion LDAP

**Verificaciones**:

1. Si el servidor LDAP esta ejecutandose
2. Si el puerto esta abierto en el firewall (389 o 636)
3. Si la URL es correcta (``ldap://`` o ``ldaps://``)
4. Si el Bind DN y la contrasena son correctos

Error de autenticacion
----------------------

**Sintoma**: Falla la autenticacion de usuario

**Verificaciones**:

1. Si el filtro de busqueda de usuarios es correcto
2. Si el usuario existe dentro del Base DN de busqueda
3. Si el atributo de nombre de usuario es correcto

No se obtienen grupos
---------------------

**Sintoma**: No se pueden obtener los grupos del usuario

**Verificaciones**:

1. Si el filtro de busqueda de grupos es correcto
2. Si el atributo de membresia de grupo es correcto
3. Si los grupos existen dentro del Base DN de busqueda

Configuracion de depuracion
---------------------------

Obtener logs detallados:

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.ldap" level="DEBUG"/>

Informacion de referencia
=========================

- :doc:`security-role` - Control de acceso basado en roles
- :doc:`sso-spnego` - Autenticacion SPNEGO (Kerberos)
- :doc:`../admin/user-guide` - Guia de gestion de usuarios
