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
6. |Fess| utiliza la API de Microsoft Graph para recuperar la información de grupo y rol del usuario
7. El usuario inicia sesión y la información de grupo se aplica a la búsqueda basada en roles

Para la integración con la búsqueda basada en roles, consulte :doc:`security-role`.

Prerrequisitos
==============

Antes de configurar la autenticación de Entra ID, verifique los siguientes prerrequisitos:

- |Fess| 15.4 o superior está instalado
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
   * - ``entraid.default.groups``
     - Grupos por defecto (separados por comas)
     - (Ninguno)
   * - ``entraid.default.roles``
     - Roles por defecto (separados por comas)
     - (Ninguno)

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

   - ``Group.Read.All`` - Requerido para recuperar la información de grupo del usuario

6. Haga clic en **Agregar permisos**

7. Haga clic en **Conceder consentimiento de administrador para <nombre del tenant>**

.. note::
   El consentimiento del administrador requiere privilegios de administrador del tenant.

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

|Fess| recupera no solo los grupos a los que los usuarios pertenecen directamente, sino también los grupos padre (grupos anidados) de forma recursiva.
Este procesamiento se ejecuta de forma asíncrona después del inicio de sesión para minimizar el impacto en el tiempo de inicio de sesión.

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

::

    # Habilitar SSO
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

Ocurren errores de autenticación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que el ID del tenant, ID de cliente y secreto del cliente estén configurados correctamente
- Verifique que el secreto del cliente no haya expirado
- Verifique que se haya otorgado el consentimiento del administrador para los permisos de API

No se puede recuperar la información de grupo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que se haya otorgado el permiso ``Group.Read.All``
- Verifique que se haya otorgado el consentimiento del administrador
- Verifique que el usuario pertenezca a grupos en Entra ID

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

