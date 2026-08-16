==========================================
Configuración de SSO con Entra ID
==========================================

Descripción general
===================

|Fess| soporta autenticación Single Sign-On (SSO) utilizando Microsoft Entra ID (anteriormente Azure AD).
Al utilizar la autenticación de Entra ID, puede integrar la información de usuario y la información de grupo de su entorno Microsoft 365 con la búsqueda basada en roles de |Fess|.

Cómo funciona la autenticación de Entra ID
------------------------------------------

En la autenticación de Entra ID, |Fess| opera como un cliente OAuth 2.0/OpenID Connect y colabora con Microsoft Entra ID para la autenticación.

1. El usuario accede al endpoint SSO de |Fess| (``/sso/``)
2. |Fess| redirige al endpoint de autorización de Entra ID
3. El usuario se autentica con Entra ID (inicio de sesión de Microsoft)
4. Entra ID redirige el código de autorización a |Fess|
5. |Fess| utiliza el código de autorización para obtener un token de acceso
6. El usuario inicia sesión
7. En segundo plano, |Fess| utiliza la API de Microsoft Graph para recuperar la información de grupo y rol del usuario, y la aplica a la búsqueda basada en roles en cuanto finaliza la resolución

.. note::
   A partir de |Fess| 15.8, la respuesta de autorización del paso 4 se devuelve como una solicitud
   GET, ya que |Fess| solicita ``response_mode=query`` al endpoint de autorización. Hasta la
   versión 15.7 se devolvía mediante un POST entre sitios, y el valor por defecto incluido
   ``tomcat.sameSiteCookies = lax`` no envía la cookie de sesión en ese caso, por lo que era
   necesario ``tomcat.sameSiteCookies = none`` como solución alternativa. Si configuró ``none``
   únicamente por ese motivo, puede volver al valor por defecto.

Para la integración con la búsqueda basada en roles, consulte :doc:`security-role`.

Prerrequisitos
==============

Antes de configurar la autenticación de Entra ID, verifique los siguientes prerrequisitos:

- |Fess| 15.8 o superior está instalado
- Un tenant de Microsoft Entra ID (Azure AD) está disponible
- |Fess| es accesible a través de HTTPS (requerido para entornos de producción)
- Tiene permiso para registrar aplicaciones en Entra ID

Configuración básica
====================

Habilitar SSO
-------------

Para habilitar la autenticación de Entra ID, agregue la siguiente configuración en ``app/WEB-INF/conf/system.properties``:

::

    sso.type=entraid

Configuración requerida
-----------------------

Configure la información obtenida de Entra ID.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``entraid.tenant``
     - ID del tenant (ej: ``xxx.onmicrosoft.com``)
     - (Requerido)
   * - ``entraid.client.id``
     - ID de aplicación (Cliente)
     - (Requerido)
   * - ``entraid.client.secret``
     - Valor del secreto del cliente
     - (Requerido)
   * - ``entraid.reply.url``
     - URI de redirección (URL de callback)
     - Usa la URL de la solicitud

.. note::
   En lugar del prefijo ``entraid.*``, también puede usar el prefijo legacy ``aad.*`` para compatibilidad con versiones anteriores.

Configuración opcional
----------------------

Las siguientes configuraciones pueden agregarse según sea necesario.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripción
     - Por defecto
   * - ``entraid.authority``
     - URL del servidor de autenticación
     - ``https://login.microsoftonline.com/``
   * - ``entraid.state.ttl``
     - Tiempo de vida del state (segundos)
     - ``3600``
   * - ``entraid.response.mode``
     - Forma en que se devuelve la respuesta de autorización. Puede ser ``query`` o ``form_post``.
     - ``query``
   * - ``entraid.default.groups``
     - Grupos por defecto (separados por comas). Se aplican a todos los usuarios de Entra ID.
     - (Ninguno)
   * - ``entraid.default.roles``
     - Roles por defecto (separados por comas). Se aplican a todos los usuarios de Entra ID.
     - (Ninguno)
   * - ``entraid.permission.fields``
     - Campos de grupo/rol (separados por comas) que se utilizan adicionalmente como valores de permiso. El ID de grupo/rol (GUID) siempre se usa como permiso, y los valores de los campos especificados aquí (ej: ``mail``) se agregan. Solo pueden utilizarse campos cuyo valor sea una cadena de texto. Microsoft Graph devuelve un campo como ``securityEnabled`` en forma de booleano y ``groupTypes`` en forma de lista, y ninguno de los dos puede convertirse en un valor de permiso, por lo que un campo así se ignora y se escribe en el registro una advertencia que indica su nombre.
     - ``mail``
   * - ``entraid.use.ds``
     - Integración con el servicio de dominio. Cuando es ``true``, para los valores de permiso en formato ``name@domain``, la parte local (``name``) con la parte del dominio eliminada también se agrega como permiso. Esto se aplica no solo a los grupos y roles, sino también al propio usuario que ha iniciado sesión: la parte local de su nombre principal de usuario (UPN) se agrega como permiso a nivel de usuario. Por lo tanto, establecerlo en ``false`` elimina también ese permiso a nivel de usuario, no solo los de los grupos.
     - ``true``

.. note::

   El ID de grupo/rol (GUID) siempre se usa como permiso, pero solo los grupos habilitados para
   correo tienen un valor ``mail``. Los grupos de Microsoft 365 están habilitados para correo, por
   lo que su nombre también se registra como permiso. **Los grupos de seguridad no están
   habilitados para correo, por lo que con el valor predeterminado solo su GUID se convierte en un
   permiso.** Si los derechos de acceso del sistema de archivos indican un grupo de seguridad, los
   permisos no coinciden y esos documentos no aparecen en los resultados de búsqueda.

   En ese caso, agregue ``displayName``, que todos los grupos tienen:

   .. code-block:: properties

      entraid.permission.fields=mail,displayName

   ``displayName`` no está calificado por dominio ni es único, por lo que no forma parte del valor
   predeterminado. Por ejemplo, si Entra ID tiene un grupo llamado ``Administrators``, también
   coincidirá con documentos cuyos derechos de acceso indiquen el grupo integrado de Windows
   ``Administrators``. Antes de agregarlo, compruebe que los nombres no entren en conflicto con los
   que ya se usan en sus derechos de acceso.

.. note::
   Con el valor por defecto ``query``, el código de autorización se incluye en la cadena de
   consulta de la URL de callback. ``form_post`` mantiene el código fuera de la URL y, por lo
   tanto, fuera del historial del navegador y de los registros de acceso de cualquier proxy
   frontal o WAF, pero convierte el callback en un POST entre sitios y requiere
   ``tomcat.sameSiteCookies = none``. Sin esa configuración, la cookie de sesión no se devuelve y
   el inicio de sesión falla. Además, los navegadores solo aceptan ``none`` en una cookie que
   también tenga el atributo ``Secure``, por lo que ``form_post`` exige servir |Fess| mediante
   HTTPS: sobre HTTP simple el navegador ni siquiera almacena la cookie de sesión y el inicio de
   sesión sigue fallando. Por ello, la mayoría de las instalaciones deberían mantener el valor por
   defecto. Cualquier otro valor se ignora con una advertencia y se utiliza ``query``.

.. warning::

   ``entraid.default.groups`` y ``entraid.default.roles`` son valores globales únicos, sin ámbito
   por usuario. |Fess| los aplica a todos los usuarios de Entra ID al iniciar sesión y vuelve a
   aplicarlos en cada resolución posterior, por lo que Microsoft Graph nunca los retira. En
   particular, no ponga nunca el rol de administrador de |Fess| — ``admin`` con el valor
   ``authentication.admin.roles`` que se incluye — en ``entraid.default.roles``: eso concede a
   todos los usuarios del inquilino acceso permanente a las pantallas de administración.

Configuración del lado de Entra ID
==================================

Registro de aplicación en Azure Portal
--------------------------------------

1. Inicie sesión en `Azure Portal <https://portal.azure.com/>`_

2. Seleccione **Microsoft Entra ID**

3. Vaya a **Administrar** → **Registros de aplicaciones** → **Nuevo registro**

4. Registre la aplicación:

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - Configuración
        - Valor
      * - Nombre
        - Cualquier nombre (ej: Fess SSO)
      * - Tipos de cuenta compatibles
        - "Solo cuentas en este directorio organizativo"
      * - Plataforma
        - Web
      * - URI de redirección
        - ``https://<host de Fess>/sso/``

5. Haga clic en **Registrar**

Crear un secreto de cliente
---------------------------

1. En la página de detalles de la aplicación, haga clic en **Certificados y secretos**

2. Haga clic en **Nuevo secreto de cliente**

3. Establezca una descripción y una fecha de expiración, luego haga clic en **Agregar**

4. Copie y guarde el **Valor** generado (este valor no se mostrará nuevamente)

.. warning::
   El valor del secreto del cliente solo se muestra inmediatamente después de la creación.
   Asegúrese de registrarlo antes de salir de la página.

Configurar permisos de API
--------------------------

1. Haga clic en **Permisos de API** en el menú izquierdo

2. Haga clic en **Agregar un permiso**

3. Seleccione **Microsoft Graph**

4. Seleccione **Permisos delegados**

5. Agregue el siguiente permiso:

   - ``User.Read`` - Requerido para recuperar las pertenencias a grupos del usuario que ha iniciado sesión (``/me/memberOf``). Se concede por defecto al crear el registro de la aplicación
   - ``GroupMember.Read.All`` - Requerido para leer atributos del grupo, como su nombre, y para resolver los grupos anidados

6. Haga clic en **Agregar permisos**

7. Haga clic en **Conceder consentimiento de administrador para <nombre del tenant>**

.. note::
   El consentimiento del administrador requiere privilegios de administrador del tenant.

.. note::
   En lugar de ``GroupMember.Read.All`` también se pueden conceder ``Group.Read.All`` o
   ``Directory.Read.All``: la lectura de los atributos del grupo y la resolución de los grupos
   anidados siguen funcionando. Sin embargo, ``/me/memberOf`` no está autorizado por
   ``Group.Read.All``, por lo que ``User.Read`` es necesario en cualquier caso.

.. note::
   Los permisos anteriores no cubren el ``displayName`` de un rol de directorio: Microsoft Graph
   lo devuelve como null. Por lo tanto, indicar ``displayName`` en ``entraid.permission.fields``
   no aporta nada para un rol de directorio y solo el ID (GUID) del rol se convierte en un
   permiso. Para usar los nombres de rol como valores de permiso, conceda además
   ``RoleManagement.Read.Directory`` (o ``Directory.Read.All``).

.. note::
   |Fess| solicita el ámbito ``https://graph.microsoft.com/.default`` al adquirir un token.
   Desde la versión 15.8, también se envía ``openid profile offline_access https://graph.microsoft.com/.default`` al endpoint de autorización, de modo que el consentimiento se solicita para el mismo conjunto.
   Esto significa que se utilizan todos los permisos de acceso configurados y para los que se ha dado consentimiento en el registro de la aplicación.
   Por lo tanto, para recuperar información de grupos, debe agregar los permisos indicados anteriormente al registro de la aplicación y otorgar el consentimiento del administrador.

Información a obtener
---------------------

La siguiente información se utiliza para la configuración de Fess:

- **ID de aplicación (Cliente)**: En la página Información general, como "ID de aplicación (cliente)"
- **ID del tenant**: En la página Información general, como "ID de directorio (tenant)" o en formato ``xxx.onmicrosoft.com``
- **Valor del secreto del cliente**: El valor creado en Certificados y secretos

Mapeo de grupos y roles
=======================

Con la autenticación de Entra ID, |Fess| recupera automáticamente los grupos y roles a los que pertenece un usuario utilizando la API de Microsoft Graph.
Los IDs de grupo y nombres de grupo recuperados pueden usarse para la búsqueda basada en roles de |Fess|.

Grupos anidados
---------------

|Fess| recupera no solo los grupos a los que los usuarios pertenecen directamente, sino también los grupos padre a los que estos pertenecen (grupos anidados).
Tanto la búsqueda de la pertenencia directa como la búsqueda de grupos padre se ejecutan en la misma tarea en segundo plano después del inicio de sesión, de modo que el inicio de sesión nunca se ve retrasado por Microsoft Graph.
La búsqueda de grupos padre utiliza la operación ``getMemberGroups`` de Microsoft Graph, que resuelve de forma transitiva: una sola llamada por cada grupo asignado directamente devuelve todos los grupos que están por encima de él, sea cual sea la profundidad del anidamiento. Los resultados obtenidos se almacenan en caché durante un período determinado.
Cuando esa tarea en segundo plano finaliza, los permisos del usuario se recalculan.

Configuración de grupos por defecto
-----------------------------------

Para asignar grupos comunes a todos los usuarios de Entra ID:

::

    entraid.default.groups=authenticated_users,entra_users

Ejemplos de configuración
=========================

Configuración mínima (para pruebas)
-----------------------------------

El siguiente es un ejemplo de configuración mínima para verificación en un entorno de pruebas.

::

    # Habilitar SSO
    sso.type=entraid

    # Configuración de Entra ID
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=http://localhost:8080/sso/

Configuración recomendada (para producción)
-------------------------------------------

El siguiente es un ejemplo de configuración recomendada para entornos de producción.

::

    # Habilitar SSO
    sso.type=entraid

    # Configuración de Entra ID
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=https://fess.example.com/sso/

    # Grupos por defecto (opcional)
    entraid.default.groups=authenticated_users

Configuración legacy (compatibilidad con versiones anteriores)
--------------------------------------------------------------

Para compatibilidad con versiones anteriores, también se puede usar el prefijo ``aad.*``.
Cuando cada propiedad ``entraid.*`` no está configurada, se utiliza el valor de la propiedad ``aad.*`` correspondiente.
Además, ``sso.type=aad`` se trata de la misma forma que ``sso.type=entraid``.

::

    # Habilitar SSO (también se puede usar sso.type=aad)
    sso.type=entraid

    # Claves de configuración legacy
    aad.tenant=yourcompany.onmicrosoft.com
    aad.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    aad.client.secret=your-client-secret-value
    aad.reply.url=https://fess.example.com/sso/

Solución de problemas
=====================

Problemas comunes y soluciones
------------------------------

No se puede regresar a Fess después de la autenticación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que la URI de redirección esté configurada correctamente en el registro de aplicaciones del portal Azure
- Asegúrese de que el valor de ``entraid.reply.url`` coincida exactamente con la configuración del portal Azure
- Verifique que el protocolo (HTTP/HTTPS) coincida
- Verifique que la URI de redirección termine con ``/``
- Si ``entraid.response.mode`` está establecido en ``form_post``, verifique tanto que
  ``tomcat.sameSiteCookies = none`` esté configurado como que |Fess| se sirva mediante HTTPS. Con el
  valor por defecto ``lax``, el navegador no envía la cookie de sesión en el POST entre sitios del
  callback; con ``none`` sobre HTTP simple, el navegador no almacena esa cookie en absoluto, porque
  ``none`` exige el atributo ``Secure``. En ambos casos el inicio de sesión falla una sola vez: el
  navegador vuelve a la pantalla de inicio de sesión mostrando "Error en el proceso de inicio de
  sesión SSO." y en el registro se escribe una advertencia con el texto
  ``Failed to process SSO login: could not validate state``

Ocurren errores de autenticación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que el ID del tenant, ID de cliente y secreto del cliente estén configurados correctamente
- Verifique que el secreto del cliente no haya expirado
- Verifique que se haya otorgado el consentimiento del administrador para los permisos de API

No se puede recuperar la información de grupo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que se hayan otorgado los permisos ``User.Read`` y ``GroupMember.Read.All``
  (``GroupMember.Read.All`` puede sustituirse por ``Group.Read.All`` o ``Directory.Read.All``,
  pero ``/me/memberOf`` sigue requiriendo ``User.Read``)
- Verifique que se haya otorgado el consentimiento del administrador
- Verifique que el usuario pertenezca a grupos en Entra ID
- Si no se pueden resolver los grupos padre anidados, se registra la advertencia
  ``Not allowed to read the parent groups of ...``. En ese caso, otorgue ``GroupMember.Read.All``
- |Fess| resuelve la pertenencia a grupos y roles del usuario en segundo plano una vez completado
  el inicio de sesión, de modo que este nunca espera a Microsoft Graph. Hasta que la resolución
  termina, el usuario solo tiene su propio permiso a nivel de usuario y lo que aporten
  ``entraid.default.groups`` y ``entraid.default.roles``. Si no se ha configurado ninguno de los
  dos —el valor por defecto que se incluye—, una búsqueda hecha en esa ventana no devuelve ningún
  documento: ``role.search.default.permissions`` está vacío de fábrica, y una configuración de
  rastreo creada con el valor ``role.search.default.display.permissions`` que se incluye concede
  ``{role}guest``, rol que un usuario con la sesión iniciada no tiene. La ventana dura hasta
  aproximadamente un segundo de retardo de planificación más las propias llamadas a Microsoft
  Graph — una para las pertenencias directas y luego una más por cada uno de esos grupos para
  recorrer los grupos anidados, emitidas una tras otra con la caché fría —, por lo que crece con
  el número de grupos a los que pertenece el usuario. Mientras tanto, la pantalla de búsqueda
  indica al usuario que sus permisos de grupo y rol todavía se están cargando y le pide que
  repita la búsqueda en unos instantes
- Si la resolución no se completa del todo, la pantalla de búsqueda indica al usuario que sus
  permisos de grupo y rol no se pudieron cargar por completo, le pide que cierre la sesión y
  vuelva a iniciarla, y que contacte con el administrador si el problema persiste. Lo de «por
  completo» es deliberado: la resolución solo se considera correcta si han tenido éxito tanto la
  consulta de pertenencias directas como el recorrido de los grupos anidados, así que un usuario
  que tiene sus grupos directos pero no sus grupos padre también recibe ese mensaje. Hay un caso
  exento, y es precisamente el que describe el punto anterior: cuando Microsoft Graph rechaza la
  consulta de grupos anidados con ``Authorization_RequestDenied`` porque nunca se otorgó
  ``GroupMember.Read.All``, |Fess| lo interpreta como una respuesta que significa que el grupo no
  tiene grupos padre, y no como un fallo. La resolución se considera entonces correcta y **no se
  muestra ningún mensaje**, aunque falten los permisos de los grupos padre. La única señal es la
  advertencia ``Not allowed to read the parent groups of ...`` en el registro, así que conviene
  buscarla siempre que se utilicen grupos anidados. La causa
  habitual del caso parcial es la limitación de peticiones: un solo HTTP 429 o 503 de Microsoft
  Graph hace que |Fess| espere el tiempo que pida la cabecera ``Retry-After`` (60 segundos si no
  indica nada utilizable, 60 minutos como máximo), y durante ese tiempo se omite toda consulta de
  grupos anidados en la instancia entera de |Fess| mientras las consultas directas siguen
  respondiendo. El fallo no es necesariamente definitivo:
  la resolución se reintenta cada vez que se renueva el token de acceso, y un éxito posterior hace
  desaparecer el mensaje y restaura los permisos que faltaban. Cerrar la sesión y volver a
  iniciarla lo reintenta de inmediato — abrir la URL de inicio de sesión SSO con la sesión aún
  iniciada solo redirige de vuelta a la pantalla de búsqueda

Configuración de depuración
---------------------------

Para investigar problemas, puede mostrar logs detallados relacionados con Entra ID ajustando el nivel de log de |Fess|.

En ``app/WEB-INF/classes/log4j2.xml``, puede agregar el siguiente logger para cambiar el nivel de log:

::

    <Logger name="org.codelibs.fess.sso.entraid" level="DEBUG"/>

Referencia
==========

- :doc:`security-role` - Configuración de búsqueda basada en roles
- :doc:`sso-saml` - Configuración de SSO con autenticación SAML
- :doc:`sso-oidc` - Configuración de SSO con autenticación OpenID Connect

