==================
Autenticación Web
==================

Descripción general
===================

Aquí se explica el método de configuración cuando se requiere autenticación web para el rastreo dirigido a la web.
|Fess| admite el rastreo de autenticación BASIC, autenticación DIGEST, autenticación NTLM y autenticación FORM.

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

.. warning::

   Si se omite el nombre de host, el nombre de usuario y la contraseña también se envían a otros hosts a los que el rastreo llega mediante enlaces o redirecciones.
   Especifique el nombre de host para que las credenciales no se envíen a hosts no deseados.

Puerto
::::::

Especifique el puerto del sitio que requiere autenticación.
Si desea aplicarlo a todos los puertos, deje el campo vacío. No se puede especificar ``-1``; solo se admiten valores de 0 o más.
En ese caso, se aplicará con cualquier puerto en la configuración de rastreo web especificada.

Dominio
:::::::

Especifique el nombre de dominio del sitio que requiere autenticación.
Si se omite, se aplicará con cualquier nombre de dominio en la configuración de rastreo web especificada.
Este campo corresponde al realm. En la autenticación BASIC y DIGEST, el realm se compara con el que devuelve el servidor, distinguiendo mayúsculas y minúsculas. Si no coinciden, no se envían las credenciales.
El desafío NTLM no incluye un realm, por lo que este campo no se utiliza en la autenticación NTLM (la autenticación tiene éxito aunque se especifique un realm incorrecto).

Esquema
:::::::

Seleccione el método de autenticación.
Puede utilizar autenticación BASIC, autenticación DIGEST, autenticación NTLM o autenticación FORM.

.. note::

   El esquema BASIC, DIGEST o NTLM no limita el método de autenticación que puede solicitar el servidor.
   |Fess| envía las credenciales con el método que solicita el servidor.
   Por ejemplo, una entrada guardada como DIGEST se envía con BASIC si el servidor solo solicita BASIC (por HTTP las credenciales viajan entonces prácticamente en texto claro).
   Una entrada guardada como BASIC responde con DIGEST si el servidor solicita DIGEST.
   NTLM y BASIC/DIGEST no se pueden sustituir entre sí.
   Si selecciona un esquema que el servidor no utiliza, no se envían credenciales y no se indexan los documentos del sitio.
   Seleccione el método de autenticación que utiliza el servidor y, si es posible, utilice HTTPS.

Nombre de usuario
:::::::::::::::::

Especifique el nombre de usuario para iniciar sesión en el sitio de autenticación.
Si la autenticación NTLM requiere un dominio, no escriba el nombre de usuario con el formato ``DOMINIO\usuario``; especifique el dominio con el parámetro ``domain`` que se describe más abajo.
Un valor como ``DOMINIO\usuario`` no se divide: la cadena completa se envía como nombre de usuario con el dominio vacío.

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

``domain``
    El dominio en el que se autentica. Especifíquelo cuando se autentique con una cuenta de dominio.
    Si se omite, el dominio se envía vacío y la autenticación de una cuenta de dominio falla.
    Un dominio escrito en minúsculas se convierte a mayúsculas antes de enviarse.

``workstation``
    El nombre de estación de trabajo que se envía en los mensajes NTLM.
    Si se omite, se envía el nombre de host de la máquina en la que se ejecuta |Fess|.

Configuración web
:::::::::::::::::

Seleccione el nombre de configuración web al que se aplicará la configuración de autenticación anterior.
Es necesario registrar la configuración de rastreo web de antemano.

Cuando falla la autenticación
-----------------------------

Si las credenciales son incorrectas, o el nombre de host, el puerto o el realm no coinciden con el sitio y por ello no se envían credenciales, el servidor devuelve 401 (Unauthorized) y no se indexan los documentos del sitio.
Un 401 se registra como URL de fallo, por lo que puede comprobarlo en :doc:`failureurl-guide`.
Los códigos de estado HTTP que se registran como URL de fallo se pueden cambiar con ``crawler.failure.url.status.codes`` (:doc:`../config/crawler-advanced`).
Tenga en cuenta que un 401 no elimina los documentos que ya están en el índice.

Eliminar configuración
----------------------

Haga clic en el nombre de la configuración en la página de lista y haga clic en el botón de eliminar para que aparezca una pantalla de confirmación.
Al presionar el botón de eliminar, se eliminará la configuración.

.. |image0| image:: ../../../resources/images/en/15.10/admin/webauth-1.png
.. |image1| image:: ../../../resources/images/en/15.10/admin/webauth-2.png
