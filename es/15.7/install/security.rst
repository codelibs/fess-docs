=======================
Configuración de Seguridad
=======================

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

   Una vez que haya cambiado la contraseña desde ``admin``, no podrá volver a establecerla en un valor simple como ``admin`` (una lista negra de contraseñas de administrador está configurada mediante ``password.invalid.admin.passwords``). También puede cambiar la contraseña inicial del usuario ``admin`` antes del primer inicio estableciendo ``index.user.initial_password`` en ``fess_config.properties``.

|Fess| ofrece una función integrada que aplica los requisitos de longitud mínima/máxima y de tipos de caracteres de la contraseña. Configure las siguientes propiedades en ``fess_config.properties`` (los valores predeterminados se indican entre paréntesis):

- ``password.min.length`` (valor predeterminado: ``8``): Longitud mínima. Se recomienda 12 o más.
- ``password.max.length`` (valor predeterminado: ``100``): Longitud máxima.
- ``password.require.uppercase`` (valor predeterminado: ``false``): Requerir letras mayúsculas.
- ``password.require.lowercase`` (valor predeterminado: ``false``): Requerir letras minúsculas.
- ``password.require.digit`` (valor predeterminado: ``false``): Requerir dígitos.
- ``password.require.special.char`` (valor predeterminado: ``false``): Requerir símbolos.

.. note::

   De forma predeterminada, la longitud mínima es ``8`` y todos los requisitos de tipo de carácter están deshabilitados. Para reforzar las contraseñas, configure explícitamente las propiedades anteriores. Tenga en cuenta que |Fess| no cuenta con una función de expiración de contraseñas (cambio periódico forzado); si desea aplicar cambios periódicos de contraseña como regla operativa, hágalo manualmente.

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

   Especifique las credenciales mediante las siguientes propiedades en ``fess_config.properties`` (no existen las variables de entorno ``SEARCH_ENGINE_USERNAME`` / ``SEARCH_ENGINE_PASSWORD``)::

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

**Método 2: Configurar HTTPS en Fess Mismo**

Agregue lo siguiente a ``tomcat_config.properties``::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.SSLEnabled=true
    tomcat.certificateKeystoreFile=[ruta al archivo keystore]
    tomcat.certificateKeystorePassword=[contraseña especificada al crear el archivo keystore]
    tomcat.certificateKeyAlias=[alias del certificado]
    tomcat.sslProtocol=[protocolo SSL (ej. TLS)]
    tomcat.enabledProtocols=lista de protocolos habilitados (separados por comas) (ej. TLSv1.2,TLSv1.1,TLSv1)

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

    $ sudo firewall-cmd --permanent --add-service=http
    $ sudo firewall-cmd --permanent --add-service=https
    $ sudo firewall-cmd --permanent --remove-service=opensearch  # en caso de servicio personalizado
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

Cualquier otro rol se puede crear libremente desde la pantalla de administración. En |Fess|, un rol es una etiqueta que solo tiene un nombre y se utiliza principalmente para el control de acceso a los resultados de búsqueda (qué documentos puede ver un usuario). Un rol en sí no está vinculado a permisos administrativos concretos, como "gestionar configuraciones de rastreo" o "editar resultados de búsqueda".

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

Actualizaciones de Seguridad Periódicas
----------------------------------------

Aplique periódicamente actualizaciones de seguridad de |Fess| y OpenSearch.

**Procedimiento Recomendado:**

1. Verifique periódicamente la información de seguridad

   - `Información de lanzamiento de Fess <https://github.com/codelibs/fess/releases>`__
   - `Avisos de seguridad de OpenSearch <https://opensearch.org/security.html>`__

2. Valide actualizaciones en entorno de prueba
3. Aplique actualizaciones en entorno de producción

Protección de Datos
====================

Cifrado de Respaldos
---------------------

Los datos de respaldo pueden contener información confidencial. Cifre y almacene los archivos de respaldo.

Ejemplo de respaldo cifrado::

    $ tar czf fess-backup.tar.gz /var/lib/opensearch /etc/fess
    $ gpg --symmetric --cipher-algo AES256 fess-backup.tar.gz

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

Según sea necesario, configure encabezados de seguridad en Nginx o Apache::

    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Content-Security-Policy "default-src 'self'" always;

Lista de Verificación de Seguridad
===================================

Antes de implementar en entorno de producción, verifique la siguiente lista de verificación:

Configuración Básica
--------------------

- [ ] Contraseña de administrador cambiada
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
