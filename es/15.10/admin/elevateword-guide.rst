==================
Palabra Adicional
==================

Descripción general
===================

Aquí se explica la configuración de candidatos de palabras adicionales para sugerencias. Las sugerencias se muestran según el término de búsqueda, pero puede agregar esas palabras.

Método de gestión
==================

Método de visualización
-----------------------

Para abrir la página de lista para configurar palabras adicionales que se muestra a continuación, haga clic en [Sugerir > Palabra elevada] en el menú izquierdo.

|image0|

Para editar, haga clic en el nombre de la configuración.

Crear configuración
-------------------

Para abrir la página de configuración de palabra adicional, haga clic en el botón de nueva creación.

|image1|

Parámetros de configuración
----------------------------

Palabra
:::::::

Especifique la palabra que se mostrará como candidata de sugerencia.

Lectura
:::::::

Especifique la lectura de la palabra candidata de sugerencia.

Permisos
::::::::

Configure la información de rol para la palabra.
La sugerencia solo se mostrará a los usuarios que tengan el rol configurado.
La especificación por usuario es {user}nombre_usuario, la especificación por rol es {role}nombre_rol, y la especificación por grupo es {group}nombre_grupo.

Etiqueta
::::::::

Configure la etiqueta para la palabra.
Si se selecciona una etiqueta diferente a la configurada, no se mostrará en la sugerencia.

Valor de impulso
::::::::::::::::

Configure el valor de impulso para la palabra.

.. note::
   Las palabras que registre, edite o elimine (incluida la carga de un archivo CSV) no se aplican de inmediato a las sugerencias. Se aplican cuando se ejecuta el trabajo "Suggest Indexer", que reconstruye el índice de sugerencias (por defecto se ejecuta todos los días a las 12:00). Para aplicarlas de inmediato, haga clic en "Suggest Indexer" en [Sistema > Programador] y luego haga clic en el botón "Iniciar ahora".

Eliminar configuración
----------------------

Haga clic en el nombre de la configuración en la página de lista y haga clic en el botón de eliminar para que aparezca una pantalla de confirmación.
Al presionar el botón de eliminar, se eliminará la configuración.


Descarga
========

Descarga las palabras registradas en formato CSV.

|image2|

Contenido del CSV
-----------------

La primera línea es el encabezado.
Desde la segunda línea en adelante se describen las palabras adicionales.

::

"SuggestWord","Reading","Permissions","Labels","Boost"
"fess","ふぇす","{role}role1","label1","100"

Carga
=====

Registra palabras en formato CSV.

|image3|

Contenido del CSV
-----------------

La primera línea es el encabezado.
Desde la segunda línea en adelante se describen las palabras adicionales.

::

"SuggestWord","Reading","Permissions","Labels","Boost"
"fess","ふぇす","{role}role1","label1","100"

.. note::
   En la columna Permissions, especifique cada valor con ``{role}``, ``{user}`` o ``{group}``, como ``{role}role1`` (separe varios valores con comas). Un valor sin prefijo, como ``role1``, no se trata como un rol y la palabra no se sugiere a los usuarios que tienen ese rol.


.. |image0| image:: ../../../resources/images/en/15.10/admin/elevateword-1.png
.. |image1| image:: ../../../resources/images/en/15.10/admin/elevateword-2.png
.. |image2| image:: ../../../resources/images/en/15.10/admin/elevateword-3.png
.. |image3| image:: ../../../resources/images/en/15.10/admin/elevateword-4.png
