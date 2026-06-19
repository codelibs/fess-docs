=====================================
Guia de integracion LDAP
=====================================

Descripcion general
===================

|Fess| soporta la integracion con servidores LDAP (Lightweight Directory Access Protocol),
lo que permite la autenticacion y la gestion de usuarios en entornos empresariales.

La integracion LDAP permite:

- Autenticacion de usuarios (inicio de sesion) con Active Directory u OpenLDAP
- Control de acceso basado en grupos y roles
- Gestion de usuarios, roles y grupos LDAP desde la pantalla de administracion (opcional)

Servidores LDAP compatibles
============================

|Fess| soporta la integracion con los siguientes servidores LDAP:

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

Descripcion general de la configuracion
========================================

La configuracion LDAP de |Fess| se gestiona en dos ubicaciones segun el proposito.

Configuracion de conexion y autenticacion (pantalla de administracion / ``system.properties``)
   Configuracion relacionada con la conexion al servidor LDAP y la autenticacion de inicio de sesion.
   Se puede configurar desde la seccion "LDAP" en la pagina **"Sistema > General"** de la pantalla de administracion,
   y se guarda en ``app/WEB-INF/conf/system.properties``.

Configuracion de la funcion de administracion LDAP y comportamiento (``fess_config.properties``)
   Configuracion relacionada con la funcion para gestionar usuarios, roles y grupos LDAP desde la pantalla de administracion,
   y con el comportamiento como la resolucion de roles. Estas opciones se definen en
   ``app/WEB-INF/classes/fess_config.properties``; edite este archivo para cambiar los valores.

.. note::

   Si solo se utiliza la autenticacion de inicio de sesion, basta con la "Configuracion de conexion y autenticacion".
   La "Funcion de administracion LDAP" (``ldap.admin.enabled``) solo es necesaria cuando se crean, actualizan
   o eliminan usuarios, roles y grupos del lado LDAP desde la pantalla de administracion.

Configuracion de conexion y autenticacion
==========================================

Estas configuraciones se pueden establecer desde la seccion LDAP en "Sistema > General" de la pantalla de administracion,
y se guardan en ``app/WEB-INF/conf/system.properties``. Tambien puede editar el archivo directamente.

.. list-table:: Propiedades de conexion y autenticacion
   :header-rows: 1
   :widths: 30 15 55

   * - Propiedad
     - Valor por defecto
     - Descripcion
   * - ``ldap.provider.url``
     - (ninguno)
     - URL del servidor LDAP. Ejemplo: ``ldap://ldap.example.com:389``. Para LDAPS: ``ldaps://ldap.example.com:636``. Se pueden especificar varias URLs separadas por espacios para failover.
   * - ``ldap.base.dn``
     - (ninguno)
     - Base DN para la busqueda LDAP. Ejemplo: ``dc=example,dc=com``
   * - ``ldap.security.principal``
     - (ninguno)
     - Plantilla de DN para la autenticacion (enlace) de usuarios. ``%s`` se reemplaza con el nombre de usuario. Ejemplo: ``uid=%s,ou=People,dc=example,dc=com``
   * - ``ldap.security.authentication``
     - ``simple``
     - Metodo de autenticacion LDAP (``java.naming.security.authentication`` de JNDI). Normalmente se utiliza ``simple``.
   * - ``ldap.initial.context.factory``
     - ``com.sun.jndi.ldap.LdapCtxFactory``
     - Clase de fabrica del contexto inicial de JNDI. Normalmente no es necesario modificarla.
   * - ``ldap.admin.security.principal``
     - (ninguno)
     - Bind DN de la cuenta de servicio para busquedas LDAP. Ejemplo: ``cn=fess,ou=services,dc=example,dc=com``
   * - ``ldap.admin.security.credentials``
     - (ninguno)
     - Contrasena de la cuenta de servicio indicada anteriormente.
   * - ``ldap.account.filter``
     - (ninguno)
     - Filtro para buscar la entrada de usuario al resolver roles de usuario. ``%s`` se reemplaza con el nombre de usuario. Ejemplo: ``uid=%s``
   * - ``ldap.group.filter``
     - (vacio)
     - Filtro de busqueda utilizado para la resolucion de grupos. ``%s`` se reemplaza por el DN del usuario u otro valor. Ejemplo: ``(member=%s)``
   * - ``ldap.memberof.attribute``
     - ``memberOf``
     - Nombre del atributo que representa la pertenencia a grupos. Se utiliza para resolver roles en Active Directory y otros servidores que posean este atributo.

Ejemplo de configuracion (edicion directa de ``system.properties``):

::

    # URL del servidor LDAP
    ldap.provider.url=ldap://ldap.example.com:389

    # Base DN
    ldap.base.dn=dc=example,dc=com

    # Plantilla de Bind DN para autenticacion de usuario (%s se sustituye por el nombre de usuario)
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # Bind DN y contrasena de la cuenta de servicio para busquedas
    ldap.admin.security.principal=cn=fess,ou=services,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Filtros para resolucion de roles
    ldap.account.filter=uid=%s
    ldap.group.filter=(member=%s)

.. note::

   El marcador de posicion ``%s`` es procesado por ``String.format()`` de Java.
   ``ldap.security.principal``, ``ldap.account.filter``, ``ldap.group.filter`` y
   los filtros de administracion usan el formato ``%s`` (no ``{0}``).
   El nombre de usuario que se pasa a los filtros es escapado automaticamente
   por |Fess| como medida de proteccion contra inyeccion LDAP.

Configuracion de la funcion de administracion LDAP y comportamiento
====================================================================

Las siguientes propiedades se definen en ``app/WEB-INF/classes/fess_config.properties``.
Para cambiar los valores, edite este archivo.

Habilitacion de la funcion de administracion
---------------------------------------------

.. list-table:: Propiedades de la funcion de administracion
   :header-rows: 1
   :widths: 35 15 50

   * - Propiedad
     - Valor por defecto
     - Descripcion
   * - ``ldap.admin.enabled``
     - ``false``
     - Habilita la funcion para crear, actualizar y eliminar usuarios, roles y grupos LDAP desde la pantalla de administracion. **No es necesaria para la autenticacion de inicio de sesion**; el inicio de sesion con LDAP funciona aunque no este habilitada.
   * - ``ldap.admin.sync.password``
     - ``true``
     - Sincroniza la contrasena del lado de |Fess| con LDAP al actualizar un usuario desde la pantalla de administracion.
   * - ``ldap.auth.validation``
     - ``true``
     - Valida la autenticacion LDAP en el momento del inicio de sesion.

Filtros y Base DN para la gestion de usuarios, roles y grupos
--------------------------------------------------------------

Se utilizan para manipular entradas LDAP desde la pantalla de administracion cuando ``ldap.admin.enabled=true``.

.. list-table:: Filtros y Base DN de administracion
   :header-rows: 1
   :widths: 38 47 15

   * - Propiedad
     - Descripcion
     - Valor por defecto
   * - ``ldap.admin.user.filter``
     - Filtro de busqueda de usuarios (``%s`` se reemplaza con el nombre de usuario)
     - ``uid=%s``
   * - ``ldap.admin.user.base.dn``
     - Base DN de busqueda de usuarios
     - ``ou=People,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.user.object.classes``
     - objectClass al crear usuarios
     - ``organizationalPerson,top,person,inetOrgPerson``
   * - ``ldap.admin.role.filter``
     - Filtro de busqueda de roles
     - ``cn=%s``
   * - ``ldap.admin.role.base.dn``
     - Base DN de busqueda de roles
     - ``ou=Role,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.role.object.classes``
     - objectClass al crear roles
     - ``groupOfNames``
   * - ``ldap.admin.group.filter``
     - Filtro de busqueda de grupos
     - ``cn=%s``
   * - ``ldap.admin.group.base.dn``
     - Base DN de busqueda de grupos
     - ``ou=Group,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.group.object.classes``
     - objectClass al crear grupos
     - ``groupOfNames``

Control de la resolucion de roles y el comportamiento
------------------------------------------------------

Controla el comportamiento de la resolucion de roles y grupos tras el inicio de sesion.

.. list-table:: Propiedades de control de comportamiento
   :header-rows: 1
   :widths: 40 15 45

   * - Propiedad
     - Valor por defecto
     - Descripcion
   * - ``ldap.role.search.user.enabled``
     - ``true``
     - Asigna roles basados en el nombre de usuario.
   * - ``ldap.role.search.group.enabled``
     - ``true``
     - Asigna roles basados en grupos.
   * - ``ldap.role.search.role.enabled``
     - ``true``
     - Asigna roles basados en roles.
   * - ``ldap.allow.empty.permission``
     - ``true``
     - Permite el inicio de sesion de usuarios sin grupos ni roles asignados.
   * - ``ldap.ignore.netbios.name``
     - ``true``
     - Elimina el nombre NetBIOS (prefijo con formato ``DOMAIN\``) de los nombres de grupo, etc.
   * - ``ldap.group.name.with.underscores``
     - ``false``
     - Permite guiones bajos en los nombres de grupo.
   * - ``ldap.lowercase.permission.name``
     - ``false``
     - Convierte los nombres de permiso a minusculas.
   * - ``ldap.samaccountname.group``
     - ``false``
     - Utiliza el atributo ``sAMAccountName`` como nombre de grupo (para Active Directory).
   * - ``ldap.max.username.length``
     - ``-1``
     - Longitud maxima del nombre de usuario. ``-1`` significa sin limite.

Mapeo de atributos
------------------

La correspondencia entre los atributos LDAP y los atributos de usuario de |Fess| se define mediante las propiedades ``ldap.attr.*``.
Normalmente no es necesario modificarlas, pero pueden ajustarse si el esquema es diferente. Algunos ejemplos representativos:

::

    ldap.attr.surname=sn
    ldap.attr.givenName=givenName
    ldap.attr.mail=mail
    ldap.attr.displayName=displayName
    ldap.attr.telephoneNumber=telephoneNumber

.. note::

   Existen casos en que el nombre de la propiedad y el nombre del atributo LDAP no coinciden,
   como ``ldap.attr.state`` que se mapea a ``st``, o ``ldap.attr.city`` que se mapea a ``l``.
   Consulte las lineas que comienzan con ``ldap.attr.`` en ``fess_config.properties`` para ver la lista completa.

Configuracion de Active Directory
==================================

Ejemplo de configuracion para Microsoft Active Directory (``system.properties`` o pantalla de administracion).

::

    ldap.provider.url=ldap://ad.example.com:389
    ldap.base.dn=dc=example,dc=com

    # Plantilla de Bind DN para autenticacion de usuario (formato UPN)
    ldap.security.principal=%s@example.com

    # Cuenta de servicio para busquedas
    ldap.admin.security.principal=cn=fess,cn=Users,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Filtro de cuenta
    ldap.account.filter=sAMAccountName=%s

    # Usar atributo memberOf
    ldap.memberof.attribute=memberOf

    # Filtro de grupos
    ldap.group.filter=(member=%s)

Para resolver grupos anidados (nested groups), puede utilizar
``LDAP_MATCHING_RULE_IN_CHAIN``, especifico de Active Directory.

::

    ldap.group.filter=(member:1.2.840.113556.1.4.1941:=%s)

Configuracion de OpenLDAP
==========================

Ejemplo de configuracion para OpenLDAP.

::

    ldap.provider.url=ldap://openldap.example.com:389
    ldap.base.dn=dc=example,dc=com

    # Plantilla de Bind DN para autenticacion de usuario
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # Cuenta de servicio para busquedas
    ldap.admin.security.principal=cn=admin,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Filtro de cuenta
    ldap.account.filter=uid=%s

    # Filtro de grupos (para posixGroup)
    ldap.group.filter=(memberUid=%s)

.. note::

   OpenLDAP estandar no tiene el atributo ``memberOf``, por lo que los grupos
   se resuelven mediante ``ldap.group.filter``.
   Si tiene habilitado el overlay ``memberof``, tambien puede utilizar ``ldap.memberof.attribute``.

Configuracion de seguridad
===========================

LDAPS (SSL/TLS)
---------------

Usar conexion cifrada:

::

    # Usar LDAPS
    ldap.provider.url=ldaps://ldap.example.com:636

Para certificados autofirmados, importe el certificado en el truststore de Java:

::

    keytool -import -alias ldap-server -keystore $JAVA_HOME/lib/security/cacerts \
            -file ldap-server.crt

Proteccion de contrasenas
--------------------------

``ldap.admin.security.credentials`` se guarda en ``system.properties``.
Las credenciales configuradas desde la pantalla de administracion se almacenan cifradas internamente.
Restrinja adecuadamente los permisos de acceso al archivo.

Failover
=========

Para realizar failover a multiples servidores LDAP, especifique varias URLs
separadas por espacios en ``ldap.provider.url``.

::

    ldap.provider.url=ldap://ldap1.example.com:389 ldap://ldap2.example.com:389

Solucion de problemas
======================

Error de conexion
-----------------

**Sintoma**: Falla la conexion LDAP

**Verificaciones**:

1. Si el servidor LDAP esta en ejecucion
2. Si el puerto esta abierto en el firewall (389 o 636)
3. Si ``ldap.provider.url`` es correcto (``ldap://`` o ``ldaps://``)
4. Si ``ldap.admin.security.principal`` y la contrasena son correctos

Error de autenticacion
-----------------------

**Sintoma**: Falla la autenticacion de usuario

**Verificaciones**:

1. Si la plantilla de ``ldap.security.principal`` es correcta (si contiene ``%s``)
2. Si el usuario existe dentro del Base DN especificado
3. Si ``ldap.account.filter`` es correcto

No se obtienen grupos ni roles
--------------------------------

**Sintoma**: No se pueden obtener los grupos o roles del usuario

**Verificaciones**:

1. Si ``ldap.group.filter`` es correcto
2. Si ``ldap.memberof.attribute`` es correcto (en caso de Active Directory)
3. Si los grupos existen dentro del Base DN de busqueda
4. Si ``ldap.role.search.*.enabled`` esta habilitado

No se puede gestionar usuarios desde la pantalla de administracion
------------------------------------------------------------------

**Sintoma**: No se pueden crear, editar ni eliminar usuarios LDAP desde la pantalla de administracion

**Verificaciones**:

1. Si ``ldap.admin.enabled`` esta en ``true``
2. Si los Base DN de administracion como ``ldap.admin.user.base.dn`` son correctos
3. Si la cuenta de servicio de ``ldap.admin.security.principal`` tiene permisos de escritura

Configuracion de depuracion
-----------------------------

Para obtener logs detallados, agregue un logger en ``app/WEB-INF/classes/log4j2.xml``.

::

    <Logger name="org.codelibs.fess.ldap" level="DEBUG"/>

Informacion de referencia
==========================

- :doc:`security-role` - Control de acceso basado en roles
- :doc:`sso-spnego` - Autenticacion SPNEGO (Kerberos)
- :doc:`../admin/user-guide` - Guia de gestion de usuarios
