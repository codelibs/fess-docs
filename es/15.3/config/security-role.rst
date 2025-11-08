=================================
Configuración de Búsqueda Basada en Roles
=================================

Acerca de la Búsqueda Basada en Roles
==================

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

Configuración de Búsqueda Basada en Roles
=================

En esta sección se explica cómo configurar la búsqueda basada en roles utilizando la información de autenticación de |Fess|.

Configuración en la Interfaz de Administración de |Fess|
---------------------

Inicie |Fess| e inicie sesión como administrador.
Cree roles y usuarios.
Por ejemplo, cree el rol "Role1" en la pantalla de administración de roles y luego cree un usuario perteneciente a Role1 en la pantalla de administración de usuarios.
A continuación, en la configuración de rastreo, escriba {role}Role1 en el campo de permisos y guarde.
Para especificar a nivel de usuario, puede escribir {user}nombre_usuario, y para especificar a nivel de grupo, puede escribir {group}nombre_grupo.
Después de esto, al rastrear con esta configuración de rastreo, se creará un índice que solo será accesible mediante búsquedas por el usuario creado.

Inicio de Sesión
------

Cierre sesión desde la interfaz de administración.
Inicie sesión con un usuario que pertenezca a Role1.
Si el inicio de sesión es exitoso, será redirigido a la página principal de búsqueda.

Al realizar una búsqueda normal, solo se mostrarán los resultados asociados con la configuración del rol Role1 en la configuración de rastreo.

Además, las búsquedas realizadas sin haber iniciado sesión se consideran búsquedas realizadas por el usuario "guest".

Cierre de Sesión
--------

Al iniciar sesión con un usuario que no sea administrador, puede cerrar sesión seleccionando la opción de cierre de sesión en la pantalla de búsqueda.

