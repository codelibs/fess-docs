==================
Host Duplicado
==================

Descripción general
===================

Aquí se explica la configuración relacionada con los hosts duplicados.
Los hosts duplicados se utilizan cuando desea tratar diferentes nombres de host como iguales durante el rastreo.
Por ejemplo, se puede utilizar cuando desea tratar www.example.com y example.com como el mismo sitio.

Método de gestión
==================

Método de visualización
-----------------------

Para abrir la página de lista para configurar hosts duplicados que se muestra a continuación, haga clic en [Rastreador > Host duplicado] en el menú izquierdo.

|image0|

Para editar, haga clic en el nombre de la configuración.

Crear configuración
-------------------

Para abrir la página de configuración de host duplicado, haga clic en el botón de nueva creación.

|image1|

Parámetros de configuración
----------------------------

Nombre regular
::::::::::::::

Especifique el nombre de host regular. Los nombres de host duplicados se reemplazan con el nombre de host regular.

Nombre duplicado
::::::::::::::::

Especifique el nombre de host duplicado. Especifique el nombre de host que desea reemplazar.

.. note::

   Una URL cuyo nombre de host coincide con un nombre duplicado se sustituye por la URL del nombre regular antes del rastreo. Esto se aplica tanto a las URL escritas en "URLs" (las URL iniciales) de la configuración de rastreo como a las URL de los enlaces encontrados durante el rastreo.
   Por ello, "URLs a incluir en el rastreo" y "URLs a excluir del rastreo" de la configuración de rastreo se evalúan sobre la URL ya sustituida. Escríbalas con el nombre de host del nombre regular.

   Por ejemplo, si el nombre regular es ``example.com`` y el nombre duplicado es ``www.example.com``, escribir solo ``https://www.example.com/.*`` en "URLs a incluir en el rastreo" deja fuera la URL inicial tras la sustitución (``https://example.com/``).
   En ese caso no se registra ningún documento en el índice y no se genera ni un error ni un mensaje de registro.

Eliminar configuración
----------------------

Haga clic en el nombre de la configuración en la página de lista y haga clic en el botón de eliminar para que aparezca una pantalla de confirmación.
Al presionar el botón de eliminar, se eliminará la configuración.

.. |image0| image:: ../../../resources/images/en/15.10/admin/duplicatehost-1.png
.. |image1| image:: ../../../resources/images/en/15.10/admin/duplicatehost-2.png
