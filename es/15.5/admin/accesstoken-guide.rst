====================
Token de Acceso
====================

Descripción general
===================

La página de configuración de tokens de acceso gestiona los tokens de acceso.

Método de gestión
==================

Método de visualización
-----------------------

Para abrir la página de lista de configuración de tokens de acceso que se muestra a continuación, haga clic en [Sistema > Token de acceso] en el menú izquierdo.

|image0|

Para editar, haga clic en el nombre de la configuración.

Crear configuración
-------------------

Para abrir la página de configuración de token de acceso, haga clic en el botón de nueva creación.

|image1|

Parámetros de configuración
----------------------------

Nombre
::::::

Especifique un nombre para describir este token de acceso.

Permisos
::::::::

Configure los permisos del token de acceso.
Descríbalo en el formato "{user|group|role}nombre".
Por ejemplo, para que los usuarios que pertenecen al grupo developer vean los resultados de búsqueda, configure el permiso como "{group}developer".

Nombre del parámetro
::::::::::::::::::::

Especifique el nombre del parámetro de solicitud al especificar permisos como consulta de búsqueda.

.. warning::

   La funcionalidad de nombre de parámetro está diseñada únicamente para su uso en entornos internos de confianza.
   Cuando esta funcionalidad está habilitada, se pueden especificar permisos adicionales a través de parámetros de URL.
   Sin embargo, en entornos accesibles externamente o cuando se expone como una API pública,
   usuarios malintencionados pueden manipular los parámetros de URL para escalar a privilegios que no deberían tener.

   Tenga en cuenta lo siguiente:

   * Use esta funcionalidad solo cuando Fess esté integrado dentro de otra aplicación o servicio que controle completamente las solicitudes entrantes.
   * No configure un nombre de parámetro cuando Fess esté expuesto a redes no confiables.
   * Asegúrese de que los parámetros de URL no puedan ser manipulados por usuarios externos al usar tokens de acceso.

Fecha de vencimiento
::::::::::::::::::::

Especifique la fecha de vencimiento del token de acceso.

Eliminar configuración
----------------------

Haga clic en el nombre de la configuración en la página de lista y haga clic en el botón de eliminar para que aparezca una pantalla de confirmación.
Al presionar el botón de eliminar, se eliminará la configuración.



.. |image0| image:: ../../../resources/images/en/15.5/admin/accesstoken-1.png
.. |image1| image:: ../../../resources/images/en/15.5/admin/accesstoken-2.png
