===================
Búsqueda por roles
===================

|Fess| ofrece una función de gestión de usuarios que permite a los usuarios que han iniciado sesión realizar búsquedas en función de los roles a los que pertenecen. Los usuarios administrados por |Fess| pueden, tras iniciar sesión, utilizar la búsqueda por roles y cambiar su propia contraseña.

En la búsqueda por roles, se comparan los permisos configurados en el contenido (rol, grupo, usuario) con los permisos que posee el usuario que realiza la búsqueda, y en los resultados de búsqueda solo se muestran los contenidos cuyo acceso está permitido. Para obtener información sobre cómo crear roles y usuarios, así como sobre cómo asignar permisos al contenido, y en general sobre la configuración de la búsqueda basada en roles, consulte :doc:`../config/security-role`.


Método de búsqueda
-------------------

Si se han configurado roles y el contenido se ha rastreado e indexado en ese estado, los resultados de búsqueda se pueden mostrar únicamente a los usuarios que posean ese rol.
Si el usuario ha iniciado sesión, la búsqueda se realiza en función de los roles y grupos a los que pertenece.
Si no ha iniciado sesión, la búsqueda se realiza como usuario guest, y solo se muestran los contenidos publicados para guest.

Inicio de sesión
-----------------

Al hacer clic en el enlace de «Iniciar sesión» que aparece en la parte superior de la pantalla de búsqueda, se muestra la pantalla de inicio de sesión. Al introducir el nombre de usuario y la contraseña e iniciar sesión, se vuelve a la pantalla de búsqueda, y a partir de ese momento las búsquedas se realizan en función de los roles a los que pertenece ese usuario.

.. note::
    Si se ha integrado con el inicio de sesión único (SSO) o con LDAP, el inicio de sesión se realiza mediante el método de autenticación correspondiente. Además, la visibilidad del enlace de inicio de sesión se puede modificar mediante la configuración.

Cambio de contraseña
----------------------

Después de iniciar sesión, al hacer clic en el nombre de usuario que aparece en la parte superior de la pantalla de búsqueda, se muestra un menú.

|image0|

Al hacer clic en «Cambiar contraseña» dentro del menú, se muestra la pantalla de cambio de contraseña.

|image1|

Introduzca la contraseña actual, la nueva contraseña y la confirmación de la nueva contraseña (reintroducida), y haga clic en el botón «Actualizar» para actualizar la contraseña.
Después de cambiar la contraseña, puede volver a la pantalla de búsqueda haciendo clic en el botón «Volver».

.. note::
    El menú «Cambiar contraseña» solo se muestra para los usuarios administrados por |Fess| (y para los usuarios LDAP a los que se les ha permitido editar). No se muestra para los usuarios autenticados mediante inicio de sesión único.
    Es posible que la nueva contraseña deba cumplir una política de contraseñas, como la longitud o los tipos de caracteres permitidos.

Cerrar sesión
--------------

Estando conectado, puede cerrar sesión haciendo clic en el nombre de usuario que aparece en la parte superior de la pantalla de búsqueda y seleccionando «Cerrar sesión» en el menú.
Si el usuario tiene privilegios de administrador, también puede ir a la pantalla de administración seleccionando «Administración» en el mismo menú.



.. |image0| image:: ../../../resources/images/en/15.8/user/role-search-1.png
.. pdf   :width: 200 px
.. |image1| image:: ../../../resources/images/en/15.8/user/role-search-2.png
.. pdf   :width: 300 px
