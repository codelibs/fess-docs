==========================================
Configuracion de SSO con Entra ID
==========================================

Descripcion general
===================

|Fess| soporta autenticacion Single Sign-On (SSO) utilizando Microsoft Entra ID (anteriormente Azure AD).
Al utilizar la autenticacion de Entra ID, puede integrar la informacion de usuario y la informacion de grupo de su entorno Microsoft 365 con la busqueda basada en roles de |Fess|.

Como funciona la autenticacion de Entra ID
------------------------------------------

En la autenticacion de Entra ID, |Fess| opera como un cliente OAuth 2.0/OpenID Connect y colabora con Microsoft Entra ID para la autenticacion.

1. El usuario accede al endpoint SSO de |Fess| (``/sso/``)
2. |Fess| redirige al endpoint de autorizacion de Entra ID
3. El usuario se autentica con Entra ID (inicio de sesion de Microsoft)
4. Entra ID redirige el codigo de autorizacion a |Fess|
5. |Fess| utiliza el codigo de autorizacion para obtener un token de acceso
6. |Fess| utiliza la API de Microsoft Graph para recuperar la informacion de grupo y rol del usuario
7. El usuario inicia sesion y la informacion de grupo se aplica a la busqueda basada en roles

Para la integracion con la busqueda basada en roles, consulte :doc:`security-role`.

Prerrequisitos
==============

Antes de configurar la autenticacion de Entra ID, verifique los siguientes prerrequisitos:

- |Fess| 15.4 o superior esta instalado
- Un tenant de Microsoft Entra ID (Azure AD) esta disponible
- |Fess| es accesible a traves de HTTPS (requerido para entornos de produccion)
- Tiene permiso para registrar aplicaciones en Entra ID

Configuracion basica
====================

Habilitar SSO
-------------

Para habilitar la autenticacion de Entra ID, agregue la siguiente configuracion en ``app/WEB-INF/conf/system.properties``:

::

    sso.type=entraid

Configuracion requerida
-----------------------

Configure la informacion obtenida de Entra ID.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Por defecto
   * - ``entraid.tenant``
     - ID del tenant (ej: ``xxx.onmicrosoft.com``)
     - (Requerido)
   * - ``entraid.client.id``
     - ID de aplicacion (Cliente)
     - (Requerido)
   * - ``entraid.client.secret``
     - Valor del secreto del cliente
     - (Requerido)
   * - ``entraid.reply.url``
     - URI de redireccion (URL de callback)
     - Usa la URL de la solicitud

.. note::
   En lugar del prefijo ``entraid.*``, tambien puede usar el prefijo legacy ``aad.*`` para compatibilidad con versiones anteriores.

Configuracion opcional
----------------------

Las siguientes configuraciones pueden agregarse segun sea necesario.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propiedad
     - Descripcion
     - Por defecto
   * - ``entraid.authority``
     - URL del servidor de autenticacion
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

Configuracion del lado de Entra ID
==================================

Registro de aplicacion en Azure Portal
--------------------------------------

1. Inicie sesion en `Azure Portal <https://portal.azure.com/>`_

2. Seleccione **Microsoft Entra ID**

3. Vaya a **Administrar** → **Registros de aplicaciones** → **Nuevo registro**

4. Registre la aplicacion:

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - Configuracion
        - Valor
      * - Nombre
        - Cualquier nombre (ej: Fess SSO)
      * - Tipos de cuenta compatibles
        - "Solo cuentas en este directorio organizativo"
      * - Plataforma
        - Web
      * - URI de redireccion
        - ``https://<host de Fess>/sso/``

5. Haga clic en **Registrar**

Crear un secreto de cliente
---------------------------

1. En la pagina de detalles de la aplicacion, haga clic en **Certificados y secretos**

2. Haga clic en **Nuevo secreto de cliente**

3. Establezca una descripcion y una fecha de expiracion, luego haga clic en **Agregar**

4. Copie y guarde el **Valor** generado (este valor no se mostrara nuevamente)

.. warning::
   El valor del secreto del cliente solo se muestra inmediatamente despues de la creacion.
   Asegurese de registrarlo antes de salir de la pagina.

Configurar permisos de API
--------------------------

1. Haga clic en **Permisos de API** en el menu izquierdo

2. Haga clic en **Agregar un permiso**

3. Seleccione **Microsoft Graph**

4. Seleccione **Permisos delegados**

5. Agregue el siguiente permiso:

   - ``Group.Read.All`` - Requerido para recuperar la informacion de grupo del usuario

6. Haga clic en **Agregar permisos**

7. Haga clic en **Conceder consentimiento de administrador para <nombre del tenant>**

.. note::
   El consentimiento del administrador requiere privilegios de administrador del tenant.

Informacion a obtener
---------------------

La siguiente informacion se utiliza para la configuracion de Fess:

- **ID de aplicacion (Cliente)**: En la pagina Informacion general, como "ID de aplicacion (cliente)"
- **ID del tenant**: En la pagina Informacion general, como "ID de directorio (tenant)" o en formato ``xxx.onmicrosoft.com``
- **Valor del secreto del cliente**: El valor creado en Certificados y secretos

Mapeo de grupos y roles
=======================

Con la autenticacion de Entra ID, |Fess| recupera automaticamente los grupos y roles a los que pertenece un usuario utilizando la API de Microsoft Graph.
Los IDs de grupo y nombres de grupo recuperados pueden usarse para la busqueda basada en roles de |Fess|.

Grupos anidados
---------------

|Fess| recupera no solo los grupos a los que los usuarios pertenecen directamente, sino tambien los grupos padre (grupos anidados) de forma recursiva.
Este procesamiento se ejecuta de forma asincrona despues del inicio de sesion para minimizar el impacto en el tiempo de inicio de sesion.

Configuracion de grupos por defecto
-----------------------------------

Para asignar grupos comunes a todos los usuarios de Entra ID:

::

    entraid.default.groups=authenticated_users,entra_users

Ejemplos de configuracion
=========================

Configuracion minima (para pruebas)
-----------------------------------

El siguiente es un ejemplo de configuracion minima para verificacion en un entorno de pruebas.

::

    # Habilitar SSO
    sso.type=entraid

    # Configuracion de Entra ID
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=http://localhost:8080/sso/

Configuracion recomendada (para produccion)
-------------------------------------------

El siguiente es un ejemplo de configuracion recomendada para entornos de produccion.

::

    # Habilitar SSO
    sso.type=entraid

    # Configuracion de Entra ID
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=https://fess.example.com/sso/

    # Grupos por defecto (opcional)
    entraid.default.groups=authenticated_users

Configuracion legacy (compatibilidad con versiones anteriores)
--------------------------------------------------------------

Para compatibilidad con versiones anteriores, tambien se puede usar el prefijo ``aad.*``.

::

    # Habilitar SSO
    sso.type=entraid

    # Claves de configuracion legacy
    aad.tenant=yourcompany.onmicrosoft.com
    aad.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    aad.client.secret=your-client-secret-value
    aad.reply.url=https://fess.example.com/sso/

Solucion de problemas
=====================

Problemas comunes y soluciones
------------------------------

No se puede regresar a Fess despues de la autenticacion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que la URI de redireccion este configurada correctamente en el registro de aplicaciones del portal Azure
- Asegurese de que el valor de ``entraid.reply.url`` coincida exactamente con la configuracion del portal Azure
- Verifique que el protocolo (HTTP/HTTPS) coincida
- Verifique que la URI de redireccion termine con ``/``

Ocurren errores de autenticacion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que el ID del tenant, ID de cliente y secreto del cliente esten configurados correctamente
- Verifique que el secreto del cliente no haya expirado
- Verifique que se haya otorgado el consentimiento del administrador para los permisos de API

No se puede recuperar la informacion de grupo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verifique que se haya otorgado el permiso ``Group.Read.All``
- Verifique que se haya otorgado el consentimiento del administrador
- Verifique que el usuario pertenezca a grupos en Entra ID

Configuracion de depuracion
---------------------------

Para investigar problemas, puede mostrar logs detallados relacionados con Entra ID ajustando el nivel de log de |Fess|.

En ``app/WEB-INF/classes/log4j2.xml``, puede agregar el siguiente logger para cambiar el nivel de log:

::

    <Logger name="org.codelibs.fess.sso.entraid" level="DEBUG"/>

Referencia
==========

- :doc:`security-role` - Configuracion de busqueda basada en roles
- :doc:`sso-saml` - Configuracion de SSO con autenticacion SAML
- :doc:`sso-oidc` - Configuracion de SSO con autenticacion OpenID Connect
