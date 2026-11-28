================================================
Proteger la búsqueda con SSO y control de acceso
================================================

Introducción
============

Una plataforma de búsqueda interna reúne documentos protegidos por permisos.
En lugar de repartir contraseñas propias de Fess, en la mayoría de las implantaciones se quiere que los usuarios inicien sesión a través del proveedor de identidad (IdP) de la organización y que los resultados de búsqueda se filtren según sus grupos.

En este artículo configuramos lo siguiente en Fess 15.9 y llegamos hasta comprobar que funciona.

- Inicio de sesión único (SSO) con Entra ID, OpenID Connect, SAML o SPNEGO
- Impedir que los usuarios que no han iniciado sesión busquen, mediante "Requiere inicio de sesión"
- Hacer que Fess reconozca correctamente HTTPS detrás de un proxy inverso que termina TLS
- Revisar los tokens de acceso y los periodos de conservación del registro de auditoría y del registro de búsqueda

Cómo diseñar roles y grupos, y cómo indicarlos en los permisos de las configuraciones de rastreo, se trata en :doc:`guide-05`.

El SSO se proporciona mediante plugins
======================================

En Fess 15.9, el procesamiento de autenticación SSO se separó del núcleo en cuatro plugins.

.. list-table::
   :header-rows: 1
   :widths: 16 18 18 22 26

   * - Método
     - Plugin
     - "SSO Type" (``sso.type``)
     - Origen del nombre de usuario
     - Origen de los grupos y roles
   * - Microsoft Entra ID
     - ``fess-sso-entraid``
     - Entra ID (``entraid``)
     - Nombre de usuario de la cuenta que ha iniciado sesión (normalmente el UPN)
     - Grupos y roles obtenidos mediante Microsoft Graph
   * - OpenID Connect
     - ``fess-sso-oidc``
     - OpenID Connect (``oic``)
     - Claim ``email`` del ID Token
     - Claim ``groups`` del ID Token. Los roles provienen solo de "Roles por defecto"
   * - SAML 2.0
     - ``fess-sso-saml``
     - SAML (``saml``)
     - NameID de la aserción
     - Valores de los atributos indicados en "Nombre del atributo de grupo" (por defecto ``memberOf``) y "Nombre del atributo de rol"
   * - SPNEGO (Kerberos)
     - ``fess-sso-spnego``
     - SPNEGO (``spnego``)
     - Parte del principal de Kerberos anterior a ``@``
     - Grupos obtenidos con la configuración LDAP de [General]

Solo en OpenID Connect el nombre del plugin (``oidc``) difiere del valor de ``sso.type`` (``oic``).

El procedimiento es el mismo para todos los métodos.

1. Instalar el plugin y reiniciar Fess
2. Registrar Fess en el IdP. La dirección de retorno (URI de redirección o URL de ACS) es ``https://<host de Fess>/sso/``
3. En la consola de administración, en [Sistema] > [General], introducir los datos del IdP en la sección del método, seleccionar "SSO Type" y actualizar
4. Abrir ``https://<host de Fess>/sso/`` en un navegador y comprobar que se puede iniciar sesión a través del IdP

Instalar el plugin
------------------

La imagen de Docker (``ghcr.io/codelibs/fess:15.9.0``) incluye los cuatro plugins de SSO (las imágenes cuyo nombre lleva ``-slim`` no los incluyen).
No se incluyen en los paquetes ZIP, DEB y RPM, así que instálelos desde [Instalar] en [Sistema] > [Plugin], o con el siguiente comando.

::

    $ bin/fess-setup install plugin fess-sso-entraid

Después de instalar o eliminar un plugin, reinicie Fess.
Use plugins de la misma versión menor que Fess (15.9.x).

Si selecciona un "SSO Type" sin tener el plugin instalado, ``/sso/`` solo vuelve a la pantalla de inicio de sesión, y en ``fess.log`` se escribe una vez un WARN ``No SSO authenticator is registered as ...``.

Dónde se guarda la configuración
--------------------------------

Los valores introducidos en [General] se guardan en ``system.properties`` (``app/WEB-INF/conf/`` en el paquete ZIP, ``/etc/fess/`` en DEB y RPM).
La configuración de OpenID Connect, SAML y Entra ID se lee en cada inicio de sesión, por lo que se aplica en cuanto se guarda, sin reiniciar.
La configuración de SPNEGO se comparte en todo el proceso, por lo que es necesario reiniciar después de cambiarla.

El contenedor ``fess01`` de Docker no tiene volumen, así que la configuración de [General] se pierde si ejecuta ``docker compose down`` y después ``up``.
Antes de recrear el contenedor, descargue ``system.properties`` desde [Información del sistema] > [Copia de seguridad] y, después de recrearlo, súbalo desde la misma pantalla para restaurarla.

SSO con Entra ID
================

En organizaciones que usan Microsoft 365, ``fess-sso-entraid`` es la opción más sencilla.
Los grupos se obtienen de Microsoft Graph después del inicio de sesión, por lo que no es necesario configurar notificaciones de grupo en el IdP.

Configuración en Entra ID
-------------------------

En Azure Portal, cree un nuevo registro en "Registros de aplicaciones" y configúrelo de la siguiente manera.

- Tipos de cuenta compatibles: Solo cuentas en este directorio organizativo
- URI de redirección: ``https://fess.example.com/sso/`` con la plataforma "Web" (debe coincidir exactamente, incluida la ``/`` final)
- En "Certificados y secretos", cree un secreto de cliente y anote su valor (solo se muestra justo después de crearlo)
- En "Permisos de API", agregue los permisos delegados de Microsoft Graph ``User.Read`` y ``GroupMember.Read.All``, y conceda el consentimiento de administrador

Sin ``GroupMember.Read.All``, no se pueden obtener los grupos principales anidados, y en ``fess.log`` aparece la advertencia ``Not allowed to read the parent groups of ...``.

Configuración en Fess
---------------------

Introduzca los valores en la sección "Entra ID" de [Sistema] > [General].

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Campo
     - Clave
     - Valor
   * - Inquilino (ID o dominio)
     - ``entraid.tenant``
     - Id. de directorio (inquilino), o ``yourcompany.onmicrosoft.com``
   * - ID de cliente
     - ``entraid.client.id``
     - Id. de aplicación (cliente)
   * - Secreto de cliente
     - ``entraid.client.secret``
     - Valor del secreto creado
   * - URL de respuesta
     - ``entraid.reply.url``
     - ``https://fess.example.com/sso/``

Por último, seleccione "Entra ID" en "SSO Type" de la sección "Sistema" y haga clic en [Actualizar].

Hacer coincidir los grupos con los permisos de los documentos
-------------------------------------------------------------

De los grupos y roles obtenidos de Entra ID, su ID (GUID) siempre se convierte en permiso.
Además, los valores de los atributos indicados en "Campos de permisos" (``entraid.permission.fields``, por defecto ``mail``) también se convierten en permisos.

Los grupos de seguridad no están habilitados para correo, por lo que con el valor por defecto solo su GUID se convierte en permiso.
Si las ACL del servidor de archivos están escritas con nombres de grupo, establezca "Campos de permisos" en ``mail,displayName``.
Sin embargo, ``displayName`` no es único, por lo que un grupo con el mismo nombre que un grupo integrado de Windows (como ``Administrators``) también coincide con los documentos de ese grupo integrado.

En los permisos de la configuración de rastreo, escriba el valor obtenido tal cual, con el prefijo ``{group}`` (por ejemplo, ``{group}sales@example.com``).

.. warning::

   Los "Roles por defecto" (``entraid.default.roles``) se asignan a todos los usuarios del inquilino.
   Si pone ``admin`` aquí, todos podrán entrar en la consola de administración.

SSO con OpenID Connect, SAML o SPNEGO
=====================================

OpenID Connect
--------------

La integración con proveedores de OpenID Connect como Keycloak u Okta se realiza con ``fess-sso-oidc``.
En el proveedor, registre Fess como aplicación web (cliente) y establezca el URI de redirección en ``https://fess.example.com/sso/``.

Los principales campos que se introducen en la sección "OpenID Connect" de [General] son los siguientes.

- URL del servidor de autorización (``oic.auth.server.url``) y URL del servidor de tokens (``oic.token.server.url``): introduzca por separado los valores que figuran en ``/.well-known/openid-configuration`` del proveedor. La URL del servidor de tokens debe usar ``https`` (solo se permite ``http`` para ``localhost``, ``127.x.x.x`` y ``::1``)
- ID de cliente y Secreto de cliente
- Scope: ``openid email``. El nombre de usuario se toma del claim ``email``, por lo que ``email`` es obligatorio
- URL base (``oic.base.url``): ``https://fess.example.com``. Si deja vacía la URL de redirección, pasa a ser ``{URL base}/sso/``

En cuanto a los grupos, los valores del claim ``groups`` del ID Token se convierten tal cual en permisos.
A diferencia de Entra ID, no se recorren los grupos principales, así que, si necesita grupos anidados, inclúyalos en el claim desde el proveedor.
Los roles no se toman de los claims; solo se asignan los valores de "Roles por defecto".

``oic.issuer``, que valida el emisor (``iss``), no tiene campo en [General], así que escríbalo directamente en ``system.properties``.

SAML
----

Con ``fess-sso-saml``, Fess actúa como SP.
El IdP devuelve la aserción mediante un POST entre sitios, por lo que con el valor por defecto ``tomcat.sameSiteCookies = lax`` el inicio de sesión no se completa.
Cámbielo de la siguiente manera en ``tomcat_config.properties`` y reinicie Fess.

::

    tomcat.sameSiteCookies = none

``none`` solo funciona con HTTPS.
Con HTTP simple ya no se podrá iniciar sesión, así que complete primero la configuración de HTTPS que se describe más adelante.

Introduzca lo siguiente en la sección "SAML" de [General].

- URL base del SP (``saml.sp.base.url``): ``https://fess.example.com``. A partir de ella se determinan el Entity ID del SP (``{URL base del SP}/sso/metadata``) y la URL de ACS (``{URL base del SP}/sso/``)
- IdP Entity ID, IdP SSO URL y Certificado X.509 del IdP: cópielos de la consola de administración del IdP. Introduzca el certificado en Base64 en una sola línea, sin las líneas ``-----BEGIN CERTIFICATE-----``
- Nombre del atributo de grupo (por defecto ``memberOf``) y Nombre del atributo de rol: ajústelos a los nombres de atributo que envía el IdP

No existe una función para cargar la URL de metadatos del IdP.
A la inversa, los metadatos de SP de Fess se pueden obtener en ``https://fess.example.com/sso/metadata`` y cargarlos en el IdP.
El nombre de usuario es el NameID, y el formato de NameID es, por defecto, el de dirección de correo electrónico.
Solo se admite el inicio de sesión iniciado por el SP, que comienza en ``/sso/`` de Fess; los inicios de sesión lanzados desde un icono del portal del IdP se rechazan.

En producción, agregue ``saml.security.want_assertions_signed=true`` a ``system.properties`` para exigir aserciones firmadas.
La configuración de firma y cifrado no tiene campos en [General] y tampoco puede indicarse como propiedades del sistema de la JVM, así que escríbala directamente en el archivo.

.. warning::

   Si se establece "Nombre del atributo de rol", los valores enviados por el IdP se convierten tal cual en roles de Fess.
   El rol de administrador es ``authentication.admin.roles=admin``, por lo que un usuario para el que el IdP envíe ``admin`` se convierte en administrador.

SPNEGO (autenticación integrada de Windows)
-------------------------------------------

Para que los usuarios de equipos Windows unidos al dominio inicien sesión sin escribir contraseña, use ``fess-sso-spnego``.
Es necesario registrar un SPN en AD (``setspn -S HTTP/<nombre de host de Fess> <cuenta de servicio>``), crear ``krb5.conf`` y ``auth_login.conf`` en ``app/WEB-INF/classes/`` y configurar las opciones de intranet del navegador.
Los grupos se obtienen de AD con la configuración de la sección "LDAP" de [General].
Siga el procedimiento de `Configuración de SSO con Auth Integrada de Windows <https://fess.codelibs.org/es/stable/config/sso-spnego.html>`__ y reinicie Fess después de cambiar los campos de SPNEGO de [General].

Comprobar que el SSO funciona
=============================

Primero, sin haber iniciado sesión, abra ``https://fess.example.com/sso/`` y compruebe que se le lleva a la pantalla de inicio de sesión del IdP.

Después de iniciar sesión, abra ``https://fess.example.com/api/v2/auth/me`` en el mismo navegador.

::

    {"response":{"status":0,"authenticated":true,"user":{"user_id":"taro@example.com", ...
      "groups":[...],"permissions":[...],"admin":false,"permission_state":"RESOLVED"}}}

Compruebe que ``groups`` contiene los grupos esperados y que ``admin`` es el previsto.
Con Entra ID, los grupos se obtienen después del inicio de sesión, por lo que justo después ``permission_state`` es ``PENDING`` y cambia a ``RESOLVED`` cuando termina la obtención.

En el registro de auditoría ``audit.log`` también se registra una línea ``LOGIN`` con el nombre de usuario y los permisos.

Si el inicio de sesión falla, se vuelve a la pantalla de inicio de sesión y se muestra "Error en el proceso de inicio de sesión SSO."
La causa aparece en un WARN de ``fess.log`` (por ejemplo, ``Failed to process SSO login``).

Aunque la configuración de SSO sea incorrecta, puede iniciar sesión con el usuario local ``admin`` desde ``/login/`` y corregirla.

.. note::

   A los usuarios que han iniciado sesión no se les asigna ``{role}guest``.
   Los documentos de las configuraciones de rastreo que solo tienen el ``{role}guest`` por defecto desaparecen de los resultados de búsqueda de los usuarios que inician sesión con SSO.
   Para saber cómo componer los permisos, consulte :doc:`guide-05`.

Impedir que busquen los usuarios que no han iniciado sesión
===========================================================

Si activa "Requiere inicio de sesión" en [Sistema] > [General], los usuarios que no han iniciado sesión ya no pueden buscar.

- Si el SSO está disponible (el plugin está instalado y hay un "SSO Type" seleccionado), los usuarios que abren la pantalla de búsqueda del tema incluido ``bootstrap`` se envían automáticamente a ``/sso/`` y, tras iniciar sesión en el IdP, vuelven a su búsqueda original
- Sin SSO, se muestra un cuadro de diálogo de inicio de sesión en la pantalla de búsqueda
- La API de búsqueda de ``/api/v2/`` tampoco puede usarse de forma anónima; solo se aceptan las llamadas con un token de acceso

Aunque no active "Requiere inicio de sesión", si el SSO está disponible y "Mostrar enlace de inicio de sesión" está activado, el enlace de inicio de sesión de la pantalla de búsqueda apunta a ``/sso/``.

Publicar con HTTPS
==================

Terminar TLS en un proxy inverso
--------------------------------

En una configuración en la que Nginx u otro proxy termina TLS y reenvía a Fess por HTTP, las solicitudes que recibe Fess aparecen como ``http://``.
En ese estado, la validación de la aserción SAML (comparación de ``Destination``) falla, y SPNEGO no ofrece la alternativa de autenticación Basic.

En ``tomcat_config.properties``, indique a Fess el esquema y el puerto que se ven desde fuera.
Este archivo está en ``lib/classes/`` en el paquete ZIP, y en ``/etc/fess/`` en DEB, RPM y la imagen de Docker.

::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.proxyPort=443

En el proxy, pase a Fess el encabezado ``Host`` original sin cambios (en Nginx, ``proxy_set_header Host $host;``).
Esto se debe a que Fess construye el nombre de host de la URL de la solicitud a partir del encabezado ``Host``.

Además, establezca ``session.cookie.secure=true`` en ``fess_config.properties`` para añadir el atributo ``Secure`` a la cookie de sesión.
Por defecto (vacío) se deja la decisión a Tomcat, pero en entornos de producción en los que un proxy termina TLS, indique ``true`` explícitamente.
Si usa ``tomcat.sameSiteCookies = none`` para SAML, las cookies ``SameSite=None`` también requieren el atributo ``Secure``.

Después de modificar cualquiera de los dos archivos, es necesario reiniciar Fess.

Recibir TLS directamente en Fess
--------------------------------

Si no usa proxy, establezca ``tomcat.SSLEnabled=true``, ``tomcat.certificateKeystoreFile``, ``tomcat.certificateKeystorePassword``, ``tomcat.certificateKeyAlias``, etc. en ``tomcat_config.properties``.
Para ver un ejemplo de configuración, consulte `Configuración de Seguridad <https://fess.codelibs.org/es/stable/install/security.html>`__.

Cerrar el puerto de OpenSearch
------------------------------

El ``compose-opensearch3.yaml`` de docker-fess expone OpenSearch, con el plugin de seguridad desactivado, en el puerto 9200 del host.
Fess se conecta por la red entre contenedores (``http://search01:9200``), así que en un servidor compartido puede quitar ``ports`` de ``search01``.

Gestionar los tokens de acceso
==============================

Los tokens con los que los sistemas de negocio llaman a la API se crean en [Sistema] > [Token de acceso].
Cómo llamar a la API se trata en :doc:`guide-11`; aquí solo enumeramos los puntos para operarlos de forma segura.

- Asigne a un token de búsqueda solo los permisos de los documentos que ese sistema puede ver (por ejemplo, ``{group}sales``)
- Un token con ``{role}admin-api`` puede usar no solo el registro de documentos, sino todos los endpoints de la Admin API. No existe un permiso más limitado del tipo "solo registro"
- Establezca "Caduca" y vuelva a crear el token cuando caduque. Elimine los tokens que ya no necesite
- Guarde los tokens en el servidor; no los incruste en JavaScript que se ejecute en el navegador
- Deje vacío "Nombre del parámetro". Si lo establece, se pueden añadir permisos mediante un parámetro de URL
- Trate el rol ``admin-accesstoken``, que puede emitir tokens, y el rol ``admin-accesstoken-view``, que puede mostrar sus valores, como equivalentes a un administrador

Decidir cuánto tiempo se conservan los registros
================================================

La ubicación de los archivos de registro y su supervisión se tratan en :doc:`guide-10`.
Aquí ordenamos los registros que se usan en las revisiones de seguridad y sus periodos de conservación.

El registro de auditoría (``audit.log``) registra, una línea por evento, los inicios de sesión (``LOGIN``), los inicios de sesión fallidos (``LOGIN_FAILURE``), los cierres de sesión (``LOGOUT``), los accesos a la consola de administración y a la Admin API (``ACCESS``), los rechazos por falta de privilegios (``ACCESS_DENIED``), etc.
El archivo se escribe en ``logs/`` en el paquete ZIP, y en ``/var/log/fess/`` en DEB, RPM y la imagen de Docker; también puede descargarse desde [Información del sistema] > [Archivo de registro].
El formato por defecto es LTSV; en la imagen de Docker es JSON en formato ECS.
Los archivos rotados se eliminan a los 360 días (``backup.audit.max.age`` de ``log4j2.xml``).

Quién buscó qué queda en el registro de búsqueda guardado en OpenSearch, que puede consultarse en [Información del sistema] > [Registro de búsqueda].
El valor por defecto de "Eliminar registros de búsqueda anteriores" en [General] es ``-1``, con lo que los registros de búsqueda se conservan sin eliminarse.
Este número de días también se aplica al registro de clics, al registro de favoritos y al registro de chat.
Si las normas internas fijan un periodo de conservación, introduzca ese número de días.

Funcionamiento con varias instancias
====================================

En Fess 15.9, las sesiones de inicio de sesión se mantienen en la memoria de cada proceso de Fess.
Los valores que se usan durante el SSO (el ``state`` de OpenID Connect y el ID de AuthnRequest de SAML) también se guardan en la sesión, así que, si coloca varias instancias detrás de un balanceador de carga, active las sesiones persistentes (sticky sessions) para que el mismo usuario se dirija siempre al mismo Fess.
Para la configuración con varias instancias en sí, consulte :doc:`guide-14`.

Tenga en cuenta que guardar las sesiones en OpenSearch para compartirlas entre varias instancias y el inicio de sesión con llave de acceso (passkey) de los usuarios locales son funciones de la versión 15.10 y posteriores.

Artículos siguientes
====================

- Diseño de roles y grupos, y cómo escribir los permisos en las configuraciones de rastreo: :doc:`guide-05`
- Integración por API con tokens de acceso: :doc:`guide-11`
- Ubicación de los registros, supervisión y copias de seguridad: :doc:`guide-10`
- Ampliación a una configuración con varias instancias: :doc:`guide-14`
- Reflejar las ACL del servidor de archivos en los resultados de búsqueda: :doc:`file-server-search`

Referencias
===========

- `Configuración de SSO con Entra ID <https://fess.codelibs.org/es/stable/config/sso-entraid.html>`__
- `Configuración de SSO con OpenID Connect <https://fess.codelibs.org/es/stable/config/sso-oidc.html>`__
- `Configuración de SSO con autenticación SAML <https://fess.codelibs.org/es/stable/config/sso-saml.html>`__
- `Configuración de SSO con Auth Integrada de Windows <https://fess.codelibs.org/es/stable/config/sso-spnego.html>`__
- `General <https://fess.codelibs.org/es/stable/admin/general-guide.html>`__
- `Token de Acceso <https://fess.codelibs.org/es/stable/admin/accesstoken-guide.html>`__
- `Configuración de Seguridad <https://fess.codelibs.org/es/stable/install/security.html>`__
- `Configuración de Registro <https://fess.codelibs.org/es/stable/config/admin-logging.html>`__
