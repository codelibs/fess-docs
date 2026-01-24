==================
Autenticación Web
==================

Descripción general
===================

Aquí se explica el método de configuración cuando se requiere autenticación web para el rastreo dirigido a la web.
|Fess| admite el rastreo de autenticación BASIC, autenticación DIGEST y autenticación NTLM.

Método de gestión
==================

Método de visualización
-----------------------

Para abrir la página de lista de configuración de autenticación web que se muestra a continuación, haga clic en [Rastreador > Autenticación web] en el menú izquierdo.

|image0|

Para editar, haga clic en el nombre de la configuración.

Crear configuración
-------------------

Para abrir la página de configuración de autenticación web, haga clic en el botón de nueva creación.

|image1|

Parámetros de configuración
----------------------------

Nombre de host
::::::::::::::

Especifique el nombre de host del sitio que requiere autenticación.
Si se omite, se aplicará con cualquier nombre de host en la configuración de rastreo web especificada.

Puerto
::::::

Especifique el puerto del sitio que requiere autenticación.
Si desea aplicarlo a todos los puertos, especifique -1.
En ese caso, se aplicará con cualquier puerto en la configuración de rastreo web especificada.

Dominio
:::::::

Especifique el nombre de dominio del sitio que requiere autenticación.
Si se omite, se aplicará con cualquier nombre de dominio en la configuración de rastreo web especificada.

Esquema
:::::::

Seleccione el método de autenticación.
Puede utilizar autenticación BASIC, autenticación DIGEST, autenticación NTLM o autenticación FORM.

Nombre de usuario
:::::::::::::::::

Especifique el nombre de usuario para iniciar sesión en el sitio de autenticación.

Contraseña
::::::::::

Especifique la contraseña para iniciar sesión en el sitio de autenticación.

Parámetros
::::::::::

Configure si hay valores de configuración necesarios para iniciar sesión en el sitio de autenticación.
Para la autenticación NTLM, puede configurar los valores de workstation y domain.
Si desea configurarlos, descríbalos de la siguiente manera:

::

    workstation=HOGE
    domain=FUGA

Configuración web
:::::::::::::::::

Seleccione el nombre de configuración web al que se aplicará la configuración de autenticación anterior.
Es necesario registrar la configuración de rastreo web de antemano.

Eliminar configuración
----------------------

Haga clic en el nombre de la configuración en la página de lista y haga clic en el botón de eliminar para que aparezca una pantalla de confirmación.
Al presionar el botón de eliminar, se eliminará la configuración.

.. |image0| image:: ../../../resources/images/en/15.5/admin/webauth-1.png
.. |image1| image:: ../../../resources/images/en/15.5/admin/webauth-2.png
