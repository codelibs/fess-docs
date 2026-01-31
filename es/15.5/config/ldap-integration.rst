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

    # Bind DN (cuenta de servicio)
    ldap.security.principal=cn=fess,ou=services,dc=example,dc=com

    # Contrasena de Bind
    ldap.admin.security.credentials=your_password

Configuracion de busqueda de usuarios
-------------------------------------

::

    # Base DN para busqueda de usuarios
    ldap.user.search.base=ou=users,dc=example,dc=com

    # Filtro de busqueda de usuarios
    ldap.user.search.filter=(uid={0})

    # Atributo de nombre de usuario
    ldap.user.name.attribute=uid

Configuracion de busqueda de grupos
-----------------------------------

::

    # Base DN para busqueda de grupos
    ldap.group.search.base=ou=groups,dc=example,dc=com

    # Filtro de busqueda de grupos
    ldap.group.search.filter=(member={0})

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

    # Cuenta de servicio (formato UPN)
    ldap.security.principal=fess@example.com
    ldap.admin.security.credentials=your_password

    # Busqueda de usuarios
    ldap.user.search.base=ou=Users,dc=example,dc=com
    ldap.user.search.filter=(sAMAccountName={0})
    ldap.user.name.attribute=sAMAccountName

    # Busqueda de grupos
    ldap.group.search.base=ou=Groups,dc=example,dc=com
    ldap.group.search.filter=(member={0})
    ldap.group.name.attribute=cn

Configuracion especifica de Active Directory
--------------------------------------------

::

    # Resolucion de grupos anidados
    ldap.memberof.enabled=true

    # Usar atributo memberOf
    ldap.group.search.filter=(member:1.2.840.113556.1.4.1941:={0})

Configuracion de OpenLDAP
=========================

Ejemplo de configuracion para OpenLDAP.

::

    ldap.admin.enabled=true
    ldap.provider.url=ldap://openldap.example.com:389
    ldap.base.dn=dc=example,dc=com

    # Cuenta de servicio
    ldap.security.principal=cn=admin,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Busqueda de usuarios
    ldap.user.search.base=ou=people,dc=example,dc=com
    ldap.user.search.filter=(uid={0})
    ldap.user.name.attribute=uid

    # Busqueda de grupos
    ldap.group.search.base=ou=groups,dc=example,dc=com
    ldap.group.search.filter=(memberUid={0})
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

Sincronizacion de informacion de usuarios
=========================================

Puede sincronizar informacion de usuarios de LDAP a |Fess|.

Sincronizacion automatica
-------------------------

Sincronizar automaticamente informacion de usuario al iniciar sesion:

::

    ldap.user.sync.enabled=true

Atributos a sincronizar
-----------------------

::

    # Direccion de email
    ldap.user.email.attribute=mail

    # Nombre para mostrar
    ldap.user.displayname.attribute=displayName

Pool de conexiones
==================

Configuracion de pool de conexiones para mejorar el rendimiento:

::

    # Habilitar pool de conexiones
    ldap.connection.pool.enabled=true

    # Numero minimo de conexiones
    ldap.connection.pool.min=1

    # Numero maximo de conexiones
    ldap.connection.pool.max=10

    # Timeout de conexion (milisegundos)
    ldap.connection.timeout=5000

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
