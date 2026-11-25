=====================================
Guía de integración LDAP
=====================================

Descripción general
====================

|Fess| soporta la integración con servidores LDAP (Lightweight Directory Access Protocol),
lo que permite la autenticación y la gestión de usuarios en entornos empresariales.

La integración LDAP permite:

- Autenticación de usuarios (inicio de sesión) con Active Directory u OpenLDAP
- Control de acceso basado en grupos y roles
- Gestión de usuarios, roles y grupos LDAP desde la pantalla de administración (opcional)

Servidores LDAP compatibles
============================

|Fess| soporta la integración con los siguientes servidores LDAP:

- Microsoft Active Directory
- OpenLDAP
- 389 Directory Server
- Apache Directory Server
- Otros servidores compatibles con LDAP v3

Requisitos previos
===================

- Acceso de red al servidor LDAP
- Cuenta de servicio para búsquedas LDAP (Bind DN)
- Comprensión de la estructura LDAP (Base DN, nombres de atributos, etc.)

Descripción general de la configuración
=========================================

La configuración LDAP de |Fess| se gestiona en dos ubicaciones según el propósito.

Configuración de conexión y autenticación (pantalla de administración / ``system.properties``)
   Configuración relacionada con la conexión al servidor LDAP y la autenticación de inicio de sesión.
   Se puede configurar desde la sección "LDAP" en la página **"Sistema > General"** de la pantalla de administración,
   y se guarda en ``app/WEB-INF/conf/system.properties``.

Configuración de la función de administración LDAP y comportamiento (``fess_config.properties``)
   Configuración relacionada con la función para gestionar usuarios, roles y grupos LDAP desde la pantalla de administración,
   y con el comportamiento como la resolución de roles. Estas opciones se definen en
   ``app/WEB-INF/classes/fess_config.properties``; edite este archivo para cambiar los valores.

.. note::

   Si solo se utiliza la autenticación de inicio de sesión, basta con la "Configuración de conexión y autenticación".
   La "Función de administración LDAP" (``ldap.admin.enabled``) solo es necesaria cuando se crean, actualizan
   o eliminan usuarios, roles y grupos del lado LDAP desde la pantalla de administración.

Configuración de conexión y autenticación
===========================================

Estas configuraciones se pueden establecer desde la sección LDAP en "Sistema > General" de la pantalla de administración,
y se guardan en ``app/WEB-INF/conf/system.properties``. También puede editar el archivo directamente.

.. list-table:: Propiedades de conexión y autenticación
   :header-rows: 1
   :widths: 30 15 55

   * - Propiedad
     - Valor por defecto
     - Descripción
   * - ``ldap.provider.url``
     - (ninguno)
     - URL del servidor LDAP. Ejemplo: ``ldap://ldap.example.com:389``. Para LDAPS: ``ldaps://ldap.example.com:636``. Se pueden especificar varias URLs separadas por espacios para failover.
   * - ``ldap.base.dn``
     - (ninguno)
     - Base DN para la búsqueda LDAP. Ejemplo: ``dc=example,dc=com``
   * - ``ldap.security.principal``
     - (ninguno)
     - Plantilla de DN para la autenticación (enlace) de usuarios. ``%s`` se reemplaza con el nombre de usuario. Ejemplo: ``uid=%s,ou=People,dc=example,dc=com``
   * - ``ldap.security.authentication``
     - ``simple``
     - Método de autenticación LDAP (``java.naming.security.authentication`` de JNDI). Normalmente se utiliza ``simple``.
   * - ``ldap.initial.context.factory``
     - ``com.sun.jndi.ldap.LdapCtxFactory``
     - Clase de fábrica del contexto inicial de JNDI. Normalmente no es necesario modificarla.
   * - ``ldap.admin.security.principal``
     - (ninguno)
     - Bind DN de la cuenta de servicio para búsquedas LDAP. Ejemplo: ``cn=fess,ou=services,dc=example,dc=com``
   * - ``ldap.admin.security.credentials``
     - (ninguno)
     - Contraseña de la cuenta de servicio indicada anteriormente.
   * - ``ldap.account.filter``
     - (ninguno)
     - Filtro para buscar la entrada de usuario al resolver roles de usuario. ``%s`` se reemplaza con el nombre de usuario. Ejemplo: ``uid=%s``
   * - ``ldap.group.filter``
     - (vacío)
     - Filtro de búsqueda utilizado para la resolución de grupos. ``%s`` se reemplaza por el DN del usuario u otro valor. Ejemplo: ``(member=%s)``
   * - ``ldap.memberof.attribute``
     - ``memberOf``
     - Nombre del atributo que representa la pertenencia a grupos. Se utiliza para resolver roles en Active Directory y otros servidores que posean este atributo.

Ejemplo de configuración (edición directa de ``system.properties``):

::

    # URL del servidor LDAP
    ldap.provider.url=ldap://ldap.example.com:389

    # Base DN
    ldap.base.dn=dc=example,dc=com

    # Plantilla de Bind DN para autenticación de usuario (%s se sustituye por el nombre de usuario)
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # Bind DN y contraseña de la cuenta de servicio para búsquedas
    ldap.admin.security.principal=cn=fess,ou=services,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Filtros para resolución de roles
    ldap.account.filter=uid=%s
    ldap.group.filter=(member=%s)

.. note::

   El marcador de posición ``%s`` es procesado por ``String.format()`` de Java.
   ``ldap.security.principal``, ``ldap.account.filter``, ``ldap.group.filter`` y
   los filtros de administración usan el formato ``%s`` (no ``{0}``).
   El nombre de usuario que se pasa a los filtros es escapado automáticamente
   por |Fess| como medida de protección contra inyección LDAP.

Configuración de la función de administración LDAP y comportamiento
======================================================================

Las siguientes propiedades se definen en ``app/WEB-INF/classes/fess_config.properties``.
Para cambiar los valores, edite este archivo.

Habilitación de la función de administración
-----------------------------------------------

.. list-table:: Propiedades de la función de administración
   :header-rows: 1
   :widths: 35 15 50

   * - Propiedad
     - Valor por defecto
     - Descripción
   * - ``ldap.admin.enabled``
     - ``false``
     - Habilita la función para crear, actualizar y eliminar usuarios, roles y grupos LDAP desde la pantalla de administración. **No es necesaria para la autenticación de inicio de sesión**; el inicio de sesión con LDAP funciona aunque no esté habilitada.
   * - ``ldap.admin.sync.password``
     - ``true``
     - Sincroniza la contraseña del lado de |Fess| con LDAP al actualizar un usuario desde la pantalla de administración.
   * - ``ldap.auth.validation``
     - ``true``
     - Valida la autenticación LDAP en el momento del inicio de sesión.

Filtros y Base DN para la gestión de usuarios, roles y grupos
----------------------------------------------------------------

Se utilizan para manipular entradas LDAP desde la pantalla de administración cuando ``ldap.admin.enabled=true``.

.. list-table:: Filtros y Base DN de administración
   :header-rows: 1
   :widths: 38 47 15

   * - Propiedad
     - Descripción
     - Valor por defecto
   * - ``ldap.admin.user.filter``
     - Filtro de búsqueda de usuarios (``%s`` se reemplaza con el nombre de usuario)
     - ``uid=%s``
   * - ``ldap.admin.user.base.dn``
     - Base DN de búsqueda de usuarios
     - ``ou=People,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.user.object.classes``
     - objectClass al crear usuarios
     - ``organizationalPerson,top,person,inetOrgPerson``
   * - ``ldap.admin.role.filter``
     - Filtro de búsqueda de roles
     - ``cn=%s``
   * - ``ldap.admin.role.base.dn``
     - Base DN de búsqueda de roles
     - ``ou=Role,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.role.object.classes``
     - objectClass al crear roles
     - ``groupOfNames``
   * - ``ldap.admin.group.filter``
     - Filtro de búsqueda de grupos
     - ``cn=%s``
   * - ``ldap.admin.group.base.dn``
     - Base DN de búsqueda de grupos
     - ``ou=Group,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.group.object.classes``
     - objectClass al crear grupos
     - ``groupOfNames``

Control de la resolución de roles y el comportamiento
----------------------------------------------------------

Controla el comportamiento de la resolución de roles y grupos tras el inicio de sesión.

.. list-table:: Propiedades de control de comportamiento
   :header-rows: 1
   :widths: 40 15 45

   * - Propiedad
     - Valor por defecto
     - Descripción
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
     - Permite el inicio de sesión de usuarios sin grupos ni roles asignados.
   * - ``ldap.ignore.netbios.name``
     - ``true``
     - Elimina el nombre NetBIOS (prefijo con formato ``DOMAIN\``) de los nombres de grupo, etc.
   * - ``ldap.group.name.with.underscores``
     - ``false``
     - Permite guiones bajos en los nombres de grupo.
   * - ``ldap.lowercase.permission.name``
     - ``false``
     - Convierte los nombres de permiso a minúsculas.
   * - ``ldap.samaccountname.group``
     - ``false``
     - Utiliza el atributo ``sAMAccountName`` como nombre de grupo (para Active Directory).
   * - ``ldap.max.username.length``
     - ``-1``
     - Si el nombre de usuario introducido es más largo, se recorta a este número de caracteres, conservando los primeros (pensado para el nombre de inicio de sesión de 20 caracteres de un Active Directory antiguo). El nombre recortado se usa para el bind, el nombre de usuario, la búsqueda de roles, los nombres de permiso y la sesión, y el inicio de sesión nunca se rechaza por su longitud. Un valor negativo (el predeterminado ``-1``) no recorta.

.. note::
   En un inicio de sesión con nombre de usuario y contraseña de LDAP, se eliminan los espacios al principio y al final del nombre de usuario introducido (los espacios dentro del nombre se conservan). El recorte se hace después, y un espacio que quede al final del nombre recortado también se elimina.

LDAP: unidades organizativas de roles y grupos anidados
-------------------------------------------------------

Si una entrada de grupo da un rol (prefijo de permiso ``role.search.role.prefix``, por defecto ``R``) o un grupo (``role.search.group.prefix``, por defecto ``2``) se decide por su DN. Para los cambios respecto a 15.9, consulte :doc:`../install/upgrade`.

15.10 analiza el DN y trata una entrada como rol solo cuando uno de sus componentes ``ou`` es exactamente ``Role`` o ``Roles`` (sin distinguir mayúsculas de minúsculas). Cualquier otra entrada es un grupo, igual que una entrada cuyo DN no se puede analizar.

Cuando ``ldap.group.filter`` está definido (por defecto está vacío), |Fess| lo usa para buscar los grupos que contienen los grupos del usuario (grupos anidados). Hasta 15.9, los DN de los grupos del usuario se insertaban en ese filtro sin escapar. Un DN con un carácter escapado, como la coma de ``CN=Sales\, EMEA,...``, no coincidía, de modo que los grupos anidados de ese grupo faltaban sin ningún error, y un DN con caracteres especiales de los filtros LDAP modificaba el filtro. 15.10 escapa los DN (RFC 4515). Los grupos anidados de esos grupos ahora se encuentran, por lo que los usuarios afectados obtienen también los permisos de esos grupos.

Nombres de usuario administrador reservados
-------------------------------------------

Los nombres indicados en ``authentication.admin.users`` quedan reservados por |Fess| para sí mismo.
En SSO actúan como lista de bloqueo: ``SpnegoAuthenticator`` no resuelve credenciales para un nombre
que coincida, y el inicio de sesión por formulario tampoco lleva ese nombre a LDAP.

Un directorio no distingue mayúsculas y minúsculas en un nombre de cuenta -- Active Directory emite
un ticket para cualquier grafía --, de modo que comparar exactamente permite que la misma cuenta
inicie sesión solo con cambiar la grafía. ``authentication.admin.users.ignore.case`` decide cómo se
comparan.

.. list-table:: Comparación de nombres reservados
   :header-rows: 1
   :widths: 40 15 45

   * - Propiedad
     - Valor predeterminado
     - Descripción
   * - ``authentication.admin.users``
     - ``admin``
     - Nombres de usuario administrador reservados, separados por comas.
   * - ``authentication.admin.users.ignore.case``
     - ``auto``
     - Cómo se comparan los nombres reservados. ``auto`` ignora mayúsculas y minúsculas solo cuando ``ldap.provider.url`` está definido; si no lo está, compara exactamente. ``true`` y ``false`` lo deciden de forma explícita.

.. note::
   Cuando ``ldap.provider.url`` está definido, ``auto`` ignora mayúsculas y minúsculas. Una cuenta del directorio cuyo nombre difiera de uno reservado solo en mayúsculas y minúsculas deja de poder iniciar sesión y ya no se sincroniza con el directorio desde la interfaz de administración. Defina ``authentication.admin.users.ignore.case=false`` para seguir comparando de forma exacta.

.. _local-username-policy:

Política de Nombres de Usuarios Locales
---------------------------------------

|Fess| compara los nombres de los usuarios locales (los usuarios de la pantalla de gestión de usuarios, no los de LDAP ni SSO) exactamente como se escriben. ``Alice``, ``alice`` y ``ＡＬＩＣＥ`` (letras de ancho completo) son tres usuarios, cada uno con su propio inicio de sesión. ``authentication.local.username.policy`` decide si al crear o renombrar un usuario local también se rechaza un nombre que se diferencia del de otro usuario solo en mayúsculas y minúsculas, ancho de los caracteres o composición Unicode.

.. list-table:: Política de nombres de usuarios locales
   :header-rows: 1
   :widths: 40 15 45

   * - Propiedad
     - Valor por defecto
     - Descripción
   * - ``authentication.local.username.policy``
     - ``preserved``
     - ``preserved`` compara los nombres exactamente como se escriben, como en 15.9. ``mapped`` rechaza un nombre nuevo o renombrado que, una vez transformado (véase más abajo), coincide con el nombre de otro usuario. El valor se compara sin distinguir mayúsculas de minúsculas. Un valor desconocido se trata como ``preserved`` y se registra una vez como advertencia.

Con ``mapped``, la creación o el cambio de nombre de un usuario en la pantalla de gestión de usuarios o con la API de administración (``POST`` y ``PUT`` de ``/api/admin/user/setting``) se rechaza en dos casos:

- El nombre transformado coincide con el nombre transformado de otro usuario. La transformación es la de ``UsernameCaseMapped`` de RFC 8265: las formas de ancho completo y de medio ancho (como el katakana de medio ancho) y el espacio ideográfico se sustituyen por su correspondencia de descomposición, las mayúsculas se pasan a minúsculas con la configuración regional raíz y el resultado se normaliza a la forma de normalización Unicode C (no NFKC). ``Alice``, ``alice`` y ``ＡＬＩＣＥ`` son el mismo nombre una vez transformados.
- El nombre es otra grafía de una entrada de ``authentication.admin.users`` (véase más arriba). ``admin`` todavía se puede volver a crear, porque es la entrada tal como está escrita, mientras que ``Admin``, ``ADMIN`` y la grafía de ancho completo se rechazan.

Un usuario que se guarda con el nombre que ya tiene nunca se rechaza, de modo que los usuarios que hoy colisionan siguen pudiendo editarse. Cuando |Fess| arranca con ``mapped``, escribe en ``fess.log`` una advertencia que enumera hasta 20 grupos de nombres almacenados que son iguales una vez transformados y hasta 20 nombres almacenados que contienen espacios en blanco o caracteres de control. No se cambia nada: esos usuarios pueden seguir iniciando sesión y editándose.

.. note::

   La política solo decide si se acepta un nombre. No cambia el inicio de sesión, que busca un usuario por el nombre exactamente como se escribe, ni el ID de usuario ni el nombre almacenado. Tampoco cambia las cadenas de permisos formadas a partir de un nombre (``{user}Alice`` y ``{user}alice`` en un filtro de roles, en los permisos de una configuración de rastreo o en un documento) ni los documentos ya indexados. Tampoco impone las reglas de caracteres de RFC 8265: un nombre con espacios, símbolos o caracteres de control se sigue aceptando.

   La comprobación no se aplica en la restauración de una copia de seguridad, en la creación del usuario ``admin`` inicial en el primer arranque ni en una escritura directa en el índice de usuarios. Si dos administradores crean ``Alice`` y ``alice`` en el mismo instante, ambos pueden tener éxito, porque no se almacena ningún nombre transformado. Unificar los nombres en el inicio de sesión y en los permisos exigiría migrar los usuarios, roles y documentos indexados almacenados, y no forma parte de este ajuste.

Mapeo de atributos
--------------------

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
   Consulte las líneas que comienzan con ``ldap.attr.`` en ``fess_config.properties`` para ver la lista completa.

Configuración de Active Directory
====================================

Ejemplo de configuración para Microsoft Active Directory (``system.properties`` o pantalla de administración).

::

    ldap.provider.url=ldap://ad.example.com:389
    ldap.base.dn=dc=example,dc=com

    # Plantilla de Bind DN para autenticación de usuario (formato UPN)
    ldap.security.principal=%s@example.com

    # Cuenta de servicio para búsquedas
    ldap.admin.security.principal=cn=fess,cn=Users,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Filtro de cuenta
    ldap.account.filter=sAMAccountName=%s

    # Usar atributo memberOf
    ldap.memberof.attribute=memberOf

    # Filtro de grupos
    ldap.group.filter=(member=%s)

Para resolver grupos anidados (nested groups), puede utilizar
``LDAP_MATCHING_RULE_IN_CHAIN``, específico de Active Directory.

::

    ldap.group.filter=(member:1.2.840.113556.1.4.1941:=%s)

Configuración de OpenLDAP
============================

Ejemplo de configuración para OpenLDAP.

::

    ldap.provider.url=ldap://openldap.example.com:389
    ldap.base.dn=dc=example,dc=com

    # Plantilla de Bind DN para autenticación de usuario
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # Cuenta de servicio para búsquedas
    ldap.admin.security.principal=cn=admin,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Filtro de cuenta
    ldap.account.filter=uid=%s

    # Filtro de grupos (para posixGroup)
    ldap.group.filter=(memberUid=%s)

.. note::

   OpenLDAP estándar no tiene el atributo ``memberOf``, por lo que los grupos
   se resuelven mediante ``ldap.group.filter``.
   Si tiene habilitado el overlay ``memberof``, también puede utilizar ``ldap.memberof.attribute``.

Configuración de seguridad
=============================

LDAPS (SSL/TLS)
-----------------

Usar conexión cifrada:

::

    # Usar LDAPS
    ldap.provider.url=ldaps://ldap.example.com:636

Para certificados autofirmados, importe el certificado en el truststore de Java:

::

    keytool -import -alias ldap-server -keystore $JAVA_HOME/lib/security/cacerts \
            -file ldap-server.crt

Protección de contraseñas
----------------------------

``ldap.admin.security.credentials`` se guarda en ``system.properties``.
Las credenciales configuradas desde la pantalla de administración se almacenan cifradas internamente.
Restrinja adecuadamente los permisos de acceso al archivo.

Failover
==========

Para realizar failover a múltiples servidores LDAP, especifique varias URLs
separadas por espacios en ``ldap.provider.url``.

::

    ldap.provider.url=ldap://ldap1.example.com:389 ldap://ldap2.example.com:389

Solución de problemas
========================

Error de conexión
--------------------

**Síntoma**: Falla la conexión LDAP

**Verificaciones**:

1. Si el servidor LDAP está en ejecución
2. Si el puerto está abierto en el firewall (389 o 636)
3. Si ``ldap.provider.url`` es correcto (``ldap://`` o ``ldaps://``)
4. Si ``ldap.admin.security.principal`` y la contraseña son correctos

Error de autenticación
-------------------------

**Síntoma**: Falla la autenticación de usuario

**Verificaciones**:

1. Si la plantilla de ``ldap.security.principal`` es correcta (si contiene ``%s``)
2. Si el usuario existe dentro del Base DN especificado
3. Si ``ldap.account.filter`` es correcto

No se obtienen grupos ni roles
----------------------------------

**Síntoma**: No se pueden obtener los grupos o roles del usuario

**Verificaciones**:

1. Si ``ldap.group.filter`` es correcto
2. Si ``ldap.memberof.attribute`` es correcto (en caso de Active Directory)
3. Si los grupos existen dentro del Base DN de búsqueda
4. Si ``ldap.role.search.*.enabled`` está habilitado

No se puede gestionar usuarios desde la pantalla de administración
------------------------------------------------------------------------

**Síntoma**: No se pueden crear, editar ni eliminar usuarios LDAP desde la pantalla de administración

**Verificaciones**:

1. Si ``ldap.admin.enabled`` está en ``true``
2. Si los Base DN de administración como ``ldap.admin.user.base.dn`` son correctos
3. Si la cuenta de servicio de ``ldap.admin.security.principal`` tiene permisos de escritura

Configuración de depuración
------------------------------

Para obtener logs detallados, agregue un logger en ``app/WEB-INF/classes/log4j2.xml``.

::

    <Logger name="org.codelibs.fess.ldap" level="DEBUG"/>

Información de referencia
============================

- :doc:`security-role` - Control de acceso basado en roles
- :doc:`sso-spnego` - Autenticación SPNEGO (Kerberos)
- :doc:`../admin/user-guide` - Guía de gestión de usuarios
