==========================================
Configuración de Búsqueda Basada en Roles
==========================================

Acerca de la Búsqueda Basada en Roles
======================================

|Fess| puede filtrar los resultados de búsqueda según la información de autenticación de usuarios autenticados a través de cualquier sistema de autenticación.
Por ejemplo, el usuario A con el rol 'a' verá en los resultados de búsqueda la información asociada al rol 'a', mientras que el usuario B sin el rol 'a' no verá esa información al realizar búsquedas.
Al utilizar esta funcionalidad, es posible implementar búsquedas segmentadas por departamento o cargo del usuario que ha iniciado sesión en entornos de portal o inicio de sesión único (SSO).

|Fess| puede obtener la información de roles desde las siguientes fuentes:

-  Parámetros de solicitud

-  Encabezados de solicitud

-  Cookies

-  Información de autenticación de |Fess|

En portales y sistemas de inicio de sesión único basados en agentes, la información de roles se puede obtener almacenando la información de autenticación mediante cookies para el dominio y ruta donde se ejecuta |Fess| durante la autenticación.
Además, en sistemas de inicio de sesión único basados en proxy inverso, la información de roles se puede obtener agregando la información de autenticación a los parámetros de solicitud o encabezados de solicitud al acceder a |Fess|.

.. note::
    La obtención de roles desde parámetros de solicitud, encabezados de solicitud y cookies está deshabilitada de forma predeterminada.
    Para utilizarlas, es necesario configurar el componente ``roleQueryHelper`` en ``app/WEB-INF/classes/fess.xml`` con los nombres de clave de referencia (``parameterKey``, ``headerKey``, ``cookieKey``), el cifrado de valores (``encryptedParameterValue``, etc.) y los separadores (``valueSeparator``, ``roleSeparator``).
    De forma predeterminada, solo está habilitada la búsqueda basada en roles que utiliza la información de autenticación de |Fess|.

Configuración de Búsqueda Basada en Roles
==========================================

En esta sección se explica cómo configurar la búsqueda basada en roles utilizando la información de autenticación de |Fess|.

Configuración en la Interfaz de Administración de |Fess|
---------------------------------------------------------

Inicie |Fess| e inicie sesión como administrador.
Cree roles y usuarios.
Por ejemplo, cree el rol "Role1" en la pantalla de administración de roles y luego cree un usuario perteneciente a Role1 en la pantalla de administración de usuarios.
Si desea asignar permisos por grupo, cree un grupo en la pantalla de administración de grupos y asígnelo al usuario.

A continuación, en la configuración de rastreo, escriba ``{role}Role1`` en el campo de permisos y guarde.
Para especificar a nivel de usuario puede escribir ``{user}username``, y para especificar a nivel de grupo puede escribir ``{group}groupname``.
Si especifica varios permisos, sepárelos con saltos de línea.

Después de esto, al rastrear con esta configuración de rastreo, se creará un índice en el que solo los usuarios pertenecientes al rol, usuario o grupo especificado podrán realizar búsquedas.
Al usuario que haya iniciado sesión se le asignarán automáticamente los permisos ``{user}username`` (que lo identifica a sí mismo), ``{role}`` (del rol al que pertenece) y ``{group}`` (del grupo al que pertenece), y estos se compararán con los permisos establecidos en los documentos.

.. note::
    Si desea denegar explícitamente el acceso desde un rol, usuario o grupo específico, añada ``(deny)`` como prefijo, por ejemplo ``(deny){role}Role1`` (si se utiliza ``(allow)``, el acceso se permite, lo que equivale a no especificar nada).

.. note::
    Cuando se integra con LDAP o inicio de sesión único, la información de roles y grupos del usuario se obtiene desde el proveedor de autenticación y se trata de igual forma como permisos.
    El comportamiento durante la integración con LDAP puede controlarse mediante ``ldap.role.search.user.enabled``, ``ldap.role.search.group.enabled`` y ``ldap.role.search.role.enabled`` en ``fess_config.properties`` (el valor predeterminado de todos ellos es ``true``).

Inicio de Sesión
----------------

Cierre sesión desde la interfaz de administración.
Inicie sesión con un usuario que pertenezca a Role1.
Si el inicio de sesión es exitoso, será redirigido a la página principal de búsqueda.

Al realizar una búsqueda normal, solo se mostrarán los resultados asociados al rol Role1 en la configuración de rastreo.

Además, las búsquedas realizadas sin haber iniciado sesión se consideran búsquedas realizadas por el usuario guest.
Para los documentos que desea mostrar a usuarios no autenticados, establezca ``{role}guest`` en el campo de permisos de la configuración de rastreo (el valor predeterminado se define mediante ``role.search.guest.permissions``).

Cierre de Sesión
----------------

Al iniciar sesión con un usuario que no sea administrador, puede cerrar sesión seleccionando la opción de cierre de sesión en la pantalla de búsqueda.
