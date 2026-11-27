==========================
Configuración de Seguridad
==========================

Esta página describe la configuración de seguridad recomendada para operar |Fess| de manera segura en entornos de producción.

.. danger::

   **La Seguridad es Extremadamente Importante**

   En entornos de producción, se recomienda encarecidamente implementar todas las configuraciones de seguridad descritas en esta página.
   Descuidar la configuración de seguridad aumenta los riesgos de acceso no autorizado, fugas de datos y compromiso del sistema.

Configuraciones de Seguridad Obligatorias
==========================================

Cambio de Contraseña de Administrador
--------------------------------------

Asegúrese de cambiar la contraseña de administrador predeterminada (``admin`` / ``admin``).

**Procedimiento:**

1. Inicie sesión en la pantalla de administración: http://localhost:8080/admin
2. Haga clic en "Usuario" → "Usuario"
3. Seleccione el usuario ``admin``
4. Configure una contraseña fuerte
5. Haga clic en el botón "Actualizar"

.. note::

   Una vez que haya cambiado la contraseña desde ``admin``, no podrá volver a establecerla en un valor simple como ``admin`` (una lista negra de contraseñas de administrador está configurada mediante ``password.invalid.admin.passwords``). También puede cambiar la contraseña inicial del usuario ``admin`` antes del primer inicio estableciendo ``index.user.initial_password`` en ``fess_config.properties``. ``bin/fess-setup init`` también la establece; consulte :doc:`fess-setup`.

.. note::

   Si inicia sesión como ``admin`` con la contraseña inicial, justo después del inicio de sesión aparece la pantalla de cambio de contraseña. Es una indicación para que la cambie, no una obligación impuesta por el servidor (el inicio de sesión ya se ha completado y también puede abrir la pantalla de administración sin cambiarla). Para asegurarse de que se cambie la contraseña, establezca la contraseña inicial con ``bin/fess-setup init`` o ``index.user.initial_password`` antes del primer inicio.

|Fess| ofrece una función integrada que aplica los requisitos de longitud mínima/máxima y de tipos de caracteres de la contraseña. Configure las siguientes propiedades en ``fess_config.properties`` (los valores predeterminados se indican entre paréntesis):

- ``password.min.length`` (valor predeterminado: ``8``): Longitud mínima. Se recomienda 12 o más.
- ``password.max.length`` (valor predeterminado: ``100``): Longitud máxima en caracteres. Con independencia de este valor, una contraseña también está limitada en bytes UTF-8 por el algoritmo de hash de contraseñas (véase más abajo).
- ``password.require.uppercase`` (valor predeterminado: ``false``): Requerir letras mayúsculas.
- ``password.require.lowercase`` (valor predeterminado: ``false``): Requerir letras minúsculas.
- ``password.require.digit`` (valor predeterminado: ``false``): Requerir dígitos.
- ``password.require.special.char`` (valor predeterminado: ``false``): Requerir símbolos.

.. note::

   De forma predeterminada, la longitud mínima es ``8`` y todos los requisitos de tipo de carácter están deshabilitados. Para reforzar las contraseñas, configure explícitamente las propiedades anteriores. Tenga en cuenta que |Fess| no cuenta con una función de expiración de contraseñas (cambio periódico forzado); si desea aplicar cambios periódicos de contraseña como regla operativa, hágalo manualmente.

**Hash de contraseñas y límite en bytes:**

|Fess| almacena la contraseña de un usuario local como un hash. ``app.password.algorithm`` (valor predeterminado: ``bcrypt``) selecciona el algoritmo para las contraseñas nuevas y modificadas, y ``app.password.bcrypt.cost`` (valor predeterminado: ``10``) establece el coste de BCrypt. Mientras ``app.password.upgrade.enabled`` sea ``true`` (valor predeterminado), un usuario cuyo hash almacenado es más antiguo (un hash antiguo sin prefijo ``{id}``, el hash de otro algoritmo o un hash BCrypt con un coste menor) recibe un hash nuevo en su siguiente inicio de sesión correcto. El algoritmo es un componente, por lo que un plugin puede proporcionar otro (consulte :ref:`webapp-plugin-password-encoder`).

El límite en bytes pertenece al algoritmo. BCrypt solo lee los primeros 72 bytes de una contraseña en UTF-8, por lo que, desde 15.10, una contraseña de más de 72 bytes se rechaza al establecerla (pantalla de gestión de usuarios, cambio de contraseña forzado en el formulario de inicio de sesión, ``/api/v2/auth/password`` y la API de administración) con "La contraseña no debe superar los 72 bytes.", con independencia de lo que permita ``password.max.length`` (100 caracteres por defecto). Un carácter que no es ASCII ocupa más de un byte (3 bytes la mayoría de los caracteres japoneses, chinos y coreanos). Una cuenta cuya contraseña se estableció antes con más de 72 bytes sigue iniciando sesión, porque la verificación de una contraseña no aplica ningún límite de longitud. Sin embargo, solo se comparan sus primeros 72 bytes, por lo que se acepta cualquier final después del byte 72. Establecer una contraseña nueva (de 72 bytes como máximo) lo elimina.

**Sesiones tras un cambio de contraseña:**

Cuando se cambia la contraseña de un usuario local, ya sea por el propio usuario o por un administrador en la pantalla de administración de usuarios o mediante la API REST de administración, las demás sesiones de inicio de sesión de ese usuario terminan en su siguiente comprobación (véase más abajo). Cada sesión de inicio de sesión consulta en el índice de usuarios la hora del último cambio de contraseña como máximo una vez por ``password.changed.check.interval`` de ``fess_config.properties`` (valor predeterminado: ``60`` segundos; con ``0`` o menos se comprueba en cada solicitud), de modo que las demás sesiones terminan dentro de ese número de segundos, en cualquier nodo. Los usuarios autenticados mediante LDAP o SSO no se ven afectados, porque sus contraseñas se gestionan fuera de |Fess|.

**Sesiones tras un cambio de roles o grupos:**

Cuando se cambian los roles o los grupos de un usuario local después de abrirse una sesión, la sesión de inicio de sesión de ese usuario termina. Esto abarca la edición del usuario (en la pantalla de administración de usuarios o mediante la API REST de administración) y también la eliminación de un rol o de un grupo que el usuario tenía. El intervalo de comprobación es el mismo ``password.changed.check.interval`` (valor predeterminado: ``60`` segundos) que en un cambio de contraseña. A diferencia de un cambio de contraseña, la sesión que realizó el cambio no es una excepción: por ejemplo, cuando un administrador cambia sus propios roles, la sesión del administrador también termina y debe iniciar sesión de nuevo. Una sesión finalizada se registra en el registro de auditoría como ``SESSION_END`` con ``reason`` ``permissions_changed``. Los usuarios autenticados mediante LDAP o SSO no se ven afectados, porque sus roles y grupos se obtienen del proveedor de identidad en cada inicio de sesión.

Cambiar la clave de cifrado
---------------------------

``app.cipher.key`` en ``fess_config.properties`` es la clave que cifra las contraseñas guardadas en las configuraciones de rastreo y de almacén de datos. El valor incluido (``___change__me___``) es público. Si la clave conserva el valor incluido, |Fess| escribe una advertencia en ``fess.log`` al iniciarse. Si la clave está vacía, |Fess| aborta el inicio (consulte :ref:`upgrade-1510-cipher-key`). |Fess| no cambia la clave por sí mismo.

Defínala antes del primer inicio, junto con la contraseña inicial del usuario ``admin``::

    $ bin/fess-setup init

En los paquetes RPM y DEB, ejecute ``/usr/share/fess/bin/fess-setup init``. El comando genera una clave aleatoria o toma la indicada con ``--cipher-key``; consulte :doc:`fess-setup`. Para definirla manualmente, edite ``app.cipher.key`` en ``fess_config.properties`` (``app/WEB-INF/classes/fess_config.properties`` en el paquete ZIP, ``/etc/fess/fess_config.properties`` en los paquetes RPM y DEB). Con el valor predeterminado de ``app.cipher.algorithm`` (``aes``), la clave debe tener 16, 24 o 32 caracteres.

.. warning::

   Si cambia la clave después de guardar contraseñas en configuraciones de rastreo o de almacén de datos, esos valores ya no se podrán descifrar. Conserve la clave junto con sus copias de seguridad de ``fess_config.properties`` y use la misma clave al pasar a otra instalación.

Habilitación del Plugin de Seguridad de OpenSearch
---------------------------------------------------

**Procedimiento:**

1. Elimine o comente la siguiente línea en ``opensearch.yml``::

       # plugins.security.disabled: true

2. Configuración del plugin de seguridad::

       plugins.security.allow_default_init_securityindex: true
       plugins.security.authcz.admin_dn:
         - CN=admin,OU=SSL,O=Test,L=Test,C=DE

3. Configuración de certificados TLS/SSL

4. Reinicie OpenSearch

5. Configure la conexión con OpenSearch en el lado de |Fess|.

   Especifique la URL de conexión mediante la variable de entorno ``SEARCH_ENGINE_HTTP_URL`` (edite ``bin/fess.in.sh`` o el archivo de entorno del servicio; el valor predeterminado proviene de ``search_engine.http.url`` en ``fess_config.properties``)::

       SEARCH_ENGINE_HTTP_URL=https://opensearch:9200

   Especifique las credenciales mediante las siguientes propiedades en ``fess_config.properties`` (los paquetes ZIP, RPM y DEB no tienen las variables de entorno ``SEARCH_ENGINE_USERNAME`` / ``SEARCH_ENGINE_PASSWORD``; las imágenes de docker-fess sí las admiten)::

       search_engine.username=admin
       search_engine.password=<strong_password>

Para más detalles, consulte `OpenSearch Security Plugin <https://opensearch.org/docs/latest/security-plugin/>`__.

Habilitación de HTTPS
---------------------

La comunicación HTTP no está cifrada, lo que conlleva riesgos de escucha y manipulación. Asegúrese de usar HTTPS en entornos de producción.

**Método 1: Uso de Proxy Inverso (Recomendado)**

Coloque Nginx o Apache delante de |Fess| para realizar la terminación HTTPS.

Ejemplo de configuración de Nginx::

    server {
        listen 443 ssl http2;
        server_name your-fess-domain.com;

        ssl_certificate /path/to/cert.pem;
        ssl_certificate_key /path/to/key.pem;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

Si TLS se termina en el proxy inverso, configure también lo siguiente en ``fess_config.properties`` para que la cookie de sesión tenga el atributo ``Secure``. Reinicie |Fess| después de cambiarlo. No lo configure si los usuarios también acceden a |Fess| mediante HTTP sin cifrar, ya que con este valor no se puede establecer la sesión por HTTP::

    session.cookie.secure=true

**Método 2: Configurar HTTPS en Fess Mismo**

Agregue lo siguiente a ``tomcat_config.properties``::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.SSLEnabled=true
    tomcat.certificateKeystoreFile=[ruta al archivo keystore]
    tomcat.certificateKeystorePassword=[contraseña especificada al crear el archivo keystore]
    tomcat.certificateKeyAlias=[alias del certificado]
    tomcat.sslProtocol=[protocolo SSL (ej. TLS)]
    tomcat.enabledProtocols=lista de protocolos habilitados (separados por comas) (ej. TLSv1.2,TLSv1.3)

Configuraciones de Seguridad Recomendadas
==========================================

Configuración del Cortafuegos
------------------------------

Abra solo los puertos necesarios y cierre los puertos innecesarios.

**Puertos que Deben Abrirse:**

- **8080** (o 443 para HTTPS): Interfaz Web de |Fess| (si se requiere acceso externo)
- **22**: SSH (solo para administración, desde direcciones IP confiables únicamente)

**Puertos que Deben Cerrarse:**

- **9200, 9300**: OpenSearch (solo comunicación interna, bloquear acceso externo)

Ejemplo de configuración en Linux (firewalld)::

    $ sudo firewall-cmd --permanent --add-service=https
    $ sudo firewall-cmd --permanent --add-port=8080/tcp  # solo si se accede a Fess directamente por el puerto 8080
    $ sudo firewall-cmd --reload

Restricción de direcciones IP::

    $ sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port port="8080" protocol="tcp" accept'

Configuración de Control de Acceso
-----------------------------------

Considere restringir el acceso a la pantalla de administración a direcciones IP específicas.

Ejemplo de restricción de acceso con Nginx::

    location /admin {
        allow 192.168.1.0/24;
        deny all;

        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
    }

Roles y Control de Acceso
--------------------------

|Fess| proporciona dos roles integrados:

- ``admin``: Rol de administrador que puede realizar todas las operaciones, incluida la pantalla de administración.
- ``guest``: Rol asignado a los usuarios no autenticados (anónimos).

Cualquier otro rol se puede crear libremente desde la pantalla de administración. En |Fess|, un rol es una etiqueta que solo tiene un nombre y se utiliza principalmente para el control de acceso a los resultados de búsqueda (qué documentos puede ver un usuario). La excepción es un rol llamado ``admin-`` seguido del nombre de una pantalla de administración, como ``admin-user`` o ``admin-scheduler``: permite a un usuario abrir esa pantalla, y la forma ``-view``, como ``admin-user-view``, permite el acceso de solo lectura.

.. warning::

   Los roles ``admin-*`` permiten repartir las pantallas de administración de uso diario entre varios operadores, pero no constituyen un límite de privilegios. Un usuario con ``admin-user`` puede asignar cualquier rol existente, incluido el rol de administrador, a cualquier usuario; ``admin-accesstoken`` puede emitir un token de acceso con el permiso ``Radmin-api``, que concede acceso a toda la Admin API; ``admin-scheduler`` puede ejecutar trabajos de script en el servidor, y ``admin-plugin`` puede instalar plugins. Trate cada rol ``admin-*`` como equivalente al rol de administrador (``authentication.admin.roles``, valor predeterminado ``admin``) y concédalo únicamente a operadores de confianza.

Siguiendo el principio de mínimo privilegio, otorgue el rol de administrador (``admin``) únicamente a los usuarios que realizan tareas administrativas y no lo otorgue a los usuarios de búsqueda en general.

**Procedimiento:**

1. Haga clic en "Usuario" → "Rol" en la pantalla de administración
2. Cree los roles necesarios
3. Asigne roles a usuarios en "Usuario" → "Usuario"

Registro de Auditoría
----------------------

El historial de operaciones del sistema, como la autenticación y las operaciones administrativas, se registra de forma predeterminada como registro de auditoría. El registro de auditoría se genera mediante el logger ``fess.log.audit`` definido en ``log4j2.xml``, y su destino de salida predeterminado es ``audit.log``.

Dado que está habilitado de forma predeterminada, no se requiere configuración adicional. Para personalizar el destino de salida o el nivel de registro, edite la siguiente definición en ``log4j2.xml``::

    <Logger name="fess.log.audit" additivity="false" level="info">
        <AppenderRef ref="AuditFile"/>
    </Logger>

Cada registro de auditoría es una línea de campos ``key:value`` separados por tabuladores (LTSV). Un registro empieza con ``action`` y termina con ``ip`` (la dirección IP del cliente) y ``time`` (UTC, ISO 8601). Cuando ``app.audit.log.format`` es ``ecs``, o está vacío y la variable de entorno ``FESS_APP_TYPE`` es ``docker``, los registros se escriben en JSON ECS, con los campos como ``labels.<key>``.

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Acción
     - Campos
     - Se escribe cuando
   * - ``LOGIN``
     - ``user``, ``permissions``
     - un usuario inicia sesión.
   * - ``LOGOUT``
     - ``user``, ``permissions``
     - un usuario cierra sesión.
   * - ``SESSION_END``
     - ``user``, ``reason``
     - |Fess| finaliza por sí mismo una sesión de inicio de sesión, a diferencia de un cierre de sesión que solicita el usuario (este es ``LOGOUT``). Se escribe un registro por cada sesión finalizada.
   * - ``LOGIN_FAILURE``
     - ``class``, ``user``
     - se rechaza un inicio de sesión, en el formulario de inicio de sesión, en la API de inicio de sesión o mediante SSO. También se registra un inicio de sesión que un autenticador SSO rechaza con una excepción.
   * - ``ACCESS``
     - ``user``, ``path``, ``execute``, ``method``, ``id``
     - una solicitud llega a una pantalla de administración o a la API REST de administración, antes de que se ejecute la acción. En la API REST de administración, es después de que se acepte el token de acceso.
   * - ``ACCESS_DENIED``
     - ``user``, ``path``
     - se rechaza una solicitud a una pantalla de administración por los roles del usuario, o la comprobación del token de acceso rechaza una solicitud a la API REST de administración (la API responde con HTTP 401).
   * - ``UPDATE_PASSWORD``
     - ``user``, ``target``
     - se cambia una contraseña: por un usuario desde la pantalla de inicio de sesión o ``/api/v2/auth/password``, o por un administrador que establece una nueva contraseña para un usuario en la pantalla de administración de usuarios o mediante la API REST de administración.
   * - ``UPDATE_PERMISSION``
     - ``user``, ``permissions``
     - se actualizan los permisos de un usuario LDAP.
   * - ``REGISTER_PASSKEY``
     - ``user``, ``target``, ``credentialId``
     - se registra una llave de acceso.
   * - ``DELETE_PASSKEY``
     - ``user``, ``target``, ``credentialId``
     - se elimina una llave de acceso: por el usuario, o por un administrador en la pantalla de administración de usuarios. Cuando un administrador establece una nueva contraseña para un usuario, se eliminan todas las llaves de acceso de ese usuario y se escribe un registro por cada llave.
   * - ``SCRIPT_EXECUTION``
     - ``scriptType``, ``source``, ``user``, ``result``, ``script``
     - se ejecuta un script. Consulte :doc:`../config/scripting-overview`.

- ``LOGIN_FAILURE``: ``user`` es el nombre de usuario escrito y ``class`` es el tipo de credencial. Cuando un autenticador SSO rechaza un inicio de sesión con una excepción, no se ha resuelto ninguna credencial, por lo que el registro no contiene ``user`` ni ``class`` y no se escribe nada de la excepción.
- ``ACCESS``: ``user`` es el usuario que ha iniciado sesión cuando la solicitud lleva una sesión. Cuando se llama a la API REST de administración solo con un token de acceso y sin sesión, es el nombre del token de acceso (el token en sí nunca se escribe; ``-`` cuando no se puede obtener el nombre). ``user`` de ``ACCESS_DENIED`` sigue la misma regla. ``method`` es el método HTTP. ``id`` es el valor del parámetro de solicitud ``id`` y solo se escribe cuando la solicitud lo incluye (no se lee en una solicitud de carga de archivos). No se escribe ningún otro parámetro de la solicitud, porque los formularios de administración contienen contraseñas y claves.
- ``ACCESS_DENIED``: en una solicitud rechazada a la API REST de administración, solo se escribe la ruta de la solicitud. No se registra ni el token de acceso ni el parámetro que lo transportaba.
- ``REGISTER_PASSKEY`` y ``DELETE_PASSKEY``: ``user`` es el usuario que realizó la operación y ``target`` es el nombre del usuario propietario de la llave de acceso. ``credentialId`` son los primeros 8 caracteres del ID de la credencial, seguidos de ``...`` cuando es más largo. La clave de la llave de acceso nunca se escribe.
- ``UPDATE_PASSWORD``: ``user`` es el usuario que cambió la contraseña y ``target`` es el nombre del usuario cuya contraseña se cambió. La contraseña y su hash nunca se escriben, y un cambio rechazado no escribe nada.
- ``SESSION_END``: ``user`` es el usuario cuya sesión terminó y ``reason`` es el motivo. ``password_changed``: la contraseña del usuario se cambió después de abrirse la sesión. ``permissions_changed``: los roles o los grupos del usuario local se cambiaron después de abrirse la sesión (al editar el usuario, o al eliminar un rol o un grupo que el usuario tenía). ``user_not_found``: el documento del usuario local ya no existe, por ejemplo porque el usuario se eliminó o se renombró. ``idp_session_ended``: el proveedor de identidad (IdP) finalizó su sesión (el ``SessionNotOnOrAfter`` de SAML, consulte :doc:`../config/sso-saml`, o el back-channel logout de OpenID Connect, consulte :doc:`../config/sso-oidc`).

Actualizaciones de Seguridad Periódicas
----------------------------------------

Aplique periódicamente actualizaciones de seguridad de |Fess| y OpenSearch.

**Procedimiento Recomendado:**

1. Verifique periódicamente la información de seguridad

   - `Información de lanzamiento de Fess <https://github.com/codelibs/fess/releases>`__
   - `Avisos de seguridad de OpenSearch <https://github.com/opensearch-project/OpenSearch/security/advisories>`__

2. Valide actualizaciones en entorno de prueba
3. Aplique actualizaciones en entorno de producción

Protección de Datos
====================

Cifrado de Respaldos
---------------------

Los datos de respaldo pueden contener información confidencial. Cifre y almacene los archivos de respaldo.

Ejemplo de respaldo cifrado::

    $ tar czf fess-backup.tar.gz /etc/fess
    $ gpg --symmetric --cipher-algo AES256 fess-backup.tar.gz

El directorio de datos de un OpenSearch en ejecución (``/var/lib/opensearch``) no se puede respaldar de forma consistente copiando archivos. Para los datos de los índices, utilice la `función de instantáneas de OpenSearch <https://docs.opensearch.org/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`__. Los datos de configuración de |Fess| se pueden descargar desde la página de copia de seguridad de la pantalla de administración (consulte :doc:`../admin/backup-guide`).

Mejores Prácticas de Seguridad
===============================

Principio de Mínimo Privilegio
-------------------------------

- No ejecutar Fess y OpenSearch como usuario root
- Ejecutar con cuenta de usuario dedicada
- Otorgar privilegios mínimos del sistema de archivos

Aislamiento de Red
------------------

- Colocar OpenSearch en red privada
- Usar VPN o red privada para comunicación interna
- Colocar solo la interfaz Web de |Fess| en DMZ

Auditorías de Seguridad Periódicas
-----------------------------------

- Revisar periódicamente los registros de acceso
- Detectar patrones de acceso anormales
- Realizar escaneos de vulnerabilidades periódicamente

Configuración de Encabezados de Seguridad
------------------------------------------

|Fess| agrega ``X-Frame-Options: SAMEORIGIN`` de forma predeterminada a las respuestas HTML (``response.headers`` en ``fess_config.properties``), por lo que no es necesario añadirlo en el proxy.

Según sea necesario, configure encabezados de seguridad en Nginx o Apache::

    add_header X-Content-Type-Options "nosniff" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

Lista de Verificación de Seguridad
===================================

Antes de implementar en entorno de producción, verifique la siguiente lista de verificación:

Configuración Básica
--------------------

- [ ] Contraseña de administrador cambiada
- [ ] Clave de cifrado (``app.cipher.key``) cambiada respecto al valor incluido
- [ ] HTTPS habilitado
- [ ] Número de puerto predeterminado cambiado (opcional)

Seguridad de Red
----------------

- [ ] Puertos innecesarios cerrados en el cortafuegos
- [ ] Acceso a pantalla de administración restringido por IP (si es posible)
- [ ] Acceso a OpenSearch restringido solo a red interna

Control de Acceso
-----------------

- [ ] Roles y permisos de acceso configurados adecuadamente (otorgar el rol de administrador solo a los usuarios necesarios)
- [ ] Cuentas de usuario innecesarias eliminadas
- [ ] Política de contraseñas configurada

Monitoreo y Registros
----------------------

- [ ] Se ha confirmado que el registro de auditoría está habilitado
- [ ] Período de retención de registros configurado
- [ ] Sistema de monitoreo de registros implementado (si es posible)

Respaldo y Recuperación
------------------------

- [ ] Programación periódica de respaldos configurada
- [ ] Datos de respaldo cifrados
- [ ] Procedimientos de restauración validados

Gestión de Actualizaciones y Parches
-------------------------------------

- [ ] Sistema para recibir notificaciones de actualizaciones de seguridad implementado
- [ ] Procedimientos de actualización documentados
- [ ] Sistema para validar actualizaciones en entorno de prueba implementado

Respuesta a Incidentes de Seguridad
====================================

Procedimientos de respuesta en caso de incidente de seguridad:

1. **Detección de Incidente**

   - Verificar registros
   - Detectar patrones de acceso anormales
   - Verificar comportamiento anormal del sistema

2. **Respuesta Inicial**

   - Identificar alcance del impacto
   - Prevenir expansión del daño (como detener servicios relevantes)
   - Preservar evidencia

3. **Investigación y Análisis**

   - Análisis detallado de registros
   - Identificar ruta de intrusión
   - Identificar datos que pueden haber sido filtrados

4. **Recuperación**

   - Corregir vulnerabilidades
   - Recuperar sistema
   - Fortalecer monitoreo

5. **Respuesta Posterior**

   - Crear informe de incidente
   - Implementar medidas de prevención de recurrencia
   - Informar a partes interesadas

Información de Referencia
==========================

- `OpenSearch Security Plugin <https://opensearch.org/docs/latest/security-plugin/>`__
- `OWASP Top 10 <https://owasp.org/www-project-top-ten/>`__
- `CIS Benchmarks <https://www.cisecurity.org/cis-benchmarks/>`__

Si tiene preguntas o problemas relacionados con la seguridad, contacte:

- Issues: https://github.com/codelibs/fess/issues
- Soporte Comercial: https://www.n2sm.net/
